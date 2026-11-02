---
id: customer-attraction/r7e9-eight-customer-strong-iid-exact-certificate-and-aggregate-entry-contracts
kind: resource
type_tag: 资源
title: 八客户强iid精确证书与聚合入口的版本合同
status: complete-five-primary-full-read-original-verifier-replayed-once
summary: 保R7e9八客户强iid唯一势最大者的完整证明、原Q[t]核验器及两个同字节报告；聚合README的数值保存点和旧OPEN按后继分域纠正，不新造实例或六人反例。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/aggregate_security/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/aggregate_security/strong_iid_failure.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/aggregate_security/strong_iid_failure_exact.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/aggregate_security/strong_iid_failure_verified_v2.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/aggregate_security/verify_strong_iid_failure.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/aggregate_security/README.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/aggregate_security/strong_iid_failure.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/aggregate_security/strong_iid_failure_exact.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/aggregate_security/strong_iid_failure_verified_v2.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/aggregate_security/verify_strong_iid_failure.py
---

五主源分别5166、4208、6436、6436、4662字节，共26908字节，均全文实读并核size、SHA256和Git blob；它们在两个冻结提交各自同字节。[原件清单与重放](../../tools/evidence/r7e9-aggregate-strong-iid-primary/README.md)保全部定位。强桥的数学已经存在于[完整iid反例](../反例/独立同分布福利支付--反例.md)；本页保存这一不同原证明与实现的完整合同及聚合入口的时态，不把八客户输入再算一个新反例。

## 所反驳的桥与完整单位客户游戏

共同有限非空目录、有限单位客户、单位提供者依次观察全部有序行动，客户在最终覆盖者间均分。所有离轨历史、重复动作和任意平局保留；一般模型允许空主题、零客户及同覆盖异标签。本例恰有三人、八名不同单位客户和四个两两不同的非空主题，不依赖额外边界约定。

用互不相交的客户块A={a₁,a₂}、B={b₁,b₂,b₃,b₄}及私客c,d，置S₀=A、S₁=B、S₂=A∪{c}、S₃=A∪{d}。按主题标签兴趣分型是mask重数{2:4,4:1,8:1,13:2}；重数表示不同单位客户，不是权重。根选0，第二人恒选1；末位全部16有序历史如下：

| 首 / 次 | 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|
| 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 2 | 3 | 2 |
| 2 | 1 | 3 | 1 | 1 |
| 3 | 1 | 2 | 1 | 1 |

末位各历史的最优收益表为((4,2,4,4),(2,3,2,2),(4,2,4,4),(4,2,4,4))，指定动作逐格达到。固定这份真实后继，第二人四种首行动后的四候选收益依次为(1,2,2,2)、(2,2,2,2)、(1,4,3/2,2)、(1,4,2,3/2)，规定行动1均最佳。根改0、1、2、3后的真实叶依次为011、112、213、312，根均得2。故全部1+4+16=21节点均最优，构成完整纯SPE；84项含自身比较中有21项自身、63项不同动作比较，未将平局删去。实际011的收益为(2,2,2)，W=6；123覆盖全部八人，故OPT₃=8。

比较量Z₃是三人静态均分游戏**最大期望调和势**处的三次独立抽样覆盖。它不是任意iid分布的覆盖、最大iid覆盖，也不是真正静态安全值。原稿明确用指定势最大者，下面还证明该分布本身唯一；一般值唯一性见[静态iid基准](../定理/静态独立同分布安全基准--定理.md)。

## 唯一全局最大者与精确严格分离

三次独立命中概率s的单客户调和势期望为
\[
f(s)=3s-\tfrac32s^2+\tfrac13s^3,\qquad
f'(s)=3g(s),\quad g(s)=1-s+s^2/3,\quad f''(s)=-3+2s<0.
\]
因此F(q)=4f(q₁)+f(q₂)+f(q₃)+2f(q₀+q₂+q₃)凹。若q₀>0，将一部分质量移至q₂保持共有A客户的命中概率，却严格提高私客c的势（f'>0）；所以每个最大者q₀=0。在该面，三个私有坐标的严格凹项保证F严格凹，最大者至多一个。

令s=(√669−23)/14、P(s)=7s²+23s−5=0，取q*=(0,1−2s,s,s)。P在非负半轴严格递增，且P(1/5)=−3/25、P(11/52)=483/2704，所以1/5<s<11/52<1/2，三个支持概率均严格正。面对两个iid q*对手，纯查询收益为
\[
U₀=2g(2s),\quad U₁=4g(1-2s),\quad U₂=U₃=g(s)+2g(2s).
\]
模P的有理运算给U₁=U₂=U₃、U₂−U₀=g(s)>0。梯度是3U，故对任意单纯形q，凹函数的支撑平面给
\[
F(q)\le F(q^*)+\nabla F(q^*)\cdot(q-q^*)\le F(q^*).
\]
这证明q*是唯一全局势最大者，而非仅报告浮点对称Nash。源MD中P(1/5)后的字面“qquad”仅是排版瑕疵；此处保正确算式。

在支持内等收益及收益守恒下
\[
Z₃=3U₁=\frac{108-312s}{7}
=\frac{4344-156\sqrt{669}}{49}.
\]
独立覆盖式4[1−(1−q₁*)³]+2[1−(1−s)³]+2[1−(1−2s)³]给相同表达。于是
\[
Z₃-6=\frac{312}{7}(11/52-s)>0.
\]
等价平方证书是675²−26²·669=3381>0；近似6.307237698…只作显示。该一个完整SPE已足以否定全称W≥Z₃，不声称此游戏全部SPE均低于Z₃。

与旧参数r=(30−√669)/7的关系是r=1−2s，7r²−60r+33=4P(s)，所以这里的Q[s]与[其他原审计的Q(√669)及Q[s]](八客户iid原审计的两种二次域与完整策略合同--资源.md)是同一Nash的换基，不是不同游戏或独立数值发现。

## 真安全值、弱桥、half及总债的准确范围

真正安全值使用两个合法竞争主题槽，竞争分布Q在看到当前查询实现前固定，可任意相关：
\[
v₃=\max_p\min_{B\in\{0,1,2,3\}^2}E_p\sum_{x\in S_a}\frac1{1+c_x(B)}.
\]
取p=(0,15,4,4)/23，十个无序竞争对的期望查询收益按组是00:220/69，01:46/23，02/03:214/69，11/12/13:44/23，22/33:212/69，23:208/69，均至少44/23。反向Q(11,12,13)=(3,10,10)/23给四纯查询收益(26,44,44,44)/23。因此匹配上下界v₃=44/23，且W−3v₃=6/23>0。

s>1/5>12/65给Z₃<36/5，所以本例还满足W>(5/6)Z₃；half余额2W−OPT₃=4。八客户例只反强iid桥，弱iid需另用[完整花瓣反族](../反例/独立同分布福利支付--反例.md)，真正W≥mv_m也未由这些例子反驳。不能把三人辅助支付桥失败写成六人half反例。

原MD另称强桥等价于根全路径总债非正。其精确意义由[残余iid值与租金](../定理/合法前缀残余独立同分布价值与租金--定理.md)承担：每个实际前缀h的残余势Nash支付Z_h，终端Z=0；当前真实终局利润u(h)，D_h=Z_h−Z_(hσ(h))−u(h)。沿实际路径望远镜得ΣD_h=Z₃−W>0。这里不曾求出每个节点Z_h或D_h，也不从总债正声称所有节点债正；有背景的Z_h是剩余玩家支付而非完整覆盖。

## 原程序、两个冻结报告与一次实际重放

[4662B原程序](../../tools/evidence/r7e9-aggregate-strong-iid-primary/original/93260d2d048c8485966d/verify_strong_iid_failure.py)只用标准库。它将八名客户按名称分别展开，从全部有序历史跟随同一action/finish规则，对每候选动作重算真实后继。utility在所选主题每名客户上用Fraction均分；另穷尽4³=64个终局求OPT。它不导入原CCE证书、规范SPE求解器、LP或相邻JSON。

二次域实现用有理对(a,b)表示a+bs，乘法约化s²=(5−23s)/7；add/neg/scale/g/cov只做精确有理运算，核支持收益等式、Z=3U与独立覆盖式。它没有通用二次域除法或sign函数；严格号依P的有理根区间和g在[0,1]正、平方差承担。Decimal精度40的sqrt只生成t/Z及差值的显示字符串，不进入任何严格比较。静态安全原始值遍历全部16个有序竞争背景，反向遍历四纯查询；p/Q归一非负亦可由给定分数直接核。

程序的凹性/唯一性主要在注释、报告字符串及本页解析证明中，不能把JSON中“unique q”的字符串当作程序另行穷尽了全概率单纯形。模块顶层会立即核验并打印报告摘要；main guard仅包argparse与可选写文件，所以导入也会执行检查及输出。--output用模式x独占新建文件，不覆盖已有文件；无--output时只打印。stdout省略all_spe_comparisons，而完整输出文件保存全部21节点的规定动作、真实终局、收益与四候选利润。代码本身的输入是写死的八客户策略，不是通用证书reader。

两个6436B冻结文件[exact](../../tools/evidence/r7e9-aggregate-strong-iid-primary/original/93a3d1664358ad847818/strong_iid_failure_exact.json)和[verified_v2](../../tools/evidence/r7e9-aggregate-strong-iid-primary/original/4c154671e1a259346569/strong_iid_failure_verified_v2.json)同SHA256 3ed7326dbc22101e0bb7d54f66c16a6fe6f9503d1a002103df243c1344993923、同Git blob。其字段含输入、actual011/三收益/W6/OPT8、21/84完整比较、q与势定义、唯一性陈述、有理符号说明、40位展示和三项not_refuted。v2是不同路径身份的同字节副本，不是新数值、更强证书或另一次独立审查证据。

本轮对这份原SHA程序在clone外新目录**运行一次**，--output独占生成6436B文件，exit0、stderr0；完整生成文件与两个冻结报告逐字节相同，stdout为省略比较数组的摘要。[实际命令与核对](../../tools/evidence/r7e9-aggregate-strong-iid-primary/replay-result.json)保全。既有check_iid_examples.py及replay-iid.json的84比较/二次域Nash/真安全证书已充分成功，核版本后复用、重跑0；本次原实现回放不冒成新增外审或盲审。

## 聚合README的八项保存点及后继状态

[5166B入口](../../tools/evidence/r7e9-aggregate-strong-iid-primary/original/15defd767fa21087c589/README.md)在2026-10-21报告一般共同目录、全部完整历史纯SPE和任意历史平局，记录强iid已反及真安全/half仍开放。其“未改共享文件/服务”等句是旧工作区当时工作叙述，不是本次状态。八项搜索/实现记录完整保存如下；计数皆为**原README历史报告**，不是本五源新增运行，也不将固定p交替LP冒全局穷尽。

| 原入口 | README历史范围和所报观察 | 证据边界 |
|---|---|---|
| probe.py | (3,6)/(4,6)/(5,7)/(6,7)的135随机完整策略锥，max mv/W=1 | 六named因string seed bug跳过，本次历史计数不含它们；“已修”是源述 |
| leaf_support_probe.py | 六named加130随机锥，max受限mv/W=1 | Q支持所有至多一次偏离叶删除一位所得背景，可混合；大于实际叶/根菜单支持 |
| random_policy_probe.py | (3,4)/(3,5)/(4,4)/(4,5)/(5,5)共1200完全随机形式策略，max受限mv/W=1 | 每锥含全兴趣ray；查询p交替非全局优化 |
| prefix_pair_probe.py | (3,6)/(4,6)/(5,7)/(6,7)的1000随机实例，最小(u₁+u₂)/(2v_m)=1 | 集合值SPE终局与ordered-prefix admissibility；静态LP数值 |
| pair_cone_probe.py | 同四规模320完整策略锥，max2v/(u₁+u₂)=1 | 固定锥/查询探索，不是一般pair定理 |
| structured_pair_probe.py | (4,6)/(5,9)/(5,8)共18形式策略，每份五q/p起点，最大比1 | 尝试先牺牲组再集中，无正见证；五起点不等于穷尽 |
| weak_iid_probe.py | 640随机完整策略锥、1920固定q LP，maxZ/W=1.0239989866135253，弱比0.8533324888446044 | 固定根q/KKT/Γ数值LP，非精确新实例；也不保弱桥现为OPEN |
| extract_leaf_dual.py / one_leaf_dual.json | 一个稀疏数值系数证书，Q只用一次偏离叶删除支持，λ可用更深离轨节点 | 接口例示，不是任意策略的通用流构造 |

各程序、best/weak/one_leaf冻结点的逐函数真实合同及实际核验另见[完整策略安全与首对查询的冻结探针](完整策略安全与首对查询的冻结探针--资源.md)。上表不代其余13源逐源清洗，不认证README计数的所有输入、argv和原环境。

入口的三个next obligations须分别保存：

1. 一次偏离叶删除支持候选：每个真实完整σ是否存在同一个Q，使所有纯查询收益同时≤W/m。若真则有限静态安全对偶给v_m≤W/m；数值阴性没有构造所有σ的Q。本五源及后继iid/PB反例均未否此特定支持候选，也不在此声称当前已证明。
2. 任意合法背景b、r≥2剩余者、每份完整子SPE的首对利润≥2v_r(b)，其中对手r−1槽。若此全称成立，实际路径相邻对分组、背景嵌入v_r(b)≥根v_m以及末位≥根v_m将给W≥mv_m。这个条件推导正确，但**全称前提已失败**：[PB-extra反例](../反例/任意合法背景的前两人额外槽安全值--反例.md)给r2475及合法背景，u₁+u₂<2v_(r+1)(b)≤2v_r(b)，其中extra有r对手槽。其背景已覆盖全部客户，不能把它称根/实际前缀或六人half反例。旧较弱PAIR链u_i+u_(i+1)+(r−2)V_(i+2)≥rV_i与首对加强并非同命题，入口未给本段V的完整定义，不凭名称补造一般定理。
3. 入口建议继续weak iid/full-tree Q，是当时路线。现全称弱iid W≥(1−1/(2m))Z_m已由完整花瓣族否；其有限640/1920阴性不改变该结论。全树真正相关Q与静态v仍为不同对象，强/弱iid失败不自动排除它们。

README开头“weak aggregate static-security”未在这五源中明确给公式，不因同名weak就替成weak iid。其停止individual-security、all-p decorrelation、静态CCE福利、纯静态PNE、actual-deletion-only等旧桥的提醒是来源路线边界，各自命题须按实际正文量词解释；不能拼成“所有静态方法不可能”。[全位置pair候选](../候选/全位置成对安全值候选与有限锥判别范围--候选.md)使用原零背景v_m，不能因任意沉没背景PB失败而宣称已假；[安全最优面SSR](../候选/安全最优查询面的聚合静态无悔预算--候选.md)亦未被本八客户强iid例反驳。

## 来源关系与接续

原MD将输入/策略归于R-6cfe旧八客户CCE稿，并自述“尚未经其他研究员独审”；README写“awaiting parent/independent review”。这保为原时点，本轮已知情对读多个后继证明及成功记录，没有新增外部审查、新颖性、最小客户数认证，亦不继承当年的未见稿身份。[CCE闭包资源](对称iid福利闭包与最低收益有限锥的来源合同--资源.md)另以对称iid Nash属于静态CCE、C₃=544/87>6推出定性强桥失败；本页的显式唯一势最大者与定量Z不依赖CCE LP的最优性证明。

本资源与既有强iid反例是同输入/同完整策略的证明和原程序实现关系；与静态iid定理是定义及KKT依赖；与残余债务定理是恒等式应用；与PB和花瓣反族是旧候选状态纠正，不能变成half反驳边。程序、报告、旧入口本身均是资源对象的证据，未另造三个数学反例ID。一般真正静态安全聚合与恰六人任意完整历史SPE的half仍需各自研究；本五源不提供通用付款。
