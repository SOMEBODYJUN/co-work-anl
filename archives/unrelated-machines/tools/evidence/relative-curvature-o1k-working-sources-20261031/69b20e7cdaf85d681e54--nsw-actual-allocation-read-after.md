# O(1/k) NSW 实际分配算法：知情作者后置实读

审者 `/root/sol_general_repair`，2026-10-18。结论：完整实读下列 182 行新算法后，逐式攻击其实际 incidence 集、same-outer 损失、跨分段相对余项、停止证明和全 jobs 恢复，未发现 fatal；它给出原 504e Exact 的另一条完整数学算法。仅限该 typed 域与存在性合同，不升级一般 UM 目标，不认证软件、新颖性或外审。

## 1. 实际读取与身份

本轮完整读取 `/workspace/scratch/038d9dcc4cac/sol_relative_curvature_O1k_independent_exact_first.md` 第 1–100、101–182 行，覆盖全部十二节；实际 hash 为 `074556f862b8548349f1710caa540f0a45c18f08a3f42822208ed9eb39d89583`，16740 bytes / 182 lines。另全文重读原 29 行 Exact `/workspace/scratch/038d9dcc4cac/sol_general_repair_relative_curvature_O1k_working_exact_v1.md`，SHA `504e4d8e13b847aa7ec10f2bb3afa874389a76b6cc0962abfe979a985238a99f`。

这不是 fresh blind 票：我是该 Exact 及另冻 log/FW Proof 的作者；已知 v4、matroid sensitivity 和自己相对曲率路线。读新稿前，root 消息已告知其是“实际 allocation + 全有理分段倒数势”，并列出 same-outer、跨 cap、νh_max、终点 S 和 bit 的攻击点。我没有读取 NSW 此前 149 行 actual-allocation 背景稿或其 d555 记录，不为这些未打开来源作实读认证。本票只核本次 182 行自足推导。

原作者 173 行 log/FW Proof 与本次 NSW 有理倒数/实际整数分配算法是不同算法；本次不把任一数学票解释为另一算法的软件实现认证。没有改动任何旧 Exact、Proof、v4 或 review 字节。

## 2. 合同与两个阈值

504e 只要求该域 Q-alone、确定性 worst-case 总位多项式 19/10 完整输出，不要求特定中间 LP 或某个固定 FAIL 证书。NSW 采用 r=18/19 而非原作者证明中的 ε，合法地改变算法：其 FAIL 只声称 V≤r，足以因 `OPT=2−V` 给 baseline `2≤(19/10)OPT`。固定叶域仍严格是 ε=15/16，未被换成 r；反证 V>r 时有 V>ε，才可提取每叶资格 matching。无匹配时 V<ε<r，baseline 同样可靠。

成功分支中间福利阈值 q=19/100，最终各组质量 t=1/10。二者不能互换。终点 L_i=q 时必须走成功；FAIL 从某 L_i<q 推 V≤r，包含 V=r 等号。基线在 V=r 达相对比 19/10，严格性没有漏洞。

## 3. 实际 I 和单 helper 候选确实可计算

全叶 matching 已存在时，资源侧 transversal T 的 rank 为叶数，dual M 的独立性恰为“删去这些资源后，剩余 B 仍能匹配全部叶”。每 positive incidence 是相应资源的 parallel copy；因而 M 独立性强制一个物理资源至多一个标签。空叶给 free M，零 rank、loops/coloops 和 unused B 都不需假设排除。

当前 I 保持 M 独立，且每 helper 只用一个原 fallback state；候选 ground 只有 I_{−j} 及 helper j 的某一个完整正 fallback support。weighted matroid greedy 的每次独立性测试均可用普通 full-leaf matching 完成。其输出的其他 helpers 只能丢现有标签，不能换原 state；j 也只有一个 state。辅助 F 的多 state 并集仅在分析中出现。不存在 exponential subset/profile oracle。

当前 j state 的候选 ground 包含 I，所以每 helper 的最佳 linear δ_j≥0。无 fallback 的 helper 始终 I_j=∅、δ_j=0。初始所有 I=∅ 可行，无需找到一个具有正值的初始 actual allocation。

## 4. same-outer L∞/L1 与比较式

对任意该 linear-optimal 候选，旧 j、新 j weighted values 为 b,b′≤h_iw_j。其它 helpers 只丢标签，按 outer 的损失为 T_l，总 T≤b′：删掉全部 j 后的 I_{−j} 已是候选 ground 内可行集，optimality 给 `(W−b)−T+b′≥W−b`。这一步不要求当前 I 全局 linear-optimal。

令 s_l=h_lΔL_l。非 owner s_l=−T_l，owner s_i=b′−b−T_i。即使 owner 还有许多其它 helpers，T_i≤T≤b′ 仍给 s_i∈[−b,b′]，故 max_l|s_l|≤h_iw_j；再由 `Σ|s_l|≤|b′−b|+T≤2h_iw_j` 得 `Σs_l²≤2(h_iw_j)²`。原稿没有遗漏 same-outer 损失，也未免费除去 λ_min。

参考 I* 来自同一次真实 V>r allocation：outer 拿至少 V 的 home 权，失 home helpers 在 B 上各有 fallback 值至少 V；每叶从同一 allocation 中拿一枚 E_l，因而 I* 是 M 独立、每 helper 一 state，且全部 i 同时 L_i*≥V²>A。没有跨 outer 复用资源或拿未知 target 作算法输入。

weighted matroid rank F 的次模性给 `F(I∪I*)≤F(I)+Σ_j[F(I∪I_j*)−F(I)]`。每个边际至多 δ_j+W(I_j)，因为先删 j 的 ground 可被其参考 state 候选覆盖，而加回旧 I_j 的增益至多其原总权。故 `Σh_iL_i*≤2W(I)+Σδ_j`，不要求 I 当前全局 optimal。这一比较是实际算法足以代替原作者 fractional profile 优化的关键。

## 5. 分段倒数与跨 cap

k≥2，m=ceil(sqrt k)、a=1/(8m)。用整数平方比较求 m，且 k≤m²≤2k，所以 a≤1/16、h_max=64m²≤128k。新域 ν≤1/(1024k) 直接给 νh_max≤1/8。

φ 在 x≤q 时线性 `(x−q)/a²`，在 x≥q 时为 `1/a−1/(a+x−q)`，两侧值和导数相同。设 d=a+max(x−q,0)，则 d≤D₀=349/400；h=1/d²。真实允许步有 |s|=|hΔ|≤1/8。

两端均在倒数段时，linear remainder 精确为 `s² d/(1+sd)`，分母至少 1−D₀/8>0，系数至多 K=2792/2851。若从倒数段下穿 q，同一 bound 保证延伸倒数分母仍正；q 点 tangent（即真实线性段）在该 concave 延伸之上，因此实际 remainder 不会更大。若从线性段上穿 q，整段 |φ″|≤2/a³，remainder≤Δ²/a³=a s²≤K s²。都在线性段时为零。x=q 的两侧连续性也包括，故没有 cap 跨越时的梯度漏付。

将此逐坐标相加并用 §4 的 square bound，任一候选满足 `ΔΦ≥ΔW−2K h_owner²w_j²`。停止时每个最佳 linear 候选同样满足 ΔΦ≤τ/N，因此

`Σδ_j≤2KνΣh_i²+τ≤(K/4)S+τ`，S=Σh_i，τ=1/100。

这只用 h_i≤h_max 和 νh_max≤1/8，没有退回旧 k²/k⁴ tiny 条件。

## 6. 终点与有限常数

若终点某 L_i<q，恰有该 h_i=h_max=64m²≥64k，故 S≥64k；不是假设多数坐标未达标。恒等/不等式 `L_ih_i≤(q−a)h_i+sqrt(h_i)` 对倒数段为等式，对线性段右侧=q h_i，均成立。Cauchy 给 Σsqrt(h_i)≤sqrt(kS)≤S/8。

反证 V>r 后，下界系数可保守丢去 +2a，得到

`Σh_i(L_i*−2L_i)≥(9657/36100)S`。

停止比较式却给至多 `(698/2851)S+1/100`。净系数为 `2334307/102921100`，而 k≥2 使 S≥128；净余量至少 `59552417/20584220>0`，产生矛盾。故 terminal bad implies V≤r。这里没有用有限数值试验推一般 k 的符号不等式。

k1 另取 h_1=1、Φ=L_1，不使用 ν、m、a、相对二次界或 prefix loss。停止给 Σδ_j≤1/100；若 V>r，则 L_1≥(324/361−1/100)/2=32039/72200>q。该分支涵盖单个 unit home。它与 v4 的单 helper 顺序 greedy 虽不同，仍满足同一 unrestricted k1 域。

## 7. 总位、完整输出与退化情况

实际 Φ 从原 incidence bitset 重算 L。其分子分母由原 w_jp_jsu 的子和及一次有理倒数/平方决定；各轮不把旧 Φ 分母递归当新输入。k 项相加最多付 k 个 polynomial-bit 分母之积。每轮候选、greedy 排序和 matching 次数均 polynomial，严格增量 >1/(100N) 与 Φ range≤(808/25)k² 给 k≥2 接受次数<3232k²N；k1 range≤1 给<100N。没有指数状态枚举、inverse-p 循环、实数根或 exact log。

成功终点 Good={j:v_j≥1/10}。令其 home mass z_i，则 `L_i≤z_i+(1/10)(1−z_i)`，q=19/100 给 z_i≥1/10。保留 Good 的 I_j，是 M 独立子集；一次 matching 给所有叶分配补中 E_l 资源。Good helpers 用当前 fallback，其他 helpers 全部回 own homes，outers 拿 Good homes，叶选择原 attaining singleton coefficient 的 state。这是一个共同 integral allocation，无 rounding loss。

完整 ordinary 输出对每原 selector 选原 state，只导出该 selected-state 真 bundle 对应的原正 incidence。所有 inactive payload、重复 indexed states 的独立 jobs、原 zero jobs 和其余 incidences 全部留 private；unused resource 机器允许负载零。每枚原 job 恰一次，原 finite endpoints 不变，资源≤一、selected private≤19/10、inactive≤一。counts 仍为 S+U、G+I、S+2I，稠密写出也 polynomial。基线同样运行全部 jobs。

没有叶、没有 fallback、B 为空、M rank 零和当前 I 为空均可正常执行；不满足 actual V>r 时不要求一定成功，FAIL 基线已覆盖。typed 域 group 非空；不在本合同中硬套无 group 的 `OPT=2−V`。

## 8. 实际有限检查和最终范围

本轮仅执行一个 Python Fraction 常数检查，实际确认 source hash/16740 bytes/182 lines、D₀、K、净系数、最小余量、k1 下界、range coefficient 808/25、baseline 等式 `(19/10)(2−18/19)=2`、Good-mass 等式 `(19/100−1/10)/(1−1/10)=1/10`。未实现或执行 NSW 的 greedy/matching/搜索/alljob 后端，也未读取它的任何软件。这不是 end-to-end 软件 audit。

冻结判断：182 行稿的新算法覆盖 504e 的完整输入量词与 19/10 输出合同，无 standing fatal。与原 log/FW 作者路线相比，它直接保持实际 I，且全程有理、不需 LP/FW；两者数学支持同一存在性 Exact，不能合并软件身份。本票不扩大到 multi-state outers、重合 homes、nonUD extras、任意普通 UM，也不替未读来源、外审或全球新颖性签字。UM-TARGET-v1 仍 OPEN。
