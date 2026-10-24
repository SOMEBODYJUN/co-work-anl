# 不交保留主题将完整旧策略嵌入正深度：一般充分引理

身份：R22-DISJOINT-RESERVATION-LIFT-v1。Root 直接推导，direct 分支只收到陈述后独立检查了全部策略拼合和根比较，未发现致命异议。具体安全值反例另由 security 生成、menu 独立定义级审查。无外审、全球新颖性或最小性认证；Q-CAG-HALF 仍 OPEN。

## Exact statement / objects / domain / quantifiers

任取 n≥2 位单位提供者的旧 CAG，有限单位客户集 N、有限非空共同目录 S，以及一份覆盖全部有序历史的纯 SPE σ。记 η>0 为这份 σ 在**所有旧决策历史**的规定行动所得最终利润的一个共同下界。对每个旧合法主题 T 定义

    δ_T=min_(S∈S)|T∩S|。

取正整数 J，使

    J/2≤η，                                      (P)
    J≥max_(T∈S)(|T|−δ_T/2)，                     (R)
    |T|/2>J/n  对每个 T∈S。                      (L)

加入 J 名不同的新单位客户，它们仅喜欢一个新主题 B；B 与全部旧客户不交。新共同目录为 S∪{B}，总人数为 n+1。结论：存在一份**全部有序历史**纯 SPE，其根选 B，在根后且没有再次选择 B 的全部历史逐字执行 σ。实际终局为 (B,z(σ))，旧玩家的每一项实际收益保持，新增首人的收益为 J，新 W=W_old+J。

σ 的平局、历史依赖、重复主题都不作限制。条件 (L) 排除了本引理输入中的旧空主题；这只是本辅助引理的明示假设，**不改变主目标允许空主题的范围**。有理数据可先共同放大为整数客户；不引入带权提供者。

## Proof: first reserve B, then retain every old ordered comparison

根后没有第二次 B 的历史称为保留域。此时删去最初的 B，剩余有序旧历史是 σ 的一个合法历史。在保留域指定 σ 的旧行动。

若在保留域改选另一个旧主题，后续仍在保留域，旧客户收益完全等于原 σ 的真实偏离收益；初始 B 与旧客户不交，不产生新外部性。原完整 SPE 比较因此逐条保留。

若当前改选 B，则无论以后怎样，B 已有最初首人覆盖，当前玩家从 B 得到的利润至多 J/2≤η。其原指定行动所得至少 η，故该新偏离不盈利。

在每个第一次额外 B 的孩子中，用有限逆向归纳填写任意完整纯 SPE。这些子树彼此不交，且以后都含额外 B，不会重新进入保留域。于是根 B 后的整个子博弈均是完整纯 SPE。没有冻结真实后继，也没有仅验证实际旧路径。

## Proof: every root deviation to an old T is bounded

对每个根旧动作 T，用逆向归纳任取其完整 n 人子 SPE。该孩子的实际后继不可能全部选 B：否则最后一人选 B 得 J/n，改选根的 T 得 |T|/2，违反 (L) 和末位最优性。

所以至少一名后继选择某旧主题 S。根主题 T 上，T∩S 的客户至少有两位覆盖者，其余客户给根至多一。因此同一真实叶上根收益满足

    d_T≤|T|−|T∩S|/2≤|T|−δ_T/2≤J。

根选 B 后实际没有其他 B，收益恰 J。故根在全部合法主题中最优。各根旧动作子树、根 B 的保留域与第一次额外 B 子树不相交，以上拼合是一份良定的完整策略。证毕。

## Evidence and relation to existing work

证明依赖有限逆向归纳和单位均分的逐客户比较，不依赖有限试验。与旧同人数 safe_catalog_padding 的合同不同：本引理增加一个先行动者，B 可以很大、实际被选，而其已占用份额将后来的 B 偏离收益压到 J/2。也可视作一般政策拼合思想的一个明确保留机制，不宣称这种思想本身新颖。

具体 old34 输入为 examples/customer_attraction/individual_security_failure.json，完整旧 σ 及其文献/审查范围见 research/current/customer_attraction/individual_security_counterexample.md。定义级 Python 重算得到

    n=3，η=29/3，J=19；
    旧主题大小=(23,23,21,23,23,21)，全部 δ_T=11。

故 (P) 是 19/2≤29/3，(R) 的最大右侧为 35/2≤19，(L) 由最小 |T|/2=21/2>19/3 得到。注意旧正文个别摘要给出的“每主题21”不能替代实际输入；本次参数由原类型表重算。

新 full certificate 与匹配静态 minimax 证书在 ../security/positive_depth_floor_{game,certificate,audit}.json，脚本 ../security/audit_positive_depth_floor.py。该第一份 BI 证书保留旧实际叶，但在部分旧历史作了并列行动替换。逐字保留全部旧 σ 的版本另在 ../direct/disjoint_reservation_literal_certificate.json；../direct/audit_disjoint_reservation_lift.py 同时核验全部保留域和新全树。两份都是合法完整 SPE。新实际收益为

    (19,29/3,67/6,67/6)，W=51，OPT_4=53，v_4=28481/2924。

因此 v_4−u_2=647/8772>0，明确否定“只对非首位要求 u_i≥v_m(0)”这一新加强。原 W≥m v_m、弱聚合桥、Mfull/Mpath 和 Q-CAG-HALF 均没有被此例否定。

## Status / objections / remaining obligation

本引理是带明确条件的全参数构造组件，不是新的受限目录福利项目。其作用是检查一般安全值归纳中把早期失败局限于根的假设：这种局限无效。它不证明任何新的普遍福利下界，也不说明所有逐人桥都不能用于一般证明。

关键仍是聚合支付：新例的失额可以由其他人的利润补回；不能把单个正深度赤字当成聚合安全值或 half 的反例。独立审查、可复现实验证书及精确范围在同一工作区保存，发布状态以本区 CLAIMS 和 README 为准。
