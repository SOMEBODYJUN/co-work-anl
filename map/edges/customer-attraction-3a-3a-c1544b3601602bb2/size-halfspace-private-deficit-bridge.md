# 七极大固定实际路由的大小半空间证书到六人 half：私有缺口桥

作者身份：Boss2，本任务恢复 3A worker；保留前 worker 有效草稿，并以本轮独立实读复核当前源正文与合同。任务 `customer-attraction-3a-3a-c1544b3601602bb2`；当前定义 pin `7a4d5f9b3ace97946884bae4fe78a665f1945a3ae9eea29a8aeef75698e884a2`。本文只组织当前两个已证对象的联合推导，不运行原证书入口、LP、SPE 搜索或成熟 1631 列重建。

## 实际数学结果与原目标核对

**同一六人完整历史纯 SPE，在恰七个不同极大覆盖、固定实际容器路由 `000010` 及 `max_{2≤j≤6}|B_j|≥|B_1|` 的子域内，满足 `W−OPT_6/2≥δN_+−(p_1−min_j p_j)/2`；故私有缺口至多 `2δN_+` 时有 half，`p_1=min_j p_j` 时有严格余量。**

原目标精确 ID 是 `customer-attraction/six-providers/exact-six-full-history-half-cover`。其完整命题量化任意有限单位客户集、有限非空共同标签目录及任意覆盖映射、每份六人完整历史纯 SPE，要求 `2W≥OPT_6`。本文只支付上述严格子域及其中的定量式，不能填写该全称目标的 whole_result；目标继续 open。

## 同一模型、符号和两个源的独立作用

共同模型保留空覆盖、同覆盖异标签、重复行动、零客户和所有有序历史上的任意弱平局。每位单位提供者观察全部先前有序标签行动后选一次；终局客户价值在其全部覆盖者之间均分。完整策略 `σ_i:S^{i−1}→S` 在每个合法有序历史和每个替代标签上均满足 IC。真实偏离后必须沿同一张原 `σ` 在改变后的有序历史续行；不合并同负载历史，不冻结在轨回复，不删任何目录动作。

记根福利 `W=Σ_i u_i=|∪_i cov(S_i)|`。本证明不把非零背景下的剩余利润当成根覆盖。

全目录恰有七个不同的包含极大覆盖集合 `B_0,…,B_6`，各有合法代表标签。每个目录标签固定一个包含其覆盖的极大容器；实际六个位置的容器路由是

\[
\rho=(0,0,0,0,1,0).
\]

实际末位覆盖恰为 `B_0`；前四位置可为 `B_0` 的不同子主题，第五可为 `B_1` 的子主题。同容器不表示动作标签相同。末位极大性来自严格扩张会增加其收益；这不自动推出整个 route 条件，也不推出 `B_0` 基数最大。

定义

\[
V=\bigcup_{j=0}^6B_j,\quad U=|V|=N_+,\quad
X_j=B_j\setminus\bigcup_{k\ne j}B_k,\quad
p_j=|X_j|,\quad p_*=\min_jp_j.
\]

这里“私有”是对七个不同极大覆盖而言，不是对原目录标签而言。完全无兴趣客户仍可保留在 `N`，但不进入 `V`、`U`、`N_+` 或任何 `p_j`。置 `K={0,2,3,4,5,6}`，位掩码 125，`O_K=∪_{j≠1}B_j`。

源 A：`customer-attraction/seven-maxima-fixed-route-size-halfspace-rational-cover-certificate`，v1 / proved，pin `c44c8904f129a2e683da716943182a40587f59d83142a5854349402f60095d0a`。它为同一 `σ`、同一 route、同一固定比较并集支付

\[
|B_6|\ge |B_1|\quad\Longrightarrow\quad
W-\frac{|O_K|}{2}\ge\delta N_+,
\tag{1}
\]

其中

\[
\delta=\frac{18498863000606739639886045305171986828695633123297448847848950678586594650307}
{6762571796424872885022917111161933156201229619283339655506473064817216175091704}>0.
\]

源 B：`customer-attraction/seven-maxima-private-block-objective-and-current-fractional-cover-scope`，v1 / proved，pin `a3aabc5153fae5241aff5fd2adf4612ce9de5a908a63eb92e494afd94051a4ec`。它支付精确静态身份 `OPT_6=U−p_*`，从而支付固定比较并集与真实最优的差额；它自身不提供本 route 的福利下界。两个源须同在一条 ALL 中。

## 静态比较桥及全部目录边界

任取原目录中的六标签比较元组。由于有限非空目录的每个覆盖都包含于某个极大覆盖，可在**静态比较**中逐项扩大到合法极大容器，不减并集。六个容器去重后至多六个，可从七个不同极大覆盖中补成六个，仍不减并集。反向，每个极大覆盖有合法代表标签，故任意六个不同极大覆盖确给一个合法六标签元组。因此

\[
\operatorname{OPT}_6=\max_{0\le j\le6}\left|\bigcup_{k\ne j}B_k\right|.
\]

遗漏 `j` 时，在 `V` 中但不在其余六集合的客户恰为 `X_j`，所以

\[
\left|\bigcup_{k\ne j}B_k\right|=U-p_j,
\qquad |O_K|=U-p_1,
\qquad \operatorname{OPT}_6=U-p_*.
\tag{2}
\]

这个论证只扩张比较元组，没有删掉游戏动作，也没有声称原策略在缩目录后仍是 SPE。非极大子主题保留在原游戏内。别名不增加不同极大覆盖数，历史也不按覆盖合并；每个极大覆盖仍有代表标签。重复标签、重复容器去重后补足即可。空覆盖标签同样有容器。空标签目录不在模型内；零客户或全目录零覆盖时不可能恰有七个不同极大覆盖，而一般原目标在这些边界有 `W=OPT_6=0`。全程不用比率或 `0/0`。

## 未用索引重标扩大的精确大小域

假设 `max_{2≤j≤6}|B_j|≥|B_1|`。选一个达标的未用索引 `j_*`，仅在 `{2,3,4,5,6}` 内统一置换，使该集合成为新 `B_6`，固定 0、1。将极大索引、全目录容器映射和所有客户会员索引一起重标，不改变实际动作标签或原 `σ`。

route 只用 0、1，因此仍为 `000010`；`K` 是除 1 外全部索引，因此 `O_K` 不变；`p_1` 身份保持，其余私有块仅置换，`p_*` 不变。新标号满足 `|B_6|≥|B_1|`，故可应用源 A。无需新数值扫描，也不要求特别对待 6 的原权重在旧标号逐项不变。不能交换 0 或 1 来强迫这个域条件，否则可能改变实际末位、第五路由和被遗漏的比较集合。

## 两源 ALL 的完整推导

在以上同一输入实例、同一完整 `σ` 和同一合法固定容器路由下，(2) 给

\[
\operatorname{OPT}_6-|O_K|=p_1-p_*\ge0.
\]

应用上述未用索引重标和 (1)，得到

\[
\begin{aligned}
W-\frac{\operatorname{OPT}_6}{2}
&=\left(W-\frac{|O_K|}{2}\right)
-\frac{\operatorname{OPT}_6-|O_K|}{2}\\
&\ge\delta N_+-\frac{p_1-p_*}{2}.
\end{aligned}
\tag{3}
\]

这条定量式没有额外开放前提。若给定输入另满足 `p_1−p_*≤2δN_+`，则 (3) 右侧非负，得到 `2W≥OPT_6`。等号边界保证 half；若缺口严格小于该阈值则得到严格 half。`p_1=p_*` 是特例：此时 `O_K` 最优，并得 `W≥OPT_6/2+δN_+`；恰七个不同极大覆盖保证 `N_+>0`。

route、大小和 private 缺口描述适用的输入子域，不是声称普遍成立而尚欠证明的命题。本边因此为 accepted / unconditional / contribution。不能把源 A 单独改写为一般六人 half，不能把源 B 的静态公式单独当作福利保证。

## 不能省略 private 缺口与其他覆盖缺口

大小条件不推出 `p_1=p_*`。纯集合例：`N={a_0,…,a_6,p,q}`，令 `B_0={a_0,q}`、`B_1={a_1,p}`、`B_j={a_j}`（2≤j≤5）、`B_6={a_6,q}`。每个 `a_j` 私属于 `B_j`，故七者两两不包含、恰为七个不同极大覆盖。此时 `|B_6|=|B_1|=2`，但 `p_1=2`、其余 `p_j=1`；`U=9`、`|O_K|=7`、`OPT_6=8`。此例只否定集合论蕴含“大小条件⇒遗漏最优”；没有给出完整 `σ` 或证明其具有实际 SPE route，不能当作 half/SPE 或源 A 反例。

本桥尚未支付原目标的其余量词：其它实际容器路由；本 route 中 `|B_1|>max_{2≤j≤6}|B_j|` 的互补大小域；route/size 域中 private 缺口超过 `2δN_+` 时所需的额外福利付款；任意数量的不同极大覆盖。七极大不是任意目录到该域的归约。缺口过大时 (3) 仍是正确有符号下界，但不足以推出 half。这些是**本桥**的覆盖缺口，不是反例域，也不表示其它既有路线均未处理其中实例。

源 B 保留的旧错误 `U−p_6` 目标、旧固定乘子 singleton 负列及后来 `k≤2` 分数覆盖证明，与本桥所用静态公式的作用分开。源 A 的十九正权有 18 基础行、1 大小行、0 ASR；其它 ASR/H 失败模板的目标、域和权重不能移来否定本证书。本文不消费这些其它路线的未读承重证明，不新增节点或 follow-up。

## 成熟固定证书复用与本轮实际阅读

本轮恢复 worker 亲自全文读取了当前三份对象合同及相应正文：源 A 证明、源 B 审查、原六人问题；另全文读取共同模型、同 SHA 目标 evidence 中的旧根问题页、证书摘要和原 3070 B JSON 的全部十九个 index/name/有理权记录。源 A 正文已完整给出活动行公式、真实偏离合法性解释、精确恒等式和成熟独立核验合同，本轮按当前精确 SHA 复用该正证书，不重新追读所有被正文引用的旧代码或所有基础引理。另实读源 B evidence 中无私有严格证书的“全部乘子和有理恒等式”完整指定节，确认旧权模板的身份；此节只作完整合同审读，不参与本桥新的正向推导。

源 A 的成熟恒等式为

\[
W-|O_K|/2=\sum_{q=1}^{18}\lambda_q S_q
+\lambda_{\rm ord}(|B_6|-|B_1|)
+\sum_{I,J}w_{I,J}R(I,J),\qquad R(I,J)\ge\delta>0.
\]

1631 是该 route 的完整 compatible 客户列域，不是 1631 个游戏或策略样本。唯一活动 ORD 为 `('ORD',4,(6,1),(1,1))`、权 `13310500/581071327`，其总行确为大小差。摘要给 18 个正基础权、0 个正 ASR 权和1个正 order 权；原 JSON route、K、十九权与最小余项同正文及摘要一致。四个最小列 `(6,16),(10,16),(18,16),(34,16)` 是成熟摘要结果，不称本轮重新逐列验证。

| 输入路径（相对 clone 根） | 本轮读取范围 | SHA256 |
| --- | --- | --- |
| `archives/customer-attraction/state/证明/七极大固定路由的大小半空间有理覆盖证书--证明.md` | 全文 | `a06141db4845abc6f6fb0599ebfa2847d00a5798894da6f2212dc6fe5fc8e351` |
| `archives/customer-attraction/state/审查/七极大单私有块证书目标与当前覆盖范围--审查.md` | 全文；本桥只用精确静态公式 | `b800495e653a5ade48b3c04d9836a78b19d60da47cb8ad7a4826bab0a25f73b2` |
| `archives/customer-attraction/state/定理/七极大无私有关联的六人严格覆盖证书--定理.md` | 仅完整指定节“全部乘子和有理恒等式”；不称全文或重跑3840列 | `a39e77677c19b50584395a100e3fd485ab85551d4f2bae11c45c529ac45133c1` |
| `archives/customer-attraction/subarchives/six-providers/state/问题/六人完整历史半覆盖目标--问题.md` | 全文 | `0626668e7a825108fc0b3699e42394b75b1c2e2a526df220a90d91a02afc8a0c` |
| `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | 全文 | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` |
| `archives/customer-attraction/subarchives/six-providers/问题--问题.md` | 全文，同对象旧根证据 | `21391fbaaa2893fef7b228a345fcf1d7f5c5d1dc8a42cc642d6bfbbeccc7c065` |
| `archives/customer-attraction/tools/evidence/ordered-maxima-single-branch-primary/exact-review/summary.json` | 全文1441 B，δ、计数和绑定 | `4d7ae70b3f3758d965f8664e352159b97ff483379ae6c9020337cae39845e736` |
| `archives/customer-attraction/tools/evidence/ordered-maxima-single-branch-primary/original/b6e38a6404bc19b47b14/exact_branch_audit.json` | 全文3070 B，全部19权及所有字段 | `db1cac116f4161c7f4cebf34fde261613fdca4a699539d6ac4923289cf5db715` |
| `archives/customer-attraction/tools/evidence/ordered-maxima-single-branch-primary/exact-review/all-1631-residuals.json.gz` | 52003 B 原字节指纹；未解压或重播 | `e3103e64a25e109556082313f3ac7ac1638b6cf38f6ba12019238c779b1667ad` |
| `research/workspaces/map-v2/Boss2/recovery-20261112-e8cf4c/wave17-halfspace-bridge-3d-review.md` | 全文，只读独立桥审查；不是本包 asset | `99a5b29e3cefaad6d0122c3696d66704be153b0e2128b1075f4dc3327197a152` |

当前 `research_runtime.load` 返回的三对象完整记录逐项与所供 current-contracts 导出相等，三个 registration pin 与任务 input_pins 全部相等；每个对象的 body/evidence 原字节及指定标题均逐项核对通过。摘要 `input_sha256` 与原 JSON 实际字节相等，`compressed_residual_sha256` 与压缩文件实际字节相等，摘要与原 JSON 的 `exact_min` 字符串相等。没有解压/遍历 1631 残差，没有导入或执行两个有副作用原入口、它们的 `--help`、成熟 checker、LP 或 SPE 求解器。没有把正文引用的代码当成本轮已读代码，也没有把读取独立3D报告当成重新执行其检查。

## author 前当前 canonical 定向排重

本轮 author 前读取当前 `research/registry.json`：SHA `020a2927997479967535eeeaa5e22ec3ad3f136534a302809de218ba920a5a50`，`edge_files` 共 2287。只遍历这份当前清单并按上述三精确端点筛选 source_ids/target_ids，命中源 A 0、源 B 1、目标 Q 8，共9条。命中边的端点、ALL结构、条件、实际作用、explanation 和 contribution/whole_result 字段已读；没有重审它们各自全部源证明。

源 B 的唯一命中为 `cag-a371-fractional-cover-and-correct-opt-pay-two-private-half`，它与9/2分数覆盖源共同支付七极大 `k≤2` 的另一结论。Q 的8条命中分别为固定策略森林证书、SCC商证书、C6安全证书充分路线、弱总安全债务路线、三个净信用充分路线和共享终局模板子域。均不是本次源 A/B 的 route/size/private-deficit ALL。源 A 当前没有 canonical 命中；此快照未发现同一精确联合边。

该排重只对上述当前清单负责，不读取旧历史边目录作数学分母，不断言其它 canonical 边的全仓正确性。本任务无 formal follow-up 对；两个 read-added 端点的比较已由本 ALL 和明确剩余域闭合，收据记 comparison_dispositions，closed_overlaps 保空。
