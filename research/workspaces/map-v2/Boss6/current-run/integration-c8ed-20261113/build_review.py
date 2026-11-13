"""Narrow independent c8ed mathematics review; writes only beside this file."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from datetime import datetime, timezone
import json
import re

ROOT = Path(__file__).resolve().parents[6]
OUT = Path(__file__).resolve().parent
TASK_ID = 'customer-attraction-3a-3a-c8ed896a23eb5fac'

def read(p):
    return json.loads((ROOT / p).read_text())

def raw_sha(p):
    return sha256((ROOT / p).read_bytes()).hexdigest()

def pin(x):
    return sha256(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def dump(name, x):
    (OUT / name).write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')

task_path = f'research/operations/map-v2/tasks/{TASK_ID}.json'
task = read(task_path)
definition, receipt = task['definition'], task['receipt']
integration = read('map/integration.json')
registry = read('research/registry.json')
objects = {o['object_id']: o for o in registry['objects']}
assert task['state'] == 'done'
assert integration['task_receipt_pins'][TASK_ID] == pin(receipt)
assert all(integration['object_pins'][o] == p for o, p in definition['input_pins'].items())
asset_hashes = {a['path']: a['sha256'] for a in receipt['assets']}
assert all(raw_sha(p) == h for p, h in asset_hashes.items())
edge_records = {eid: read(p) for eid, p in task['edge_paths'].items()}
assert all(integration['edge_pins'][eid] == pin(e) for eid, e in edge_records.items())

# Exact small arithmetic only. No original solver, LP, IC tree or pricing audit.
n = 64
u = F(n) - F(1, n)
opt = 2*n*n - 2*n - 2
tail = 2*(n-1)*(n-2) + F(7*n-13, 6)
delta = opt-tail
upper_component = 2*u-delta
upper_pair = upper_component/(n-1)
lower_pair = -F(1, 2)-F(7, 32)
assert (u, opt, tail, delta, upper_component, upper_pair) == (
    F(4095,64),8062,F(15769,2),F(355,2),-F(1585,32),-F(1585,2016))
assert lower_pair-upper_pair == F(17,252)
assert 63*(-14)+2016*(-1) == -2898
assert 64*upper_component == -3170
assert (-2898)-(-3170) == 272
assert 63*64 == 64*63 == 4032

assert [30*F(13,5),150*F(13,5),750*F(13,5)] == [78,390,1950]
assert 90+10+10+1+1 == 112
assert 112+3+14 == 129 and 557+129 == 686
assert F(15)*(5*F(13,5)-5*F(16,3)+F(4,5)) == -193
assert 15*5*F(44,3) == 1100
kcap = {str(ell): [29985*ell*(ell+1)-25000,31000+29985*(4-2*ell)] for ell in [2,3,4]}
assert kcap == {'2':[154910,31000],'3':[334820,-28970],'4':[574700,-88940]}

theorem_path='archives/customer-attraction/state/定理/五人共同最大主题的六十一行有理福利界--定理.md'
theorem=(ROOT/theorem_path).read_text()
weights={name:int(value) for name,value in re.findall(r'\| `([^`]+)` \| (\d+) \|',theorem)}
eight_names=['MAX:fixed:2','MAX:fixed:6','MAX:fixed:7','MAX:fixed:8','MAX:fixed:9','KRS:fixed:3:4','KRS:fixed:5:3','KCAP:4']
eight={name:weights[name] for name in eight_names}
k_sum=sum(weights[f'MAX:fixed:{i}'] for i in [2,6,7,8,9])+78*(weights['KRS:fixed:3:4']+weights['KRS:fixed:5:3'])-88940*weights['KCAP:4']
assert k_sum == 0
B=97275245595766169345344732162388171335572553542163071570
D=48223297642041699827812459022585106799808829370156816010
beta=F(183538199237294659142159872004505983652023685928609569,90987354041588112882665017023745484527941187490861917)
assert F(B,D)==beta and 2<beta<F(5043,2500)

masks=[4,27,29,30,31,32,43,45,46,51,53,54,59,64,127]
leaves=[(0,6,3,4),(1,6,3,4),(2,6,3,4),(3,6,0,1),(4,6,0,1),(5,6,0,1),(6,0,3,4)]
omissions={str(r):[mask for mask in masks if not any(mask&(1<<a) for a in leaf)] for r,leaf in enumerate(leaves)}
assert omissions == {'0':[4,32],'1':[4,32],'2':[32],'3':[4,32],'4':[4,32],'5':[4],'6':[4,32]}
assert all(any(mask&(1<<a) for a in [0,2,5,6]) for mask in masks)

scalar_points=0
for m in range(2,8):
    for W in range(6):
        for I in range(W+1):
            for Dp in range(4):
                for Ds in range(4):
                    for Delta in [F(0),F(1,2),F(2)]:
                        S=F(W)+Delta-Dp-F(I+Ds,m)
                        if S<0:
                            continue
                        E=W-I
                        OPT=I+Dp+Ds
                        rhs=F(2*m-1,m)*W+Delta+F(m-1,m)*(Ds-E)-S
                        assert OPT==rhs
                        assert m*(2*W+3*Delta-OPT)==m*S+W-(m-1)*(Ds-E)+2*m*Delta
                        if OPT-2*W-3*Delta>0:
                            assert Ds-E>F(W+2*m*Delta+m*S,m-1)
                        scalar_points+=1
for m in range(2,8):
    for s in [F(1,2),F(1),F(7,3)]:
        assert 2*(m+1)*s-(2*m-1)*s == 3*s
assert 22-2*22-3*F(7,3)==-29
assert 22-2*19-3*F(7,3)==-23
checks={
    'scope':'Fresh exact scalar arithmetic and finite support identities; no scientific replay.',
    'prefix64':{'u':str(u),'OPT':opt,'F_tail':str(tail),'Delta':str(delta),'root_upper':str(upper_component),'additive_upper':str(upper_pair),'additive_gap':str(lower_pair-upper_pair)},
    'same_histogram':{'count_each_cell':4032,'lower':-2898,'upper':-3170,'gap':272},
    'copy_K_columns':[78,390,1950],
    'KCAP_u_and_K_coefficients':kcap,
    'eight_K_multipliers':eight,
    'weighted_K_sum':k_sum,
    'beta_exact':str(beta),
    'beta_between_2_and_5043_over_2500':True,
    'fixed53_support_omissions':omissions,
    'fixed53_covered_comparison':[0,2,5,6],
    'root_shared_net_scalar_points':scalar_points,
    'scalar_points_are_not_claimed_SPE_instances':True,
    'same_root_G_values':[-29,-23],
    'all_assertions_pass':True,
    'old_LP_solver_IC_pricing_programs_executed':0
}
dump('exact-arithmetic.json',checks)

full_body_paths=[
 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
 'archives/customer-attraction/state/障碍/只见旧客户完整直方图的通用信用不可能性--障碍.md',
 'archives/customer-attraction/state/障碍/允许未覆盖旧客户的归一化负载可加信用--障碍.md',
 'archives/customer-attraction/state/反例/任意人数首步补全余额--反例.md',
 'archives/customer-attraction/state/障碍/最优剩余利润的局部系数与共享负载信用--障碍.md',
 'archives/customer-attraction/state/定理/实际遗漏私有席位谱与锐界--定理.md',
 'archives/customer-attraction/state/引理/私有最优遗漏计划的单根缺陷与尾部席位界--引理.md',
 'archives/customer-attraction/state/推论/共享遗漏减额外覆盖的净缺陷预算--推论.md',
 'archives/customer-attraction/state/算法/完整历史纯SPE终局全集--算法.md',
 'archives/customer-attraction/state/定理/多主题独立保险的三倍根修复与半覆盖等价--定理.md',
 'archives/customer-attraction/state/定理/两名剩余三比较任意背景半覆盖--定理.md',
 'archives/customer-attraction/state/程序/常数三根缺陷原发现与十二完整计划的独立回放--程序.md',
 'archives/customer-attraction/state/资源/三人根缺陷三种子的完整历史计划与客户覆盖--资源.md',
 'archives/customer-attraction/state/构造/五十三单位四人完整策略与内生水位基准--构造.md',
 'archives/customer-attraction/state/引理/五人根复制真实末回复刚性--引理.md',
 'archives/customer-attraction/state/引理/五人共同最大主题变量的复制刚性与容量行--引理.md',
 'archives/customer-attraction/state/引理/五人最大主题根容量切割--引理.md'
]
read_scopes=[{'path':p,'sha256':raw_sha(p),'read_scope':'complete current Markdown body, including stated proof and boundaries','binary_or_program_audit_reexecuted':False} for p in full_body_paths]
read_scopes.append({'path':theorem_path,'sha256':raw_sha(theorem_path),'read_scope':'Beginning through the first 8300 characters: sections 1–3 complete, most of section 4 through the beginning of equation (17); separately complete section 5 multiplier table. Section 4 ending and sections 6 onward not independently read. Eight active shared-K rows and their exact K-column sum reviewed; 53 old rows and 6144-condition pricing audit not reaudited.','binary_or_program_audit_reexecuted':False})

# Per-edge status means THIS independent supplement's scope, not a change to
# the accepted canonical edge and not a replacement for the published review.
reviewed={
 'ca-c8ed-copy-rigidity-pays-krs':('fresh-derivation-reviewed',
  '通用COPY的同一真实K、两路径九合同和全型余项已完整读；90固定有序异对、两组10聚合及含对角25索引的d²给112条。最大源逐客下界整理得15O+193K≤1100u。方向和contribution准确。',
  '仅支付112 COPY；KCAP、大小行及公共K对偶列另付，不认证旧浮点矩阵。'),
 'ca-c8ed-exact-ordered-recursion-supports-root-only-compiler':('fresh-derivation-reviewed',
  'R(q)必要/充分/非空归纳完整已读。有序孩子可独立拼接；指定根孩子保合法目标，其余选各自根利润最小实现，故只根免IC。最大根收益为max(u_a(z),M(0))，遗憾正为max(0,M(0)−u_a(z))。',
  '只完成完整正深度可信计划构造；固定计划锥全IC、共同d、严格有理阳性及去别名仍为其它义务。'),
 'ca-c8ed-fixed-53-support-and-private-spectrum-pay-tail':('fresh-deduction-with-inherited-finite-strategy',
  '完整读53构造的精确输入、成熟399非根/7根证据分解及七真实叶；不重新扫描400动作。新核15兴趣mask×七叶只漏4/32，全覆盖比较(0,2,5,6)成立。q≤2的尾席位支付给OPT4=N≤2W−u1−u2。',
  '任意重数须另满足原τ正深度IC与原合法别名条件；原点静态v4及IC不外推任意重数。'),
 'ca-c8ed-histogram-to-additive':('fresh-derivation-reviewed',
  '若存在归一f，按旧H多重数定义G；b=0被归一抹除，含c=0旧客仍保留，G空=0。两合同逐式等同于已排除的H合同，故方向仅H障碍⇒可加障碍。',
  '只给不可能性；17/252三族证书不由272产品差恢复，已保contribution。'),
 'ca-c8ed-prefix-to-additive':('fresh-derivation-reviewed',
  '全n完整策略分类与同背景尾利润消元均完整实读；n64的u、OPT、Ftail、Δ、首孩子H及信用上界独立Fraction重核。总覆盖F(C)和剩余利润F(b)区分准确。',
  '此源只付交叠组件真实性与根数据；AB/all-big下界及尾利润消元仍由各自正文，不把首步余额负当half反例。'),
 'ca-c8ed-prefix-to-histogram':('fresh-derivation-reviewed',
  '同n64真实组件数据和尾利润已读并重核；64独立产品给相同H的UPPER=−3170。产品F准确可加，未对G错误假设可加。',
  '完整H矛盾还需LOW的63份all-big和2016份AB；该产品证明完整读，源边本身仍准确只报组件贡献。'),
 'ca-c8ed-private-position-seats-pay-omission-in-tail':('fresh-derivation-reviewed',
  '固定私有遗漏子块的逐位置阈值归纳只在正深度使用IC。q个第一席之和≥D，前q大席至少这些席，最后q位逐位置相加支付D；q=0直接OPT≤W。',
  'q≤m−1和全目录私有性承重；共享遗漏、q≥m及53具体支架另有义务。'),
 'ca-c8ed-private-spectrum-to-single-root-defect':('fresh-derivation-reviewed',
  '完整读源残余引理和目标根放松。根强制一个整B_j后仍有足够残余席：无人触块时私有份额直接保底，有人触块时同一叶覆盖包含支配其收益。只根以u1+Δ付一次；正深度各位用原谱。最优比较扩到极大主题保持并集，得D+I/m≤W+Δ。',
  '私有最优遗漏条件用于OPT≤(2−1/m)W+Δ；一般共享遗漏未被支付。'),
 'ca-c8ed-root-capacity-pays-kcap':('fresh-substitution-with-inherited-theorem',
  '完整读容量正文与目标行。整数负载因式分解、同一最大根分支五补元平均以及z≤u方向准确。源k2/3乘10、k4乘20得三条目标行，六个系数已精确重核。',
  '二值四尾两斜率定理只按容量正文完整陈述复用，未新读其独立主body/证书；不宣称新的基础定理全源审计。其余112 COPY/14大小行另付。'),
 'ca-c8ed-root-regret-shared-net-budget':('fresh-derivation-reviewed',
  '固定Q=P\\C的阈值证明不需要最优遗漏全私有；第一席给Dp+(I+Ds)/m。用E=W−I及SΔ精确消元，两个恒等式与严格G阈值已Fraction逐点重核。Δ0为完整SPE目标；m1另由单人最优性给E=Dp+Ds、S=0。',
  '仅净账和必要阈值；没有新增支付Ds−E的真实行，不能二次花E或W。'),
 'ca-c8ed-same-root-vector-cannot-replace-ordered-plan':('fresh-context-reviewed',
  '资源正文已给完整31动作表及同23客户输入，全部实读。只重设V10根0保正深度表；(0,1)处真实平局2/1产生W22/19，同u1与Δ。G−29/−23及{2,3}actual系数1/0、IC系数+1/−1独立核。',
  '这是完整树锥输入信息的有限checks，不否定编译合同；未重跑成熟全树IC。'),
 'ca-c8ed-shared-k-eight-active-rows':('fresh-eight-row-contribution-reviewed',
  '源129行完整读，目标八活跃行3.3和完整乘子表5已读。两个KRS的K列78、五MAX列1及KCAP4列−88940代目标整数权，Python精确加权K列=0。只支付这八行及消列。',
  '其余53旧活跃行与6144条件态全域余项不在本次独立复核，沿既已发布审读和成熟证据保留；不得把八行贡献升级为本次重证完整β。'),
 'ca-c8ed-strict-rational-root-witness-and-insurer-transfer':('fresh-derivation-reviewed',
  '完整读锥合同和保险全部H/LX/LY/LZ历史模式。共同d≥Δ与严格O−2W−3d>0经整体清分母保符号；d>0以s=d修根，新half缺陷≥该正量，d0则旧计划已SPE。完整Cartesian与同人数条件保留。',
  'ALL两源必需；未给任何阳性点，十二负seed/浮点优化不升级为普遍half或精确锥上界。'),
 'ca-c8ed-two-real-tail-players-screen-three-player-root-cones':('fresh-context-reviewed',
  '任意背景两余者定理的四组真实IC、逐客公式及零/正背景证明完整实读。把m3实际根作旧前缀恰余两人，W包含根覆盖，所以O≤2W，d≥0遂排全部严格阳性；有理重数整体清分母合法。',
  'checks只屏蔽m3阳性输入，不反驳条件编译器；不换成尾两人利润，也不外推更大人数。')
}

not_fresh={
 'ca-c8ed-compare-terminal-normalization-costs':'已读完整边文本的两个固定输入比较；34/36完整终局与θ正文未独立读取。',
 'ca-c8ed-d-exact-seven-pays-positive-violation':'已读完整边文本及有理g/权和界；D7七行、旧原子质量和联合283行源码未独立读取。',
 'ca-c8ed-d-joint-finds-seven-rows':'已读活动行发现→一般包络的语境边；D-copy与一般包络主body未独立读取。',
 'ca-c8ed-exact-terminal-recursion-pays-last-average-obstruction':'已完整读一般全集递推；34客户输入与40终局/八最小端点固定证据未独立读取。',
 'ca-c8ed-individual-security-provides-34-client-input':'已读same-input语境边；34客户两主body未独立读取。',
 'ca-c8ed-query-square-pays-old-nonnegative-obstruction':'已读有限两J行−3/13的关系文本；OLD全表与平方正性主body未独立读取。',
 'ca-c8ed-r2fc-checks-finite-collision-free-ends':'已读三个k端点的有限checks文本；碰撞自由B/Q全k归纳与R2fc固定证据未独立读取。',
 'ca-c8ed-r2fc-five-client-audit-load-bridge':'已读五客户全部主题、五节点策略及负载关系文本；其主body/原冻结审计未独立读取。',
 'ca-c8ed-r2fc-seventy-eight-load-two-floor':'已读78客户f2必要界的文本；78客户真实树及11客户独立主body未独立读取。',
 'ca-c8ed-signed-marginal-pays-old-triple-identity':'已读三支持β和53/60失败的关系文本；PM表示定理和OLD数据主body未独立读取。',
 'ca-c8ed-three-tail-profit-pays-d-copy-rows':'已读三尾5/3对两条联合行的索引聚合文本；三尾证明与D源码未独立读取。',
 'cag-unanimous-terminal-residual-pays-sharp-root-bound':'已读自足逐客R−x/m与恒A锐例的完整边文本；两相关主body未独立读取，保留已发布canonical审读。'
}

per_edge=[]
for eid,path in task['edge_paths'].items():
    e=edge_records[eid]
    judgement, derivation, remaining = reviewed.get(eid,('relation-text-only; reuse-published-review',not_fresh.get(eid,''),'本次未独立清偿其完整来源阅读；沿当前已发布同批审读，不新增任何清除声明。'))
    per_edge.append({'edge_id':eid,'path':path,'sha256':raw_sha(path),'native_pin':pin(e),'integration_native_pin_match':True,
        'kind':e['kind'],'relation_mode':e['relation_mode'],'declared_result':e.get('whole_result',e.get('contribution',{}).get('result',e.get('scope'))),
        'this_supplement_judgement':judgement,'mathematical_reason':derivation,'remaining_and_scope':remaining,
        'fresh_review_supports_no_new_pending_clearance':True,
        'current_evidence_refs':e.get('evidence',[])})

fresh_full_body_object_ids=[oid for oid in definition['object_ids']+definition['read_object_ids'] if objects[oid]['body']['path'] in full_body_paths]
result={
 'schema':1,'task_id':TASK_ID,'reviewer':'Boss6 independent integration-c8ed worker',
 'created_utc':datetime.now(timezone.utc).isoformat(),
 'decision':'Already integrated at exact current pins; stop duplicate full-packet reading as instructed by Boss6. Preserve this independent source-reading supplement only.',
 'real_mathematical_errors_found':[],
 'snapshot':{'task':{'path':task_path,'sha256':raw_sha(task_path),'state':task['state'],'owner':task['owner']},
   'registry':{'path':'research/registry.json','sha256':raw_sha('research/registry.json')},
   'integration':{'path':'map/integration.json','sha256':raw_sha('map/integration.json')},
   'receipt_file':{'path':f'map/receipts/{TASK_ID}.json','sha256':raw_sha(f'map/receipts/{TASK_ID}.json')},
   'receipt_native_pin':pin(receipt),
   'all_receipt_assets_byte_SHA_match':True,
   'all_26_edge_native_pins_match':len(per_edge)==26,
   'all_35_input_object_pins_match':len(definition['input_pins'])==35,
   'integration_pending_changes_at_read':integration['pending_changes'],
   'published_review_attribution':'Current review_note explicitly names Boss2 wave21 eight completed packets including this exact task; archives/customer-attraction comparison_scope includes the eight-receipt source/target review.'},
 'reading_scope':{'task_final_receipt':'complete receipt coverage, asset list, core/read endpoints and formal closed_overlaps read',
   'all_26_edges':'actual conditions, directions, explanations, whole/contribution/context scopes read; not all underlying sources independently read',
   'full_current_Markdown_bodies':read_scopes,
   'fresh_full_body_object_ids':fresh_full_body_object_ids,
   'programs_and_binary_evidence':'No raw frozen solver/certificate/action input, original program or full matrix independently reread or executed unless explicitly identified above. Markdown embeds complete V10/V11 31-action tables and precise fixed53 seven leaves, which were read.'},
 'edge_reviews':per_edge,
 'scope_of_discharge':{'fresh_derivations_reviewed':[e['edge_id'] for e in per_edge if e['edge_id'] in reviewed],
   'only_relation_text_reviewed':[e['edge_id'] for e in per_edge if e['edge_id'] not in reviewed],
   'changed_objects_or_edges_cleared_by_this_worker':[],
   'reason':'All current task/edge/object pins already match the published integration and current pending set is empty. This supplement does not mutate integration or clear anything. Unread source scopes are never represented as fresh review.',
   'no_global_or_full_packet_completion_claim':True},
 'exact_arithmetic':{'path':str((OUT/'exact-arithmetic.json').relative_to(ROOT)),'sha256':sha256((OUT/'exact-arithmetic.json').read_bytes()).hexdigest()},
 'unpaid_mathematics':['Shared optimal omissions need a new same-W payment; the net-defect identity does not supply it.',
   'A genuine strict root-only attack needs a full rational positive witness; saved negative seeds/float LP values do not prove universal impossibility.',
   'Fixed53 arbitrary multiplicities remain conditional on genuine positive-depth IC and original legality; static security is not inherited.',
   'Eight shared-K rows do not replace the 53 old true rows and full-domain exact residual proof.',
   'D7 applies to fixed old atom masses; floating negative third-D completion and positive joint violation are separate finite diagnoses.',
   '34/36 endpoint, OLD signed table, collision-free/harmonic and unanimous conclusions retain the domains and inherited published review documented by their existing edges.'],
 'actions':'Only files in this review directory written; no edge/registry/coverage/integration/task edit, no git/sync/queue call, no subagent.'
}
dump('review.json',result)

lines=['# c8ed 已发布集成的独立窄核补充','',
 '当前 task receipt、26 条边和 35 个输入对象的原生 pin 全部与现行 integration 匹配。当前 pending_changes 为空；Boss2 wave21 已明确发布本包数学审读。依 Boss6 后续指示，本次停止重复全包阅读，仅保存已经完成的独立实读与精确小算术。没有发现真实数学错误，没有清除或修改任何图状态。','',
 '本次完整读取模型、两个信用障碍、首步族及尾利润消元、私有谱及根放松/尾席位/净账、全集递推、保险修复、两余者三比较、十二seed编译合同、三人seed完整表、53构造及证据分工、COPY、129行和容量正文。61行定理只读至第4节公式(17)开头，另读完整第5节乘子表；未重审6144条件定价。未执行旧LP、全树IC或旧定价审计。','',
 '已独立核准的实际关系与边界如下：','',
 '| 边 | 本次判断 | 保留义务 |','|---|---|---|']
for e in per_edge:
    lines.append('| '+e['edge_id']+' | '+e['this_supplement_judgement']+' | '+e['remaining_and_scope'].replace('|','／')+' |')
lines.extend(['','精确小算术包括 n64 的同背景利润、17/252 三族差、同H产品272差；COPY共同K列与三条KCAP系数；八活跃行的整数K列严格消去；15种mask在七根的遗漏恒等式；root-only净账的标量等式及严格阈值；同根seed的−29/−23和保险3s成本。标量枚举不被称为SPE实例。详见 exact-arithmetic.json。','',
 '逐文件当前SHA、完整/部分实读范围、逐边判断、原生pins以及未付义务详见 review.json。未独立读取来源的12条边仅复用已发布同批审读，绝不计作本worker新完成的源审计。'])
(OUT/'review.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'review':str(OUT/'review.json'),'md':str(OUT/'review.md'),'fresh_scoped_edges':len(reviewed),'relation_text_only_edges':len(per_edge)-len(reviewed),'full_body_files':len(full_body_paths),'scalar_points':scalar_points,'errors_found':0},ensure_ascii=False))
