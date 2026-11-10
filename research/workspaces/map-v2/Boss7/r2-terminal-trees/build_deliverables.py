import json, hashlib
from pathlib import Path
CLONE=Path('/workspace/scratch/d5435ebfeb39/co-work-anl-boss7')
OUT=Path('/workspace/scratch/d5435ebfeb39/worker-staging/r2_terminal_trees')
TASK='customer-attraction-3a-3a-75ccbefadfb68761'
task=json.loads((CLONE/f'research/operations/map-v2/tasks/{TASK}.json').read_text())['definition']
registry=json.loads((CLONE/'research/registry.json').read_text())['objects']
objects=registry if isinstance(registry,dict) else {x['object_id']:x for x in registry}
P='CA-PRICED-HIDDEN-REPLY-v1'; TABLE='M-4d83bece0286411d82b700f3e95c43ed'; BRIDGE='M-5341008ca882414a84b007cd72cd93b2'; FREE='M-390974a759e04773b897cf89fbc1762a'
base='archives/customer-attraction/tools/evidence/R-07e871289a6b4c1fb07244c97eb4aac8/general_from_half5/'
def ref(path,section=None):
 d={'path':path,'sha256':hashlib.sha256((CLONE/path).read_bytes()).hexdigest()}
 if section:d['section']=section
 return d
proof=objects[P]['body']; obstacle=objects[TABLE]['body']
common={'kind':'implies','status':'accepted','premises_mode':'all','relation_mode':'unconditional','reviewed_by':'Boss7'}
edges=[]
e={**common,'edge_id':'boss7-ca-75cc-correct-tail-priced-row-family','source_ids':[P],'target_ids':[TABLE],
'conditions':'有限单位客户、有限非空共同标签目录及完整有序历史纯SPE；m仅取5或6。actual源位置i从1计，原引理k_total=m−i+1含当前源，隐藏后继数n_hidden=k_total−1=m−i。T、Q均为原共同目录合法标签，比较索引可重复；原来的基础行单独保留，不以本投影取代强PAIR。',
'roles':{P:'提供对任意真实余尾和任意非负价格/容量/分支末位查询乘子的合法隐藏回复投影。',TABLE:'本边仅支付四格表中R5PC、R6PC新增PC行的必要性及准确行数，不支付四个精确最优值。'},
'explanation':'固定实际源i，取n_hidden=m−i个同一σ真实后继。给前n_hidden−1位α=1/8、β=0，最后一位α=1/5、β=1/20，查询乘子μ=1/4；引理的实际末前负载ℓ=Σ_{h<m}a_h，源背景p=Σ_{h<i}a_h。源IC、每个真实后继在actual末节点的全目录报价、共同K容量及该分支真末位对Q的IC非负组合，得到r+(Σα)u_m+(1/20)K≥Σψ。原six_stress.py的priced_projection按此准确隐藏位个数逐字面min；没有把六人第三位的三个后继误缩成两个。T,Q遍历m²个实际对、2m个实际/平均比较方向及同索引、异索引两类，共m²+2m+2行/源。异索引四会员权为d(d−1)、d(m−d)、d(m−d)、(m−d)(m−d−1)，统一除m(m−1)，来自先固定有序不同索引再对客户换序，未假定两个会员独立。故m=5增加4×37=148行，61→209；m=6增加5×50=250行，81→331。所有m个比较主题可重复，空覆盖与弱平局不破坏原真实IC。',
'scope':'只证明四格表指定PC增强的合法性、正确人数域和61→209/81→331的构造对应；不由一般引理推导任何有限LP最优数值。',
'contribution':{'result':'表中R5PC与R6PC的全部新增定价行是共同末位价格投影在准确余尾长度和指定参数上的合法实例；所报209/331行与原生成合同吻合。','remaining':'四个精确最优W值、对应K=1/m、各原始支持/全部slack、非负匹配对偶和全部192/448客户列及K列余项，仍由目标的冻结四矩阵证书分别承担。基础强PAIR行与静态目录非SPE诊断不由PC投影本身推出；这些必要行没有共同全树充分性。'},
'evidence':[proof,obstacle,ref(base+'71a951f150023e0843d6.raw'),ref(base+'b8fa1741de1a4a642368.raw'),ref(base+'da16429efa6114469f95.raw')],
'review_note':'已实读一般引理全部正文和五项登记evidence正文、six_stress完整原码、四格冻结报告全部字段/全部slack及来源正文。仅作数学/版本阅读和短符号计数，没有import/执行旧程序或重跑LP；明确区分k_total与隐藏位数。'}
edges.append(('correct-tail-priced-row-family.json',e))
e={**common,'edge_id':'boss7-ca-75cc-same-reply-capacity-bridge','source_ids':[P,TABLE],'target_ids':[BRIDGE],
'conditions':'与四格表完全相同的六人actual/d变量、448客户类型、非负共同K及O=1；保原R6PC全部331行。固定actual倒二源前四负载b，r=u5，强制合法T后的末位回复R必须取原同一完整σ的真实后继。引理k_total=2，只有一个隐藏回复，α_1=0、β_1=1、μ=1；K为同一共同目录大小上界。',
'roles':{P:'支付一个真实末回复下的容量端点；不能用各项独立选R替代。',TABLE:'提供被增强的R6PC精确331行系统和指定原始点。',BRIDGE:'本边支持新增50桥的合法性、331系统的真实保留与所指定旧点被一条桥排除；目标381精确最优数值另有证书。'},
'explanation':'将一般投影特化为k_total=2、α=0、β=1、μ=1。逐客户h(g)=(t−g)/(b+t+g)+g+q/(b+t+1)，零分子按0；t=0与t=1都满足h(1)−h(0)=b/(b+1)≥0。因此ψ=t/(b+1)+q/(b+t+1)，即r+K≥f_b(T)+U_b(Q,T)。直接全客户恒等式为r+K−f_b(T)−U_b(Q,T)=[r−U_b(T,R)]+[U_b(R,T)−U_b(Q,T)]+[K−|R|]+Σ_{x∈R}b_x/(b_x+1)≥0。前两项分别是原倒二源偏离IC与该真实末节点查询Q的IC，未给受迫T添加最优性。对T/Q取36个实际对、12个实际/平均比较双向与同/异索引2类，共50桥；原bridge_system逐项附在make_system(6,priced=True)之后，故381可行域投影包含于原331可行域，旧331下界证书仍为有效下界。指定旧331原始点对T=A6、Q=平均比较主题的新增行slack=−910382419/40191006672<0，确被排除。只排这一点不能单独推出新精确最优或所有旧最优均被排除；本边不作该推断。',
'scope':'同一六人448类型系统内的50条真实容量桥与指定331点的精确分离；不比较O-only408系统，也不把局部松弛点称为完整SPE。',
'contribution':{'result':'331→381是保留全部旧行并加入50条合法同一真实末回复容量桥的增强；所指定331点违反其中一桥。','remaining':'381系统精确最优W=223069978871/561166163550及K=469628955/2494071838，需要目标自己的完整原始可行点和匹配对偶（含全部448类型及K列）证明。一般投影和排除一个旧点均不能替代这些证书；尚未付不同强制主题互查与更早真实分支的共同目录闭合。'},
'evidence':[proof,obstacle,ref(base+'2755fd86267d9632f6a2.raw'),ref(base+'5b7db8b564999c07a81c.raw'),ref(base+'b8fa1741de1a4a642368.raw'),ref(base+'dd8d7881ca67276a727c.raw')],
'review_note':'完整实读容量桥全客户恒等式、同回复原码、原331/381证书的全部字段及准确负slack；源端点保持ALL。没有从失效的静态331目录反推原模型反例，没有把不同背景F_b免费合并，也未重跑任何旧入口。'}
edges.append(('same-reply-capacity-bridge.json',e))
e={**common,'edge_id':'boss7-ca-75cc-free-copy-cuts-from-true-projection','source_ids':[P,BRIDGE],'target_ids':[FREE],
'conditions':'在完全相同的六人448类型+K系统和O=1归一化内，保留381行；actual倒二源背景b=Σ_{h≤4}a_h、actual末前负载ℓ=Σ_{h≤5}a_h，k_total=2。每次强制T保同一个真末R，允许不同T有不同回复；局部投影未保这些回复的跨菜单互查。',
'roles':{P:'保证任意非负α、β、γ（γ=引理μ）的单隐藏末回复切面合法。',BRIDGE:'确定加六切面前的381行、相同变量与旧点。',FREE:'本边仅推出387新增六行的真实局部必要性和嵌套关系；精确最终最优与七类完整有理闭包见证仍独立承担。'},
'explanation':'一般投影k_total=2给u5+αu6+βK≥Σ_x min_{g∈{0,1}}[(t−γg)/(b+t+g)+(β+α/(ℓ+1))g+γq/(b+t+1)]。这正是原parametric_row的v0/v1；实际主题源T=A_j直接t=a_j，平均比较源先按t=0/1以(m−d)/m、d/m条件分组。对平均比较源自身查询用q=t，其他比较索引用q=(d−t)/(m−1)，不是无条件d/m。保留这相关性后，六条冻结切面分别由(α,β,γ)=(3/4,1/4,1)与(3/4,0,1/2)应用于(T=A6,Q=avg)、(T=opt,Q=A6)、(T=opt,Q=other)而来；乘子全非负，故每条都合法。381行生成器原样保留后附这六行，得到387行。第一参数组前两条在指定381点slack均为−26995068737/2992886205600<0，因此至少该旧点被严格排除；后续四条分别在其加入时的冻结点上有报告中的精确负slack。有限最小值是合法下界消元，不表示各客户独立最小g可以组成同一合法回复。',
'scope':'仅支付381→387六条指定切面的合法性、准确参数/索引映射与嵌套有限系统。该证明不保证任何一组隐藏会员可实现为共同目录或完整有序历史σ。',
'contribution':{'result':'全部六条自由局部乘子切面均由同一真实回复投影严格实例化，381全部旧行保留，构成目标387系统的合法必要条件增强。','remaining':'目标W=8664083663/21693341273、K=4363459416/21693341273的精确最优需387原始/对偶；任意非负αβγ在所保单回复域不能分离最终点，还需七份完整有理回复质量见证及它们对全部容量、actual末价、查询类和第五位偏离约束的核验。上述存在性和数值由目标原证据分别承担，不能从一般合法切面或381精确最优推得。跨不同强制T的共同回复菜单和更早源仍未统一。'},
'evidence':[proof,obstacle,ref(base+'2755fd86267d9632f6a2.raw'),ref(base+'5b7db8b564999c07a81c.raw'),ref(base+'5cf473265575f67bc3d6.raw'),ref(base+'dd8d7881ca67276a727c.raw')],
'review_note':'完整实读6cuts/5rounds/387原始及稀疏对偶/全部七类回复见证与verify_reply_closure源码，核条件类型中的自身/其他查询保持相关。只将一般引理确实承担的合法行步骤写成contribution，不以finite无新cut、浮点gap或既有PASS代替精确见证；本轮原代码执行0。'}
edges.append(('free-copy-cuts-from-true-projection.json',e))
for name,e in edges:
 p=OUT/f'map/edges/{TASK}/{name}';p.write_text(json.dumps(e,ensure_ascii=False,indent=2)+'\n')
coverage={}
def cov(oid,state,scope,reason,edgeids=None):
 d={'state':state,'object_pin':task['input_pins'][oid],'comparison_scope':scope,'reason':reason}
 if edgeids:d['edge_ids']=edgeids
 coverage[oid]=d
cov('M-41a0370106d6473c9bda2043a2e36d82','isolated-after-review','comparison_group[0]：与M-ed4a…逐项对读同一β/36λ、原64列全部描述/余项、37参数比较、域外单原子、2196→2396补零及完整CAG定义。读原恢复源码与执行记录但没有执行它。','64列余项37零27正与λ≥0给βW−O=ΣλGx+Σρx≥0；同一向量域外ρ<0只阻止把这个证书提升为全型。有限64支持定理没有被反驳；它也不推出域外精确负数，没有独立精确原始达β点，故不称LP精确最优。两个已登记精确陈述互不蕴含/互不否定；本包不为共同β造refutes边。与六人331/381/387变量/行族不同，不能搬固定支撑上界。')
cov('M-ed4a8319bd9b451e9ca6708625e02486','isolated-after-review','comparison_group[0]：实读同一新恢复有理参数和旧binary-float37参数对照的全部字段；完整单原子坐标、36个活动行系数、64原子不含该列及恢复证书。','新向量在合法域外原子ρ=−1379654864542047563229603046815707129343247/443022966458998162254539154957350589175972<0；补200零乘子仍不改ρ。但此原子不必G≥0，不是W0/O1可行原始点或SPE。全37新参数均不同于binary-float，旧1047负列不能成批转授。精确反驳对象是“这份向量全型非负”，本组另一core只说固定64列上界，故不能以其为refutes目标。')
cov('M-319838d1feed4226b1537d20f8d5e876','isolated-after-review','comparison_group[1]：O-only408系统与四格R5/R6、R6PC331、381与387各自完整原码/冻结证书/定义逐一比较，特别对读408语义检查器与原1049列/109正对偶行报告。','408点W1/O=93445653738551/37969467558408及全部隐藏分支共同边缘是精确必要行障碍；1049列是另一个对偶模板维数，不能混成408最优性。O-only保o与复制真实末主题分支，R6PC等保d和不同局部投影；未给出保持全部行/共同菜单的互译，不据数字或同six-person主题写包含/迁移。所有<1/2松弛点均缺完整σ，408也缺六个显式比较主题；原模型half不被否定。')
cov(TABLE,'linked','comparison_group[1]：四矩阵完整构造、192/448类型、61/81/209/331全部报告字段与slack、精确原始/对偶、静态目录非SPE诊断；新增CA-PRICED v3全部正文/五项登记evidence，分别核其正确尾长与PC参数。','接受局部合法性边：一般投影按每个actual源准确m−i隐藏位产生全部PC增强，固定参数/同异索引平均给209/331行。另ALL[一般投影,本表]给331→381同真末回复容量桥及指定旧点被排除。四个精确最优仍各由冻结匹配原始/对偶承担；已知五人真half不妨碍其必要行值<1/2。所实现静态目录第五位复制A6的真末回复始终让其严格获利，不能当SPE反例。',[edges[0][1]['edge_id'],edges[1][1]['edge_id']])
cov(BRIDGE,'linked','comparison_group[1]：原331、bridge_system新增50行、381完整证书及六切面源程序/报告/数学恒等式全读；对同一actual/d/K变量及一般投影k_total2精确核对。','ALL源支付同一真实R的r+K≥f_b(T)+U_b(Q,T)及旧331点负slack；桥后精确最优值与K由381自己的原始/对偶证明。第二ALL边只支付381→387六切面的局部必要性。排除一个旧最优点不单独证明严格最优提高，源中两个精确匹配证书才分别证明两个数值；不拼接独立回复。',[edges[1][1]['edge_id'],edges[2][1]['edge_id']])
cov(FREE,'linked','comparison_group[1]：387完整final支持/dual、6cuts/5rounds、七类全部有理groups/reply_mass，verify_reply_closure全源码；与381及CA-PRICED一般单回复投影精确比较。','ALL边证明六个指定非负参数切面来自合法真实投影，保381旧行。目标的精确最优与七份完整有理回复存在依旧由自己的证书承担。对每T这七份见证确实同时付局部质量/容量/末价/全部适用查询/第五位IC，故任意非负αβγ在该单回复域不能再切最终点；它们未给不同T的回复彼此在真实末节点的查询或更早源一致性。局部闭包不等于完整σ，不可从此反驳half。',[edges[2][1]['edge_id']])
cov('customer-attraction/closeout-efa3b6d8aa4287878c5047a8','isolated-after-review','comparison_group[3]单source wrapper指定完整section“背景利润归纳不是任意路径M和”；与CAG合法背景R_b、同包单回复投影/多回复必要行闭包分别核域，读其真实IC/返还/整尾漂移界限。','本文保全的是旧背景最优剩余利润Bellman障碍和单后继去相关恒等式，不能把同写F的任意路径真实门槛M候选当作被否命题。全A大主题n客户+n−1不交单例、n人每历史全A为完整SPE：root利润1、Wn、OPT2n−1；rootA后F_(n−1)=2n−min_{1≤q≤n}(q+n/q)，根差h_n−1无界但half余量1。单后继差的符号由同一历史末位可查询别源合法回复及对称交集给出；多位后继不能当一个合法联合动作。与本包局部回复投影只共享未付跨枝共同预算，未形成推出另一core整条数学陈述的边；保持source unassessed身份，不把资源closeout升级为新普遍定理。')
assets=[]
for name,e in edges:
 p=f'map/edges/{TASK}/{name}';assets.append({'path':p,'sha256':hashlib.sha256((OUT/p).read_bytes()).hexdigest()})
receipt={'coverage':coverage,'assets':assets,'closed_overlaps':[],'follow_up_tasks':[],
'in_packet_comparisons':[
 {'core_id':'M-41a0370106d6473c9bda2043a2e36d82','peer_id':'M-ed4a8319bd9b451e9ca6708625e02486','reason':'固定64支持有效与域外同向量失败相容；后者仅否全型推广，不反前者。全37参数身份与两套精确残差已明确，当前无需另排相同比较。'},
 {'core_id':'M-319838d1feed4226b1537d20f8d5e876','peer_id':TABLE,'reason':'O-only408和indexed Rm家族变量及真分支保留方式不同，未有保全部行的映射；只给各自方法障碍，不能按数值互推。'},
 {'core_id':TABLE,'peer_id':BRIDGE,'reason':'原331行全部保留，50真容量桥合法并排一个原点；两个最优数各由各自匹配证书承担，已交局部贡献边。'},
 {'core_id':BRIDGE,'peer_id':FREE,'reason':'同变量381→387合法六切面已交局部贡献边；7见证局部闭包边界与一般完整菜单义务已清楚。'}],
'reading_review':{'completion':'主worker已完成7core及共同模型、一般投影新增正文/五项evidence的所需实读；另3core由并行审读者提供的coverage/read-ledger合并后成为完整10core交付。当前主worker草稿不能单独done。','new_mathematical_program_runs':0,'original_LP_SPE_BI_random_or_audit_runs':0,'file_SHA_checks':'原任务38次reading_refs合36 distinct文件全部SHA与指定相符；这是输入身份检查，非数学实验。','artifact_state':'外部staging未绑定草稿；root须待read-add pushed后复制，edge-bind/edge-check并更新assets最终SHA。'}}
(OUT/f'map/receipts/{TASK}.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
# A ledger records full text spans actually read by this worker; it does not claim referenced historical programs were re-run.
terminal_token='/five-root-parent-audits-primary/';terminal_token2='/tree-inputs-and-padding-resumed-boss3/'
ledger=[]
for rr in task['context_plan']['reading_refs']:
 if terminal_token in rr['path'] or terminal_token2 in rr['path']:
  continue
 entry={**rr,'reader':'Boss7/r2-terminal-trees','read_scope':'task指定完整section' if 'section' in rr else '全文/全部字段；JSON仅压去空白，无省略系数/行名/原子/见证'}
 if any(x['path']==rr['path'] and 'section' not in x for x in ledger):continue
 if 'section' not in rr:ledger=[x for x in ledger if x['path']!=rr['path']]
 ledger.append(entry)
for rr in [objects[P]['body']]+objects[P]['evidence']:
 if not any(x['path']==rr['path'] for x in ledger):ledger.append({**rr,'reader':'Boss7/r2-terminal-trees','read_scope':'新增登记依赖全文；仅当前正文，不冒称其所有跨链接原件已读'})
(OUT/'read-ledger-main.json').write_text(json.dumps({'task_id':TASK,'entries':ledger,'initial_task_file_sha256':'534ac22a5bd3a62c891bb1fe455156bc61ce759c39bb8639be25aa611bc5bab1','program_runs':0,'notes':['combined输出曾截断的e8、2755、b8第四矩阵及5cf cuts/rounds已另逐项完整补读；b8前三矩阵与5cf全部七见证已由无截断范围实读。','原77420B证书全部metadata/dual/437行名/zero-slacks与64原子分两pass全读；参数比较全部37行全读。','十客完整正文/781串表及独立资源全文由主worker实读；其原781 JSON/code/report/manifests交r2-terminal-c2完整实读并另合ledger。','M66及M8a指定sections主worker已读，另由r2-security-boundaries独立复核。']},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'edge_files':[x[0] for x in edges],'coverage_core_count':len(coverage),'ledger_spans':len(ledger)},ensure_ascii=False))
