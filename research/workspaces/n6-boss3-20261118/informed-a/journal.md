# Boss3 idea 线研究日志

- 身份：Boss3 / idea / studio slot informed-a
- RUN：n6-boss3-20261118；session_tag：boss3-20261118-live1
- 工作树：co-work-anl-boss3；指定分支 rebuild/research-v2；初始 HEAD e0b8e7d28c5164fbd5fd0ef689886c1279e380b7
- 目标：customer-attraction/six-providers/exact-six-full-history-half-cover
- 任务：实读当前题面和相关图证据，提出可检验首选与实质不同备选，确定首个区分试验，并独立否决不成立初案。
- 开始状态：已读 AGENTS.md 与 prompts/research-line-design.md；尚未读取本 RUN spec/packet、Boss2 证据或 Main 初案。只修改本人 informed-a 文件，不 commit/push，不运行 studio line/save，不改 registry 或正式结果。

## 输入与断点

开始：2026-11-18（系统日期）。下一动作：对比 Boss3/Boss2 的精确题面与量词，然后读取两条指定超边及其承重正文。

## 首轮实读与路线（2026-11-18）

两份 spec 的题目与定义文件 SHA 完全相同。Boss3 仅 pin 精确定义、输入终局量、策略真实续局及全部历史量词；Boss2 不 pin section。实读题目全文与共同目录模型全文，确认同一六人原题，未把零客户、空覆盖、重复标签/行动或离轨弱平局删去。

已读指定两条正式超边及全部承重数学正文：
- `boss2-partial-fractional-cover-to-six-half`；正文《六人分数部分覆盖与有效覆盖量》全文；其 certificate/verify/replay 全文。尚未重放；尚未实读其所用《五条真实偏离的六人分数覆盖四十九比十》全文，因此目前只按已发表条件边作路线定位，不声称已从底层独立重证。
- `boss2-four-extras-to-six-half`；正文《六不交最大锚与四种额外覆盖》全文，特别是两类末端前缀及所有有序历史归纳。
- Boss2 Main journal 全文，知道 t=5 旧松弛失败、对称/六种非对称原模型补全都没有生成坏 SPE，不把必要松弛当反例。
- 未审笔记 `third-from-last-anchor-deficit.md`、`strict-anchor-floor.md`、`disjoint-comparison-exposure.md`、`penultimate-deficit-recombination.md` 全文。它们保留待非作者核验身份，不能直接当正式前提。

### 选路回执

首选：在六不交最大锚子类，将 q≤4 种数条件替换为共同前缀、同一目录的跨锚攻击暴露预算。第一个可检验子义务是 q=5：枚举合法 `(s,当前位置,M,d)`，按真实末二/倒三与重复攻击严格排除逐类核账。Main 已交 execution 做 q5；本人继续一般预算。

备选：在连续客户目标权证书中把最优六槽的真实后继一起耦合，而非每个槽独立松弛。第一试验针对旧 t=5 必要松弛的坏型，查能否满足同一个合法目录、同一真实跨枝回复表；不重跑旧已认证计算。

首轮用词修正：我向 Main 的短回执曾说 q5 的“唯一潜在坏前缀”。实读后尚未证明唯一；准确为原粗预算至少有两类缺口：无重复 s=4，以及有重复 s=5 且 M-d>0。已告 execution，必须结合槽数分类，不能预设唯一。

### 下一动作

推导按前缀重数和各锚损失的顶槽暴露预算，标出其充分性与计算证书；向执行线发送短引用与可区分试验。尚未接触 Main 初案具体数学稿，故未作认可/否决。

## 稳定旧对象映射：单支持锐6/11

Main 转来 independent 自足重证：实际六个标签覆盖同一A时6OPT6≤11W，66客户7标签匹配。本人未向 independent 回送任何外部内容；给 Main 的图核如下：

- 稳定旧ID `customer-attraction/repeated-first-theme-terminal-strict-two-bound`，正文 `archives/customer-attraction/state/定理/重复首主题终局的严格二倍界--定理.md` §对m个最优主题的两份共同预算，式(P)/(L)。同覆盖取A=B、a=b=0,c=W，直接得OPT_m≤(2−1/m)W，m6正是6/11；正文明确保同覆盖标签和完整原历史。
- 匹配族已有ID `customer-attraction/actual-uncovered-private-spectrum-sharp`，正文《实际遗漏私有席位谱与锐界》§每个人数的完整SPE匹配构造：|A|=m，加m−1不交singleton，所有历史恒选A，W=m、OPT=2m−1。独立新66客户7标签分配可作为恢复核验的另一见证，但数学常数和结论不新。
- Main 决定按自主重证/恢复核验保存，不另造同义节点；未对全球文献新颖性作查询。

## (E)接口及实验勘误

已封存 `prefix-exposure-r1.md` 与 manifest；判断为正式q4复制/重复排除机制的精确可检验接口，不主张新全域机制，建议保笔记。直接(E)与q4不互含，混合尾部条件才包住原q4分类。q6免疫半锚例不被q4/三条分数覆盖边支付；未验证给定σ的H，因此未宣称与Boss2 path-harmonic边严格分离。

审查发现r1 §5及旧exposure_probe.py的K5循环起点0对应B0=T0，实际q4。旧文件冻结未改。本人明确指出统一平移1仍碰锚；另造真q5起点{1,4,8,12,16}，脚本assert额外覆盖互异、均非六锚，精确重放得到E=(8/3,17/6,8/3,8/3)，固定前缀当前保5、W最小29（OPT30）。新文件 `prefix-exposure-r2-erratum.md`、`exposure_probe_q5_r2.py`、`exposure-probe-q5-r2.json`。已告Main与执行线。错误仅在旧实验q标签，不改变(E)推导或正式q4正文。

## 最小真实BR回灌试验

已实读执行线 `probe_bc_tail_lp.py` / `probe-bc-tail-lp-output.json` 和 `q5-prefix-reduction.md`。把B/C必要松弛的other原子质量均匀分到另外s−1个新锚，保E,A,Y为三种额外覆盖，加六锚，清分母为单位客户原菜单。脚本 `tail_completion_probe.py`，精确输出 `tail-completion-probe.json`。

B输入K=132，总792客户；C输入K=1140，总6840客户。原候选Y仍为A后的真实末位最佳回复，最小失败出在倒二IC：
- B：A收益3/4，改任一其它新锚Tk后所有末位最佳回复为另一个新锚，收益7/8，严格获利1/8。
- C：A收益11/15，改其它新锚Tk后所有末位最佳回复为另一个新锚，收益13/15，严格获利2/15。

可复用的最小跨子枝约束：固定h、强制Tj后倒二实际Aj收益u5_j；对每个Tk，令L_jk为同一σ在再强制Tk后的真末位回复，则u5_j≥Σ_{x∈Tk}[p_x+1_Tj(x)+1_Tk(x)+1_Ljk(x)]^{-1}，且L_jk须在同一合法菜单比较全部原标签。不能用独立自由回复替代。

该试验只排均分other的q3补全，不排其它非对称/含4或5额外覆盖的补全。原候选坏叶的福利比已分别107/132和373/570，均>1/2，所以即使局部低于K/2也不能当原根half反例。已向执行线发送完整短回执；共享菜单A_k/Y_k耦合试验仍由执行线负责。

### 下一精确断点

等待执行线共享4未出现extra/5强制锚模式试验。优先看真倒二强制Tk后的末位回复在固定菜单中是否可实现，而非只收紧自由P均值界。若真实B/C存在当前低于K/2，转同一实际叶的总福利预算；保W/OPT完整判据。未重跑Boss2 t5旧已认证计算。没有修改其他线文件、registry或正式档案，未Git提交。

## 第三次checkpoint前的正式旧源核与路线否决

### 已知更强尾部：q5局部tail不得重复授予

实读正式《末两人逐人保底与全人数弱福利界》全文，当前稳定ID `customer-attraction/last-two-individual-floor-and-all-n-welfare`（legacy `CA-LAST-TWO-FLOOR`），SHA `204030503c37b18f8d26ce664b9cb99afc688fed77c8221a00cf0d8d7b21b34b`。又实读《末位最坏背景值与目录计数界》全文，ID `customer-attraction/last-slot-value-and-catalog-counting`，SHA `6263b3d935b1c2d3d7ae6aee4016ae78cb369de1f28ddb284e8202fd21b69c3d`。

前者§1/2对任意合法四人有序前缀，末两位各≥θ(P)≥θ6(0)；后者§2前缀嵌入、§3式(3)第二界θ6≥[2OPT6−5K]/12。六不交最大锚给OPT6=6K，于是**倒二和末位各≥7K/12，不需q限制**。因此本轮q≤5倒二/末位K/2应作为旧定理更弱实例化保存，不新增正式对象。Main与执行线已对齐此判断。

相应真实图边已实读：
- `cag-7046-last-two-floor-pays-terminal-pair`：CA-LAST-TWO-FLOOR接全位置pair候选的末两位置，仅给2v_m；不买早期pair。
- `ca-b9bd-last-two-floor-pays-security-chain-end`：ALL{CA-LAST-TWO-FLOOR, last-slot-value-and-catalog-counting}接安全链末端；不买前段预算。
- `ca-r33-last-two-and-counting-pay-early-floor`：另结合三人锐界接早位容量对象；本轮没有用其中三人根分支。

本轮7K/12实际直接使用两份成熟正文的明确式，未经pair或安全链开放前段。关于是否需新连接边由Main决定，使用旧正文不等于新节点增量。

### 重复动作剔除的准确范围

K>0时7K/12>K/2，末两位任何规定动作若与过去任一标签同覆盖，则终局每客至少两人，当前收益≤|B|/2≤K/2，矛盾。同覆盖异标签同样排除；空覆盖收益0亦排除。末位还不能复制倒二。K=0全零独立处理，不宣称严格排除。只删**真实规定后继的可能类型**，原合法偏离菜单保持全部标签。

### B/C新缩减稿与其数学义务

已完整落盘 `tail-menu-reduction-r1.md`。核心是任一B/C原三人前缀，记新锚折扣P_j、总P，强制T_j后的真实两尾为A,Y：

- 若A为extra、Y为其它新锚，真倒二比较其余s−1锚给u5≥K−2(P−Pj)/(s−1)，同叶A∩Tj收益缺额给w_j≥K−Pj−2(P−Pj)/(s−1)。
- 若A为其它新锚、Y为extra，真末位查询剩余s−2锚及Y的分享缺额给w_j≥K−Pj−(P−Pj)/(s−2)。
- B:s4、P≤K/2，两式对每个j均≥K/2。因此若B当前规定收益严格低于K/2，其四条强制新锚分枝的两尾都必须是至多四种未出现extra中的两个不同覆盖。这不依赖前段逐人归纳。
- C:s5、P≤2K/3，至少四个锚有Pj≤K/3，同样迫使这至少四枝两尾为不同未出现extra；若P≤K/2则全部五枝。重锚一枝不能凭空删去。

execution正在实读该准确稿，才据B模式枚举。它仍是逐人K/2加强目标的缩减，尚未证明B/C可付。

### 旧共享模式数值探针的受限域与不可升级

执行线告知：其旧100个pair-multiset必要LP，B浮点最低.5、C约.529506，追加末两位7/12值不变。但旧outside只给t·E背景，漏掉旧锚客户上的+1，因此只覆盖额外主题不碰旧锚的受限目录，不是一般必要松弛；不可据这组数值宣称B/C一般成立。本人未运行该100模式计算，数字来自执行回执。执行正在补全六锚block和freshoutside，保旧锚+1，再试B全部1365种multiset；只有精确有理证书且核全域后才可承重。

### 已否决与当前精确下一步

1. 否决只靠纯暴露(E)细化即可处理q5：真q5循环区间r2已有所有E_j>K/2但真实子局当前收益5的精确分界。旧r1实际q4已另存勘误；不改旧字节，不让实验标注错误污染(E)解析推导或已发表q4定理。
2. 否决把独立tail原子点当原模型反例：均分other的同一合法q3菜单中，原Y真BR但第五位A违反真实强制锚后续IC；B有1/8获利、C有2/15获利，且候选坏叶W/OPT本就>1/2。
3. 否决将q5末两位K/2重复授为新局部定理：现有一般尾部7/12更强。
4. 实际叶若有至少三个不同锚，已直接W≥3K=OPT6/2。因此原题真坏根只能actual至多两锚。若共享菜单发现真实B/C当前< K/2，下一方向应转**同一实际叶总福利**，不能把更强局部floor失败当半覆盖反例。

下一动作精确为：execution核 `tail-menu-reduction-r1.md` §5 B四枝均为双extra，然后在六锚全部block+外部客户+真实旧背景的共同五extra菜单上处理B的1365模式；先查必要LP，若候选负点则按同一合法菜单与真末位/倒二IC回灌，若全域数值非负则提炼逐模式有理对偶。本人可继续审查模式共享客户域、覆盖大小约束、原历史量词及同叶福利转路。

未读项：Boss2 t5旧更多枝数值脚本未深入重读/未重跑；执行新的100/1365模式脚本尚未实读（等准确版本）；独立线完整新66客户证明未用作本线前提。未访问任何网络文献或凭据，未修改其他线文件，未commit/push。
