---
id: "unrelated-machines/dual-rail-one-exception-fullcube-review-version"
kind: review
type_tag: 审查
title: "双轨指定例外与完整cube精确前沿的版本审查"
status: complete-primary-read-and-scoped-mathematical-reconstruction
summary: "指定端口阈值修辞修补、rho1 arity锐界、全cube任意完整调度精确OPT与趋一NO；保四合同不同外端和历史有限cut范围。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/dual_rail_threshold_soundness_boundary_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/dual_rail_threshold_soundness_boundary_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/dual_rail_threshold_soundness_boundary.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/dual_rail_threshold_soundness_boundary.md"
evidence_manifest: ../../../../tools/evidence/um-next-available-reviews/source-manifest.json
---

# 单例外的准确输入与已修阈值措辞

本页与[scalar/split页](双轨标量与拆分unit的共同调度及锐例审查--审查.md)共同处置主源72273b87376cc8657417。当前主稿全文148行已实际比较，最终SHA069d7ac109263c410b0874e86840d5ad8fb0720b03b4acaae80825c7d11550ee。以下单例外是另一加权模型；完整cube则是归一化scalar的特殊族，分别保留正式身份。

UM-DUAL-RAIL-ONE-EXCEPTION-FLOOR-v1：每轨port内端为非负有理w_e，总W≤1，selector时间1；每clause一scalar外机，全部port外端1/A，整数A≥1全局共同，arity≤2A。给有理ρ≥1。含空轨变量selector停空轨且不外送；其余变量的两条非空rail**各给一枚真实指定exception**，各自满足W−w_e≤ρ−1。两候选可接同clause，仍是不同occurrence。

每变量两exception各给半质量，同clause时合为1。每clause收到的exception incidence至多arity，故半质量≤A。整数容量匹配给每变量挑一个实际exception；只将它外送，selector放它的rail，其余port内留。选轨负载1+W−w_e≤ρ，另一轨≤1，clause≤A/A=1。容量可截变量数，至多变量数次单位增广；空轨、零权port、W=0但非空rail均不需另一虚构exception。

固定指定e的等价式是w_e≥W+1−ρ；允许自由选时才用max_e w_e≥W+1−ρ。W=1时阈值表达式化为2−ρ；W<1时max≥2−ρ是更强充分条件，不能替换固定e。旧版本“只有W=1才等价”字面过强，例如ρ≥2时不同表达式也可同时恒真；最终只修这段说明。原定理一直按指定e假设，没有因此被反驳。审者把最终段换回旧段恢复完整旧hash1a75b459…139e2c，核实仅此一段变化；本轮只保该历史核对，不假称已取得旧scratch原件。

ρ=1时arity2A界锐：两clause、2A+1变量，每rail唯一port内部1，正/负各连一clause、外端1/A。任何C<1+1/A≤2都迫每变量至少一port外送，每clause最多A件，总2A不足。按A与A+1变量分给两clause达1+1/A。A=1同样成立；这是该合同越界例，不是NP-hardness。

# 完整符号cube与精确最优值

UM-DUAL-RAIL-FULLCUBE-EXACT-FAILURE-v1取整数A≥1、d=2A−1，d变量、全部2^d符号clause，每符号轨出现k=2^(d−1)次。沿scalar模型造2d+2^d台机器、d+d2^d任务。A≥2时每个源赋值都有全真d文字clause，连弱阈值d−1也无解；A=1时d=A=1不属于此NO断言。此显式可验NO族不是困难源。

对整数A≤B≤d，令
\[
R_B=\sum_{s=0}^d(s-B)_+\binom ds,\quad r_B=\lceil R_B/d\rceil,
\quad F_B=\max\{B/A,1+r_B/k\}.
\]
其真实全任务OPT恰为min_B F_B，不能把min_B偷改成总取B=A；原审查记录A20时最优B21。

下界处理任意完整调度峰C≥1。若C≥d/A，B=d已有F_d=d/A≤C。否则B=floor(AC)∈[A,d−1]。完整cube允许逐变量翻轨并同步置换所有clause masks，故不失一般性selector都在负轨。把正port全部收回没有selector的正轨，负载恰1≤C，其他机只减负载；没有丢失更优物理解。每负轨最多h=floor((C−1)k)枚内留，一个size-s负文字clause至少内留(s−B)_+枚，因此dh≥R_B、h≥r_B，C≥F_B。

上界固定B建删除网络：每size-s>B clause供给s−B，对其s个变量的边容量1，每变量容量r_B。均匀分(s−B)/s给出有理满流；全变量对称使每变量恰R_B/d≤r_B。整数满流选择真实内留port，其余负port外送、正port内留、selector负轨。每clause恰min(s,B)件外送，全负clause达到B/A。内留总数R_B，各变量≤ceil(R_B/d)，R_B>0时至少一轨达到上整值，R_B=0时selector给1，故实际峰恰F_B。

网络单位增广次数≤R_B≤d2^d，候选B数≤d。这是按显式展开2^d clauses/d2^d ports的输入和输出长度多项式；不是poly(A)，更不是按log A多项式。

# 趋一实际NO族及A3证书

固定负出现后，负文字总数≤A的可选clauses有Σ_(t≤A−1)binom(2A−2,t)≥k/2。每变量各挑k/2枚负port外送，无需协调：这些clause本来至多A负文字。负轨3/2、正轨1、clause≤1，所有原任务完整。

更强地B=A给R_A=(d binom(2A−2,A−1)−k)/2。用S∼Bin(d,1/2)的有限和估计E(S−A)_+≤sqrt(d)/4，得到
\[
OPT_A\le1+1/(2\sqrt d)+1/k\to1.
\]
任意固定1<ρ<2可取A大到此上界<ρ且ρA<d；源连floor(ρA)弱阈值也NO，实际却有C<ρ，否定的是这份具体编码soundness。没有排除相关核心、非归一化跨层负载或其它读出机制。

A3、d5、k16的42机165任务：五个size4负集各缺i，内收(i+1 mod5)的port；全5负clause再内收0、1，其余负port外放、正port内留。负轨内收(2,2,1,1,1)，峰9/8。若C<9/8，前述任意调度正规化使每负轨最多1枚，总≤5；五size4和一size5 clause却要求≥7枚，矛盾。因此真实OPT=9/8。

# 审读范围、有限输出与接续

cover_consistency只审数学，未核规范代码或运行直方图，独立检查A1..100闭式是有限算术。另一审者先按statement重构fullcube，后来把旧scratch§2–5与canonical§5–8机械对照，除编号/Claim/定位句和尾空行外相同；不把这当新盲审。两人都读后核最终§4修句。

根记录cube独立A1..5的6342个cuts、352个breakpoints、10份完整实际证书；cut oracle重建原矩阵和所有负载breakpoints，但未枚举2^(原任务数)份σ。单例外2000随机、597223份实际σ及A1..8越界证书亦属历史记录。root修过空轨不应要求另一轨exception的过强域验证和错误source标签；只这两处，不表示完整公共JSON solver已实现。本轮未重跑这些程序，也未将旧provisional8/5等版本新增为定理。

ST半质量、匹配和流整数性均为经典工具。当前四合同无已给出的standing fatal，只是历史审读结果；本页由上述自足证明保其范围，不以审者人数代证。新颖性、外审、独立论文价值和一般UM主目标保持未认证/开放。
