# Q_D 低峰解码障碍的定向源差分复核

任务为 `boss2-wave10-repair-27a28f031620be97`，唯一核心为 `M-4bfb99ccca4f4f77a6aaee6882ef1170`。本文件记录本 worker 的实读、数学复核和继承边界；旧目录不改写，交付的支持边保持原 `b5-qd-and-private-tree-config-force-decoder-parameter-growth` 身份。

## 当前合同及精确版本差分

| 端点 | 当前版本 | 当前 registration pin |
|---|---:|---|
| `M-4bfb99ccca4f4f77a6aaee6882ef1170` | 1 | `ffff30e05741e26c01e4451d09bdfb6d40401902d39594f7db2d775ddb904781` |
| `M-9452d445c1744d5eaac946ee974d2162` | 4 | `cddd9bf3289e55ce350e792f70fdfea147cf0b44bfc0da08d9355f0c40a48e64` |
| `UM-Q-PRIVATE-TREE-BOUNDED-MULTIPLICITY-CONFIGURATION-FLOOR-v3` | 2 | `ac628d8a3fbf87017b10a2aa913e6d6485c9f01ae2a3175f276c5017bb28a5a1` |

三个完整当前合同均已定向实读；当前 task 定义的 canonical JSON pin 重算为 `bc69c7013f33ca250f83e58309295a038547fb0dad35d247a06b80289c8e5161`。所属、远端 claim 与 pushed 前置由 Boss 提供；本 worker 未操作队列或 Git。

旧边的 Q_D 是 v2，pin 为 `4f17391d9a650c85fd816ba6878831d96f6b046bc69a1e8a5e5bcf77749ccd41`。从现行 v4 record 删除这次零 jobs 的 objections 尾句、把版本减至 3、仅将共享审查证据 SHA 换回 `63629abaa5cd2bcc0e42ff051936b91882ea63c711dfdac231f238763b682255`，精确重算出 v3 pin `4126eff22b627cb6b93e95ca4c20542452b045c2df488d91bdbb5f4fd99f4e32`。再删去 P_gate 全任务调度的 objections 尾句、版本减至 2、共享审查 SHA 换回 `a5d9a684e8d8413457f5cf999e28b8a6aa93b140256be3031d6f3e2e02742195`，精确恢复旧边 v2 pin。此逆构是本轮按 canonical JSON 规则重新算得，未读取 Git 历史。

两次变版均未改 object_id、title、kind、truth_status、model、statement、quantifiers、assumptions、scope、body 或 sources。v2→v3 的实际变化是共享审查§一.1补全 **P_gate** 的全任务正向调度：root pin 留 root，选 connector 去 gate、selector 去选中 private；未选 connector 留 root、selector 去 gate，其余全部 incidence 留 private。此叙述不把 gated 的 balanced β 与 flat 的全组 max-min V 混同。v3→v4 是同页§二.1修复零 jobs 的配置覆盖摘要，未改变 Q_D 源数学。

## 唯一即时源差分与逐 job 覆盖

共享审查 `archives/unrelated-machines/state/审查/归一化菜单福利与配置证书双源审查--审查.md` 的现行 SHA 为 `33bd31b883b26f49508808dd7175cd104f391b86642bff90ea2bce7f1142097b`。将唯一一次

> 以 1−λ 权重放全部 incidence jobs（含零 jobs）；

反向替换为旧句“以 1−λ 权重放所有 positive incidence；”，完整文件原始字节 SHA 精确恢复 `63629abaa5cd2bcc0e42ff051936b91882ea63c711dfdac231f238763b682255`。主定理原字节 `8bfbaa80b98546b6d1320e9760bb9491165e26a6cef1b6cd35eb86116c822f66` 的§1本来已正确。

把一个 normalized state 的 jobs 分成正私有时间 I₊ 与零私有时间 I₀。private 机以 λ 取 `{selector}∪I₀`，以 1−λ 取 `I₊∪I₀`；两配置负载均为 1。每个零 job 的 private 覆盖为 λ+(1−λ)=1；正 job 的 private 覆盖为 1−λ，唯一 unit resource singleton 覆盖 λ，合计仍为 1；selector 在本组全部 states 的覆盖为 Σλ=1。只以正 support 收取资源列容量，资源余量取 empty，零 jobs 无需资源 singleton。未选 states、indexed duplicates、λ=0/1 和显式 unused resources 仍保原身份。

Q_D 的所有 incidences 私有时间为 1/D 或 1，均严格正；因此原边使用的 selector singleton 与全 incidences 的两配置已经完整。补句不改变其任何参数或解码计算。

## whole 必要参数定理的实际复核

所有整数 D≥2 均使用原完整 flat 普通 UM Q_D：每 state 独立 private、每资源独立 unit 机、每 group 一枚 unit selector、每 incidence 一枚独立原 job，全部 states 的 jobs 保留。其三项源事实分别为 actual 菜单值 V=1/D、完整 machine CONFIG(1) 可行、完整 flat actual OPT=2−1/D。整数值的上界来自 main 同行取两件 g 会迫两个 helper 同取唯一 A_a 的不交矛盾；取一件 g、相应 helper 取 A_a、其余 helper 取各自 g 达到值 1/D。整数全任务值桥与分数 λ 证书是两条独立论证。

目标必须是原 v3 完全私有、全局 d,h≥1 的显式满 d 叉高 h 普通 UM：不同 states 的内部机也私有，root selector 为 unit，每内部/leaf job 的父端 1/d 与唯一子端/外端 1，无其它 jobs、预载或有限资格。μ=max|f⁻¹(z)|≥1 是每**完整 state**的最大叶逆像重数，跨 root/state 总共享次数不受该 μ 限制。

在完整目标 CONFIG(1) 下，v3 给同一共同 λ 及真实 multiplicity 容量；T=1 时 a=d。令 r=ceil(d/(μ+2))。由于 d≥(μ+2)(r−1)+1，有 b=d−μ(r−1)≥2r−1≥1；h≥1 的凸性给 (2r−1)^h+1≥2r^h，故 b^h≥2r^h−1，且 μ(r−1)<d。rainbow blocker/Haxell 的已证有限存在性于是支付 root 间资源不交的真实 r 子树选择。

完整实际回填始终使用原 d 与原处理时间 1/d：活跃内部机是一件 incoming unit 加 d−r 枚 small，负载 2−r/d；全部未选/零 λ states、原 d 树未选枝的 jobs 均父置，非活跃内部机负载 1，外机至多一件 unit。每个原 job 恰排一次，存在完整目标实际见证 σ′，C′≤2−r/d<2。辅助 a-tree 不改变机器、任务、资格或负载分母。

本目标定理内部的 actual decoder 前件是：**对每份完整目标实际调度，峰 C<2 时存在全部 Q_D 原 jobs 的完整调度，峰≤C**；不输入未知 OPT，不附算法性。对给定有理 C<2 的每份实际调度同样逐份成立，ceil 阈值未被连续松弛。将该前件用于上述 σ′，有 2−1/D≤C′≤2−r/d，即 Dr≤d。r≥1 给 d≥D；r≥d/(μ+2) 给 μ≥D−2。Q_D 实际下界与 v3 实际上界须共同使用，保单条两源 ALL，不能拆为任一源独立足够。

若仅知整数 μ≤μ₀，同一定理可用较松 μ₀，仍必要有 D ceil(d/(μ₀+2))≤d；D>μ₀+2 不可能，D=μ₀+2 时 D|d 仅为必要条件。固定 d≤d₀ 排除 D>d₀。保留全部非空有限域和完整 assignments，目标 CONFIG1 给 OPT′<2 且两侧最优值均达到：decoder 应用到目标最优调度推出 OPT_D≤OPT′；反向对每份低峰目标调度取同一份完整源最优调度，得到峰不增的存在性输出。因此在该域和 CONFIG1 前件下 decoder⇔OPT_D≤OPT′，不构造算法。

整条支持边证明的是“若该完整 CONFIG1/actual-decoder 合同成立，则参数必须增长”的已证蕴含定理；编译合同是目标命题内部量化前件，未作为已存在的编译资产。因此保 accepted/unconditional 与原 whole_result。若把一个已给 actual decoder 接口专门用于 Q_D，必须同时保留上述 Q_D 三事实和原 actual decoder，输出仅为 Q_D 的新完整实际低峰解码保证；本边使用该保证导出参数必要条件，未把接口认证升级为一般 CONFIG、raw K2 证书语义或共同整数 law。

N 的 binary-selector/port 正规形具有各顶点自身 selector、其它时间与共享方式，不能按图上二叉认作 d=2 的 v3 完全私有树。参数充分性/锐利性、满足合同的编译存在、变参数位多项式输出、一般 UM hardness 与一般近二不可能均非本边结果。

## 本轮阅读与继承边界

本轮完整实读 AGENTS、worker 提示词、任务和前任务全文、旧 support 与旧 receipt；IMPLEMENTATION 的阶段/预算/登记规则及完整第三阶段和定向替代接口已读。完整实读目标定理、flat 主定理、Santa/UM 值桥、当前共享福利/配置审查。私有树主定理实读“精确模型与域”“CONFIG(1)的共同full-state λ消元”以及有界重数 v3 整节至“冻结配置审查的独有发现”，未冒称把较早 v2 注入正文全篇重新审计。

预核 `research/workspaces/map-v2/Boss2/recovery-20261112-e8cf4c/qd-decoder-source-delta-precheck.json`（SHA `44326f85e8829bce6eb2d72964e39cd559193da17796d8b05ffe418f1ea23ca9`）完整阅读后独立重算本轮源差分、全部 10 reading_refs 的当前文件 SHA、Q_D v2/v3 逆构 pins、旧资产 SHA 与上列承重推导。source-correction 记录全文及 zero-impact/macro-3D 中本任务版本差分和数学范围相关段落用于版本追溯；这些较大报告的别包范围未认证。

三个未变 flat 审查（Exact/Proof、row3/degree9 预 Exact、v1/v3 独立/作者）、v3 资源合同与四源审查按原 worker 已成熟审读继承，本轮仅核其当前完整文件 SHA 与任务 refs 一致。外部 Annamalai/Haxell PDF、历史 scratch Exact/Proof、旧程序及有限证书的审计同样继承；没有本轮新 PDF 实读、新外审、新独立盲审或科学程序重跑。

旧 task 未声明 follow-up overlap 或 follow_up_tasks，未发现需新增只读端点的本包证明缺口。四份旧 direct evidence 的原 SHA 全部未变。唯一旧资产 `map/edges/boss5-474257b8-qd-decoder-3a-69d5a688c474b34c/support.json` 保持原字节 SHA `92611abbd9eaf8072df600f345908257e578c54a06d7d1817d7ed6c6864e27a2`，由新目录 support.json 替换其现行角色；旧路径不覆盖。最终 native bind/check、receipt 新 SHA 刷新及 pushed/done 由 Boss 在语义稳定后处理，本文件不声称已完成这些步骤。
