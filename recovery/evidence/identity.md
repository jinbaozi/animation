# 样本身份与部署链路

## 材料

- 上传包：`/home/ubuntu/.cursor/projects/workspace/uploads/wlm_ea1d.zip`
- SHA-256：`edc7018449d4deb9fb560405643359b90461edbe43aee6f3e7136297f03caab9`（`sha256-upload.txt`）
- 解压副本：`evidence/materials/wlm/`
- 单文件哈希：`sha256-materials.txt`
- 主程序 jar：`WorkLoadManagerNew-jar-with-dependencies.jar`
- SHA-256：`29db632e00fc26291f2c841384015db8546efbf3e6330790173cdae5eda5b52d`

`sha256-materials.txt` 是上传原件的哈希。提交前把配置和启动脚本里的口令、内网地址换成了占位符，所以工作区里的 `application.properties`、`benchmark.sh` 和 `config_*.properties` 不再等于这些哈希。jar 未改。

这不是 ELF。`file` 识别为 Java jar。REA MCP 与 Ghidra 在本机会话中未暴露，分析使用 `jar`、`javap` 和 CFR 0.152（`/tmp/cfr.jar`）。

## 构建身份（脚本声明，来自 jar Manifest）

- `Main-Class: com.cmbcdba.WorkLoadManager1`
- `Build-Jdk: 1.8.0_321`
- `Built-By: leiche`
- `Created-By: Apache Maven`
- 应用类：`WorkLoadManager`、`WorkLoadManager1` 及其内部类 `KeySequence`、`loadRunner`、`TimeMonitor`
- 其余为 MySQL Connector/J（`com.mysql.jdbc`）
- DWARF / Build ID / `.gnu_debuglink`：不适用。未获得单独的 Maven POM 或 class 的源码调试包。类文件带 `LineNumberTable` 和 `LocalVariableTable`。

## 发布产物到实际进程

以下行号指 `evidence/materials/wlm/` 中的脚本。

1. `auto_run_benchmark_v2.sh` 第 25 行 `pkill -9 java`，第 36 行 `pkill -9 mysqld`，随后调用 `benchmark.sh`。测试窗口 `TEST_TIME=120`，轮次 2。INSERT 线程 1/10/50/100，SELECT 线程 1/10/50/100/200。路径写死 `/home/wlm/`。
2. `benchmark.sh` 第 6–9 行：操作 `insert`，配置 `application.properties`，jar `WorkLoadManagerNew-jar-with-dependencies.jar`，`thread='100'`。
3. 第 32–34 行用 `sed` 改 `tpslog`、`rate`、`thread`。
4. 第 38 行：insert 时用本机客户端执行 `truncate table test_1`。
5. 第 51 行：`nohup java -Xms1024m -Xmx2048m -jar $JARFILE $CONFIG &`。脚本没有先结束已有的 WorkLoadManager。
6. 第 53、59 行：只有 `ps` 里 java 进程数恰好为 1 时才等待。已经有两个 java 时，等待条件不成立。
7. `application.properties`：`loop=100000`，`thread=100`，`rate=1,0,0,0`，表 `test`，库 `tpcc`，JDBC `localhost:3306`。文件里还有被注释的内网地址。

`nohup.out` 里 `Start` 出现两次且中间没有 `End`，随后主键冲突。`tps_insert_100.log` 在同一秒写两行（一行约 9k，一行 0）。这与两个 JVM 共用同一个 tps 文件相符。故障日志里的 jar 异常类名与本 jar 主类一致，可以对应到这份二进制。原始主机上的进程内存映射未获得，不能做运行时 Build ID 核对。

## 关键字节码

`com.cmbcdba.WorkLoadManager1$loadRunner.run`：

- 异常点：`LineNumberTable` 行 329，`executeUpdate`
- 处理：字节码偏移 1194 `ldc2_w 10000`，1197 `sleep`，1204 `invokevirtual run()V`
- 摘录：`loadrunner-exception-path.javap`

`KeySequence.init` 对所有数据库执行 `select count(*)`，把结果同时赋给 `key` 和 `currentKey`。插入窗口从该值起，步长为 `buffer`（配置为 100）。
