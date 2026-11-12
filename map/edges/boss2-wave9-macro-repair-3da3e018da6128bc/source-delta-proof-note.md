# 归一化 CONFIG 局部链的 source delta 核验

任务：`boss2-wave9-macro-repair-3da3e018da6128bc`；身份：Boss2。本文保存当前已发布任务 pin 上的数学复核和最小源更正建议。源更正尚须 Root 按原处勘误、引用刷新与 native task refresh 流程接续；本包不能直接据当前草稿宣称最终 done。

## 当前输入与实际审读

任务定义规范化 JSON SHA-256 为 `cd48a0e20744ffd85d399b969ec83cb38acf86ac2c8dec9d1a3621d7e5e6230a`。本地任务为 `claimed`、owner `Boss2`，claim request `ebeb85d2c4e441d1a06c86c8e1887ad5`。前任务 `round20-um-macro-source-repair-repair-7adac135318f96e8` 为 done；其收据原始 SHA-256 为 `cc115c079c0c48dce6b3d5caebee679bcdba3597f985bbb9e7ec4af471e5b48f`。

本轮完整实读 AGENTS、IMPLEMENTATION、worker 入口、实际任务定义、前任务定义及收据、详细 3D 审查、三个当前登记 record、共同定理正文、现行福利审查和四份旧 edge JSON。额外对照冻结 primary 的 §1–2，核清 P_gate 的矩阵及完整正向分配；没有重读 primary 全文，没有重跑历史科学程序。3D 审查 SHA-256 为 `7a2a51765a6157790260e153052dcb8aeb0e5c43d6e8cf4b345afa9ffb398def`。

14 core / 6 read 的 20 个 input pins 全部与当前 registry 的对象规范化 JSON SHA 一致。三份变化 record 是：

| 对象 | 当前版本 | 当前 pin |
| --- | --- | --- |
| `M-9452d445c1744d5eaac946ee974d2162` | 3 | `4126eff22b627cb6b93e95ca4c20542452b045c2df488d91bdbb5f4fd99f4e32` |
| `M-f0619ab2e98f41eb9fa9c02a48c19aaa` | 4 | `73cab4763a7fcab682efdc03aca50b35d091e600a350f1dab0e1840673aa184f` |
| `M-080d9b22ae87408f9a673a898c7a6dc3` | 4 | `5041d21ea4cc71de0cf1e759aade84c0cc09a86d8539510dc3683242679ff85c` |

三 record 的数学合同均未变：变化为 version、福利审查 evidence SHA 和 objections 中追溯此次 P_gate 全任务说明的尾句。共同正文仍为 `archives/unrelated-machines/state/定理/规范化平菜单的CONFIG与正支撑LP双向保持--定理.md`，SHA `8bfbaa80b98546b6d1320e9760bb9491165e26a6cef1b6cd35eb86116c822f66`。旧收据 66 个 reading refs 覆盖 55 个不同文件；本轮逐原始字节核 SHA，只一份福利审查变化，其余 54 文件不变。核 SHA 不表示本轮重读全部旧证据。旧 14 核心的完整成熟审读与实际值独立证明按父任务授权继承。

## P_gate 改动的全任务核算

福利审查当前 SHA 为 `63629abaa5cd2bcc0e42ff051936b91882ea63c711dfdac231f238763b682255`。此次已发布增量位于 §一.1：它补明根 pin、未选 connector、未选 selector 和全部其余 incidences 的去向。冻结 primary 的完整矩阵中，根 pin 在 R 耗时 1；每组 connector 在 R 耗时 1/n、在自身 gate 耗时 1；selector 在 gate 或本组任意 private 均耗时 1；每 incidence 在 private 耗时其原系数、在对应 resource 耗时 1。

给非空 H 和真实不交 bundles，逐组选 attaining state。J0 留 R；选中 connector 去 gate、selector 去 attaining private；仅将选中 state 在其 bundle 内的正 incidences 导出 resource；其余全部 incidences 留原 private，包含未选 states 和零作业。未选 connector 留 R，未选 selector 去 gate。于是根负载是 `2−|H|/n`，每 gate 负载 1，选中 private 负载 `2−v_g(B_g)`，其余 private 负载 1，资源因 bundles 不交至多一件 unit job。β=0 用根接全部 connectors、gate 接全部 selectors、incidences 全私有的峰 2 基线，不能用空 H 取最小组质量。

反向 C<2 时，gate 接 connector 的组 H 满足 `|H|/n≥2−C>0`；selector 被迫去本组某 private，该 state 外送的原资源质量至少 `2−C`。unit resource 端点在 C<2 时至多接一件，故这些选中 bundles 全局不交。C≥2 时仅用 β*≥0；根 pin 另给 OPT≥1。这是完整 P_gate 的 `OPT=2−β*`，β* 同时收费组比例和所选组最小质量。Q_D 的 flat V 是全部 groups 的 max-min 实际菜单值，没有根/gate 的可选组比例，不能把二者任意代入。

## flat CONFIG 的零作业完整配方

本轮另识别现行福利审查 §二.1 的一个压缩表述省略。本文不改源文件；此项须交 Root 作最小原处勘误及引用刷新。其数学证明在未变共同正文 §1 已完整成立。

令同一 state 的全部 incidences 分为 `I_pos` 和 `I_zero`。FSLP 资源容量必须按 `1[p_gsu>0]` 的 0/1 incidence 计算，不能改为系数权重。给定 λ，在 private 采用

\[
C_{\mathrm{sel}}=\{J_g\}\cup I_{\mathrm{zero}},\qquad
C_{\mathrm{inc}}=I_{\mathrm{pos}}\cup I_{\mathrm{zero}}=I_{\mathrm{all}},
\]

分别赋概率 λ 和 `1−λ`。第一配置负载为 1，第二因 norm1 负载也为 1。零作业私有覆盖为 `λ+(1−λ)=1`；每个正 incidence 私有覆盖 `1−λ`，资源 singleton 覆盖 λ，因此总覆盖 1；selector 在本组全部 states 上覆盖 `Σ_s λ_gs=1`。资源空配置补足容量。未选 states 的 payload、零作业、重复 indexed states、未用资源均保留；既不删 job，也不把零 membership 算入 FSLP 容量。

反向记 private 含 unit selector 的边缘 α。正 incidence 不能与 selector 同处 private 的负载一配置，故资源端至少须承担 α；每 resource 的 unit singleton 容量得正支撑 α 和≤1。每组 selector 覆盖得 `A_g=Σ_s α_gs≥1`，按组令 `λ=α/A_g` 只减资源使用。阈值 1、norm1 和完整 job 身份均是承重前件。该有限有理证书变换没有提供整数 allocation、未知隐式 CONFIG 的求解器或 actualOPT≥1 promise。

最小原句/改句位置均为 `归一化菜单福利与配置证书双源审查--审查.md` 的唯一标题“1. FSLP 与完整 flat machine CONFIG(1)”下第一段，当前全文 SHA 如上。原句：

> 给定 λ，在 private root 上以 λ 权重放 selector 加零 jobs，以 1−λ 权重放所有 positive incidence；资源机放每个 positive incidence singleton 配置并以 empty 补足。

建议只把其中“以 1−λ 权重放所有 positive incidence”改为“以 1−λ 权重放全部 incidence jobs（含零 jobs）”；其它文字保留。若按原句字面仅在 λ 配置保零作业，则 λ<1 时零作业只覆盖 λ，不能接下一句“覆盖恰一”。更正恢复共同正文已经给出的配置，不改变该证明或三个对象的数学合同。不得把此已识别省略写成“现行审查全部句子均无瑕”。

## Q_D 局部合成及阈值边界

对每个显式整数 D≥2，取 main 各 state 概率 `1/D`；每 helper 在其 g 上取 `1−1/D`，在对应 A_a 上取 `1/D`。每 g 列负载 `1/D+1−1/D=1`；每 A_a 列负载 `D·(1/D)=1`。这是同一份正支撑 FSLP 有理证书，并非按小权重降低资源收费。

第一源把此证书沿 N 的 binary-selector-tree 与 menu-port-path 转换。其成熟 normal form 保每组 K≤3、每资源跨组数≤3。state-dummy SC 对每组 K 个 states 建 K 名 agents 和 K−1 枚 unit dummies；这里的 K−1 是 SC dummy 数，UM 的 selector 是每组一件 unit job。每 agent 的 real row 总值为 1，加 dummies 得 row total=K≤3。旧 real item 正 owner 数至多 `3·3=9`，dummy 正度 K≤3。

K>1 时，agent s 以 λ_s 取全正 real support，以 `(1−λ_s)/(K−1)` 分给每个 dummy singleton；每枚 dummy 的组内总边际为 `(K−Σ_s λ_s)/(K−1)=1`。K=1 时 λ_1=1，无 dummy、无除零。逆向阈值一时不含 dummy 的合格配置必须含完整正 real support；dummy 容量给这种配置质量总和≥1，归一化即回 FSLP。若 t>1，每 agent 的 real 总值只有 1，合法配置必含本组 dummy；K 名 agents 所需 dummy 边际至少 K，而只有 K−1 容量，矛盾。因此这个中间 SC 的最高有限 CONFIG 阈值恰 1。

至此才满足 SC unit-helper 路径的正向 `0<t≤1` 与旧最高阈值≤1前件。反向允许全部 t>0：每 helper 的合格配置至少占一个 copy，t>1 时可以同时占两端，不能强剪成 singleton。对 d 个不同正 owners 的旧 item，d−1 helpers 的总期望占用至少 d−1；copy 总容量 d 留给所有旧 owners 至多一份边际，因此反投影保旧 item 容量和同阈值。正向 hole/prefix 混合保有限有理支持；old agent row 不增，新 helper row=2，每 copy 至多原 owner 加两个邻 helper，最终 item 正度≤3、row≤3。

零阈值由空配置/正阈值反证另列；空 items/全零 rows 不凭正阈值证明直接跳过。d=0 的无正 owner 项、d=1 的单 copy 无 helper、K=1 的单 state 无 dummy、全零语法 membership 和重复索引均分别保留。实际路径正向只在 `0<v≤1`；不能从 fractional CONFIG 变换推出实际积分性。

故两个共同前提保持 ALL，交付范围仍为 accepted 局部贡献：Q_D 和经 N/state-dummy/SC path 的完整实例有显式有限 CONFIG(1) 证书；最终 SC 最高有限阈值恰 1、row≤3、item 正度≤3，中间 real item 正度≤9；转换按显式 D 与支持编码为 poly(D)，不能称 poly(log D)。D≥2 保 `0<1/D≤1/2`。

完整目标另含实际菜单值 `1/D`、SC actualOPT `1/D` 和完整 flat UM actualOPT `2−1/D`。这些分别依赖整数鸽巢上下界、N 的 actual 值保持、state-dummy 的实际分配桥与 flat 全作业值桥。它们在成熟正文/先行审读已有，本文准确继承；两条 fractional 桥不独立支付这些步骤，P_gate 的 β* 也不代替 flat V。本轮没有重证或重跑全部 actual 证据，也不把这些独立已证步骤称为新 open。

## 资产与比较的精确处置

四件旧资产均核原始 SHA。只有 `normalized-config-bridges-qd-degree-three.json` 的三个 endpoint pins 与福利审查 SHA 过时；在本任务独立目录保原 edge ID、accepted/ALL/unconditional 与原 contribution/remaining，最小更新三个 pins、一份 evidence SHA/evidence_pins 和本轮审读文字。旧 review_digest 删除，留 Root 对最终语义运行 native edge-bind/write/check；当前草稿未绑定，不冒用旧 digest。

该旧 edge 在直接前任务 supersession 下为 replaced，replacement_paths 指向本任务新 edge。依 IMPLEMENTATION，新任务 done 后旧边从现役清单退出，旧文件不需直接覆盖或删除。pin-capacity、qary-fixed-affine 和 um0066 三份边按原路径及原 SHA retained，未改任何字节。前两条仍交各自 whole_result；um0066 仍仅交 μ=1 恢复 v2 B 的局部 contribution，不能靠数值代入覆盖其 LP/CONFIG1/非注入 promise 全合同。

当前任务无新增 overlap_comparisons。旧收据 closed_overlaps 与 follow_up_tasks 均为空；其 inherited_closed_overlaps 两项 pin→saturated、qary→binary 已解决，照原记录继承。本轮没有另造泛比较或待发布任务。NP-source 强制请求、普通 UM 的物理一致性 gadget 和变 rank Haxell 位多项式输出等原范围外开放义务仍按原覆盖保留。

Root 已确认待勘误审查被本包三个端点及另外三个现行对象引用；后者不在本 worker 写入范围。本 worker 只保存此当前 pin 草稿及最小改句，不改源/registry/coverage/integration，不执行 Git、work.py mutation、队列或凭据读取。Root 完成源更正与 native refresh 后，fresh worker 可只对该 zero-job source delta 和受影响 pins/evidence 做准确复核，再重绑、更新 assets SHA、checkpoint 与 done。
