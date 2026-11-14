"""Small exact integration checks; no LP or original full-policy replay."""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import json
from pathlib import Path

TOPICS = [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)]


def loads(c):
    return tuple(sum(c[a] for a, t in enumerate(TOPICS) if x in t) for x in range(5))


def utility(a, c):
    ell = loads(c)
    return sum((F(1, 3 + ell[x]) for x in TOPICS[a]), F())


@lru_cache(None)
def outcomes(c):
    if sum(c) == 4:
        return frozenset([c])
    children = []
    for a in range(6):
        q = list(c)
        q[a] += 1
        children.append(outcomes(tuple(q)))
    threshold = max(min(utility(a, z) for z in children[a]) for a in range(6))
    return frozenset(z for a in range(6) for z in children[a] if utility(a, z) >= threshold)


def add(p, q):
    out = [F()] * max(len(p), len(q))
    for i, v in enumerate(p):
        out[i] += v
    for i, v in enumerate(q):
        out[i] += v
    return out


def multiply(p, q):
    out = [F()] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def main():
    completions = set()
    for z in outcomes((1, 0, 0, 0, 0, 0)):
        q = list(z)
        q[0] -= 1
        completions.add("".join(str(a) * v for a, v in enumerate(q)))
    assert completions == {"245", "244", "234", "155", "145", "135", "123", "045"}
    root = outcomes((0,) * 6)
    spectra = {tuple(sorted(loads(z))) for z in root}
    assert spectra == {(1, 1, 1, 2, 3), (1, 1, 2, 2, 2)}

    order = [(1, 1), (1, 2), (1, 3), (2, 2), (1, 4), (2, 3), (2, 4), (3, 3), (3, 4), (4, 4)]
    polynomials = []
    for greater, lesser in zip(order, order[1:]):
        factors = list(greater + lesser)
        numerator = [F()]
        for i, sign in enumerate([1, 1, -1, -1]):
            term = [F(sign)]
            for j, k in enumerate(factors):
                if j != i:
                    term = multiply(term, [F(3 + k), F(1)])
            numerator = add(numerator, term)
        assert min(numerator) >= 0 and numerator[0] > 0
        polynomials.append({"greater": greater, "lesser": lesser, "coefficients_at_B_eq_x_plus_3": list(map(str, numerator))})

    scalar_checks = []
    for b in [3, 4, 10, 100]:
        v = F(3, 2 * (b + 2)) + F(1, 2 * (b + 3))
        u = F(1, b + 2) + F(1, b + 3)
        p_first = F(3, b + 1) + F(2, b + 2) + F(3, b + 3)
        p_second = F(2, b + 1) + F(6, b + 2)
        assert u - v == -F(1, 2 * (b + 2) * (b + 3))
        assert p_first - 4 * v == F(2 * (b + 4), (b + 1) * (b + 2) * (b + 3))
        assert p_second - 4 * v == F(4, (b + 1) * (b + 3))
        assert F(1, b + 4) + F(1, b + 5) > F(1, b + 1)
        scalar_checks.append({"B": b, "negative_first_debt": str(u - v), "positive_total_by_spectrum": [str(p_first - 4 * v), str(p_second - 4 * v)]})

    parameter_checks = []
    for j in range(509, 517):
        local = [F(j, 6)] * 3 + [F(-1), F(139, 2), F()]
        pairs = [local[i] + local[i + 1] for i in range(5)]
        assert min(pairs) > 0
        welfare = 546 + j
        tax = F(647, 2) + F(4 * j, 3)
        potential = 801 + F(11 * j, 6)
        assert welfare + tax - potential == sum(local) == F(137, 2) + F(j, 2)
        assert 2 * welfare - (621 + j) == 471 + j
        parameter_checks.append({"J": j, "adjacent_balances": list(map(str, pairs)), "root_balance": str(welfare + tax - potential)})

    report = {
        "scope": "Independent main-topic outcome recursion, all-B order polynomials and aggregate arithmetic. Original complete ordered-policy and static minimax certificates are reused, not rerun.",
        "main_root_terminal_count": len(root),
        "cached_states": outcomes.cache_info().currsize,
        "root0_completions": sorted(completions),
        "terminal_load_spectra": sorted(spectra),
        "all_B_order_numerators": polynomials,
        "plateau_scalar_checks": scalar_checks,
        "six_player_fixed_J_checks": parameter_checks,
        "execution_note": "An initial inline check used an incorrect second-spectrum aggregate. The expression was corrected to 2/(B+1)+6/(B+2) from the literal load spectrum before this successful full run. No source or frozen evidence was changed.",
    }
    output = Path(__file__).with_name("four-pending-math-checks.json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"root_outcomes": len(root), "states": outcomes.cache_info().currsize, "order_comparisons": len(polynomials), "J_cases": len(parameter_checks), "status": "passed"}))


if __name__ == "__main__":
    main()
