# 共享外端 small-query / return-pool：作者 Proof v1

对应先冻Exact：`shared_outside_small_query_return_pool_exact_v1.md`，SHA256 `37304837169ba1e11595c9681528dfe21efe2ccf8a04e6bafc73b7c2b8cf2e4e`。

作者：rank_deficiency_fee，2026-10-18。Exact先交root供独立审查，本Proof另冻先仅交root，不直接发给reviewer。只写clone外scratch，未改repo/Work/Git。

## 1. 原矩阵与pattern

k≥2，a_i>0有理且Σ_i a_i≤1。内部H及P₁,…,P_(k−1)，真实outside E₁,…,E_k，全部互异；四类标签不混同。原jobs恰q₁,…,q_k,b₁,…,b_k。q_i仅H:a_i/E_i:1；b_i仅所有P_r:1/E_i:1；其余∞。没有aux、预载或复制jobs。

给S,T⊆[k]，pattern要求q_i在H当且仅当i∈S，b_i在E_i当且仅当i∈T。其余q_i在自己的E_i，其余b_i可任意分配到P。P上的共居是普通UM可选安排，绝不先当硬容量1。

每个b的全部有限端均为1，因此任意完整实际调度峰≥1。H上任何subset的q负载不超过Σa_i≤1。

## 2. Good patterns 的精确OPT1与完整构造

假设∅≠T⊆S。把q_S全部放H，q_[k]\S各放自己的E_i；b_T各放自己的E_i。因T⊆S，E_i不会同时收到q_i与b_i，所以每个E_i至多一件unit。

剩余k−|T|件b需在P执行，因T非空，k−|T|≤k−1。按索引把它们一一注入前k−|T|台不同P机器，各time1。H负载Σ_(i∈S)a_i≤1，全部P/E负载≤1。每件q和b原job都恰一次，全部资格合法，实际峰≤1；由b-unit下界，精确OPT(S,T)=1。

此只证明good pattern存在峰1最优安排，并非其任意P分配都峰1。若将多件b故意放同一P，完全可能得到峰2或更大。最优值的陈述不抹去这些非最优实际调度。

## 3. 所有bad patterns 的实际下界2

若T=∅，全部k件原b必须在k−1台P上执行。P资格time均1；鸽巢保证至少一台接两件，实际负载≥2。此覆盖S任意，包括inactive S=T=∅；没有把超出slots的b当“无资格”删除。

若T不是S的子集，取i∈T\S。q_i因i∉S实际在E_i，b_i因i∈T也实际在同一E_i，两个不同原jobs的真实负载合计2。此下界不依赖P上如何选择。

Bad patterns恰为以上两条件的并。因此任何bad pattern的每一完整实际调度都峰≥2，覆盖任意multiquery/multireturn/partial子集，不只列出的singleton cross。

## 4. Bad patterns 的峰2完整上界

对任意S,T，先按pattern放全部q：q_S在H，其余在各自E_i；再把b_T放自己的E_i。每个E_i最多q_i与b_i两件unit，负载≤2。H负载≤1。

令m=k−|T|≤k为剩余b数。若m≤k−1，将它们放不同P；若m=k（即T空），先k−1件一一放不同P，最后一件再放P₁。因k≥2，P₁存在，每台P至多两件unit。由此所有原jobs都恰一次，真实峰≤2。

结合第3节，在每个bad pattern中精确OPT(S,T)=2。没有不合法pattern；即便b数超过k−1，也可通过真实P共居在峰2完成。

## 5. Weak低负载的原样解码与strict区别

取任意完整actual σ，C(σ)<2，定义其真实S、T。若T空或T不含于S，第3节给C≥2矛盾。因此必∅≠T⊆S。

此外，所有P/E上仅有unit原jobs，在C<2时每台至多一件，所以这些机负载≤1；H即使同时接多件q，负载仍≤Σa_i≤1。因此**这份原σ本身**已经峰≤1，无需先重新优化P或归一化。它不意味着第2节good pattern中的任意实际P安排都峰≤1：那些把多b堆同一P的安排本来就不属于C<2前提。

任意1≤B<2的weak输出都被以上论证覆盖。反向good pattern的strict构造峰1≤B，因此全部weak可行patterns恰为∅≠T⊆S。具体返回b_i在E_i，就必有同索引q_i在H；T非空保证至少一枚返回，但S\T允许非空，不能错误加强为S=T或恰一query/return。

Aligned_i对应S=T={i}，故OPT1；inactive对应S=T空，OPT2；cross(j,i)对应S={j},T={i}且i≠j，OPT2。给δ∈(0,1)、B=2−δ无需改矩阵，结论仍成立。

## 6. 构造、位长与范围

上述好/坏pattern安排只扫描2k件原jobs；不枚举全部S,T。读取实际σ即可按q/b目的地得S,T，再逐机按有理原时间回算。给good S,T时的峰1构造无需任何未知source/optimum witness。

机器2k、jobs2k，q资格总2k，b资格总k·k，finite条目k²+2k；dense4k²项。整数k是显式列出的任务数，a_i为二进制有理数，和及负载的精确计算位长多项式。没有按分母、δ倒数或2^(2k)patterns展开。

整个孤立模块总有S=T=[k]的strict1安排：全部q共同H、全部b各自E_i。因此没有source NO。它虽含真正small query共居，外部身份containment仍仰赖q_i唯一outside E_i的完整矩阵。额外outside资格、变量环identification、shared guards、H上新增任务或其它medium机制都需要新实际证明；本Proof不免费扩域。

特别不能由此消去真实变量一致性的源义务；仅将全部q可共同停车的模块接固定nearunit/unit停车网络，属于已有uniform/home parking边界，不是新增hardness。这里仅回收共享outside下可保返回索引属于实际query集合的正接口，标准单位pool/共享端技术不冒称原创。
