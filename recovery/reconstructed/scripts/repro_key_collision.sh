#!/bin/bash
# Isolated comparison: original jar and behavior-equivalent build collide on a
# sparse primary key and sleep; the patched build seeds from max(c1)+1 and finishes.
# Requires a local MySQL-compatible server. Defaults match the MariaDB used in evidence.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
EQUIV="$ROOT/reconstructed"
SOCK="${WLM_SOCKET:-/tmp/wlm-mariadb.sock}"
PORT="${WLM_PORT:-3307}"
USER_NAME="${WLM_USER:-tpccapp}"
PASS="${WLM_PASSWORD:?set WLM_PASSWORD}"
DB="${WLM_DB:-tpcc}"
CP="$EQUIV/lib-mysql-connector.jar"
OUT="${WLM_OUT:-/tmp/wlm-repro}"
mkdir -p "$OUT"

mysql_admin() {
  if [ "$(id -u)" -eq 0 ]; then
    mariadb --socket="$SOCK" -e "$1"
  else
    sudo mariadb --socket="$SOCK" -e "$1"
  fi
}

reset_sparse() {
  mysql_admin "DROP TABLE IF EXISTS ${DB}.test_1;
CREATE TABLE ${DB}.test_1 (
  c1 int NOT NULL,
  c2 int,
  c3 varchar(100),
  c4 char(100),
  c5 datetime(6),
  PRIMARY KEY (c1)
);
INSERT INTO ${DB}.test_1 (c1,c2,c3,c4,c5) VALUES (50,50,'b','c',NOW(6));"
}

reset_empty() {
  mysql_admin "DROP TABLE IF EXISTS ${DB}.test_1;"
}

write_props() {
  local tps="$1"
  local loops="${2:-20}"
  cat > "$OUT/application.properties" <<EOF
dbtype=MySQL
log=
tpslog=${tps}
thread=1
loop=${loops}
rate=1,0,0,0
buffer=100
url=jdbc:mysql://127.0.0.1:${PORT}/${DB}?useSSL=false&serverTimezone=UTC&characterEncoding=UTF-8&useUnicode=yes
username=${USER_NAME}
password=${PASS}
tablename=test
tablespace=
tablenum=1
sql=
EOF
}

run_class() {
  local classes="$1"
  local log="$2"
  local tps="$3"
  local loops="${4:-20}"
  write_props "$tps" "$loops"
  local start end
  start="$(date +%s.%N)"
  set +e
  timeout 18 java -cp "$classes:$CP" com.cmbcdba.WorkLoadManager1 "$OUT/application.properties" \
    >"$log" 2>&1
  local rc=$?
  set -e
  end="$(date +%s.%N)"
  python3 -c 'import sys; print("elapsed_sec %.3f" % (float(sys.argv[2]) - float(sys.argv[1]))); print("exit %s" % sys.argv[3])' \
    "$start" "$end" "$rc" | tee "$log.time"
}

echo "== build equivalent =="
"$EQUIV/build.sh" "$OUT/equiv-classes"

echo "== build fix in a copy =="
rm -rf "$OUT/fix-tree"
mkdir -p "$OUT/fix-tree"
cp -a "$EQUIV/src" "$EQUIV/lib-mysql-connector.jar" "$EQUIV/build.sh" "$OUT/fix-tree/"
( cd "$OUT/fix-tree" && patch -p1 < "$ROOT/fix/wlm-perf-fix.patch" )
"$OUT/fix-tree/build.sh" "$OUT/fix-classes"

echo "== empty table, both should insert c1 0..19 =="
reset_empty
run_class "$OUT/equiv-classes" "$OUT/empty-equiv.log" "$OUT/empty-equiv.tps"
mysql_admin "SELECT COUNT(*) AS c, MIN(c1) AS mn, MAX(c1) AS mx FROM ${DB}.test_1;" | tee "$OUT/empty-equiv.sql"
reset_empty
run_class "$OUT/fix-classes" "$OUT/empty-fix.log" "$OUT/empty-fix.tps"
mysql_admin "SELECT COUNT(*) AS c, MIN(c1) AS mn, MAX(c1) AS mx FROM ${DB}.test_1;" | tee "$OUT/empty-fix.sql"

echo "== sparse c1=50, original jar and equivalent collide; fix continues at 51 =="
reset_sparse
JAR="$ROOT/evidence/materials/wlm/WorkLoadManagerNew-jar-with-dependencies.jar"
write_props "$OUT/sparse-jar.tps" 60
start="$(date +%s.%N)"
set +e
timeout 18 java -jar "$JAR" "$OUT/application.properties" >"$OUT/sparse-jar.log" 2>&1
rc=$?
set -e
end="$(date +%s.%N)"
python3 -c 'import sys; print("elapsed_sec %.3f" % (float(sys.argv[2]) - float(sys.argv[1]))); print("exit %s" % sys.argv[3])' \
  "$start" "$end" "$rc" | tee "$OUT/sparse-jar.log.time"
mysql_admin "SELECT COUNT(*) AS c, MIN(c1) AS mn, MAX(c1) AS mx FROM ${DB}.test_1;" | tee "$OUT/sparse-jar.sql"
reset_sparse
run_class "$OUT/equiv-classes" "$OUT/sparse-equiv.log" "$OUT/sparse-equiv.tps" 60
mysql_admin "SELECT COUNT(*) AS c, MIN(c1) AS mn, MAX(c1) AS mx FROM ${DB}.test_1;" | tee "$OUT/sparse-equiv.sql"
reset_sparse
run_class "$OUT/fix-classes" "$OUT/sparse-fix.log" "$OUT/sparse-fix.tps" 60
mysql_admin "SELECT COUNT(*) AS c, MIN(c1) AS mn, MAX(c1) AS mx FROM ${DB}.test_1;" | tee "$OUT/sparse-fix.sql"

echo "== select smoke on the fixed table =="
cat > "$OUT/application.properties" <<EOF
dbtype=MySQL
log=
tpslog=$OUT/select-fix.tps
thread=1
loop=5
rate=0,0,0,1
buffer=100
url=jdbc:mysql://127.0.0.1:${PORT}/${DB}?useSSL=false&serverTimezone=UTC&characterEncoding=UTF-8&useUnicode=yes
username=${USER_NAME}
password=${PASS}
tablename=test
tablespace=
tablenum=1
sql=
EOF
timeout 15 java -cp "$OUT/fix-classes:$CP" com.cmbcdba.WorkLoadManager1 "$OUT/application.properties" >"$OUT/select-fix.log" 2>&1 || true

python3 - << PY
from pathlib import Path
out = Path("$OUT")
def elapsed(name):
    text = (out/name).read_text(errors="replace")
    for line in text.splitlines():
        if line.startswith("elapsed_sec"):
            return line.split()[-1]
    return "missing"
def has(name, needle):
    return needle in (out/name).read_text(errors="replace")
report = []
report.append(f"empty_equiv_elapsed {elapsed('empty-equiv.log.time')} duplicate {has('empty-equiv.log','Duplicate entry')}")
report.append(f"empty_fix_elapsed {elapsed('empty-fix.log.time')} duplicate {has('empty-fix.log','Duplicate entry')}")
report.append(f"sparse_jar_elapsed {elapsed('sparse-jar.log.time')} duplicate {has('sparse-jar.log','Duplicate entry')}")
report.append(f"sparse_equiv_elapsed {elapsed('sparse-equiv.log.time')} duplicate {has('sparse-equiv.log','Duplicate entry')} end {has('sparse-equiv.log', chr(10)+'End') or (out/'sparse-equiv.log').read_text(errors='replace').rstrip().endswith('End')}")
report.append(f"sparse_fix_elapsed {elapsed('sparse-fix.log.time')} duplicate {has('sparse-fix.log','Duplicate entry')}")
report.append("empty_equiv_sql " + " ".join((out/'empty-equiv.sql').read_text().split()))
report.append("empty_fix_sql " + " ".join((out/'empty-fix.sql').read_text().split()))
report.append("sparse_equiv_sql " + " ".join((out/'sparse-equiv.sql').read_text().split()))
report.append("sparse_fix_sql " + " ".join((out/'sparse-fix.sql').read_text().split()))
report.append("select_fix_end " + str((out/'select-fix.log').read_text(errors='replace').rstrip().endswith('End')))
report.append("select_fix_error " + str('Exception' in (out/'select-fix.log').read_text(errors='replace')))
text = "\\n".join(report) + "\\n"
(out/'report.txt').write_text(text)
print(text)
ok = True
eq = (out/'empty-equiv.sql').read_text()
fx = (out/'empty-fix.sql').read_text()
ok = ok and '20' in eq.split() and '0' in eq.split() and '19' in eq.split()
ok = ok and '20' in fx.split() and '0' in fx.split() and '19' in fx.split()
ok = ok and has('sparse-jar.log','Duplicate entry')
ok = ok and float(elapsed('sparse-jar.log.time')) >= 10
ok = ok and has('sparse-equiv.log','Duplicate entry')
ok = ok and float(elapsed('sparse-equiv.log.time')) >= 10
ok = ok and not has('sparse-fix.log','Duplicate entry')
ok = ok and float(elapsed('sparse-fix.log.time')) < 8
sp = (out/'sparse-fix.sql').read_text().split()
ok = ok and '61' in sp and '50' in sp and '110' in sp
ok = ok and (out/'select-fix.log').read_text(errors='replace').rstrip().endswith('End')
print('RESULT', 'PASS' if ok else 'FAIL')
raise SystemExit(0 if ok else 1)
PY
