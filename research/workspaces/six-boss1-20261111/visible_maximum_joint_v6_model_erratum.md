# v6 冻结模型更正：X 保留实际前四背景的全目录最大潜力条件

Boss1；`six-boss1-20261111`。编写席：`/root/visible_joint_v6_prepare`。
本页按 Main 的后续明确要求，作为冻结包之外的独立模型更正。后续读取 v6 完整输入时，须将本页与冻结模型合同合读；下列两处关于全局 X 的错误表述以本页为准。冻结包内文件、完整输入和原冻结清单均不改写。

## 1. 更正对象与准确替代解释

冻结文件中的两处原句如下。

| 冻结位置 | 原句 | 更正后的全局含义 |
| --- | --- | --- |
| `visible_maximum_joint_v6/model_contract.json`，顶层键 `X`，第 536 行 | `arbitrary legal label; no new optimality or maximum-potential assumption` | X 是在给定完整纯 SPE 的同一 actual 路径前四动作负载 P 下，一次选定的全目录最大 `f_P` 合法标签；继承父输入所需的该最大性。 |
| `visible_maximum_joint_v6/source_review.md`，§1，第 18 行 | `X为任意合法标签` | 全局 X 按下述 `argmax f_P` 定义选取；任意合法标签的量词只用于新增局部来源的 T 接口，不能覆盖父系统对 X 的定义。 |

第一句的 “no new … assumption” 不能被解释为取消原有最大性；整个句子作为完整模型描述过宽。完整 4177 行系统没有被证明对任意选取的合法 X 都成立。准确的结论是：对每个原模型实例及其给定完整纯 SPE，按原定义选出 X 后，所有已准入来源在同一个模型中成立。

冻结对象身份为：

| 对象 | SHA256 |
| --- | --- |
| v6 `exact_input.json` | `8f953bca6b65a8093d5fcf0fdb5a432ba3603137fe1015cd06fc8f6324e68769` |
| v6 `freeze_manifest.json` | `0aa45d8f1517b6958ae6187b5ebbf89a3ea31926347d997a696fe20fd4b35da2` |
| v6 `SHA256SUMS` | `15efcb6c531412464a490fab6bb62b2c2869da526b06b79dc596e80f135d33d7` |
| 被更正解释的 `model_contract.json` | `9f40a6906054e52804aa9d6f6e75379645a49ed53c2367be3390d0288301251a` |
| 被更正解释的 `source_review.md` | `95c4ada9588a6aa03f39e3cbbb0870413071b09c4ce6ca94f72fa6dcd80a3433` |

## 2. 原有 X 的精确定义

采用正式[共同目录完整历史模型][D]：有限单位客户集 N，有限非空合法标签目录 S，允许空覆盖、同覆盖异标签和重复行动；一份完整纯策略在每个合法有序历史上给出动作，SPE 比较使用该固定策略的真实续局和弱不等式。标签身份与有序历史不作合并。

固定恰六人的一份完整纯 SPE，记其 actual 动作为 A1,…,A6。对每个客户 y，定义同一 actual 路径的前四负载

\[
P_y=\sum_{j=1}^{4}\mathbf 1_{\{y\in\operatorname{cov}(A_j)\}},
\qquad
f_P(Q)=\sum_{y\in\operatorname{cov}(Q)}\frac{1}{P_y+1}.
\]

然后一次选取

\[
X\in\operatorname*{arg\,max}_{Q\in\mathcal S}f_P(Q),
\qquad F_X=f_P(X).
\tag{X}
\]

这正是最初可见 C 联合层的来源审查 §1 的定义，[P0] 以及正式共同最大潜力引理 §1、式 (2) 的选择。[L1] 有限非空目录保证存在；不要求严格最大值、正客户数或唯一最大者，任意弱平局选择一个即可。同一个 X 的会员位用于所有客户型、所有查询及各强制动作分支，不能逐客户、逐查询或逐分支重新选择。

式 (X) 的背景始终是该 actual 前四动作所产生的 P。它不声称 X 在根的零背景、强制改选 X 后的另一前缀，或任意其他合法历史的背景下仍最大。即使另一历史具有相同负载，实际续局仍由原完整策略在该有序历史上的取值决定。

另取

\[
C\in\operatorname*{arg\,max}_{Q\in\mathcal S}
|\operatorname{cov}(Q)|.
\]

C 才是达到全目录最大裸覆盖的合法标签。X 的定义是带权潜力最大，不能改写成裸覆盖最大；C 不因此获得 `f_P` 最大性。X、C 可以相同、可以是同覆盖异标签，也可以完全不同。[P0]

在正 OPT6 的归一化中，客户重数、收益、F_X 和最大裸大小 K 一同除以 OPT6，P 的整数负载定义不变。这一共同正缩放不改变 X 与 C 的最大者。O 保持冻结合同中已经明确的最优六合法标签覆盖并；OPT6 为零时原实例直接处理，不形成归一化的 0/0。

## 3. 继承行为什么需要该条件

本次只读核对确认：v6 的前 3056 个完整 raw 行对象与冻结 v5 的 3056 个对象逐项相等。下列位置均采用零起始 raw 索引。

| raw 索引 | 原行名 | 与 X 最大性的关系 |
| --- | --- | --- |
| 218 | `TRUE_X_TAIL_CUT` | 同一 actual-P 的最大性支付真实分支标签 Y 的潜力预算，并支付 actual RC 中真实末回复的潜力上界。 |
| 875 | `FMAX_C` | 使用 `F_X − f_P(C) ≥ 0`。 |
| 876 | `MX_C` | 使用 actual 第五人的真实偏离 IC、真实末回复的 BR，以及 `F_X − f_P(R_C) ≥ 0`。 |

`FMAX_C`、`MX_C` 和相关 RC 行的来源与假设在最初可见 C 联合层审查 §4.1–§4.2 中已明写。[P0] 例如令 `D_y=P_y+1`、`x_y` 为 X 的会员，MX 的结论为

\[
u_5\ge\sum_y\frac{c_y}{D_y+x_y}.
\]

该证明中的 X 最大性不能由 “C 合法” 或 “X 合法” 替代。

对 `TRUE_X_TAIL_CUT`，正式承重证明固定 actual 历史 `(A1,A2,A3)`，强制第四人选这个同一 X，再沿原策略取得真实第五、六标签 Y,T。它同时保留两个不同分母：actual 的 `D=P+1`，以及强制分支的 `h=a1+a2+a3+x+1`。[L2, §1–§2]

六预算中权重 800 的预算是

\[
f_P(Y)\le F_X,
\]

这里的 Y 来自强制分支，但潜力按 actual 的 P 评价。权重 900 的预算来自 actual 前四历史上的 RC：对合法 Q,R，

\[
f_P(Q)+f_P(R)-g_P(Q,R)\le u_5+F_X,
\quad
g_P(Q,R)=\sum_y\frac{q_y r_y}{(P_y+1)(P_y+2)}.
\]

其支付项包括 `F_X−f_P(V_Q)≥0`，其中 V_Q 是 actual 第五人改 Q 后的真实末回复。V_Q 不被强制等于另一分支的末回复。两项合计给切式中的 `1700 F_X=(800+900)F_X`；因此这个全目录最大性是来源证明的实质假设。[L2, §2、§4]

父系准入页 `universal_union_wallet_v2/source_review.md` §3 已把该最大性分别标为 “同一actual-P最大性MAX(Y)” 和 “actual RC(T,Omean)”。[P1] Main 对该六预算投影的独立检查记录为 `PASS`，范围是 256 类型、1024 个四态值，K 系数为 71，并明确记为已准入该父系统。[M1] 该检查验证的是带这些来源假设的切式，不会把其中的最大性假设消除。当前 raw 218 保持 K 系数 71；后来加入可见 C 位只是忠实拉回，不能改变证明的前提。

v5 的最终 Main 来源审查确认完整 3056 行准入、旧行原样继承、513 个非负变量、两个等式和 30 个 `rhs=−1` 均保留。[P2] 其冻结清单绑定父输入
`12f456dfbc789a5c1826d248e4851b84f66b428554d181b7ba12cbfdb920f3ac`。
v6 继续逐对象继承这一整块，因此也继承其中各来源的模型条件。

## 4. 新增局部 T 量词与全局特化

新增 λ/δ 局部来源中，适用的一般 T 接口允许任意合法标签，不要求 T 自身为最大潜力标签；C-only 来源另按其原证明使用固定 C 和既有 C 等式。这个局部量词继续成立。

对完整 v6 输入，先在给定原实例与 actual 路径上按式 (X) 选定全局 X，再在需要 X 作为查询目标的新增局部来源中取 `T=X`。因为这样的 X 是合法标签，局部结论可以直接特化；局部证明不需要最大性，不等于已经依赖最大性的旧 3056 行也能取消最大性。其他实际动作或 C 目标按各来源原有路由处理。

这恢复的是原系统一直使用的辅助标签选择，并未对原博弈增加限制：每个有限非空目录和每条给定 actual 路径都存在这样的 X。完整矩阵是该原模型的必要约束系统；这不声称任意非负矩阵可行点都能实现为完整 SPE，也不声称有限矩阵逐一编码了整个未知目录的全部比较。

## 5. 完整输入与冻结不变

更正只改变上述两句的模型解释。完整系数、元数据、顺序、源 ID、数值除数、目标、两个等式和独立 K 列全部不变。原顺序仍为

\[
3056+230+160+550+180+1=4177.
\]

前 3056 行连同其原尺度保持原样；1120 条新增 λ/δ 行的数值除数仍为 25；最后 Main 根严格行的数值除数仍为 1。原重复行、零型行及全部 513 个非负列保留。该更正不触发重新装配，不改变 `model_contract_sha256` 的冻结字节绑定；该绑定指向第 1 节已定位的原合同，解释修正由这份旁挂页独立提供。

写本页前已只读复核 v6 `SHA256SUMS` 的全部 35 项，全部通过；输入、冻结清单及校验清单 SHA 与第 1 节一致。写本页后再做同样的只读校验，并单独报告本页 SHA。没有优化器调用，没有修改 Git、RUN、map、registry 或已冻结来源。

## 6. 实读来源与 SHA 绑定

本页的数学范围以以下正式正文、父系准入和 Main 检查为据。路径相对于仓库根；链接相对于本页。

| 标识 | 来源与定位 | SHA256 |
| --- | --- | --- |
| D | `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md`，输入、完整历史策略量词与真实续局 | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` |
| L1 | `archives/customer-attraction/state/引理/共同最大潜力主题的末两位容量投影--引理.md`，§1 式 (2) 的一次性最大潜力标签选择 | `59b65b69603451171497184bc8654d964ae69a5d4e76b305c1a4ca13114e0ed5` |
| L2 | `archives/customer-attraction/state/引理/共同最大潜力主题的两尾跨实际钱包投影--引理.md`，§1–§2、§4 | `eccbb5b921c02db0551f51b002c7e9682b57e9cb82a947eaff02e10e3c7cc0f7` |
| P0 | `research/workspaces/six-boss1-20261111/visible_maximum_joint/source_review.md`，§1、§4.1–§4.2 | `e69440b5e52b528f540605a1fd3ddc833be99a48779b265e6389a9d615067b3a` |
| P1 | `research/workspaces/six-boss1-20261111/universal_union_wallet_v2/source_review.md`，§3 | `12cb88813b5d78170f25c9e77b825d2554f21de2c25733d424afd846908c605e` |
| P2 | `research/workspaces/six-boss1-20261111/visible_maximum_joint_v5/source_review.md`，完整 3056 行最终来源准入 | `94c5c4e4f9e1795ecee09dc85181e84bf2d3ee6f5a7c79d300c652c3f2db1fb6` |
| P3 | `research/workspaces/six-boss1-20261111/visible_maximum_joint_v5/freeze_manifest.json`，完整父输入与准入页绑定 | `b49d8bba4197fc6d656005770dace9c5a777816b5e3eaa1105565fb23db51a27` |
| M1 | `research/workspaces/six-boss1-20261111/main_true_x_tail_cut_check.json`，`PASS`、256 类型、1024 四态、准入标志 | `15cf53444775462b0c09cad61efdc64ccdc87553e2c88fe02b269b2b37d008c0` |

[D]: ../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md
[L1]: ../../../archives/customer-attraction/state/引理/共同最大潜力主题的末两位容量投影--引理.md
[L2]: ../../../archives/customer-attraction/state/引理/共同最大潜力主题的两尾跨实际钱包投影--引理.md
[P0]: visible_maximum_joint/source_review.md
[P1]: universal_union_wallet_v2/source_review.md
[P2]: visible_maximum_joint_v5/source_review.md
[P3]: visible_maximum_joint_v5/freeze_manifest.json
[M1]: main_true_x_tail_cut_check.json
