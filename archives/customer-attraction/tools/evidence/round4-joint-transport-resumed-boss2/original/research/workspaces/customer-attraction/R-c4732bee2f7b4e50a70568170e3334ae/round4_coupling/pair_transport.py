"""Cross-family two-query partition rows with exact shared-index transport.

This extends the within-family round3 pair rows: source branches and target
query tuples belong to different families and share only the anchor t bit.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
import hashlib
import json

from joint_transport import ACTOR, family

ORBITS = ('all_equal', 'query_equal', 'first_branch', 'second_branch', 'all_distinct')


def LM(q, b, c, B, C, K):
    return ((1, b+c, b*c),
            (q-1, B-b+C-c, K-b*c),
            (q-1, (q-1)*b+C-c, b*(C-c)),
            (q-1, B-b+(q-1)*c, (B-b)*c),
            ((q-1)*(q-2), (q-2)*(B-b+C-c), (B-b)*(C-c)-(K-b*c)))


def assignment_max(matrix):
    """Exact subset DP, with a literal permutation audit below."""
    n = len(matrix)
    @lru_cache(None)
    def solve(mask):
        row = mask.bit_count()
        if row == n:
            return F(0)
        return max(matrix[row][col] + solve(mask | (1 << col))
                   for col in range(n) if not (mask >> col) & 1)
    return solve(0)


def source_data(atom, label):
    a, b, c, d, e, *_ = map(int, atom['bits'])
    out = [[], []]
    for bits in family(atom, label):
        prefix = a + (b if label == 'AB' else e) if label != 'second' else a
        p = prefix + sum(bits[:-2])
        first, last = bits[-2:]
        H = F(first+last, p+first+last) if first+last else F(0)
        H += F(first, (p+1)*(p+2))
        out[bits[0]].append((p, H))
    return out


def row(atom, source, target, query_positions, orbit, brute=False):
    target_data = family(atom, target)
    source_groups = source_data(atom, source)
    q = len(target_data)
    u, v = query_positions
    B = sum(bits[u] for bits in target_data)
    C = sum(bits[v] for bits in target_data)
    K = sum(bits[u]*bits[v] for bits in target_data)
    result = F(0)
    for t in (0, 1):
        query_group = [bits for bits in target_data if bits[0] == t]
        matrix = []
        for p, H in source_groups[t]:
            costs = []
            for bits in query_group:
                n, L, M = LM(q, bits[u], bits[v], B, C, K)[orbit]
                costs.append(n*H - F(L, p+1) + F(M, (p+1)*(p+2)))
            matrix.append(costs)
        if brute:
            result += max((sum((matrix[i][col] for i, col in enumerate(perm)), F(0))
                           for perm in permutations(range(len(matrix)))), default=F(0))
        else:
            result += assignment_max(matrix)
    return result


def harmonic_closed_row(atom, source, target, positions, orbit):
    """Closed-form transport for same-query-index and fully diagonal rows.

    Pair membership cardinalities 0,1,2 sort against p in the same order
    for 1/(p+1) and 1/(p+2). No source/target cross coupling is assumed.
    """
    assert orbit in (0, 1)
    data = family(atom, target)
    source_groups = source_data(atom, source)
    q = len(data)
    u, v = positions
    B = sum(bits[u] for bits in data)
    C = sum(bits[v] for bits in data)
    K = sum(bits[u]*bits[v] for bits in data)
    H = sum((h for group in source_groups for p, h in group), F(0))
    if orbit == 0:
        answer = H
    else:
        answer = (q-1)*H
        answer -= (B+C)*sum((F(1, p+1) for group in source_groups for p, h in group), F(0))
        answer += K*sum((F(1, (p+1)*(p+2))
                         for group in source_groups for p, h in group), F(0))
    for t in (0, 1):
        intersection = sum(bits[u]*bits[v] for bits in data if bits[0] == t)
        union = sum(bool(bits[u]+bits[v]) for bits in data if bits[0] == t)
        # In both lists, sorting p also sorts each inverse denominator.
        ps = sorted(p for p, h in source_groups[t])
        if orbit == 0:
            ps.reverse()
        extremum = sum((F(1, p+1) for p in ps[:union]), F(0)) \
            + sum((F(1, p+2) for p in ps[:intersection]), F(0))
        answer += extremum if orbit == 1 else -extremum
    return answer


def additive_row(atom, source, target, positions, orbit):
    """All 160 source-AB/AE cross-family rows are exactly separable.

    Source p=fixed+t is constant within the preserved anchor group, so no
    unrecorded cross-family matching enters the sum. This simplification
    was independently noticed by the unrestricted-pricing teammate.
    """
    assert source in ('AB', 'AE')
    a, b, c, d, e, *_ = map(int, atom['bits'])
    prefix = a + (b if source == 'AB' else e)
    data = family(atom, target)
    u, v = positions
    q = len(data)
    B = sum(bits[u] for bits in data)
    C = sum(bits[v] for bits in data)
    K = sum(bits[u]*bits[v] for bits in data)
    H = sum((h for group in source_data(atom, source) for p, h in group), F(0))
    n = LM(q, 0, 0, B, C, K)[orbit][0]
    answer = n*H
    for bits in data:
        p = prefix + bits[0]
        _, L, M = LM(q, bits[u], bits[v], B, C, K)[orbit]
        answer += -F(L, p+1)+F(M, (p+1)*(p+2))
    return answer


def specs():
    for source, target in product(('AB', 'AE', 'second'), repeat=2):
        if source == target:
            continue
        arity = 4 if target == 'second' else 3
        for positions in combinations_with_replacement(range(arity), 2):
            for orbit, name in enumerate(ORBITS):
                yield f'{source}:{target}:pair{positions[0]}{positions[1]}:{name}', \
                    source, target, positions, orbit


def audit():
    checks = 0
    # Independent direct enumeration of triple-index sums before matching.
    for q in (1, 2, 3):
        for query in product(tuple(product((0, 1), repeat=2)), repeat=q):
            B = sum(z[0] for z in query)
            C = sum(z[1] for z in query)
            K = sum(z[0]*z[1] for z in query)
            for p in (0, 1, 5):
                for i in range(q):
                    totals = [F(0)] * 5
                    for j, k in product(range(q), repeat=2):
                        orbit = 0 if i == j == k else 1 if j == k else \
                            2 if i == j else 3 if i == k else 4
                        b, c = query[j][0], query[k][1]
                        totals[orbit] += -F(b+c, p+1)+F(b*c, (p+1)*(p+2))
                    compact = [-F(L, p+1)+F(M, (p+1)*(p+2))
                               for n, L, M in LM(q, *query[i], B, C, K)]
                    assert totals == compact
                    checks += 1
    return checks


def evaluate(path):
    document = json.loads(path.read_text())
    atoms = document['atoms']
    masses = [F(atom['exact_mass']) for atom in atoms]
    negative = {}
    literal_checks = 0
    minimum = None
    for name, source, target, positions, orbit in specs():
        value = F(0)
        for atom, mass in zip(atoms, masses):
            cut = row(atom, source, target, positions, orbit)
            assert cut == row(atom, source, target, positions, orbit, brute=True)
            if orbit in (0, 1):
                assert cut == harmonic_closed_row(atom, source, target, positions, orbit)
            if source in ('AB', 'AE'):
                assert cut == additive_row(atom, source, target, positions, orbit)
            value += mass * cut
            literal_checks += 1
        if value < 0:
            negative[name] = str(value)
        if minimum is None or value < minimum[1]:
            minimum = name, value
    return {'scope': 'Necessary cross-family pair-query transport rows; no SPE or welfare proof',
            'source_path': str(path.relative_to(ACTOR.parent.parent.parent.parent)),
            'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'compact_literal_triple_checks': audit(),
            'row_count': len(list(specs())), 'matching_DP_vs_permutation_checks': literal_checks,
            'two_harmonic_closed_forms_exact_checks': literal_checks*2//5,
            'constant_background_additive_row_exact_checks': len(atoms)*160,
            'negative_rows': negative,
            'minimum': {'name': minimum[0], 'slack': str(minimum[1])}}


if __name__ == '__main__':
    path = ACTOR / 'round4_pricing/exact_primal_overlap1.json'
    report = evaluate(path)
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
