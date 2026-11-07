"""Boss1: precise threshold objects and accepted existing-owner evidence.

Seven mature pages and the common model were read, including recovering all
truncated source ranges. No original mathematical program was run here.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
import registration

NAME = 'register-lead-threshold-and-owner-evidence-03'
MC = 'M-94bfb2bc835a4b29ba5ed87ef2e48585'
POP = 'M-807f05190d1f4272b17deb8d040f979a'
BASE = 'archives/customer-attraction/state/'
THRESHOLD = BASE + '资料/动态局部门槛的独立见证锥与人口预算--资料.md'
CCE = BASE + '引理/静态粗相关均衡的安全下界与三单例严格间隙--引理.md'
INSURER = BASE + '定理/多主题独立保险的三倍根修复与半覆盖等价--定理.md'
HISTORY = BASE + '资源/静态福利比较与末回复配对锥的原稿接续--资源.md'
SEEDS = [BASE + '资源/' + name + '--资源.md' for name in (
    '五人根缺陷种子对的平局分叉与共享遗漏',
    '五客户空根计划的正深度可信性与根遗憾',
    '四人根缺陷四种子的完整计划与版本差异')]
MODEL = BASE + '定义/共同目录完整历史模型--定义.md'


def ref(path, section=None):
    result = {'path': path, 'sha256': hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}
    if section:
        result['section'] = section
    return result


def write(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


task = json.loads((ROOT / ('research/operations/p25-register-v2/tasks/' + NAME + '.json')).read_text())
if task['state'] != 'claimed' or task['owner'] != 'Boss1':
    raise ValueError('Only the currently claimed Boss1 task may be written')
definition = task['definition']
canonical = json.loads((ROOT / 'research/registry.json').read_text())
known = {o['object_id']: o for o in canonical['objects']}
model = ('有限单位客户、有限非空共同标签目录及覆盖映射、单位顺序提供者；'
         '允许空覆盖、重复行动、同覆盖异标签和全部有序离轨弱平局；'
         '每个真实偏离后沿所指定完整策略续走，客户在终局覆盖者间均分。')
objects = [
    {
        'object_id': MC, 'version': 1,
        'title': '动态局部门槛独立见证多锥的精确反例完备性与单位整数化',
        'kind': 'method', 'truth_status': 'proved', 'model': model,
        'statement': ('固定有限标签、人数m、actual完整策略σ、actual各前缀h_i的独立局部完整SPE见证τ_i及至多m槽比较T。'
                      '非负客户type质量r、σ全部有序IC和各τ_i全部局部IC构成有理齐次弱线性锥。'
                      '若该锥有W(actual)+Σ_i leader(τ_i)−coverage(T)<0的实点，则可保弱IC、平局等式及正支持取有理点，'
                      '整体清分母成不同单位客户，给actual-TB的真反例；因为Θ(h_i)≤leader(τ_i)、coverage(T)≤OPT_m。'
                      '反之每个真actual-TB反例可取各Θ的独立达到见证和最优T，落入这样的有限多锥架构。'
                      '去掉actual IC并取任意合法路径时只认证TB-ANY模式。'),
        'quantifiers': ('每个固定有限架构及全部非负实type质量；完备性跨所有有限m、标签、actual策略、独立局部见证和比较组，'
                        '不要求嵌套见证彼此一致或延伸actualσ。'),
        'assumptions': [
            '局部Θ是完整局部SPE最低首利，不是强制孩子的L_h(A)或静态安全值',
            'actual模式必须保σ的全部完整有序历史IC',
            '见证在新质量下只须仍为局部SPE，不要求继续达到最小Θ',
            '严格负目标及有理弱线性约束；所有客户质量一起清分母'],
        'scope': 'TB/独立见证的精确有限锥认证方法；无一般人数或标签数的有限上界、高效性或普遍TB保证。',
        'objections': ('主页全文及REP/MC/有理归约承重推导已读；0004保REP与任意路径终端W动态规划的不同主身份。'
                       '原guard初失效后修复只属原MD的两个历史时点，本次没有读取或运行相关原代码/JSON。'
                       '浮点负数或固定单锥阴性不能替代全部精确IC/严格目标或全族结论。'),
        'body': ref(THRESHOLD, '固定多策略锥的必要性、充分性和有理归约'),
        'evidence': [ref(MODEL), ref(THRESHOLD, '局部完整均衡与强制孩子必须区分'),
                     ref(THRESHOLD, 'TB和独立见证的精确等价')],
        'sources': [THRESHOLD, 'source:1d7a3ead39c6c2dd0ab5', 'source:49a89089d75c6892e592']
    },
    {
        'object_id': POP, 'version': 1,
        'title': '动态局部完整SPE最低首值的全人口累计预算',
        'kind': 'open-problem', 'truth_status': 'open', 'model': model,
        'statement': ('开放命题POP：对每个有限共同目录和m≥1，Σ_{r=1}^m Θ_r(空历史)≥OPT_m，'
                      'Θ_r为该同一目录r人完整局部纯SPE中首人收益的最小值。'
                      '普遍TB-ANY若成立，添加合法空主题并取全empty路径即推出POP；此条件箭头已有证明，不是POP证明。'),
        'quantifiers': '所有有限单位客户目录与每个m≥1；每个r各自对全部完整有序历史r人SPE取最小首利。',
        'assumptions': [
            '同一目录的不同人数动态门槛，不改用静态不观察查询的v_r',
            '全空路径只是合法形式路径，不要求它是完整SPE路径',
            '存在可覆盖客户时空主题收益0，永不在局部SPE中选；全零客户全部量为0'],
        'scope': '更强任意路径TB-ANY的必要后果；不等同actual-TB、逐次最优边际界或原六人half。',
        'objections': ('完整读POP推导与四客户动态/静态分离：A={1,2},C={3,4},B={1,3}时Θ1=Θ2=2，'
                       '但v1=2,v2=3/2，故不能以静态和替代。原(30,15,13,9)仅MD历史报告，'
                       '未重新认证原数值/输入；逐次边际失败不反累计POP。本次无新数学运行。'),
        'body': ref(THRESHOLD, 'POP是更强未证桥的必要后果'),
        'evidence': [ref(MODEL), ref(THRESHOLD, '局部完整均衡与强制孩子必须区分'),
                     ref(THRESHOLD, 'TB和独立见证的精确等价')],
        'sources': [THRESHOLD, 'source:1d7a3ead39c6c2dd0ab5', 'source:49a89089d75c6892e592']
    }
]
cce_ids = ['customer-attraction/static-cce-uniform-deletion-security-lower-bound-and-strict-gap',
           'M-8093886eed9c4824be53388b7d10d78b']
insurer_id = 'customer-attraction/multi-theme-independent-insurer-three-regret-repair-and-half-equivalence'
for oid in cce_ids:
    obj = copy.deepcopy(known[oid])
    obj['version'] += 1
    obj['evidence'].append(ref(HISTORY, 'CCE与真正安全值：真静态关系，假全人数替代桥'))
    obj['sources'].append(HISTORY)
    obj['objections'] += (' 本次定向全文读主引理和原稿接续页，实际接3711B原稿的来源及正确静态关系/严格间隙边界；'
                          '不把后来同人数CCE桥反例连带用于否定n v_n安全下界，无新增程序或重证。')
    objects.append(obj)
obj = copy.deepcopy(known[insurer_id])
obj['version'] += 1
obj['evidence'].extend(ref(path) for path in SEEDS)
obj['sources'].extend(SEEDS)
obj['objections'] += (' 本次全文读主定理和三份根种子资源，接入3/4/5人数的原完整source-plan与有序平局/根菜单校准。'
                      '这些计划只保正深度SPE且Δ>0，不追认为完整SPE；四五人同suffix改根与单末位平局分叉分别保留。'
                      '种子负G−3Δ只描述固定输入，不认证重优化客户锥上界；不另造单次输入/PASS节点，未重跑旧IC或OPT。')
objects.append(obj)

owner_map = {THRESHOLD: [MC, POP], CCE: cce_ids, INSURER: [insurer_id],
             HISTORY: cce_ids, **{path: [insurer_id] for path in SEEDS}}
reasons = {
    THRESHOLD: '主页全文实读；独立多锥有理完备性与POP开放预算分别认身份；REP/TB/TA由0004主owner承载，不重复登记。',
    CCE: '同一静态普遍下界与三单例严格间隙的原两个身份，仅递增证据版本。',
    INSURER: '同一完整Cartesian三倍根修复，主证明及三种成本完整保留，只增有限source-plan证据。',
    HISTORY: '精确CCE原稿来源只归静态两owner；PNE反例和删槽方法的其他部分由0003/0070另行承接。',
    **{path: '完整实读客户、动作域、根菜单、正深度IC及原审计边界，作根修复的有限输入来源；非完整SPE/新普遍定理。' for path in SEEDS}}
materials = [dict(ref(path), disposition='objects' if path in {THRESHOLD, CCE, INSURER} else 'attachment',
                  object_ids=owner_map[path], reason=reasons[path]) for path in owner_map]
batch = {'schema': 2, 'baseline': definition['baseline'], 'objects': objects, 'materials': materials, 'edge_files': []}
checked = registration.validate_batch(ROOT, batch, definition['materials'], definition['baseline'])
batch_path = 'research/registration/batches/' + NAME + '.json'
write(batch_path, batch)
receipt = {'batch_file': ref(batch_path), 'assets': [ref(batch_path)],
           'allocated_object_ids_once': [MC, POP],
           'summary': {'objects': len(objects), 'materials': len(materials),
                       'new_objects': 2, 'existing_objects_updated': 3,
                       'reading': 'Seven mature pages and common full-history model fully read; truncated multi-page tool output recovered by exact ranges.',
                       'mathematical_program_runs': 0,
                       'identity_boundary': 'REP/TB/TA stay with0004; no new seed-input, audit or PASS nodes; original done assets unchanged.'},
           'validation': checked}
write('research/registration/receipts/' + NAME + '.json', receipt)
print(json.dumps(receipt['summary'], ensure_ascii=False))
