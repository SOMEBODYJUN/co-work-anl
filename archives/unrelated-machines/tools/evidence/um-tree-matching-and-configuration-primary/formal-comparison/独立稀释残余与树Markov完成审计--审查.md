---
id: "unrelated-machines/independent-residual-markov-completion-review-20261030"
kind: "review"
type_tag: "审查"
title: "独立稀释残余与树 Markov 完成审计"
status: "finite-audits-classified"
truth_status: "exact-fraction-independent-replays-with-candidate-boundaries"
review_level: "full-json-read-and-cross-archive-comparison"
source_refs:
  - "source:2c063637583fe836db36:evidence/runs/unrelated_machines/independent_set_big_residual_audit.json"
  - "source:4793fd8514c206c37797:evidence/runs/unrelated_machines/independent_tree_markov_completion_audit.json"
  - "source:f9cbe459c9a8df5b68f5:evidence/runs/unrelated_machines/independent_dilution_audit.json"
evidence_manifest: "../../tools/evidence/independent-residual-markov-20261030/source-manifest.json"
---

# 1. 阅读范围与对象分离

本批完整读取三份独立/重算 JSON：小图 independent-set big-residual 候选障碍、树状局部状态拼接的 Markov completion 审计，以及对稀释终端族的独立 exact replay。它们都用精确整数或 `fractions.Fraction`，但研究对象分别是图残余、局部状态拼接和稀释树族；只能合并为“独立有限边界证据”，不能拼成一个统一 theorem。

本批与《稀释逃逸、行度交易与共享终端局部审计》比较了 k=4,h=3 的完整展开、压缩公式、row-degree 和 k=2 frame；与《重型匹配凸化与逃逸残余审计》比较了 path-only/global rejection；与《配置剥离与联合匹配有限审计》比较了 bundle-peeling 和 tensor 的局部—全局量词。下文只保留三源独有字段。

# 2. independent-set big-residual：有限候选障碍

来源 `2c063637583fe836db36` 的 claim 是 `UM-INDEPENDENT-SET-BIG-RESIDUAL-INTERFACE-v1`，状态明确为 `candidate_obstruction_not_hardness`。命令使用 `independent_set_big_residual_audit.py`，Python 3.12.14，代码 SHA 为 `0961efd2...7febae`。

实际检查 1080 个实例，定义域为：所有 (n\le4)、最大度不超过3的简单图；(k=0,\ldots,n)；参数 ((q,h)=(3,1/3))；(r\in\{0,1,2\})；使用 exact Fraction assignment enumeration。来源明确未检查 general UM hardness、near-two approximation gap，也未对所有 (alpha,h,r) 做 exhaustive enumeration。

可复用的数学身份是“指定小图、指定 q/h/r 族上，枚举能区分 big residual 接口的 1080 行 exact assignment 数据”。它可以作为后续构造候选的回归集，尤其是检查独立集残余与 big job 接口是否在低度图上已经失效。它不能承担 hardness：图规模只有四顶点，参数范围固定，且来源没有把 `status` 升级为 gap 或归约。

后续若要形成正式障碍，需先给出任意 (n)、度界、(alpha)、(h)、(r) 的输入合同，再证明从图到 unrelated-machines 处理时间矩阵的映射、整数 OPT 下界和配置/分数阈值的同一量词。目前仅保留为 candidate obstruction。

# 3. 树 Markov completion：局部拼接可能产生一个坏完成

来源 `4793fd8514c206c37797` 只含精确 Fraction/整数结果，核心对象有两条 source global schedules：

[
\Pr(\text{schedule}_1)=\Pr(\text{schedule}_2)=1/2,
\qquad \max\text{ load}=1.
]

它对 complete assignments 穷举 32 个，得到 integer optimum=1。随后把五个局部位置的状态拼成四个 glued support 行，每行概率 (1/4)，并冻结 assignment/load；四行的 `best_completion` 依次为 1、1、2、1，因此

[
\Pr(\text{best completion}=2)=1/4.
]

四个局部行的关键数据如下：

| 行 | 局部状态（压缩记法） | 冻结 assignment | frozen loads | best completion |
|---:|---|---|---|---:|
| 1 | (1:c,2:ab,3:\emptyset,4:d,5:e) | (a,b\to2,d\to4,e\to5) | ((0,1,0,1/2,1)) | 1 |
| 2 | (1:c,2:ab,3:\emptyset,4:de,5:c) | (a,b\to2,d,e\to4) | ((0,1,0,1,0)) | 1 |
| 3 | (1:a,2:b,3:\emptyset,4:d,5:e) | (a\to1,b\to2,d\to4,e\to5) | ((1,1/2,0,1/2,1)) | 2 |
| 4 | (1:a,2:b,3:\emptyset,4:de,5:c) | (a\to1,b\to2,d,e\to4) | ((1,1/2,0,1,0)) | 1 |

这个对象的逻辑边界是清楚的：全局 schedule 分布每个样本最大负载为1，但先按局部状态拼接、冻结部分 assignment 后，有 (1/4) 的局部行只能以 makespan2 完成。它是“局部边缘/支持信息不足以保证统一低峰值完成”的有限机制见证。

它不是一般 Markov theorem：源只给出四个 glued support 行和 32 个 complete assignments，没有任意树深度、状态数、分支概率或全局耦合量词。`best_completion=2` 也不是一个新的 unrelated-machines hardness，因为没有从任意输入生成这种局部状态分布的归约。后续若要利用该边界，应明确局部状态 sigma-field、可见 assignment、completion 规则及概率量词，再证明拼接操作与原调度实例的同一性。

# 4. independent dilution：k=2/3/4 的独立重算

## 4.1 运行和独立性

来源 `f9cbe459c9a8df5b68f5` 标题为“独立重算稀释终端实际证书”，Python 3.12.14，Fraction exact，seed=20261016；submitted code SHA 和 audit code SHA 都保存在原 JSON。它明确声明：candidate/probe generators 是 imported，数值断言独立重算；没有调用任何 submitted `check_*` 或 `star_matching_certificate`；有限算术不证明 universal family theorem 或 `UM-TARGET-v1`；第9节一般 rejection proof 只做符号阅读，没有测试 generic LP solver。

## 4.2 三个 k 的精确数据

| k | h | machines/jobs | all edges | config columns | actual probe vectors | all star edges | largest F | largest fractional load | independent integer value | brute OPT |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 1 | 6/7 | 14 | 16 | 14 | 14 | 2 | 3/2 | 3/2 | 3/2 |
| 3 | 1 | 14/17 | 74 | 74 | 74 | 74 | 5 | 4/3 | 5/3 | — |
| 4 | 3 | 426/521 | 4562 | 4570 | 58（typed coverage + one full bottom blocker + seed sample） | 4562 | 11 | 5/4 | 7/4 | — |

k=2 的 128 个全 assignment 穷举给出 independent brute optimum=3/2，并且 independent constructed integer value=3/2。k=3、4 的 independent constructed integer value 分别为 5/3、7/4，但没有把所有 14/17 或 426/521 的 assignments 全量枚举；k=4 的 58 个 actual probe vectors 也不是全 4562 边的逐向量 schedule oracle，而是 typed/底层 blocker/seed sample 的选择。

## 4.3 与主稀释审计的独有关系

主稀释批已记录 k=4,h=3 的 427 机/521 作业/4914 eligible edges、(T=5/4)、构造值 (7/4)、4562+352 LST probes 和 GHMR/star 证书。本 independent replay 的独有内容是：

- k=2 的 128 assignment 全枚举与 3/2 最优值；
- k=3 的 74 条边/74 配置列的全 probe 向量核验；
- k=4 的 4562 star-edge 全覆盖、但仅 58 个 typed actual probes；
- 明确禁止调用提交的 checker/certificate routine，并保留两个代码哈希。

因此它增加了独立算术重算和小 k 的完整性，但没有把 k=4 的压缩/局部证书升级为全局配置—调度等价，也没有证明 (k\to\infty) 的比率族。

# 5. 统一比较、处置与接续

1. 与稀释主审查：本批 `f9c...` 是独立重算，不能重复计数为新实例族；它的 unique content 是独立代码路径、k=2 全 assignment、k=3 全 probe 和 k=4 typed sample。`479...` 的 Markov completion 不属于同一机器树模型，只保留为局部支持拼接障碍。
2. 与 heavy matching：两批都显示 local/probe/partial support 可以通过而全局完成或全局资格仍有缺口；但本批没有 path-only/global filter 的 171 机实例，不能把 `best completion=2` 解释为 heavy matching ratio。
3. 与配置剥离联合匹配：2c 的小图枚举与 bundle/tensor finite audits 方法相近，但变量和输入合同不同；不把 1080 行 candidate obstruction 加入 Hall 或 C2 结论。
4. 与 CAG 六人目标：三源都没有目录客户、完整历史或 SPE 覆盖量词，保持 unrelated-machines 独立身份。

逐源处置：

- `2c063...`：保留为 candidate obstruction，正文明确未检查 hardness/near-two/general parameters；证据副本完整保存。
- `4793...`：保留四个 glued support 行、全局 optimum=1、probability(best completion=2)=1/4，分类为 finite local-completion obstruction；不称 Markov theorem。
- `f9cbe...`：集成独立 dilution replay；保留 k=2/3/4 全字段、assignment/probe 覆盖和 imported-generator/no-checker 限制；不称 universal family theorem。

后续若继续，应先把局部支持拼接和稀释 probe 嵌入同一明确 machine/job 输入，再证明全局 configuration coupling；对于 2c，应扩大 n/参数并给出整数 OPT 和阈值的统一证明。当前三源的正式真值等级保持“有限精确重算、局部完成障碍、候选而非硬度”。
