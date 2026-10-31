# VW2010v1 Theorem 12：来源后端预核

状态：只核已发表来源后端；新 weighted-menu 桥的 Exact 尚未收到，未读取其作者 Proof，未实现或猜测该新桥。

来源：repo 中 `history/source/literature/unrelated_machines/verschae_wiese_2010_configuration_lp_v1.pdf`，SHA-256 `2a5ec312fb443928b3801af830006b41ef94f4da7f9759bdab22b16a59a88a7a`。实际读取 PDF 页 10–11（印刷页 9–10），§5.1、Lemma 11、Theorem 12 及其证明，并渲染两页作图像核对。原系统 pdftoppm 缺 libpoppler.so.160，改用现有 fitz 成功渲染，未修改来源 PDF。

## 1. 来源精确保证

MaxMin-balancing 中，每个 item/job 至多有两个可接收其正价值的 agent/machine，各端价值允许不同。Theorem 12 给纯组合 2-approximation；对正整数阈值 T，其 oracle 或者构造每 agent 价值至少 T/2 的分配，或者证明不存在每 agent 价值至少 T 的分配。原文声称配合适当数据结构与二分可达二进制输入长度 |I| 的 O(|I|²) 时间，并引用 [23] 的实现细节。

这里的 oracle 不是精确 T-feasibility：成功仅证明存在 T/2 解，不证明 OPT≥T。后续接口不能混淆这两种语义。

## 2. forced-largest 预分配

每个 agent i 的当前双端 items 为 A_i，唯一正端 items 及已强制给 i 的 items 为 B_i。A_i 按 i 端价值降序排列，A'_i=A_i 去掉最大 item。所有同权排序可按 item index 确定性破同值。

- 若 value_i(A_i)+value_i(B_i)<T，当前全体可用价值已不足 T，拒绝。
- 若总量≥T，但 value_i(A'_i)+value_i(B_i)<T，则任何 T 解都必须把当前最大 item a_i,1 给 i。该强制是逻辑必需，不是贪心近似步骤。
- 强制后将该 item 加入 B_i，**并从两个端点的 A 列表全局删除它**；另一 agent 失去它的对应价值，可能触发不足或进一步强制。不能只在 i 端做 A→B 而让另一端仍保留同一 item。
- 每次强制删除一枚当前双端 item，故至多发生 item 数次。A_i 为空时直接按 B_i 总量检查，不能读取不存在的最大 item。

若停止且未拒绝，则每个 agent 均满足 value_i(A'_i)+value_i(B_i)≥T。原有 B_i 与 forced owner 均唯一，未强制的 item 仍有两个端点。

## 3. 两匹配 pairing 与直接迭代 BFS

对每枚剩余双端 item 建两个 occurrence 顶点，以“同 item”边相连，形成一个匹配。每 agent 的当前降序 occurrence 列表按 (1,2)、(3,4)、… 两两配对，形成另一个匹配。两类边之并最大度为 2，任何环两类边交替，长度必为偶数。

因此按固定顶点顺序用 deque 做 BFS 二染色即可，完全不需要递归。把每 item 的黑色 occurrence 对应的 agent 作为 owner，恰好分配一次；各 agent 的每个 local pair 恰获得一枚 item。

设 i 的剩余降序价值为 p1≥p2≥…≥pr。pair 分配给 i 的价值至少 p2+p4+…；由于 p2≥p3、p4≥p5 等，

    p2+p4+… ≥ (p2+p3+…+pr)/2 = value_i(A'_i)/2。

加上 B_i 后至少 value_i(A'_i)/2+value_i(B_i)≥T/2。奇数个 occurrence 时最后未配对者只可能增加价值，不破坏该下界。

## 4. 二分与总位复杂度的安全实现语义

先讨论整数价值。令 U=min_i sum_j v_i,j，OPT≤U，且 T=U+1 必被初始总量检查拒绝。把低端设为 0 并保存一份零保证完整分配，把高端设为 U+1（已知拒绝），重复测试中点：成功则保存该 T/2 解并提高低端；拒绝则降低高端。

不必额外假定 oracle 的成功/失败谓词在 OPT 上方单调：每次拒绝都有严格证书 OPT<T，所以高端始终大于 OPT。结束时高端=低端+1，且 OPT 为整数，故最终低端≥OPT；保存解价值≥低端/2≥OPT/2。若 U=0，OPT=0，直接返回合法完整分配即可。零positive-agent items 的合法收尾取决于具体输入域，待新桥 Exact 明确后再定，不在此预核中猜测。

若输入价值为二进制非负有理数，可乘共同分母 D（分母乘积或 lcm）变成整数。D 的位长不超过输入分母位长总和，缩放后整数价值和 U 的位长仍为输入总位长的多项式界。二分 O(log(U+1)) 次而非 O(U) 次；各次只做精确整数加减、比较、排序和图遍历。因此直接实现是总位多项式，不依赖按数值大小枚举。

Python 可直接使用任意精度 int、固定排序、active item 标志、每 agent 的降序列表/跳过已删除 item 的指针、精确总和、force queue 与最终 deque BFS。force 只影响两个端点；重建 pair 图只需扫描 surviving occurrences。最朴素反复扫描版本也为多项式，但不能未经实现分析就冒称达到原文 O(|I|²) 的精确运行时间。

## 5. 待新 Exact 的接口检查点

新桥必须明确 agent 集非空、价值非负、每 item 正支持≤2、singleton/zero-support items 如何分配、完整原任务如何保留、零OPT如何处理、后端价值与目标调度峰的关系。以上只是将检查点列明，不断言新桥满足它们。

本记录不读取未来作者 Proof，不实现新桥，不改变 repo 或 Work，不构成一般 UM 改善结论。
