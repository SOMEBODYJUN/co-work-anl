# 低阶成本空间、稀疏资源与 selector dual：独立攻击报告

## 审查对象与结论

审查对象是根对话固定副本 `/workspace/scratch/ecf05625b47b/selector_local_moment_bridge_reviewed_freeze.md`，SHA256：

`f4541469f8aadbb57037b10e1248ed6b1db24d493e31d0d1974c0f85bb6aecbe`。

一般实参数证明的结论为 **PASS（内部独立重构及攻击，非外部审查）**：主待审命题的共同成本空间上界 D、≤D 正系数单项式资源压缩、≤Σm_i 个零费 private-action markers、原 core 结构保持、概率 dual 的 ≤D+1 状态支持均正确。稿中新增的 one-mover degree-moment/separation 等价与 entirely transient parity dual 例也未发现漏洞。没有获得全类 O(d/log d) 上界、动作数或人数 cutoff、或随 d 增长的非存在下界。

审查前先只读 MODEL、既有 finite_action_duality.md 和相关 core 定义，完成 `independent_reconstruction.md` 后才读作者稿。独立重构与原稿在证明接口上吻合，但不是将原稿改写后冒充独立重构。

## 冻结版本的可追溯性

根对话最初给出的待审 note hash 为 `1f852f5f6dd5daedcff77859b31f4be1b71815b70fcd9d6e35434f4949d8fbbb`；我首次实际读取作者目录时其 hash 已为 `3ae034e3a114c5bb4a84e015f450b5008c1f2360461de1ff3fa08e138cb57cc3`。此不匹配当时立即报根对话，不能宣称审查了最初 hash。随后作者又在原路径写入 f454 版，根对话另存固定副本并要求据此审查。

我将初读 3ae 版本和最终 f454 版本分别保存在本目录 `author_read_3ae034.md`、`reviewed_freeze_f4541469.md`，各自 hash 已精确核对。3ae→f454 唯一差异是 §2 增加一般 M=Σm_i 上界：

`D <= M sum_{r=0}^{min(d,n-1)} (M-n)^r/r! = O_d(M^{d+1})`。

该增补正确：对每 i，r 阶基本对称和 ≤ `(Σ_{j≠i}(m_j−1))^r/r!`，再以 M−n 控制并求和；r=0 的项按空积1处理。没有其他数学或边界变化。初始 1f852→3ae 的差异未在本审查中取得，故本 PASS 只挂最终明确固定的 f454。作者 audit 脚本 hash 始终为 `faa86c37eb121de2f12b0a3f0ebf3f5e9b2a6433eef559253ea638f0a9c4efab`；重跑时当前 exact_audit.json 已挂 f454，与重跑结果完全相同。

## 对主证明的攻击

1. **截断空间是否真的共同、是否丢掉自己的动作依赖？** 对每玩家 i，自己动作保持全部 m_i 维函数，对手只取至多 d 名玩家的 contrast 张量。单项式资源的自己的指示量可提在外，资源被使用时自己的负载贡献固定为 w_i；故余式至多涉及 k≤d 名对手。m_j=1 时没有 contrast，公式自然为零维因子。完整空间 W 是所有玩家分量的直和，不能只对单个成本表数维后忘记乘玩家数。

2. **锥压缩是否暗中引入负费用、变次数或损坏全部状态？** 沿线性关系减到一个正系数归零时，其余仍非负；最终只保留原有正项的签名和次数。保持的是完整向量 C∈W，因而所有玩家/状态/真实偏离都保持。系数允许改变；不能同时要求单位系数或原 resource 身份保持。相同签名不同次数作为不同 monomial type 计数没有矛盾。

3. **零费用、空策略、标签与非空资源？** 全零 C 可以保留零个正费用资源；至多 M 个 markers 保证资源集非空及动作标签分开。即使原有空策略，改变其底层集合而保成本合法；稿件没有宣称逐字保留空集策略。m_i=1 不妨碍一般压缩；core 断言另要求每名玩家至少两个动作。

4. **core 空交是否可能被新分解破坏？** 原空交意味着每个原资源对每玩家的动作关联块都 proper。只在原支持中锥消元保此性质；single-action markers 也 proper，并保证非空、反链。若任意选择全部签名字典的新分解，空交可能不再自动成立；稿中明确选原签名，故此攻击不成立。

5. **dual 支持界是否依赖 stationary/recurrent，或只保被压缩资源而漏掉其他列？** B=A_hQ 的 rank≤D。等价地，Ψ_h(s) 是 W 上完整偏离 functional 的坐标。对 augmented `(Ψ,1)` 做仿射消元保持完整 feature vector，因此保全部资源列期望，不依赖先对某一游戏压缩资源。任一已有概率 dual 可减至≤D+1；它不是 dual 存在性定理，也不限制支持为 recurrent。

6. **对 α、权重或算术域有隐藏限制？** 正权保证 MODEL 与一名 mover 的 span 隔离系数非零；α 可取任意实 α≥1。表示与 convex elimination 的证明适用于一般实数据，不因 Fraction 审计只测有理点而退化成有理域命题。稿件未承诺实参数的有理证书。

## 对新增机制的攻击

§4 的相反方向签名产生互为负的 α=1 列，故每个原始非负 test 的期望必须相等。k=0 逼两方向质量均1/2。由 r 次 `(w_i+Σ_{j∈T}w_j1_{s_j=u_j})^r`，顶阶系数为 `r!∏w_j>0`，减去低阶项即可归纳得到全部 categorical degree≤d 的 context moments。所需单动作对手块也是 proper，故 core cone 并不损坏 span。有限凸包分离给严格 polynomial separator 的等价，空方向集合由常数处理。α>1 时只能保留原始非负 tests 的 multiplicative sandwich；稿中没有错误推广到所有 signed polynomials。

§5 的 flag 保证所有支持状态真实 transient：flag0 偶态先翻玩家1成奇态，下一步翻flag；flag1永不离开，并单调清除坐标2,…,m，最后只剩唯一二循环。支持上的成本差为 even/odd parity sum；玩家1完整成本的 active-variable degree≤k+1≤d+1<m=d+2，因此交替和逐 monomial 为零。权重任意正实不改变次数。α>1 再减非负 arrival term 仍为dual。唯一二循环本身也有两边均重dual，故此例只能证明“transient 支持可以可行”，不能证明“transient mass 必要”或“recurrent 限制有无界损失”；稿件已明确这些限制。

“Cross-player compensation in (4) is in general necessary”这一句可由 n=2,d=1 的四状态交替玩家 square selector 具体化：每玩家的两个方向在不同 opponent context，degree1 无法单独匹配；给每条边以 mover weight 的质量可抵消每个 affine resource margin。该句正确，但若整合稿希望完全自足，可补这一小例或链接已有 affine weighted-cycle 论证。它不是主结果的缺口。

## 独立精确审计的范围

`independent_exact_audit.py` 未调用作者实现，以 direct resource loads、anchored categorical finite differences、独立 Gaussian row elimination 交叉核验；输出为 `independent_exact_audit.json`，全部通过：

- 七组完整成本压缩，覆盖 n=1、m_i=1、d=0、分数权、非二元动作、full/core 签名与全零费用。压缩前正单项式数量 1/21/126/63/52/40/0，最终 1/3/14/6/15/10/0，均≤对应 D。最后一组字典有8个可用 monomial types 但原正支持为0。
- 1730 个 order>d 的 anchored categorical finite differences 精确为零；90 个全部玩家/状态成本表位置在各组压缩前后精确相同，包含重复检验位置。
- 两组 n=5,d=0 的32状态概率 dual：α=1 全部真实翻同一玩家，支持压至2；α=3/2 按状态选择不同玩家的 self-move，支持压至10，均≤D+1=11。两组都对1023个完整签名列保全部期望且满足dual。self-move 仅用于一组代数接口边界，不当成 parity family 的真实移动例。
- one-mover span 在动作数(2,3,2)、分数权、full/core两字典、d=0/1/2中，primitive-test span 秩分别等于完整context moment维数1/4/6。
- 作者标准库audit完整重跑，与当前冻结 JSON 的全部字段相同；重跑结果保存在 `author_audit_rerun.json`。该审计本身是有限验证，不能替代一般证明。

代码 SHA256：`b7d1ac642f61fe2ec447c6c3e50c711ce28834795b64236ad3a2cb2c017e9b0a`。
独立 JSON SHA256：`9ce2ccebe46ad8bc255fe4afbef0648308a26a2fdc11b0f0ef2d59d148d85e59`。

## 状态边界

没有未解决的数学 blocker。源路径“freeze”曾被原位修改是已记录并由固定副本、精确diff与hash纠正的 provenance 事件；它不证明数学错误，也不能省略不提。该报告不是优先权或文献新颖性核查，不升级为外部同行审查，不把有限审计当全类增长界。

## 入库路径与最小适配

现行正文[有限次局部矩、全成本压缩与暂态择证对偶](../../../current/weighted_congestion/template_certificates/selector_local_moments.md)与所审f454固定版的数学Claim/式子相同；改中文首标题、身份/状态/导航，删去未需依赖的“cross-player一般必要”解释句，保留“任意selector不保证单mover证书”的范围。两份规范audit只把启动读会话freeze文件求hash替换为所审hash的字面元数据；所有成本、输入、消元与断言不变，令后续研究者无需暂存路径。新源码hash和规范运行由`selector_local_moments.json`、`independent_selector_local_moments.json`记录；本审查前述旧代码hash只标识所审原稿。两份代码路径为`tests/audits/weighted_congestion/template_certificates/verify_selector_local_moments.py`和`tests/audits/weighted_congestion/template_certificates/independent_selector_local_moments.py`。

## Canonical 入库后的只读适用核对

根对话整合后再次只读核对 `research/current/weighted_congestion/template_certificates/selector_local_moments.md` 与 f454 固定版的完整 diff：三条 Claim 与全部承重式保持相同；只有中文标题、状态/导航/审计合同，以及将“cross-player compensation 一般必要”的解释句改为“不保证任意 selector 的 one-mover-supported certificate”。这些变动不改变已审数学命题，故本内部 PASS 适用于该 canonical 数学正文。

两份 canonical audit（`verify_selector_local_moments.py`、`independent_selector_local_moments.py`）逐份 diff 仅有一行把启动时读取 scratch proof 文件求 hash 改为 f454 hash 的字面元数据；全部输入、成本计算、消元、差分与断言均未改，原有限审计适用。后续规范运行的新 source hash 与回放由根对话单独记录，不把本审查的旧 source hash 冒充为新文件 hash。

本次发现并已报根对话的唯一入库问题为正文 §8 的 review 相对链接少一级 `..`（`../../reviews/` 应为 `../../../reviews/`）；它是导航问题，与上述数学及 audit 适用结论无关。本子审查没有修改 repository。

## 异权仿射全签名成本射线：独立重构与冻结攻击

## 身份与结论

审查 Claim：`WC-AFFINE-FULL-SIGNATURE-RIGIDITY-v1`。

审查固定正文：`/workspace/scratch/ecf05625b47b/affine_full_signature_rigidity_frozen.md`，SHA256：

`7a2ee0b7ed466d426b3ee6d9142c30be95392cb454bbfb860d7045a21cff1299`。

独立重构后逐式攻击的结论为 **PASS（内部数学审查，非外部同行审查或新颖性认证）**。对 n≥2 的不全等正权、binary标签和 `V_i(s)=s_iΣ_jw_js_j`，任何保持完整成本表的 MODEL 有限多项式表示，忽略零费用或无人使用资源后，全部资源确为全玩家仅动作1使用、费用 a_e x，且所有 a_e>0 之和为1。因此 V 为有限表示成本锥 K_fin 的极射线，且提高次数也不能把所有正资源支持降到<n。没有未结数学 blocker。

根对话最初只给出 n≥3、两两不同权的支持下界 statement。未读新证明时，我独立推得完整刚性、n≥2 和“不全等权”加强，写成 `independent_affine_fullsupport_rigidity.md`；其最后一次预审稿 SHA256 为 `26951d356708cf0a78363ea679e5d9cb7080da2b9b33aac54675d74b7d5e9067`。随后才读取上述7a2冻结证明。本次未出现冻结 hash 不匹配；同内容快照保存在 `reviewed_affine_rigidity_7a2ee0b7.md`。

## 逐式攻击结果

1. **零成本是否允许不同资源抵消，从而让动作0用正资源？** 不允许。非负系数的非零多项式在任意正负载严格正；一个使用资源的玩家使负载至少 w_i>0。目标所有动作0成本为零，故任何正资源都不出现在动作0。实际上全0一个状态即已足够排除。zero markers 不受限制，无人使用的正费用多项式给零向量，正确地被忽略。

2. **pair contrast 对任意有限degree是否同号？** 对 a>b>0，

   `F_k=a[(a+b)^k−a^k]−b[(a+b)^k−b^k]`

   `=(a−b)[(a+b)^k−Σ_{r=0}^k a^{k−r}b^r]`。

   k=0,1 时恰0；k≥2 时每个二项式系数≥1且有严格较大内项，所有幂乘积为正，故严格>0。费用系数非负且资源有限，各次有限，和为0确实逐项强迫该异权pair共同资源的高次系数为0。不需统一degree上限，也没有仅依赖数值检验的步骤。

3. **为什么仅一对异权就能排除全game的非线性，而非需要两两不同？** pair共同资源斜率和1已经在p的solo状态贡献 w_p，耗尽其全部成本。所有常数和p的其他正资源因此被排除。接着p与任意j的pair成本差逼p全部斜率均覆盖j，所以每个p正资源全用户。它们同时耗尽每位玩家的solo成本，最终排除其余所有有使用者正资源。因此多名同权玩家不损坏证明；只需存在一对异权。

4. **affine资源斜率可能为0，是否破坏“逐项严格正”一步？** 在排除共同常数 B_e 后，若 A_e=0 则资源为零多项式，属于被忽略部分；所有保留的正资源均 A_e>0。总斜率1保证至少一个保留资源。第3节对任意j漏失斜率的和为0，遂逐项不能漏j。

5. **extreme ray 是否暗中把锥闭包或无限表示纳入？** 没有。K_fin 中每个向量都有有限 MODEL 表示，U+Z 用资源不交并仍是有限表示。刚性迫每个非零资源向量为同一个V的正倍，故两个子和也是其非负倍且系数和1。此处只证明 K_fin 的极射线，未证明闭包的极射线或暴露射线。

6. **标签/core/PNE范围是否正确？** 同标签完整成本保持排除交换动作语义。两个私人零费 action markers 保证动作非空、互不包含、空交且彼此不同。全0状态各玩家成本为0、任何偏离成本非负，是精确PNE；故该例是保真表示障碍，不是均衡非存在例。允许改变权、加玩家、只保近似不等式或单向lift的归约并未被排除。

## 等权边界核对

冻结 §4 的一般构造正确。n≥3、单位权，任取整数 q≥1 满足2^q≥n：每个玩家对一条费用 x^q/(2^q−1) 的动作1共享资源，另给每玩家私人动作1常数 `1−(n−1)/(2^q−1)≥0`。玩家i动作1且有m名其他动作1时，其成本为

`[m2^q+(n−1−m)]/(2^q−1)+1−(n−1)/(2^q−1)=1+m`。

全部成本精确保留且正资源支持≤2<n。n=3,q=2给最小清晰例；n为2的幂、q=log2n时私人常数为0，可直接删除，不违背合法性。n=2等权也不满足完整费用刚性：w_1=w_2=w时，一个全用户费用 `2w/3+x²/(3w)` 在可达正负载w、2w恰等于x。因此“不全等权”确实是该精确命题的重要条件。

## 独立 exact audit

独立源码 `independent_affine_rigidity_audit.py` 未调用作者实现。完整输入在源码，使用 Fraction/整数与真实资源负载，无随机性、solver或容差；输出 `independent_affine_rigidity_audit.json` 全部通过。

- 五个正分数权的全部25个有序pair、degree0..8，共225个 F_k 代数/符号核验：70正、70负、85零，反转权顺序符号正确。
- n=2/3/4，权分别 `(1/2,3/2)`、`(1,1,2)`、`(1/3,1/3,7/5,7/5)`，枚举全部333个非空binary动作签名与degree0..6，共2331个正单项式资源列。由直接状态成本构造五个依次非负的零face functional：动作0、异权pair高次、p solo预算、p资源全部含j、余下solo预算。每个阶段只在先前face上核非负，最终每组唯一剩余列恰为“全玩家仅动作1、费用x”。该有限审计覆盖重复但非全等权；不把后期functional错误宣称为全锥非负。
- n=3..8 的12组等权构造（最小可行q及q+1），逐状态逐玩家共7152个真实成本位置精确等于V，并以实际资源子集核marker后的非空/反链/空交，最大正资源支持均为2。
- n=2、w=3/2 的非affine全资源费用 `1+(2/9)x²`，另8个真实成本位置精确等于V，核等权刚性边界。

审计代码 SHA256：`72cfc0f3bf8a1a40c6dbb8f99ef06be58383b1eb7100c5a035d4b8b17b775b87`。
一般实参数与任意有限degree的证明由冻结正文承担；这些 finite exact checks 不是对任意degree或所有实权的穷举。

## 状态与适用边界

该新 Claim 不修改先前三条局部矩/压缩/暂态 Claim 的数学身份。成本空间维数小与资源潜在用户支持小是不同性质，本刚性不反驳已有≤D资源数压缩。它提供一个全用户仿射成本射线的保真表示障碍，不提供全类 Cd/ln d 上界、近似均衡下界或关于其他归约的普遍不可能性。若 canonical §9 仅整合上述固定正文并增加身份/审计导航，则本 PASS 适用于相同数学命题；最终入库差异仍应只读核对。

刚性正文规范整合于同一账户第9–10节，数学内容与7a2固定稿相同，仅改标题编号和审查/命令导航。独立源码原样迁入`tests/audits/weighted_congestion/template_certificates/verify_affine_full_signature.py`；规范新路径运行结果为`evidence/runs/weighted_congestion/template_certificates/affine_full_signature_rigidity.json`。该新Claim允许任意有限degree，先前三Claim仍沿用原精确身份。

规范入库后，原独立审查者再次只读逐式核对§9–10：除标题编号与审查状态外同7a2冻结正文；不全等正权、有限表示锥、全成本保真、等权边界及全0精确PNE限制均相同。独立代码SHA256仍72cfc0f3，导航目标存在。内部PASS适用于该规范数学正文；此次核对不改代码或冻结结果。


## 完整proper锥的必要暂态质量：同时化推论审查

### 全 proper 签名锥中暂态必要性的独立重构与冻结攻击

审查者由主研究者内部委派；不执行 Git 或对外群聊。本记录是 scratch 审查资产，供主研究者核对后整合。

#### 冻结对象与顺序

先仅读取精确 statement（SHA-256 `c55819d7419000c36ff7d5a0257cc46af509f7e2d4d3fbd6c953410d7615e694`）及适用 `AGENTS.md`、`MODEL.md`。未先读 proof 或其他审查者意见。独立重构完成后，先向主研究者报告构造及关键次数瓶颈，才读取最终 proof（SHA-256 `c2cde533f35fbc9d8bcaa0bc0894aad2d015af7528835b71f9e98515d041f5c7`）。收到的首个 proof hash 为 `051efaed5f305a92805dae1a1957f6fd92d558414194661891cbb4df9c5dfebd`，该版本未读取；主研究者随后明确最终冻结版本修改仅删除一处不需要的 M=0 例，而精确 statement 不变。

随后读取既有 `stationary_selector_obstruction.md` §7、`selector_local_moments.md` §5、`cyclic_clone_improvement_cycles.md` §3–4，核对依赖及增量。

#### 不看 proof 的独立重构

取 n′ 核心坐标及 flag。在 flag=0 的偶校验半立方体统一选择核心玩家1翻转，再令其奇校验目标翻 flag 到1；在 flag1 上先朝原环上固定点逐坐标路由，在环内保留真实改善边。均匀偶校验质量完全处于暂态。

对一列资源，只有玩家1的费用函数参与 λ 的列积。该函数是其当前动作 membership predicate 乘以真实负载 k 次幂，故在二元变量上多线性化次数不超过 k+1。用至少 d+2 个活跃二元坐标，全部 k≤d 的偶/奇和相消。β≥1 只再减非负到达费用，所以同一 λ 全倍率可行。原正系数游戏在环上逐行严格正，排除 recurrent-only dual；其最小环余量和最坏环外负余量给暂态质量界。每态所选玩家当前动作的 singleton 常数资源排除该态点质量 dual，也排除共同模板均衡态。

冻结稿使用 m=d+2 个活跃坐标、固定其余核心坐标；这与独立重构等效，并降低 λ 支撑。

#### 逐项攻击结果

1. **唯一循环与真实动作。** 每条 selector 边恰翻一名玩家。flag0 至多两步到 flag1；flag1 在首次入环前距固定环点的 Hamming 距离下降，故没有其他循环。进入环的其他顶点后直接遵守原环，不要求继续向固定点移动。
2. **完整 proper 锥。** 在完整锥中，每个玩家/动作都有 singleton 资源，可以全部保留零费用。由此两个动作均非空、互不相交且互不包含，标签不会因成本为零而合并。没有调用空策略、单动作玩家或共有零成本动作。
3. **parity 全列抵消。** 在 λ 支撑上只动玩家1。`g=f_1(x_1)(w_1+background+sum_(j≠1)w_j f_j(x_j))^k` 正是当前真实费用；当 f_1=0 时前因子将表达式消去，当 f_1=1 时自身负载确为 w_1。多线性次数≤k+1<m，含 flag 或非活跃坐标的资源只改变固定 background。k=0、无人当前使用、任意正实权均无额外问题。证明实际上覆盖更大的任意签名锥，但主命题的 proper 假设正确地用于嵌入原 a。
4. **全部 β≥1。** B(β)=B(1)−(β−1)A，A 是偏离后非负成本列；因此 λ 不随 β 变化。不声称 recurrent 必要性在每个 β 都成立，必要性只在给定原 α。
5. **严格环与额外玩家。** 原正资源不含新增玩家，旧资源上的真实当前/偏离成本逐项不变。附加玩家的两个动作仍在完整模板中以零费 markers 区分。所有旧资源若重签名相同，可把同次系数相加；不改变有限非负向量 a 的存在。
6. **质量界。** 对概率 dual μ，`0≥Eμ b≥η(1−t)−Mt`，因此 `t≥η/(η+M)>0`。η>0 足以保证分母严格正；M=0 时 t=1 亦自洽。无玩家费用除法，零费用按不等式处理。
7. **无点 dual 与无共同 sink。** 取所选玩家当前动作的常数 singleton 列，当前费用1、真实到达费用0，B 行值恒为1。故每态 δ_s 都失败。精确量词为 `¬∃s∀a≥0: s 是 a 游戏的 α-PNE`，不能交换成 `∃a≥0∀s: s 非 α-PNE`。
8. **低 d。** d=0、1 的严格改善环前提可能为空，但条件定理并未声称存在这样的输入。parity 与路由机制在 d=0（m=2）仍良定。近 d 推论另限定 d≥2。
9. **近 d 推论。** 原 cyclic clone 的最终 theorem 策略族为2^E，不能直接称 binary。本推论应明确取其 §3–4 构造的两个互补动作，去掉后来2^E扩展；这些动作的资源签名对每名玩家至多出现一次。改善闭环仍合法，若原文只给闭 walk，可按有限有向图首次重复抽取简单环。原游戏其余均衡态有无与本推论无关。

未发现上述冻结命题范围内仍然成立的 fatal objection。建议最终自足版本开头明确 dual 指概率分布（非包括零向量的未归一化锥），并显式写出“共同 PNE”的量词。

#### 精确有限独立核验

独立 scratch 程序 `review_transient_core_independent.py` 不导入作者程序；采用 `fractions.Fraction`、显式资源/当前用户集/真实偏离负载，无 solver、随机性或浮点容差。

输入取旧 §7 二玩家二次环，权(1,2)，α=52/51，四资源签名与系数为 `(1,1):13x`、`(1,0):3x²`、`(0,1):3x²`、`(0,0):13x`。补两个 ordinary 权3/2、7/3，flag 权5/4。n′=4，最终5玩家、32状态，parity 支撑8状态。

完整枚举242个非空 proper 签名及次数0、1、2，共726列；在β=1逐列精确为0，在β=52/51、2逐列≤0。每状态实际 selector 边恰翻一位，每条轨道仅进入原四环；每态 singleton 列在三组 β 取值1。原环余量为 `(62/51,1,62/51,1)`，η=1、M=48/17，暂态质量下界17/65。将 parity 同一构造测试到声明范围外次数3，得到某列21/4>0，核实证明确实依赖 k+1<m，未误把有限次数抵消升级成所有次数。

这些有限核验仅检查实现及边界，不替代上述一般证明。

#### 与既有结果的真实关系

- `stationary_selector_obstruction.md` §7 已给删列子锥中的“暂态必要”，其 dual 是空状态点质量；没有完整签名锥、无人为空动作、无点 dual 同时性。
- `selector_local_moments.md` §5 已给完整 proper 锥中完全暂态 parity dual；其唯一二环另有 recurrent dual，因此未证明暂态必要。
- 本命题将前者的真实坏环路由与后者的暂态 parity 层同时保留，得到完整 proper 锥中的必要暂态质量，且借既有 cyclic clone 扩至近 d 倍率。增量是清晰可复用的拼接接口推论，不是新的全类存在机制。
- 该 selector 有明确 dual，所以恰不可能被某费用向量在全状态严格实现。结果不构造没有 α-PNE 的游戏，不证明任意 selector dual 可行，不给统一 C,d0；原问题仍 OPEN。新颖性未认证，外部同行评审未发生。

最终规范§11与冻结proof从明确构造开始剔除标题层级/空白后逐字一致；概率dual、binary近d限制和无共同PNE量词补充均通过scope核对。两规范代码已重跑，冻结source hash匹配；纯接口修改不改变证明或旧Claim。

## 并行成果合入后的主研究者规范复核

本轮合并正文整稿SHA256为`bda327be7c578ad72d7767033dc09c8bc890c28f23863b61a022d9ea1ec52ace`。近似支持失真保留第11–12节；远端完整proper锥暂态必要性从其原第11节顺延至第13节（子节13.1–13.2），全部公式、量词、假设、证明和冻结证据保持原字节，只有章节编号改变。两项Claim不同身份，未互作证明前提；原冻结hash仍对应各自实际审查版本。
