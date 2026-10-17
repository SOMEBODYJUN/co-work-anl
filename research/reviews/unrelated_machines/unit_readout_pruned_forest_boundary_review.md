# 单位读出配额森林：三合同实际审查

读取目的：核全部变量mandatory、每个原任务、所有机器负载、显式总位复杂度，以及源阈值和实际森林的量词差别。正文最终SHA256为 `225441481810c629afb4af0bcb5d5eb19dad505a30c2680461bd4255dba30b90`。三数学合同无尚成立fatal，外审、新颖性和独立论文价值未认证。

审查顺序按下列原文分别保留：shared先只凭forest IFF陈述重构，cover另按half-density陈述重构，pcsp只凭hitting陈述重构；最终两位读取完整冻结稿攻击。不是把所有读后攻击统称盲审。BCG的比较句已按root和shared亲读原PDF修正：Lemma4.6保M仅在先删除≥2 big-item players的子实例，Lemma4.7回填仅floor(M/2)。这不是三个自足证明的承重前提。

根研究者亲读五份最终代码并实际重跑：六份完整证书4440 jobs、2544 loads、256个NO源赋值；半密度构造1160穷举wiring与300随机、深度/巨大A、空和非法域，另提取所有变量森林；leaf规范24参数569子树叶集与264328全叶子集，独立26参数264332全染色并验证深1000显式链提取。两个叶程序互不import；半密度构造与六证书reader独立，后者不导入生成器。有限检查不承担一般证明。

root还重建两份同64open的原297job/170machine全部资格并重新累加170个loads，独立按显式叶前缀DP回算每sign的max quota：[4,0]对[1,1]，真OPT分别1和7/4。新半槽CLI锐例从全部原边回算14台loads，并按真实literal occurrence计数核实与旧split锐例同构，未重新声称物理枚举。

软件范围：半密度公共输入用显式leaf paths，列min(A,d)保留units及每port到它们的全部边，其他原units用精确零区间表示；默认matching只用ceil(d/2)。root只修A校验允许非负，k/h仍正，新增A0空clause（空/非空树）边界后重跑，原scratch源码90c647...保留、最终规范SHA050e0534c7156e6ee0b5f17458c1cce83f85a818bb1b5790dacec88958b2b3fb。一般C的IFF双向算法为数学构造，软件仅做针对证书及half-density提取，不冒称已提供通用任意C的forest solver。

[现行正文](../../current/unrelated_machines/unit_readout_pruned_forest_boundary.md)、[冻结实际输出](../../../evidence/runs/unrelated_machines/unit_readout_pruned_forest_boundary_audit.json)保留可核对象。下列审查中的scratch文件名仅为实读身份定位，必要内容已在这里保存。递归majority来源只为经典模型背景，root亦实际打开primary PDF核§2.2，准确登记manifest为未落地，不当作全参数横截公式的文献证明。

---

# 单位读出双树边界：最终三合同数学全文攻击

内部审查者 `cover_consistency`。实际先全文读取 canonical `research/current/unrelated_machines/unit_readout_pruned_forest_boundary.md` 的 `cf11045c27b8c1849af8f928aea96d0f813991e0cd0653586e5b426624c68f39` 版，随后再全文读取仅修 §5 Paper Fact 适用子实例说明的最终版，SHA-256：

    225441481810c629afb4af0bcb5d5eb19dad505a30c2680461bd4255dba30b90

以下结论绑定这个最终字节。此前冻结 identity `764196...` 及本人的半密度陈述重构分别留原稿，不倒写审查过程。半密度上界是在仅收到该接口陈述、未读shared halfdensity证明/代码时重构；工具此前已知，任务也提示可看半槽。identity是先读冻结证明后攻；新hitting命题是本次全文读后攻击。没有把三者统一冒称statement-only。

## 总判断和未做事项

三正式数学合同在其各自域内均没有standing fatal objection：

- `UM-UNIT-READOUT-PRUNED-FOREST-IDENTITY-v1`：一般arity、C∈[1,2)的实际σ与逐变量mandatory r森林packing等价。
- `UM-UNIT-READOUT-HALF-DENSITY-THREE-HALVES-v1`：额外d_c<=2A_c后，所有深度/wiring都有实际C<=1+floor(k/2)/k，unit<=1。
- `UM-PRUNED-TREE-LEAF-HITTING-v1`：完整叶域内的精确最小命中q^h及最大r-free大小k^h−q^h。

本次只审数学。没有读取或审计主文链接的程序、JSON原矩阵、六证书的软件运行、matching程序或后续64-open代码；原先自己的单独数学/代码任务另有原始记录，本报告不将其混成新canonical程序审计。§5最终Paper Fact增加了删除big-item players及回填floor(M/2)限制；本次未重新读BCG原PDF，全球来源核查由实际读原文者记录，该比较不是三个自足证明的承重前提。

## I. identity的每个原任务及全部mandatory变量

selector使每变量恰有一个active根，不能丢弃不利变量，也不能用单一全局根只覆盖有利可达分量。每active内部点已有原sigma的unit incoming；其k条小outgoing的父置数<=floor(k(C−1))，所以至少r=ceil(k(2−C))条原已下传。只选择这些原下传job中的r条，内部child因对应原父边在child端而继续获得unit incoming。

一次定义完整正规形：active节点保留r下传、k−r父置；inactive全部父置。每active负载正好1+(k−r)/k<=C；inactive父边在父端，自己仅k小outgoing合1。因此没有漏掉被剪掉的jobs、未选轨或重复给inactive计父边。选中的外叶全是原外叶子集，C<2且unit外端时间1保证原每slot至多一job；复用原slot即可，不需重新调用分数残余容量。

反向给森林及slot注入时同一赋值规则立即给每枚原job唯一原有限端、全机负载界。A0但有port只令该port不能外送，父端仍有限；森林若需要它就确实无法注入。这个一般arity域本身没有三半可行保证。

整数边界全部正确：C1给r=k，C<2给r>=1，k1/h1无隐含除零，V空按空森林/空job及闲置dummy处理。r按有理乘法向上取整，不按分母数值枚举；显式树扫描加一次全job赋值及现成slot复用均总位多项式。

## II. 全深度半密度证明没有丢祖先兼容性

半槽证明给全部jobs同一次matching，先于最终σ和森林剪枝。因此不是先冻结叶容量、后假装祖先还能实现。

每树机器恰一枚incoming时间1（根selector/非根父边），以及k枚outgoing时间1/k。将incoming半片排首，再配k枚outgoing半片；外unit把每clause的ports半片成对使用，需ceil(d_c/2)<=min(A_c,d_c)台。每job两真实端各半、每槽至多两半片，所以Hall覆盖所有jobs。若incoming在该机被匹配，它独占第一槽，其他outgoing至多floor(k/2)枚；若incoming不在该机，最多全部k枚小job，负载1。每外unit只有一个槽，匹配后至多一port时间1。

本证明同时核了根、任意深度非根、所有外部机器，不要求统一选符号或逐层统一朝向。k1上界1；A0时密度前提必d0；空变量和binary A截到arity合法。分支/树深压缩参数不能用来把指数生成成本叫作polylog。

14机15任务的split四clause锐例确为k2h1。给出的实际unit见证需保留第一clause的一枚x+port在selector旁，外送数变2,1,2,0；不能沿用scalar例的3,1,2,0并把三枚unit job塞进两slot。该例无C<=1且全负载半整数，真实OPT3/2。它只使绝对T1上界锐；自身OPT3/2，不能充当算法近似比3/2的tight示例。

把C0=2−ceil(k/2)/k代入identity得到r=ceil(k/2)，所以额外密度域的**每种**wiring都可packing这种mandatory森林。canonical已准确升级旧有限反例的弱范围，同时保留一般arity域不能套这个结论。

## III. §7的模型与代数计数

k4h3每sign有1+4+16=21内部机、64ports。七变量unit全cube为294内部+512unit=806机器，7 selectors+280内部边+896ports=1183jobs；scalar比较是294+128=422机器，外端改1/4，不能混为unit资格。64全正及64全负source中，3真4假使每clause真出现为3或4，完整所选sign树下传给C1。全cube任意赋值都有七真clause，弱阈值6无解，与每个特定wiring的source-independent三半调度不矛盾。

局部私有host模块的pins是不同合同：42内部+128hosts=170机器，169basejobs+128pins=297jobs。全开一轨给C1；只开负轨digits<2的8叶给二叉pruned C3/2。C<2不可能激活全闭子树，否则一直至少向下传一件最终到闭host形成2；负根只能向首digit0/1两分支下传，至少两枚1/4留根，负载>=3/2。此推理是针对含pins模块直接作的，不把它套进nopins identity。

这些代数计数也吻合六证书总4440jobs、2544loads，但本次没有核软件逐项读出的事实或128赋值枚举。

## IV. hitting精确递推及所有边界

q=k−r+1。若root有至少r个children各含R-avoiding r子树，就能拼出rooted avoiding子树；故R是命中集当且仅当至少q个child的R限制各为命中集。叶base H0=1给Hh=qH_(h−1)=q^h。固定q个children递归取红q子树达到该数，其叶必与任意r子树相交，因为每层r+q=k+1强迫公共child。补集最大r-free大小因而是N−q^h。

双色提取同样正确：blue-good节点有至少r个good孩子；root good提取纯蓝r子树，root bad至少q个bad孩子并递归提取纯红q子树。这给显式全树上的线性DP及多项式证据构造/核验，不需要枚举全部r子树。

r1时命中集必须全部N叶，rk时任一单叶已命中唯一完整k树；h1是任意r子集的q点命中门槛；k1唯一链只有一叶。输出复杂度以显式完整树或完整叶地址域为准，不能把只有二进制h和稀疏叶描述的隐式巨大树混入。

补叶的严格不等号正确：|real|<q^h使其不能命中全部r子树，故virtual补集含完整r子树；但仍需这些dummy叶的外部资源能同时容纳，叶域定理不替代clause packing。等号存在锐blocker。正文“数量>=q^h不保证命中”应作一般数量不足以判位置的范围陈述，不是说h1/r1/rk等每个边界都存在此失败；正式hitting公式已准确覆盖这些边界。非退化反例可取k4h3r2，选27个真实叶避开某一固定二叉子树，其数恰阈值但仍非blocker。此为说明性精度事项，非formal Claim的fatal。

## V. 64-open坏模块的独立数学证明

k4h3r2，q3。全digits<3的27叶是完整3-pruned子树，其叶命中每个二叉子树；补集F有37叶且无二叉子树。正开F，负开任27叶子集F，总开64；两轨open集合都r2-free。

任何C<7/4调度若C<1已被selector排除；其余C∈[1,7/4)给ceil(4(2−C))>=2。闭host的pin1加port1是2>C，所以激活递推选出的叶必须全开放。在所选轨每active节点至少两下传，从而提取完整二叉子树，其叶全open，矛盾。这只复用激活计数，不非法引用nopins identity。

任选一枚open叶，将selector放其轨根、沿单路径的edge/port下传；每active点incoming1加3枚1/4留本地，正好7/4；所有inactive点小jobs合1，所有未选ports父置；选叶host pin0加port1，其余hosts只有各自0/1pin。全部169basejobs及128pins完整分配，实际C7/4。因此无需等待代码就有一般下界及显式上界的真OPT7/4。

对照只开正轨64叶时，完整正轨全下传、负轨全父置，所有负载<=1；selector又给>=1。同样64开放数量产生OPT1与7/4，确实否定忽略祖先兼容性的“仅叶容量冻结”恢复合同；不否定第6节一次共同matching的dense模型。本报告没有声称运行待补的64-open程序。

## VI. 超半密度、空YES及r1

若每变量正负出现相等，每变量无论取何值总真occurrence恰该变量总出现一半，故任何赋值总真数为md/2。非空m>0、常数arity d>2A使总真数>mA，因此strict YES为空。这个论证只针对该平衡源域，不能排除不平衡、constants或dummy padding的其他合同。

r1时每变量选一sign根的一条叶路径，内部骨架私有，选择一个可达clause slot就足够，等价变量到可达clauses的容量匹配。binary A可截实际变量数/arity，至多变量数次增广给实际路径及σ，确实总位多项式。因此该阈值区域的可行性已可判；用于promise-hard source的归约必须处理这一事实，本文没有无假设宣布一般困难性不可能。

最终standing：三个限定数学合同和新模块真OPT7/4均无fatal。程序审计、原文Paper Fact全球完备性、新颖性与外审未在本次认证；一般UM-TARGET-v1及其反面仍未解决。


---

# 单位读出森林及半密度边界：冻结全文实际审查

对象：`research/current/unrelated_machines/unit_readout_pruned_forest_boundary.md`。

首次全文读取SHA256为 `cf11045c27b8c1849af8f928aea96d0f813991e0cd0653586e5b426624c68f39`。发现并反馈§5外部Paper Fact的预处理适用范围后，root仅修正该句。最终实际复核SHA256为 `225441481810c629afb4af0bcb5d5eb19dad505a30c2680461bd4255dba30b90`。

**最终standing fatal objection: NONE**。三个精确Claim在所列域内成立；未发现尚存的证明断点。本记录不认证外审、新颖性、独立论文价值或一般UM反面。

## 独立来源界限

- 森林IFF在只给精确Claim时独立重构，未读root正文或原两树文件，另有 `unit_readout_pruned_forest_identity_statement_first_review.md`。
- 全高度half-density构造是在已经知道标准ST/先前双轨half-slot技巧后独立转用，不称未知工具的盲审或新算法；随后写了自足半槽实际构造与审计。
- 六份原P证书、一般hitting阈值、bad64例和sourcebalance段均属本次最终全文读后攻击，不能合称先陈述盲审。
- 数学全文审查不自动升级root为兼容A0所作的软件小修。原90c源代码hash仅是来源，不声称最终code未改。

## 1. IFF对象与两个方向

§1明确selector只能两私有root、internal edge只能parent/child、port只能parent及所属clause单位机；没有额外背景负载，clauses机器不交叠。正是必要域：若给port额外外端，原σ可能绕过指定clause，IFF不能随意放宽。不同clauses单位机不重叠保证注入等价逐clause计数。

对实际C<2，每active内部已有unit1，留父小jobs数≤floor(k(C−1))，故外送数≥ceil(k(2−C))=r。实际外送r子集递归对每selector分别执行，覆盖所有mandatory变量。每slot实际最多一port，所以所选叶继承原σ注入，无fractional残容量假设。

反向及正规化中，所选边送child/slot，其他所有jobs统一放parent。active负载恰1+(k−r)/k≤C；inactive没有被送来的parent job，全部k个outgoing只负载1。未选整轨、剪除分支后代、所有原任务和unit机均计入。不是只构造partial solution，也没有在中间迁移态假定负载界。k1/h1/C1/精确ceil边界/A0均正确。空变量显然空job，必要时dummy；复杂度按显式原树而非binary(k,h)压缩表示，原scope问题已明确。

A可截q=min(A,arity)而不改变可行性：任意调度使用的distinct单位机数不超过该clause port数，可对同等资格的units重命名至前q并保留每机负载。A0端仍留内部有限边，合法但可能阻止选中leaf。

## 2. Paper Fact适用范围修复

亲读本地已登记BCG TR-848-09原作者PDF印14–16：Definition4.3的M-pyramid含全部sources、原sinks、branching下界，技术上forest；Definition4.5前先删除有至少两个big items的players。Lemma4.6的精确M correspondence用于剩余子实例的dependency graph；Lemma4.7回填只保证floor(M/2)。

初稿泛称全部InfDegreeOne exact对应不够精确；最终正文已按此修复。该外部事实不作为本页三个Claim证明依赖；本页也准确指出selector的一出边选择不能被偷换成统一M≥r branching点，及旧单mandatory根b*模型不能自动强制全部变量。修复后无站立异议。

## 3. 半密度全高度三半及奇k界

给每internal incoming半片强制首，后k个outgoing半片两两成槽；clause的d叶半片两两分到ceil(d/2)≤A个真实units。每job正好两不同槽，每槽度≤2，Hall边计数覆盖所有jobs，完全是ST半质量有序槽的特殊化。

若大incoming选本机，占首槽，剩余outgoing匹配数至多floor(k/2)，故实负载≤1+floor(k/2)/k；若未选，全部small总1。每外unit只有一槽，实际≤1；未用完整原unit零。所有变量selectors在同一次matching，未独立挑最有利局部任务。k1且V非空时上界1、selector下界1，OPT1；V空OPT0。A0在dense条件下强制d0，直接旁路即可。

3/2是绝对T1上界的class锐性，正文正确没有宣称approximation ratio紧。split四clause子例确是h1/k2且d3≤4；把一x+ port留根后外部计数2,1,2,0，各clause可注入两units，x+负载1.5、其他rails≤1。此前实际下界和half-grid证明可复用，无需把806单位例误称有已证OPT下界。

## 4. 六份完整原P证书的实际读取核验

亲读certificate JSON，输入SHA256 `b44ee0f44485f2e1497b87338106d642beaa85b96196a810c569b4d120febefd`。实际运行独立读取器 `unit_readout_two_tree_independent.py`（不导入生成器），code SHA `6bb5272d8387c6e8998d534ba4fccade0227cb492a79601d381784e31ded9c8f`：6 complete certificates，4440 jobs、2544 machine loads、两个NO版共256源赋值，全部pass。

计数独立反算：k4/h3每sign internal1+4+16=21、internaledges20、ports64。七变量internal294，basejobs7+14*(20+64)=1183；128clause各4units给806 machines，单外端版给422。binary pruning每var active internal7、外叶8，共56外ports。负literal且总负数≤4的clauses每variable有1+6+15+20=42个，正文保守“至少32”成立，足放8叶；其余ports与剩余occ可双射。所选外port计数≤4，各unit可注入。完整cube128个符号clauses使每源赋值出现全7真clause，弱阈值6也失败；而这些实际σ是3/2。

YES版masks确为64份0和64份127；3真4假使每clause真数3或4，完整selected sign树外送64叶/var，真实C1，selector给下界1。单外端1/4版不同成本仅比较，正文没有导入unit IFF。

private模块42internal+128distinct private hosts=170 machines；basejobs1+2*(20+64)=169，128个0/1pin给297 jobs。实际读取128 private_host一一不同。两full-open profile C1；only8 negative binary-leaves profile C1.5。C<2进入全闭子树必最终到closed host造成2；正轨全闭、负根至少两条全闭分支，所以其unit selector+两件1/4本地jobs已≥1.5。lower与upper一致，且pins域明确在IFF/dense之外。

## 5. 叶命中精确阈值

令q=k−r+1。高度h的红set命中每个r树，当且仅当至少q个child的红限制各命中该child的r树：不足q便有r个child各给避红r树；至少q则任何r个child都遇一命中child。child叶不交，最小代价递推H_h=qH_{h−1},H_0=1，得q^h。固定q-ary subtree叶达到，取补集给最大r-free N−q^h。

双色算法同样正确：blue-good按至少r good children递推；root bad则至少q bad children，递归提取纯红q树，其叶必交任何r树。k1/r1/rk/h1边界无误；显式树或叶地址的构造复杂度说明准确。strict padding条件也正确：真实叶数<H才必有全dummy r树；同等H可以已经成为锐blocker。共同外部资源容纳dummy仍为额外条件，未由叶set定理免费推packing。

“真实叶数≥H不一般保证命中”应读作一般不足，而非对退化h1、r1、rk也断言存在同大小坏摆放；本页正式Exact Statement没有错误量词。若需句式绝对无歧义，可加“一般”二字，非修复证明所必需。

## 6. bad64私有host反例的独立实际回算

不用其生成器，直接从六cert的完整private原P复制到内存并改pin：F为4^3 words中并非三位全<3者，|F|=37；正轨开F，负轨开F中lex首27，合64 open。递归blue-good谓词实际确认两轨均无binary-pruned tree。对正轨单路径(0,0,3)只下传该路径jobs，其余放parent；所有pins按新open集合0/1，逐job重算170 machine、297 jobs，最大负载恰7/4。

一般lower：C<7/4且selector使C≥1时r=ceil(4(2−C))≥2；内部激活递推必须产生某轨全二叉树，叶只能在open hosts（closed pin+unitport会到2）。两open set均r-free矛盾。单路径upper中active1+3/4、inactive1、host≤1，故真实OPT7/4。对照仅正全64 open的C1确为OPT1。此只反驳忽视祖先兼容性的任意半数开放恢复，不反驳第6节无pin的一次全局matching。

## 7. source balance、padding及r1边界

每variable正/负occ相等时，任何赋值的真occ总数固定为全部occ/2=md/2。因此m>0、uniform arity d>2A时，要求每clause真数≤A的严格YES为空。限定m>0避免空公式，且正文未泛化排除不平衡源、constants或非uniform padding。

补叶必须同时避免纯dummy r树以及验证其外部资源packing；hitting定理只给局部set门槛。超过dense模型后，要解码的是每个全变量r森林，而不只是完整sign赋值；这一未解决义务没有被有限证书隐藏。

r1时每变量可任选一sign的一个root-to-leaf路径，只需变量到可达clause slots的容量匹配，maxflow按min(A,leaf count)实现，无numeric A展开。选匹配叶后唯一parent路径和IFF给实际schedule，方向准确。

## 最终状态

在最终SHA `225441481810c629afb4af0bcb5d5eb19dad505a30c2680461bd4255dba30b90` 下：forest IFF、half-density全高度ST推论、叶命中阈值均证明闭合；6cert和bad64数值/结构检查一致；Paper Fact适用范围已修复。没有尚存fatal objection。更广的源归约、外审、新颖性和一般UM目标仍不由这些结果完成。


---

# 完全分枝树的叶横截集与平衡源计数：先陈述独立审查

本稿只按root提供的精确陈述独立重构；未读hardness_route本次新稿或代码，未改repo/Git。一般树结论成立。平衡源推论需补“至少一个clause”的前提；空formula是原未加前提版本的真实边界反例。

## 1. 精确对象

整数k≥1,h≥1,1≤r≤k。T是完整k叉根树，所有原叶在深度h。r-pruned subtree包含原根，所有选中内部点恰保留r个原孩子，全部输出叶仍在深度h；不能提前在内部停止。其叶集合大小恰r^h。

记t=k−r+1。要证明：最小叶集合H使它与每一r-pruned subtree的叶集合相交，恰需t^h枚；等价地，最大的D⊆Leaves(T)若其内部不含任何完整深h r-pruned subtree，其大小恰k^h−t^h。

这里“D含子树”仅指该子树全部叶在D；其内部点是原树节点，不要求另有叶颜色。叶子树的全体路径由叶地址唯一恢复。

## 2. 更强的二色递归二择一

把H叶标红，补集D标蓝。自底向上标记good：叶good当且仅当蓝；内部点good当且仅当至少r个孩子good。

- 根good：每个选中good内部点取恰r个good孩子，直到原深度h。实际得到蓝色叶的完整r-pruned subtree。
- 根bad：每个bad内部点至多r−1个good孩子，所以至少k−(r−1)=t个bad孩子。各取恰t个bad孩子递归到底，得到一棵t-pruned subtree，其t^h枚叶全部红。

两种不同颜色的r-pruned与t-pruned subtrees不可能同时存在：在共同根，两个孩子集合大小r,t且r+t=k+1，所以至少有一个共同孩子；沿共同孩子继续h层必到共同叶，与颜色不同矛盾。

因此给任意叶二色配置，都可实际提取“蓝r子树”或“红t子树”恰一侧。这不是只给存在性或平均计数。

## 3. 最小横截集及全部参数锐性

如果H碰每个r-pruned subtree，蓝D不含一个，根bad，前述算法实际提取t^h个不同红叶，故|H|≥t^h。

反向任意选一棵t-pruned subtree，把其叶集合H作为横截集。上一节的逐层孩子交集论证说明它与每个r-pruned subtree相交，且|H|=t^h。于是最小值恰t^h，取补集也给最大无r子树叶集合恰k^h−t^h。

这也给另一简短递推：根被H阻断当且仅当至少t个子树分别被其局部H阻断；令τ(0)=1，则τ(h)=tτ(h−1)=t^h。所有k,r,h的锐例都实际存在，不是渐近界。

边界逐项核对：

- k=1,r=1：只有一条深h路径及一叶，横截数一，无子树最大叶集零。
- r=1：r-pruned就是到任意原叶的路径，H必须含全部k^h叶；公式t=k正确。
- r=k：唯一r-pruned是整树，任意一叶横截；t=1正确。
- h=1：选r个根孩子，最小打断所有r子集需k−r+1=t个叶。

若允许输出树在深度<h提前停止，该陈述将是另一个模型，不能沿用本证明。

## 4. 显式构造、提取与位复杂度

对显式树用一次后序扫描计算good，每节点计good孩子数；然后从根按固定孩子次序提取r个good或t个bad孩子。用显式队列/栈实现，避免深h带来的语言递归栈限制。所选边均原边，非根唯一父亲、全可达，每选中内部点恰指定孩子数，输出叶全原深h。

时间O(|V(T)|+|E(T)|)，输出大小至多原树；计数、节点标签及叶集合输入的位处理也多项式。计算t^h和k^h的整数位长受显式树长控制。

此复杂度按**显式展开树**计，或按足以显式编码全部输出路径的叶地址输入计；不承诺对仅二进制(k,h)的压缩树poly(log k+log h)。尤其k=1时唯一叶数一，但输出深h路径有h条边；若只给高度的二进制而不提供显式路径，就不能以“叶数一”误报多项式输出。

## 5. Unitforest dummy逃逸的准确条件

若某条rail的真实occurrence对应叶集合R，且

    |R| < (k−r+1)^h,

则它不可能是所有r-pruned subtrees的横截集，故补集dummy叶D必含完整r-pruned subtree。上面算法直接提取它，所用全部叶都不是真实occurrence。

严格小于不能改成小于等于：大小恰t^h的固定t-pruned blocker就能使dummy无任何r子树。另一方面，|R|≥t^h也不意味着必然阻断，仅存在这样的极值blocker；实际布局仍需DP核对。

这个结论仅提供rail树内的纯dummy组合选择。它不证明dummy物品/任务的外部机器有容量，也不证明多rail同时可pack，更不保证共享dummy资源不冲突。只有另行核实outside容量和联合唯一性无阻，才能把提取结果转成所研究物理网络的真实逃逸。它不排除全部unitforest或多层一致性编码。

## 6. 平衡出现次数的严格源空性：必须非空clause

假定源有m≥1个clauses，每个真实arity为d、严格要求true occurrence数≤A，且d>2A；每变量的正occurrence数与负occurrence数均为t_v。任意Boolean assignment恰使其一整种符号的t_v枚occurrences为真，因此全源真occurrence总数恒为

    Q=sum_v t_v = md/2.

若所有clause均满足，则Q≤mA，但md/2>mA，矛盾。可乘二全用整数避免奇偶误读：总arity md=2sum t_v自动为偶数。重复literal照真实occurrence重复计数，也不改变结论。

所以非空、全局符号完全平衡、每clause严格阈值低于arity一半的这个源类根本没有严格YES。要使相应归约有非平凡completeness，必须打破这组全局计数假设（或采用改变arity/budget/degree的有效padding）；本计数本身不提供任何padding可靠性或新的NP-hard源。

**必要边界反例。** m=0时所有变量可正负出现各零，"每clause arity d>2A"也真空成立，但空formula有全部assignment作YES。独立审计用三变量给八个满足赋值。因此无m≥1前提的“YES为空”全量词版本是假，需明确修正；树横截集结论不受影响。

## 7. 有限独立核验

独立代码 `independent_pruned_tree_duality.py` 不导入任何同行程序；默认stdout在 `independent_pruned_tree_duality_audit.json`。在26组(k,h,r)小参数中完整枚举全部r-pruned叶集合及全部264332种叶染色，逐例比较显式tree DP结果与枚举横截性质，并检查提取树的原边、唯一父亲、实际各内部度、叶深度及红/蓝身份。覆盖k1至h6、k2至h3、k3/k4至h2及各r。

另用k1,h1000的显式1001节点树检验迭代提取1000条边，无递归栈假设。平衡源用三变量八个signed full clauses、A1、arity3，逐八种赋值回算总真数12>预算8；空formula负控制给八个YES。

冻结代码SHA256

    0527cce3e88cbf4c7828c3c6a098286ab6457cce224069c12f237ff597a04165.

有限核验不是一般证明；一般证明在第2–4节。

## 8. 已知机制、文献事实与新颖性分层

该DP等同于read-once递归r-of-k threshold Boolean formula：蓝叶输入一，内部gate输出一当且仅当至少r子gate为一。本叶横截集就是一个0-certificate，r-pruned蓝叶是1-certificate；递归证书大小给t^h和r^h。这是非常基本的递归threshold机制，不能包装成新组合技术。

**实际核实的Paper Fact仅限模型祖先。** Magniez–Nayak–Santha–Sherman–Tardos–Xiao, *Improved bounds for the randomized decision tree complexity of recursive majority*, primary PDF https://arxiv.org/pdf/1309.7565 ，§2.2（PDF第4–5页）定义完整三叉树上逐层多数的3-MAJ_h，即本k3,r2特殊情形的递归threshold模型。该文引言亦讨论其基本2^h读取量级。未找到本次全(k,r,h)精确横截公式的命名定理定位；不把相近模型或query-complexity结果偷说成已核实的通用横截定理。

**Interpretation。** 本证明是这一经典递归threshold/certificate机制的直接自足应用；其研究价值可能在于约束具体unitforest padding参数，而不是公式本身新颖。**Novelty。** 未认证全球优先权、独立成文价值或外审，不作新颖性宣称。

## 最终审查状态

树Claim按给定显式全树、完整深h剪枝定义成立，构造和提取总位多项式；dummy逃逸只在outside/联合资源另经核实时才是实际调度结论。平衡源推论加m≥1后成立，原未加前提版本有空formula反例。未读同行新稿、未作repo/Git/公屏操作，未升级一般UM-TARGET-v1。
