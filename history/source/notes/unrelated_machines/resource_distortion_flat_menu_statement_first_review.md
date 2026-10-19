# 逐资源正成本畸变的实际调度界：陈述先行独立重构

本文件由 `negation_logic` 仅依据 root 给出的 statement 独立重构。写作时尚未读取 `source_promise_decoder_draft.md` 或作者证明。先冻结本文件并向 root 报告 SHA256，之后才允许作者读后审查。本文件不是正式入库 Claim，不宣称原创性，也未实现外部 Santa Claus 算法。

## 1. 精确域、必要边界及审查结论

设非空有限组集 G；每组 g 有非空显式 state 集 S_g。每个 state x=(g,s) 有一台独占 private 机器，全部 private 机器两两不同，并与 resource 机器集合 U 不交。组 g 的一枚 selector 只能在本组的 private 机器上执行，时间均为 1。每枚 incidence job e 有一个 private 端 x(e)，其时间为非负二进制有理数 p_e，另有一个 resource 端 u(e)，时间为 1；没有其他有限端。所有原 incidence jobs 包括 p_e=0 的 jobs 都保留。令

\[
W_x=\sum_{e:x(e)=x}p_e\le1,\qquad b_x=1-W_x\ge0.
\]

通常一对 (x,u) 只有一枚 incidence；下面证明也覆盖显式重复的 incidence，因为只会在同一 (x,u) 上选一枚最大 p_e 的 job 外送。

对每个有正 p_e 的资源 u 定义

\[
q_u=\min\{p_e>0:u(e)=u\}.
\]

假设每个这样的 u 都有 \(\max\{p_e>0:u(e)=u\}\le\kappa q_u\)，其中 \(\kappa\ge1\) 可以随输入变化。没有正项的 u 不限制，构造时不为它建礼物；若整个输入没有正项，可取 κ=1。

**重构结论。** 对每个固定实数 α>6，存在同一确定性总位多项式程序，对所有本域输入输出全部原 jobs 的合法调度 σ，满足

\[
C_{\max}(\sigma)\le2-\frac{2-\operatorname{OPT}(P)}{\alpha\kappa}
\le\left(2-\frac1{\alpha\kappa}\right)\operatorname{OPT}(P).
\tag{1}
\]

程序本身不使用 κ 或 OPT，只用原输入的有限有理数。κ 仅用于分析，故不会因数值 κ 巨大产生伪多项式循环。基于下述外部受限 Santa Claus 定理，限定声明可闭合；没有发现该域内 fatal。

**边界修正。** 必须写 G 非空，或把空组集作为单独输出零调度的分支。非空 G 保证 OPT≥1。若 G 为空则 OPT=0，式 (1) 中间项为正，不能仍声称它小于右侧零；这只是所写不等式链的域边界，零输入本身可直接解决。private 与 resource 的机器身份不交也是承重定义。

## 2. 已知最优调度提供什么见证

全部 incidence 留在各自 private，任取每组一个 state 放 selector，得到合法峰值至多 2；任一 selector 给峰值下界 1。因此

\[
1\le O:=\operatorname{OPT}(P)\le2,\qquad D:=2-O\in[0,1].
\tag{2}
\]

若 D>0，则最优调度峰值 O<2，每台 resource 机器至多接一枚 unit incidence。令 x_g 为其 selector 所在 state，E_g 为从该 state 外送到 resource 的 incidence 集。不同组的 E_g 使用的 resource 两两不交，而且组内也至多一件使用同一 resource。选中 private 的负载为

\[
1+W_{x_g}-\sum_{e\in E_g}p_e\le O,
\]

所以

\[
b_{x_g}+\sum_{e\in E_g}p_e\ge D.\tag{3}
\]

这只是分析见证，不把最优调度或该 E_g 作为算法输入。D=0 时不需要从峰值恰 2 的最优调度提取资源注入，因为此时后面的 Santa 下界为零。

## 3. 显式受限 Santa Claus 实例

为每个原 state x 建一名 Santa 玩家。礼物如下。

1. 每个 q_u 已定义的原资源 u 建一件实际礼物 r_u，礼物公共价值 q_u。玩家 x 对它感兴趣当且仅当存在 incidence e 满足 x(e)=x、u(e)=u、p_e>0。
2. 每个 b_x>0 建一件只给玩家 x 正价值的私有 baseline 礼物，价值 b_x。b_x=0 时不建这件辅助礼物，不删任何原 job。
3. 每组 g 建 |S_g|−1 件不同的 dummy 礼物，每件公共价值 1，只有本组全部 state 玩家对它感兴趣。

每个玩家对每件礼物的价值恰为零或该礼物的公共价值，所以严格落在 restricted Santa Claus 的域。每个原资源只有一件礼物，不能给不同 state 分别复制同一资源。所有这些表都是显式的，dummy 的资格表至多 \(\sum_g|S_g|^2\) 项，仍为原 state 总数的二次规模。

记该 Santa 实例最优最小效用为 V。由 (3)，可为每组选中玩家 x_g 分配对应真实资源礼物及其私有 baseline。对 e∈E_g，\(q_{u(e)}\ge p_e/\kappa\)，且 κ≥1，故该玩家收到的效用至少

\[
b_{x_g}+\sum_{e\in E_g}q_{u(e)}
\ge\frac{b_{x_g}+\sum_{e\in E_g}p_e}{\kappa}
\ge\frac D\kappa.
\]

本组其余 |S_g|−1 名玩家各得一件 dummy，效用为 1≥D/κ。所有资源互不冲突，故

\[
V\ge D/\kappa.\tag{4}
\]

D=0 时 (4) 由非负性自动成立。不能把对每个 state 的资源集合取并后直接当一个组的 additive valuation；dummy 构造保留“只读一个实际 state”的语义。

## 4. 外部算法输出如何读回全部原 jobs

调用确定性 restricted Santa Claus α-近似，得到一份实际不交礼物分配，所有 state 玩家效用至少 V/α≥D/(ακ)。每组只有 |S_g|−1 件本组 dummy，因此至少一名 state 玩家 x_g 没收到任何对其有正价值的 dummy。取这种玩家，忽略分给它的零价值礼物；其效用 a_g 全部来自 baseline 和真实资源礼物。

对它得到的每件真实资源礼物 r_u，在原 (x_g,u) 的 incidence 中取一枚最大正成本的 job e(x_g,u)，将其外送到 u；该 job 的 p_e≥q_u。把组 g 的 selector 放在 x_g。其余全部原 incidence，包括所有 zero jobs 与未选 state 的 jobs，都留在原 private。

每件真实礼物只属于一个玩家，因此这些外送 jobs 在所有资源机器上至多一枚，每个资源负载≤1。未选 private 负载 W_x≤1。选中 private 负载为

\[
1+W_{x_g}-\sum_{u:r_u\text{分给}x_g}p_{e(x_g,u)}
\le2-\left(b_{x_g}+\sum_{u:r_u\text{分给}x_g}q_u\right)
\le2-a_g
\le2-\frac D{\alpha\kappa}.
\]

baseline 即使没实际分给 x_g，也有 a_g≤b_x+Σq_u，所以这里没有免费假定它必被分配。由 D≤1、ακ>6，最终上界大于 1，故它同时控制所有 private 与 resource 机器，给 (1) 第一项。全部原 jobs 各执行一次；所有额外 Santa 礼物只用于选择，不是删除或代替原 jobs。

令 c=1/(ακ)∈(0,1)，有

\[
(2-c)O-[2-c(2-O)]=2(1-c)(O-1)\ge0,
\]

给 (1) 第二项。固定 κ 时，这确实给本结构类统一的 2−1/(ακ) 实际近似；κ 无界时改善可能趋零，不能升级 UM-TARGET-v1。

## 5. 原始文献核对与位复杂度补链

已联网实读 Davies–Rothvoss–Zhang, *A Tale of Santa Claus, Hypergraphs and Matroids*, **arXiv:1807.07189v4**，提交修订日 2026-01-04。必须指定 v4，因为该文 §4 明确更正旧版 4+ε 分析，当前 Theorem 3 为 6+ε。

- 原文 §1 定义是 \(p_{ij}\in\{0,p_j\}\)，§1.1 Theorem 3 给实际近似算法，时间 \(n^{O_\varepsilon(1)}\)。这里没有导入一般异值 Santa 或纯估值结果。
- 确定性不是仅凭摘要猜测：§2 Algorithm 1/2 是组合选择、matroid 独立性测试及交换；Expansion Lemma 8 的构造采用贪心；§3 采用显式有理 LP 与 bipartite matching。固定输入次序和确定性 LP/匹配/贪心平局规则即可确定化，未见随机采样步骤。本审查没有重证其整个增广树定理。
- 对任固定 α>6，预选固定有理 β∈(6,α)，再取足够小的固定有理内部误差，使原文效用系数至少 1/β>1/α。程序不需要编码给定实数 α。
- 构造中只有原数的精确最小值、最大值、加减和资格判断；baseline 的分母乘积二进制长度至多原分母总位长。辅助实例的总位长为原输入位长多项式。
- 原文 §3 开头“可假定知道 integral OPT，否则二分”不应解释为调用精确 NP oracle。可先把辅助实例全部正礼物值乘公共分母 Q，Q 的位长为各分母位长之和。总礼物值 U 的位长为输入多项式。对整数目标 t，用 §3 的 LP 可行性及 Theorem 2 形成总过程：若真实 V≥t 则成功，成功时输出实际最小效用≥ct，失败则证明 V<t。超过目标的单件礼物先截为 t，保留所有真实 t-可行见证。先置 lo=0（零效用分配）、hi=U+1（真上界）；中点成功就记分配并置 lo=t，失败置 hi=t。无须成功标签单调：不变式 hi>V，最后 lo=hi−1≥V，所以保存的分配效用≥cV。若 V=0，初始零分配已满足保证。只需 O(log(U+1)) 次调用，目标位长与每次精确有理 LP、加和及比较均多项式。此处补的是未知目标接口，不重证外部定理。

原始链接：

<https://arxiv.org/abs/1807.07189v4>

<https://arxiv.org/html/1807.07189v4> （§1、Theorem 3、§2 Algorithms 1/2 与 Lemma 8、§3、§4）

<https://arxiv.org/pdf/1807.07189v4>

## 6. 保留的审查义务与范围

当前证明是“已知 restricted Santa 算法 + 显式新接口”的条件导入；未实现 Santa 黑盒，未声称全篇原始文献已重新证明，全球新颖性未核验。本文件没有读取作者证明，因此之后对作者稿的一致性/差别应另写，不能回填本文件为读前已发现。

必须另作有限 exact arithmetic 检查：零项、W<1 baseline、同资源异值、dummy 恰少一件、重复 incidence、巨大分母以及最终两段不等式。有限检查不证明一般结论。若 formal Claim 允许 G=∅，需单独记零分支并避免保留错误的中间不等式；若 private/resource 可同名合并，本证明不适用。
