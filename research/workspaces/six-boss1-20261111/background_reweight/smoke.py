"""Small local arithmetic audit; this is NOT the full optimization run."""
from fractions import Fraction as F
import json
import time
from cone import BRIDGE, HERE, LABELS, NAMES, SCALES, Oracle, check_inputs, exclusive, literal_vector, old_point, target


def main():
    check_inputs()
    start = time.monotonic()
    masks = [0, 1, 31, 32, 511, 512, 992, 1023]
    oracle = Oracle(masks)
    hist_index = {(b, k): {tuple(h): i for i, h in enumerate(dom.hist[k])}
                  for b, (ns, dom) in oracle.domains.items() for k in (3, 4)}

    def check_individual_rows(w, a, kcol):
        b = w['background']
        ns, dom = oracle.domains[b]
        bits = dict(zip(LABELS, map(int, w['bits'])))
        for j, name in enumerate(NAMES):
            tag = next((tag for tag, ids in oracle.family.items() if j in ids), None)
            if tag is not None:
                (k, p, terms), const, kap = dom.family_parts(tag, bits, {name: 1})
                ix = hist_index[b, k][tuple(w['histograms'][tag])]
                val = F(const+sum(v*int(dom.features[k, p][f][ix]) for f, v in terms), 120)
            elif j < 53:
                val, kap = dom.fixed_value(name, bits, w['d'], w['menus'])
            else:
                i = j-53
                actual = tuple(map(int, w['bits'][:5]))
                val = (F(actual[i], b+sum(actual)) if actual[i] else F(0)) - (F(b, b+sum(actual[:i])+5-i) if b else F(0))
                kap = 0
            assert F(val)/SCALES[j] == a[j], (name, w, val, a[j])
            assert F(kap)/SCALES[j] == kcol[j], (name, kap, kcol[j])
    x = old_point()
    old = oracle.separate(x, 0, exact=True, return_all=True)
    assert not old['complete_domain'] and old['conditional_cases'] == 96
    lookup = {}
    for b in (0, 1):
        data = json.loads((BRIDGE/f'fixed53_b{b}_profit.json').read_text())
        for r in data['all_6144_conditional_residuals']:
            lookup[b, r['bits'], r['d']] = F(r['rho'])
    direct = 0
    for r in old['rows']:
        w = r['witness']
        a, k = literal_vector(w)
        check_individual_rows(w, a, k)
        assert F(r['residual']) == lookup[w['background'], w['bits'], w['d']]
        assert F(r['residual']) == target(w)-sum(v*c for v, c in zip(x, a))
        assert sum(v*c for v, c in zip(x, k)) == -F(226487, 10**21)
        direct += len(NAMES)
    # A new common vector must get NEW hidden-family maxima, rather than
    # simply using the old witness list as a purported separation oracle.
    point = json.loads((HERE/'local_seed/iteration_000_numeric.json').read_text())
    changed = [F(v).limit_denominator(10**9) for v in point['normalized_multipliers'].values()]
    new = oracle.separate(changed, 0, exact=True, return_all=True)
    for r in new['rows']:
        w = r['witness']
        a, k = literal_vector(w)
        check_individual_rows(w, a, k)
        assert F(r['residual']) == target(w)-sum(v*c for v, c in zip(changed, a))
        direct += len(NAMES)
    report = {'status': 'LOCAL-ARITHMETIC-CHECK-PASSED', 'complete_domain': False,
              'mask_ids': masks, 'contexts_per_vector': 96, 'vectors_checked': 2,
              'literal_row_evaluations': direct, 'old_vector_matches_archived_conditional_minima': True,
              'each_individual_mutable_row_matches_literal_index_evaluation': True,
              'new_vector_minimum_on_test_contexts': new['minimum'],
              'new_vector_negative_test_contexts': new['negative_conditional_cases'],
              'new_vector_worst': new['worst'], 'seconds': time.monotonic()-start,
              'no_universal_new_bound_claim': True}
    (HERE/'local_smoke.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
