# Tagged affine LINE均匀单边际：canonical完整范围实读审查 v1

审查者：rank_deficiency_fee，2026-10-18。实际全文读取最终canonical的header与§1–4，另冻本记录；未改repo/Work/Git或原raw字节。

## 1. 精确读取对象与先行链

正式ID：`UM-TAGGED-AFFINE-LINE-BALANCED-MARGINAL-TINY-VALUE-v1`。

本次实际全文读取：

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/tagged_affine_line_uniform_marginal_gap.md`

wholeSHA256：

`b81d3f53d711d30ac83f5ba94f12a9a14e7ffc8242cd176373d05bf3c457c501`。

认证该准确字节版本的header和§1–4全部数学/actual/计数及scope。不认证新CONFIG结论、源CSP最大满足比例、pairwise-independent hard image或计算困难性。

冻结链已重新核hash、未变：

* Exact：`tagged_affine_line_balanced_marginal_tiny_value_exact_v1.md`，`b081198ffd09ee9e8549c75d4aa2c9d1cef0648a445b45cc6b00f9eb71bb2c50`。
* 作者Proof：`tagged_affine_line_balanced_marginal_tiny_value_proof_v1.md`，`c502f53e78440eb2e98813a428d57416de1c9e025808df82d838b5ec618dc34a`。
* 独立Exact-first：`tagged_affine_line_balanced_marginal_rank_exact_first_review_v1.md`，`0d8a1657c494f8bffbb8612ba01f7694fdc5936568c8bd117ef45913acba84bc`。
* 作者Proof读后：`tagged_affine_line_balanced_marginal_rank_author_read_after_v1.md`，`df1723d41b2feb8a0c795fdf0575e363130b541f4c6cb7f5d98dc1e1f7f8079b`。

真实顺序：rank仅据指定Exact独立重构先冻，root实际通读后才解封作者Proof；rank之后实际读Proof再另冻读后。Root先听作者口头策略，不记为盲审。Root所述R3/5/7 Fraction回算仅数字辅助，不作本一般证明的derives；本审查者没有新运行/软件声明。

## 2. Header与§1：对象、几何、边际合法性

R≥3 prime；变量u_a,v_a的tag全异，各资源块完整F_R²。Groups为main及R(R−1)helpers，每组恰Rstates；同变量跨groups的intercepts互异，u_a为0及非零j、degreeR，v_a为非零j、degreeR−1。

Main state t在全部u_a取slope t，其正权B_t属于u_t原line、R−1点各1/(R−1)。Helperℓ≠a的z=j/(a−ℓ)非零，满足ℓz+j=az，故正点确在其u_a完整line及B_a；ℓ=a时v_a label−j，fallback P_a=(v_a,1,0)确在line。每state总权1，其余完整line的zero incidences保留。

均匀选t或ℓ使各incidence label为state index的置换，故每个label边际1/R。它是明确给定local分布，不来自未知actualYES，也未冒称joint independence。整个对象是真tagged LINE，未替换成cube正支持。

完整UM每state独立private、每resource独立机器、每group selector1，各incidence只按原权private或对应resource1执行，其它∞。Zero时端合法且任务保留；每原job有finite端，机器数正，无预载/守卫/拒绝。

## 3. §2–3：全partial精确值与全actual精确最优

**全partial上界。** 对每H_(a,j)，ℓ≠a遍历B_a任意点，ℓ=a选P_a。任何minquality>0迫每helper领取其selected唯一正unit点。若main选任意state t，blockt的R−1helpers从B_t∪{P_t}取R−1不同点，最多一个fallback，因此至少R−2枚B_t已占，main至多取得1枚正点、质量≤1/(R−1)。Min0也满足上界。没有预绑helper，也没有限定非main blocks的自由选态。

**显式达界。** Main任意t领取(u_t,1,t)；H_(t,1)fallback，其余H_(a,j)选ℓ=a−1领取(u_a,j,aj)。每个非main block匹配其完整B_a，main block除z1外全部B_t由其它helpers占，fallback在独立v_t tag。全部helpers得1，main得1/(R−1)，真正pairwise-disjoint。R3可直接沿同一公式，不以有限数值枚举代替证明。

**全部原job上界。** Selectors按选态，仅导出所领正点原incidences，所有其它jobs（所有unselected states、所有zero jobs）留自身private。Selectedmain负载2−1/(R−1)，selectedhelpers1，unselectedprivate总1，资源≤1。每原job一次、每机同一assignment回算，构造未丢任务。

**任意完整actual下界。** C≥2自动满足；C<2时每helper selected正job因selector1而必外送，unit resources至多一job。Main实际state t的blockhelpers占至少R−2枚B_t，故main最多外送1件positive job、selected private保留至少(R−2)/(R−1)正工作，加selector给C≥2−1/(R−1)。Unselected额外exports只占资源，zero exports不减main正质量。因此上下界覆盖任意完整实际schedule，精确OPT成立。

## 4. §4：padding、counts、位长与pairwise边界

Parts以F_R编号，u_a属a、v_a属a+1。每helper在其它R−2parts补独有fresh变量/intercept0/labelℓ/整line权0；每group变共同arityR且每part一变量。新degree1、边际仍均匀、state总权不变。

Partial allocation忽略新零点双向保质量；旧actual扩展新zero jobs留private0，新actual删除新jobs/资源投影不增负载且旧资格未变。因此V与actualOPT精确不变。不是从原输入删除zero jobs后冒充全任务调度。

令g=1+R(R−1)、S=Rg。Base变量2R、resources2R³，main incidencesR³加helpers2R³(R−1)，I=R³(2R−1)；machinesS+2R³、jobsg+I、finiteS+2I。Padding变量V'=2R+R(R−1)(R−2)，resourcesV'R²，I'=R³g；machinesS+V'R²、jobsg+I'、finiteS+2I'，dense为相应乘积。全部与raw Exact及独立计数相同。

时间仅0、1/(R−1)、1及未述∞，位长O(logR)；field运算、显式支持/资格生成、达界allocation/全部jobassignment与全机负载回算按显式polyR规模。不称仅binaryR时poly(logR)输出，不用optimum oracle。R3给V1/2、OPT3/2；R2不在正式域。

Main任两旧labels恒相同，helpers两旧labels恒相差常数，joint支持R对而非均匀independence的R²对；padding同依赖ℓ不改变。这准确区分单边际与pairwise independence，未给Chan/LST code-coset hard image结论。

## 5. 最终范围与认证

在wholeSHA `b81d3f53d711d30ac83f5ba94f12a9a14e7ffc8242cd176373d05bf3c457c501`下，canonical header与§1–4完整自足，和冻结Exact/Proof、先行独立重构及作者读后一致；未发现standing fatal objection。

精确认证的是：真tagged affine LINE、各incidence uniform单标签边际、state相关非负norm1权仍能使实际V=1/(R−1)趋0、完整actualOPT趋2；共同arity/R-partite零权padding保这些值。没有新CONFIG值或gap认证，没有源CSP value/YES-NO困难性声明，没有把趋二实例当近二计算困难性。额外pairwise-independent关系、真实hard image及全局source decoder仍未解。

无新软件/有限实验/外审/全球新颖性认证，原raw保持不变，UM-TARGET-v1仍OPEN。
