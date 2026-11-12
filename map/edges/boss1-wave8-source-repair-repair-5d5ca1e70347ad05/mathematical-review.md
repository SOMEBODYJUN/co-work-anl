# 合法尾族、有限根与固定负载正核的定向修复

本稿对应任务 `boss1-wave8-source-repair-repair-5d5ca1e70347ad05`，沿用 Boss1，内部核对词 `FINITE2-CURRENT`。任务定义原生 pin 为 `f7176ff87884881d37dbb7bda50d9cd53ef939c696deaa490d16c2a5a777ea67`，本轮核查时任务为 claimed、owner Boss1；已推送的派工依据由父 Boss 提供，本 worker 未访问凭据、未查询远端、未写共享 clone、Git 或队列。

本轮结果是准确复用一条已有 accepted/unconditional/specializes 的局部 contribution，并重交两个核心的当前覆盖。边 `cag0bb-legal-tail-family-specializes-finite-p2-p3-tail-payload` 的原文件 SHA `09620034ec80aafd12c1b376c678b45b2846f622a1f4e89683a13d633318f231`、端点 pin、证据字节及审读摘要均保持当前。没有新增或改写逻辑边，也没有重复 edge_id。

## 输入究竟改变了什么

六个任务 input pins 全部独立重核与当前登记相同。两个核心 M-99341ce9d6544f5fa702a372e617f03b、M-be4510d9c7b844f0830fb90f34bfe7af 仍为 v2，pin 分别为 `13b73ac9158fc6cb4735c192e87cb4ce7b24c3df0cfd427af384b7601fdea8f1`、`b64d95cb28098a7d2a6171ca1aa65ede53e8cb2b471d6625bca6829c1b310636`。合法背景族及两个定义输入也未变。

旧 done 包唯一过时的只读输入是 p1 的 `customer-attraction/actual-prefix-fresh-coverage-global-counterexample`：v4 的 pin `7496d3ac6c5ba7c1dbebb37408f2a8f77c42ff7c793bd46c49de55597f503615` 已变为 v5 的 `e2905ccdb431606ece1925a18b114090cb464352225866e952b1aa59501d9be7`。本轮从已发布修正提交 `b03a23a02e828a6c920d35db9e315d21da5cd732` 的前版本作只读比较，独立核实：

- 对象仅 version、objections 的追加说明、evidence 中一处完整文件 SHA 改变；数学陈述、模型、量词、主文和其它证据引用不变。
- `R-2fc背景遗憾探针与无碰撞五客户负载桥--障碍.md` 的完整字节差恰为“五客户固定实例”节中的“源报告对应四个客户的主题集合”改成“源报告对应四个主题的客户集合”。旧/新 SHA 分别为 `f7fd1bc59bbfc1090203a9909274ea2b1704f9eaf382fac37272f371cd0c4d07`、`d049f4ce14db153c68e7ec3711c3944eca6919a30d31145b66d2feee822a1cbb`。
- p1 对象实际引用的 `background_regret_probe.py` 有限 Markov 锥探针节逐字节相同。它只是历史浮点随机探针，不是52客户实例或完整根证书；本轮未运行它。

所以本修复刷新 read input，而不改变已有贡献边的数学。M993 过去“尾收益差0”的登记量名问题早已在 v2 改为“新增覆盖 Δ=0”，此次没有再改记录或源。实际末首收益差仍是1；旧建议的精确前后语句与纠错理由留在保留的旧 mathematical-review、narrow-review 和本稿，不再把已解决建议当作当前行动义务。

## 一般合法尾族支付的精确有限特化

六标签按 A,B,T,Q,R,S 编号，十类不同单位客户的重数如下。这里不是自由负载或扩大目录；背景由合法有序前缀 h=A^pB^p 生成。

| 兴趣掩码 | 一般重数 | p=2 | p=3 |
|---|---|---:|---:|
| 1 | (p+1)(p+4) | 18 | 28 |
| 2 | (p+1)(p+5) | 21 | 32 |
| 4、8，各自 | 2p+3 | 7 | 9 |
| 20、24、36、40，各自 | 2 | 2 | 2 |
| 49、50，各自 | (p+1)(p+2) | 12 | 20 |

本轮实读一般族全文、有限根证据主文全文及两个短根审计 JSON。逐型代入与两个成熟根审计完全相同，总客户数分别85、126，玩家数为6、8。用 a=2p+6、b=a+1，源的完整两人尾局首选 A，末位对六个首动作的回复为 `(B,R,R,R,S,R)`。源正文列出全部36格末位收益，并证明每个指定回复为行最大，六个尾首真实偏离收益都等于 a。因此它确实给每个 p≥0 的完整合法背景尾 SPE，包括离轨节点和平局。

同一十类型对 R、S 对称。原根在 h 后的实际限制为 `(B,S,S,S,S,R)`，不是源手写尾策略逐节点相同：它们恰在 hB、hT、hQ 的三个离轨末节点选择不同的 R/S 同值最佳回复。在 B、T、Q 三行，两主题的末位值同为 b；尾首相应的收益也都为 a。其余回复相同，实际继续均为 AB。此判断来自本轮实读的解析表和成熟84项 Fraction 接口报告；本轮没有重新运行这84项尾 IC。

本轮对两个完整动作流做全字节 SHA、长度、数字字母表、末换行核验，只解码实际路径、h 首动作和六个 h 后末回复。实读了必要短合同，未逐节点语义重读全部动作、未执行全树 IC。选择性解码独立确认 AABBAB、AAABBBAB 及上述原根回复向量，与旧证据一致。

| p | 实际完整路径 | 根 W / OPT | h 后实际两人收益 | 尾利润 P | 新增覆盖 Δ_cov | fresh 最优 |
|---:|---|---|---|---:|---:|---:|
| 2 | AABBAB | 63 / 85 | (10,11) | 21 | 0 | 22 |
| 3 | AAABBBAB | 100 / 126 | (12,13) | 25 | 0 | 26 |

对 p≥1，过去已经覆盖 A∪B，尾 AB 不覆盖任何新客户。所有原负载零客户恰为 T∪Q，它们不交且每主题有 b 人，所以两主题最大新覆盖恰 2b=4p+14；尾总利润为 a+b=4p+13。于是同一个前缀对每个实 λ 均有

\[
P+\lambda\Delta_{\rm cov}-O_2(h)=-1.
\]

这些数字和完整合法尾机制正是源族在 p=2、3 给目标的局部贡献。p=0 时背景为空，新增覆盖另算，不能外推上述正参数 GLOBAL 亏损。源同族保护集合价格 B_(T∪Q)(a)=2>b−a=1 的证明也保留，但不是本边新增的根可达结论。

## 根实际可达与完整 IC 的付款边界

M993 整条结论还要求两份指定完整根 SPE、h 的实际可达，以及所有有序决策节点的真实偏离 IC。独立成熟根合同分别支付9331节点/55986项含自身比较和335923节点/2015538项含自身比较。比较在每个有序历史按同一给定策略的真实新历史续行；只缓存终局收益，不把策略商成计数函数。本轮核验原策略字节仍为它们指定的 SHA，复用成熟全树审计，没有重跑根生成、逆向归纳或完整 IC。

在独立根证书给出实际终局 hAB 后，覆盖数字还可直接由输入核对：W=|A∪B|=(p+1)(4p+13)=63、100；A,B,T,Q 盖全部客户且玩家数至少4，因此 OPT=N=85、126。覆盖算术本身不给出“hAB 是完整根 SPE 的实际终局”。两根均满足 2W>OPT，不是六人或一般根 half 的反例。p1 的52客户四人具体259节点根对象也不是从这两个有限根推出的。

因此保留边的 accepted、unconditional、specializes、premises_mode=all 和 contribution.result/remaining。局部特化已经证明，不需因一般 p 根可达开放而降为 proposed；但不能改成 whole_result，也不能去掉余项。根证书是目标的独立证明来源，未被源合法尾局定理取代。一般 p≥4 的实际根可达解析证明仍未付。

## 同终局子树替换的完整联合前提

旧数学稿保存的拼接证明成立，且只在完整联合前提下使用：已有完整根 SPE σ；同一合法 h 子博弈有另一完整 SPE η；两者从 h 实现同一完整终局。把整个 h 子树替换为 η，得到完整根 SPE σ′。

证明按全部有序节点分三类。h 子树内的 IC 由 η 支付；与 h 不可比较的节点及全部后继未变；在 h 的每个严格祖先 g，对 g 的每个当前候选行动沿相应完整策略完成，路径若不进入 h 则终局不变，若进入 h 则由 h 后完整终局相同而终局仍不变。因此每个祖先行动者的每个候选完成收益逐项相同，原 IC 保持。它检查全部候选行动而不只检查根实际路径。

本例两版本从 h 均实现 AB，将 hB、hT、hQ 三处 S 改为 R 就是整个二人尾子树替换。已有原根实际到达 h，且 h 前动作未改，故这两个派生根继续实际到达 h。只有相同尾利润、W、新增覆盖或尾玩家收益一般不足以保祖先效用；本包采用更强的同一完整终局 hAB。旧84项报告中的三处补丁位置和派生完整编码 SHA 原样保留，本轮不重新生成补丁。尾证书本身不能制造原来没有证明的根可达；一般 p 的合法尾可延伸为某份根 SPE 的子树，也不等于该 h 必然实际到达。

## 固定负载正核的证明与尚未支付的真实分支

Mbe 的固定查询 A、同一背景 b、给定加入主题 R₁,…,R_k（允许重复）之陈述准确。对某一客户，若它不在全部加入主题交集内，至少一次差分消去该项；在交集中，所有差分都给标量函数 f(t)=1/(t+1) 的连续向前差分。令

\[
g_k(t)=\frac{k!}{\prod_{\ell=1}^{k+1}(t+\ell)}.
\]

g_k(t)−g_k(t+1)=(k+1)!/∏_(ℓ=1)^(k+2)(t+ℓ)=g_(k+1)(t)。由 k=0 的 f 和该归纳式，完整得到

\[
(-1)^k\Delta_{R_1}\cdots\Delta_{R_k}U(A;b)
=k!\sum_{x\in A\cap R_1\cap\cdots\cap R_k}
\frac1{\prod_{\ell=1}^{k+1}(b_x+\ell)}\ge0.
\]

系数 k! 必须保留。两主题式通过共同覆盖项抵消，只剩 A\B 上的非负倒数差；R=A 的一阶式正是已定义的单步分母差税，沿同一负载链可消去中间分母得税的拼接恒等式。这些是固定加入负载格上的完整代数结论，不需 SPE 假设。

在同一完整 σ 的真实偏离中，令 b_i 是 actual 过去负载、r_i 是 actual 后缀、f_ij 是第 i 人改选 T_j 后 σ 的真实新历史后缀，则

\[
S_{ij}-V_{ij}=\sum_{x\in T_j}
\frac{f_{ij}(x)-r_i(x)}{(b_i(x)+1+r_i(x))(b_i(x)+1+f_{ij}(x))}.
\]

分子 f_ij−r_i 可正可负；同一 σ 在不同有序历史可用不同平局续局。局部正核未给 f_ij 与 r_i 的统一坐标序，也未把互斥偏离枝变成同一条加入链。把这些枝的正项分别写成非负核，仍不能把它们共同计入 actual 钱包；先取正部还会改变上式。

记 Q=(1/m)ΣS_ij、P_query=(1/m)ΣV_ij、D_adapt=Q−P_query。对固定最优比较索引元组，实读资源给出

\[
P_{\rm query}-(OPT-W)=E-D_{\rm adapt},\qquad E\ge W/m.
\]

UR 所需是存在某个最优元组使 D_adapt≤E。E 的下界不能推出该上界，actual IC 只给 V_ij≤u_i、从而 P_query≤W，方向仍不足。需要从同一 σ 的完整离轨 IC 取得共同预算证明，或给符合该精确根查询量词的反例。两个有限 GLOBAL 尾利润亏损不反驳 UR/RM，也不反驳局部正核。Δ_cov 与 D_adapt、尾利润 P 与根查询 P_query 各守原定义。

据此 Mbe 继续 isolated-after-review。本轮在给定六对象比较范围内没有新增可成立的一般跨枝付款或根可达逻辑边。固定税定义的一阶同式在正文中复用，不因共有定义制造模型 hub。一般共同付款和 half 义务保持数学 open，不写成 needs-decision。

## 十二份旧资产的准确处置

旧任务及旧 receipt、全部12份资产均已完整实读，并与旧 receipt SHA 独立匹配。下列路径统一以 `map/edges/customer-attraction-3a-3a-0bb4847cebdb22cd/` 为前缀；收据逐完整路径列出原 SHA 和处置。

| 旧文件 | 处置 | 实际用途或替代去向 |
|---|---|---|
| legal-family-to-finite-tail-contribution.json | retained | 唯一 canonical 贡献边，端点及证据当前，原字节保留 |
| finite-tail-interface-check.py | retained | 成熟84项精确尾 IC、选择性解码和三位补丁的可复现代码，本轮不运行 |
| finite-tail-interface-check.json | retained | 同输入成熟精确结果、补丁与派生编码 SHA，不冒作新计算 |
| mathematical-review.md | retained | 原完整比较、真实分母账与完整子树替换证明；原执行叙述是历史 |
| narrow-review.md | retained | 后续数量名修正、拼接前提的成熟细化及准确历史边界 |
| reading-ledger.json | retained | 原广泛实读与成熟计算实际范围的必要出处 |
| narrow-reading-ledger.json | retained | 后续窄审实际范围的必要出处，不冒作本轮阅读 |
| binding-snapshot.json | replaced | 本轮 current-input-check.json 绑定当前六 pin、字节与任务 |
| readonly-binding-preview.json | replaced | 本轮 current-input-check.json 保存独立只读原生 edge-check 与未变绑定 |
| source-refresh-check.json | replaced | 本轮 current-input-check.json 对全部当前17文件、唯一标题及精确版本差分重核 |
| manifest.json | replaced | 本轮 delivery-manifest.json 给准确保留/新文件清单与 SHA |
| record-only-correction-proposal.json | retired | 只退休已解决的 M993 v1 量名建议；准确纠错与证明留在两份 retained review 及本稿，现行 v2 已正确 |

worker 不删除或改写任何旧文件；以新收据 supersession 表达上述去向，父 Boss 按任务集成。旧七文件保留时均为成熟数学/必要出处，内含旧 request、旧 read pin 或原轮“待修正”等文字只描述历史。当前六输入、实际本轮阅读、未付义务与操作状态由本轮 review、ledger、核验记录和 receipt 给出。

## 本轮实际执行及正式比较处置

实际新读范围在 reading-ledger.json 逐文件记录。本轮完整读任务、旧任务/收据与全部12资产，六条当前登记记录、六份必要数学正文（模型、税定义、一般尾族、有限根核验主文、局部核资源、p1主文）、两个短根审计和 changed R-2fc 页；完整读父 Boss 的两份已发布短审，再逐项独立判断。其余 p1 附件只做当前字节/唯一标题检查和成熟合同复用，不宣称全文新读。两份动作流只做全字节身份与有限位置解码，不宣称全树语义新读。

新执行为原生 pin、17个当前登记文件 SHA/唯一标题、12个旧资产 SHA、两动作流编码与选定位置、p1 精确字节差分和一次只读原生 edge-check。尾 IC、根 IC、BI、LP、根/补丁生成、大型搜索均为0。父 Boss 在 wave9 短审的阅读和科学执行不计入本 worker 本轮实读或执行。

当前 definition.context_plan 没有 overlap_comparisons；comparison_groups 是两个单核心问题，不是 formal 待关闭对象对。closed_overlaps 与 follow_up_tasks 均为空，没有遗漏声明 follow-up，没有伪造承接任务 ID，也没有新依赖。一般 p≥4 实际根可达、一般 D_adapt≤E 共同付款、全目标 half 与最优规模等原开放义务继续保留。两核心身份、证据和版本均已辨清，故不使用 needs-decision。
