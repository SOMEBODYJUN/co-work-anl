"""Independent exact finite audit; the Markdown proof covers arbitrary p."""
import json
from itertools import combinations
from pathlib import Path


def r_value(mask, p, a):
    xa = (mask >> a) & 1
    others = [j for j in range(p) if j != a]
    return (xa - sum(xa * ((mask >> j) & 1) for j in others)
            + sum(((mask >> j) & 1) * ((mask >> k) & 1)
                  for j, k in combinations(others, 2)))


def functional(values, p, a):
    return values[0] + sum(values[(1 << a) | (1 << j)]
                           for j in range(p) if j != a) - values[1 << a]


def check(p, a):
    r = [r_value(mask, p, a) for mask in range(1 << p)]
    assert min(r) >= 0
    assert functional(r, p, a) == -1
    assert r[1 << a] == 1
    assert all(r[(1 << a) ^ (1 << j)] == 0 for j in range(p))
    # A nonnegative function on K is a nonnegative combination of the
    # cylinder indicators 1[x_K=pattern]. Check every such generator.
    count = 0
    min_l = None
    for k_mask in range((1 << p) - 1):
        indices = [j for j in range(p) if (k_mask >> j) & 1]
        for compact in range(1 << len(indices)):
            pattern = sum(((compact >> pos) & 1) << j
                          for pos, j in enumerate(indices))
            vals = [int((x & k_mask) == pattern) for x in range(1 << p)]
            result = functional(vals, p, a)
            assert result >= 0
            count += 1
            min_l = result if min_l is None else min(min_l, result)
    # For p>2, the degree-two r has zero full parity sum; this certifies
    # that equality only on nonempty inputs already fixes its empty value.
    parity_sum = sum(((-1) ** mask.bit_count()) * r[mask]
                     for mask in range(1 << p))
    if p > 2:
        assert parity_sum == 0
    return {"p": p, "a": a, "minimum_r": min(r), "L_r": -1,
            "proper_cylinder_generators": count, "minimum_generator_L": min_l,
            "full_parity_sum_r": parity_sum}


if __name__ == '__main__':
    rows = [check(p, a) for p in range(3, 9) for a in range(p)]
    out = {"scope": "Finite exact corroboration only; arbitrary-p proof in review Markdown",
           "rows": rows, "all_checks_passed": True}
    path = Path(__file__).with_name('boolean_proper_blocks_audit.json')
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({"all_checks_passed": True, "cases": len(rows),
                      "generator_checks": sum(row['proper_cylinder_generators'] for row in rows)},
                     ensure_ascii=False))
