from pathlib import Path
import json,hashlib,sys
root=Path('/workspace/scratch/bbb425bb840f/co-work-anl-boss6')
out=Path('/workspace/scratch/bbb425bb840f/boss6-staging/map-cag59aa-round48')
sys.path.insert(0,str(root/'tools'))
import research_runtime as rr
registry=json.loads((root/'research/registry.json').read_text()); objects={o['object_id']:o for o in registry['objects']}
task_path='research/operations/map-v2/tasks/customer-attraction-3a-3a-59aab9449e77a9e4.json'
task=json.loads((root/task_path).read_text()); d=task['definition'];tid=d['task_id']
erel='map/edges/'+tid; edir=out/erel;edir.mkdir(parents=True,exist_ok=True)
receipt_path='map/receipts/'+tid+'.json'; (out/'map/receipts').mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def ref(p,section=None):
 v={'path':p,'sha256':sha(root/p)}
 if section:v['section']=section
 return v
ids=d['object_ids'];S1,S2,S3,BD,AP,NF,CY,MID,TWO,ST,H,INT,D,CORE,RESET,CR,REST,PROD,BG,CAP=ids
PM='customer-attraction/prefix-monotone-benchmark-minimal-leader-failure-and-branch-outside-expansion'
DP='M-3b33bff2ccf041a9a82eb35664d00a69';ML='M-425fa58f82324fee96bc65a77ecb333a';OB='CA-OBLIVIOUS-MIXED-SECURITY-2N1';PAIR='M-d2a4dbe6afaf49878f1132e3d59186be'
static=objects[S1]['body']['path'];extra=objects[NF]['body']['path'];defect=objects[D]['body']['path'];hbody=objects[H]['body']['path'];construct=objects[BD]['body']['path'];menu=objects[RESET]['body']['path'];credit=objects[CR]['body']['path'];restart=objects[REST]['body']['path'];floor='archives/customer-attraction/state/定理/末两人逐人保底与全人数弱福利界--定理.md'
edges=[]
def edge(name,kind,src,tgt,mode,conditions,roles,explanation,scope,evidence,whole=None,contrib=None):
 e={'edge_id':'ca-b6-r48-'+name,'kind':kind,'status':'accepted','source_ids':src,'target_ids':tgt,'premises_mode':'all','relation_mode':mode,'conditions':conditions,'roles':roles,'explanation':explanation,'scope':scope,'evidence':evidence,'reviewed_by':'Boss6','review_note':'本包fresh worker实读当前登记完整陈述、域/量词/全部承重正文与所列证据；独立逐式比较，无旧数学程序、LP、BI或全树审计重跑。'+scope}
 if whole:e['whole_result']=whole
 if contrib:e['contribution']={'result':contrib[0],'remaining':contrib[1]}
 proved_source_domain_names={
  'slack-zero-rigid-optimal-load',
  'rigid-load-at-actual-prefix-payment',
  'static-count-converts-dominance-payment',
  'static-count-converts-positive-defect-payment',
 }
 conditional_source_names={
  'prefix-monotone-to-integer-extra-one-normal-form',
  'positive-defect-integer-parameter-reduction',
  'zero-positive-defect-recovers-load-dominance',
 }
 domain_review_notes={
  'slack-zero-rigid-optimal-load':'本边在目标本来的Δ0静态锐性域内完整推出S2；Δ0是目标适用条件，不是额外开放证明前提。固定p的精确slack及对所有最优Qprime的排除均已支付；不获得实际SPE前缀。',
  'rigid-load-at-actual-prefix-payment':'本边证明目标自身的条件命题：静态锐性且给定完整SPE实际前n−1槽负载=L时逐人付款。此前缀相等是目标适用域，不是本边另需研究的证明步骤；没有推出任意SPE自动满足它。',
  'static-count-converts-dominance-payment':'本边只宣称H已给W≥mθ(h)≥mv时静态计数界完成最后系数转换；既定H及实际尾保底是目标原适用域。contribution.remaining已明确其它证明组件，不将它们或H普遍成立冒作本边结论。',
  'static-count-converts-positive-defect-payment':'本边只宣称给定完整SPE已满足存在D≤s/2且真实尾保底时，静态v界完成half最后系数转换；small-D是目标原适用域，未证明其普遍存在。contribution.remaining保留叶账、尾保底及参数条件。',
  'prefix-monotone-to-integer-extra-one-normal-form':'源对象整体登记conditional，按该完整源合同保留conditional；本边已证的最小失败限制域推导无新增缺步。G=v_(r+1)的具体PM和末位基例均已在边内支付，普通合法历史不另充开放前提；仍不声称F成立或跨根信用可合付。',
  'positive-defect-integer-parameter-reduction':'源对象整体登记conditional，按该完整源合同保留conditional；本边已证的限制域推导无新增缺步，普通合法叶/整数参数不另充开放前提。此处只用D的已证定义与整数hinge代数，不使用small-D存在；未枚举或认证全部SPE。',
  'zero-positive-defect-recovers-load-dominance':'源对象整体登记conditional，按该完整源合同保留conditional；本边已证的D0=H限制域推导无新增缺步，普通合法叶/固定总权参数不另充开放前提。贡献只含H条件福利与LA/LB等价；独立85节点扩类证据仍按contribution.remaining另承。',
 }
 if name in proved_source_domain_names:
  e['relation_mode']='unconditional'
  e['review_note']+=' '+domain_review_notes[name]
 if name in conditional_source_names:
  e['relation_mode']='conditional'
  e['scope']=e['scope'].replace('条件关系只保合法叶/参数合同','仅使用合法叶/参数合同的已证定义和整数代数')
  e['review_note']=e['review_note'].replace('条件关系只保合法叶/参数合同','仅使用合法叶/参数合同的已证定义和整数代数')
  e['review_note']+=' '+domain_review_notes[name]+' 此为当前完整源合同的保守依赖类型，不表示关系证明存在数学缺口；不改source truth_status，不扩大whole_result/contribution。'
 p=edir/(name+'.json');write(p,e);edges.append((p,e));return e['edge_id']
E={}
E['s2']=edge('slack-zero-rigid-optimal-load','implies',[S1],[S2],'conditional',
 '同一个有限静态游戏，任取真最优联合对偶Q与OPT_n元组；另假设Δ=(2n−1)v−OPT_n=0。Q可相关，q仅平均槽边际；n=1单独处理。',
 {S1:'全部非负余量在Δ0逐项归零，提供负载固定与比较取等。',S2:'完整锐性结论，包括显式p、全部纯最坏回复、跨所有最优Q的唯一负载。'},
 'S1非负分解令Rov、Rout、每个比较δ及J为零。C上d=1、jx=0迫H=L；C外L=0且H非负迫H=0。有限客户/背景给每个正支持原子同一整数L，fB(A)=g(A)≤v且比较主题取v，故θ=v。n≥2且qA>0才由正系数得到g(A)=v；n1不作此推断。固定这份Q和比较tuple，定义pA=(比较出现次数+(n−1)qA)/(2n−1)，客户命中率在C为(1+L)/(2n−1)，外为0。对任意纯B′、负载h，以(1+L)/(1+h)=1+(L−h)/(1+L)+(h−L)^2/((1+L)(1+h))逐客展开，得到(2n−1)(Ep fB′−v)=Σ槽(v−g(a))+Σ外h+ΣC(h−L)^2/((1+L)(1+h))。三项全非负；h=L时直接命中率式使左边0，同时第一和也为0，反向零差由外项/平方迫全部h=L。故p最优且所有最坏回复恰负载L。再固定此p，任取另一个最优Q′，其对p期望既≥v又≤v；非负slack均值零迫每个支持背景h=L。因此真正排尽全部其它最优Q，唯一的是整客户负载，非标签/tuple/p/C唯一。',
 '只在静态锐性假设下；全部最优对象量词保留，不获得实际SPE前缀。',[ref(static),ref(objects[S1]['evidence'][1]['path'])],whole=objects[S2]['statement'])
E['s3']=edge('slack-to-same-background-rounding','implies',[S1],[S3],'unconditional',
 '任意n≥1，同一真最优Q与同一OPT_n元组；FC、JC、Rout均由这份共同输入定义，不假设iid或实际均衡。',
 {S1:'给JC+Rout≤Δ以及jx精确倒数余项。',S3:'存在一个正支持纯B的共同查询cap与θ−v定量界。'},
 '先对每个同一个B同时界所有A：Dx=(1+Hx(B))^(−1)−(1+Lx)^(−1)，fB(A)≤v+ΣC Dx+ +Rout，因g(A)≤F(A)≤v且C外Dx+≤L/(1+L)。右侧与A无关，故可先max_A再E_Q；没有把max和E交换。EDx=jx，故EΣC Dx+=(JC+EΣC|Dx|)/2；将|Dx|写为sqrt[样本J余项·1/(1+H)]，先随机性再客户和两次Cauchy给EΣ|Dx|≤sqrt(JC FC)。FC≤ΣjF(Tj)≤nv；有限正支持有一个B的cap≤其均值，得v+Rout+(JC+sqrt(JC FC))/2。S1的JC+Rout≤Δ给0≤θ−v≤Δ+sqrt(nvΔ)/2。零值/n1无除零。',
 '仅至少一个支持背景；不保证全部支持近优、不支付任何SPE前缀嵌入。',[ref(static)],whole=objects[S3]['statement'])
E['dynamic']=edge('rigid-load-at-actual-prefix-payment','implies',[S2],[DP],'conditional',
 '同一个n人游戏静态Δ0，给定完整SPE的实际前n−1槽恰有S2共同负载L；不以静态纯背景存在替代这个实际条件。',
 {S2:'提供唯一L、每个合法主题g≤v、纯cap v及显式原始slack。',DP:'此前缀条件下每位≥v且W≥nv。'},
 '末位面对实际负载L真BR得v。实际前缀每槽主题包含在C（C外L0），Σ槽g=ΣC L/(1+L)=(n−1)v；每项≤v，故每个槽g=v。最终客户分母L+1末位覆盖≤L+1，先前玩家实际收入≥g(自身主题)=v。末位亦v，求和W≥nv。n1空前缀且静态最大主题直接成立。',
 '完整条件命题；S1的Δ0结构和S3的纯支持存在均不能取消实际前缀同L。',[ref(static,'8. 退化边界与真正能接回 SPE 的条件推论'),ref(static,'5. 显式原始最优分布与所有最坏回复')],whole=objects[DP]['statement'])
E['family']=edge('boundary-plus-distinguishing-seed-family','implies',[BD],[AP],'unconditional',
 '固定同一43节点σ与六个标签；以正文给定22单位客户种子w1和198边界w0作不交副本线性相加，N为任意正整数。种子同σ的全历史可行性按精确成熟证书复用。',
 {BD:'198个不同单位客户的w0、同一完整σ、私有型1/2/4及W/OPT边界。',AP:'Nw0+w1的互异覆盖完整SPE族、真实唯一最优支持与逼近式。'},
 '种子六私有型人数(1,3,1,1,3,1)，mask47与61各6，共22。已读成熟七层验证合同分别核w0与w1同σ全部258含自身IC；每条IC在客户人数上线性，故N倍w0加w1对每个N仍非负，不重新跑树。六私有型正数使覆盖两两不同。实际收益和W按客户相加为(48N+6,48N+6,42N+5)、138N+17；T124盖198N+19。任意至多三标签支持S≠124缺T一标签，w0私客损至少23N，种子相对T最多改善22−19=3，故总损≥23N−3>0，T唯一最优支持（排列非唯一）。OPT/W=33/23−124/[23(138N+17)]从下趋界；不把别名边界本身称覆盖互异。',
 '固定σ/比较的显式单位客户族；不外推全部策略最坏值或有限N达到界。',[ref(construct),ref('archives/customer-attraction/state/计算/固定完整策略的七层共同客户证书--计算.md'),ref('archives/customer-attraction/tools/evidence/stationary-pair-transport/examples/customer_attraction/root_stationary_kernel.json')],whole=objects[AP]['statement'])
E['nf']=edge('prefix-monotone-to-integer-extra-one-normal-form','specializes',[PM],[NF],'conditional',
 '取Gr(b)=v_(r+1)(b)，并保目标本来的if：若全合法背景、全部目录/完整SPE的F_r失败，取最小剩余人数坏点r及t=Gr(b)>u。同一原σ强制根后真续行。',
 {PM:'PM/末位基例下的最小失败真后继保底与每枝扩张。',NF:'真正整数extra-one的逐后继根外折扣及总信用正规形。'},
 'PM的具体实例先付：v_r(b+1_A)≥v_(r+1)(b)，因固定A加r−1自由槽是r自由槽对手域子集，推送同一联合Q，未要求iid或看query。末位真实即时最大值≥v2(b)，给G1基例。套通用最小失败归约，得到每根dA≤u<t和每个真实后继收入≥t。对任一该叶后继B，将同分母份额分成A交和A外，交集和≤dA，所以outside_A(B)≥t−dA>0；逐后继求和为(r−1)(t−dA)。这严格补出目标的逐人式，非仅引用通用总Vout。保同一合法背景/整条σ/整数竞争槽；不把跨枝信用相加当实际W。',
 '完整条件归约；不宣称F_r成立，也不由此给显式最小r实例或跨根付款。',[ref(objects[PM]['body']['path']),ref(extra),ref('archives/customer-attraction/tools/evidence/R-0f99797b33de46bfb498541a0bc5fae9/security/c3317c7ab24c0a5af1b5.raw')],whole=objects[NF]['statement'])
E['two']=edge('structured-theta-two-label-and-separate-two-player-base','implies',[ST],[TWO],'unconditional',
 '原共同标签目录至多两标签，任意合法背景、r≥1、每份完整有序历史SPE；最小人数r≥3的附加结论另由任意目录两人基例承担，不从标签数边界推人数。',
 {ST:'k≤2极大覆盖自动满足归属{1,k−1,k}，给首位≥θr(b)。',TWO:'全背景两标签F_r及一般最小坏点r≥3、至少三主题。'},
 '标签至多二，覆盖去重后极大数k≤2，所有可覆盖客户归属大小自动允许；ST给u≥θr(b)。弱minimax和多加一自由竞争槽单调性给θr(b)≥vr(b)≥v_(r+1)(b)，故两标签F_r全人数成立，空/重复覆盖标签仍合法。独立排任意目录r1/r2：r1真实即时max≥v2。r2取f_b最大A，对给定原σ在hA后每个真实末位BR B，U_b(A,B)−U_b(B,A)=f_b(A)−f_b(B)≥0，且U_b(B,A)=max_TU_b(T,A)≥θ2(b)。原根IC将该强制A的真实收益保底转回实际u≥θ2(b)≥v2(b)≥v3(b)。因此任意目录的最小F坏点r≥3；两标签已排又给至少三标签。这两步分别支付目标完整句，无开放跨枝付款被使用。',
 '完整小目录定理和一般人数下界；零客户全0、空题、覆盖别名、任意平局均保留。',[ref(extra),ref('archives/customer-attraction/tools/evidence/R-0f99797b33de46bfb498541a0bc5fae9/security/80aba6921fb21711d77e.raw'),ref(floor)],whole=objects[TWO]['statement'])
E['integer']=edge('positive-defect-integer-parameter-reduction','implies',[D],[INT],'conditional',
 '只调用D对象对任意合法m槽终局的缺口定义/恒等式部分，m≥2；α+β=t=m−2。不使用small-D存在或均衡性质。',
 {D:'固定同一叶的D定义与早期整数p、尾两个指标。',INT:'实参数最小D精确由0…t的整数候选达到。'},
 '令β=t−α。交集指标都1使分子t−p≥0、分母p+2固定；A独有区为(α−p)+/(p+1)，B独有区为(t−α−p)+/(p+1)，外区正部0。所有p为0…t整数，故全部hinge折点p或t−p为整数。D在[0,t]连续凸分段仿射，各仿射段最小值可取某端点，平坦段亦取整数端点；所以实最小=整数k0…t最小。t0/equal-tail/空差集无需例外计算。',
 '条件关系只保合法叶/参数合同，不附加实际未证small-D；仅一个给定终局的m−1参数检测，非全部SPE枚举。',[ref(defect)],whole=objects[INT]['statement'])
E['hzero']=edge('zero-positive-defect-recovers-load-dominance','specializes',[D],[H],'conditional',
 '同一完整根SPE及actual前t=m−2槽/末两A,B；存在α,β≥0、总权t，且D(α,β)=0。',
 {D:'精确P=αuA+βuB+R−D和尾保底链。',H:'H的守恒福利结论与点态条件等价；独立85节点扩类见证不在本推导内。'},
 '每个被计D项非负、分母c>0，D0当且仅当p≥α1A+β1B，未覆盖客户两边0。因此条件正是H。恒等式给P≥αuA+βuB；两实际尾各≥θ(h)，得W≥mθ(h)≥mv。静态计数界给mOPT≤(2m−1)W。H区间等价亦直接逐membership：交集p=t，A/B差集分别α≤LA、β≤LB，存在总权t当且仅当LA+LB≥t，空差集最小按t。',
 '只得到H对象的条件定理和等价检查；不从一般代数生成独立四客户完整σ。',[ref(defect),ref(hbody)],contrib=('H条件及其LA/LB等价检查，和H下完整条件福利W≥mθ(h)≥mv、mOPT≤(2m−1)W。','H对象另含四客户四人85节点可实现严格扩类见证；那由已读独立成熟原JSON/审计合同承担，不由本D0推导产生。'))
for key,target,desc in [('obH',H,'H下W≥mθ(h)≥mv时得mOPT≤(2m−1)W'),('obD',D,'small-D下W≥(m−1/2)s≥(m−1/2)v时得W≥OPT/2')]:
 E[key]=edge('static-count-converts-'+('dominance' if target==H else 'positive-defect')+'-payment','implies',[OB],[target],'conditional',
  '同一m人有限单位客户共同目录，原完整SPE、同一actual末两及合法早期前缀；目标所需H（或存在D≤s/2）与实际尾部保底必须另有，不能从静态值存在取得。',
  {OB:'真正相关静态值v_m≥OPT_m/(2m−1)。',target:'把已经取得的实际收益门槛转换成目标福利系数。'},
  '对完全同一输入调用v_m≥OPT_m/(2m−1)。'+('若H已给W≥mθ(h)≥mv，则W≥mOPT/(2m−1)，整理得mOPT≤(2m−1)W。' if target==H else '若实际终局存在D≤s/2，则由精确叶账W≥ms−D≥(m−1/2)s；真实两人保底与背景域包含给s≥θ(h)≥θm≥v，故W≥(m−1/2)OPT/(2m−1)=OPT/2。')+'本边不把θ纯minmax换成v混合maxmin，不提供早期玩家一般v保底。',
  '目标证明的定量转换贡献；所有实际路径条件明确保留。',[ref(objects[OB]['body']['path']),ref(hbody if target==H else defect),ref(floor)],contrib=(desc,'目标完整句还需'+('H→P≥αuA+βuB、末两实际SPE保底、H等价条件及85节点扩类证据。' if target==H else '同叶D/R精确账、真实末两SPE保底、参数合同、整数有限化及存在small-D；本静态来源不证明这些前提普遍成立。')))
E['equiv']=edge('same-policy-restart-two-registered-formulations','equivalent_to',[RESET],[REST],'unconditional',
 '逐一对应同σ、同合法有序h、同过去覆盖P、同余人数r及同最优A/真实尾B；C_A/C_B都含旧P，F为静态总覆盖补全。',
 {RESET:'λ≤ρ、真实重置恒等式及全人数all-big精确见证。',REST:'同一个重启恒等式及不能删restart的全人数见证。'},
 '两记录不按标题同义，而按完整statement核对：G、ρA、λB、R_B和C_A/C_B定义逐项相同，R_B=ρA−λB+(C_A−C_B)由两边减同G恒等。RESET比REST另显式写λB≤ρA：因为B真尾中已出现，把含A的同一合法静态元组之B移到首位，剩r−1槽仍覆盖C_A，故F_(r−1)(P∪B)≥C_A、λ≤ρ；此步不要求移动后仍SPE。REST的全人数all-big输入在根规定S=B大题、强制singleton A时C_A=m+1/ρ=m−2/η0，A私客未被S或尾盖，故|t|1；强制大B时C_B=m、λ0/R_B=m−1/restart1。由此双向恢复两条注册statement全部额外数值。两正文其它菜单求和界/保ξ省η候选并非这两个目标statement的附加命题，未宣称整篇互推。',
 '精确注册对象的双向等价，仅关于静态菜单损失与真实重新续行的分离；全人数ETA候选的后来真值另依其主owner。',[ref(menu),ref(restart)],whole='ALL('+RESET+') ⇔ ALL('+REST+')：同一σ重启差恒等式、λ≤ρ及m≥3 all-big正restart1的相同整数游戏见证互相恢复；不声称两个全文其它候选互推。')
E['crreset']=edge('all-big-credit-family-supplies-positive-restart-witness','implies',[CR],[RESET],'unconditional',
 '使用信用障碍中每个m≥3的大m客户主题B与m−1个不交单例、每有序历史恒B的同一完整σ；根强制单例A后真尾仍全B。',
 {CR:'提供全人数合法完整SPE all-big输入及同σ各强制分支。',RESET:'其全人数零λ但正reset的见证部分。'},
 'CR全历史可信性：过去a次B、余r时遵循收益m/(a+r)≥1，偏离单例至多1。根最优补全G=2m−1；强制单例A后尾全B，C_A=m+1、ρ=m−2、η0、|t|1。把尾中大B放根仍可静态补全全部，λB0；真实重新沿同σ却全B，C_B=m、R_B=(2m−1)−m=m−1，所以C_A−C_B=1。精确说明信用反族同时给RESET见证，但不是由预算失败推出half失败。',
 '只复用同一完整整数输入证明目标的见证部分；不能仅凭该族给所有历史重置恒等式。',[ref(credit),ref(menu)],contrib=('对每个m≥3，完整all-big SPE根强制singleton后真尾大B给ρ=m−2、λ0、η0、|t|1、R_B=m−1、reset1。','RESET普遍同σ恒等式R_B=ρ−λ+(C_A−C_B)及λ≤ρ另由同一静态覆盖代数承担；预算折扣失败和half是不同断言。'))
# Reading ledger: all original task reading refs were actually displayed; complete files versus exact sections are distinguished.
refs=d['context_plan']['reading_refs']
full=set(r['path'] for r in refs if 'section' not in r)
# These three original partial references were read as complete bodies.
full.update([static,menu,objects[BG]['body']['path']])
extra_full=[objects[PM]['body']['path'],'archives/customer-attraction/tools/evidence/stationary-pair-transport/examples/customer_attraction/root_stationary_kernel.json']
for p in extra_full:full.add(p)
ledger=[]
seen=set()
for r in refs:
 p=r['path']
 if p in seen:continue
 seen.add(p)
 sels=[x.get('section') for x in refs if x['path']==p and x.get('section')]
 ledger.append({'path':p,'sha256':sha(root/p),'actual_read':'complete-body' if p in full else 'complete-exact-listed-sections','sections':[] if p in full else sels,'read_method':'displayed complete text; no mathematical execution','scope_note':'首次组合静态输出发生截断；已另连续读static285–505及独审全文补齐；作者程序合同完整页已在该输出末段读完。' if p==static else '已读精确正文/证据合同；未把其历史重放计为本轮执行。'})
for p in extra_full:ledger.append({'path':p,'sha256':sha(root/p),'actual_read':'complete-body','sections':[],'read_method':'displayed complete text; no mathematical execution'})
stationary='archives/customer-attraction/state/反例/真实后继占用平稳分布的付款失效与放大余项--反例.md'
ledger.append({'path':stationary,'sha256':sha(root/stationary),'actual_read':'exact-section-plus-following-remainder-displayed','sections':['本例自由Q反而安全，且精确minimax可验证'],'read_method':'displayed source text; extraction continued through final sections; no run','scope_note':'用于PM所列例子不是最小失败的精确比较；未冒称本文开头完整读取。'})
write(edir/'reading-ledger.json',{'actor':'Boss6','task_id':tid,'formal_primary_core_count':20,'all_core_statements_quantifiers_assumptions_read':True,'entries':ledger,'scientific_runs':{'old_CLIs':0,'LP':0,'SPE_solver':0,'BI':0,'random_scans':0,'mature_tree_replays':0},'mature_contract_reuse':['static author12/1308/1299/700 and successor80/1275/1 distinct','seven-layer primal-dual/fixed43node258 rows and22customer seed','R373 198customer exact source/replay identity','old4customer85node H witness','allbig n3/n5 original code/reports39/3905 and7/21 local rows','structured theta3744scalar10instance/cycle exact domains from mature contracts'],'not_claimed':'No automatic traversal/reexecution of all hyperlinks or archived raw artifacts from already mature contracts. Every displayed file/section is listed honestly; extra evidence bytes checked below need not mean full semantic read.'})
# Hash current declared inputs and every direct body/evidence reference; this is freshness, not a substitute for reading.
pin_checks=[];ref_checks={}
for oid in d['object_ids']+d['read_object_ids']:
 actual=rr.pin(objects[oid]);expected=d['input_pins'][oid]
 if actual!=expected:raise RuntimeError('stale object '+oid)
 pin_checks.append({'object_id':oid,'version':objects[oid]['version'],'registration_pin':actual,'matches_task':True})
 for r in [objects[oid]['body']]+objects[oid]['evidence']:
  rr.ref_bytes(root,r)
  ref_checks[r['path']]={'path':r['path'],'sha256':sha(root/r['path']),'all_direct_declared_refs_match':True,'semantic_read_scope':'see reading-ledger; byte verification alone is not claimed as full reading'}
ready=json.loads((out.parent/'ready-cag59aa-round48.json').read_text())
sourcefresh={'task_id':tid,'owner':task['owner'],'request_id':task['request_id'],'definition_pin':rr.pin(d),'ready_definition_pin':ready['definition_pin'],'ready_remote_tip':ready['remote_tip'],'core_count':20,'read_count':len(d['read_object_ids']),'object_checks':pin_checks,'direct_source_checks':list(ref_checks.values()),'task_snapshot_sha256':sha(root/task_path),'registry_snapshot_sha256':sha(root/'research/registry.json'),'all_input_pins_match':True,'pending_source_correction':{'path':credit,'current_sha256':sha(root/credit),'exact_old_sentence':'这项充分候选仍未证；保留全部项则退回原目标的恒等重写。','issue':'same-tail body calls full-xi/drop-eta candidate still unproved, while current required main-menu evidence states all-n ETA is refuted by two-player26/67 examples; primary credit/refund theorem unchanged','root_notified':True,'delivery_role':'complete current-pin draft before any Root-controlled refresh; not final done authorization'}}
if sourcefresh['definition_pin']!=ready['definition_pin']:raise RuntimeError('ready mismatch')
sourcefresh['relation_mode_final_review']={'four_proved_source_domain_relations':'accepted/unconditional; original target conditions and whole_result/contribution bounds preserved','three_conditional_source_relations':'PM specialization, D integer reduction and D0/H specialization retain accepted/conditional under the full source objects current conditional registration type. Their domain-restricted proofs are complete; ordinary legal leaves/integer parameters are not additional open premises.','source_truth_status_changed':False,'native_gate_alignment':'Conservative source-type dependency retained exactly; no validator change or duplicate source object. No unresolved native relation-mode gate after this classification.'}
write(edir/'source-freshness.json',sourcefresh)
# Read-only native binding previews. Root installs, calls native bind/write/check and refreshes final hashes.
previews=[]
for p,e in edges:
 b=rr.edge_bindings(root,e,objects,verify=True)
 previews.append({'edge_reference_id':e['edge_id'],'staging_file':str(p.relative_to(out)),**b})
write(edir/'binding-preview.json',{'kind':'read-only-native-binding-preview-not-logical-edge','entries':previews,'writes_to_clone':0})
# Per-core coverage, with genuine comparisons and exact unpaid scope.
coverage={}
def cov(i,reason,scope,keys=()):
 edgeids=[E[k] for k in keys];coverage[i]={'state':'linked' if edgeids else 'isolated-after-review','object_pin':d['input_pins'][i],'reason':reason,'comparison_scope':scope}
 if edgeids:coverage[i]['edge_ids']=edgeids
cov(S1,'精确非负S1完整支持Δ0的S2及全Δ的S3；对最优Q严格保δ≥0，q只是平均槽边际。','S1/S2/S3与动态前缀DP完整比较；作者/后继成熟审计合同区分真实minimax与generic-cap。',['s2','s3'])
cov(S2,'不只单个Q支持固定：显式p精确slack排全体Q′共享L；再在实际前缀同L条件下接动态付款。','static全文1–11节、原9142B及两个成熟审计正文；DP全部登记陈述。',['s2','dynamic'])
cov(S3,'同B同时对全部A界后取E，得至少一个支持B；没有任何一般actual前缀嵌入。','S1正余项与S3正部两次Cauchy、DP实际前缀条件；pure存在和actual相等严格区别。',['s3'])
cov(BD,'198点与R373 mult2逐11兴趣型/43动作/portfolio全相同；与seed线性相加给互异族。','构造全文、七层合同、四发现器合同、R373 full JSON/code/report；mask57对审查表56为已登记抄错，不改输入。',['family'])
cov(AP,'逐IC线性叠加和私客损23N胜种子增3，得到全N完整SPE/唯一最优支持/下趋界。','同43节点σ的198点+22种子精确身份；不继承抽象9/4或另一客户输入。',['family'])
cov(NF,'通用PM在Gr=v_(r+1)下精确专化，并补同叶逐后继交集≤dA得到outside≥t−dA；条件if保留。','通用PM正文、extra-one整页/原6293B、最小r复核及原3893B资源指定节；一般F已经另反但正规形有效。',['nf'])
cov(CY,'环菜单对k7…12满足完整t=v4门槛，k≥13只满足尾>根；全部k末位有2>3/2偏离，所以不满足NF的真实孩子SPE条件。Mfull值/安全值匹配不替深IC，不能由此refutes NF。','NF与真后继门槛t；环r3形式菜单v4=2−6/k、Mfull=2−14/(3k)，成熟有限回归/两个negative原程序合同全文；未重演旧运行。')
cov(MID,'均匀驻留下(1/4,1/4,−1/2,−1/2)平均−1/8精确否中间归属逐客模板。ST定理只允许1/k−1/k，此形式菜单不是真SPE且不能否ST或NF。','结构raw整篇逐类型驻留付款与源页中间归属例；与环严格排序非SPE障碍不同，未制造跨模板逻辑否定。')
cov(TWO,'两标签由ST自动允许k≤2及θr≥vr≥v_(r+1)；一般r≥3独立用r1和任意目录r2真实BR差值+原根IC。','NF原稿§3/4、ST结构证明、末两保底正文；明确人数/标签数两个下界不同承担。',['two'])
cov(ST,'完整单例/全体/缺一驻留非负三类证明可专化两标签；中间会员−1/8落在假设外，没把structured theta扩成任意目录。','raw9971B完整E/R/驻留付款/共同核/锐例；结构审计仅成熟3744/10合同，无本轮扫描。',['two'])
cov(H,'D0恰是H且区间等价逐membership；得到守恒福利。独立四客85节点扩类不能由D代数声称产生，保原证据复用。','D/R、实际H全文、旧85JSON全部动作和末两保底/静态计数全文；共同核m6K42是H外正D另一个严格扩类。',['hzero','obH'])
cov(INT,'D(α,t−α)全hinge整数，连续凸分段仿射最小有整数端点；m−1候选精确。','同D/R定义每客户c与p整槽合同；t0/A=B/空差集均涵盖，非SPE全树有限化。',['integer'])
cov(D,'叶恒等与末两SPE保底再经真正静态计数给small-D充分half；D0专化H，实参数检查有限化。','D/R/H/共同核/fullθ与v量词；保R判据相消等价既定W门槛，不提供一般付款。',['integer','hzero','obD'])
cov(CORE,'K共同核+m私客族所有有序历史选新最小标签为SPE；D=R=t全参数。K0否每份SPE可选smallD，K≥m(2m−5)在H外满足充分条件。没有refutes边指向D/R条件定理：全族W=OPT，smallD普遍存在是另一个未登记的加强对象。','同D/R/H和整数检测完整比较；六人K42给D4=s/2，K0给D4>1/2；所否目标与proved-if明确分开。')
cov(RESET,'与REST逐定义/同σ/全人数见证精确互恢复；λ≤ρ由静态重排另证。CR提供相同all-big正restart见证。','RESET/REST完整statement与两正文其它内容分开；ML联合λ界只静态，不蕴含真R小。',['equiv','crreset'])
cov(CR,'删ξ/η及固定α<1的预算反族，所有菜单分布由逐行min量化。该同一输入另提供RESET正restart见证。减少被减项系数仍保上界，未反half。','全all-big解析证明，主菜单恒等、并行审查精确域/原MD/code/fullJSON，m3/5只有限；full-xi/drop-eta全人数候选状态冲突已报Root，数学主结论未改。',['crreset'])
cov(REST,'与RESET完全相同的登记重启断言；没有因相似标题宣称其全文保信用候选与联合λ界双向成立。','同h同σ两枝C_A/C_B、allbig严格reset1，保ξ省η历史停点与当前主owner状态区别。',['equiv'])
cov(PROD,'任意product SPE投影只是终局，不自动为factor SPE；P1单向/P4条件与共同价格目标不由本包静态安全刚性、ST或BG推出。已知福利非加族仍Bprod=(a+q)=W/2，不能当价格候选反例。','候选完整正文与本包静态v/实际θ及BG各量比较；缺的是实际跨坐标补偿/全部历史支付唯一条件，不是普通收益可加。没有无关hub。')
cov(BG,'BG-GAP以最优剩余利润F_r(b)和真实剩余P比较，非本包覆盖补全F_k(P)、λ/ρ；同尾信用恒等或D/R不给BG-GAP。34/19仅原MD历史有限诊断，不能认证全称。','完整资源中BG-GAP/非循环信用边界与RESET/CR/D比较；末位余项若只知v为真实末位而非最小，不能付r·minu。未代读五个历史源或重跑。')
cov(CAP,'END在d0≤c非增、d0≥c为p/c+(a−p)/d0−a/d，最大两端；不依赖SPE。与D的整数hinge有限化是不同优化函数/域/极值方向；与ξ同尾静态信用亦无同分支负载映射，不能迁移常数。','完整联盟信用正文END/CAP与本包D、CR/RESET比；取等负载不保证SPE，首次m7超一非half反例。')
closed=[
 {'core_id':S1,'peer_id':DP,'reason':'已实读并由S1→S2→DP给条件动态付款链；仅在实际前n−1负载=L时，额外条件没有由静态锐性自动取得。'},
 {'core_id':S3,'peer_id':DP,'reason':'已实读；S3只给存在纯支持B且近优，未指定给定σ实际前缀，不能转成DP。精确边S2→DP已保存真正可用条件，当前对无需另派3B。'},
 {'core_id':RESET,'peer_id':ML,'reason':'同一body两独立断言：ML给任意合法尾Σλ≤(r−1)(t+η)，RESET是两个真枝差恒等和正reset见证。all-big λ0/η0但t1且reset1，无矛盾；没有由静态界得到R小的逻辑边，问题已精确分离。'},
 {'core_id':H,'peer_id':OB,'reason':'已按同一输入v_m和actualθ链建立static-count-converts-dominance-payment局部贡献，未将静态安全当全体收益保底。'},
 {'core_id':BD,'peer_id':PAIR,'reason':'已读完整126收益点合同：PAIR不守同支持总收益1/2≠5/8、无任何signed共同客户；BD为63非负客户层的另一点，收益034为(8/23,8/23,7/23)非PAIR(3/8,3/8,1/4)。同43策略/portfolio或同另一9/4标量不合并客户输入，无推导/反驳。'},
 {'core_id':D,'peer_id':OB,'reason':'真正静态计数界只支付small-D充分结论最后系数；已建立局部贡献，D存在仍非普遍，common-core K0不反该条件定理。'}]
# Complete substantive report, including zero-edge comparisons and preserved source issue.
review={'task_id':tid,'reviewer':'Boss6','new_edge_count':len(edges),'coverage_counts':{'linked':sum(x['state']=='linked' for x in coverage.values()),'isolated-after-review':sum(x['state']=='isolated-after-review' for x in coverage.values()),'needs-decision':0},'whole_vs_contribution':{e['edge_id']:'whole_result' if 'whole_result'in e else 'contribution' for _,e in edges},'closed_overlaps':closed,'follow_up_tasks':[],'exact_open_obligations':['S3纯背景存在不能满足给定SPE实际前缀负载L','跨根真实后继根外信用尚无共同actual钱包；通用PM归约不补此付款','D≤s/2是充分类，普遍存在已由K0完整族否定；保持R/尾超额或更多真实分枝的不同预算仍需证明','相同P静态低λ不控制同σ的真实C_A−C_B；full-credit路径式本身重述OPT−2W','任意coupled product SPE的共同价格补偿及BG-GAP未由本包支付','联盟END合法负载取等不等于完整SPE可实现或跨分支容量'], 'pending_source_status_issue':sourcefresh['pending_source_correction'],'canonical_review':{'registry_sha256':sha(root/'research/registry.json'),'scan_scope':'all current canonical edge endpoint incidences with these20cores','exact_new_relation_duplicates':0,'incidental_match':'ca-r36-minimal-extra-one-forbids-real-count-ring already canonical; its M63/ring endpoints outside this packet, no rerun/reuse or new coverage claimed'},'mature_run_policy':'All old successful large proof/audit/LP/tree calculations reused by exact source contracts. Current code only emits records, hashes refs/pins and previews bindings; scientific executions0.'}
review['final_relation_mode_review']={'accepted_unconditional_edges':9,'accepted_conditional_edges':3,'four_proved_source_relations_upgraded':['slack-zero-rigid-optimal-load','rigid-load-at-actual-prefix-payment','static-count-converts-dominance-payment','static-count-converts-positive-defect-payment'],'three_source_type_conservative_relations':['prefix-monotone-to-integer-extra-one-normal-form','positive-defect-integer-parameter-reduction','zero-positive-defect-recovers-load-dominance'],'mathematical_reason':'All seven domain-restricted implications are proved without new gaps. Four have proved sources and the target statements own conditions do not constitute additional open premises. Three keep conditional only because the complete PM/D-R source objects are currently registered conditional. Concrete PM and last-player base are paid inside the specialization proof; D integer reduction uses only proved definition/algebra on legal integer leaves. Ordinary legal leaves/integer parameters are not open obligations. All original conditions, whole_result and contribution bounds remain.','native_gate_alignment':sourcefresh['relation_mode_final_review']['native_gate_alignment']}
write(edir/'mathematical-review.json',review)
assets=[{'path':str(p.relative_to(out)),'sha256':sha(p)} for p in sorted(edir.glob('*.json'))]
receipt={'coverage':coverage,'assets':assets,'closed_overlaps':closed,'follow_up_tasks':[],'reviewed_by':'Boss6','task_snapshot':{'task_id':tid,'owner':task['owner'],'request_id':task['request_id'],'definition_pin':rr.pin(d)},'source_status':'Complete current-pin mature draft; Root-controlled same-tail ETA status correction pending before final current-input closure.'}
write(out/receipt_path,receipt)
files=[{'path':str(p.relative_to(out)),'sha256':sha(p)} for p in sorted((out/'map').rglob('*')) if p.is_file()]
write(out/'delivery-manifest.json',{'task_id':tid,'owner':task['owner'],'request_id':task['request_id'],'definition_pin':rr.pin(d),'files':files,'canonical_reused_assets':[],'counts':review['coverage_counts'],'new_edges':len(edges),'closed_overlaps':6,'follow_up_tasks':[],'source_freshness_file':erel+'/source-freshness.json','delivery_state':'mature-old-pin-draft-await-root-source-correction','no_hash_cycle':'Manifest hashes receipt and map assets; receipt does not list manifest or itself.'})
print(json.dumps({'out':str(out),'edges':len(edges),'counts':review['coverage_counts'],'closed':len(closed),'files':len(files),'request_id':task['request_id'],'definition_pin':rr.pin(d),'manifest_sha256':sha(out/'delivery-manifest.json')},ensure_ascii=False,indent=2))
