---
id: "unrelated-machines/real-requested-pin-kernel-all-threshold-capacity-and-saturated-value"
kind: "review"
type_tag: "审查"
title: "真实请求pin核的全阈值容量判定与饱和值"
status: "draft-proof-reconstructed; fixed-numbered-pool; finite-q2-audit; source-bridge-open"
summary: "完整保真实singleton请求UM核、精确iff/充分输出、近饱和质量列表与显式近二值；不替原查询模型添加pins或声称NP归约。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/unrelated-machines/R-56ef7110b0a749ac8b85029bd8c6dd61/weighted_requested_pin_kernel_exact_closure_draft.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/unrelated-machines/R-56ef7110b0a749ac8b85029bd8c6dd61/weighted_requested_pin_kernel_exact_closure_draft.md"]
---

# 普通UM核和真实请求

本源逐字嵌入作者稿，root已全文回算，但没有声明先行的独立完整攻击，保持DRAFT，不进入current/可靠Claim。对象与原half-root查询模型分开：请求是**新增真实singleton unit任务**，不能当作后者免费提供的强制义务。

给有限fee顶点W，每v有非空有限标签集Σᵥ，每(v,b)有有限端口Iᵥᵦ，可为空。整数D≥2，δ=1/D，有理0<β<1。每端口p=(v,b,i)给正有理aₚ，逐标签完整预算Σ_(i∈Iᵥᵦ)aᵥᵦᵢ≤1。给实际请求集合Q，每请求p恰加入一个pin。不同名称互异，未列边∞：

| 全部原任务 | 有限端与真实时间 |
|---|---|
| 每端口guard zₚ | Hₚ:β；Aᵥᵦ:aₚ |
| 每p∈Q的实际pin | 仅Hₚ:1 |
| 每标签wᵥᵦ | Aᵥᵦ:1；Bᵥᵦ:1 |
| 每标签、r∈[D]的fᵥᵦᵣ | Bᵥᵦ:1/D；Cᵥᵣ:1 |

每个f只能到同v、**固定原编号r**的C。同v不同标签共享同编号C，不跨v、不重编号。全部未请求guards、全部标签w和所有D枚f仍须执行。令mᵥᵦ(Q)=Σ_(请求i)aᵥᵦᵢ∈[0,1]。W空时全任务空，补dummy机器、OPT=0；以下W非空，有unit w，OPT≥1。

# 全阈值充要条件及边界

给非负有理阈值C：C<1不可能；C≥1+β总可行，把z全留H、w全留A、f全留B，pins占其唯一H，峰≤1+β。中间区域
\[
1\le C<1+\beta<2,\quad
k=\lfloor D(C-1)\rfloor\in\{0,\dots,D-1\},\quad
n_v(C)=|\{b:m_{v,b}>C-1\}|,
\]
的精确判定是
\[
\boxed{\ \forall v,\quad n_v(C)(D-k)\le D\ }
\quad\Longleftrightarrow\quad
n_v(C)\le\left\lfloor\frac D{D-k}\right\rfloor.
\]
不把C<1造成的负floor代入；D−k>0由C<2得。质量恰C−1的标签不计入n，因为其unit w留A可恰达C。

**任意调度的必要性。** 请求H已有unit pin，β+1>C迫其guard实际去A。mᵥᵦ>C−1的标签若w留A就超载，故w在B；B上已有unit，至多留k枚f，该标签至少D−k枚unit f送固定pool。C<2迫每台C至多一unit，只有D台，故所列不等式必要。未请求guards、非强迫w或其他非规范移动只增加非负负载；证明没有假设一打开标签就全部f外送。

**同时充分回填。** 对Sᵥ={b:mᵥᵦ>C−1}按固定顺序，在原[D]中给每标签选D−k个编号集合Rᵥᵦ，彼此不交；判定保证够用。全部pins在H；请求guards去A，其余留H。对Sᵥ标签，w去B，只将R内f送各自C，其余恰k枚留B。其他标签w留A、全部f留B。逐机核：

| 原机器 | 同一份完整调度的负载 |
|---|---|
| 请求H / 非请求H | 1 / β |
| Sᵥ内A | mᵥᵦ≤1≤C，依赖逐标签完整预算 |
| Sᵥ外A | 1+mᵥᵦ≤C |
| Sᵥ内B / 其他B | 1+k/D≤C / 1 |
| Cᵥᵣ | 编号集合不交，至多一unit |

所有原任务和新增pins恰一次，不是逐标签各自可延伸。扫描显式端口/任务/原编号、有理子和/floor/比较即可多项式输出。巨大二进制D若未展开，不声称poly(log D)输出D枚任务。

# 任意实际查询调度给出的有限质量列表

若更大实例含这个核，完整峰C<2调度σ中每H至多一件实际unit查询。删除其他外部任务，把每个已执行unit查询替成同H的一枚singleton pin，保全部z/w/f原位置，负载不增。故在1≤C<1+β时，实际Q(σ)满足
\[
L_v=\{b:m_{v,b}(Q(\sigma))>C-1\},\quad
|L_v|\le\left\lfloor\frac D{D-\lfloor D(C-1)\rfloor}\right\rfloor.
\]
若C=2−ε、β=1−η、0<η<ε<1，分母D−floor(D(1−ε))=ceil(Dε)，所以
\[
L_v=\{b:m_{v,b}>1-\varepsilon\},\qquad
|L_v|\le\left\lfloor D/\lceil D\varepsilon\rceil\right\rfloor\le1/\varepsilon.
\]
这是**近饱和质量标签**的列表大小，不是全部已用标签的大小，更不是正比例源边覆盖。原half-root可只外送左查询，右请求全空，[异权单侧调度](异权双查询收费的完整单侧三半调度--审查.md)正展示该缺口。核不强制两端实际请求。

# 显式饱和请求的实际近二值

q≥2，一个fee顶点，q个标签，D=q，每标签q端口、a=1/q，全部q²端口加入真实pins，β∈(1−1/q,1)，例如1−1/(2q)。每标签m=1。全部guards到A(负载1)，w到B；标签b只外送其fᵦᵦ到原Cᵦ，其余q−1枚留B。所有H只一pin、C各一unit，B峰2−1/q。

反之若1≤C<2−1/q<1+β，所有guards去A、所有w去B，k=floor(q(C−1))≤q−2，每标签至少两枚unit f外送，q标签至少2q件竞争q台C且C<2，矛盾；C<1已排除。故真实OPT恰2−1/q，覆盖任意非规范调度。显式m=q²+3q、n=3q²+q、有限端5q²+2q。

同一个internal kernel若只给**一个标签**的q端口加pins，则只开该标签、全部f到pool，其余标签按未请求模式，OPT=1。两输入internal jobs相同，但pin任务集合不同；这是请求模式的实际值差异，不是某NP源YES/NO归约，且核本身已有多项式判定。

# 本批精确证据与成熟度

源196行完整实读。嵌入作者块SHA `7b273faf03a36276ebd9ac22d398a07acac7cdcc72d76e67c067c2439d7907c0`另核字节，outer源SHA见[清单](../../../../tools/evidence/um-missing-one-pin-kernel-primary/source-manifest.json)。root的已读回算不等于后置独立完整攻击；本轮清洗也不是Exact-first或外审。

本批一次独立Fraction小审计取q=D=2、β=3/4、每标签两端口a=1/2，穷尽16个请求集合×1024份全部internal任务分配=16384完整实际分配，固定pins唯一端；在144个实际峰断点/中点/阈值上核iff，均吻合。全4pins实际OPT3/2，单标签两pins实际OPT1；不是任意q程序证明。无浮点/求解器，旧程序新run0，见[报告](../../../../tools/evidence/um-missing-one-pin-kernel-primary/run-small-exact/report.json)。

仍缺真实source桥：NO须强制多标签近饱和请求，YES须兼容少数标签并付全原任务；不能拿显式近二数值替代困难性。一般UM目标、外审与全球新颖性均未解决。完整[草稿原文](../../../../tools/evidence/um-missing-one-pin-kernel-primary/original/f898a9baa38fb0fd0651.md)保持原字节和DRAFT。
