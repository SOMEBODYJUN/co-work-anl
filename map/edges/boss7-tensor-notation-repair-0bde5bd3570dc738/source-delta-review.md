# 裸 Cartesian 附属审计记号修订：六核心定向继承与两条关系复核

任务：`boss7-tensor-notation-repair-0bde5bd3570dc738`；沿用 Boss7，2026-11-16。
直接替代已 done 的 `boss2-6405-source-repair-74d84ac2223f267e`。
本轮只修订 A 的证据版本绑定，亲自复核由 A 参与的两条 ALL 关系；其它有效数学按原 SHA 继承。
不把前任务的全包读取、37 页 PDF、有限复算或历史独立审查称为本轮执行。

## 1. 唯一变更、当前身份与实际读取范围

A 是 `UM-NORMALIZED-FLAT-CARTESIAN-TENSOR-REVERSE-AMPLIFICATION-v1`。
`research show` 核到当前 v3、`truth_status=proved`、`binding_status=current`，pin 为
`54a098141d2c72f69ed8b861f27d4f6602bffc7f1e3fcfe768ea0340b9c7e94c`。
原 v2 pin 为 `d81f97599f437f633889dd1bbb6df2f76d3f2c3e1e9de833eaf7f0a4f02832aa`。
两个任务的 input_pins 逐项比较，只有 A 改变；六核心的当前 pin 均以本轮 `research show` 核对。

改动只在附属有限审计
`archives/unrelated-machines/state/审查/裸Cartesian张量反向放大独立实际稀疏审计--审查.md`
的 `2. 稀疏普通 UM 输入与完整 jobs 口径`：

\[
b_i+g_i a_i=\ell_i(g_i)\pmod2
\quad\longmapsto\quad b_i+g_i a_i=\ell_i\pmod2.
\]

修订后 SHA 为 `9f737f4273c0ec43254231039be810b99da901ca5ce3af7ebf3d07b2d6d6f74e`。
冻结 original 的 §3 本来就是 `ell_i`，SHA 为
`55041afcaa86bf12918f76085449b881a08bad0814cbcd1ba4173069f62508f4`。
一般完整菜单遍历 indexed 向量 \(\ell\)，不施加共同局部函数；循环见证
\(\ell_i(g)=g_{i+1}\) 在 \(t\ge2\) 可以依赖其它坐标。
因此修订消除的是清洗时额外暗示的受限语义，A 的主证明、model、statement、quantifiers 和数学状态均不变。

本轮完整实读并逐式比较以下数学正文／冻结原件：

| 文件 | 本轮读取及用途 |
| --- | --- |
| `archives/unrelated-machines/state/反例/裸笛卡尔菜单乘积的精确反向放大--反例.md` | 全文；重点 §1–5 的原菜单、任意标签上界、循环下界、全部原任务 OPT 与显式规模 |
| `tools/evidence/private-tree/bare-cartesian-proofs/normalized_flat_cartesian_tensor_reverse_amplification_proof_v1.md` | 全文；亲核 A 的冻结作者原证明，不以复核报告代替原证明 |
| `archives/unrelated-machines/state/审查/裸Cartesian张量反向放大独立实际稀疏审计--审查.md` | 修订后全文；有限 audit 的真正支持定义、全 jobs 与 t=1/t≥2 的区别 |
| `archives/unrelated-machines/tools/evidence/tensor-reverse-actual-audit-20261031/original/tensor_reverse_actual_audit_review.md` | 全文；§3 正确原记号与有限运行口径 |
| `archives/unrelated-machines/state/定理/归一化菜单的三态资源度三正规形--定理.md` | 全文；选择树、K=1、off-path、全部调度与 positive partial、端点、显式位复杂度 |
| `archives/unrelated-machines/state/定理/完整菜单的资源度三路径归约--定理.md` | 全文；ports、每 helper 三件真实任务、任意目标低峰逆投影、正 partial、OPT=2/V=0；文献归属段只作范围说明 |
| `archives/unrelated-machines/state/审查/裸菜单读后与保值降度及调色板障碍--审查.md` | 全文；本边仅复核 §2–5 的迁移贡献，不重新认证 palette 历史／外部困难性 |
| `archives/unrelated-machines/state/定理/逐坐标一致菜单的整数资源配额--定理.md` | 全文；任意固定 f 的全局资源平移、三符号并集、全部 Hall 子集、整数化与 §5 repair |
| `archives/unrelated-machines/state/审查/逐坐标配额读后与统一保值修复界限--审查.md` | 全文；固定 θ,c 后选同一 t 的存在性反例及未被否定的域 |

同时读本轮任务、前任务及其回执、两条受影响原边、三个给定勘误／影响文件；核三份保留逻辑边的端点、条件与证据绑定。
前任务的六份阅读／有限核验附件只核 SHA 并保留其历史身份，不重新执行其脚本。
任务给定完整背景估计 417,992 tokens 大于声明 reading budget 300,000，且另含未计数 PDF；本轮采用定向 repair，不声称重读该全部背景。
没有重跑历史 sparse-P 审计、t=1 枚举、quota 实验或 BLMRS 文献审读；一般结论以下用解析证明复核。

## 2. A 的两个数值：一般标签、一般 partial 与全部实际任务

令 \(D=2^t\)，\(t\ge1\)。组和 indexed state 都遍历 \(\mathbb F_2^t\)，资源是
\((a,b)\in\mathbb F_2^{2t}\)，支持为 \(b_i+g_i a_i=\ell_i\)，每项权 \(1/D\)。
每个固定 \((g,\ell)\) 对每个 a 恰有一个 b，故有 D 项，质量恰1；实际矩阵保全部 \(D^3+D\) 件原任务。

任取实际所选标签，补组 \(h=g+\mathbf1\) 的两支持共同资源由
\(a_i=\ell_i(g)+\ell_i(h)\)、\(b_i=\ell_i(g)+g_i a_i\) 唯一确定。
若每组都领 D 项则这两组冲突，故任意标签和任意 partial 都有最小质量至多 \((D-1)/D\)。
循环选 \(\ell_i(g)=g_{i+1}\)，给 g 领取全部 \(a\ne\mathbf1\) 对应的 D−1 项。
若同一资源由 g,h 领取，\(\delta=g+h\) 满足 \(\delta_{i+1}=a_i\delta_i\)。a 的一个零位沿环迫全部 δ 为零，故领取真实不交。
t=1 同样成立，t=0 不在域。因此 \(V(P_t)=1-1/D\)。

达界完整调度把每个 selector 放循环所选 private，只外送其 D−1 件已选 incidence；剩余及全部未选 states 的 incidence 均留原 private。
已选 private 峰 \(1+1/D\)，未选 private 为1，资源至多一 unit；每件原任务恰一次。
任意完整峰 \(C<2\) 调度中，补组两个实际所选 states 在共同资源上的两件不同 incidence 至多一件可外送，另一件与实际 selector 同 private 给 \(C\ge1+1/D\)。
未选任务外送不能释放该冲突；\(C\ge2\) 分支平凡。
故 \(OPT(P_t)=1+1/D\)。这里既没有删未选任务，也没有把有限 audit 外推成一般证明。

## 3. 第一条关系：A 与正规形 N 联合迁移

N 是 `UM-NORMALIZED-FLAT-MENU-THREE-STATE-DEGREE-THREE-NORMAL-FORM-v1` v4，当前 pin
`90151b0b805a9fb10bde855a89b069771b031383ce88493450dfb04c6269858c`。
A 的每 state 质量1、完整 selector/incidence 资格精确落在 N 的显式 normalized flat 输入域。

选择树 T 每顶点恰一 selector，非 root 有 fresh own-resource；root 两 child singleton、非 root internal own 与两 child 三态、非 root leaf own 与原 state 两态。
原 private 与全部 incidence 保身份；K>1 的原 selector 移到 root，终 leaf 新 selector 替换原单位负载；K=1 原任务不动。
正向按源 selector 的实际 state 走树路径，off-path 取 own，所选 singleton 外送，其余留 private，原 incidence 的所有实际端决定保持。
逆向 \(C<2\) 时所选 singleton 必外送，root 已占 child-own 就迫 child 不能选 own，沿实际链到一个原 state；移回 root selector 替换 leaf selector，删除新任务，全部旧 incidence 仍按原实际端投影。
不假定 off-path 只存在规范活动，也不合并多个 leaf。

随后对 T 后全部旧资源、own-resource 与零权 membership 作路径 D。
资源接 d 组则有 d ports 和 d−1 helpers；每 helper 一 selector、两件不同 incidence，恰两 singleton states。
正向为至多一件实际旧 unit export 留孔，其它 ports 由 helpers 占用；所有任务各执行一次。
逆向任意 \(C<2\) 时 d−1 件所选 helper incidence 被迫外送到不同 ports，至多一件旧任务外送；未选 helper 外送只会额外占容量。
合 ports 后原任务合法，峰不增。每 port 只接一旧组和至多两 helper，故资源跨全部菜单按组计的度≤3；三态上界仍保持。

对每个 \(0<v\le1\) partial，singleton 必领与质量1给同样两向链／留孔证明。
有限最大值闭合 V=0；每 state 归一化给两侧全 private≤2，严格低峰两向加最优性闭合 OPT=2。
\(C=2\) 不能使用强制外送；给定高峰调度时可另用全 private 基线。
新增数目按显式 incidence 线性界控制，原二进制有理数只复制，不按分母或阈值倒数展开。

因此 ALL(A,N) 得到显式总位多项式的 \(P_t^*=D(T(P_t))\)，并有
\[
K_{\max}(P_t^*)\le3,\quad\Delta_{\rm resource}(P_t^*)\le3,\quad
V(P_t^*)=1-2^{-t},\quad OPT(P_t^*)=1+2^{-t}.
\]
A 给本族数值，N 给真实桥，不能拆成任一源单独足够。
原 `transfers/accepted/all/unconditional` 的 **contribution** 保留，仍只支付目标 read-object 的 §2–5。
T 引入的 singleton 经 D 仍为 singleton，故输出不再是每 state 至少2项的裸族；不保原组数、组交互度 M 或旧 selector 资格。
保值压态／降度保留的是已改善的 NO，不能恢复它；不推出新 hardness 或一般 UM 入域转换。

## 4. 第二条关系：free 高值与 coordinate quota 联合否定常数 repair

quota 的当前对象 pin `ea3d4f6579be1c34dfb18208ba8a905c326089874074f0c3ee2422d932bed386` 不变。
对任意固定共同 \(f_i:\mathbb F_2\to\mathbb F_2\)，统一资源双射
\(a_i'=a_i+f_i(0)+f_i(1)\)、\(b_i'=b_i+f_i(0)\) 把全部组同时化到零标签。
该平移不依 g，保真实共享；逐组分别重命名不能使用。
每坐标两条允许线恰有一个共同符号和两个独占符号，全部允许资源并集恰 \(3^t\)，故共同整数配额上界
\(k_t=\lfloor3^t/2^t\rfloor\)。

若资源含 h 个共同符号，它兼容 \(2^h\) 组，每兼容边给 \(2^{-h}\) 容量。
每组得到 \((3/2)^t\)，每资源总给1，故任意组子集 A 都满足
\(|N(A)|\ge(3/2)^t|A|\ge k_t|A|\)。
拆每组 k_t 槽后任意槽子集的邻集仍满足 Hall，得到真实不拆资源的整数匹配；所以每固定 f 的受限值恰 \(k_t/D\)，再优化所有 f 也不能增大。
连续比较值 \((3/4)^t\) 不替代该整数 floor，更不是原 UM 的 NO 值。

现在先固定任意 \(\theta\in[0,1)\)、\(c>0\)。A 的循环分配 \(A_t\) 值 \(1-2^{-t}\to1\)，故足够大 t 进入高值域。
同一菜单的任意逐坐标输出 B，即使从头重选全部 f、states、bundles，也有
\[
\frac{v(B)}{v(A_t)}\le R_t:=\frac{\lfloor(3/2)^t\rfloor}{2^t-1}
\le\frac{(3/4)^t}{1-2^{-t}}\longrightarrow0.
\]
取同一个足够大 t 使 \(v(A_t)\ge\theta\) 且 \(R_t<c\)，便有所有 B 都不保 c 比例。
这是存在性层面的否定，不涉及算法效率，不要求 B 保留 A 的具体资源。
free 值独自没有受限输出上界，quota 独自没有高值输入，因此原 ALL 的 `implies/accepted/unconditional/whole_result` 完整保留。
目标当前 pin `0e83cb7446ad2dc09b8a030adb02e74de1c38a27ad7aeee913cdf6e8ba5c5582` 不变。
\(\theta=1\) 的空输入域、随 t 衰减 c 或改变菜单／资源／任务的 compiler 均不被此结论排除。

## 5. 资产处置、继承范围与未付义务

前任务回执有11项资产，当前文件 SHA 全部与该回执逐项相符。
两条含 A 端点的边在本任务新目录写替代文件，**保 edge_id 和全部数学语义**，仅更新本轮审读说明与绑定；不改旧文件。
其余三条逻辑边及六份阅读／验证附件共9项按原 SHA retained，逐项去向见本轮 receipt.supersession。
保留附件内的“本轮／Pass1–5／全37页／实际运行”均属于前任务的历史记录；没有复制为本轮读取或运行声明。

另外三个核心本轮只核当前对象陈述／pin、前任务覆盖和资产／绑定闭合，继承其已发布有效数学：
q2 仍只付共同证书之后的最终 soundness，Fδ、完整 YES 调度、任意低峰证书提取与 source hardness 未付；
restricted Santa 仍有同一 token 非零端值不统一的边界，不升级一般困难性；
有理位桥仍保原实际算法蕴含，独立 SCHA 假设未被本次修正证明。
这些三核心没有以 A 为其已交关系的端点或证据，本次单行符号修订不触及它们。

当前及直接旧任务均无 `overlap_comparisons` 中的 follow-up 对；原回执 follow_up_tasks/closed_overlaps 都为空。
本次没有新的未答比较；保留上述数学开放义务，不编造新队列承接，也不以零边掩盖现有五条关系。
本轮新交两边已以本 clone 根 `work.py research edge-bind --write` 绑定后 `edge-check`，两次均 exit 0，返回 `edge-structure-valid-not-a-mathematical-verdict`，repair 的 proof_scope 为 `whole`，normal-form 迁移为 `step`。
三条 retained 逻辑边也只读 `edge-check` 通过，proof_scope 依次为 restricted `whole`、q2 `step`、有理位桥 `whole`；它们的字节均未改变。
这些程序结果只核结构与绑定，数学判定来自上面实际原证明推导。
Git、checkpoint、done、assemble 和公屏由 Boss 串行处理。
