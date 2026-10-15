# 当前研究前沿

## 当前主攻：加权原子拥塞

当前协作集中判定全类 O(d/ln d) 近似纯均衡存在命题，完成须给一般肯定证明或严格否定证明；常数和次数起点不能依赖博弈规模或权重。精确量词与唯一门槛见[本题验收](research/weighted_congestion_frontier/ACCEPTANCE.md)。局部引理、方法障碍和有限实例仍可入库，不能替代该完成标准。

WC-TARGET v1 保持 OPEN。所有已发现远端研究分支的独有成果已经进入共同分类；精确去处见 [FILES.md](research/weighted_congestion_frontier/FILES.md)。旧公屏和旧会话不作为状态来源。

最重要的已保存进展是奇环 hub/cohort 的有限全状态非存在构造：
T_d=max_(R>1)[R(1+R)^d+1]/[(1+R)^d+R^(d+1)]∼d/ln d，因而 a_*(d)≥T_d。
R1 的线性重置实现与 R3 的同次数实现归属于共同机制，保留原作者和各自独立审查。它们不是两项互不相关的突破。[现行数学入口](research/current/weighted_congestion/README.md)说明精确范围。

全类上界仍是已核对文献 d。关键未解义务是全类 O(d/ln d) 存在性，或绕开当前全部 light-forcing 测试的更强全状态非存在机制。一般 cohort 奇环的实际均衡阈值也不能从证书失效推出。

固定权重与动作数的[全状态线性证书接口](research/current/weighted_congestion/template_certificates/finite_action_duality.md)已独立重构：关联签名消去任意资源数，逐selector给非负系数/primal与概率dual替代。[严格反例整数规范形与闭端点](research/current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md)又消去固定倍率反例的实参数：规范形仍无规模界，普遍阈值端点可行。尚无统一C,d0；[最小点选择等价](research/current/weighted_congestion/separable_ordinal_obstruction.md)也只澄清旧势障碍的量词。

## 工具、边界与待审项

- 已保存：[高次份额势](research/current/weighted_congestion/high_degree_share.md)及两套独立精确审计，提供实例相关近精确界、纯高次必要小份额和固定正权向量的一致高次极限。
- 已保存：文献源包络锐渐近与完整对称两列拓扑限制、稀疏权密度势及拼接、局部窄权带势、密度 padding、有限非对称拓扑分离、三负载曲率、异权端点还原、多列逃逸与辅助 step-DAG。
- 已独立重构并攻击：[任意玩家乘子与依游戏资源可分序势障碍](research/current/weighted_congestion/separable_ordinal_obstruction.md)，精确范围只含所写边际夹逼与全部改善边下降证书，所构游戏仍有精确均衡。
- 待审：普适复制桥的其他推论、保守多项式端点扩展及完整两列轨道稿。它们有正文或精确计算，不能因入 main 就称为已审定理。
- 已知来源欠账：三玩家稿所引 resource_cone 独立审查、非分离 frontier 的原证明/程序未在任何已观察分支中找到。保留可读材料，按真实缺失范围标注。
- 世界新颖性、外部同行评审均未认证；本轮整理没有将其补成事实。

[有序权组冻结](research/current/weighted_congestion/weight_bands/ordered_tail_freezing.md)新增依分组的结构存在界与两权级精确参数限制：即使最佳分组，潜在尾部参数也不能全类统一。[DAG端点泄漏预算](research/current/weighted_congestion/polynomial_curvature/dag_low_leakage_budget.md)给任意DAG指定检测系统的可行充要条件；固定泄漏的辅助源门槛仅有平方根量级。下一步须超出这些潜在参数和检测合同；主目标不变。

新增[两权类别双排序混合势](research/current/weighted_congestion/weight_bands/two_weight_order_blend.md)：全局仅两权时，任意cohort人数/权比均有平方根次数存在界；完整一般证明和独立攻击已核对。真正下一步是多权扩展与共享乘子控制，不把两权范围升级为全类。

[循环窗口复制的真实近d改善环](research/current/weighted_congestion/cyclic_clone_improvement_cycles.md)将旧可分势障碍提升为任意全局全边下降势障碍，仍有全空精确PNE。[共同幂混合最小点障碍](research/current/weighted_congestion/common_power_mixture_obstruction.md)另直接排除指定连续目标族的全部最小点。全类存在性仍OPEN；下一步须选择改善步或构造超出这些目标族的全局选态，不能把循环当无均衡。

[有限可动权类的三角排序势](research/current/weighted_congestion/weight_bands/finite_weight_class_potentials.md)已给A_(d,k)隐式界，固定k为d^(1−1/k)，任意固定背景精确吸收、k个R窄簇损失R^d。d≥16且k≤ln d/lnln d的明确子类达到2d/ln d；无界可动类别时A趋d，唯一全类题仍OPEN。真正前沿已收缩为无界可动权类的选态桥或全状态增长反例，不再把固定背景或仅两类稠密cohort当未解接口。

## 其他长期资产

设施选址保留共同目录双设施尖锐界、复杂度边界、任意设施数因子 2 存在性与有限构造；一般位多项式构造继续开放。顺序客户吸引保留真实完整 SPE、结构类福利界和失败桥，一般半覆盖继续开放。它们分别从根 README 的模型表进入，无需当前拥塞研究者先通读。

## 持续施工与保存

按 [GROWTH](research/GROWTH.md) 先固定 claim 再落正确目录；完成可复用阶段内容和相应核验后立即 checkpoint 到 main，不创建研究分支。候选可以按候选保存。公屏可自由研讨有启发的未完成 idea、卡点和合作问题，不要求先成稿或审查；致命反驳及时核查登记。普通排错和逐轮日志无需强制汇报或入库。

根 README 保持稳定地图。本文件只呈现现在，过程提交留在 Git 历史。具体文件状态、来源和冻结证据分开登记，见 [仓库工作程序](research/REPOSITORY_GUIDE.md) 与 [逐文件索引](research/weighted_congestion_frontier/FILES.md)。

研究读取现从[按问题分流的总目录](research/README.md)进入，各专题按证明链组织；[中文资产总目录](research/CATALOG.md)登记具体文件名、作用和状态依据。现行数学审查按模型归位，投稿旧判断从历史来源追溯，旧路线用固定 Git 版本恢复。命名与导航整理没有新增或升级数学结论。

已审新边界：[择证循环支撑](research/current/weighted_congestion/template_certificates/stationary_selector_obstruction.md)中单位速度平稳dual无界损失，仿射按移动者权重有显式dual，仅支撑recurrent states等价全模板αFIP；一般存在路线不应无证增加此要求。[有向分叉强迫割均衡](research/current/weighted_congestion/directed_fanout_forcing_cut.md)在UF下对异权light/多出侧/自环给α≥T_d全反位PNE。真正未解是全类统一dual估计或新全状态primal；可判别的下界逃逸点为UF失败、侧资源多hub共享及动作副本非对称，当前无闭合机制。

[阶跃DAG极值幅度的多项式全入状态](research/current/weighted_congestion/step_dag/polynomial_extremal_all_in.md)已直接控制真实多项式成本：不要求低漏/平台保真，幅度(N)下d≥16给4√(d/ln d)状态。全类题仍OPEN；当前最具体新缺口是任意卫星幅度如何归约或怎样选择其他稳定light集合，不能只改变已锚定费用形状。
