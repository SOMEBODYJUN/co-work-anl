---
id: unrelated-machines/anonymous-token-degree-four-nonextension-two-schur-review
kind: review
type_tag: 审查
title: 匿名标签四次非扩展的双Schur证据与冻结范围
status: exact-given-point-nonextension; historical-proof-and-replay-scopes-preserved
summary: 区分两个Schur空间、形式kernel负平方与任意原身份扩展不存在；保Exact先行/作者读后/更强affine学习/最终知情读和软件版本，不倒填盲审。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/anonymous_token_label_lift_and_nonextension_review.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/anonymous_token_label_lift_and_nonextension_review.md
---

# 匿名标签四次非扩展的双Schur证据与冻结范围

## 精确反例与两个正性证明

主源5938B全文实读，其新Claim只覆盖home-unit canonical新增§7/7.1–7.7，当前304行全文SHA dd3a012c9e24eb64a6ddc4f8e953ccc787aa27cc8a6945a454af2357d5689fb8。本批实际读该文件112–304行，并完整读后得affine-context稿；原13728B前缀只核SHA d8eeff7d6763b03172f57770021a250782ad796a10a44d1bb4ac62777e7556e9，不重审旧桥/去环/软件状态。

设十个Boolean heads $X_i$恒有$\sum X_i=4$，另有Boolean $Y$。$\nu$是全部210个四元子集的均匀真law；有符号$\beta$为：完全落前半或后半的10个四集各权$1/8$，前后各二的100个四集各$-1/400$，其它零。总权$10/8-100/400=1$，但**不是概率或true conditional law**。令$\delta=1/100$，到总次数四定义

$$Lf(X)=\mathbb E_\nu f,\qquad L(Yf(X))=\delta\mathbb E_\beta f\quad(\deg f\le3).$$

Boolean和四集cardinality ideal到四次成立。X抽象行由$\nu$、Y抽象行由Bernoulli($\delta$)分别给同行矩；这不声称它们有共同真law或已经是全部原任务CONFIG+M2。

$M_\beta=[\mathbb E_\beta X_iX_j]$对角$2/5$、同半非对角$7/20$、跨半$-1/25$。按常数、半符号、两个半内和零空间，其三类特征值

$$D=(8/5,2,1/20).$$

原作者把二次$q_0(X)$扩大为210个子集上的任意函数，令B为子集—点incidence、$W=\operatorname{diag}\beta$；扩大Gram为

$$\begin{pmatrix}I_{210}/210&\delta WB\\\delta B^TW&\delta M_\beta\end{pmatrix}.$$

Schur需$M_\beta-\delta\,210B^TW^2B\succeq0$，后者在三空间的扣项谱为$(5271/100,105/2,5313/1600)$，余谱为$(10729/10000,59/40,2687/160000)>0$。所以实际67维aggregate共同M2确实PSD。

独立55维证明以45维pure-X pair加10维Y-head为指标，在pure-X块上用$A^{-1}$ Schur，扣项谱不同，为
$E=(4932/125,15,453/1000)$，余谱
$D-\delta E=(3767/3125,37/20,4547/100000)>0$。这是不同空间/充分Gram，不因费用谱不同而矛盾。原Fraction审计给67×67 M2 rank55、46×46原标签M1 rank38、232个cardinality检查和45×45逆矩核对；这些是固定构造的历史有限精确证据，不承担任意组的一般证明。

## 形式核失败与任意原身份扩展均失败

取显式$k=r=4,h=0,A=1$，十heads与未动$Y$，前半$s_i=1$、后半$s_i=-1$。两不同原标签的二次多项式

$$Q=Y\sum_i s_i(x_{1,i}-x_{2,i})$$

在不放回形式核下有
$L'Q^2=(2\delta/12)(16-20)=-1/150$，故[一般M1提升](../证明/原任务标签提升的一阶PSD与全语境容量块--证明.md)不保持同样M2。

更强结论不只否定某个人工kernel。任意保全部aggregate次数$\le4$矩的原标签扩展，若满足原任务Boolean/one-hot到四次、每head完整行CONFIG和共同M2，必须有上述证明页的完整head×affine-context $K\succeq0$。取$t_i=s_iY$便得到

$$c^TKc=\delta(16-20)=-1/25<0,$$

等于$4\sum_a L(q_a^2)$，矛盾（四平方和会为$-1/100$）。旧作者另一条证明用标签置换平均恢复下降阶乘矩，同head多原标签的零对矩经M2 null性排除到四次，再得到$-1/150$；两证明都保，不把必要K说成充分扩展条件。

K必须联合head/context。旧Proof(9)的任意固定异context交叉块不能单独称PSD；后得faa5ab完整affine学习给不需同菜单、标签平均、Boolean aggregate的原任务SOS，允许context含本组个别标签。它加强域不追溯为早期Exact-first已盲审的内容；源码原字节保留。

## 普通实例OPT1不等坏点是原见证

native映射只有13机$r,z_1,\ldots,z_{10},y_0,y_1$和6件任务：g仅r用时1；四f在r各$1/8$、每z用时1；y在r$1/2$、在两y端用时1，共48个有限端。g留r，四f各去不同z，y去y0，给峰1，且g迫OPT≥1，所以实际OPT1。

坏匿名点并非完整原作业K2或strong-C2证书；输入本身有完全合法Dirac原M2点。拒该给定aggregate functional不等原实例sound FAIL，不排换点、强表示、部分修矩；更不建立growing-depth gap或一般near2源/decoder。

## 实际先验、冻结先后与原字节

| 实际阶段 | 原来源/范围与不能倒填的独立性 |
|---|---|
| Exact先行 | 审者只收到5a953e…，独立重构091585…先冻结；root完整读145行后才释放作者Proof88904a…。不是此前全无题目知识。 |
| 作者读后 | 审者实际读Proof§1–6后冻6836e7…；root读Exact/Proof及该66行记录。与先行重构是同一链，不能计作第二张盲票。 |
| 后得全affine域 | faa5ab…给直接原任务SOS，root实际全文读；§7.6明示增强，原作者交叉块歧义被澄清，不重写旧字节。 |
| 当前附录 | 作者append7a7079…，root读旧整页/新附录，仅替换pending-final状态/链接成dd3a…；13728B旧prefix逐字不变。root亲核不是独立票。 |
| 最终知情读取 | 审者实际读112–304新§7，旧prefix只hash不重签，冻2ef622…；root读53行最终记录。不是新盲审。 |

主源列七份历史原件的Container/Original SHA均相同：Exact、Proof、Exact-first、作者读后、canonical-actual-read、affine学习及旧作者程序。本批按[provenance-bindings](../../../../tools/evidence/um-review-contracts/provenance-bindings.json)逐路径/SHA对库存核身份，完整64位绑定均保；**未由hash核验扩称重新全文读完这七份历史手稿**。数学承重读域是当前§7与完整faa5学习，旧审查实际过程按其冻结自述保存，不升级外部时间戳或查新证据。

## 软件重放是历史事实而非本批新run

原review记录root全文读两份stdlib/Fraction自足程序，在两个新目录重放；作者脚本按script位置写结果，所以先复制原字节，另只把ROOT一行改cwd后第三目录再跑。三次作者输出同SHA a1140d82f3f1b7cf94dd33611fb66ee290f1cfeccc1d00e51328e1f213c42c0b，独立输出同b3496538d7bf399ea6000838919dca9cfe855c3c3064eb3f2ba3870c053c068a。无seed；第三次只是适配，不是第三份独立数学证明。

旧作者code8cfc38…保原字节，新规范test为f9b1a149ce49fc34d5a86ae3e018c08027081978ea6144efcb31b1cf9a21fd2f，并非审者最初已审版本；独立code01de46cee0e87f0cd19edb2b6bc2cab25501ee106c8d9100c5a631f6dc651497未改。数学审者未读作者code，不代签软件；author_proof_or_code_read=false属于独立程序创建时的先验，root后得知情重放不算新盲审。

本批不复跑这些已处理程序，不冒称generic lifting/SDP后端。有限232/210/67/46只针对该点；一般M1与SOS由证明承担。旧[三JSON审查](匿名令牌非扩展与双见证查询分离三源审查--审查.md)另外有two-witness v2，不能把它的定理范围并入本新ID。全输入共同状态构造、完整label类型PSD、原身份可计算扩展和源相关decoder仍未闭合；外审/新颖性未认证。[原件、实际读域及接续](../../../../tools/evidence/um-review-contracts/README.md)。
