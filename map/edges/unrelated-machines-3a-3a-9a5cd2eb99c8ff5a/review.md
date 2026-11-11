# 精确负载 DP 与 PARTITION 共同推出有界树宽的完整 FPTAS/弱困难性结论

## 当前对象、范围与复用

本包核心 M247=`M-247deecec83946358afe4e89413a7bd1` v5；比较 M14=`M-14dbe6980117492aa7a3b48c52378dcb` v5 与 KP=`M-e8d9614430ab49fc99125452d10388f1` v1。三者的当前 registration pins 与任务 input_pins 相同。模型为不可拆分任务、显式有限资格端、二进制正整数有限加工时间的 R||Cmax；不要求同一任务在各机器时间相同。

当前 canonical 已有 `um-constant-tw-exact-load-dp-contributes-fptas-runtime-v5-ea3c`，方向 M247→M14，accepted / unconditional / ALL / contribution，准确支付 FPTAS 算法半部。其 edge、完整 review 与 receipt 本轮实读，旧字节保留。本轮逐条检查当前 registry.edge_files 指向的边 JSON：三端点的现有 incident 边中没有 {M247,KP}→M14 的共同 ALL whole_result。本包不再造第二条 M247 单前提算法贡献边；新增的共同 ALL 边补齐独立困难性后，才声明 M14 的整个结论。既有贡献边依然有效，不被本包 supersede。

## 一、M247 的两参数与正确 DP 语义

源 PDF 页1–11的定义、Theorem2/3 和 treewidth 全段已亲自连续文本实读；视觉核页4、6、9、10、11。中文完整正文及正式 join audit 亦完整实读。源页4的 L 必须是实际枚举的机器负载集合大小。目标阈值 T 内只能说 L≤T+1（含零）；全体调度的可达负载不自动被 OPT 界住。另一支对 d=max_i |J(i)| 枚举每机资格任务子集，给 L≤2^d，指数不能删。

对 OPT 参数支，阈值依次 T=0,1,…直至首次可行，总代价仍为 (OPT+1)^{O(k)+1} poly(input)，所以是参数对 (k,OPT) 的 FPT；不是仅由 k 的 FPT。对资格度支，预先枚举每机至多2^d个子集和，位长为输入位长的多项式，再运行 L^{O(k)} DP，得到 (k,d) 的 FPT。目标求和/比较的整数位运算开销仍须计入；O(nm) 的论文式不把大整数算术当成免费。

完整 Cmax 的 join 必须加入父活跃负载 max_i λ_i。audit 的完整矩阵是 x,y 两任务及 a,i,b 三机器，p_ax=p_by=2、p_ix=p_iy=1，其他端禁止。dual 取父袋{i}、子袋{i,a}/{i,b}；incidence 取父袋{i}、子袋{i,a,x}/{i,b,y}，空根/空叶按 audit 补齐。父 λ_i=2 强制左右各贡献1；子完整 Cmax各1而父2，精确否定原印式，不是否定修正后的 Theorem2。已经失活机器只属于一个子树，活跃机器的合并负载由 λ 固定，非负性保证子部分不超过父总负载，故加项后正反最优性都成立。

等价 closed-max 表值只计已忘机器：join 合并任务计数、相加活跃 λ，并取两个 closed-max 的最大值；forget-machine 时以 max(c,λ_i) 收入完整机器负载。任务选边计数为0/1，introduce-edge 唯一，forget-job 强制恰1；空根正是合法调度的完整 Cmax。nearly-inactive machines 为 M_t\M_parent，incidence 任务拆分覆盖 J'∪Jtilde，左右投影负载相加等于父 λ。这些均采用当前已修正正文，不把源印式的遗漏变成额外条件。修正不增状态维度。

## 二、算法半部：复用旧完整缩放证明

固定任一 dual 或 incidence 树宽界 k。先处理空任务（返回空调度）及无资格任务（判不可行）。既有 ea3c review 的完全自足路线是：逐任务选择其最短有限端，所得合法调度的峰值 B_min 满足

OPT≤B_min≤Σ_j min_i p_ij≤n OPT。

令 ε0=min(ε,1)，q=ε0 B_min/n²，只在有限端取整数 a_ij=ceil(p_ij/q)。若允许零加工时间且 B_min=0，已有调度即最优；当前正整数非空模型 q>0。对原最优 σ*，每机至多 n 个任务，故 q load_a(σ*,i)≤OPT+nq。令

K=floor(n²/ε0+n)，L≤K+1。

此 cap 保留 σ* 与至少一个缩放最优调度。每个中间负载都是最终负载的非负子和，所以逐状态剪枝安全。M247 的明确 L^{O(k)} DP（含已修正 join）及实际父指针给缩放最优调度 σ_a，满足

C_p(σ_a)≤q C_a(σ_a)≤q C_a(σ*)≤OPT+nq≤(1+ε)OPT。

资格边不增加，原分解继续可用。对 dual 宽 k，每个 M(j) 是大小≤k+1的团且被某袋包含，把 M(j)∪{j} 作为叶袋接上即得 incidence 宽≤k+1。给定分解直接运行；未给分解时旧 review 已给固定 k 的 |V|^{O(k)} 边界/连通分量分解搜索的完备性证明，不把该入口说成参数 k 的 FPT。

网格用整数除法 ceil(n² v p_ij/(u B_min))（ε0=u/v）计算，操作数位长是输入与精度编码长度的多项式。大于 K 的单端跳过，不按 B_min 数值大小建立数组。nice incidence DP 每个活跃任务一位、每机0..T负载，最多2^{O(k)}(T+1)^{O(k)}状态；二分0..K只多对数因子，真实回溯为每个任务输出实际机器。因此对每个固定 k，时间对输入位长与1/ε为多项式，次数允许依 k；这准确是 M14 的 FPTAS，不声称 EPTAS。

M14 正文的另一条二倍上界路线也已付清条件：给一个合法上界 OPT≤B≤2OPT，取 δ=ε0/2、q=δB/n，cap 应是 B+nq=(1+δ)B，缩放负载数≤floor(n/δ+n)+1。原最优调度舍入后峰值≤OPT+δB≤(1+ε0)OPT，回溯同上。不能用原 PDF 的 (1+δ/n)B 及 n/δ+2。B_min 路线不冒充二倍界，也不需要未实读的 LST 外部算法来计算 B。

## 三、困难性半部：KP 的显式二机映射

KP 的精确语言是显式正二进制整数 c_1,…,c_s 是否存在和为 S/2 的子集，S=Σc_j；其 NP 完全性合同、完整指定证据路径已实读。Cook 完全性仍是该对象明确导入的外部起点，本包没有重新阅读 Cook 原文或 Karp 原 PDF。

全输入 many-one 映射如下。非合法编码先映射固定 NO；空合法序列（若编码允许）映射空任务、T=0 的 YES 实例。S 为奇数时映射固定 NO：一任务在两机器加工时间都为2，阈值1。S 为正偶数时建立两台相同机器，每个 j 在两机的时间均为 c_j，阈值 T=S/2。所有任务均恰有这两个资格端，任务数不膨胀，整数求和和写阈值按二进制位长为多项式。

若 KP 是 YES，把对应子集放机器1，其余放机器2，峰值T。反向若两机峰值均≤T，总负载S=2T迫使两机都恰为T，机器1上的任务给 KP 见证。故 YES与NO同时保留。调度判定属于 NP：每任务一个机器位是多项式证书，精确整数加法可验证阈值。

非空主构造的 dual 图为 K2，宽1；incidence 为 K_{2,s}，取一条由袋{machine1,machine2,j}组成的路径，宽≤2，全部资格边被覆盖、两个机器袋连通、每任务仅一个袋。空/固定分支的宽度不超过这些界。因此 NP-hardness 已发生在 dual≤1、incidence≤2 的常数宽度类，而不是声称宽0子类也困难。

该归约给数值型 PARTITION 障碍，不给强困难性或近似 gap。二机子类可用0..S的子集和表在 O(sS) 算术步求精确最优。更一般，对每个固定 k，M247 的阈值负载 DP 在合法可计算上界 U=Σ_j min_i p_ij（或 B_min）内二分 T，代价为 U^{O(k)} poly(input)，是伪多项式精确算法。NP-hardness 与该伪多项式 DP 共同兑现 M14 的弱 NP-hard 表述；本包不由 PARTITION 归约推出“非强困难”的无条件复杂性分离。

## 四、共同 ALL 的完整结论与不可逆方向

新增关系为 {M247,KP}⇒M14。M247 给可裁剪、可回溯的精确负载 DP及缩放算法；KP 给二进制 PARTITION 的 NP 完全性。两者连同上面的显式桥共同推出：整数 R||Cmax 的有界常数 dual/incidence 树宽类仍弱 NP-hard，而每个固定宽度和每个 ε>0 有运行时间 poly(input,1/ε) 的 (1+ε) 合法调度算法。所有附加桥都在本 review 证明，没有未付开放前提，故 accepted / unconditional / premises_mode:all / whole_result。不是把两条独立替代证明合并，而是整条目标的两个必要分工。

KP 本身不证明算法，M247 本身不证明 NP-hardness；保 ALL 不能拆成两个单前提 whole 边。既有 ea3c 单前提算法贡献原样保留。反向 M14⇒M247 的整条 FPT 不成立于现有推导：取极小 ε 逼整数最优最多给含 n^{O(k)} 的时间，未交付参数对 FPT 的固定输入次数，也未交付最大每机资格度支。本包不把这个“现有推导不能支持”写成数学上的不可归约或定理否定。

## 五、实际阅读与交付边界

亲自实读：AGENTS、IMPLEMENTATION、worker提示、当前任务；三对象完整记录及绑定；结构参数中文全文；正式 join audit 全文；冻结 PDF 页1–11连续文本及页4/6/9/10/11视觉；KP的body和全部7个指定必要章节（§1、§2、§4.1–4.3、§5.4–5.5）；ea3c 的完整edge/review/receipt。当前 canonical edge_files仅为去重逐条加载JSON，未重审其它数学端点，也未把其它历史worker的PDF阅读记成本轮。

PDF页12–19已经导出但没有作为本轮实读；rankwidth段中文已读，仅确认与本核心证明不承重，不声称重审其PTAS。Karp/Cook原PDF未读；不新增外部文献结论。没有旧科学程序重跑、没有有限扫描来替代证明；反例和两机映射都是上面的精确符号推导。任务未声明overlap_comparisons；两只读对端的比较在收据逐项关闭，无需新后续任务。无新正文/registry修正请求。只写本任务write_paths及独立recovery目录，Git和队列由Boss组织；原生bind/check作为局部校验，不替代数学审读。
