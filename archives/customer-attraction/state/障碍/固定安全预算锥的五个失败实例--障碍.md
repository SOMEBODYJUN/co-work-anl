---
id: "customer-attraction/fixed-security-budget-cone-failures"
kind: "obstruction"
type_tag: "障碍"
title: "固定五游戏的安全最优查询正预算与攻击边界"
status: "complete"
truth_status: "positive-budget-bounds-on-five-fixed-games-and-specified-distributions"
review_level: "full-json-read-and-rational-field-reconciliation"
scope: "五个固定单位客户游戏、每个指定安全最优p、全部完整纯SPE的预算极值；另比较三固定策略重数锥正证书"
summary: "五游戏指定安全最优p的最大sum_C−W均严格负，故最小W−sum_C均严格正；这阻止在该固定搜索空间调整SPE平局来攻击GB，不是GB/税付款失败或half反例。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/customer_attraction/selected_security_budgets/all_SPE_GB_global_decorrelation_failure.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/customer_attraction/selected_security_budgets/all_SPE_GB_individual34.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/customer_attraction/selected_security_budgets/all_SPE_GB_individual360.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/customer_attraction/selected_security_budgets/all_SPE_GB_original36.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/customer_attraction/selected_security_budgets/all_SPE_GB_root_tax_failure.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/certificates/customer_attraction/selected_security_budgets/all_SPE_GB_root_tax_failure.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/customer_attraction/selected_security_cones.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/certificates/customer_attraction/selected_security_cones.json"
---

# 固定五游戏的安全最优查询正预算与攻击边界

本页保留旧路径和稳定id以兼容已有引用；这里的“障碍”是这些固定搜索空间不能给出指定GB反例，并非GB付款接口被反驳。原JSON和数值不改。

## 五固定游戏、指定p与全部完整SPE

固定游戏G及其保存的安全最优查询分布p，对完整SPE实际前缀的真实强制行动分支删去当前槽，记竞争元组B_i(b)，定义C_i(p)=Σ_(a,b)p_a p_b f_(B_i(b))(a)。预算目标是Σ_iC_i(p)≤W。报告中的GB_violation_sumC_minus_W记录对该固定游戏全部完整纯SPE最大化的Σ_iC_i(p)−W。

因此该最大值为负，等价于相同固定游戏/指定p的全部完整SPE都有严格正的W−ΣC余量；不能解释成预算失败或遗漏付款。最大化既包括可实现有序终局路径，也在当前进入者不获利约束下为各首次偏离子树独立最大化查询；不同首次偏离子树可拼成同一完整策略。

| 固定游戏 | 人数/主题 | 达到路径 | W | ΣC | 最大ΣC−W | 对应最小W−ΣC | 根终局计数菜单/可实现有序路径 |
|---|---:|---|---:|---:|---:|---:|---:|
| global_decorrelation_failure | 4/6 | (5,0,0,2) | 85 | 828050154289/10570351740 | −70429743611/10570351740 | 70429743611/10570351740 | 2/6 |
| individual34 | 3/6 | (0,3,4) | 32 | 1252/41 | −60/41 | 60/41 | 20/40 |
| individual360 | 3/6 | (0,4,3) | 336 | 1191500603/3710088 | −55088965/3710088 | 55088965/3710088 | 15/23 |
| original36 | 3/6 | (0,3,4) | 34 | 187/6 | −17/6 | 17/6 | 20/48 |
| root_tax_failure | 4/6 | (0,0,0,4) | 38 | 73/2 | −3/2 | 3/2 | 12/102 |

菜单/路径数不计完整策略的数量。原budget_menu_generator.py直接运行其中四游戏；individual34来自另批固定游戏扩展，不倒填成本四项入口的第五次运行。[生成器审查](../审查/固定有限游戏SPE菜单预算生成器--审查.md)保完整菜单及首次偏离极值合同，[指定锥与五游戏审查](../审查/指定完整策略锥安全证书与预算边界--审查.md)保五行正余量的正确方向。

## 与selected_security_cones的不同正向结论

selected_security_cones.json是三份固定完整形式策略、任意非负客户兴趣质量的锥证书；它与上述五个固定客户游戏、指定p、全部SPE的极值不是同一个量词。逐查询有d−E_Qf=Γᵀλ+r，其中Q为合法静态背景分布、λ和r逐坐标非负。对任意满足Γw≥0、w≥0的客户质量取内积，便给d·w≥E_Qf。d=d_i证明该固定策略锥上的u_i≥v_n；d=c/n证明W≥n·v_n。

三策略共13证书、4914坐标的正乘子/余项核验，不是“负余项失败实例”。61/89客户对应策略锥的每位都可支付，36原策略锥的后两位及聚合可支付；根逐人桥的不同客户重数反例与聚合正证书相容。具体合同见[完整策略锥静态安全对偶](../定理/完整策略锥的静态安全值对偶--定理.md)及上述指定锥审查。

## 范围和接续

五行正预算只涵盖这些固定游戏及每个保存的一个安全最优p；不因此认证任意游戏、任意最优p或六人half。三策略锥的正证书也只涵盖那三份完整策略，不能推广到其他策略。若要从GB或真正聚合安全桥寻找反例，应改变已被精确正预算排除的搜索空间，不能把这些负ΣC−W记录当作现成反例。

真正已失败的全分布补偿预算使用非安全最优p，见[三人全p反例](../反例/三人全分布补偿预算--反例.md)；与本页指定安全最优p正预算不冲突。一般安全最优查询付款、真正聚合安全桥及六人half仍须独立证明；五人half另有定理。

本页纠正此前对同一字段的反向解释，保留原冻结数值与源身份，不新增旧源done、外审或一般结论。
