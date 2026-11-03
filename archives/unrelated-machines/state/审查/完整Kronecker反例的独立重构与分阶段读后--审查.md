---
id: "unrelated-machines/actual-kronecker-reconstruction-and-staged-reviews"
kind: "review"
type_tag: "审查"
title: "完整Kronecker反例的独立重构与分阶段读后"
status: "historical-reviews-reconciled"
summary: "保留先陈述重构、旧作者读后、结构新增读后及最终§7审查四个不同事件；补严LP对偶归一化与零边界，逐项核64行独立表和100任务证书，并确认19492字节审查前缀。"
legacy_ids:
  - "SCRATCH-UM-KRONECKER-SQUARE-COLLAPSE-INDEP-v1"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/actual_kronecker_square_independent_reconstruction.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/actual_kronecker_square_independent_reconstruction.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/actual_kronecker_square_author_read_after.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/actual_kronecker_square_author_read_after.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/actual_kronecker_square_structural_read_after.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/actual_kronecker_square_structural_read_after.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/actual_kronecker_square_final_section_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/actual_kronecker_square_final_section_review.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/private_graft_and_resource_repetition.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/actual_kronecker_product_review.md"
---

# 完整Kronecker反例的独立重构与分阶段读后

本对象整理[完整矩阵Kronecker偶次幂坍缩](../反例/完整矩阵Kronecker偶次幂坍缩--反例.md)及未剪枝 assignment LP 可乘性的四个历史审查事件。它们分别是先看精确对象的独立重构、后来读取旧作者证明、再读新增结构证明、最后核规范§7，不能合并成四次零信息盲审，也不能用早期读后来认证当时尚未出现的结构稿。

数学范围保持两个身份分开：固定八机十任务种子的实际OPT从3/2在完整平方降为1，所有偶次幂仍为1；任意合法非负有理矩阵的**未剪枝**assignment LP满足乘法恒等式。前者由完整实际证书及坐标乘积证明，后者另需有限LP对偶。有限证书、求证程序、拒绝错误输入的软件检查是不同义务。

本轮全文读四份来源，包括独立稿的64行机器表和全部100项任务记录。新做的只有表与已保全JSON的逐项一致性检查，以及最终审查文件的精确前缀身份核对；没有重跑MILP、1024原分配、400边完整检查或四次幂审计。原读序、运行、无standing fatal与独立性均按冻结记录解释，不冒作本轮新历史。

## 1. 四个事件及允许认证的范围

| 事件与来源ID | 当时已经看到的材料 | 实际新增内容 | 不得倒推的范围 |
|---|---|---|---|
| 独立重构；221ea63c6d0986674d81 | 仅收到seed与完整产品定义，原记录称尚未读作者证明或证书 | 从零重建矩阵、另找不同完整调度、解析seed与所有偶次幂、发现正权容量不变量、给64行表 | 不表示不用MILP寻找证书；不自动成为一般LP恒等式的完整审查 |
| 旧作者读后；34e86b9eb2f8c0846c1d | 已完成并冻结前一重构，再收到作者路径 | 全读旧Exact/Proof/checker/作者证书，独立重算作者输入与100项分配，并严格核一般LP域和对偶 | 明确尚未读STRUCTURAL_PROOF及结构脚本 |
| 新结构读后；9906c96ed0d5a9ec774a | 已知原对象与旧作者证明，随后读新增结构稿 | 初态四类任务、SR/RS逆映射、RR缺陷、15不同任务的旧新端与13行余额，另写验证程序比作者现有JSON | 不是新的盲审；没有执行会原位重写作者结构JSON的原脚本；不把有限结构当一般LP证明 |
| 最终规范§7读后；60b386cf5dbd5cc25e1e | 前三事件完成，随后读规范旧版及最终版 | 比较规范15行表与已经核过的结构表，确认两个身份、域修正及来源角色 | 只审§7.1–7.4，未重审§1–6，不覆盖后来§8–9，不是新盲审或外审 |

最终记录提到规范旧版短标6b766，但未给出其完整hash；这里不补造。最终版的完整hash及与后来组合稿的关系在§6给出。

## 2. 独立重构确有完整数学见证

原独立稿把数学记号A/B写成f/e：状态为S_za、资源为R_ty，f_z在同组两状态时间1，e_zat在S_za时间1/2、在R_{t,zt+a}时间1。按z→g、a→l、t→原B的第三坐标重命名，恰是现反例的完整种子；所有64台平方机器、100件有序原任务、400有限端均保留，没有删mixed任务。

其seed下界直接对C<3/2反证：两selector所占状态的两件半单位任务都必须外送；两条不同斜率线有一个共同资源，迫两枚unit相撞。独立稿另给与作者上界安排不同的一份完整3/2调度：f0→S00、f1→S10；e000留S00，e001→R10，e100→R00，e101→R11，其余四枚incidence都留原S。十件任务均执行，两个已选S负载分别3/2和1。

### 完整64行表与已保存JSON的身份

原独立稿按每台平方机器列出实际任务及每项时间，64行合计100件，四类数量分别为ff四件、fe十六件、ef十六件、ee六十四件。全文原表已按原字节保存于[独立重构稿](../../../../tools/evidence/private-tree/kronecker-review/actual_kronecker_square_independent_reconstruction.md)，无需在本审查复制第二份长表。

其声明的独立证书SHA256为cc62a3c385008150e411590240c78ef8c6f6b182d7625552fc1523220ad0e9a3，正是此前保全的[显式标签证书](../../../../tools/evidence/private-tree/actual-kronecker/evidence/certificates/unrelated_machines/actual_kronecker_square_independent_assignment.json)。本轮[表与JSON比较程序](../../../../tools/evidence/private-tree/kronecker-review/compare_independent_table.py)解析原表全部64行及100个任务对，用Fraction比较目的机器、每项时间和逐行负载，结果全部相同，见[新比较结果](../../../../tools/evidence/private-tree/kronecker-review/independent_table_comparison.json)。这是两种记录表达的逐项身份检查，没有重新进行400条资格边核验。

该证书与作者数值证书在同一编号下有29个目的地不同，完整数据与精确核验已在[核心计算对象](../计算/完整Kronecker矩阵与双平方证书核验--计算.md)保存。两个不同证书不能仅凭“不相同”认证发现过程独立；先仅据对象重构、后读作者的顺序依据的是对应冻结记录。

### 正权容量不变量及全部偶次幂

独立稿在读取作者证明之前已记下c(S)=2、c(R)=1、w(f)=2、w(e)=1，并逐端满足
\[
c(i)p_{ij}=w(j),\qquad \sum_i c(i)=\sum_j w(j)=12.
\]
对任何完整平方调度，
\[
\sum_{i,h}c(i)c(h)L_{ih}
=\left(\sum_jw(j)\right)^2=144
=\left(\sum_ic(i)\right)^2.
\]
所有权严格为正，故全部负载≤1时每行必恰1。结构作者稿随后也有相同速度/体积解释；不能把这一观察独占归给某一稿，也不能把不变量当作自动给出可行调度的算法。

平方证书按相邻坐标对相乘，给每个q≥1的完整\(P^{\otimes2q}\)全部任务一个合法目的地，每行负载为q个平方行负载之积1；全selector元组给下界1。完整规模为\(64^q\)机器、\(100^q\)任务、\(400^q\)有限端，最小有限时间\(4^{-q}\)，单系数位长O(q)。这是对显式输出收费，不是binary q下的位多项式生成。

因此固定反例也排除了把\(OPT(P\otimes P)\ge OPT(P)\)或\(OPT(P\otimes P)\ge OPT(P)^2\)当成普遍规则。但它不排特选困难图像上的附加约束，也不建立一般调度算法或困难性源。

## 3. 作者读后补严的一般LP命题

本节来源独有的承重作用，是对原稿“非负矩阵的未剪枝LP可乘”补齐精确域和对偶归一化，而不是只重述平方有限证书。

令机器数m≥1、任务数n≥0，有限处理时间非负有理，每任务可用集合E(j)非空。产品资格要求两个坐标端都有限；即使一边时间为0，也不能把0×∞当作有限端。F(P)为
\[
\min T,\quad x_{ij}\ge0,\quad
\sum_{i\in E(j)}x_{ij}=1,\quad
\sum_{j:i\in E(j)}p_{ij}x_{ij}\le T\quad(\forall i).
\]

### T为自由变量时的严格对偶

m≥1且行负载非负，约束已迫使T≥0，包括n=0。无需额外声明T为非负变量。给各行对偶权y_i≥0、任务列等式自由变量α_j，T自由使其系数必须为零，得到
\[
\sum_i y_i=1,\qquad \alpha_j\le y_i p_{ij}\quad(i\in E(j)).
\]
最大化\(\sum_j\alpha_j\)，消去α即得
\[
F(P)=\max_{y\ge0,\ \sum_i y_i=1}
\sum_j\min_{i\in E(j)}y_i p_{ij}.
\]

各列x的单纯形积紧，最大行负载是有限连续函数，故原初值有限取得；y单纯形紧，有限非空资格下的min目标连续，故对偶最优点取得。有限LP强对偶给相同值。不是说包含未限定上界T的整个原初可行域本身紧。

如果另显式加T≥0，对偶初始约束会是\(\sum_i y_i\le1\)。由于p非负，把不足的质量补到任意机器后每个\(y_ip_{ij}\)不减、各列min不减，所以最优值仍可在单位单纯形达到。这里没有除以F，也没有假设F>0；不能用“最优值正所以归一化”来遮掉零值情形。

### 两个方向及所有边界

原初最优x、u作乘积，每任务对的质量和为1，支撑仍为两个原资格的Cartesian积，每个机器对的负载恰为原两行负载之积，给\(F(P\otimes Q)\le F(P)F(Q)\)。

对偶最优y、z的乘积非负且总和1；因各因子非负，
\[
\min_{i\in E_P(j),\,h\in E_Q(k)}
(y_ip_{ij})(z_hq_{hk})
=\left(\min_{i\in E_P(j)}y_ip_{ij}\right)
 \left(\min_{h\in E_Q(k)}z_hq_{hk}\right).
\]
对全部任务对求和得相反不等式。非负性同时支撑这个min分解和原初负载的乘法上界。

| 边界 | 证明如何覆盖 |
|---|---|
| 有限零时间、零对偶坐标 | 乘法与有限集min仍成立，没有除法或0×∞ |
| F(P)=0或F(Q)=0 | 原初积给上界0，非负性给下界0 |
| 一方n=0 | 产品无任务；原初负载0、对偶空和0 |
| m=1、未用机器、任意∞模式 | 非空有限资格和单纯形论证仍适用 |
| m=0 | 不在域；空单纯形不能暗中沿用 |
| 负有限时间 | 不在域；上述非负min与乘法界不能照搬 |

种子半半原初每行1，S/R对偶权为1/6、1/12，任务贡献\(2/6+8/12=1\)。未剪枝的F因此为1；不把它改称按p≤T删长边的LST值、CONFIG值或整数OPT的乘法恒等式。新增结构审查只验证有限见证，没有取代本节一般证明。

## 4. 新结构审查的具体增量

结构读后是另一个事件：当时读了新STRUCTURAL_PROOF及其脚本、含100项分配与13行余额的原JSON。原记录说审者没有执行会覆盖作者JSON的脚本，而在自己目录另写验证器，按原资格重建后与既有JSON比较。不能把旧作者读后记录中明确“尚未读结构稿”的范围事后扩大。

其逐类攻击有以下实质内容：

- SS层的四台所选机器各由一件AA填满，另外十二台各四件1/4的BB，全部16行初载1。
- SR映射\((A_g,B_{hkc})\mapsto(S_{gh},R_{c,k+hc})\)确为双射：给定\((S_{ga},R_{cd})\)，先定h=a，再唯一解k=d+hc。RS同理由l=b+ga反解，混合任务没有遗漏。
- RR固定(a,c)时，矩阵\(\begin{pmatrix}a&1\\1&c\end{pmatrix}\)行列式为1+ac。仅a=c=1块出现两台对角负载2、两台非对角0，其他60行都是1。
- 十五个任务对不同；表中old必须是初态真正给出的端，而非任取合法端；new两坐标均合法，并逐项重算乘积费用。13台变化为四台各1/2移出移入、五台各1移出移入、两台对角各移出1、两台非对角各移入1，其余51台不变。
- 这是同时替换的最终证书。原初态峰本来为2，既未证明也不需要逐件顺序中间负载≤1。

速度/体积的全行饱和解释与上一独立记录相合。[裸菜单t=2的5/4](../反例/裸笛卡尔菜单乘积的精确反向放大--反例.md)属于另一矩阵，仅用于比较，不是本完整平方OPT1的前提。上述结构数学及完整十五项表已在反例正文保留。

## 5. 软件与证明的不同角色

独立重构并非“完全不用优化器”：原稿明确从零用SciPy/HiGHS MILP寻找另一份二元调度，再用不导入寻证代码的独立Fraction检查器验证。搜索程序SHA为e9fb2ccef15ddb659e3de6d329c5cd6ad39024ffeb0d3b9312c9c4602d067fca；其optimal/success状态不构成数学上界证明。

原独立检查记载重算全部80个种子候选端、6400个平方候选端，确认20/400有限端，再核100实际任务恰一次、每个执行端及费用、64行负载和400端的不变量。作者读后又独立核作者数据，随后实际运行已读作者checker。结构读后则另写程序避免覆盖原JSON。最终规范读后只需解析规范15行表并比对已核结构表，不应记为又做一次盲重构。

原记录提及但本轮未取得原源码的文件包括kronecker_independent.py、verify_kronecker_certificate.py、verify_structural_read_after.py及其旧独立audit输出。实际保全的是四份原记录、已经规范冻结的完整输入/双证书/最终checker，以及本轮新的表比较工具。不能把最终checker冒作这些旧脚本未经修改的字节，也不能因旧脚本未取得而抹去现在可直接阅读、按资格核验的完整数学证书。

正确输入上的数学审查不自动认证错误输入拒绝。后来的负编号、额外行、primal输出作用及稀疏列表规则修正另见[核验器版本与拒绝界限](../计算/Kronecker核验器版本与稀疏输入拒绝--计算.md)。本对象不把旧正确输入运行追认为旧版本已拒绝所有畸形输入。

## 6. 最终§7的准确字节范围

最终审查绑定的完整文件SHA256为6e0f4996e94e5873425d2f29d95be494a60cc5eaf1b62f6e46541df5d5c479da；它在当时覆盖到§7，审者正式数学范围仍仅§7.1–7.4，不重新认证其前缀§1–6。

本轮实际读取后来组合源e5496b330081be45f325，其完整44686字节SHA为e4a4b3a4dd693946da8c52533b85f38c44e434714bfbb04e264fe5a07114449d。取首次“## 8.”标题之前的19493字节，去掉分隔空白并保留一个末尾LF，得到**19492字节**；内部无字节改写，其SHA恰为上述6e0f4996…。已保留[对应旧完整文件字节](../../../../tools/evidence/private-tree/kronecker-review/reviewed_canonical_through_section7.md)及[精确前缀比对](../../../../tools/evidence/private-tree/kronecker-review/version_prefix_comparison.json)。

因此能把最终读后精确定位到当前冻结组合稿的这个前缀。后来§8的完整克隆周期、§9的有界重数接线不在该次审查范围；即使其文字接在同一个当前文件，也没有因此得到旧§7审查认证。最终审查还独立比较了规范十五行与已核交换表，记录来源去重及LP域归因修正；这些不构成额外算法实现。

## 7. 原记录资源与本轮证据

四份原记录完整保存，包含全部原表、hash、先验与缺口：

| 来源ID与原记录 | 字节 | SHA256 |
|---|---:|---|
| 221ea63c6d0986674d81；[独立重构](../../../../tools/evidence/private-tree/kronecker-review/actual_kronecker_square_independent_reconstruction.md) | 8395 | d3c5084f2db5dc7130007f530cde2408f6541fe86ce15f6855fd8fa314fe72a7 |
| 34e86b9eb2f8c0846c1d；[旧作者读后](../../../../tools/evidence/private-tree/kronecker-review/actual_kronecker_square_author_read_after.md) | 5459 | 56bc8917853f48a6cf229bf10daf2800fa7ed6d5c35ac8c62b3ad27e75bf53ad |
| 9906c96ed0d5a9ec774a；[结构新增读后](../../../../tools/evidence/private-tree/kronecker-review/actual_kronecker_square_structural_read_after.md) | 4558 | 1c4b10aded36e95ffab01e09ca5debe80e77aa2ddcd28bac50caf8de8b44c511 |
| 60b386cf5dbd5cc25e1e；[最终规范§7读后](../../../../tools/evidence/private-tree/kronecker-review/actual_kronecker_square_final_section_review.md) | 5067 | e8ef51f7582f9308ffd4f72e463697a60850f7e7f0561a41e0fbef9a532b3b9f |

本轮表比较可以用新输出路径复现：

~~~bash
python3 tools/evidence/private-tree/kronecker-review/compare_independent_table.py \
  --output cleanup/workspaces/Boss3/private-tree/independent-table-new-comparison.json
~~~

它只解析原稿表并与既存证书逐项比较，拒绝覆盖已有结果，没有调用优化器或重新展开完整矩阵。版本前缀比对记录同时给出当前全文、原始前缀与单末换行前缀的字节数及hash，避免只凭相似标题认定版本身份。

## 8. 结论与接续边界

四份记录在其各自范围内共同支持固定反例、全部偶次幂以及单独的一般未剪枝LP恒等式。它们没有为旧公屏曾提到的10机14任务实例取得完整原件，故不认证那份旧实例的具体数值或首次发现；可确认的是当前8机10任务对象、两份不同证书和十五件交换。

本审查不是一般近二目标的反证，不提供NP-hard源，也不认证全球新颖性、外审或论文价值。若继续研究选定困难图像上的乘积，仍需额外源相关一致性，并对每个低负载完整调度建立解码；不能把这种限制免费加入原普通矩阵语义。复用本对象时，应分别引用数学反例、LP域证明、具体代码版本和对应执行记录，保留各自的量词和版本范围。
