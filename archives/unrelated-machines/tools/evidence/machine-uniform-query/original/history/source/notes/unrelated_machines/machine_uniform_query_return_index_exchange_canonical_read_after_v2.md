# 逐机统一 query/return 索引交换：canonical 完整 v2 实际读后

审查者：rank_deficiency_fee，2026-10-18。实际全文读取正式 canonical 后另冻本记录；两版 Exact、两份独立记录及作者 Proof 读后记录原字节不改。未修改仓库、Work 或 Git。

## 1. 读取对象、SHA 与正式范围

实际全文读取：

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/machine_uniform_query_return_index_exchange.md`

whole-file SHA256：

`b930c8d0e8f2607495eb4addb94c071c60a2edfa85669c36847d5f77599feb5a`。

本次正式认证该完整字节版本 §1–5 的 v2 数学与构造范围，ID为 `UM-MACHINE-UNIFORM-QUERY-RETURN-INDEX-EXCHANGE-v2`。v1只作为strict模式matching化约的历史关系；不认证两版矩阵逐项包含，也不虚构单独v1作者Proof。

对应冻结链重新核hash：

* v2 Exact：`machine_uniform_query_return_index_exchange_exact_v2.md`，`f80c3b9cb7a8b0d3b3b8b0d553426659a036543a1fe9640fbb79a5d3502e20bf`。
* v2作者Proof：`machine_uniform_query_return_index_exchange_proof_v2.md`，`991b06066d8f5db814e18604e490adb9718588fc01685653fa88ad58e5e2a7c7`。
* v2独立Exact-first：`machine_uniform_query_return_index_exchange_rank_exact_first_review_v2.md`，`ed73bfdb5a07965e8d8eedaeaf4c78342a7ce880198a61890527993b92751e17`。
* v2作者Proof实际读后：`machine_uniform_query_return_index_exchange_author_proof_read_after_v2.md`，`4846c82a40562fd91e68c193351ca52dfff89f6645c36b2d9e5df7aa92dd135e`。
* v1独立Exact-first：`single_capacity_query_return_index_exchange_rank_exact_first_review_v1.md`，`f808ca79a664a34ee298453c695dde96c868d8a7dfa9a471f3c36b3cf771e6eb`。

## 2. 全文数学与实际输出核查

**对象与量词。** N=|A|+2k、k≥2，所有原任务身份互异；A在所有模式中固定必做。每机全部finite时间相同=s_h≥0，跨机任意，有T>0，无隐含预载。允许任意资格、任意aux、多余或空闲机器、零容量和空H。任一A无资格时aligned前件失败，算法只报告不可行，不假造见证。

**精确容量。** s_h>0取min(N,⌊T/s_h⌋)，s_h=0取N；s_h>T取0。因为每机负载精确为件数乘s_h且总任务≤N，容量化对任意任务子集严格等价。虚拟slots不复制jobs，投影回原机给真实总负载≤T；零时间无除零。空H下aligned含至少k件boundary jobs故不可行。

**构造与全部aux。** 从aligned_i删q_i后，M保留A∪(R\{b_i})的L−1件原jobs。另aligned_j在U=A∪R∪{q_j}有L条边，故增广存在。当前仅b_i和q_j未匹配：新增前者得inactive，新增后者得mismatch(j,i)。翻转仅重排原已匹配jobs，不删除或拆分A中的任何任务。原机可尚有其它jobs，空余slot足够作终点；没有假设某原机必须完全空闲。

**inactive与双方向。** inactive在T不可行时，增广不能从b_i成功，因此给strict≤T错配。交换i,j得反方向，全部aligned可行时逐对覆盖全部k(k−1)错配。无inactive承诺的二选一算法仍有效，不保证恰一模式可行。不给见证可先容量matching判两aligned；不需隐藏源assignment。

**Matroid与rank。** 共同C收缩后b_i、b_j非loop且平行，和独立记录的两元素证明一致。Rank截断只用于保留小集合独立性的证明语言；不当作实际移除机器或新增物理限制。容量截N有独立的任务数理由，两种截断没有混用。

**Weak B。** 另给B≥T，inactive在B被禁才单调推出在T被禁；输出本来≤T，也≤B。不把仅B可行的aligned当成T见证，不将任意B调度压成T。无需B<2T。

## 3. 完整测试封装的合法性精度

Canonical现已明确：对每boundary原job添互异O_j，唯一新增finite端timeT；A无outside端。**当前件aligned可行时，每件A必已有内部finite端，而所有boundary jobs均有outside端，且2k≥4保证机器数正，因此该封装是合法完整ordinary UM输入。** 输出模式内全部A与所列boundary jobs在H恰一次，其余boundary jobs各在自己的O_j，所有N件原jobs都实际执行一次、全机峰≤T。

若某A根本无内部finite端，局部关系仍可用来报告所有aligned不可行，但其带无资格job的封装不能被称为合法UM目标。此前历史记录中笼统的“封装合法”措辞，应依本页明示的前件可行条件理解；此精度修正不影响任何matching交换或实际输出，因为那些输出始终以两份可行aligned见证为前提。

模式X仍是原job目的地的指定/投影，outside测试机没有物理强制它；inactive X=R也与所有boundary outside的X=∅不同。若真实归约共享outside端，切换模式可能增加那些外部机器的负载；本页没有给全局回填，不推出任意fullformula strict可行，也不替代源NO decoder。

## 4. 历史v1、位长与准确扣除

v1允许同机异权、finite时间在(B/2,T]、T≤B<2T，故其strict/weak内部都每机至多一件。将finite端统一为T得到相同strict可行模式的matching对象；在v2构造后恢复原finite时间≤T才得v1实际输出。这不是原矩阵逐项包含，canonical对此已准确表述。作者Proof对应§4直接处理该关系，没有另一个v1作者Proof文件。

容量/slots≤|H|N，资格展开≤原finite资格数乘N；dense全部项计入编码长。有理比较、取floor、截N、匹配/增广、投影原机及按件数乘s_h回算，均总位多项式，不按未截断T/s_h或分母数值展开。零容量/零时间/无资格辅助均不产生非法算术或虚假合法目标。

容量matching、增广与transversal matroid交换是标准技巧；这里仅登记具体原query/return身份合同及逐机统一时间范围，不认证全球新颖性、新matching理论或所有身份复制器不可能。没有新增软件、有限枚举、复杂性源或一般UM后端。

## 5. 正式结论

在whole-file SHA `b930c8d0e8f2607495eb4addb94c071c60a2edfa85669c36847d5f77599feb5a`下，canonical完整v2与冻结Exact/Proof、先行独立重构和作者读后一致，封装合法性前提已准确补清；本次未发现standing fatal objection。

认证限逐机统一非负时间、固定辅助集的局部容量matching接口。未覆盖同机异权共居、模式相关辅助、预载、bundle/多尺度或内部外部不可分负载；不提供这些额外条件的充分性、全局NO decoder、near2源或主目标反面。UM-TARGET-v1仍OPEN。
