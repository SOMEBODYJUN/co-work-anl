# 独立完整表述审查（editorial）

## 运行身份、材料与边界

- 模式：`editorial`；完成全文恢复，再完成必要性与指称精度两项审查。
- 冻结阅读稿：`review_snapshots/exposition/multiple/main.tex`，227 行；完整读过正文、公式、所有证明及书目调用。
- 正文 SHA-256：`c8bfa0d94aaf22a732338fba5b1cc9216ba878329c62ddca04f485858240172a`。阅读前执行 `sha256sum /workspace/scratch/3b7c4918eb2c/review_snapshots/exposition/multiple/main.tex`，与指定值一致。
- 同读书目：`review_snapshots/exposition/multiple/references.bib`；SHA-256 为 `76c5adc0fe3480de812dc8f71b0784ceef73fe0707385066ba389fd343c8238d`。未打开任何引用来源，未判断书目或历史断言的准确性。
- 仅加载指定的 `read-research-paper/SKILL.md`、共享 `exposition-standard.md` 与 `skeptical-editor-review.md`。没有接触写作者对话、项目状态、原证明、来源全文、先前审查、修补建议或历史版本。没有编辑论文；本报告是唯一写入的文件。
- 契约：面向熟悉 Nash 均衡与 lexicographic order、但未读本证明的算法博弈论和组合优化研究者；承诺共同地点目录下任意设施数的 2-approximate SPE 存在性；约八页的完整、自足证明。受保护内容：无；不审范围：无另行限定。数学真值、来源准确性、优先权及首次阅读体验不在本角色的认证范围内。
- 有效性：输入身份已核验，隔离及只读条件满足。完成状态：完整两遍审查，强制清单与裁决覆盖已完成。

以下定位均指冻结 `main.tex` 的行号。由定理计数器可恢复的编号为：Definition 1.1；Construction 2.1；Lemmas 2.2–2.6；Theorem 2.7；Proposition 2.8。无需依赖编译产物恢复这些编号。本次没有编译，因此“约八页”仅作为篇幅与细节契约，而非已测量的页数结论。

## 从全文恢复的论文契约

论文研究有限客户端、正实权重、有限共同地点集及任意 `k >= 2` 个有标签设施的两阶段博弈。设施收益是期望负载；客户端每次使用一个可达设施，独立混合，成本含自己的全部权重。近似仅用于设施的移动收益；每个 placement 的客户端续局均须为精确 Nash 均衡。

主要承诺是 Theorem 2.7：存在因子二的 SPE，选定路径上的客户端各自选一个覆盖自己的占用地点，再在该地点设施间均匀独立随机化；其他 placement 可取纯均衡。次要承诺是 Proposition 2.8：有理显式输入下，可输出多项式位长的指定路径与单方偏离均衡，再以确定默认规则描述其余续局；这不是多项式时间搜索的承诺。

结果与依赖层次如下：Construction 2.1 选有限族中的字典序极大负载向量；Lemma 2.2 证明选定混合策略的客户端均衡性与正负载下界；Lemma 2.3 给出移动后的重量预算；Lemma 2.4 把预算转成含允许单独重客户端的分配；Lemma 2.5 以严格改进过程保持负载界并达到纯均衡；Lemma 2.6 逐一实现设施偏离的因子二界；Theorem 2.7 把这些互不冲突的续局补成完整 SPE；Proposition 2.8 说明有限构造与编码。

该结构符合目标读者与细节预算。初等的配对求和及势函数变化都展示了关键运算，没有把概念论证推给引用。Abstract 共 132 个以空白分隔的单词，在默认 150 词内，且独立说明问题、结果和方法。没有发现需要为缩短篇幅而删除的整段。

## 逐节审查

| 单元 | 开篇与局部衔接 | 独立单元的必要性、指称及冗余结论 |
|---|---|---|
| Abstract，19–21 | 由两阶段模型进入旧界与新界，再给客户端续局形状和证明机制。 | 作用完整；方法细节仍在摘要预算内。无需删去方法或来源定位来追求更短。 |
| §1 Introduction，24–29 | 首段解释为何必须对所有 placement 选续局；随后说明相关界与本稿限制，再给证明思路。 | 背景、改进与方法有不同工作，保留；没有以宽泛引用代替本稿所需的技术结论。 |
| §1.1 The model and the result，31–65 | 普通 prose 先说明将定义的对象，再给模型。 | 模型和精确定义为读者使用主结果所必需；成本、未服务客户端、标签和混合策略的约定齐备。结尾分立的 **Organization**、**Conventions and notation** 顺序符合标准。 |
| §2 A factor-two equilibrium，67–68 | 由完整续局需求转入重量预算、分配和改进过程。 | 作为主证明总节有清楚角色。此处重述依赖用于进入正文，未构成无工作的重复。 |
| §2.1 Lexicographic selection and transfer bounds，70–134 | 先说明均匀随机化如何保持原子性与相同地点负载相等，再进入有限选择。 | 将选定路径均衡与偏离重量界放在一起合乎共同依赖。83 行的比较与 134 行的解释各解决后面实际需要的理解问题；无需删除。无独立客观缺陷。 |
| §2.2 Packing clients and equilibrating after a move，136–198 | 从 Lemma 2.3 的预算转入原子分配，再明确初始分配尚非均衡。 | 分配、负载界不变性与两个偏离分支构成不同阶段，独立成节合理。193 行的分配对象没有唯一直接指称（SE-1）；170 行以描述性别名代替已有编号（SE-3）。其余 Case 1/2 的局部回顾是核对各自假设所需。 |
| §2.3 Completion of the continuation，200–223 | 开篇指出要把偏离续局同时选定，解释有标签 placement 的作用。 | 从逐偏离结论到完整 SPE 的衔接必要；有限编码后果放在此处也有自然位置，不必再分节。220 行确定默认规则的客户端顺序未给定（SE-2）。来源界与效率边界的结尾有明确用途。 |
| Bibliography，225–226 及所读 `.bib` | 单个正式书目条目对应正文唯一来源。 | 正文已说明引用的结果内容与 Theorem/Observation/Section 定位。本审查不核验来源内容；未发现表述层面的书目指称缺陷。 |

## 强制清单

清单中的 `keep` 是该项在本次两项审查下的裁决，不是数学或来源认证。重复出现而对象相同的短语合并为一项，并列出出现位置。`replace` 项全部对应下方 SE finding；没有未进入 finding 的可操作缺陷。

### A. 显式说明性 remarks

正文没有编号或以 “Remark” 标示的正式 remark。下列是以独立解释句、解释段承担 remark 工作的全部候选；把正文中直接执行证明的句子另列于精度清单，而不重复归为 remark。

| ID | 定位、开头 | 裁决与读者收益 |
|---|---|---|
| RM-1 | 43，“In particular, the whole weight…” | `keep`：防止将原子客户端的条件成本误认作自身期望贡献 `w_i p_if`。 |
| RM-2 | 54，“The client equilibrium requirement is exact…” | `keep`：明确近似因子只放宽设施条件，保护对 Definition 1.1 的正确理解。 |
| RM-3 | 83，“The maximum exists…”及随后的 elementary comparison | `keep`：给 Construction 2.1 的存在性和数次字典序反证提供直接可用的比较内容。 |
| RM-4 | 106，“These are precisely the clients newly covered…” | `keep`：把 (3) 中的集合差与移动后首次覆盖的客户端相连；指称是紧邻显示式中 `w` 的输入集合。 |
| RM-5 | 134，“The terms involving J account…” | `keep`：解释 Lemma 2.3 中额外交集项为何足以允许随后任意重分配，区别于单纯重复公式。 |
| RM-6 | 151，“The assignment obtained by packing need not…” | `keep`：说明为何在 packing 后还必须增加 Lemma 2.5，并给出接下来 loads 的纯策略语境。 |
| RM-7 | 210，“The on-path construction gives equal…” | `keep`：说明选定路径的同址对称性不约束偏离续局，防止将均匀构造外推给整个 continuation。 |
| RM-8 | 223，“Proposition … distinguishes a short description…” | `keep`：将位长结论与运行时间结论区分，且准确留下界与高效构造两项后续问题。 |

### B. 否定或防御性范围限定

| ID | 定位、限定 | 裁决与读者收益 |
|---|---|---|
| NQ-1 | 57，“a polynomial-time algorithm … remains open” | `keep`：有限精确构造容易被误读成高效算法，此处在首次宣布构造时排除这一误读。 |
| NQ-2 | 59，“the result concerns a restriction…” | `keep`：交代共同地点假设相对相关工作的模型范围，并说明它在证明中的具体用途。 |
| NQ-3 | 59，“still leaves a gap…” | `keep`：定位新上界的意义和未解决的最优因子，不是替作者范围辩护。 |
| NQ-4 | 151，“need not be a client equilibrium” | `keep`：这是进入改进过程的必要逻辑桥，不能因有 Lemma 2.5 而删除。 |
| NQ-5 | 210，“need not preserve symmetry…” | `keep`：对应 RM-7，对由主构造引出的实际可能误解作边界说明。 |
| NQ-6 | 223，“neither step has a polynomial running-time bound in this proof” | `keep`：在详细编码证明之后给出准确的证据边界，受益对象是希望从 Proposition 2.8 得到算法保证的读者。 |
| NQ-7 | 223，“remain separate questions” | `keep`：分开最优保证因子和寻找高效构造两项不同问题，避免暗示其中一项已由编码结论解决。 |

模型中的 `p_if=0`、未服务情形、`r != s_f` 以及 lemmas 的分支条件是数学定义或假设，不是防御性范围话语。未发现没有具体受益读者的 defensive qualification。

### C. 反复使用的非正式别名与短称

| ID | 词语与定位 | 精确对象及裁决 |
|---|---|---|
| IA-1 | “on path / off path / other continuations”，20、57、204、207、210、215、220 | `keep`：所选 placement `s` 及所有其余 labeled placements；是读者已知的博弈论用语，并由模型直接落实。 |
| IA-2 | “site assignments / assigned location”，74–83、99、121、182–193、218 | `keep`：Construction 2.1 的函数 `t(i)` 及其随后明确变更；没有引入另一种客户端策略概念。 |
| IA-3 | “newly covered [clients]”，102–106、121、131、188、195 | `keep`：`C_r` 减去原占用地点覆盖集之并；(3) 明示集合，195 的 “genuinely” 区别这些客户端与 `J` 中重新安置的客户端。 |
| IA-4 | “old / surviving occupied location”，102、134、182–195 | `keep`：偏离前的 `O` 及偏离后仍有设施的成员；Case 1/2 给出 `q_u >= 2` 与 `q_u=1` 的确切判别，节省重复集合表述。 |
| IA-5 | “stationary facility”，29、137、179、182–195、210 | `keep`：移动设施 `f` 以外的设施；179 行显式说明，之前普通用语也由单设施移动语境确定，不需增加术语系统。 |
| IA-6 | “heavy / isolated [heavy] client”，29、137、151、154–161、188、195、210 | `keep`：证明中指重量大于 `2a`、独占某一设施的客户端；精确阈值和位置条件紧邻正式 statement 给出。 |
| IA-7 | “cap / required load bound”，29、137、151、170 | `keep`：设施负载至多 `2a`；这一短称帮助区分单独重客户端设施与须受界约束的其他设施。仅 170 行将其变成 lemma 指称的问题另见 IA-8、SE-3。 |
| IA-8 | “packing and cap lemmas”，170 | `replace`：应直接指 Lemmas 2.4 and 2.5；现有描述要求读者把未正式命名的 “cap lemma” 映射回已有编号（SE-3）。 |
| IA-9 | “actual deviation”，207、215、218、220 | `keep`：`s[f <- r]` 且 `r != s_f`；Lemma 2.6 已明示条件，计数 `k(|S|-1)` 及 207 行不同坐标的说明保持一致。 |
| IA-10 | “displayed [strategies/profiles]”，215、220 | `keep`：命题所列路径上与实际偏离的显式 profiles，区别于默认规则；220 行直接把两类 profiles 点明，没有要求读者恢复另一份证据。 |

### D. 呈现为 theorem、criterion、principle、method 或 argument 的名称

没有发现未说明内容的外来命名原则、虚构的传统 theorem 名称或把普通计算包装成专名的用法。以下覆盖承载方法／结果标签工作的短语。

| ID | 定位、名称形状 | 裁决与说明 |
|---|---|---|
| NM-1 | 27，“their Theorem 5 / Observation 4 / Section 6” | `keep`：正式来源 locator 与各自的数学内容及研究问题同句给出，未让名字代替内容。 |
| NM-2 | 20、29、62、68、70、80、89 等，“lexicographic maximum / selection / maximality” | `keep`：惯常的次序与优化表述；Construction 2.1 定义有限候选族和目标，并非借助一个未陈述的命名定理。 |
| NM-3 | 83，“the following elementary comparison” | `keep`：比较规则立即完整陈述；没有先要求读者识别一个外部 principle。 |
| NM-4 | 20、68、139–149，“atomic packing argument / lemma” | `keep`：摘要和节开篇是方法预告，正式内容与证明在 Lemma 2.4；不是未经定义的既有 theorem 名。 |
| NM-5 | 170，“packing and cap lemmas” | `replace`：已有正式编号时不应以临时结果别名代替；与 IA-8 同一缺陷，见 SE-3。 |
| NM-6 | 163–167、207、220，“potential / strict improving client moves” | `keep`：势函数、变化式和有限性论证均在本稿给出，后续调用的是编号 (8)，没有隐含导入外部 convergence theorem。 |
| NM-7 | 62、212–223，“finite certificate / encoding consequence” | `keep`：普通结果说明由 Proposition 2.8 的输出、位长和检查界精确落实，没有擅造标准 certificate theorem 名。 |

### E. 指称精度候选：结果指针、精确谓词、短条件／集合与引用应用

此清单记录第二遍中所有需检验的相关用法。直接给出的每个等式不另立候选；它们已在全文读取并作为下表指称的锚点。

| ID | 定位、候选 | 裁决与精确接口 |
|---|---|---|
| RP-1 | 20、27、59，旧界与相关模型的引用 | `keep`：新旧结果状态分明；27 行给 Theorem 5、Observation 4、Section 6 的定位和内容，59 行明确模型限制。没有技术应用依赖未知来源内容。 |
| RP-2 | 25、29，“choice of client equilibrium at every placement / controlled client weight / complete continuation” | `keep`：引言以普通语言交代目标和证明阶段；45–54 行随即给 continuation 与设施条件，未先使用必须猜测的纸内技术定义。 |
| RP-3 | 32–43，可达、未服务、独立混合与 Nash 条件 | `keep`：`A_i(s)`、概率支持／和、负载和条件成本完整给出；“minimizes”明确了正概率策略支持的最优性谓词。 |
| RP-4 | 45–54，continuation、单方移动和近似定义 | `keep`：输入为全部 labeled placements，输出为精确客户端均衡，(2) 明示所有设施和地点的量词。 |
| RP-5 | 57、59、62、65，主结果预告、公共地点作用、路线与约定 | `keep`：结论的混合／纯续局范围明确；全局约定不夹入证明；章节指针明确，没有用概括标签代替已编号的论证应用。 |
| RP-6 | 74–80，Construction 2.1 的分配与最大化 | `keep`：`O,q_t,t(i),J_t,W_t,p` 的对象和选择依赖均可直接恢复，有限族描述足以理解选择对象。 |
| RP-7 | 83，elementary comparison 及 “The comparison remains valid…” | `keep`：所比较条目的改变条件和严格提高结论同段给出；后句解释较小条目也增加时为何不受影响。 |
| RP-8 | 86–99，“reach R / selected profile / This strictly increases…” | `keep`：`R` 在 statement 内定义为最大 `w(C_t)`；改变的两组坐标及 `b` 前后值明列，局部 “This” 指紧邻的重分配操作。 |
| RP-9 | 102–106，“These … newly covered” | `keep`：紧邻 (3) 中输入 `w` 的集合差就是客户端集合，虽 `N_r` 本身是重量，句子并不要求另找一个集合。 |
| RP-10 | 109–131，survive/disappear 四个重量条件与反证 | `keep`：四式分别明确目的地范围和 `q_u` 条件，证明按相同分支顺序处理，使用 (4)–(7) 的编号；“no other facility load decreases”等短谓词有逐项构造支撑。 |
| RP-11 | 134，“terms involving J / arbitrary redistribution” | `keep`：精确指 (6)–(7) 的交集项；这是解释其允许任意子集被安排到目的地的作用，而非额外未写出的技术准则。 |
| RP-12 | 137–148，“next lemma / cap / each part / every pair…” | `keep`：此前仅预告概念，Lemma 2.4 立即给出 `a,h,(h+1)a,2a` 与 singleton 条件，配对求和展示了被省略会影响理解的运算。 |
| RP-13 | 151–167，“hypotheses are invariant / randomization cannot improve” | `keep`：前句不等式给负载不变性；独占重客户端的最低成本给不移动原因；混合无益由固定其他客户端后纯行动均不改善解释。 |
| RP-14 | 170，“packing and cap lemmas” | `replace`：精确对象为 Lemmas 2.4、2.5，当前要求读者从标签重建编号（SE-3）。 |
| RP-15 | 179–188，“stationary / keep … assigned location / This serves…” | `keep`：设施集合明确为 `F \ {f}`；Case 1 先打包原客户端再分配新覆盖客户端，断言所有 covered 客户端被服务有唯一构造指称。 |
| RP-16 | 191，“All remaining clients of J…” | `keep`：前两句依次处理可达 stationary facility 和仅可达移动设施者，“remaining”唯一指移动后无可达设施的 `J` 成员。 |
| RP-17 | 193，“its total assigned weight / these clients” | `replace`：需打包的是地点 `t` 的全部原客户端与新加入客户端之并，最近名词却是 added clients，未直接指定合并后的输入集合（SE-1）。 |
| RP-18 | 195–197，“genuinely newly covered / Once again / In both cases” | `keep`：前者区别 (3) 的集合与原 `J`，后两者逐一核对 Lemma 2.5 的初始分配条件并明确引用该 lemma。 |
| RP-19 | 201、207，“distinct unilateral deviations / These placements” | `keep`：前者是补全续局的局部动机，后者按不同 facility label 与不同 target 说明互异性；不是无新作用的重复。 |
| RP-20 | 207，“assertion is immediate / Equation … ensures termination” | `keep`：零 `R` 分支的零负载已写出；余下 placement 的过程直接调用已给的势函数变化式，不须再展开同一计算。 |
| RP-21 | 210，同址负载相等与偏离后 symmetry 限定 | `keep`：精确对象分别是 Construction 2.1 的 `p` 与偏离后所选纯均衡，不会把对称性误记为 theorem 的必要条件。 |
| RP-22 | 212–215，“next proposition / displayed strategies / Their…” | `keep`：命题输出列表和后续证明把显式 profiles 与默认规则区分；位长、显式检查范围和状态没有被混为一个高效求解结论。 |
| RP-23 | 218，“these processes terminate” | `keep`：指同句点名的 Lemma 2.4 mergers 与 Lemma 2.5 improving moves；二者的有限终止论证已给出。 |
| RP-24 | 220，“least-index client” | `replace`：`F={1,...,k}` 有顺序，`I` 只被定义为有限集合，未指定客户端的顺序；需补上确定默认规则所依赖的 ordering（SE-2）。 |
| RP-25 | 220，默认规则的 accessible/cost-minimizing facility | `keep`：设施标签已有顺序；最小化目标由 (1) 明确，严格改善客户端的选择条件也已给出。缺陷只在 RP-24 的客户端顺序。 |
| RP-26 | 220，负载分母、位长、(1)/(2) 检查 | `keep`：说明精确比较的编码依据，并明确用哪两个编号条件检查客户端与设施；没有把“可检验”替代成未说明的 verifier。 |
| RP-27 | 223，“short description / efficient search / separate questions” | `keep`：明确区分结论的证据状态，最后两问题是未解决目标而非 conjectural theorem。 |

## 按重要性排序的发现

### SE-1 — Case 2 的 packing 输入集合指称不唯一

- 定位：193 行，Lemma 2.6 的 Case 2。
- 开头引文：“At a surviving old location t, the added clients…”；特别是 “Apply Lemma … to place these clients…”。
- 类别：`[precision]`。关联：RP-17。
- 意图：把地点 `t` 上的全部待服务重量打包到 `q_t` 个 stationary facilities，满足 Lemma 2.5 的初始条件。
- 精度证据：191 行只把客户端分配到地点。193 行最近明确命名的集合是新加入者，即某个 `K_t subseteq J intersect C_t`。但 (6) 的预算控制的是 `W_t + w(K_t)`，供 packing 使用的列表应包含原 `J_t` 与 `K_t` 的全部客户端。“its total assigned weight”暗示整个地点的总重量，“these clients”的最近语法先行词却是 added clients；读者必须自行将输入扩展为 `J_t union K_t`，才能完成所述的设施分配。
- 必要性结论：这段不能删除；否则从地点级分配到设施级初始分配的步骤缺失，受益对象是需要逐项追踪原子客户端的目标读者。
- 裁决：`replace`；明确指“地点 t 的全部已分配客户端”，或明确原集合与新加入集合之并即可。无需增加新 lemma 或重写证明路线。
- 重要性：中等，局部构造的对象边界。置信度：高。

### SE-2 — 确定默认规则使用了未指定的客户端顺序

- 定位：220 行，Proposition 2.8 的默认规则；对照 32 行模型。
- 开头引文：“For the default rule, assign each covered client … repeatedly choose the least-index client…”。
- 类别：`[precision]`。关联：RP-24。
- 意图：给未显式存储的所有 placements 一个固定、确定、有限描述的客户端续局规则。
- 精度证据：模型给设施 `F={1,...,k}`，所以两个 “least-index … facility” 有现成顺序；客户端只有有限集合 `I`，并未设 `I={1,...,n}` 或固定总顺序。读者必须从显式输入编码自行选取一个枚举，才能解释 “least-index client” 并复现这条确定规则。这不是势函数终止性的数学审查，而是所输出构造缺少一项选择约定。
- 必要性结论：默认规则的内容必须保留，它实现 polynomial-size continuation description；仅补足所用顺序即可，不能删去规则来消除问题。
- 裁决：`replace`；在模型、约定或默认规则处固定客户端顺序，并说明按此顺序取首个改善者。无需改变算法或增加效率论证。
- 重要性：低，构造接口的小缺项。置信度：中高；算法读者容易自行补全，但稿内尚未给出该数据。

### SE-3 — 已编号的两个 lemmas 被临时描述性别名引用

- 定位：170 行。
- 开头引文：“The packing and cap lemmas now apply…”。
- 类别：`[precision]`；同时涉及结果指称标签，不判为虚构既有 theorem 名。关联：IA-8、NM-5、RP-14。
- 意图：把刚证明的两项工具交接给全体设施偏离的初始分配构造。
- 精度证据：目标是 Lemmas 2.4 和 2.5。二者已有编号，却未正式命名为 “packing lemma” 和 “cap lemma”；读者须把描述映射回两个 statement。这里歧义很小且对象就在近处，但共享标准明确要求已有编号的结果使用编号指称。这是局部引用接口的修复，不是要求作者放弃 “cap” 这一有用短称。
- 必要性结论：保留交接句的工作；它说明接下来 Lemma 2.6 的目的和依赖。无需因其内容可由上下文推知而删掉。
- 裁决：`replace`；用两个正式 lemma 编号标明依赖。
- 重要性：低。置信度：高；作为可读性障碍的程度轻，作为所给精确引用标准的偏差明确。

## 裁决与完整覆盖

- Necessity audit: **PASS**
- Referential-precision audit: **FAIL**
- Overall editorial verdict: **FAIL**

三个 SE findings 均为局部指称／构造接口问题；其中 SE-1 影响 Case 2 的分配对象追踪，SE-2 补全确定规则的输入约定，SE-3 使已有编号结果的引用符合约定。所有 `replace` 清单项均已进入上述 findings。逐节审查没有另留未编号的客观缺陷。

未发现客观上必须删减的重复段、没有具体读者收益的防御性声明或必须取消的术语。保留摘要中的作者名单、两段效率边界、两个 Cases 中各自核对可行性的句子，以及关于同址对称性的解释，均有可辨认读者工作；它们不应仅因个人偏好的简短风格而算作缺陷。本文的历史上下文选择、主定理放在工具之后的路线及是否给次要编码结论独立节标题，也不构成此次 FAIL 的依据。

本裁决不认证数学正确性、源文准确性、创新性或首次阅读顺畅性。报告提出的局部修复方向供写作者裁决，本审查没有编辑权限。
