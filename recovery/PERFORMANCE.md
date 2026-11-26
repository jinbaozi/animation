# 性能结论

## 复现口径

历史记录来自上传包，时间是日志里的本地时间。本次实测在隔离的 MariaDB 10.11.14 上完成，监听 `127.0.0.1:3307`，socket `/tmp/wlm-mariadb.sock`，库 `tpcc`。它不是原来的 MySQL 8.0.31，也不是原来的主机。原机 2 分钟全并发吞吐对比未验证。

命令：

```bash
export WLM_PASSWORD='<数据库口令>'
recovery/reconstructed/scripts/repro_key_collision.sh
```

脚本编译行为等价版，在副本上打 `fix/wlm-perf-fix.patch` 后再编译修复版，然后跑三组：

- 空表，`loop=20`，`thread=1`，`rate=1,0,0,0`
- 表中只有 `c1=50` 一行，`loop=60`。原 jar、行为等价版、修复版各跑一次
- 修复版再跑 5 次点查

超时 18 秒。结果在 `evidence/repro/`。

## 历史记录

| 记录 | 日期 | 身份 | 条件 | 结果 | 用途 |
| --- | --- | --- | --- | --- | --- |
| `result_init/benchmark_summary_20261009_014104.log` | 2026-10-09 01:41 | 未记录 jar 哈希 | 脚本声明每次重启 MySQL 并清 page cache，2 轮，约 120 秒 | insert 100 线程平均 TPS 32583 / 32598；select 100 约 336k；select 200 约 464k | 参考基线 |
| `result_glibcp22/benchmark_summary_20261009_183040.log` | 2026-10-09 18:30 | 目录名表示 glibc p22，jar 哈希未获得 | 同上 | insert 100 约 36186 / 35926；select 100 约 541k / 523k | 比 result_init 更快，不能作为变慢证据 |
| `result_init-2` | 2026-10-13 | 不完整 | 样本数约 271–273 秒，和 `TEST_TIME=120` 不一致 | 只有部分 select 200 | 只作参考 |
| `tps_insert_100.log`、`nohup.out`、`benchmark_summary_20261014_142737.log` | 2026-10-14 14:26 起 | 异常栈指向 `WorkLoadManager1$loadRunner.run` | 汇总文件只有表头，测试没有跑完 | 同一秒两行 TPS；14:27:37 到 14:27:52 中断约 15 秒；主键冲突 | 本次异常记录 |

## 本次实测（2026-11-25 20:55–20:58，Asia/Shanghai）

| 版本 | 场景 | 墙钟 | 退出码 | 结果 |
| --- | --- | --- | --- | --- |
| 行为等价 | 空表 20 次插入 | 1.365 秒 | 0 | `count=20 min=0 max=19`，无异常 |
| 修复版 | 空表 20 次插入 | 1.376 秒 | 0 | 同上 |
| 原 jar | 已有 c1=50，再插入 60 次 | 10.362 秒 | 0 | 日志 `init 1`，`Duplicate entry '50'`，然后 `End`。表 `count=110 min=1 max=160` |
| 行为等价 | 同上 | 10.365 秒 | 0 | 与原 jar 相同，栈在重建源码的 `executeUpdate` |
| 修复版 | 同上 | 1.413 秒 | 0 | 日志 `init 51`，无异常。表 `count=61 min=50 max=110` |
| 修复版 | 点查 5 次 | 不足 2 秒 | 0 | 打印 `End`，无异常 |

空表上两边插入的主键范围一致。稀疏主键上，原 jar 与重建版都先冲突再空等约 10 秒，修复版直接从 51 开始写完。

机器是 4 核云主机。没有做 100 线程、120 秒的吞吐对照。冷启动，各场景 1 次。历史 30 万以上的 select TPS 不能在这台机器上复核。

## 瓶颈在哪里

时间花在应用自己的异常路径，不在这次对照里的数据库计算。

1. `nohup.out` 有两段 `Start / init / Run`，中间没有 `End`。`benchmark.sh` 第 51 行直接 `nohup java ... &`，第 59 行只在 java 进程数等于 1 时等待。两个进程会同时写同一个 tps 文件，对应 `tps_insert_100.log` 里同一秒的两行。
2. 第二个进程用 `select count(*)` 当作下一批 `c1`。表里已经有更大的主键时，`count(*)` 小于下一次可用键。字节码在冲突后 `sleep(10000)` 再调用 `run()`。稀疏主键实测从 1.4 秒变成 10.4 秒，多出来的就是这一次睡眠。
3. 递归的 `run()` 不重新取号，只从内存里的 `KeySequence` 再要一个 100 宽的窗口。所以冲突后会出现主键空洞（实测缺了 51–100），并在另一个进程仍在写入时再次撞键。每次撞键再睡 10 秒。`finally` 在递归返回后再次关闭连接并递减 `numberCount`。
4. `result_glibcp22` 比 `result_init` 更快。现有记录不支持把变慢归因于 glibc p22。依赖版本、CPU 配额和原机 MySQL 配置对 2026-10-14 这次掉速的贡献未验证。

## 根因状态

已确认：变慢来自程序。重叠启动加上 `count(*)` 取号，触发主键冲突；冲突处理固定睡眠 10 秒并递归重入。部署脚本允许第二个 JVM 启动，是触发条件。

未确认：原机上 100 线程、120 秒的 TPS 能恢复多少。阈值未获得。本次只量化了单线程稀疏主键这一条路径：约 10.4 秒降到约 1.4 秒，并且不再撞键。

## 修复与回退

补丁只放在 `fix/`，默认重建树不包含它们。

```bash
recovery/fix/apply.sh
recovery/reconstructed/build.sh
recovery/fix/revert.sh
```

- `wlm-perf-fix.patch`：MySQL 用 `count(*)` 和 `ifnull(max(c1), -1) + 1`。`key` 取后者，空表仍从 0 开始。其他数据库仍只用 `count(*)`。去掉 10 秒睡眠和 `this.run()`。点查的 `ResultSet` 用完即关。
- `benchmark-single-instance.patch`：在 truncate 之前，若进程表里已有 `WorkLoadManager`，脚本以退出码 2 停止。隔离测试：有同名进程时退出码 2，且不会执行 truncate；没有该进程时继续走到原来的 mysql 调用。

适用条件：主类是 `com.cmbcdba.WorkLoadManager1`，MySQL 兼容的 `c1` 主键，启动脚本是这份 `benchmark.sh`。两个进程如果绕过脚本同时启动，内存取号仍可能在窗口耗尽后撞车；脚本守卫挡住的是这次日志里的第二次启动。
