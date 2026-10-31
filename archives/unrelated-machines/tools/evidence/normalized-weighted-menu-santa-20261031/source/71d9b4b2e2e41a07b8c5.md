# Santa 值桥 canonical 实际全文读取与认证范围

对象：`co-work-anl-boss11/research/current/unrelated_machines/normalized_weighted_menu_santa_value_and_size.md`。

本次 canonical SHA-256：`42450690b6dc42cf8a40371071a890aa14e272ef6295c7853c4f1b9bb7fdfcad`。已实际读取全文 §1–6 并核验 hash；没有修改 repo、旧来源、Work 或 Git，没有运行软件或枚举。

**认证范围：仅 §1–3，ID `UM-WEIGHTED-MENU-STATE-DUMMY-SC-VALUE-BRIDGE-v1`。该范围通过，无 standing fatal。** §4–6 的另一 ID `UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION-v2` 本次确已读到，但其 Θ 身份、锐界、端点构造与规模否定范围不纳入本审查的独立证明认证，应由另一审查负责。不能把“全文读取”写成“本审查独立证明了全文两个 Claims”。

## 1. 先前审查与本次次序

先独立读取冻结 Exact，SHA `ae57bf15737c54e6aadf8732869c242622ad75110facc2dbaed5fb8f7549320b`，独立重构后冻结 Exact-only 记录，SHA `575a8d52e90779f8a3bb6c6e2496f1b890ad2383cd273e77012cbaa648d5557a`。

之后首次读取作者 Proof，SHA `5decc348be346acd663478d1c13a768d0e7d06c407abacf593fc09018ff34665`，另冻 Proof read-after 记录，SHA `858bcc8727ace4acef79b7f1119df304005ba135f8bf057873921d69901eb844`。

最后才读取本次 root 自足 canonical。旧记录不被覆盖。本记录认证的只是本次开头 hash 的最终组合 §1–3 是否保持已经独立审过的数学域及证明。

## 2. §1：完整实际对象与值身份

主对象仍是非空 groups、非空显式 indexed menus、各 state 的非负 private 总和**恰 1**、每 state 独立 private machine、每 resource 独立 unit machine、每 group 一个 unit selector、每原 incidence 一枚 distinct job，且没有其它 jobs/资格/约束。允许零项和重复 indexed state 内容，不要求 resource degree 小。

SC 仍是一 state agent、一 resource real item，以及每 group K_g−1 枚不可拆单 owner dummy，dummy 对本组全 agents 值 1、外组值 0。没有把同一 resource 的不同 incidence jobs 复制成多枚 real items。所有原 incidence 在反向调度中仍保留。

存在性量词、V∈[0,1]、OPT_SC=V、OPT_UM=2-V、给定 t∈[0,1] 的 iff，以及“不给 OPT/不声称求最优”的边界均与冻结 Exact 一致。

## 3. §2：每份给定 allocation/schedule 的双向转换

- **资源 bundles→SC：** 最大 clause state 收真实 bundle；其它 agents 各得不同 own dummy。clause≤1 保证 dummy 足以支持共同目标。
- **SC→一个 state/group：** K_g−1 枚 own dummy 不能覆盖 K_g agents，至少一个 agent 没拿 own dummy。foreign dummy 值 0，该 agent 的真实 bundle 值≥SC minimum；实际 real item 唯一 owner 令各 B_g 不交。没有拼接多个 state bundles；K_g=1 自动成立。
- **资源/SC→完整 UM：** 只选一个 selector state，导出其 bundle 对应 incidences；其它全部原 incidence——特别未选 state jobs——留原 private。resource≤1，未选根负载 1，选根负载 2-a，给峰≤2-t。零 private job 留根不会改质量。每 job 一次、原资格与 p 不变。
- **实际 UM→SC：** 当 C<2，每 resource 最多一枚 unit；selector 所在 state 的实际 private load 正好为 2-导出质量，故质量≥2-C。忽略未选 states 的 exports 不妨碍所取 B_g 不交。C≥2 时不再声称独占，只保证零目标，正确覆盖 C=2。

反向给达到 V 的 bundles 得 UM≤2-V，任意 UM C 的下界给 UM≥2-V；V=0/OPT=2 不需从峰 2 取得正 SC value。V=1 给 UM=1；t=0 两边总可行，t>0 使用严格 2-t<2。逐机串行输出实际时刻的明确句已在 canonical，完整 schedule 义务闭合。

## 4. §3：规范化、度数、counts 与源义务

计数仍为 S agents、m real items、S−n dummies；dummy positive entries=Σ K_g(K_g−1)≤S²，dense entries=S(m+S−n)。给定 allocations 的扫描、全部 n+I 原 jobs 的回填及二进制有理部分和均为多项式，没有隐式 state/数值复制或求最优过程。

real-row 总量 1 与 full-row 总量 K_g 明确区分；共同已给 T 的 SC 缩放得到 UMOPT=2-OPT_SC/T，没有用未知 optimum normalization。W≤1 只能先 bonus-normalize 并在 augmented resources 重定义 V，不能沿用原 V；原零工作 state 的提示例与此范围一致。

resource 的 group-degree 与 SC 的 state-agent degree 明确区分，不能免费调用 degree-two SC 后端。式(3) 的 YES≤1↔SC=1、NO>2-δ↔SC<δ 严格方向正确；1 与 1/2 的 SC 源只给 1 与 3/2 的 UM 阈值，不提供 near-two source。

本次仅确认 canonical 对外部 source 及 degree-three embedding 的陈述是条件性接口，未实际读取所链接 embedding 的字节，不独立认证其证明。canonical 本身没有据该引用宣布一般 SC hardness 或一般 UM 结果。

## 5. §4–6 的阅读状态与证据归属

本次已实际读到其参数 d、k、Θ、K_min 身份、support 截取证明、两个端点、固定 η 规模界和局限范围。此前本审查的 Exact-only 与 Proof read-after 都仅属于 SC 值桥，绝不覆盖这些新规模文字。

本记录不为规模 Claim 发独立通过结论，不把其证明或来源归给本审查者，也不代替该 Claim 的 Exact-first 审查。它与 §1–3 在同页，并不扩展本次认证范围。

## 6. 最终判定

**指定 canonical 快照 §1–3 数学通过；§4–6 全文已读但独立认证不在本审查范围。** 原 norm1 主对象、所有原 jobs、OPT2 边界、给定分配实际转换与位复杂度均保持，没有 standing fatal，也没有新增软件或有限枚举声明。
