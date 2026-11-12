# Boss1 3D 只读审查：perfect exact4 与独立正规化到三一致超图

审查对象是 canonical 边 `exact-four-to-one-v4-and-biregularization-to-three-uniform-independent-set-9fa9ce8a7e4a75ec`，正式 done 包是 `boss5-mz-visual-repair-9fa9ce8a7e4a75ec`。本审查不代替原包主覆盖，不造新 done，不修改仓库、队列、正文、登记、边或收据。

**判定：whole / accepted / unconditional / ALL 可以采用。** 两个 source 的共同合同，经本轮独立核查的正规化、typed 层化、逐 ID 解析接口和精确无权展开，支付目标 `M-9f8033b6e1a4485b97636171b09f8218` 整句。未发现需要新 repair 的承重缺口。此结论严格保留两个共同输入，不把 source 任一项单独提升为充分，不把成熟解析定理复用冒称本轮重新证明。

## 1. 精确对象、当前版本与实际读取

本轮使用 `research_runtime.load(..., verify=False)` 读登记结构，仅对本范围正文、evidence、当前 receipt assets 和旧资产处置逐文件核 SHA，没有全仓重复 hash。最终快照详见 `current-bindings.json`。最终观测 HEAD 是 `013e6e5f6574b9ee1afb2f8f2ce3b8a7329f4967`；边、收据的原始字节 SHA 与程序使用的规范化 JSON pin 分开记录，二者不可混同。

| 对象 | 当前版本 | 当前 registration pin | 本轮判断的合同 |
|---|---:|---|---|
| `M-ab4a576ed0be482b89d4a646ffc102b9` | 4 | `e2f4d171f9174665027371524263e60473a991292495c0041683392feaa38077` | 每个先固定 ε>0 的 perfect exact4、常数字母表、NO≤ε 的 NP-hard 源；不附赠双正规 |
| `PCP-EXACT-PROJECTION-PERFECT-COMPLETE-BIREGULAR-ROUNDING-v1` | 1 | `3fb491cd85e99950c05f1ce9bbcd8ec6daabc5bf1aae02627ef4efb4e7307922` | 保原投影、标签与 perfect YES，值误差≤η、显式多项式的独立双正规化 |
| `M-9f8033b6e1a4485b97636171b09f8218` | 4 | `389687c25c6745ad7df87c021157ed183a8364e118d6d1fa6614a14a0b3d5816` | 固定 δ 的有限无权三一致超图，完整二着色 YES 与无比例≥δ独立集 NO |

当前边原始 SHA：`b88c501a9db991931813fb90707a0b0b3595195597a57a0b6339ab6f765379fc`；native pin：`546769546af0188be6685de781e0546f34977b7907a1834ebfeb6187bf9f675c`。

当前收据原始 SHA：`11e81a960b2a279161747ddcc26abea54aa1e1ac4b8a8292ddabdc46941c92af`；native pin：`960745558098fdc046ca8f276cac3089801a56e3f009228c103194ef0a585b1d`。任务仍是 done、owner Boss5，task 嵌入 receipt 与文件 receipt 的 native pin 相同；integration 中对应的 edge/receipt pin 也相同。

实际新读范围：

- `AGENTS.md`、`research/IMPLEMENTATION.md`（包括第三阶段）、`prompts/03-map-worker.md`；当前及被替代 task/receipt 的定义、状态、数学说明和逐资产处置。
- 三个当前 endpoint 的完整记录；共享 v4 正文全文（SHA `d0273adacbf4ccbb9d6cd954cdfd44dddb5f8a8e969067107f63c77bdaaf4b78`）；独立正规化正文全文（SHA `13803e66abc6432815634589e75cbc08238ad74287d89707120274fdfc7927d6`）。
- 当前 `proof-review.md` 全文（SHA `87b2cf6a26b8bfc7e440f6701d6969a25e8726c239e964c86b88a19ebf705868`）、当前 reading ledger；abad 旧 proof 的源合同、完整正规化、typed 层化和超图章节及旧阅读 ledger；19cf 历史 proof 的“ 双正规化桥与三一致超图”完整章节。旧 proof 的图应用未在本 worker 独立认证。
- FMW 冻结 Revision2 原 PDF（SHA `48baa160d5d15e61aaf99b24b6fc15518c20f204d165fc96de1251d9d8a82ea0`）印/物理 pp4–6 的定义、主源合同与 Corollary1.10；Appendix B pp99–100 完整精确化。未新读其119页全部源内核。
- KS14 冻结 arXiv v2 原 PDF（SHA `2dcb03c6bc10dda5503452719c74bb57c5463e8b34bdbef5d06463cb7d74dc24`）：§2.2–2.3、Definitions2.4/2.6/2.7、Conjecture2.5与脚注、Theorem2.8；§5 的相关空间/算子/解析合同、D 分布、§5.1–5.3至Eq.(33)和解码结尾；Appendix A 全文。印7/24/25/28页（物理8/25/26/29）已渲染目视，特别核负指数、参数顺序和最终常数。

成熟复用边界：FMW 外层/middle/Grassmann 内核作为当前已认证 theorem 合同复用，保留其正文和冻结证据入口，没有重证 Condition3.12、Lemma6.64 等。KS14 的相关空间、不变性、reverse hypercontractivity 及 Lemma5.14 的解析结论作为成熟已证合同复用；本轮独立验证它们怎样接到当前带身份多重约束和均匀测度。GS20 及两图归约只作旧资产处置背景，不承担本条超图边的推导；本轮没有重新审 GS20 全文。MZ 原论文未在本 worker 重审，本条边也不以其作为数学前提。没有旧科研程序、枚举或 LP 重跑。

## 2. 两个 source 确为共同 ALL

FMW Definition1.1 明确允许平行边，值按所有 constraint-ID 的重数均匀计。Definition1.3 与 Theorem1.6 给共同域 `[m]→[k]`、m=4k、逐右标签恰4个原像、YES恰1、任意小先固定 NO 值。Appendix B 每原边复制 k0=ceil(4/ε) 条约束：失败旧标签对最多两条通过；两侧都在删去部分时同余 `2ℓ=KL−KR (mod k0)` 至多 gcd(2,k0)≤2 个解，故 ε/2+2/k0≤ε，偶数 k0 也无遗漏。完美旧标签配共同新坐标满足全部新约束。“同一 constraint graph”不能解释成未增加重数。

KS14 原 Conjecture2.5 另要 biregular，脚注明说当时不知道可否 WLOG；因此 FMW 源不能独自支付它。正规化引理本身又没有 NP-hard 源。当前 `source_ids` 同时保两者、`premises_mode:all` 正确。

## 3. 独立正规化的承重核算

令原未加权二部图有 E≥1 条带身份约束，删孤点后左右度为 d_u、d_v。每原点建其度数个 clones，左右各 E 个。每 e=(u,v) 的所有 clone 对各放原投影及权 1/(d_ud_v)，保留 e-ID；每 clone 加权度1，总权 E。

对任意固定 clone 标签，每个原顶点独立均匀抽一个 clone 的标签。原 e 的期望满足指标等于其 clone 对满足指标的平均，故原归一满足率的期望等于新加权满足率。因此新加权最优值≤原值；反向复制原最优标签得到≥，所以值精确相同。原 perfect 标签满足每一复制约束。这里每原点只抽一个标签，跨 incident 边共享该标签，故确为合法原策略。

取 S=Σ_e d_ud_v≤E³，D=ceil(S/(ηE))。每带 e-ID 的 clone 对有分数重数 x=D/(d_ud_v)，每个 clone 行/列和均为整数 D。取 floor 后，剩余整数度需求由分数余量给可行容量1二部流；整数流给每变量 floor/ceil，仍逐点度 D。各平行变量独立，不能把同端点不同投影合并。所得两侧各E点、全部度 D、总边数 DE。

固定任意 clone 标签 I∈{0,1}，整数化前后归一分数的差≤Σ|xhat−x|/(DE)≤S/(DE)≤η。此为每份标签逐点同时成立的确定性界，取最大后两值同样差≤η，无概率并集、无标签枚举。留下的边全是原类型，故 perfect YES 仍恰1、exact4仍逐边成立。

S≤E³、D≤E²/η+1、DE=O(E³/η)。有理数位长、流网络、输出全部显式边都可控；固定η才给此处多项式。没有把二进制η的 log(1/η) 当成显式展开的规模合同。选源 NO≤ζ/2、η=ζ/2，得到本条边所需 perfect exact4 / biregular / NO≤ζ。

## 4. typed 有序层化：两种均匀性及 soundness

设正规化源 `V→U`，V度b、U度a，按F的 constraint-ID 计。Q=TL+L−1。第l层点是 `(A,z)`，A⊆[Q]且|A|=l−1：A上U型，其他位置V型；允许重复原变量且各位置各自赋标签。点数和标签数分别为

`n_l=C(Q,l−1)|U|^(l−1)|V|^(Q−l+1)`，
`K_l=k^(l−1)m^(Q−l+1)`。

对l<l′，h=l′−l，从V位置取H（|H|=h），每j∈H独立抽当前V端点的一条 incident ID，换成其U端点。H及每个e_j均作为层间约束身份的一部分，身份不写入两个端点。投影对H逐坐标用π_e，其他恒等；目标每个标签的fiber恰4^h。

固定源层点出度 `C(Q−l+1,h)b^h`；固定目标层点入度 `C(l′−1,h)a^h`，均常数。于是均匀源点、均匀H、每位置均匀incident ID给均匀层间约束。源双正规又保证均匀V点加incident ID到达均匀U点，位置独立保证目标点均匀。约束测度的 `Pr[e_j=e]=1/(|V|b)=1/|F|` 与目标点测度的 `Pr[w=w0]=1/n_l′` 分别已付，不是任意图上的可互换约定。

若两个源标签在U位置不同，恒等坐标使它们永不碰撞；否则取一个不同V位置j，碰撞要求j∈H，故概率≤h/(Q−l+1)≤1/T。此为按incident ID的smoothness，不依赖同端点投影相同。

从第一层均匀全V tuple起，每次均匀剩余位置、均匀incident ID的链，每层边缘均匀；任意两层的H有同样h!次序，各ID tuple同概率，故两层联合恰是均匀层间约束。若s≥ceil(2/ρ)个层各取密度≥ρ集合，链命中次数X满足EX≥sρ≥2，`E C(X,2)≥((EX)^2−EX)/2≥s²ρ²/4`。对层对平均至少有一对的联合命中概率≥ρ²/2，强于KS14所需ρ²/4，weak density已付。

最关键的层间soundness：任意层对标签的整约束通过率设为p；在H中再均匀选distinguished j，整约束通过蕴含j处原约束通过。固定A,H,j、其他位置原变量及其他替换位置的ID，j处原ID仍均匀于F，因为原tuple是独立有放回抽样，没有添加“不同变量”条件。固定上下文时，源层j标签仅依赖V端点，目标层j标签仅依赖U端点；两端均看不到e_j-ID。它们就是合法原源策略，满足率≤val(source)，对上下文平均给p≤val(source)。同端点不同π_e仍逐ID测试，端点标签不能据ID改答。允许重复符号不损害独立性，反而避免了无碰撞条件化偏差。perfect标签逐位置复制则满足全部层约束。

## 5. KS14实际分析、三点互异与无循环参数

原KS14在l<l′时印 `d^(l−l′)`，Appendix A也印负的替换数；实际K_l/K_l′=4^(l′−l)，故h=l′−l、r_h=4^h才是正fiber。当前正式Boss5 done repair已经明确实施此最小局部符号修正，无须再新开任务。这个原文问题不能借负指数直接调用测试，也不推翻成熟解析结论。

固定目标δ，先取有理0<α<min(δ,1/2)、L=ceil(32α^−2)、噪声θ∈(0,1/2)。h只有1,…,L−1，r_h=4^h全是固定常数。逐h按KS14 §5选择ν_h、γ_h、τ_h、s_h；其η_h=2θ/r_h，reverse-hypercontractive下界 `(α/2)^(4/η_h)>0`，故Eq.(30)可先选足够小ν_h，使相应Gaussian下界仍严格正。Lemma5.14随后给正γ_h、τ_h，s_h有限。再取T≥max_h T_h，满足Eq.(30)–(32)、坏incident比例和影响比较。最后取正有理

`ζ < min_h α² τ_h² γ_h²/(2048 r_h)`，

再调用FMW源（ζ/2）与正规化（η=ζ/2）。KS14这些阈值独立于long-code维数；T虽影响Q与K_l，却不改变r_h，也不会反向影响此前解析常数。如此无源字母表循环；找到哪一层对后可按该h解码，不需要一份策略同时服务所有h。

每条π_e的每个fiber独立用D_(θ,r_h)：均匀X,Y，初置Z=−Y，以概率θ选一个坐标，把Y,Z该处同改为−X。完美标签的颜色为码字所选坐标。若标签坐标未改，Y、Z异色；若改了，两者均−X而与X异色，故完整二着色。

r_h≥4，每fiber至多改1坐标，至少另一个未改坐标仍Y=−Z，故y≠z；x来自另一层的另一块，自然与二者不同。没有退化边需要默删。最终相同三点超边可去重，但源ID不能去重。

独立集有权质量≥α时，heavy块取密度≥α/2。heavy块的总基础点质量≥α/2；至少αL/4个层有≥α/4比例heavy点，L的选择保证足够应用ρ=α/4的weak density，得到heavy到heavy的ID占比≥α²/64。对每个ID，独立集避开全部支撑等于该测试乘积期望为0；Lemma5.14逐π应用。对每个固定源层点，低于s_h的Fourier坐标集合未被打散概率≤s_h²/T；Lemma5.15给坏incident比例≤(s_h²/T)^(1/4)。层间双正规使该局部界按ID汇总为全体约束比例，T足够后至少α²/128的ID为heavy-good。

Eq.(33)给一公共坐标i*，两侧smoothed influence质量分别≥τ_h/2与其fiber中≥τ_h/(8r_h)。按每个顶点自己的smoothed coordinate influences归一抽标签，质量总和≤1/γ_h，故该ID满足概率≥τ_h²γ_h²/(16r_h)。函数及抽标签分布仅依赖顶点和当前层对h，不看incident ID。不同投影可有不同公共坐标，仍可按ID线性求期望，得到一份层对标签使满足率≥α²τ_h²γ_h²/(2048r_h)>ζ，矛盾。

这一步没有把“图中同端点一条π”的简写误读成必须合并投影，也没有把边多重数密度当作不同邻点密度。

## 6. 精确整数cloud与固定参数显式规模

第l层每个码字权 `w_x=2^(−K_l)/(L n_l)`，每层总权1/L。令Kmax=maxK_l、`B=L(∏_l n_l)2^Kmax`，每码字建 `Bw_x=(∏_{j≠l}n_j)2^(Kmax−K_l)` 个clones，均正整数，总数B。每原三点边展开为三云之间全部三元组。

任意clone独立集所占据的原顶点集合必独立，否则从各占据云任取一个已占clone就含完整边。因此clone独立集数/B≤所占原点的权；反向复制任何原独立集的完整云达到其权。最大无权独立集比例与原最大加权质量严格相等，无额外误差。原三点不同，三云互异，展开后仍每边恰3个不同点；每云同色复制保二着色。

固定δ后L、T、Q、源字母表与所有K_l都是常数；n_l为输入规模固定次幂。设正规化后点规模N、约束数F，多层点≤常数·N^Q，约束数≤常数·N^Q F^(L−1)，每π的测试支撑为常数大小，B≤常数·N^(QL)2^Kmax。完整三部展开即使用粗上界“原边数×B³”，仍为确定性多项式。常数很大不影响固定δ合同；没有声称δ随输入改变的统一多项式。

结论输出有限无权3-uniform超图：YES恰2-colorable；NO最大独立集比例<α<δ。目标整句所需的非平凡固定阈值范围已完整支付；较大δ沿用同一更强NO输出，按当前目标/原论文惯例表述。不附加simple源、常数最大度或排程模型。

## 7. 旧资产处置、可清pending及保留边界

旧abad收据共有11个assets，本次supersession逐项覆盖11项。8个非边资产retained，均在新receipt按旧SHA列入且当前字节匹配；旧超图v3边replaced到本条v4完整ALL边及当前proof，二者都在新receipt。旧八色边replaced到现行canonical共享边及review；旧三色direct JSON retired的理由是其数学由现行exact4→八色→三色复合与保留proof承载。这后两项是本轮核出的处置完整性，不是本worker对GS20整链另作认证。没有用删除独有超图证明来“清理”旧资产。

在final bindings所记快照，允许Root采用本审查清：

- pending `edge_ids` 中且仅其中的 `exact-four-to-one-v4-and-biregularization-to-three-uniform-independent-set-9fa9ce8a7e4a75ec`。
- pending `object_ids` 中超图目标 `M-9f8033b6e1a4485b97636171b09f8218` 对应的本次3D义务。
- 源 `M-ab4a576ed0be482b89d4a646ffc102b9` 的当前合同及本条超图应用已经审清；其整个pending对象若还承载其他图应用比较，应由Root合并那些实际审查再清。本worker不替它们全局背书。

必须继续保留：所有其他pending edge/object（明确包括三色目标 `M-d007675a9ed240898c90e831af80b092`：本worker未实读两条当前共享图边及current graph endpoints完整记录），以及整个`archives/unrelated-machines` archive scope，直到其其他义务独立付清。当前规范化lemma不在pending也不需要新增pending。此3D结论不对外部图事实作UM/SPE迁移。

数学边界仍须随关系保留：source的量词是∀固定ε∃常数r，不支付MZ实际R的幂次soundness；MZ近完美/一般投影也不能代替perfect/exact4。保留source IDs的ALL、约束重数测度、端点不见ID、有限h先定解析常数、显式展开依赖固定δ以及无常数度承诺。它们在当前证明中均已支付或准确限域，不是未完repair。

当前没有新发现的承重错误、未付lemma、待派repair或owner冲突。本轮不申请任何原任务、不抢写Boss5资产。历史负指数问题的最小修法已在当前Boss5正式done包中存在；没有新增正式repair的必要。

## 8. 末次current确认

本审查生成时再次定向读取三个对象、任务、边、收据、全部本范围evidence和receipt assets。三端registration pins与当前边/任务一致；当前边仍在registry canonical清单；integration的edge/receipt native pins与所审文件一致；当前及retained资产的SHA全部匹配。父Boss工作期间integration/registry整体文件有正常更新，本审查只以末次`current-bindings.json`快照为准，未把早先整体SHA冒充最终状态。所审数学资产从实际读取到末次核验未发生版本变化；本输出不清写任何pending。
