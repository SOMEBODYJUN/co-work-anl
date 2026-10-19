# v2 完整作者证明实际读后审查

2026-10-18。实际次序（不回填）：本人先独立重构 `independent_general_lp_v2_reconstruction.md` SHA `7beb7a1f4a75414758942e2a87378ccb6ecb1ad81fd5fe8af5fcdeb01a329113`；随后实际全文读 v2 Exact SHA `4dd1cff4786ffbccda5ee1bdedc18a34ba9b5c6408829c57e70ba4f92609c04a` 并冻攻击稿 `v2_formal_exact_attack.md` SHA `c0e9a95fd4d97f94a44f423f39e575ef1976d0546f1bfcc7487558389460578d`；接 root 通知后才全文实读作者 `../near_two_reduction/gated_weighted_menu_general_ratio_author_proof_v2.md`，SHA `16eb74e6978811c90ce4b94fef3d6d3bbd657858e893423d804e4e9a125db7da`。

## 结论与覆盖

§1–8 的完整数学证明与本人先行重构一致，没有发现 fatal。此前v1通过不作为此结论依据；本次确已独立重构新LP、两阶段claims、balanced welfare及whole-class未知OPT比例后才读作者Proof。

逐项实核：

- §2 LP row equality、正x/零job保持、W*≤L、L≤n及本域L>0。本人初稿row≤1/null与正式equality差异已前稿支付，未默读成相同。
- §3 初始跨组独立、每resource真实claim概率sum x≤1；没有把x/z误作全局占用。相同p的states概率合并合法。
- §4 状态阶段的conditional resource tail、coin阶段逐非平凡coin，及不同资源共用state相关性不会破坏逐资源期望求和。已固定prefix无需保持sumtail≤1，不把初始弦界重复套条件分布。
- §4 所有有理运算都能按原输入/LP解/ratio分母的多项式乘积统一支付。原证明给‘固定多项式次幂’较保守但有效；无按极小概率倒数或配置子集数展开。
- §5 用 h=#{r>b} 的非严格福利上界与本人用 h=#{r≥b} 的strict矛盾写法等价。任意W/n=0或1边界、n·b非整及有限最优见证均合法。
- §6 所有原连接器固定自身gate、selectors、未选states、zero incidences、unused resources的全机负载，及C<2任意调度decoder/β*=0/C≥2支路均覆盖。没有将可忽略的额外exports变成免费资源。
- §7 D=(18−13β)/8始终正，解析二次式最小1/64正确，故平方比较无符号陷阱；算法实际不知β且不计算sqrt。pin排OPT0，含n1。
- §8 源YES≤1+eta / NO≥2−delta 的比较使用严格可计算绝对阈值，未把未知OPT传decoder。gamma_hi与gamma_bad互补纠错范围准确；未扩大到flat或generalUM。

§1 新增了DNS直接机制归属，已解决本人v1来源建议。13/8未称锐或全局新颖；状态诚实。

## 有限证据的边界

本人本次只读取作者Proof全文，没有实际读取/复跑其 audit程序及JSON。因此§9报告的36/72/3/12组、非平凡coin20枚、原对偶最优证书及observed ratio，只能记为作者所报有限证据，不得把本人这一数学审查登记为独立实施核验。正式canonical若引用这些数据，root或另一实现审者仍须实际读/跑相应原件。

本文没有更改作者Exact/Proof、旧NSW正文、共享claim或任何git内容。先行独立稿、作者读后稿及原字节保持分离。v2本文范围的内部数学攻击通过，不是外审或主UM突破。
