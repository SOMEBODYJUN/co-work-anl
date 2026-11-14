# 七客户基准查询：完整策略、遗漏总题与回复闭包边界

本包的 whole result 是一个精确的有限边界结论：在五名单位提供者、七个带索引标签的共同目录中，固定保存点的完整有序策略在全部历史上对基准查询集 (J=\{0,1,2,3,4\}) 的 14005 条真实偏离行全部非负，且标签 5 的 2801 条行也全部非负；但全七标签的 19607 条行中有 2089 条严格负项，全部来自遗漏总题 6。因此“完整保存策略 + 全部历史上的基准字母表 IC”不能推出该策略是完整纯 SPE。根节点标签 6 的真实后继给收益 2，而规定标签 0 给收益 1，是直接的严格反例。该点的 (W=5,\operatorname{OPT}_5=7)，所以 (\operatorname{OPT}_5/W=7/5) 且 (2W-\operatorname{OPT}_5=3>0)；它不构成 half 反例。

## 实读与证据边界

任务 `customer-attraction-3a-3a-3abb0916925eba1f` 的对象 pin 为
`148640666d17985b801b5dc242774e8af08a86ddb15404611e25ecf3314e715c`。本轮完整阅读并核对了任务声明的五个 reading refs：

* `archives/customer-attraction/state/计算/七客户基准查询部分行的完整策略与遗漏总主题--计算.md`，SHA256 `4f2c981a79255c6df7c37017e8437c7ce0e82e9f123898cf5f33321098ce7418`；
* `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md`，SHA256 `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88`；
* `archives/customer-attraction/state/程序/基准字母表限制的原有限审计与三次保存点--程序.md`，SHA256 `eca65ad21848a99c50ca816a2f2829ca5e8387ac9b437f77927bc61ffd155d49`；
* `archives/customer-attraction/tools/evidence/ra0-tree-transport/full-reading.md`，SHA256 `07e296e7703e155efceb30fdd0afc6f50a5e6d469ab11a6237375abb9bd9d79e`；
* `archives/customer-attraction/tools/evidence/ra0-tree-transport/fixed-seven-client-all-history-profiles.jsonl`，SHA256 `479da7e6cdc570a6dfb5443d71a7a9d45733e12cabed5553ea00c6cd2e1955c7`。

我还读取了 deferred 的 `CAG-MODEL`（definition pin `3216d1db43ff83e0e0c9cf2479e79611277c9d9291a68e7f9b85ec4bb299dc5c`）、全历史最优比较字母表障碍（pin `18f1360db6164427d2cd68abba6ffaa7dab2d435e25148edc0400caf2871960e`）以及回复闭包引理（pin `0f33a623a2ceea9a2698288c80d4254a7fe2f20832f0869fc9921867f719dcd0`）。CAG-MODEL 仅提供共同目录、均分收益、完整有序历史和纯 SPE 的定义，不承担本包任何推导；没有为共享定义建立 hub 边。

## 模型和有限策略

五个 H 客户记为 (H)，另有单位客户 (s,t)。七个标签的覆盖是

\[
S_0=S_3=S_4=S_5=H,\qquad S_1=\{s\},
\quad S_2=\{t\},\quad S_6=H\cup\{s,t\}.
\]

重复覆盖标签保留索引，不能先商掉；标签 6 是 H 与两个私客的总主题。保存质量为 (w_{66}=w_{68}=1,w_{121}=5)，即原质量尺度中的 (1/5,1/5,1) 清分母 5 后的七单位输入。基准查询集 (J=\{0,1,2,3,4\}) 覆盖全部七客户，因此直接有 (\operatorname{OPT}_5=7)，不需要把 LP 中原本未强制的 OPT 约束倒填为前提。

完整动作表对每个有序历史 (h\in\{0,\ldots,6\}^{<5}) 给出一个动作，共
\(1+7+49+343+2401=2801\) 行。实际叶为 ((0,0,3,4,4))，每名提供者收益 1，福利 (W=5)。我没有把有序历史压成计数策略，也没有用 actual 路径替代离轨节点。

## 全历史精确核验

逐行解析 fixed-seven profiles 后得到下列不重叠计数：

| 查询标签 | 负 IC 差 | 正 IC 差 | 零 IC 差 |
| ---: | ---: | ---: | ---: |
| 0 | 0 | 712 | 2089 |
| 1 | 0 | 2616 | 185 |
| 2 | 0 | 2660 | 141 |
| 3 | 0 | 712 | 2089 |
| 4 | 0 | 712 | 2089 |
| 5 | 0 | 712 | 2089 |
| 6 | 2089 | 0 | 712 |

所以 (J) 的 14005 条行是 (0) 负、7412 正、6593 平；标签 5 也完全安全；全目录则有 2089 条负项。根行保存为规定动作 0，七个强制收益为
\[
(1,1,1/2,1,1,1,2),
\]
故标签 6 在根处就给出严格改进，根 IC 差为 (-1)（原质量尺度为 (-1/5)）。固定策略不是全目录纯 SPE。profiles-summary.json 保存了这些计数、深度分布、根行、动作计数和闭包见证；它不是新的数学对象，只是本轮的可复核 support。

该反例边界必须保持：它只反驳“受限 J 行（即使加标签 5）足以认证完整 SPE”这一推理；它不反驳共同目录模型的 SPE 存在性，也不反驳任何完整目录半福利定理。(W=5)、(\operatorname{OPT}_5=7) 明确给出半界剩余 3。

## 原有限审计的保存语义

原有限审计的四个 (m=1,2,3,4) 全树记录、36090 个任意背景标量检查和五个大 (m) 算术摘要已按正文核对。它们说明 benchmark 模板的 self 行、离轨历史和“只漏总题”的程序合同，但不是本七客户点的第二份完整策略。七客户 step 0 是唯一带有精确质量和 2801 动作表的保存点；step 22 和 step 30 的 `exact:false` 记录没有 masses/actions/audit，不能通过巨大有理数重建完整策略。原生成器、LP、规范 solver 与旧审计均未在本轮重跑。

## 回复闭包桥

以 (C_0=J) 做完整有序回复闭包时，动作表直接给出
\[
\sigma(0,3)=5,\qquad \sigma(0,0,0,0)=6.
\]
因此闭包加入 5、6，且 (C_*=\{0,1,2,3,4,5,6\})。这与回复闭包引理的精确边界吻合：只有当所有由 (J) 生成的回复都纳入，并且闭包目录内每个动作的真实后继 IC 都非负时，限制策略才等价于新目录游戏上的完整纯 SPE。当前点的闭包就是全目录，标签 6 根行仍为负，所以引理不认证该策略，也没有把“闭包存在”误写成“福利付款存在”。

## 与全参数障碍的关系

全历史最优比较字母表障碍使用 disjoint blocks (J_i,A_i) 与 union action (R) 的显式 (m)-参数族，证明 (\operatorname{OPT}/W=m/H_m) 无界，并明确根改 (R) 获利，所以同样不是 SPE/half 反例。七客户点不是该族的参数实例：它有两个遗漏标签、同覆盖 H 的重复标签和不同动作表。两者可作语境上的 boundary check——“完整保留选定字母表行仍漏掉真实回复动作”——但不能建 `specializes` 或 `implies` 逻辑边，也不能把七客户的 (7/5) 外推成无界族。此包保留一条 context `checks` 边指向该障碍，专门记录这一同机制而非同构输入的核对。

## whole_result / contribution / remaining

* **whole_result（本对象）**：固定七客户质量和完整 2801 行策略已由成熟精确 profiles 绑定；对 (J\cup\{5\}) 的全部真实历史偏离非负，但标签 6 有 2089 个严格负项，根行已给出 1 到 2 的改进。因此保存策略不是完整 SPE；(W=5,\operatorname{OPT}_5=7)，无 half 反例。
* **contribution（本包）**：独立解析 profiles 的行数、正负零分布、根负项、动作表 closure 见证，并把它们与回复闭包引理及全参数障碍逐项对齐；新增 support 仅为可复核摘要。
* **remaining（未支付）**：没有为 step 22/30 恢复精确质量/动作；没有证明一般闭包有统一福利付款；没有把有限点提升为任意 (m) 或完整 SPE/half 定理；没有重跑原程序或声明新的外审/新颖性结果。

没有具体的 follow-up obligation。CAG-MODEL 的共享定义已处理但不连边；障碍族与本点只作语境核对，闭包引理的适用边界由 context checks 边记录，均不改变原对象的 truth status。
