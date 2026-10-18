# Tagged affine LINE balanced-marginal tiny value：作者 Proof v1

对应 Exact：`tagged_affine_line_balanced_marginal_tiny_value_exact_v1.md`，SHA256 `b081198ffd09ee9e8549c75d4aa2c9d1cef0648a445b45cc6b00f9eb71bb2c50`。作者 rainbow_gap_source，2026-10-18。本 Proof 仅交 root；独立审查者须先实际读 Exact 并冻结其独立重构，不能将先读本 Proof 的记录称作盲审。

## 1. 合法 line incidence、归一化与 uniform 边际

main 的 state t 在变量 u_t 用 slope t、intercept0，故 B_t 的每点均在所选完整 line 上。|B_t|=R−1，所列权和恰1；其余变量的整条 line 都是0权，不能从实际 P 中删掉这些任务。

helper H_{a,j} 的 ℓ≠a state 正权点取 z=j/(a−ℓ)。j≠0且a−ℓ≠0，所以 z≠0；并且

ℓz+j=ℓj/(a−ℓ)+j=aj/(a−ℓ)=az。

因此该点属于 u_a 上 slope ℓ、intercept j 的完整 line，同时属于 B_a。ℓ=a 时，v_a 的 slope 为−j、intercept j，故 (v_a,1,0) 在其 line 上。helper 每 state 只有这一枚正权且值1，因而归一化。

u_a 的 intercept 为0及所有非零j，恰为F_R各元素；v_a 为全部非零j，仍单射。变量度如 Exact。main 在每个 incidence 的标签为 t，helper 两个 incidence 的标签分别为ℓ及ℓ−a−j，均是其 state index 上的双射。因此R个 states 均匀抽取时，每个 incidence 的标签均匀；没有使用任何实际 YES witness。

固定 helper H_{a,j}，当ℓ遍历F_R\{a}，z=j/(a−ℓ)遍历F_R\{0}。所以该 helper 的正资源选择恰是 B_a 每点及额外点 P_a=(v_a,1,0)；不同 helpers 在同一个 block a 上都有这同一组正资源可选。此事实不预先绑定 helper 到某个 B_a 点。

## 2. 所有 partial allocations 的上界

考虑任意 minquality v>0 的 partial allocation；main 选择某 state t。每个 helper 的 selected state 只有一个权1点，所以正质量要求它实际领取该唯一正点。不同 helpers 的这些点必须互异。

block t 的 R−1 个 helpers 的所有可能正点都落在 B_t∪{P_t}，总共R点。它们领取R−1个互异点，故 B_t 中最多还有一个点能给 main。main state t 的全部正质量都在 B_t、每点值1/(R−1)，所以 v≤1/(R−1)。当 minquality=0 时此上界当然成立。证明量化所有 state choices 及所有 partial subsets；没有假定 helper 使用某个特定 mode。

## 3. 达界的完整 partial allocation

任选 main state t，例如 t=0，让 main 领取 (u_t,1,t)。对于 block t，让 H_{t,1} 选 ℓ=t 并领取 P_t；其余 H_{t,j}（j≠0,1）选 ℓ=t−1，领取 (u_t,j,tj)。这些点在 B_t 中 z=j，避开 main 的 z=1 点，且互异。

对于每个 block a≠t，所有 H_{a,j} 选 ℓ=a−1，领取 (u_a,j,aj)。它们在各自 B_a 中恰好构成全部 R−1 点的一个匹配。不同 blocks 的 tagged variables 不同，不会跨 block 重名。每个 helper 因而质量1，main 质量1/(R−1)，证得 V 恰等于所列值。R=3时上述集合仍合法，不涉及空分母；例如 selected block 的剩余 helper j=2 照常处理。

## 4. 完整 UM 的实际上界及下界

从上述 allocation 构造完整实际 schedule：每组 selector 放在其 selected state root；所选 state 的上述正点 incidence jobs 导出到对应 resource machine；其余每一枚 incidence job 都留其自己的 private root，包括全部未选 states 和全部0权 jobs。

resource machine 至多承受一枚unit job。每个未选 state 的 private row 总和1；每个 selected helper 的唯一正 job 已导出，其 private root 只剩 unit selector 和0权 jobs，负载1。selected main root 留R−2枚权1/(R−1)的正 jobs，加unit selector，负载2−1/(R−1)。故全部原任务实际峰值达到该数。

反向看任意完整实际 schedule。若其峰C≥2，下界已成立。若C<2，每组 selector 所在 state root 唯一确定其 selected state。在 selected helper root，unit selector 不能与其唯一 private-unit positive job 共处，因此该 positive job 必须导出。由于任何 resource-unit job 的用时为1，C<2时每台资源机至多一枚 job。未选 states 额外导出的任务只会进一步占容量，不放松这条限制。

main selector 位于 state t root。block t 的R−1个 selected helper positive jobs 必须导出到 B_t∪{P_t} 中R−1个互异资源，故 main 的B_t正 jobs 至多导出一枚。该 main root 至少承受 selector1与其余R−2枚 private jobs，所以 C≥2−1/(R−1)。完整 actual OPT 等式由此成立，没有借助删除未选 states 的松弛模型。

## 5. 共同 arity、partite padding 的精确保持

按 Exact 把u_a放part a、v_a放part a+1，每个 helper 在其余parts加独有fresh变量。a≠a+1，故原两个变量的parts不同；main每part一个u_a。新完整 line 的权全部0，所以每state权和仍1。新增变量只属一个helper，degree1、intercept0合法；其 slope=ℓ均匀。每个helper补至R个distinct variables且每part恰一变量。

partial allocations 可以删去或忽略新0质量资源，正质量完全不变，故 V 双向精确保留。old schedule 延伸时，把新增0权 incidence jobs 全留其 private roots，增加负载0；新增资源机空置。new schedule 投影时删除这些新增 jobs 及新增资源机，所有旧 job 的合法选项不变、负载不增。因此 actual OPT 也双向精确保留。

局部分布不变成 pairwise independent：main任意两个变量的labels恒相等；helper两个旧变量labels恒相差−a−j。两坐标联合分布只支持R对，而均匀pairwise independent应支持R²对。padding增加的labels也确定于ℓ，不能改变此失败。

## 6. 显式规模与结论范围

main有Rstates，每state有R条line、每条R点，故main完整incidences R³。R(R−1)个helpers各有Rstates、每state两条R点line，合计2R³(R−1)；总I=R³(2R−1)。总state数Rn，变量2R、资源2R³，所以Exact机器/jobs计数成立。

padding每helper添R−2个fresh变量，总变量2R+R(R−1)(R−2)；全部n groups共同arityR、各Rstates、每变量R点，故总incidences nR³。仅用有限域加乘除及有理1/(R−1)；列出资源、incidences、全部finite资格以及可选dense矩阵均按R多项式。达界allocation由§3的显式公式在同样规模内给出，schedule延伸逐任务执行；没有数值指数展开或优化oracle。

因此这是真 tagged affine-line 表示中的、单变量 uniform marginals 仍不能给全实际常数值的反例。它使用 arbitrary state-dependent weights，包含大量必须保留的0权任务，且main与helpers的局部关系都非pairwise independent；它不属于已认证的Chan pairwise-independent code-coset source image。本证明没有任何NP-hardness或真实YES/NO归约结论，也没有从局部CONFIG/FSLP证书冒称actual解。
