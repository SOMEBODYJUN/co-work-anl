"""New definition-level finite check; never an original-source replay.

Only stdlib. Inputs are literal below. Run once in a fresh output directory.
The count-state outcome recursion retains every history-dependent SPE outcome;
it never requires identical choices at distinct histories having equal counts.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, product
import json
import pathlib
import sys


def out(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): out(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [out(v) for v in x]
    return x


def value(types, q, a):
    return sum((F(w, sum(q[j] for j in B)) for B, w in types
                if a in B), F())


def cover(types, q):
    return sum(w for B, w in types if any(q[j] for j in B))


def add(q, a):
    return q[:a] + (q[a] + 1,) + q[a + 1:]


def outcome_solver(types, labels, total):
    @lru_cache(None)
    def solve(q):
        if sum(q) == total:
            return frozenset([q]), None
        children = [solve(add(q, a))[0] for a in range(labels)]
        threshold = max(min(value(types, z, a) for z in children[a])
                        for a in range(labels))
        result = frozenset(z for a in range(labels) for z in children[a]
                           if value(types, z, a) >= threshold)
        assert result
        return result, threshold
    return solve


def tail_check():
    count = 0
    for r in range(2, 11):
        for b in range(9):
            for a in (0, 1):
                for n in range(r):
                    p = F(n, r - 1)
                    actual = F(a, b + a + n) - F(n, (r - 1) * (b + a + n)) if a + n else F()
                    g = F(a, b + r - 1) - F(n, (r - 1) * (b + r - 1))
                    C = (1 - p) * (F(1, b + n + 1) - F(1, b + r - 1)) if a and n < r - 1 else F()
                    D = p * (F(1, b + n) - F(1, b + r - 1)) if not a and n else F()
                    D2 = F(n * (r - 1 - n), (r - 1) * (b + n) * (b + r - 1)) if not a and 0 < n < r - 1 else F()
                    assert actual == g + C - D and C >= 0 and D == D2 >= 0
                    count += 1
    # Existing 36-client catalog; only this one branch's algebra is checked.
    types = [(frozenset([x, y]), 1) for x in range(3) for y in range(3, 6)]
    types += [(frozenset(x + y), 3) for x in combinations(range(3), 2)
              for y in combinations(range(3, 6), 2)]
    q = (1, 0, 0, 1, 1, 0)
    d = value(types, q, 0)
    mean = (value(types, q, 3) + value(types, q, 4)) / 2
    C = D = gap = F()
    for B, w in types:
        a = int(0 in B)
        n = int(3 in B) + int(4 in B)
        p = F(n, 2)
        gap += w * F(a - p, 2)
        if a and n < 2:
            C += w * (1 - p) * (F(1, n + 1) - F(1, 2))
        if not a and n:
            D += w * p * (F(1, n) - F(1, 2))
    assert (d, mean, C, D, gap) == (10, 12, F(1, 2), F(5, 2), 0)
    return dict(scalar_cases=count, r=[2, 10], background=[0, 8],
                old_36_client_branch=dict(d=d, mean=mean, C=C, D=D, score_gap=gap),
                full_36_client_strategy_checked=False)


def gluing_check():
    m, k = 2, 4
    X, Y = tuple(range(5)), tuple(range(5, 9))
    types = [(frozenset([x, y]), 1) for x in X for y in Y]
    types += [(frozenset([y]), -1) for y in Y]
    counts = sorted({tuple(h.count(a) for a in range(9)) for h in product(range(9), repeat=2)})
    packet_checks = 0
    for q, r in combinations_with_replacement(counts, 2):
        used = {a for a in range(9) if q[a] or r[a]}
        missing = next(x for x in X if x not in used)
        positive = [(B, w) for B, w in types if w > 0 and missing not in B]
        assert sum(w for B, w in positive) == k * k
        for z in (q, r):
            assert cover(types, z) == cover(positive, z)
            for a in range(9):
                if z[a]:
                    assert value(types, z, a) == value(positive, z, a) >= 0
        packet_checks += 1
    sharp_rows = 0
    for q in counts:
        for r in counts:
            union = [j for j in range(9) if q[j] or r[j]]
            for a in union:
                if not (q[a] and r[a]):
                    continue
                others = [j for j in union if j != a]
                ratios = []
                for bits in product((0, 1), repeat=len(others)):
                    B = [a] + [j for j, bit in zip(others, bits) if bit]
                    ratios.append(F(sum(r[j] for j in B), sum(q[j] for j in B)))
                assert value(types, q, a) <= max(ratios) * value(types, r, a)
                sharp_rows += 1
    b = [1] * 5 + [-1] * 4
    C = [sum(w for B, w in types if i in B) for i in range(9)]
    H = F()
    for i, j in combinations(range(9), 2):
        Cij = sum(w for B, w in types if i in B or j in B)
        H -= b[i] * b[j] * (2 * Cij - C[i] - C[j])
    direct = sum(w * sum(b[j] for j in B) * (sum(b[j] for j in B) - 1) for B, w in types)
    assert H == direct == -8 and C == [4] * 9
    # Explicit full ordered formal strategy, arbitrary canonical tie choice.
    policy = {}
    for a in range(9):
        q = add((0,) * 9, a)
        best = max(range(9), key=lambda j: value(types, add(q, j), j))
        policy[(a,)] = best
    best_root = max(range(9), key=lambda a: value(types, add(add((0,) * 9, a), policy[(a,)]), a))
    policy[()] = best_root
    rows = 0
    for h, a in policy.items():
        q = tuple(h.count(j) for j in range(9))
        prescribed = add(q, a)
        if not h:
            prescribed = add(prescribed, policy[(a,)])
        u = value(types, prescribed, a)
        for other in range(9):
            changed = add(q, other)
            if not h:
                changed = add(changed, policy[(other,)])
            assert u >= value(types, changed, other)
            rows += 1
    return dict(m=m, k=k, labels=9, terminal_count_vectors=len(counts),
                two_terminal_packets=packet_checks, sharp_dilution_rows=sharp_rows,
                formal_decision_histories=len(policy), formal_IC_including_self=rows,
                hypermetric=H, root=best_root, last=[policy[(a,)] for a in range(9)],
                legal_global_customer_instance=False)


def bank_check():
    # New unequal-core input, not any missing original four-instance input.
    # C0,A0,B0,L0,C1,A1,B1,L1; code0=00, code1=01; Y is empty.
    h = 61
    codes = [(0, 0), (0, 1)]
    types = []
    for i, size in enumerate((10, 1)):
        types.append((frozenset([4*i, 4*i+1, 4*i+2]), size))
    for coordinate in range(2):
        for bit in (0, 1):
            members = []
            for i, code in enumerate(codes):
                members.append(4*i + (2 if code[coordinate] == bit else 3))
            types.append((frozenset(members), h))
    prefix = (0, 1, 0, 1, 1, 0, 0, 0)  # A0,L0,C1
    target = add(add(add(prefix, 3), 2), 2)
    last_prefix = add(add(prefix, 3), 2)
    assert all(value(types, add(last_prefix, a), a) <= value(types, target, 2) for a in range(8))
    frozen_rows = []
    for a in range(8):
        z = add(add(add(prefix, a), 2), 2)
        frozen_rows.append(value(types, z, a))
    assert max(frozen_rows) == value(types, target, 3) == h
    solve = outcome_solver(types, 8, 6)
    reachable, threshold = solve(prefix)
    deviated, _ = solve(add(prefix, 6))  # real B1 deviation
    for z in deviated:
        suffix = [z[a] - add(prefix, 6)[a] for a in range(8)]
        assert all(not suffix[a] for a in (0, 1, 4, 5, 6))
        for coordinate in range(2):
            loads = [0, 0]
            for i, code in enumerate(codes):
                loads[code[coordinate]] += z[4*i+2]
                loads[1-code[coordinate]] += z[4*i+3]
            assert loads == [2, 2]
        assert value(types, z, 6) >= F(123, 2)
    def permitted_order(order):
        q = prefix
        for a in order:
            if target not in solve(add(q, a))[0] or value(types, target, a) < solve(q)[1]:
                return False
            q = add(q, a)
        return True
    orders = [(3, 2, 2), (2, 3, 2), (2, 2, 3)]
    flags = [permitted_order(s) for s in orders]
    assert not flags[0]
    return dict(d=2, core_sizes=[10, 1], Y=[], h=h, G=10, total_players=6,
                prefix=prefix, target=target, target_count_reachable=target in reachable,
                ordered_suffixes=[dict(actions=s, reachable=f) for s, f in zip(orders, flags)],
                root_threshold=threshold, frozen_loader_action_values=frozen_rows,
                B1_deviation_outcomes=sorted(deviated),
                B1_min_current_profit=min(value(types, z, 6) for z in deviated),
                cached_count_states=solve.cache_info().currsize,
                new_input_not_original_probe=True)


def main():
    target = pathlib.Path(sys.argv[1])
    assert target.is_dir() and not list(target.iterdir()), 'output directory must be empty'
    result = dict(kind='new-literal-definition-audit-not-original-replay',
                  tail=tail_check(), gluing=gluing_check(), bank=bank_check(),
                  general_proofs_supplied_separately=True)
    text = json.dumps(out(result), ensure_ascii=False, indent=2) + '\n'
    (target / 'result.json').write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
