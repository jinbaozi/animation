# MySQL 8.0.31 验证

服务器：`/usr/local/mysql/bin/mysqld`，`Ver 8.0.31 for Linux on x86_64 (Source distribution)`。

监听：`127.0.0.1:3306`，socket `/data/myinst1/tmp/mysql.sock`，库 `tpcc`。

程序：`mvn -f recovery/reconstructed/pom.xml -B package` 生成的 `WorkLoadManagerNew-1.0-jar-with-dependencies.jar`。主类 `com.cmbcdba.WorkLoadManager1`。单进程，`thread=1`，空表开始。

| 步骤 | 退出码 | 标准输出 | 表 |
| --- | --- | --- | --- |
| 插入 30 行 | 0 | `Start` / `init` / `0` / `Run` / `End` | `count=30 min=0 max=29` |
| 点查 10 次 | 0 | `init 30` 后 `End` | 行数不变 |
| 更新 5 次并删除 5 次 | 0 | `init 30` 后 `End` | `count=25 min=0 max=29` |

三条日志都没有 `Exception`。日志文件：`insert.log`、`select.log`、`mix.log`。
