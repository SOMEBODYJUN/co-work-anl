# 本轮精确身份与证据层级

主目标Q-CAG-HALF不改量词，仍OPEN。以下仅为个人阶段身份，正式共享整理前需按对象去重登记。

## B8-PURE-MENU-CONVEX-CUT-NO-v1

Exact statement：存在本模型的5人5主题单位客户实例和长度3合法历史，使纯末两人SPE利润最小值157/15，但先对子菜单收益—福利向量取凸包、再作同一可信首步门槛截断，会允许利润311/30，严格小1/10。对象、输入、全部量词和25格计算见continuation_geometry/README.md及blind_input.json；利润为末两人的最终收益和，不是根覆盖。依赖仅均分收益定义和有限末位BR枚举；root与tree_transport独立Fraction重算通过。Status：自足辅助反例、内部独审通过；不改变一般half。

## B8-CROSS-FAMILY-ENVELOPE-v1

Exact statement：对五人真实索引菜单的每位客户，将AB最后行动收益及比较second-I的异索引偏离按共同t_i分组，上界对角匹配给一条所有合法菜单实现必须满足的线性聚合行。精确D_i、计数、上包络H和量词见credible_counterexample/cross_family_envelope.md。原437与447冻结点严格违反此行；root独立枚举全部兼容边际的binary匹配核对。Status：必要条件引理与两冻结点排除，非原猜想反例。516/708行仍有精确二以上原始可行点，范围始终为固定支持松弛；未恢复精确最优对偶就不称最优。

## B8-GLOBAL-POSITIVITY-ARITY-v1

Exact statement：任意p≥4，固定a，Boolean二次函数r=x_a−Σ_(j≠a)x_ax_j+Σ_(j<k,j,k≠a)x_jx_k非负，但不能写成有限个逐项非负、每项仅依赖真子目录变量的函数之和。r空型为0，故属于低阶无常数收益矩空间；全兴趣型取正值。原文与分离泛函见tree_transport/global_positivity_arity.md，direct_global有独立证明审查。Status：一般方法障碍，非half结论；不能推断half的特殊余项都需要该障碍函数。

## B8-RANK2-INDIVIDUAL-THETA-NO-v1

Exact statement：七环7个单位边客户，每个顶点主题覆盖其两条incident边，m=4，存在完整历史纯SPE路径(0,1,4,6)，收益(1,3/2,2,3/2)，而全局最坏末位BR值theta4=3/2。故实际客户关联秩≤2也不保证∀i u_i≥theta_m。输入及400节点完整策略在independent_reconstruction/cycle_seven_*.json。W=6、OPT=7，聚合W=mtheta以及弱逐人u_i≥OPT/(2m−1)在本例均成立；不能扩大反驳范围。发现者有定义级核验；独立审查见tree_transport对应文件，以实际审查回执为准。

## 保留的开放候选

- 静态宽限SA：∀真实SPE、∀合法T，D_T≤(1+1/m)W。仍未证明或反驳。
- 保留覆盖信用的真实均匀偏离预算P≥OPT−W。direct_global/coverage_credit_debt.md给精确等价债务式，尚未支付。
- 非凸祖先承诺预算B=Σq_at_a≥OPT/2。只有精确表示和有限探针。
- 首两人真实收益≥2v_r(b)，或存在安全最优p的更强双查询接口。均未证；逐人安全值、任意安全最优p版本及若干强替代桥已失败。
