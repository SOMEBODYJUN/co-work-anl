---
id: customer-attraction/star-core-petal-fraction-audit-domain-and-original-report
kind: program
type_tag: 程序
title: 星核花瓣族的Fraction审计域与原报告
status: full-original-code-and-report-retained-no-new-entry
truth_status: finite-original-exact-regressions-and-decimal-display-separated-from-general-analytic-proof
review_level: full-code-report-and-prior-model-theorem-read-current-informed-source-review
scope: 四个小全有序历史回归、245组静态参数与重复n30报告调用、固定n30/K100有理iid端点；不枚举大树
summary: 保标准库自含代码/原报告，解释均衡分摊、最坏private平衡公式、含self计数、静态K1与SPE K2域；70位Decimal/240二分仅显示，原报告不是本轮新运行或全参数证明。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/new_security/verify_star_family.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/new_security/star_family_exact_audit.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/new_security/README.md
---

# 星核花瓣族的Fraction审计域与原报告

5445B原程序所有函数/main及2625B原JSON全部字段、30个分数余量和五个长Decimal字符串全文。两稿MD同先前正常取得的7121/9014B逐字节相同，其完整数学已在[匹配静态安全值定理](../定理/星核花瓣目录的匹配静态安全值--定理.md)落实；本批对两个MD作准确首次primary duplicate，不再次授新星族或新弱iid机制。现[四原件及回执](../../tools/evidence/star-family-original-audit-contracts-primary/README.md)完整保留。

本轮没有导入或执行原程序，没有新Fraction/math checker、DP/LP/SPE/IC或随机搜索。源码与报告的有限检查内容是原有证据；本页理解其真实数学合同，不把读取原status写成当前成功运行，更不补造历史stdout、退出码、耗时或代码版本绑定。一般结论的依据仍是完整解析证明。

## 单位客户输入与真实续局计算

n≥2名单位提供者、K朵花瓣。两客户核H，2(n−1)名B私有客户，K名单独花瓣客户互不相同；A=H、B、C_j=H加自己的私有客户，目录共同、可重复选择。全部客户价值/玩家权重一。[原模型](../定义/共同目录完整历史模型--定义.md)的全部有序历史和离轨平局保留。

程序标签A0、B1、C₁2、C₂3、…、C_K(K+1)。policy在根返回0，其它非末位返回1；末位全B返回2，唯一非B为C₁返回3，唯一非B为其它C返回2，其余返回1。它正是“末位选最小的不同花瓣”控制器，要求K≥2；函数没有自己校验此域。K1时另一标签3不合法，不能因为静态回归含K1就说程序也检查了K1的该SPE。

terminal以实际tuple历史不断调用policy完成；每个偏离用terminal(h+(b,))，随后沿**同一真实控制器**继续，不冻结在轨后继。utility只在玩家实际所选标签已存在于最终z时读取：B得2(n−1)/count_B，A得2/nonB_count，C_j另加1/count_Cj。它按单位客户压缩计数，并非用加权玩家或另一个静态NE模型。对任意没出现在z的行动直接调用utility不属于合法读取域，不能把辅助函数当加入该行动后的收益。

代码仅依赖标准库fractions.Fraction、itertools.product、decimal.Decimal/localcontext、pathlib.Path和json，没有规范均衡库、候选packet、LP或优化器导入。Fraction用任意精度整数有理运算，与前批numpy int64程序的机器范围不同；Decimal只在后面的显示段出现。

## 小实例真正全历史回归的准确计数

exhaustive_small(n,K)遍历depth0,…,n−1的全部(K+2)^depth有序历史；在每个历史算指定行动的真实续局收益，再与全部K+2个候选行动的真实续局比较，包括“偏离到自己”。检查为精确Fraction的gap≥0，失败由assert抛出。原main固定四组：

| n,K | 主题数 | 决策历史数 | 含self行动比较 | self比较 | 真正非self比较 |
|---|---:|---:|---:|---:|---:|
| 2,2 | 4 | 5 | 20 | 5 | 15 |
| 3,2 | 4 | 21 | 84 | 21 | 63 |
| 4,3 | 5 | 156 | 780 | 156 | 624 |
| 5,4 | 6 | 1555 | 9330 | 1555 | 7775 |
| 合计 | — | 1737 | 10214 | 1737 | 8477 |

计数公式为d_n=Σ_(t=0)^(n−1)(K+2)^t，比较数(K+2)d_n。报告四条各有n、K、comparisons、minimum_gap，数目依次20/84/780/9330、minimum_gap均为字符串“0”。因包含self，最小值0不说明所有非self偏离严格或给出独立严格裕度；真正平局及全历史可信性由[完整分类证明](../定理/星核花瓣目录的匹配静态安全值--定理.md)说明。

原报告没有存每个历史的动作或全部IC行。源码的枚举覆盖这些小输入，不能把小参数的数量变成n30/K100巨大树的枚举规模。n30那份完整SPE依据是全历史分类证明，main不对它调用exhaustive_small。

## h_balanced为何是真正最坏private平均

固定静态背景中r个C竞争槽，分到K个花瓣，整数次数q_j≥0、Σq_j=r。query花瓣均匀，private收益是K⁻¹Σ_j1/(q_j+1)。函数1/(t+1)离散严格凸：若两个次数相差至少2，将一个槽由较大移向较小会降低其两项和。故最小在次数只差1的平衡配置。

写r=qK+t、0≤t<K，K−t个次数q、t个次数q+1，原h_balanced正返回

$$h_{bal}(r,K)=\frac{K-t}{K(q+1)}+\frac{t}{K(q+2)}.\tag{1}$$

这对每个整数r≥0、K≥1是实际可达的最小值，不需要枚举K^r个有序竞争元组。重复选择也在q中保留。r<K时化为1−r/(2K)；一般仍有下式，其中u为非负整数：

$$h_{bal}(r,K)\ge1-\frac r{2K},\quad
\frac1{u+1}-\left(1-\frac u2\right)=\frac{u(u-1)}{2(u+1)}\ge0.$$

程序没有处理K0或任意畸形输入，合同仅限上述数学域。

## exact_security的参数域、全部r与原30余量

该函数assert n≥2、K≥1。设D=2Kn+4K+n、s=4K/D、v=2−2/D，p_B=1−s、每个p_C=s/K。背景A可改C而不增加此查询收益；给定C总次数r∈{0,…,n−1}，由(1)得到真正最坏背景下的查询期望

$$A_r=(1-s)\frac{2(n-1)}{n-r}
+s\left(\frac2{r+1}+h_{bal}(r,K)\right).$$

源码另算将private替成1−r/(2K)的elementary值L_r，逐r断言h_bal≥该下界、A_r≥L_r，以及

$$L_r-v=\frac{2r(r-1)[2K(n+1)+r+1]}{D(n-r)(r+1)}\ge0.\tag{2}$$

再算静态Q：全B背景质量α=n/D，其余为B^(n−2)加均匀C；断言query B/C均为v、query A为1+α≤v。它回传D、query_total_C/query_B/query_each_C、value、dual_mass_all_B、三个dual_payoff、逐r的A_r−v、W_minus_n_v共11字段。这是[定理匹配p/Q](../定理/星核花瓣目录的匹配静态安全值--定理.md)的有限实现，不只算一个任意query上界或任意背景值。

原main有限回归为

$$n\in\{2,3,\ldots,50\},\qquad K\in\{1,2,3,10,100\},$$

共49×5=245组。它们不等于“所有K≤5”。每组r有n个检查，共5Σ_(n=2)^50 n=6370个r槽；main随后为报告又调用一次exact_security(30,100)，所以若按main全部调用计是246入口、6400个r槽。原JSON的security_formula_regressions=245准确指有限参数格，而不是全部函数调用数。JSON未逐条存245组结果，只存这个计数和n30/K100一例；这些有限格不替代全n/K的解析证明。K1仅出现于静态格，不能继承K≥2的SPE控制器。

n30/K100原报告完整值为：

| 字段 | 原精确值/身份 |
|---|---|
| D | 6430 |
| query_total_C | 40/643 |
| query_B | 603/643 |
| query_each_C | 2/3215 |
| value | 6429/3215 |
| dual_mass_all_B | 3/643 |
| dual_payoff_A | 646/643 |
| dual_payoff_B、dual_payoff_C | 各6429/3215 |
| W_minus_n_v | 6/643 |

exact_primal_margins_by_nonB_competitors有30个字符串，依r0,…,29排列，全部原字面值已读并留原件。此时r<K100，h_bal恰等于elementary，故这些“primal margins”就是(2)在D6430、n30、K100的值：开头0、0、6203/135030，末项505876/9645。它们是固定query面对背景的静态安全余量，**不是**玩家IC裕度或顺序债务。general proof见定理，原有限报告不扩成所有n/K程序认证。

## 固定弱iid端点、精确下界与Decimal显示

g(n,t)以Fraction计算[1−(1−t)^n]/(nt)，t0分支返回1。weak_iid_witness硬编码n30、K100、s₀1/20，精确算

$$B_0=58g_{30}(19/20)=\frac{116}{57}(1-20^{-30}),$$
$$C_0=g_{30}(1/2000)+2g_{30}(1/20).$$

所有严格断言都在Decimal段**之前**：g私有下界3971/4000、核心下界392/375、和24457/12000，(19/20)^10<3/5，C₀>和>116/57>B₀>120/59；最后确认

$$\underbrace{\frac{59}2B_0-60}_{\text{原guaranteed\_gap}}
=\frac2{57}-\frac{3422}{57\cdot20^{30}}>0.\tag{3}$$

为何s₀比较能否定真正凹势最优iid q*的弱支付桥，依赖[定理中的严格凹/KKT/单调唯一交点](../定理/星核花瓣目录的匹配静态安全值--定理.md)。程序自身没有重新证明这些一般优化事实，也没有将真正静态v换成iid值。

原weak_iid_counterexample九字段为n、K、unit_customers160、W60、exact_B_at_s0、exact_C_at_s0、threshold120/59、proved_strict_weak_iid_gap_lower_bound、numeric_display。B₀/C₀保存为完整大整数分数字符串；lower_bound保存

$$18837575859649122807017543859649122777\ /
536870912000000000000000000000000000000,$$

它对应(3)的**严格正下界**，不是原真正根λ下的实际失败量。大分数完整原值和对象身份均留[原JSON](../../tools/evidence/star-family-original-audit-contracts-primary/source-root/research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/new_security/star_family_exact_audit.json)；本批未声称重新执行该大整数审计。

Decimal段以localcontext精度70、初始[0,1]作240次中点更新：若B(s)<C(s)则lo=s，否则hi=s；末点root=(lo+hi)/2，λ=58g₃₀(1−root)。它只填五个字符串s、lambda_value、iid_total_Z、weak_iid_payment、weak_iid_failure_gap。原显示约为s0.0503421618320140、λ2.035820961645497、Z61.07462884936、弱支付60.05671836854、失败量0.05671836854。

该段没有有向舍入或真根区间的精确符号验证，70位运算下240次中点更新也不自动给出2^−240的严格误差证书；不让末位显示数字承担严格反例。精确严格正性已经由(3)和定理的有限有理端点建立。原long Decimal字符串逐项完整保留，不改写成精确λ或代数根。

## main输入输出、证据及复用

main没有参数解析、没有外部数据文件输入，固定生成四个小回归、245参数格、另一次n30静态值和固定弱iid点。报告根五字段为status、small_full_history_regressions、security_formula_regressions、n30_K100_security、weak_iid_counterexample。status原样是“Independent exact audit; general classification proof in README.md”。它承认一般证明另在README，不能从该status推出未枚举的大策略树已查完。

输出位置由Path(__file__).with_name('star_family_exact_audit.json')固定在代码同目录，写indent2 JSON加换行，并打印同一JSON序列化内容；成功执行时二者的文本合同相同。没有CLI输出路径或随机seed，新增命令参数不在源码读取。报告本身没有历史argv、解释器、原源码SHA、stdio事件或退出码，本轮也不制造它们。当前保存的是原程序/原报告及完整语义，不声称实际生成时已确认某个版本或新主机复现成功。

两个MD的“独立编写/内部审查”是原资料的研究身份；源码确无规范库、作者packet导入，可以确认自含实现边界，不能据此补称盲审先验、外部同行评审或世界新颖性。旧族的m20/m≥41及八客户n3/K2已经在先有正文；全n/K静态匹配式及n30端点已由新定理保全，本页只增加代码和有限证据的准确合同。

[来源、full23原claim和指纹](../../tools/evidence/star-family-original-audit-contracts-primary/README.md)区分两MD的同SHA正常show复用与码/报首次正常取得。旧源码/报告的读取不算新运行；一般分析已充分，本批0原入口、0新数学checker，不机械重演审计。后续若用这些函数，需要保持n/K合法域、真实后继及竞争背景不观察查询抽样的量词；有限回归、静态r检查、iid端点和Decimal显示四类证据不能相互替换。关系为原定理的实现/有限回归/来源联系，正式超图留第三阶段。
