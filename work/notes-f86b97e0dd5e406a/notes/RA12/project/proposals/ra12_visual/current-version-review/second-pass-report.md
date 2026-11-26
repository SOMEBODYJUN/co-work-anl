# RA12 最新两稿独立第二遍复核

本次接受 41 项当前恢复方案，复核 41 条问题记录，未发现仍需改稿或新增出处的实质问题。原稿中的低至中等置信读法及真实备选继续保留。这个结论是本篇第二遍复核的结果。

复核身份为 /root/ra12_visual，实际模型 gpt-6.2-sol，推理档 max。我此前参与本篇原图阅读、字形恢复、逐源核查与旧版本审查。本轮逐项核对当前版本与证据。

## 版本与检查范围

| 文件 | 实测起止 SHA-256 |
| --- | --- |
| source-transcript.md | c0fb0c63abf731a3ba5693e14d7f1c93f130296716d7ad5484e4ec41403b095d |
| study-notes.md | 373e90a051418289d80f176e7ffa9958dfb6fd16bd79b0329c3080d9ad48c1aa |
| source-target-map.json | 46aee54cef869184c66c6319bfb46cfb37f9f1f1aad9e02f7c8b351e84b2e56b |

完整范围为 7 物理页、42 重叠区、111 来源、96 目标、577 双向对应边、41 恢复和 41 问题。逐项复核两稿对应的文字、公式、分类及当前标签。程序复查所有 529 已登记工件的实际字节哈希、全部页区哈希、坐标与重叠关系、逐目标行哈希覆盖及映射互逆。Pandoc 解析得到保真 30 块公式，学习 31 块公式及 3 张表。

49 幅的完整实际图像观察以前一轮我逐张打开的记录为依据，本轮重新核对全部图哈希并回核当前内容和映射。第7页整页与六区本轮再次实际打开。111 幅的来源局部笔迹来自我在旧终审实看的 800 dpi 逐源图，本轮逐行回核相同图义与当前映射，相关 800／1200 dpi 工件另有实际重开清单。本轮共重新打开 37 幅，其中 30 幅为已登记的原 PDF 定向图，覆盖 REC35–41 登记的全部原 800／1200 dpi 图。

- 上一轮我的 49 幅观察 [second-pass-report.json](../granular-update/second-pass-report.json) f9e00096f23f1a23a04244a6a9056aa5de9e38719695c749bd887bd95235883d
- 早一轮我的 111 幅逐源阅读 [granular-source-reread.json](../final-7f2b9670fcd1/granular-source-reread.json) 727a349cdcdb4a265c370c8eb2ab72cfea3b40708c02aae667b94d218990022f
- 111 幅原 PDF 直渲图索引 [crop-index.json](../../../audit/granular-reread-7f2b9670fcd1/crop-index.json) 720c21bb60ec6ed6fb0ce650404ff0d572ac9bf1a030913280ad2d7b0f846956

## 页与正文对应

- **第 1 页**。提纲、例题及拼接引理的原顺序齐全。重开题头 800、1200 后核到 i/e 间只分出两条较高纵笔，当前 T004/S005 兼记近 Littewood 与 t/l 共笔。例题两左一右、并下限点及第三条两处限定校读仍有说明。开覆盖把片内开提升为全域开，闭覆盖另需局部有限，可测拼接另需可数。
- **第 2 页**。原题的则和三段 Lusin 内容可追，紧闭和值层、右端 X_i 临时误记、两个 E 未下标各自保留。重开 U15 800、1200，Σ 上下无另写索引；当前 S023 原引用裸 Σ，与 T016 一致。按不交值层得到闭并和误差和，正向证明不用原漏标差式。
- **第 3 页**。闭 δ 与 k 的先后原写、限制函数及 s.t. 均依原段保留。一般交集只保连续和几何误差，逐点收敛本身不保连续极限。重开两处 Englov／Engrov 及该页「且」，前者作第 4 页姓名的异形对照，后者只作 P5 连接字形比较；B1 横仍可定位。
- **第 4 页**。原上半保留 Gδ、Hδ、帽 Fδ 与两横 B2/B3、严格不等和单对差式括。重开页首原名的 800 及三幅 1200，g 后接 r 而圆环在 r/v 间，当前近 Egrov 和紧连写备选并存。下部环带闭拼接逻辑成立，再看闭集旁句支持保留「上的有一个」，个左有短提候选。
- **第 5 页**。两个姓的题签在各条件旁，就地登记 Tietze 首 e 开口与第五位点、Urysohn 末部可能分笔。第 (3) 条原独立 ∃ 已回到「则」后，[0,1) 原右圆弧保留，学习订正端点及 C(F) 类型。两限制间 B 样笔与真正的合取对照具备直接图。Remark 仍止于「分」，页底第三项 a.e. 长箭属于本页。
- **第 6 页**。原证明标题的细单杆与 P5 a.e. 箭分属两处。延拓第一行 g 与逐 k 的 g_k、随后限制原漏脚标、可和误差、事件等式和好坏集合方向均在。原边字易与考察仍分开说明；任意和「在＋纵向小字」备选未被简化为直接可读处处。好集是相对 E 的外并内交，只保证几乎处处最终逐点恒等。
- **第 7 页**。新重开整页与六区，四边、上下重叠及页面中心均无字迹或后续内容。T044 直接列七张原图，S052 表列的空白页事实有整页图。现有 111 来源中没有 P7 的伪造内容框。

## 42 个重叠区域对应

| 原区 | 观察及当前核对 |
| --- | --- |
| p0001-r1c1 | 原左上见姓名、三条提纲和例题左端。新看题头登记英字两高竖；第三条两个校读与例题有限测度的弧继续各自归原位。 |
| p0001-r1c2 | 左边只接第一条的‘区间并’，右大块空白。下接全称 ε、存在区间列及 s.t. 样简写。 |
| p0001-r2c1 | 例题原式 m 后与并前分别有左弧，右只有一弧。引理的 Y 后句点、X 左独写墨、若后 f_a 与首逆像短横连在这一带。 |
| p0001-r2c2 | 上接例题末，读完开覆盖式、则后的全函数 f 和末并项的外括归属；右半空白，无第二段并图。 |
| p0001-r3c1 | 首是‘注意’旁移的小笔团和限制连续性，随后由 X_a 开、闭覆盖的局部有限条件，末可测函数两疑字和可数覆盖。‘注意’右钩的形状可作心低部，仍应保留独字异读。 |
| p0001-r3c2 | 先接子空间拓扑等式右侧，后见 X 中开和证毕样结尾。右下为局部有限闭覆盖和邻域只交有限成员，旁句止于覆盖。 |
| p0002-r1c1 | Lusin 题头、a.e. 有限到满足的小损失式、限制前 s.t.；末横行是‘并给出闭集构造 Fδ 的表达式’。 |
| p0002-r1c2 | 接可测函数末和 ∀δ>0、∃Fδ 的闭字上注；下部限制函数等式右齐。右侧留白。 |
| p0002-r2c1 | 从闭集表达式末至 Pf (1)、值层族起、展开式两点、Lebegue 样英文字和紧闭∃。后一行 s.t. 位于损失式之前。 |
| p0002-r2c2 | 从 E_l 一带到原 E=∪X_i，X 有交叉；以下的正规性及 δ/ℓ 接在相应左部，右无独立旁笔。 |
| p0002-r3c1 | 以令 Fδ 的有限并起，测度链左两项各有外括，(2) 后 f∈M(E)，底见则、函数族和 s.t. 的开端。 |
| p0002-r3c2 | 中右旧实查已见链式两左一右及裸 Σ，本轮 U15 原PDF两倍数复看证实。S023 原引述与 T016 同步，正常有 i 的值层求和另在订正式。 |
| p0003-r1c1 | 从‘由(1)’、全称 δ 和 k 到 Fδ 的上标‘闭’与 E，无独立 ∃。该行右部给 s.t. 与分母有指数的预算，第二行起且、令和交式。 |
| p0003-r1c2 | 左端承 δ/2^k 的末笔；上部‘则’在定义后，中部续完亏损再转到交子集闭。右大块空白。 |
| p0003-r2c1 | 上接且每个交项子集，二写连续后有‘下证’，下起因 f a.e. 有限和零事件，旁写另一个归一式；g=f/(1+∣f∣) 后的则有独立字位。 |
| p0003-r2c2 | 接交集连续句和下证，中部零测式 +∞ 后一右弧，后续两分式的绝对值有别。当前两稿分别解释原括、分母绝对值和有限性。 |
| p0003-r3c1 | 首‘或用 Egorov 定理’，有限 m(E)，存在 φ_k→f，∀δ>0 ∃ Fδ⊂E，闭字在上，s.t. 之后左侧开始预算。 |
| p0003-r3c2 | 底部接 m(E∖Fδ) 末以及 B1 的独立横线，右侧大部空白；未见比较量或界值，学习稿的预算不视为本区原写。 |
| p0004-r1c1 | 页首用／同保留择优，紧邻 Egrov 样五组，后见 Gδ⊂E 与原 s.t.。对照图新开后，原 r/v 间圆环与 P3 Englov/Engrov 两处相区分；B2 依旧在原测度式后留横。 |
| p0004-r1c2 | 左缘承上一格 f。可测的内正规性收尾，预算不等号右是一道长空线。 |
| p0004-r2c1 | 最上承 Hδ，带帽 Fδ 和交式居左。引导两字和损失的并、严格小于、分拆第一项共享 Gδ 后的竖笔依序可见。 |
| p0004-r2c2 | 区首给不等空线，以下只见亏损链右端和拆项的 Gδ∣Hδ。余右部全空。 |
| p0004-r3c1 | m(E)=+∞，定义环带 B(0,k)∣B(0,k−1)。下一行并的下限 k=1 明确；末‘需要用局部有限性’。 |
| p0004-r3c2 | 横接最后 B 的括号，从「但在」和 A_k∩E 到「上的有一个闭集」。新重看 1200 可分的、两个部件的有和个前短提，保留有一个为可行读法。 |
| p0005-r1c1 | 先是‘Lusin 逆定理也成立’和 Th. 设 (X,τ)，下见 (1) X 正规、(2) 全称闭子集及若 f∈C(F)。 |
| p0005-r1c2 | 上左承‘下述等价’，下行只续 Tietze 的存在 F、s.t. 和末限制等式。右有留白。 |
| p0005-r2c1 | 首接延拓输入 C(F)，其下括注 Tietze 的首 e 开口/末 e 闭眼，且处附近原独写 B 样形。再下为 Remark 与单列的 C=A∪B。 |
| p0005-r2c2 | 实见则后 ∃ 与右端 [0,1) 写法。Urysohn 小签回环紧邻高升笔，随后另圈和 n；正文披露可行分笔。Remark 下接 & 及右缘可见的截句。 |
| p0005-r3c1 | 首‘设 f 是 E 上几乎处处有限函数’，三项依次可测、简单函数逐点、连续函数 a.e.。简单列的括末可见一个小点。 |
| p0005-r3c2 | 接有限函数、E∈M、连续类及 s.t. 末点；本页末行仅有 a.e. 标长箭趋 f。下一页证明标题的箭形不归入 U19 几何框。 |
| p0006-r1c1 | 页首 Pf 的细单杆箭头，另见第一个全空间 g、逐 k 闭 F_k、g_k 与保真不带脚标的限制，后为 1/2^k。此次 U01 800/1200 确认箭头。 |
| p0006-r1c2 | 承接 g∣Fδ=f、下一行 g∣F_k=f 的右侧及连续类，右限制式在 g 后无独立 k。第3页预算的 δ 未出现在这里。 |
| p0006-r2c1 | Borel Cantell 的末 i 未独立见；首 ∞ 上极限及失配式可辨，页边字正常图受裁，考察直接可读。包含式右 F_k 后另见孤右弧。 |
| p0006-r2c2 | 仅重叠给 F_k 的末尾和独立的两处 =0，右域与其他位置空白。 |
| p0006-r3c1 | 外 ∩ 内 ∪ 的内并无上限，下一行（几乎任意）x 用限定校读，继而外 ∪ 内 ∩。末行 N(x)、s.t. 与阈值下擦，本稿取 ≥ 并保留 > 备选。 |
| p0006-r3c2 | 接上端零、下极限式的右弧，再以 f=g_k 恒等收尾。未见再往下延长的证明，纸底留白。 |
| p0007-r1c1 | 左上空白，顶边与左边均无笔。 |
| p0007-r1c2 | 右上空白，顶点与页区右边无墨。 |
| p0007-r2c1 | 左中空白，上中重叠处无字迹。 |
| p0007-r2c2 | 右中空白，重叠带未牵出公式或页边字。 |
| p0007-r3c1 | 左下空白至纸底，未见编号。 |
| p0007-r3c2 | 右下空白至纸底，无签记或边注。 |

## 先前发现的回查

- **F01（RA12-REC-40）**。S023 与 T016 的原式均为裸 Σ，数学式绑定 i 另说明。
- **F02（RA12-REC-41）**。T033 原位重作独立 ∃，T034 说明保真与学习语义译写。
- **F03（RA12-REC-37/38/39）**。P4 的 Egrov 近形、P5 两姓局部笔形与有限置信候选均在两稿说明。
- **F04（RA12-REC-32/35）**。第5页末 a.e. 与第6页标题单杆由各自实体框标注。
- **F05（RA12-REC-35）**。T034 已可直达本页独写及同手 B、且的比较图，且仍为限定读。
- **F06（RA12-REC-35）**。T044 有当前重新打开的 P7 整页六区，S052 有整页图。

S023 引述原并项时用下标 i 概括原本有上下限的并，具体原并可回到 T016。S023 原式的裸 Σ 和值层订正式的有索引求和各有据。P4 闭集旁句的个前短提出现在有与个之间，配合整句可读「有一个」。

T029/S029 的第 3 页与第 4 页姓名原形均有直接图证，正文的 P4 引述归 P4 来源。T034 的 P3「且」属于比较图证，P5 两个限制条件的原墨内容回 P5-U10。空白页由实际页／区图支撑。S003、S005、S042、S052 及 T015、S013、S021、S045 的原记号和跨页出处逐一核过。

## 各恢复与相应问题的当前独立结论

| 恢复／问题 | 判断 | 依据 |
| --- | --- | --- |
| RA12-REC-01／RA12-ISSUE-01 | 接受现有方案 | 原引理先给 f:X→Y，若后 f_a 带下标，两个箭头均右指 Y。限制子空间的逆像用开覆盖升回 X。首逆像只见短横，以后两项 −1 及逆像类型恢复；反向命题虽成立却不是纸面证明。 |
| RA12-REC-02／RA12-ISSUE-02 | 接受现有方案 | 首 F 下闭环 δ，同线预算及下行下标是 k，方程首没有独立 ∃。选择逐 k 的闭 F_k 再相交，可在共同域限制连续并控损失。若把同一个 Fδ 绑定全部几何预算会错误强迫损失为零。 |
| RA12-REC-03／RA12-ISSUE-03 | 接受现有方案 | 失配谓词在花括内，包含号右是 E∖F_k，F_k 后孤右弧有独立注记。坏集外交内并，好集取补外并内交；只在偶数项失配的点检验了操作顺序。有限阈值可平移，不能升级为一致收敛。 |
| RA12-REC-04／RA12-ISSUE-04 | 接受现有方案 | 题头取「定律」，保留集、函数、收敛三条顺序。有限开区间题实写对称差，单侧差无法控制多出的部分。第三条额外笔与短提在 REC15/17 处理，现版也披露题头两高竖与可行连写，定理所指和各笔字母分开。 |
| RA12-REC-05／RA12-ISSUE-05 | 接受现有方案 | 并、给、出三字有独立部件可辨。纸上 X_i 与两处未下标的 E 保留，f 后上下两点单列说明。以两个不交正测度值层检验旧差集式；实际构造先紧内近似再有限闭拼接。 |
| RA12-REC-06／RA12-ISSUE-06 | 接受现有方案 | 首预算 k 明显升写，末和式 k 与 2 接近共底。保真保留 2k 并说明低指数备选；∑1/(2k) 发散，不能支持共同闭集的预算。 |
| RA12-REC-07／RA12-ISSUE-07 | 接受现有方案 | 上模值逆式绝对值对分明，下带符号逆式确无 g 的绝对值。代 f=−2 能排除原带符号逆式；学习保留 ∣g∣<1 并在有限点恢复正确分母。 |
| RA12-REC-08／RA12-ISSUE-08 | 接受现有方案 | 页首‘用’的穿框长轴与第 3 页或用、第 4 页需要用相似，‘同’保留。Gδ 是删去的坏集，三条原留空未被视为已写；B2 规范为 m(E∖Gδ)>m(E)−δ/3，后续联合损失的原严格号与学稿 ≤ 分开。 |
| RA12-REC-09／RA12-ISSUE-09 | 接受现有方案 | 原环带、分片交、各片闭近似与局部有限提示均有实迹。‘上的有’中第一字的形异于有，个左短笔可作一。球链本身不能当局部有限，写环带后有界邻域只交有限块。并号上无独立加号。 |
| RA12-REC-10／RA12-ISSUE-10 | 接受现有方案 | F 的两横和 [0,1) 右端圆弧均可辨。B 非空时 1 须在值域，延拓输入域为已给闭 E，学习稿相应订正。两限制间的 B 样独写只作「且」的语法校读。当前 T033 独立 ∃、T034/S037 姓名近形和 T034 比较图均已回核。 |
| RA12-REC-11／RA12-ISSUE-11 | 接受现有方案 | ‘除非’阝/余形和第二组双直比所谓贴合，已明示中置信恢复。右缘实际止于‘分’，下一行 C=A∪B 独立；可测分隔足以推出加性，A=B={0} 检验了不能逆推必须可分。 |
| RA12-REC-12／RA12-ISSUE-12 | 接受现有方案 | 第 6 页首个 g 是全空间延拓，后逐 k 的存在式为 g_k，原限制式 g 未见脚标。学习恢复两个匹配限制，预算为 2^{-k} 而非页 3 的 δ 权重。把所有延拓当同一个 g 一般不可能。 |
| RA12-REC-13／RA12-ISSUE-13 | 接受现有方案 | 正常页面左缘边字受裁。重开已登记的原矢量放宽裁框图，围绕笔与两处内墨支持‘易’，不强合为‘易考察’；考察可直接读，和第 4 页‘考虑’区别明确。保留另的低置信读法。 |
| RA12-REC-14／RA12-ISSUE-14 | 接受现有方案 | 页尾确为可测函数，近似见一处低捺与后一亻、以样笔，不满足逼近需两套走之。正文保留另读；可数并可测是蓝色解释，未把孤句当作完整定理。 |
| RA12-REC-15／RA12-ISSUE-15 | 接受现有方案 | 的、独立团、几、乎分开。弯折、中轴和末扫支持‘是’作为低至中置信候选，不能靠 Egorov 倒推出‘列’，列的独立刂亦欠证。备选列、也及改笔目前有记。 |
| RA12-REC-16／RA12-ISSUE-16 | 接受现有方案 | 并号等号右实际只有水滴点。有限列一致重编号无碍并集，数学不能对点形作独立的 1，当前标为规范恢复。首项 i 样与学习统一从 1 开始的边界可分。 |
| RA12-REC-17／RA12-ISSUE-17 | 接受现有方案 | 每和个之间有极短上提，首两条同位短横更长。取平行结构弱至中读一有据，每个与每一个数学同义因此保留普通点迹备选。 |
| RA12-REC-18／RA12-ISSUE-18 | 接受现有方案 | 例题整式两左一右，且 ∞ 后独立右弧与开区间末门框样收钩不同。分组必须令测度作用于整个对称差，不能用其数学类型推断纸上有第二右弧。 |
| RA12-REC-19／RA12-ISSUE-19 | 接受现有方案 | 目标右上点、中竖穿横和下钩与 P1 要求相近，较合求而非估或证。保留原 < 并以不交两项可取等号反查学习订正。 |
| RA12-REC-20／RA12-ISSUE-20 | 接受现有方案 | B1 左端和 s.t. 末点在 1200 图分立，现源框 x0=1891、x1=1760，真实边缘在内。正向看新界包住墨迹，反向旧框会裁掉左尖和点且区属未变。 |
| RA12-REC-21／RA12-ISSUE-21 | 接受现有方案 | S052 与第 1 页例题及提纲、T015/S021/S013 与第 4 页环带、S045 与第 6 页实际证明方向的 18 条指定出处均有实质联系。四处原已修复的比较目标可回到实际图，新增的 T034 和 P7 图证在 REC35 单列。证据关联不被混作正文源边。 |
| RA12-REC-22／RA12-ISSUE-22 | 接受现有方案 | X 左独立字与 P3 且同有左竖、右包及底扫，后另有反 E 样 ∃、一个开覆盖。有依据选择且，数学只确定独立条件。分歧和并非唯一的边界明确。 |
| RA12-REC-23／RA12-ISSUE-23 | 接受现有方案 | 注意后有两点及偏低卧钩。视觉上保留意的偏位心底稍优，数学角色的独立则具有与同手 U 钩可类比的根据，当前明确二选及不同意见，均不改变限制连续性引入。 |
| RA12-REC-24／RA12-ISSUE-24 | 接受现有方案 | P1-U18 真有两个分开的有形，第一横穿左斜、第二另有完整月样，限后是个，没有独立多；学习有限多个属语义规范。P4-U17 的首形为的，属另一处。 |
| RA12-REC-25／RA12-ISSUE-25 | 接受现有方案 | 并号后外左弧与限制左括分开，U 后二右弧独立。保真有原外层，学习引式保留，首逆像 1 的恢复另有注明，外括不改变并的对象。 |
| RA12-REC-26／RA12-ISSUE-26 | 接受现有方案 | P2 可测函数末独立则与 P3 则 g 的右钩可比。P2 限制式／预算式，P3 首预算的三个 s.t. 均实际看到，各在本句正确位置。T014、T020 现只用显式薄空格作版式。 |
| RA12-REC-27／RA12-ISSUE-27 | 接受现有方案 | Lebegue 是 e 到 g 间未见独立 s 的近形，Borel Cantell 在末双直后直接收冒号，末 i 未独立成形；两处正文已就地披露。内正规性与可和零测论证确定所指定理，无法反证全部规范字母均写全。其余姓名本轮的正反检验另见 REC36–39。 |
| RA12-REC-28／RA12-ISSUE-28 | 接受现有方案 | 损失链上 m 后与并号后独立两左弧，随后可数一右弧，当前保真原迹保留。数学式的闭合与原两处 E 漏 i 是独立问题，S023 现分别说明，并将另一处原裸求和号与规范有索引的求和分开。 |
| RA12-REC-29／RA12-ISSUE-29 | 接受现有方案 | P3 共同闭集损失的测度项物理只有一对括弧，并右和 E 间无内左弧。按 De Morgan 取各差集的并；把 F_k 放到并的辖域外会留下游离 k。 |
| RA12-REC-30／RA12-ISSUE-30 | 接受现有方案 | P3 零测式 +∞ 后确只有一右弧，左小弧与绝对值左界的分笔保留不确定。蓝注标明规范补全。单取正无穷不足以排除负无穷，原数学有限性支持取模。 |
| RA12-REC-31／RA12-ISSUE-31 | 接受现有方案 | P4 Gδ 到 Hδ 只有一条外邻差画，H 的左斜属于 H 本身。首项外一对保留，兼写候选已载。H⊂E∖G 使左结合分解成立，右结合会把 H 误放回去。 |
| RA12-REC-32／RA12-ISSUE-32 | 接受现有方案 | P5 A/B 间交叉闭环与 P6 箭头细横确可辨，保真与学习表达均作区分。现 P5-U19 仅以 a.e. 长箭头为本页原笔，将下一页箭形交给 U01 的细单杆标签。学习 ⇒ 是逻辑表达，证法仍由 (1) 到 (3)。 |
| RA12-REC-33／RA12-ISSUE-33 | 接受现有方案 | 两组笔不似 P5 两个同形处。右纵小笔与中等置信任意可相容，P3/P4 的在形又给另一个有据分笔。正文与候选明确保存分歧，数学只确定全测度点逐点最终恒等。 |
| RA12-REC-34／RA12-ISSUE-34 | 接受现有方案 | S003 的 Δ、M(E)、a.e. 及 s.t. 已有具体原记号来源。S005 指下一题的有限测度/对称差链接 P1-U05/06，S042 引闭 A/B 分离链接 P5-U08–10。逐边可逆且语义确有对应，新增比较图与正文源分开。 |
| RA12-REC-35／RA12-ISSUE-35 | 接受现有方案 | 新重开 P5 的限制行及同页交集 B、第 3 页且，独写连接符有近 B 的折环，两限制合取只支持「且」的语法校读。P5-U19 与 P6-U01 分属不同物理页，a.e. 长箭头及标题单杆各归其框。新重开的 P7 整页六区均无墨，T034、T044、S052 的直接图证齐全。P3 比较字与空白页都未生成不实内容边。 |
| RA12-REC-36／RA12-ISSUE-36 | 接受现有方案 | 800 整单元和 1200 姓名图中，i 与 e 间分出两条高竖和短横，未辨另一个 l 竖。Littewood 近形和第二 t/l 共笔均能解释此形。三条原则确定所指 Littlewood，无法从数学判定某一个字母的实际书写；T004 和 S005 已如实限定。 |
| RA12-REC-37／RA12-ISSUE-37 | 接受现有方案 | P4 三幅 1200 局部均见 g 后直接到 r，后接圆环，再到 v。将圆环移到 g 与 r 间的解释与实际位置冲突，仍可保留紧连写。P3 两处引名另有 n 状连笔，与 P4 原形有别；一致收敛证明支持同一个标准姓名。T029 与 S029 分别有直接对照图。 |
| RA12-REC-38／RA12-ISSUE-38 | 接受现有方案 | 看见 i 上一点、首 e 位的开口弧、末 e 的闭眼及 z／7 形上方独点。Tictze 近似分字与开放 e、简写 z 都能解释这些墨迹。闭集连续延拓识别 Tietze 的指称，不能从命题推回任一分字唯一；T034/S037 的说明限定得当。 |
| RA12-REC-39／RA12-ISSUE-39 | 接受现有方案 | 三幅 1200 裁图皆见 s 后开放回环接高升笔，再见独立 e 样闭环与 n。我的字形近 Urysden，也能作 o/h 不规则连笔。闭集两端分离可确定规范 Urysohn，不能排除已记的 Urysoden 和 Urysolen 近形。当前两稿就地保留读法分歧。 |
| RA12-REC-40／RA12-ISSUE-40 | 接受现有方案 | 新重开的 U15 800 与 1200 均见求和本体下方直接为空，邻近 i 属 E 或 F 的项下标，未构成 Σ 下标。T016、S023 的原引述都用裸 Σ。按前面有限值层为订正式绑定 i 在数学上必须，不能据此补出原迹未写的字符。 |
| RA12-REC-41／RA12-ISSUE-41 | 接受现有方案 | 则字结束后有独立反 E 形，横画与接续的「连」完全分离，且同页给出的另一个 ∃ 为直接对照。T033 原位保留 ∃，保留 [0,1) 的视觉事实；学习稿的存在句和 [0,1] 订正与端点要求相容，不能把两个中文字符反投为原笔。 |

## 本轮实际重开影像

| 证据 ID | 项目相对路径 |
| --- | --- |
| artifact:granular-39393b8f1f6e006c99 | `audit/granular-reread-7f2b9670fcd1/RA12-P001-U01-800.png` |
| artifact:ev-proposals-ra12_math-granular-update-crops-p1-littlewood-letters-1200-de397556 | `proposals/ra12_math/granular-update/crops/p1-littlewood-letters-1200.png` |
| artifact:granular-544433a3a4033821a1 | `audit/granular-reread-7f2b9670fcd1/RA12-P002-U15-800.png` |
| artifact:ev-proposals-ra12_visual-granular-update-crops-p2-raw-sum-index-1200-93e9ae0f | `proposals/ra12_visual/granular-update/crops/p2-raw-sum-index-1200.png` |
| artifact:granular-f65f1d92d17a4e0651 | `audit/granular-reread-7f2b9670fcd1/RA12-P003-U09-800.png` |
| artifact:granular-d778f57ceca09485ad | `audit/granular-reread-7f2b9670fcd1/RA12-P003-U16-800.png` |
| artifact:granular-d9dc95996c4f15c064 | `audit/granular-reread-7f2b9670fcd1/RA12-P004-U01-800.png` |
| artifact:ev-proposals-ra12_visual-granular-update-crops-p4-egrov-name-1200-75d24442 | `proposals/ra12_visual/granular-update/crops/p4-egrov-name-1200.png` |
| artifact:granular-ce71df24e20b4a0eba | `audit/granular-reread-7f2b9670fcd1/RA12-P005-U07-800.png` |
| artifact:ev-proposals-ra12_visual-granular-update-crops-p5-tietze-name-1200-d9295eaa | `proposals/ra12_visual/granular-update/crops/p5-tietze-name-1200.png` |
| artifact:granular-bd762a88d8c1db434b | `audit/granular-reread-7f2b9670fcd1/RA12-P005-U11-800.png` |
| artifact:ev-proposals-ra12_visual-granular-update-crops-p5-urysohn-name-1200-9dced233 | `proposals/ra12_visual/granular-update/crops/p5-urysohn-name-1200.png` |
| artifact:granular-361e28af4bfc30a530 | `audit/granular-reread-7f2b9670fcd1/RA12-P005-U09-800.png` |
| artifact:ev-proposals-ra12_visual-granular-update-crops-p5-urysohn-exists-1200-4a66dee1 | `proposals/ra12_visual/granular-update/crops/p5-urysohn-exists-1200.png` |
| artifact:granular-196207eb1ec0df3947 | `audit/granular-reread-7f2b9670fcd1/RA12-P005-U10-800.png` |
| artifact:visual-crop-p0005-second-urysohn-standalone-1200 | `proposals/ra12_visual/crops/p0005-second-urysohn-standalone-1200.png` |
| artifact:visual-crop-p0003-second-qie-known-1200 | `proposals/ra12_visual/crops/p0003-second-qie-known-1200.png` |
| artifact:visual-crop-p0005-second-urysohn-ab-known-1200 | `proposals/ra12_visual/crops/p0005-second-urysohn-ab-known-1200.png` |
| artifact:granular-bf95d9f8e01b0b634c | `proposals/ra12_adversarial/final-7f2b9670fcd1/p3-qie-comparison-1200.png` |
| artifact:granular-baacc9e34374370788 | `audit/granular-reread-7f2b9670fcd1/RA12-P003-U03-800.png` |
| artifact:granular-0049b9cf568d7a0640 | `audit/granular-reread-7f2b9670fcd1/RA12-P005-U19-800.png` |
| artifact:granular-8606c0c810dc9a0d2f | `audit/granular-reread-7f2b9670fcd1/RA12-P006-U01-800.png` |
| artifact:granular-ebebc37237a74fe374 | `proposals/ra12_visual/final-7f2b9670fcd1/p6-proof-single-arrow-1200.png` |
| artifact:ev-proposals-ra12_visual-granular-update-crops-p4-local-has-count-1200-0b8945ad | `proposals/ra12_visual/granular-update/crops/p4-local-has-count-1200.png` |
| artifact:ev-proposals-ra12_math-granular-update-crops-p4-egorov-letters-1200-196fac78 | `proposals/ra12_math/granular-update/crops/p4-egorov-letters-1200.png` |
| artifact:ev-proposals-ra12_adversarial-granular-update-p4-egrov-name-1200-c6199dec | `proposals/ra12_adversarial/granular-update/p4-egrov-name-1200.png` |
| artifact:ev-proposals-ra12_math-granular-update-crops-p5-tietze-letters-1200-ada79724 | `proposals/ra12_math/granular-update/crops/p5-tietze-letters-1200.png` |
| artifact:ev-proposals-ra12_adversarial-granular-update-p5-tietze-name-1200-fdb03c1e | `proposals/ra12_adversarial/granular-update/p5-tietze-name-1200.png` |
| artifact:ev-proposals-ra12_math-granular-update-crops-p5-urysohn-letters-1200-c1a4abf1 | `proposals/ra12_math/granular-update/crops/p5-urysohn-letters-1200.png` |
| artifact:ev-proposals-ra12_adversarial-granular-update-p5-urysohn-name-1200-158da950 | `proposals/ra12_adversarial/granular-update/p5-urysohn-name-1200.png` |
| image:p0007 | `pages/p0007.png` |
| image:p0007-r1c1 | `regions/p0007-r1c1.png` |
| image:p0007-r1c2 | `regions/p0007-r1c2.png` |
| image:p0007-r2c1 | `regions/p0007-r2c1.png` |
| image:p0007-r2c2 | `regions/p0007-r2c2.png` |
| image:p0007-r3c1 | `regions/p0007-r3c1.png` |
| image:p0007-r3c2 | `regions/p0007-r3c2.png` |

结构化记录另含每个来源、目标、恢复及问题的完整 ID、位置、阅读依据、证据或实际双向去向。接受的是现行限定校读和规范化方案。台账原状态在本轮记录时仍为待登记。
