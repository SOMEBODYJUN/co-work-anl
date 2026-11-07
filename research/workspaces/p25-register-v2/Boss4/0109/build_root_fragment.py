import json,hashlib
from pathlib import Path
out=Path('research/workspaces/p25-register-v2/Boss4/0109/root-fragment.json')
task=json.loads(Path('research/operations/p25-register-v2/tasks/register-ab98f323ad-0109.json').read_text())['definition']
def ref(p,sec=None):
 x={'path':p,'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
 if sec:x['section']=sec
 return x
m=task['materials'];body=ref(m[41]['path'])
peer='archives/unrelated-machines/state/审查/占位基面与残余边缺口有限审查--审查.md'
peer1='archives/unrelated-machines/state/审查/失真组联合槽舍入与固定汇点占位双源审查--审查.md'
source=['source:1fdb08ccd3717fa2ad9c','source:82af0ae2f147b7c28726']
base={'version':1,'truth_status':'proved','body':body,'sources':source}
objs=[dict(base,object_id='UM-OCCUPATION-MODE-SIDE-CONSTRAINT-v1',title='占位基与有限模式的K侧约束顶点至多2K个非单值home',kind='lemma',model='有限宏到home资格图；所有宏均须覆盖的transversal base多面体B(M)。每home有限0/1 empty/occupied模式，occupied仅依赖该home是否被宏占用；P(Q)为与base匹配相容的实际模式选择凸包。',statement='给P(Q)添加任意K条线性侧不等式。任一交切顶点y正支持中，含至少两项正模式的home数R≤2K。令x占位向量的最小base面为G，混合标签home集F、每home正模式数a_h，则dimG≥|F|/2，dim_P=dimG+Σ_h(a_h−1)−|F|≥R/2，交切顶点又有dim_P≤K。给正支持可用带下界宏匹配恢复覆盖全部宏及强制occupied homes的兼容整数选择，但该支持恢复不自动保侧预算。',quantifiers='任意整数K≥0、任意有限覆盖匹配图、任意上述模式库及有理线性侧约束、每个可行交切顶点；K=0保原积分性。',assumptions=['occupation向量属于覆盖全部宏的base而非仅独立集。','所有同home occupied模式与该home所有可匹配宏同等兼容；不能依赖具体宏身份/尺寸。','y是模式多面体交切的投影顶点；扩展LP任意basic point的投影不一定是它。'],scope='一般模式面维数引理及支持兼容恢复，不直接给预算控制或一般UM调度器。',objections='本轮全文实读M41–44与两个跨批审查，复用成熟双向交替匹配/纤维维数证明；未重跑有限程序。M42只核小规模base暴露面，M43是指数审计函数库；20760是带重数离散权面数，均不冒作任意实权一般证明。',evidence=[ref(m[42]['path']),ref(m[43]['path']),ref(m[44]['path'],'occupation必须是覆盖全部宏的base'),ref(peer,'2. 固定汇点 occupation 模式面：一般引理和算法合同'),ref(peer,'3. occupation 面有限证据（37cf）'),ref(peer1,'二、固定 K 共享汇点的占位拟阵合同')]),
 dict(base,object_id='UM-FIXED-SINK-PRIVATE-GROUP-THREE-HALVES-v1',title='固定K共享汇点与唯一home私有组的给定阈值三半实际调度',kind='algorithm-guarantee',model='显式普通不相关机器；不交homes H与K个sinks Z，宏只可在H，私有任务分成互不交J_h，每任务只可去唯一home h及Z子集；原finite处理时间为非负二进制有理。',statement='给T≥0，所有有限宏端>T/2，在上述结构内确定性算法返回FAIL或一份覆盖全部原任务各一次的实际分配。若OPT≤T必有成功支，故FAIL⇒OPT>T；每成功输出Cmax≤3T/2。T>0时sink向上取整尺度T/(4N)、home保真实时间，每组DP；枚举≤10K² heavy homes/实际模式、删其余heavy模式、lex精确LP投影顶点、带下界宏匹配及模式回溯共同输出。全体sink取整预算5T/4一次，≤2K改变home各贡献≤T/(8K)，得3T/2。',quantifiers='每个固定整数K≥1、每个给定结构/分区与T≥0；总位多项式次数依赖K。对所有合法输入成功⇒输出界，OPT≤T⇒成功；成功不反推OPT≤T。',assumptions=['宏资格剪去p>T后，无端/全覆盖匹配失败可靠拒绝；完整结构满足宏端>T/2。','每个私有job只有一个home组，组间不共享原任务；sink资格可任意子集，home可不可用。','预算按全部N=max(1,Σ|J_h|)共同取整；occupied模式仅是0/1标签，不依具体宏边身份或大小。'],scope='固定K受限UM构造；允许空组、无宏、零/∞和大分母，T=0先用原零端检查。K=0可另用直接残余匹配，但不是此K≥1算法量词。',objections='不把K随输入增长时N的K次DP和heavy枚举称统一多项式。成熟证明完整，原449行程序只核DP/小多面体/支持恢复/阈值逻辑，未交付通用LP或完整scheduler；本轮未重新运行。此项不给未知OPT免费搜索。',evidence=[ref(m[44]['path']),ref(peer,'2. 固定汇点 occupation 模式面：一般引理和算法合同'),ref(peer1,'二、固定 K 共享汇点的占位拟阵合同')]),
 dict(base,object_id='UM-FIXED-SINK-MACRO-PROMISE-APPROX-v1',title='有限宏边严格大于OPT一半承诺下固定汇点三半近似',kind='promise-approximation',model='同固定K、唯一home私有组的不相关机器模型，未输入T或OPT；全部finite时间二进制非负有理。',statement='额外承诺每条有限宏边严格大于OPT/2时，固定K可确定性总位多项式输出完整实际调度Cmax≤3OPT/2。先处理OPT=0；取共同分母积D，有正整数q*=D OPT。宏非空且最小finite宏边a时U=2aD−1≥q*，q≤U均有q/D<2a；宏空用任意合法原调度C令U=DC。初始化U成功并存见证，维持lo<q*及hi成功，FAIL只更新lo，成功只更新hi，至hi=lo+1≤q*返回成功见证。无需接受谓词单调。',quantifiers='每个固定K≥1、每个满足全部有限宏端>OPT/2的合法显式结构输入；O(log(U+1))个给定阈值调用，各数值位长多项式。',assumptions=['含OPT的额外承诺承重，不能免费验证或在一般输入删除。','保给定home/sink分区、唯一home私有组、普通原任务身份和K固定。','先用全部零端处理OPT0；宏非空a=0、U<1或初始失败可报告未认证，promise内不会触发。'],scope='promise类未知最优值近似，区别于给T的单侧FAIL保证和一般UM目标。',objections='成功阈值可以低于OPT而只给三半输出，不得以成功当T可行判定；需要lo<q*的单侧不变量而不是接受集合单调。本轮复用成熟整数网格证明；16380有限表与1024宏网格是阈值逻辑审计，不是端到端scheduler测试。',evidence=[ref(m[44]['path'],'非单调阈值表与固定参数恒等式'),ref(peer,'2. 固定汇点 occupation 模式面：一般引理和算法合同'),ref(peer1,'二、固定 K 共享汇点的占位拟阵合同')])]
ids=[o['object_id'] for o in objs]
mat=[]
for i in (41,42,43,44):
 row=dict(m[i],disposition='objects' if i==41 else 'attachment',object_ids=ids if i in (41,44) else [ids[0]],reason='父Boss4本轮完整实读，按侧约束面/给T算法/含OPT承诺三身份区分；原资源为完整证明或必要算法证据，不为每个有限计数造节点。')
 mat.append(row)
x={'schema':2,'baseline':task['baseline'],'objects':objs,'materials':mat,'edge_files':[],'read_scope':{'complete_mature_bodies':[m[i] for i in (41,42,43,44)],'complete_peer_bodies':[ref(peer),ref(peer1)],'unread_assigned_indices':[i for i in range(len(m)) if i not in (41,42,43,44)],'note':'此为父的成熟部分，不是整批完成；原历史证据/源码未新运行，完整字段待整批合并。'}}
out.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');print(out,len(objs),len(mat))
