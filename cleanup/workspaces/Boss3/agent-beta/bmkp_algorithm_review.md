# 两容量 BMKP 候选算法的独立反方审查

状态：**有希望的候选，非已证定理**。2026-10-20；已读 generalized_assignment/TWO_CAPACITY_LEMMA.md 的当前落盘稿。审查对象是“per-capacity profiles→joint types→global heaviest critical→nested matching→cheap LP”路线。旧版利润预算、cap、discard、OPT网格异议已修，不作为当前fatal。文末给出独立替代cheap舍入引理，避免未经核查导入母文Lemma22的全覆盖字面合同。

母文：[Chen 等 ICALP2026 完整稿](https://arxiv.org/html/2605.05233v1)，§4 Lemma8/Definition11,15/Observation17/Lemma21,22，§7明确constant capacity types问题。本次web refs：turn106view0、turn143view0/1/2、turn144view0/1。本文的新论证均为内部草稿，不能当母文的既有结论。

## 已独立重建的条件模块

### 1. profile 给出的 slack 足以同时支持两容量 label 的上舍入

固定一种容量 `B`，将母文的容量1定义按B缩放；`η` 是工作精度。

- heavy 阈值是 `(1−η²)B`。long bin 若含 heavy `h`，profile representative 的 weight `u≥w(h)` 满足 `w(rest)≤(1−η)(B−u)`。
- 任意其中的 light-expensive item `e` 满足 `w(e)≤B−u`。Definition15 选择能容纳 e 的最重 profile representative，故它对应的 residual 不大于 `B−u`；每项 label 上舍入增重至多 `η²(B−u)`。
- long bin expensive 数至多 `1/η` 时，总增重至多 `η(B−u)`。把heavy换成label u后，刚好仍不超B。
- 无heavy的long bin有 `η³B` slack。任意heavy representative的residual至多 `η²B`，无eligible representative时使用default。每项light-expensive增重至多 `η⁴B`，合计不超过 `η³B`。

因此，**只要 per-capacity Lemma8 的 profile/slack 见证已合法取得，且昂贵项数界已明确保证**，直接定义两套 labels 并取联合类型可以保初始 rounded feasibility。无需先以不明方式把两容量分别作最重critical选择。

### 2. 全局 heaviest canonicalization 可以避免 item supply 冲突

固定联合类型 `τ=(u_1,u_2,g,heavy/light statuses,expensive flag)`。定义critical为所有long bins中全部expensive items的并集。若同类型critical e比noncritical f轻，交换二者：f原来只能在short bin或unused；long的自身容量label不变，short实际重量下降；fine profit bucket宽δ时每槽实际profit损失小于δ。重复可得每τ最重的指定数量items为critical。这个交换不会改变各bin的cardinality或各容量模式的label总量。

必要条件：cheap/expensive为**全局**标记；long中不能有“非critical expensive”。不能把两个容量各自的最重集分别拿来拼。

### 3. 两容量 short matching 的嵌套约束本身可解

完成short bins只使用未占用expensive items，singleton用独立dummy vertex表示。达到共同profit threshold的small-eligible edges是large-eligible edges的子集。找总边数 `s_1+s_2`、其中至少s1条small-eligible边，等价于固定cardinality的最大权matching，权重为small eligibility。再取s1条small边给小bins，其余给大bins。无须解决一般带精确颜色计数的Exact Matching。

须枚举每容量的short数量，或给出等价的empty-critical-bin计数方式。全cheap long bins也会有空critical config，不能误把所有空config直接当short。

### 4. matching 与 cheap LP 的共享见证，在正确分池后可保留

若 short matching **只取 noncritical expensive**，cheap LP **只取 `p<η`**，则两个池不交。保留canonical结构见证中每个long bin的cheap items，选任意满足相应small/large数量的short matching并不会夺走这些cheap。short新profit直接达标；unused expensive可以丢弃。故这个版本的相容性攻击没有产生反例。

## 发现并通知作者的必须修正点

### A. 利润未cap时“常数种joint types”是假

对候选目标T需先normalize并令 `p_e←min(p_e/T,1)`。这保留“OPT≥T”带来的目标1可行性：某bundle若含原profit至少T的item，cap后至少1；否则不变。若不cap，`floor(p/η²)`种数可能随输入数值增长，不能声称只依赖η。

### B. cheap LP 不能强迫所有剩余物品进入真实bins

BMKP允许unused，total weight可远大于总capacity。LP应写 `Σ_j x_ej≤1`，或添加discard dummy bin（容量Σw、目标profit0），再用母Lemma22的 `Σ=1` 版本。真正的cheap池要定义成 `{e:p_e<η}`；不能把所有不在critical/matching里的items都叫cheap，因为其中还可能有unused expensive。

### C. 母Lemma8的高profit假设与新singleton预算：已修

母文在应用Lemma8前要求 `p_e<2/3−6η`。若仅把 `p≥2/3−4η` 缩成singleton，残余仍可能违反该假设。可修方案：在未知OPT结构上先将含 `p≥a:=2/3−6η` 的bins缩为singleton并保留为short；其他bins再应用母结构引理。这样新short单例最初只保证profit a，canonical后可能只剩 `a−δ`，**不能仍声明short threshold为 `2/3−4η`**。

当前稿已经在 `q_pre=2/3−6ζ` 处缩high-singletons，并令 `Q=q_pre−3ζ`。所有short的保守profit下界为`q_pre−2δ`，若两件都低于Q，则各自至少`3ζ−2ζ²>ζ`。这修复了旧异议；不能继续声称最新算法漏了母Lemma8的profit假设。

### D. 工作精度、昂贵项数和未知OPT的有限枚举

须固定 `1/η` 为整数，明确long bins最多 `1/η` expensive items的预处理是否被结构变换保持。必要时可以从已round-feasible见证中删项，使任何保留long至多该数；但必须证明删除heavy或转成short时不破坏后续类型/利润保证。

不能把指数多项式中的指数随input增长：profile数、joint-type数、configuration数都只能依赖ε和固定capacity-type数。OPT可用几何网格覆盖正profit范围，网格长度对输入位长多项式；若用二分则必须说明decision procedure成功谓词的单调性，而不是仅凭存在性保证随口二分。

## 新增：独立的 discard 版 cheap 舍入（4pmax）

母Lemma22显示合同要求每件最终恰分一次。该字面合同不能导入：一个weight2的item、两个capacity1的bins、每边fraction1/2时，fractional可行却没有任何完整整数分配。该反例只排除字面的全覆盖子合同，**不是对母论文主定理作否定**。本候选允许discard，可完全独立使用下面引理。

**引理。** 给共同物品weights/profits `w_e,p_e≥0`，每bin容量`B_j≥0`及profit下界`t_j`。若LP

`Σ_e w_e x_ej≤B_j, Σ_e p_e x_ej≥t_j, Σ_j x_ej≤1, x≥0`

可行，则可多项式时间求互不交、允许unused的整数sets `T_j`，容量严格守住且 `p(T_j)≥t_j−4pmax`。

**完整证明。** 对剩余LP取BFS，把所有`x_ej=1`的items固定到相应bin并扣除其weight/profit，移除这些item；已固定物品不再分配。只看剩余正fractional变量，记数E，当前bin数M。若某item的列和约束紧，则该item至少有两个正fractional变量（单个真分数不能和为1），故紧列数`N_tight≤E/2`。极点的正fractional变量数不超过活跃非零约束行数，因此`E≤N_tight+2M≤E/2+2M`，从而`E≤4M`。存在真实bin至多接四个fractional正变量。

结束这个bin：不接受其fractional份额，输出已经固定给它的整件。其weight不大于该轮fractional weight上界；profit与该轮目标相比只损至多四件的分数利润，故全程损失≤`4pmax`。移除此bin但**保留其fractional items**；其他bins原fractional分配不变可行，列和只会下降。重复至所有bin结束。所有输出整件在首次固定后即被移除，不会重用；最多M次BFS，rational LP位复杂度多项式。没有调用母Lemma22。

等价地可以加无约束discard node使每item等式和为1；此时E≤N_fractional+2M且每fractionalitem至少两条正边，同样得到E≤4M。本文与GA子线分别重建了这一引理，boss4也独立核了计数。

**当前预算修复。** 将原`2ζ` cheap损失改成`4ζ`，每包下界为`Q−4ζ=2/3−13ζ`；几何网格`1+ζ`后至少`2/3−14ζ`。选`ζ≤ε/16`足够，不能继续沿用`ζ≤ε/12`。

## 尚未闭合或需最终写全的审稿义务

1. 把“未知OPT按容量分组、产生short、对其余groups用Lemma8”写成严格结构引理，逐个保留母文所有假设，特别是高profit和cardinality。
2. 给出所有labels的实际B缩放定义，证明含`∞`标记的types仍有限，unusable items不误进入small slot。
3. 写出counts/configuration枚举的完整domain，说明至少一轮命中全部结构见证，并将具体items分配给同type slots时的profit损失计入。
4. 将short singleton/pair阈值、long loss、独立cheap rounding `4ζ`、OPT网格loss合并成一个明确ε界，更新ζ定义。
5. 写可执行小规模算法，枚举整数4–8项和两capacity，审计的不只是OPT而是每个中间lemma。当前玩具文件没有验证这个BMKP算法。

6. 显式写long expensive数≤K的规范化。母Lemma8的重物品移位中会把多个light集合合并；如合并后昂贵数>K，取任意K件昂贵项可保profit≥1并减轻weight，但要说明此删除不破坏profile与short分类；不能只引用原输入的昂贵数界。

当前结论：修复后的路线暂无我找到的fatal；有独立BFS舍入和profile rounding重建支撑。还需整稿、边界与算法级验证，不升级为已解公开问题；新颖性也未认证。

## 最新版本对齐（最终冻结，2026-10-20）

已重新完整读取当前 `generalized_assignment/TWO_CAPACITY_LEMMA.md`。当前参数是 `ζ=1/ceil(max{100,20/ε})`、`U=1−ζ`、`γ=Uζ`、`δ=Uζ²`、`K=1/ζ`，`q_pre=2/3−8ζ`、`Q=2/3−11ζ`；独立discard舍入损失至多`4pmax<4ζ`，gap-oracle输出至少`2/3−15ζ`，几何网格后至少`2/3−16ζ`。上文旧`q_pre=2/3−6ζ`、`ζ≤ε/16`及`2/3−13ζ`等数值保留为探索历史，**不是当前稿的参数或当前异议**。最新稿已显式记账heavy-cheap删除并用U重归一化，已补全结构重组后K规范化；profit cap、unused/discard、单向gap-oracle、几何网格、short利润来源、cheap/expensive分池也已修复。本文不再把这些旧缺口或母Lemma22的字面全覆盖合同列为当前阻断，当前算法已自立GA-03-L3而不依赖该导入。

最终判断仍为**候选算法，未认证总定理**：我已独立重建全局critical交换、nested matching、profile上舍入与4pmax BFS舍入模块，并读到上述修复；没有在这次最终版本对齐中重新逐行验证整份新稿或新增计算。真正尚缺的是母Lemma8输入提取/归一化/short与profile符号的精确逐行核查、整稿联合覆盖与边界的完整证明审阅，以及算法实现和中间不变量的回归；新颖性/发表价值也尚未认证。按boss4要求本次冻结，不再新增问题或计算。
