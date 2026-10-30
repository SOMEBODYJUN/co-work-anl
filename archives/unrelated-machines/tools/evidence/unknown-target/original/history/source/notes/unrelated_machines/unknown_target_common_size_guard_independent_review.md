# Unknown-B common-size 满流 guard：独立审查

## 1. 读取现有正文/脚本之前的 Exact-first 推导

父任务给出的修复 Exact：feasible(B) 先检查 B<max_i f_i，若是则 false；否则各机容量 floor((B-f_i)/q)，残余 job→合法机器的整数满流当且仅当完整峰≤B。候选为 {f_i+qt : i∈M, t=0,…,n}，排序有限二分；n=0 输出 max_i f_i。当前未读取未来 root 修改。

在非空有限机器集、固定非负冻结负载 f_i、严格正共同残余大小 q、每 job 必须完整分配到合法机器的模型中，以上修复正确。

**原反例。** f=(2,0)、q=1、一个残余 job 仅能放机器 2。B=1 时，忽略冻结峰的残余满流会成功，但任何完整调度的机器 1 负载仍为 2。把 job 放机器 2 可达到峰 2，所以真实 OPT=2，不是 1。

**必要方向。** 若完整峰≤B，则每台 f_i≤B；设机 i 上有整数 k_i 个残余 job，则 f_i+qk_i≤B，故 k_i≤floor((B-f_i)/q)。沿其合法边发送每 job 一单位得到满流。

**充分方向。** guard 后所有 B-f_i≥0，容量非负。整数满流给每 job 一个合法机器，且每台计数不超过其容量，因此 f_i+qk_i≤B。此推理逐一覆盖全部机器，包括不连任何残余 job 的冻结孤立机器。

**候选与二分。** 任意有限可行分配的完整峰在某台机器达到，为 f_i+qt，0≤t≤n。故 OPT 属于所给有限候选集。guard 后的可行性对 B 单调。候选数≤m(n+1)，排序后二分需 O(log(m(n+1)+1)) 次可行性调用（不是全部运行时间）；初次排序和每次满流仍另计多项式成本。若允许某 job 没有合法机器，必须报告 infeasible，而不能无条件输出候选最大值。

**空残余与孤立机。** n=0 时无须流，唯一目标是 max_i f_i。n>0 时高冻结孤立机器可决定 OPT，不能从机器集、候选或 guard 中删除；f_i=0 的孤立机器当然无害。若 q=0 或机器集空，必须按精确输入域另行处理，不能直接使用除法或 max 空集。

以上先于读取当前正文和脚本完成。后续代码审查只针对精确快照，任何变化应另行标 hash。

## 2. 修复前实际快照

随后读取修复前正文与脚本。正文 SHA 为 `735e4ab2a304eba9220996dc332329cc15cd38b12733fbb9b1b743aea5709678`；脚本 SHA 为 `e48c9e2e047dc486a76252492ed70c855579a5188b7e1d80587a713b76f62c40`。

正文确用 max(0,floor((B-f_i)/q))，没有先检查冻结峰；脚本 feasible 同样缺少该 guard。上节反例确实命中，不是只存在于抽象接口。

脚本前置 BFS 从不更新 match，所以实际上只是对每个 job 检查是否存在正容量邻机；它是冗余的必要条件检查，不会单独造成错误拒绝。其后 DFS 才执行真正的容量匹配：失败分支不修改匹配，每次访问满机器递归考察其全部当前 occupant，成功后一路返回并置换，未发现第二个布尔正确性漏洞。递归实现是 tiny audit，不应据此声称对任意输入规模都不会触及 Python 递归深度。

修前脚本只有两个非空连通实例，注释所说 disconnected/zero jobs 并未实际覆盖。脚本也只实现 feasible 和穷举 oracle；没有实现完整未知 B 二分器或输出任务分配见证。因此它是小规模谓词审计，不是完整算法产品。

组件推广必须保留无残余边的冻结机器：可以视为无 job 的机器组件，或把 max_i f_i 加入全局 max。若只对含 job 的组件取 max，会重新丢失同一个冻结峰约束。

## 3. 修复后实际 read-after（三文件及最终两句）

root 实施修复后，本审查者实际读取三份文件的全文并核验 SHA：

- 正文 `research/current/unrelated_machines/unknown_target_common_size_exact_repair.md`：当时 SHA `345c71dcc169df59f8f5f33a43a2a3a9329e2545250475ed354721c6956b39ff`。
- audit `tests/audits/unrelated_machines/unknown_target_common_size_exact_repair.py`：SHA `a4c0f8ff93c8d016609787a36c4a6ab181a1e640b949507214d4c4f221b15890`。
- 审查 `research/reviews/unrelated_machines/composition_decoder_obstruction_review.md`：SHA `bd3b3d52d9796f74c57e00b524820a9bc97443b248e31694e4b3eba1f69b6dc9`。

正文与 feasible 都已在容量计算前拒绝 B<max f。正文保留旧反例并解释它是原判定证明/代码错误，不是改换数学对象；调用数改成 O(log(m(n+1)+1))。audit 增加 f=(2,0)、job 只去机器 2 的回归和 n=0 回归，并对列明四例的每个候选阈值逐点比较 feasible 与 brute_opt。补充审查保留原 fatal 与修复经历，没有将 tiny audit 升格为一般算法。

本审查者提出组件推广需明确保留孤立冻结机器后，root 只改正文两处。本审查者随后再次实际读取这两句：

- 命题处现在要求把每个含新任务分量的 B_c* 与所有不接收新任务的冻结机器负载共同取最大值；
- 证明处现在明确全局峰还含孤立冻结机器负载，且不能因机器不属于含任务分量而删去 f_i。

两句正确关闭了组件聚合的边界歧义。最终正文 SHA 为 `9f5950fd508009c3a1cf5ab57050a1e57d559490c29993570310f1a19ac8e1d2`；audit 与补充审查的上述 SHA 未变。单共同尺寸的 guard 判定、候选二分、n=0 以及机器侧不相交的不同尺寸组件推广均在明确域内成立。

## 4. 实际运行及证据归属

**root 的 repo 审计范围：** root 报告运行脚本列明的四例。本审查者也实际执行同一修后脚本，得到 `ok`。不得将下列更大的 scratch 校验记成 root 的 repo 运行范围。

**本审查者独立 scratch 校验：** 脚本 `audit_unknown_target_guard_independent.py` 调用被审 audit 的 feasible 与其 brute_opt；本审查已逐行核明后者直接枚举全部合法完整分配并计算全机峰，不复用流判定。scratch harness 遍历：m=1,…,3；n=0,…,3；f_i∈{0,1,2}；q∈{1,1/2}；每个 job 的任意资格子集（包括空集）；每个候选阈值及 B=-1。共 33,210 个实例、225,648 个阈值比较全部通过。对可行实例，首个可行候选也等于枚举 OPT。结果写入 `unknown_target_guard_independent_audit_result.json`。扩展实例族和运行属于本审查者，brute_opt 的来源仍为 peer audit，不将其冒称本审查者新写的 oracle。

此有限校验支持实际 predicate 代码与精确证明相符，不代替全量词证明，不验证任何一般 UM 近似结论。

## 5. 保留的实现限制

现有 repo 脚本只实现布尔 feasible、小规模 brute_opt 和四例审计；没有实现完整未知 B 二分器或输出分配见证。前置未填匹配的 BFS 冗余但不是布尔正确性 fatal。共同容量匹配的递归 DFS 在 Python 的固定栈深下也不能当成任意规模通用实现。

本审查者实际构造合法可行长链：n=m=1200，f_i=0，q=B=1；前 1199 枚 job i 的资格为 [i,i+1]，最后一枚仅 [0]。完整见证是最后 job 放机器 0、前 job i 放机器 i+1。当前 feasible 实际抛出 `RecursionError`，记录于 `unknown_target_guard_recursion_probe.json`。这说明脚本的适当状态是 tiny predicate audit / audit_only，不是生产级总位多项式算法实现；它不反驳使用迭代普通最大流的数学算法。

父任务明确保持 metadata 为 implementation audit_only，不要求本轮重写 flow；本审查者未修改任何 repo 文件，也未把递归限制隐藏为“通用实现已完成”。

## 6. 最终判定

**数学修复通过；修后 tiny audit 在声明的小规模范围通过；通用算法实现未提供。** 原 guard fatal 被真实修复，n=0 与冻结孤立机没有遗漏，组件推广已显式保留它们。没有发现 guard 之外的第二个布尔匹配逻辑错误；上述 RecursionError 是真实且已保留的规模限制。

该结论对应第 3 节最终三文件 hash，且严格区分 Exact-first 推导、修前实际读取、修后全文 read-after、最终两句回读、root 四例运行与本审查者独立有限校验。
