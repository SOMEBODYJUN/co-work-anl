# 结构参数正文：指定远端增量与任务 850 的定向复核

结论：应完整保留远端的零计数修正和四对象 v3 记录。任务 850 的 M247 → M14 FPTAS 贡献在数学上仍成立，原证明无须改写；但远端注册输入已经变更，原边、任务和收据仍绑定 v2，不能直接宣称当前有效。应按 done 任务定向替代流程复用原论证，更新证据和两端 pin，并明确处置旧资产。

## 精确比较范围

- base：`56650ea6813513decee236e0353647e07ff7cc63`。
- remote：`724c402aeef432b2e6848fe1b1b67a0ddae33ba3`。
- 主正文：`archives/unrelated-machines/state/文献/结构参数下的指派限制调度--文献.md`。
- 数学合同：M14、M247、M232、M345 的上述两次提交中的完整 registry 记录。
- 任务资产：`map/edges/unrelated-machines-3a-3a-850a6179151b732e/`、对应收据及任务定义；旧边、review、ledger 均完整阅读。
- 操作规范：根 `AGENTS.md`、`prompts/03-map-worker.md`、`research/IMPLEMENTATION.md` 的登记、边与定向替代要求。

本报告的远端判断来自 `git show REV:path` 与两提交间的 `git diff`，不是用正在合并的工作树猜测远端。没有执行 work.py、队列写入、Git 写操作或旧数学程序；没有重读 19 页 PDF、重新审计其他文献或接手 Boss5 的任务。

## 唯一正文变更及独立数学核对

正文差异严格为一行替换，位于“Rankwidth DP 的状态压缩”。base 的计数上界为

`n^{κ(e,b)d} ≤ n^{2^k d}`。

remote 改成：各类型/尺寸的计数状态数精确为 `Π_{h,s}(φ_{h,s}+1)`，从而

`Π_{h,s}(φ_{h,s}+1) ≤ (n+1)^{κ(e,b)d} ≤ (n+1)^{2^k d}`，

并说明零计数必须包含在内，原 PDF 的 Remark 20 漏了 `+1`。

这个修正正确：固定跨切类型 h 与任务尺寸 s 后，其可选子多重集由整数 `ι_{h,s} ∈ {0,…,φ_{h,s}}` 决定，恰有 `φ_{h,s}+1` 种选择。各坐标独立枚举，候选向量数为乘积；若后续守恒、可实现性约束筛除状态，实际保留数只会更小。每个 `φ_{h,s}≤n`，坐标数至多 `κd`；cut-rank 的 k 维 GF(2) 行空间最多有 `2^k` 种邻接行，所以 `κ≤2^k`，两个不等式均成立。一个任务的单一类型/尺寸就有 0 和 1 两种计数，足以反驳旧式在 `n=1` 时给出的 1 种上界。

这个修正不改变类型翻译函数、任务守恒关系、Lemma 21 的 minimax 递推、叶子可行性或舍入与回译。对固定 k、d，`(n+1)^{O(d2^k)}` 仍为多项式。正文保留的论文渐近写法 `O(m 2^k n^{O(d2^k)})` 也可保留：对 `n≥2` 有 `n+1≤n²`，可吸收进 O 指数；`n=0,1` 可直接处理。没有新的 rankwidth PTAS 缺口由此产生。

因此本次唯一直接数学受益对象为 M345 的计数状态解释。treewidth 三个结果完全没有承重公式发生变化。

## 四个对象的精确记录差异

四个记录均只有两个字段改变：`body.sha256` 和 `version:2→3`。对象身份、title、model、statement、quantifiers、assumptions、scope、truth_status、kind、objections、evidence、sources 全部逐字段相同。没有偷偷改换定理、模型或前提。

| 对象 | 远端版本 | 远端 registration pin | 本次数学影响 |
| --- | --- | --- | --- |
| M-14dbe6980117492aa7a3b48c52378dcb | 3 | `b4a7cba894657b841b9c88baf9c45f372ed6f7cbbaca225813ea6933b6d7c0ea` | 常数 dual/incidence 树宽 FPTAS 与独立弱 NP-hard 合同未变；共享全文引用刷新。 |
| M-247deecec83946358afe4e89413a7bd1 | 3 | `f2082f5eaf3a9d65644b2cfe1be641dca8c0d1013cf4712153ec597b09f36f07` | `L^{O(k)}O(nm)` 精确负载 DP 与双参数前提未变；共享全文引用刷新。 |
| M-232414c2d8e744ccaba95138638a15dc | 3 | `037638b148f2b51444341f14dc95545968466fd4541106af21854e842e91db76` | primal 精确 FPT 合同未变；共享全文引用刷新。 |
| M-3452046f3bdd47c48b17a0a3038ba4b2 | 3 | `123edc333d989cf39bad49b906105e6da8f08f300912fec22f7d62f62e7a0da9` | 固定类型/尺寸计数补含零状态；PTAS 量词和渐近复杂度未变。 |

pin 按仓库 `tools/research_runtime.py::pin` 的规范，即 UTF-8、`ensure_ascii=False`、key 排序和紧凑 JSON 的 SHA256，直接由精确提交的记录计算。base 的 M14/M247 pins 分别为 `2e991ac64d1bc297760daccd30f713ae70c2bdaa42bb3e54a02ae554563a4e86` 与 `fd687a135427e3d9654468452b5db3a8279a4f60bfa41d99904b9d214a241a41`，与原边一致。

正文的原始字节：

- base SHA256：`b2ae90415d0b340c9c0039bf68005854f06b0da4acc35e0f44a22a97d2ebc5ed`，18,718 bytes。
- remote SHA256：`f322df148d7781110aa8b4460adcbcd1cdffbc2f857ca93f5536abefa6f5fa3a`，18,922 bytes。
- 原 PDF 的证据 SHA256 仍为 `4b47eaccfcffe81f6713522269b6afa2124bec3d619d6ef3a1b5341db7e48bae`。
- remote registry 的 material 记录已同步至 `f322df…`，owner 集仍为上述四对象。
- remote registry baseline 为 `research/registration/baseline-boss5-local-proof-fixes-20261111.json`，SHA256 `956ed86acb2d7cfdc81b54766dea42ad95a5444db17be9be4ab672c65178cb89`；该 baseline 的对应 material 也是 `f322df…`。保留这次完整分母更新，不能用旧 baseline 覆盖。

## 任务 850 原证明为何仍成立

原边 `um-constant-tw-exact-load-dp-contributes-fptas-850a` 是 `accepted / unconditional / ALL` 的局部贡献，source M247，target M14，只支付 FPTAS 算法，独立弱困难性保在 remaining。它完全不使用跨切类型计数的 `n^{κd}` 估计。对本次 delta 定向重核其承重链如下。

1. **可计算上界。** 逐任务选择最小有限处理时间的机器，所得合法调度的 makespan 为 `B_min`。任取原最优调度，每任务最小端不超过其在最优机上的时间，而后者不超过 OPT，因此 `OPT≤B_min≤Σ_j min_i p_ij≤nOPT`。这一步不调用未付的 LST 2-近似，也没有把 `B_min` 冒作 `≤2OPT` 上界。
2. **网格。** `ε0=min{ε,1}`、`q=ε0 B_min/n²`、`a_ij=ceil(p_ij/q)`。空任务、无资格任务、`B_min=0` 按原 review 的分支先处理；其余 `q>0`。原最优调度每机至多 n 个任务，故 `q load_a≤load_p+nq≤OPT+nq`，且 `nq=ε0 B_min/n≤ε0OPT`。
3. **cap 和零负载。** 设 `K=floor((B_min+nq)/q)=floor(n²/ε0+n)`。至少一份原最优调度的缩放副本落在该 cap 内，缩放最优值不更大。局部负载是最终负载的非负子和，中间裁剪不丢该见证。负载状态本来是 `0,…,K`，共有 `K+1` 个，原边没有犯本次 rankwidth 漏零计数错误。
4. **DP 与结构。** M247 明确给出负载 DP 的 `L^{O(k)}O(nm)` 时间，而非任意 `f(k,OPT)poly(input)`。代入 `L≤K+1`，固定 k 得到输入与 `1/ε` 的多项式时间。向上取整不增加资格边；删除超 cap 的单端也不增宽。dual 分解转 incidence 分解使用正确的 `|M(j)|≤k+1` 团界，宽度至多 `k+1`。原 review 的 incidence flag/load 实现按任务是否已分配与机器负载记录，忘任务时要求已分配，join 时任务标志和至多 1、机器负载相加；每资格边只介绍一次，语义正确。
5. **恢复和位复杂度。** 精确缩放最优调度回溯后，`C_p≤q C_a≤OPT+nq≤(1+ε)OPT`。用 `ceil(n² v p_ij/(u B_min))` 的整数除法计算缩放值，操作数位长为输入与精度编码的多项式；状态数组依 K，而非原处理时间数值大小。固定宽度分解的 `|V|^{O(k)}` 搜索只需固定 k 的多项式，原 review 已给其边界连通性和根袋论证。
6. **作用范围。** 两机 PARTITION 特例仍给独立弱 NP-hard 性：dual `K2`，incidence `K_{2,n}`，树宽分别 1 与至多 2。本边仍只提供 FPTAS 的 contribution，不应扩成 whole_result。反向利用 `ε<1/OPT` 也没有补出 M247 的完整参数对 FPT 合同；保留原不加反向边的判断。

先前已经修正的团界减一、cap `B+nq`、primal cone 旁注、大任务 `δ²B` 网格和 incidence 守恒语义都完整保留在 remote；这次没有任何理由撤回它们。

## 原资产仍有效的内容与当前失效的绑定

以下资产在两次指定提交间逐字节相同（不是仅无 diff 的推断，已分别计算 SHA）：

| 旧资产 | SHA256 |
| --- | --- |
| `exact-load-dp-to-fptas.json` | `a726448138447c62ac6115750d6149817d5fd8cddf0182937f14bb5f140cf2a5` |
| `review.md` | `5f958ba7b25b627252cbc6a06eec9abfa0125fb72348dd15ed6038936f0a4ade` |
| `reading-ledger.json` | `bd76823f72b2eee0de5094e91b55873cad73ba45b00c5d153f4706028734dc8d` |
| 对应 task850 收据 | `419c73b1f6d4d586cb8b9e07fa32dd5ff792484b88a1fa5ae57b8495b1ef16c5` |

原边的 `endpoint_pins` 仍为 M14/M247 v2；正文 evidence/evidence_pins 仍为 `b2ae904…`；旧收据 coverage 的 `object_pin` 与旧 done 任务 `input_pins` 也仍为 v2。按远端 v3 记录，至少这两端 pin 与一个正文 evidence 已 stale。边的论证成立，不能据此把旧绑定当作 current。

## Root 可执行的最小修复

1. 合并时保留 remote 的正文、四个 v3 记录、material SHA 和新 baseline。无需因本次 delta 再升四个对象至 v4；若 Root 另改对象内容，则最终 pin 应从最终合并记录重算。
2. task850 已 done，按 IMPLEMENTATION 的定向替代机制发布其 repair（`supersedes` 指向旧任务，核心仍 M14、共享只读仍 M247）。不要只改旧 done 的本地任务 JSON 来制造新有效交付。若已有别人发布的有效替代，先继续该替代，避免重复。这里没有执行任何队列动作。
3. 新边复用同一数学关系和完整推导，保留 contribution/remaining、ALL 与 unconditional。正文 evidence 改为 `f322df…`；最终 endpoint pins 用表中 v3 值；reviewed_note 补一句“精确提交增量仅补 rankwidth 零计数，不影响 treewidth 贡献，原证明已复用核对”。在新路径下重新 bind 和 edge-check，得到新的 evidence_pins/review_digest。
4. 新 review 保留原舍入/DP/位复杂度/困难性段落，附上本报告的唯一增量说明和新 current-version 表。旧 review 的“最终当前版本 v2”属于原交付时点，可改为“原交付时点版本”或在新 review 明确其历史性质；不要全局替换原始阅读记录中的旧 SHA，避免把历史阅读伪装成后来已读。
5. 新 ledger 保留原阅读范围，新增 delta revalidation 条目：两精确提交、远端全文 SHA、M14/M247 v3 pins、唯一计数段的阅读与上述乘积证明。不要声称本轮新读 PDF 页13–19或全19页。M232/M345 只做本次精确字段差异核对，不能虚报其全证明重审。
6. 新收据 coverage 为 M14 `linked`、pin 用 v3、新边 ID 列在 edge_ids；新 edge/review/ledger 的最终 SHA 列入 assets。在 `supersession` 对旧三个资产逐项给 `replaced` 与实际 replacement_paths；若确实保留某旧文件原字节，才能用 retained 原 SHA。旧边因为绑定 stale，不应仅 retained 后继续充当当前接受逻辑边。
7. 对 M247/M232/M345 其他队列包只按真实最新远端归属刷新，不在本数学比较中接手或重派 Boss5 的任务。四个对象身份和数学陈述都没有新研究缺口，无需因此创建 3B/3C 开放问题。

本报告未修改 clone。唯一写入范围为 `/workspace/scratch/62622ba39554/staging-structural-remote-delta/`。
