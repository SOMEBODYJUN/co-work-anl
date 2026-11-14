"""Prepare scoped candidates. --installed refreshes the authorized receipt after native binding."""
import json, hashlib, pathlib, sys, copy

ROOT=pathlib.Path(__file__).resolve().parents[6]
W=pathlib.Path(__file__).resolve().parent
TASK='boss2-wave22-um-repair-035b5cca45e95a7c'
OLD='unrelated-machines-3a-3a-a44aa88fd1dbbb12'
def read(p): return json.loads((ROOT/p).read_text())
def sha(p): return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def dump(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def ref(p,section=None):
    d={'path':p,'sha256':sha(p)}
    if section: d['section']=section
    return d

t=read(f'research/operations/map-v2/tasks/{TASK}.json')['definition']
old=read(f'map/receipts/{OLD}.json')
registry={o['object_id']:o for o in read('research/registry.json')['objects']}
pin=lambda d:hashlib.sha256(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert all(pin(registry[i])==v for i,v in t['input_pins'].items())
note=str((W/'review.md').relative_to(ROOT))
note_ref=ref(note)
common=f'map/edges/{OLD}/common-small-witness-to-schedule.json'
pair=f'map/edges/{OLD}/pair-subdivision-preserves-method-gap.json'
new=f'map/edges/{TASK}/fixed-half-one-sided-finder-obstruction.json'
destinations={common:W/'candidates/common-small-witness-to-schedule.json',
              pair:W/'candidates/pair-subdivision-preserves-method-gap.json',
              new:W/'candidates/fixed-half-one-sided-finder-obstruction.json'}
for target in (common,pair):
    edge=read(target)
    for k in ['endpoint_pins','evidence_pins','review_digest']:
        edge.pop(k,None)
    for r in edge['evidence']: r['sha256']=sha(r['path'])
    edge['evidence'].append(note_ref)
    edge['reviewed_by']='Boss6'
    if target==common:
        edge['roles']['unrelated-machines/task-level-shared-capacity-algorithm-obligations']='支付一般共同容量义务中的给定见证解码；未知阈值搜索仅作明确finder前提下的形式接续。'
        edge['explanation']='对H外任务按每机p非增切单位槽，交长给每原任务总流1及每槽容量至多1，Hall得到一次覆盖匹配。第一槽支付正支撑最大小端≤原T/2，后槽向前一完整槽收费；固定h_i后同一实际分配逐机≤(3/2+δ)T，H不变。输入包含H,x的全部位长，T0与空任务直接保留。形式上，若另有总确定性位多项式finder对所有OPT≤T均给可验Aδ，则先验输出并舍入，分母积Q网格含OPT，U=Σ_j min_i p_ij给可接受上界；整数二分保持拒绝low<Q·OPT与接受high，即使OPT以下接受性不单调，邻接结束仍得high≤Q·OPT。这里finder前提不是已给算法：当前half-unit证明在P≠NP下，对每固定δ<1/2已排除固定原T/2的此一侧完备总finder；另见本修复新增的精确障碍contribution。'
        edge['scope']='给定共同H,x的完整条件解码，以及明确finder antecedent下的形式阈值搜索。small仍按原T/2；不把被P≠NP障碍排除的finder列作当前可求路线，不否定其他共同容量或一般调度。'
        edge['review_note']='本轮完整实读当前条件槽主证明、half-unit主证明及独立审查，核有序槽全机收费、显式位长、零边界及一侧非单调二分；当前端点为v4。旧独立审查的δ窗口仅按其历史范围读取。'
        edge['contribution']={'result':'给定所列共同见证，验证与保持H的全原任务(3/2+δ)T恢复可确定性总位多项式完成；形式上，一侧完备可验总finder可接未知阈值搜索。',
                              'remaining':'一般任务级共同容量仍需不同可求接口或真实联合槽损失控制。对本边固定原T/2且每固定δ<1/2的finder antecedent，P≠NP下已有half-unit run-and-verify障碍，不能继续当作未受限制的开放构造步骤。'}
    else:
        edge['review_note']='本轮完整实读当前成束/细分review、规范程序合同和独立资源，重核T≥H的配置提升、C<2H的压回、H≤OPT≤2H保值和完整pair行列边际。证据SHA改用当前字节；旧数学contribution保持，有限H网格另有本轮独立Fraction核验，未升级其有限范围。'
    dump(destinations[target],edge)

proof='archives/unrelated-machines/tools/evidence/um-ghmr-flat-moment-and-hall-primary/comparison/research/current/unrelated_machines/joint_matching_completion_and_block_cuts.md'
review='archives/unrelated-machines/state/审查/联合选择槽舍入三源精读--审查.md'
obligation='unrelated-machines/task-level-shared-capacity-algorithm-obligations'
edge={
 'edge_id':'um-035b-fixed-half-one-sided-finder-obstruction',
 'kind':'implies','status':'accepted',
 'source_ids':['UM-JOINT-HALF-CHOICE-NP-v1','UM-JOINT-HALF-PROMISE-NO-v1'],
 'target_ids':[obligation],'premises_mode':'all','relation_mode':'conditional',
 'conditions':'P≠NP。对每个固定有理δ∈[0,1/2)，small恒按原T/2、big为T/2<p≤T。拟议finder须总确定性位多项式，且对每个OPT≤T输入输出可验共同big匹配H与H外small列和1的x，逐机h_i+Σp_ijx_ij≤(1+δ)T；承诺外允许任意字符串或拒绝。',
 'roles':{
  'UM-JOINT-HALF-CHOICE-NP-v1':'唯一half-small、T1、finite仅1/2与1的整个子类中，Aδ存在当且仅当实际OPT≤1，并由显式逐x三激活任务的3DM归约给NP完全性。',
  'UM-JOINT-HALF-PROMISE-NO-v1':'把精确选择困难性转成一侧YES完备总finder的run-and-verify障碍，明确承诺外任意输出及统一多项式时界。',
  obligation:'限制一般构造义务中固定原半阈值、先找Aδ再支付T/2的具体充分路线；一般目标仍开放。'},
 'explanation':'唯一small端迫H外每任务x为0/1，h_i+ℓ_i是half-integer；≤1+δ<3/2即≤1。显式3DM每x三激活任务在R_x各half、big可到含x的S_a；每triple两关联任务small在S_a、unit分别到Y/Z元素机。峰1时每x至少激活一S，故r≥q；每激活S已满unit，两关联件必须撤到总共2q个元素槽，故2r≤2q，提perfect3DM。反向匹配构造完整峰1并给A0。若所列总finder B存在，对任意源实例运行B并精确验证输出：YES满足OPT≤1必有效，NO根本没有Aδ，任何承诺外输出不能误接受。构造、B和验算均位多项式，判定Perfect3DM与P≠NP矛盾。δ1/2时全small已给所有源Aδ，故不纳入严格窗口。若仅保证承诺域内最终停机则此时间推论不成立；已知统一poly承诺时界可截断。',
 'scope':'这是对所列共同见证finder的条件障碍contribution，连到开放问题的具体接口。不是refutes整个一般UM目标，不否定给定H,x的有序槽恢复、改变分界、直接实际调度或利用真实槽损失的其他路线。',
 'contribution':{
  'result':'假设P≠NP，每固定δ<1/2，固定原T/2的Aδ接口不存在在所有OPT≤T上保证输出见证的总确定性位多项式finder，即使T1、唯一small、finite仅1/2和1。',
  'remaining':'一般任务级共同容量与统一次二实际调度仍需其他接口、联合舍入或更精确损失控制；本障碍没有排除一般(2−ε)调度算法，也没有将δ1/2端点判为可解。'},
 'evidence':[ref(review,'2. Half-unit joint-choice 与 3DM/promise 障碍'),
             ref(proof,'1. 共同匹配与剩余分数容量的精确接口'),
             ref(proof,'3a. 半单位任务封闭共同见证的整个低于2窗口'),
             ref('archives/unrelated-machines/tools/evidence/um-ghmr-flat-moment-and-hall-primary/comparison/research/reviews/unrelated_machines/half_unit_joint_choice_review.md'),
             ref('archives/unrelated-machines/state/文献/Karp归约框架与完全问题--文献.md','5.2 原3DM归约的全部坐标与循环一致性'),note_ref],
 'reviewed_by':'Boss6',
 'review_note':'完整实读两个当前登记对象及原§3a/独立审查，独立复核half积分性、r双边计数、run-and-verify量词和δ端点。新有限脚本比较全部q≤2源和额外重复/孤立输入，只作边界复核。来源为conditional(P≠NP)，目标用局部contribution，不冒作开放对象全称反驳。'}
dump(destinations[new],edge)

receipt=copy.deepcopy(old)
for i,cov in receipt['coverage'].items():
    cov['object_pin']=t['input_pins'][i]
    cov['comparison_scope']='定向复用前批已完成的比较，本轮核当前登记与原asset/证据SHA；前批范围：'+cov['comparison_scope']
private='UM-PRIVATE-CLAUSE-QUERY-RETURN-UNIVERSAL-THREE-HALVES-v1'
receipt['coverage'][private]['comparison_scope']='本轮完整实读当前v3主证明、异权私有子句续审查及登记，重新核正T outside位置染色、全部cross库、共同N+h/2N+h匹配、重复pin标签、完整原任务回填；复用前批与乘积切片的模型对照。'
pairid='UM-PAIR-SUBDIVISION-GAP-v1'
receipt['coverage'][pairid]['comparison_scope']='本轮完整实读当前v2成束review及程序/独立资源三份合同，重新核T≥H提升、C<2H压回、保值H区间、完整pair边际及两树阈值仅上界；不重跑旧k4巨图。'
small='UM-JOINT-SMALL-ROUND-v1'
receipt['coverage'][small]['comparison_scope']='本轮实读当前v4、主§1–2与§3a、当前half-unit及旧joint-matching独立审查、共同槽三源审查、Hall有限审计，按固定原T/2比较给定H,x的正向解码和一侧完备finder障碍。'
receipt['coverage'][small]['reason']='给定共同H,x时Hall与前槽收费完整，H不变、零目标/空任务及显式总位长均保留；形式上的一侧搜索接续不需要低阈值单调。但固定原T/2且每固定δ<1/2的总finder在P≠NP下由half-unit run-and-verify排除，不能继续把它作为尚无约束的正面构造缺口。此障碍不反驳本给定证书定理或一般UM。'
cov=receipt['coverage'][obligation]
cov['comparison_scope']='复用前批固定阶矩、逐对细分、固定槽同步修复的已付比较，并本轮实读问题页与新共同H/x正向及half-unit一侧finder障碍；各路线保独立模型和量词。'
cov['reason']='给定共同见证的确定性全任务恢复是已付步骤；形式阈值搜索的finder antecedent须单列。P≠NP下，固定原T/2与每固定δ<1/2的Aδ一侧完备总finder已被半单位归约排除，故具体路线受阻而一般任务级容量仍open。固定阶保矩、独立pair及单目的地同步批次各只限制其明示接口，不能合为一般调度不可能性；新余量、联合真实槽损失或不同可求系统仍待构造。'
cov['edge_ids'].append(edge['edge_id'])
receipt['object_ids']=t['object_ids'];receipt['read_object_ids']=t['read_object_ids'];receipt['input_pins']=t['input_pins']
receipt['follow_up_tasks']=[];receipt['closed_overlaps']=[]
assets=[]; supersession={}
for a in old['assets']:
    p=a['path']
    if p in destinations:
        assets.append({'path':p,'sha256':sha(p) if '--installed' in sys.argv else hashlib.sha256(destinations[p].read_bytes()).hexdigest()})
        supersession[p]={'disposition':'replaced','replacement_paths':[p],
                         'reason':'当前登记/必要来源订正后重审并刷新绑定；保留仍有效数学contribution。'+('明确给定证书与被P≠NP限制的finder前提。' if p==common else '保T≥H、C<2H与H保值区间以及pair非全局量词。')}
    else:
        assert sha(p)==a['sha256']
        assets.append(a)
        supersession[p]={'disposition':'retained','reason':'原asset字节不变；全部当前端点pin及证据SHA仍匹配，完整解释已读，复用前批已付比较。'}
assets.append({'path':new,'sha256':sha(new) if '--installed' in sys.argv else hashlib.sha256(destinations[new].read_bytes()).hexdigest()})
receipt['assets']=assets
receipt['supersession']={OLD:{'reason':'三项登记来源订正的定向修复；22核心保留，8旧边原SHA保留、2旧边同路径替换，并新增固定原半阈值finder的精确条件障碍。', 'assets':supersession}}
dump(W/'receipt-candidate.json',receipt)
manifest={'task_id':TASK,'status':'workspace-candidates-awaiting-native-binding',
 'copies':[{'source':str(p.relative_to(ROOT)),'destination':d} for d,p in destinations.items()],
 'receipt_candidate':str((W/'receipt-candidate.json').relative_to(ROOT)),
 'receipt_destination':f'map/receipts/{TASK}.json',
 'after_native_binding':'Run this script with --installed, then copy receipt-candidate.json to receipt_destination; verify before checkpoint/done.',
 'preserved_assets':8,'replaced_assets':2,'new_assets':1,'coverage':len(receipt['coverage'])}
dump(W/'install-plan.json',manifest)
audit=[]
for a in old['assets']:
    d=read(a['path'])
    audit.append({'path':a['path'],'asset_sha_matches':sha(a['path'])==a['sha256'],
      'endpoint_deltas':{i:{'old':v,'current':t['input_pins'][i]} for i,v in d['endpoint_pins'].items() if v!=t['input_pins'][i]},
      'evidence_deltas':[{'path':r['path'],'old':r['sha256'],'current':sha(r['path'])} for r in d['evidence'] if r['sha256']!=sha(r['path'])]})
dump(W/'old-asset-audit.json',audit)
print(json.dumps(manifest,ensure_ascii=False,indent=2))
