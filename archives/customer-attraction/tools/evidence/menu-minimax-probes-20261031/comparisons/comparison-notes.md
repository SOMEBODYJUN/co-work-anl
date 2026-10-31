# menu_minimax 三源比较记录

本批三源完整实读，分别对应既有非空主题强聚合反例的独立审计、同一方向的数值发现输出和交替锥 LP 探针。

| ID | 文件 | 字节 | SHA-256 | 范围 |
|---|---|---:|---|---|
| `86d61de22b9904f6ff09` | `audit_nonempty_extra_slot.py` | 3088 | `23b1ab2edd72f24949ce4929e5463b9864b8a5050f14befb505c7637a1a1122e` | 13 mask types，复制 67 次并加 topic-6 私有客户；57 histories、342 nonself comparisons、Fraction D/G 预算和 SPE slack。 |
| `68f076e510cfcfb1e6ab` | `extra_slot_aggregate_probe.json` | 3362 | `d983ac16c4fa0fc11d0f8da325676a56b3c09a30739dbe882f02ac821b680f1a` | `scope=numerical discovery only`，75 次，best ratio 0.9285714…（约 13/14），n=3,k=6，保存浮点 p/weights/branches/actions。 |
| `3e7ed02343d3b3c5e93d` | `extra_slot_aggregate_probe.py` | 3032 | `fafb904356f71a350ffee5537fe26fa6ecce8a545dc8c79d8e67c372a5be3627` | 依赖另一工作区 `background_pair_probe.py`，随机 n/k/density/weights，交替 SciPy LP 与 SLSQP，最多 75 次 discovery。 |

## 与既有 exact 反例和安全值对象

现有 `state/反例/完整强制终局聚合去相关的非空主题反例--反例.md` 已承载 B9-NONEMPTY-AGG-EXTRASLOT-NO-v1：K=67/J=1、2279 个单位客户、57 histories、342 nonself、W=2144、OPT3=2278、ΣD−ΣG=−7/384 和 K>66J 阈值。新 audit 脚本是独立、无 parent-audit import 的重核，不创建第二个反例节点。

现有 LAST 候选、静态混合安全值定理、aggregate-security exact audits 和 direct-cover/dynamic-credit 对象仍区分强 `ΣG_i^+(p)<=ΣD_i(p)`、弱 `ΣG<=W`、自由完整菜单、真实路径支付和 Q-CAG-HALF。三源没有扩大任何范围。

## 数值和依赖边界

Audit 脚本使用 Fraction、全历史 actions 和 asserts，但本轮未重新执行；既有 exact output 已保留同一实例。JSON 是浮点 discovery output，ratio<1 不证明安全；probe Python 依赖未在本批认领的 `background_pair_probe.py`，使用 LP/SLSQP、有限随机 trials、无 exact/full-SPE certificate。三源均不迁移到 unrelated-machines。
