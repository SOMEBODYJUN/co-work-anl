"""Independent definition-level attack on the 2396-row projected point.

No imports from the author's row generator or canonical indexed rows.
All arithmetic is exact. This rejects the frozen projected point, not HALF.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "next_credible/enhanced_2396_exact_obstruction.json"


def membership_patterns(d, ell, h):
    """Fix t_i=1 for i<d; enumerate every compatible L membership."""
    for inside in combinations(range(d), h):
        for outside in combinations(range(d, 5), ell - h):
            selected = set(inside) | set(outside)
            yield tuple(int(i in selected) for i in range(5))


def main():
    data = json.loads(SOURCE.read_text())
    total = F()
    records = []
    checked_pairings = 0
    for atom_index, atom in enumerate(data["atom_masses"]):
        # Original bit order: A B C D E U V W X Y.
        bits = tuple(map(int, atom["bits"]))
        prefix_load = bits[0] + bits[1] + bits[4]  # true ordered prefix ABE
        d = sum(atom["AB_hist"][4:])
        target_ell, target_h = atom["menus_lh"][1]  # after AEU,T_i
        source_ell, source_h = atom["menus_lh"][2]  # after ABE,T_i
        coefficient = (F(source_ell - target_ell, prefix_load + 1)
                       - F(source_h - target_h,
                           (prefix_load + 1) * (prefix_load + 2)))
        # Directly reconstruct every possible within-t alignment. There is no
        # l_source*l_target product in a last player's payoff comparison.
        pairings = 0
        for source in membership_patterns(d, source_ell, source_h):
            for target in membership_patterns(d, target_ell, target_h):
                direct = sum((F(source[i] - target[i],
                                prefix_load + int(i < d) + 1)
                              for i in range(5)), F())
                assert direct == coefficient
                pairings += 1
        assert pairings > 0
        checked_pairings += pairings
        mass = F(atom["mass"])
        total += mass * coefficient
        records.append({"atom": atom_index, "prefix_load": prefix_load,
                        "optimal_membership_count": d,
                        "coefficient": str(coefficient),
                        "mass": str(mass), "term": str(mass * coefficient),
                        "compatible_pairings_checked": pairings})
    expected = F(-33962942532321286037391724417608677893,
                 2370629578513027021549656484975223155224)
    assert total == expected and total < 0
    report = {
        "scope": "fixed projected point cannot be completed as a full SPE",
        "independence": "only the frozen input was read; no row generator imported",
        "source": str(SOURCE.relative_to(HERE.parent)),
        "true_history": ["A", "B", "E", "T_i"],
        "actual_reply": "L_i^2",
        "compared_legal_topic": "L_i^1",
        "slack": str(total),
        "compatible_pairings_checked": checked_pairings,
        "records": records,
    }
    target = HERE / "independent_aligned_menu_audit.json"
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "records"}, indent=2))


if __name__ == "__main__":
    main()
