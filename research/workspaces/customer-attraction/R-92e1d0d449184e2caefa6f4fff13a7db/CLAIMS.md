# 精确命题身份与状态

Q-CAG-HALF采用共享model.md原全部量词，仍OPEN。本页个人研究登记不自动更新共享canonical数学状态。

## LOCAL-STATIONARY-FULLTAIL-SHARP-v1

- Objects/Domain：r>=2、n=r−1、整数b>=0、有限标签集合、无self非负整数尾路由矩阵M，每列和n，驻留分布π；I_i∈{0,1}为单客户根关联，0<=K_i<=Σ_j M_ji I_j为整数真实尾覆盖。
- Exact statement：δ_i=(nI_i−K_i)/[n(b+I_i+K_i)]，I=K=0按0，Eπδ>=−max_{a,t>=1,a+t<=n} at(r−a−t)/[n(a+t)(b+r−a)(b+t)]。该界在四标签形式菜单对每r,b可取等。b0的L=(1−r/floor((r+1)^2/4))/(r−1)。
- Companion statement：单客户根期望R、尾总收益B满足B<=[n+floor(n²/4)/(b+1)]R，亦有四标签形式菜单取等。
- Assumptions/Scope：仅所写路由与驻留接口；无真实子博弈最优性假设。形式菜单可以填成完整形式策略，不声称SPE。合法极大目录的私有anchor另有其收益，不把单客户取等偷换成全实例取等。
- Dependencies：原均分公式、驻留一阶矩、非负配对。
- Evidence：relay_transport正文与Fraction核验、parent独立配对证明和不导入发现代码的有理核验；path_exchange独立推得乘法界。
- Objections：没有证明负flux菜单可实现SPE；无法用实际W支付跨分支目录并集账单，所以不否定theta、真正安全聚合或half。
- Status：完整解析证明，父独立内审通过；外审/新颖性未认证。后续额外独审以实际文件为准。
- Related files：relay_transport/stationary_defect_sharp.md、parent/stationary_independent_review.md、两目录脚本及JSON。

## CLONE-INCUMBENT-MONOTONICITY-NO（审计case）

- Exact statement：存在CAG-MODEL完整四人纯SPE、仅两个不交主题A大小3/B大小2；实际ABAA中根收益1，而第二人实际历史A改选A并沿同一完整策略执行得到AABB，根收益3/2。故“后继克隆固定主题只能损害原持有者”无效。
- Domain/Quantifiers：存在性反例，全部15有序节点完整定义；玩家/客户单位，允许任意平局。W=OPT=5。
- Dependencies/Evidence：完整输入策略JSON与独立定义级Fraction核验；父重放通过。
- Status/Novelty：小型失败候选审计，不主张全球新颖性，不改变half；一般真实clone分解在正文。
- Related files：path_exchange/insertion_attack/README.md、clone_gain_m4.json、check_clone_gain.py。

## ROOT-MENU-TAIL-SAFETY-PLUS-LAST-NO-v1

- Objects/Domain：原模型三人、四主题、十个单位客户；为每个根行动a任取首项为a的三槽终局Z_a，并按根收益最大选择实际根a*。v_s(b)仍为不观察查询的真正静态s人安全值。
- Refuted Exact Statement：若每枝后继总利润>=2v2(1_a)，且每枝终局的最后行动在其真实二项前缀上最佳，则菜单实际W>=3v3(0)。
- Counterexample：类型{0,1}:2、{2}:3、{3}:2、{0,3}:3；Z0=(0,0,3)、Z1=(1,0,3)、Z2=(2,2,0)、Z3=(3,3,0)，a*=0。根收益(2,1,3/2,2)，尾总(5,6,13/2,5)，v2(1_a)=(5/2,45/16,3,5/2)，每枝末位最佳。W=7，v3=12/5，3v3−W=1/5。
- Evidence：匹配p=(3,0,4,3)/10和Q((0,3),(0,2),(2,3))=(3,1,1)/5；父独立Fraction LP顶点枚举与逐客户核验。
- Fatal SPE objection：根0后倒二选0收益2，改2后末位唯一BR3，改者收益3。故此菜单不能被完整SPE支持。
- Scope：只否定上述必要条件接口；不反驳真正W>=mv、half或现有H_I/G_I递归，后者有额外真实当前行动门槛。
- Status：指定反例精确内部审查通过；无外审/新颖性认证。
- Related files：security_aggregate/tail_security_menu_obstruction.md、audit_menu_obstruction.py、menu_obstruction_audit.json；parent/menu_independent_review.md、check_menu_independent.py、menu_independent_check.json。
