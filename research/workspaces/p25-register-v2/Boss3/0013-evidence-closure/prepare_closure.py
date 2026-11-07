import copy
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / 'tools/registration.py').is_file())
OUT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools'))
import registration
import research_runtime as runtime


def load(path):
    return json.loads((ROOT / path).read_text())


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def pin(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def ref(path, section=None):
    result = {'path': path, 'sha256': sha(path)}
    if section is not None:
        result['section'] = section
    return result


def delta_record(base, refs, source, objection=''):
    result = copy.deepcopy(base)
    result['version'] += 1
    for item in refs:
        if item not in result['evidence']:
            result['evidence'].append(item)
    if source not in result['sources']:
        result['sources'].append(source)
    if objection:
        result['objections'] += ' ' + objection
    return result


TP = 'research/operations/p25-register-v2/tasks/register-ab98f323ad-0013.json'
BP = 'research/registration/batches/register-ab98f323ad-0013.json'
RP = 'research/registration/receipts/register-ab98f323ad-0013.json'
REG = 'research/registry.json'
BASE = ref('research/registration/baseline-5cd4b9018.json')
NOTICE = 'research/workspaces/p25-register-v2/Boss3/0027-evidence-closure/external-owner-notices.json'
SOURCE = 'archives/customer-attraction/state/审查/净券换位与调和组件的内部审查范围--审查.md'
TASK = load(TP)
ORIGINAL = load(BP)
CANON = load(REG)
CM = {o['object_id']: o for o in CANON['objects']}
MM = {m['path']: m for m in CANON['materials']}
NOTICES = [x for x in load(NOTICE)['notices'] if x['target_task'] == TP]
assert len(TASK['definition']['materials']) == 39
assert TASK['state'] == 'done' and TASK['owner'] == 'Boss3'
assert sha(TP) == '7e74b000f9b8a362776a649a4a98fd5b7bfa8059fe0b79828af214623b9b9729'
assert len(NOTICES) == 4
assert sha('research/workspaces/p25-register-v2/Boss3/0027-evidence-closure/schema2-af99-supplement-candidate.json') == '285fba960cf1200bef01a6b42013d2538993144fe9dbf95dc9f9d64c0fd2e1b9'
PROTECTED = {p: sha(p) for p in [TP, BP, RP, REG]}

# Imports and validation are permitted, but no nested Git command is permitted.
git_attempts = []
original_run = subprocess.run


def guarded_run(args, *a, **kw):
    if (isinstance(args, (list, tuple)) and args and args[0] == 'git') or (isinstance(args, str) and re.search(r'(^|\s)git\s', args)):
        git_attempts.append(str(args))
        raise RuntimeError('Git is prohibited in this worker scope')
    return original_run(args, *a, **kw)


subprocess.run = guarded_run

incoming = []
changes = []
clarification = None
for notice in NOTICES:
    oid = notice['target_object_id']
    old = CM[oid]
    new = delta_record(old, notice['source_refs'], SOURCE)
    assert pin(old) == notice['base_record_sha256']
    if oid == 'M-9803edf0cfc8420dae511fa143f8c51d':
        new['statement'] = (
            '固定任意可由完整纯SPE实现的终局主题计数q，在实现q的全部完整SPE中取实际收益向量字典序最大者。'
            '对其中每个相邻严格上升u_i<u_(i+1)，必有M_(m−i)(h_i,S_(i+1))>u_i。'
            '若该q另满足OPT_m>2W，令τ=2W/(2m−1)，LAST给u_m>τ>W/m，'
            '故存在最后一个u_i<τ的位置，其后u_(i+1)≥τ，且只保证上述门槛>u_i。'
            '另在固定实例、合法h和余人数r≥2，置t=v_(r+1)(b)；若首对利润α+β<2t的完整子SPE集合非空，'
            '在该集合取α最大者，则α<β时M_(r−1)(h,B)>α。此PB选择仅给首对barrier。')
        new['quantifiers'] = (
            '对每个有限实例及每个可实现固定终局计数q，在该q全部完整SPE实现中作lex选择，得到所有相邻位置的barrier；'
            'half最后低点另外假设该q的OPT_m>2W。PB部分另对每个固定合法背景和r≥2、'
            '非空首对和<2v_(r+1)(b)的子SPE集合取首利最大，只推出其首对barrier。')
        new['assumptions'] = [
            '固定计数部分在该q全部完整SPE实现中取字典序最大，不附加不被任意相邻换位保留的菜单/PB筛选',
            'PB部分的坏集合只以首对总和α+β<2t定义；首利最大化不授任意后续位置的barrier',
            '最后低点额外使用OPT_m>2W及原实例LAST界；不主张half坏计数或PB坏点实际存在'
        ]
        new['objections'] += (
            ' 本次将v1合写的PB首利最大选择与固定q全实现lex选择分述。PB坏性只在首对换位下按首对和保持，'
            '不能据此把PB筛选域内lex极值用于所有后续位置；固定q的half坏性由同一W/OPT保持。'
            '这是既有正文两种选择域的陈述澄清，未新证坏点存在、未将M>u_i提高为M≥τ。')
        new['scope'] = '条件极端结构：固定q全实现lex的所有相邻barrier、另列PB首对极端及half坏q的必要last-dip。'
        clarification = {
            'object_id': oid, 'old_complete_record': old, 'proposed_complete_record': new,
            'exact_field_diffs': {k: {'v1': old[k], 'v2': new[k]} for k in new if new[k] != old[k]},
            'bearing_sections': [
                ref(old['body']['path'], '固定PB坏点及固定终局计数的极端结构'),
                ref(old['body']['path'], '同规定终局负载的子树替换保留严格祖先比较'),
                ref(old['body']['path'], '真正half坏计数的最后低利润跨越'),
                ref(SOURCE, 'mixed按陈述重构的换位与固定计数扩展')],
            'why': 'v1以斜杠合写两种极值选择域。PB首对和在首对交换下保持，但后续位置交换可能改变首对和；固定q全部实现的lex选择才支持每个相邻上升。原正文证明不变。'
        }
    changes.append(new)
    incoming.append({
        'request_id': notice['request_id'], 'target_task': TP, 'target_boss': 'Boss3',
        'object_id': oid, 'current_preimage': old, 'current_preimage_sha256': pin(old),
        'proposed_unique_union_record': new, 'union_record_sha256': pin(new),
        'source_refs': notice['source_refs'],
        'decision': 'accepted-for-prepared-candidate-parent-review; no formal registration or DONE mutation',
        'difference_from_sender_union': [k for k in new if new[k] != notice['union_record'][k]],
        'all_old_evidence_and_sources_preserved': all(x in new['evidence'] for x in old['evidence']) and all(x in new['sources'] for x in old['sources'])})

save('incoming-four-exact-unions.json', {'schema': 1, 'source_notice': ref(NOTICE), 'canonical_base': ref(REG), 'decisions': incoming})
save('M9803-quantifier-clarification.json', clarification)

# The original 0014 owner has delegated only the missing static-counterexample
# evidence on these three already assigned pages to this primary author.
STATIC_ID = 'customer-attraction/frozen-suffix-optimal-topic-assignment-counterexample'
STATIC_SOURCES = [
    'archives/customer-attraction/state/审查/静态最优指派桥盲审的双求值与量词核对--审查.md',
    'archives/customer-attraction/state/计算/静态指派与因果单删的单位客户原审计--计算.md',
    'archives/customer-attraction/state/算法/全历史策略与最优静态指派的双通路精确审计--算法.md']
static_refs = [ref(STATIC_SOURCES[0]),
    ref(STATIC_SOURCES[1], '静态最优指派桥的精确方向'),
    ref(STATIC_SOURCES[1], '本轮执行和复现'),
    ref(STATIC_SOURCES[2], '本次主复跑与有限结论')]
STATIC_RAW = [
    'archives/customer-attraction/tools/evidence/r105-code/original/independent_assignment_audit.py',
    'archives/customer-attraction/tools/evidence/r105-code/replay/independent_assignment_audit.json',
    'archives/customer-attraction/tools/evidence/r105-code/replay/run-manifest.json',
    'archives/customer-attraction/tools/evidence/parent-suffix-and-static-audits/original/audit_static_assignment.py',
    'archives/customer-attraction/tools/evidence/parent-suffix-and-static-audits/runs/audit_static_assignment/source-tree/parent/static_assignment_unit_audit.json',
    'archives/customer-attraction/tools/evidence/parent-suffix-and-static-audits/run-manifest.json']
static_refs += [ref(p) for p in STATIC_RAW]
static_old = CM[STATIC_ID]
assert pin(static_old) == '628f92efaa59a9a103e9312932b909e7f11bf41d09584943afab4dc0d0cba88e'
static_new = delta_record(static_old, static_refs, STATIC_SOURCES[0],
    ' 本次同一v2接回原0014三源的独立核验：整数六分之一/Fraction两求值逐216终局一致，'
    '43有序历史258含自身IC（215真偏离）无违反；六最优有序元组乘六排列的36次检查给六种不同指派，'
    '四个成本1736、两个1737，故min1736>W1735。另一单位六分之一入口与原r105代码一次重放'
    '分别保精确报告/manifest。独立与执行均是源内历史身份，不称本轮新盲审或执行。'
    '强冻结K≤W的失败不否弱(1+1/m)W，不并B10静态新版或35/13缩小输入；'
    '通用双求值算法与ASD/VR仍由原0014保独立身份，非SPE自定义输入的half flag缺前提只属实现边界。')
static_new['sources'] += [p for p in STATIC_SOURCES[1:] if p not in static_new['sources']]
changes.append(static_new)
save('static-1953-three-source-exact-union.json', {
    'schema': 1, 'target_task': TP, 'object_id': STATIC_ID,
    'current_preimage': static_old, 'current_preimage_sha256': pin(static_old),
    'proposed_unique_union_record': static_new, 'union_record_sha256': pin(static_new),
    'source_refs': static_refs, 'sources_read_in_full': [ref(p) for p in STATIC_SOURCES],
    'primary_body_read_in_full': static_old['body'],
    'acceptance_state': 'primary-author-accepted-in-this-prepared-candidate; parent review and formal publication pending',
    'evidence_comparison': '同一input SHA2ae935及policy SHA1c59b0；原MD历史先看raw输入的独立双求值、另一父整数入口、同原码SHA的247083B复现是三条不同证据链。原body及全部旧refs保留；正文矩阵按行/列转置后与绝对价格表一致。',
    'new_execution_count': 0, 'new_object_ids': 0,
    'not_claimed_as_static_evidence': '两原审计页的ASD/VR分支与通用算法健全性，不归并为本1953反例身份；原manifest含其他执行，仅静态事件被援引。'})

# Every original material is audited. The schema candidate includes the same 39
# versions plus four genuinely added review sources, without touching task 0013.
materials = [copy.deepcopy(MM[m['path']]) for m in TASK['definition']['materials']]
for original, row in zip(TASK['definition']['materials'], materials):
    assert original['sha256'] == row['sha256'] == sha(row['path'])

materials[1]['reason'] = (
    '一般全锥对偶归CA-SECURITY-CONE-DUAL，三固定策略十三证书归CA-SELECTED-SECURITY-CONES。'
    '五游戏表全部是固定安全最优p下最小GB>0，不是失败：17/6、60/41、55088965/3710088、3/2、70429743611/10570351740。'
    '0070当前claimed Boss2且无发布record/receipt，尚须原owner给该有限正预算对象完整记录；本页live数学body保objects，不假称该路接收。')
deletion_id = 'cag-disjoint-replication-security-dilution-and-actual-deletion-support-obstruction'
threshold_id = 'cag-petal-weak-iid-explicit-threshold-and-asymptotics'
# A prepared foreign union is not an effective reverse-owner receipt. Keep the
# current owner set until its actual primary author accepts and publishes it.
materials[2]['object_ids'] = copy.deepcopy(MM[materials[2]['path']]['object_ids'])
materials[2]['reason'] = (
    '精确owner已定位Boss1/0005：三人36客户、actual034、W34、OPT36、v3=10；查询5对全部实际删位背景恒12，'
    '另均值负载max397/35超W/3恰1/105。当前完整v1尚未引用本恢复程序/独立核验页，已准备其完整preimage→v2并集请求；'
    '接收前保needs-decision仅指来源路由，非数学未判，不与31客户固定均匀核合并。')
materials[8]['object_ids'] = copy.deepcopy(MM[materials[8]['path']]['object_ids'])
materials[8]['reason'] = (
    '八客户静态cap、不同边缘独立产品及静态基准原有五owner完整保留。小树循环末回复与m=K≥53/100切口'
    '现精确归Boss3/0033对角阈值对象，非固定K100每m≥41的同一参数结论。正确100切口1969/2000；'
    '197/200是旧补充报告变量被覆写的显示错误。0033 v1尚未引用本恢复原审计页，已备完整v2并集请求；接收前保来源路由needs。')
reset_ids = ['ancestor-realized-path-promise-unrestricted-offpath-reset', 'M-36f14d3a58914546b7b36129ad249b45', 'M-8ef7265f9f1a4f099357a456882d021a']
materials[19]['object_ids'] = list(dict.fromkeys(materials[19]['object_ids'] + reset_ids))
materials[19]['disposition'] = 'attachment'
materials[19]['reason'] = (
    '原needs直接闭合：重置递推、三客户cap误算、任意m的all-L反族三个canonical v1已各以本path/同SHA全文evidence接收；'
    '与原CA-SPE-NON-PNE一同保留反向owner。真实floor从无祖先Π的孩子全集取；13节点完整树与m3…30计数回归域分开。'
    '不另增版，不等同一摘要再次接收，不运行程序。')
materials[25]['reason'] = (
    '本页三倍root-only修复、half等价R4及fresh等价的原live owner全部保留。旧成本双路经全文比较直接闭合为同源证明摘要：'
    'disjoint-petal-fixed-root-suffix-span-and-client-cost主body完整保总C≥(m+1)Δ、内部子主题动态删除与同根全部尾；'
    'disjoint-petal-fixed-root-three-dilution-sharp-bound主body完整保全部主题共同核、内部根w−a、k1/k≥2、S9和异号S10。'
    '本页比较节没有新独立证明或独有证据，原source已由两主body全承接，不为重复导航给外owner增版或制造待接收。'
    '总C、actual W和half稀释3Δ仍是三种成本。')
materials[28]['reason'] = (
    '选择性末对钱包本体归actual-terminal-pair-selective-frozen-wallet；后续HW段是同一round9/exchange原证明的准确摘要。'
    'same-actual-welfare-harmonic-terminal-wallet-payment v2主body已完整证明COPY/CLIENT/HW及更强精确REFUND，并保早期税未付。'
    '该同源摘要不增独立数学证据，旧待接收直接闭合，不要求主owner再接同一摘要；C/C′不跨query/context重复用。')
materials[35]['reason'] = (
    '32源资源的本批七owner与全部原程序/报告入口保留。十三人四对象M-c405b8dd9ee94307bc1b7d126a91577e、'
    'M-071b750f45014136aeb16dd799e7fb3a、M-a32763b94ce840fc892cb43c0a8d9971、M-0e5c7bae36da477685f01562bb31bbe4'
    '的0061主body已完整承接同一packet源码、9312B报告、gzip输入和解析/静态证书；本资源只是导航/合同摘要，不为重复导航增版。'
    '克隆链、净relay及其未付一般整行预算仍归0070 claimed Boss2，当前无完整发布记录，保精确来源/身份拆分路由needs；'
    '不能把开放付款当必须求解义务，不能以有限程序或目录为新节点。')
SOURCE_PENDING_CANDIDATE = 'research/workspaces/p25-register-v2/Boss3/0027-evidence-closure/schema2-af99-supplement-candidate.json'
source_pending_row = next(m for m in load(SOURCE_PENDING_CANDIDATE)['materials'] if m['path'] == SOURCE)
source_row = copy.deepcopy(source_pending_row)
source_row['object_ids'] = list(dict.fromkeys(source_row['object_ids'] + [x['target_object_id'] for x in NOTICES]))
source_row['reason'] = ('0027唯一pending材料母件的HF/K0原owner保留；0027-external-04至07四项独立重构已由0013主作者实际接入同一v2：'
    'mixed保AB/BA、同负载祖先比较与固定q全实现lex；global保唯一第二节点regret。三记录仅补证据，M9803澄清PB首对/固定q全位置。'
    '全页仍保needs-decision仅因0027-external-01/02的SAFE/CLIP及0027-external-08的调和review其他合同尚不在本作者接收范围；'
    '不把0013四项闭合冒称整页其他路已收。父发布时与0027同一材料行合并，不发互相覆盖的旧材料版本。')
materials.append(source_row)
for i, path in enumerate(STATIC_SOURCES):
    row = copy.deepcopy(MM[path])
    row['object_ids'] = list(dict.fromkeys(row['object_ids'] + [STATIC_ID]))
    row['disposition'] = 'objects' if MM[path]['disposition'] == 'objects' else 'attachment'
    row['reason'] = [
        '原双求值算法owner完整保留；1953客户固定反例的独立双求值全216终局、43有序历史/258真实IC及全部36有序元组×排列检查已由0013主作者在同一完整v2实际接证。旧needs缺此来源接收现闭合；不是新盲审或本轮执行。',
        '原ASD/VR两owner完整保留；本页静态最优指派桥的精确方向及本轮执行和复现两节的另一单位六分之一审计/表/manifest已由0013反例同一v2接证。ASD/VR其他数学保持独立身份；旧needs仅缺静态接收现闭合。',
        '原通用全历史双求值算法owner完整保留；本次主复跑与有限结论节的同raw input/code SHA、247083B完整报告和run-manifest由0013固定1953反例同一v2接证。通用算法不重复登记；non-SPE自定义输入half flag只属实现边界，本固定输入258IC通过。'][i]
    materials.append(row)
candidate = {'schema': 2, 'baseline': BASE, 'objects': changes, 'materials': materials, 'edge_files': []}
save('schema2-af99-supplement-candidate.json', candidate)
save('all-current-preimages-and-unique-pending-union.json', {
    'schema': 1, 'canonical_base': ref(REG), 'objects': [
        {'object_id': o['object_id'], 'current_full_preimage': CM[o['object_id']],
         'current_preimage_sha256': pin(CM[o['object_id']]), 'only_pending_full_record': o,
         'pending_record_sha256': pin(o)} for o in changes],
    'materials': [{'path': m['path'], 'current_full_preimage': MM.get(m['path']),
                   'pending_full_material_row': m} for m in materials],
    'shared_4f45_prior_pending_mother': {'candidate': ref(SOURCE_PENDING_CANDIDATE), 'material': source_pending_row},
    'rule': '仅本文件所列5个唯一v2候选；所有旧字段/证据保留。shared4f45须与0027同一行union，禁止覆盖HF/K0或误关SAFE/CLIP/harmonic未接路。'})

external_specs = [
    (deletion_id, 'Boss1', 'register-ab98f323ad-0005', materials[2]['path'],
     '同一36客户/43有序历史/258项IC、三删位6×3完整矩阵和两个不同受限背景反驳。原主body已有解析结论，恢复程序页另保原实现/输出及独立定义级重建成功证据，故需保完整入口；不改任意K不交稀释结论或31客户量词。',
     '恢复原审计及独立重建是这一固定36客户证明的新完整证据入口；未将三人静态失败提升为安全聚合或half失败。'),
    (threshold_id, 'Boss3', 'register-ab98f323ad-0033', materials[8]['path'],
     '同一两参数花瓣目录及循环不同瓣末回复规则；小树2/2、3/2、4/3与100人类型界分开，100正确切口1969/2000、53正系数解析合同与主body一致。固定K100每m≥41另有主身份，不合成同参数定理。',
     '本恢复原审计页补原Fraction实现、冻结883B/3695B报告及旧显示参数纠错；全m≥53仍由主body解析恒等式承重，有限程序不是全域扫描。')]
external = []
for index, (oid, boss, taskid, path, comparison, objection) in enumerate(external_specs, 1):
    old = CM[oid]
    new = delta_record(old, [ref(path)], path, objection)
    request = {
        'request_id': '0013-external-' + str(index).zfill(2), 'target_object_id': oid,
        'target_boss': boss, 'target_task': 'research/operations/p25-register-v2/tasks/' + taskid + '.json',
        'target_task_state_observed': load('research/operations/p25-register-v2/tasks/' + taskid + '.json')['state'],
        'canonical_base': ref(REG), 'current_preimage': old, 'current_preimage_sha256': pin(old),
        'source_refs': [ref(path)], 'mathematical_comparison': comparison,
        'full_union_record': new, 'full_union_record_sha256': pin(new),
        'acceptance_state': 'prepared-prepared-not-sent-not-claimed-received',
        'rule': '接收者以自己最高完整主record合并；本请求不授权写其正式文件。若母件变化，定向合入同一唯一pending母件，不发布旧同版本竞品。'}
    external.append(request)
save('external-owner-full-record-requests.json', {'schema': 1, 'sender': 'Boss3/register-ab98f323ad-0013', 'requests': external, 'delivered': False})

# Source-only notices are deliberately not counterfeit object preimages. 0070 has
# no published mathematical record yet and remains owned by Boss2.
task70 = 'research/operations/p25-register-v2/tasks/register-ab98f323ad-0070.json'
source_only = []
for path, source_ref, note in [
    ('archives/customer-attraction/state/障碍/固定安全预算锥的五个失败实例--障碍.md',
     ref(materials[1]['path'], '五个固定游戏的完整 SPE 预算核验'),
     '五固定p/全部可实现完整SPE的正GB极小值；负ΣC−W最大值不是GB失败。需0070原作者给实际独立对象分解及完整record，不要求解决一般GB。'),
    ('archives/customer-attraction/state/障碍/真实克隆链的零松弛漂移与双调和抵销--障碍.md', ref(materials[35]['path']),
     '31节点零本地松弛drift1/6与全部2q人双调和抵销分清；资源页只导航已有完整证明/原程序报告。需原作者给该页独立对象完整身份，未配对drift无界不反half。'),
    ('archives/customer-attraction/state/引理/净中继债务的包络余项与真实信息消元--引理.md', ref(materials[35]['path']),
     'E/F/K及δ−s投影消元与两8客户完整SPE非单射分开；一般整行付款open不是身份缺失。需原作者给该页实际记录/子对象分解。')]:
    text = (ROOT / path).read_text()
    page_id = re.search(r'^id:\s*["\']?([^"\'\n]+)', text, re.M)[1]
    source_only.append({'target_boss': 'Boss2', 'target_task': task70, 'target_task_ref': ref(task70),
                        'observed_state': load(task70)['state'], 'observed_receipt': load(task70).get('receipt'),
                        'confirmed_page_id_not_assumed_complete_object_decomposition': page_id,
                        'primary_body': ref(path), 'source_ref': source_ref, 'mathematical_routing_question': note,
                        'state': 'receiver-current-full-record-needed; no stub, no executable union, no invented version'})
save('0070-source-only-routing-breakpoints.json', {'schema': 1, 'routes': source_only, 'requires_solving_open_problem': False})

routes = [
    {'material_index': 2, 'state': 'partially-routed-live-body; receiver-full-record-needed', 'precise_result': materials[1]['reason'], 'receiving_task': task70},
    {'material_index': 3, 'state': 'exact-owner-and-full-union-prepared-awaiting-real-receipt', 'precise_result': materials[2]['reason'], 'request_id': external[0]['request_id']},
    {'material_index': 9, 'state': 'exact-owner-and-full-union-prepared-awaiting-real-receipt', 'precise_result': materials[8]['reason'], 'request_id': external[1]['request_id']},
    {'material_index': 20, 'state': 'closed-same-path-same-sha-full-evidence-already-current', 'precise_result': materials[19]['reason'], 'receiving_ids': reset_ids},
    {'material_index': 26, 'state': 'closed-duplicate-proof-summary-fully-contained-in-primary-bodies', 'precise_result': materials[25]['reason'], 'receiving_ids': ['disjoint-petal-fixed-root-suffix-span-and-client-cost', 'disjoint-petal-fixed-root-three-dilution-sharp-bound']},
    {'material_index': 29, 'state': 'closed-same-source-hw-summary-primary-complete', 'precise_result': materials[28]['reason'], 'receiving_ids': ['same-actual-welfare-harmonic-terminal-wallet-payment']},
    {'material_index': 36, 'state': 'packet-route-closed-duplicate; clone-relay-await-receiver-current-record', 'precise_result': materials[35]['reason'], 'receiving_task': task70}]
save('all-seven-old-routes-mathematical-comparison.json', {'schema': 1, 'routes': routes})

snapshot = load('research/workspaces/p25-register-v2/Boss3/0013-evidence-closure/original-and-current-full-preimages.json')
published_states = []
for short in ['0030', '0034', '0028']:
    path = 'research/operations/p25-register-v2/tasks/register-boss3-evidence-followup-' + short + '-20261107.json'
    task = load(path)
    batch_ref = task['receipt']['batch_file']
    published_states.append({'task': ref(path), 'state': task['state'], 'owner': task['owner'],
                             'receipt_batch_ref': batch_ref, 'actual_batch_sha_matches': sha(batch_ref['path']) == batch_ref['sha256'],
                             'canonical_integration_not_inferred_from_done': True})
pending_path = 'research/workspaces/p25-register-v2/Boss3/0027-evidence-closure/exact-bound-full-record-unions.json'
pending_m2a = next(x for x in load(pending_path)['unions'] if x['object_id'] == 'M-2a8a88d1fafa45b999f1506d22096df1')
save('existing-highest-published-and-pending-mothers.json', {
    'schema': 1, 'canonical_base_observed': ref(REG), 'higher_formal_done': published_states,
    'existing_pending_M2a_union': {'source_file': ref(pending_path), 'entry': pending_m2a,
                                 'rule': '原0034 v2已DONE；8dc三section只在0027这一唯一union母件待lead接。0013不另写v2或v3，不退役M036。'},
    'existing_weak_identity_reconciliation': ref('research/workspaces/p25-register-v2/Boss3/weak-frozen-budget-identity-reconciliation/identity-comparison.json')})

specific_notes = {
    1: '保Σr=1加性目标与0053 W=1目标不同，四有理恢复不是全域结论。',
    2: '三固定图全客户锥证书与五固定游戏指定p预算域分开。',
    3: '31客户固定均匀删除失败但优化actual支持成功；非36客户任意actual删除支持失败。',
    4: '同时任意相关非对称CCE逐人≥v；不向顺序SPE付款。',
    5: '三单例C3=21/10与v3=2/3、所有顺序SPE W3分开。',
    6: 'PC是m人与m+1人最低CCE平均比较，open正常登记。',
    7: 'WC同m乘1−1/(2m)，不因强CCE反例被否；open。',
    8: '占用LP涵盖全部非对称CCE，保有符号1−Σy；唯一formal v2已DONE未canonical。',
    9: '静态PNE上界2m+1，不声称最低CCE等值或一般WC。',
    10: '三状态CCE是可行上界，m≥3/K≥2。',
    11: '共同latent iid全称Jensen不排不同边缘独立产品。',
    12: '给定q代数核与所有q最优性分开；v3=44/23由不同边缘产品达到。',
    13: '静态对称Nash所有极大点同Z；没有动态付款。',
    14: '指定43节点图且均匀q为Nash两个条件，非所有图/所有q。',
    15: '固定图全非负实背景首对，非任意图首对；不冒称新增独审运行。',
    16: '全兴趣轨道对称/k≥m与条件图可信，不只主题等大。',
    17: '全q解析负flux，首次重复永久BI；root恰纯θ而非严格低θ。',
    18: '纯整数背景θ与混合安全v不同；支配只是充分条件。',
    19: '度二/相反组一一归属是前提，263客户只是菜单代数。',
    20: 'K5完整SPE/θ=u，与纯C5假菜单不同；成本>q不否安全桥。',
    21: '三客户及47客户两个独立完整SPE证书，冻结静态偏离与真实续局不混。',
    22: 'CP open量化完整SPE/每个有序h∃同一价格∀query；陈述的SPE前提控制quantifiers中的完整策略简写。',
    23: '旧namespace ID已按正式retirement转LOCAL-SWAP-ASCENT-CAP-NO-v1，保旧全证据不复活。',
    24: '十客户有限独有构造与解析无界族分列。',
    25: 'AB/BA相同终局负载只许可重标可选尾，不强制原selector匿名。',
    26: '完整子SPE且逐客户终局负载相同，才保严格祖先全部IC。',
    27: '本轮v2澄清PB首对极值与固定q全实现lex，所有附加half前提保留。',
    28: '唯一第二节点min regret，非root-only；c_T≥α才保根BR，无自动更早祖先context。',
    29: 'm≥3且每个旧根包括C自身有完整回退，精确四损非一般最优。',
    30: '正深度全SPE计划root-only三损修复；fullCartesian和整体清分母不可删。',
    31: '固定m普遍half iff 所有root-only计划G≤3Δ；没有给坏计划。',
    32: '2p完整Cartesian两保险主题修复，非只加两个总主题。',
    33: '同一保险根的两真尾/总C成本，不是half稀释。',
    34: '完整Cartesian的最优fresh费用静态相加，无需SPE。',
    35: 'fresh预算的root-only等价不是half等价。',
    36: '末两位共同固定背景/C′一行钱包，不按query/context重复领取。',
    37: '1953客户三人全部最优元组/六排列强冻结失败，弱式未否。',
    38: '八客户仅均匀排列失败，存在最优好排列。',
    39: '冻结矩阵交集运输/对偶，无需SPE；静态环条件不付真实响应。',
    40: '同一σ真实后继的signed E，非逐客户非负差。',
    41: '弱Q是∀实例σ∃最优T∃排列，原0034 v2和0027唯一pending母件保全，不处理M036退役。',
    42: 'B10最高v3已DONE，保0033独立核与0028累计全证据，不造旧同v2竞品。',
    43: '14客户唯一最优分区的冻结一次owner失败，非新增槽价格失败。',
    44: 'R与P_hat共一W，强D≤A被静态last-owner反例否；JOINT仍正确。',
    45: '48客户所有根source toll失败，但末归属强账在该点成立。',
    46: '同计数可选全集等价不许固定selector匿名；actual零clock不付另一支。',
    47: '两单客户角色身份对齐独有例，与五客户群体总损失例分开。',
    48: '任意策略纯恒等式，ρ0需正标记已有负载；无需SPE。',
    49: '先固定客户无关整行λ再标记incidence，标量流守恒不够。',
    50: '不同背景F不因有限递归伸缩；只保精确恒等式，不恢复已否WP2。'}
identity_rows = []
for i, row in enumerate(snapshot['objects'], 1):
    current = row['canonical_record']
    highest = row['published_highest'][0]
    active = CM['LOCAL-SWAP-ASCENT-CAP-NO-v1'] if i == 23 else highest['record']
    identity_rows.append({
        'original_index': i, 'original_object_id': row['object_id'], 'active_object_id': active['object_id'],
        'original_record_sha256': pin(row['original_record']),
        'canonical_version_observed': current and current['version'],
        'canonical_record_sha256_observed': current and pin(current),
        'highest_formal_version_observed': highest['record']['version'], 'highest_formal_record_sha256': highest['record_sha256'],
        'highest_formal_locations': [{k: x[k] for k in ['path', 'sha256', 'record_sha256']} for x in row['published_highest']],
        'same_highest_record_unique': row['same_highest_records'],
        'retirement_already_canonical': row['retirement'],
        'mathematical_comparison': specific_notes[i],
        'action': 'update-in-this-unique-prepared-v2' if active['object_id'] in {o['object_id'] for o in changes} else 'reuse-highest-complete-record-no-competing-update',
        'full_preimages_file': 'original-and-current-full-preimages.json'})
save('identity-audit-all-50.json', {'schema': 1, 'original_objects': 50, 'original_materials': 39,
                                    'canonical_active_redirect_record': CM['LOCAL-SWAP-ASCENT-CAP-NO-v1'], 'rows': identity_rows})

# Actual newly read ranges: mature proofs not reread below remain accurately
# reused through their complete existing bodies and evidence.
deep = {3: [(1, 67)], 9: [(1, 143)], 20: [(1, 125)], 24: [(1, 119)],
        26: [(1, 96)], 29: [(1, 121)], 36: [(75, 138)], 2: [(80, 118)]}
read_ranges = []
audit_rows = []
for i, (taskmat, proposed) in enumerate(zip(TASK['definition']['materials'], materials), 1):
    path = taskmat['path']
    text = (ROOT / path).read_text()
    lines = text.splitlines(keepends=True)
    headings = [(j+1, l.strip()) for j, l in enumerate(lines) if re.match(r'^#{1,6} ', l)]
    if i in deep:
        spans = deep[i]
        mode = 'targeted-full-mathematics-read' if spans == [(1, len(lines))] else 'specified-bearing-range-read'
    else:
        first = headings[0][0]
        start = headings[1][0] if len(headings) > 1 and headings[1][0]-first < 7 else first
        spans = [(start, min(start+9, len(lines)))]
        mode = 'mature-proof-reuse; statement-entry-read'
    positions = set()
    for start, end in spans:
        positions.update(range(start, end+1))
    positions.update(n for n, _ in headings)
    summary_lines = [(j+1, l) for j, l in enumerate(lines[:headings[0][0]-1]) if l.startswith('summary:') or l.startswith('status:')]
    positions.update(n for n, _ in summary_lines)
    actual_text = ''.join(lines[n-1] for n in sorted(positions))
    row = {'path': path, 'sha256': taskmat['sha256'], 'material_index': i, 'line_count': len(lines),
           'newly_read_inclusive_line_ranges': spans, 'atx_heading_lines_read': [n for n, _ in headings],
           'summary_status_lines_read': [n for n, _ in summary_lines], 'mode': mode,
           'cost': registration.text_cost(actual_text),
           'not_newly_reaudited': 'Linked raw code/large arrays/old finite executions; mature proof portions outside stated intervals are reused, not claimed freshly read.'}
    read_ranges.append(row)
    audit_rows.append({'material_index': i, 'assigned_ref': taskmat, 'actual_sha_matches': sha(path) == taskmat['sha256'],
                       'baseline_sha_matches': {m['path']: m['sha256'] for m in load(BASE['path'])['materials']}.get(path) == taskmat['sha256'],
                       'original_disposition': ORIGINAL['materials'][i-1], 'canonical_disposition_observed': MM[path],
                       'proposed_disposition': proposed, 'read_scope': row,
                       'mathematical_disposition': 'same mathematical identities/proof bodies retained; no nodes for numbers, PASS, programs or navigation'})
extra_read_paths = [SOURCE,
    'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
    'archives/customer-attraction/state/引理/同一实际福利对末对钱包的调和复制付款--引理.md',
    'archives/customer-attraction/state/引理/祖先路径承诺的无约束旁枝重置--引理.md',
    'archives/customer-attraction/state/定理/不交花瓣同根续局的跨度与客户成本--定理.md',
    'archives/customer-attraction/state/定理/不交花瓣同根保险的三倍损耗锐界--定理.md',
    'archives/customer-attraction/state/证明/花瓣弱iid反族的显式阈值与渐近机制--证明.md',
    'archives/customer-attraction/state/引理/不交复制的安全值稀释与实际删除支持障碍--引理.md',
    'archives/customer-attraction/state/计算/十三人两查询强桥与完整WP及两种背景值--计算.md',
    static_old['body']['path']] + STATIC_SOURCES + [STATIC_RAW[2], STATIC_RAW[5]]
for path in extra_read_paths:
    text = (ROOT / path).read_text()
    read_ranges.append({'path': path, 'sha256': sha(path), 'newly_read_inclusive_line_ranges': [[1, len(text.splitlines())]],
                        'mode': 'full-read-for-model-or-specific-route-proof-comparison', 'cost': registration.text_cost(text)})
save('material-audit-all-39.json', {'schema': 1, 'rows': audit_rows, 'supplementary_added_materials': materials[39:]})
source_totals = {k: sum(r['cost'][k] for r in read_ranges) for k in ['chars', 'utf8_bytes', 'estimated_tokens']}
metadata_text = json.dumps({'objects': snapshot['objects'], 'task': TASK, 'notices': NOTICES,
                            'static_record': static_old, 'static_materials': [MM[p] for p in STATIC_SOURCES]}, ensure_ascii=False)
metadata_cost = registration.text_cost(metadata_text)
math_records = []
for row in snapshot['objects']:
    math_records += [o for o in [row['original_record'], row['canonical_record']] +
                     [x['record'] for x in row['published_highest']] if o]
math_records += changes
route_math_ids = reset_ids + [
    'disjoint-petal-fixed-root-suffix-span-and-client-cost',
    'disjoint-petal-fixed-root-three-dilution-sharp-bound',
    'same-actual-welfare-harmonic-terminal-wallet-payment', deletion_id, threshold_id,
    'M-c405b8dd9ee94307bc1b7d126a91577e', 'M-071b750f45014136aeb16dd799e7fb3a',
    'M-a32763b94ce840fc892cb43c0a8d9971', 'M-0e5c7bae36da477685f01562bb31bbe4']
math_records += [CM[x] for x in route_math_ids]
math_fields = ['object_id', 'version', 'title', 'kind', 'truth_status', 'model',
               'statement', 'quantifiers', 'assumptions', 'scope', 'objections']
unique_math_fields = sorted(set(k + ': ' + json.dumps(o[k], ensure_ascii=False)
                                for o in math_records for k in math_fields))
math_field_cost = registration.text_cost('\n'.join(unique_math_fields))
required_instruction_paths = ['AGENTS.md', 'research/IMPLEMENTATION.md',
                              'research/PHASE3_READINESS.md', 'prompts/02.5-3-worker.md']
instruction_costs = [{'ref': ref(p), 'cost': registration.text_cost((ROOT / p).read_text()),
                      'accounting': 'conservatively charge entire instruction file, including any reused portion'}
                     for p in required_instruction_paths]
task_cost = registration.text_cost(json.dumps(TASK, ensure_ascii=False))
accounted_reading_cost = (source_totals['estimated_tokens'] + math_field_cost['estimated_tokens'] +
                         task_cost['estimated_tokens'] + sum(x['cost']['estimated_tokens'] for x in instruction_costs))
save('reading-scope-and-budget.json', {
    'schema': 1, 'declared_budget': {'model': 'gpt-6.1-sol', 'context_tokens': 500000,
        'source': 'user declaration of Sol official default; not platform telemetry', 'reading_and_metadata_tokens': 300000,
        'reserve_tokens': 200000, 'output_tokens_included_in_reserve': 100000,
        'actual_runtime_usage_tokens': None, 'fresh_system_prefix_usage': 'unknown', 'runtime_remaining_tokens': None},
    'actual_new_source_range_totals': source_totals, 'conservative_metadata_inventory_cost': metadata_cost,
    'metadata_inventory_not_claimed_fully_newly_read': 'This serializes duplicate original/canonical/highest copies and all ref strings. It is a machine comparison inventory, not 453284 newly read tokens. Do not add it to new source reading as if the duplicate records were all reread.',
    'substantive_metadata_read_cost': math_field_cost,
    'substantive_metadata_accounting': 'Each distinct reviewed mathematical field block is charged once; repeated identical model and old/current/highest fields were compared without rereading. Hash/path/ATX inventories are machine verification, not full proof reading.',
    'required_instruction_costs': instruction_costs, 'full_task_and_receipt_cost': task_cost,
    'accounted_reading_plan_estimate_tokens': accounted_reading_cost,
    'unallocated_structural_metadata_allowance_tokens': 300000-accounted_reading_cost,
    'budget_interpretation': 'Text-cost estimates for planning only; actual platform usage and fresh prefix remain unknown. The remaining small allowance covers identifiers/paths/validation summaries. No further large source reading is planned for this completed continuous 39-material scope.',
    'metadata_scope': 'Complete original/current/highest record preimages machine-compared; mathematical statement/quantifier/conditions read, repeated source/ref strings hash/ATX audited, no claim of rereading all linked raw proof bytes.',
    'planning_cost_includes_overlapping_metadata': True, 'read_ranges': read_ranges,
    'historical_original_receipt_reading_claim_is_not_repeated_as_fresh_reading': TASK['receipt']['summary']['reading'],
    'current_remaining_unread_necessary_scope': 'No unread bearing proof for five updates or seven routing decisions; 0070 receiver record publication remains an identity/source routing breakpoint, not proof or open-problem solving.'})

# True structure/SHA/unique-ATX validation. No map_tasks gate is invoked here:
# that gate reads Git and is reserved for the parent's serial window.
peer_objects = {}
for row in snapshot['objects']:
    if row['canonical_record'] and row['published_highest_version'] > row['canonical_record']['version']:
        peer_objects[row['object_id']] = row['published_highest'][0]['record']
validation = registration.validate_batch(ROOT, candidate,
    expected_materials=[{'path': m['path'], 'sha256': m['sha256']} for m in materials],
    baseline_ref=BASE, peer_objects=peer_objects)
external_checks = []
for request in external:
    obj = request['full_union_record']
    body = obj['body']
    view = {'schema': 2, 'baseline': BASE, 'objects': [obj], 'materials': [
        {'path': body['path'], 'sha256': body['sha256'], 'disposition': 'objects', 'object_ids': [obj['object_id']], 'reason': 'Exact current primary body, read-only in source request validation view'},
        {'path': request['source_refs'][0]['path'], 'sha256': request['source_refs'][0]['sha256'], 'disposition': 'attachment', 'object_ids': [obj['object_id']], 'reason': 'Proposed source union, not asserted received'}], 'edge_files': []}
    external_checks.append({'request_id': request['request_id'], 'result': registration.validate_batch(ROOT, view,
                             expected_materials=view['materials'], baseline_ref=BASE)})
all_refs = []
for row in snapshot['objects']:
    for obj in [row['original_record'], row['canonical_record'], row['published_highest'][0]['record']]:
        if obj:
            all_refs += [obj['body']] + obj['evidence']
for obj in changes + [x['full_union_record'] for x in external]:
    all_refs += [obj['body']] + obj['evidence']
unique_refs = {json.dumps(x, ensure_ascii=False, sort_keys=True): x for x in all_refs}
ref_checks = []
for item in unique_refs.values():
    raw = runtime.ref_bytes(ROOT, item)
    section = item.get('section')
    ref_checks.append({'ref': item, 'bytes': len(raw), 'sha_exact': True,
                       'unique_atx': None if section is None else sum(h[0] == section for h in runtime.heading_sections(raw.decode())) == 1})
save('reference-sha-and-unique-atx-audit.json', {'schema': 1, 'refs': ref_checks})
assert all(sha(p) == value for p, value in PROTECTED.items())
save('validation.json', {'schema': 1, 'method': 'actual tools.registration.validate_batch; direct API, no Git-dependent map_tasks validator',
    'candidate': ref(str((OUT / 'schema2-af99-supplement-candidate.json').relative_to(ROOT))),
    'candidate_result': validation, 'exact_material_scope': 'all 39 original assigned versions plus one 4f45 review source and three original0014 static audit sources; original task not redefined',
    'declared_baseline': BASE, 'higher_DONE_read_only_peers': {k: {'version': v['version'], 'record_sha256': pin(v)} for k, v in peer_objects.items()},
    'external_union_validation_views': external_checks, 'unique_refs_verified': len(ref_checks),
    'protected_preimages_unchanged': PROTECTED, 'git_attempts': git_attempts, 'math_program_runs': 0,
    'new_object_ids': 0, 'new_edges': 0, 'publication': 'prepared files only; no new claim, no DONE, no registry write, no messages sent to external owners'})
print(json.dumps({'candidate_validation': validation, 'external_validation': external_checks,
                  'refs': len(ref_checks), 'source_cost': source_totals, 'metadata_cost': metadata_cost,
                  'accounted_reading_plan_estimate_tokens': accounted_reading_cost,
                  'protected_unchanged': True, 'git_attempts': git_attempts}, ensure_ascii=False, indent=2))
