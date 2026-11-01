---
id: customer-attraction/static-pne-and-residual-double-bridge-scan-short-circuit-shrink-contract
kind: program
type_tag: 程序
title: 静态PNE与残余双桥扫描的短路约简合同
status: complete-two-native-contracts-and-identical-frozen-carrier-routing
truth_status: 精确有限输入判别器与返回值约简合同；当前50客户载体不属该扫描main直接生成域；无新运行或最小性认证
review_level: 两新码完整实读及规范闭包充分实读复用；同SHA旧完整证书数学复用；非独立盲审或外审
scope: 主扫描2/3/4玩家与4/5/6标签；全历史SPE终局全集、全部静态PNE与静态m槽残余查询；约简保玩家数并可改主题/客户
summary: check先逐SPE测试PNE再测残余、frozenset早返可能遮住后续PNE；shrink只认返回kind PNE，非PNE谓词完备约简。原载体含16/9重数，scan main只生成1..8且约简不合并行，不能伪造来源链。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/global_proof/scan_bridges.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/global_proof/shrink_pne.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/global_proof/bridge_counterexample.json
---

# 静态PNE与残余双桥扫描的短路约简合同

本三源13390B：1758B双桥扫描、1608B约简、10024B冻结数据包。两码全文实读；数据包本ID `1f8acbb453e97a357dd0` 本次确有**新的正常show**，但其size/SHA256/blob及全部字节与此前充分读过的`be06cfee0feeef2d2a12`完全相同，故精确复用完整50客户/85历史数学，不重复扫描JSON正文，不伪装为复用本ID旧show。两文件名在本次实际路径/捕获中各自保留。

程序依赖、原字节及新normal捕获见[证据包](../../tools/evidence/bridge-pne-scan-and-shrink-three-primary/README.md)。本页给它们实际判定的两个量词、所有动态操作、当前数据包的生成域冲突，以及为什么原文件存在不足以构成一条已复现的发现链。

## 精确模型与规范闭包

两码从`customer_attraction`包入口导入有限类型Instance、CustomerType与ExactSPESolver；约简另导入verify_certificate。包入口691B、model8640B、exact9943B、certificate6201B共25475B，此前已逐份完整实读，本次核当前同SHA并针对构造器/全集/输出再核相关语句。没有import这些模块。

Instance中m表示单位玩家，有限共同主题标签数k；客户重数表示不同单位客户。覆盖者均分，收益用Fraction。构造器允许空覆盖主题、覆盖相同的不同标签、无客户或不喜欢任何主题的客户行；标签名字必须非空且互异，m>0时至少一题。此实现接口比要求覆盖集合互异的目录更宽；程序没有额外排空覆盖/别名，故任意未来输出须另核严格目录条件。本实际50客户包四题均非空互异，已有充分对象处理。

Instance**不合并相同兴趣的CustomerType行**，to_dict同样逐行保存；重复类型作为不同单位客户组在收益/覆盖求和中合法累加。这个实现事实决定约简中一行重数的意义，也决定后文来源链不能凭聚合猜测。

完整历史模型保所有有序前缀、空根、重复行动及任意平局。ExactSPESolver按前缀计数缓存的是**全部可实现终局集合**，不是一份计数统一动作策略。对终层R(z)={z}，递推为

\[
 L_a(k)=\min_{z\in R(k+e_a)}U_a(z),\quad M(k)=\max_aL_a(k),
\]
\[
R(k)=\bigcup_a\{z\in R(k+e_a):U_a(z)\ge M(k)\}.
\tag{1}
\]

当前动作必须面对每个真实子SPE，给必要性；反向对actual孩子保目标，对每个其它孩子选使当前玩家利润最小的合法子SPE，在不同有序子树独立拼合，给充分性。等号保平局；全零输入也非空。规范`outcomes()`返回frozenset，源scan直接迭代它，没有排序、最小福利或最坏比排序保证。`certificate(target_counts=c)`再展开一份完整有序动作表，默认选第一个合法actual动作和各偏离孩子的极小利润终局；同一计数不同历史没有被强制绑定。

## 全部静态PNE与它为何非空

`comps(n,k)`以第一坐标x=0,…,n递归，k=1时输出(n,)，对n≥0/k≥1恰枚举所有总和n的k维非负计数，各一次，共\(\binom{n+k-1}{k-1}\)个。它没有声明支持正玩家空目录或k=0；本main固定m≥2/k≥4。

对每个终局计数c，源码先算所有占用主题利润，对每个c_a>0和每个备选b检查

\[
 U_b(c-e_a+e_b)\le U_a(c).
\tag{2}
\]

一旦某项严格大便将该c排除并短路剩余比较；平局仍PNE，b=a的自身比较也遍历。这里后人**不响应**，是同输入的同时行动静态Nash定义；与(1)的顺序真实续局比较不同。压缩到计数对相同单位玩家的静态PNE是完备的，任意有序排列同样稳定，不必枚举m!排列。

为什么`min(... for c in pne)`在合法有限共同目录实例有值：取调和势

\[
\Phi(c)=\sum_Tw_T H_{\sum_{a\in T}c_a},\quad H_0=0.
\]

玩家由a改b时，仅喜欢a的客户使势减少其旧利润份额，仅喜欢b的使势增加新利润份额，同时喜欢两题的总覆盖人数不变、对这名玩家的份额也不变；所以势差等于该玩家利润差。有限计数域上势最大点无严格盈利偏离，即至少一个PNE。零客户、零覆盖题、重复标签的覆盖或不感兴趣客户行均不破坏这个存在证明。此为本页解释min的数学依据，不是本次额外运行PNE枚举，也不扩为异构/加权提供者结论。

因此源码确算

\[
P(I)=\min_{p\in\operatorname{PNE}(I)}W_I(p).
\tag{3}
\]

这是真正的**全部静态PNE的最小福利**，不是某个PNE、同时混合Nash、CCE、安全值或静态OPT。若某个完整SPE终局c有P(I)>W(c)，则所有同输入PNE都比该SPE福利高，足以反驳静态最差PNE支配桥。程序未求最低CCE或iid价格，不可由标签PNE转授其它基准。

## 残余分支是静态m槽并集查询

固定当前SPE终局c，实际客户覆盖为C。源保留每个兴趣集合与c所有占用主题均不相交的客户行，组成新Instance，**保原m玩家数和全部k标签**。它既未删除玩家，也不是固定原策略后继的尾博弈：这里只在客户被限制后的目录上算静态最大覆盖。

model.optimal_welfare枚举所有大小0至min(m,k)的互异主题支持，非负覆盖下等价于恰m槽允许重复的主题元组（k≥1时余槽可用重复补齐）。故得到

\[
F_m(C)=\max_{T_1,\ldots,T_m\in\mathcal S}
\left|\left(\bigcup_jT_j\right)\setminus C\right|.
\tag{4}
\]

未覆盖的兴趣空行若存在不增加任何query覆盖。源码只返回数值r，不存实现(4)的query元组，不要求该元组在原输入达到OPT或唯一最优。因此r>W反的是“全部可用m个主题覆盖的实际遗漏≤W”强桥；不能自动说每个原最优组合或有利重选原最优组合都失败，也不等于单题最大M(C)乘m。原27/71点分别说明这些量词的差别，见[完整版本资源](../资源/残余桥两份整数见证的目标与完整回复版本--资源.md)。

若要证明half，对某个原最优并集O应保R=|O\C|、G=|C\O|和R−G=OPT−W。r或R>W不等于R>W+G，更不等于OPT>2W。程序没有测试half比率，更不建立一般或六人反例。

## `check`的早返顺序与分类限制

先完成全集outcomes与全部PNE，随后按**未排序frozenset**逐c：先比较P(I)>W(c)，若真立即返回('PNE',c,P(I),solver)；否则构造该c残余并算r，若r>W(c)立即返回('RESIDUAL',c,r,solver)。只有全部c两项都不触发才返回None。

三个返回语义应分别保留：

- PNE：存在一份SPE实现返回c，且全部静态PNE福利都更高；不排其它SPE还有残余失败。
- RESIDUAL：存在返回c的SPE且(4)>W；**不排后面的另一个c有PNE失败**。
- None：在这份固定输入全部纯SPE终局上，两种强桥都没有被否定；不是一般阴性或对其它模型的证明。

特别地，较早c的RESIDUAL可遮住较后c的PNE，尽管对同一个c优先PNE。源没有先全扫所有PNE违例再扫残余，不能把返回kind当两个互斥数学类别或对PNE存在性完备的二元标签。frozenset迭代没有跨环境的次序合同，也不保证返回最差福利c。见证本身正确，受影响的是挑哪一类/哪一个点和后续约简的可接受集合。

## 1758B main的真实生成域和I/O

只有`if __name__=='__main__'`内启动随机扫描。import会导入规范包、定义函数，不启动2000次；本次也未import。main用Random(197)，每次先随机选k∈{4,5,6}、m∈{2,3,4}，随后对每个非空mask独立以rng.random()<.4保留，保留时给randint(1,8)重数。每mask恰试一次、每兴趣行最多一条，故所有生成实例的每行重数≤8；可能没有任何客户或有空覆盖/相同覆盖标签，构造器允许。2000是预算，不保证不同输入、均衡或目录域穷尽。

命中任一kind后，向原仓库根相对路径`research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/global_proof/bridge_counterexample.json`以w覆盖写pretty JSON，六字段kind/instance/counts/welfare/comparison/certificate；certificate由solver为所选c重构，main没有再调用verify_certificate。PNE的comparison是(3)，RESIDUAL的comparison是(4)，同一字段不通用等于原OPT。

stdout只打印kind、c、实际福利、比较值和零起j，不打印完整JSON文件；随后break。未命中每50次（含0）打印j及四舍五入到两位的elapsed，命中会在该条进度前退出。无CLI参数/输出目录选项，不清旧文件、不写完整2000阴性报告；旧JSON存在不能证明本版本完成或命中。未提供stdout/stderr/exit或原环境，本次不补造。

## 1608B约简的实际变化和停止含义

约简顶层导入canonical四名称，并以**相对导入**`from .scan_bridges import check,comps`读取本1758B函数。`comps`和time在约简文件未直接使用；check会用scan模块自己的comps。正确执行需有包上下文建立__package__；直接当孤立脚本运行通常不能解析这个相对导入。同时base读取仍是上述仓库根相对路径，不因模块位置自动改变cwd。没有main guard，import会启动读文件/搜索/校验/写入；本次没有import探路。

唯一JSON数据输入是本批实际已取得的bridge_counterexample.json。源只读取其instance，**忽略原kind/counts/welfare/comparison和85动作证书**；后续每个trial重算全部SPE和全部静态PNE，允许换成另一SPE终局和另一整棵离轨策略。不保原actual路径、原target或certificate，只保原玩家数。

每轮先尝试逐主题t删除：从每客户兴趣集合去t，索引>t减1，若新兴趣空则直接丢该客户行，否则保原multiplicity。主题改名为0,…,k−2的字符串。它不是只删一个动作而固定客户编码：只喜欢t的客户会变得无兴趣并从表示中删掉，其余顾客的兴趣重新映射。不同原类型可变成相同新类型，但Instance不合并，仍是多条客户行。剩余主题的覆盖可空或互同，源没有检查严格集合目录。

若check(trial)返回且kind恰PNE，则接受第一次这样的删题、打印topic并立即重开外层，优先继续删题；返回RESIDUAL时即使另一个SPE有PNE失败也拒绝。没有删题被接受才试逐客户行i，把其重数按0,1,…,旧重数−1从小到大试；0删除这一行，正数仅替此行。第一项返回PNE即接受，打印weight/i/val/当前客户数/行数，再重开全部删题和减重。两行同兴趣时，也不将它们的总质量当单一坐标。

对本实际50客户初始输入，四题大小30、34、31、41，任意四玩家终局至少覆盖30；残余可覆盖量≤50−W≤20<W，所以**不可能触发RESIDUAL**。已有完整SPE福利49而所有PNE福利50，故初始check必返回某个PNE见证，和frozenset顺序无关。这样实际入口的PNE不变量充分；未来约简trial则未必还有这个静态界，早返屏蔽仍真实影响接受集合。

成功删题使(k,总客户数)的第一坐标严格下降、第二不增；成功减一行使第一不变、总客户数严格下降。有限非负整数的这个字典序势保证在合法入口不无限接受。PNE失败不可能在只有一个主题时发生，所以从本正入口不断接受PNE trial不会到正玩家空目录；程序并无专为任意坏schema/k0提供兜底。

终止时，已经试过所有单主题删除以及每一条现存客户行的**所有更小重数**，均没有被返回值谓词“check返回PNE”接受。这只是源的greedy/oracle局部固定点。它不证明真实“存在PNE失败SPE”谓词下所有这些trial都失败，因为较早RESIDUAL可挡后面PNE；更不证明全局最少客户/类型/主题，或不需先增后减、多坐标变化的其它更小输入。逐删优先和行顺序都影响结果。

最后再次check(inst)并解包，直接把返回kind写入obj，没有显式assert kind=='PNE'；存在PNE失败保证某一强桥返回非None，但代码未把类型重验写成单独条件。随后重构所选target完整cert，并调用verify_certificate(inst,cert).assert_valid()；该代码路径是全树SPE证书校验，不是另一个独立定义级PNE审计。本次未运行，不能把源里的调用当观测到的验证成功。

输出文件是**pne_bridge_discovery.json**，以x排他模式新建，非pne_bridge_reduced.json，也不覆盖bridge_counterexample输入。目标已存在会报错；没有新输出事件或源清单中的这个文件，不补造原成功。stdout混合进度、去certificate后的五字段JSON、最后`print('path',cert)`的对象表示，不能将整段stdout当一个六字段JSON报告。原source没有步数/耗时/最终最小性证书。

## 当前10024B数据载体的明确来源边界

原包六字段、50客户九类型、四玩家和85个完整动作已由[现存充分资源](../资源/全局覆盖入口的静态PNE证书与净差合同--资源.md)完整承载：AB1、AC2、BC1、ABC5、BD2、ABD16、CD8、ACD6、BCD9；actual ADDD福利49、静态PNE比较50。与be06原pne_bridge_reduced.json逐字同SHA/blob，数学复用不重新认证或改旧正文。

但**它不可能是本1758B扫描main的直接输出**：生成域每mask单行重数1..8，本包却含16和9。即使假设接上本1608B约简，它只删题并逐行保重数、或把一行减小；构造器/序列化不合并重复类型，所以从main原始≤8各行出发仍不可能出现单行16/9。当前代码与载体之间没有提供这样的同字节生成链，不能说它由这两原件本次或历史已复现地产生。

程序函数check本身不受随机生成上界约束，**可以消费**这个实际50输入；约简也确实把它当输入。能够消费、文件名常作发现输出、以及同SHA冻结版本存在，是三项不同事实。这里不猜谁何时复制/合并/改过版本，不根据这些路径补造新日志或原运行。shrink忽略原85动作并重新挑全SPE，输出若有也未必与冻结同完整策略或字节。

## 关系和实际保存状态

静态PNE支配桥本仓已有三人16客户例和[全部历史严格唯一的12客户例](../反例/全部历史严格唯一均衡与静态PNE福利的分离--反例.md)，50载体不是新一般失败机制。残余m槽界与[27/71原版本](../资源/残余桥两份整数见证的目标与完整回复版本--资源.md)及[唯一最优参数族](../反例/唯一最优组合的全遗漏支付--反例.md)各保原模型、原actual和唯一性合同；本check不做唯一最优约束，不能直接继承那些优化器/参数族结论。

本3实际16XR全16 claim pushed `9f40d76914d79901dfe630474f1f2448653ce815`、owner Boss4/in-progress与原SHA已核；raw local_sync=needs-attention原样，独立恢复证明2untracked+2tracked同字节、无missing/different/unmerged、stash保留并列保存，不称synced。原JSON本ID是新normal，数学是旧sameSHA充分读复用；两新码则本次全文主读。

0原scan/check/shrink/规范import/证书重放/新数学checker，0Git/共享R写或自claim/done。代码的if/verify调用和有限域只是实读出的合同，当前没有stdout/exit成功事件。独立stage保存正文、原件与完整认领/取得捕获/逐源收据，由Root先checkpoint数学再done。
