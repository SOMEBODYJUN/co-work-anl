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
