# cagec68 正式数学比较

本稿属于任务 `customer-attraction-3a-3a-ec68c7458819c0fb` 的正式 fresh primary 阅读与比较。只写本 staging；clone、源文、registry、Git、队列均未修改。全部 Python 使用 `-B`，没有运行 LP、完整 SPE、IC、DP、价格发现、旧证书重放或新448格枚举。

开工核实任务仍为 claimed，owner Boss6，request `ab4c64f9f8144271b4e6ffec72af82e7`，definition pin `2c22d235ac9abd30bc0ed210eec5acc3e9c63b5b5dd46312d014cab604b488fa`。四 core 和 CAG-MODEL 的当前 registration pin 与 task 五项完全相符。任务无 `overlap_comparisons` 字段。ready 所报 remote `b8eba4b8f2fbd64d7da81b62d0d56d90a0e83a31` 是 Root 的已发布快照来源；本 worker 没有运行 Git 或网络验证它。

本轮独立完整实读五份当前 registry 合同、三篇不同主文、全部任务 reading_refs 的规定范围：14 个去重 Markdown 文件，其中12全文、2精确章节。448表正文的全部64行/448个系数已读。字节SHA检查、预研、Root既有阅读、文中历史原代码/JSON/运行声明均没有冒作本 worker 的新全文阅读或执行。精确范围见 reading-ledger.json。

为便于叙述，A是actual4无K八slack上包络；B是actual2/3/4共同K三上包络；C是六安全actual价与平均CAP七行；D是完整旧八词hist条件联合。正式边始终使用完整数学ID。

## 共用模型与量词

取同一有限单位客户总体N、同一有限非空共同标签目录、恰六名单位提供者、同一份定义于全部有序历史的纯SPE σ，以及同一actual路径A1…A6。允许空主题、重复、同覆盖异标签、零客户和任意历史平局。同覆盖或同负载不足以合并σ的不同历史。六个合法比较槽T1…T6可重复、可空，不要求最优；只有另用OPT行时才取真正最优六元组。

plain B=A6。在actual前三原前缀h后强制第四位B，原σ给真后继Q/R；第五位再强制Ti给Yi=σ6(h,B,Ti)。A、B的source4、D在这个身份下可以使用同一q/r/ell。源2/3在不同实际原前缀强制B，各有自己的真后继、末菜单及更多隐藏位，不能因相同字母认同。Ti枝旧Bi/Ci和后来的Re/Ze也不同于plain B与Q/R。

所有slack非负性只在全客户求和后成立。早期偏离允许未来沿原σ真实改变，使用剩余人数给安全分母；只有末位没有未来，才是精确查询价。强制者本身不被视为其强制枝新节点的最优行动者。共同K为同一目录最大主题大小（或同一公共上界），每个加权容量支出均须支付。

## A与B：共享actual4隐藏，先合账再max

A使用八slack权(3360,96,660,595,220,522,522,108)，没有K；B source4使用F/G/LQ/LR/CAPQ/CAPR/E权(89632,2576,11205,11557,6311,6899,2832)，K系数13210。B source2/3分别另付88778K、2563K，源2的H收入是该真枝Q2收入，不能换actual u4。A不是B的K=0特例，两组原权也不成比例，不能据共同G公式或共同max机械互推整条对象。

有一项完整解析比较可以保留。令J0_x为A逐客户组合，f4_x为B source4去掉全局13210K后的客户项。对同一个原σ、actual叶、六T和真actual4枝，两者共享同一隐藏z_x=(q_x,r_x,ell_x)。对任一统一全局λ≥0，

\[
\lambda13210K+\sum_x[J0_x(a_x,d_x,z_x)+\lambda f4_x(a_x,d_x,z_x)]\ge0.
\]

定义扩大隐藏域上的

\[
\Phi_\lambda(a,d)=\max_{q,r\in\{0,1\},\ \ell=0,\ldots,6}
 [J0_x(a,d,q,r,\ell)+\lambda f4_x(a,d,q,r,\ell)].
\]

真实赋值在此域中，逐客户上界求和给

\[
\lambda13210K+\sum_x\Phi_\lambda(a_x,d_x)\ge0,
\qquad
\Phi_\lambda(a,d)\le\psi_0(a,d)+\lambda\psi_4(a,d).
\]

所以先保共同隐藏再max所得必要行至少不弱于分别投影再加：它的左端不大于后者左端，且仍必须非负。没有证明严格增强、任何新表值、新点分离或half。固定q/r后两项对ell仿射，联合项仍只需ell=0/6端点。λ必须对全体客户统一；各单客户slack可以负，不能逐客户换λ再援引全客户非负组合。对B不同source，只可共同合入投影，并付(Σ_i λ_iκ_i)K；不认同不同枝的隐藏。该有用比较没有合适既有新目标，留在审读与coverage，不造ALL(A,B)⇒B自指边或新节点。

## A与C：具名Q/R查询与六Y菜单有不同量词

A的H/L对具名Q/R报价，G/E用于其真后两人菜单组合；C查询六个合法Yi并平均，覆盖actual1…6及平均容量。具名安全价不自动包含所有回复菜单的普通价，七行也不含A的源偏离F和完整S/Z/V消交集组合，故没有whole-result互推。相同actual4菜单可以共用ell加入七行，C分母只依actual前缀，不依ell，因此不破坏固定q/r后的端点凸化；CAP需另付其K系数。兼容性已解决，不单为“都仿射”造边。

## A与D：可见拉回不等于共同隐藏完成

D完整字段H=(actual六位a,完整八词hist)，d(H)由hist确定。A的ψ(a,d(H))可直接放在每个hist质量列，K和其余隐藏列为0，客户和完全相同。任一真实σ同时产生这组H与A枝，故这一必要投影可以共同约束同一点，不要求Q/R=旧Re/Ze。

反向从可见投影通过不能推出D某个指定q/r/ell分布满足A八原slack，亦不能为每条行分别选择隐藏完成后当成一份共同完成。若保同一个actual4枝未投影行，应保共同q/r/ell。A原文已含该可见合账，故不造重复边；此结果不证明完整策略。

## B与C：三K表没有免费补齐Yi七价

B的CAP_j和L_j控制真后继具名Q_j，E对六T查询，G是菜单IC组合。C控制其六个新末回复Yi的actual全部价与平均容量；这些不是原三K组合已经证明的行。每个source2/3/4可用自己的真实六Yi实例化C，加最大M根菜单共四指定菜单、28行；各ell保各自身份，不能任意识别。每行仿射，加入各分支条件块与端点表示兼容。四菜单不是全目录所有新回复闭包，三K表通过不等于新七价通过。

审查时序页的后继证据明确：5664与5692有相同K、16hist和W，但214隐藏质量不同；旧5664的source2末价为负、新5692该余量0。因此相同W不能传递七行可行性。5692确通过其列明28行，后来另两条有效pending切面仍可排该固定向量；这些范围可同时为真。本轮仅实读成熟正文，不重跑这些点或把旧负值转移给新点。

## B与D：同source4共享，source2/3保各自条件块

D直接展开actual4的B枝，所以与B source4共享q/r/ell；B source2/3隐藏q分别16/8态，D现有actual4 q/r只有4态，不能由共用a/d/K将它们认成同一分布。投影层三条κ_iK+ψ_i可直接拉回D的H列，完全不要求不同源隐藏相同。

若另加source2/3未投影行，需保各自全H条件块；不含跨块乘积的行族可对已经给定的相容边缘作条件积。但这只是有限矩表示域的事实，不证明旧任意点有各块可行完成、不证明全部跨历史身份，也不把D的十cross/原37行扩成所有分支或完整SPE。当前比较已完成；一般全历史义务不作为没有具体目标的follow-up。

## C到D：交付的七行保持局部贡献

新边为C→D，kind=implies、accepted、relation_mode=unconditional、contribution。没有独立登记桥节点，故不用transfers；端点拆分和条件积的精确桥直接证明如下。这条边只是向D提供七行保持步骤，绝非证明D整条。

对任一**已经给定**的非负类型质量扩展，令H包含actual六位和完整八词hist；固定H,q,r，整数ell∈{0,…,6}的质量为m_(H,q,r,ell)。设

\[
z_{H,q,r,0}=\sum_{\ell=0}^6(1-\ell/6)m_{H,q,r,\ell},\qquad
z_{H,q,r,6}=\sum_{\ell=0}^6(\ell/6)m_{H,q,r,\ell}.
\]

则z非负，逐(H,q,r)保总质量及ell一阶矩。因此保完整H与q/r相关性，且保任何在固定(H,q,r)后对ell仿射的行系数和。

设s_a(a)=a_a/Σa（零分子取0）、P_a(a)=Σ_(j<a)a_j。C六价的客户系数为

\[
s_a(a)-\ell/[6(P_a(a)+7-a)],
\]

平均CAP为全局K加客户系数−ell/6。所有P_a+7−a≥1，且均不含ell，所以七行精确保持。a6为精确末位价，不升级较早安全价。

若所给扩展同时含同一H下旧隐藏联合质量w_H(o)，与新端点质量z_H(v)，v=(q,r,e)，共同H边缘为x_H，取

\[
\pi_H(o,v)=w_H(o)z_H(v)/x_H\quad(x_H>0),
\]

x_H=0时两边非负边缘强制全0，π也全0。求和直接得到旧边缘w和新边缘z均不变。七行仅依actual a及新ell，故同旧隐藏作此全H条件积后仍精确保留；保旧边缘也保只依旧边缘的既有矩。本构造不声称保未提供的Q/R×旧R/Z真交叉矩。

0/6拆分一般产生非整数质量，即使输入来自整数单位客户。它构造的是必要松弛中的非负类型/有限矩表示，**不是新的一份单位客户SPE、真实目录六回复或原σ重构**。对有理输入可清分母得到整数类型，但清分母也不会补上缺失的完整目录/策略身份。

这里量化“任一已给定扩展”，不量化“任一旧可行点存在满足新增价的扩展”。七行合法性由C给出，质量/一阶矩桥由以上公式付清；没有使用未证数学前提。因此conditional distribution只是表示方法，native relation_mode取unconditional。native `edges()` 要求unconditional源为definition/proved，C当前是proved；其余普通定义域条件已经完整写入conditions，而非以D自身为待证前提。

未付界限：C不证明D完整旧hist来源、原十条cross查询合法性或原37 B枝行合法性；不保证任意旧点可扩展、不保未列跨乘积、不实现完整σ、不闭全目录、不证明half。此处保持给定矩的等式证明全部完成，这些剩余义务不能把本局部结果误写成whole_result。

## Canonical查重与交付边界

只枚举当前 `registry.edge_files` 的1718条canonical JSON端点元数据；四core相关恰两条，均全文实读：A到旧1097×599边缘及A到旧1033×211边缘。精确路径、SHA与reviewed_edge_id列在ledger。两条均不重复创建；两peer不在task input pins，故不列入receipt assets、不冒作本包linked，不额外给其body/evidence全文信用。

本包新增仅C→D七行保持一条边；A、B按本包六对实读比较取isolated-after-review，这并不否认A已存的全图关系。没有新read-add需要，也没有发现须修订源文/registry的新错误。task没有声明follow-up对，六个in-packet对全部已处理，不造closed_overlaps或空泛3B/3C任务。

Root负责最终native bind/check、安装、checkpoint、推送和done。本worker仅交付未绑定的边及可复核草稿，Root绑定若改变边文件须同步重算manifest/receipt资产SHA；ledger保留本轮历史实际阅读，不倒填执行。
