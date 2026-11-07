"""Boss2: exact PK identity judgments, complete mature proof entrances, no new proof runs."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[5]
home=Path(__file__).parent
task=json.loads((root/'research/operations/p25-register-v2/tasks/register-ab98f323ad-0094.json').read_text())['definition']
refs=task['materials']
ids=json.loads((home/'new-ids-root.json').read_text())['object_ids']
model='固定有限n≥1和严格正实质量w_i，完整Boolean输入s；向量核K_(S,k),i只在i∈S且s_i=1时等于(Σ_(j∈S)w_js_j)^k，k为非负整数，k0第一分支规定1。K_fin为有限非负组合，未设统一次数上界；V_r为各active表多重线性次数≤非负整数r。'
objects=[]
def own(oid,i,title,kind,status,statement,quantifiers,assumptions,scope,objections,evidence=()):
 o=dict(object_id=oid,version=1,title=title,kind=kind,truth_status=status,model=model,statement=statement,quantifiers=quantifiers,assumptions=assumptions,scope=scope,objections=objections,body=refs[i],evidence=[refs[j] for j in evidence],sources=['source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/positive_kernels/occupancy_rank_faces.md'])
 objects.append(o);return o
own('positive-kernels/occupancy-active-rank',23,'正占用核、完整active表与顶背景交互秩','definition','definition',
 '固定上述核字典，active表f_i(x)=C_i(1,x)，Δ_T f_i(R)=Σ_(A⊆T)(−1)^(|T|−|A|)f_i(1_(R∪A))；q=r+1≤n−1时L_q为全部i、|T|q的顶背景R=N减(T∪{i})差分和。B(C)=Σ_i C_i(1_N)，单核质量b_(S,k)=|S|(Σ_Sw)^k>0。',
 '每个固定n,w和完整表；差分允许合法不交T/R，L_q只在1≤q≤n−1使用。', ['w_i>0；非空支持；有限非负表示'],
 'B是全激活状态总响应，非所有输入状态总和。无需博弈模型。',
 '本轮完整读取0094材料23–29的成熟数学正文和审查范围；复用证明，不重新执行原数学程序。')
face=own('PK-INTERACTION-RANK-FACE-v1',24,'正占用核交互秩的所有表示过滤与暴露面','theorem','proved',
 '对每个C∈K_fin和整数r≥0，C∈V_r当且仅当其每个有限非负表示的每个正项都满足min(k,|S|−1)≤r，亦等价存在此种表示。r≤n−2时该子锥为K_fin∩ker L_(r+1)，L在K_fin非负，故为暴露面；r≥n−1时全锥。单核active秩精确min(k,|S|−1)。',
 '固定n,w；全部已可表示的C；每一个有限非负表示及所有正系数项。',
 ['严格正质量与非负系数；r为非负整数；C预先属于K_fin，禁止真空量词'],
 '高次数与大支持需联合过滤，线性核可有任意支持；不宣称所有资源支持小。',
 '有符号系数可抵消；零质量正确反例是w=(1,0,0)而非(1,1,0)；负质量破坏差分非负。r≥n−1不称真暴露面。', [23,28,29])
budget=own('PK-SHARP-FORBIDDEN-MASS-v1',26,'固定质量的锐坏项预算与合法低秩删项','theorem','proved',
 'n≥2，0≤r≤n−2，q=r+1。γ=min_(|S|≥q+1) q!(|S|−q)e_q(w_S)/[|S|(Σ_Sw)^q]>0，是所有坏单核L_q(K)/B(K)的精确最小值，达到于某支持的k=q。任意给定有限非负表示删min(k,|S|−1)>r项得C_low∈K_fin∩V_r，坏项总B质量≤L_q(C)/γ且逐坐标0≤C−C_low≤L_q(C)/γ。若任意A∈V_r且完整表绝对一致误差≤ε，则L_q(C)≤n binom(n−1,q)2^q ε，该系数为L_q精确绝对系数和。',
 '对每个固定n,w,r，所有有限最高次数、所有给定有限非负表示；固定参数下统一于次数和表示。',
 ['n≥2，0≤r≤n−2，w_i>0；若用ε界须完整表绝对一致误差'],
 '锐性仅是坏单核归一化质量预算，不声称最终距离常数最优。截断输入是已给表示，非未知表恢复算法。',
 'q1时γ=1/2跨正质量一致；q2,n3,w=(1,t,t)时γ趋0，固定质量预算不可扩大为所有质量统一常数。抽样、相对误差及底背景检测不满足此前件。', [23,24,28,29])
closure=own('PK-OCCUPANCY-CONE-CLOSURE-v1',25,'正占用核闭包的unanimity生成与低秩截面交换','theorem','proved',
 '在完整有限维响应表通常欧氏拓扑中，cl K_fin=cone({K_(S,k)}∪{U_S})，U_(S),i=1_(i∈S)∏_(j∈S)s_j，右侧仍为有限非负和。n≥2原锥非闭，n1为闭射线。每个r≥0有cl K_fin∩V_r=cl(K_fin∩V_r)，低秩闭包只增|S|≤r+1的U_S；r≤n−2亦等于cl K_fin∩ker L_(r+1)。r0有限低秩锥闭，n≥2,r≥1则非闭。固定参数γ预算亦延至闭锥：每C∈cl K_fin存在D∈cl(K_fin∩V_r)，逐坐标0≤C−D≤L_q(C)/γ。',
 '每个固定有限n、严格正实质量；每个非负整数r；闭锥预算另限0≤r≤n−2。',
 ['完整有限维响应空间，通常欧氏拓扑；非负系数和严格正质量'],
 '有限表示与闭包不能混同；闭包生成式由归一化紧致性独立证明，截面交换另可用固定质量预算。',
 'U_S/|S|为B1归一化极限；不可把无界次数极限误写成已有有限正表示。闭包审查参与构建后复核，并非全程独立盲审。',[23,24,26,28,29])
bridge=own(ids[0],23,'零动作恒零成本的非负多项式拥塞表占用核表示','representation-lemma','proved',
 '在有限Boolean二动作拥塞模型中，玩家权严格正、资源费用为非负系数多项式，若每个玩家动作0对所有对手状态成本恒0，则每个非零正费用资源不被任何动作0使用；仅动作1使用相应资源。按资源费用单项式展开，完整响应表为K_fin中元素，零费用资源不影响表。',
 '每个满足此前提的有限二动作模型，全部状态同时；不要求均衡。',
 ['每个动作0在所有对手状态成本恒0','资源费用为非负系数多项式；玩家质量严格正'],
 '只是逐状态表示的充分桥，未证明一般含动作0/两动作共用资源的成本表属于该核域。',
 '正负系数或未付零动作定向时不得套用；不推出均衡存在、selector可行性或近似上界。',[24,28])
bridge['model']='有限Boolean二动作加权拥塞模型，玩家逐状态响应为所用资源延迟之和（不另乘自身质量），资源延迟为负载的非负系数多项式，玩家质量严格正；每名玩家动作0恒零响应。'
open_specs=[
 ('非Boolean动作及selector签名的正核接口扩展','为非Boolean动作或selector签名明确合法核、交互阶数和背景差分，证明相应非负性、检测泛函及无界次数极限方向；现有三PK接口未给出此模型映射。','目标扩展域须单独定义，不能仅更名Boolean输入。'),
 ('部分观测及其他误差域的交互秩检测义务','在明确观测分布与量词后，对抽样响应、相对误差或仅偏离比建立适用检测与稳定预算；目前完整表绝对一致误差预算没有覆盖这些误差域，底背景已有漏高背景的边界。','既有预算仍有效；开放的是新误差合同，不能把有限底背景通过当闭包检测。'),
 ('未知完整响应表的非负占用核表示恢复义务','在明确输入编码及正质量的计算域后，由未知完整响应表判定或恢复有限非负核表示，并确定算法及位复杂度；给定表示上的逐项截断不解决此义务。','不宣称此判定已经不可判定或NP难；博弈应用仍须另证所属核域及目标映射。')]
for oid,(title,statement,scope) in zip(ids[1:],open_specs):
 own(oid,27,title,'open-obligation','open',statement,'按所列扩展模型/观测合同/表示输入分别提出的具体未解义务，当前来源未给通用算法或迁移定理。',[],scope,'清楚的数学open，身份及当前来源已明确；不以此阻止三条结构定理登记。',[23,24,25,26])
materials=[]
for i in range(23,30):
 body_owners=[o['object_id'] for o in objects if o['body']['path']==refs[i]['path']]
 owners=[o['object_id'] for o in objects if any(r['path']==refs[i]['path'] for r in [o['body']]+o['evidence'])]
 if body_owners:
  materials.append(dict(refs[i],disposition='objects',object_ids=owners,reason='root完整实读本页成熟陈述、量词、承重证明和纠错；按精确主ID登记，不改正文。'))
 else:
  owners=[face['object_id'],budget['object_id'],closure['object_id']]
  materials.append(dict(refs[i],disposition='attachment',object_ids=owners,reason='审查/有限精确核验分别归三条解析主定理；不以PASS或有限数值另造节点，不把参与闭包构建后复核称全程独立盲审。'))
(home/'pk-fragment.json').write_text(json.dumps(dict(schema=2,objects=objects,materials=materials,edge_files=[],reading_scope={'root_complete_material_indices_zero_based':list(range(23,30)),'remaining_material_indices':list(range(23))+list(range(30,51)),'no_new_mathematical_run':True}),ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'objects':len(objects),'materials':len(materials),'new_ids':ids},ensure_ascii=False))
