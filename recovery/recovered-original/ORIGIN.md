# 找回记录

Git 历史、reflog、其他工作区和编辑器本地历史中没有 `WorkLoadManager1.java` 的原始文件。未获得独立调试符号包。下面的文件是从当前部署 jar 反编译得到的，并与 `javap` 的 `SourceFile`、`LineNumberTable` 对照过。

| 文件 | 来源 | 标识 |
| --- | --- | --- |
| `WorkLoadManager1.java` | `WorkLoadManagerNew-jar-with-dependencies.jar` 中的 `com/cmbcdba/WorkLoadManager1*.class`，CFR 0.152 | `SourceFile: WorkLoadManager1.java`，Manifest `Build-Jdk: 1.8.0_321`，`Built-By: leiche`，`Main-Class: com.cmbcdba.WorkLoadManager1` |
| `WorkLoadManager.java` | 同一 jar 的旧入口类，不是 Manifest 主类 | 同类反编译 |
| `config_*.properties` | jar 内资源 | 各数据库示例配置 |

jar SHA-256：`29db632e00fc26291f2c841384015db8546efbf3e6330790173cdae5eda5b52d`

这些反编译文件保留 CFR 头，作为找回结果。可编译的行为等价工程在 `../reconstructed/`，其中行号因反编译排版与原始 `LineNumberTable` 不完全一致。

jar 内配置里的口令和内网地址在入库前已换成占位符。
