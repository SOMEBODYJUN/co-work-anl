---
id: customer-attraction/pb-standard-fractional-plateau-two-scalar-audits-and-four-level-report
kind: computation
type_tag: 计算
title: PB标准分数平台双标量审计与四层报告合同
status: five-originals-fully-read-and-retained; no-current-run
summary: 两个独立标准库实现各有15项不同标量谓词，作者还含字面dummy真值，induction另给四层负载行及两项精确差断言；全报告和非盲于作者正文的读序保全，不把有限标量当全历史SPE或聚合。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round4_general/security/audit_pb_fractional_plateau.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round4_general/security/pb_fractional_plateau_audit.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round4_general/induction/independent_review_pb_fractional_plateau.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round4_general/induction/independent_check_pb_fractional_plateau.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round4_general/induction/independent_pb_fractional_plateau_checks.json
---

# 五原件与数学合同

作者2395B程序/1679B完整JSON，induction 4908B审查MD/3320B程序/3412B完整JSON，共15714B均实际normal全文，SHA/size/blob逐件核。当前只作代码、全字段及解析证明比较，未导入或执行任一源码，未生成新报告/stdout/exit-code。此前7303B作者主稿已完整清洗，本批不是靠它的15/4摘要代替原件读取。

固定[PB标准分数平台](../反例/PB标准分数鞍点的真实前三步平台--反例.md)的原模型及旧完整子SPE：r2475、k3、d20、q12、块数B=2063、H100000、M10⁹。每段B个12客户R块和两个1200000客户D块，regular目录逐段Cartesian，另有全singletons。R背景11客户M/1客户M+1，D背景HM。此时
\[
 f(c)=11/(M+c)+1/(M+c+1),\quad g(c)=1200000/(HM+c),
\]
\[
 L=3(r-1)/B=7422/2063,\quad F_R=f(1+L),\quad F_D=g(1),
\]
\[
 \Delta=d(F_R+2F_D),\quad u=3df(3),
 \quad s=d[f(1+3r/B)+2g(r+1)].
\]
HR=[11/(M+1+L)²+1/(M+2+L)²]/B，HD=1200000/(HM+1)²，κ=3dHR。δ_r的竞争质量为r−1，不混extra质量r的7425/2063，也不混整数安全值v。

真正全目录鞍点需query支持F_R<F_D、singleton查询上界，以及背景负梯度HR>HD、各singleton方向<κ。前三次真实F前后，静态层j0..3的竞争质量r−j−1，hot新增j，再用θ_j=3(L−j)/(r−j−1)恢复每个客户分母。概率/边际合法性及凸KKT的普遍步骤由上述正式证明和本审查MD承担，程序只核固定参数的具体标量，不枚举所有目录行动。

# 原审查读序：独立于实现，不是未读作者证明

4908B审查开头明确：已经阅读作者主稿、PB完整构造/全部历史证明及自由分数原定义；**未读取或导入作者审计脚本及输出**，随后从定义重构，再用自己的Fraction代码核标量。因此这是非盲于作者正文的内部数学审查；其代码独立性不等于盲审、外审或新颖性认证。

它给出完整上下界：q*均匀三R给query cap，p*均匀一R加两D给凸目标J(q)，负梯度为−(r−1)H_A。q*支持H_A最大κ且所有singleton方向较小，故任意q有∇J(q*)·(q−q*)≥0，J(q)≥Δ，从而δ_r(b)=Δ。它另逐客户重构j1..3的合法Cartesian分布，核M/M+1两层，不只拼客户边际；嵌入方向给反向界。

对完整SPE，该审查只重核旧G/P/F和regular/singleton保底及Greedy尾计数；明确不重新证明巨量全部历史。背景合法、已覆盖全部客户、可能离轨，不转根/聚合/half反例。其末尾“15项/4行通过”是这份原实现和冻结报告的历史状态，当前不添一次成功。

# 两代码的实际入口、依赖和写盘

两者仅导入fractions、pathlib、json，无外部输入、作者模块、第三方优化器、随机数或浮点认证，也没有主函数guard或argparse。函数/参数/谓词、断言、写盘和stdout全在顶层；导入或附`--help`也会执行，不能作安全只读帮助查看。代码没有构造48495120个客户对象、巨大目录或SPE树。

| 实现 | 实际路径与输出合同 |
|---|---|
| 作者2395B | `Path(__file__).with_name('pb_fractional_plateau_audit.json')`，在该路径覆盖完整报告；随后stdout只给5字段摘要：all_checks_pass、L、theta、delta_minus_u、local_chain_D |
| induction3320B | 先`HERE=Path(__file__).resolve().parent`，覆盖该真实目录中的`independent_pb_fractional_plateau_checks.json`；stdout只给6字段摘要：status、scalar_checks、plateau_rows、L、Delta_minus_u、theta_j1 |

二者write_text不拒绝已有目标，不写当前工作目录，写盘成功后才print；均indent=2并末尾换行。作者不resolve而induction resolve，因此经符号链接启动时目的路径解析不能笼统称同一合同。没有异常捕获。当前未执行，冻结输出未被覆盖，原stdout也未作为本批新取得证据。

作者以Fraction别名F，块数名Q；induction以Fraction别名Q，块数名B，避免二者同名。作者定义f/g为Fraction再除，induction以有理分母直接构造Fraction；均保持有理算术。作者参数表含t=10，但后续谓词不使用t或f(10)；induction参数表没有t，P/F条件在代码中直接写10。

# 作者15个谓词：没有旧PB全历史认证

θ=3(L−1)/(r−2)，hot=θ/3、outside=(3−θ)/(B−3)。完整checks如下，原JSON全部为true：

| 作者字段 | 实际条件 |
|---|---|
| query_best_uses_one_real | F_D>F_R |
| gradient_best_uses_three_real | HR>HD |
| regular_query_beats_any_singleton | Δ>1/(M+1) |
| max_regular_gradient_beats_singleton | κ>max{1/[B(M+1+L)²],1/(HM+1)²} |
| delta_beats_old_security_lower | Δ>s |
| old_security_lower_beats_actual_u | s>u |
| delta_beats_actual_u | Δ>u |
| child_mixture_probability_valid | 0≤θ≤1 |
| hot_load_preserved | 1+(r−2)hot=L |
| outside_load_preserved | (r−2)outside=L |
| dummy_load_preserved | **字面True**，没有数值表达式 |
| three_prefix_copies_also_feasible | L≥3 |
| all_three_mixtures_valid | j=1,2,3逐项0≤3(L−j)/(r−j−1)≤1 |
| all_three_hot_loads_preserved | j=1,2,3逐项hot累计等于L |
| all_three_outside_loads_preserved | j=1,2,3逐项outside累计等于L |

程序一个`assert all(checks.values()), checks`之后才写报告。dummy不被竞争主题选中需要数学构造说明；该字面True不是另一次计算认证。三个all项只遍历给定j，不生成主题分布或枚举子策略。作者程序未重核旧PB的G/P/F，也未断Punish人数界或singleton树补齐；这些依赖继续由旧完整证明负责。

# induction15项与四层行：检查域有交有别

induction的checks也恰15项，但不能按同一个“15”认为完全相同或全部更强：

| induction字段 | 实际条件 |
|---|---|
| query_regular_one_real_strictly_best | F_R<F_D |
| query_singleton_real_M_below_Delta | 1/(M+1+L)<Δ |
| query_singleton_real_Mplus1_below_Delta | 1/(M+2+L)<Δ |
| query_singleton_dummy_below_Delta | 1/(HM+1)<Δ |
| gradient_three_real_strictly_best | HR>HD |
| gradient_singleton_real_M_below_kappa | 1/[B(M+1+L)²]<κ |
| gradient_singleton_real_Mplus1_below_kappa | 1/[B(M+2+L)²]<κ |
| gradient_singleton_dummy_below_kappa | 1/(HM+1)²<κ |
| strict_Delta_above_s | Δ>s |
| strict_s_above_actual_u | s>u |
| oldPB_greedy_scalar_G | g(r)>2f(1)−f(2) |
| oldPB_punish_scalar_P | f(10)+(d−1)f(1)+2dg(r)>d[f(2)+2g(1)] |
| oldPB_fill_scalar_F | 3f(3)>f(10)+2g(1) |
| oldPB_singleton_strictly_dominated | dq/(M+r+1)>1/(M+1) |
| oldPB_tail_no_hot_revisit | r−3<2(B−3) |

作者用更大的统一singleton查询上界1/(M+1)，induction分实际三个分母；作者max-gradient一项由两个最大类别支付，induction展开为三个类别。后者额外重核G/P/F和uniform regular保底，但没有重建水位/再次偏离或检查全部旧PB计数。尾项只给一个足够上界，不生成Greedy路径或单独断其填零下界。

induction随后循环j=0,1,2,3，每行算mass=r−j−1、θ_j、hot/outside边际及两个总负载，逐行断四个布尔条件：概率在[0,1]、至少三个不同outside可选、总real主题质量恰3、两个累计负载都等于L。完整原行如下：

| j | mass | θ_j | hot边际 | outside边际 | hot总负载 | outside总负载 |
|---:|---:|---|---|---|---|---|
| 0 | 2474 | 9/2063 | 3/2063 | 3/2063 | 7422/2063 | 7422/2063 |
| 1 | 2473 | 16077/5101799 | 5359/5101799 | 7422/5101799 | 7422/2063 | 7422/2063 |
| 2 | 2472 | 4/2063 | 4/6189 | 1237/849956 | 7422/2063 | 7422/2063 |
| 3 | 2471 | 3699/5097673 | 1233/5097673 | 7422/5097673 | 7422/2063 | 7422/2063 |

各行四布尔在原JSON均true。j0的“至多一个hot”混合与作者root均匀三R不是相同主题分布，但边际相同，δ只看分数客户负载，不存在冲突。j0..3是四个静态层；真实u/F节点只有前三个j0..2，不能借第4行称第四位也选F。

四行断言后，induction断全部15项，再用代码中硬编码的两个完整Fraction断Δ−u和s−u恰等指定数。摘要仍只计15个checks及4行，没有将逐行4项或两项exact-equality揉成全树激励次数。没有为原模型提供一个参数组以外的新普遍福利定理。

# 全部报告字段与精确值

作者完整报告有12个顶层字段：parameters、checks、L、theta、delta_r_b、actual_first_u、delta_minus_u、local_chain_D、real_query_discount、dummy_query_discount、real_gradient_minus_dummy_gradient、scope。参数8项含t。induction报告有14个顶层字段：status、author_audit_imported、parameters、customers、L、Delta、u、Delta_minus_u、s_minus_u、F_D_minus_F_R、H_R_minus_H_D、checks、plateau_load_checks、scope。参数7项不含t。

`author_audit_imported=false`是原报告字段；实际induction原代码也只有上述标准库导入，未调用作者实现。这不变成当前重新运行的独立性事件。customers=48495120只是参数计数式，不是已展开客户或策略数。两份scope均明确继承PB完整SPE、不是root/aggregate/half反例；旧root逐人待机制状态按后来银行反族区分，不改冻结字面。

两报告共同数值的字段名虽有大小写差，以下字符串完全一致：

| 数学量 | 完整精确值 |
|---|---|
| L | 7422/2063 |
| Δ | 15321488532301272834506953626319 / 21279845216955608346116069553955476639 |
| u | 180000000705 / 250000001750000003 |
| Δ−u | 253635774167992828702040109522630428194 / 231302667020810055653950767176470257283490990439844779 |
| HR−HD | 1031871770261959213793005082273595501735155721971772865847 / 181132724983035392816739446827236838660725596706651312596277712136669894528400 |

作者另外完整给F_R=51071628281626319/4255969043391079109532780、F_D=1200000/100000000000001、θ_1=16077/5101799和局部D=−(Δ−u)。induction另外给
\[
 s-u=\frac{655518746053822970420433555247437051305}
 {604541061548383275389777051408169916255944671102717364},
\]
\[
 F_D-F_R=\frac{23906611959811054373681}
 {425596904339112166922321391079109532780}>0.
\]
全参数、原15字段名及四行11个字段都保在两原JSON，并在[全字段绑定](../../tools/evidence/fractional-saddle-author-and-induction-audits-five-primary/report-field-binding.json)中原样映射。这里只比较原字符串/结构，不把重新解析JSON冒作Fraction重算。不同schema、断言域与输出合同决定两程序/两报告分别retained，不判字节duplicate。

# 当前处置及后续边界

4908B审查的定义级上下界、真实读序及三F分布比较integrated到本计算和已有标准平台；两代码/报告功能和全部字节retained。作者7303主稿此前只保15/4声明，此次五原补齐真实实现/报告；不回写旧冻结包的“当时未取得”时序。

标准平台前三个局部额D<0不意味着r人总利润为负。已有标准平台正文把固定U>rΔ的直接解析补核明确标成当前人工证明；这两旧报告都**没有U或aggregate_balance字段**，不能把那个补核倒填为旧程序结果。R11 extra报告的较小Δ_+正余额也不能代本Δ付款。当前没有一般聚合或half反例、外审、新颖性声明或新的全模型扫描。

本批actual9XB全9claim pushed/synced 413fb760a46bc7476f514dd55bcec041cc4db103，只有本5源primary，其余4不done。这个新raw确为synced，不能拿前19WY或26WV的needs-attention/proof改写它。Worker无Git/claim/网络/凭据，数学程序0运行；精确原件、owner、全9raw和结构检查见[证据](../../tools/evidence/fractional-saddle-author-and-induction-audits-five-primary/README.md)。
