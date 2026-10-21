"""Independent exact audit of per-client anchor-preserving menu envelopes.

This checks identities and finite matching extrema, not existence of an SPE,
a globally consistent topic matching, or any general welfare bound.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def classify(pattern, anchors):
    return tuple((sum(z for (z, w), a in zip(pattern, anchors) if a == t),
                  sum(w for (z, w), a in zip(pattern, anchors) if a == t),
                  sum(z*w for (z, w), a in zip(pattern, anchors) if a == t))
                 for t in sorted(set(anchors)))


def predicted(d, anchors, counts):
    max_sum, min_sum, max_difference = F(0), F(0), F(0)
    for t, (k, ell, h) in zip(sorted(set(anchors)), counts):
        vals = sorted(v for v, a in zip(d, anchors) if a == t)
        top = lambda n: sum(vals[len(vals)-n:], F(0)) if n else F(0)
        bottom = lambda n: sum(vals[:n], F(0))
        max_sum += top(h) + top(k+ell-h)
        min_sum += bottom(h) + bottom(k+ell-h)
        max_difference += top(ell-h) - bottom(k-h)
    return max_sum, min_sum, max_difference


def harmonic_extrema(d, e, anchors, counts):
    high = low = F(0)
    for t, (k, ell, h) in zip(sorted(set(anchors)), counts):
        aa = sorted(v for v, a in zip(d, anchors) if a == t)
        ee = sorted(v for v, a in zip(e, anchors) if a == t)
        u = k+ell-h
        high += sum(aa[-u:], F(0)) if u else F(0)
        high += sum(ee[-h:], F(0)) if h else F(0)
        low += sum(aa[:u], F(0)) + sum(ee[:h], F(0))
    return high, low


def main():
    configurations = exact_assignments = extrema_classes = identities = 0
    harmonic_identities = harmonic_classes = 0
    states = tuple(product((0, 1), repeat=2))
    for q in range(1, 7):
        anchor_patterns = {tuple(0 for _ in range(q)),
                           tuple(i % 2 for i in range(q)),
                           tuple(i // 2 for i in range(q))}
        loads = {tuple(0 for _ in range(q)),
                 tuple(i for i in range(q)),
                 tuple((3*i+1) % 4 for i in range(q))}
        own = tuple((3*i+q) % 2 for i in range(q))
        for anchors, p in product(sorted(anchor_patterns), sorted(loads)):
            configurations += 1
            d = tuple(F(1, load+1) for load in p)
            e = tuple(F(1, load+2) for load in p)
            tax = tuple(a-b for a, b in zip(d, e))
            H = tuple(F(own[i]+own[(i+1) % q], p[i]+own[i]+own[(i+1) % q])
                      + F(own[i], (p[i]+1)*(p[i]+2))
                      if own[i]+own[(i+1) % q] else F(0) for i in range(q))
            A, D = sum((v*f for v, f in zip(d, own)), F(0)), sum(d, F(0))
            observed = {}
            harmonic_observed = {}
            for pattern in product(states, repeat=q):
                exact_assignments += 1
                counts = classify(pattern, anchors)
                sum_value = sum((v*(z+w) for v, (z, w) in zip(d, pattern)), F(0))
                difference = sum((v*(w-z) for v, (z, w) in zip(d, pattern)), F(0))
                harmonic_score = sum((a*(z+w)-b*z*w for a, b, (z, w)
                                      in zip(d, tax, pattern)), F(0))
                if counts not in observed:
                    observed[counts] = [sum_value, sum_value, difference]
                else:
                    observed[counts][0] = max(observed[counts][0], sum_value)
                    observed[counts][1] = min(observed[counts][1], sum_value)
                    observed[counts][2] = max(observed[counts][2], difference)
                if counts not in harmonic_observed:
                    harmonic_observed[counts] = [harmonic_score, harmonic_score]
                else:
                    harmonic_observed[counts][0] = max(harmonic_observed[counts][0], harmonic_score)
                    harmonic_observed[counts][1] = min(harmonic_observed[counts][1], harmonic_score)
                k, ell = sum(z for z, w in pattern), sum(w for z, w in pattern)
                inter = sum(z*w for z, w in pattern)
                # Literal last-node query comparisons for the three patterns.
                oo = sum((d[i]*(own[i]-pattern[j][0] + own[i]-pattern[j][1])
                          for i in range(q) for j in range(q) if i != j), F(0))
                dd = sum((d[i]*(2*own[i]-pattern[i][0]-pattern[i][1])
                          for i in range(q)), F(0))
                do = sum((d[i]*(own[i]-pattern[i][0]) for i in range(q)), F(0))
                do += sum((d[i]*(own[i]-pattern[j][1]) for i in range(q)
                           for j in range(q) if i != j), F(0))
                assert oo == 2*(q-1)*A - (k+ell)*D + sum_value
                assert dd == 2*A - sum_value
                assert do == q*A - ell*D + difference
                identities += 3
                paired_off = sum((H[i]-d[i]*(pattern[j][0]+pattern[j][1])
                                   + tax[i]*pattern[j][0]*pattern[j][1]
                                   for i in range(q) for j in range(q) if i != j), F(0))
                paired_diag = sum((H[i]-d[i]*(z+w)+tax[i]*z*w
                                    for i, (z, w) in enumerate(pattern)), F(0))
                assert paired_off == (q-1)*sum(H, F(0))-(k+ell)*D+inter*sum(tax, F(0))+harmonic_score
                assert paired_diag == sum(H, F(0))-harmonic_score
                harmonic_identities += 2
            for counts, values in observed.items():
                assert tuple(values) == predicted(d, anchors, counts)
                extrema_classes += 1
                assert tuple(harmonic_observed[counts]) == harmonic_extrema(d, e, anchors, counts)
                harmonic_classes += 1
    report = {
        'scope': 'Exact finite audit of per-client anchor-preserving matching envelopes only',
        'q_values': list(range(1, 7)),
        'configurations': configurations,
        'literal_assignments': exact_assignments,
        'identity_checks': identities,
        'extrema_classes': extrema_classes,
        'retained_overlap_identity_checks': harmonic_identities,
        'retained_overlap_extrema_classes': harmonic_classes,
        'all_checks_passed': True,
        'global_matching_caveat': 'Summing per-client extrema permits client-dependent permutations; it is an upper-envelope relaxation of one consistent topic matching.',
        'not_claimed': ['SPE existence', 'global matching realizability', 'general half coverage'],
    }
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
