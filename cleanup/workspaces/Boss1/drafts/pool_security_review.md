# Boss1 R-171 池化四源安全复核（独立）

复核对象：四个冻结源及 `archives/customer-attraction/state/审查/R-171池化响应探针与来源增量审查--审查.md`；不修改正式页。

## 源身份与 SHA-256

对 `cleanup/workspaces/Boss1/drafts/originals/`、`archives/customer-attraction/tools/evidence/R-171-security-audit-20261031/original/` 与 `cleanup/inventory.jsonl` 逐字节核对，四份副本均一致，且与 inventory 的 source_sha256 一致：

| id | 文件 | SHA-256 | size |
|---|---|---|---:|
| `00e6b017434d941748a5` | `pool_packet_report.json` | `a00ca0a0b49fc7bcf292e076e13bac10d0a86f0c9908eefd0c27b22918e27d8c` | 1169 |
| `32aaa81a217034da0f7c` | `pool_probe.py` | `6071e80857f313062d32cd0a566647fe5b84a6afa379e322b5f2267d4329c5fa` | 5292 |
| `d96fc2e90151962cc7fd` | `two_player_pool_report.json` | `c736025e50c1b3a31fb5c5aade26310cfd2406524aa9d494afe1bbc82a876192` | 460 |
| `4c52f58685795cdfcf9e` | `pool_packet_probe.py` | `03fb10ce0a9f5d5c244a89e2fdbf65bb27a8f94b4b3dd55473552c9e40189609` | 1430 |

`pool_packet_probe.py` 的实际 packet 输入 `research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz` 字节 SHA-256 为 `bad2b15d1abe89d9fa8671df84de8638a4b1ca46279712baa5482abb2bdf18ce`；它与 `R-171.../continuation/prices/packet13_source.json.gz`（inventory id `27a2017f46e8f8aae51e`）同字节，故应在正式页注明该别名/输入哈希，避免把 packet 源与四个增量源混为一谈。

## 数值字段复核

- `pool_packet_report.json` 的键为 `nodes=27243`、`gamma_rows=31454`、`n=13`、`k=6`、`start=0`、`iteration=0`、`ratio=1.0`、状态 `finite numerical discovery only`；`p` 为六个 `1/6`，`weights` 长度 63 且仅位置 62（mask 63，全主题类型）为 1；实际路径为 `[5,5,5,5,5,5,5,5,5,5,0,0,1]`。正式页写成 ``starts=0`` 是字段名错误，应为 ``start=0``，并把它和“30 个起点、每点 15 轮”的搜索设置分开写。报告中的单一非零权重是 LP 归一化解，不是 packet 原始 8 类客户的 multiplicity（原 packet 共 36 个单位客户）。
- `two_player_pool_report.json` 的可见键只有 `policies_checked=81`、`status=finite floating discovery only` 与 `best`；`best` 含 `ratio=1.0`、均匀三点 `p`、`start=0`、`iteration=0`、路径 `[0,0]`，权重向量 7 项且 mask 7 位置为 1。`n=2,k=3` 以及每策略 3 个 p 起点来自归档的 `two_player_pool_probe.py`/security-core 记录，不在这 460-byte JSON 内；正式页应注明这是脚本级 provenance，并引用 source id `c8322648ab9d6633541a`，不要把 JSON 单独说成自足的 3-start 证书。
- `pool_probe.py` 源码确实保留全部有序历史 Gamma 行、`np.unique` 去重、`H`（删除偏离者）与 `full`（完整终局）两种背景；固定 p 的 LP 与 SLSQP 局部 p 更新分别受有限起点/15 轮限制。`pool_packet_probe.py` 按 `counts` 总量降序重建真实 `targets`，再沿根策略累加 H；该实现与正式页叙述一致。

## 与现有 R-171 对象的一致性与边界

- 与 `R-171池化响应固定p有限审计--计算.md` 的旧 36 客户 Fraction 见证一致：旧对象的 `P_pool=8987733/272272`、`P_unpool=69/2`、`J=405651/272272`、`W-3P_pool=269515/272272>0` 及 `{0,5}` 客户 `D-P=-1/44` 均未被四源改写。
- 与 `R-171池化响应负载Jensen信用与条件接口--引理.md`、`R-171-security-core-20261031/original/README.md` 及 `pooled_response_loads.md` 的量词边界一致：这些结果只是固定策略锥/固定 packet/二人小模型的有限数值发现；`ratio=1` 只能表示本次局部搜索未找到 `>1` 分离，不能升格为全 p、全 SPE、任意 m 的 POOL 或 HALF 定理。正式页对此总体表述正确，应保留 `finite-numerical-discovery-only`。
- 正式页第 1 节把四源笼统写成“单位客户”略不精确：packet 输入显式含 integer `multiplicity`，`pool_probe.py` 的随机分支也生成带 `weight` 的 `CustomerType`。建议改为“单位客户展开/整数重数客户类型”，并明确 LP 的归一化权重与原 packet multiplicity 不同。

## 建议的最小修订

1. 将正式页 `starts=0` 改为 `start=0`；另列搜索配置“30 starts × 15 iterations”。
2. 在 front matter 或来源表加入四个 SHA-256（上表）及 packet 输入 SHA `bad2b15d…18ce`；注明该输入与 `packet13_source.json.gz` 同字节。
3. 将“单位客户”改为“单位展开的整数重数客户类型”之类的准确措辞。
4. 两人报告段落注明 `n=2,k=3`、三起点来自已归档 `two_player_pool_probe.py`（id `c8322648ab9d6633541a`），而非 460-byte JSON 自带字段；继续保留“有限局部扫描，不是全局 simplex 穷尽”。
5. 把“最优权重集中在单一客户类型”限定为“对 `c^T w=1` 的 LP 归一化向量，仅 mask=63 非零”，防止误读成 packet 原始 multiplicity。

除上述字段/出处修订外，未发现 SHA、节点/行数、路径、ratio 或现有 R-171 量词冲突；不应把有限 ratio=1 扫描升级为定理。
