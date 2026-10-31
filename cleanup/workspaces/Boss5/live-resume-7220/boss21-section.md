## Boss21：真实近二反面与实际调度解码

### 来源身份与历史状态

本节来自冻结工作区 `research/workspaces/unrelated-machines/R-0bbb78b7ca994fa99daee018cb914ebe/` 的完整README（源722087a0e8ad7b2a0316，7行997字节）及配套workspace.json（源c1661b95bed75f84f298，6行149字节）。冻结commit为 `68fad804ec5946cb296f77dc5b336308a66abf12`；README SHA256为 `ac2f5d9c3332734842d6a5292763353c43e0316af11e429e3653f3c01aaa0a2f`，JSON为 `8248c8f803a731c21891741665a610347dbcb649163181cd9ac008306eb330bc`。原字节、完整阅读与比较记录见本批证据目录。

README称该clone固定actor为 `R-0bbb78b7ca994fa99daee018cb914ebe`，当时入口为main / unrelated-machines。配套JSON的schema为1、save为`unrelated-machines`、actor相同、instance为 `5b647a702cb14136b2c1642d5a15e30c`。这些字段保留历史路由及来源身份，不是当前进程、owner、分支绑定或数学见证。

其历史目标是攻击真实近二反面及实际调度解码，原 `UM-TARGET-v1` 和一般反面都明确保持OPEN。README记六个内部gpt-6.1-sol、max努力级别攻击源gap、物理一致性、放大和复杂度；这是当时协作记录，不证明六份独立审查已发生，也不提供人数认可式认证。原目标中的实际算法量词是：存在统一ε>0及一个确定性总位多项式算法，使所有合法普通UM输入都输出完整原任务的合法调度，且峰值至多(2−ε)OPT。限定域结构算法、有限实验和某一种decoder失败均不能替换该目标或其精确否定。

### 已有长期增量的准确数学导航

README实际指向资源畸变完整flat菜单的[规范定理](../定理/逐资源正权畸变与κ边界--定理.md)和[实际审查](../审查/逐资源正权畸变与固定κ边界审查--审查.md)。本节已完整比较原主稿、合订审查及现行对象；它们承担数学结论，README本身没有独立证明或新增认证。

承重输入域如下：非空有限groups，每组非空显式indexed states；每state x有独立private机M_x，每资源u有独立资源机R_u，两类机器彼此互异。每组一件selector只能在本组private机耗时1；每incidence(x,u)是一件独立原job，只能在M_x耗时非负二进制有理p_xu或在R_u耗时1。同state资源不重列，W_x=Σ_up_xu≤1；没有额外任务、预载、资格或一致性约束，全部未选states和零权原jobs都存在且须执行。允许空incidence state、重复indexed states和unused/all-zero资源。

令b_x=1−W_x，同资源全部正private权构成P_u，并定义

\[
\kappa=\max\bigl(\{1\}\cup\{\max P_u/\min P_u:P_u\ne\varnothing\}\bigr).
\]

零项不进入比值，不造0/0。κ可以随输入增长，算法不按它的数值循环。给跨组两两不交资源B_g，定义baseline值

\[
V=\max_{B_g\ {\rm disjoint}}\min_g\max_{x\in S_g}
\left(b_x+\sum_{u\in B_g\cap S_x}p_{xu}\right).
\]

完整实际OPT=2−V：正向选达到组效用的state放selector、只导出领取incidences、其它全部原jobs留private；反向对任意峰C<2的完整调度，读取selector的真实state和导出资源，unit资源独占给跨组不交并推出V≥2−C；C=2端点另由正向矛盾闭合。W<1时不可省baseline；全W0就是V1、OPT1。

restricted Santa桥对每state建player，每原正资源仅建一件固有值q_u=minP_u的real item，每b_x>0建own baseline，每组建|S_g|−1件组内unit dummy。其最优最小值V_-满足V/κ≤V_-≤V：左侧给选中state其资源与baseline、其余states各取dummy；右侧每组选dummy-free player读出真实不交资源。每原资源不能按incidence克隆。

对每固定实α>4，先取固定有理4<a<α，接受Cheng–Mao restricted Santa完整a近似实际allocation合同，得到最小效用t≥V/(ακ)。按组取dummy-free player，仅外送其收到且正资格的real items对应原jobs，其余全部原jobs回private。即使未收到own baseline也有t≤b_x+Σq≤b_x+Σ导出p，故选中private≤2−t；未选private和资源≤1，t≤1，全部机器共同受界。于是

\[
C_{\max}\le2-\frac{2-\mathrm{OPT}}{\alpha\kappa}
\le\left(2-\frac1{\alpha\kappa}\right)\mathrm{OPT}.
\]

算法不接收OPT、最优调度、配置证书或κ上界；α固定后的次数可依赖α。辅助表规模按显式states/incidences/资源与有理位长多项式；不把大分母或κ数值一元展开。完整推导、bonus与baseline双表示和全部原任务回填见[证明对象](../证明/资源畸变的双表示与全任务回填--证明.md)，本节不另立同义定理。

### 固定κ源筛选、纠错及证据层

固定κ₀≥1，若一个确定性多项式归约的**全部输出**均在上述完整flat域且κ≤κ₀，YES实际OPT≤1，NO实际OPT≥2−ε，并有严格ε<1/(ακ₀)，可取固定有理

\[
2-1/(\alpha\kappa_0)<\theta<2-\varepsilon.
\]

算法在YES输出峰<θ，而NO任何调度峰>θ。因此在P≠NP下，该像类不能承载如此严格分隔的NP-hard promise。等号不给该separator；随机归约须保留相应概率/复杂度合同。这解释README所说“固定κ完整flat源不能承载任意趋二真实gap”。它是既有工具的结构推论，不是一般UM hard或easy的结论。κ随目标误差发散只是逃离这个必要条件，绝不自动产生NO gap。W<1已被baseline覆盖，增加states、资源重数或仅重新分配state总质量不会自动逃离域。

原审查保存的纠错和阅读身份随导航保留：α>4来自另一篇Cheng–Mao定理1；DRZ旧4+η分析已更正，正确6+η只能独立支持较弱α>6。首次statement-only不追记为全文读后；作者读后、首次完整读后、实现措辞增量和最终θ局部复读分别保留版本身份。直接baseline与原作者真实bonus增广改变的是不同矩阵，须凭保OPT证明比较，不能说只是改记号。θ修补解决任意固定非有理实常数不能默认精确比较的问题。详细顺序及原哈希见[真实先验与阈值修补](../审查/资源畸变审查的真实先验与阈值修补--审查.md)。这些是冻结审查的历史事件，本次不冒称新blind审查或重新核读外部PDF。

两路有限测试是[双路有限穷举资源](../资源/资源畸变的双路有限穷举与历史运行--资源.md)所记录的不同对象：主程序945份输入核bonus表示、值比较和普通矩阵；独立baseline程序1301份输入枚举1328275份完整原调度及20798份正资格辅助allocation，α=41/10与7分别10770份合格allocation逐原job解码通过。输入数、调度数和allocation数不能混用。有限检查不证明全体有理输入、不构成近二hardness、不实现CM/DRZ完整后端；本次新增数学程序运行0，不移接旧exit0为新运行。

### 未完成的typed-dummy接续与真实全调度义务

README只说typed-dummy源筛选“进行中”“拟接”既有mixed-small正文，没有给具体typed-dummy矩阵、完整归约或已完成结果。已读相关[多小端密度流审查](../审查/多小端密度流障碍与单位读出校准槽双源审查--审查.md)与[双流实际算法](../算法/多小端原生任务的双流实际调度--算法.md)，不能将其倒填为未定位typed-dummy稿已获证明。

可复用筛选合同是：{1,1/k}真实资格中，每机small incidence数t_i≤k，至少γt_i来自具有两个以上small原端点的任务。Q为没有small端的unit-only任务；Q若无容量1完整匹配，则任何C<2完整调度不可能，故OPT≥2。若有匹配，给其余每job在d_j个small端均匀分数1/d_j，每机ρ_i≤t_i−b_i/2≤(1−γ/2)k；容量ceilρ_i整数流完整安排small任务，叠加Q得到实际峰

\[
1+\max_i\lceil\rho_i\rceil/k\le2-\lfloor\gamma k/2\rfloor/k.
\]

γ条件是逐机而非全局平均；Q空时去掉前导1，不能无条件当相对OPT比率。要逃离固定柔性密度筛选，需要γ趋零、多尺度或真实联合unit/medium容量等另证机制；这些只是必要方向，不是hardness的充分构造。

“coherence切片不是真实输入约束”同样承重。[笛卡尔分块一致性审查](../审查/笛卡尔分块一致性与二度菜单联合取整双源审查--审查.md)的额外选择域mathcal L只给受限C_mathcal L=2−V_mathcal L；若block/coordinatewise条件在外部语义中，普通UM矩阵仍可选择域外selector。二元菜单原普通矩阵可全局cyclic逃逸，真实OPT=1+2^(−t)，故一致性域低值不直接给原矩阵NO。未来必须把一致性编译成真实jobs、资格和共同容量，并同时保YES。

README最后保留的缺口是**真实近二NO，以及从任意低载、全部原jobs的实际分配到源见证的可靠decoder**。要在明确复杂度假设下排全部统一ε改善，通常须对每个固定足够小δ给位多项式源归约，带已知可计算正有理标尺T：YES完整OPT≤T、NO完整OPT≥(2−δ)T。soundness要处理任意完整合法σ，只要Cmax(σ)<(2−δ)T就多项式解出与源NO冲突的见证；不能只读取选中states、抽象token、指定规范调度或给定但未知的strict witness。相关历史合同见[真实源NO路线卡](../资源/真实源NO全调度解码路线卡的历史合同--资源.md)。局部CONFIG gap、语义切片、有限逃逸排除或κ增长均没有履行这项义务。

本入口因此作为历史资料和研究接续保存；它不改变一般UM目标、反面、外审、全球新颖性或六人共同目录SPE问题的状态。原“桌面不复制一份数学资产”的意思是沿规范正文和证据导航；本节保其语义和边界，数学资产继续由各正式对象承担。
