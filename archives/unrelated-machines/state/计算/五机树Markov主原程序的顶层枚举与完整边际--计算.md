---
id: "unrelated-machines/five-machine-tree-markov-primary-top-level-and-full-marginals"
kind: "computation"
type_tag: "计算"
title: "五机树Markov主原程序的顶层枚举与完整边际"
status: "complete-primary-read-and-original-CLI-retained"
summary: "主程序顶层真实执行一次，32合法分配与四个树耦合态完整核验；坏态四分之一、冻结后最优2，修复与四机边界分开。"
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/tree_markov_completion.py", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/tree_markov_completion.py"]
source_ids: ["2171ba148bfb1f9ac193"]
truth_status: "explicit mathematical contracts and finite original runs separately scoped"
review_status: "informed internal reread; original historical independence preserved; no new blind review"
---

# 实际代码和完整输入

4173B `tree_markov_completion.py`、SHA981a354c…全文读并核冻结blob；原CLI一次exit0。此文件**没有main guard**：从marginals建立、32分配枚举到四态/完整边际核验和print都在顶层，本批只直接运行一次，未被其它脚本import；没有外部输入、随机数、repo依赖或子进程。其它三primary有guard，不能把此顶层执行漏计或另算一次。

五台机器1..5，任务顺序(a,b,d,e,c)，未列端为∞：a在1时间1、2时间1/2；b在2时间1/2、3时间1；d在3时间1、4时间1/2；e在4时间1/2、5时间1；c在1或5均时间1。T1，c给OPT≥1。真实分布D各以1/2取完整调度A=(c→1,a/b→2,d→4,e→5)和B=(a→1,b→2,d/e→4,c→5)，均峰1，所以OPT1。

选树路径1–2–3–4–5、树任务a,b,d,e。脚本完整保存每台配置marginal及四条树边full-configuration pair，按
\[
\Pr(S_1,\ldots,S_5)=\mu_1(S_1)\prod_{(u,v)\in F}\mu_{uv}(S_u,S_v)/\mu_u(S_u)
\]
枚举各单机正支持配置的笛卡尔积；分母皆来自正支持。机器3恒空，将左右A/B分支重新独立。每个正概率态丢弃c的暂时配置，只冻结四个树任务，分别试c的两个实际端。

| 左/右分支 | 树端1/5负载 | 最佳补c |
|---|---|---|
| A/A | 0,1 | 1 |
| A/B | 0,0 | 1 |
| B/A | 1,1 | 2 |
| B/B | 1,0 | 1 |

每态概率1/4。坏态a→1,b→2,d→4,e→5，c放任一端都令峰2；这是给定树、**每个**正概率态、冻结树任务、不许迁移的严格<2T合同反例。原D本来已给最优调度，不能说D信息不够或所有调度算法都失败。

# 实际枚举和可修复边界

原CLI完整枚举2^5=32合法σ并核OPT1；对四个正态逐任务验证树分配合法/一次覆盖，逐态试两个c端；又独立从新四态聚合重算全部五份完整单机marginals和四条树边pair，精确等于旧数据。输出保存全输入、D、pair数据、state、partial、tree_load、最佳补全及最佳c机器，不只保PASS。无数值容差；坏质量恰1/4。

坏态只把a从1移到2，再放c→1便回峰1；原程序未自动运行这一步，但由给定矩阵可直接证明。至多4机的同合同正面结论也来自canonical证明：连通树存在一个顶点或中央边覆盖全部树边，其fullstate/pair出现在原D支持中，决定全部树任务方向，原支持态给T补全。本次32个分配没有枚举所有四机输入；上述界不含断开森林、多共享任务或伪造pair数据。

# 旧程序、读后与本轮去向

5545B canonical和2966B审查全文已核；审查基线8701…，canonical736284…、主码981a…均对得上。历史先精确输入独立重建后读全文/源码，本轮知情核验不冒新blind。5078B新stdout与冻结主输出逐字节同。BW批执行的是3592B独立程序e00e219…，也核32/四态，但它不import本主程序；BW未执行此主入口，本批才对已领主源正式执行和处置。旧独立2098B结果保持比较身份，不新增run或新反例族。

[完整原件与运行](../../tools/evidence/um-locally-cached-four-audits-primary/README.md)、[5078B新stdout](../../tools/evidence/um-locally-cached-four-audits-primary/runs/tree-markov.stdout)、[已有最终审查](../审查/五机树Markov再耦合补全反例最终审查--审查.md)、[BW独立程序对象](五机树Markov独立原程序的逐态最优补全--计算.md)。生成树pair不等于共同全叶law/localizer；换树、择态、保更多相关性、树任务迁移和一般UM目标仍不受该有限反例排除。
