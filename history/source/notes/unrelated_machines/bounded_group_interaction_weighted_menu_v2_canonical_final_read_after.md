# 有限组交互加权菜单：澄清后 canonical 最终实际读后

审查 ID：`UM-BOUNDED-GROUP-INTERACTION-WEIGHTED-MENU-v2`。

日期：2026-10-18。本文件另行冻结，未覆盖旧 canonical 读后记录、Exact-only 独立记录或作者 Proof 读后记录。本次再次实际读取了澄清后的 canonical **全文**，不是仅根据 root 的改动说明认证。

## 当前实际读取对象

路径：

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/weighted_menu_bounded_group_interaction_rounding.md`

字节数：`10,554`。

实际 SHA256：

`b0897b06723f4dd410ad230806a0ae03712a178b6a259ec8dd1688e04a6a8889`

## 最终结论

**PASS；无 standing fatal 或待解决的数学异议。** 当前 canonical 与已通过的 Exact-first 独立推导及作者 Proof_v2 完整一致。实际输出全部原 jobs；state 内资源集合无重；失败分支正确给 relative guarantee 而非 unconditional absolute guarantee；精确尾项、零时间、空状态、beta=1、binary 大参数和 dense 矩阵/assignment 输出均完整处理；cube 的 q 正确约束完整变量并集。

旧读后记录唯一提出的措辞澄清现已准确落地：§2 明确以下 state/resource 均属当前归一化实例，包含 bonus，不能将“原资源”误读为仅限增广前 P 的资源。于是 §3 heavy graph 和 §5 slot graph 中的真实资源均包括相应 bonus resources，不存在遗漏归一化 heavy edge 的疑义。

## 实际版本差分核验

对本次全文读取的 b089 版本，仅把新澄清句逆替换回原来的“以下先设所有W_gs=1。”，所得全文的 SHA256 精确等于旧实际读取版本：

`d305cf8e2dd5c70dc30e7811c3ed71787eba179d30171bfdeb794468a25e56d1`

因此已通过密码学散列核验：当前版本与上一实际读后版本相比，只有这处约定句改变；输入域、算法、全部不等式、复杂度和 scope 均未改变。此差分核验是对再次全文阅读的补充，不替代全文阅读。

旧完整逐项核对记录仍原位保存为：

`/workspace/scratch/038d9dcc4cac/bounded_group_interaction_weighted_menu_v2_canonical_read_after.md`

SHA256：

`2f80f102cde097cb10dc439d1114e90f1c05a7f28bceefd5becee11afb001593`

旧记录对 d305 版本的认证保持其历史含义；当前 canonical 的最终认证以本文件明确的 b089 版本为准。

## 最终边界确认

- 两分支真实保证仍为：成功实际峰至多 `R=2-beta`；失败真实 `OPT>=1+beta` 且返回峰至多 2，利用 `2/(1+beta)<=R` 得所需 ratio。没有宣称所有输入均有 absolute R 调度。
- 归一化对所有 deficient indexed states 加 bonus，反向扩展导出所有 states 的 bonus，投影只删除 bonus；没有丢失未选 states 的原 jobs。
- Hall 的右度计数继续要求同 state 资源无重；out-of-domain 非单射反例保留且未被误用为扩大域的一切比 1 算法不可能性。
- full-slot 尾项计账包含空尾及不完整尾；`n<Delta` 的空 sampled sum 不等式成立，但正质量下界排除 success 中真实 L 组处于该情形。
- binary 参数未按数值展开；dense 矩阵仅多项式项数；最终 assignment 给每个原 job 一个合法 machine identifier。
- `M<=q(d-1)` 中 q 是完整菜单变量并集上界；resource-degree 界按全部菜单而非有利选态计算。
- root 指定后续创建的 embedding 文件是 pending 导航，不是本文自足证明的前提。本次不因该导航尚待建立而给数学 fatal，也不预先认证其 embedding 内容。

没有修改 repo、Git、Work、旧冻结记录或当前 canonical。本次没有新增实现、外审、新颖性或因子锐性认证。
