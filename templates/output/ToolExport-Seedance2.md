# Tool Export: Seedance2

> 用途：从 Prompt Export IR 导出 Seedance2 实际提交 Prompt
> 语言：英文

## 导出规则

- 每条 Prompt 必须引用 `shot_id`。
- 主体、动作、视线、场景、灯光、风格均来自 Prompt Export IR。
- 禁止直接从剧本或分镜跳过 Prompt Export IR 生成。
- 时间戳格式按 `project-manifest.md` 的 Seedance2 tool profile 执行。
- Negative Prompt 使用英文名词枚举，不使用否定句。

## 校验清单

- [ ] 引用了 Prompt Export IR 的 `shot_id`
- [ ] 人物描述与人物资产卡一致
- [ ] 场景描述与场景资产卡一致
- [ ] 无项目风格禁用词
- [ ] AD Reference 编号不跳号、不重复

