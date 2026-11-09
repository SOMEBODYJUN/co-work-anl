# 六文件最小原处勘误：数学交叉核对与局部登记 delta

审查标记：`474257b8-errata-math`。范围是根确认同批的六份 canonical 文件；只写 Boss5 独占工作区，没有修改共享正文、baseline、registry、边、队列或 Git。

**结论：六份拟更正副本均通过本次定点数学核对，未发现拟更正文引入新的数学错误。** 三类原始错误与两处追加的长链转述错误均可按当前副本原处应用；对象身份、statement、模型、量词、truth_status、假设、scope、objections 和来源身份沿用当前登记。

最终可应用局部数据在 `errata-math-474257b8-final-six-source-delta.json`：6 源文件、15 个对象各增 version 一次、25 处 body/evidence 精确引用更新、2 条 canonical 边需要重绑定、1 个有效 done 需要定向替代、10 个未完成任务需要刷新。此前四文件主 delta 与二文件补充 delta 仅为拆分视图，不应在已应用六文件 delta 后再重复应用。

## 1. Bamas 二项式与损失因子

同冻结 PDF 的实际 SHA-256 为 `e1120098a847eb10689c529579af5d44b93ee5f6e655eae7621a2333bf76e8de`。本次读取物理第 19、33、34 页文本，并实际查看根已渲染的第 19、34 页。

第 19 页给

\[
k_s=\frac{\binom m{\rho m}}{\binom{(1-\rho)m}{\rho m}},\qquad
k_1=\frac{\binom{(1-\rho)m}{\rho m}}{\binom{2\rho m}{\rho m}},\qquad
k_2=\binom{2\rho m}{\rho m}.
\]

因此无损需求连乘基准是

\[
N_1=k_s,\qquad
N_2=k_sk_1=\frac{\binom m{\rho m}}{\binom{2\rho m}{\rho m}},\qquad
N_3=k_sk_1k_2=\binom m{\rho m}.
\]

物理第 33 页三项目标与第 34 页展开连乘均吻合，其中第 34 页第二项末式直接是正确的 N2。原页把 N2 写为 `C(m,2ρm)/C(ρm,ρm)`，不是等价变形。

当每个已选非汇点仅需覆盖原需求除以 α 时，单父性使深度 3 的三层规模分别至少 N1/α、N2/α²、N3/α³；整数出度还须向上取整。这里 N1、N2、N3 不是任意有损树的规模等式。一般 lift 的同一解释须按实际层深付损失：在 L(j/ε) 的乘性下界对应 Nj/α^(j/ε)，不能把三大阶段误当成只有三条边。拟更正 §4 的“逐层支付相应因子”符合这一限定。

Theorem 1 的一轮 SA 间隙陈述、Theorem 2 的 path-hierarchy 量词和一般 SA 高轮猜想区分均未改变；该转录勘误不产生一般 unrelated-machines 困难性结论。

## 2. Good helpers、outer homes 与全部原 jobs

实际全文读取本对象登记明确引用的两条完整 v5 原证明：

- 作者 `relative-curvature-o1k-working-sources-20261031/c8f99fb9dc315aa27225--author-proof-working-v1.md`，SHA `0f5e322441789f5d2dae8fb0592fff86aede3d71f093cb727e2ea78b0f1b2593`，尤其 §1、§2、§10。
- 独立 actual-I `relative-curvature-o1k-working-sources-20261031/58de49571a4172661609--independent-exact-first.md`，SHA `074556f862b8548349f1710caa540f0a45c18f08a3f42822208ed9eb39d89583`，尤其 §2–4、§10。

同时读共享 UD 正文 `共享UD tiny状态势与19比10回填--证明.md` 的 §1、§2、§5、§6 必要段；SHA `e857e20f4498aef53ebe9c3ef0a9f3bc7f5937c5cd3fb554365c1d3e553a2868`。

三处一致：Good helper **保留它自己的实际 B fallback bundle**，并释放自己的 home 给相应 outer；其余 helper 回 own home。outer 唯一 state 的正支持只在 homes，故把 B bundle 给 outer 不能承担其正价值。home 全局互异且与 B 不交，Good 的 B bundles 保持单占，UD 叶在同一补资源集合中获得共同匹配。

阈值限定必须区分：原无额外叶 v1 的 W_i>1/5 与 q=1/10 实际推出 z_i>1/9>1/10；稿中保留较弱 z_i>1/10 正确。作者 v5 prefix-flow 成功给 W_i>19/100，推出 z_i>1/10；独立 actual-I 成功允许 L_i=19/100，对应 z_i≥1/10，等号仍成功。两句拟勘误没有更换这些阈值或证明路线。

普通矩阵 P(Q) 的回填保持每个 state 一 private、每个 resource 一 resource-machine、每 group 一 unit selector、每 listed incidence 一原 job：selector 放其所选原 state 的 private；仅所领真 bundle 中的 selected-state 正 incidence 送 exact resource；其余全部 jobs 留自己的 private，包括零、inactive payload 和重复 indexed state。归一化使 selected private≤1+(1−q)=19/10，inactive private≤1，resource≤1，每 job 恰一次且仅用原有限端点。unit selector 给 OPT≥1。两篇拟勘误只修正资源领取者，不外推 k⁴/k²/O(1/k)、k=1、叶模型或软件身份。

## 3. q=1 的真实有限运行范围

读《可选资源束的配额树穷举与正确计数》全文，并读其绑定原代码 `tools/evidence/um-parity-quota-and-three-dimensional-programs/original/8af37296657f6ee6656d.py` 的实际主循环（源码 SHA `910572cc92e1ad6f8b2bbd4988c3c837e60858bce706fbf8752e8f66dee4deb8`）。本次没有运行计数程序。

q=1、资源 {0,1} 的非空束标签只有 {0}、{1}、{0,1} 三个。`mask in range(1 << len(universe))` 枚举其任意子集，含空系统，共 2³=8 个；每个 K=1,2,3,4，恰 32 次比较。stdout 的 `exhaustive_q1=16*4` 是末尾 print 的硬编码历史串。拟更正保留该真实 stdout，仅把数学运行范围改为 8×4=32，正确。

q=2 的 1200 个固定 seed 样本各测 K=1,2,3,4,7（6000 次）和固定 one-bundle-floor 分支沿用原有限边界；样本不保证互异，不产生任意 q/K 或一般调度算法的全称结论。

## 4. 追加两处 long-chain 勘误

完整读取《最优凸包开链三原入口的单个最优解与全匹配计数》，交叉核两份原页与拟更正副本的精确 diff。

固定输入排序与 tiny 平局顺序，root 只有 k 槽但有 k+1 rootjobs，至少一个必须离根；它迫整链激活。每额外后缀均有正成本，tiny 激活成本 ct=(d+2k−2)/(2k)>0，macro 成本 cb=ct+1/(2k)>ct。bad 已给成本 W0+ct，因此所有最小成本 cover matching 恰激活一 tiny、无额外后缀；macro 占 root 槽 0，又迫排序首 tiny 离根。故得到**唯一实际机器归属**。这不足以声称一般槽注入也唯一；原三小例的 matching_count=1 仍是有限观察。第一份改句准确收窄这个量词。

最小 slot-cost 返回该 bad，峰 Bk=2−1/k。随后再显式激活另一条 tiny 链，才得到 Rk=2−2/k，改 d+1 件任务、涉及 d+2 台机器。第二次激活增加正成本 ct，因此不能把 R 写成原最小成本流的直接输出。第二份拟勘误准确区分 B 与后续 actual repair，不改变严格 lex 支持下界、弱 Cmax 非增路径或一般问题范围。

## 5. 登记与 canonical 图波及

当前本地 registry 快照 SHA：`19c1521d1c73399106c03d12267c80f80dbe95e0c6b9d12714ba2c1189ba1da3`；其 baseline 是 `research/registration/baseline-map-additive-recount-v1.json`，SHA `285c85dbac89bc1c9ad088228eeb3d00225c7d202e4422862a518d8610cefaa9`。最终 delta 对所有命中对象列出了当前 version/pin、拟 version/pin、精确 JSON pointer、old/new ref（保 section）、每个材料的 old/new SHA 及原 disposition/owners/reason。

15 对象分组：Bamas 四 owner v1→v2；multiouter v1/v4/v4b/v5 四 owner 当前记录 v2→v3；计数页的 M-4803…、joint-slot、promise 三 owner v2→v3，bundle-floor v3→v4；long-chain owner v3→v4、closed-cycle weak owner v3→v4、escape-threshold owner v2→v3。long-chain owner 命中两页，仍只增一次。

450 条 canonical 边全部扫描了端点 ID、endpoint_pins、evidence 与 evidence_pins，精确命中两条（都无直接计数页 evidence 命中，但 joint-slot 端点 pin 变化）：

| edge_id | 文件 | 当前文件 SHA |
|---|---|---|
| um-0195479a-supplied-distortion-implementation | map/edges/unrelated-machines-3a-3a-0195479a27d65198/supplied-distortion-implementation.json | e8b62d49e9bdc625c783d4927c2404f1945436134754fbf63a79c04c8139124a |
| um-0195479a-true-source-distortion-check | map/edges/unrelated-machines-3a-3a-0195479a27d65198/true-source-distortion-check.json | c8206ed8557450b3472189d1797949be68d4e990b6cd11e2df764e4a6995785a |

二者 joint-slot 当前 pin 为 `f3d75df5a26fcf4d57cf754c13123eb898e2fbf8091f1a185e2e1558bfaf2653`，应用本 delta 后是 `588541dd728a2da8d248d4e7a018a443ffed37034139fd451b3a62d4ac18a54c`。原数学关系证据未受此计数修订影响，但仍须重新绑定和交代资产。

有效 done 是 **round9-source-repair-repair-d0ac122f3ce74353**（Boss1），它已 supersede 原 `unrelated-machines-3a-3a-0195479a27d65198`。应定向替代有效接替包，不能再给旧 0195 done 重做替代。最终 delta 保其 15 个 prior assets 的精确 refs，其中受端点变化的就是上表两条；其余资产也须在替代收据逐一保留/处置。joint-slot 是该包 read input，按当前 map-draft 规则需要针对受读依赖影响复核原核心。

另有 10 个未完成同问题任务：0066175b7e3c8a0d、17669e4ba1771673、3f971da9d312cddb（当前 Boss5 claimed）；6992d380256546e6、6cef82148f2404c9、7670a89f413f26a6、a56e5e8b03d8a1fd、aa15ae15f8c96819、b10995ada0ae22bc、cc2c7c0ee62cf157（当前 available）。它们的完整 task_id、core/read 精确命中、input pins 和读取 refs 在最终 delta。旧 083337f4ee4443ff 已 withdrawn，仅保历史，不刷新。

根发布后可对最终 JSON 的 `grouped_repair_task_ids` 一次传入重复 `--repair-task`；未完成任务沿同 ID/write_paths 刷新，有效 done 生成定向接替。此前保留的草稿和原 worker 沿同问题继续。

## 6. 本次核验与适用边界

局部 delta 已做重建校验：逐个 old ref 与当前记录和源 SHA 匹配；仅替换引用 SHA、version+1 后重算 proposed pin；所有带 section 的新引用仍存在且标题唯一；baseline 对六原源的旧 SHA 均匹配当前字节；非 binding 字段逐字段保持一致。主/补 delta 分别已重建通过，最终六文件联合 delta 同一算法生成，15 个 owner 无重复增版。

最终 delta 是当前本地快照的精确建议。根发布前按其已掌握的权威远端状态做最终 CAS/版本复核；本次没有冒称同步或更改任务状态。

## 7. 两条 joint-slot canonical 边的最后定点反馈

根接受六源 delta 后，本次只追加实读上述两条 canonical 边及其必要承重材料，没有扩展到其他资产或新核心，也没有运行原程序。完整读取原数学稿 `um-following-palette-and-distortion-primary/comparison/research/current/unrelated_machines/distorted_group_joint_slot_rounding.md`（SHA `de39d3d70e4a1d5835eaecf196d0a0bcff51006f6d7eb4006354344b737f5deb`）全文，尤其 §2–4；完整读取规范 `distorted_group_joint_slot.py` 与 `distorted_group_software_review.py`，并读独立 `distorted_group_independent.py` 的 `all_sources`、`verify`、实际前缀/全任务回算和确定性/退化夹具必要段。两边当前全部 evidence refs 的文件字节 SHA 逐一吻合。

**关系结论：q=1 的 64→32 计数说明不改变这两条边的 implements/checks 关系。** 那个更正在另一 K-uniform bundle 分支；这里承重的是失真组的共同 a/y、成本有序槽、整数流/独立有限打包与实际前缀。两边 `kind`、`status:accepted`、`relation_mode:context`、端点 IDs、conditions、roles 和 scope 均可保留。第一条可保持全部数学文字重新绑定；第二条的原解释另有一处零需求分支遗漏，需要在重绑前一并补清，具体如下。

### 7.1 supplied-distortion-implementation：可原文重绑

给定合法证书的实现先准确验证 `Σ_h a_bh=1`、home 占用 `x_h≤1`、同流守恒 `Σ_z y_hz=x_h`、真实资格和逐 sink 的 `Σ_h b_hz d_h y_hz≤κT`。按 c_hz=b_hz d_h 而非 d_h 排序的正区间交长，与 a/y 构成同一分数流；整数容量给同时覆盖所有宏、互不复用 home/槽的整数解。占用 home 的实际前缀满足出口≤d_h，上包络使实际 sink 加工成本受 c_hz 支配；相邻完整槽收费得到总 sink 界。全部宏和私有任务都按原有限资格回算。

给定见证的这一方向只需所选宏端≤T，确实无需宏下界>T/2；后者用于从真实 T 调度证明 LP 必要性的另一方向。该边已准确区分两方向，并明确不包含通用 LP/未知 OPT 软件。因此 conditions/explanation/scope 无须数学改字，可在 joint-slot 新 pin 下原文 edge-bind/edge-check。有限软件审查仍是原来的 5 个合法与 10 个拒绝输入；不能因本次读代码写成新运行。

### 7.2 true-source-distortion-check：关系成立，补一个 d_h>0 分支限定

其真实源→见证→独立打包→完整原任务输出的 checks 关系成立。必要性证明是：宏端 β>T/2 使每 home 至多一宏；若 d_h>0，则该占用 home 的真实出口 e_h 满足

\[
e_h>W_h-T/2\ge W_h-rT=d_h>0.
\]

因此 `y_hz=e_hz/e_h` 合法，下包络给 `b_hz d_h y_hz≤κ·实际sink加工量`。先在每个真实源态形成这一份 a/y，再取共同平均，保持占用守恒与全部 sink 预算。独立代码的 `verify` 明确先执行 `if not d[h]: y[h][None]+=mass; continue`，只有正需求分支才断言严格出口链；随后以另一套正区间槽与指数回溯选同一宏/home/slot打包，执行并重算每件原任务。边中 4/3、2/3 的 token 质量及 3/10 对 1/2 的前缀例与实际代码一致。scope 已准确限制为有限检查，没有把指数 oracle 写成一般位多项式算法。

现有 explanation 的片段“同态被占home的真实出口超过W_h−T/2≥d_h，按其各sink体积分配y”省略了正需求条件。若 d_h=0 且 W_h<T/2，`W_h−T/2≥d_h` 不成立；此分支原证明和代码实际走旁路。故建议仅将该片段精确补为：

> 对d_h>0的被占home，真实出口e_h>W_h−T/2≥d_h>0，按各sink出口home体积归一给y；d_h=0的被占home走私有零成本旁路

供根直接采用的完整新 explanation：

> 逐个源态以宏归属形成a；对d_h>0的被占home，真实出口e_h>W_h−T/2≥d_h>0，按各sink出口home体积归一给y；d_h=0的被占home走私有零成本旁路。平均保守恒，并由下包络得到逐sink的κT预算。有限独立oracle枚举正a及正交槽且不复用home和槽。二home夹具的虚拟token质量4/3、2/3，实际首前缀成本3/10受1/2 token支配，确认非整数末槽与真实q加工的分离。两程序的算法域有交集，任意给定合法a/y与由真实源调度导出a/y的输入合同不同。

这处是既有解释的分支补全，不改变 checks 关系、声明范围、证据字节或端点对象。根按这一最小文字更正后重新绑定即可。本子任务未修改任何共享边或任务，最终有效 done 定向替代仍由根串行处理。

## 8. 第七份原处最小更正与当前七源联合 delta

根随后确认同一未限定不等式也存在于《失真组实际源调度与联合槽独立程序复跑--计算.md》“从真实源调度到实际前缀”第二段，并要求纳入同一原处更正事务。本节将该文件加入，更新 §5–7 关于最终文件数、owner 数、当前输入快照及第二条边的绑定建议；前六源的已核数学和版本增量不变。

已准备 `errata-math-474257b8-seventh-source-corrected.md` 与单段 `errata-math-474257b8-seventh-source.diff`。原 SHA 为 `0d163eaa1d2002f1ec96d81ba6ac32e8468b68f4b93d1e357c225b65b6c51341`，新 SHA 为 `3ff4fc9e22775b542dd600a8b01787c3f8d6fb180b4ea550f8564ec278f56a78`。只替换该段，其余字节通过反向替换逐字节校验保持一致。新段为：

> 对一组真实T源调度作均匀混合；宏位置给a。对每个源态中d_h>0的被占home，宏>T/2迫实际出口e_h>W_h−T/2≥d_h>0，按各sink出口home体积归一给y，所以正需求的归一没有0/0；d_h=0的被占home走私有零成本旁路。对这些y取同一均匀混合，得到逐sink预算Σ_h b_hz d_h y_hz≤κT。

这样先在每个源态按正需求分支形成同一 a/y，再取同一权重的平均。d_h=0 分支完全不进行出口归一；原文下一段的私有 dummy 与此一致。数学依据仍为已实读原证明 §2 及独立代码 `verify` 的 `if not d[h]` 旁路分支，没有改变有限证书或一般定理量词。

**本事务应采用 `errata-math-474257b8-final-seven-source-delta.json`，替代此前六源及拆分 delta。** 它按当前 registry 快照重新生成：

- 当前 registry SHA：`6457844b0a6187f3707e6603078c51d25a39681828fe1b36221f2b17acee2b6e`。
- 当前 baseline：`research/registration/baseline-map-config-and-customer-round12-v1.json`，SHA `f795e0cc698164c8e0c07a92fc367d960f89d1f2c7465142f54b78e78f06ced1`。
- 七源联合共 **16 个 owner 各增 version 一次、26 处 body/evidence 引用替换**；没有将前六源先增版后再增第二次。
- 新增唯一 owner：`unrelated-machines/distorted-group-source-schedules-independent-joint-slot-replay`，v1→v2；当前 pin `282a327578461d0e06b51f6f02fcbaa16b0dda520109ae5a3602657bb2ba3dc8`，拟新 pin `5732f445cb6680964717e5365fd9dffcc842bb595780f4236de31e1b680277ff`。它只更新带原唯一标题的 `/body` 引用与 version，其他记录字段全部相同。

当前 canonical 清单 446 条边已按同一精确路径/端点规则扫描；仍仅命中原来两条。第一条 supplied-distortion-implementation 仍只因 joint-slot target pin 改变，可保持数学文字重绑。第二条 true-source-distortion-check 现在有三项必要更新：按 §7.2 补 explanation 的分支条件；其 `/evidence/0` 及相应 evidence_pin 将本计算页改绑到新 SHA `3ff4…6a78`；两个 endpoint pins 同时更新到 joint-slot 的 `588541dd728a2da8d248d4e7a018a443ffed37034139fd451b3a62d4ac18a54c` 与本 source owner 的 `5732f445cb6680964717e5365fd9dffcc842bb595780f4236de31e1b680277ff`。随后重算绑定和 review_digest，关系种类与 scope 仍保留。

任务波及数未扩大：仍为有效 done `round9-source-repair-repair-d0ac122f3ce74353` 和原 10 个未完成任务，七源 delta 的 `grouped_repair_task_ids` 是完整当前清单。有效 done 原核心中的本 source owner 也换 pin；旧 0195 仍只作历史，不能绕过 round9 successor 重替。当前逐任务 state、owner、input pins 以七源 delta 为准，保留根当前 handoff/刷新安排。

七源联合 delta 已逐个重建验证全部 16 owner 的 old pin、old ref、old 源 SHA、唯一 section 标题和 proposed pin，全部通过；七份 baseline 旧 SHA 与当前原字节全部相同，16 个 owner 无重复身份或重复增版。本子任务只写独占前缀文件，未修改任何 canonical 正文、共享 registry/baseline、边、任务或 Git。
