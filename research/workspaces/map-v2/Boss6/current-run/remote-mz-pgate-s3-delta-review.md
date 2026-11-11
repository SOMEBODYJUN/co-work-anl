# 56650ea → 724c402：三个非 structural 数学正文的定向增量复核

结论：三处远端修改均为有效的局部纠错/展开，应保留。它们没有改变 Boss6 已完成的固定色板着色目标及两条 canonical 证明边，也没有改变本地新增 ∞ helper M-LP 保持定理或 cap-M-LP 反族的前提、结论与证明。此范围内没有需要新增数学修补的义务；合并后正文 SHA/对象版本/阅读包 pins 的同步由父 Boss 的 registry 集成流程处理，不能把内容身份更新误写成旧边被数学否定。

本检查不是三个 foreign-task 的完整重新审计，不接管 Boss5 队列。clone 只读；唯一写入是本 staging 文件。没有 Git 写操作、work.py、认领/完成队列操作、native edge-bind/edge-check 或科学 replay。

## 精确比较身份

- Base：`56650ea6813513decee236e0353647e07ff7cc63`。
- Remote：`724c402aeef432b2e6848fe1b1b67a0ddae33ba3`。
- 用于核对 Boss6 已有边和新增对象的本地固定提交：`a8393f9356f7159631d0f9ce7ed4804bc79cbab4`。
- 对目标三文件执行 `git diff --unified=12 BASE REMOTE -- <three paths>`，再通过 `git show REMOTE:path` 阅读，不把当前工作树当成 remote。
- 该精确三文件 delta 为 4 insertions / 2 deletions。另一个《结构参数下的指派限制调度》不在本 worker 范围。

下表 F1/F2/F3 的完整路径分别为：

1. F1：`archives/unrelated-machines/state/文献/四对一与字母表soundness两篇文献整理--文献.md`。
2. F2：`archives/unrelated-machines/state/审查/归一化门控福利证明与参数互补八源溯源--审查.md`。
3. F3：`archives/unrelated-machines/state/审查/identity-coupling-raw-k2-sa3-final-sections--审查.md`。

| 文件/版本 | Git blob | SHA-256 | bytes / lines |
| --- | --- | --- | --- |
| F1 base | `b0ca7bb5977540232e44e52623a57b43c03e34ee` | `0e1f9f27706ce17087037ef05c6265d8f3d2e6ede5801cdbe87b559c4ff9f2ac` | 17635 / 136 |
| F1 remote | `0322caaf852b786f77dd438ae096c226f25f7915` | `6d5be138de6825a1208776cbb485316c5b0e9d197870e32ab7c1d8ca5cf2f746` | 18364 / 138 |
| F2 base | `e49527ba81dc51865cd2dcc3e8b79a523e3294e2` | `e9456866cda488928a44cb50741a2ff05a30eb3be094d7754584a9fe6048b0a2` | 13423 / 175 |
| F2 remote | `1581bf611b63052a29343653907db513854bb0e9` | `9e00d296c74e95a1e1bf35cc8e5a442333b1b212c53da563ffec5fabb3bda546` | 13583 / 175 |
| F3 base | `62015e590bd74c299fa01fa2b2f603a6f915f5c0` | `b7af17547dbfb0bb485a9dfe53aec4becfd5db42a46ce1306f3b66d803f052a0` | 11311 / 157 |
| F3 remote | `aa75831a54cc7dd54e61c6f277f9452433537241` | `afefdddd492c8f830b35817a12b6c2596d5eacd350b42a2b9d344e20c2b6b81c` | 11487 / 157 |

## F1：MZ Claim 3.2 的两个中间式修复

实际改动在 §3.2 新增一段。它针对 Minzer–Zheng 的 Claim 3.2，不针对 FMW Theorem 1.6 或其图着色推论。

按冻结原文 §3.1.3/§3.1.4，每个坐标先以概率 β 取 U≠V（V 是 singleton），此时 r 份均匀独立 advice 全零的概率为 q^{-r}。因此暴露事件

\[
E_i=\{U_i\ne V_i,\ \text{all advice}=0\}
\]

的概率为 βq^{-r}。原文所写的“U_i=V_i，或 U_i≠V_i 且 advice 全零”有概率 1−β+βq^{-r}，确实不等于 1−βq^{-r}。改成“advice 并非全零”后才是 E_i 的补事件，概率正确。取 m=ceil(q^r/β)，则整块没有暴露坐标的概率为 (1−βq^{-r})^m≤e^{-1}；有暴露坐标的概率有绝对正常数下界。通过取首个暴露坐标并对其余坐标的问题固定作平均，原来的“块值 1−η 推出一个标准 variable-versus-equation 策略值至少 1−10η”的论证可保留；这里 η 是块失败率，不能与最终源完备误差混同。

第二处把块长误当块数的等式确应删除。令 Ψ=G_{β,r}^{⊗m}、t=floor(k/m)。因为 mt≤k，丢弃最后 k−mt 个检验只会增加最大成功率，故方向是

\[
\operatorname{val}(G_{\beta,r}^{\otimes k})
\le \operatorname{val}(G_{\beta,r}^{\otimes mt})
=\operatorname{val}(\Psi^{\otimes t})
\le2^{-\Omega(\varepsilon^2t)}.
\]

q^r/β≥1，所以 m≤2q^r/β；k≥2m 时 t≥k/(2m)≥βk/(4q^r)，付清 Claim 3.2 显示的 2^{-Ω(ε²q^{-r}βk)}，没有翻转不等号或把 floor 当成 ceiling。

充分大 ℓ 的附加说明也与该文实际参数一致：原文式 (7)/§7.1 取 k=q^{2(1+c)ℓ}、β=q^{-2(1+2c/3)ℓ}，故 βk/q^r=q^{2cℓ/3−r}。r 和正 c 先固定，增大 ℓ 即可满足 k≥2m。源完备误差随后按 η_source≤τ/k 选择；这个块数修复不要求再让 ℓ 依赖 η_source。不能将该大 ℓ 结论泛称为所有任意参数 k 的下界。

**对既有固定色板任务的影响。** 实际检查了任务 `unrelated-machines-3a-3a-8091c8950447d8fa` 的定义/receipt、该包完整 review 和两条 canonical 的前提、roles、whole_result、explanation、scope、evidence、review_note。它们的完整目标始终是每个预先固定 k≥3 的“3-colorable 对 non-k-colorable”NP-hard promise。第一条由 FMW exact4/perfect completeness 支付 GS20 的 d=4 前提；第二条由 FMW Cor1.9 的八色/小独立集 gap，取 k→固定 C≥8→固定 δ<1/C，再走 GS20 Lemma8。两条均未使用 MZ 的 imperfect completeness 或 Claim 3.2。故新增 MZ 修复没有撤销、削弱或补充这些 canonical 的数学前提，应保留原边字节及 SHA。本文没有重新复证 FMW 全篇或 GS20 全文。

## F2：完整 P_gate 的正向见证逐任务展开

修改前一句对未选 selector 的去向过于简略；新句逐类给出的分配正确。定义域仍是有限显式 normalized menu，每个 state 的非负 incidence 权重和为 1，完整 ordinary-UM P_gate 包含 root pin、每组 connector/selector、所有 indexed-state incidence jobs。

令 β>0 的 balanced witness 为 H 和两两不交的 B_g，并对每个选中 g 选一个达到 v_g(B_g) 的 state s_g。则 β≤|H|/n≤1，并且所选 state 在 B_g 上的正权重至少 β。按新段落分配：

- root pin 在 root，未选组 connector 在 root，故 root 负载为 1+(n−|H|)/n=2−|H|/n≤2−β。
- 选中 gate 只承载 connector，未选 gate 只承载 selector，负载都为 1。
- 每个选中 attaining private 承载 selector 和未导出的 incidence，负载为 1+1−v_g(B_g)≤2−β。
- 其余所有 private（包括未选 state 和未选组的 state）承载原有全部 incidence，总负载为 1；零 incidence 留 private 的负载为 0，不产生遗失任务。
- 资源机器只承载见证导出的正 incidence。B_g 两两不交使每个资源至多接一个单位作业，负载≤1≤2−β。

因此所有原 jobs 恰执行一次，正向峰值界成立。原反向在 C<2 下利用 root 负载、单位 gate 冲突与单位资源独占提取 β*≥2−C，方向未变；β*=0 的完整基线仍给 2。故 OPT(P_gate)=2−β* 及其明示条件保持。没有把这一完整门控值桥推广到 flat compiler 或一般 unrelated-machines。

## F3：实际 schedule 的 Dirac S3 与指定点不升级

§14 的域仍为完整 normalized-flat 原变量体系、1≤T<2、指定 pullback A_s=a_s、Z_e=a_sE_e。新句正确地区分两个量词：

1. 一个给定 raw K2/CONFIG functional 未必满足完整 S3；原 §13 的共同 signed functional 仍以 L(b1b2b3)=−1/160 违反所需的全局三 literal 非负性，指定 pullback 的负式依然有效。
2. 若另有一个实际 threshold-T 完整 schedule，可在该合法 0/1 端点向量逐多项式取值，定义 L_σ(f)=f(σ)。Boolean/cover 等式在该点为零；boxes、physical slack 及所有 literal 乘子非负。在 T<2 的资源机器上，单位作业的整数件数至多一，故 unit-cap 行也满足。因此 L_σ 确为另一个 S3 functional（并满足所有相应平方非负性）。

这不使原先指定的 K2/CONFIG 点获得新矩，也不推出从一般 S3 可解码实际 schedule。它与“FAIL 单向排除实际 threshold-T schedule”正好相容。原句把实际 schedule 也列入“不自动产生 S3”的对象会被按存在性误读；新句修复了这一点，保留同点提取与换点存在性的严格分界。没有修改 S3→canonical-SA1 的次数账、quality 恒等式、K2 direct-pullback 反例或算法复杂度。

## 与新增 ∞ helper M-LP / cap 对象的关系

为判断是否存在真实共享承重步骤，只读取本地固定提交中的新 M-LP 正文 1–145 行（原定义、主定理、全部正/反向容量证明、规模/度和 CONFIG 正向入口），及新 cap 正文 1–150 行（精确模型、原始整数/CONFIG 值、完整 cap 参数分类、被否接口、D∞ 构造计数开头），并作其标题/source 位置定位。未再次完整阅读 281/220 行正文或其全部 primary。

已读内容足够确定这两条新证明使用不同的约束与对象：M-LP 为 maxmin.pdf Definition2.2 的逐物品容量、大端质量加 z、小端价值≥Mz、small x≤z、非负性；D∞ 证明由 helper 两个目标大端及 z_h=0 支付 d−1 单位占用，反向扣容量。cap 反族用共享/私有估值 v=(n−1)/n、a=(2n−1)/n²，独立证明 (0,a]∪(v,1]，再使用该 D∞ 保持接口。它们不调用 FMW/MZ 的 PCP 重复、P_gate 的 root/gate/selector 值桥或 raw S3 functional。共用“资源/配置/归一化”词语不足以形成依赖。

因此本 remote delta 不改变直接全正阈值 M-LP 桥、cap 非前缀、raw-CONFIG 二倍接口反例或其三度像。有限 unit-helper 的 actual/CONFIG separatebody 不是这三文件的修改目标，本次没有对它新增认证，也没有用 P_gate/S3 代付它的前提。

## 实际阅读及支持文件身份

- 读取仓库 `AGENTS.md` 和 `prompts/03-map-worker.md`，按父任务限定只作本增量复核。
- F1/F2/F3：remote 正文完整 138/175/157 行已读；base 仅读精确 diff 及其上下文，并通过 Git object 计算完整 hash。不得把 hash 计算写成 base 全文重审。
- Primary：`archives/unrelated-machines/tools/evidence/retired-literature-four-to-one-20261031/minzer_zheng.txt` 在 remote，blob `0dd6f6037320665b790d42a8b69bddd468ae4f74`，SHA-256 `50489f53b4a19fe224c3d70896b497f4640d36b977596a3ae7f0c2a25ecef113`，428656 bytes / 6398 lines。实际连续读 820–953、1315–1342、2988–3021 行，并按 Claim3.2/参数关键词定位。未重新渲染 PDF、未声称全文 6398 行再读。
- 既有 task JSON：local 固定提交下 SHA-256 `c654565ef475aef782b0821fc968560620a385b84bdc2c8b1d6452750d7d77ab`，blob `71ec7f3b511d9260be3de42dce639aa6ea35f056`；169 行完整 task/receipt 已读。
- 既有包 review：`map/edges/unrelated-machines-3a-3a-8091c8950447d8fa/review.md`，local SHA-256 `e7fe237e5dd9c815953daa9efacb9e67c7fd8445050d05793c6a308b2ee64997`，blob `35983b16a642ef53d745a95a76626fabac61cc85`；44 行完整已读。
- Canonical `perfect-four-to-one-to-three-color-constant-palette.json`：local SHA-256 `97eac092b022b11c8a303a5c3e5beb6c64342433c1e826290260aaed94e2f73b`，blob `c027769270ac600d8c2d8d7c723190e212076d16`。
- Canonical `eight-color-independent-set-to-three-color-gap.json`：local SHA-256 `c8bc2d5efd3b33c41c7fa15730785b5fa562592c1f7cbfd8987ba37618287917`，blob `ea64e0d04f4623043fc3dc9ae2188ab4c5c3ab59`。两 canonical 的 proof-bearing 字段实读；未重读其全部 linked PDFs/comparison-proof。两份原字节均与工作树相同。
- 新 M-LP：`archives/unrelated-machines/state/定理/无限helper链对阈值规范化MLP的全正阈值双向保持--定理.md`，local SHA-256 `f07cd5f7128a9e8ac0f4667b8e69f5d89905b8d4e4d999edd090612cb95a9dfb`，blob `993e47a9a5090f45ed49db092bc5a952eedf53d6`，26276 bytes / 281 lines；范围如上。
- 新 cap：`archives/unrelated-machines/state/反例/三度二无限度内capMLP非前缀与根号人数分离--反例.md`，local SHA-256 `b3454530c3cfff2700e16d39114ade01a645526863d5130efcc61e5253c3fece`，blob `f4fefe4a100edc58203d4898a27330207614a3be`，17129 bytes / 220 lines；范围如上。

另有 registration/workspace 路径定位和已存在 integration-review 摘要的定向读取；其中较大的聚合输出被工具截断，未把其未显示部分计作实读，更未用其代替上述正文检查。用于新增对象的 proposed registration 文件不在固定 local 提交中，未据失败的 git-show 推断其登记内容。没有全仓 registry 审计或全局关系扫描。

## 父 Boss 可直接采用的 disposition

- 保留 remote 对三个正式文件的全部 4/2 行差分。
- 保留固定色板两 canonical 原字节和数学结论；无需新增反驳边、条件边、外部 source 依赖或 Boss5 follow-up。
- 新 ∞ helper M-LP/cap 对象按父 Boss 已完成的独立证明与 registration 继续集成；本 delta 不引入新数学 gate。
- 如父流程按正文 SHA 登记对象/生成 reading pins，使用上列 remote hash 刷新相应身份；这是出处同步，不是重新审查本范围之外的 foreign task 或重放已有科学。
