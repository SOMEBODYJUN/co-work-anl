"""Exact unit-customer replay and catalog-deletion check for two finite games.

No historical model, solver, or audit functions are imported. Each customer is
expanded to a distinct unit and each ordered terminal is evaluated. Separately,
the unchanged historical independent script is executed as a subprocess; its
five-topic report is compared in full modulo the recorded local input path.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
WORK = ROOT / 'original/research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c'


def audit(data):
    n = data['players']
    m = len(data['topics'])
    assert n == 3 and data['topics'] == list(range(m))
    weights = {int(T):w for T,w in data['weights'].items()}
    assert all(type(w) is int and w > 0 and 0 < T < 2**m for T,w in weights.items())
    customers = [tuple(a for a in range(m) if T >> a & 1)
                 for T,w in weights.items() for _ in range(w)]
    assert len(customers) == 472
    policy = {tuple(h):a for h,a in data['actions']}
    histories = [h for k in range(n) for h in product(range(m),repeat=k)]
    assert len(policy) == len(data['actions']) == len(histories)
    assert set(policy) == set(histories) and set(policy.values()) <= set(range(m))
    signatures = [tuple(a in T for T in customers) for a in range(m)]
    assert all(any(T) for T in signatures) and len(set(signatures)) == m
    terminal_pay = {}
    terminal_W = {}
    for z in product(range(m),repeat=n):
        values = [F(0)] * n
        covered = 0
        for interests in customers:
            indices = [i for i,a in enumerate(z) if a in interests]
            if indices:
                covered += 1
                for i in indices:
                    values[i] += F(1,len(indices))
        assert sum(values) == covered
        terminal_pay[z] = values
        terminal_W[z] = covered

    def complete(h):
        while len(h) < n:
            h += (policy[h],)
        return h

    menus = {h:[terminal_pay[complete(h+(a,))][len(h)] for a in range(m)]
             for h in histories}
    slacks = [menus[h][policy[h]] - menus[h][a] for h in histories for a in range(m)]
    assert min(slacks) >= 0
    if 'minimum_incentive' in data:
        assert F(data['minimum_incentive']) == min(slacks)
    q = tuple(map(F,data['q']))
    assert len(q) == m and min(q) >= 0 and sum(q) == 1
    alpha = [sum((q[b]*q[c]*terminal_pay[a,b,c][0]
                  for b,c in product(range(m),repeat=2)),F(0)) for a in range(m)]
    v = sum((q[a]*alpha[a] for a in range(m)),F(0))
    assert all(value <= v for value in alpha)
    assert all(not q[a] or alpha[a] == v for a in range(m))
    # Recompute the same queries with the three-player binomial formula.
    by_type = []
    for a in range(m):
        value = F(0)
        for T,w in weights.items():
            if T >> a & 1:
                t = sum((q[b] for b in range(m) if T >> b & 1),F(0))
                value += w * (1-t+t*t/3)
        by_type.append(value)
    assert alpha == by_type == list(map(F,data['alpha']))
    Z = sum((q[a]*q[b]*q[c]*terminal_W[a,b,c]
             for a,b,c in product(range(m),repeat=3)),F(0))
    assert Z == 3*v == F(data['Z'])
    actual = complete(())
    W = terminal_W[actual]
    assert list(actual) == data['path'] and W == int(data['W']) and W < Z
    return {
        'customers':len(customers),'types':len(weights),'labels':m,
        'decision_nodes':len(histories),'comparisons':len(slacks),
        'minimum_SPE_slack':str(min(slacks)),
        'strict_comparisons':sum(x > 0 for x in slacks),
        'tie_comparisons_including_self':sum(x == 0 for x in slacks),
        'ordered_terminal_profiles':len(terminal_W),
        'actual':list(actual),'payoffs':list(map(str,terminal_pay[actual])),
        'W':W,'OPT_3':max(terminal_W.values()),'alpha':list(map(str,alpha)),
        'Z':str(Z),'strong_gap_Z_minus_W':str(Z-W),
        'weak_margin_W_minus_5Z_over_6':str(F(W)-F(5,6)*Z),
        'node_rows':[{'history':list(h),'selected':policy[h],
                      'true_continuation_payoffs':list(map(str,menus[h]))} for h in histories],
    }, policy


def main():
    manifest = json.loads((ROOT/'source-manifest.json').read_text())
    for row in manifest['sources']:
        raw = (ROOT/row['retained_at']).read_bytes()
        assert len(raw) == row['size'] and sha256(raw).hexdigest() == row['sha256']
    small_path = WORK/'dynamic_security/strong_iid_472_five_topics.json'
    large_path = WORK/'dynamic_security/strong_iid_472.json'
    small = json.loads(small_path.read_text())
    large = json.loads(large_path.read_text())
    small_report, small_policy = audit(small)
    large_report, large_policy = audit(large)

    kept = (0,1,3,4,5)
    mapping = {a:i for i,a in enumerate(kept)}
    projected = {}
    type_projection = []
    for T,w in large['weights'].items():
        mask = int(T)
        new = sum(1 << mapping[a] for a in kept if mask >> a & 1)
        assert new
        projected[new] = projected.get(new,0) + w
        type_projection.append({'old_mask':mask,'new_mask':new,'customers':w})
    assert projected == {int(T):w for T,w in small['weights'].items()}
    restricted = {}
    for h,a in large_policy.items():
        if all(b in kept for b in h):
            assert a in kept
            restricted[tuple(mapping[b] for b in h)] = mapping[a]
    assert restricted == small_policy
    assert [large['q'][a] for a in kept] == small['q']
    assert all(small_report[k] == large_report[k] for k in ('W','Z','payoffs'))
    assert small_report['OPT_3'] == 434 and large_report['OPT_3'] == 472

    original_script = WORK/'strategy_geometry/cone_abstraction/strong_iid_independent.py'
    frozen = json.loads((WORK/'strategy_geometry/cone_abstraction/strong_iid_472_independent_report.json').read_text())
    original_reports = []
    for path in (small_path,large_path):
        result = subprocess.run([sys.executable,str(original_script),str(path)],
                                check=True,capture_output=True,text=True)
        report = json.loads(result.stdout)
        original_reports.append(report)
    comparable = lambda x:{k:v for k,v in x.items() if k != 'source_witness'}
    assert comparable(original_reports[0]) == comparable(frozen)
    assert original_reports[0]['source_sha256'] == sha256(small_path.read_bytes()).hexdigest()
    assert original_reports[0]['all_history_comparisons'] == small_report['comparisons']
    assert original_reports[1]['all_history_comparisons'] == large_report['comparisons']

    # A separate, previously cleaned CCE example uses the very same 31 actions.
    related = ROOT.parent/'cce-welfare-counterexamples/source/evidence/certificates/customer_attraction/worst_cce_welfare_failure.json'
    related_data = json.loads(related.read_text())
    related_policy = {tuple(row['history']):row['action'] for row in related_data['actions']}
    assert related_policy == small_policy
    print(json.dumps({
        'status':'PASS','source_files_hash_checked':len(manifest['sources']),
        'five_topic_expanded_unit_audit':small_report,
        'six_topic_expanded_unit_audit':large_report,
        'deletion':{'removed_old_label':2,'old_to_new':mapping,
                    'type_projection':type_projection,'closed_policy_restriction_nodes':len(restricted),
                    'actual_and_iid_values_preserved':True,'OPT_3_preserved':False},
        'historical_independent_reports':original_reports,
        'frozen_five_topic_report_equal_modulo_local_source_path':True,
        'same_31_actions_as_thirteen_customer_CCE_certificate':True,
        'related_CCE_certificate_sha256':sha256(related.read_bytes()).hexdigest(),
        'root_saturation_proof_not_certified_by_finite_audit':True,
        'scope':'These two finite strong-iid counterexamples only. No static safety value, aggregate-safety bridge, weak-iid counterexample, or six-provider half result.',
    },ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
