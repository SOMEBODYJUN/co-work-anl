"""Definition-level exact checks; no LP, no imports from discovery scripts."""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent


def all_subsets(labels):
    for k in range(len(labels)+1):
        for s in combinations(labels, k):
            yield frozenset(s)


def coverage(weights, labels):
    labels = set(labels)
    return sum((w for b, w in weights.items() if labels.intersection(b)), F(0))


def payoff(weights, q, a):
    return sum((w/F(sum(q[i] for i in b)) for b, w in weights.items() if a in b), F(0))


def restrict(weights, labels, drop_empty=True):
    out = {}
    for b, w in weights.items():
        c = frozenset(set(b).intersection(labels))
        if c or not drop_empty:
            out[c] = out.get(c, F(0))+w
    return out


def counts(n, p):
    if p == 1:
        yield (n,)
    else:
        for k in range(n+1):
            for rest in counts(n-k, p-1):
                yield (k,)+rest


def kappa(q, r, a):
    return max(F(sum(r[i] for i in b), sum(q[i] for i in b))
               for b in all_subsets(list(range(len(q)))) if a in b)


def check(m):
    p = m+1
    labels = list(range(p))
    anchor = 0
    satellites = list(range(1, p))
    signed = {frozenset({0}): F(-1)}
    signed.update({frozenset({0, i}): F(1) for i in satellites})
    source = {frozenset({0, i}): F(1) for i in satellites}
    # Add one invisible empty-interest customer. Every proper projection now
    # has a nonnegative measure of the SAME total mass m, including empty type.
    signed_projective = dict(signed)
    signed_projective[frozenset()] = F(1)
    local_checks = 0
    projective_checks = 0
    local_measures = {}
    for d in all_subsets(labels):
        if len(d) > m:
            continue
        restricted = restrict(signed, d)
        assert all(w >= 0 for w in restricted.values())
        if 0 not in d:
            explicit = {frozenset({i}): F(1) for i in d}
        else:
            explicit = {frozenset({0, i}): F(1) for i in d if i}
            explicit[frozenset({0})] = F(m-len(d))
        for s in all_subsets(sorted(d)):
            assert coverage(explicit, s) == coverage(signed, s)
            assert coverage(restricted, s) == coverage(signed, s)
            local_checks += 1
        with_empty = restrict(signed_projective, d, drop_empty=False)
        assert all(w >= 0 for w in with_empty.values())
        assert sum(with_empty.values()) == m
        local_measures[d] = with_empty
    # This is consistency of projected measures, not a customer-identity gluing.
    for d, measure in local_measures.items():
        for e in all_subsets(sorted(d)):
            assert restrict(measure, e, drop_empty=False) == local_measures[e]
            projective_checks += 1
    # Integer quadratic identity, independently checked type by type.
    b = [-1]+[1]*m
    def intersection(i, j):
        return coverage(signed, {i})+coverage(signed, {j})-coverage(signed, {i, j})
    row_value = sum(F(b[i]*(b[i]-1), 2)*coverage(signed, {i}) for i in labels)
    row_value += sum(b[i]*b[j]*intersection(i, j) for i, j in combinations(labels, 2))
    remainder = sum(w*F(sum(b[i] for i in typ)*(sum(b[i] for i in typ)-1), 2)
                    for typ, w in signed.items())
    assert row_value == remainder == -1
    boolean_checks = 0
    for typ in all_subsets(labels):
        z = sum(b[i] for i in typ)
        singleton = sum(F(b[i]*(b[i]-1), 2) for i in typ)
        pair = sum(b[i]*b[j] for i, j in combinations(sorted(typ), 2))
        assert singleton+pair == F(z*(z-1), 2) >= 0
        boolean_checks += 1
    # Every ordered-history deviation uses the original constant continuation.
    spe_signed = spe_source = 0
    for depth in range(m):
        for h in product(labels, repeat=depth):
            q = tuple(h.count(i) for i in labels)
            equilibrium = (q[0]+m-depth,)+q[1:]
            for alternative in labels:
                outcome = list(q)
                outcome[alternative] += 1
                outcome[0] += m-depth-1
                outcome = tuple(outcome)
                assert payoff(signed, equilibrium, 0) >= payoff(signed, outcome, alternative)
                assert payoff(source, equilibrium, 0) >= payoff(source, outcome, alternative)
                spe_signed += 1
                spe_source += 1
    # Equations expressing the quadratic row in terminal payoffs.
    row_representations = 0
    for i in labels:
        q = tuple(m*(j == i) for j in labels)
        assert m*payoff(signed, q, i) == coverage(signed, {i})
        row_representations += 1
    for i, j in combinations(labels, 2):
        q = tuple((m-1)*(a == i)+(a == j) for a in labels)
        assert ((m-1)*payoff(signed, q, i)+payoff(signed, q, j)
                == coverage(signed, {i, j}))
        row_representations += 1
    # Finite regression of all sharp same-topic comparisons for small m.
    dilution_checks = 0
    if m <= 4:
        terminal = list(counts(m, p))
        for a in labels:
            qs = [q for q in terminal if q[a]]
            u = {q: payoff(signed, q, a) for q in qs}
            assert all(v >= 0 for v in u.values())
            for q in qs:
                for r in qs:
                    assert u[q] <= kappa(q, r, a)*u[r]
                    dilution_checks += 1
    # The source's anchor and all singleton satellite sets are different.
    source_sets = [frozenset(typ for typ in source if a in typ) for a in labels]
    assert len(set(source_sets)) == p
    assert coverage(signed, {0}) == m-1
    assert coverage(signed, satellites) == m
    return dict(players=m, topics=p, local_coverage_checks=local_checks,
                consistent_projection_checks=projective_checks,
                boolean_type_checks=boolean_checks,
                signed_full_history_comparisons=spe_signed,
                genuine_source_full_history_comparisons=spe_source,
                terminal_row_representations=row_representations,
                sharp_dilution_checks=dilution_checks,
                global_quadratic_row_value=str(row_value),
                comparison_ratio=str(F(m, m-1)))


if __name__ == '__main__':
    report = {'status': 'exact finite checks passed; general claims use written proofs',
              'results': [check(m) for m in range(3, 6)],
              'general_half_status': 'OPEN',
              'scope': 'local customer realizability does not imply one global realization; no half obstruction'}
    (BASE/'integer_quadratic_gluing_audit.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
