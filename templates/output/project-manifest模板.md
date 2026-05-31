# Project Manifest

> 项目：{项目名称}
> 版本：v1.0
> 生成日期：{YYYY-MM-DD}

---

## 1. 项目基础信息

| 字段 | 内容 |
|---|---|
| project_name | {项目名称} |
| source_file | {原始小说路径} |
| total_word_count | {总字数} |
| target_platforms | {抖音/快手/B站/视频号} |
| target_tools | {Seedance2/即梦/豆包/其他} |
| style_profile | {风格锁定结果} |
| delivery_scope | VideoPrompt包；人物资产卡；场景资产卡 |

---

## 2. 体量规划

| 指标 | 数值 | 说明 |
|---|---:|---|
| target_shots | {N} | 参考 `ceil(total_word_count / 80)` |
| target_sequences | {N} | 按目标工具时长推算 |
| character_count | {N} | 来自人物清单 |
| scene_count | {N} | 来自场景清单 |

---

## 3. 工具 Profile

| 工具 | 语言 | 时间格式 | 负面词规则 | 参考图规则 |
|---|---|---|---|---|
| Seedance2 | 英文 | {格式} | {规则} | {AD Reference规则} |
| 中文审阅版 | 中文 | {格式} | {规则} | {可选} |

