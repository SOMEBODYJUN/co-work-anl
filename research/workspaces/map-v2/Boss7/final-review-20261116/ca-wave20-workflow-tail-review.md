# CA Wave20 workflow 尾句独立定向复核

Boss7，2026-11-16。仅审 Boss5 将 “The terminal-tax T/35 and equivalent-policy230 comparisons are saved mathematical preparation, not counted as done primary work.” 从 open_math 拆出并更新交付状态这一项；不重做六份 CA v7 链，亦不重新审定 Wave20 其余结论。

**采用本项清理，未发现承重误配。** 三个具名任务具有正式且仍有效的 done 收据，资产/输入/现行整合 pin 匹配。T/35、FREE230、付费230的数学分别实读，范围没有因 done 而扩大；当前 disposition 也明确不支付一般 full-tax、aggregate、commonQ 或 sequential half。

## 读到的快照与有效交付

17:11:48 UTC 的 integration SHA256 为 `cc347a484cbb0731788b9f98395fbab05a4c6676d60b788cea89b15c33b765ea`。17:14:34 UTC 观察到并发更新为 `c08cbe61cb3f074a4c82fada92835ff4868964d79123cca250c69c7092d8c0c9`；三收据 pin、四边 pin 与本项 open/resolved 文字均未改变。Boss5 编辑日志的 after SHA `b23d2a39…` 仅为其当时快照，未作为本次现行 SHA。

成文前再次读 `map/integration.json`：时间 `2026-11-16T17:15:49.498834+00:00`，SHA256 `c08cbe61cb3f074a4c82fada92835ff4868964d79123cca250c69c7092d8c0c9`。本报告不覆盖并发状态。

按 IMPLEMENTATION“定向替代”及 `tools/research_runtime.py::_effective_map_done`，只有 done 后继的 definition.supersedes 排除旧 done。本次只读反查全部本地 task JSON，三任务自身 supersedes 均为空，均无任何本地后继；故无需追继承，它们自身就是有效交付。三内嵌 receipt 与正式 receipt parsed JSON 相同；全部资产逐文件 SHA 相符，全部 core/read input_pins 和四边 endpoint_pins 与当前 integration.object_pins 相符，四边全部 evidence_pins 与实际文件字节相符。

- `customer-attraction-3a-3a-518b9d3ca3cd7082`，owner `Boss2`。task `research/operations/map-v2/tasks/customer-attraction-3a-3a-518b9d3ca3cd7082.json`，文件 SHA256 `aa62db4df1330df30d5acf74d08de3683bd7daea85ad0779d8db6f7c81559fbe`；正式收据 `map/receipts/customer-attraction-3a-3a-518b9d3ca3cd7082.json`，文件 SHA256 `af50b6d3fe0d69a219f31ce83791c605a67df28e5f4eaf5b359b79f472548f4f`；稳定 JSON 收据 pin 与当前 integration 同为 `43615b0cb9329d179db8306f8235380bdbd860ef9497c039ad868694f978e927`。
- `customer-attraction-3a-3a-be5b8b19d5f51a21`，owner `Boss7`。task `research/operations/map-v2/tasks/customer-attraction-3a-3a-be5b8b19d5f51a21.json`，文件 SHA256 `e0a1264a4f3873f3dac95d2772963fb76c24148e7ba7b710ba6c2618c55a5810`；正式收据 `map/receipts/customer-attraction-3a-3a-be5b8b19d5f51a21.json`，文件 SHA256 `b37c22f7981953fe3553229dbcedaf40f068b0bdc8358606e65d7eab17a13183`；稳定 JSON 收据 pin 与当前 integration 同为 `864ee805c8b82248bce12f71dc62c5108d21339d3168654dcbec34a6ae37be3e`。
- `customer-attraction-3a-3a-65bd2cb73d647bac`，owner `Boss1`。task `research/operations/map-v2/tasks/customer-attraction-3a-3a-65bd2cb73d647bac.json`，文件 SHA256 `95e87a6b8df8ee968548c802e0082b0b353579bc57da309727c45c70151a5655`；正式收据 `map/receipts/customer-attraction-3a-3a-65bd2cb73d647bac.json`，文件 SHA256 `7a52757d8de4cd642154a218c4ef686dfb6fea7a19723692d94581e37de948b3`；稳定 JSON 收据 pin 与当前 integration 同为 `ef7f604227c9d074b5b80ca9adf257f9d67dfa76eb1172060a81306da1ed62c3`。

当前 `archive_reviews["archives/customer-attraction"].open_math[23]` 保留：

> Wave20 pays the entire static PNE half theorem and two restricted cone/value steps, while the general sequential frozen-budget transfer remains unavailable. General full-tax/aggregate/commonQ and sequential half obligations keep their actual open or refuted status.

`resolved_workflow_notes[8].current_disposition` 分别具名 518b / be5b / 65bd，并明确“固定根A的同后继等锥及相应有限界不支付一般全终局税、共同Q、聚合付款或一般顺序half。”本次只认可这项历史交付状态清理及其实际数学限制；未重新核该段静态 PNE half 与另外两 restricted steps。

## 数学实读结论

**T/35 的准确量词。** 四人、六共同标签、63 非空兴趣型；固定 259 历史动作表 σ：前三深度恒 A，末位按旧 61 客户真实收益最大化、同收益偏大标签，随后不随新重数改表。Γ 为全部 1554 真实 IC 行，四槽逐位置计终局负载 c。T=Σx、W=Σ1[c>0]x、τ_full=Σc/(c+1)x。15 个四标签支持 J 的证书给 `w+t−o_J=ν_J·1+Γᵀλ_J+s_J`，λ,s≥0、ν≥1/35。因此所有 x≥0、Γx≥0（含零质量）满足 `OPT₄≤W+τ_full−T/35`。这是真正固定 σ 整锥的结论，强于只查有限点；没有支付其它动作表、目录或人数的一般 full-tax。七客户 x₂=x₄=x₈=1、x₄₉=4 达到 W4、OPT7、τ16/5、余量1/5=T/35。旧 61 客户前三槽税45/2和全税271/10必须区分；τ≤4W/5仍仅是容量。

**同后继等锥只限定第一族指定根 A。** 税 capture 与 FREE 原 root_tax_failure 动作表全部 259 项相同。强制根 b 的叶 `(b,A,A,L)` 与 h=(A) 强制 b 的叶 `(A,b,A,L)` 因末位只依前三动作多重集而同 L、同负载、同偏离者 b；六条根行逐类型等于 h=(A)（也等于 h=(A,A)）复制行。因此此根 A 的完整 IC 与正深度 IC 客户锥相同，根对偶乘子可移到非根复制行。若 a=W+τ−O_J−T/35、b=4W/5−τ、d=T−O_J，则

`7W/4−O_J=(35/36)a+(35/36)b+(1/36)d`。

后两项逐类型非负，故原 15 份税对偶给同根 A 全部支持 O_J≤7W/4；七客户点除4后，0123、1234、1235 三支持达到7/4。这里只另证这三项精确最优及全15项共同上界，不支付其余12支持更小的各自最优、另外五根或另三族。此根 A 真 δ 恒0，付费最优取 Δ0才与 FREE 一致。六根不能混同：仅 mask49 一客户在同后继全部正深度 IC 可行，指定根 B 收益0，改 A 收益1/4，所以 δ1/4。

**两个230的身份及目标不同。** 都取四张指定正深度后继表、20个实际根配置、90+16+120+4目标，W1截面；客户重数是整个非负锥的变量，原例客户不是固定 LP 输入。FREE 删除根IC并最大化 O_J；付费版保 `root_payoff_gap+Δ≥0`、Δ≥δ≥0，并最大化 O_J−3Δ，最优点Δ=δ。其正深度行均须从真实历史重建，不能对去重完整行集合“减根行”。

| 后继来源 | (m,p) / 目标数 | FREE 最大 O_J | 付费最大 O_J−3Δ |
| --- | --- | ---: | ---: |
| root_tax_failure | (4,6) / 90 | 7/4 | 7/4 |
| eight_cce_welfare_gap | (3,4) / 16 | 2 | 3/2 |
| aggregate_theta_failure | (3,6) / 120 | 149/103 | 33/23 |
| fractional_actual_load_failure | (4,4) / 4 | 5/4 | 9/8 |

付费版228达到点δ0；两份 fractional 根2、3点δ=Δ=1/24、O−2W=−3/4，它们不是完整根SPE反例。付费四锥仅排除这些指定锥的 OPT−2W>3δ，未证明普遍付费式；FREE四锥也不推出一般FREE-ROOT或half。两页均保W0边界。

**65bd交付完成不改变 isolated-after-review。** 此收据交付的是四锥与任意背景两尾接口的 checks/context 比较。只有m3两族可把根当合法旧前缀后调用两余者三比较O≤2W，且W含旧根覆盖；m4两族不在两尾量词内。518两条 implies 均保局部 contribution/remaining，be5b 为含根遗憾坐标的 conditional specialization。正式done与accepted不支付目标对象尚未得到的普遍量词。

## 本次独立核及证据

本次从保存动作表及payoff定义独立重建97902个Γ有理系数，与capture逐项相同；核根A在两深度的六条复制行，核15份tax有理原始/对偶及945转换坐标，并核mask49根B的δ1/4。两份原230 JSON的全部记录已解析以辨目标、计数、最大值和正遗憾记录；本次未逐坐标重验两份230的全部对偶，未运行原main、LP或发现搜索。程序/正文与保存证书的精确数学含义已实读，不凭done或status判定数学。

四条实读关系的文件SHA与现行integration edge pin：

- `map/edges/customer-attraction-3a-3a-518b9d3ca3cd7082/fixed-cone-pays-terminal-tax.json`：文件SHA256 `5d745e3dcdaa69d419a7749a5b4c5379b15588483e02af83022c8ad7c95d4dee`；edge pin `a83e45e683ab513ccb3a5791ea3ea76ac68ad0bbdf328b1a4e9e9d5a36dc6746`。
- `map/edges/customer-attraction-3a-3a-518b9d3ca3cd7082/fixed-tax-certificates-pay-free-root-a.json`：文件SHA256 `53186aceb40359dc55ea37e967360c2c0314bf8b47ef5064d71275e3e58a9f3a`；edge pin `d4e0b2d2b43498faad1ee20aaef263290b52be3b46934287af4df13d65f94865`。
- `map/edges/customer-attraction-3a-3a-be5b8b19d5f51a21/strategy-cone-specializes-positive-depth-root-regret-certificates.json`：文件SHA256 `e39fc653611828cd9411cdcee52bd8cc37bc86dcbbd739a7ef3777a396c99d50`；edge pin `8817bb79c8ae93537eab9f9c0998f86ebfddd12e721028e1264bbca0e10c481f`。
- `map/edges/customer-attraction-3a-3a-65bd2cb73d647bac/fixed-cones-check-two-tail-arbitrary-background-boundary.json`：文件SHA256 `fbcd3d0b2ecb4dc009626746fd12010abbf53150d298613741692bb91b21f0fa`；edge pin `1e64a8f29a85e11c4282964ac601e154ee9044338954d114efbb859801ca2f5d`。

关键实读来源的文件SHA256：

- `AGENTS.md` — `20293db840f907c32f774b0d7f72450c56e6c0ad937720699d14f7c02e693cc9`。
- `research/IMPLEMENTATION.md` — `fb6613cd0c429f28b8bcfb1064076a629540cfbee8f7e3d670b0b39e78ff0d4b`。
- `tools/research_runtime.py` — `414713215bc28a062a2ef0330b150f81298987e893278fe90b44b38c7f4d4023`。
- `research/workspaces/map-v2/Boss5/finalization-20261116/customer-attraction-workflow-note-review.json` — `15f2d606bdda33b00aa507f88f5871515648ce1d0ef53e332a1830cfdcfb3945`。
- `research/workspaces/map-v2/Boss5/finalization-20261116/integration-note-edit-log.json` — `82d38a3352078760a9925705348e27f0d42180a01f0e095a83f90011228e84bd`。
- `archives/customer-attraction/state/程序/完整策略客户锥的终局税探针--程序.md` — `eb2a26f26d4862ec891544404e5b722eccee24b764be9de8e03d564ab3cdac95`。
- `archives/customer-attraction/state/计算/正深度根遗憾锥的二百三十份有理证书--计算.md` — `e04c918a0319c4c1d7bf89d0109b978e46ac9fc38979f8ce7ce3b0ab841fb22d`。
- `archives/customer-attraction/state/程序/任意指定根四后续策略锥的原攻击与全部有理记录--程序.md` — `939efd90923cc30640c3f69dfe86051570aafc702bc9506592e8c5336c0b7b9f`。
- `archives/customer-attraction/tools/evidence/terminal-tax-fixed-policy-probe/replay/capture.json.gz` — `822bc77673cf4af08206acf04a91f588db7f10e4ea61bcf0ce8effbfc9d1eeae`。
- `archives/customer-attraction/tools/evidence/terminal-tax-fixed-policy-probe/exact-audit.json` — `52ba6139d795a5b7ad8de0bd52e4dd20c1b4db1f47aef147129d9b4532e25b94`。
- `archives/customer-attraction/tools/evidence/d398-parent-diagnostics-primary/original/root_regret_probe.py` — `5d055514b60fd8e3e92076c23e36142253bb3d62bbf2d82dcb983c7e1a56f7ef`。
- `archives/customer-attraction/tools/evidence/d398-parent-diagnostics-primary/original/root_regret_probe.json` — `8440166fc55f8974f4e5c65e6dc6a960df6af4c0b4c9fb43fab171f2019cc732`。
- `archives/customer-attraction/tools/evidence/arbitrary-root-regret-attack-two-primary/original/research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/credible_attack/root_regret/attack_arbitrary_root.py` — `cb3b9878ba1a4d6192bb7583d76c913b95dcf9a0b303159729223288e43a159d`。
- `archives/customer-attraction/tools/evidence/arbitrary-root-regret-attack-two-primary/original/research/workspaces/customer-attraction/R-65d0f88edf3849b39ca5eb79760e970b/credible_attack/root_regret/attack_arbitrary_root.json` — `df987b3c4bc28f6b074d77788c9ce901ab2ffa0f52682f216fcb382d1c6b0cf5`。
- `archives/customer-attraction/tools/evidence/arbitrary-root-regret-attack-two-primary/original/evidence/certificates/customer_attraction/root_tax_failure.json` — `59fd58d85a3c3b989837467eb3523286d1f5ee529b0f119cd4d263bef6984111`。

执行边界：唯一写入为本报告；未执行Git/sync/work.py/队列/公屏/checkpoint，未修改canonical、任务、边、收据、registry、coverage或integration，未读凭据。
