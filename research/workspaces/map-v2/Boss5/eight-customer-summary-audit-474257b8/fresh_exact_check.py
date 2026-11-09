#!/usr/bin/env python3
"""Independent, tiny unit-customer arithmetic; never imports the old solver.

Read-only repository inspection. All products enumerate explicit compatible local
best replies in this 3-player input, rather than invoking a historical program.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import difflib
import hashlib
import json

REPO = Path('/workspace/scratch/a70fb040a4fc/co-work-anl-boss5')
OUT = Path(__file__).resolve().parent
SOURCE = 'archives/customer-attraction/state/资源/独立前沿入口与大主题精确审计的范围--资源.md'
CERT = 'archives/customer-attraction/tools/evidence/boss1-resume-independent-frontier/related/56c9f48879a8e92904e9/pruning_eight_customer.json'
SCRIPT = 'archives/customer-attraction/tools/evidence/boss1-resume-independent-frontier/related/1d09e0c20e7f8209a8e0/pruning_eight_customer.py'
IDS = ('ACTUAL-OPTIMUM-PRUNING', 'M-578fa5bf35b54839b0ed006759fe2f4e', 'M-c58776924de144e9970788260ee5558a')
TOPICS = {'A': frozenset((0, 1)), 'B': frozenset((2, 3, 4, 5)), 'C': frozenset((0, 1, 6)), 'D': frozenset((0, 1, 7))}
OLD = '原根选A，深度一全部选B；深度二除BA、BB、BC后选D以及BD后选C以外，全部选B。'
NEW = '原根选A，深度一全部选B；深度二在BA、BB、BC、CB后选D，在BD、DB后选C，其余均选B。'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def payoff(leaf, position):
    return sum((Fraction(1, sum(customer in TOPICS[t] for t in leaf))
                for customer in TOPICS[leaf[position]]), Fraction(0))

def welfare(leaf):
    return len(set().union(*(TOPICS[t] for t in leaf)))

def finish(prefix, strategy):
    while len(prefix) < 3:
        prefix += strategy[prefix]
    return prefix

def check_strategy(strategy, menu='ABCD'):
    rows = []
    for length in range(3):
        for tup in product(menu, repeat=length):
            prefix = ''.join(tup)
            leaves = {a: finish(prefix + a, strategy) for a in menu}
            values = {a: payoff(leaf, length) for a, leaf in leaves.items()}
            chosen = strategy[prefix]
            rows.append({'history': prefix, 'chosen': chosen, 'leaves': leaves,
                         'values': {a: str(v) for a, v in values.items()},
                         'best_replies': [a for a, v in values.items() if v == max(values.values())],
                         'local_IC': values[chosen] == max(values.values())})
    return rows

def all_spe_paths(menu):
    # Each terminal-history row has only |menu| exact utility calculations.
    last = {}
    for h in product(menu, repeat=2):
        prefix = ''.join(h)
        values = {c: payoff(prefix + c, 2) for c in menu}
        last[prefix] = {'values': {a: str(v) for a, v in values.items()},
                        'best_replies': [a for a, v in values.items() if v == max(values.values())]}
    # Pick one last-player BR after every possible second-player action, then
    # retain precisely the second player's best replies to that full choice.
    child_leaves = {}
    for first in menu:
        admissible = set()
        for replies in product(*(last[first + second]['best_replies'] for second in menu)):
            leaves = [first + second + third for second, third in zip(menu, replies)]
            values = [payoff(leaf, 1) for leaf in leaves]
            admissible.update(leaf for leaf, value in zip(leaves, values) if value == max(values))
        child_leaves[first] = sorted(admissible)
    # Child subtrees are disjoint, so their actual leaves may be chosen
    # independently. Choose a maximizing root action for each full combination.
    root_leaves = set()
    for leaves in product(*(child_leaves[a] for a in menu)):
        values = [payoff(leaf, 0) for leaf in leaves]
        root_leaves.update(leaf for leaf, value in zip(leaves, values) if value == max(values))
    profiles = []
    for leaf in sorted(root_leaves):
        profiles.append({'path': leaf, 'counts': [leaf.count(a) for a in menu],
                         'payoffs': [str(payoff(leaf, i)) for i in range(3)],
                         'welfare': welfare(leaf)})
    return {'menu': menu, 'last_player_rows': last, 'child_spe_leaves': child_leaves,
            'root_spe_paths': profiles, 'minimum_welfare': min(r['welfare'] for r in profiles),
            'optimum': max(welfare(''.join(x)) for x in product(menu, repeat=3))}

raw = (REPO / CERT).read_bytes()
cert = json.loads(raw)
strategy = {''.join('ABCD'[x] for x in r['history']): 'ABCD'[r['action']]
            for r in cert['full']['certificate']['actions']}
assert set(strategy) == {''.join(x) for length in range(3) for x in product('ABCD', repeat=length)}
old_strategy = dict(strategy, CB='B', DB='B')
corrected_strategy = {'': 'A', **{x: 'B' for x in 'ABCD'},
                      **{''.join(x): 'B' for x in product('ABCD', repeat=2)}}
for h in ('BA', 'BB', 'BC', 'CB'):
    corrected_strategy[h] = 'D'
for h in ('BD', 'DB'):
    corrected_strategy[h] = 'C'
assert corrected_strategy == strategy
original_rows = check_strategy(strategy)
old_rows = check_strategy(old_strategy)
assert all(row['local_IC'] for row in original_rows)
assert [r['history'] for r in old_rows if not r['local_IC']] == ['']
full = all_spe_paths('ABCD')
reduced = all_spe_paths('ABD')
assert {r['path'] for r in full['root_spe_paths']} == {
    ''.join('ABCD'[x] for x in row) for row in cert['full']['ordered_paths']}
assert {r['path'] for r in reduced['root_spe_paths']} == {
    ''.join('ABD'[x] for x in row) for row in cert['delete_C']['ordered_paths']}
assert full['minimum_welfare'] == 6 and full['optimum'] == 8
assert reduced['minimum_welfare'] == 7 and reduced['optimum'] == 7
audit = {'identity': 'Boss5 / 474257b8 / independent fresh audit',
         'method': 'Direct unit-customer Fraction arithmetic, explicit local best-reply composition; no historical module import or execution.',
         'source_sha256': sha((REPO / SOURCE).read_bytes()), 'certificate_sha256': sha(raw),
         'menu': {a: sorted(s) for a, s in TOPICS.items()},
         'payoff_formula': 'q=nA+nC+nD; uA=2/q; uB=4/nB; uC=2/q+1/nC; uD=2/q+1/nD, for labels actually selected.',
         'strategy_node_count': len(strategy), 'alternative_comparisons': 63,
         'old_summary_differences': [{'history': 'CB', 'summary': 'B', 'certificate': 'D'}, {'history': 'DB', 'summary': 'B', 'certificate': 'C'}],
         'corrected_summary_exactly_equals_certificate': corrected_strategy == strategy,
         'certificate_all_21_nodes': original_rows, 'old_summary_all_21_nodes': old_rows,
         'original_game': full, 'delete_C_game': reduced,
         'verdict': 'Only the prose summary was wrong. Frozen complete certificate and stated finite counterexample remain correct.'}
dump('audit.json', audit)

source_bytes = (REPO / SOURCE).read_bytes()
source_text = source_bytes.decode()
assert source_text.count(OLD) == 1
new_text = source_text.replace(OLD, NEW)
(OUT / 'proposed-source.patch').write_text(''.join(difflib.unified_diff(
    source_text.splitlines(keepends=True), new_text.splitlines(keepends=True),
    fromfile='a/' + SOURCE, tofile='b/' + SOURCE)))
registry = json.loads((REPO / 'research/registry.json').read_bytes())
owners = []
for obj in registry['objects']:
    refs = [obj['body']] + obj.get('evidence', [])
    hits = [ref for ref in refs if ref.get('path') == SOURCE]
    if hits:
        owners.append({'object_id': obj['object_id'], 'current_version': obj['version'],
                       'proposed_version': obj['version'] + 1,
                       'matched_refs': hits,
                       'semantic_statement_change': False})
assert {o['object_id'] for o in owners} == set(IDS)
edge_hits = []
for path in sorted((REPO / 'map/edges').rglob('*.json')):
    e = json.loads(path.read_bytes())
    endpoints = set(e.get('source_ids', []) + e.get('target_ids', [])) & set(IDS)
    evidence = [r for r in e.get('evidence', []) if r.get('path') == SOURCE]
    if endpoints or evidence:
        edge_hits.append({'path': str(path.relative_to(REPO)), 'sha256': sha(path.read_bytes()),
                          'edge_id': e.get('edge_id'), 'affected_endpoint_ids': sorted(endpoints),
                          'direct_source_evidence': evidence, 'canonical': str(path.relative_to(REPO)) in registry['edge_files']})
all_exact_sha_hits = []
old_sha = sha(source_bytes)
for top in ('research', 'map', 'archives/customer-attraction/tools/evidence'):
    for path in sorted((REPO / top).rglob('*')):
        if path.is_file() and path.suffix in ('.json', '.md', '.jsonl'):
            if old_sha.encode() in path.read_bytes():
                all_exact_sha_hits.append(str(path.relative_to(REPO)))
impact = {'source': SOURCE, 'old_sha256': old_sha, 'proposed_sha256': sha(new_text.encode()),
          'old_sentence': OLD, 'new_sentence': NEW, 'section': '八客户：完整证书、全部终局和OPT损失',
          'owners': owners, 'current_registry_baseline': registry['baseline'],
          'canonical_edges_needing_endpoint_rebind_but_no_math_change': edge_hits,
          'source_material': [m for m in registry['materials'] if m['path'] == SOURCE],
          'all_observed_exact_old_sha_hits': all_exact_sha_hits,
          'preserve_historical_input_bytes': [CERT, SCRIPT, 'research/registration/batches/register-ab98f323ad-0057.json'],
          'atomic_change_scope': [SOURCE, 'research/registration/<new targeted inputs>.json',
              'research/registration/<new targeted baseline>.json',
              'research/registration/batches/<new targeted owner update>.json',
              'research/registry.json'],
          'map_refresh_scope': [e['path'] for e in edge_hits] + [
              'map/receipts/<replacement of customer-attraction-3a-3a-203aabf39359445c>.json',
              'map/coverage.json', 'map/integration.json'],
          'important_boundary': 'Old freeze and old delivered batch/receipt are historical snapshots: do not blindly replace their SHA. New baseline+incremental owner update; refresh/supersede affected map delivery with old valid mathematics preserved.'}
dump('impact.json', impact)

lines = ['# 八客户完整策略摘要的独立算术复核', '',
         '身份：Boss5；内部词474257b8。仓库全程只读；本目录为仓库外审计材料。', '',
         '结论：冻结JSON的21节点完整策略有效。原资源摘要恰漏CB→D、DB→C；若按错误摘要把这两处设为B，根偏离C或D各得3，大于在轨A的2，故根IC失败。两个末位节点本身依然是合法平局，不能把这个摘要错误说成原证书失败。补上两动作逐条等于原JSON，原有限反例和OPT损失结论均成立。', '',
         '## 输入与收益公式', '',
         '`A={0,1}, B={2,3,4,5}, C={0,1,6}, D={0,1,7}`；三位单位玩家。记终局各主题次数为nA,nB,nC,nD、q=nA+nC+nD。已被选择的主题每人收益为`uA=2/q, uB=4/nB, uC=2/q+1/nC, uD=2/q+1/nD`。这是逐客户分母直接相加；零次主题不使用其收益公式。', '',
         '证书实际动作：根A；一层A/B/C/D后均B；二层BA/BB/BC/CB后D，BD/DB后C，其他均B。', '',
         '## 逐历史检验', '',
         '表中四值是当前行动者选A/B/C/D并沿冻结策略真实后继到终局所得收益；共21节点、63次非自身比较。所有选定动作达到本行最大值。', '',
         '|历史|所选|A|B|C|D|', '|---|---|---:|---:|---:|---:|']
for row in original_rows:
    lines.append('|' + '|'.join([row['history'] or '根', row['chosen']] + [row['values'][a] for a in 'ABCD']) + '|')
lines += ['', '## 两处遗漏怎样破坏根', '',
          '原证书根四个真实后继依次为ABB、BBD、CBD、DBC。根收益依次`2,2,2,2`。CBD中先选C者得`2/2+1=2`；DBC中先选D者同样得`2/2+1=2`，于是根A合法平局。', '',
          '错误摘要把CB与DB都改成B，根后继变成ABB、BBD、CBB、DBB。CBB的C独占客户0、1、6，得`2/1+1=3`；DBB的D独占0、1、7，同样得3。根选A仍只有2，所以根分别有严格获利偏离。', '',
          'CB处末位B得`4/2=2`，末位D得`2/2+1=2`；DB处末位B同得2，末位C同得2。遗漏之后C后次位B从4降至2，但其备选A/C/D为`1,3/2,2`，仍是合法BR；D后次位同理为`1,2,3/2`。因此仅根失败。只修CB仍留下根D偏离，只修DB仍留下根C偏离；在其余动作固定时两处都必须修。', '',
          '## 全部SPE路径、福利与OPT', '',
          '新算术脚本直接对每个两步历史列末位BR，再显式选择每个动作孩子的一份合法末位回复，最后分别取第二位和根的最佳回复，保留所有平局。未导入、执行或修改历史求解器。所得完整路径与冻结JSON逐集合相等。', '',
          '|原计数(A,B,C,D)|所有路径|W|', '|---|---|---:|',
          '|(0,1,1,1)|BCD, BDC, CBD, CDB, DBC, DCB|8|',
          '|(0,2,0,1)|BBD, BDB, DBB|7|',
          '|(0,2,1,0)|BBC, BCB, CBB|7|',
          '|(1,2,0,0)|ABB, BAB|6|', '',
          '删C后全部根SPE只有DBB，W=7。B/C/D在原菜单可覆盖八名客户，故原OPT=8；删C后客户6无任何可选主题覆盖，最多7，而B/D已覆盖剩余全部七名，故OPT=7。这一输入仅否定该次删未用C仍保某个不更高福利SPE，不能作保OPT版本；它不同于一般删B族。', '',
          '缩减菜单的逐末位BR和每个第一步的所有子SPE终局完整写入audit.json。原菜单与缩减菜单分别得到14条与1条根路径。', '',
          '## 唯一最小源补丁', '',
          '仅把资源原句替换成：', '', NEW, '',
          f'资源旧SHA256：`{old_sha}`；该唯一句子替换后的预期SHA256：`{sha(new_text.encode())}`。补丁见proposed-source.patch。', '',
          '## 原子登记及图更新边界', '',
          '当前registry恰三个对象全文引用该资源：ACTUAL-OPTIMUM-PRUNING的evidence，以及M-578fa5bf35b54839b0ed006759fe2f4e、M-c58776924de144e9970788260ee5558a的body；三者当前均version=1。按全文证据字节变更更新至version=2并换新SHA，保数学身份、真值、statement及其余正文。M-c587对应的两人结果数学上未改，只因整页字节指针刷新。', '',
          '不得全局替换旧SHA：历史baseline、旧已交登记批、原证书、原源码、原self-check/source-manifest仍保原字节。新建定向inputs/baseline及三owner增量批，并将source+新冻结+owner增量+registry同组发布。新证据若拟入库应由Boss选择实际必要内容，普通算术本身不造新对象。', '',
          '两个现行canonical边都仅因ACTUAL-OPTIMUM-PRUNING端点pin改变而需重绑定；两边均不直接引用本资源，数学解释仍成立：', '']
for e in edge_hits:
    lines.append('- `' + e['path'] + '`')
lines += ['', '已done的203a包需按定向替代交付保存其他有效覆盖、边和SHA，仅更新三owner pin、两条重绑边及对应asset SHA。随后刷新map/coverage.json与map/integration.json；队列与Git由Boss串行执行。所有发现的旧SHA命中及当前精确路径收在impact.json，命中历史文件不代表应改历史快照。', '',
          '本次复核不改变全人数保actual/唯一OPT支持删B定理，该定理有独立B/Q、F/E解析证明。错误局限于另一指定八客户删C例的完整策略摘要。', '']
(OUT / 'audit.md').write_text('\n'.join(lines))
snapshots = []
for rel in (SOURCE, CERT, SCRIPT, 'research/registry.json', registry['baseline']['path'],
            'archives/customer-attraction/tools/evidence/boss1-resume-independent-frontier-completion/source-manifest.json',
            'research/registration/batches/register-ab98f323ad-0057.json',
            'map/receipts/customer-attraction-3a-3a-203aabf39359445c.json', 'map/coverage.json', 'map/integration.json'):
    data = (REPO / rel).read_bytes()
    snapshots.append({'path': rel, 'sha256': sha(data), 'bytes': len(data)})
snapshots.extend({'path': e['path'], 'sha256': e['sha256'], 'bytes': (REPO / e['path']).stat().st_size} for e in edge_hits)
dump('source-sha-manifest.json', {'repository_read_only': True, 'snapshot_inputs': snapshots,
     'proposed_source': {'path': SOURCE, 'sha256': sha(new_text.encode()), 'bytes': len(new_text.encode())}})
files = []
for path in sorted(OUT.iterdir()):
    if path.is_file() and path.name != 'artifact-sha-manifest.json':
        data = path.read_bytes()
        files.append({'path': str(path), 'sha256': sha(data), 'bytes': len(data)})
dump('artifact-sha-manifest.json', {'files': files})
print(json.dumps({'verdict': audit['verdict'], 'source_old_sha256': old_sha,
    'source_proposed_sha256': sha(new_text.encode()), 'owners': [o['object_id'] for o in owners],
    'paths_original': len(full['root_spe_paths']), 'paths_delete_C': len(reduced['root_spe_paths']),
    'canonical_edges_to_rebind': len(edge_hits), 'output': str(OUT)}, ensure_ascii=False))
