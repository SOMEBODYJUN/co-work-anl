# 逐机统一 query/return 索引交换：作者 Proof 实际读后 v2

审查者：rank_deficiency_fee，2026-10-18。先行两份独立 Exact-first 记录已由 root 实际读取，本次获准后才全文读取指定作者 Proof。此记录另冻，不改原件，不写仓库、Work 或 Git。

## 读取对象与冻结链

实际全文读取：

`/workspace/scratch/038d9dcc4cac/machine_uniform_query_return_index_exchange_proof_v2.md`

whole-file SHA256：

`991b06066d8f5db814e18604e490adb9718588fc01685653fa88ad58e5e2a7c7`。

对应 Exact：`machine_uniform_query_return_index_exchange_exact_v2.md`，SHA256 `f80c3b9cb7a8b0d3b3b8b0d553426659a036543a1fe9640fbb79a5d3502e20bf`。

先行独立记录原字节仍为：

* v2：`machine_uniform_query_return_index_exchange_rank_exact_first_review_v2.md`，SHA256 `ed73bfdb5a07965e8d8eedaeaf4c78342a7ce880198a61890527993b92751e17`。
* v1：`single_capacity_query_return_index_exchange_rank_exact_first_review_v1.md`，SHA256 `f808ca79a664a34ee298453c695dde96c868d8a7dfa9a471f3c36b3cf771e6eb`。

本次只存在并读取上述 v2 作者 Proof；没有单独 v1 作者 Proof，不虚构其路径、哈希或读取记录。v1关系由该Proof §4核对。

## 逐项比对

1. **实际容量化一致。** 作者按同一内部机所有finite端=s_h将负载写成整数件数乘s_h，取c_h=min(N,⌊T/s_h⌋)，零时间单列取N、超过T取0。这与独立重构完全相同，对任意模式精确，而不只保对齐。Slots可为证明工具；归并回原机仍满足真实总负载≤T，无任务拆分。N≥4、空H、零容量行、A本身不可匹配均正确处理。

2. **原jobs增广一致。** 作者从aligned_i删q_i，保留A∪(R\{b_i})的L−1件原jobs；在U=A∪R∪{q_j}上，另一份aligned_j见证有L条matching边，因此有增广。起点只能b_i或q_j，分别输出inactive或mismatch(j,i)。与独立记录的“先搜q_j，失败再搜b_i”是同一个增广结构；作者可一次对两未匹配起点作多源搜索。翻转保留全部已匹配原jobs，A没有被删除或匿名代替。

3. **inactive承诺与反方向一致。** 若inactive在T不可行，b_i起点的成功增广不可能存在，故构造必给strict≤T错配；交换i,j得反方向，逐对得全部错配。不要求原机满载、两见证使用同一机器集，或有某台原机完全空闲；容量剩余slot就是合法增广终点。

4. **matroid语言范围准确。** 收缩固定A并截断边界秩k只解释相同matching对象，不是物理新增约束。作者直接增广证明不依赖另行假定某个集合是base。独立记录另给共同C收缩后的两非loop平行元论证，两者结论与全部量词一致。

5. **weak B前件准确。** B≥T且inactive在B被禁，单调推出inactive在T被禁；作者输出本来就在T，因此也在B。它没有把“aligned仅在B可行”误替代T前件，也没把任意B调度压至T。这里无需B<2T。

6. **全部原任务与outside范围一致。** 作者将输出模式外的每个边界原job放互异O_j、耗时T，完整封装覆盖N件原jobs恰一次、峰≤T。该封装是合法普通UM，但模式是指定的去向投影，并非额外强制逻辑。作者明确不保证真实共享外端的负载可回填，不从局部错配推出任意fullformula strict可行。

7. **v1模式化约准确。** Proof §4正确使用v1所有finite原端在(B/2,T]且T≤B<2T，从而strict/weak内部每机至多一job；将finite端统一为T只保持模式matching可行性。得到matching后恢复v1真实端时间≤T，才给v1实际输出。v1允许同机异权，不是逐项属于v2；两域没有被混同。

8. **位复杂度与技术扣除一致。** 截N容量、二进制有理比较/取整、≤|H|N的slots、显式matching、完整原机输出均位多项式，不按未截断比值或分母复制。作者扣除标准容量matching/增广/transversal matroid交换，不称新理论、一般UM算法或源hardness；未以有限测试作证明。

## 结论

在指定Exact/Proof字节下，作者完整Proof与两份先行独立重构相合，未发现standing fatal objection。可支持登记v2逐机统一非负时间域的精确局部query/return身份交换；v1保留为历史模式特例记录。

认证仍不覆盖同机异权co-location、模式相关辅助集、未述预载、bundle/多尺度、真实内部外部负载耦合或fullformula/near2源。没有新软件、外审或全球新颖性认证。
