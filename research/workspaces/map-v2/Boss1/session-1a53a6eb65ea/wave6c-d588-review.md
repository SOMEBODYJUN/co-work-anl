# POTENTIAL-TAX-3D：d588 当前版本采用审查

审查对象为 `customer-attraction-3a-3a-d58827fb2a79c8e2`。结论：可按当前精确版本采用本任务的 16 个核心覆盖、4 条新逻辑边、1 条既有 canonical 逻辑边及 1 份证明资产。5 条逻辑边中 4 条证明目标整条陈述，另 1 条只证明四谱中的 P/Q_pair 承重步骤，现有 whole/contribution 划分正确。未发现需要修订源正文、对象版本、任务或资产的数学错误。12 项 isolated-after-review 的理由经具体问题复核成立；这只是本包比较范围的处置，不是断言这些对象在总图没有任何关系。

本审查只读仓库，全部输出在仓库外。没有执行 Git、队列、registry、clone 写入，没有运行 LP、BI、旧审计、全客户系数枚举、生成器或随机扫描。采用依据是主正文的证明、资产本身、现行登记版本和冻结成熟证据；本轮结构解析和 SHA 核对不冒充数学程序认证。

## 冻结身份与读取范围

- task state：done；owner：Boss2；task 内嵌 receipt 与当前 receipt 逐字段完全相同。
- receipt 路径：`map/receipts/customer-attraction-3a-3a-d58827fb2a79c8e2.json`。
- receipt 原始字节 SHA-256：`1e06442e8615af468d4dfa17f0bb46e55ae17d6001f0d97b423d94102b94d8a1`。
- receipt canonical pin：`27d5cd95fcb5e4381779cba224d2d29879d8a5b2467abab6aeb90e380e97c39a`。
- 实际分母：16 core、5 read-only 对端、21 input pins；不是 18 个 core。“初始18”是 16 core 加最初两项共享对象的旧读取计数，read-add 后为21项输入。
- 21 个 task input pin 都与当前 `research/registry.json` 对应对象的 canonical pin 相同。6 项资产的原始 SHA 均与 receipt 相同；5 条边全部 endpoint pin/evidence pin 与当前对象/文件匹配。
- receipt 有 51 项 read_refs，对应47个不同文件；本轮核了全部47个文件的原始SHA。主证明、全部16 core 的主正文、5条边和 proof 资产均实读；成熟证明页中引用的大型历史程序/报告没有全面重新展开或重跑。具体 full-text / stored-report / structured-header / SHA-only 范围在 `bindings.json` 标明，避免把字节核对写成全文数学实读。

## 五条逻辑关系

### 1. COPY 全有序索引对 → 完整二阶矩目标

边 `cag-d588-copy-all-ordered-indices-second-moment` 的唯一 source 是当前 v2 的真实末回复 COPY，target 为 `M-bf3dfd10aea3433aaa79c2a75559ce25` v1。应采用 whole-result。

源在同一五人完整策略中固定任意合法 T，根强制 T 后沿同一 σ 得 `(T,B2,B3,B4,B5)`；真正倒二改 B5 后，保留同 σ 的真实末回复 C。源证明九个非负总合同分别是根 IC、四个共同最大 K 的 cap、真正倒二复制 IC、原末位对 Q/C 的比较、复制历史末位对 Q 的比较。被强制的倒二不是新枝优化者，也没有偷偷使用其 PAIR。正文给出的恒等式与128型/48最坏型非负表证明

\[
F_T(Q)=|Q\setminus T|+|Q\cap T|/5\le 44u/3+13K/5-16|T|/3.
\]

给一个固定最优五索引元组 `(T1,…,T5)`，对全部25个有序 `(i,j)` 求和。含对角、同标签重复和同覆盖异标签；它们是索引槽，不能去重成不同集合。一个客户被 d 个槽覆盖时，query 槽有 d 种；根槽有 d 种使其份额1/5，另5−d种使其份额1。因此左端是 `d[d/5+(5−d)]=5d−4d²/5`。右端是 `25(44u/3+13K/5)−80D/3`。移项乘15精确给

\[
5500u+975K-475D+12S_2\ge0.
\]

此时 D/S2 来自同一最优元组，u/K 来自同一实际策略和同一共同目录。源逐对允许任意合法 T,Q，所以其它合法菜单也不改 actual u/K；但不能把一个菜单的 D/S2 搬到另一菜单。whole-result 与 target 的全部陈述相合，没有将互斥枝尾利润当作 actual W，没有由单个最大源投影假装恢复二阶矩。

### 2. Möbius 唯一反演 → 匿名计数势的完整相容式

边 `cag-d588-mobius-fixes-anonymous-count-compatibility`：`CA-MOBIUS-BOOLEAN` v1 → `customer-attraction/anonymous-count-potential-compatibility` v1。应采用 whole-result。

源对完整归零有理 Boolean 表，利用调和核的 A 单项式系数 `(-1)^(|A|+1)/|A|`，两次 Möbius 变换唯一求出全部非空兴趣类型 x_B。这不仅拟合 Boolean 层，也固定同一 x 的所有重复计数调和扩张，故不能随后自由填匿名终局势。

三条 target 关系均在同一调和表示中完整得到：轴 `Φ(te_a)=H_tΣ_(B∋a)x_B`；两标签三人前后差分别为 `11(x_a−x_b)/6` 与 `(x_a−x_b)/2`，故三倍前差等于十一倍后差。额外主题交换对称令 `x_a=x_b=h`，四人 A/B/C 的 h 系数为25/12、17/6、3，共享型系数同为25/12；于是 `B−A=3h/4`、`C−A=11h/12`，得十一倍前差等于九倍后差。

这里提供者匿名不推出主题交换对称。完整 Boolean 反演与只保到 d=min(m,p) 阶的截断交集矩也不同；后者可有高阶不可见核，未反驳前者的全表唯一性。边没有声称穷尽全部固定人数线性约束。

### 3. Möbius 唯一反演 → 非负/整数实现的整条判据

边 `cag-d588-mobius-nonnegative-and-unit-realizability`：同一 source → `M-4d61acfe4fb1427dabcf76b30a824dcc` v1。应采用 whole-result。

任何客户表示 y 若实现同一完整 F，唯一性强制 y=x。所以非负有理精确实现当且仅当 x_B≥0；未经缩放的不同单位客户实现当且仅当 x_B 为非负整数。充分性分别直接用质量 x 或复制 x_B 名不同客户。清共同分母 D 给 DF 的单位客户实现，不能把缩放后的游戏写成原值实现。

二标签三个非空势值全为1时，`c_a=c_b=1,c_ab=−1`，`z_a=z_b=1,z_ab=2`，反演精确为 `x_a=x_b=−1,x_ab=2`。该 F 单调次模，但所有正缩放仍含负型，反例结论正确。标签同覆盖在当前模型合法；额外要求覆盖两两不同时，还须每对标签有正质量兴趣型将其区分，不能从非负性推出。边完整保留了这些范围。

### 4. 固定背景两人税 → 四谱中的 P/Q_pair 步骤

边 `cag-d588-two-player-tax-supplies-spectral-pair-rows`：`CA-TWO-REMAINING-TAX` v1 → `customer-attraction/five-player-maximum-root-overlap-spectra` v1。只采用 contribution；不得改作 whole。

T2 的三个真实比较保留首人改 T 后同 σ 的末回复 Q，再在实际末节点比较 Q；精确差另有 `g(A,A)−g(A,Q)≥0` 与 `g(T,S)≥0`。因此在五人真最大根枝的同一末两人历史 `(M,B2,B3)`，合法背景 p、实际 `(B4,B5)` 给所有比较对统一上界

\[
H=v_4+v_5+\sum_{x\in B_4}[(p_x+1)(p_x+2)]^{-1}.
\]

对十个 `i<j` 索引对相加：d 个覆盖槽导致 d(5−d) 个单覆盖对，binom(d,2) 个双覆盖对，后者 pooled 份额2/(p+2)。所以

\[
Q_{pair}=10H-\sum_x\{d(5-d)/(p+1)+d(d-1)/(p+2)\}\ge0.
\]

每个最优并集客户任选一覆盖槽，含它的四对每对至少贡献1/(p+1)，因为双覆盖时 `2/(p+2)≥1/(p+1)` 对所有非负 p 成立。故 `(5/2)H≥Σ_(d>0)1/(p+1)`；添加并集外非负 `p/(p+1)` 给

\[
P=(5/2)H+\sum_{all}p/(p+1)-O\ge0.
\]

十对共享这一历史和H，不是跨树借十份实际福利。整条四谱还需要根R、共同最大K的CAP、真第三位J、真末位L、各份指定乘子和192型余项。old 证书 P/Q 乘子都是0。当前 contribution.remaining 将这些未由T2提供的步骤明确留下，因而是准确 accepted 局部结果。

### 5. 复用022eb：最大根合法行 → 同线的不同完整余项

`cag-022-maximum-root-supports-distinct-spectral-residuals` 原路径、原 SHA 复用；source 为四谱对象，target `M-5d32f2d5969b4b88a3832d007993a57e` v1。应采用 whole-result，不能因为标量线相同而删除。

同一 `B=89090/1753,C=29147/3506` 下，把 P 表示的 CAP2 乘子8089/3506换成1/2，P 从1188/1753换成0，Q_pair加297/1753，其它行不变；所有支持行仍属于同一真最大根分支且乘子非负。两份成熟证书的192型条件最小值分别是

\[
e_P=113(d-1)_+/1753,\quad
e_Q=(d-1)_+/5+297(d-1)_+(4-d)/35060.
\]

完整 e_Q 非负；其中第二项在d5为负，不能单独标作非负增税。准确差为 `297(d−1)_+(20−d)/35060`，d≥2严格正。用 `Σ(d−1)_+=D−O`、`Σ(d−1)_+(4−d)=5D−S2−4O`，清分母得到

\[
26860O+8497D-297S_2+291470K\le1781800u.
\]

这与旧 pair-envelope 的 e_Q 一样但 K/u 系数不同，不能拼成同一证书。ρ 是发现参数，已从有理恒等式消去，不是对实际 u/K 的新增假设。原 audit 按(B,C)去重只审首个表示的历史范围，不能替代后来成熟“全部存储记录”的证据；本轮复用后者和自足证明，没有再跑2112型或浮点发现。

## 十二项 isolated-after-review 的数学判断

1. `M-58ef82731528424394935220507e6fc1`：条件half的付款确实成立，但需要最优实际遗漏客户的一个共同分割，每人至多一次真实偏离，且后继不覆盖其组。补位族中早查询 B/D 后 T 会覆盖新增遗漏客户，恰缺这一前提；不交F必要界也不构造这样的分割。不能把多个逐主题IC重复花成总W。

2. `M-bb7fa19357034cdb89eb096c2a6c5a53`：假设扩目录后仍存在保同一实际路径的完整SPE，末位IC给v≤u_m。倒二首次F后末位选旧S_m至少u_m，而复制F只v/2，v>0时严格排复制，故倒二独得v。这个必要结论只付末两人。更早偏离会改变多个后继；没有普遍保SPE扩张，也没有一般所有人付款。与上一项不存在所需完整蕴含。

3. `customer-attraction/r3d253-fixed-background-static-security-remainder-review` v3：逐客户 `φ_b(d)+ρ_b(d,L)=(d+L)/(b+1+L)` 正确，d0单独定义、s0不用除s，任意r/s和有限minimax给 `F_r+R≤(r+s)v_(s+1)`。d*是比较终局、Q*是静态对偶；换真实负载会丢F_r最优性，换actual收益没有等式。若另有最优query精确流，确可联合得条件 `(2−1/n)W`，但方法对象不保证普遍流存在，当前core无该所得端点，不能凭相同安全值造整条边。

4. `M-1302624aad874058a6d7dc2cd254018d`：绑定的5930…actual13_v1是6751源必要行版本、63正有理atom、W1且比较O约2.0006335。header 的最小源slack0是旧恢复声明，没有保存生成器SHA/全6751行；当前基础恢复类6565也不能冒该版本。它不是29e0…的另一63点。非负atom、三直方图和menus边缘不是完整Boolean势表，也没有共同目录/全历史σ逆实现；O不自动OPT。故不能用本包非负Möbius判据或五人谱给它真实反例身份。

5. `customer-attraction/symmetric-quadratic-fresh-all-outcome-BI-fixed-policy-floor-probe`：对象是禁止重复的signed对称二次边际势，θ是纯m−1背景后选最佳fresh报价。集合值BI的完整有序子树拼接逻辑正确，固定旧报价LP的z只是θ下界；三份failure=null和浮点微差不证一般floor。任意长牺牲构造用高阶势，未证明在此二次类；完整编译的均匀大偏置改变相对安全值缺口。没有直接进入原单位客户CAG的逻辑桥。

6. `customer-attraction/full-root-matrix-cross-coefficients-and-self-coupling` v3：保根完整列有r竞争槽，另插query；`D−pᵀKp=pᵀHp`、对角插入自税及PAIR→SELF→WP→M_full≤u→u≥v_(r+1)的单向链成立。有限p列表不证全p，但某固定σ所有H项非负可解析证全p；反向不能倒推。独立全树流用n−1背景，既不是同一K列也没给可行流。当前正文另已保留普遍桥反例，本包没有新保证，也不因旧有限无失败报告改变其状态。

7. `customer-attraction/tail-ABB-five-multiplier-rational-candidate-failed-class`：五乘子在l≥2非负不够；唯一坏类 `(1,1,1,0,1)` 的分子移l3+u后全严格负、分母移l2+u全正，故每实l≥3负，l3为−47/7930而l2为81/10367正。只否特定三接触等式产生的五乘子模板。一个坏客户系数列未必能单独满足真实IC，不能变成half反例、全部七行模板失败或actual13/K矩阵的否证。

8. `M-47c853fbc6c84223b683f6fcb277610b` v2：真实全有序IC先生成再合相同收益端点，不合策略历史；固定π与不观察query的Q须乘积独立，`d=divλ+nΣQ s_b(π)` 精确守恒且λ/Q非负才付该π保底，π最优才付nv_n。共同删除势只放宽守恒到势投影，不给全层E、共同signed客户或非负客户。五动作无势循环没有势，弱强有限势又有同支持效率冲突；两者都不能反原CAG。该对象是充分证书接口而非普遍可行定理，implements语境不充linked。

9. `customer-attraction/Brethouwer-four-player-lower-bound-model-scope-and-closure-obligation` v2：文献四人2.0558498235对应玩家特定S_i，当前页未给完整关联/重数/σ。本轮只审仓内成熟模型边界页，没有重新检索外文PDF。目录取并新增跨角色动作与离轨义务，向下闭包也可能改SPE；四到六人、单位客户整数化各是独立义务。定义CAG只给对照域，不证明迁移；没有可用的原共同目录反例边。

10. `customer-attraction/padded-on-path-same-topic-kernel-budget-boundary`：全m构造的旧偏离路径靠立即最大值且后继不降收益完成全树粘合；唯一最优全Z+B+D。受限节点必须原规定选分配槽主题时，B/D至多一个末节点，另一个遗漏客户query负载2强制Pjj≥1，从单元素核得一权重≥2、其它≥1，预算精确22(m+1)。解除节点限制同族全部复用末A节点可P0/λ1，预算W22m、查询和44+11(m−2)。这是路由接口失败，不能反一般独立流；全m由解析证明而非m2…5有限JSON外推。

11. `CA-WORST-PNE-WELFARE-NO` v2：六客户类型展开16单位客户；完整21节点σ actual033、收益17/3,14/3,14/3，W15。20个静态计数中只有0111/0102两种PNE且全W16，OPT16。它完整否定“每份顺序SPE≥同实例最差静态PNE”，比终局非PNE更强；却没有否静态minimax、CCE、恰六人或half。实际调和势133/6、PNE45/2的差1/3仅是本固定例的另一静态比较，不补跨树付款。

12. `customer-attraction/closeout-3e0d9dd985280d79001d6049`：13与72客户同动作表但不同重数/IC多项式，不能互授运行。每条调和IC是Δ(t)的积分非负，不推出同一t同时逐点非负；正文三真实末位比较已解析排公共t。两点均W=OPT，不反half、客户实现或独立背景运输。graphθ只在singleton/pair域、固定旧最佳报价作下包络，无配套结果与精确验收，不能凭候选代码制造新反例边。

## Planned overlaps 与后续处置

四个 planned pair 都有准确处置。两个 in-packet Möbius pair 分别由上述两条 whole 边闭合。两个原 follow-up pair 通过 read-add 后在本任务已闭合：COPY→second moment 是整条；T2→spectra 只到P/Q_pair步骤，其余完整四谱由目标正文原证明承担。`closed_overlaps` 的两个理由与此相符，`follow_up_tasks: []` 可保留；没有遗漏一个仍需发布的本包比较。

保留的数学研究义务包括：一般遗漏分割/后继排除；独立最优query流的普遍存在；actual13共同目录逆实现；更广二次fresh保底；ABB替换接触集；异目录到共同目录及四到六人的全历史迁移。这些不能冒本包待交任务，当前没有需要新增版本或新比较端点的已确认错误。本审查建议采用当前五边及16core覆盖，继续保留其它并发未审对象/边，采用范围不外推。

`bindings.json` 提供当前 task/receipt pin、21 input pins、每资产SHA、5边完整endpoint pins/evidence pins、16core结论及4 planned pair处置，可直接供Boss1构造通用采用记录。采用前若任一绑定改变，仅复核受影响部分；本报告不授权将新版本悄然置换进已审集合。
