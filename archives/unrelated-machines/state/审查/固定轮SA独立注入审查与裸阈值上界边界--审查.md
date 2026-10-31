---
id: "unrelated-machines/fixed-literal-sa-independent-review-threshold-domain"
kind: review
type_tag: 审查
title: "固定轮SA独立注入审查与裸阈值上界边界"
status: complete-primary-read-and-scoped-mathematical-reconstruction
summary: "完整signed literal局部注入条件容量及r=m端点；区分可行证书下界与全类精确gap，保裸r1/T<1修正。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/fixed_sa_assignment_gap_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/fixed_sa_assignment_gap_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/fixed_sa_assignment_gap.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/fixed_sa_assignment_gap.md"
evidence_manifest: ../../../../tools/evidence/um-next-available-reviews/source-manifest.json
---

# 实际阅读与历史独立身份

主源19754a51b44607548db4全文1466B/17行已读，当前0168a2c67a96432d1caf全文84行及既有《固定轮literal-SA的单位指派趋二间隙》117行已比较。前轮该review仅旁读，不能据已有原件省略本次实读或冒先前已done。它记录先行重构局部注入，再攻击容量乘式、负literal、r≤m及位长；没有代码、有限枚举或外审记录。本轮是知情数学核对，不是新盲审。

# 精确松弛和完整伪解

单位assignment基底为每jobΣ_i x_ij=1、每机Σ_j x_ij≤T、0≤x≤1。轮次r≥1指各原行乘至多r−1个literal x或1−x后Boolean线性化，所需总阶≤r；不静默更换文献轮编号。

给每对m≥r≥1，m机、m+1个unit jobs，所有p=1，T=1+1/(m−r+1)。真实调度允许同机多个job。对任意涉及Q、q≤r个任务的literal事件Λ，取Q→[m]均匀注入μ_Q，A_Λ为满足整个事件的注入集合，y_Λ=|A_Λ|/(m)_q。无注入置0，不仅检查语法上直接矛盾；两个不同job指定同机是原调度允许的事件，但此伪解主动给0，不是添加原模型禁令。

忘记任务时每小注入有相同数扩展，所有重叠moments一致。对q≤r−1，未查询job有m−q个扩展，故Σ_i y_(Λ∧x_ij)=y_Λ；已查询job逐注入列和1。非负和补literal事件给boxes；零事件的所有单literal扩展亦0，不通过除零忽略。

正事件条件于每个满足注入φ：若机器i被Q占据，已查询贡献1、所有单独扩展贡献0；若空闲，未查询m+1−q个job各以1/(m−q)在其单独扩展中到i，总1+1/(m−q)。对满足Λ的混合仍≤1+1/(m−r+1)=T。这里仅逐项相容q+1局部统计，未构造全部m+1任务注入m机的全局law。乘回y_Λ给所有容量literal乘式，负literal同样覆盖。

鸽巢给整数OPT2，一机两件、其余一件达到。故证书比值2−2/(m−r+2)固定r时趋2。T是本构造的可行阈值，不是已求精确SA最小阈值。m=r时T2、比值1；r>m不在域。moment分母(m)_q位长O(r logm)，固定r的显式大小(m(m+1))^O(r)，可变r不承诺统一多项式。不存在任何新有限实验来替代该全称推导。

# 原主稿额外全类上界必须限定基底

原稿称投影assignment/LST后ST给2T，故全类gap上确界恰2。该话对剪枝p>T端的LST，或此主族T≥1的单位阈值域成立；裸r1 LP允许T<1，不能无条件套用。m机仅一个unit job，x_i1=1/m、T1/m满足裸r1 LP，真实OPT1，gap=m可大于2。r≥2时容量乘x_ij给(T−1)y_x≥0，非空job列和排除T<1，但统一r≥1陈述仍需条件。

既有117行正式页已明确补此域，本review原文没有处理该额外全类断言。因此其“无fatal”只保参数主构造，不认证裸LP全类上界。该限制不影响m+1任务族的趋二下界。

m>r时T<2，每机CONFIG只能空/单件，总质量≤m不能覆盖m+1，所以CONFIG直接不可行；m=r/T2不应称配置不可行。配置合取、增长层SOS/Lasserre、跨机器联合cuts与直接原矩阵算法不被此review排除。本族原OPT可显然求出；固定值格点算法搜索真实整数阈值2，与近1局部证书不冲突。

结果只阻断“固定r此literal-SA证书→相对同T统一(2−ε)T舍入”，不排一般相对真实OPT近似、P≠NP意义复杂度或模型间SA保真。原件冻结，既有定理不覆写，未新增程序运行/外部PDF核验。
