# first-saturation frontier 的独立审查

2026-10-23，menus。收到父代理的摘要陈述后，先写本节；此时尚未打开 `tree_credit/first_saturation_frontier.md` 的正文或证明。下面第一节只重构摘要可以合法推出的抽象流量结论，未看正文的假设不得自行补作已证。

## 1. 只见陈述时的独立重构

摘要给定：合法 SOURCE-NET γ/f 与非负 residual ρ；每 role 的 source 先全部支付 Ksrc_i≤η_i。incoming 的完整支付需求为 F_i，按统一比例

    θ_i=min{1,(η_i−Ksrc_i)/F_i}

接纳，未接纳部分在第一次出现此种拒绝时停止；每 state 原流转移因子为 1/c，支付权 w=A/D。宣称 Aabs+Bstop=R−G，K≤W，E=K−Aabs≥0，U=W−K≥0，half等价Bstop≤E+U，并有饱和 role 集 J 的首次命中界。

在尚未知 γ/f、D、吸收质量定义时，我可以独立验证的结构如下：

1. 若 η_i≥0，Ksrc_i≤η_i 且 F_i≥0，则 F_i>0 时 θ_i∈[0,1]，incoming 支付 θ_iF_i≤η_i−Ksrc_i。若 F_i=0，必须单独定义 θ_i=1（或另给不影响流的约定）；不可直接保留 0/0。于是 K_i=Ksrc_i+θ_iF_i≤η_i，求和给 K≤Ση_i=W。这要求 F_i 是同一 role **所有相关状态**的合并需求，不能逐状态各复用一次剩余容量。
2. ρ 的非负性和转移的次随机性使“接纳—吸收—首次停止”可按非负质量定义。若初始总净质量确为 R−G，且所有未吸收质量最终停止（例如有限有向无环图和所有末状态全部吸收），那么质量守恒给 Aabs+Bstop=R−G。摘要本身尚未说明末端无逃逸，需正文查。
3. 由前两项不能单独推出 Aabs≤K。必须存在逐状态的合法支付关系，或 SOURCE-NET 的汇总恒等式，保证已吸收信用不大于同一套 γ/f/IC 付款。支付 w=A/D 需要 A≥0,D>0（A=0,D=0 时须约定 w=0 并检查没有正吸收遗漏）。这是最重要的待查点。
4. 若确有 Aabs+B=R−G、E=K−Aabs、U=W−K，则 E+U=W−Aabs，故 B≤E+U 等价 R−G≤W。只有再有 R−G=OPT_m−W（或本稿明确的同等目标余额）才等价 half；不能仅从上述流等式宣称与 half 等价。
5. 首次停止质量仅会发生在 θ_i<1 的饱和 role。给定一个与原非负流一致的路径分解，先忽略全部容量拒绝得到 raw 路径；加上首次拒绝规则以后，每条停止路径应当映射到其 raw 路径首次进入 J 的事件，停止质量不超过相应 raw 首次命中质量。source 若在 J 中仍被无条件接纳，则“首次命中”必须明确是**首次 incoming 命中**还是包括初始 source；前者可能是锐的，后者仍可作较松上界，但不能混用等号。

这些是从陈述独立得到的预算与量词检查点，尚不构成对父稿具体定义的通过结论。

## 2. 阅读正文后的逐项审查

在先写完第1节后，读取了本 actor 的 `tree_credit/first_saturation_frontier.md` 全文，再按其确切引用读取 R-cd789 的 `round3/GENERAL_PROOF_WORKING.md` 最后一节 SOURCE-NET 与 `round3/mixed/capture_hitting_capacity.md`。没有读取作者的程序或有限实验，也没有以既有独审摘要代替本次代数检查。此处独立性准确范围为：构造与守恒先由摘要重构，SOURCE-NET 被引用来源的证明我是在读本稿后核对其使用条件，不能称重新盲证了 SOURCE-NET 的全部 maxflow 资产。

### 2.1 SOURCE-NET 接口及钱包

实际 C=I∪G、最优 O=I∪R，故 OPT≥W 给 |R|≥|G|。来源给同一组 owner、γ/f，ρ_x=1−γ_x∈[0,1]、Σρ=|R|−|G|，η_i=u_i(I)+γ_i≥0 且 Ση_i=|I|+|G|=W。

本稿保留这一份对象，没有按未来 query 重新选取消客户。source 费用 Ksrc_i 的来源论证也接得上：若 g_i=u_i(G)≤|Q_i∩R|，预先本地取消 δ_i=g_i 使 γ_i≥g_i，η_i≥u_i；source query 的系数≤1，故 Ksrc_i≤u_i≤η_i。若 g_i>|Q_i∩R|，本owner的全部R取消，Ksrc_i=0。每owner只用一个原合法比较主题 T_i，故这里不发生多个 source query 各领一次 u_i。

### 2.2 零分母、统一接纳与整条 IC

对一个正R质量状态，query a 包含该客户 x，所以其完整原收益 D_i(a)≥1/m>0。D_i(a)=0 时没有此种正质量。u_i=0 由原SPE迫使全部 D_i(a)=0，所以该role无正R源或捕获流，稿中零约定合法。

按role递增处理使 F_i 仅取决于已处理角色的流；预留的 source 不是待决定变量。F_i=0 时 θ_i=1 明确排除 0/0；F_i>0 时 e_i=η_i−Ksrc_i≥0，θ_i∈[0,1]。单一 θ_i 缩放该role全部 incoming，收费正好为 Ksrc_i+θ_iF_i≤η_i；若 θ_i<1 则取等。

同一 (i,a) 的各客户吸收、源与到达质量都先求和，再使用唯一非负系数 w=(Asrc+θ_iAin)/D_i(a)。这是完整原真实IC d_i(a)≤u_i 的合法常数倍。路径数或客户数不额外复制 IC，多个 arriving branches 合流也不复制该role的钱包。

### 2.3 守恒与 A≤K

对R客户，实际前缀不覆盖x，query终局的覆盖者恰为当前角色加更深 coverers，故 c=1+更深人数；当前吸收1/c、向每个更深coverer各送1/c，总概率为1。role严格递增，末角色的 c=1，故无逃逸、无无限路径。

source初始质量ρ、每次到达先停止或接纳、接纳后再作上述守恒分流。因此 Aabs+Bstop=Σρ=|R|−|G|。这里 stopped 流不再展开，每个粒子首次停止一次，合流不会改变这个事实。

把所有已接纳query的吸收记为 A_s。其 coefficient w_s=A_s/D_s，原IC给 A_s=w_sD_s≤w_su_i。对有限状态求和正好 Aabs≤K，不能再按客户重复求新的IC。结合 K≤Ση=W，E=K−Aabs≥0、U=W−K≥0。于是

    B−E−U=(|R|−|G|)−W=OPT_m−2W.

所以 B≤E+U 对这份构造**恰等价** half；不是已经取得的额外正预算。正文准确保留其未证身份。

### 2.4 J 与首次命中

θ_i 由确定总流算出，整个构造完成后 J={i:θ_i<1} 是固定role集合。忽略拒绝得到同一原capture链，可耦合每个source粒子。停止只能发生在source之后的J，故对x应使用目标集 J∩{s(x)+1,…,m}。其大小正是稿中 k_x，即使 source role本身也在J，也不会被错误当作停止机会。

引用HIT对所有固定role集合成立，且不依赖query标签或匿名平局。直接复原其逆向界：若后面最多还有k个目标role，当前直接后继有t个目标及n个非目标，则命中概率≤[t+n k/(k+1)]/(1+t+n)≤k/(k+1)，其中差为(k−t)/[(k+1)(1+t+n)]≥0。故 STOP-HIT 合法，单个非source角色的总停止质量≤ρ_x/2也合法。多行不可相加独领ρ/2，正文没有这样做。

### 2.5 RANDOM-CUT

每个实现保留非J的薄owner Q_i、以合法query替换J。把未替槽Q_i扩为合法T_i得到一个恰m槽的目录组合，原薄覆盖是其子集，所以覆盖≤OPT。owner不在J的O客户不会丢；owner在J的客户恰在全部随机query漏掉x时丢。O外客户恰在至少一个query覆盖时新增。比较新增与漏失，再取独立期待，逐客户得到稿中乘积式。

这个论证不对Q_i调用SPE，也没有假定Q_i是合法动作。任意联合action law把乘积改为联合未覆盖事件即可。J为空、重复主题、空owner与零客户都无例外。

### 2.6 COV-STOP 的一个记号修正

§1仅对 x∈R∩a 定义 r_(i,a)(x)=1/(1+更深coverers)。§5的χ随后在全部 x∈a 上使用r，且用 D_i^(N\R)。为了这两式形式自足，需要补一句：

    对全部x∈a定义r_(i,a)(x)=1/c_x(Z_i(a))；
    对R客户实际前缀零，故才简化为1/(1+更深coverers)。

这应视作局部定义缺口；若非R也误用1+更深，则Σχ=0确实可能错误，因为旧覆盖者分母被漏掉。按作者意图使用完整原收益份额后，代数严格成立：

    Σ_xχ=Astop−λD=0,
    Σ_Rχ=Astop−λD_R=λD_(N\R)≥0.

对i∈J实际上必有L_i>0：θ_i<1蕴涵F_i>0，而该role u_i>0，至少一个正到达吸收被拒绝，所以某个λ>0。故在停止role上p_i=λ/L_i不会遇到零归一化。

正文正确拒绝从COV-STOP推出逐客户 B_i(x)≤L_ip_i(x)。Σ_Rχ≥0仅给加权聚合方向，并非无权逐客户支配；把max_x b换作IC系数会改变已支付的财经容量。

## 3. 结论与准确范围

在上述 r 的全客户定义补齐后，§§1–4的一般构造、守恒、整条IC收费、首次HIT和随机hybrid cut，以及§5所写COV-STOP，未发现数学异议。它们严格保留同一owner、同一γ/f、原实际前缀完整query、任意历史平局与source/incoming的一份钱包。

本次没有证明前沿付款 B≤E+U。STOP-HIT与RANDOM-CUT之间仍缺同一组action laws和真实停止质量/owner库存的耦合。确认辅助流量的合法性不能提升Q-CAG-HALF的状态，也不能把 B≤E+U 这一精确等价重写计作已证一般福利进展。
