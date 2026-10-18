# 共享负载直方图递推恰为配置投影：条件相关性丢失的精确边界

读取目的：检查“旧全机凸表示只共用一份，各分支只拆非负坐标”是否真的保住共同容量。下述弱递推与 CONFIG 的负载直方图投影完全相同；它可计算，但可行不承诺统一小于配置阈值两倍的实际调度。`UM-TARGET-v1` 仍 OPEN。

## 1. 精确身份与对象

**ID/version：`UM-SHARED-LOAD-HISTOGRAM-CONFIG-PROJECTION-v1`。** 此正式首次身份对应 scratch Exact/专用 Proof v2；不追认旧 full Proof v1 的“每层真 hull”字面。

**Objects / Domain / Quantifiers。** 任意整数 \(m\ge1,n\ge0,K\ge0\)，有序带标签任务 \(J=[n]\)，机器 \(M=[m]\)。有限处理时间 \(a_{ij}\in\{0,\ldots,K\}\)，其余为 \(\infty\)。本整数表示允许某任务没有有限端，以覆盖阈值删边后的不可行输入。零时间任务仍是独立任务，不按负载值合并。

对每个前缀 \([j]\)，定义机器配置

\[
\mathcal C_i^j(K)=\{C\subseteq[j]:a_{i\ell}<\infty\ (\ell\in C),\ \sum_{\ell\in C}a_{i\ell}\le K\}.
\]

空配置总合法。CONFIG\(_j(K)\) 给每台机器一个该族上的概率分布 \(Y_i\)，要求每个原任务覆盖恰一：

\[
\sum_i\Pr(\ell\in Y_i)=1\qquad(\ell\le j).
\]

不同机器不假设共同 coupling。令
\(P_j\subseteq\mathbb R^{m(K+1)}\) 为其完整负载直方图投影：

\[
y_{r,s}=\Pr\left(\sum_{\ell\in Y_r}a_{r\ell}=s\right),\qquad 0\le s\le K.
\]

**Definitions：弱共享递推。** 初态 \(\widehat H_0=\{h^0\}\)，其中 \(h^0_{r,s}=\mathbf1[s=0]\)。第 \(j\ge1\) 步令 \(E_j=\{i:a_{ij}<\infty\}\)。选择
\(\theta_i\ge0,z^i\ge0\ (i\in E_j)\)，满足

\[
\sum_i\theta_i=1,\quad
\sum_s z^i_{r,s}=\theta_i\quad(i\in E_j,r\in M),\quad
\sum_i z^i\in\widehat H_{j-1},\quad
\sum_{s>K-a_{ij}}z^i_{i,s}=0.                 \tag{1}
\]

令 \(S_{ij}\) 只把第 \(i\) 行质量 \(s\mapsto s+a_{ij}\) 平移，其余行不变，输出 \(y'=\sum_iS_{ij}z^i\)；全部可输出点组成 \(\widehat H_j\)。容量面确保平移的正质量不越界。空资格或空前层使新层为空。

本定义特意**没有**逐分支条件 \(z^i\in\theta_i\widehat H_{j-1}\)。aggregate 在上一步弱集合中，而不是每一步都在真实共同调度凸包中。

**Exact Statement / Conclusion。** 对每一个上述输入、每个 \(0\le j\le n\)，

\[
\boxed{\widehat H_j=P_j.}                    \tag{2}
\]

存在系数与右端均为 \(0,\pm1\) 的显式有理 LP，其投影恰为此集合，变量和约束数均为

\[
O\big(m(j+1)(K+1)+|E_{[j]}|(K+1)\big).       \tag{3}
\]

这是数值 \(K\) 的伪多项式界；有理目标的优化另计其总编码长度。空性判定、可行点和 Farkas 不可行证书均按该显式 LP 总位长为多项式。没有假定精确整数调度 oracle。

## 2. 任意弱轨迹给完整配置

对任意最终弱点，有限次递归取其存在性 witnesses 得到整条轨迹。在阶段 \(\ell\)，对机器 \(r\) 定义

\[
\operatorname{add}_{r,\ell,s}=z^r_{r,s},\qquad
\operatorname{stay}_{r,\ell,s}=\sum_{i\ne r}z^i_{r,s},
\]

不可用 \(r\) 的 add 为0。这两者之和是旧行直方图，分别沿 \(s\mapsto s+a_{r\ell}\) 和 \(s\mapsto s\) 传送，合计为新行。由容量面，没有正流越过 \(K\)。每行从负载0发单位流，因此是带层负载 DAG 上的单位流。

逐行分解为有限路径混合。每条路径按 add 的阶段标签记录一个真实合法配置；零时间 add/stay 即使同起止点，也用不同弧变量保住任务标签。机器 \(r\) 包含任务 \(\ell\) 的概率为 \(\sum_s\operatorname{add}_{r,\ell,s}=\theta_{r,\ell}\)，跨机器和为1。因此得到完整 CONFIG，末层负载直方图正是给定点。此方向给 \(\widehat H_j\subseteq P_j\)，没有产生跨机器共同路径 law。

## 3. 任意配置给全部弱前缀

给任意 CONFIG 的每行随机配置 \(C_r\)，令阶段 \(\ell\) 的包含概率为 \(x_{r\ell}=\Pr(\ell\in C_r)\)，所以 \(\sum_rx_{r\ell}=1\)。按该行真实前缀配置定义

\[
v^+_{r,s}=\Pr(\ell\in C_r,\ \operatorname{load}(C_r\cap[\ell-1])=s),\quad
v^-_{r,s}=\Pr(\ell\notin C_r,\ \operatorname{load}(C_r\cap[\ell-1])=s).
\]

取 \(\theta_i=x_{i\ell}\)，逐行设

\[
z^i_{r,s}=\begin{cases}
v^+_{r,s},&r=i,\\
x_{i\ell}v^-_{r,s}/(1-x_{r\ell}),&r\ne i,\ x_{r\ell}<1,\\
0,&r\ne i,\ x_{r\ell}=1.
\end{cases}                                  \tag{4}
\]

当 \(x_{r\ell}=1\)，其它 \(x_{i\ell}=0\)，且 \(v^-_{r,\cdot}=0\)，故最后分段不丢质量、不除0。每分支每行总量恰 \(\theta_i\)，每行跨分支和为 \(v^++v^-\)，即旧前缀直方图；不可用行没有 own 分支，但其 \(x=v^+=0\)，其余分支仍给整行 \(v^-\)。own 行只取含当前任务的配置，非负前缀加本任务不超过完整配置容量，因此本机面约束成立。平移后恰为下一前缀直方图。

从空配置出发归纳，所有 aggregate 均属于此前构造的弱集合，得到完整轨迹和 \(P_j\subseteq\widehat H_j\)。本证明覆盖所有实概率点，而非只覆盖某一给定有理证书。

## 4. LP、位复杂度与可靠拒绝

每机设层 \(0,\ldots,j\)、负载 \(0,\ldots,K\) 的节点。每层有 skip 弧；有限端且平移不越界时另设 selected 弧。每机单位流从 \((0,0)\) 出发；末层流量就是显式 \(y\)。对每个任务再加跨机器 selected 弧总流量为1的等式。逐机路径与配置一一对应，故 LP 投影就是式\(2\)。这些跨机器等式是 side constraints，不能调用纯网络 TU 来声称该 LP 整数。

节点、弧和末层坐标计数给式\(3\)，包括 \(j=0,K=0\)。每机弧流量至多1，LP有界；标准确定性有理 LP 算法适用。整数时间只决定弧终点下标，非零矩阵元素均为 \(\pm1\)。求可行点或不可行证书的位长为显式规模的多项式；给定有理目标需再计目标编码长度 \(L_{\rm obj}\)，不使用精确实数比较。

对一般 UM 输入 \(P\)、\(T>0,n\ge1\)，固定有理 \(0<\delta<1\)，先删 \(p_{ij}>T\) 的端，取

\[
q=\delta T/n,\quad K=\lfloor n/\delta\rfloor,\quad a_{ij}=\lfloor p_{ij}/q\rfloor.
\]

固定 \(\delta\) 时 \(K=O(n)\)，所有 floor/有理运算、LP构造及证书均按原始总输入位长为多项式。若 \(\delta\) 为输入，复杂度可依赖数值 \(1/\delta\)，不称只依赖其对数。

若原实例有实际 \(T\) 调度，其所用端全部保留，逐机
\(\sum\lfloor p_{ij}/q\rfloor\le\lfloor T/q\rfloor=K\)，给 CONFIG 的点质量。因此 LP 不可行可靠蕴含 \(\mathrm{OPT}(P)>T\)。资格删空即可靠拒绝；可行则没有新的实际调度承诺。\(T=0\) 只逐任务查零端，\(n=0\) 返回空调度，不定义 \(q\)。

## 5. 四机六任务：末层全为 Dirac 仍未保真

以下直接用整数坐标，\(K=3\)：

| 机器 | \(j_1\) | \(j_2\) | \(j_3\) | \(j_4\) | A | B |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 3 | ∞ | ∞ | 2 | 1 | ∞ |
| 2 | 2 | 3 | ∞ | ∞ | 1 | ∞ |
| 3 | ∞ | 3 | 2 | ∞ | ∞ | 1 |
| 4 | ∞ | ∞ | 3 | 2 | ∞ | 1 |

前四任务在容量3下每机恰一；支持图为8-cycle，只有两个匹配，负载 \(D=(3,3,2,2)\)、\(O=(2,2,3,3)\)。前四步可由这两份完整前缀调度各半取得。

CONFIG 证书：每机各半概率取以下两配置：机1 \(\{j_1\}/\{j_4,A\}\)，机2 \(\{j_2\}/\{j_1,A\}\)，机3 \(\{j_2\}/\{j_3,B\}\)，机4 \(\{j_3\}/\{j_4,B\}\)。每配置负载3，每任务覆盖1；因 \(j_2\) 两端均3，配置阈值恰3。

从前四步各行负载2/3各半的点，放 A 的分支1/2各取质量1/2：own 行全取负载2，另一候选行全取3；机3/4在每分支各取1/4的2与1/4的3。平移后，机1/2恒3、机3/4各半2/3。这不是实际 \(H_5\)：真实 A 只能从 O 放入，故真实 \(H_5\) 的机3/4恒3。

弱递推继续从此 \(\widehat H_5\) 放 B，分支3/4各取自己的负载2，另一候选行取3，机1/2取3；平移后每行都为负载3的 Dirac。若强制从真实 \(H_5\) 取 aggregate，两个 B 分支反而都为空；不能混称这两个系统。

实际最优值恰4：若峰小于4，前四任务仍必须一机一件；D阻塞A，O阻塞B，均至少3+1。反向用D、A→1、B→3达到负载 \((4,3,3,2)\)。六件全部执行一次。将时间和容量同时除3即原有理展示的 CONFIG=1、实际OPT=4/3；这只是精确缩放。

## 6. 真共同状态、既有 gap 和准确否定范围

令 \(\Phi(u)_{r,s}=\mathbf1[u_r=s]\) 为各机负载的一位编码。若保留真实容量 \(K\) 可行的共同前缀状态凸包 \(H_j=\operatorname{conv}\{\Phi(L(\sigma))\}\)，容量测试是坏负载坐标为零的非负暴露面；此面内所有正原子都可扩展。精确分支需要 \(z^i\in\theta_iH_{j-1}\)，不能仅用各行质量和一个 aggregate 查询代替。这是充分的共同相关性，尚无一般位多项式生成/查询/解码算法；多项式环境维度本身不提供它。参见[前缀原子解码接口](succinct_prefix_atomic_decoding_bridge.md)。

式\(2\)只关闭本页精确定义的递归弱化。[经典模型与配置间隙](model_and_classical_barriers.md)中的 CONFIG 趋二族，经上述向下舍入仍有合法配置，因此也通过本页 LP；任何“该 LP 可行就相对原配置阈值统一输出 \(<(2-\varepsilon)T\)”的合同均不能成立。它不否定相对真实 OPT 的一般算法，也不否定使用额外输入信息、重开分支或其它共同表示。

**Assumptions / Dependencies。** 集合恒等式和计算合同无复杂度假设，仅承重本页完整递推定义、有限路径分解和标准有理 LP；方法边界另调用既有 CONFIG gap，不把有限例子作为一般 gap 证明。有限四机矩阵为显式反例，不充当全输入证明。

**Evidence / Counterevidence / Objections。** Exact v1 曾先行独立重构；随后作者实际读后发现旧 full Proof 的 true-H 字面错误与 \(j=0\)、目标位长措辞问题。原字节和勘误保留，专用 v2 修复后作明确实际读后，不重新称盲审。本正文采用修复对象并直接给整数例；实际审查、版本哈希及原有限核验范围见[审查记录](../../reviews/unrelated_machines/shared_load_histogram_recursion_equals_configuration_projection_review.md)。

**Status / Scope / Related Files。** 数学证明完整；实际审查次序与范围以所链记录为准；没有实现一般 LP 求解/调度 finder，未外审，全球新颖性未认证。本文不采用另行探索的 fixed-k 联合层次、PHP、tensor rank 或拟阵结果，也不把旧 full Proof 全文升级。UM-TARGET-v1 仍 OPEN。
