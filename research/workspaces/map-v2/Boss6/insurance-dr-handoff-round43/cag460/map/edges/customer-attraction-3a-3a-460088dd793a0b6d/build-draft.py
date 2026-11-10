"""Boss6: read-only fixed-certificate application; writes only this staging tree.

No LP, SPE search, full row regeneration, NumPy projection traversal, git or queue.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json
import sys
import difflib

ROOT = Path('/workspace/scratch/bbb425bb840f/co-work-anl-boss6')
OUT = Path(__file__).resolve().parent
TASK = 'customer-attraction-3a-3a-460088dd793a0b6d'
REL = 'map/edges/' + TASK
STAGE = OUT.parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from research_runtime import edge_bindings, pin, require_edge_result

def get(path):
    return json.loads((ROOT / path).read_text())

def put(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def ref(path, section=None):
    result = {'path': path, 'sha256': sha256((ROOT / path).read_bytes()).hexdigest()}
    if section:
        result['section'] = section
    return result

task = get('research/operations/map-v2/tasks/' + TASK + '.json')
definition = task['definition']
registry = get('research/registry.json')
objects = {o['object_id']: o for o in registry['objects']}
assert task['owner'] == 'Boss6' and task['state'] == 'claimed'
for oid, expected in definition['input_pins'].items():
    assert pin(objects[oid]) == expected, oid
for r in definition['context_plan']['reading_refs']:
    assert ref(r['path'])['sha256'] == r['sha256'], r['path']

P = 'customer-attraction/six-actual-fourth-five-row-full-index-projection-independent-review-scope'
OLD = 'M-5d7bf32e11384c81bce9adfb2b273883'
RIG = 'customer-attraction/all-m-nearly-saturated-root-rigidity'
FIVE = 'CA-FIVE-INDEXED-ROWS-NO'
SAT = 'customer-attraction/five-indexed-primal-root-saturation-incompatibility'
DYN = 'customer-attraction/dynamic-exchange-assignment-certificate'
STATIC = 'customer-attraction/frozen-suffix-optimal-topic-assignment-counterexample'
REWARD = 'customer-attraction/closeout-c51b12d5cc02690c50ef6183'
BOSS9 = 'customer-attraction/closeout-2d733632702535e93ba596f9'
MIN = 'M-66132ab86a054b33b1c753158dd4f3ad'
MAX = 'M-e3fc9489148a4369adfc1e663579be9c'

proj_body = objects[P]['body']['path']
sat_body = objects[SAT]['body']['path']
rig_body = objects[RIG]['body']['path']
five_body = objects[FIVE]['body']['path']
cert_path = 'archives/customer-attraction/tools/evidence/five-player-indexed/evidence/certificates/customer_attraction/five_player_indexed_bound.json'
proj_dir = 'archives/customer-attraction/tools/evidence/R964-six-independent-fourth-projection-three-primary/'
point_path = proj_dir + 'related-original/b43e77694bd2abc24dfe/research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba/parent/joint_system.json'
table_path = proj_dir + 'related-original/b62dfdc807c4b60b5083/research/workspaces/customer-attraction/R-964def22ed03479582e83410444f2ea2/parent/fourth_indexed_projection.json'
point = get(point_path)['certificate']
table = get(table_path)
coeff = {(x['actual_bits'], x['d']): int(x['coefficient']) for x in table['coefficients']}
assert len(coeff) == len(table['coefficients']) == 448
separation = sum((F(x['weight']) * coeff[x['actual_bits'], x['d']] for x in point['support']), F())
assert len(point['support']) == 14 and all(x['d'] == 1 and F(x['weight']) > 0 for x in point['support'])
assert separation == F(table['exact_separation']) < 0

primal = get(cert_path)['primal']
atoms = primal['atoms']
mass = [F(a['mass_numerator'], primal['denominator']) for a in atoms]
bits = [tuple(map(int, a['bits'])) for a in atoms]
u = sum((n * F(b[0], sum(b[:5])) for n, b in zip(mass, bits) if b[0]), F())
csize = sum((n * b[2] for n, b in zip(mass, bits)), F())
dsize = sum((n * b[3] for n, b in zip(mass, bits)), F())
cd = sum((n for n, b in zip(mass, bits) if b[2] and not b[3]), F())
dc = sum((n for n, b in zip(mass, bits) if b[3] and not b[2]), F())
inter = sum((n for n, b in zip(mass, bits) if b[2] and b[3]), F())
assert len(atoms) == 64 and min(mass) > 0
assert csize == dsize == 5 * u and cd == dc > 0
assert inter / 5 + dc == u + F(4, 5) * dc > u
arithmetic = {
    'scope': 'Two fixed applications of mature exact certificates; not a new universal-row or SPE audit.',
    'projection': {'input': ref(point_path), 'table': ref(table_path), 'support_count': 14, 'all_d': 1,
                   'exact_weighted_sum': str(separation), 'table_keys': 448,
                   'five_row_projection_regenerated': False, 'old_701_feasibility_rechecked': False},
    'root_saturation': {'input': ref(cert_path), 'atoms': 64, 'all_positive': True,
                        'root_u': str(u), 'C': str(csize), 'D': str(dsize),
                        'C_minus_D': str(cd), 'D_minus_C': str(dc), 'intersection': str(inter),
                        'last_D_profit_on_all_C_branch': str(inter / 5 + dc),
                        'strict_excess': str(F(4, 5) * dc),
                        'primal_437_feasibility_rechecked': False, 'dual_global_domain_rechecked': False},
    'new_lp_calls': 0, 'new_SPE_tree_audits': 0, 'original_entry_runs': 0,
}
put('fixed-application-arithmetic.json', arithmetic)

edge1 = {
    'edge_id': 'cag-460088dd-fullindex-necessary-cut-excludes-fixed-701-marginal',
    'kind': 'implies', 'status': 'accepted', 'source_ids': [P], 'target_ids': [OLD],
    'premises_mode': 'all', 'relation_mode': 'unconditional',
    'conditions': '同六人模型、同一完整σ及六个合法比较槽。应用输入为SHA595e9299…证书的全部14个d=1原子与原有理质量；欲排除的延拓必须保持其(a,d)质量边缘。当前只做该固定输入求和，不把旧701行可行性当本轮新验证。',
    'roles': {P: '同σ五个真实总slack的正权和，完整八格联合直方图逐客户最大化后给ΣM≥0；固定v1五权和448格。',
              OLD: '同一个14原子边缘的精确加权和严格为负，故其所有保持边缘的完整SPE延拓被必要行排除。'},
    'explanation': '对任何假设的保边缘延拓，各真实隐藏(t_i,b_i,c_i)联合直方图属于该1716型扩大域，故客户真实60倍加权slack≤M(a,d)。同一σ的五条总行各非负，所以Σ客户M≥60Σ_r L_r S_r≥0。固定全部14原子直接代入同一448格表却得Σweight·M=' + str(separation) + '<0，矛盾。该计算只消费14个质量及其d1系数；新行必要性不依旧701行可行性。若另借原成熟701可行证书，可进一步解释信息增量，但不把该额外历史验证当本边已重跑。逐客户取max是放松；min方向无法给这一不等式，各客户max共同可实现也未被要求或证明。',
    'whole_result': '指定D=2328624438118763005493408946711611424627685837归一的全部14个d1正质量原子违反该第四位五行必要上包络，行值为−477655697294286535400901211536620530629699393508359780/D<0；故不存在保留其实际六位/比较重数质量边缘的完整六人纯SPE延拓。',
    'scope': '完整覆盖目标M-5d7…的固定点非延拓句；不判新702/5108/5180系统、其它权、另一第四位B投影、ROW或六人half。',
    'evidence': [ref(proj_body), ref(point_path), ref(table_path)],
    'reviewed_by': 'Boss6', 'review_note': '已实读真五行、强PAIR恒等式、最大投影方向、448表与14原子；按成熟全域合同复用，当前仅复核固定14项精确和。逐目标核whole_result，未以必要松弛点冒SPE反例。',
}
edge2 = {
    'edge_id': 'cag-460088dd-indexed-primal-and-root-rigidity-exclude-fixed-completion',
    'kind': 'implies', 'status': 'accepted', 'source_ids': [FIVE, RIG], 'target_ids': [SAT],
    'premises_mode': 'all', 'relation_mode': 'unconditional',
    'conditions': '固定同SHA18e074…旧437行64原子、ABCDEUVWXY会员及旧质量与名义实际根收益u；C,D均为合法主题。允许扩目录或拆分原子，但须逐客户保持该联合投影和根利润；单位整数实现可同倍清分母。',
    'roles': {FIVE: '精确指定旧437行primal及64原子质量/会员数据；可行松弛和对偶最优性各守其域。',
              RIG: '任意m和同σ根偏离的大小界及Δ=0饱和集合刚性；专门取m=5。',
              SAT: '同一固定旧点有两个等大但异覆盖饱和主题，故保会员质量与根收益的全部共同目录完整SPE扩展不存在。'},
    'explanation': '先从同一64原子证书仅以Fraction重算A的名义根收益u、C/D大小与差，得到u=' + str(u) + '、|C|=|D|=5u及|D\\C|=|C\\D|=' + str(dc) + '>0。若存在所声明保数据完整五人σ，根可强制任一目录主题T而保证|T|/5，故全目录|T|≤5u。真实强制C后根IC与下界相等，每个C客户必须负载5，后四个主题覆盖均含C且大小≤|C|，所以各覆盖恰C。真实末位此时改D得到|C∩D|/5+|D\\C|=u+4|D\\C|/5>u，违反该同σ真末位BR。这是RIG的m5、Δ_C=0特例。CA-FIVE的O>2W仍只是必要系统点，不提供完整策略；本推导解释同一点为何不能补全，不否认其437行精确可行/最优性。',
    'whole_result': '固定SHA18e074…的旧质量、C/D会员与根收益u时，C,D大小均为5u且双向差各29804534291965508075715774863499600009/(2·70560308704423797361284609157664425493)>0，与任意完整五人纯SPE的根饱和集合刚性冲突；不存在保这些数据的全目录补全。',
    'scope': '完整支持目标固定64点全目录非补全，不外推到所有437点、重优化527/1067/3524/3935点、旧60原子557点或五/六人half。',
    'evidence': [ref(five_body), ref(cert_path), ref(rig_body), ref(sat_body)],
    'reviewed_by': 'Boss6', 'review_note': '完整读RIG全m逐客户因式证明和饱和特例、同点obstruction及437必要模板合同；当前静态复核64个会员/质量汇总，不重复LP/437全行/全域对偶或SPE树。共同前提保单条ALL。',
}
edge3 = {
    'edge_id': 'cag-460088dd-frozen-dynamic-certificate-checks-static-assignment-refutation',
    'kind': 'checks', 'status': 'accepted', 'source_ids': [DYN], 'target_ids': [STATIC],
    'premises_mode': 'all', 'relation_mode': 'context',
    'conditions': '相同六标签1953单位客户输入SHA2ae935…、完整策略SHA1c59b0…和冻结精确报告SHA82dc1b…；只复用其成熟43完整历史/258比较合同，不把当前来源保全重新命名为全树新执行。',
    'roles': {DYN: '保全Möbius输入、完整43历史策略、原精确报告与作者回放代码，作为固定反例的检查证据来源。',
              STATIC: 'proved的同输入静态最优元组/排列存在式反例；其完整结论另有原始输入独立审计，source保全与数学结论身份分开。'},
    'explanation': '两页逐字段对应同一actual034、收益(1733/3,1736/3,1736/3)、W1735、唯一最优支持125及OPT1740。正singleton质量排除重复最优元组；全部最优有序元组只是125的六排列。去β1736/3后的冻结矩阵[[0,-1,0],[1,0,1],[0,0,0]]的全部六排列费用是1736/1737/1736/1736/1737/1736，最小W+1，穷尽了“存在最优tuple、存在排列”两个量词。真实根选1/5后suffix改变为(2,0)/(0,2)，与冻结(3,4)不同，原真实IC并未失效。证书原报fresh=37历史/156比较、full=43/258；旧两页fresh转写错误及“缺witness”登记误述已提出原处修订，修订前本context文字按原JSON的真实数值使用。',
    'scope': '保存固定反例的来源检查关系；不将finite证据保全对象偷升普遍定理，不反驳弱冻结预算、真实动态ROW或half（本例half余量1730）。该核心只有context，coverage仍isolated-after-review。',
    'evidence': [ref(objects[DYN]['body']['path']), ref(objects[STATIC]['body']['path']),
                 ref('archives/customer-attraction/tools/evidence/dynamic-exchange/original/assignment_exact_audit.json'),
                 ref('archives/customer-attraction/tools/evidence/dynamic-exchange/original/assignment_full_policy.json'),
                 ref('archives/customer-attraction/tools/evidence/dynamic-exchange/original/assignment_instance.json')],
    'reviewed_by': 'Boss6', 'review_note': '已读两完整正文、原author全文、witness/代码/冻结报告及后续独立审查量词合同；current未运行作者入口、发现器或258比较，复用成熟精确合同。已read-add实际pushed后纳端点；known原文错误由独立patch交Boss。',
}
edges = [('fullindex-cut-excludes-fixed-701-marginal.json', edge1),
         ('indexed-primal-and-root-rigidity-exclude-fixed-completion.json', edge2),
         ('dynamic-certificate-checks-static-assignment-refutation.json', edge3)]
canonical_matches = []
for p in registry['edge_files']:
    e = get(p)
    for _, new in edges:
        if e.get('kind') == new['kind'] and set(e.get('source_ids', [])) == set(new['source_ids']) and set(e.get('target_ids', [])) == set(new['target_ids']):
            canonical_matches.append({'path': p, 'sha256': ref(p)['sha256'], 'edge_id': e['edge_id']})
assert not canonical_matches, canonical_matches
for name, edge in edges:
    require_edge_result(edge)
    edge.update(edge_bindings(ROOT, edge, objects, verify=True))
    put(name, edge)

coverage = {}
def cov(oid, state, reason, scope, eids=None):
    x = {'state': state, 'object_pin': definition['input_pins'][oid], 'reason': reason, 'comparison_scope': scope}
    if eids:
        x['edge_ids'] = eids
    coverage[oid] = x

cov(P, 'linked', '普遍必要上包络确能排同一14原子边缘；方向是隐藏贡献≤max投影。完整same-σ五行先付清，不能以逐客户max的存在误称共同策略。',
    '与M-5d7…全文同页比较；读真实S0…S4、强PAIR、完整1716直方图/448格和独立程序原报告；未重跑109824配置。', [edge1['edge_id']])
cov(OLD, 'linked', '固定14点ΣwM严格负与任何完整SPE的ΣM≥0矛盾，whole_result覆盖其固定边缘非延拓。旧701可行性按原成熟证书复用，不将必要点W/O误作SPE/half反例。',
    '全部14支持及d1系数、必要行域和same σ量词；与fullindex theorem比较而非另一第四位B投影。', [edge1['edge_id']])
cov(MIN, 'isolated-after-review', '与max规则是独立输入/方向，互不推出。17客户三人五主题例有五处逐坐标极小删除，根T4地板31/6→37/6使最坏15→17；降当前过去租金不等于保祖先可信支持。未发现这两个精确反例间的逻辑迁移；保所有规则相等向量/根/终端约定。',
    '完整Pareto正文E递推/v_b定义/四输入与5删除；精确JSON的根集合、地板、删除及节点数，303节点全策略按成熟证书复用未重跑。')
cov(MAX, 'isolated-after-review', '三独立max例均因一次末位平局删去较低过去租金真实孩子，祖先阈值被抬，最坏10→11、11→12、18→21。不能由min失败推出max失败，亦不否定全部可证明状态压缩；所列真实SPE均half。',
    '与min完整比较A/B/D逐项占优数据及真实根地板；保每已占主题一坐标、不乘背景次数、未来利润不同于完整覆盖。')
cov(BOSS9, 'isolated-after-review', 'README只说明实际D^r且fresh Ai后真实尾Bi^r模板在r≥2有两个末位菜单d≥rc/2、d≤c/(r+1)冲突。跨主题信用、多层支付及森林UTP跨坏终局叶消息仍open；无完整SPE/half反例，不把与两奖励尾名称相似视作定理迁移。',
    '完整审查、1890B原README与比较记录；与本包两奖励尾不同目录/回复限制核边界，未假称读取未领取repeated_tail/forest候选完整证明。')
cov(SAT, 'linked', 'ALL旧437原子证书与全m根刚性专取m5、ΔC=0，给同64点C/D正差矛盾；完整whole_result。两in-packet精确overlap均已比较，无额外follow-up。',
    '同SHA64原子固定会员及质量、实际根u，RIG全部证明、CA-FIVE437系统/双证书作用域、资源437指定旧点section、两真实投影完整正文。', [edge2['edge_id']])
cov(REWARD, 'isolated-after-review', '完整原4668B证明可复用且独立补核。d≥x；a>0时旧Aj保证L=x/2+a，排两回复Ai/Ci且双Bi被末D严格击败，故末个Ci偏Ai获≥L迫a≤x/2，OPT/W≤3/2。当前正文错误D触及Xi一句及承重省略已给最小修订；数学已付，不记open。其指定族不直接推出本包其它完整陈述。',
    '完整现body、原two_reward_tail_obstruction.md全部证明；k≥3、全部块两两不交、恰目录、same σ真实尾、a0与b0平局逐项核；不重跑1514扫描或全树。')
cov(DYN, 'isolated-after-review', '已有原冻结证据可checks同输入静态存在式反例，但finite保全记录仅作context；完整反例另守proved身份。fresh应37/156、full43/258，witness在七源且audit可独立于发现器重放，误述已给修订。半覆盖余量1730，真实改后缀不同于冻结assignment，均未外推。',
    '与read-add的v4静态反例全量词比较，完整现/原author正文、witness、Fraction代码与报告；读取输入/全policy结构和绑定，按成熟合同0新全树运行。')

reading = {
    'task_id': TASK, 'owner': task['owner'], 'request_id': task['request_id'],
    'input_pins_checked_from_current_records': definition['input_pins'],
    'all_declared_ref_bytes_match': True,
    'complete_semantic_read': [
        'AGENTS.md; research/IMPLEMENTATION.md(all322 lines in chunks); prompts/03-map-worker.md; primary brief; actual task definition and12 endpoint records',
        proj_body + ' (all230 lines including448 values and14 support)',
        objects['CAG-MODEL']['body']['path'],
        objects[MIN]['body']['path'], objects[BOSS9]['body']['path'], sat_body, rig_body,
        'archives/customer-attraction/state/计算/六十四原子的两份真实投影与保存门槛分版--计算.md',
        'archives/customer-attraction/state/定理/五人索引最优偏离福利界--定理.md(all407 lines including row generation,57 multipliers,global proof and32 minima)',
        'archives/customer-attraction/state/计算/五人索引偏离双证书--计算.md',
        objects[REWARD]['body']['path'], objects[DYN]['body']['path'], objects[STATIC]['body']['path'],
        'archives/customer-attraction/tools/evidence/R-077c0cacfba24288be91dee1acf6d484/first/original/a1a068311b18332bba1a.md (all4668 bytes)',
        'archives/customer-attraction/tools/evidence/workspace-r12-credible-attack-20261031/original/README.md',
        'archives/customer-attraction/tools/evidence/workspace-r12-credible-attack-20261031/comparisons/comparison-notes.md',
        'dynamic-exchange/original/README.md; static_optimal_assignment_counterexample.md; assignment_witness.json; assignment_exact_audit.json; audit_assignment_witness.py (all text,not executed)',
        'archives/customer-attraction/state/引理/冻结指派的客户恒等式与最优比较量词--引理.md',
        'archives/customer-attraction/state/审查/静态最优指派桥盲审的双求值与量词核对--审查.md',
        'R964 review_fourth_projection.py and original819B report (all text,not imported/executed)',
        'five-player-indexed original main2560B and independent2115B reports (all fields including32-group tables)',
    ],
    'selected_bearing_spans_and_fields': [
        '任意主题根行的刚性等价与有限补全探针--资源.md only exact unique section437行指定旧点的根饱和排除; remainder byte checked only',
        '五人索引偏离模板--障碍.md §§1–4 complete mathematical contract; §5 numerical64-row table partly displayed, not claimed new full table audit; all64 bits/masses consumed separately for fixed saturation application',
        'joint_system.json certificate(all8 fields,all14 support); menu_cuts/pair_cuts/records structure only, not old701 audit',
        'fourth_indexed_projection.json all448 entries bound to the complete body table; fixed14 entries consumed arithmetically; no regeneration of109824 hidden configurations',
        'four-pareto-cases-and-floor-consumption.json all4 fixed cases orientation/input size/root menus/welfare/floors/pruning events/node and comparison counts; existing303 ordered actions/slacks reused by exact SHA contract; no claim complete raw131597B reread; unrelated floor_report_consumption not used',
        'five_player_indexed_bound.json metadata/type orders/primal normalization/all64 bits/masses; dual beta/row count/scope/57-coefficient mature theorem proof read; all histograms/437 raw row names not freshly reaudited',
        'dynamic assignment_instance.json and assignment_full_policy.json exact bytes/schema/43-key contract checked; all policy values already read in author tables; no new1953-unit/258-IC replay',
    ],
    'mature_contract_reuse': {
        'CA-FIVE-INDEXED-ROWS-NO': 'SHA18e074… with primary and independent exact reports; 437 feasible rows/74 tight/57 positive multipliers,6144 domain conditions. No new LP or global proof traversal execution.',
        'Pareto': 'SHAc58e045… fixed full ordered witnesses303 histories/1430 comparisons; no new tree or random scans.',
        'projection': 'SHA6c447fb… original109824-case report; current short14-term sum only.',
        'assignment': 'SHA82dc1b… original37 fresh/43 full histories,156/258 comparisons; independent current proof body contract reused,0 new code entry.',
    },
    'new_computation': 'Only source SHA/pin/JSON structure and14-term/64-atom fixed Fraction arithmetic; no NumPy hidden traversal,LP,original main or SPE tree.',
    'canonical_search': 'Registry canonical edge_files filtered for every core/read endpoint; exact new source/target/kind sets absent. Existing root→shared-punisher and ALLroot+rigidity→localLP have different targets and are not duplicated.',
    'read_add': {'object_id': STATIC, 'actual_request_id': task['request_id'], 'pin': definition['input_pins'][STATIC]},
    'declared_references': definition['context_plan']['reading_refs'],
}
put('reading-ledger.json', reading)

reward_path = objects[REWARD]['body']['path']
reward_old = (ROOT/reward_path).read_text()
start = reward_old.index('再看最后一个实际选 (C_i) 的玩家。')
end = reward_old.index('因此真实覆盖福利为', start)
reward_step = r'''再看最后一个实际选 (C_i) 的玩家，重标其组为 (i)。其原收益为 (x)，因为随后两个 (D) 均不触及 (X_i)。令它偏离 (A_i)，并沿同一完整策略在该改变后有序历史后的真实两人子SPE继续。若 (a=0)，结论已成立；以下设 (a>0)，记 (L=x/2+a)。

第一名回应者可选任一旧组 (j\ne i) 的 (A_j) 保证 (L)。末位若选 (C_j)，得 (x/3)，严格不及合法 (D) 的 (b+d\ge x)；若选 (A_j)，得 (x/3+a/2)，严格不及另一旧组 (\ell\ne i,j) 的 (A_\ell) 所给 (L)；若选 (B_j)，得 (x/3+b)，严格不及 (D) 的 (b+d\ge b+x)。因此每个真实末位最佳回复都不再触及该旧组，第一回应者选 (A_j) 的最终收益恰为 (L)。这里 (k\ge3) 保证所需另一旧组存在，未指定有利平局。

第一回应者若选 (A_i)，收益至多 ((x+a)/2<L)，若选 (C_i)，收益至多 (x/2<L)，所以均不选。对末位，不论第一回应者选什么，该行动最多触及一个旧组；仍有一个 (\ell\ne i) 未被回应者触及，末位选 (A_\ell) 得 (L)。故其也不选收益至多 ((x+a)/2) 的 (A_i) 或至多 (x/2) 的 (C_i)。

两回应者不能都选 (B_i)：否则末位得 (x/3+b/2)，改选 (D) 得 (d+b/2\ge x+b/2)，严格更多。由于目录恰为列出的主题，偏离者的 (a_i) 块完全不被后继触及，(X_i) 至多再被一个 (B_i) 覆盖，故偏离 (A_i) 的真实收益至少 (x/2+a)。原节点最佳回复遂给

\[
 x\ge x/2+a,\qquad a\le x/2. \tag{2}
\]

这些严格比较在 (b=0) 时仍成立，因为 (d\ge x>0)；(a=0) 已单列，不把零块同覆盖标签强制认作相同有序历史。

'''
reward_new = reward_old[:start] + reward_step + reward_old[end:]
reward_new = reward_new.replace('每个互不相交的客户块 (X_i) 有 (x>0) 个单位客户，每个 (a_i) 有 (a\\ge0) 个客户；另有共享块 (B) 大小 (b\\ge0)，奖励私有块 (d) 大小 (d\\ge0)。', '客户块 (X_1,\\ldots,X_k,a_1,\\ldots,a_k,B,d) 全部两两不交；每个 (X_i) 有 (x>0) 个单位客户，每个 (a_i) 有 (a\\ge0) 个客户，共享块 (B) 大小为 (b\\ge0)，奖励私有块 (d) 大小为 (d\\ge0)。')
reward_new = reward_new.replace('而恰取 (A_1,\\dots,A_k,D,D) 的最优候选覆盖至多', '选取 (A_1,\\dots,A_k,D) 已覆盖全部客户，重复 (D) 可补齐 (k+2) 个槽。因此')
reward_new = reward_new.replace('来源与原字节见', '本页补足的真实尾菜单证明逐项依据原 `two_reward_tail_obstruction.md` 第二步（冻结原件SHA-256 `4dc5c215681e31b85e53d3c65b0d5174e07a65c53f3ea1b13f128b45d6b2dbd0`），未以1514组有限扫描代替任意k证明。\n\n来源与原字节见')
(OUT/'two-reward-body-replacement.md').write_text(reward_new)

dynamic_path = objects[DYN]['body']['path']
dynamic_old = (ROOT/dynamic_path).read_text()
dynamic_new = dynamic_old.replace('七源全部已clean show取得并全文实读，原件保存在', '原整理七源已完整保全并实读，原件保存在')
dynamic_new = dynamic_new.replace('原审计代码未重跑因其未领取witness依赖缺失，冻结exact报告与正文已完整读取。', '原审计未在本页重跑；见证已保存，审计重放不需发现或简化器；冻结exact报告与正文已完整读取。')
dynamic_new = dynamic_new.replace('README指向的 `assignment_witness.json`虽在本批原件中，生成它的发现/简化脚本不在本批；故本轮不声称重跑作者Fraction审计，避免把缺失未认领依赖当成本批已验证程序。', 'README指向的 `assignment_witness.json` 在七份原件中，作者Fraction审计只依赖这份已保存见证和标准库，重放所需输入齐全。生成/简化见证的脚本未领取，不构成该审计的缺失依赖。原整理未执行作者审计，以下复用冻结报告，不声称本页新增一次重放。')
dynamic_new = dynamic_new.replace('43 / 156（fresh action计数按源报告）', '37 / 156（不重复标签的辅助域）')
dynamic_new = dynamic_new.replace('本批虽完整读取了这些原件，但没有执行这份代码，因为生成/简化脚本不在七源且会覆盖原冻结派生文件；因此本页状态是“原报告和输入全读、作者审计未在本批重跑”，不是伪造的exit0。', '原整理完整读取了这些原件，但未执行会覆写同目录冻结派生文件的代码；这是一项未运行的事实，不能解释成见证输入缺失。若需隔离重放，可使用已保存见证和脚本，不需发现/简化生成器。因此本页仍为“原报告和输入全读、作者审计未在本批重跑”的有限来源保全对象。')
(OUT/'dynamic-certificate-body-replacement.md').write_text(dynamic_new)
static_path = objects[STATIC]['body']['path']
static_old = (ROOT/static_path).read_text()
static_new = static_old.replace('fresh历史43/258比较', 'fresh历史37/156比较、完整历史43/258比较')
static_new = static_new.replace('`assignment_witness.json`、发现MILP和简化脚本不在本批领取范围，故本轮没有声称重跑作者代码；冻结实例、策略、报告已全文读取并逐字段对照。', '冻结见证 `assignment_witness.json` 已与输入和作者审计脚本一并保存，作者审计的输入和标准库闭包完整，不需要发现MILP或见证简化器。本页整理未运行作者审计；这里复用冻结实例、策略、报告与既有完整证明，不将原内部审查改称本页新增运行。')
(OUT/'static-assignment-body-replacement.md').write_text(static_new)

changes = []
for label, path, old, new in [('two-reward', reward_path, reward_old, reward_new), ('dynamic-certificate', dynamic_path, dynamic_old, dynamic_new), ('static-assignment', static_path, static_old, static_new)]:
    assert old != new
    patch = ''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile='a/'+path, tofile='b/'+path, n=0))
    (OUT/(label+'-source-repair.patch')).write_text(patch)
    changes.append({'path': path, 'old_sha256': sha256(old.encode()).hexdigest(), 'proposed_sha256': sha256(new.encode()).hexdigest(), 'replacement_asset': REL+'/'+label+'-body-replacement.md' if label != 'static-assignment' else REL+'/static-assignment-body-replacement.md'})

reward_proof = 'archives/customer-attraction/tools/evidence/R-077c0cacfba24288be91dee1acf6d484/first/original/a1a068311b18332bba1a.md'
proposal = {
    'status': 'proposal-only; preserve current mathematics then Boss source repair, registry refresh, task handoff, fresh-worker continuation',
    'body_changes': changes,
    'record_changes': [
        {'object_id': REWARD, 'from_version': objects[REWARD]['version'], 'proposed_version': objects[REWARD]['version']+1,
         'keep_kind': 'theorem', 'keep_truth_status': 'proved',
         'statement': '任意k≥3且块X_i,a_i,B,d全部两两不交，|X_i|=x>0、|a_i|=a≥0、|B|=b≥0、|d|=d≥0，共同目录恰为C_i=X_i、A_i=X_i∪a_i、B_i=X_i∪B、D=B∪d，m=k+2。对每份完整有序历史纯SPE，若实际路径各C_i恰一次后D,D，则d≥x、a≤x/2，且W=kx+b+d、OPT=k(x+a)+b+d≤3W/2；离轨回复沿同一σ，不冻结尾部。',
         'model': '有限单位客户、共同有限标签目录；恰为所列对称块目录，k≥3且m=k+2，所有块两两不交，完整历史纯SPE与任意离轨平局。',
         'quantifiers': '任意上述整数块大小及k、每份完整σ；条件为指定实际路径，结论不推出该路径一定存在。',
         'assumptions': ['目录恰为所列C_i,A_i,B_i,D，所有块两两不交且组大小对称', '实际每个C_i一次后两个D；偏离续局始终用原同一完整σ', 'k≥3、两个回应者；零a/b块保标签身份'],
         'scope': '限定目录与实际路径的条件性3/2保证，普遍量词在该族内完整证明。',
         'add_evidence': [ref(reward_proof)], 'body_hash_from_replacement': changes[0]['proposed_sha256'],
         'reason': '删错误D影响Xi句并补原已成熟证明，不把省略的已证步骤写open；statement改为准确完整定理，保持稳定ID。'},
        {'object_id': DYN, 'from_version': objects[DYN]['version'], 'proposed_version': objects[DYN]['version']+1,
         'keep_kind': 'computation', 'keep_truth_status': 'finite',
         'statement': '保全同一1953单位客户输入、43完整历史/258比较策略及原精确报告；fresh辅助域为37历史/156比较，唯一最优支持125、OPT1740、W1735、六静态assignment成本最小1736。原整理未重跑作者脚本；witness已在七源中，缺少发现/简化器不阻碍审计重放。该对象记录固定证据及其来源合同，不作一般half推导。',
         'body_hash_from_replacement': changes[1]['proposed_sha256'], 'reason': '更正fresh字段和必要依赖误述，保finite来源保全身份。'},
        {'object_id': STATIC, 'from_version': objects[STATIC]['version'], 'proposed_version': objects[STATIC]['version']+1,
         'keep_kind': 'counterexample', 'keep_truth_status': 'proved',
         'body_hash_from_replacement': changes[2]['proposed_sha256'], 'statement_unchanged': True,
         'reason': '只改证据段fresh/full计数，现主statement与精确反例结论已正确。'},
    ],
    'dependent_reference_action': 'Boss按实际命中引用更新body SHA、对象版本/基线/registry；然后task handoff保存当前草稿、refresh实际pins并交fresh worker。冻结原代码/报告不改。',
    'affected_draft': ['dynamic-certificate-checks-static-assignment-refutation.json evidence/endpoint pins; receipt reward and dynamic core pins; reading-ledger source snapshot'],
}
put('source-repair-proposal.json', proposal)

review = '''# Boss6 round43：六组比较与原处修订交接

当前八核心与四只读端点均依实际task和registry pins实核。数学已成熟：两条accepted无条件逻辑边分别将六人完整索引必要投影应用到固定14原子，以及将旧64原子与全人数根刚性保单条ALL推出固定点非补全；一条checks/context保静态assignment有限原证据。三项新边的精确source/target/kind组合不在当前canonical清单中。

Pareto两方向是不同反例，max三例各删一次末位低过去租金平局，min例五次删点；当前向量上的支配与祖先支持非同一排序。逐规则否定安全性，互不推出另一固定实例，均非half反例。Boss9入口只停同D/B重复尾模板，不停所有多层信用或森林UTP；其原候选正文未在本任务主读，不能把入口概述当已证完整候选。

五人CA-FIVE与根不相容互补：前者精确437行必要松弛仍可行且最优>2，后者用其保数据点上的真实根必要约束排全目录补全；两个真结论没有矛盾。新527/1067/3524/3935点不在该固定排除内。

两奖励尾a≤x/2已由4668B原完整证明与本次独立重构补齐。原省略段还误说D影响Xi，D与Xi其实不交。补丁恢复sameσ两个真实回复、两个旧组菜单、a0和b0情形，不把原正确定理降成open。完整原证据应显式加入登记，statement不再复制错误证明句。两个零块别名不需策略标签相同。

动态来源fresh37/full43两个域、156/258两种比较混写；原witness确在七源，作者审计并不依赖未领取发现/简化器。新静态只读端点有同fresh误写，后续独立审查页已经指出，原处仍未修。三个replacement和最小patch均已保存。数学结论不变：静态最优存在式的所有tuple/排列都被该同输入1953客户真SPE否定；half余量1730，真实改变后缀仍可信。

所有核心coverage已逐个写，三linked五isolated-after-review。context不计linked。task仅两项in-packet overlap，已在ALL边内实际处置，closed_overlaps不得重复录入；没有follow-up对，也未制造后续队列任务。read-add确已发布STATIC，对照当前request保存。

这是source修订前完整成熟草稿，不能跳过Boss保存handoff→原处修订/registry刷新→实际task刷新→fresh worker窄核→重新绑定/收据SHA这一流程直接done。两条逻辑边本身不依本次拟改的reward/dynamic/static页，数学内容可精确保留；checks边和相关receipt需换新pins/SHA。原文错误不是身份歧义，故没有needs-decision。

实际阅读边界详reading-ledger：完整承重正文/原始4668B证明与成熟合同实读；大型raw437证书、303树、109824配置未重审或重跑，全部标明字段/区间。当前只有14项与64原子固定Fraction统计、SHA/pin/结构读取；0LP、0大树、0原入口执行。未使用Git、队列、凭据或Library，也未写规范clone。
'''
(OUT/'review-and-handoff.md').write_text(review)

assets = []
for p in sorted(OUT.iterdir()):
    if p.is_file() and p.name not in {'manifest.json'}:
        assets.append({'path': REL+'/'+p.name, 'sha256': sha256(p.read_bytes()).hexdigest()})
receipt = {'coverage': coverage, 'assets': assets, 'follow_up_tasks': [], 'closed_overlaps': [],
           'source_freshness': {'task_owner': task['owner'], 'task_request_id': task['request_id'],
                                'input_pins_match': True, 'declared_ref_bytes_match': True,
                                'status': 'current-pins-draft; known-three-source-repair-proposal-requires-handoff-refresh-and-fresh-review-before-done'},
           'draft_handoff': 'Preserve this full mathematical draft; pending Boss source repairs and fresh worker rebind, not an authorization to done current stale-after-repair receipt.'}
receipt_path = STAGE/'map/receipts'/ (TASK+'.json')
receipt_path.parent.mkdir(parents=True, exist_ok=True)
receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n')
manifest = {'task_id': TASK, 'owner': task['owner'], 'request_id': task['request_id'],
            'files': assets + [{'path': 'map/receipts/'+TASK+'.json', 'sha256': sha256(receipt_path.read_bytes()).hexdigest()}],
            'canonical_reused_assets': [], 'canonical_exact_relation_matches': canonical_matches,
            'note': 'Manifest is not a receipt asset; it hashes receipt but neither itself nor a hash cycle.'}
put('manifest.json', manifest)
print(json.dumps({'staging':str(STAGE),'receipt':str(receipt_path),'edges':3,'logical_edges':2,'context_edges':1,
                  'coverage':{'linked':3,'isolated-after-review':5},'request_id':task['request_id'],
                  'files':len(manifest['files'])+1,'separation':str(separation),'C_D_difference':str(dc)},ensure_ascii=False))
