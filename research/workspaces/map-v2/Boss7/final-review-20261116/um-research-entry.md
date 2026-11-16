# 一般 UM 原目标的研究入口：两条成果线与一条独立障碍线

Boss7，2026-11-16。原目标 `UM-TARGET-v1` 仍为 **open**。当前图有可直接复用的精确成果：裸 Cartesian 的反向放大经正规形迁移，以及显式 fractional NSW 的 norm1 菜单后果；另有保原机器身份的全局 coupling 判据和局部不延拓障碍。以下分别给真实结论、完整前提和下一步缺口，不把保值桥、局部计数或存在性等价合成为一般 UM 算法。

## 1. 实际快照和原问题

初次核快照为 **2026-11-16 17:02 UTC**，交稿前于 **17:06 UTC** 复核；仅据本 clone 的实际字节，未查询远端、执行 Git/sync/队列/公屏或改动 canonical、边及收据。并行集成使三个总文件有变化，但本入口采用的全部对象版本、四条边字节、有效清单成员及端点 pin 均再次确认未变。实际两次快照如下：

| 文件 | 17:02 SHA256 | 17:06 SHA256 |
| --- | --- | --- |
| `research/registry.json` | `202c608164e5e7f706c6178d16a0f13089c01abf7b7fdc3cc5b091370fb1f4a8` | `ee1148cd8c8053496e64e259902fb4890ea9a5add5a9c5a090b0d14739fc64ac` |
| `map/coverage.json` | `13e4679a603f05bd4ce9767b73afadd9b6c1d5018afaa6e0f581994d0e286f18` | `51d9a531636b1e8c0fe358546cf39bfb065828e05acff6698d4c393541872ab7` |
| `map/integration.json` | `135bdadeca23e9346a77097d2818dd9c005e68f7d906af6b4eae587977b141fb` | `6764c7300f0d954df5fbbea0537f77e2a52b04981a40a58e023ea56238efe62b` |

Boss5 本轮最终补记：17:06 快照中 `boss5-cartesian-receipt-repair-01720ef708fa6bdb` 尚为 claimed；后续已 done 并 integrated，旧 b77 已被有效后继替代。修复只处理收据元数据，五项原 SHA 资产及数学保留。下述 E1 使用现役 **0bde** 路径和 Cartesian **v3**；旧 reading SHA 与 f663/v2 仅是历史记录。当前验收见 [本轮完成记录](../../Boss5/finalization-20261116/phase3-completion.md)。

起点实读 `archives/unrelated-machines/问题--问题.md` 全文（`UM-TARGET-v1` v4）及 `state/定义/不相关机器与两个调度松弛--定义.md` 全文（`UM-MODEL-v1` v1）。问题是：存在统一常数 \(\varepsilon>0\) 和一个确定性总位多项式算法，对**每个**有限显式非负二进制有理/∞矩阵（每个原 job 至少有一个有限端），输出每个原 job 恰一次、只用有限端的实际调度，满足 \(C_{\max}\le(2-\varepsilon)OPT\)。机器数与全部编码位数均为输入；空任务、每任务有零端的零最优分支须保留。

原题到下面各线首先是**问题/定义导航**，不是逻辑蕴含。当前真正接回原题的一条可用条件边是：

**E0** `um-280160f5-reliable-threshold-interface-solves-uniform-target`，路径 `map/edges/unrelated-machines-3a-3a-280160f5f3f5d37d/reliable-threshold-interface-solves-uniform-target.json`。

- source `M-5af596d5d75441cba006ff7ba31a19a4` v2 → target `UM-TARGET-v1` v4；accepted，ALL，**conditional，whole_result**。
- 未付前提是存在固定 \(k\ge2\) 的统一接口：任意原 \(P,T\) 都在总位多项式时间返回全调度 \(C_{\max}\le(2-1/k)T\)，或可靠且可独立验证的 \(FAIL\Rightarrow OPT>T\)。拒绝一份充分证书不够。
- 条件到结论的证明已付：零分支后，取有限端分母乘积 \(Q\)、\(U=\sum_j\min_i p_{ij}\)，在 \(1/Q\) 网格二分并保存真实成功调度，调用次数 \(O(\log(QU+1))\)。接受集合不必单调；这不提供未知接口本身。

## 2. 成果线一：裸 Cartesian 精确值 → 三态/资源度三后的精确值

| 别名 | 当前 object_id / version / 状态 |
| --- | --- |
| A | `UM-NORMALIZED-FLAT-CARTESIAN-TENSOR-REVERSE-AMPLIFICATION-v1` / v3 / proved |
| N | `UM-NORMALIZED-FLAT-MENU-THREE-STATE-DEGREE-THREE-NORMAL-FORM-v1` / v4 / proved |
| R | `unrelated-machines/bare-cartesian-read-after-normal-form-palette-scope` / v1 / unassessed review |

**E1** `um-cartesian-reverse-values-transfer-through-three-state-normal-form`，路径 `map/edges/boss7-tensor-notation-repair-0bde5bd3570dc738/um-cartesian-reverse-values-transfer-through-three-state-normal-form.json`。

精确逻辑为 **ALL(A,N) → R 的 §§2–5 contribution**；accepted/unconditional。A 给源族两值，N 给真实双向桥，缺一不可。它没有 whole_result，也不把 R 的全部历史、palette 或来源陈述升级为 proved。

对整数 \(t\ge1,D=2^t\)，组和 indexed states 分别由 \(g,\ell\in\mathbb F_2^t\) 标记，真实资源 \(u=(a,b)\)，
\[
S_{g,\ell}=\{(a,b):b_i+g_i a_i=\ell_i\ \forall i\},\qquad p_{g\ell u}=1/D.
\]
每 state 恰 D 项、总量1。每组一件 unit selector；**每个** \((g,\ell,u)\) 都是一件不同 incidence，private 时间1/D、资源端时间1；全矩阵有 \(D^3+D\) 件任务，包含全部未选 states。

补组 \(g+\mathbf1\) 的任意两态恰交一资源，故至少一组最多领取 D−1 项。循环标签 \(\ell_i(g)=g_{i+1}\)、领取 \(a\ne\mathbf1\) 的资源达到 D−1：碰撞将给 \(\delta_{i+1}=a_i\delta_i\)，一个零位沿环迫使 \(\delta=0\)。因此
\[
V(P_t)=1-1/D,\qquad OPT(P_t)=1+1/D.
\]
实际上界只外送已选 state 的 D−1 件，所有其他任务留各自 private。任意实际 \(C<2\) 调度中，由 selector 真实去向读出的补组共同资源对应两件不同 jobs，不能都外送，至少一件与 selector 同机给 \(1+1/D\)；\(C\ge2\) 单列。这是完整普通矩阵的最优值，不是只对 partial bundles 的界。

N 的输入严格是**每原 state 总量1的显式完整 flat UM**。先 T：K 个 states 作二叉树叶、每顶点一 selector、own singleton 资源；K>1 时旧 selector 资格改到 root，K=1 原位。逆向只沿 root 强迫链提取一个原叶，允许 off-path 额外活动，全部原 incidences 保留。再 D：在全部旧/own 资源的组 membership 上建 d ports、d−1 个二态 helpers；每 helper 有一 selector 和两件不同 incidences。\(C<2\) 强迫 helpers 占 d−1 个不同 ports，至多一件旧外送；正 partial 亦双向。全 private ≤2基线与有限达到补齐 \(OPT=2,V=0\) 端点。

E1 因而实际交付
\[
P_t^*=D(T(P_t)),\quad K_{\max}(P_t^*)\le3,\quad
\Delta_{\rm resource}(P_t^*)\le3,\quad
V(P_t^*)=1-2^{-t},\quad OPT(P_t^*)=1+2^{-t}.
\]
资源度按**全部菜单的组数**计，不是组交互度 M；构造按显式总位长多项式，非 poly(t)。输出含 singleton，已脱离裸 Cartesian 族。精确保值压态/降度只保留已经改善的 NO 值，不能恢复源 gap。

**接续缺口：** 若要走困难性/放大，须另给 normalized 显式源的真实 YES 与“全部选态、任意 partial”NO，或在完整 ordinary 矩阵中从任意低峰实际调度解出所需跨坐标一致性并保 YES/位长。裸积、任意一般 UM 入 flat、未归一化源入 norm1 都未由本边支付。不能把状态支持为 product 偷换为标签 \(\ell_i\) 只依赖 \(g_i\)。

### 已付的同菜单修复障碍（E1b）

`UM-COORDINATE-OBLIVIOUS-CARTESIAN-MENU-QUOTA-v1` 给每个固定共同函数族 \(f_i:\mathbb F_2\to\mathbb F_2\)、\(\ell_i(g)=f_i(g_i)\) 的精确受限值

\[
V_{obl}(t)=\frac{\lfloor(3/2)^t\rfloor}{2^t}.
\]

它允许任意 partial，且重选全部 f 仍不增这个最优值。与 A 的 free 值 \(1-2^{-t}\) 联合，现役边 `um-cartesian-free-and-coordinate-quota-imply-no-constant-repair`（文件 `map/edges/boss7-tensor-notation-repair-0bde5bd3570dc738/um-cartesian-free-and-coordinate-quota-imply-no-constant-repair.json`）以 **ALL {A, quota} / accepted / unconditional / whole_result** 完整推出 `UM-CARTESIAN-COORDINATE-CONSTANT-REPAIR-OBSTRUCTION-v1`。

对任意固定高值门槛 \(\theta<1\) 和比例 \(c>0\)，足够大 t 的同菜单高值分配 \(A_t\) 满足 \(v(A_t)\ge\theta\)，但所有逐坐标分配 B 都有 \(v(B)<c\,v(A_t)\)，因为 \(\lfloor(3/2)^t\rfloor/(2^t-1)\to0\)。连这样的统一保值修复**存在性**都失败，不依赖计算效率。这不排除改变菜单、资源或任务的新一致性编译，也不针对随 t 衰减的保值比例或本族中空的 \(\theta=1\) 输入域；这些范围须分别陈述。后续不再把同菜单正常数保值的逐坐标事后 repair 列作开放工具。

## 3. 成果线二：显式 XOS fractional NSW → unit-FSLP/REPAIR/全部 jobs

| 别名 | 当前 object_id / version / 状态 |
| --- | --- |
| B | `UM-EXPLICIT-XOS-DETERMINISTIC-FRACTIONAL-NSW-v1` / v6 / proved |
| C | `UM-NORMALIZED-MENU-ALMOST-ALL-AND-REPAIR-LP-BARRIER-v1` / v6 / proved |

**E2** `um-explicit-fractional-nsw-gives-normalized-quality-repair-and-full-schedule`，路径 `map/edges/boss3-sourcefix-repair-8d806bdc7cc35ff1/nsw-to-normalized-quality-repair.json`。**ALL(B) → C，accepted/unconditional/whole_result**；C 中各输入条件和 promise 都保留，unconditional 不是取消这些条件。

B 对有限非空 indexed additive clause lists、非负二进制有理系数的**显式、无权 XOS**给同一确定性总位多项式实际不交输出 \(S=Alg(I)\)，不输入 y；对每个有限有理正分数配置 benchmark y 同时有
\[
NSW_v(S)\ge\mathcal B_v(y)/1125000.
\]
y 每行质量1、每原物品总边际≤1、每正质量条目实际价值严格正。算法先固定 \(H,V,T\) 和最终匹配，证明才量化任意 \(H\)-比较双射 \(\pi\) 和任意 y。固定残余 lift 对**每个**分数残余族给 \(\sum z v/V\le2|A|\)；局部 Q 网格只改辅助权；任意比较 rematching 用全 U 的真最优 singleton 匹配作逐路径反事实，最终同一最优匹配支配所有 \(\pi\)。不存在需另付的“同一输出对全部比较匹配/y”欠账。无正 singleton 匹配时 Hall 同时排除正实际 NSW 和正 benchmark，按零分支返回；未在零上取 log。

C 另要求同一 n≥1 个组、m≥1 原资源、每个原 state 总量1。令 \(P_{gs}=\{u:p_{gsu}>0\}\)，unit-FSLP 是
\[
\lambda_{gs}\ge0,\quad\sum_s\lambda_{gs}=1,\quad
\sum_{g,s:u\in P_{gs}}\lambda_{gs}\le1.
\]
列是**正 support indicator**，既非 p 权也不数零 incidences。可行 λ 给 benchmark1，B 给同一实际输出 \(NSW\ge1/3000000>2^{-24}\)。固定有理 \(0<\eta<1\)，令 \(K=\lceil1/\eta\rceil,q_\eta=2^{-24K},c_\eta=q_\eta/2\)，则
\[
\#\{g:r_g<q_\eta\}<\eta n,\qquad
\#\{g:r_g\le c_\eta\}<\eta n.
\]
证明是 NSW 乘积与 \(r_g\le1\) 的严格计数，不要求 ηn 整除；可变 η 的收费关于 K，非 \(\log(1/\eta)\)。这里的 norm1 是原输入前提；B 的内部残余归一化不提供任意外部源到该模型的变换。

REPAIR 向**相同 n 组**添加同一 D 个全局共享 unit singleton 资源及 alternatives，不加 agents。固定 \(0\le a_{rep}<\gamma_{lo}\le1\)、\(D\le a_{rep}n\)、\(0<\eta<\gamma_{lo}-a_{rep}\)、\(0\le\delta_q\le c_\eta\)。准确 promise 是：YES 存在原 allocation 使至少 n−D 组 unit；NO 对每个原 allocation 至少 \(\gamma_{lo}n\) 组质量≤δq。增强 unit-FSLP 可行性分离这两类：YES 可用 D 个不同 repair 补齐；NO 删除 repair 至多救 D 组，与 C 的低组计数矛盾。promise 外无判别承诺；它不构成 E0 的一般可靠 FAIL，也没有给到此 promise 的困难源归约。

实际调度按**原 unfloored table**重取 attaining state：selector 放选中 root，只外送该 state 分配到的正资源 incidence，其余、全部未选态及显式零 jobs 留原 root。每原 job 恰一次，
\[
L_{selected}=2-r_g,\qquad L_{unselected}=1,\qquad L_{resource}\le1.
\]
故全矩阵峰≤2，少于 ηn 个 selected roots 超过 \(2-q_\eta\)；unit allocation 才直接给实际 OPT=1。软件 A–F 尚未实现是工程状态，不撤回已证数学规格。

**接续缺口：** 把少于 ηn 个例外 selected roots 接到**同一实际全机容量**的修复/重选机制，并证明固定余量与总位复杂度；或给所研究外部源的显式 norm1、正-support LP、原组/资源和全部 jobs 保持接口。NSW 乘积不控制全组 minimum，当前结论不保证全机 \(2-\varepsilon\)。加权、oracle-only 或一般次可加后端均不在 B 的已证域。当前 integration 的 R50 若仍泛称上述 B/C/D/E 未付，应按现行 v6 收窄，不能据旧条件综合对象回退该成果。

## 4. 独立定义/障碍线：保原机器分组与全局 coupling

| 别名 | 当前 object_id / version / 状态 |
| --- | --- |
| G | `EA-GROUPED-CONFIG-COVER-v1` / v1 / proved |
| S | `UM-CAPACITY-ONE-PAIR-GAP-v1` / v3 / proved |
| L | `EA-GROUPED-CONFIG-GLOBAL-GLUE-v1` / v1 / proved |

**E3** `ea-um-grouped-cover-and-pair-gap-give-global-glue-criterion`，路径 `map/edges/boss2-cross-grouped-config-3c-395e59322b5bee40/ea-um-grouped-cover-and-pair-gap-give-global-glue-criterion.json`。**ALL(G,S) → L，accepted/unconditional/whole_result**。

G 的整数等价是 \(OPT\le T\iff\exists C_i\in\mathcal C_i(T),\cup_iC_i=J\)：每台**原机器**一个真实负载≤T的配置；交叠任务择一删重不增负载。它不是 CONFIG 分数值等于 OPT，也未给求配置的算法。

GPC₂ 给每原机器完整行律、每原 job 期望重数1，以及全部机器对的同边际且支持不交的 pair laws。若**给定全部 pairs**有同一个全机联合延拓 μ，则有限个不交事件同时几乎处处成立，\(X_j\in\{0,1\}\) 且 \(EX_j=1\)，故每个 job 几乎处处恰一次；正质量元组给实际 T 调度。反向真实 T 调度只给**存在某套** Dirac 行律/pairs，不能延拓任意预先指定 W。

S 的容量一星族对每 k≥2 在 T=1有全部 GPC₂ pairs，真实 \(OPT=2-1/k>1\)：k 个 X 对 k−1 个 G 迫一中心留 X；本块 k 个 Y 占 k 台 R，只余一台接 Z，中心至少再留 k−1 件时间1/k的 Z；相反显式调度达界。四类非乘积 pairs（G–G、同块 R–R、V–R、V–G）保完整行边际，其余支持分离取乘积，k=2 的零项合法。由解码知该族 T=1不存在联合延拓；这不是仅漏造一份见证。

进一步，可调度也不保证指定 pairs 可粘：三机三单位任务全可达、T=1、各行均匀时，分别规定 \(x_2=x_1+1,x_3=x_2+1,x_3=x_1+1\)（模3），每 pair 合法却全体矛盾。无色目录丢原机器身份是另一个障碍，本线保身份后仍暴露全局相关性。

**接续缺口：** 若用于算法，须给可在原输入位复杂度内生成/选择的共同状态及正质量元组恢复；只写有限联合延拓 LP 可能有指数变量。不能把“每对可行”换成“全机可行”，也不能把拒绝某指定 W 的延拓当作原实例不可行。星族只否定这个局部接受合同的阈值保证，不否定一般 UM 统一改善。

## 5. 后续 Main / 三个 Solver 的最小消费分工

以下是研究入口，不启动暂停中的旧研究系统、不新建重复构图任务。

| 角色 | 精确起点 | 下一项应产出的数学责任 |
| --- | --- | --- |
| Main | `UM-TARGET-v1`、`UM-MODEL-v1`、E0 | 保原题全部量词；对所选方案说明原输入怎样入域、阈值过程的成功/FAIL、固定余量和总位复杂度。三线成果作为各自的局部工具，只有补全共同前提才能组合。 |
| Solver 1 | A、N、E1 的 ALL 闭包及 R §§2–5；另带 E1b 的 free+quota ALL 闭包 | 明确全部 indexed states 和实际 jobs，覆盖任意 full-vector 重选；证明真实 NO 或新的低峰→一致性及 YES/位长保持。同菜单统一常数保值的逐坐标事后 repair 已否；改变菜单/任务/资源的新编译须给自己的全调度证明。再次保值降度本身不产生 gap。 |
| Solver 2 | B、C、E2 whole | 固定例如 η=1/2（q=2^−48）后，针对拟用修复机制写清例外根的原任务去向和**共同**接收容量；证明全组/全机固定改善，或给该机制的精确反例。B 的同输出全 y 保证及 C/D/E 不重列开放。 |
| Solver 3 | G、S、L、E3 whole | 选择并写清一个可计算的加强共同状态合同：能自主选择 pairs 时保哪些原行/标签，怎样取实际元组；证明所选结构的完备性或精确障碍。避开“给定任意 W 均可粘”这个已否命题。 |

用 `context`/packet 消费时，E1 必保 A 与 N 两个前提；E1b 必保 A 与 quota 两个前提；E3 必保 G 与 S。E2 的 source 单一但目标 norm1/unit-FSLP/REPAIR 条件不能被过滤掉。若只拿 contribution，携带其 remaining；若选 whole，仍按完整目标陈述消费。正支持、反驳、条件结果和研究线索分别阅读。当前这些路线没有一条已经支付 E0 所需的全原输入接口。

## 6. 精确证据定位与本轮核对

本轮直接实读的承重正文：原题/模型全文；A 全文；N 全文；`archives/unrelated-machines/state/定理/完整菜单的资源度三路径归约--定理.md` 全文；R §§2–5（其余只作范围辨别）；`tools/evidence/private-tree/partial-quota-welfare/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary.md` 第1–639行（共用位引理、A、B1–B6、C/D/E、F勘误，未用F2）；B/C 的当前主 body 两页全文；G/L/S 三篇主正文全文；E0 source 的“阈值接口与可靠失败”整节；E0–E3 全边。三个 Boss7 既有复核报告仅作定位/交叉检查，没有替代本轮读证明。

| 采用边 | 完整文件 SHA256 |
| --- | --- |
| E0 | `276bdbcab33202815d533ea389b7215aee859770a9ff76c96468314da4b23cc5` |
| E1 | `e6c3a2932b3a2ba565dd5b16c3cc2c52e80d7a3b116f7deaddf4be185db48903` |
| E2 | `cc507044caf4d53b3efe0c60cd2fbd5651331535ee1343842fbb2833e5b92d0a` |
| E3 | `2ffdeb2fbd7575a13e5a23da97f6203dd8704c4195307ef217fab625ebaea2a0` |
| E1b（Boss5本轮补入） | `30532f4b034ef64d4b06c3cf9e53896bbba11a8902128e88548b4e4b8de8b6b7` |

原入口的 E0–E3 四边均在上述两次快照 `registry.edge_files`；逐项按现行序列化规则重算 endpoint pins、review_digest 和各直接 evidence 的全文 SHA，全部匹配；所用十一个登记对象的主 body SHA 亦匹配。这里的字节核对辅助导航，不代替以上数学判断；未新增科学实验、实现或全仓验收。本轮未发现所采用关系在其明示范围内的承重缺步；列出的缺口均是从这些已付局部结果继续研究一般目标时尚需另证的责任。

Boss5 增补 E1b 前已实读原 free 构造、整数配额与同菜单阻断证明，并对照现役完整联合边；独立 fresh 终审见 `research/workspaces/map-v2/Boss5/finalization-20261116/um-entry-final-review.json`。E1b 的两源与目标均为现役 proved 对象；该补充只使已有障碍可见，没有新造关系或扩大阻断域。
