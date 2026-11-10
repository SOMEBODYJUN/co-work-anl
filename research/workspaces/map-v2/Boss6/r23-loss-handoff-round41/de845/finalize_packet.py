import json,hashlib,pathlib,sys
REPO=pathlib.Path('/workspace/scratch/bbb425bb840f/co-work-anl-boss6')
OUT=pathlib.Path(__file__).parent
TASK='customer-attraction-3a-3a-de845558940d83ed'
EDIR=pathlib.Path('map/edges')/TASK
RPATH=pathlib.Path('map/receipts')/(TASK+'.json')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(o):return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
t=json.loads((REPO/'research/operations/map-v2/tasks'/f'{TASK}.json').read_text());d=t['definition']
registry=json.loads((REPO/'research/registry.json').read_text());objects={o['object_id']:o for o in registry['objects']}
assert t['owner']=='Boss6' and t['state']=='claimed'
assert all(pin(objects[k])==v for k,v in d['input_pins'].items())
sys.path.insert(0,str(REPO/'tools'));import research_runtime as rr

# The extra conditional budget proof is preserved outside task assets pending
# the Boss's decision on an exact dedicated mathematical target.
pending=OUT/EDIR/'pay-budget-funds-arb-net-demand.json'
if pending.exists():
    (OUT/'candidate').mkdir(exist_ok=True)
    pending.replace(OUT/'candidate'/'pay-budget-funds-arb-net-demand.json')
new=[]
for p in sorted((OUT/EDIR).glob('*.json')):
    if p.name in {'reading-ledger.json'}:continue
    x=json.loads(p.read_text())
    if 'edge_id' not in x:continue
    rr.verify_endpoints(REPO,x,objects);rr.require_edge_result(x)
    x.update(rr.edge_bindings(REPO,x,objects,verify=True));write(p,x)
    new.append((p.relative_to(OUT).as_posix(),x))
assert len(new)==8,len(new)
ids={x['edge_id']:p for p,x in new}
E=lambda slug:'ca-de845-'+slug

F='customer-attraction/forward-customer-absorption-whole-row-envelope-and-net-budget'
PAY='M-8a3d5457d56c413189e2683b8ddecde0'
HALL='customer-attraction/optimal-owner-all-subset-harmonic-transport-and-anchor-isolation'
ANCHOR='M-3c46dcd1fcae445bad3d6d64684c21d2'
NS='M-966d7f6ae9b243a8a2c6a6571e2f1056';NOPT='M-87293a52db92485094df7979eb9c6564'
THETA='CA-EXTREME-MAXIMAL-THETA-v1';WELF='CA-EXTREME-MAXIMAL-WELFARE-v1'
EX='customer-attraction/optimal-five-query-indexed-exchange-and-outside-tax'
M1='CA-MOBIUS-BOOLEAN';M2='CA-MOBIUS-FULL-HISTORY-EMBED'
PROM='customer-attraction/terminal-promotion-potential-drop-and-sharp-new-branch-tax'
PAIR='M-e960d7f4ebca40a38760eb3ae044cc19';TAX='M-aeb30b10477d40d08ec5149f606b133a'

review='''# Boss6 de845 完整比较审读

当前任务由Boss6持有，22个核心按17个问题组完整比较。原25个输入的登记pin及46个distinct文件SHA均逐项核同；read-add实际发布后另核7端点与其必要正文/证据。全部32个端点当前登记pin列于reading-ledger。对原task的46文件，两个资源只要求特定节，其余正文、代码、报告已连续实读；长JSON以无损compact全字段视图读取，工具曾截断的段落均另补读。新增必要正文9份，使实读55个distinct源文件。只复用成熟解析证明和已存精确有限证书，没有运行旧数学程序、LP、大枚举或重建全树。

## 1. 前向客户吸收：精确恒等式、残源嵌入与新的条件方向

实际读共同目录/残余税定义、forward全文、52客户固定策略压力LP合同及联合银行资源§3。forward的状态严格是原actual-prefix query，每次child重回原actual前缀。每个OPT客户一单位源给A+P=OPT；query最大访问包络λ购完整f，D_env=Σλf−A包括全部客户。净账恰为OPT+ΣλΓ，故PAY的存在性是付同一IC松弛总额，不能从P≤|O∩C|、D_env≥0或流终止推出。

read-add FINANCE与ARB全文逐项比较r/D。R=O\\C无past，q≤1缩放仍为合法严格未来自然coverer分流，正tracked行的r=1/全部query覆盖数、完整D=forward f。金融乘子w=A^q/f≤λ；K=Q+ΣwΓ≤Q+ΣλΓ，另K≤gross ΣΛu。这个是不依赖开放PAY的真实局部贡献，不能据金融总吸收自动COORD。

另独立发现完整条件付款：δ=OPT−W=|R|−|G|，任取R上总量δ的q≤1，K=δ+ΣwΓ。若PAY已付ΣλΓ≤2W−OPT，则K≤W，因而ARB净需求最小费≤W。推导不是把P−D_env退款直接当现金，而是R守恒、w≤λ和同σ Γ≥0三者联合。该证明另与FREE等份流程逐项比较：父依赖动作及混合起点可由角色逆推最小价逐项压低，固定每(i,x)argmin仍共同兼容；所以Σqκ_FREE≤K≤W。已按ALL[PAY,forward,FREE]→既有KAPPA候选交accepted conditional whole，保对每份σ存在PAY见证同一最优O的量词。仍没有证明普遍PAY存在，亦未保旧Hall自由trim和初始化钱包可兼用。

## 2. 最优owner运输与锚隔离

完整读同叶HYB、Bernoulli积分HHYB、Hall-A/B全部割和B隔离证明、同叶预留页及852条有限回归正文。B源H_c/c不是普通1/c利润，已覆盖missing-owner终端不是实际遗漏，A/B不能双领容量。Q_i⊆B_i时HYB单点库存空，故source0；E中无该owner，出边/终端全无；任意非负守恒流均入0。强制整个最优前缀才隔离全部过去角色，仅当前actual-prefix query不够。有限9目录/14owner/852记录、11474割、1479正增广仅核静态图，逆角色流不能当原游戏未来链。

同一HYB还有不同有用方向：单槽k选择Q_k恰为T_k私有块即可给五查询单槽最优交换；多槽I另按I选owner，使所有外槽覆盖客户都归外槽，得完整多槽覆盖差。配对与全部25求和、固定C/实际A+B及τ_out≤r/2分别保留，推出五索引库完整目标。这里不用Hall支付或SPE，私有客户容量仍可能被S_i覆盖，不能作免费actual资金。

## 3. actual13_v1 与 source_last 两固定必要点

完整读共同目录抬升程序正文、actual13_v1全部63投影系数/13正有理乘子和长负分数、source_last全部53系数及两乘子。actual13输入SHA5930…的actual八态747行投影严格负约−0.0002629082666，max侧只浮点可行，joint未执行。source_last输入SHA66d6…的两H模型虽然跑联合128行，但actual:cap:V与K-envelope按13395/13396及1/13396已消H并严格分离，非新增跨历史兼容性。两点不同质量、行族及隐藏维数，不能互相推出；无双方精确边缘抬升，更不能将失败点当完整原SPE。与同叶Hall流、Boolean signed反演及CC三角比较都缺共同非负全局会员/完整策略，故本组不造逻辑边。

## 4. 任意人数 near-saturation 与受限模板边界

完整读局部引理及3518字raw。A式只用真末位IC和全目录共同容量U；源Γ才把Δ换成(M−1)(u−s)。逐客户三类非负证书取末位容量k、中间k/2，达到B=k−1,V=k²/2。模板下界另由三个坐标迫t≥k,p≥k/2,B≥t−1，k2无中间项。已交边只将上界证书作为目标尖锐性可达侧，余必要性不从“有证书”反推。U=u与K/k是同机制的两付款端点，不自动补全跨节点44/60行全局证书。

## 5. 极端归属θ、末位计数与含核心锐福利

完整读最小坏剩余人数、每后继真收益、无自路由整数矩阵、可零坐标平稳π、单例/全体/缺一逐客户付款和全部玩家传播；另读静态θ/隐藏抽样v区分、背景嵌入、F_r≤(2r−1)θ_r、旧theta首位页及有限复现。缺一付款中路由人数≥1是整数条件，不能改分数。θ求和加静态计数给P_r≥rθ≥rF/(2r−1)。空根仅静态扩到极大主题，核心贡献c/m，残余计数得含核心强化；all-big私瓣族在全部有序历史给每m锐性。13有限实例不是普遍证明。已给一条ALL[θ,lastslot]完整福利边；两个in-packet overlap在本包已处理，不填closed_overlaps。

## 6. 同分布额外查询反例与整数3/8界

读iid全文及其31节点124非自身偏离、5×5 K/D、p、150 RESET对完整JSON，再读冻结点资源§3。准确正差G−Dbar=13/1722，实际u−G=839/574>0。它只反平均真实强制收益封顶，不反实际u、路径总账或half。整数3/8界则对任意联合完整整数负载分布成立，保a≤n和对角损耗；其AA/空主题极限不是SPE。iid例可以作为该代数上界的一个同分布输入，但上界不能生成该完整策略或推出强式反例，反例也不反3/8。与PAY是不同源/分布合同，没有新逻辑边。

## 7. 笛卡尔补偿有限审计

全文读12给定策略DAG参数例及12个全部SPE边缘最小福利例。指定策略核全部九叉历史的DAG，集合值递推另给有限最差福利，非一个完整solver重复两次。padding新增两字段是安全端点卷积算术，不是在扩目录上重新验IC。n4/m6：联合最差125、OPT137、分量最低81+48=129，真实非可加而half有余。分量各自三极大单例归属满足极端结构，联合九主题客户归属数3不在{1,8,9}，θ结构假设不能直接迁移；全收益唯一性前提亦不由“分量根边缘唯一”获得。与fresh M2/抽象退化LP无同模型推导，保isolated。

## 8. Möbius M1 到全历史M2

全文读M1/M2、read-add所列全收益布尔正性与长前缀构造证据。M1唯一规定signed重复计数势，只能编译删除边际，负重数不是客户。清分母后K=4M+1同时保正singleton和严格fresh优于old：仅偏置中对齐未用标签，差≥1/2；signed两真实叶最坏−2M。归纳覆盖所有重复有序历史。给定辅助完整策略，在每个首次重复孩子独立填fresh受限BI，原辅助子树平局全保；恰为满射投影而非策略一一对应，根收益D u+Kb。p<n不适用，n1/M0零边界单列。已完成follow-up M2/M1，边为完整目标，不需要再发3B；不迁移福利比例或half失败。

## 9. 三重复目标严格唯一锥的精确退化

全文读13固定目标/37最优行合同与九锥LP、当前强FOMA纠错。112/122、113/133、122/112各同支持导致一条唯一性0·w+δ≤0，强迫δ≤0；全主题类型质量1使任意固定σ IC全等、W1、全部覆盖和冻结费用1，δ0可行，所以三项精确最优0。其它六项只有零可行点和历史float0，无精确上界。该允许同覆盖标签的质量锥不同于固定原客户数、强/弱指派命题及真实反例；与最优交换的“某个最优元组”也不同。不能把退化推成FOMA正面结果，无新边。

## 10. 逐原子回撤的固定余流合同

全文读盲审、独立恢复及工作区账本。盒分离R/R'充分必要只管同一F、t、b的上界，f=F−Σbt须逐角色保留；没有非负分解时另要F'≥0。一角色F2/c3/2和两角色F=(1,0)/t=(1/2,1/2)精确反简化价格接受，后者总量相等仍错位。λ≡1返还全零，仍是原总资金约束；细粗差Σmin(D_i,E_i)是固定合同改善，不是SPE新资金。forward退回的D_env、Hall同叶容量与这个固定原子余流并非同对象，无法直接用反例否真实金融流或用分离支付共同cap，保isolated。

## 11. 重复惩罚末位D外选项

读重复H障碍、共享遗漏资源指定段及literal删背景/角色交换全文。actual末位D最佳迫p/2+q+b≤t，最后H玩家在E_i上的γ双方同消，(p+q)/(r+1)<t−b（q>0）给严格D偏离，即使其它动作可命中E_i仍成立。这个目录含遗漏Q，不同于旧不含Q惩罚，且不能否定所有非重复惩罚。literal去PB背景的G与Fill只是两充分条件冲突，保G路径覆盖亦不足反half；fresh k块存在需额外目录假设。全k pair/reservoir仅末位真BR，倒二δ≥7/成本≥21但早期未付。与forward形式harmonic树都见离轨失败，却不满足同一目录结构，不能冒成互相refutes。

## 12. 两分离遗漏块两人付款

全文读50兴趣型域定理与7776浮点/四单位精确点资源。u1≥θ2≥min(α,β)由最大裸主题真实偏离和两人收益差证明，u2≥max块由actual A不碰U/V；合得global D≤W及四单位锐点。此处极大目录可能任意C内交叠，不自动满足极端归属结构；两人完整理性是另一独立证明。与一般R≤W已假相容：旧反例outside兴趣不在这两个完整pair类型。此点global D=W=OPT2只是数值相同，任意比较R/G要另分。不能把限定域界迁移到forward一般R或重复惩罚Q，保isolated。

## 13. 相邻真实有序换序

全文读5条非负行、256型ρ、Fraction源码与全部有理余项JSON。J按A/C主题身份区分，不按位置混收益；两前缀同负载不强制同续局。7/12恒等式用两个真实三尾各自G，最大裸主题仅浮点发现LP附加条件，解析证书不需要。14/9粗界另借同背景三人比较，不能为多次换序反复花一份actual尾。与末主题提前重置是不同操作/人数/势差，亦不能由末两人强PAIR单独付三尾共同cap；已比较保isolated，无全局付款或锐性新断言。

## 14. 末主题提前三主题族与强PAIR

三主题族2t/2t/3t全部13节点39值实读；actual(A,B,B)收益(3,2,2)t，提前(B,C,B)为(5/2,2,5/2)t，源Γ=t/2，双方W=OPT7t，Phi损失t。四主题21节点零Γ族另为actual012/提前232/回放201，W7/6和Phi9/8，不混成同一σ。read-add强PAIR与普遍税端点后全文核三IC及新枝b'=b+1_C，Phi_old−Phi_new≤g_b'(D,D)−g_b'(D,E)，三主题给税系数1锐。此关系由e64包实际pushed canonical精确复用，路径和SHA见receipt/manifest，本文不重复造同一边。follow-up强PAIR比较已经解决，已closed并列canonical证据。R23辅助§1“首位收益”应为收益损失Γ已告Boss，等待源版本流程刷新；三主题正文与statement不受这处用语影响。

## 15. CC-TRI-NO 与完整表示的边界

全文读四虚拟位3/−1/1数组、全部局部投影、K3,2全部可见三角、g²值−24及任意块提升；m2或m≥4、3floor(m/2)>m是域，m3不覆盖。g空类型为零且平方可见，所以另选空质量/总量也不能修复。有限字面审计m2/4/5不是m6新run；另整数格族d3检查不是同三角族。signed arrays不是单位客户或SPE，不能与actual13辅助点直接互推；M1是完整子集调和表唯一signed反演，当前是截断覆盖矩/正性，数据核不同。未找到准确端点的逻辑推导，保isolated；并未声称客户正性与全树IC联合系统被否定。

## 16. 覆盖与未付义务

新边八条：五条whole（其中PAY→KAPPA为conditional）、三条unconditional contribution；canonical重置边以实际pushed精确SHA复用。没有proposed数学缺步，也没有输入身份needs-decision。所有原core已读完；linked仅指已接受逻辑关系（包括精确局部贡献），其余isolated各有以上实际比较。一般PAY、ARB净源≤W、跨叶incoming、共享税钱包、六人half仍open。没有把有限浮点/必要点/形式收益或代码PASS扩张为普遍结果。
'''
(OUT/EDIR/'review.md').write_text(review)
proposal="""# R23辅助页最小措辞补丁提案

当前源：archives/customer-attraction/state/障碍/R23-promotion势能桥与零遗憾重置精确反例--障碍.md

当前SHA：20b3d868fded89f6aa1ce018394dab93ec59c763a7d867062279ec2d73944bf7。

位置：§1“结论先行”第一段末句。将唯一字符串 `来源遗憾/首位收益` 替换为 `同一来源节点行动者的收益损失（IC 松弛 Γ）`。

改后该句：因此，任何试图用“同一来源节点行动者的收益损失（IC 松弛 Γ）”乘一个固定有限常数去支付该 promotion reset 的证明路线都失败。

理由：四主题族来源行动者实际/提前收益均2t，Γ=0，而势降t；它否定有限常数乘Γ。绝对首位收益为2t而非0，不能据此声称任何有限常数乘绝对收益也都无法支付。三主题族Γ=t/2、势降t，只给另一份独立尖锐见证，不与四主题零Γ策略合并。

影响：只收窄辅助页这一过强用语，不改三主题13节点正文、注册statement、强PAIR普遍税界或系数1锐性。该辅助文件属于terminal核心证据，修改后须刷新该核心登记版本/pin，并定向重绑实际复用的e64 ALL边及相应阅读收据。当前de845草稿绑定修改前v3精确pin，后继刷新由Boss串行处理；worker未写clone或源文件。
"""
(OUT/EDIR/'source-proposal.md').write_text(proposal)

linked={
 PAY:[E('forward-ledger-isolates-pay-slack-obligation'),E('forward-pay-budget-implies-free-kappa-budget')],
 F:[E('forward-ledger-isolates-pay-slack-obligation'),E('forward-residual-flow-embeds-in-arb'),E('forward-pay-budget-implies-free-kappa-budget')],
 HALL:[E('hall-b-transport-isolates-owner-complete-roles'),E('hall-hybrid-specializes-to-five-index-exchange')],
 ANCHOR:[E('hall-b-transport-isolates-owner-complete-roles')],
 NS:[E('near-saturation-certificate-attains-template-corner')],NOPT:[E('near-saturation-certificate-attains-template-corner')],
 THETA:[E('theta-and-catalog-counting-give-sharp-core-welfare')],WELF:[E('theta-and-catalog-counting-give-sharp-core-welfare')],
 EX:[E('hall-hybrid-specializes-to-five-index-exchange')],M2:[E('mobius-inversion-with-positive-bias-compiles-full-history')],
}
scopes={
 PAY:('组1：forward(1)–(5)/PAY?、两指定资源段、FINANCE/ARB同r完整行合同。','净账与IC松弛条件完全等价，但对每份真实SPE选择μ/λ并支付总ΣλΓ仍open；已给精确局部贡献，未将开放前提升级。'),
 F:('组1：全部OPT客户的真实query DAG、过去吸收、全客户D_env及R残源到ARB。','守恒和整行净账已证；R客户p=0使原自然未来coverer流成为ARB可行子域，w≤λ且K=Q+ΣwΓ。共同金额与COORD自动投影未由此获得。'),
 HALL:('组2和组5索引：HYB/HHYB、Hall-A/B全割、锚隔离、852静态回归及五槽交换。','B图任意流锚隔离完整成立；HYB按可变owner特化给五索引静态交换全库。调和source不等于实际利润，A/B与不同叶不能双领库存，跨叶IC支付未解。'),
 ANCHOR:('组2：同一owner同叶B图、owner完备段、完整最优前缀段及A图区别。','HYB单点迫外源0且B图无自有出边/终端，非负守恒迫任意流入0。完整最优前缀隔离成立，但单actual-prefix查询及Hall-A任意流不在结论内。'),
 'M-4e7276c6fbc64750b9aa12f8c0872139':('组3：actual13_v1 SHA5930…、747行/八隐藏态、63全系数与13有理乘子；对比source_last及CC截断正性。','固定质量actual边缘精确负；max只浮点成功，joint未执行。source_last是不同53原子/两H域，不能互推；未获得同一完整共同目录/SPE或双方精确边缘实现，不造兼容性新边。'),
 'M-807b03bb63d54b02a6ccb1e4e1140c5f':('组3：source_last SHA66d6…、两actual行消H、53系数长负分数与actual13身份差。','13395/13396容量行加1/13396 K-env已独立否actual边缘，新增互查及max侧未承担严格性。不同点的actual13十三支持不转成此点新机制；未登记该点所否的一般新命题，故本范围隔离。'),
 NS:('组4：任意k,b的三类ρ证书、容量U、源缺额Δ和两个读出；raw全部解析段。','显式证书给模板B=k−1,V=k²/2可达，作为目标边界的局部贡献。A式末位IC/容量与B式源IC范围分开；U=u/K/k不支付全局跨节点预算。'),
 NOPT:('组4：受限模板三个必要坐标及k2边界，对比可行上界证书。','必要t≥k,p≥k/2,B≥t−1独立于全局SPE最优性；上界证书达到相同角点，已连可达侧，未把它当系数必要性的单独证明。'),
 THETA:('组5：最小坏剩余人数、整数无自路由π、三类逐客户支付、前缀嵌入；末位值in-packet overlap。','给全部玩家≥纯θ，联合通用F计数后推完整含核心福利与锐性。θ≠隐藏抽样v，整数缺一条件不放宽一般中间归属；有限复现只核实现。'),
 WELF:('组5：同背景剩余利润、空根核心静态消去、全历史all-big锐族；末位计数in-packet overlap。','ALL[逐人θ,通用计数]支付P_r及核心强化，且显式策略逐m取等。非零背景不把剩余利润冒完整覆盖，早期真实行动无需含核心。'),
 'customer-attraction/iid-extra-query-exceeds-average-forced-payoff':('组6：31节点124偏离JSON、K/D/p全表、150 RESET对及六点字段资源§3；对比3/8/PAY。','G−Dbar=13/1722而G−u=−839/574，精确只反平均强制值。3/8是同分布负载上界，不生成此SPE或反实际u；forward是query整行选流而非本p独立额外槽，未找到准确逻辑边。'),
 'customer-attraction/coupled-cartesian-complete-policy-and-factor-extrema-exact-audit':('组7：12指定策略DAG/12全SPE边缘最小值、padding字段及结构θ/M2比较。','有限m6联合125<分量81+48说明非可加但half有余；联合九极大归属3不满足{1,8,9}，强分解需全收益唯一性，不能从分量根唯一推出。端点算术不等扩目录IC，无可迁移全称边。'),
 EX:('组2/5索引：单槽owner取private、多槽按I选owner、配对/全25/固定C/前缀行、外税和两钱包实际范围。','由HYB特化及τ_out≤r/2得到目标全静态库；右侧是指定OPT私有客户容量，不是自动unused W。实际复位ρ_i与第三位尾S_i是不同历史，联合钱包仍未付。'),
 M2:('组8：M1唯一signed反演、M2全部重复历史支配/辅助投影/完整扩展和根平移；对读截断矩/长前缀。','已完成M1→完整M2且关闭声明follow-up。K4M+1严格gap而非仅正重数支撑全历史；投影满射非一一对应，福利比不保持。'),
 'M-0eafbe74c0e042a2a079968e9bbbcedc':('组9：13固定目标/37行合同、九锥LP、112/113/122同支持退化及M1/最优交换比较。','严格唯一多重集有0w+δ≤0且全主题质量1在δ0可行，三LP精确最优0；其余六仅float0。这个闭实质量锥不能推出强/弱FOMA或原指定实例真值，未造逻辑边。'),
 'customer-attraction/atom-retraction-blind-review-fixed-residual-contract':('组10：固定F/t/b盒分离、逐角色f、两反例、恢复和自由删槽账本；与forward/Hall/FINANCE比较。','两抽象例准确反省f判据，常价格仍要求原总资金；没有给真实query DAG/SPE实现，不能用它否forward或普遍金融资金。下界需非负分解或另加，与已付A分开，保隔离。'),
 'customer-attraction/repeated-punisher-last-outside-option-and-no-background-transplant':('组11：H_i含遗漏的末位D比较、共享遗漏指定段、literal去背景和低头高尾全文；对比forward形式树。','γ同消使最后H严格偏离D，q>0/r≥1承重。只能排此重复尾形状；旧不含Q目录、全k末位路径和一般更换punisher不同。形式harmonic复制虽也不SPE，未满足同合同，不生互相refutes。'),
 'customer-attraction/integer-complete-load-three-eighths-source-decorrelation':('组6：J/H成对恒等式、整数Δ、对角损耗、AA/空主题锐族及版本路由全文；对比iid例和金融分流。','3/8对任意合法整数终局联合分布已证；其非SPE极限不能转真实p菜单锐性。iid正差不否此上界，实n扩域失败不同于单位整数模型；V/源税/实际slack仍须共同付款，本范围无新端点关系。'),
 'customer-attraction/two-player-two-separated-omitted-blocks-total-omission-payment':('组12：50兴趣型、两人θ/末位max块、四单位等号点与7776浮点合同；比较极端归属/一般R。','两分离投影给global D≤W是独立两人真BR证明；任意C内交叠不自动满足极端归属，非零背景和一般outside兴趣无此结论。点上D=OPT2只是数值，不与R/G身份混，未造泛化边。'),
 'customer-attraction/adjacent-real-order-swap-payment-envelope':('组13：同σ两个有序前缀、五行G、256全ρ及原码JSON、发现LP最大性与14/9预算。','7/12仅局部两尾合付，解析不用A/C裸最大；两有序历史同负载不等后继。多次换序共享actual尾无保证，与末主题promotion势差非同操作，不能互推或称锐，保隔离。'),
 PROM:('组14：三主题13节点族、四主题零Γ族区别、强PAIR及普遍新枝税端点和R23辅助§1/§3/§4。','三主题源Γ=t/2、双方福利7t、势差及新枝税t；普遍税界和系数1锐由强PAIR与本族ALL支持，复用实际pushed canonical，未重复造边。新枝费用不等原actual已付款；R23收益措辞窄勘误待Boss刷新。'),
 'CC-TRI-NO':('组15：四虚拟位全部投影/K3,2三角/−24平方、块提升m域、有限字面审计；对比M1与actual lift。','m2或m≥4的signed截断矩反蕴含，m3不覆盖；非负平方可见且空类型零使无法修复。不是单位客户/SPE，M1完整调和表和actual13固定必要质量是不同数据核，未产生实际half或兼容性逻辑边。'),
}
coverage={}
for k in d['object_ids']:
    s,r=scopes[k];x={'state':'linked' if k in linked else 'isolated-after-review','object_pin':d['input_pins'][k],'comparison_scope':s,'reason':r}
    if k in linked:x['edge_ids']=linked[k]
    coverage[k]=x

# Exact canonical edge reuse will be added after the corresponding actual push.
reuse=[]
canonical_names=set(registry.get('edge_files',[]))
canonical_names.add('map/edges/customer-attraction-3a-3a-e64cb2654bcab2e5/strong-pair-gives-sharp-three-player-reset-tax.json')
for name in canonical_names:
    p=REPO/name
    if not p.exists():continue
    x=json.loads(p.read_text())
    if x.get('status')=='accepted' and x.get('source_ids')==[PAIR,PROM] and x.get('target_ids')==[TAX]:
        rr.verify_endpoints(REPO,x,objects)
        assert x.get('endpoint_pins')==rr.edge_bindings(REPO,x,objects)['endpoint_pins']
        reuse.append({'path':name,'sha256':sha(p),'edge_id':x['edge_id']})
if reuse:
    assert len(reuse)==1
    coverage[PROM]['state']='linked';coverage[PROM]['edge_ids']=[reuse[0]['edge_id']]

files={}
for r in d['context_plan']['reading_refs']:
    p=REPO/r['path'];assert sha(p)==r['sha256']
    z=files.setdefault(r['path'],{'path':r['path'],'sha256':r['sha256'],'read_scope':'全文；长JSON无损compact全部字段/系数，截断段已补读','declared_sections':[]})
    if r.get('section'):z['declared_sections'].append(r['section'])
for name in ['通用菜单时机与固定策略锥压力的原诊断合同--资源.md','联合银行预算与客户吸收的审查和执行边界--资源.md']:
    for k,v in files.items():
        if k.endswith(name):v['read_scope']='仅task指定连续节：'+ '；'.join(v['declared_sections'])
extra=['算法/任意未来查询的完整行采购价与对偶--算法.md','资源/任意子查询付款的两种充分证书与原等价勘误--资源.md','定理/有限阶交集矩的全收益表示与布尔正性--定理.md','构造/任意长前缀牺牲的无重复势博弈与合法嵌入--构造.md','程序/单隐藏末回复的配对投影恒等式核验程序--程序.md','反例/零源与特定回放松弛不能支付末主题重置--反例.md','算法/自由查询与自由起点的单位采购价格--算法.md','算法/客户级自由接纳与累积税的整行付款--算法.md','审查/全角色运输与联合激活的历史审查边界--审查.md']
for name in extra:
    k='archives/customer-attraction/state/'+name;p=REPO/k
    files[k]={'path':k,'sha256':sha(p),'read_scope':'read-add端点必要正文/证据全文','declared_sections':[]}
ledger={'task_id':TASK,'owner':t['owner'],'request_id':t['request_id'],'stage':'3A','input_pins':d['input_pins'],'input_pin_checks':{k:pin(objects[k]) for k in d['input_pins']},'distinct_source_files':len(files),'files':list(files.values()),'core_comparison_groups':d['context_plan']['comparison_groups'],'reading_boundary':'正文、task指定证据及必要read-add文件全读；不递归把所有导航引用作为新实读或新程序运行。','mathematical_execution':{'new_LP':0,'old_program_reruns':0,'new_full_tree_audit':0,'description':'仅成熟解析证明/字面有限证书审读及exact SHA/registration pin/edge_bindings格式核查。'},'canonical_reuse':reuse}
write(OUT/EDIR/'reading-ledger.json',ledger)
assets=[{'path':p,'sha256':sha(OUT/p)} for p,x in new]
assets += [{'path':(EDIR/f).as_posix(),'sha256':sha(OUT/EDIR/f)} for f in ['review.md','reading-ledger.json','source-proposal.md']]
assets += [{'path':x['path'],'sha256':x['sha256']} for x in reuse]
receipt={'coverage':coverage,'assets':assets,'follow_up_tasks':[],'closed_overlaps':[{'core_id':M2,'peer_id':M1,'reason':'本包accepted完整M1→M2边已处理唯一反演、充分正偏置、全部重复/离轨历史扩展及根平移，比较闭合，无需新3B。'},{'core_id':PROM,'peer_id':PAIR,'reason':'普遍新枝税来自强PAIR，系数1锐来自独立三主题13节点族；同一ALL关系以e64已实际pushed canonical精确复用（见assets），不重复建边。'}]}
if not reuse:
    receipt['closed_overlaps']=receipt['closed_overlaps'][:1]
    write(OUT/'receipt-awaiting-canonical.json',receipt)
else:write(OUT/RPATH,receipt)
manifest={'task_id':TASK,'owner':'Boss6','request_id':t['request_id'],'new_files':[{'path':p.relative_to(OUT).as_posix(),'sha256':sha(p)} for p in sorted((OUT/'map').rglob('*')) if p.is_file()],'canonical_reuse':reuse,'pending':['R23辅助措辞窄勘误后刷新terminal pin；第8条PAY→FREE-KAPPA条件完整边已保存；待Boss核全部目标和发布']}
write(OUT/'manifest.json',manifest)
write(OUT/'handoff.json',{'task_id':TASK,'owner':t['owner'],'request_id':t['request_id'],'read_complete':True,'input_fresh_at_manifest':True,'new_accepted_edges':len(new),'canonical_reuse_complete':bool(reuse),'remaining':manifest['pending'],'proof_note':'第8条forward-pay-budget-implies-free-kappa-budget.json为完整条件推导；candidate原ARB预算草稿只保发现记录，不列assets。','install_rule':'Boss串行安装与edge-bind --write/edge-check/checkpoint/done；worker从未写clone。'})
print(json.dumps({'edges':len(new),'sources':len(files),'cores':len(coverage),'linked':sum(x['state']=='linked' for x in coverage.values()),'isolated':sum(x['state']=='isolated-after-review' for x in coverage.values()),'canonical':reuse,'receipt_ready':bool(reuse)},ensure_ascii=False))
