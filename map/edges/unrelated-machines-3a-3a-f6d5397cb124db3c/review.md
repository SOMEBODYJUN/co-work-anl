# XOS福利两算法合同及CF通信障碍比较

## 任务、版本与实读边界

审读身份：Boss6。任务：`unrelated-machines-3a-3a-f6d5397cb124db3c`，3A主覆盖仅 `M-bafae50558c441728f16cbfc7dce9f82`（version 2，pin `73243ca77a1d4fdf7c89c8e99d9cd60264cfbdf6d1ee671b1adec63d6d0dfefd`）。共享端点为 `M-8fdee11afd164305a429734ee5ae705a`（version 2，pin `5a4576c51598ca30c504ceff1d46a7f61cbf24c25cb4816468ee635b78297a7f`）与 `M-bcf19c1d04ba4f39b746241304786dc1`（version 2，pin `186d9ce8713657ac38d25fd1e13e4a0875f808a76902d55ce134381948f76bbe`）。本次从当前task文件核得owner=Boss6、state=claimed；read-add request `e37132f904e7423198d3a2a2cb59a93b` 已在task requests内。三次只读 `research show --body` 均返回上述pins且body/evidence current。本worker未写clone、Git、队列、registry或native bindings。

共同body是 `archives/unrelated-machines/state/文献/组合拍卖与投影游戏集合覆盖两篇文献整理--文献.md`，SHA `ee4b62663ff651341ae40162b5319b31b9230d71c93b81333d43cfbf92d4fb22`，本次完整读过，但第二篇Set Cover/PGC的摘要仅作排除无关来源的定位，不用来制造关系。关键primary是同档evidence的 `dobzinski_auction.pdf`，SHA `d0700d7674db45b4330d558c731c0200567f2c7a999f5eef7952029cab26dd15`，15页；使用既存layout文本 `dobzinski_auction.txt`（SHA `d97e661087cfa4972ed4635c045982d98d28a53bbdd4b4a993fb509f4d6acafc`）阅读文本行1–350与452–656；另直接渲染、视觉核对PDF页8、9、10的公式、算法和proof。必要完整范围为§2/§2.1、§3共享LP/舍入/接口段、§3.2及Lemma3.3完整证明、§3.3及Lemma3.4–3.6完整证明和紧例、§4.1完整归约（PDF页10–11）。PDF页1–5的引言和模型段一并读过，页6只读共享段及§3.1开头，未实读§3.1完整CF上界证明、§4.2 XOS下界或其后机制/value-query证明；这些不作为本包推导前提。源文献内引用Nisan [15]的原始通信gap定理按本篇明确使用的外部前提继承，未另取Nisan全文；本次已读本篇从该gap到CF的完整归约，而非独立重证[15]。

成熟body关于两算法与类层次的结论是历史成果；本次重新实读了上述承重primary段，下面的合同、证明不变量、复杂度数法及比较是本次核对结果。未重跑历史validation脚本、算法实现、求解器或科学测试。细分读取见同目录 `reading-ledger.json`。

## 共同模型与访问合同

有m件物品M和n个bidder，估值单调、归一化，目标为互不相交分配的福利和 `W(A)=Σ_i v_i(A_i)`。XOS指 `v_i(T)=max_ℓ q_{iℓ}(T)`，其中clause按标准约定为非负系数的加性估值。若起始表达式允许负系数，单调性也允许将每个clause的负系数置0：置0后的clause在T上的值等于原clause在T的正系数子集U上的值，仍≤v_i(U)≤v_i(T)，且最大值不减，故得到等价的非负XOS表达式。返回bundle S的maximizing clause q具有 `q(S)=v_i(S)`，且对任意T有 `q(T)≤v_i(T)`，特别对其后保留的子bundle也成立。demand查询给价格向量p后返回最大化 `v_i(T)−p(T)` 的集合T。maximizing-clause查询给S后返回支持它的加性clause。这两个接口必须同时计入一般XOS合同。

PDF §2.1 Proposition2.1说明显式XOS表达式能按clause逐一计算demand和maximizing clause，时间为输入表达式长度的多项式；clause数本身可能关于m指数大。§2.1 Proposition2.2对submodular估值用固定物品顺序的边际值构造支持clause，2|S|次value查询已足够，归一化边际和为v(S)，submodularity保证所有子集上的支配关系。结合value可由多项式demand模拟，submodular子类只需demand即可。本文对一般XOS明确说不知道能否从demand模拟XOS查询；本包保持该历史文献的接口声明，不将其改写成一般XOS接口可免费互换，也不据此宣称当前已证明不可模拟。

引言的general-query模型允许任意种类查询，但每条查询只针对一个bidder的估值；通信费用仍按交换比特计算。它不是一个免费返回整个拍卖最优解的联合oracle。对满足XOS promise的实例，可以把合适的、有限编码的clause查询当作其允许的单bidder通信；一般CF函数却未必有满足上述支配/相等性质的clause可返回。访问模型和估值类要同时保留。

## 确定性组合算法的实际输出与证明

PDF页9–10，§3.3，Theorem3.3和Lemma3.4–3.6。本算法只依次处理bidder 1,…,n一遍，不是反复加价直到某阈值的收敛过程。初始化p⁰=0、所有已持有集合为空。第i轮，在旧价pⁱ⁻¹下取精确demand集合D_i，从此前各bidder集合中移走D_i内物品，令i持有D_i；查询D_i的支持clause q_i，仅对j∈D_i把价格改为q_i(j)。最终仍给bidder i的物品记为A_i。原文把当轮集合和最后集合分别记作S_i、A_i；此处D_i用于避免偷换其后缩水的S_i。

**可行性与支撑不变量。** 每次分配前从以前持有者夺走相同物品，所以所有持有集合一直不相交。A_i⊆D_i；每个j∈A_i在第i轮后没有再被取走，故其终价等于q_i(j)。于是 `pⁿ(A_i)=q_i(A_i)≤v_i(A_i)`。曾未分出的物品价格一直为0；把它们留空或单调地补给某人都不损害证明。因此 `P:=pⁿ(M)≤Σ_i v_i(A_i)`，这里右侧是实际输出的福利，不是LP值或期望。

**逐坐标价格不下降。** 对j∈D_i，若q_i(j)<pⁱ⁻¹_j，则利用q_i(D_i)=v_i(D_i)及q_i(D_i\{j})≤v_i(D_i\{j})，删掉j后的效用严格增加，违背D_i是demand。故每次更新坐标均满足q_i(j)≥pⁱ⁻¹_j，其他坐标不改。本次视觉核对PDF页9–10：原PDF的Lemma3.5以pⁱ记待比较的旧价格，和前文pⁱ表示第i轮更新后价格的约定有索引混用；此处正确推导明确使用incoming pⁱ⁻¹，不据错误索引改写算法。原文该证明中末尾可用的关系是 `q_i(D_i\{j})≤v_i(D_i\{j})`，前一项已有严格改善，整个反证成立，不依赖排版行末所写的第二个严格号。

**价格增量就是本轮最大效用。** 设 `Δ_i=pⁱ(M)−pⁱ⁻¹(M)`。因为仅D_i内更新，且clause在D_i上恰好实现估值，`Δ_i=q_i(D_i)−pⁱ⁻¹(D_i)=max_T[v_i(T)−pⁱ⁻¹(T)]`。这是两界间的承重桥，不是把demand集合误当作数值。对任意最优可行分配O，`v_i(O_i)−pⁱ⁻¹(O_i)≤Δ_i`；逐坐标单调性给 `v_i(O_i)−pⁿ(O_i)≤Δ_i`。相加并用 `Σ_iΔ_i=P`、`Σ_i pⁿ(O_i)≤P`，得 `OPT≤2P≤2W(A)`。若把最优分配补全为分割，第二个≤可取等号。该论证对每个合法demand/clause回答成立，固定确定性tie-breaking即可得到确定性算法，结果不依赖幸运随机选择。

**终止与复杂度。** 正文步骤直接给n轮、恰好n次demand和n次XOS-clause调用，不因价格增幅小而出现额外轮数。用每件物品的当前owner和价格维护夺取，除oracle本身外O(nm)量级的扫描/更新足够；不必按伪码逐个旧集合再重复扫描造成额外n因子。此数法是本次从原算法读取的实现上界，不是声称原文实现了仓库后端。若输入、价格和oracle返回的系数是有限位有理数，价格始终只复制返回clause的系数，不做无界次微小增量；常规运算/消息长度需连同编码位数计费。允许任意精度实数的纯oracle模型不能自动产生与返回编码长度无关的Turing时间界。本包不把n次查询数夸为任意实数模型下的免费位运算界，也不称其为原文未声明的强多项式Turing定理。

**本算法的2确为实际可达到的最坏因子。** 原文页10紧例为两物品a,b；bidder1是值1的unit-demand，bidder2只对含b的集合值1。第一轮在零价合法选D₁={b}及支持clause q₁(b)=1、q₁(a)=0；第二轮旧价b=1时合法选空集（或取走b），最终福利1，而把a给1、b给2的OPT=2。两估值皆为XOS。这只说明该算法在合法tie-breaking下的紧性，不是XOS全模型存在性硬度；它与下一节更优算法完全相容。

## LP随机舍入算法的精确保证

PDF页5–6的§3共享段、页8–9 §3.2 Theorem3.2及Lemma3.3；引言Theorem1.2把结果写为e/(e−1)。先解configuration LP：每bidder至多一个bundle、每item总负载≤1，最优值OPT*≥OPT。用demand作为dual separation，经ellipsoid等标准LP过程得到多项式大小可用支持。随后每个bidder独立按x_{i,S}选一个S_i（剩余概率取空），可能发生多bidder争同物品的pre-allocation。对每个S_i查询支持clause；把每件物品分给当前所选clauses中该物品系数最高的bidder，便得到真正可行的输出A。由XOS全局支配，逐item最大系数和≤真实W(A)。

证明中可以把每个支持clause限制到它所支持的S上（S外系数记0），以保证 `v_i(S)=Σ_{j∈S}q_{i,S}(j)` 且LP目标分解仅计算S内物品；这种删系数仍是v_i的有效加性下界，在S上取等号。若实际算法使用返回的完整clause，逐item最大值只会更大，真实福利仍支撑该和，所以不需要附加oracle。这是对原文省略集合限制记号的展开，不是另建一个数学对象。

固定item j，记 `X_i=Σ_{S∋j}x_{i,S}`，`V_i=(Σ_{S∋j}x_{i,S}q_{i,S}(j))/X_i`（X_i=0项删除）。独立选择使各i收到j的事件独立，且Σ_iX_i≤1。把bidder按V_i递减排，先考虑把j交给首个收到j者的辅助规则；其期望贡献是 `Σ_i[Π_{h<i}(1−X_h)]X_iV_i`。对每个前缀k，AM–GM及 `0≤Σ_{i≤k}X_i≤1` 给

`1−Π_{i≤k}(1−X_i)≥[1−(1−1/k)^k]Σ_{i≤k}X_i≥c_nΣ_{i≤k}X_i`，其中 `c_n=1−(1−1/n)^n`。

对该前缀不等式用非负权重V_k−V_{k+1}求和，得到辅助规则的期望贡献≥c_nΣ_iX_iV_i。真正逐item取最大系数不会更差。再对j求和，精确得到 `E[W(A)]≥c_n OPT*≥c_n OPT≥(1−1/e)OPT`，即随机期望近似因子 `1/c_n≤e/(e−1)<2`。n=1时c₁=1。有限n公式由PDF页8、9原式视觉核过。每次输出都可行，但证明给的是期望福利；不能把它读成每个随机种子都达到该比例，也不能仅凭期望给出某个指定高概率界或确定性选解程序。

与价格算法相比，该算法先付configuration LP/ellipsoid与多项式次demand查询的费用，后付每bidder一次clause查询及O(nm)分配扫描；它不是原文的无LP组合一趟算法。本文明确把更好比值归于randomized rounding，并另称2算法为deterministic/combinatorial/fast/simple。本包没有断言不存在去随机化；从“存在某种去随机化”也不能免除其具体方法、查询和组合属性的证明义务。引言中CF算法后面的derandomization句子不能直接搬作§3.2 XOS算法的全部合同，更不能推出本core所指定价格算法的每次输出保证。

## 数值改进与整条算法合同的关系

共享promise与oracle下，Theorem1.2/3.2把“可达福利近似比”由2提高到e/(e−1)，有限n甚至为1/c_n。这是实质的比较成果，保存为 `supersedes` 语境边，方向为 `M-8fdee11afd164305a429734ee5ae705a` → `M-bafae50558c441728f16cbfc7dce9f82`，scope明确只比较数值维度，而且前者为期望合同、后者为确定性实际输出合同。它不表示整个目标定理被逻辑蕴含或算法失效。

不能交whole逻辑边：core除比例≥1/2外，还明确指定确定性、组合价格更新的算法身份及其实际输出保证；LP随机舍入定理没有支付这些属性。上述n+n查询数是本次核出的该算法性质，不另将它添作原core陈述的独立要求。反向也不能把2保证升级成c_n。把“更好期望至少意味着存在一个好分配”的纯存在句称为对core算法证明的一步，会丢掉算法身份与构造义务，本包也不作此局部contribution。两个完整证明分别已经实读并保存在本review；没有把clause支配、价格不变量或一次算术另立节点。

## CF通信障碍为何与两XOS算法相容

PDF引言Theorem1.3和§4.1 Theorem4.1（页10–11）。模型结论是对每个固定ε>0，要求在所有CF实例上保证因子2−ε的协议，必须在某些实例通信指数多比特；不是每个CF实例都难，也不是对所有CF子类分别有2障碍。原文从Nisan [15]的general valuations gap继承：高情形可同时满足n个bidder、福利n，低情形至多满足一个、福利≤1；私有输入I_i⊆T_i的长度t可关于自然参数指数大。

归约令空集值0、非空集 `v'_i(S)=1+v_i(S)`。原v_i是“包含某感兴趣bundle则1，否则0”的单调0/1估值，所以新估值单调归一化，非空值落在[1,2]；对两个非空集合，右侧至少2而左侧至多2，故CF，带空集也成立。高情形的n个非空获胜bundle给福利2n；低情形任何分配至多有一个bidder拿到原值1，其余基准值至多1，福利≤n+1。选n足够大使 `2n/(n+1)>2−ε`（例如n+1>2/ε），一个普适(2−ε)算法会以实际可行输出的福利区分这两情形，继承通信下界。本次读了本篇完整归约，外部Nisan gap未独立重证。这里用≤n+1已足够，不需要额外假设每个低实例一定达到该上界。

XOS严格包含在CF内，方向可直接核：按上述标准非负系数约定，任一加性clause q有q(S∪T)≤q(S)+q(T)，最大化再各自上界得v(S∪T)≤v(S)+v(T)。严格性可用三物品例：所有非空真子集值1、全体值2。它单调CF；若为XOS，支持全体的某clause需q₁+q₂+q₃=2，而三个两物品子集的支配约束分别为q₁+q₂≤1、q₁+q₃≤1、q₂+q₃≤1，求和却给总和≤3/2，矛盾。该小例只核类严格性，不是另一个通信hardness实例或独立研究节点。

所以CF下界不通过“限制到XOS”继承：hardness对大类的最坏情形量词不会自动作用到每个严格子类。价格算法的2还恰处于下界未禁止的边界；更优XOS算法则仅对严格子类承诺，完全相容。两个算法要求支持clause，普通CF函数甚至可能没有这样的答案。不能把相容性仅解释成“general query缺demand”：原文general query允许任意单bidder查询，其通信模型本已强于这种特定访问；重要差异是promise、可返回对象和通信位数，而不是查询名字。

显式XOS语言的多项式时间是按描述长度算，描述可关于m指数大；general-query下界按自然参数/通信算。一个读取指数长显式表达式的“输入长度多项式”程序，完全可能花费自然参数指数多通信。反之，oracle算法的多项式查询数也只有当价格与回复有限编码、长度受控时才对应多项式通信。不能跨这两个度量免费搬运复杂度。由此保存 `M-bcf19c1d04ba4f39b746241304786dc1` → core 的 `motivates` 语境边，精确说明为何保留XOS及oracle边界；它不证明或否定core的整条算法结论，也不声称2对XOS最优。

## 覆盖、闭合与未付事项

本包两条accepted边均为语境，主core仍 `isolated-after-review`。这是对已指定三端点的实读比较结果，不是断言core永无逻辑关系。task当前没有额外overlap_comparisons/follow-up条目；原生closed_overlaps只核task已声明的follow-up对，故本收据closed_overlaps为空；已完成的core–较好XOS比值、core–CF障碍分别记入additional_comparisons，并附上述数学理由，没有必要再派同一比较。未发现需先增补对象或纠正现行registry的实质来源错误，因而没有read-add或follow_up_tasks请求。

保留的开放界限是：不能从所读文献自行推得无LP、确定性e/(e−1)组合算法或一般XOS的demand→clause模拟。这是不能冒填的合同义务，不把它包装成新已证结果，也不以needs-decision延迟本包。全部结论仅为社会福利和，不是MaxMin/makespan、SPE、平衡或单个bidder收益阈值见证。Set Cover/PGC同页的结果未参与任何边。
