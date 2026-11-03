"""B4: consume frozen records, audit new interfaces, reuse mature component audit.

Standard library only. No import or execution of legacy scripts, no LP solver.
The 47,872-component calculation is deliberately not run again.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import ast
import hashlib
import json
import math

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
PREFIX = 'research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/direct'
SRC = HERE / 'original' / PREFIX

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def consume(x, count):
    count[type(x).__name__] = count.get(type(x).__name__, 0) + 1
    if isinstance(x, dict):
        for k, v in x.items():
            consume(k, count)
            consume(v, count)
    elif isinstance(x, list):
        for v in x:
            consume(v, count)
    elif isinstance(x, float):
        assert math.isfinite(x)

def source_check():
    manifest = json.loads((HERE / 'source-manifest.json').read_text())
    results = []
    for r in manifest:
        p = HERE / 'original' / r['path']
        assert p.stat().st_size == r['size'] and sha(p) == r['sha256']
        z = dict(id=r['id'], name=p.name, bytes=r['size'], sha256=r['sha256'])
        if p.suffix == '.py':
            z['syntax'] = 'AST parsed, not executed'
            ast.parse(p.read_text())
        elif p.suffix == '.json':
            x = json.loads(p.read_text())
            counts = {}
            consume(x, counts)
            z['all_nodes_consumed'] = counts
            z['top_schema'] = list(x) if isinstance(x, dict) else [list(v) for v in x]
        results.append(z)
    assert len(results) == 20 and sum(x['bytes'] for x in results) == 66174
    return results

def share(a, d):
    return F(a, d) if a else F(0)

def paid(x, a, own, other):
    b = x[0] + x[1]
    s = b + sum(x[i] for i in own)
    u = lambda i: share(x[i], s)
    p = b + x[own[0]]
    den = b + x[own[0]] + x[own[1]] + 1
    tax = (u(own[1]) + u(own[2])
           + share(x[own[1]], (p+1)*(p+2))
           - share(x[a]+x[own[2]], p+x[a]+x[own[2]]))
    return (F(1,9)*(u(own[0])-share(x[a],b+3))
            + F(1,6)*(u(own[0])-share(x[own[2]],b+3))
            + F(23,36)*(u(own[2])-share(x[a],den))
            + F(1,3)*(u(own[2])-share(x[other],den))
            + F(5,18)*tax)

def swap():
    residuals = []
    table = {}
    for x in product((0,1), repeat=8):
        sy = x[0]+x[1]+sum(x[2:5])
        sz = x[0]+x[1]+sum(x[5:8])
        vy = sum(share(x[i],sy) for i in (2,3,4))
        vz = sum(share(x[i],sz) for i in (5,6,7))
        j = share(x[0],sy)+share(x[1],sz)-share(x[1],sy)-share(x[0],sz)
        rho = F(7,12)*(vy+vz)-j-paid(x,0,(2,3,4),7)-paid(x,1,(5,6,7),4)
        assert rho >= 0
        residuals.append(str(rho))
        key = (x[0],x[1],x[4],x[7])
        table[key] = min(table.get(key,rho),rho)
    old = json.loads((SRC/'audit_swap_payment.json').read_text())
    assert old['residuals'] == residuals and old['zeros'] == residuals.count('0') == 16
    expected = [['0','0','0','0'],['0','73/216','0','73/216'],
                ['0','0','73/216','73/216'],['59/90','659/1080','659/1080','16/27']]
    matrix = [[str(table[a,c,l,r]) for l,r in product((0,1),repeat=2)]
              for a,c in product((0,1),repeat=2)]
    assert matrix == expected
    return dict(types=256, arithmetic='Fraction', minimum='0', zeros=16,
                all_frozen_residuals_equal=True, old_ac_by_tail_lr_minimum=matrix)

def refund():
    raw = json.loads((SRC/'weighted_maximum_old_refund_obstruction.json').read_text())
    pol = {tuple(t['history']):t['action'] for t in raw['certificate']['actions']}
    histories = [h for n in range(5) for h in product((0,1),repeat=n)]
    assert set(pol) == set(histories)
    assert all(pol[h] == (0 if len(h)<=2 or h.count(0)<2 else 1) for h in histories)
    def end(h):
        while len(h)<5:
            h = h+(pol[h],)
        return h
    def u(a,z):
        return F(1,z.count(a))
    comparisons = 0
    for h in histories:
        chosen = u(pol[h],end(h))
        for a in (0,1):
            assert chosen >= u(a,end(h+(a,)))
            comparisons += 1
    y,z = end(()),end((0,0,1))
    assert y == (0,0,0,1,1) and z == (0,0,1,1,1)
    old_refund = sum(u(a,z)-u(a,y) for a in y[:2])
    tail_difference = sum(u(z[i],z)-u(y[i],y) for i in (3,4))
    assert old_refund == F(1,3) and tail_difference == -F(1,3)
    oldroot = REPO/'archives/customer-attraction/tools/evidence/maxroot-gamma-shared-menu-primary/source-root/research/workspaces/customer-attraction/R-bfbfe64dd5f94fa09d36b75198633f2b/five_only'
    differences = []
    for name in ('two_singletons_gamma_counterexample.json','audit_two_singletons_gamma.json'):
        p = oldroot/name
        obj = json.loads(p.read_text())
        actions = obj.get('certificate',obj)['actions']
        prev = {tuple(t['history']):t['action'] for t in actions}
        differences.append(dict(path=str(p.relative_to(REPO)),sha256=sha(p),
                                different_history_actions=sum(pol[h]!=prev[h] for h in histories)))
    return dict(histories=31, comparisons_including_self=comparisons,
                actual=list(y), forced_H=list(z), old_total_refund=str(old_refund),
                current_IC_slack='0', eta='0', coverage_added=0,
                future_QR_profit_difference=str(tail_difference),
                comparison_to_mature_policies=differences)

def components():
    old = json.loads((SRC/'audit_imported_half5_local_independent.json').read_text())
    base = REPO/'archives/customer-attraction/tools/half5-exact/components'
    for name,h in old['input_sha256'].items():
        assert sha(base/name) == h
    mature = REPO/'archives/customer-attraction/evidence/half5-exact/replay/local.json'
    current = json.loads(mature.read_text())
    assert current['input_sha256'] == old['input_sha256']
    records = {(r['family'],r['index']):r for r in current['checks']}
    for r in old['checks']:
        q = records[r['family'],r['index']]
        assert r['states']==q['types'] and r['zeros']==q['zero_residuals']
        assert F(r['minimum'])==0 and q['verified'] is True
    assert len(records)==len(old['checks'])==36
    assert sum(r['states'] for r in old['checks'])==47872
    return dict(input_hashes_checked=7, component_records_compared=36,
                recorded_coefficient_states=47872, newly_replayed_coefficient_states=0,
                mature_report=str(mature.relative_to(REPO)),mature_report_sha256=sha(mature),
                boundary='Recorded result and seven input hashes agree; old report does not bind its own script or row_manifest SHA.')

if __name__ == '__main__':
    result = dict(status='PASS_B4_FIXED_INTERFACES_AND_RECORD_BINDING',
                  frozen_sources=source_check(),swap=swap(),refund=refund(),components=components(),
                  not_run=['legacy LPs','legacy random search','47,872 component replay','global HALF5 replay'])
    (HERE/'fixed-interface-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='frozen_sources'},ensure_ascii=False,indent=2))
