# 36 客户指定完整策略的 SUMmin 全混合预算：独立复核

复核身份：Boss7；日期：2026-11-16；副本：`/workspace/scratch/3a7354feb634/co-work-anl-boss7`。

**结论：Boss3 关于本分支的新增数学成立。** 原 36 客户输入和原完整策略 σ 的实际叶为 z=(0,3,4)，收益 (10,12,12)，W=34。六个真实完整三槽背景的额外查询价格依次为

\[
\bigl(K(0,z),\ldots,K(5,z)\bigr)
=\left(\frac{20}{3},\frac{35}{4},\frac{35}{4},\frac{22}{3},\frac{22}{3},\frac{19}{2}\right).
\]

每行都可强制本行的 actual 动作，使完整终局仍为同一个 z。因此对这份固定 σ 及**同一个任意**混合查询 p，

\[
\sum_{i=1}^3R_i(p)\le 3\mathbb E_{T\sim p}K(T,z)
\le\frac{57}{2}<34,
\qquad W-\frac{57}{2}=\frac{11}{2}.
\]

这是全 p 的解析预算，不是保存查询点的有限检验。57/2 是本论证给出的充分上界，本审没有求 max_p Σ_iR_i(p)，也不声称此上界取到。未发现此 36 客户推导需要数学修补。

## 实际阅读和操作范围

本审全文读取 `AGENTS.md`、`prompts/03-map-worker.md`，并读取 `research/IMPLEMENTATION.md` 的数学登记、第三阶段建边、whole_result/contribution、accepted conditional 和定向替代范围。本审未按通用工作流操作 Git 或队列，服从本次更窄的只读数学复核授权。

数学正文及证据的实际范围如下；“全文”只指表中明确列出的单个文件。

| 路径 | 实际阅读范围及用途 |
| --- | --- |
| `research/workspaces/map-v2/Boss3/final-review-20261116/summin-conditional-review.json` | 全文；本审只判断其中独立 36 客户分支，不复核一般 n 编译族。 |
| `archives/customer-attraction/state/反例/三人聚合末位保底--反例.md` | 全文；输入、五类终局、完整策略、弱平局、θ_3 与被否命题。 |
| `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | 全文；共同标签目录、全部有序历史、同一 σ 的真实续局、重复动作和弱最优性。 |
| `archives/customer-attraction/state/候选/全槽逐行最小价格的共同预算与有限报告--候选.md` | 全文；Zi(A)、K_i、R_i、同一 p 和一般开放预算的精确定义。 |
| `archives/customer-attraction/tools/evidence/aggregate-security/original/examples/customer_attraction/aggregate_theta_failure.json` | 全文；原 18 种客户类型和三人、六标签输入。 |
| `archives/customer-attraction/tools/evidence/aggregate-security/original/evidence/certificates/customer_attraction/aggregate_theta_failure.json` | 全文；43 个有序决策节点动作、实际叶和原证书数值。 |
| `research/registry.json` | 只提取 36 客户反例和 SUMmin 候选两个精确对象记录；不声称审读全 registry。 |
| `tools/research_runtime.py` | 235–310 行；accepted 逻辑边、contribution 和 finite 源必须 conditional 的现行结构约束。 |
| `research/operations/map-v2/tasks/boss3-summin-budget-repair-d86bee169e3617da.json` | 全文；只确认正式 repair 的声明范围，不认领、刷新或修改。 |

只运行一次标准库 Fraction 小算术：核 18 类型、43 动作键及公式策略一致，重算五类代表终局、actual 收益/覆盖、六个查询的负载直方图及三个 actual 动作列。没有求解 LP/MILP，没有重跑 SPE 大树或原优化器，没有核算一般 n 反族。

## 原输入、完整策略和 SPE 的解析复核

目录标签为 X={0,1,2}、Y={3,4,5}，原 JSON 中每个跨组二元类型 {x,y} 恰有 1 个客户，共 9 类；每个“两 X、两 Y”类型恰有 3 个客户，共 9 类。因此是 18 个互异类型、36 个不同单位客户；三人、六标签，均与原正文相同。每标签覆盖 3+18=21 人。任取全部三个 X 标签即覆盖所有 36 人，故 OPT_3=36。

用这些类型直接计算收益 Σ_{B∋a}r_B/c_B，得到下表，完全复现原正文的五类代表值。按组内置换、组交换和终局位置置换，它们覆盖所有终局类型。

| 代表终局 | 各位置收益 | 覆盖 W |
| --- | --- | ---: |
| (0,1,2) | (12,12,12) | 36 |
| (0,3,4) | (10,12,12) | 34 |
| (0,0,1) | (9,9,15) | 33 |
| (0,0,3) | (25/3,25/3,37/3) | 29 |
| (0,0,0) | (7,7,7) | 21 |

原证书的动作键集合恰为全部长度 0、1、2 的有序历史，基数 1+6+36=43，无缺键或重复键。逐键比较确认它恰是以下同一 σ：根选 0；历史 (a) 后选 a 相反组最小标签；历史 (a,b) 后选 b 组中最小且此前未出现的标签。第三步至少存在一个候选，因为组大小为三，而此前至多出现两个不同标签。

完整 SPE 的核验不只检查 actual 分支。由上表逐类可得：

| 第三人前缀类型 | 候选动作和第三人收益 | σ 的选择 |
| --- | --- | --- |
| a=a | 复制 a 得 7；同组新标签得 15；异组标签得 37/3 | 同组新标签，15 最大。 |
| 同组不同 a,b | 复制已有标签得 9；同组第三标签得 12；异组标签得 10 | 同组第三标签，12 最大。 |
| 跨组 a,b | 复制已有标签得 25/3；任意未用标签得 12 | b 组未用标签，是弱平局最优动作。 |

这三种前缀类型穷尽全部 36 个末位节点和其全部合法候选动作。对任意首标签 a，第二人复制 a 时，指定第三人取同组新标签，第二人得 9；第二人选择任一不同标签时，按原第三人策略续局均得 12。因此原第二人所选异组标签是弱最优，不要求唯一性。首人无论选哪个 a，原后两人均取其相反组两个不同标签，首人均得 10，根选 0 亦为弱最优。全部 43 个节点均满足同一 σ 下的逆向最优性，包含重复和离轨历史；没有冻结 actual 后继进行比较。

从根按原证书行动确得 (0,3,4)，收益 (10,12,12)，W=34；与证书 `root_history`、`root_payoffs`、`welfare` 相同。本论证允许全部历史的弱平局，并没有通过另选平局或换 SPE 获得预算。

## 六个额外查询价格的独立重推

固定 z=(0,3,4)，令每个兴趣类型 B 在实际叶的负载

\[
c_B=|B\cap\{0,3,4\}|.
\]

这里 z 三标签不同，所以计数可如此写；计算的一般定义仍是按实际三槽逐个计数。对于查询标签 T，令

\[
h_{T,k}=\sum_{B\ni T,\ c_B=k}r_B\quad(k=0,1,2,3),
\qquad K(T,z)=\sum_{k=0}^3\frac{h_{T,k}}{1+k}.
\]

以下每行 h 的总和均为 21，核对了每标签客户总量。为便于复算，同时列出 9 个二元类型和 9 个四元类型的两部分贡献。

| T | (h_0,h_1,h_2,h_3) | 二元类型贡献 | 四元类型贡献 | K(T,z) |
| --- | --- | ---: | ---: | ---: |
| 0 | (0,1,14,6) | 7/6 | 11/2 | 20/3 |
| 1 | (1,8,9,3) | 2 | 27/4 | 35/4 |
| 2 | (1,8,9,3) | 2 | 27/4 | 35/4 |
| 3 | (0,5,10,6) | 4/3 | 6 | 22/3 |
| 4 | (0,5,10,6) | 4/3 | 6 | 22/3 |
| 5 | (2,7,12,0) | 5/2 | 7 | 19/2 |

例如查询 0 的二元贡献为 1/3+1/3+1/2=7/6。含 0 的四元类型中，两类实际负载为 3、四类负载为 2，每类重数为 3，所以贡献 2·3/4+4·3/3=11/2，合计 20/3。其余标签可逐行用所列负载直方图复算。对称只用于解释 1 与 2、3 与 4 的等价，没有把 θ_3 或收益 u_i 当作 K。

## actual 动作列给出的全 p 预算

原定义要求每行从原 actual 前缀出发，强制 A 后沿同一完整 σ 完成全部三槽。对三个实际动作分别有

\[
Z_1(0)=(0,3,4),\qquad
Z_2(3)=(0,3,4),\qquad
Z_3(4)=(0,3,4).
\]

前两式确实调用原 σ 的后继，第三式是末位强制；三式均保留强制者，没有删成两槽背景。这也是更一般的事实：对固定完整 σ，任一行强制它的 actual 动作会沿同一历史返回 actual 叶。

令 p=(p_0,…,p_5) 为任意目录分布，所有行使用同一个 p，定义

\[
g_p(z)=\frac{20}{3}p_0+\frac{35}{4}(p_1+p_2)
+\frac{22}{3}(p_3+p_4)+\frac{19}{2}p_5.
\]

因为每行最小化菜单包含上述一列，R_i(p)=min_A E_pK_i(T,A)≤g_p(z)。选择的列 A 分别为 0、3、4，固定于该行，既不依赖抽出的 T，也不要求各行使用同一个动作标签。求和后由 p 非负且和为一，g_p(z)≤max_TK(T,z)=19/2，从而得到全文开头的 Σ_iR_i(p)≤57/2<34。

这一步没有交换 min 与期望，没有假设所有互斥离轨枝共同实现，也没有要求逐行 R_i≤u_i。此上界甚至只用三个已有 actual 列，不需要算其他列或求最优查询分布。

## 逻辑范围、现行 finite 状态与集成接口

这只证明**上述 36 客户输入、上述明确完整 σ** 的 SUMmin-full；它不是对该输入全部完整 SPE 的全称结论，更不是对全部三人或任意 m 的全称结论。原反例仍给 θ_3=12、W=34<3θ_3=36：从末位比较看，重复两槽背景最佳回复为 15，不同两槽背景最佳回复为 12，故 θ_3=12。θ_3 是两槽纯背景后再最佳回复的值；本审 K(T,z) 是固定三槽终局外的查询价格，二者不能替换。

因此此分支实际满足 SUMmin，不能用来反驳一般 SUMmin；指定三人分支的确认也不证明一般 SUMmin 或一般六人 half。已有 SUMmin⇒half 条件链的接口是：对所需实例和每份完整 σ，先有同一 W 的全 p 共同预算，再接完整 m 槽静态比较。此处只支付一个指定的 m=3 输入/σ，未满足六人原题的全称前提。本审不重证已完成的条件链。

当前读取的登记记录为：

| 对象 | version | truth_status |
| --- | ---: | --- |
| `customer-attraction/three-player-aggregate-last-floor-counterexample` | 1 | finite |
| `customer-attraction/e7-summin-full-common-budget-exact-discount-and-finite-tests` | 2 | open |

源正文虽给解析证明、且本审已核原输入与完整策略，当前图端点的正式状态仍为 finite。本次不改登记。按 `tools/research_runtime.py` 300–301 行，accepted 逻辑边只要源不全在 definition/proved 中，就不能标 unconditional。因此若正式 repair 保持当前端点，36 客户新边应是 `kind:implies`、`status:accepted`、`premises_mode:all`、`relation_mode:conditional`，并使用 **contribution**：

- `result` 精确写指定输入和指定 σ 的“∀同一 p，Σ_iR_i(p)≤57/2<34”，条件明确绑定原输入、原完整策略、actual 前缀、真实三槽续局。
- `remaining` 明确写一般 SUMmin 仍需对全部有限共同目录实例、全部完整 σ 和相应人数证明预算；此固定三人分支没有完成目标整条陈述。

这里 accepted 表示局部推导完整，conditional 保留现行 finite 源的正式前提地位；二者没有矛盾。它不能写成一般目标的 whole_result，不能标 refutes，也不能以 accepted 擅自把 open 目标或 finite 源升格。若日后另行更新源状态，需按正式登记改版流程处理，本审不预设发生。

本审读到了 repair 任务的本地快照；其 `definition.goal` 明确要求两条独立局部预算与保留原条件链。读取时 `map/edges/boss3-summin-budget-repair-d86bee169e3617da` 目录尚不存在，文件名定向检索也未命中新边。因此本审没有审定任何尚未落盘的新 edge、收据或绑定；本地任务 state 不被当作远端实时交付状态。后续正式资产成熟后，root 仍需核其确切措辞、端点及证据绑定、原三资产去向和真实 done，之后再做 canonical 集成。

## 可复核绑定与剩余事项

本次关键实读字节 SHA-256：

| 文件 | SHA-256 |
| --- | --- |
| Boss3 `summin-conditional-review.json` | `82792be5888d09d9822fa21b9794e8b149932d340f6b0aaff61cc778bc424c15` |
| 三人聚合末位反例正文 | `f2ff6b486d46f5e05d9acb2497ec1114ac8ab4698460fb46656d320e640fe4c0` |
| 原输入 `aggregate_theta_failure.json` | `be0e1a54d3a7ddfeba327c03ce1975932e8fd1018926147b9c555fe6af180aaf` |
| 原 43 节点证书 `aggregate_theta_failure.json` | `cf08edab0813de8eccee8d5466d15b40bd42c980da9b0b68c925f4ae80991010` |
| 共同目录完整历史模型正文 | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` |
| SUMmin 候选正文 | `e952c73849b2ac561ac4ebb761b3ae0c1af06d61f27e743c593ea0103c52698a` |
| 当前 registry 快照 | `202c608164e5e7f706c6178d16a0f13089c01abf7b7fdc3cc5b091370fb1f4a8` |
| `tools/research_runtime.py` | `414713215bc28a062a2ef0330b150f81298987e893278fe90b44b38c7f4d4023` |
| 正式 repair 任务本地快照 | `6b62a81c994b20b0e0052a1280ca0e74736d69e10e3de2e76edf3c81c17fbeed` |

剩余事项是正式 repair 的提交与集成核对，以及目标原有的一般数学开放义务；不是本分支新发现的证明缺口。本审未读凭据或连接器，未执行 Git/sync/queue/checkpoint/公屏，未改旧文件，唯一写入为本审查文档。
