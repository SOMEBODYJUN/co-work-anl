# v5 新增§21–27：最终实际阅读范围与攻击

审者 `/root/sol_general_repair`，2026-10-18。结论：完整实读 v5 新增 104 行后，压缩正文保留了 074556 实际-I/全有理算法的承重推导，限定域数学无 standing fatal。本票是知情作者后置 final-read，不是新 fresh/blind 票，不代签软件、外审或新颖性。

## 1. 精确字节和实际范围

实际源为 `/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/multi_outer_single_state_tiny_home_rounding.md`：52640 bytes / 486 lines，整文件 SHA-256 `f91b32aba8da447fb0838849fb1a63a1d48296b96e5bb156646eb01c67c27aec`。

本轮完整阅读第 383–486 行，包含开头空行及§21–27全部正文，共 104 lines / 11122 bytes；该后缀 SHA-256 `b424b1bc66afac3913fa8e1e39bdd160b4e91bf677de4bc9202a9337a9a1d65f`。没有输出截断。旧第 1–382 行本轮只核字节 hash：41518 bytes，SHA-256 `9ddf2305f65389409b7f4955a58a72256c98113d52e782cf108588d6819bde99`；这不构成旧全文重审或把旧审票自动扩域。

背景：我是新 O1k 504e Exact 和另一 0f5e profile/log/FW Proof 的作者；此前已完整读 NSW 074556 的 182 行算法并冻知情后置票 `d93d31e65a79b8bd1037c81bc002effff77156fb0de7184ea558f82d9994ab78`，该票含本人的 Fraction 常数核算。root 先告知本稿由 074556 压缩，本轮据此复核。未在本轮打开新审查链接、任何软件、运行 JSON、NSW 437c 或其它此前未读源。

## 2. Domain、证书和所有阈值

v5 明确另立算法与域身份，k≥2只用 ν≤1/(1024k)，k1不设 tiny；原 fallback 系数仍可大。outers单 state、homes全局互异、每home一个own-unit helper及 B-only threshold-UD 叶均承继明确 typed 定义。没有转为一般 UM。固定叶阈值仍 ε=15/16；r=18/19只用于可靠 FAIL 的实际 V 界，二者没有混用。

FAIL 无叶 matching 时 V<ε<r；终点某 L_i<q 时只推 V≤r，而此弱等号已足以 `(19/10)(2−r)=2`。成功 q=19/100 给 Good mass至少 t=1/10，包括 L_i=q 的等号。程序不以“实际 V>r”作测试；该前件只在反证中构造共同参考。OPT=2−V 的 C<2 decoder 与 C≥2 平凡分支继承既有非空 normalized-flat 合同，未将一般零 OPT 约掉。

## 3. 真实 I、matroid 候选和 same-outer

vacancy M 的实际定义 `D⊆B independent iff B\D 匹配全部叶` 足以固定资源侧 ground；positive incidences 为 parallel copies，另检资源不重复。实际 I 和每个候选始终每 helper至多一个原 fallback state；其它 helpers只能丢旧项，不会换其原state。weighted greedy + matching 为可实现 finite oracle；当前旧state候选含 I，δ_j≥0。无 fallback 的 j 始终空、δ_j=0。

§22 的 weighted-rank 次模求和得到 `h·L*≤2h·L+Σδ_j`，不误加“当前 I 全 ground optimal”。参考从同一次实际 allocation 提取，故全部 outer同时 L_i*≥V²，叶匹配与这些 B bundles 共存；没有给不同 i 复制 B。

§23 实际保留 `T≤B_new` 的 linear-optimality 依据。owner净坐标包含 T_i，即使其还有其它 helpers仍落 [−B_old,B_new]；因此 weighted L∞、L1、square三式均成立。压缩未把 same-outer 丢失或 λ_min 付款省掉。

## 4. 相对余项和 global progress

§24 四种位置均付清：倒数/倒数精确 remainder；倒数→线性使用 `d+Δ>0` 与 tangent dominate；线性→倒数付 `a s²`；线性/线性为零，q边界连续。m整数求得、m²≤2k、νh_max≤1/8确保这些是每个实际候选允许的步，没有冻结沿程gradient。

停止求和每 helper付 τ/N，故合计 τ；`Σ w_j²≤ν` 与 `h_i≤h_max` 只使用新 O1k tiny。某终点 bad coordinate 给 S≥64m²≥64k，Cauchy 给 Σ√h≤S/8，产生净系数 `2334307/102921100` 及 k≥2 最小余量 `59552417/20584220>0`。Φ range≤(808/25)k² 与每步严格增>1/(100N) 给 <3232k²N 接受次数，不依赖实际 YES。各常数与此前本人 Fraction 反算一致。

k1 实际-I算法单独取 h=1、Φ=L，不套相对二次界或 prefix loss，<100N步，终点比较 `(A−τ)/2=32039/72200>q`。它正确覆盖 ν=1。

## 5. 全 jobs、总位和 source 范围

成功时 Good 的 I 子集仍 M-independent，故补上一次共同完整叶matching；所有 homes不同，非Good helpers归own，Good与叶B资源不交。逐selector及selected-state真 bundle 输出保全部原 inactive/zero/duplicate jobs；所有其它 incidence留private，各 job恰一次，原finite endpoints合法，资源≤一、selected private≤19/10、inactive private≤一。counts保持 S+U、G+I、S+2I。FAIL全private baseline同样运行每个原job。

每轮从原 incidence bitset 重算 L，原产品子和有共同 polynomial-bit 分母；h、φ和 k项求和只有有理倒数/平方，非递归分母扩张。结合显式步数、有限候选和 matching可得 worst-case总位多项式；本算法不借另一 profile/log/FW Proof 补任何 oracle。

unit-home直接桥按已引 normalized-flat 非空 group 域 m≥1 理解。正值迫 outer拿home覆盖 V>0，V=0由原 V≥0补齐；C<2的完整 unit链迫selector回旧fallback，C≥2用旧baseline，反向新机器负载一。Q counts与 finite endpoints S+2I+6m相符；旧selector获新endpoint这一事实与正文相容，正文没有声称仅添加不交固定jobs。它不认领一般UM→Q归约。

最后的 source排除只针对整个像均在该typed域的NP归约。固定 γ∈(0,.1) 时 YES输出≤1.9而NO实际≥2−γ>1.9，确能区分；未排一般 normalized-menu 或一般UM源。multi-state outer、home重合、nonUD extras和general输入仍未解。

## 6. 冻结判定

新增§21–27完整数学规格及当前scope无fatal，支持正式 v5 限定算法与 source边界。正文诚实区分实际-I有理后端和另一 profile/log/FW 算法，也明确旧软件不升级。关于 root/NSW审读的过程描述与我收到的消息及实际打开范围相容，但我没有用未打开的票替它们作独立来源认证。

本次只有源字节/hash检查；未执行算法、matching后端或任何 end-to-end代码。全称正确性由上述证明核对支持，非有限软件结果。未改repo、旧正文或旧冻结票；一般 UM-TARGET-v1正反面仍 OPEN。
