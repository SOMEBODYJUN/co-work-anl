"""Primary software/mathematical-audit curation; finite and conditional scopes stay explicit."""
from pathlib import Path
import hashlib,json,re
E=Path(__file__).resolve().parent;S=E.parents[2];R=S.parent.parent/'boss4-research';F=S/'archives/customer-attraction/state/资料';G=S/'tools/evidence/cleanup';W=S/'cleanup/workspaces/Boss4/r3-collaboration-model-and-cag-audit-primary-next';F.mkdir(parents=True,exist_ok=True);G.mkdir(parents=True,exist_ok=True);W.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
src=read(E/'source-manifest.json');deps=read(E/'dependency-manifest.json');byid={x['id']:x for x in src+deps}
def txt(i):return (S/byid[i]['saved_path']).read_text()
def obj(folder,name,ident,summary,selected,body,tag='资料'):
 p=folder/(name+'--'+tag+'.md');meta={'id':ident,'kind':'resource','type_tag':tag,'title':name,'status':'primary-source-fully-read-evidence-and-quantifiers-separated','summary':summary};refs=list(dict.fromkeys('source:'+z['commit']+':'+z['path'] for x in selected for z in x['sources']));p.write_text('---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in meta.items())+'source_refs:\n'+''.join('  - '+json.dumps(x,ensure_ascii=False)+'\n' for x in refs)+'---\n\n# '+name+'\n\n'+body.strip()+'\n');return str(p.relative_to(S))
b1=r'''
本对象完整读完message_routing_model.py主源a59d00149f09ad642406的188行/8320字节，SHA a83b61cdcff42be14022c6292d4fc10abd46384c9a35c41bcf855035d3036037；两冻结refs同字节。它是内存规格与条件负载算术，不是实际board/root实现，不是客户吸引数学证明。[原件及来源](../collaboration-model-and-cag-audit-primary/source-manifest.json)逐ID保全。

## Message与Model的完整状态/路由合同

Message为frozen dataclass，含save、ident、sender、kind、recipients/mentions的frozenset、text；类型注解不等于完整运行时schema验证。Model保存rosters引用，以及messages、public、inbox、conversations、read、adopted、active这些本地字典/集合，没有线程锁、服务器、持久队列或后台Work唤醒机制。

publish先取所选save的已知roster，拒空ident/空白text/未知sender，recipients与mentions必须是该roster子集。public不得有recipients，通知mentions去自己；dm/room须非空其他参与者，dm恰一对端，私聊mentions不得把内容通知给会话外人。未知kind拒绝。全部验证后才存；key是(save,ident)，同key同Message重放不再追加，同key改内容拒绝。它不是实际board的32个十六进制字符的全局ID合同，也不验证真实身份或权限。

公开列表只记公开ID；私聊/room按(save,kind,排序参与者集合)记会话，收件人进inbox，正文仍在完整messages中。因此这里的路由排除不是同仓读取权限/加密。room多方概念也不表示当前实际board已实现多方房间。read/adopted只是独立集合，程序没有完整“数学采纳”API；audit手动标read再断言未入adopted，只核二者概念分离。

## audit真正做了哪些事

生成R0001至R0500共500个**逻辑标签**，S1/S2各用同一roster。两层循环计算a!=b的总数500×499=249500；字段directed_pairs_checked记这个对数，**没有为249500对逐对发送/递送**。实际只发布五个手造Message：S1的一对DM、一个两人提及公开、一个两收件人room，S2一对DM，以及后来给离线逻辑R0500的DM。逐条核inbox、public、跨save隔离和其他标签空inbox。

同ID同内容重放后消息数/投递条数不变；九个坏请求覆盖改同ID内容、未知收件者、自己DM、多收件DM、私聊外提及、public附recipients、未知save、空room、未知kind。拒绝后比消息数/投递条数不变。active只含R0001时仍可为R0500存inbox，说明此内存模型不以在线集合为发送前提，**不证明离线真实Work被唤醒**。

它另按源码位置parents[3]找repo，Git只读取git-common-dir，在该目录下TemporaryDirectory中创建500个/S1/workers/actor/README.md，再核目录数和R0500文件后清除。不是创建500个Work/agent，不做Git push、网络、凭据读取或真实消息。本批没有再运行这个已成功的同SHA程序。

## 条件负载与竞争算术

每人每t分钟一消息、每消息一次push的**假设**给500/t pushes/min与30000/t writes/hour。t为1、5、10、60时，每分钟分别为500、100、50、25/3次，每小时分别为30000、6000、3000、500次。若每人每分钟一个REST poll，则500×60=30000 requests/hour；程序没有执行这些请求。

指定对抗同步模型中，每轮全部幸存者重试同一head且一人成功，k名写者总尝试k+(k−1)+…+1=k(k+1)/2、拒绝k(k−1)/2；k=1/10/100/500分别是1/55/5050/125250次尝试及0/45/4950/124750拒绝。这些是条件组合计数，不是backoff/网络条件下的实际吞吐预测。

main只接受--output，先算audit，再把JSON写新文件x（必要时创建父目录）或stdout；记录Python版本、当前脚本全部字节SHA及复现命令。audit断言是Python assert，不能在-O下把无检查输出当PASS。

## 精确复用与当前关系

已完整读并保存既有[运行JSON](../collaboration-model-and-cag-audit-primary/context/message_routing_model.json)，其source_sha256恰等本主源a83b…、Python3.12.14、500/249500及全部条件表一致；程序无其他项目代码依赖，故本批准确复用，不重复无疑run。该JSON已Boss2完成，本批不复done或改写其旧资源。旧数据是规格/负载算术；另一批十个真实本地clone的并发集成是不同证据，二者都不提供500真实Work、生产GitHub或数学结论认证。

用途是理解规格中消息范围、身份标签、读/采用分离及压力假设。源码的“room”、roster和(save,id)不能自动转成当前实际协议；阶段二完成仍依真实主源阅读/正文/收据，而不是逻辑标签或运行计数。
'''
p1=obj(G,'有限逻辑消息路由的状态与负载假设','repository-cleanup/finite-message-routing-model-contract','完整188行规格模型与同SHA旧结果；249500只是有向对计数，五个手造消息/500临时目录和条件竞争公式不扩生产。',[src[0]],b1,'资源')

oldroot=E/'preclaim-context/archives/customer-attraction/tools/evidence/fractional-load-boundaries';a=read(oldroot/'replay-actual-load.json');cover=read(oldroot/'replay-cover.json');new=read(E/'runs/new-cones-report.json');structure=read(E/'cone-input-structure.json')
b2=r'''
本对象完整读完四个主源：tests/audits/__init__.py源8a30bebfdd2a93bc7608（71字节/1行）、fractional_actual_load源5ee052fc2fac798bfaaf（7376/168）、fractional_cover源19e82f83a9d90ed20863（9745/212）、new_security_cones源3e153d43f71d6ebd66e6（3795/66）。两冻结refs同字节，完整commit/path/SHA及未改原件在[逐源表](../../../../tools/evidence/collaboration-model-and-cag-audit-primary/source-manifest.json)。前三数学程序全文、所有真实入口/默认值/输出及检查均实际读完，不按标签把有限计算升级为六人half证明。

71B包文件全文仅为：`"""Reproducible checks; recorded outputs live under evidence/runs/."""`。它只是审计包说明，不导入/执行全体审计，也不保证任意输出实际已写入。与691B customer_attraction/__init__.py不同；后者导入model/exact/certificate，这四代码依赖已分别完整读完。

## 共同数学模型及精确依赖

有限单位客户、有限非空共同主题标签目录、单位提供者依次观察全部有序历史各选主题，客户在最终覆盖者间均分。允许重复、空主题、同覆盖标签、零客户和任意离轨平局。客户整数重数代表不同单位客户克隆，不是玩家权重或单个不可拆分有重客户。源Model另允许零玩家/空目录这一边界扩展；本三审计的实际人数都正，不能把该扩展偷换当前恰六人焦点。

cover程序的真实依赖是CustomerType/Instance、ExactSPESolver和独立verify_certificate，全部字节及完整阅读范围在[dependency-manifest](../../../../tools/evidence/collaboration-model-and-cag-audit-primary/dependency-manifest.json)。Model用Fraction均分、枚举至多players个主题支持求覆盖最优，无效率声明。ExactSPESolver缓存每个prefix counts的**全部可实现终局集合**，阈值max_a min_孩子u_a；它未固定一个计数Markov续局。ordered_outcomes枚举可实现有序根路径，不枚举全部完整策略；certificate逐有序历史另选合法孩子/平局。独立verifier不调solver，重建全部有序历史并逐真实偏离检查，这两层角色必须分开。

三个审计使用普通Python断言；本批新锥运行不带-O，同环境解释器确认optimize0。它们不是在-O下仍有完整校验的生产验证器。actual_load的raw dict入口并非通用健壮schema验证器（例如单位客户由range(multiplicity)展开），本资源只认证实际合法冻结输入和构造域，不把所有坏输入行为说成已检查。cover主入口实际只供Fraction数据，无浮点/LP求解器；函数注解本身不强制拒绝一切直接API浮点调用。

## 固定实际负载：全历史证书与有限规范族

actual_load默认读取四人输入和独立85行策略表；可--max-players（至少2，默认6）扩有限族，--output用x拒覆盖并建父目录。它展开单位客户，要求策略键恰是全部有序决策历史、无重复、动作合法；每个(h,a)先选a再沿**同一完整策略**完成，Fraction算当前人最终收益并核规定动作最优。全部非自身比较构成完整SPE认证，不是只看根叶。逐客户利润和等于福利；穷举全部比较主题元组求OPT，并另外核保持有效的覆盖代数。

若实际客户负载为c_x，m人时α=(m−1)/m，g(T)=Σ_(x∈T)1/(1+αc_x)、M=max_Tg(T)、G=Σ_(c_x>0)1/(1+αc_x)。程序分别记录弱桥缺口(m−1/2)M−W、精确税余额W+G−mM和half余额2W−OPT，符号不能混同。任意比较元组的客户负载d_x给逐客户1_(d_x>0)≤(d_x+αc_x)/(1+αc_x)，故覆盖上界OPT≤(2m−1)M仍有效；“有充分桥”不等于桥总成立。

真实四人17客户类型为A:3、Q:1、AD:1、BQD:12，主题A/B/Q/D；原策略根B,B,B,A，85历史/255非自身比较，u=(4,4,4,4)，W16/OPT17，g=(16/7,48/13,61/13,388/91)，G544/91。弱桥差11/26>0，但精确税余额292/91>0、half余额15>0。完整原动作表与规范β表有13个离轨差异，已逐项读[原比较](../../../../tools/evidence/collaboration-model-and-cag-audit-primary/preclaim-context/archives/customer-attraction/tools/evidence/fractional-load-boundaries/certificate-comparison.json)的来源，不能拿同叶/同标量替换原表。

construct(m)用类型A:m−1、Q:1、AD:1、BQD:m(m−1)。全B前缀先B末A；否则用两个总奖金一资源Q/D的有限逆向β：比较两个孩子最终倒数奖金、平局选Q。它为每个有序历史生成动作，不用短视greedy代替真实续局。默认main只对m=2至6全树审计，并另外用零客户和缺一动作表作边界。各有限结果如下。
'''
b2+='\n| m | 客户/历史/非自身比较 | W/OPT | 弱桥缺口 | 精确税余额 | half余额 |\n| --- | --- | --- | --- | --- | --- |\n'+''.join('| '+str(x['players'])+' | '+str(x['customers'])+'/'+str(x['ordered_decision_nodes'])+'/'+str(x['proper_action_comparisons'])+' | '+str(x['W'])+'/'+str(x['OPT'])+' | '+x['weak_bridge_gap']+' | '+x['exact_tax_bridge_gap']+' | '+str(x['half_gap_2W_minus_OPT'])+' |\n' for x in a['family_full_history_audits'])
b2+=r'''

任意m≥4的族由已实读解析证明承担：弱差=[m³−4m²+3m−1]/[2(m²−m+1)]>0，不是有限循环的外推。该族精确税仍被支付；另13人完整自动机才否定精确税，不能说本程序重核了该自动机。已读[完整反例与后续状态](../../../../tools/evidence/collaboration-model-and-cag-audit-primary/preclaim-context/archives/customer-attraction/state/反例/实际均匀缩放负载的弱付款桥--反例.md)保两种失败及half仍正、真正安全值v仍被支付的区别。

本主源SHAea6…与已有replay manifest完全同字节，输入fba8…/策略3471…及原输出/核hash入口都已完整读并保存，故准确复用，不重复无疑run。[旧精确报告](../../../../tools/evidence/collaboration-model-and-cag-audit-primary/preclaim-context/archives/customer-attraction/tools/evidence/fractional-load-boundaries/replay-actual-load.json)含85行全部分支收益及m2–6全部标量；不是新发现、外审或最小性认证。

## 分数覆盖：真实前缀利润，不是分数背景替身

cover审计中的z_T≥0覆盖任意比较客户子集C，a_x=Σ_(T∋x)z_T≥1，τ=Σz_T≥1，O=|C|。它不是自由分数背景t_r的优化，也没有求最小τ_C。对实际位置i，过去负载b_i、余r=m−i+1，g_i(T)=Σ_(x∈T∩C)1/(b_i(x)+r)。真实改T后的负载至多b_i+r，所以完整SPE给u_i≥g_i(T)。逐客户覆盖和同一实际叶旧玩家最终利润给

$$O\le\sum_{j<i}g_i(S_j)+r\sum_Tz_Tg_i(T)
\le P_{i-1}+r\tau u_i,\qquad P_{i-1}=\sum_{j<i}u_j.$$

旧项付款用实际最终负载c_x≤b_i+r，故g_i(S_j)≤u_j；没有冻结离轨后继或拿前缀覆盖数当旧利润。由非负递推系数得到

$$W\ge O F_m(\tau),\qquad F_m(\tau)=1-\prod_{r=1}^m(1-1/(r\tau)).$$

空C单独用W≥0，不代入τ0；τ1末因子零；即使P_i>O也可同方向递推。程序还检查旧统一付款Σ_r1/[m+(τ−1)r]及乘积归纳；普遍关系由已读[解析引理](../../../../tools/evidence/collaboration-model-and-cag-audit-primary/preclaim-context/archives/customer-attraction/state/引理/分数覆盖的真实前缀利润预算--引理.md)承担。m≥5且τ_C≤7/2得到half；一般只有τ_C≤m，所得约H_m/m，不能闭合六人half。后续恰六人τ≤9/2需额外真实末对行，不是本程序直接代入的结论。

主入口640个算术循环槽位（m1–80、八个τ，部分参数可重复）核产品/递推/单调，4650个a/r/t槽位核Bernoulli比较和清分母恒等式；F5(7/2)=8656/16807、F5(3)=421/729、F7(4)=132355/262144，旧uniform5,3=22003/45045<1/2。数值等式可精确复核，有限参数不是全实域证明。Bernoulli子检查取a∈{1,1/2,1/3,2/7,7/8}、r=1至30、t=0至30，令q_t=∏_(j=1)^t(1−a/(r+j))，逐项核q_t≥r/(r+at)，以及

$$(r+t+1-a)(r+a(t+1))-(r+t+1)(r+at)=a(1-a)(t+1).$$

该恒等式与0<a≤1、q_0=1给相应归纳比较的解析理由；程序只在上述有限网格回归，不把循环本身当所有实a/r的证明。

finite_spe_checks穷举k1–3全部非空兴趣mask的0/1重数、m1–4，共552游戏，再加seed621031的24个k4,m5重数0–3游戏（每六例加两个无兴趣客户）。每游戏供应明确可行覆盖：空C、全兴趣最小incidence均匀权、双重及以上客户半权、一个最优整数portfolio、各单主题、同类型部分克隆的全一权；去重后逐实际可实现有序路径核上述各行/总界。**没有算分数最优，也没有覆盖任意有理z。**

旧成功同SHAe505…报告为576实例、2457路径、41182前缀比较、10051空比较、22244个τ1检查、12零客户/92空主题实例。每游戏只对首条路径展开并独立核一份完整策略，共576份/15836节点，不是对2457路径各输出完整策略；solver的全部path语义和独立verifier角色已核代码。旧run输入/四依赖SHA和[报告](../../../../tools/evidence/collaboration-model-and-cag-audit-primary/preclaim-context/archives/customer-attraction/tools/evidence/fractional-load-boundaries/replay-cover.json)已精确绑定，本批不复跑。

## 21份新固定完整策略锥：输入、证书与严格量词

new_security_cones不导入优化器、生成器或上述CAG核心。它读取552002B冻结gzip（SHA a4e84d0478ba0ededabe547870ad0a4916cd05a78e686183ed6ef1b660583045）；解压6153467B，全部JSON字段/向量类型遍历，21项source元数据和全部Q实际读取、5662项λ及所有精确row/系数留原件并经下述逐定义核验。这里是相关输入全字段解析/精确计算检查，**不是声称人工逐字阅读6MB数字文本或额外done该gzip源**。[输入结构](../../../../tools/evidence/collaboration-model-and-cag-audit-primary/cone-input-structure.json)分清此范围。

每case先固定n名玩家、k个主题与全部有序历史策略σ，兴趣类型T遍历1至2^k−1，客户质量w_T≥0。重建真实终局，令

$$\Gamma_{h,a;T}=\frac{\mathbf1_{\sigma(h)\in T}}{\#_Tz_h}-\frac{\mathbf1_{a\in T}}{\#_Tz_{ha}},\qquad
\mathcal K_\sigma=\{w\ge0:\Gamma w\ge0\}.$$

零分子项按零；非零分子时终局含该动作，分母正。policy恰覆盖全部历史、无重复、动作精确int合法；terminal按**有序h**缓存，不把等计数历史并成同一政策。L=lcm(1,…,n)使LΓ整数；所有历史/行动真实重建后去重等值行，不丢约束。`source`生成标签/name只是元数据，审计不重新执行生成器或证明seed来源。

合法静态竞争B长度n−1，允许重复主题。定义f_B(a)_T=1_(a∈T)/[1+#_TB]，根覆盖c_T=1_(T被σ根叶覆盖)。证书共用概率Q≥0、ΣQ=1，并为每个query a提供非负λ_a，使精确计算余项

$$r_a=c/n-\mathbb E_Q f_B(a)-\Gamma^T\lambda_a\ge0.$$

每λ行须确在全树重建的LΓ集合、系数非负，Q每个B主题/长度合法；stored exact_certified和Gamma_scale标签本身不替代这些检查。与任意w∈Kσ内积得W/n≥E_Q f_B(a)·w对全部a成立；故任意查询混合p的该Q期望≤W/n，min_B期望也≤W/n，取max_p即**该固定策略锥上W≥n v_n**。这是有限有理证书证明全非负质量锥的条件数学结论，不是仅在某一个客户点的浮点实验；整数/有理清分母点可展开单位客户，不引入有权玩家。

Q固定支付整个锥，但λ可按query用不同真实离轨行；辅助静态Q不是顺序混合SPE。空兴趣客户无贡献可另外加；质量零允许空主题/同覆盖标签。没有从21个σ推广到任意σ。七/八主题、五/六人的具体case域如下，全部opaque名称、root、Q和精确λ保原件。
'''
b2+='\n| case/source类别 | n/k | 有序历史/含自身比较 | 坐标/Γ行 | Q项/λ项 |\n| --- | --- | --- | --- | --- |\n'+''.join('| '+x['name']+' / '+next(c['source_metadata_read'].get('name',c['source_metadata_read'].get('seed_family','')) for c in structure['cases'] if c['name']==x['name'])+' | '+str(x['players'])+'/'+str(x['topics'])+' | '+str(x['ordered_histories'])+'/'+str(x['all_action_comparisons'])+' | '+str(x['coordinate_identities'])+'/'+str(x['unique_Gamma_rows'])+' | '+str(x['Q_support'])+'/'+str(x['Gamma_multiplier_support'])+' |\n' for x in new['results'])
b2+=r'''

其中19份5人7主题、1份5人8主题、1份6人8主题；不是此前selected三策略13证书/4914坐标的同一输入。新程序报告的“support”实际按Q/λ列表项计数；不能单靠字段名推断去重严格正支持。minimum初始化0不提供正余量证明；这里全兴趣类型的Γ=0、c/n=E_Qf=1/n，故该坐标残差确为0，结合全部非负检查可知真实最小残差0。这是数学解释，不把初值本身冒称测得严格正余量。

已完整比较Boss2两现页《任意尾长隐藏回复价格投影》《新策略安全锥与半顶点候选增量审计》及其旧8620B结果。旧报告只绑定gzip SHA而无本审计代码SHA；本批在代码/输入全结构先读后，以普通未优化解释器**新增运行一次**，source52e8…+inputa4e8…明确绑定，exit0/7.257秒，得到21case、95349历史、709573含自身比较、20971坐标。除source文件路径外，所有新旧结果字段逐项完全相同，旧页当时未重跑的事实不改。

[新运行记录](../../../../tools/evidence/collaboration-model-and-cag-audit-primary/runs/new-cones-run.json)、[原stdout/stderr和报告](../../../../tools/evidence/collaboration-model-and-cag-audit-primary/runs/new-cones-report.json)、[新旧比较](../../../../tools/evidence/collaboration-model-and-cag-audit-primary/new-old-cones-comparison.json)保命令/时间/Python版本/输入和代码SHA；无Git、网络、真实身份、公屏或凭据操作，无源码修订。只用标准库精确Fraction，不把旧float探索20例并入这21个exact对象，也不复done Boss2 gzip/旧报告。

new_security_cones的唯一可选位置参数是gzip路径，默认repo/evidence/certificates/customer_attraction/new_policy_security_cones.json.gz；还可--output写新文件x，父目录须已存在，随后仍打印完整JSON。它要求case数恰21，不提供一般输入搜索/优化或自动发现证书功能。cover同样只可--output独占写且不代建父目录，stdout总打印报告；actual_load另有上文有限人数参数和建父目录行为，不能混为同一CLI合同。

## 可复用与不能扩大之处

三程序各解决不同接口：固定实际缩率负载的弱桥反例、可行分数覆盖的真实前缀利润回归、固定完整策略锥的聚合安全证书。自由背景t、整数静态v、固定实际负载g、覆盖权z和指定安全最优p预算不是同一对象；五固定游戏的负max(ΣC−W)实际是正GB余量，不能从文件旧名误当预算失败。

本批已读全部相关定义/反例/引理/锥对偶及后续符号纠错，快照见preclaim-comparison-manifest和comparison-manifest。真正普遍结论由其证明与完整量词承担；当前恰六人、任意有限共同目录、任意完整有序历史纯SPE的half未因这几个程序关闭。程序输入/输出、解析族、有限精确证书、条件全锥结论和外审/新颖性分别保留。这里没有新一般SPE定理、阶段三图导入或全仓完成声明。
'''
# The raw old comparison is an actual newly read related input; retain it at the linked path.
p=E/'preclaim-context/archives/customer-attraction/tools/evidence/fractional-load-boundaries/certificate-comparison.json'
if not p.exists():
 original=R/'archives/customer-attraction/tools/evidence/fractional-load-boundaries/certificate-comparison.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(original.read_bytes())
p2=obj(F,'客户分数负载覆盖与固定策略锥的审计合同','customer-attraction/fractional-and-cone-auditor-contracts','三数学审计全部源码/真实输入与证明接口；前两旧run复用，21新锥一次精确绑定，有限/固定锥/任意SPE严格分开。',src[1:],b2)
save(E/'formal-manifest.json',[{'path':p,'bytes':(S/p).stat().st_size,'sha256':sha(S/p)} for p in [p1,p2]])
save(E/'reading-scope.json',{'actual_claim_tip':'0ce8ce7ffa2978e0b2cd136ee44191bdb989479d','actual_claim_capture':'/workspace/scratch/37f0f9248cfc/boss4-r3-next10am-claim.json','primary_bytes':29307,'primary_lines':{x['id']:len(txt(x['id']).splitlines()) for x in src},'all_primary_independently_fully_read':True,'preclaim_only':'17 related complete read snapshots, primary0 at that phase; actual capture verified before primary materialization','related_model_code_full_reads':['customer_attraction/__init__.py','model.py','exact.py','certificate.py'],'input85_policy':'entire JSON all row/action values actually read; original13 off-path differences preserved','new_cone_input':'all6153467B parsed/typed;21case metadata/all Q manually read;5662lambda rows/probabilities retained and fully exact-computed, not manual6MB text-read claim','related_existing_formal_read':10,'old_runs_reused':['router samea83b SHA model result','actual_load sameea6 SHA full input/cert/report','cover samee505 SHA full dependency/replay/report'],'new_runs':['new_security_cones once with explicit52e8 source+a4e8input SHA, no prior codeSHA binding available'],'extra_sources_done':[],'primary_unread_or_truncated_ranges':[]})
receipts=[]
for x in src:
 router=x['id']=='a59d00149f09ad642406';receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':f'完整{x["size"]}字节/{len(txt(x["id"]).splitlines())}行主源码实际全文读完并核inventory SHA，全部控制/输入/输出/断言/默认值原样保。'+('71字节只有包说明docstring，未当验证逻辑。' if x['id']=='8a30bebfdd2a93bc7608' else ''),'comparison_note':('与同SHA旧运行JSON、真实board/root规格差别比较：500标签/有向对计数不当实际Work吞吐，room和(save,id)不覆盖当前真实协议。' if router else '与真实输入/依赖全代码、原/规范85策略差别、576实例回归、21case全字段结构/精确检查、现数学证明及后续纠错实际比较；已done引用源只相关，不复done。')+'旧成功无疑run准确复用，唯一新21锥run明确代码/输入绑定与范围。','decision_note':'integrated为自足资源，保全部独有语义、承重条件/量词、真实证据、数学状态与未覆盖域；有限检查、固定策略全锥和任意六人目标分开，不从标签/计数/负号误升证明；源不改、无shared Git/真实身份/公屏/凭据。','disposition':'integrated','targets':[p1] if router else [p2]})
save(W/'semantic-receipts.json',receipts);save(W/'next-candidates.json',read(E/'next-candidate-snapshot.json'));(W/'relation-review.md').write_text('''# 关系范围\n\n逻辑路由是一般软件规格资源，另三审计是CAG实现/有限检查与固定策略锥证书；不把不同模型或量词强造推导。分数覆盖有完整解析前缀证明、弱桥有解析反族、21锥有逐坐标证书，各自真值和当前half目标分开。相关Boss2原gzip/旧报告和旧资源只比较不覆写/复done；不进mapper或造图连通。\n''')
save(E/'attempts-and-boundaries.json',{'preclaim':'related only until unique capture was actually pushed; five expected IDs all included','exports':'three primary read-only clean show, two exact prior preserved math-auditor bytes, inventory SHA checked all; yielded read processes exited0','run_policy':'router/actual_load/cover exact prior successful evidence reused; no repeat. One new21cone audit because old report lacks auditor codeSHA binding; exit0','new_data_scope':'whole gzip parsed with every field/vector retained and exact all-coordinate arithmetic, not claiming manual6MB numeric prose reading or extra source done','not_done':['shared Git/claim/done/checkpoint/spawn/mapper','real Work/public messages/credentials/network','new general half theorem/novelty/external review','old13 automaton rerun/waterfill rerun','all other audit modules auto-executed']})
checks=[]
def check(n,v):
 checks.append({'check':n,'passed':bool(v)})
 if not v:raise AssertionError(n)
inv={x['id']:x for x in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())}
for x in src+deps:
 p=S/x['saved_path'];check('exact source identity '+x['id'],all(x[k]==inv[x['id']][k] for k in ['path','size','sha256','blob','sources']));check('exact bytes '+x['id'],p.stat().st_size==x['size'] and sha(p)==x['sha256'])
c=read(E/'actual-claim-receipt.json');check('actual pushed subset',c['status']=='pushed' and c['actor']=='Boss4' and {x['id'] for x in src}<=set(c['ids']) and c['local_sync']['status']=='synced')
router=read(E/'context/message_routing_model.json');check('reused router exact source',router['source_sha256']==byid['a59d00149f09ad642406']['sha256'] and router['logical_workers']==500 and router['directed_pairs_checked']==249500)
oldmanifest=read(oldroot/'source-manifest.json')
for ident in ['5ee052fc2fac798bfaaf','19e82f83a9d90ed20863']:check('reused exact auditor '+ident,any(x['id']==ident and x['sha256']==byid[ident]['sha256'] for x in oldmanifest))
check('prior actual full strategy result',a['concrete_full_history_audit']['ordered_decision_nodes']==85 and len(a['concrete_full_history_audit']['all_history_rows'])==85 and a['concrete_full_history_audit']['weak_bridge_gap']=='11/26');check('prior cover true scope',cover['finite_spe']['instances']==576 and cover['finite_spe']['ordered_spe_paths']==2457 and cover['finite_spe']['prefix_comparison_checks']==41182)
run=read(E/'runs/new-cones-run.json');check('new exact source input run',run['returncode']==0 and run['source_sha256']==byid['3e153d43f71d6ebd66e6']['sha256'] and run['input_sha256']==byid['760834c0f64c80b5ccc1']['sha256']);check('normal assertion mode verified',run['same_interpreter_optimization_level_verified_after_run']==0 and run['argv_uses_no_optimization_flag']);check('all21 coefficient checks',new['status']=='PASS' and (new['cases'],new['all_ordered_histories'],new['all_comparisons'],new['identities'])==(21,95349,709573,20971));check('old data result equality preserved',read(E/'new-old-cones-comparison.json')['all_fields_equal_except_source_path']);check('21 true input structures',len(structure['cases'])==21 and sum(x['lambda_terms'] for x in structure['cases'])==5662)
for p in [p1,p2]:
 t=(S/p).read_text();meta=t.split('---\n',2)[1];check('flat MATEK '+p,all(re.search('^'+k+':',meta,re.M) for k in ['id','kind','type_tag','title','status','summary','source_refs']));check('formal C0 '+p,not any(ord(c)<32 and c not in '\n\r\t' for c in t));check('formal trailing '+p,all(l==l.rstrip() for l in t.splitlines()))
check('five primary receipts',len(receipts)==5 and {x['id'] for x in receipts}=={x['id'] for x in src})
for x in receipts:check('complete semantic receipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note']) and all((S/p).is_file() for p in x['targets']))
result={'passed':True,'checks':len(checks),'scope':'exact bytes/full source scope/finite and fixed-cone evidence/receipts/format only; not generalhalf or production certification','formal_forbidden_C0':0,'formal_trailing_whitespace':0,'details':checks};save(E/'self-check.json',result);save(W/'self-check.json',result)
(E/'README.md').write_text('''# 五源逻辑路由与CAG数学审计\n\n主源29307B完整实读：188/1/168/212/66行。原输入/四依赖代码/现正式数学证明与后续纠错实际比较。路由、actual_load、cover同SHA旧成功run复用，不重复；21新策略锥只有旧输入SHA报告，所以新增一次52e8代码+a4e8gzip明确绑定，exit0。\n\n95349有序历史/709573含自身比较/20971坐标精确通过，证明仅固定21完整策略锥；不是三旧selected锥、任意SPE或当前六人half。6.15MB输入全字段结构/精确数字核验不冒称人工逐字阅读，不额外doneBoss2输入/旧报告。源未修，程序assert需正常未优化解释器；无shared Git/实际消息/身份/凭据或网络。\n''');(W/'delivery.md').write_text('''# 五源交付\n\n两自足资源、五integrated收据、五原件/真实依赖/旧精确证据和唯一新增21锥运行。Root按exact manifest复制、实际pushed后done；本子任务不shared Git/claim/done/spawn。下一候选为实际local progress缺项，Root另核全局Owner。\n''')
print(json.dumps({'formal_files':2,'formal_bytes':sum((S/p).stat().st_size for p in [p1,p2]),'primary_bytes':29307,'receipts':5,'checks':len(checks),'passed':True},ensure_ascii=False))
