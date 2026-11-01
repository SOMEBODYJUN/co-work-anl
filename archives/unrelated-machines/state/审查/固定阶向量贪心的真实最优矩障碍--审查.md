---
id: "unrelated-machines/review-polynomial-vector-greedy"
kind: "review"
type_tag: "审查"
title: "固定阶向量贪心的真实最优矩障碍"
status: "complete"
truth_status: "finite-exact-obstruction-with-parameterized-boundary"
review_level: "full-source-read-and-independent-output-comparison"
scope: "三份 polynomial/vector greedy 冻结输出及其真实最优源、Gram/三阶矩检查和固定阶限制"
summary: "三冻结输出保原身份；规范主程序r1 q3/5/7/13、r2 q11完整源及q3七维投影，独立规范程序仅r1 q3/5/7全Gram与q13计数。旧r2 q7归属已按匹配源码SHA校正，原审查附录r2 q11/13另属第三实现；不授一般调度硬度。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/polynomial_vector_greedy_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/polynomial_vector_greedy_independent.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/polynomial_vector_greedy_primary.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/polynomial_vector_greedy.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/polynomial_vector_greedy_independent.py"
evidence_manifest: "../../tools/evidence/polynomial-vector-greedy-20261030/source-manifest.json"
---

# 固定阶向量贪心的真实最优矩障碍

## 1. 对象

三份冻结输出研究一种先给定真实最优源 schedule，再把源状态压缩成固定阶乘积/Gram 向量、按向量分数逐任务选择机器的贪心。它们认证的是这个指定压缩接口的行为；它们不是对所有 R||Cmax 算法的下界，也没有替换真实最优源的定义。所有运行均为整数或精确 Fraction，无随机采样和浮点容差。

原字节和哈希在 [source-manifest.json](../../tools/evidence/polynomial-vector-greedy-20261030/source-manifest.json)。本轮全文阅读主账本、独立合并/Gram 输出和源重放输出，并把“发现证明”“完整有限运行”“实际输入核对”分开。

## 2. 主障碍：真实最优源为6，贪心到13

`5b894...` 的 claim 是 `UM-TRUE-MOMENT-VECTOR-GREEDY-LINEAR-GAP-v1`。主程序实际检查 2,197 个合法 source schedules，每个 source schedule 的 makespan 都为 6；同一输入下，固定阶向量贪心生成的 schedule makespan 为 13。一个 private anchor machine/job 结构给出 (operatorname{OPT}ge6)，因此这是贪心相对于真实源质量的显式有限 gap，而不是把未知 optimum 的程序输出当作 optimum。

主账本还记录了两次命令：primary 导出目录和 independent 重算。源重算的算术字段写明 `integer and Fraction, no random sampling or tolerance`。其中一个历史实现曾把空乘积当整数导致 Gram 常数项浮点除法；冻结前已改为 Fraction 并重跑，当前冻结数据不包含该失败版本。这是证据链的一部分，不应把修正前的探索输出混入证明。

主源的限制同时写明：有限证据不覆盖任意 (r,q) 或任务顺序；没有在坏的 (r^2) 素数上做完整高阶矩逆；不提出 hierarchy integrality gap、一般 scheduling hardness 或文献新颖性。因此可保留“固定阶向量贪心会线性偏离真实最优源”的实例障碍，不能写成一般复杂度下界。

## 3. 独立 q=3,5,7 与 r=2 复核

`a314...` 使用 Python 3.12 与 NumPy 2.3.5，声明 scope 为“specified compressed-multiplication vector greedy given explicit true optimal source”。它逐 q 保存 source atoms、ordinary jobs、private anchor、所有 source makespan 和完整实际 Gram/projection。r=1 的三组为：

| q | source states | ordinary jobs | exact OPT | greedy | ratio |
|---:|---:|---:|---:|---:|---:|
| 3 | 27 | 3 | 6 | 6 | 1 |
| 5 | 125 | 5 | 6 | 6 | 1 |
| 7 | 343 | 7 | 6 | 7 | 7/6 |

q=3 的 Gram 维度为4，q=5为16，q=7为36；输出保存两个相反任务顺序的实际 Gram、所有列出的三阶矩矩阵和每一步的精确 score gap。以 q=5 为例，首个 ordinary choice 的 score 为 (2/5) 对 (1/5)，随后严格差为 (38/625,224/15625,ldots)，最终向量非零且 anchor identity position 全部核对。q=7 的首差为 (1/7)，每个普通任务仍选机器0；anchor在各已检查插入位置的作用为恒等，greedy makespan为7。

同一独立规范输出没有r=2行：它与8997B源码SHA匹配，参数为q3/5/7/13，代码固定三次多项式源。q3/5/7各做正序、逆序的完整V1 Gram与全部三阶作用；q13只做源容量、全部377个至多三点集的raw/merged计数，再按已证块恒等式核评分，没有形成完整Gram。旧“同一独立输出r2 q7”是参数归属错误，本次依实际代码及匹配的冻结JSON校正，没有重跑或回写原报告。

另一份6178B主程序及2143B source-replay输出的准确域为：r1 q3/5/7/13全部源和至多三点子集；r2 q11的161051个系数原子、全源容量与十个选定至多五点集；r2 q3的243个原子和七维实际V2 Gram／投影。后者q3≤B10不属坏比率参数，不将小维投影核验当作坏族全部V2矩阵已反算。其三步score为(2/3,1/3)、(4/9,2/9)、(208/729,100/729)。另3038次评分检查是r1至4、素数q<80上的闭式Fraction回归，不是3038个完整调度源展开。

第三个实现是已全文阅读的原独立审查附录scratch：r1 q7/11/13检查完整V1残差，r2 q11/13只核源、有限独立性及ANOVA候选范数，未建完整V2。它有自己的三种顺序和seed20261017，不能混入两个规范入口的无seed枚举。三个层级共同支持已发表固定阶解析证明，各自有限范围和执行身份分别保留。

## 4. 参数化解释与量词

独立输出把 q≥7 的 prime family 解释为 exact ratio (q/6)，并称该族 unbounded；这个解释依赖冻结研究稿中的 separate block proof。实际输出仍明确三条边界：

* 没有声称存在一个可从任意输入 (P) 计算 source (D) 的一般近似算法；
* q=13 检查了实际 source 和所有 3-wise counts，但完整 Gram 只在 q=3,5,7 展开；
* arbitrary order 的结论来自另一个 block proof，不来自对所有顺序的有限枚举。

因此更准确的数学对象是：给定一个 explicit true-optimal source、给定固定阶的压缩乘法向量和指定 block family，存在精确可重放的线性/参数化 greedy gap 证据。它可以作为后续算法候选的负面接口测试，也可以要求任何新算法明确说明如何脱离该固定阶压缩；它不能直接作为 R||Cmax 的 hardness、hierarchy gap 或不存在多项式算法的证明。

## 5. 与其他不相关机器对象的关系

它和配置/菜单审计共享“真实源 schedule 与配置代理必须分开”的原则：这里真实 source makespan=6 是输入证据，贪心=13 是指定向量接口的输出；不能把后者当作 configuration OPT。它与森林边界和 Hall/联合匹配批次的连接是障碍性：若后续想从矩压缩向配置/菜单证明转移，必须重新验证 source 的完整性、所有顺序量词和高阶矩可逆性。

它也和已有私有菜单树的 (5/3) 结构界保持独立身份。私有菜单树界要求注入状态、叶重数和配置 LP 前提；本批的 q/r 参数族不自动满足这些前提，也没有把 (q/6) gap 解释成同一配置间隙。

## 6. 处置

三源均已全文阅读、实际输入和输出范围逐项核对、原字节保全。`5b894...` 作为主账本，`a314...` 作为 q=3/5/7 与 Gram 的独立运行，`b319...` 作为固定阶源重放和 recurrence 核验，三者合并到本审查对象。保留浮点修正历史、有限 q/r 范围、3-wise 与高阶矩缺口，不把固定阶障碍扩大为一般调度复杂度结论。

## 7. 本次原程序首次主清洗的校准范围

两份6178/8997B原程序均全文实读；14380B主稿和16295B独立审查及嵌入代码也全文读，采用的主稿SHA与原审查最终指针完全相同。3378B主账本和2143B重放报告全文核，86113B独立输出本次只补核源SHA、参数和各run域等所需字段，不称重新全文审查其全部Gram数值。原较早批次对三输出的全文处置仍原样保留，本次补的是程序/版本及参数归属。源码SHA均与相应冻结输出内source_sha256一致，因此r2 q7不能解释为这两份冻结字节的不同运行参数。

发布证据曾重命名：3378B账本的原路径为polynomial_vector_greedy_audit.json，现存证据名为primary；2143B规范stdout的原路径为polynomial_vector_greedy_primary.json，现存证据名为source_replay。正文source_refs已按稳定源ID及SHA恢复原路径，不把发布别名当冻结原路径。账本files中21ce05…指向2143B原primary输出，不是3378B账本的自哈希；三原字节和旧发布文件均保留。

规范构造的实际机器/任务拓扑亦已在[原反例对象](../反例/固定阶压缩乘法向量贪心真实最优源--反例.md)按原稿和导出校准：q−1普通机器加一个专用机、q普通任务加一个B-time anchor。完整算法、输入导出/排他写及有限证据合同见[规范审计程序](../程序/多项式真实源的两份规范审计与输入导出--程序.md)。原程序、原报告和done均不改；当前0原入口/新数学checker，before快照和guard更新指纹另存新证据。
