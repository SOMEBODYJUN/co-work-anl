"""Build self-contained semantic resources; never execute the primary auditors."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[3]
E = ROOT / 'tools/evidence/independent-security-and-waterfill-audit-primary'
W = ROOT / 'cleanup/workspaces/Boss4/r3-independent-security-and-waterfill-audit-primary-next'
W.mkdir(parents=True, exist_ok=True)
sources = json.loads((E / 'source-manifest.json').read_text())
deps = json.loads((E / 'dependency-manifest.json').read_text())
byid = {x['id']: x for x in sources + deps}

def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def document(path, ident, title, summary, ids, body):
    refs = [f"source:{s['commit']}:{s['path']}" for i in ids for s in byid[i]['sources']]
    head = ['---', 'id: ' + json.dumps(ident), 'kind: "resource"', 'type_tag: "资料"',
            'title: ' + json.dumps(title, ensure_ascii=False),
            'status: "full-source-read-exact-scope-and-runtime-boundaries-preserved"',
            'summary: ' + json.dumps(summary, ensure_ascii=False), 'source_refs:']
    head += ['  - ' + json.dumps(ref) for ref in refs]
    text = '\n'.join(head) + '\n---\n\n' + body.strip() + '\n'
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    return {'path': path, 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

individual = r'''
# 个体安全和全树流独立审计的完整合同

本页承接主源263d8b8cde0651ffc00a（individual_security_independent.py，17216B/393行，SHA895d1cfd…）与0494c0e5b61617175486（lift_and_flow_independent.py，9241B/209行，SHA210a36cf…）。两冻结refs同字节，全部源码、真实入口、默认输入、生成文本及未使用变量均已实际读完；[逐源原件](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/source-manifest.json)保完整commit/path/SHA。两程序只导入标准库，未导入作者模型、求解器、候选验证器、优化器或策略文件。

## 模型与个体审计的真实输入域

共同有限目录、单位提供者顺序观察全部有序历史，单位客户在最终覆盖者间均分。整数重数是不同单位客户的压缩表示，不是有权玩家。此具体输入审计要求正整数人数、不同主题名、正整数重数、非空且无重复的兴趣集合、兴趣索引和全部策略动作精确int合法、不同压缩兴趣类型；还要求各主题的客户覆盖两两不同。它因此不是允许无兴趣客户/重复覆盖标签的全部CAG输入的通用schema验证器。

每个长度0至n−1的有序历史恰有一个动作，重复历史、缺失历史和非法动作拒绝。terminal(h)每一步在改变后的有序历史查同一完整策略，偏离后没有冻结后继。遍历m^n终局，逐份核支付和等于覆盖并求OPT；遍历全部决策节点和全部m动作核规定行动最优，同时保全部交叉查询矩阵。所有节点的u_minus_value都相对**原根n人静态安全值**，不是残余背景子局的新安全值。

默认输入是history/source/notes/customer_attraction/individual_security_2026-10-10/compressed_34.json，源1384d853217106a4f948，SHA d0dbcd994e1ac697669599638e38c6a3d8dcd50cd32bca5d3710cb4533015b68；真实全部字段和43动作已经读完，[输入原件](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/dependency-manifest.json)独立保全。六主题X0/X1/X2/Y0/Y1/Y2编号0–5，客户mask与重数为

| mask | 重数 | mask | 重数 | mask | 重数 |
| --- | ---: | --- | ---: | --- | ---: |
| 4 | 1 | 27 | 4 | 29 | 3 |
| 30 | 3 | 31 | 2 | 32 | 1 |
| 43 | 3 | 45 | 3 | 46 | 3 |
| 51 | 3 | 53 | 3 | 54 | 3 |
| 59 | 2 | | | | |

根选0；第二人选与首动作相反组的最小标签；第三人选第二动作所属三标签组中此前未出现的最小标签。这为重复和离轨历史都给完整动作。实际(0,3,4)，u=(29/3,67/6,67/6)，W32/OPT34。43历史、258含自身比较、215非指定偏离中144严格亏损/71平局，216终局、15个严格正主题对称差全部核对。它只否定逐人保底；W−3v=213/82>0、W−OPT/2=15>0，未否定聚合安全或half。

## 匹配静态安全证书、唯一性与真实预算

对合法n−1主题静态竞争元组B（允许重复），定义f_B(a)=Σ_(T∋a)w_T/[1+#_TB]，v=max_p min_B E_p f_B(a)。程序枚举全部无序重数组合作为等效静态背景，原始p和合法对偶Q均精确非负/归一化且Q背景不重复；计算lower=min_B E_p f，upper=max_a E_Q f并核相等，不调用LP近似。

本输入p=(10,10,21,10,10,21)/82，对偶在01、02、12、34、35、45上的概率为(23,9,9,23,9,9)/82。21无序背景等效36有序背景，126纯查询给lower=upper=v=2411/246，因此u1−v=−11/82。对偶正支撑约束必须对任意最优p取等，正对偶slack查询必须零权；限制到其余查询后，归一化和正支撑行精确消元rank6，未缩放正支撑矩阵det=−12055/48，所以p唯一。rank和det均用Fraction高斯消元，不是数值秩。

每个节点h和每个实际首次偏离b得到真实完整终局，删除当前人后为B_h(b)。设

$$D_h=sum_a p_a f_{B_h(a)}(a),quad
C_h=sum_{a,b}p_ap_b f_{B_h(b)}(a),quad e_h=u_h-D_hge0,quadkappa_h=D_h-C_h.$$

全部43节点的6×6矩阵即1548条背景查询实际计算；实际路径总预算为GB=W−Σ_i C_i=Σ_i(e_i+κ_i)，程序独立核等式。

| 实际历史 | D | C | e | κ |
| --- | ---: | ---: | ---: | ---: |
| 空 | 29/3 | 2411/246 | 0 | −11/82 |
| 0 | 5311/492 | 1252/123 | 61/164 | 101/164 |
| 0,3 | 2597/246 | 2597/246 | 25/41 | 0 |

故Σe=161/164、Σκ=79/164、GB=60/41>0；负根债由真实后继补偿，不能把逐人失败改写为全局预算失败。normalized_individual_gap=11/2788只是负最小个体差除34客户。输入compression字段的fixed_source_p_strict_gap=13/681、HiGHS最优/零mip_gap/浮点dual_bound≈34是历史MILP提议元数据；本审计不运行MILP，也不据这些字段证明全局最小客户数或新颖性。

## 个体程序的输出和模板边界

argparse在模块顶层执行。可给位置输入路径与--output-dir；新目录必须不存在，创建发生在验证输入之前。完整results.json在报告模板和最终primary_unique断言之前写出，故失败后目录/JSON存在本身不等于成功；没有output-dir时只打印summary。报告硬编码三位收益、W−3v、“15对/六主题”等措辞，并无对应一般n/m模板；rank函数支持一般矩阵，不能据此把报告宣布为任意人数入口。

尤其“首位安全失败、聚合/half/GB严格为正”的报告文字不是逐项assert。规范34客户输出的精确数值确实支持这些文字，本页已分别核值；不能把任意合法输入生成同样模板当作这些结论已由程序强制。源码末尾只另assert primary_unique；若给其他域可能报错或产生不合域报告。源代码不改，本轮不另制造玩具输入扩大测试次数。

## 尾部提升的有限组合回归及一般条件

lift脚本没有外部输入，客户向量、形式策略和q全部内嵌。它对n=4至10、d=0至n、b=0至n−4的252个参数三元组，逐四元**索引**子集I枚举j=|I∩[d]|，核

$$sum_{|I|=4}§frac{j}{b+j}
=sum_{j=1}^4 {dchoose j}{n-dchoose4-j}§frac{j}{b+j},$$

零分子项为零；d>0时核其≥C(n−1,3)/(b+1)。解析理由是选一名覆盖客户的索引，包含它的C(n−1,3)个I都满足j≥1且j/(b+j)≥1/(b+1)；有限252网格本身不是一般定理。

随后n=4至100的97次系数检查用β=1499/750，确认(n−4)(1/2−β/4)≥0及βn/4+(n−4)(1/2−β/4)=n/2−1/750。真正背景提升还须假定所有合法真实整数背景和完整尾部SPE满足F_k(b)≤β_k V，0≤β_k≤k/2。对最优n主题的k索引子集求和给

$$OPT_nle(§beta_kn/k)V+sum_x b_x/(b_x+1).$$

真实节点改选最大主题K得每位u_i≥K/n，故V≤W−(n−k)K/n，K≤W；整数背景使Σb/(b+1)≤Σb/2≤(n−k)K/2。于是条件消元得到OPT_n≤(n/2−k/2+β_k)W。本程序没有证明背景利润前提；已读现行[背景提升推论快照](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/context/archives/customer-attraction/state/推论/尾部利润界向总人数提升--推论.md)给其现有依赖。k4系数在n6为2249/750>2，不闭合六人half；五人零背景根界不能替换背景版前提，(0,1)实背景不能直接使用b/(b+1)≤b/2。

## 全树势、独立前缀流与不能丢的余项

给定任意完整形式策略σ、非负客户类型质量w和分布q，allocated逐客户按覆盖者位置均分并算Φ(z)=Σ_Tw_T H_load(T)，核Σu=W。令Z_k前k动作独立抽q、余下仍按改变历史上的σ执行，Ψ=E W(Z_n)，G_k=E_(h∼q^(k−1),a∼q)[u_mover(z_h)−u_mover(z_ha)]。删除原玩家位置i，定义Δ_(k,i)=EΦ(Z_(k−1)\i)−EΦ(Z_k\i)。玩家收益等于删除自身的势差；逐客户d(H_d−H_(d−1))=1又给W(z)=nΦ(z)−Σ_iΦ(z\i)，故望远镜为

$$W-Psi=nsum_kG_k+sum_kleft[nDelta_{k,k}-sum_iDelta_{k,i}
ight].$$

源码对每个真实偏离与全部iid终局核这些身份，也报告另一单位流余项W−Ψ−ΣG。身份对任意形式策略成立；只有完整SPE才令每条Γ及G非负。定义α_a=E_(B∼q^(n−1))f_B(a)，E_a=Ψ−nα_a；始终Σq_aE_a=0，不等于每条E_a非负。前三均匀实例E=0，最后非均匀n4例明确不是静态Nash或SPE认证。

原36客户形式策略仍为上文X/Y规则，客户跨组二标签各1、两X两Y四标签各3。W34、Ψ97/3、G=(0,1/2,31/18)，单位余项−5/9、倍n删除余项−5。完整258IC均非负，W−Ψ=5/3却正；失败的是预先固定平均流的支付，不是该例福利桥。

深度分离客户向量为{4:11988,25:17316,26:12481,29:7312,34:19357,37:12481}，总80935。G=(0,0,607489/216)≥0，E=0，但W−Ψ=−472195/36；完整Γ有57负行，根改1/2分别获利2827/6216。它分离所有非负深度平均权模板，不是SPE。

节点平均分离的全部15个正质量为

| mask | 重数 | mask | 重数 | mask | 重数 |
| --- | ---: | --- | ---: | --- | ---: |
| 2 | 4452686231690 | 4 | 6839265002855 | 6 | 12413611540204 |
| 18 | 2005873636422 | 21 | 55545726786729 | 26 | 11682751932414 |
| 30 | 144170590014021 | 31 | 453930615027141 | 32 | 252949420150890 |
| 33 | 5430105756036 | 41 | 4622970055818 | 43 | 77652459511935 |
| 45 | 70066680831603 | 49 | 29955175098349 | 51 | 46800753774087 |

总1178518685350194；43节点的M_h=Σq_aΓ_(h,a)最小0（9零/34正）、E=0，W−Ψ=−1085816540911589/12，却有59负的完整Γ行。若c−ψ是非负M_h、E及客户余项的组合，和该w内积应非负而实际负，矛盾。因此它排除节点内部先按此q平均的模板，不排除保留每条真实偏离的独立乘子，也不是half或完整SPE反例。

额外n4例用mask质量{1:2,2:3,3:5}、q=(1/3,2/3)、策略a(h)=(Σ_(j从1编号)j h_j+|h|) mod2，实际(0,1,0,1)，W10、Ψ775/81，G=(0,35/54,−7/27,−25/162)，两余项16/81、−41/81；15节点有6负Γ且M最小−14/9，E=(−20/81,10/81)。它检验身份不依赖三人/均匀分布，不声称一般n4策略合格。

## 本批实际运行与旧证据身份

两旧JSON分别166047B、51188B，原始全文字段/结构已读并保，前者只绑定输入SHA、后者含全节点数字但都无当前代码SHA运行绑定；本批在真实依赖齐全后各新增一次普通未优化、隔离标准库运行，exit0，分别0.116/0.617秒。个体完整新results与旧JSON除绝对输入路径外全部字段相同；流的新CLI摘要每个字段与旧完整报告对应部分相同。

流源码的output局部变量含完整全节点/删除矩阵/非均匀结果，但main**没有写出或打印该变量**，只打印选择字段。OUT路径变量未使用。故本次新CLI没有新生成51188B全结果；该旧完整报告仍作为历史证据，不反向伪造为本次原CLI输出。全部运行、stderr和比较见[运行记录](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/runs/new-run-summary.json)与[逐字段比较](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/new-old-comparison.json)。assert要求optimize0，本轮-I/-B并核解释器optimize0；无Git、网络、身份、公屏或凭据操作。

本批不再跑360候选的发现MILP、不额外done相关输入/旧报告、不认证最小性/外审/新颖性。当前六人任意完整纯SPE的half仍开放；逐人反例、固定平均流模板分离和真实iid福利反例是不同对象。
'''

selected = r'''
# 指定完整策略锥与全SPE正预算的原程序核验

主源cb88477459c73d47fafe（selected_security_budgets.py，3890B/72行，SHAfa481f8e…）及c0b20181754a4455d3cb（selected_security_cones.py，3344B/65行，SHA49cb05ae…）全部全文实读；两冻结refs同字节。[源原件与定位](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/source-manifest.json)保持不改。所有真实JSON/政策/Q/字段已读，数值向量全部原字节保全、全结构解析并定义级Fraction核验；319884B锥包的每个数字不冒称人工逐字读，也不额外完成这些相关源。

## 五个固定游戏：有序完整SPE菜单的精确递归

有限共同目录，正人数单位提供者，单位客户整数重数，全部有序历史。utility(z,i)直接按覆盖者均分，query(a,B)用1+竞争负载，coverage(z)取覆盖客户重数。可重复主题、离轨历史及各自平局全部保留。程序不导入生成器/求解器，而以ordered tuple h为lru_cache键，完全不做计数状态压缩。

叶菜单M(z)={z}。给定h，各行动孩子菜单已归纳得到，设

$$L(h)=max_bmin_{zin M(hb)}u_{|h|+1}(z),qquad
M(h)=§bigcup_b{zin M(hb):u_{|h|+1}(z)ge L(h)}.$$

必要性来自任意离轨孩子的收益至少其菜单最小值；充分性是为每个未选行动独立选择达到最小值的合法孩子策略。孩子历史子树彼此不交，所以可拼成一份完整纯SPE。不同有序路径即使计数相同仍分别保留，菜单不是全部完整策略的计数，也不是只沿在轨最优。

固定根可实现路径z和位置i，自己选原z_i的孩子由该路径固定；改选b≠z_i可在M(z_<i,b)中任取令当前人收益≤u_i(z)的完整续局。设Cbranch(z,i)=Σ_a p_a f_(z删除i)(a)，则每个备选b分别最大化Cbranch，再乘p_b加总。不同实际位置的首次偏离子树按首次离轨位置分离，可同时独立拼接，故这给该z上最大Σ_iC_i，遍历全部z即给所有完整SPE的最大ΣC−W。

程序还从输入重建一棵完整达到策略，检查全部有序历史真实偏离，并核其ΣC−W确等上述最大值。静态p/Q通过所有m^(n−1)合法背景的floor=min_B E_p f与cap=max_a E_Q f相等来确认证据；真实输入Q背景/动作合法性另在本批全字段检查中明确核过，不把原程序未全面做的schema检查补称其源码已有。

## 全部五输入与结果：负violation恰是正GB

BASE固定repo/evidence/certificates/customer_attraction/selected_security_budgets，main无argparse，依次只读original36、individual34、individual360、root_tax_failure、global_decorrelation_failure五JSON并打印报告，不写文件。verify(path)是函数入口。输入总807?字节不是数学断言；精确逐件字节/SHA见[输入清单](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/dependency-manifest.json)。五游戏/全部动作表/全部p与Q和历史作者字段均实际读完。

| 固定游戏 | n/m/客户 | 完整有序路径数 | 规定策略含自身IC | 最小GB=W−ΣC | 静态v |
| --- | --- | ---: | ---: | ---: | ---: |
| original36 | 3/6/36 | 48 | 258 | 17/6 | 10 |
| individual34 | 3/6/34 | 40 | 258 | 60/41 | 2411/246 |
| individual360 | 3/6/360 | 23 | 258 | 55088965/3710088 | 93177/908 |
| root_tax_failure | 4/6/61 | 102 | 1554 | 3/2 | 9 |
| global_decorrelation_failure | 4/6/89 | 6 | 1554 | 70429743611/10570351740 | 508643/26546 |

五项严格正。源字段GB_violation_sumC_minus_W记录最大ΣC−W，恰为本表负值；failure等文件名不是GB失败证明。其量词为**每个固定客户游戏、一个指定精确安全最优p、所有完整纯SPE**。没有量化该游戏其他安全最优p，更不量化任意客户游戏/六人。现行符号纠错正文和gb-sign-correction已实际比较，维持正确方向；旧原件/旧处置均不覆盖。

规范34客户个体输入与预算达界输入game和security完全相同，43动作中有12个离轨差别；原政策与另一个达界政策各自保全，不能只凭同根叶/同GB替换。360固定游戏的预算达到策略根(0,4,3)，其全SPE最小GB=55088965/3710088；早期特定(0,3,4)策略的GB=65339377/3710088是另一个更大正值，不是数值矛盾。61客户预算策略根(0,0,0,4)，锥包则(0,0,0,5)；89客户预算根(5,0,0,2)，锥包根(2,5,0,0)。相关游戏、形式策略与顺序身份不能合并。

程序只依实际使用的game、security primary/dual、possible_ordered_SPE_paths、violation及strategy动作核上述项目；输入额外顶层players/topics、root_SPE_count_menus、W/outcome/utilities/sum_C和部分security value标签不都是单独assert目标。原始元数据全部保留，不能把PASS说成每个作者字段已被原码逐项认证。该审计不是一般坏JSON验证器：有些合法动作/背景类型约束在原码只假定，实际冻结输入已另查精确int/范围，不扩通用schema能力。

## 三棵固定形式策略：任意非负客户质量锥

另一程序只读selected_security_cones.json（源7a48fb9d35ad4f79eb56，319884B，SHA48eba055b3f439e21d95d7f96b7f179f2cd907337ca42d57ade7b0f931327a70），没有优化器或生成器。对每case固定n,m与全部有序历史策略σ，非空客户兴趣T遍历1至2^m−1。定义真实完成终局z_h、z_ha和

$$Gamma_{h,a;T}=§frac{mathbf1_{sigma(h)in T}}{#_Tz_h}
-§frac{mathbf1_{ain T}}{#_Tz_{ha}},qquad
mathcal K_sigma={wge0:Gamma wge0}.$$

零分子为零；非零时分母正。每条Γ真实重算后按完全相等Fraction向量去重；不冻结续局、不用计数策略替代原σ。policy全历史/重复键和动作范围均核；本旧程序的范围比较不是后来21锥脚本的精确int断言，实际输入的int身份已另检查，二者版本不能混写。

逐证书目标d_i,T是实际玩家i的最终份额，aggregate目标是覆盖c_T/n；索引0从第一人开始。每个合法静态背景元组B长n−1、可重复，f_B(a)_T=1_(a∈T)/(1+#_TB)。证书提供一个全查询共用概率Q和按查询a分的非负乘子λ_a，程序要求λ行是重建的真实Γ行，并核所有类型余项

$$r_a=d-mathbb E_Q f_B(a)-Gamma^{mathsf T}lambda_age0.$$

对任意w∈Kσ内积，d·w≥E_Q f_B(a)·w对全部查询成立。再对任意混合p平均，min_B E_p f_B(a)≤E_Q E_p f≤d·w，取max_p得逐人u_i≥v_n或聚合W≥n v_n。固定Q/λ适用于整个锥，不是单点浮点实验；有理/整数质量可清分母展开单位客户，空兴趣客户不贡献可补回。这里不是有权提供者或顺序混合策略。

| 固定σ/name | n/m | 根叶 | 目标证书 | 历史/Γ比较构造 | λ列表项 |
| --- | --- | --- | --- | --- | ---: |
| aggregate_theta_failure | 3/6 | 0,3,4 | 第二人、第三人、aggregate | 43/258 | 80 |
| root_tax_failure | 4/6 | 0,0,0,5 | 每位及aggregate | 259/1554 | 33 |
| global_decorrelation_failure | 4/6 | 2,5,0,0 | 每位及aggregate | 259/1554 | 38 |

共3棵树、561历史、3366含自身Γ构造，复用于13证书；每证书6×63=378坐标，合4914。报告重复列出各证书的树规模不能再当13棵新树；nonzero_Gamma_multipliers源码按列表条目计数151，不仅凭名字断言每项严格正或去重。minimum_residual在本旧程序从全部实际余项取min，而非新21锥版本的零初值；实际13项均0。

完整Q去向如下。原三人第二人Q=(0,4)、第三人Q=(0,3)均为纯背景；aggregate在01、02、03、04、05、34、35上的概率依次1982/6471、1442/6471、1/3、565/6471、5/719、55/2157、115/6471。四人root-tax前三位Q=(0,0,5)，末位Q=(0,0,0)，aggregate为后两背景按3/4、1/4混合。global-decorrelation四位分别Q=(0,0,5)、(0,0,2)、(0,2,5)、(0,2,5)，aggregate在(0,0,2)取1/4、(0,2,5)取3/4。全部Q/151λ真实行与系数保原件和[全字段结构](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/input-structure-and-readiness.json)。原三人第一位没有对应全锥逐人证书，恰与34客户沿同形式策略的逐人反例相容。

这些正锥结论量化任意**使该固定σ为SPE**的非负客户质量和全部查询混合，并不量化任意σ。五固定游戏全SPE正GB与三固定σ全客户锥是交叉的不同量词；不能把其中一个当另一个的证明，更不能并作任意六人half。

## CLI身份、异常与本次精确绑定

selected-cones以第一个sys.argv位置参数为JSON，否则用repo默认路径，直接__main__打印完整报告；没有--output解析或自动保存。字节/环境及真实输入先齐全后，本批budget原CLI运行一次exit0/1.119秒，完整报告与旧1825B JSON全部相同。

cone首条命令直接执行同文件为__main__、无位置参数，exit0/0.568秒，但保存stdout/stderr均空；原空捕获保留，**不称额外PASS**。源码guard内是print(json.dumps(verify(path)))，所以按入口语义应进入verify，既不是import-only，也不是只加载定义；首轮无函数trace，无法单独确认空输出原因或给它补造报告。仅为此真实异常做一次同__main__、显式同一输入路径、PIPE捕获接续，exit0/0.501秒得到6686B/4914坐标，与旧报告全部字段相同。

准确统计为2次cone CLI调用，按静态入口应有2次verify调用，但只有1份报告可核的主体完成；首轮主体执行属于源码入口推断，不独立算数学证据，也不加倍样本。第二条是显式参数的相同主入口重跑，不是新算法/独立实现。两条原始命令、输入/代码SHA、首空记录及接续报告见[运行身份审查](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/run-status-assessment.json)。全部用-I/-B普通未优化解释器，assert有效；无Git、网络、账号、公屏或凭据操作。

旧6686B/1825B报告没有当时审计代码SHA绑定，本次给当前主源补真实绑定；不反向改写其历史身份，不覆盖旧页“当时clone无活动入口”的准确当时记录。已存在完整冻结源可读是现在事实，与旧缺入口历史并存。此批不执行发现生成器，不额外done相关12源，不作阶段三导图或六人目标完成声明。
'''
selected = selected.replace('输入总807?字节不是数学断言；', '')

waterfill = r'''
# 分数尾水位审计的有理停点和命令行边界

主源30f18dd774474c944e78，tests/audits/customer_attraction_waterfill.py，7112B/160行，SHA e563e9c1a50150216abeb3c00ec6d7b731fdb607e4e6e25e3404e2603b46f491，两冻结refs同字节。全部源码和16个真实有理fixture/无理分支实际读完，[主源清单及原件](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/source-manifest.json)不改。它仅导入标准库，没有作者模型、SPE求解器、优化器或代数根库。

## 静态输入、量和共同池

这是给定终局的辅助负载审计，**不是加权提供者SPE结论**。有限客户全集N、背景b_x≥0、保留单位根A、尾部主题S_j、阈值t≥0，尾质量w_j从1降至[0,1]。当前证明合同取整数背景，实际fixture也全是整数；Python函数把b与t转Fraction、只检查非负，不据此宣布全部实背景/输入schema均已认证。root/tails应在universe内，函数不提供完整子集类型验证。

令a_x=1_A(x)、c_x(w)=Σ_jw_j1_(x∈S_j)、L_x=b_x+a_x+c_x。单位尾密度U_j=Σ_(x∈S_j)1/L_x，实际尾利润w_jU_j；根R=Σ_(x∈A)1/L_x，背景利润B=Σ_x b_x/L_x，尾总利润V=Σ_x c_x/L_x，M=Σ_jw_j。被覆盖支撑保存，零权尾可没有有限unit值，程序输出null且不把密度当利润。

初态全1的低尾缺口D=Σ_j(t−U_j(1))_+。Q_T(w)=Σ_(x∈T)1/(b_x+1+c_x)，表示替换旧根；J_T(w)=Σ_(x∈T)1/(b_x+1+a_x+c_x)，表示保留旧根再插入单位查询。所有查询使用**同一w**和同一全客户池H=Q_N(w)−Q_N(1)，不是每条查询再领一份信用D。

## 单遍过程、端点与解析理由

按尾下标各处理一次。当前U_j≥t则不变；否则先试把w_j置零。若不会删除最后覆盖，且零端点U_j≤t，就置零；否则从fixture stops[j]取一个0<ρ<1的**已给有理候选**，精确核U_j=t。没有通用根搜索器；缺候选会失败，不自动求有理/代数根。非空主题U_j随自身正权严格递减，所以精确等阈值候选唯一；有私有客户时自身权趋0使U_j趋∞，必须在正权先停。

以后其他权下降只会提高已处理尾密度；初始高尾保1，所有最终正权尾过线、支撑不变。一次自身s→s'的逐客户增量是

$$F(z)=1/(z+s')-1/(z+s)=(s-s')/[(z+s')(z+s)].$$

F随非负其他负载z非增，Q用的其他负载比U_j至少多1−a_x≥0；因此本步ΔH≤ΔU_j≤(t−U_j(1))_+。本程序逐步累积E=ΣΔU_j，精确核H≤E≤D。对全部T⊆N枚举，验证0≤ΔJ_T≤ΔQ_T≤H≤E≤D；Q_A=R还给根返还Γ=R(w)−R(1)≥0。解析一般构造见已读[共同信用引理快照](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/context/archives/customer-attraction/state/引理/分数尾水位的共同查询信用与利润守恒--引理.md)，有限fixture不替代证明。

逐覆盖客户的根/背景/尾利润和恒为1，故程序另核

$$V(w)=V(1)-Gamma-[B(w)-B(1)]ge tM,quad
Gamma+[B(w)-B(1)]+tMle V(1).$$

背景返还和根返还已从同一尾利润扣除；不保留旧尾利润后再免费加两份返还。它是同叶代数，不自动保全原完整策略的根/离轨IC，不能对辅助分数尾直接调用单位玩家人数归纳。

## 全部16个有理fixture的实际输入

下表除标明外b=0，o是只用于补全集的outside客户，方括号保尾顺序。stops只在正部分停点需要。Q/J均枚举全集全部子集。

| 名称 | N；A；有序尾 | t / 给定部分停点 | 最终w / D,E,H |
| --- | --- | --- | --- |
| zero_threshold_unchanged | {x,z}；{x}；[{x}] | 0 | (1) / 0,0,0 |
| unit_credit_constant_equality | {x}；{x}；[{x}] | 3/4；ρ0=1/3 | (1/3) / 1/4,1/4,1/4 |
| sole_tail_private_survives | {x,o}；空；[{x}] | 2；ρ0=1/2 | (1/2) / 1,1,1/6 |
| root_shared_zero_below_threshold | {x}；{x}；[{x}] | 2 | (0) / 3/2,1/2,1/2 |
| root_shared_zero_exact_threshold | {x}；{x}；[{x}] | 1 | (0) / 1/2,1/2,1/2 |
| initial_high_retained | {x,y}；{x}；[{x},{x,y}] | 1/2 | (0,1) / 1/6,1/6,1/6 |
| two_low_second_becomes_high | {x}；{x}；[{x},{x}] | 1/2 | (0,1) / 1/3,1/6,1/6 |
| empty_tail_removed | 空；空；[空] | 1 | (0) / 1,0,0 |
| mixed_private_partial | {x,y}；{x}；[{x,y}] | 8/3；ρ0=1/2 | (1/2) / 7/6,7/6,1/3 |
| repeated_tail_partial | {x}；{x}；[{x},{x}] | 2/5；ρ0=1/2 | (1/2,1) / 2/15,1/15,1/15 |
| three_low_sequential_zero | {x}；{x}；[{x},{x},{x}] | 1/2 | (0,0,1) / 3/4,1/4,1/4 |
| no_tails | {x,o}；{x}；[] | 3 | () / 0,0,0 |
| old_background_return_k_1 | {x,z}；{z}；[{x}]；b_x=1 | 1 | (0) / 1/2,1/2,1/6 |
| old_background_return_k_2 | 同上；b_x=2 | 1/2 | (0) / 1/6,1/6,1/12 |
| old_background_return_k_7 | 同上；b_x=7 | 1/7 | (0) / 1/56,1/56,1/72 |
| old_background_return_k_100 | 同上；b_x=100 | 1/100 | (0) / 1/10100,1/10100,1/10302 |

16例共49个子集，每个同时核Q与J（不是49份独立一般证明）。three_low的两步own增量1/12、1/6共E1/4；重复尾的正停点后另一尾也升至阈值；空尾可删、私有客户尾正停、t0保持全1、无尾时空质量均逐分支检查。完整结果另保每步endpoint、unit_before/after、own_increment、positive_mass及根/背景/尾利润。

unit_credit例H=Γ=D=1/4，证明自由阈值合同的信用常数1不可降低，不是阈值取真正安全值的反例。背景族对任意整数k≥1解析得D=1/[k(k+1)]、ΔB=1/(k+1)=kD、H=1/[(k+1)(k+2)]，所以背景返还没有统一常数倍D上界；程序只回归k=1,2,7,100，任意k结论由上述公式证明。

## 无理停点与严格有理夹逼

另一个例A={x}、尾{x,y}、b0、t2给U(ρ)=1/(1+ρ)+1/ρ=2，即2ρ²=1，唯一正根ρ=1/√2。程序从[0,1]开始100次严格有理二分，按U(mid)>2更新lower，否则upper；核0<lo<hi<1、U(lo)>2>U(hi)、lo²<1/2<hi²及宽2^−100。

实际区间为

$$lo=896364335596578238699711011639/1267650600228229401496703205376,$$
$$hi=112045541949572279837463876455/158456325028528675187087900672.$$

这里D=1/2，全客户共同增益H(ρ)=2/(1+ρ)−1。核0<H(hi)<H(lo)<1/2，H(lo)=371286264631651162796992193737/2164014935824807640196414217015；两个端点都另核根1/(1+ρ)加加权尾ρ/(1+ρ)+1恒为2。没有把浮点残差当精确根，没有给无理根有理输出或位多项式算法保证。

## 入口、既有精确复用与可信策略边界

16例、100次二分、argparse及打印全部在模块顶层，导入该文件也会执行这些检查并消费命令行；它不是无副作用库。只支持--output，可建父目录、以x拒覆盖；文件内保完整16例/无理report，stdout只打印16/49、两query模型、宽度和k100倍数的摘要。父目录/文件存在及退出0应结合普通assert解释器和实际报告，不能单独当数学证明。

本源码e563…与已有fractional-load-boundaries/source-manifest精确相同，replay.py全文已读：先核所有原文件SHA，再在临时镜像执行该标准库审计，所有成功后才复制完整报告。旧replay-summary为passed且16/49，完整replay-waterfill与原冻结10992B JSON全部字段相同。本批准确复用这次同SHA成功，**水位新增运行0次**，不为同一有限网格凑次数；原输入/程序/报告都保全。[旧证据与依赖清单](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/dependency-manifest.json)和[新旧精确比较](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/new-old-comparison.json)分清旧重放与本批新四程序证据。

现共同信用引理另记录高尾保1的IC翻转、允许高尾一起缩的统一收缩修复、变分总质量及全树角色税；本水位脚本没有核这些后续完整策略命题。静态同叶构造不自动产生辅助加权SPE，不证明跨互斥分支总信用，不关闭任意六人half。旧页当时活动路径未具备与现在有冻结源码可读分别保留；没有外审/新颖性认证或阶段三关系导入。
'''

def exact_formulas(body, formulas):
    pattern = re.escape('$$') + '.*?' + re.escape('$$')
    assert len(re.findall(pattern, body, re.S)) == len(formulas)
    values = iter(formulas)
    return re.sub(pattern, lambda match: '$$' + next(values).replace('§', chr(92)) + '$$', body, flags=re.S)

# The section marker is an encoding placeholder, replaced with a literal TeX
# backslash only inside Python. This avoids host-language string escapes.
individual = exact_formulas(individual, [
    r'D_h=§sum_a p_a f_{B_h(a)}(a),§quad C_h=§sum_{a,b}p_ap_b f_{B_h(b)}(a),§quad e_h=u_h-D_h§ge0,§quad§kappa_h=D_h-C_h.',
    r'§sum_{|I|=4}§frac{j}{b+j}=§sum_{j=1}^4 {d§choose j}{n-d§choose4-j}§frac{j}{b+j},',
    r'OPT_n§le(§beta_kn/k)V+§sum_x b_x/(b_x+1).',
    r'W-§Psi=n§sum_kG_k+§sum_k§left[n§Delta_{k,k}-§sum_i§Delta_{k,i}§right].',
])
selected = exact_formulas(selected, [
    r'L(h)=§max_b§min_{z§in M(hb)}u_{|h|+1}(z),§qquad M(h)=§bigcup_b§{z§in M(hb):u_{|h|+1}(z)§ge L(h)§}.',
    r'§Gamma_{h,a;T}=§frac{§mathbf{1}_{§sigma(h)§in T}}{§#_Tz_h}-§frac{§mathbf{1}_{a§in T}}{§#_Tz_{ha}},§qquad §mathcal K_§sigma=§{w§ge0:§Gamma w§ge0§}.',
    r'r_a=d-§mathbb E_Q f_B(a)-§Gamma^{§mathsf T}§lambda_a§ge0.',
])
waterfill = exact_formulas(waterfill, [
    r"F(z)=1/(z+s')-1/(z+s)=(s-s')/[(z+s')(z+s)].",
    r'V(w)=V(1)-§Gamma-[B(w)-B(1)]§ge tM,§quad §Gamma+[B(w)-B(1)]+tM§le V(1).',
    r'lo=896364335596578238699711011639/1267650600228229401496703205376,',
    r'hi=112045541949572279837463876455/158456325028528675187087900672.',
])
dump(E / 'format-recovery.json', {
    'stage': 'before first completed self-check or delivery',
    'detected_by': 'formal C0 check in build_delivery.py',
    'cause': 'host-language backslash escapes altered TeX before Python raw strings',
    'repair': 'derived writer C0 removed; all eleven display formulas rebuilt with literal backslash placeholders and reread',
    'frozen_sources_inputs_runs_modified': False,
    'prior_failed_self_check_not_called_PASS': True,
    'mathematical_source_reruns_for_format_repair': 0,
})

formals = [
    document('archives/customer-attraction/state/资料/个体安全和全树流独立审计的完整合同--资料.md',
             'customer-attraction/independent-individual-and-flow-auditor-contracts',
             '个体安全和全树流独立审计的完整合同',
             '34客户全部节点/静态鞍点/唯一性；完整流代数与两个非SPE分离向量；两个新原码运行的真实输出边界。',
             ['263d8b8cde0651ffc00a', '0494c0e5b61617175486'], individual),
    document('archives/customer-attraction/state/资料/指定完整策略锥与全SPE正预算的原程序核验--资料.md',
             'customer-attraction/selected-cone-and-ordered-budget-auditor-contracts',
             '指定完整策略锥与全SPE正预算的原程序核验',
             '五固定游戏全有序SPE正GB及三固定形式策略全质量锥证书；输入/政策身份、CLI空输出接续和4914坐标不扩量词。',
             ['cb88477459c73d47fafe', 'c0b20181754a4455d3cb'], selected),
    document('archives/customer-attraction/state/资料/分数尾水位审计的有理停点和命令行边界--资料.md',
             'customer-attraction/waterfill-auditor-domain-and-exact-stops',
             '分数尾水位审计的有理停点和命令行边界',
             '全部16有理fixture/49共同Q-J子集/无理夹逼与利润守恒；精确候选根非通用求根器，同SHA旧运行复用。',
             ['30f18dd774474c944e78'], waterfill),
]
dump(E / 'formal-manifest.json', formals)

assessment = {'primary_CLI_invocations': 5, 'distinct_new_primary_codes_executed': 4,
    'successful_report_invocations': 4, 'new_waterfill_invocations': 0,
    'waterfill_prior_same_SHA_success_reused': True,
    'selected_cones': {'CLI_invocations': 2, 'entry_for_both': 'direct Python file __main__; not import-only, not runpy',
        'first': 'default input path; exit0/0.568s; stdout/stderr empty; command/bytes recorded, no function trace; no independent PASS/report claim',
        'followup': 'same __main__ with explicit same input path, PIPE captured; exit0/0.501s; 6686B report/4914 identities',
        'verify_calls_expected_from_static_entry_semantics': 2,
        'completed_verify_bodies_supported_by_saved_report': 1,
        'first_body_execution_directly_traced': False,
        'first_body_execution_inference': 'source guard evaluates verify(path) before print; normal direct-file semantics imply entry, but empty capture cause not determined',
        'not_two_independent_mathematical_evidences': True, 'unique_coordinate_identities': 4914},
    'old_reports_have_no_retrospective_code_SHA_binding': True,
    'no_source_modifications': True, 'no_shared_Git_network_identity_public_board_or_credentials': True}
dump(E / 'run-status-assessment.json', assessment)

target_by_id = {i: row['path'] for ids, row in [
    (['263d8b8cde0651ffc00a', '0494c0e5b61617175486'], formals[0]),
    (['cb88477459c73d47fafe', 'c0b20181754a4455d3cb'], formals[1]),
    (['30f18dd774474c944e78'], formals[2])] for i in ids}
notes = {
 '263d8b8cde0651ffc00a': ('393行全码、34客户真实7178B输入/全部43动作/pQ/历史MILP元数据实读；全部终局/静态和预算矩阵的定义与结果理解。', '与34稳定反例、360历史候选、全SPE预算的12离轨差比较；新原CLI一次，完整结果与旧166047B除路径全同；模板固定三人六主题、部分结论文字非assert不扩通用验证器。'),
 '0494c0e5b61617175486': ('209行全码、内嵌36/六类型/15类型及非均匀n4全部真实输入实读；252索引身份和97系数域、完整势/删除流推导及负Γ含义理解。', '与现背景提升/完整树障碍/旧51188B全部字段结构比较；新CLI一次，仅摘要与旧全报告对应字段相同；未把未写出的output局部变量说成新全报告。'),
 'cb88477459c73d47fafe': ('72行全码、五个真实固定JSON的所有游戏/政策/security及作者字段完整语义读；ordered菜单归纳及互斥首次离轨子树最大预算理解。', '与三页符号纠错及旧1825B结果比较；一次新CLI重枚举全部ordered菜单，五正GB保持；指定最优p/固定游戏与任意安全分布/任意游戏量词分开。'),
 'c0b20181754a4455d3cb': ('65行全码、三政策全部561历史/13套Q与全部字段实读；151λ条目/全部向量结构和精确定义核，不冒称人工逐数字文本阅读。', '与指定锥对偶/旧6686B/后来21新锥范围比较；首CLI exit0空捕获不称PASS，必要同__main__显式输入一次接续，1份报告4914坐标全同旧；2调用不当2独立证据。'),
 '30f18dd774474c944e78': ('160行全码、16有理fixture全部输入/候选停点、49共同Q/J子集和100次无理夹逼定义实读；利润守恒与背景kD族理解。', '与静态共同信用引理、前缀席位审查及旧报告/同SHA replay完整比较；旧成功无疑run复用，新增0次；候选根/顶层副作用/辅助质量不冒作一般SPE或求根算法。'),
}
receipts = []
for row in sources:
    i = row['id']
    receipts.append({'id': i, 'full_file_reviewed': True, 'related_material_checked': True,
        'unique_content_accounted_for': True, 'read_note': notes[i][0] + f" 原件{row['size']}B与inventory SHA逐字节一致，两冻结refs同字节。",
        'comparison_note': notes[i][1], 'decision_note': '完整独有内容集成自足资料；保量词/时态/真实运行身份与未认证域，不覆盖旧原件/旧资源，不额外done引用源，不导阶段三图；当前任意六人half仍开放。',
        'disposition': 'integrated', 'targets': [target_by_id[i]]})
dump(W / 'semantic-receipts.json', receipts)
dump(E / 'reading-scope.json', {'primary_files': 5, 'primary_bytes': 40803,
     'primary_full_actual_lines': [393, 209, 72, 65, 160], 'primary_line_sum': 899,
     'related_inventory_JSONs': 12, 'related_bytes': 644421,
     'related_inputs': 'six game/policy input files (five distinct games) + one cone pack; all full human semantic metadata/policies/Q; all numeric vectors parsed/retained/exact checked; input sources not additionally done',
     'old_reports': 'individual full output structurally traversed and entire new JSON compared except absolute path; lift full structure/metadata read and CLI projection compared; selected two full reports read; waterfill all16/irrational full report read',
     'formal_context_full_read': 13, 'rules_snapshot': 'AGENTS/OBJECTS previously full-read; current exact snapshots retained',
     'old_missing_entry_statements': 'historical facts preserved; frozen source now available, no old page overwritten',
     'primary_runs': assessment, 'phase_three_imports': 0, 'universal_six_player_half_closed': False})
(W / 'relation-review.md').write_text('''# 本批关系审查

个体34客户否定逐人静态安全桥，正聚合/half/GB仍成立；五固定游戏指定安全最优p上的全SPE正GB与三固定形式策略任意非负质量锥为不同量词。完整流身份与非SPE分离向量只排指定平均模板，尾水位是同叶辅助代数。相应真实源码、输入、现后续纠错和旧无活动入口时态均已实际比较。

这里只提供阶段二自足资源与有理由的接续方向，不创建阶段三边、不导旧图、不复done已完成的相关输入，也不闭合任意六人half。
''')
(E / 'README.md').write_text('''# 个体安全、指定锥/正预算与尾水位五主源

五源40803B/899行完整实读，三份自足资料；真实输入/全部字段与现正式纠错实际比较。四代码需要补旧报告所缺代码SHA运行绑定；individual/lift/budget各一，cone首CLI空输出与一次显式输入接续全部保留：总5调用、4份成功可核报告，非5份独立数学证据。水位同SHA旧成功精确复用，新增0次。

固定游戏/固定策略锥/任意客户质量、非SPE流分离及静态辅助水位各守量词；六人一般half仍开放。原件/旧页不改，无shared Git、网络、身份、公屏或凭据操作。唯一准备失败是先猜错旧水位物理路径，已从真实存在路径核SHA恢复；不是数学运行失败。具体scope、原件/输入/命令和异常在相邻JSON。
''')
(W / 'delivery.md').write_text('''# 精确交付

5主源完整正文/原件/真输入、3自足资料、5逐源receipt；copy-files.json逐件路径/bytes/SHA，独立外部staging。运行与格式自查不替代一般数学证明；无需对无疑同SHA水位旧成功复跑。
''')

checks = []
def check(label, condition):
    assert condition, label
    checks.append({'check': label, 'passed': True})
for row in sources + deps:
    data = (ROOT / row['saved_path']).read_bytes()
    check('exact inventory bytes ' + row['id'], len(data) == row['size'] and hashlib.sha256(data).hexdigest() == row['sha256'])
claim = json.loads((E / 'actual-claim-receipt.json').read_text())
resolution = json.loads((E / 'sync-resolution.json').read_text())
check('actual pushed Boss4 five subset', claim['status'] == 'pushed' and claim['actor'] == 'Boss4' and set(x['id'] for x in sources) <= set(claim['ids']))
check('original sync conflict separately resolved', claim['local_sync']['status'] == 'needs-attention' and resolution['status'] == 'resolved-and-verified' and resolution['all_five_claims_Boss4_in_progress'] and not resolution['missing'] and not resolution['different'] and not resolution['unmerged'])
ready = json.loads((E / 'input-structure-and-readiness.json').read_text())
check('all actual input fields/stdlib dependencies ready', ready['all_twelve_JSON_fields_traversed'] and ready['lambda_terms_checked_structurally'] == 151 and len(ready['canonical_vs_budget34_policy_differences']) == 12)
newold = json.loads((E / 'new-old-comparison.json').read_text())
check('new old full comparisons and exact run counts', newold['all_comparisons_passed'] and newold['new_primary_source_invocations'] == 5 and newold['successful_report_invocations'] == 4 and newold['new_waterfill_invocations'] == 0)
runrows = json.loads((E / 'runs/new-run-summary.json').read_text())
for run in runrows:
    check('recorded CLI exit and assertion mode ' + run['name'], run['exit_code'] == 0 and run['runtime']['optimize'] == 0 and run['runtime']['isolated'] == 1)
check('first cone empty attempt not promoted', (E / 'runs/selected-cones.stdout.txt').stat().st_size == 0 and assessment['selected_cones']['completed_verify_bodies_supported_by_saved_report'] == 1)
follow = json.loads((E / 'runs/selected-cones-explicit-run.json').read_text())
check('followup exact code/input report', follow['exit_code'] == 0 and follow['source_execution_count_this_batch'] == 2 and follow['stdout_bytes'] == 6686 and follow['source_sha256'] == byid['c0b20181754a4455d3cb']['sha256'] and follow['input_sha256'] == byid['7a48fb9d35ad4f79eb56']['sha256'])
ind = json.loads((E / 'runs/individual-34-files/results.json').read_text())['summary']
check('individual actual finite boundaries', ind['security_value'] == '2411/246' and ind['individual_security_margins'][0] == '-11/82' and ind['GB'] == '60/41' and ind['half_coverage_margin'] == '15' and ind['policy_node_count'] == 43 and ind['alternative_evaluations'] == 258)
bud = json.loads((E / 'runs/selected-budgets.stdout.txt').read_text())
check('five true positive all SPE fixed p budgets', len(bud['cases']) == 5 and all(Fraction(r['minimum_GB_budget_over_all_pure_SPE_at_given_optimal_p']) > 0 for r in bud['cases']) and [r['ordered_SPE_outcomes'] for r in bud['cases']] == [48, 40, 23, 102, 6])
con = json.loads((E / 'runs/selected-cones-explicit.stdout.txt').read_text())
check('three fixed policies thirteen exact certificates', con['identities'] == 4914 and len(con['results']) == 13 and len({r['case'] for r in con['results']}) == 3)
oldman = json.loads((E / 'context/archives/customer-attraction/tools/evidence/fractional-load-boundaries/source-manifest.json').read_text())
check('waterfill exact prior source SHA', any(r['id'] == '30f18dd774474c944e78' and r['sha256'] == byid['30f18dd774474c944e78']['sha256'] for r in oldman))
water = json.loads((E / 'context/archives/customer-attraction/tools/evidence/fractional-load-boundaries/replay-waterfill.json').read_text())
check('waterfill old actual domain', len(water['rational_cases']) == 16 and sum(r['queries_checked'] for r in water['rational_cases']) == 49 and Fraction(water['irrational_case']['width']) == Fraction(1, 2**100))
for row in formals:
    text = (ROOT / row['path']).read_text()
    check('flat MATEK ' + row['path'], all(re.search(r'^' + key + r':', text, re.M) for key in ['id', 'kind', 'type_tag', 'title', 'status', 'summary', 'source_refs']))
    check('formal C0 ' + row['path'], not any(ord(c) < 32 and c not in '\t\r\n' for c in text))
    check('formal trailing whitespace ' + row['path'], all(line == line.rstrip(' \t') for line in text.splitlines()))
check('five complete receipts', len(receipts) == 5 and {x['id'] for x in receipts} == {x['id'] for x in sources})
for receipt in receipts:
    check('semantic receipt ' + receipt['id'], all(receipt[k] for k in ['full_file_reviewed', 'related_material_checked', 'unique_content_accounted_for', 'read_note', 'comparison_note', 'decision_note']) and all((ROOT / p).is_file() for p in receipt['targets']))
report = {'passed': True, 'checks': len(checks), 'details': checks,
          'scope': 'primary/input exact bindings, true execution/reuse identities, finite/fixed-cone domains, receipt and formal format; not universal math or production certification',
          'formal_forbidden_C0': 0, 'formal_trailing_whitespace': 0}
dump(E / 'self-check.json', report)
dump(W / 'self-check.json', report)
print(json.dumps({'formal_files': len(formals), 'formal_bytes': sum(x['bytes'] for x in formals),
                  'primary_files': 5, 'primary_bytes': 40803, 'semantic_receipts': 5,
                  'checks': len(checks), 'passed': True}, ensure_ascii=False))
