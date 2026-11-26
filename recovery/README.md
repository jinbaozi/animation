# WorkLoadManager 恢复

当前部署物是 Java fat jar，不是 ELF。Git 历史里没有原始 `.java`。源码由 jar 反编译恢复，并用 `javap` 核对了主类、行号和异常路径。REA 与 Ghidra 在本机会话中不可用。

## 结果

| 目录 | 内容 | 状态 |
| --- | --- | --- |
| `recovered-original/` | CFR 反编译结果和 jar 内配置 | 已找回的反编译文本，不是仓库里的原始提交 |
| `reconstructed/` | JDK 8 行为等价工程、构建脚本、对照测试 | 空表插入和稀疏主键冲突已与原 jar 对上 |
| `fix/` | 可单独打上和回退的性能补丁 | 稀疏主键复测已通过 |
| `evidence/` | 哈希、部署链路、字节码摘录、本次运行日志 | 上传包副本在 `materials/`。口令和内网地址已替换为占位符 |

适用环境：JDK 8 或更高版本，字节码目标 1.8。JDK 8 的 `javac` 没有 `--release`，所以 Maven 使用 `source`/`target` 1.8。依赖是 MySQL Connector/J 5（已放在 `reconstructed/lib-mysql-connector.jar`）。运行需要一个可连接的 MySQL 兼容库。

## 构建

在 `recovery/reconstructed/` 用 Maven 打出和原部署物同名的可执行包。依赖是 MySQL Connector/J 5.1.46，字节码目标是 JDK 8，主类是 `com.cmbcdba.WorkLoadManager1`。

```bash
mvn -f recovery/reconstructed/pom.xml -B package
java -jar recovery/reconstructed/target/WorkLoadManagerNew-1.0-jar-with-dependencies.jar /path/to/application.properties
```

`recovery/reconstructed/build.sh` 只编译 class，不打包。`target/` 是本地产物。

已在本机 MySQL 8.0.31（`127.0.0.1:3306`，库 `tpcc`）上用这个 fat jar 跑通。空表、单进程、`thread=1`：插入 30 行、点查 10 次、更新并删除各 5 次，退出码都是 0，输出都有 `End`，没有 `Exception`。记录在 `evidence/mysql-8.0.31/`。用户使用 `mysql_native_password`，因为原程序带的是 Connector/J 5.1.46。

## 运行

复制 `reconstructed/src/main/resources/application.properties.example`，把 `password` 和 JDBC 地址改成测试库。`thread=1` 适合先做冒烟。

```bash
java -cp recovery/reconstructed/build/classes:recovery/reconstructed/lib-mysql-connector.jar \
  com.cmbcdba.WorkLoadManager1 /path/to/application.properties
```

参数顺序与原 jar 相同：第一个参数是配置文件。进程在工作线程结束后打印 `End` 并退出。原 `benchmark.sh` 的启动行是：

```bash
java -Xms1024m -Xmx2048m -jar WorkLoadManagerNew-jar-with-dependencies.jar application.properties
```

重建脚本在 `reconstructed/scripts/benchmark.sh`。口令从环境变量 `WLM_PASSWORD` 读取，不再写死。它仍会调用 `/usr/local/mysql/bin/mysql` 并 truncate `tpcc.test_1`。没有这份 MySQL 客户端时不要直接跑它。

## 测试

```bash
export WLM_PASSWORD='<数据库口令>'
export WLM_PORT=3307
export WLM_SOCKET=/tmp/wlm-mariadb.sock
recovery/reconstructed/scripts/repro_key_collision.sh
```

已通过：

- 空表：原逻辑与修复版都插入 `c1` 0 到 19
- 只有 `c1=50` 时：原 jar 与重建版都报 `Duplicate entry '50'`，约 10.4 秒后结束；修复版约 1.4 秒，主键 50 到 110，无冲突
- 修复版点查 5 次正常结束
- 启动脚本在已有 `WorkLoadManager` 进程时退出码为 2

未验证：原机 120 秒、100/200 并发的 TPS；`WorkLoadManager`（不带 1）旧入口；Oracle、DB2、GoldenDB 等其他数据库分支。

## 性能修复

说明、历史数字和本次数字在 `PERFORMANCE.md`。应用补丁：

```bash
recovery/fix/apply.sh
recovery/reconstructed/build.sh
```

回退：

```bash
recovery/fix/revert.sh
```

## 仍缺的材料

- 原始 `.java`、Maven `pom.xml`：未获得
- 与故障进程对应的原机 `/proc` 映射或 mysqld 版本输出：未获得
- 2026-10-14 那次完整 `benchmark_summary`：未获得，文件只有表头
