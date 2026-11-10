from pathlib import Path
import json, hashlib, re
ROOT=Path('/workspace/scratch/bbb425bb840f/co-work-anl-boss6')
OUT=Path('/workspace/scratch/bbb425bb840f/boss6-staging/map-cag476-round43')
TASK='customer-attraction-3a-3a-476c2ac4e44ed290'
D=json.loads((ROOT/f'research/operations/map-v2/tasks/{TASK}.json').read_text())
TD=D['definition']; EDIR=Path('map/edges')/TASK
(OUT/EDIR).mkdir(parents=True,exist_ok=True);(OUT/'map/receipts').mkdir(parents=True,exist_ok=True)
rr=json.loads((ROOT/'research/registry.json').read_text())['objects'];rr=list(rr.values()) if isinstance(rr,dict) else rr
O={r['object_id']:r for r in rr}
I={
'fresh':'M-83989a1c488c41feba71945a83af2078','swing':'M-a4546084e30f41a68cb0fbdffbf3f15b','insurance':'customer-attraction/equal-value-last-replies-one-third-swing-and-five-player-full-insurance-budget',
'ind':'M-482bb579abd84fb39d3ea98cb587b33f','r4':'customer-attraction/r4-background-candidate-transport-obstruction','matched':'M-f1b40e09d6bd4fd0b70bb026d17134ac','hinge':'customer-attraction/maxroot-hinge-pricing-index-domains-and-frozen-discovery',
'coupon':'customer-attraction/net-coupon-row-uniform-subset-hull-and-local-prices','copy':'customer-attraction/first-deviation-source-copy-strict-future-migration-and-weighted-remainder','dr':'customer-attraction/finite-four-layer-dr-potential-full-slot-aggregate-deficit',
'mono':'customer-attraction/monotone-shapley-complementarity-anchor-dominance-unbounded-root-ratio','frequency':'customer-attraction/frequency-two-client-quadratic-fresh-safety-boundary','entrant':'customer-attraction/unscaled-entrant-float-outcome-and-full-strategy-cone-probes','replay':'customer-attraction/full-tree-sequential-replay-deleted-potential-endpoints',
'credit':'M-b83c6050d75e4252bbe71ed2e71569e6','reject75':'M-1e78e33744804d7a9a95653cc365083e','rent':'M-671448c4da884c49b65296697fb471c5','positive':'M-d668031578d94dd98aea2aedd90792e5','probe':'customer-attraction/background-aggregate-security-original-random-probe-lower-bound-contract','residual':'CA-RESIDUAL-NO',
'exact':'CA-EXACT-PURE-SPE-ALL','balance':'M-21108b01d92540379cb7c7227ec6ade3','exchange':'M-229d7c0b44324c27b2755e659b46d235','rentcost':'M-37ed3633879744afb8bccdd54383f00b','milp':'customer-attraction/fresh-quadratic-root-floor-joint-policy-milp-big-m-contract'}
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(rel,data):
 p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n' if not isinstance(data,str) else data)
 return {'path':str(rel),'sha256':h(p)}
def refkey(k,section=None):
 b=O[I[k]]['body'].copy()
 if section is not None:b['section']=section
 return b

# Every paragraph below is a mathematical comparison at the current pins, not a claim that the whole graph has no other relations.
C={
'fresh':('严格小保险子域的五经济块全异与完全效率',
'完整比较M-839...稀疏配对全历史归纳、同页局部摆动及全Cartesian预算。其a>2b严格fresh结论独立于等值末回复，且可允许删Cartesian配对；一般29/17预算不以此严格阈值为前提。将它限到目标全Cartesian、至少五等大经济块及actual全保险覆盖域，取b=max_K|K|且a>2b，实际五步各取未用经济块，故k=5，W=5a+B。任何五槽比较覆盖≤5a+B，实际本身可行，得W=OPT5。此为有用的严格子域贡献；a≤2b及没有actual全保险时的全局29/17须另用摆动证明。'),
'swing':('同保险背景等值末回复支付29/17证明的关键损失',
'逐客户3d+t≤c覆盖全部p≥0及三会员位，零分子按0；求和只在同一(p,K)且末位保险总收益相等时消t，得到损失≤actual保险覆盖/3，三客户例锐。完整Cartesian保证倒二只换fresh经济坐标后，末位在两条真实历史都能把每个保险主题配fresh经济块，因此末位经济利润同为a，保险最大值相同。真实当前IC于是给a(1−1/c)≤B_actual/3。这精确支付全保险预算，不能以任意跨枝总收益相等或p≤3的32型程序代替一般证明。'),
'insurance':('一般受限族29/17与严格小保险子域最优并存',
'固定同一五人完整σ，末位任意历史都fresh，actual至少两经济块；actual全保险使W=ka+B及OPT5≤5a+B。k≥3给≤5/3；k2迫前四同块且c4，局部1/3摆动给B≥9a/4，从而≤29/17。全Cartesian是保持保险坐标并共同最大化保险的承重条件，actual全保险是最后福利预算条件，两者均不可删。另在a>2max|K|子域，稀疏fresh核给k5并得W=OPT5。29/17未证明锐，原13/7与控制器11/8不冒成一般五人/六人结果。'),
'ind':('所有偏离孩子BG的IND不能与仅actual孩子结构互换',
'完整读R4整页及原候选。M-482...的假设是全部真实r−1偏离孩子均满足同一UNION-BG；对每个最优r槽元组每槽j，用该孩子最优值恰C_h*与该枝守恒得R_h*≤A_j+V_jtail=d_j+2V_jtail−B_j≤u+2V_jtail−B_j。这里B_j是活跃者在原U上的份额。R4另核只假设actual孩子BG，不能提供这些离轨孩子前提。要由IND支付父BG仍须有j令2V_jtail−B_j≤A_h+Vtail；标量凸混合成功已蕴含单个j成功。52例各分支给左12>右9，说明SWITCH不普遍成立，但不否定有明确孩子前提的IND。当前包无逻辑边把该附条件展开误当普遍BG。'),
'r4':('新增覆盖余额与静态EX1共同给全tuple每槽必要界',
'与R12及正式G余额、M229静态交换比较，均固定同一输入总体、实际父/孩子、完整σ及最优tuple。令C=|U|+M_r(U)，C′=|U∪A|+M_(r−1)(U∪A)，δ=C−C′。E_parent=G_parent=W+u+Vtail−C，E_child=G_child=S=W+Vtail−C′，故父失败等价δ>u+S。实际孩子BG只给S≥0。M229的k1/Y空EX1对每个最优tuple每槽给δ≤|P_j\\A|−|E_A|，合并得|P_j\\A|>u+S+|E_A|。若存在一个最优tuple有空P_j，则不可能父失败；少于r主题达到最优时重复合法补槽即得空私块，零支持边界同样保留。不是IND，也未反向把大私有块当收益保底或父失败充分机制。'),
'matched':('真节点p与u匹配后逐索引求和的161行',
'完整读匹配审查及maxroot整页。AB/AE强制T_i不是优化者，真正第四位k2、p=oldbg+t，u_x=r/(oldbg+t+r+s)；Sbranch真正第三位k3,p=a+t,u_x=h/(a+t+h+i+j)，真正第四位k2,p=a+t+h,u_x=i/(同分母)。统一HINGE先分别在这五个真索引历史成立，再同族完整直方图求和；共同d和菜单c保持同一五槽菜单。AB/AE各2×17，Sbranch3×14+3×17，合161。固定旧bits、共同d、全部maxbits后每新行只读一族，保条件分解；不平均p/u，不逐菜单另挑直方图。9179含selfIC/3220使用是四输入旧QA，未作本轮新全域核。'),
'hinge':('一般k域铰链与匹配索引投影的真实域',
'五人任意真节点余k2/3/4/5，p≤5−k，L=4(k−1)。同历史取同一加权最大H，五次BNS加t倍同H菜单容量后用hℓ≤ℓ_+消去，得ψ行。完整断点17/14/10/7使连续t≥0全族由端点承担，尾t≥L−1只弱化。用该已证方法在匹配AB/AE/Sbranch真节点给161行完整支持。它与k3双菜单是仿射重参但全k域不同；浮点6541行受限点1.994...和后续2.004...都不是SPE或精确全域证书，当前u不得从祖先cap搬来。'),
'coupon':('局部current支配凸包与终点HIT/钱包的分界',
'完整读局部三节、非盲核及九节点抽象DAG。阈值(1+|U_t|)dt混合给每个p_j≤p_i iff含current均匀子集凸包；任实λ_i,z的局部支持函数精确。合法SAFE/CLIP只给此抽象类中的行，不称每个顶点CAG可实现。future的z必须是完整续价，二层各半例终点1/4而即时角色价0，故局部PRICE不单独给全图终点价。九节点没有客户/完整σ，144/2187/64只是其固定回归合同。已知canonical ca-causal-closure-r34-same-context-to-hitting使用本核与额外SAFE/HIT端点；仅核其完整边合同和当前结构有效，不在本包未读全端点时重交此边。本包已声明端点内无新逻辑关系；这不是该对象在全图无边的断言。共同actual钱包/单券cap仍未付。'),
'copy':('source-copy严格未来税与广义密度/净券的支持错配',
'旧g第k位a=g_k，当前b，A=finish(g)、Q=finish(g,a)。COPY-IC为同历史整行动松弛，Q两位同a给u_l(Q)=u_k(Q)，后者不是actual u_k。tracked客户必须另保canonical/action-source支持a∩b；广义密度f≤1不能补a覆盖x。共享客户倒数差只有j>l迁移，完整和为P_Q−M_A+ell_copy；每正recipient≤同Q叶该客户半份额。WEIGHTED用一个整行θ乘IC，R=Σ(f−θ)δ无已证符号；多t的Q未来利润也不共用一个actual钱包。净券current支配、同law回放或单孩子prefix回推都不支付这些不同叶/不同源总金额。这里只保成熟局部恒等式，不造强连边或声称copy质量半收缩。'),
'dr':('显式有限四层DR反例已证，当前登记model/status须纠正',
'完整读70整数势、150含重复DR方格、80末层边际（与DR合付140单调边）、21策略/84含selfIC、12实际完整菜单及双审合同。actual012总边际效用8，全部菜单价11/4，总33/4，严格差1/4。它是三人四标签匿名删除边际势辅助模型，不是单位客户CAG；同一固定三人收益表也不可能非负客户实现：全000每人3⇒主题0总质量9，012主题0收益2<9/3。与monotone-Shapley不同，它给有限DR但没有共同覆盖效率/BC；正边际表示定理不能套到该势表。|q|≤4的有限证书不提供全n延拓。registry现model写单位客户且truth_status=finite，和body的已证精确存在性矛盾；保存最小修订建议，当前pin覆盖待metadata定向刷新，数学结论不降格为扫描。'),
'mono':('正边际共同表示支撑弱Shapley反模型的线性身份贡献',
'对每m≥2，P={a}∪D,|D|=m，C(S)=1_(a∈S)(1+|S∩D|/(m−1))+(3m/2)1_(D⊆S)。应用M-d668...全部低层PM/反演/E+BC，得到同一signed客户表示及非负收益（这里另用C单调）。原body另完整证明a对每个固定m−1对手弱占优，并对明确全历史恒a策略逐节点使用该比较，得W1、OPT_m3m/2、比率无界。本新边仅支付共同signed/E+BC/收益非负的精确部分；不从静态弱占优推出任意动态策略结论。二标签C(a)+C(b)−C(ab)=−1/(m−1)<0，已违反次模与非负客户；故不反CAG或单调次模Shapley。'),
'frequency':('频率二完整编译候选与fresh联合MILP的不同义务',
'完整读候选、联合MILP合同、旧171/591资源及新261/1116超时资源。频率二构造pair重数s(K−2β_ab)、private s(C+α_a−d_a)，在distinct终局严格给u_a=s(B+v_a)，s必须共同保留。核心目标却量化全部原CAG重复前缀/离轨、任意有理系数与m≤p，并要求θ_CAG=s(B+θ_fresh)。联合MILP精确编码的是无重复全部fresh历史与τ≤θ，不含重复CAG行动；其齐次盒不丢固定p,m严格fresh分离，但没有补编译阈值/重复节点义务。2288输入是有限回归，45秒近零primal非精确正反例也非全局上界；旧无primal报告更非不可行。高偏置安全边界OPT<2W不变成half反例。本包无完整推导完成通用compiler，不以一般Möbius编译代付精确频率二合同。'),
'entrant':('α1插入桥的真13人反例与有限裁剪零统计',
'完整读两探针合同与同packet八类型算术/资格分层。ENT1 mM1≤W+G1若真，逐客户OPT≤mM1+W−G1足推half；一般ENT1却已在13人36客户同完整SPE失败：actualP十次A两次B一次，W33,M1=3,G1=359/66，缺口37/66>0，仍OPT36<2W。成熟27243节点/112050IC资格按合同复用，未重新跑。m4p5的250及m5p7的140只是浮点LP计数，从零裁剪的0.0不是390精确最优零；终局screen与完整策略锥后验门也不同。α1不与α=(m−1)/m、残余M(C)、真正静态v_r或辅助DR混同。当前包未新增缩放或一般half关系。'),
'replay':('同law删槽端点抵消与异law自由列的额外付款',
'完整读回放代数、父审JSON及自由列合同。固定actual位置i，B枝后继在A枝逐位合法回放，Γ逐节点非负；删槽势望远镜给D_i(p)−C_i(p)。独立性只用于静态query，A/B同law只用于当前删槽势期望抵消。改B~q_i须保−[E_pΦ(V_i(A))−E_qΦ(V_i(B))]，不能自由挑最小列后仍免费抵消。最后槽删除差0，i=m两和空，i=m−1单后继非负；早位后继删除差无普遍符号。36例余额6/5=64/15−46/15精确显示跨势项可负；它不凭一次负项反一般AFC。source-copy的a∩b严格未来差与此任意独立双query分布不是同一前提，净券支配亦不给该当前端点。'),
'credit':('R12新增覆盖余额换名到正式G对象，保独立两层租金比较',
'对同一合法前缀与真实尾，R12 E=Gnew+P−M_r(B)，正式余额G=P_r+Δ_r−O_r(b)，以B={b>0}、Δ=Gnew、O=M完全同一。R12 δ=M_r−a−M_(r−1)，故L=u−δ，E_h=E_hA+u−δ即正式G递推；r0=0、r1真末位非负、空根2W−OPT及沿actual路径望远镜均保留。配套分式的全整数符号域由代数证明，不从2394扫描外推SPE。in-packet M37只在特定两层A/C/共同t满足两BR约束时强制u≥(b+2)c/2，固定叶删除守恒也不比较真实后继；它不付一般δ−u−S。因此不把旧租金失败尝试当背景E≥0。'),
'reject75':('75客户指定路径的全部真末BR严格拒绝',
'完整读审查正文、1768B原脚本、727B冻结输出、源重放审查及五源页§6。25遗漏对每类3个单位客户，目标(3,4,5,6,7)。前缀(3,4,5)第四改0，十末位收益精确向量的最大303/20只在1或2；二者均给第四303/20>151/10，严格增益1/20，所以任意完整SPE均不能实现指定路径。不是给定一棵完整坏SPE，也未否所有两加三路径。保险Cartesian与这里遗漏对结构不同；86客户输入及21策略锥各有独立owner，不能拼入本75客户证书。成熟精确证书复用，不新跑全树/LP。'),
'rent':('多真实互斥分支共享Q池不倍增有效根缺陷',
'完整读共享租金正文与稳定B四项税/全历史触发器。显式n≥2,K,s≥1族非末恒B、末无T取T否则B，在包括混合P_j/T的全部历史均为SPE；恒B也SPE。actualB^(n−1)T及各P_j真根分支共享同Q租金ε=s/(n−1)，不加权(K+1)ε可大，但W=(K+1)ns+s也随K长，OPT=(K+1)ns+min(n,K+1)s，仍half。最小根M=(K+1)s，h=M+ε，K分支不将h−M变Kε。一般逐客户Σ_vλ_v1_(x∈Q_v)≤1才支付一个B池，IC未产生这些权重。source-copy单Q半份额/净券逐行支配不能替代跨源共同cap，也不把五项各领一份K。'),
'positive':('全部低层E+BC等价PM，应用于明确单调互补C',
'完整读正式证明、12229字符原主稿全部五节及背景回路精确scope。任实共同截断C与全部1≤|q|≤m，PM系数β_R>0且总1/q_a；布尔反演给共同signed实现，E+BC按低层递推唯一确定同收益。固定终局同支持守恒、逐对切片、或收益非负不替代全部低层BC及非负客户。对本包monotone辅助C可合法应用这些线性身份，并由C单调推出U≥0；这正说明弱放松可具真实共同signed资料而仍根half失败。原9/4和15/7有限层不作为本新边证据，特别15/7旧层名不是完整两主题耦合。与既有signed+稀释→外部旧人租金canonical是不同目标，不重复。'),
'probe':('全集算法准确支付最差剩余利润选择，静态下界仍须合法p',
'完整读3803代码的正式合同、证据README及CA-EXACT完整归纳。全集R(prefix)恰含所有完整子SPE可实现最终总计数q，剩余总利润V(q;prefix)=Σ_{a:q_a>0}(q_a−prefix_a)U_a(q)仅依q，故min_R V恰为全部子SPE最低剩余利润；每个argmin可按原算法逐有序节点展开σ。探针本身未展开/独立验证或保存该σ，理论存在性不冒成一次已有完整输出。下界矩阵精确全r−1静态多重集，给定合法非负归一p̂的全行Fraction最小值≤v_r(b)，不需LP最优性；源码没有另assert p̂≥0或scale>0，均留认证前提。1500seed域的阴性旧说明没有完整stdout/输入日志，不外推一般聚合。follow-up与CA-EXACT的实际比较已在本包完成，无另建3B。'),
'residual':('M(C)逐人与聚合桥的14客户完整反例不反BG',
'完整读五主题14客户表与三桥审计合同。五末位回复均真BR，所有根真实偏离都得4，完整σ actualAB收益4/5，W9，actual遗漏主题T给M(C)=5，故u1<M及W<2M。OPT2=10，仍half；同末表根D另有W8，不声称最差，也不能把旧actualM5搬到DE。和R4比较：最优B/T私块各5且避A，但EA=A有4，δ=1、S=5，父坏差−8，故此例只反‘大私块必付root同大小利润’，不反PRIVATE-LOSS或BG；末位u_m≥M仍真。也不等多主题残余M_r(B)、最优并集遗漏量或静态v_r。当前包未把其精确被否桥强接到一个本身为真的目标节点。')
}

# Review content includes the complete new deductions; evidence points to these sections and exact source bytes.
intro='''# Boss6 round43：20核心的实质比较与当前pin交付草稿

本稿沿用Boss6，只读指定clone；不运行旧LP、随机主循环或完整策略树扫描，不改Git、队列、registry或原正文。数学来自本稿列出的实际完整阅读与成熟证据合同。所有比较固定各自模型、同一完整σ、同一客户总体及相应最优比较tuple；共享CAG定义不产生自动hub。

当前草稿仍保DR旧pin，供Root先durable保存、最小登记修订/refresh后fresh窄续。该对象是明确已证辅助反例，待修的是登记模型与层级；没有未付的反例数学证明。其余独立结果可复用。

'''
sections=[intro]
for n,k in enumerate([x for x in I if x in C],1):
 title,body=C[k];sections.append(f'## {n}. {I[k]}：{title}\n\n{body}\n\n')
sections.append('''## 新关系证明A：保险摆动与两个独立结论

一般预算：至少五个等大互不交经济块，每行动一个经济块加保险主题，全部Cartesian配对合法，actual覆盖全部保险宇宙。任意位置选择一个经济正质量行动，经济收益至少a/5>0，而全空行动收益0，所以所有真SPE节点均排除全空行动；因此actual用k=2块时，末位fresh确使前四个实际行动同一经济块，c=4。末位若用旧经济块，保同保险坐标改fresh严格增利，因此所有真末位fresh。actual倒二改fresh经济坐标后，两条末位所面对的保险背景相同，完整Cartesian使每个保险主题都可配fresh经济块并取同一经济收益a；故它们保险最大值相等。局部3d+t≤c求和付当前保险损失≤B/3。若倒二原经济块在前四人出现c次，真实IC给a−a/c≤B/3。actual用k2块时c4，得B≥9a/4；k≥3时无需此界。以W=ka+B、OPT5≤5a+B逐区间得到29/17及5/3。这推完整目标，没有用a>2b。

独立严格子域：若每保险主题≤b且a>2b，稀疏fresh全历史逆归纳已使五实际经济块全异。放回目标actual全保险域，W=5a+B，OPT5既≤5a+B又≥actual W，故W=OPT5。这只付严格子域，不拿它证明a≤2b。

## 新关系证明B：HINGE到161真实索引行

源k2/3一般铰链量化所有真节点与任意两五槽合法菜单。对AB、AE每个强制T_i后的真正第四位分别用该历史自己的p=oldbg+t、u_x=r/(oldbg+t+r+s)；对Sbranch分别用真正第三/第四位的p与h或i份额。每个索引独立选本历史最大H并消去，再相加；相同d/c在整族五个索引固定，得到Σ_θ n_θψ(p_θ,k,u_θ,d,c;t)。断点数17/14给34+34+93=161。因每项只读该family及固定旧bits/d/maxbits，保条件分解；共享d不能分族重新优化，同family多菜单也不能换直方图。这完整推出匹配源合同中的普遍行与分解，不赋予浮点全域最优或共同策略可实现性。

## 新关系证明C：R12到正式余额，再与EX1联合到R4

令合法前缀负载b的旧覆盖U={b>0}。R12的M_r(U)是正式O_r(b)，R12的新增覆盖Gnew是正式Δ_r，R12的利润P是正式P_r，因此E_h=G_r。实际当前A新增a，R12机会损失δ=M_r(U)−a−M_(r−1)(U∪A)，正式L=u+a+O_(r−1)(b+1_A)−O_r(b)=u−δ。故R12的E_h=E_hA+u−δ完整给正式G递推；r0=0、r1真末BR基例和空根G=2W−OPT也完全相同，沿实际路径相加即目标望远镜。此方向不反称正式G对象还包含R12的附带容量分式。

再使用正式G对象和静态交换owner M229作一条ALL边。写父最优总覆盖C=|U|+O_r(b)，actual孩子最优C′=|U∪A|+O_(r−1)(b+1_A)。同一实际总覆盖W、当前终局收益u、实际尾利润Vtail给G_parent=W+u+Vtail−C，G_child=W+Vtail−C′=S。G递推使父坏差C−W−u−Vtail=δ−u−S。actual孩子BG等价S≥0；父失败因此δ>u+S。

对任一达到C的r槽最优tuple T，取P_j=T_j\\(U∪⋃_(k≠j)T_k)，E_A=A\\(U∪⋃T)。M229的ME在k1/Y空，即其EX1，给C′≥C+|E_A|−|P_j\\A|，也即δ≤|P_j\\A|−|E_A|。两式合并，得到每个tuple每个槽同时|P_j\\A|>u+S+|E_A|。存在空私块的最优tuple直接矛盾；最优可用≤r−1主题时合法重复补槽，零支持时任意合法主题也在U内，所以完整低支持继承边界成立。该联合从未假设所有偏离孩子BG，也未使用IND的分支尾利润；更未证明普遍BG为真。

## 新关系证明D：正边际表示对单调互补反模型的贡献

对任m≥2，固定P={a}∪D、|D|=m，β=1/(m−1)、K=3m/2与C(S)=1_(a∈S)(1+β|S∩D|)+K1_(D⊆S)。C是全域归零单调函数。M-d668的PM与布尔反演在全部低人口层给共同signed表，其收益等于有标号槽Shapley分摊；PM的正系数乘本C非负边际使U≥0，全部层E+BC成立。这里只支付目标中共同signed/E+BC/非负收益身份。a的固定对手弱占优、恒a完整SPE与W/OPT计算在目标正文已有独立完整证明；不由本部分身份单独推出，更不由静态弱占优推出任意动态SPE结论。C(a)+C(b)−C(ab)=−β已排除非负客户与次模，不能在贡献后删掉辅助模型边界。

## 新关系证明E：全集到最低剩余利润选择

固定合法prefix计数k与r=m−|k|。CA-EXACT归纳恰给每个完整有序子SPE可实现终计数集合R(k)，每个q∈R(k)可逐有序历史独立拼接实现。给定q，suffix中选a的人数是q_a−k_a，故全suffix利润严格为V(q;k)=Σ_{a:q_a>0}(q_a−k_a)U_a(q)。取min_(q∈R(k))V既不遗漏任何完整子SPE，也不纳入不可实现q，有限性使最小值达到；任选argmin可按CA-EXACT的证书构造展开。计数缓存集合不要求同计数有序历史同平局。这支付probe的最差利润选择，尚不声称probe驱动已展开/保存/独立验证该策略。

该贡献也不认证float LP的最优性或有理化后的概率合法性。只有另核p̂≥0、Σp̂=1，静态全部r−1多重集矩阵的Fraction min才是v_r的有效下界。原1500轮没有可借的完整stdout/阴性JSON；理论正确算法不替代一份实际保存的独立反例证书。

## 当前实际未付义务与处置

数学开放义务：IND的跨枝SWITCH一般不成立，不能继续当待证普遍命题；改变前提的新桥仍须另说明。source-copy的R符号、整行θ共同预算、多Q到actual钱包未付。净券局部凸包不付actual券cap/共同钱包。frequency2的一般完整重复历史/阈值编译及fresh根/逐人floor没有在此包闭合。早位回放删槽和与异law当前端点仍无统一付款。共享租金各源权重的逐客户共同容量未由IC给出。真正背景聚合安全桥与恰六人/一般half均未由本包解决。

这些不等同于目标自身已证部分尚欠证明：保险29/17、两条余额/交换关系、匹配161、正边际线性贡献和全集最低利润方法在各自精确条件下论证完整；单调互补反模型、DR明确有限辅助反例、75客户指定路径拒绝、14客户残余桥反例本身均已证。DR当前仅有metadata修订/刷新义务。背景probe↔CA-EXACT follow-up本包已实质解决，不另发布3B；两个in-packet对只记实际比较，不放closed_overlaps。
''')
review=save(EDIR/'comparison-review.md',''.join(sections))

# Complete actual reading ledger: full files really displayed, two long pages only their exact requested sections.
seen={}
for x in TD['context_plan']['reading_refs']:
 key=x['path']; p=ROOT/key
 assert h(p)==x['sha256'],(key,h(p),x['sha256'])
 if key not in seen:
  only=key.endswith('五人半覆盖上传证书与个体安全运输尾部五源接续审查--审查.md') or key.endswith('固定背景共同客户回路的适用范围与接续--资源.md')
  z={'path':key,'sha256':h(p),'reading_mode':'exact-section-complete' if only else 'whole-file-complete','whole_file_lines':len(p.read_text().splitlines()),'execution':'not executed; mature mathematical/evidence contracts read'}
  if only:z['sections']=[x['section']]
  else:z['actual_lines']=[1,len(p.read_text().splitlines())]
  seen[key]=z
for k,secs in [('balance',None),('exchange',['多槽交换ME/MM的全部静态内容'])]:
 b=refkey(k);p=ROOT/b['path'];z={'path':b['path'],'sha256':h(p),'reading_mode':'whole-file-complete' if secs is None else 'exact-section-complete','execution':'not executed; analytic proof read'}
 if secs:z['sections']=secs
 else:z['actual_lines']=[1,len(p.read_text().splitlines())]
 seen[b['path']]=z
for p,sec in [('archives/customer-attraction/state/引理/最优补全私有块交换与分支账本--引理.md','不需要均衡假设的交换关系'),('archives/customer-attraction/state/引理/最优替换基数与同叶中继的净遗漏边界--引理.md','任意合法静态替槽的正确方向')]:
 seen[p]={'path':p,'sha256':h(ROOT/p),'reading_mode':'exact-section-complete','sections':[sec],'execution':'not executed; pure static proof read'}
canonical=[{'path':'map/edges/customer-attraction-3a-3a-7b5d2e180fc235e1/same-context-to-hitting.json','sha256':'b909deebb014a18c351e33b331b53f973bed3c874b7fcccabed9d43139a78fe5','edge_id':'ca-causal-closure-r34-same-context-to-hitting','disposition':'navigation-only; current exact edge contract read and read-only edge-check passed; outside declared endpoint comparison, not re-submitted'}, {'path':'map/edges/customer-attraction-3a-3a-3cdc3f8b2e711f10/signed-and-dilution-pay-incumbent-rent.json','sha256':'4545957cd62d23f0f2165af481cf9e7b11fa105f4e621a523cb6a9640acc657c','edge_id':'cag-3cdc3f8b-signed-and-dilution-pay-incumbent-rent','disposition':'navigation-only; different rent target, not re-submitted; read-only edge-check passed'}]
ledger=save(EDIR/'reading-ledger.json',{'schema':1,'task_id':TASK,'owner':'Boss6','request_id':D['request_id'],'task_definition_sha256':h(ROOT/f'research/operations/map-v2/tasks/{TASK}.json'),'scope_note':'All original 48 requested refs are covered by 44 distinct files; duplicates read in their complete common file. Added CA-EXACT body was already one original requested whole file. M211 whole body and M229 exact body/evidence sections are additional real reads; no claim to have reread the many CA-EXACT implementation evidence pages or prior raw mathematical programs. Registry model/statement/quantifiers/assumptions/scope/objections/body/evidence reviewed for all core/read endpoints; source locator arrays are navigation, not a claim to read all pointed raw sources.','instruction_files':[{'path':p,'sha256':h(ROOT/p),'reading_mode':'whole instruction file read; IMPLEMENTATION truncation gap subsequently read at lines105-155'} for p in ['AGENTS.md','research/IMPLEMENTATION.md','prompts/03-map-worker.md']], 'readings':list(seen.values()),'mathematical_execution_count':0,'structural_checks':['all read file SHA values checked against task exact refs','canonical adjacency scan for actual local relation deduplication','two mature external canonical edge-check calls, both exit0; structure is not mathematical verdict'],'canonical_navigation':canonical,'new_direction_deduplication':'No canonical edge touched M211 or M229 at scan; no existing canonical has the new local R12→G or ALL(G,EX1)→R4 target relation. The two known external canonical edges remain unchanged.'})
old=O[I['dr']]
proposal=save(EDIR/'registration-correction-proposal.json',{'schema':1,'object_id':I['dr'],'current_version':old['version'],'current_registration_pin':TD['input_pins'][I['dr']],'disposition':'Root-only minimal registry edit, then version/pin refresh and fresh narrow continuation; no body edit proposed','old_fields':{k:old[k] for k in ['truth_status','model','statement','quantifiers']},'new_fields':{'truth_status':'proved','model':'有限共同标签P={0,1,2,3}的三人匿名删除边际势辅助博弈；非负单调DR势φ定义在全部|q|≤4多重集，φ(0)=0，终局收益u_j(z)=φ(z)−φ(z删j)。不假定客户表示；完整策略定义于全部有序历史，标签可重复，允许离轨平局。','statement':'存在正文给定的70项整数四层势φ、21节点完整三人纯SPE σ及独立均匀查询p=(1/4,1/4,1/4,1/4)：全部12个实际完整菜单列价格均11/4，故Σ_i min_A G_p(Z_i(A))=33/4>8=Σ_i u_i；同一三人终局收益表不可能由非负客户均分实现。','quantifiers':'存在这份明确有限四层势、完整有序历史策略与uniform查询，精确反驳任意有限层非负单调DR匿名删除边际势类上的SUMmin-full全称桥；不声称全n延拓或原非负客户CAG反例。'},'unchanged_fields':['object_id','kind','assumptions','scope','body','evidence','sources'],'rationale':'精确显式有限反例存在性已由完整表与解析证明支付，finite仅用于有限扫描观察；现model的单位客户前提与正文明确非CAG及固定三人不可能客户表示矛盾。','evidence':[refkey('dr'),O[I['dr']]['evidence'][0]],'exact_paid_proof':'70势值/21完整策略/84IC/150DR/140单调边/12菜单；actual012收益2,3,3、SUMmin33/4−8=1/4。000每人3迫主题0总质量9，012的0收益2低于9/3=3，解析排同固定三人非负客户实现。','limits':['Only |q|≤4, no infinite extension','Auxiliary deletion-marginal game, not original CAG','No general or six-provider half claim','No new mathematical program run in this map review']})

# Edge evidence points to exact source bytes and this self-contained deduction review, with no circular edge hashes.
def edge(name,sources,targets,conditions,roles,explanation,scope,proofsec,refs,whole=None,contrib=None):
 e={'edge_id':'cag-476-r43-'+name,'kind':'implies','status':'accepted','source_ids':[I[k] for k in sources],'target_ids':[I[k] for k in targets],'premises_mode':'all','relation_mode':'unconditional','conditions':conditions,'roles':{I[k]:v for k,v in roles.items()},'explanation':explanation,'scope':scope,'evidence':refs+[dict(review,section=proofsec)],'reviewed_by':'Boss6','review_note':'实际完整读取所列核心正文/承重证明与精确必要依赖；按本边显示的模型、方向、全部量词和结果范围逐句核对。成熟证据合同复用，本轮不重跑旧LP/全树/随机程序。'}
 if whole is not None:e['whole_result']=whole
 if contrib is not None:e['contribution']=contrib
 return save(EDIR/(name+'.json'),e)
assets=[review,ledger,proposal]
assets.append(edge('equal-insurance-swing-to-full-cartesian-budget',['swing'],['insurance'],
'五人；至少五个等大a>0互不交经济块，保险宇宙I与经济不交；全部经济×保险Cartesian配对合法，可附全空动作而无破坏结构的其它动作；固定同一份完整有序历史纯SPE且actual覆盖全部I。所有改变经济坐标的行动和后继均取原σ真实完成。',
{'swing':'给同一保险(p,K)下两个保险收益等值真末回复造成的当前保险利润损失≤actual保险覆盖/3。','insurance':'将倒二fresh经济坐标复制的真实IC与该局部摆动合并，完成k2/k≥3全部预算。'},
'末位保同保险坐标改fresh经济块可严格增利，故每个真末回复经济独享a。倒二把经济坐标换fresh、保持K时，前三人保险负载p与K不变；完整Cartesian让末位每保险主题都可配fresh经济块，所以两真实末回复最大化同一保险目标，总保险收益相等。若倒二实际经济块在前四人中用c次，则真实IC和source摆动给a(1−1/c)≤B/3。actual用k2块时前四同块，c4，得B≥9a/4；actual全保险W=2a+B，OPT5≤5a+B，故比≤29/17。k≥3时同两式直接给≤5/3。末位fresh排k1，因此覆盖全部目标情形。',
'完整目标的受限五人全Cartesian且actual全保险结论；1/3局部锐不表示29/17锐，也不外推任意目录或六人。',
'新关系证明A：保险摆动与两个独立结论',[refkey('swing'),O[I['swing']]['evidence'][0]],
whole='上述全部五人完整SPE的末位均fresh；若actual只用两经济块，则B≥9a/4；若至少三块则OPT5/W≤5/3；综合得OPT5≤(29/17)W。'))
assets.append(edge('sparse-fresh-to-small-insurance-optimality',['fresh'],['insurance'],
'在目标全Cartesian五人族中另限b=max_K|K|且a>2b；至少五个等大经济块、保险宇宙与经济不交、actual覆盖全I；每个经济块至少一个合法配对，允许全空动作。',
{'fresh':'对所有有序历史完整子SPE给当前经济块从未使用，因此actual五块全异。','insurance':'得到该目标中严格小保险参数子域的更强完全效率。'},
'将全Cartesian目录视为source允许的稀疏配对特例。a>2b给任一实际位置选择此前未用经济块，五位置经济并集为5a。actual全保险使W=5a+B；任意五槽比较最多五经济块及I，故OPT5≤5a+B=W。actual本身是合法五槽又给OPT5≥W，故W=OPT5。该推导不需要等值末回复摆动，不把source列作一般29/17证明必要前提。',
'目标的a>2max|K|子域；独立加强，不覆盖a≤2b或没有actual全保险。',
'新关系证明A：保险摆动与两个独立结论',[refkey('fresh')],
contrib={'result':'在目标全Cartesian及actual全保险结构内，若a>2max_K|K|，则actual五个经济块全异且W=OPT5。','remaining':'目标还量化a≤2max|K|的其它参数；一般29/17预算由等值末回复1/3摆动另付。本边不覆盖这些参数，也不删除actual全保险条件。'}))
assets.append(edge('universal-hinge-to-matched-161',['hinge'],['matched'],
'固定同一五人完整有序历史纯SPE及其AB/AE/Sbranch真实索引叶；比较T与各回复菜单都是同目录五槽合法菜单，共同d/c不依当前索引改选；真正p与当前份额u来自同一精确索引历史。',
{'hinge':'给全部k2/3真节点的统一ψ不等式和17/14完整断点。','matched':'在四类真节点逐索引应用并同族直方图求和，得到161行与条件分解。'},
'AB/AE强制T_i后真第四位使用p=oldbg+t,k2,u_x=r/(oldbg+t+r+s)，两菜单各17断点，故每族34。Sbranch真第三位用p=a+t,k3,u_x=h/(a+t+h+i+j)，真第四位用p=a+t+h,k2,u_x=i/(同分母)，三菜单分别14/17断点，合93。每个索引在其本历史先应用source HINGE再相加，得到Σθnθψ(pθ,k,uθ,d,c;t)≥0，绝不平均p/u。每新系数仅读同族直方图及已固定旧bits/共同d/全部maxbits，故保三个family条件分开定价；同族多个菜单仍在同一完整直方图上联合评价。34+34+93=161，给目标全部普遍行和分解结论。',
'完整匹配161合同；不把强制T_i作优化者，不认证四输入以外新QA、浮点oracle精确最优或跨族SPE实现。',
'新关系证明B：HINGE到161真实索引行',[refkey('hinge'),refkey('matched')],
whole='对所有同一五人完整σ的三索引族、全部合法菜单与完整断点，AB/AE各34及Sbranch93共161匹配真节点铰链行成立；固定旧bits/共同d/全部maxbits后每行只依单族完整直方图，保条件分解。'))
assets.append(edge('r12-credit-to-background-balance',['credit'],['balance'],
'同一个有限单位客户输入、同一合法有序前缀负载b与旧覆盖U={b>0}、同一固定完整策略的实际尾；R12新增覆盖按U扣除而利润仍含旧客户份额，O0=M0=0。最后一人非负基例另限真最佳回复。',
{'credit':'提供E_h=E_hA+u−δ、δ=M_r−a−M_(r−1)、r0/r1端点。','balance':'在Δ=新增覆盖、P=尾利润、O_r=M_r(U)、G=E的精确变量对应下得到目标整条余额分解。'},
'取R12 M_r(U)=正式O_r(b)，R12 Gnew=正式Δ_r，R12 P=正式P_r，所以E_h=G_r。当前A新增a给δ=O_r(b)−a−O_(r−1)(b+1_A)，因此正式L=u+a+O_(r−1)−O_r=u−δ。source递推即G_r=G_(r−1)+L，沿同一实际路径由G0=0望远镜得到ΣL。空根P=Δ=W且O=OPT，故G=2W−OPT；r1真实末BR给O1≤u并保Δ≥0，故G1≥0。恒等式本身不需SPE，所有子式都取同一输入/真实路径。该单向whole不反称目标还给source附带的容量分式，也不推出普遍G≥0或L≥0。',
'目标整条新增覆盖余额分解及明确端点；一般背景信用仍被52客户actual前缀反驳。',
'新关系证明C：R12到正式余额，再与EX1联合到R4',[refkey('credit'),refkey('balance')],
whole='对任意合法背景和固定完整实际策略路径，正式G_r=P_r+Δ_r−O_r恰满足G_r=G_(r−1)+L，L=u+a+O_(r−1)(b+1_A)−O_r；G0=0并沿actual路径望远镜，空根G_m=2W−OPT_m，r1的真末位SPE子局G1≥0。'))
assets.append(edge('balance-and-static-exchange-to-r4-private-blocks',['balance','exchange'],['r4'],
'同一有限输入、合法旧覆盖U及其真实负载b、同一完整子SPE父/actual孩子、同一个达到父C的r槽最优tuple；只假设actual孩子BG即S=W+Vtail−C′≥0，并在必要界部分假设父BG失败。静态EX1按比较槽保留重复，E_A随所选最优tuple并集定义。',
{'balance':'保E=G、L=u−δ的实际父/孩子缺口，父坏差=δ−u−S。','exchange':'已登记静态ME的k1/Y空投影EX1，对每个最优tuple每槽给δ≤|P_j\\A|−|E_A|。','r4':'联合得到全最优tuple全槽的严格私有残块必要界及低支持继承。'},
'置C=|U|+O_r(b)，C′=|U∪A|+O_(r−1)(b+1_A)，δ=C−C′，actual总覆盖W。source balance给G_parent=W+u+Vtail−C，G_child=W+Vtail−C′=S，父失败当且仅当δ>u+S。source exchange在P=U,S=A、最优tuple T及k1/Y空时，以P_j=T_j\\(U∪⋃_(k≠j)T_k)、E_A=A\\(U∪⋃T)给C′≥C+|E_A|−|P_j\\A|。因此对每个tuple每个j有|P_j\\A|≥δ+|E_A|>u+S+|E_A|。若存在一个最优tuple含空P_j，u≥0、S≥0、|E_A|≥0使此严格界不可能，故actual孩子BG推出父BG。最优由≤r−1主题达到时可重复补槽得空私块；零支持时全部主题在U内，也能合法补槽。本推导无全部离轨孩子BG前提，不用IND，不把必要大块反读成保底。',
'目标whole：每个最优tuple每槽的必要界及存在一个空私块/低支持时的BG继承；不证明普遍BG或SWITCH。',
'新关系证明C：R12到正式余额，再与EX1联合到R4',[refkey('balance'),refkey('exchange'),{'path':'archives/customer-attraction/state/引理/最优补全私有块交换与分支账本--引理.md','sha256':'5bdc6de1c6e8aa7163903d8339badd8b757e8c1836c21ae6d320c4fe99cc2d8e','section':'不需要均衡假设的交换关系'},refkey('r4')],
whole='若同一actual孩子BG成立而父BG失败，则任一达到父C的r槽最优tuple的每槽j同时满足|P_j\\A|>u+S+|E_A|；因此存在一个最优tuple含空P_j，特别最优由≤r−1主题达到时，actual孩子BG足以推出父BG。'))
assets.append(edge('positive-marginals-to-monotone-signed-boundary',['positive'],['mono'],
'每个m≥2固定同一个P={a}∪D、|D|=m、β=1/(m−1)、K=3m/2与全域C(S)=1_(a∈S)(1+β|S∩D|)+K1_(D⊆S)；使用有标号行动槽Shapley，重复标签不先合并。PM/E/BC保所有低人口层并始终同一C。',
{'positive':'提供任实共同C的signed实现、PM及全部低层E+BC；其正系数与此C单调合给全部收益非负。','mono':'支付目标中辅助反模型仍具共同signed身份、效率/平衡贡献及非负收益的准确部分。'},
'C由锚unanimity、β倍AND(a,b)和K倍全卫星unanimity非负和构成，因此归零单调。source布尔反演给同一张signed客户表实现全部C；有标号槽Shapley边际等于该表均分收益，source PM给全低层共同收益并满足E+BC。因本C的每个边际非负且PM系数正，所以全部终局收益非负。该结论不是说signed表非负；任卫星b有C(a)+C(b)−C(ab)=−β<0，故非负客户和次模已失败。本贡献不从这些线性身份推导动态福利。',
'精确局部贡献；目标的弱占优、明确恒锚完整SPE和无界比由目标body独立完整计算，非本贡献单独所得。',
'新关系证明D：正边际表示对单调互补反模型的贡献',[refkey('positive'),refkey('mono')],
contrib={'result':'上述每m≥2单调互补C的全部低人口层收益属于一份共同signed客户表示，等于有标号槽Shapley分摊，满足全部E+BC且收益非负；该C同时在二标签违反次模/非负客户必要性。','remaining':'整条目标中的锚对每个固定对手弱占优、恒a策略在全部有序历史为SPE以及W1/OPT3m/2/根比无界，依目标正文另有已完成的直接证明；本部分身份不单独推出这些结论，也不外推非负客户CAG。'}))
assets.append(edge('exact-outcomes-to-worst-background-profit',['exact'],['probe'],
'固定有限非负整数单位客户输入、合法prefix计数k、剩r≥1、总人数m=|k|+r；R(k)为规范精确全集而非浮点screen或一个平局选择器。当前仅论证最差剩余总利润选择，不对任何随机运行输出作存在性补造。',
{'exact':'给R(k)恰为全部完整子SPE可实现终计数且每个目标可逐有序历史展开。','probe':'允许从R(k)取V(q;k)=Σ_{a:q_a>0}(q_a−k_a)U_a(q)的精确最小值作为最低剩余利润。'},
'每份完整子SPE的终计数q由source必要性在R(k)；每个q∈R(k)由source充分性可拼接完整有序子SPE。固定q后剩余选a人数恰q_a−k_a，故suffix总利润严格为V(q;k)，不含旧k_a玩家租金。有限集合上min_R V于是恰是所有完整子SPE最低剩余利润，最小值达到；argmin可由source证书构造逐有序节点独立展开，不要求同计数历史同续局。该理论可实现性和实际展开/独立全树验证的执行证据分别保留。静态p̂下界矩阵和概率合法性仍按probe自身合同，算法不补p̂≥0检查。',
'最差剩余利润选择的完整局部支持；不称驱动已导出/独立验证σ、不称精确静态v_r、一般聚合安全桥或1500轮新阴性。',
'新关系证明E：全集到最低剩余利润选择',[refkey('exact'),refkey('probe')],
contrib={'result':'对任合法prefix，min_(q∈R(prefix))Σ_{a:q_a>0}(q_a−prefix_a)U_a(q)恰为全部完整历史子SPE的最低剩余总利润；每个argmin有可逐有序历史展开的完整策略实现。','remaining':'probe驱动本身没有展开/保存该目标策略或调用独立全树验证；合法概率p̂的非负/归一及scale条件、静态全部行下界、实际反例输出和执行绑定须另付。理论选择正确不认证历史随机阴性或一般聚合定理。'}))

# Coverage uses only actually declared endpoints. The pending M211/M229 read-add must complete before Root binds/install/done.
edge_map={
'fresh':['sparse-fresh-to-small-insurance-optimality'],'swing':['equal-insurance-swing-to-full-cartesian-budget'],'insurance':['equal-insurance-swing-to-full-cartesian-budget','sparse-fresh-to-small-insurance-optimality'],
'r4':['balance-and-static-exchange-to-r4-private-blocks'],'matched':['universal-hinge-to-matched-161'],'hinge':['universal-hinge-to-matched-161'],'mono':['positive-marginals-to-monotone-signed-boundary'],'credit':['r12-credit-to-background-balance'],'positive':['positive-marginals-to-monotone-signed-boundary'],'probe':['exact-outcomes-to-worst-background-profit']}
cov={}
for k,(title,body) in C.items():
 row={'state':'linked' if k in edge_map else ('needs-decision' if k=='dr' else 'isolated-after-review'),'object_pin':TD['input_pins'][I[k]],'comparison_scope':title+'；完整实际阅读与边界见comparison-review相应核心节及reading-ledger。','reason':body}
 if k in edge_map:row['edge_ids']=['cag-476-r43-'+x for x in edge_map[k]]
 cov[I[k]]=row
assert set(cov)==set(TD['object_ids'])
manifest=save(EDIR/'manifest.json',{'schema':1,'task_id':TASK,'owner':'Boss6','request_id':D['request_id'],'draft_status':'current-pin-complete-mathematics; pending DR metadata refresh/fresh continuation and Root binding','new_files':assets,'canonical_reuse':[],'canonical_navigation':canonical,'no_hash_cycle':'This manifest hashes neither itself nor receipt. Receipt may include this manifest as an asset. Root must update edge/receipt/manifest hashes after canonical edge binding.','source_freshness':'All original requested source hashes checked. Do not refresh any source body; DR proposal changes registry fields only.'})
receipt={'coverage':cov,'assets':assets+[manifest],'closed_overlaps':[{'core_id':I['probe'],'peer_id':I['exact'],'reason':'本包已完整实读CA-EXACT的必要/充分/非空及有序证书展开，与probe同prefix的V(q;k)精确比较；R(k)全部可实现终计数加V只依计数完整支付最差剩余总利润选择，局部支持边cag-476-r43-exact-outcomes-to-worst-background-profit已交。probe驱动未展开/独立核目标σ和概率合法性仍另列，不构成未做的比较。本pair无需额外3B。'}],'follow_up_tasks':[],'delivery_note':'当前pin数学成熟草稿，DR旧model/status待Root最小修订并refresh后fresh窄续。所有Git/队列/规范修改与最终edge-bind/check/checkpoint/done由Root串行。不得以此草稿直接done。'}
rec=save(Path('map/receipts')/(TASK+'.json'),receipt)
print(json.dumps({'request_id':D['request_id'],'counts':{s:sum(x['state']==s for x in cov.values()) for s in ['linked','isolated-after-review','needs-decision']},'edges':len(edge_map),'new_edge_files':7,'receipt':rec,'manifest':manifest,'total_read_files':len(seen),'undeclared_pending':[I[x] for x in ['balance','exchange'] if I[x] not in TD['read_object_ids']]},ensure_ascii=False,indent=2))
