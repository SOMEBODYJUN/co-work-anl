---
id: "unrelated-machines/top-two-tree-markov-and-type-profile-three-source-review"
kind: "review"
type_tag: "审查"
title: "双件见证、树 Markov 与类型压缩三源审查"
status: "finite-exact-evidence-integrated"
truth_status: "one alternate top-two objective boundary, one exact five-machine Markov counterexample, and one conditional type-profile bridge, all with explicit scopes"
review_level: "full-json-read-current-proof-code-and-prior-review-comparison"
scope: "top-two pair witness, tree Markov completion failure, and Santa type-profile compression/rank bridge"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/top_two_pair_witness_independent.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/top_two_pair_witness_independent.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/tree_markov_completion_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/tree_markov_completion_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/type_profile_compression_and_rank_bridge_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/type_profile_compression_and_rank_bridge_audit.json"
---

# 读取范围与版本身份

本审查逐项读取三个冻结 JSON、规范程序、当前数学正文及既有 review。库存稳定 ID 与文件 SHA 为：`345a1bb3b88897a2d267` / `top_two_pair_witness_independent.json` / `343ccb0fe2afb63d66484acc9bb72b690930b2bf5fdabb098862ebc87dd59c65`；`72369fac674ccdc4c862` / `tree_markov_completion_audit.json` / `cf2d1bd613e8ac0567f051cc0cf22c0e3059e1775a2e78cff3aec17a5e51b855`；`92a3abb5f2ed72b98573` / `type_profile_compression_and_rank_bridge_audit.json` / `17974884024a0ff480ae459dd43fdad9694aadf9a8ba933b356a2df4316ebb24`。legacy-cleanup 与 main 绑定的是同一冻结路径版本，不计作重复实验。

## 1. 双件目标的独立边界：B₂ 不是普通 makespan

`top_two_pair_witness_independent.json` 固定目标为“每台机器上最大至多两件任务之和”的外层最大值 (B_2)，singleton 以零补齐；它不是普通 makespan，且逐点只有 (B_2\le C_{\max})。JSON 的 provenance 给出独立程序 SHA `0d4749f6896508c0422a166c6c0cd63811a640da2baa764b5562c7507aad23a9`、时间缩放 2、`f_i` 使用正端口与负端口 successor 的出现位置环表示，以及 canonical implication cycle 反向选择顺序。

有限 cases 包括 ring length 1、ring length 2、single pure clause 和 contradictory pure clauses。前三个可满足例均有 192 个完整 assignments，`twice_opt=2`、`twice_min_pair_objective=2`，并核对 truth-table SAT、低 pair assignment 解码及 histogram；矛盾纯子句例穷举 36,864 个 assignments，`sat_by_truth_table=false`、`twice_opt=3`、无低 pair decoder。固定边界还核对空机、全空、singleton unit/half、unit+half pair 和第三件被 top-two 忽略等情形。

当前正文的数学对象是：给阈值 (T)，保留 (p_{ij}\le T) 的端，令 (q_j=\min_i p_{ij})，把 (2q_j>T) 的重任务送入二部覆盖匹配；匹配失败可靠推出 (O_2>T)，匹配成功输出完整分配并保证 (B_2\le3T/2)。精确候选阈值只来自原 finite times、0 与 (2q_j)，谓词随 (T) 单调；因此可在输入位长内搜索首次成功阈值。该过滤器支持的反向归约边界是 pair-only 低负载合同：若 NO 量化所有实际保留端分配都存在同机双件超载，(\rho\ge3/2) 时可判别；只攻击 canonical 分配不足以得出 soundness。

出现位置环归约把每个原变量的文字副本放在循环子句中，unit 任务耗 1，clause half 任务耗 (1/2)，机与 job 资格度至多 3。任意 (B_2<3/2) 的完整分配不能把 unit 与 half 放同机，于是每对 literal 机的一侧真值可解码，循环子句迫副本一致。该结论只处理固定双件目标；正文明确普通总负载可无界大，不能把 (B_2\le3/2) 写成 UM 普通 makespan 算法。\(\rho=3/2\) 时等号使严格 NO 条件消失，三半是本合同的转折而不是趋二 gap。

## 2. 五机树 Markov 再耦合：保 pair 边际仍丢非树兼容性

`tree_markov_completion_audit.json` 是 T=1 的精确 Fraction 反例。机器 1–5，任务 (a,b,d,e,c)，端点为
(a:(1,1/2)\)、(b:(1/2,1))、(d:(1,1/2))、(e:(1/2,1))、(c:(1,1))。真实分布 D 以 1/2 取调度 A：机器负载 ((1,1,0,1/2,1))；以 1/2 取调度 B：((1,1/2,0,1,1))，故 OPT=1。生成树 F 是路径 1–2–3–4–5，只保存树任务 (a,b,d,e) 的相邻 pair marginals，沿父条件分布做 Markov 再耦合。

由于中间机器 3 的配置恒空，左边与右边分支独立，得到四个正概率态；在坏态中冻结 (a\to1,b\to2,d\to4,e\to5)，两端 1 与 5 均已满，非树任务 c 只能去 1 或 5，任一补全 makespan 恰为 2。JSON 的 `complete_orientations_enumerated=32`、`target=1`、`exact_OPT=1`、`markov_outputs` 四态和 completion optimum 均以精确分数记录。该结果反驳“每个正概率树耦合态都可在固定树任务后严格补到 <2T”的合同；它不反驳换树、修复树任务、保留更多相关性或重新选态。正文还给出一步修复：把 a 从 1 移到 2 后再把 c 放 1 即恢复 T 调度，因此它是对特定接口的反例，不是所有修复算法的下界。

当前正文的结构边界是：在每任务恰两端、每机器对至多共享一任务且 pair marginal 来自真实全局 D 的合同下，至多 4 台机器的连通树有覆盖顶点/中央边，因此存在原 D 支持态提供 T 补全；不能把这条边界扩展到断开森林、多个共享任务或非真实分布的 pair 数据。独立程序不导入主程序，均使用 Fraction/整数，无随机采样；有限枚举只核这个输入及其 32 个合法分配，不替代一般 Markov 理论。

## 3. 类型 profile 压缩与真实匹配 rank bridge

`type_profile_compression_and_rank_bridge_audit.json` 以 exact integers/Fraction 检查两个相连对象。其代码 SHA 为 `santa_block_type_profiles.py=64ffa9b8d6d3fb4ff253b53a2c1d1772f73c300363ad1dfa218517321b8dfd86`、`type_matching_rank_bridge.py=1c0ac2c662838795bfd8a616cd7cf88f135b29d7a8e6948b0abc70071c9c1ffc`；审计状态为 PASS，scope 明确是 finite implementation audit，不能替代 universal statements。

### 单阈值 block-profile 压缩

固定正有理 ε，给显式非负有理矩阵和资源子集。cap 至 1、删去小于 δ/n 的值、按 ((1+δ)^{-k}) 向下取整，再以共同 block budget (H=\lceil4t/\delta\rceil) 枚举整数 count profiles。正文的分块引理给每 type 的舍入损失至多 δ/t，总损失至多 δ，保留的 profile 价值至少 (\gamma=1/(1+\varepsilon))。量词是“每个原值至少 1 的实际子集都包含一个输出 profile 子集”，算法不输入 OPT、不求共同 profile、不判定 YES。

审计累计检查 424 个 small matrix/epsilon 参数、7612 个 emitted profiles、288 个 complete YES checks、19620 个原值至少 1 的实际子集、4 个 cutoff 边界和 8 个大 count 向量；另有旧文献 cutoff (1/((1+\eta)n)) 的反例，说明该字面删除量词需要改成 η/((1+η)n) 或本稿 δ/n 的局部修复。此纠错只针对 cutoff 字面步，不宣称原文整体主定理失败。

### Normalized type matching 的精确值恒等式

给每玩家显式非空 indexed profile 菜单 (C_i)，定义
\[
f_{ic}(B)=W(c)^{-1}\sum_{v>0}v\min\{c(v),\#\{j\in B:v'_{ij}=v\}\},\quad F_i(B)=\max_{c\in C_i}f_{ic}(B),
\]
以及互不相交 bundles 的值 (V=\max\min_i F_i(B_i))。构造每个 profile 一个 private machine、每个资源一个 resource machine、每玩家 selector 和每个 positive type 的 token jobs，得到完整 UM 矩阵满足
\[
\operatorname{OPT}_{UM}=2-V.
\]
前向用 B_i 选择达到 F_i 的 profile、把相应 token 外送到不同资源；反向从峰值 (C<2) 的真实调度读取 selector 选择的 profile 和其实际外送资源 B_i。资源独占使 B_i 两两不交，选中 private machine 的负载 (2-f_{ic_i}(B_i))，故 (F_i(B_i)\ge2-C)。未选 profile 的 jobs 必须全部留在 private machine；不能从 actual 调度删掉它们。

该恒等式要求玩家集、资源集和每个 profile 菜单非空，正归一化 (W(c)>0)，indexed duplicate profiles 保持独立身份；m=0、空菜单、零 type/zero count 需单独分支。有限 audit 记录 124 个 fixture variants、1260 个 complete actual assignments、331 个严格次二态反向验证、V=0/1/1/2、缺失/零 type、duplicate profiles 和 257-bit 分母边界，并核拒绝 5 类非法输入。它是给定菜单长度下的实际后端恒等式，不是一般 SC/UM 近似算法。

`F_i` 作为 profile 的最大值一般不次模。审计和正文给出资源值 (1/4,1/2,1/2,3/4) 的反例：(F(\{a,b\})=F(\{a,c\})=3/5)、(F(\{a,b,c\})=1)、(F(\{a\})=1/4)，故 (6/5<5/4)。每个固定 profile 的 (f_{ic}) 可以是加权 partition-matroid rank，但 max-profile 不能直接调用次模算法。

## 4. 三源之间的关系、处置与开放义务

1. 双件 (B_2) 过滤器处理的是不同于普通 makespan 的内层 top-two 目标；它给 pair-only 归约一个三半边界，不替代树 Markov 或类型 profile 对象。
2. 树 Markov 反例说明只保生成树边际不能保证非树任务的共同可行性；类型 profile 后端则展示如何在显式菜单中保持资源独占并做 exact value bridge，二者共同提示“局部边际/菜单压缩”必须附带全局兼容性合同。
3. 类型 profile 的 Exact A/B 仍需外部源 gap 或共同 profile 选择才能接到一般 UM 反面；有限 audits 只回归公式、边界和实际任务身份。

**可保留的完整内容：** (B_2) 的匹配阈值与出现位置解码合同、五机 Markov 再耦合的严格 2T 反例及至多四机边界、固定 ε 的 block-profile 局部完整性、显式菜单下 (OPT=2-V) 恒等式和 max-profile 非次模反例。

**仍开放：** 普通 makespan 的近二整数 YES/NO 归约、修复/重选树 Markov 态的统一余量、shared-type profile 的全局共同选择、未知 YES 见证搜索、一般 SC/UM 算法与外部新颖性。任何后续推进都需重新声明任务/资源身份、所有量词和位复杂度，不能把三份有限 JSON 合并成一个主目标定理。
