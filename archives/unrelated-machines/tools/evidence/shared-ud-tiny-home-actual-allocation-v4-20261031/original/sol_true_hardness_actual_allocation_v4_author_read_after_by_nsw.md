# v4 actual-allocation 势算法：新作者稿的全文读后独立攻击

审者：`/root/sol_nsw_independent_attack`，2026-10-18。结论：对本页指定 typed v4 域，所读新算法可重构，未发现 fatal。它维护实际 integral helper B-bundles，使用单 helper 更新和直接可算势，不需要前一算法的 fractional optimum / FW。此票是实际全文读后的算法攻击，不是我再次做 Exact-only blind，也不是软件或全球新颖性认证。

## 1. 实际阅读、身份和顺序

唯一新增本地源为 `/workspace/scratch/038d9dcc4cac/sol_true_hardness_shared_ud_tiny_home_k2_v4_exact_first_attack.md`，实际 SHA-256 `69036ac605760a193093869fc2af26b6fed35d76ed1c49f776185d17e9089f10`，12401 bytes、149 lines。分 1–85、86–149 两块实际阅读全文，无截断，覆盖其阅读账、§2–8 的全部算法及证明、最终范围。

本稿之前，我已读旧 k⁴ Exact `80fd4ff5…`、冻先行独立 `ee7f19b…`、在父 agent 实读后读作者 Proof `409ce884…` 并冻 read-after `e4ad54e…`，再知情实读新 k²/k1 v4b 作者追加稿 `1e371087…` 并冻 `d2621c15…`。父 agent 实际读完 d262 后，才给我本次新算法稿。前三票不改字节，不把它们当作本新算法的证明。

本次源自述其在只读新/旧 Exact 后独立重构；我的票仅核它给出的新算法及数学，不重新认证其历史全部读取行为。送审信息已经说明这是新 actual-allocation 势路线，因此我不能自称对该路线 blind。没有读 O1k 草稿、其他新 Exact/Proof/reviews、代码、运行产物或链接；未向其他 fresh 审者传机制。没有 Git、repo、Work 或 token 操作。

## 2. 本新算法的精确对象与两个输出分支

实际审查域与已读 v4b 相同：k≥1 single-state outers、Σ_{j∈J_i}w_j=1 的全局互异正 homes，每 home 唯一 unit-own helper，任意 normalized B-only fallback states，B-only exact-threshold-UD leaves（ε=15/16）；k=1 无额外 ν 上界，k≥2 有 ν=max w_j≤1/(16384k²)。全部原 zeros、indexed duplicate states、inactive jobs 和 unused resources 仍保留。

令真实 normalized-menu max-min value 为 V，实际完整普通矩阵满足 OPT=2−V∈[1,2]。正向仅导出实际 selected-state bundle 的正 incidence jobs，其他所有 incidence jobs 留各自 private，selector 放 selected private；反向 C<2 使每 resource 的 unit jobs 独占，selector 所在 state 的导出价值≥2−C。C≥2 给下界 C≥2−V 平凡，最优等式由正向合并得到。未对输入 ordinary schedules 追加 canonicalization 假设。

新算法的实际 comparator 阈值是 r=18/19，不是旧作者算法的 ε。取 a=r²=324/361、目标 t=1/10、当前 welfare 成功阈值 ℓ=19/100。算法有两种合法结论：构造全部 groups 值≥t，给 C≤19/10；或者证明 V≤r，给全部 jobs 基线 C≤2。后一分支包含等号，因为

    (19/10)(2−18/19)=2。

所以失败结论不必是严格 V<r；没有错误沿用旧“严格 OPT>17/16”才能给比值的逻辑。r>ε；无全叶匹配时 V<ε<r，自然也是基线分支。

## 3. Matroid 状态和每个候选真的可计算

全叶匹配存在时，resource-side transversal matroid A 的 rank 为叶数 q，M=A*；R independent in M iff B\R 可匹配全部叶，rank 公式 r_M(R)=|R|+r_A(B\R)−q 正确。空叶对应 free matroid，rank0/loops/unused resources 仍可处理。

所有原 positive fallback incidence (j,s,u) 是 M 的带标签平行 copies。oracle 先检查原 u 不重复，再在 B\所用资源上做一次完整叶 matching；这实现真正 matroid independence，不是未知 states 的优化 oracle。

状态是每个有 fallback helper 的一个原 state s_j，以及独立的实际 incidence 集 I，每个 I_j 只用 s_j。无 fallback helper 记空，永不拥有 B 资源。当前 v_j≤1、L_i=Σw_jv_j≤1。它只是实际 helper B-bundles，不声称迭代中已给 outers 和全部 leaves 完整正质量输出，更没有逐 job transient-load 保证。

对固定当前正权 h_i 和候选 helper j/state s，只在 I_{−j} 加该 state 全部正 copies 的 ground 上做 weighted matroid greedy。其他 helpers 不可能得到新 incidence，只能保留或丢失旧项；j 可以整包换 state。ground、排序和匹配查询全显式 polynomial。旧 state 的候选包含原 I，所以 δ_j=max_s[W(I'_{j,s})−W(I)]≥0；无 fallback j 的 δ_j=0，且参考也只能为空。每轮对所有 state 各取一个固定 tie 规则的线性最优候选即可，无需枚举该 state 的全部 optimal sets。

## 4. “2×当前福利”比较式的从零重构

定义完整标签 ground 上 weighted matroid rank F(S)=max_{K⊆S independent}W(K)。正 h,w,p 使 F 单调次模；按降序权 threshold ranks 的非负组合直接证明，不要求 current I 是整个 ground 的线性最优点，也不用最优 fractional basis coupling。

I 本身 independent，故 F(I)=W(I)。任意参考 I* 每 helper 至多用一个 state，其 I_j* 可以为空。把 I_j 加回 ground 能增加的 weighted rank 至多 W(I_j)，所以

    F(I∪I_j*)≤F(I_{−j}∪I_j*)+W(I_j)
              ≤W(I)+δ_j+W(I_j)。

第二步对非空 I_j*，枚举的该原 state 的全部 positive copies 包含它；空 I_j* 时直接用 F(I_{−j})≤W(I) 和 δ_j≥0；无 fallback helper 同样成立。这也处理当前/参考 state 不同、相同或有标签交集的情形。

单调与次模性再给 W(I*)=F(I*)≤F(I∪I*)≤F(I)+Σ_j[F(I∪I_j*)−F(I)]。合上式及 Σ_jW(I_j)=W(I)，得到

    Σ_i h_iL_i* ≤2Σ_i h_iL_i+Σ_jδ_j。                  (R)

因此确实只支付两份当前福利，没有把删除当前 I_j 的损失漏掉，也没有免费假设每个 outer 各自有可拼接的参考解。辅助 F 可以含同 helper 多 states，仅作 rank 上界，当前/参考输出仍各自只有一个 state。

## 5. 同一真实 allocation 给共同参考，而非输入 oracle

假设仅用于反证的真实 V>r。取达到 V 的一次全部 groups 实际分配；outer i 拿到的正 home 权≥V。任何被拿 home 的 helper 丢失 unit-own 正资源，故其达到 V 的 state 必是原 B-fallback，且其实际 B bundle 值≥V。仅保留这些 helper bundles，其他 helpers 空，给每个 i 的 L_i*≥V²>a。

叶同时值≥V>ε，因此各叶原 bundle 有一枚 H_l 代表，且这些代表彼此不同、与保留的 helper B-bundles 不交。于是全部参考 I* 的 union 在 M independent。这是同一个实际 allocation 的资源解，没有按 i 分开重用 B，也没有让算法获得 V 或其见证。positive-only ground 可删去参考中所有零贡献项而保持价值和独立性。

## 6. 同 outer 损失和二次曲率付款

k≥2 取 γ=3/10、b=1/(50k)、τ=1/100，N=helpers 数，

    Φ(L)=Σ_i[−(γ−L_i)_+²+bL_i]，g_i=2(γ−L_i)_+，h_i=g_i+b。

Φ 的 gradient 为 h，全局 2-Lipschitz，故对每个真实候选变化 Δ 有 Φ(L+Δ)≥Φ(L)+h·Δ−ΣΔ_i²。这里 Φ 的值由候选的实际 I' 直接重算，没有 exact potential optimum 或 FW 近似。

独立核 same-outer 成本如下。j 属 outer i，候选新 j weighted contribution≤h_iw_j。I_{−j} 本身是 candidate ground 内可行集，所以任一个线性最优候选中，其他 helpers 的 weighted 总损失 D_loss 不超过新 j weighted contribution，尤其≤h_iw_j。其他 helpers 真只能丢旧项，不存在隐含新收益。这个事实对每一个同权最优 tie 都成立。

同 outer 的其他 helper 未加权损失≤D_loss/h_i≤w_j；j 自身新旧贡献差绝对值≤w_j，所以保守但合法的 owner bound 是 |Δ_i|≤2w_j。其他 outers 只有非正变化，其未加权总损失≤D_loss/b≤h_iw_j/b，平方和不超过总损失平方。因此

    Σ_lΔ_l²≤4w_j²+(h_i/b)²w_j²。                       (E1)

这确实包含 owner 内别的 helpers 被挤出。虽能局部写更紧界，本票只核稿中 (E1)，不悄扩大 ν 或算法域。

算法只采用真实 Φ 增加>τ/N 的候选，停止时全部所算线性最优候选的真实增益≤τ/N。对实现 δ_j 的那个 state 候选使用 (E1)，得 δ_j≤(E1)+τ/N；不用 tie 中的特殊 optimum 才成立。求和并放入无 fallback helper 的零项，Σ_{j∈J_i}w_j²≤ν，得到

    Σδ_j≤E+τ，E≤ν[4k+b^(−2)Σ_i h_i²]
                  ≤ν[5k+b^(−2)(3/5+2b)G]，G=Σg_i。

最后一步来自 Σg_i²≤(3/5)G、Σh_i²=Σg_i²+2bG+kb²。ν≤1/(16384k²)、k≥2、2b≤1/50 给

    E≤5/32768+(1550/16384)G。                          (E2)

每步新 L 都仍来自合法 normalized one-state helpers，故上述 L∈[0,1] 和 g_i∈[0,3/5] 的范围没有在更新后失效。

## 7. 矛盾常数和阈值等号

若真实 V>r，由 (R) 的共同参考，D=Σh_i(L_i*−2L_i)≤E+τ。g_i>0 时 L_i<3/10，而 b 部分只用 L_i≤1，故

    D≥(a−3/5)G−(2−a)bk
      =(537/1805)G−398/(361·50)。

若某当前 L_i<19/100，则 g_i>11/50，合 E2 需

    [537/1805−1550/16384]G
      ≤398/(361·50)+5/32768+1/100。

系数=3000229/14786560>0；在边界 G=11/50，左减右已经是 18388693/1478656000>0，故严格更大的 G 不可能。全部 exact 分数已用独立 Fraction 重算。原稿的保守结论“V>r 时终点全部 L_i≥19/100”充分，且其边界余量事实上更强；本票不因此改原算法。

最终实际测试为某 L_i<19/100 才 FAIL；Li=19/100 走成功恢复。FAIL 从上述反证推出 V≤18/19（包括 V 等号），baseline 的相对保证在等号恰为 19/10。停止条件是没有候选 Φ 增>τ/N，因此用于证明的所有候选增≤τ/N，两种严格/非严格比较方向均一致。不能把此票误改成依赖一个严格 baseline gap 的 theorem。

## 8. k=1 不受 tiny 约束

k1 使用同一实际候选集合，直接 Φ=L_1、h_1=1。每个线性最优候选的真增益就是线性增益，停止后 Σδ_j≤τ。若 V>r，(R) 直接给

    L_1≥(a−τ)/2=32039/72200>19/100。

没有 quadratic error、没有 ν 或 Σw² bound，也没有 prefix rounding。一个 w_j=1、无 fallback、零 rank 等都由该同一 algorithm/反证/基线处理；不能把 k≥2 的 g,b 公式拿来暗中给 k1 加条件。

## 9. 真分配和每枚原 ordinary job

成功时每个 L_i≥19/100，令 Good={j:v_j≥t=1/10}，Good home mass 为 W_i。因 v_j≤1、非 Good v_j<t≤t，L_i≤W_i+(1−W_i)t，故 W_i≥(19/100−1/10)/(9/10)=1/10，包括等号。Good 保留其实际 I_j fallback bundle并把 home 给 outer；非 Good 丢弃 B bundle、回原 own state拿唯一 home。所有 outers/helpers 值≥t。

Good B union 是 I 子集，matroid hereditary 给仍 independent；在其补中重新做一次全叶 matching，为每叶枚举一个在其匹配 H_l 资源上系数≥ε 的原 state。该 matching 与 Good 真 B bundles 在同一物理 B 上 disjoint。再用 homes 全局互异且 B disjoint homes，得到所有 groups 的共同实际分配。

selector 去上述原 indexed state private，只导出真实 selected-state bundle 的正 incidence jobs，全部其他原 incidence jobs 留各自原 private，包括显式 zeros、inactive 正 payload、duplicate indexed states、unused resource 上 listed jobs。每 job 恰一次、finite endpoint 原有，resource≤一 unit job、selected private≤19/10、inactive private≤1。baseline 则全部 payload 留 private、每 group 任取原 state接 selector，C≤2。无需添加辅助 ordinary machines/jobs/资格，counts 仍 S+U、G+I、S+2I。

## 10. 终止、总位复杂度和最终范围

k≥2 势 range [-9k/100,1/50]，每接受真增>1/(100N)，所以 moves<9kN+2N；k1 线性 range [0,1] 给 moves<100N。每轮候选数至多原 fallback state 数，各候选 ground≤现有 I 加其原 support，weighted greedy 次数及每次 matching 图均 polynomial。无候选可接受就停止，包括输入真实 V 低的情况，不依赖只能在 YES 实例终止。

所有 L 从当前原 incidence bitset 每次直接重算，系数 w_jp_jsu 的分母可统一到 bitlength 为输入分母位数和的一个数。h、Φ、候选 weights、阈值比较只对这些固定来源量作有限层有理乘加和平方；不把前轮复杂分母递归嵌入下轮。排序与 matching 可精确确定性做，当前 I 大小≤|B|，k,N、states、零 jobs、资源数全部显式，生成 P 及逐 job 输出也为 polynomial。没有给定点、OPT/target 见证、configuration/profile oracle、精度参数、随机时间或 generic exact SDP。

本票结论：69036ac6 全部 149 行中的新算法，按其给出的保守常数完整闭合；2-current 比较、sameouter loss、k² 曲率、k1 unrestricted、包含等号的可靠 FAIL、真实全组恢复及 alljob bitpoly 均通过。它不靠早先 smooth-optimum/FW 算法的 PASS；三个既冻记录各保原先范围。本轮仅 Fraction 常数核算，未实现或运行该算法，未认证作者其他软件/历史 sources，未读 O1k 草稿。一般 UM、多state outers、home overlap、nonUD extra groups 仍未解决，全球新颖性未认证。
