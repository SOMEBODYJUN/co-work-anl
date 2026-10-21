#!/usr/bin/env python3
"""Read frozen 2396 projected data and evaluate the available three-family cut.

No row generator imported; source data are not modified. The available Z menus
are identical T_i, hence this particular clique row is redundant with self O.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "R-64201cd12083425899e2d643ec9bc087/next_credible/enhanced_2396_exact_obstruction.json"


def main():
    data = json.loads(SOURCE.read_text())
    q = 5
    edges = list(combinations(range(3), 2))
    self_O = [F(0) for _ in range(3)]
    orientations = []
    atoms = data["atom_masses"]
    by_k_mass = {k: F(0) for k in range(q + 1)}
    for atom in atoms:
        mass = F(atom["mass"])
        k = sum(atom["AB_hist"][4:])
        by_k_mass[k] += mass
        bits = tuple(map(int, atom["bits"]))
        bs = [bits[0] + bits[1] + bits[2],
              bits[0] + bits[4] + bits[5],
              bits[0] + bits[1] + bits[4]]
        for r, b in enumerate(bs):
            ell, h = atom["menus_lh"][r]
            a, g = F(1, b + 1), F(1, (b + 1) * (b + 2))
            A = a * ell - g * h
            O = (q - 1) * A - (q - 1) * a * k + g * (k * k - k)
            self_O[r] += mass * O
    assert all(x >= 0 for x in self_O)
    for orientation in product((0, 1), repeat=3):
        sources = [edge[choice] for edge, choice in zip(edges, orientation)]
        envelope, deduction, actual, residual = F(0), F(0), F(0), F(0)
        for atom in atoms:
            mass = F(atom["mass"])
            k = sum(atom["AB_hist"][4:])
            bits = tuple(map(int, atom["bits"]))
            bs = [bits[0] + bits[1] + bits[2],
                  bits[0] + bits[4] + bits[5],
                  bits[0] + bits[1] + bits[4]]
            gs, Os, Es = [], [], []
            pair_min = max(0, 2 * k - q)
            t, s = divmod(3 * k, q)
            chi = q * t * (t - 1) // 2 + s * t - 3 * pair_min
            assert chi in (0, 1)
            for r, b in enumerate(bs):
                ell, h = atom["menus_lh"][r]
                a, g = F(1, b + 1), F(1, (b + 1) * (b + 2))
                A = a * ell - g * h
                O = (q - 1) * A - (q - 1) * a * k + g * (k * k - k)
                E = (q - 1) * A - (q - 1) * a * k + g * (k * k - pair_min)
                assert E - O == g * (k - pair_min)
                gs.append(g)
                Os.append(O)
                Es.append(E)
            direct = sum(Os[r] for r in sources)
            local_E = sum(Es[r] for r in sources)
            local_cut = min(gs[r] for r in sources) * chi
            local_residual = local_E - local_cut - direct
            assert local_residual >= 0
            envelope += mass * local_E
            deduction += mass * local_cut
            actual += mass * direct
            residual += mass * local_residual
        assert envelope - deduction == actual + residual >= 0
        assert actual == sum(self_O[r] for r in sources)
        orientations.append({"edge_sources": sources,
            "independent_envelope": str(envelope), "clique_deduction": str(deduction),
            "new_row_slack": str(envelope - deduction),
            "new_row_slack_float": float(envelope - deduction),
            "existing_self_O_sum": str(actual), "nonnegative_residual": str(residual)})
    report = {
        "status": "exact_evaluation_passed_no_cut",
        "source": str(SOURCE.relative_to(HERE.parents[3])),
        "source_objective": data["objective"],
        "available_families": ["H0=ABC; Z_i=T_i; F_i=L_i^0",
                               "H1=AEU; Z_i=T_i; F_i=L_i^1",
                               "H2=ABE; Z_i=T_i; F_i=L_i^2"],
        "positive_atoms": len(atoms),
        "mass_by_K": {str(k): str(v) for k, v in by_k_mass.items()},
        "existing_self_O_slacks": list(map(str, self_O)),
        "unit_weight_all_orientations": orientations,
        "all_nonnegative_weights_reason": "Each edge's actual O row equals its source family's self O row; the clique envelope is this weighted sum plus a pointwise nonnegative residual.",
        "unavailable_reply_menu_use": "Taking Z_i^r=L_i^r would require sigma_5(H_r+L_i^r), which is not recorded. The old L_i^r must not be substituted for this reply.",
        "scope": "Frozen projected point only; does not certify an SPE or improve the five-player bound."
    }
    target = HERE / "evaluation_2396_clique.json"
    with target.open("x") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(json.dumps({"status": report["status"], "self_O_slacks_float": list(map(float, self_O)),
                      "min_unit_weight_slack": min(x["new_row_slack_float"] for x in orientations),
                      "max_unit_weight_slack": max(x["new_row_slack_float"] for x in orientations)}, indent=2))


if __name__ == "__main__":
    main()
