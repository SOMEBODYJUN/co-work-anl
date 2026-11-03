# 数学研究Agent的代码依据与适配

本次重新克隆并实读Pharos固定提交`aa0b72e4a7211311a3156ef7d993cd3be9f57445`。它的README标注Preview；没有本题比较试验，不能称为效果最好。采用其有代码支持的按需数学记忆机制，继续使用本仓库自己的Git协作；没有部署其CLI服务或完整角色流水线。

| 精确位置 | 实际机制 | 本仓库适配 |
|---|---|---|
| `agents/skills/worker/query-memory/SKILL.md` | 区分个人记忆、共享发现与事实图；先搜摘要，再读少数完整条目和证明 | search只读登记元数据；show/context只核验实际命中数学字节，不每次扫描全仓正文；失败记录不自动作已证前提 |
| `pharos/gateway/server.py`的fact_search/fact_get | search给陈述定位，get可按需附证明 | 元数据检索、完整body和精确section读取分开；保留中文检索，不照搬只匹配ASCII的BM25 tokenizer |
| `pharos/core/schema.py`的Fact/compute_fact_id | 事实含陈述、证明、predecessors、glossary和外部引用；内容形成ID | 稳定object_id与version分开，绑定完整记录、正文和证据；同页可含多对象，附件不作命题 |
| `pharos/core/factgraph.py` | predecessor DAG、后继查询和撤回支持 | 保留多前提all超边；过期要求复核，不自动判所有后继为假 |
| `agents/skills/main/operation/checkpoint/SKILL.md` | 保存可恢复的当前研究判断，恢复先读现有状态 | 按用户要求实质进展即checkpoint；run保存packet、agent_id、不可变笔记、反馈和continuation_of，不搬四小时审计循环 |
| `agents/skills/worker/direct-proving/SKILL.md` | 直接证明、核查迁移条件、具体记录失败步骤 | Solver自由解题，保留精确缺口；不引入上游强制次数、耗时和常驻Verifier |

两类Solver、空历史启动、Boss编号、公屏、共同分支、频繁Git保存和多人构图账本来自本项目需求。登记与超边验证是结构/版本检查，不是形式证明。上游软件为Apache-2.0；本次未复制其源码或提示词正文，原有vendored依赖的LICENSE/UPSTREAM继续保留。

固定版本一手链接：

- [README](https://github.com/frenzymath/Pharos/blob/aa0b72e4a7211311a3156ef7d993cd3be9f57445/README.md)
- [query-memory](https://github.com/frenzymath/Pharos/blob/aa0b72e4a7211311a3156ef7d993cd3be9f57445/agents/skills/worker/query-memory/SKILL.md)
- [gateway](https://github.com/frenzymath/Pharos/blob/aa0b72e4a7211311a3156ef7d993cd3be9f57445/pharos/gateway/server.py)
- [schema](https://github.com/frenzymath/Pharos/blob/aa0b72e4a7211311a3156ef7d993cd3be9f57445/pharos/core/schema.py)
- [checkpoint](https://github.com/frenzymath/Pharos/blob/aa0b72e4a7211311a3156ef7d993cd3be9f57445/agents/skills/main/operation/checkpoint/SKILL.md)
