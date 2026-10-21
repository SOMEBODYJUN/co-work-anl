# 一般Q-CAG-HALF：全局机制分支

主目标仍OPEN，原模型和全部完整历史纯SPE量词不变。本目录仅个人研究资产；root汇总，不自行git或work通信。

- `strict_unique_spe_static_gap.md`：Claim `B2-STRICT-UNIQUE-SPE-STATIC-GAP-v1`，三人四主题十二单位客户，唯一完整SPE在全部21历史严格最优，W11而唯一静态PNE计数ABC福利12；给全十五兴趣类型正质量的1215客户整数版本、严格余量与稳健性。root已独立逐客户确认原例，正文仍无外审或规模最小性认证。
- `audit_strict_static_gap.py`、`.json`：不导入发现代码/solver/优化器的Fraction单位客户展开审计，核查原例及满支持版本。
- `strict_static_bridge_search.py`、`compress_strict_bridge.py`及对应JSON：精确有限随机发现与MILP压缩，数学结论只由自足表和定义级审计承担。另保留五主题16客户中间例；最终正文使用四主题12客户例。
- `min_price_attack.py`、`.json`：对存储的完整有序策略锥保留全部历史SPE行及“指定玩家为实际最低收益”的行，攻击`B(min_i u_i)<=W`。目前仅查询全目录等权、质量在会员次数阈值的有限菜单；无正候选不作一般证据。

下一步继续一般最低收益价格机制，不停留在严格静态桥小例。核心新候选为：利用指定实际收益u_i不超过全部在轨后继收益的序关系行，争取`B(u_i)<=W`或对坏价格预算进行真实后继分支的严格下降。尚无一般承重证明，不把该候选改写为已有结果。
