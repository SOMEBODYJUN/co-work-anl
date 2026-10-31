---
id: "unrelated-machines/single-layer-quota-and-two-state-pool-finite-review"
kind: "review"
type_tag: "审查"
title: "单层配额超图与两状态行列池有限审查"
status: "finite-audit-integrated-with-exact-family-boundaries"
summary: "整合单层配额超图的精确树值审计与两状态行列池的修复前沿审计；保留逐配额层义务、可裁剪资源导致的 5/8 反例及 h_k 闭式，不把有限核验外推为一般 UM 近二或复杂度结论。"
truth_status: "exact-stated-family-and-finite-audit-classified"
review_level: "full-json-read-legacy-main-byte-equality-and-manuscript-cross-check"
scope: "single-layer quota hypergraph value identity and corrected two-state residual row-column pool frontier"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/single_layer_quota_hypergraph_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/single_layer_quota_hypergraph_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/two_state_pool_exact_frontier_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/two_state_pool_exact_frontier_audit.json"
source_ids:
  - "c480b169f713b5cd680f"
  - "7899c2fad926969cf900"
evidence:
  source_sha256:
    single_layer_quota_hypergraph_audit: "3c04a81caa6f549465e446b5023c1783491e3f259323adcd137551d7631956c4"
    two_state_pool_exact_frontier_audit: "e9007061ba847674429ebb1717a1cf9b309e4ccea3a9cfe547b1c5777ed2e5aa"
  legacy_main_byte_equal: true
---

# 实读范围与层次

两份冻结 JSON 在 legacy-cleanup（68fad804…）与 main（aefc58ea…）的同路径内容逐字节相同，SHA 记录在 frontmatter。又全文回读其引用的 `single_layer_quota_hypergraph_obstruction.md`、`duplication_state_majority_floor.md`、`two_state_pool_partial_resource_review.md`，并逐段读取规范/独立审计脚本，核对边界、资源单父约束、精确算术和输出量词。两源都属于 unrelated-machines 的需求树—调度桥接口；与 customer-attraction 六人 SPE 目标保持独立。

# 单层配额超图：树值恒等与逐层一致性

给有限选择点集合 `X`、零需求资源 `Z`，每个 `x` 有非空资源邻域 `A_x`。根需求为 `q`，每个 `x` 需求 1，中间点 `e_x` 需求 `K`，资源终端需求 0；边是 `r→x→e_x→z`（`z∈A_x`）。对 `t=1,…,K`，令 `ν_t(A)` 为可选点的最大个数，使每点取得 `t` 个资源且这些子集两两不交，并令 `ν_0=|X|`。

正文给出的自足恒等是

`b*(Q(A;q,K)) = max_{0≤t≤K} min{1, ν_t(A)/q, t/K}`，

并由任务桥梁得到对应调度族 `OPT=2−b*`。上界从任意评分 `b>0` 的根树中取 `t=ceil(Kb)` 个中间点孩子，并从根下的选中点取 `ceil(qb)` 个；单父条件自动给出两两不交资源子集，因此 `ν_t/q` 和 `t/K` 都至少约束 `b`。反向固定达到 `ν_t` 的不交子集族，构造根、选择点、中间点和资源边，三类正需求比例分别是 `ν_t/q`、1、`t/K`，恒等式闭合。`t=0`、空邻域、`b*=0` 都有显式边界。

该恒等式的归约含义比“完整配额匹配”更严格。若希望 YES 有 `b*=1`，必须有 `t=K` 且 `ν_K=q`；NO 需要对所有中间层 `t=1,…,K` 同时压低 `min(ν_t/q,t/K)`。只压低 `ν_K` 无法排除 `t` 较小的部分领取，因为部分资源足以解码低比例树。给邻域加私有资源会同时抬高多层 `ν_t`，因此不能只修复 YES 而保持 NO soundness。

冻结审计 `single_layer_quota_hypergraph_audit.json` 声明命令 `python3 tests/audits/unrelated_machines/single_layer_quota_hypergraph.py`、Python 3.12.14、宇宙大小 3、`q=1..3`、`K=1..4`、set count 1..3、100 个固定种子随机案例；输出 `exhaustive_cases=4788`、`random_cases=100`、`status=passed`。审计比较的是不交 `t`-子集族与根树值，使用 Fraction，不调用一般调度求解器。普遍性来自正文证明；有限运行只核实现和小边界。

同源的平方根重数审查提供相邻但独立的组合引理：最大不交 `t`-束和资源总关联度 `Δ` 给 `(q−s)(K−t+1)≤Δst`，进而 `s/q≥(K−t+1)/(K−t+1+tΔ)`；它不能被本批超图 JSON 直接吸收为一个新定理。两者共同的接续义务是逐层控制部分配额，而不是只检查完整束。

# 两状态残余行列池：原锐性撤回与修复公式

`two_state_pool_exact_frontier_audit.json` 攻击的原对象是两状态复制的行列资源池：`q=2s` 个变量、根需求 `2s`，每变量需求 1，行/列标签原需求 `K≥s`；状态 0 的 `s` 个变量拥有行资源，状态 1 的 `s` 个变量拥有列资源，行列资源在网格上相交。资源可被标签裁剪，实际树只要求选中标签的真实孩子互不复用。

旧稿曾把“不能同时选两侧”写成完整束冲突，并据此宣称 `b*=min(1/2,s/K)` 对所有 `K≥s`。这是错误的量词替换：树可以只取每个标签的一部分资源。`s=K=4` 的显式树选一行和四列；行取前三格，前三列各取三格，第四列取三格，15 枚资源各用一次。根出度 5/8、标签配额 3/4，所以真实分数为 `5/8>1/2`；JSON 同时保留根/变量/标签/资源的合法性和唯一父检查。

修复后的精确族身份是

`b* = max_{1≤k≤2s} min{k/(2s), h_k/K}`,

其中 `h_k=min{s, floor(s²/k)}`。上界：选 `k` 个非空标签时每标签最多拿 `s` 枚、总资源至多 `s²`，最少整数配额不超过 `floor(s²/k)`；根比例再给 `k/(2s)`。达到构造分两段：`k≤s` 选行并取整行；`k>s` 选全部 `s` 行和 `h=k−s` 列，令 `t=floor(s²/k)`，按模 `s` 循环给列各分 `t` 格，并给每行从剩余格中取 `t` 格。`ceil(ht/s)≤s−t` 保证每行有足够剩余，资源全局不重用。构造只按显式 `s²` 资源和 `2s` 标签扫描，`K` 只进入 Fraction 比较，不按二进制需求展开。

该公式解释旧例：`s=4,K=8,16,32` 仍分别为 `1/2,1/4,1/8`；但 `s=K=4` 为 `5/8`。更精确地，独立审查指出旧式 `min(1/2,s/K)` 在本族中成立的阈值是 `K≥2s−2`；JSON 逐项列出 `K` 和 `old_equation_correct`，显示 `s=3,K=3`、`s=4,K=4,5` 等失败区间。

# 冻结运行与证据边界

主审计字段记录：规范 selected-set matcher 使用 Fraction，`s=1..6` 完整选集；`s=4,K=4` 的显式 counterexample 精确值 `5/8`；每个 `s` 的各 `K` profile、matching calls 和 `old_equation_correct` 均保留。独立程序还记录资源枚举 `s=1,2,3`、所有选集/统一 quota 的整数流检查 `s=1..4`、循环构造 `s=1..100`、499 个优化实际树检查、以及 `K=s,2s−1,2s,3s,10^100+s` 的精确 Fraction 回算。两套程序相互独立，未以闭式公式跳过可行性检查；有限审计不是一般证明。

`duplication_state_majority_floor.md` 的多数状态地板仍有效：状态内资源束不交时，选多数状态可得 `min{|G(δ)|/(2q_r),δ}`；本行列池只撤回其过宽的“整束冲突锐性”声称。两状态池的精确前沿依赖明确的残余行列网格和可裁剪资源，不是任意双状态实例的统一算法、硬度或近二缺口。

# 处置与接续

两个来源均 `integrated` 到本审查。独有内容是单层 `ν_t` 恒等式的审计计数、逐配额层 soundness 义务、两状态池 `5/8` 反例、`h_k` 精确前沿和旧公式的失效阈值。后续若构造近二归约，需要同时控制全部中间配额层，并在两状态复制中保留资源裁剪、状态内不交和实际树的单父约束；不能把完整束冲突当成可裁剪标签的结论，也不能把本批有限审计迁移到当前六人 SPE 覆盖目标。
