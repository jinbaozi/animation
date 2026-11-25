#!/bin/bash

# ==================== 1. 基础配置 ====================
BENCHMARK_SCRIPT="/home/wlm/benchmark.sh"
TEST_TIME=120     # 每组测试持续时间（秒）
ROUNDS=4          # select 测试的组数/轮数

# 数据库相关配置
MYSQL_SOCKET="/data/myinst1/tmp/mysql.sock"
MYSQL_PASS="123456"
MYSQL_USER="root"

# 并发梯度配置 (INSERT 与 SELECT 并发梯度)
INSERT_THREADS=(1 10 50 100)
# (1 10 50 100 200)
SELECT_THREADS=(200)

# 测试结果汇总日志
SUMMARY_LOG="/home/wlm/benchmark_summary_$(date +%Y%m%d_%H%M%S).log"
APP_PROP="/home/wlm/application.properties"

# ==================== 2. 辅助函数 ====================

# 清理/停止压测 Java 进程
stop_benchmark_java() {
    pkill -9 java > /dev/null 2>&1
    sleep 2
}

# 关闭并重启 MySQL 数据库，并清理 Linux OS PageCache
restart_db_and_drop_cache() {
    echo " 🔄 [数据库维护] 正在优雅关闭 MySQL 数据库..."
    /usr/local/mysql/bin/mysqladmin -u"${MYSQL_USER}" -p"${MYSQL_PASS}" shutdown -S "${MYSQL_SOCKET}" > /dev/null 2>&1
    
    # 等待进程彻底退出
    sleep 3
    pkill -9 mysqld > /dev/null 2>&1
    sleep 2

    echo " 🧹 [系统维护] 执行清理 PageCache (echo 3 > /proc/sys/vm/drop_caches)..."
    echo 3 > /proc/sys/vm/drop_caches
    sleep 2

    echo " 🚀 [数据库维护] 启动 MySQL 数据库..."
    /usr/local/mysql/bin/mysqld_safe --defaults-file=/etc/my.cnf &
    
    # 循环探活，直到数据库 Socket 正常响应用以确保 Ready
    echo -n " ⏳ 等待 MySQL 启动拉起..."
    local retry=0
    while ! /usr/local/mysql/bin/mysqladmin -u"${MYSQL_USER}" -p"${MYSQL_PASS}" ping -S "${MYSQL_SOCKET}" > /dev/null 2>&1; do
        sleep 2
        retry=$((retry+1))
        echo -n "."
        if [ ${retry} -gt 30 ]; then
            echo -e "\n ❌ [错误] 数据库启动超时，请检查 MySQL 日志！"
            exit 1
        fi
    done
    echo -e "\n ✅ 数据库启动成功并已准备就绪！"
}

# 动态修改 benchmark.sh 中的参数
update_config() {
    local oplist=$1
    local thread=$2

    # 使用 sed 替换 benchmark.sh 中的 OPLIST 和 thread 变量赋值
    sed -i -E "s/^(OPLIST=).*/\1'${oplist}'/" "${BENCHMARK_SCRIPT}"
    sed -i -E "s/^(thread=).*/\1'${thread}'/" "${BENCHMARK_SCRIPT}"
}

# 解析并统计测试日志
analyze_log() {
    local log_file=$1
    if [[ -f "${log_file}" ]]; then
        awk '
        {
            for (i=NF; i>=1; i--) {
                gsub(/[^0-9.]/, "", $i);
                if ($i ~ /^[0-9]+(\.[0-9]+)?$/ && $i != "") {
                    val = $i + 0;
                    sum += val;
                    count++;
                    if (val > max || max == "") max = val;
                    if (val < min || min == "") min = val;
                    break;
                }
            }
        }
        END {
            if (count > 0) {
                printf "样本数: %ds | 平均TPS: %.2f | 峰值TPS: %.0f | 最小TPS: %.0f", count, sum/count, max, min;
            } else {
                printf "日志为空或未能提取到有效TPS数据";
            }
        }' "${log_file}"
    else
        echo "未找到日志文件: ${log_file}"
    fi
}

# 执行数据预加载函数 (用于 select 轮次前铺平 1kw 数据环境)
preload_insert_data() {
    echo -e "\n 📦 [数据准备] 开始执行每轮前的 Insert 数据预铺任务..."
    stop_benchmark_java

    # 1. 修改 application.properties 中的 loop 参数为 100000
    if [[ -f "${APP_PROP}" ]]; then
        echo " ⚙️ [配置调整] 修改 ${APP_PROP} 中的 loop=100000"
        sed -i -E "s/^(loop=).*/\1100000/" "${APP_PROP}"
    else
        echo " ⚠️ [警告] 找不到配置文件 ${APP_PROP}，请检查路径！"
    fi

    # 2. 修改 benchmark.sh 为 insert 操作与 100 并发
    update_config "insert" "100"

    # 3. 启动压测
    echo " ⏳ 正在启动 100 并发预写数据 (100线程 * 10W次)..."
    bash "${BENCHMARK_SCRIPT}" > /dev/null 2>&1 &

    # 4. 【关键修复 1】：等待并确认 Java 进程真正拉起（最多等待 15 秒）
    local wait_start=0
    while ! pgrep -f java > /dev/null 2>&1; do
        sleep 1
        wait_start=$((wait_start + 1))
        if [ ${wait_start} -ge 15 ]; then
            echo -e "\n ❌ [错误] 15秒内未检测到 Java 压测进程启动，请检查 benchmark.sh 或环境变量！"
            break
        fi
    done

    # 5. 【关键修复 2】：确认 Java 启动后，轮询等待其完全执行结束
    if pgrep -f java > /dev/null 2>&1; then
        echo " 🏃 Java 压测进程已就绪，开始持续写入数据，请耐心等待..."
        
        # 持续监听，只要存在 java 进程就继续等待
        while pgrep -f java > /dev/null 2>&1; do
            sleep 5
            echo -n "."
        done
        echo -e "\n ✅ [数据准备] 100 并发预写数据已全部顺利执行完成！"
    fi

    # 6. 还原 application.properties 中的 loop 参数为 0
    if [[ -f "${APP_PROP}" ]]; then
        echo " ⚙️ [配置还原] 还原 ${APP_PROP} 中的 loop=0"
        sed -i -E "s/^(loop=).*/\10/" "${APP_PROP}"
    fi

    # 善后清理
    stop_benchmark_java
}

# ==================== 3. 主测试逻辑 ====================

echo "==========================================================" | tee -a "${SUMMARY_LOG}"
echo "            开始自动化数据库 benchmark 压测与统计           " | tee -a "${SUMMARY_LOG}"
echo "配置说明: 每次变换并发均重启 MySQL 并清理 OS PageCache" | tee -a "${SUMMARY_LOG}"
echo "==========================================================" | tee -a "${SUMMARY_LOG}"

# -------------------- 阶段 A: SELECT 阶段测试 --------------------
echo -e "\n==========================================================" | tee -a "${SUMMARY_LOG}"
echo "   🚀 开始执行 [SELECT] 阶段测试 (共 ${ROUNDS} 轮)" | tee -a "${SUMMARY_LOG}"
echo "==========================================================" | tee -a "${SUMMARY_LOG}"

# SELECT 压测前，先插入铺平基础数据
preload_insert_data

for round in $(seq 1 ${ROUNDS}); do
    echo -e "\n----------------------------------------------------------" | tee -a "${SUMMARY_LOG}"
    echo " 🔹 [SELECT] 第 ${round}/${ROUNDS} 轮测试" | tee -a "${SUMMARY_LOG}"
    echo "----------------------------------------------------------" | tee -a "${SUMMARY_LOG}"

    for t in "${SELECT_THREADS[@]}"; do
        # 1. 压测前重启数据库 + 清理 cache
        stop_benchmark_java
        restart_db_and_drop_cache

        # 2. 修改配置参数
        update_config "select" "${t}"
        target_log="/home/wlm/tps_select_${t}.log"
        rm -f "${target_log}"

        echo " ⏳ 正在测试: 操作=select | 并发=${t} | 组次=${round} | 持续=${TEST_TIME}s..."

        # 3. 启动压测
        bash "${BENCHMARK_SCRIPT}" > /dev/null 2>&1 &

        # 4. 倒计时持续压测
        sleep "${TEST_TIME}"

        # 5. 停止压测进程
        stop_benchmark_java

        # 6. 读取并解析结果
        stats=$(analyze_log "${target_log}")
        echo "   ✅ [第${round}轮] select | 并发 ${t} 线程 ➔ ${stats}" | tee -a "${SUMMARY_LOG}"
    done
done


# -------------------- 最终收尾 --------------------
stop_benchmark_java

echo -e "\n==========================================================" | tee -a "${SUMMARY_LOG}"
echo " 🎉 所有压测全部完成！" | tee -a "${SUMMARY_LOG}"
echo " 完整汇总日志保存在: ${SUMMARY_LOG}" | tee -a "${SUMMARY_LOG}"
echo "==========================================================" | tee -a "${SUMMARY_LOG}"
