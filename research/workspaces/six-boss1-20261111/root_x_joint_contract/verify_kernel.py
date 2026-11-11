"""Independent standard-library checks of the common-X interface contract.

Imports no mapping constructor, diagnostic, optimizer or parent builder.  Frozen
inputs are read only for descriptors; old point weights are not inspected.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement, permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent


def freeze(v):
    return tuple(map(freeze, v)) if isinstance(v, list) else v


def sparse_add(*rows):
    d = defaultdict(F)
    for row in rows:
        for j, c in row:
            d[j] += F(c)
    return {j: c for j, c in d.items() if c}


def bits(v, n):
    return tuple((v >> k) & 1 for k in range(n-1, -1, -1))


def payoff(a, den):
    return F(a, den) if a else F()


def main():
    counts = Counter()
    mapping = json.loads((HERE/'own_blocks.json').read_text())
    raw = json.loads((BASE/'full624_augmented_lp/recovery/augmented_lp_exact.json').read_text())
    old = [{k: v for k, v in c.items() if k != 'weight'} for c in raw['columns'][:4849]]
    lift = json.loads((BASE/'terminal_response_cycles/max_b_symbolic_lift.json').read_text())
    x, ys, own, b4, hist = {}, {}, defaultdict(dict), defaultdict(list), {}
    for j, d in enumerate(old):
        if d['kind'] == 'hist':
            h = j
            hist[h] = d
        if d['kind'] == 'joint-reply':
            own[h, freeze(d['group'])][tuple(d['state'])] = j
        if d['kind'] == 'actual-B-family-state' and d['source'] == 4:
            b4[d['hist_column']].append((j, tuple(d['hidden'])))
    for i, c in enumerate(lift['new_columns'], 20585):
        if c['kind'] == 'common-X-mass':
            x[c['hist_column']] = i
        else:
            ys[c['hist_column'], freeze(c['query_token'])] = (i, c['query_marginal'])
    seen = set()
    for b in mapping['blocks']:
        h = b['H_column']
        assert b['X_column'] == x[h]
        if b['key'][0] == 'own-RZ':
            g = freeze(b['key'][2])
            ss = own[h, g]
            direct = {'00': {h: F(1), **{j: F(-1) for j in ss.values()}},
                      **{''.join(map(str, state)): {j: F(1)} for state, j in ss.items()}}
            tq, tr = ('R', g), ('Z', g)
        else:
            direct = {f'{a}{b0}': {j: F(1) for j, s in b4[h] if s == (a, b0)}
                      for a, b0 in product((0, 1), repeat=2)}
            tq, tr = ('H', 0), ('H', 1)
        assert b['yQ_column'] == ys[h, tq][0] and b['yR_column'] == ys[h, tr][0]
        for s in direct:
            assert sparse_add(b['mass_by_QR'][s]) == direct[s]
        assert sparse_add(b['mass_by_QR']['10'], b['mass_by_QR']['11']) == sparse_add(ys[h, tq][1])
        assert sparse_add(b['mass_by_QR']['01'], b['mass_by_QR']['11']) == sparse_add(ys[h, tr][1])
        total_mass = sparse_add(*b['mass_by_QR'].values())
        if b['key'][0] == 'own-RZ':
            assert total_mass == {h: F(1)}
        else:
            # This is the inherited B4 eight-state mass equality, not a
            # coefficient identity replacing eight original columns by H.
            assert total_mass == {j: F(1) for j, _ in b4[h]}
        seen.update((b['yQ_column'], b['yR_column']))
        counts['own_block_mapping_checks'] += 1
    assert seen == set(range(20601, 21021)) and len(mapping['blocks']) == 210
    full_descriptors = {j:c for j,c in enumerate(old)}
    full_descriptors.update({20585+i:c for i,c in enumerate(lift['new_columns'])})
    selected = [[j,full_descriptors[j]] for j in mapping['expected_column_indices']]
    encoded = json.dumps(selected,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    assert sha256(encoded).hexdigest() == mapping['expected_descriptor_sha256']

    # Small integer population checks; interval and all eight cells are exact.
    for H in range(5):
        for m00, m10, m01 in product(range(H+1), repeat=3):
            m11 = H-m00-m10-m01
            if m11 < 0:
                continue
            for X in range(H+1):
                for yq in range(min(X, m10+m11)+1):
                    for yr in range(min(X, m01+m11)+1):
                        lo = [0, yq-m10, yr-m01, yq+yr-X]
                        hi = [m11, yq, yr, m00-X+yq+yr]
                        six = [yq+yr-X+m00, m10-yq+yr, m01+yq-yr,
                               m00+m10-X+yr, m00+m01-X+yq, X+m11-yq-yr]
                        enum = []
                        for beta in range(H+1):
                            psi = [X-yq-yr+beta, yq-beta, yr-beta, beta]
                            if all(0 <= p <= m for p, m in zip(psi, (m00, m10, m01, m11))):
                                enum.append(beta)
                        assert bool(enum) == (max(lo) <= min(hi)) == (min(six) >= 0)
                        if enum:
                            assert min(enum) == max(lo) and max(enum) == min(hi)
                        counts['exact_own_interval_grid_cases'] += 1
    # The 4x4 comparison positions responsible for the six new facets.
    # All expressions are evaluated on a basis, independently of the grid.
    for i in range(7):
        a = [F(int(k == i)) for k in range(7)]
        m00, m10, m01, m11, X, yq, yr = a
        lo = [0, yq-m10, yr-m01, yq+yr-X]
        hi = [m11, yq, yr, m00-X+yq+yr]
        six = [yq+yr-X+m00, m10-yq+yr, m01+yq-yr,
               m00+m10-X+yr, m00+m01-X+yq, X+m11-yq-yr]
        assert [hi[j]-lo[k] for k, j in ((0,3),(1,2),(2,1),(1,3),(2,3),(3,0))] == six
        old_slacks = {(0,0):m11, (0,1):yq, (0,2):yr,
                      (1,0):m10+m11-yq, (1,1):m10,
                      (2,0):m01+m11-yr, (2,2):m01,
                      (3,1):X-yr, (3,2):X-yq, (3,3):m00}
        assert all(hi[j]-lo[k] == v for (k,j), v in old_slacks.items())
        counts['facet_symbolic_basis_checks'] += 16

    # Simultaneous S6 keeps X fixed, with deliberately correlated root states.
    perms = tuple(permutations(range(6)))
    for h, c in hist.items():
        words = [w for w, n in enumerate(c['hist']) for _ in range(n)]
        states = {z: [((i+1)*(7 if z else 3)+w*5) % 32 for i, w in enumerate(words)] for z in (0,1)}
        atom_weight = {0: F(2,5), 1: F(3,5)}
        one, off = defaultdict(F), defaultdict(F)
        for z in (0,1):
            for p in perms:
                w, s, v = words[p[0]], states[z][p[0]], words[p[1]]
                one[w,s,z] += atom_weight[z]/720
                off[w,s,z,v] += atom_weight[z]/720
                counts['S6_fixed_X_permutation_images'] += 1
        for w, n in enumerate(c['hist']):
            if not n:
                continue
            for z in (0,1):
                assert sum((v for (v0,s,z0), v in one.items() if v0 == w and z0 == z), F()) == F(n,6)*atom_weight[z]
                for s in range(32):
                    normalized = atom_weight[z] * F(sum(words[i] == w and states[z][i] == s for i in range(6)), n)
                    assert one[w,s,z] == F(n,6)*normalized
                    for v, nv in enumerate(c['hist']):
                        assert off[w,s,z,v] == F(n,6)*normalized*F(nv-int(v == w),5)
                    counts['root_word_state_X_marginal_checks'] += 1
    assert sum(sum(n>0 for n in c['hist']) for c in hist.values()) == 38

    # A common-X construction on all six roots; endpoint fibres never divide.
    for h,c in hist.items():
        words = [w for w,n in enumerate(c['hist']) for _ in range(n)]
        for X in (F(),F(1,2),F(1)):
            marginal = defaultdict(F)
            total_by_X = defaultdict(F)
            for z,Hz in ((0,1-X),(1,X)):
                if not Hz:
                    continue
                for choices in product((0,1),repeat=6):
                    mass = Hz
                    ss = []
                    for w,b in zip(words,choices):
                        mass *= F(1,3) if not b else F(2,3)
                        ss.append((w+5*z+11*b)%32)
                    total_by_X[z] += mass
                    for i,s in enumerate(ss):
                        marginal[i,z,s] += mass
                for i,w in enumerate(words):
                    for b in (0,1):
                        s = (w+5*z+11*b)%32
                        assert marginal[i,z,s] == Hz*(F(1,3) if not b else F(2,3))
            assert total_by_X[0] == 1-X and total_by_X[1] == X
            counts['six_root_common_X_gluing_endpoint_cases'] += 1

    # True-source SAFE lower prices, including the last-player equality.
    for t, state, z in product((0,1), range(32), (0,1)):
        e = bits(state,5)
        N = t+sum(e)
        p = t+sum(e[:3])
        W = payoff(e[3]+e[4],N)+F(e[3],(p+1)*(p+2))
        for k in range(1,6):
            bg = t+sum(e[:k-1])
            safe = F(z,bg+6-k)
            for future in product((0,1), repeat=5-k):
                actual = payoff(z,bg+z+sum(future))
                assert actual >= safe
                if k == 5:
                    assert actual == safe
                counts['root_SAFE_future_boolean_cases'] += 1
        for q in (t,)+e:
            literal = W-F(z+q,p+1)+F(z*q,(p+1)*(p+2))
            split = W-F(q,p+1)+z*(-F(1,p+1)+F(q,(p+1)*(p+2)))
            assert literal == split
            assert F(z+q,p+1)-F(z*q,(p+1)*(p+2)) == F(z,p+1)+F(q,p+1+z)
            counts['root_PAIR_X_state_split_cases'] += 1
        assert W-F(2*z,p+1)+F(z,(p+1)*(p+2)) == W-z*(F(1,p+1)+F(1,p+2))
    for p in range(5):
        def U(q,r):
            return F(q,p+1)-F(q*r,(p+1)*(p+2))
        for d,e,z,q,r in product((0,1), repeat=5):
            i1, i2, i3 = U(d,e)-U(z,r), U(r,z)-U(q,z), U(e,d)-U(r,d)
            lhs = U(d,e)+U(e,d)+F(d,(p+1)*(p+2))-F(z+q,p+1)+F(z*q,(p+1)*(p+2))
            assert lhs == i1+i2+i3+F(d*(1-r),(p+1)*(p+2))
            counts['PAIR_three_IC_boolean_identity_cases'] += 1
        for z,q in product((0,1),repeat=2):
            assert F(z,p+1)-(F(z+q,p+1)-F(z*q,(p+1)*(p+2))) == -U(q,z)
            counts['actual_RC_cap_cancellation_cases'] += 1

    # Exact small transport vertices: check both finite dual formulas.
    mu = (F(1,4),F(1,2),F(1,4))
    for epsilon in (0,1):
        for prices in permutations(tuple(F(1,p+1+epsilon) for p in (0,1,4))):
            for q in (F(),F(1,4),F(1,2),F(3,4),F(1)):
                values = []
                for free in range(3):
                    others = [j for j in range(3) if j != free]
                    for bb in product((0,1),repeat=2):
                        theta = [F(),F(),F()]
                        for j,b in zip(others,bb):
                            theta[j] = b*mu[j]
                        theta[free] = q-sum(theta,F())
                        if 0 <= theta[free] <= mu[free]:
                            values.append(sum((prices[j]*theta[j] for j in range(3)),F()))
                lower = max(l*q-sum((mu[j]*max(F(),l-prices[j]) for j in range(3)),F()) for l in prices)
                upper = min(l*q+sum((mu[j]*max(F(),prices[j]-l) for j in range(3)),F()) for l in prices)
                assert min(values) == lower and max(values) == upper
                counts['conditional_transport_dual_cases'] += 1

    # New legal-query orbits, with X and unindexed A/H fixed.
    oldq = [('A',i,()) for i in range(6)]
    oldq += [(f,0,(i,)) for f in ('T','B','C') for i in range(6)]
    oldq += [(f,z,(i,j)) for f in ('R','Z') for z,i,j in product(range(2),range(6),range(6)) if z or i != j]
    oldq += [('H',i,()) for i in range(2)]
    newq = [('Y',k,(i,)) for k,i in product(range(5),range(6))]
    X = ('X',0,())
    def canon(pair):
        names, ans = {}, []
        for f,k,ids in pair:
            ans.append((f,k,tuple(names.setdefault(i,len(names)) for i in ids)))
        return tuple(ans)
    def unordered(p,q):
        return min(canon((p,q)),canon((q,p)))
    allq = oldq+[X]+newq
    assert len(oldq) == 158 and len(allq) == 189
    assert len({canon((p,q)) for p,q in product(oldq,repeat=2)}) == 490
    root_pair = {canon((('source',0,(i,)),q)) for i in range(6) for q in allq}
    rc = {canon((p,q)) for p,q in product(allq,repeat=2) if p in newq or q in newq}
    rcu = {unordered(p,q) for p,q in combinations_with_replacement(allq,2) if p in newq or q in newq}
    assert len(root_pair) == 41 and len(rc) == 360 and len(rcu) == 185
    counts.update(root_PAIR_X_query_orbits=len(root_pair), actual_RC_ordered_new_orbits=len(rc),
                  actual_RC_unordered_new_orbits=len(rcu))

    # Two logical traps, with exact arithmetic.
    assert F(1,2)+F(1,2) > F(1,2)  # canonical minima fail for disjoint Q,R
    assert F(1,4)+F(1,4) == F(1,2)  # reselected y completes the SAME X
    assert 2*F(3,8) > F(1,2)         # independent row maxima cannot share eta
    summary = dict(status='INDEPENDENT_EXACT_COMMON_X_CONTRACT_KERNEL_PASS',
                   checks=dict(counts), all_16_histograms_retained=True,
                   root_word_groups=38, root_states_per_group=32,
                   symbolic_own_blocks=210, symbolic_facets=1260,
                   LP_calls=0, old_point_values_evaluated=0,
                   frozen_files_written_by_this_program=0, point_diagnostic_executed=False,
                   scope='Finite coefficient/frequency/kernel checks support the written proofs; no full-root law or SPE feasibility claim.',
                   mapping_sha256=sha256((HERE/'own_blocks.json').read_bytes()).hexdigest(),
                   verifier_sha256=sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))


if __name__ == '__main__':
    main()
