# 归一化 CONFIG 局部链的当前零 incidence 增量核验

任务：`boss2-wave9-macro-repair-3da3e018da6128bc`；身份：Boss2。source 更正已发布并进入当前任务 pins，本轮数学审读完成。本文及配套 edge/receipt 留给 Boss 对最终字节执行 native bind/check、checkpoint 与 done；本 worker 没有执行或冒称这些操作。

## 当前任务和版本边界

当前任务 definition 的规范化 JSON SHA-256 为 `a51448886eaa287b935cbc3bbad940b169cb35cb6fc0471d74f29d9fe991901b`；任务文件原始 SHA-256 为 `b97ce196efbe7f9c8f264006de758670e324a2055da0e450eceeb80bddfc953c`。本地任务为 `claimed`、owner `Boss2`，claim request 为 `2531db0de77d46cd97f21dedc8466531`。父 Boss 提供的已推送任务快照为 `37910e9d597b5f64a2a3fb33032734b927eca2cd`；本 worker 未自行查询远端、运行 Git 或访问队列。

14 core / 6 read 的全部 20 个 input pins 均按当前 registry 对象的规范化 JSON 重算并匹配。三份受影响记录为：

| 对象 | 版本 | 当前 pin |
| --- | --- | --- |
| `M-9452d445c1744d5eaac946ee974d2162` | 4 | `cddd9bf3289e55ce350e792f70fdfea147cf0b44bfc0da08d9355f0c40a48e64` |
| `M-f0619ab2e98f41eb9fa9c02a48c19aaa` | 5 | `7fe755e2d8d7e0dd39ba154180fa2f3344420f4bf0a951d533bf9e709337df8f` |
| `M-080d9b22ae87408f9a673a898c7a6dc3` | 5 | `d0b2a08064ea4ddb1eb3d096b576113c85d2effdc50f43593b10cf756e4c217a` |

对每份当前 record，减一版本、共享审查 SHA 换回 `63629abaa5cd2bcc0e42ff051936b91882ea63c711dfdac231f238763b682255`、仅删去 objections 的此次零作业说明尾句，均精确恢复上轮草稿的旧 pin。因此 object_id、title、kind、truth_status、model、statement、quantifiers、assumptions、scope、body 与 sources 未变，三个合同没有增加前提。

共同主定理正文仍为 `8bfbaa80b98546b6d1320e9760bb9491165e26a6cef1b6cd35eb86116c822f66`。共享福利/配置审查现为 `33bd31b883b26f49508808dd7175cd104f391b86642bff90ea2bce7f1142097b`；source delta 仅在 §二.1 将补集配置的“所有 positive incidence”改为“全部 incidence jobs（含零 jobs）”。它恢复主定理 §1 已有完整配方，不改变结论。

## 实际读取与继承

本轮完整实读 AGENTS、IMPLEMENTATION、worker 入口、当前任务、三个受影响的当前 registry records、现有 edge/证明 note/receipt 和四份 prior edge JSON。14 core / 6 read 的全部当前数学合同字段和 14 个 coverage 理由均逐项阅读，20 个对象 pin 已重算。

本轮完整重读共同主定理全文及本边全部五份审查 evidence：Exact/Proof 版本核验、row3/degree9 预 Exact、v1/v3 独立与作者核验、现行福利/配置双源审查、v3 三向有限证书审读范围。直接重建主定理 §1 与共享审查 §二.1 的逐 job 覆盖，并核 §2–5 的 tree/port、state-dummy、单位 SC 路径与 Q_D 合成。

当前和直接前任务 receipt 的 coverage/assets/pins/supersession/reading metadata 已核；zero-incidence-source-correction 全文，以及 zero-incidence 3D impact 的 independent_math、macro draft、provenance 部分已读。较早 3D 报告只用于其版本、资产和范围记录，不冒称本轮重读报告涉及的全部别包边或 primary。

直接前 receipt 为 `map/receipts/round20-um-macro-source-repair-repair-7adac135318f96e8.json`，SHA `cc115c079c0c48dce6b3d5caebee679bcdba3597f985bbb9e7ec4af471e5b48f`。依父 Boss 明确授权继承其 66 refs / 55 files 的成熟全包审读；全部引用文件原始 SHA 本轮再次核实，仅共享审查一份改为上述 `33bd…`，其余 54 文件字节不变。核 SHA 不算 fresh 全文。上轮 P_gate primary §1–2 阅读、未变实际值的原始完整证据、外部 NSW PDF、BCG/Haxell 原文和历史科学程序均按来源继承；本轮不冒认 fresh，新增科学程序运行数为零。

## flat CONFIG 的完整零作业配方

固定 state，将全部 incidence jobs 分成 `I_pos` 和 `I_zero`。给同一份 FSLP 证书 λ，在 private 上取两配置：

\[
C_{sel}=\{J_g\}\cup I_{zero},\qquad C_{inc}=I_{pos}\cup I_{zero}=I_{all},
\]

权重分别为 `λ_gs` 和 `1−λ_gs`。selector 为 unit，state 私有权总和恰一，故两配置负载均一。零 job 的 private 覆盖为 `λ+(1−λ)=1`；正 incidence 的 private 覆盖 `1−λ` 加资源 unit singleton 覆盖 λ 也为一；selector 跨 states 覆盖 `Σ_sλ_gs=1`。每资源的容量以 `1[p_gsu>0]` 的 **0/1 正支撑**收费，余量放 empty，不按小系数降低收费，不把零 membership 计为正支撑。

保留 `λ=0/1`、全部未选 states、重复 indexed states、unused resources 和每个原零 job。一个零 job 同时列在两个互斥配置事件中，其边际权重和恰一，没有复制或删任务。

反向令 private 含 selector 的边缘为 α。正 incidence 不能与 unit selector 同处负载一配置，private 覆盖至多 `1−α`，资源端至少承担 α。unit 资源配置至多容一件 incidence，故正支撑列 `Σα≤1`；每组 selector 覆盖给 `A_g=Σ_sα_gs≥1`，取 `λ=α/A_g` 只减资源使用。零 job 能与 selector 同居，不能用于该排斥下界。覆盖≥1的显式有限证书可按 job 剪冗余、必要时拆分权重，支持增量多项式。

此次更正已支付零作业覆盖，无新数学缺口；结论限于 norm1 两端结构的阈值一和给定有限有理证书转换，不提供整数 allocation、隐式 CONFIG 求解器或 actualOPT≥1 promise。

## Q_D 的共同证书和三座桥

对每个显式整数 `D≥2`，main 的 D 个 states 各取概率 `1/D`；每 helper 以 `1−1/D` 取 home g、以 `1/D` 取 A。每 g 列为 `1/D+(1−1/D)=1`，每 A 列为 `D·(1/D)=1`。所有资源都按正支撑而非系数收费。

第一源的 `N=menu-port-path∘binary-selector-tree` 双向保持 FSLP。tree 正向用子树概率，逆向从 root 送一单位流，own 容量保证非 own 分支可承接 parent 流，叶概率恢复旧 states，允许 off-path 激活。菜单 port-path 正向取 `h_j≥a_j` 且和一的 hole 分布，helper 使用边际 `1−h_j`；逆向相加 d 个 port 容量扣 d−1 个完整 helper 行，得旧正支撑和≤1。语法 membership 与正支撑分开，`d=0/1`、全零 membership、`K=1` 与重复索引保留。

N 后每组 state 数 `K≤3`，每资源跨组数≤3。state-dummy SC 每组 K 名 agents 加 `K−1` 枚 unit dummies；这不是 UM 的单个 selector。每 agent real row 恰一，完整 row 为 `1+(K−1)=K≤3`。real item 正 owner 度至多 `3·3=9`，dummy 正度≤3。

`K>1` 时，agent s 以 λ_s 取全正 real support，对每枚 dummy singleton 赋权 `(1−λ_s)/(K−1)`。每枚 dummy 总边际 `(K−Σ_sλ_s)/(K−1)=1`，得到有限 CONFIG(1)；`K=1` 时 λ_1=1，无 dummy、无除零。反向阈值一且无本组 dummy 的配置须含完整正 real support；dummy 容量迫这类配置的组内总质量≥1，归一化即回 FSLP。

对任意 `t>1`，每 agent 全部 real 总值仅一，合法配置必含本组 dummy。K 名 agents 需 dummy 边际至少 K，而容量仅 K−1，矛盾；K=1 直接由无 dummy 和 real row 一排除。因此先得 CONFIG(1) 可行，再排全部 t>1，中间 SC 的**最高有限 CONFIG 阈值恰一**。

## SC unit-helper 路径的方向和 degree‑3

至此才满足第二源正向 `0<t≤1` 和旧最高有限阈值≤一条件。对 d 个不同正 owners 建 d copies、d−1 helpers；重标旧配置，以 hole/prefix 分布给 helpers 单位 singleton 配置。逆向适用于全部 `t>0`：每 helper 至少消耗一份正 copy；`t>1` 时可且可能必须同时拿两端，绝不能强剪 singleton。相加全部 copy 容量，helpers 至少消耗 d−1 边际，留给 old owners 至多一，故投影保旧 item 容量和同一阈值。正向给新 CONFIG(1)，逆向排新 t>1，最高有限阈值仍恰一。

旧 agent row 不增、新 helper row 二，每 copy 至多有一个 old owner 加两个邻 helper，故最终 **row≤3、item 正 owner 度≤3**。无正 owner、单 owner 无 helper 和阈值零分别处理。有限证书只经有理部分和、组内归一化、树流、剪枝和 hole 混合；按显式 D 与输入/支持编码为 `poly(D)`，不能称 `poly(log D)`。

两源共同支付完整合成，保 ALL / unconditional / accepted 和局部 contribution，任何一源单独都不支付此合成。

## 独立实际值、P_gate 和未付义务

整条 Q_D 目标另含实际菜单 `1/D`、SC actualOPT `1/D`、完整 flat UM actualOPT `2−1/D`。整数鸽巢上下界、N actual 保持、state-dummy 整数桥和 flat 全作业值桥在成熟正文/先行审读中分别已有。本轮重读主定理展开的 Q_D 鸽巢与 state-dummy 整数桥，其余原始完整实际值证据按授权继承；两条 fractional 桥不因此变成 whole_result，独立已证步骤也不改称新 open。

P_gate 的 β* 同时收费组比例和选中组最小质量。现行审查 §一保全部原 jobs：非空 H 的 root 负载 `2−|H|/n`、gate 一、选中 private `2−v_g`、其余 private 一；β=0 用峰二基线。C<2 反向用 unit 资源独占提取不交 bundles。该 `OPT(P_gate)=2−β*` 不将 β* 等同 flat 全组 max-min 值 V；本次 §二.1 更正没改 §一。primary §1–2 本轮继承上轮实读，不冒称 fresh 读取 primary。

新增数学 open 为零。明确 open 对象 `M-ff169368da6147ccbe40ceb2b3b5730b` 仍是共同 H/x/z 的统一位多项式提取、全任务恢复和 sound FAIL 义务，正常交 isolated-after-review。NP-source 强制请求、普通 UM 物理一致性 gadget、变 rank Haxell 位多项式实际输出等保持原范围；无身份或来源 needs-decision。

## 四件 prior assets 与 receipt

四件 prior assets 原始 SHA 再次核对。pin-capacity `07e7a6e47391ef0456a702e205de1e245898d77ecd0ccfe5e3d1a4cd581e960b`、qary `68e9112daec1637327c84271e74c42136dafe030cd2d15ff44bbe1b2b481a004`、um0066 μ=1 `0e8ddf05392b67a56d26d2d7874f5e9883e1ba8197c3d3512baa113fef92bfa0` 的 endpoint/evidence pins 均匹配当前字节，原路径/原 SHA retained。前两条保持 whole_result；um0066 只支持 v2 B 的存在界 contribution，不吞并其 LP、CONFIG1、非注入 promise。

唯一旧 normalized edge SHA `4dca9371ef33db56efd5e792cae6f97e165e9dc892b52bbf9405c53a11e04418` 在直接前任务 supersession 下 replaced，replacement_paths 指向本任务新 edge。保同 edge ID、ALL、unconditional、accepted、contribution/result/remaining 与数学范围，只刷新当前 endpoint/evidence pins 和审读追溯。旧文件未覆盖或删除，review_digest 未伪造；Boss 最终 bind 后须重算新 edge asset SHA。

当前定义没有任何新的 follow-up overlap 对，故 closed_overlaps 和 follow_up_tasks 均为空；旧 pin→saturated、qary→binary 两项只保 inherited_closed_overlaps。其它真实比较留 coverage/completed_in_scope_comparisons，不冒作任务声明。

本 worker 只改本任务新 edge、本文和独立 receipt；source 更正在 receipt 记为已核实解决。剩余操作是 Boss 的最终 native 绑定、检查、推送和交付，不是待数学决策或待源勘误。
