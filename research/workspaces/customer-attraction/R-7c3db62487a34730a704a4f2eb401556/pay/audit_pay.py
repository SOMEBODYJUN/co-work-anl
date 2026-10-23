"""Fraction audit of PAY formulas; finite checks do not replace the proofs."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from customer_attraction import Instance, CustomerType, verify_certificate
from customer_attraction.certificate import StrategyCertificate

spec = importlib.util.spec_from_file_location('pay_subject', HERE/'all_path_pay.py')
subject = importlib.util.module_from_spec(spec)
spec.loader.exec_module(subject)


def brute(m, k, types):
    """Independent direct evaluation of all exact breakpoints and endpoints."""
    ts = {F(0), F(4)}
    for w, b, d in types:
        if d:
            ts.add(F(4*m*(b+1), d*(k-1)+m*(b+1)))
    def score(t):
        return sum(w*(1-F(2*(k-2)*d, m*(b+k))
                      -min(t*d/(m*(b+1)), (t*d/m+4-t)/(b+k)))
                   for w, b, d in types if d)
    return min((score(t), t) for t in ts)


def main():
    quantile_checks = 0
    for m in range(2, 10):
        for k in range(2, m+1):
            for r in range(1, 6):
                types = [(j+r, (j*j+r)%(m-k+1), (j+r*r)%m+1)
                         for j in range(1, 8)]
                assert subject.charge(m, k, types) == brute(m, k, types)
                quantile_checks += 1
    assert subject.charge(5, 2, []) == (F(0), F(0))
    assert subject.charge(5, 2, [(9, 0, 0)]) == (F(0), F(0))

    # All 128 ordered-history policies in a two-topic, three-player input.
    # This independent verifier does not use the outcome-set solver. It checks
    # that the count-DAG optimization keeps arbitrary ordered-history ties.
    tiny = Instance(('A','B'),(CustomerType(frozenset({0})),
                              CustomerType(frozenset({1}))),3)
    histories = [h for depth in range(3) for h in product(range(2),repeat=depth)]
    valid_policies = 0
    exhaustive_value = None
    for choices in product(range(2), repeat=len(histories)):
        actions = dict(zip(histories, choices))
        path = ()
        while len(path) < 3:
            path += (actions[path],)
        cert0 = StrategyCertificate(actions, tiny.counts(path))
        if not verify_certificate(tiny,cert0).valid:
            continue
        valid_policies += 1
        pay = tiny.player_payoffs(path)
        margins = []
        for depth in (0,1):
            b = tiny.counts(path[:depth])
            E = sum(pay[:depth])
            best = min(brute(3,3-depth,[(1,b[0],d0),(1,b[1],3-d0)])[0]
                       for d0 in (1,2))
            margins.append(best-2*E)
        val = min(margins)
        exhaustive_value = val if exhaustive_value is None else max(exhaustive_value,val)
    dag_value = F(subject.inspect_instance(tiny)['max_over_SPE_paths_min_over_prefix_opt_t'])
    assert dag_value == exhaustive_value

    sharp_family_checks = 0
    prefix_family_checks = 0
    for m in range(3, 41):
        types = [(m-1, 0, 1), (m, m-2, 1)]
        score, t = brute(m, 2, types)
        assert t == F(4*m, m+1)
        assert score-2*(m-2) == -F(m*m-4*m+7, m*m-1)
        sharp_family_checks += 1
    for n in range(4, 41):
        types = [(n*(n-2), 0, 1), (n-1, 1, 1),
                 (n*(n-2), n-3, 1), (n-1, n-2, 1)]
        score, t = brute(n, 2, types)
        assert t == F(4*n, n+1)
        E = n*n-2-2*(n-F(1,n)-F(1,n-1))
        exact = -2*n+8-F(4,n)-F(4,n-1)-F(8,n+1)
        assert score-2*E == exact < 0
        prefix_family_checks += 1

    monotonicity_checks = 0
    for m in range(5, 41):
        M = 3*(m-1)
        rows = []
        for p in (1, 2):
            score, t = brute(m, m-p, [(M, p, 1), (m-1, 0, 1)])
            rows.append((score-2*F(p*M,m), t))
        assert rows[0][1] == F(8*m,3*m-2)
        assert rows[1][1] == F(4*m,2*m-3) < rows[0][1]
        g1 = F(12*m**4-78*m**3+156*m*m-126*m+36, m*m*(3*m-2))
        g2 = F((m-1)*(8*m**4-76*m**3+236*m*m-300*m+144),
               m*m*(m-2)*(2*m-3))
        assert rows[0][0] == g1 > 0
        assert rows[1][0] == g2 > 0
        h = m-5
        assert g1.numerator > 0
        assert 12*m**4-78*m**3+156*m*m-126*m+36 == (
               1056+1584*h+786*h*h+162*h**3+12*h**4)
        assert 8*m**4-76*m**3+236*m*m-300*m+144 == (
               44+360*h+296*h*h+84*h**3+8*h**4)
        monotonicity_checks += 1

    m = 5
    inst = Instance(('B',)+tuple('L'+str(j) for j in range(1,m)),
                    (CustomerType(frozenset({0}),3*(m-1)),)+tuple(
                    CustomerType(frozenset({j}),1) for j in range(1,m)),m)
    actions = {h: 0 for depth in range(m) for h in product(range(m),repeat=depth)}
    cert = StrategyCertificate(actions, (m,)+(0,)*(m-1))
    checked = verify_certificate(inst, cert)
    checked.assert_valid()
    obj = {'status': 'exact complete SPE counterexample to monotone optimal PAY parameter',
           'scope': 'not a PAY or half-coverage counterexample',
           'instance': inst.to_dict(), 'certificate': cert.to_dict(),
           'checked_histories': checked.checked_histories,
           'checked_deviations': checked.checked_deviations,
           'unique_optimal_counts': [1]*m,
           'prefixes': [dict(length=p,
                         best_t=str(brute(m,m-p,[(12,p,1),(4,0,1)])[1]),
                         minimum_PAY_margin=str(brute(m,m-p,[(12,p,1),(4,0,1)])[0]
                                                -2*F(p*12,m))) for p in (1,2)]}
    (HERE/'monotone_parameter_m5.json').write_text(json.dumps(obj,indent=2)+'\n')
    report = {'status': 'exact finite implementation audit passed',
              'quantile_vs_all_breakpoints': quantile_checks,
              'ordered_history_policies_enumerated': 2**len(histories),
              'ordered_history_SPE_policies': valid_policies,
              'independent_exhaustive_policy_max_min': str(exhaustive_value),
              'count_DAG_max_min': str(dag_value),
              'sharp_big_theme_family_checks': sharp_family_checks,
              'prefix_balance_family_checks': prefix_family_checks,
              'monotone_parameter_family_checks': monotonicity_checks,
              'm5_complete_SPE_histories': checked.checked_histories,
              'm5_complete_SPE_deviations': checked.checked_deviations,
              'analytic_unbounded_quantifiers': 'proved in pay_quantile_and_path_cut.md; not inferred from finite checks'}
    (HERE/'audit_pay_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
