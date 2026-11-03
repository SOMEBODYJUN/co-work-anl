# 未认领 trueH 投影来源的实读备忘

这是 Boss5 内部只读代理给实际来源 owner 的接续材料，**不是正式数学对象、不是运行证书、不是 done 回执**。父方整笔 claim 没有成功后已停止进一步扫源；本备忘只保存截至该指令前确已读到的内容与有限只读算术观察。没有认领这十二源、没有修改共享正文、没有 checkpoint/done、公屏或 Git 写操作，也没有运行发现 LP、定价搜索、源恢复 QR、原作者入口或旧 144 态完整审计。没有读取凭据。

## 1. 文件身份与实际阅读范围

工作 clone 为 `/workspace/scratch/9552e7f8d046/co-work-anl-boss5`。先读了根 AGENTS、cleanup/README、cleanup/OBJECTS、tools/README；检查了现有未跟踪成果及 origin，全部保留。原件均直接从已存在的本地 Git blob 读取；本备忘并不声称源已完成清洗。

下面十二源的共同冻结目录是
`research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/certificate/`。
inventory 为每个版本记有两个相同内容的来源定位：
`68fad804ec5946cb296f77dc5b336308a66abf12`（legacy-cleanup）与
`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`（main）。下表 SHA 是冻结 inventory 身份，不假称本次又逐提交独立重新核过所有字节。

| 源 ID | 文件 | 字节数 | SHA-256 |
|---|---|---:|---|
| `ec252894adebab9b017d` | `project_current_trueH.py` | 4717 | `c04de18b161e7c072bd1d6ea40468e0fedec756a4f4ff284a4f0d84343c4a6c9` |
| `ac2fe9ddfcab41331382` | `exact_trueH_projection.json` | 66702 | `f6e57535800e501d66c9ae32d1fac52ef55ccd810bb9a022b1be77dc4ce5beab` |
| `1ce17b08f4a55272868d` | `trueH_table_certificate.json` | 7100 | `eba2f2bf0e65d05ad3c7ee890c9fb1bfd3ded96ad8d00f0edb1662281ce43982` |
| `f4b7fe87b66d27263c18` | `trueH_table_certificate.py` | 4771 | `27916f63c68097ef853aeaf20fa93bd13d3199daeda5f684bdef169bbdfe2d3e` |
| `8f7aa8d127d91eb529e4` | `exact_current_trueH_projection_fixed_v1.json` | 477 | `8186b019eb855f19f5f5d73511f9d1ae6e3e004e506365f14e9a8a8d91e12d56` |
| `e2b88efed33a8a09b96b` | `exact_current_trueH_projection_payment_v1.json` | 50831 | `ed3d941a64b7bc5c9e7aeecc7677974f829006fad3490ab42713477d3fe1dfe1` |
| `299cb1f862ee32648c27` | `exact_current_trueH_projection_payment_v2.json` | 54877 | `3cfb6a0e6bda9da51a8ddb1e2e70302772f6dd5aa4c26df35c72a0877d078283` |
| `01bd4ece36eece649506` | `exact_current_trueH_projection_source_last_v1.json` | 57273 | `d4e1c565f785770dce101e4506f99b2755275d2083f49d8f9b763e1abc30f115` |
| `8088f2839957ff686cb9` | `exact_current_source_fixed_v1.json` | 41559 | `5bb6dba2eeb2792afd2f70813b25b0c60ccaafa0c369782e02c384c8ec01270c` |
| `1e9e5db93eb53e07cab4` | `exact_current_source_payment_v1.json` | 38924 | `7c36aca134513863787b699330b3ccb400522a47eef154b0d07ff4f642f58a56` |
| `819dbc7abbecdce9ce29` | `exact_current_source_payment_v2.json` | 42029 | `e4fd3ae57d52be1763ddd4de383999b4615b4baf3ef76d1334bd3ad74a0c2ec3` |
| `c5eab3805b28321d8cdd` | `exact_current_source_source_last_v1.json` | 43942 | `66d63289facc5945502371e6a8fd8857eef9eb9ed95835b08686cd39ee20a2db` |

两 Python 已全文读，包括 main、依赖、恢复阈值和报告写出。十 JSON 均完整解析，顶层每字段读取；表证书的全部 144 个 residual 和 18 组 maximizer 已展开读取。五份原子点（四 source 加旧55合并点）已用只读 Python 遍历全部 JSON 叶，并把每份使用质量逐项转成 Fraction，计算 W、比较覆盖、d/p 分布和旧坐标重复数。payment 两版及 source_last 的全部原子描述以稀疏完整表示输出阅过。fixed/旧55的原始逐项长输出曾被工具显示截断，不能把那次输出冒充逐字显示完整；它们的所有叶、描述与质量都在程序内被遍历。未完成新源全部行／八态系数的定义级重建，不能由这里的遍历当作源级 done 质量声明。

已全文读的直接相关材料有：

* 本冻结 `certificate/README.md`、`trueH_seven_rows.md`。
* `weighted_true_branch.py`（`226371a6e7c7c6440cc8`，7706B，SHA `df6320716f09054459bbc1426dc0c9fde3aa9379ca9f97385e08c578fccb1e6c`）、`max_indexed_coupling.py`（`891a9e91438dc2380ff1`）、`weighted_maximum_query.py`（`dfeeda2f80a50ab3e4e4`）、maxroot 的 `trueH_payment_pricing.py`（`36564ce6b130325083d5`，4469B，SHA `adf09af85278d5c1b90dd5f534ad4464c82249ad84b5f886aa5e40fc3280c507`）、`trueH_source_last_pricing.py`（`623808766aaaf4b79877`）。fixed-closure 的读取输出中尾部遭截断，因此只把其中已读的类继承／row定义用于下述具体比较，不宣称全文件实读。
* 旧 `exact_cross_primal.py`（`deff75f97796e260ebb1`，2862B，SHA `7418a39f215c852725d827581ea0f984e57d79a72c9a22e61a9fb693932556b2`）全文；父方 `root/audit_trueH_seven_rows.py`（`0ab533b07b8b8e158844`，1916B）全文。没有执行它们。
* 正式 `state/引理/真实第三位投影的五人最大根包络--引理.md`、`state/定义/共同目录完整历史模型--定义.md`、`state/审查/五人证书复核边界--审查.md`、`tools/evidence/maxroot-gamma-shared-menu-primary/README.md`；五人half定理精确命题、基础IC/末两人证明及当前状态段，未重新逐条核其53行附录。

## 2. 数学对象应当怎样保留

模型是有限单位客户、有限非空**共同标签目录**，覆盖映射允许不同标签同覆盖、空覆盖；五名单位权提供者逐次观察完整有序历史行动。固定任意一份完整历史纯 SPE，所有离轨弱 IC 与任意平局保留。不存在“源点可行所以有真实SPE”的逆向结论。

取一个裸大小最大的合法主题 M。在原最大根分支 `(M,z2,z3,z4,z5)` 的第三位历史 `(M,z2)`，令逐客户旧负载 `p=1_M+1_z2`，当前第三位沿原策略的收益为 u。选合法

`H ∈ argmax_T Σ_(x∈T) 1/(p_x+3)`，记 `K=Σh/(p+3)`。

强制第三位选 H 后沿同一原策略继续为 Q,R；H 是被强制者，Q/R 才是真后继优化者。会员位为 h,q,r，三个新位的完整放松域为 `{0,1}^3`。记

`V_H=Σh/(p+h+q+r)`，`V_Q=Σq/(p+h+q+r)`，`V_R=Σr/(p+h+q+r)`，

`B=V_Q+V_R+Σq/[(p+h+1)(p+h+2)]`。

任取五个合法 T_i 作为比较菜单，d 为其逐客户重数；另取五个合法 J_i，j 为其重数。重复菜单索引允许。零分子份额置零。七条合法非负行及整数权为：

| 权 | 合法总行 | 所用真条件 |
|---:|---|---|
|17040|`u−V_H`|原第三位 IC，强制H后仍沿同一策略|
|9000|`K−Σq/(p+3)`|同一个H的加权最大性，Q合法|
|10080|`K−Σr/(p+3)`|同上，R合法|
|600|`5V_R−Σd/(p+h+q+1)`|真末位R对五个T_i的IC|
|1085|`|M|−|H|`|M是全目录裸大小最大；不是把祖先利润封顶|
|360|`5B−Σ[(5r+d−2rd)/(p+h+1)+2rd/(p+h+2)]`|真末两人税对五个(R,T_i)对相加|
|2679|`5K−Σj/(p+3)`|H对五个J_i的同一加权最大性|

展开加权和，公共部分为 `17040u_x+1085·1_M−2679j/(p+3)`，隐藏部分 G 的精确最大值是 `−F(p,d)`。其 F 表为：

|p\d|0|1|2|3|4|5|
|---|---:|---:|---:|---:|---:|---:|
|0|0|960|1220|1480|1740|2000|
|1|0|1665/4|2745/4|3785/4|4825/4|5865/4|
|2|0|320|524|728|932|1136|

因此合法必要式是

`P=17040u+1085|M|−Σ2679j/(p+3)−ΣF(p,d) ≥ 0`。

方向必须保清：原七行加权和非负，逐客户以隐藏 G 的**最大值**替代使和增大，所以 P 非负。各客户分别取max仅扩大域，并没有在游戏中让每个客户各选一组H/Q/R。144=3×6×8是全部系数域，不是144个游戏抽样。

原稿后续 v2 已说明这个关系可用于**任意真实第三位历史**：p为该历史两位旧负载，u为该节点原策略规定收益，M只作全目录裸大小cap，不必在该前缀内。不把H或强制比较T_i当优化者，不继承祖先旧收益封顶。这一范围已被正式包络引理吸收，应当链接复用，避免再立同一七行“新引理”。

## 3. 恢复源点的准确合同

`project_current_trueH.restore(source,stem)` 的真实流程：

1. 读 `row_names, atoms, primal_float`；仅取浮点质量 `>1e−8` 的原子。它不处理一般已经精确化且没有primal_float的输入。
2. 用 `exact_cross_primal.evaluator()` 免初始化取行对象，再硬改 `U.__class__=trueH_payment_pricing.Universe`，设 `U.specs=tb.cm.mp.menu_specs()`。
3. 每原子重建精确行，断言其键集合与源 `row_names` 完全一致；另取归一化行 `w(a)=1_[bits前五位至少一位1]`。
4. 浮点矩阵上以 `abs(A·approx)<1e−7` 选候选活跃行；加入W行；pivoting QR以 `abs(diag R)>1e−8` 判秩，断言满列秩。
5. 选足量方程，用 `fraction_solve` 精确解质量；断言所有质量严格正；以精确 Fraction 计算**源列出的全部旧行**余量并断言最小值≥0。
6. 写 `exact_current_source_<stem>.json`。报告只存源行数、正原子数、最小精确slack及全部原子质量；**没有存每一旧行的余量，也没有给最优性、真实OPT、完整策略树或SPE**。

浮点QR在这里选方程，不是最终可行性根据；只有随后精确全行回代承担该恢复合同。原报告四份均声称最小旧行精确slack为0，这次未重新执行该26千余旧行合同，不能写成本次已独立重验。

### 硬编码 evaluator 的版本门槛

源docstring说“每源自己的行求值器”，但冻结4717B实现的 `restore` 实际硬编码 payment 的类。payment基线 `indexed_hinge_fullpricing.json`有6541行；`trueH_payment_pricing`追加24行形成6565。fixed/source_last需其它更强类：fixed报告6747行，source_last报告6687行。因此冻结CLI原样用于这些更强源时，不能自动选择正确evaluator，行集合断言会阻止将不匹配系统当匹配系统。

只读检索在该工作区非JSON源码中未找到可交付的 `tp.Universe` 注入wrapper，不能凭此断言历史绝未临时patch，也不能凭冻结report倒推原CLI现在能直接重现。owner宜保留冻结代码、明确该门槛；如要修复可复制一个新适配器显式接收源的准确类，并与原版本分别保存，不能修改原SHA后声称原实现重放。新恢复前必须审清更强类新增行，不能只改 `source_rows` 数字。

### 四份 source 的只读精确量

全份使用质量均严格正；本次对AB_hist按定义求出的比较重数全部等于d=1；所有旧描述+max_bits键均无重复；四源均精确满足W=1。AE/second共享同一比较重数属于输入合法性合同，owner仍应在自己的完整结构审计中逐条明确核对，不能用本次AB计数代替。这里O只是存储比较菜单并集的质量，不宣称真实OPT。

|版本|源行数（原报告）|正原子|p=0/1/2原子数|由全部质量重算O，W=1|与2关系|
|---|---:|---:|---|---|---|
|fixed_v1|6747|50|31/2/17|`474043013008363585388854742884388297608824001525293125745869641403 / 237879513518000844345522240400840813014566854105077931387953430204`|<2|
|payment_v1|6565|47|29/2/16|`8436188318473755865108291393058957774967800720228638247843209215 / 4234312318264949490774716853940946719804870047850668914816696338`|<2|
|payment_v2|6565|51|30/2/19|`121892925637935754676928259325567243661043382636172017317088755 / 60924087640655341312865535284623834719020991777561812649212191`|>2|
|source_last_v1|6687|53|31/2/20|`144677050808319352273515168205687346317441282070208340917322145845 / 72314711991979195448494116302479156833802677237778887741696677748`|>2|

这些递归读数分别遍历source JSON的2055、1932、2096、2178个标量叶；只是覆盖声明，不是数学证书数量。已逐质量转F，尚未把全部描述的类型/直方图合法性写成新审计器。

## 4. 747 行八态 lift 与精确分离

恢复质量后，对每旧原子a引入8份非负质量 `y_(a,s)`，且 `Σ_s y_(a,s)=m_a`。`weighted_true_branch.rows(a,s)`有747行，原始HQR位共享；所有行只作为原SPE的必要条件。程序先用HiGHS找这个有限lift。失败时再找共同误差变量的辅助LP，从非正边际取正权，限分母 `10^8` 成Fraction；随后逐原子用精确

`g(a)=max_(s∈{0,1}³) Σ_r λ_r·row_r(a,s)`，`G=Σ_a m_a g(a)`。

只有 λ≥0 和精确 G<0 才是固定边缘不可延拓的Farkas式证明；浮点infeasible或浮点最优本身不是证书。所有真SPE提供一组同策略HQR真实位，必要行使其总加权和≥0，而逐原子上包络仍≥原和；因此G<0排的是**保持这些旧质量/特征的延拓**。它不排重优化旧质量，不给加强锥精确最优，不提供游戏或half反例。

### 四份 current projection 的实际内容

|版本|正原子|报告floating_lift_feasible|报告精确G|准确解释|
|---|---:|---|---|---|
|fixed_v1|50|true|无|477B只存scope/hash/数量/success/message/code_sha；**没有保存lift质量**，更没有精确可行证明|
|payment_v1|47|false|`-873030838468862296964238756691087720236458052575800500150227171047 / 392978057633533432339819921780551383171650379400924880646307953737104`|精确负投影报告，约−0.002221576552457277|
|payment_v2|51|false|`-51081548527424177215708978507637147569348823179105213658663519161 / 62824919175043787961826939985504098362254446721021741203867611359200`|精确负投影报告，约−0.000813077823229664|
|source_last_v1|53|false|`-194597830513655836230296803885961955507035637229812839633162328143 / 621424425051074552887392772759304221058477673063313241993646784114480`|精确负投影报告，约−0.0003131480235873605|

三负表每entry都含完整atom（含exact_mass）、coefficient、maximizing_state；不另存外层exact_mass。47/51/53份描述与有理质量必须与各自source逐项绑定。四projection的 `exact_source_sha256` 恰为上表四个source版本SHA。四表的code_sha都等于4717B原脚本SHA。

两payment负表使用同一七个正权：

|row名|有理权|乘51560后的整数|
|---|---|---:|
|`trueH:source-IC`|426/1289|17040|
|`trueH:weighted-cap:f1`|225/1289|9000|
|`trueH:weighted-cap:f2`|252/1289|10080|
|`trueH:R:K:opt`|15/1289|600|
|`trueH:global-size:0`|217/10312|1085|
|`trueH:tax:f2:opt`|9/1289|360|
|`trueH:weighted-cap:z4`|2679/10312|13395=5×2679|

因此是上述P选J五次重复max路径末主题z4，再除51560。source_last只将最后一行换 `trueH:weighted-cap:U`，即五次重复固定合法主题U。不是发现新的机制，不是13行actual投影，也不是跨历史H兼容冲突。这些等权重换算直接由已读分数得出，完整八态/每原子系数尚待owner定义级回代。

### 输入历史版本的绑定

四source报告的输入SHA分别为：

|版本|source内记录的原浮点输入SHA|已读冻结输出版本的比对|
|---|---|---|
|fixed_v1|`caeadfa406adaba5718146074e7a57f946e5875e1c6ea6d219dee5676f32e14c`|当前冻结`trueH_fixed_closure_fullpricing.json`为SHA `73bf5a2d9bb79784ad2a0e12dfb355403ab1bb6726e07832b2bd90b1d6f53360`；不是同一输入快照|
|payment_v1|`2b03e3e1d1399b6723fb47984c24cc40b30f52e2470affb2739f3a74024505de`|与当前同名fullpricing不同；不可用当前文件冒充最初受限点输入|
|payment_v2|`bd1a698af753dc9378f0c1202abf681d5fa7c90018139d4d8d00ac257218aa4a`|匹配`e37100bc3c8a1b89926e`，`maxroot/trueH_payment_fullpricing.json`，6565行|
|source_last_v1|`9048f6eb8efb1cb29cd0f6e1b4e436709ea3d98ca5dfa869de9f874e4e25f1c1`|匹配`120a3f86296da1fcb620`，`maxroot/trueH_source_last_discovery.json`，6687行|

未继续全仓按这两个旧输入SHA排查可用历史快照，故应写“本备忘未绑定到当前冻结同名文件”，不能写“全仓不存在”。四份精确源点本身全部旧描述和质量均存在，不因此丢弃负投影可独立回代的资产。

## 5. 旧55原子投影的合并质量陷阱

`exact_trueH_projection.json`报告55个合并旧原子、8态、747行，浮点lift失败并保存七个正有理权及每原子的max系数。其精确G为

`-169500194513991512083150016856795303715058552168132987135 / 24368697863582404164257358829723456062199106455303425183072`。

原报告使用lambda为整数七权除40844；最后的J行是 `Sbranch:trueH:weighted-cap:mW`（2679/40844），使用second_hist中第三个后继菜单mW的五索引重数，不是固定z4五次。标准表程序断言 `atom_coefficient(a)=40844*entry.coefficient` 并以**entry外层质量**求和，得到table报告分离值

`-169500194513991512083150016856795303715058552168132987135 / 596628583478170702288153922968452063025147058449305288`。

`weighted_true_branch.lift`先按 `mp.atom_key(a)+(max_bits,)` 合并原来的H_bit拆分质量，允许重新选择H。`projected_atoms[i].atom`却保留该合并类的第一个原记录，包含它原来的H_bit和原exact_mass；另存entry.exact_mass才是合并总质量。因此在0起索引

`0,15,16,17,19,23,24,42,51`

共九处，**内层atom.exact_mass与外层entry.exact_mass不同**。这不是应改写的历史数据错误，也不是用来抛弃负投影的理由；回代必须用外层合并质量，内层字段作代表记录保留。新四source没有这种双层质量格式，不能按旧解析器混用。

只读全部使用质量重算：W=1，比较覆盖
`200041434567641869132724720689474222359301995810509781 / 99438097246361783714692320494742010504191176408217548 >2`，55份全d=1、p计数36/0/19，旧描述+max键无重复。全JSON递归为2603标量叶。source报告输入SHA是 `952601aa1e7ec1365692a6ce8def7feb5819669a416b5311eec4204136ce8f6f`；本备忘没有追完该输入绑定，不写其为本次独立核过5484旧行。

## 6. 原表证书程序与已成熟核验的复用

4771B `trueH_table_certificate.py`仅标准库。从七条原式独立构造G，逐 `(p,d,h,q,r)` 核144余项、逐18格保存全部取max状态；再读上述旧55投影，重建其逐原子系数并断言40844比例、外层合并质量分离值。报告含范围、relation、notation、七权、F表、完整域、144 residual、18 maximizer、旧点分离、source/code SHA。报告notation仍写最大根路径，后续任意真实第三位范围来自七行原稿v2，不能静默把原JSON字段改掉。

这不是发现程序的row evaluator导入复用；但是程序作者与其知情陈述的独立代码身份应分别叙述，不自动称外审或盲审。父方 `audit_trueH_seven_rows.py`另从七行字面重建144态，明确写known weights/nonblind；它不读取作者输出。

已经存在成熟成功事件：
`archives/customer-attraction/tools/evidence/maxroot-gamma-shared-menu-primary/README.md`第一个入口记原最大根audit.py一次退出0、stderr空、3701B stdout与冻结audit.json逐字节一致；其审计覆盖144 trueH隐藏态、13份包络各192型及相关障碍。正式 `真实第三位投影的五人最大根包络--引理.md`自足包含七行及F表、任意真实第三节点范围。owner应复用该结果，不再为了本批“有运行”而重复144态或大型主域审计。

真正尚可新增且不重复的适量核验，是独立标准库对这55/47/51/53份保存原子的**八态max/保存maximizer/质量/scale**逐项回代，另核四source与projection的全部结构绑定、输入版本；不需跑LP、定价、QR或全仓half主证。建议报告明确称知情定义级固定数据复核，别把本备忘先前的解析算术包装成已完成这个核验。

## 7. README状态纠正必须保留

冻结certificate/README已经有最终后续判断，不可只读旧“OPEN”段：五人原目标已由独立交付 `CA-FIVE-HALF-EXACT-v1`证明，旧n5搜索停止。本组点不会否定五人half；当前恰六人的一般目标没有由本组解决。

README对四点的准确归因是：

* payment_v1：初始6565行受限点O/W<2；八态分离只找回P对原末主题重复五次的漏查询。不能把它写为“仍>2点被切”。
* payment_v2：补列6565行精确点O/W>2；同样是P的原末主题漏查询。
* source_last_v1：6687行精确点O/W>2；找回P对其它固定合法主题的漏查询；两个单历史已各自不兼容，不能归因跨H共同目录。
* fixed_v1：初始6747行精确点O/W<2；完整单747-HQR、两单历史H及联合四态H都仅浮点lift可行，不作方法阴性、精确延拓或“2倍缺口”的归因。

跨历史共同目录接口只有在各单历史先可行、共同互查再失败时，才能把失败归到新增共同兼容条件；本12源不提供这样的精确证书。README还叙述后来的6750/6751点、actual13、7497显式actual扩展与正式导入证明，但它们不在本12源范围内，不能凭导航段一并勾选或认证运行。

## 8. 建议对象安排与阶段三关系依据

若实际owner继续本批，适合把**程序恢复合同、四新点、旧55格式与精确分离资源**整为自足计算/程序资源对象，链接既有七行包络引理，不再重复授同一数学引理。原12源原字节与准确manifest应放该owner独立证据目录，保所有版本差异；逐源receipt要指向其真正独有内容与边界。

已有真实关系可供阶段三接续，当前不建图：

1. 完整历史模型给真节点IC与同策略后继语义；固定背景两人税给第六行；裸最大主题/加权最大主题给其余cap。
2. 七行共同推出P，144态表认证全系数域；既有包络引理已承担一般命题。
3. 恢复器把各自浮点支持转成固定旧必要行的精确可行点；该关系是实现与有理恢复合同，非SPE存在。
4. 八态max对所列点给严格分离，只排保边缘延拓；两payment和source_last只是P的漏查询实例，不能造“新机制依赖”边。
5. fixed_v1的float success是有限诊断，不与任意游戏蕴含同类边。
6. 五人half正式定理与旧锥点>2相容，因为前者使用更多合法信息；从本组不能迁移恰六人或任意背景五剩余人的福利结论。

本备忘至此停止。owner应按自己真实补充阅读、核验与发布情况决定是否done；不得把Boss5未claim阅读备忘当作已推送正式成果或代签完成声明。
