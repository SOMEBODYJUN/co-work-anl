"""Read every frozen certificate and check it with exact rational arithmetic.

No original generator is imported and no LP solver is used here.  The row
coefficients below are reconstructed from the displayed mathematical formulas.
The original JSON files, including every floating proposal, remain separate.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import math
import sys


def rows(m, word):
    """Universal (B membership, C membership, optimum multiplicity) atoms."""
    atoms = [(b, c, j) for b, c in product((0, 1), repeat=2)
             for j in range(m + 1) if b or c or j]
    nB, nC = word.count(0), word.count(1)
    names = [f"node{i + 1}:{label}" for i in range(m)
             for label in ("K:0", "K:1", "sum-opt", "cover")]
    names += ["last-two:cover", "last-two:sum-pairs",
              "last-two:pair:0,0", "last-two:pair:0,1",
              "last-two:pair:1,1"]
    coefficients = {name: [] for name in names}
    welfare, optimum = [], []
    for b, c, j in atoms:
        bits = (b, c)
        d = nB * b + nC * c
        actual = [F(bits[a], d) if bits[a] else F(0) for a in word]
        welfare.append(F(d > 0))
        optimum.append(F(j > 0))
        for i in range(m):
            p = sum(bits[a] for a in word[:i])
            k = m - i
            values = (actual[i] - F(b, p + k),
                      actual[i] - F(c, p + k),
                      m * actual[i] - F(j, p + k),
                      m * k * actual[i] + F(p, p + k) - F(j > 0))
            for label, value in zip(("K:0", "K:1", "sum-opt", "cover"), values):
                coefficients[f"node{i + 1}:{label}"].append(value)
        p = sum(bits[a] for a in word[:-2])
        H = actual[-2] + actual[-1] + F(bits[word[-2]], (p + 1) * (p + 2))
        coefficients["last-two:cover"].append(F(m, 2) * H + F(p, p + 1) - F(j > 0))
        coefficients["last-two:sum-pairs"].append(
            F(m * (m - 1), 2) * H - F(j * (m - j), p + 1) - F(j * (j - 1), p + 2))
        for Q, R in ((0, 0), (0, 1), (1, 1)):
            count = bits[Q] + bits[R]
            pair = F(count, p + count) if count else F(0)
            coefficients[f"last-two:pair:{Q},{R}"].append(H - pair)
    return atoms, welfare, optimum, coefficients


def check_two_support(path):
    report = json.loads(path.read_text())
    assert set(report) == {"scope", "m"}
    assert report["scope"] == (
        "Uniform in all finite common catalogs and all full-history pure SPE with a specified "
        "two-label on-path word; LP row source uses actual moves and the true last-two tax "
        "inequality. Uncertified floating values are not theorems.")
    assert set(report["m"]) == {str(m) for m in range(2, 11)}
    total_patterns = total_residuals = total_nonzero_multipliers = total_coefficients = 0
    summaries = []
    for m in range(2, 11):
        block = report["m"][str(m)]
        assert set(block) == {"worst_proposal", "worst_path", "all_exact_dual_ok",
                              "every_certificate_below_two", "patterns"}
        records = block["patterns"]
        expected_words = [(0,) + tail for tail in product((0, 1), repeat=m - 1)]
        assert [tuple(r["path"]) for r in records] == expected_words
        betas = []
        for record in records:
            assert set(record) == {"path", "proposal", "beta", "exact_dual_ok", "dual", "minimum_residual"}
            word = tuple(record["path"])
            atoms, W, O, G = rows(m, word)
            assert len(atoms) == 4 * m + 3 and len(G) == 4 * m + 5
            beta = F(record["beta"])
            multipliers = {name: F(value) for name, value in record["dual"].items()}
            assert set(multipliers) <= set(G)
            assert all(value > 0 for value in multipliers.values())
            residuals = [beta * W[t] - O[t] - sum(mu * G[name][t] for name, mu in multipliers.items())
                         for t in range(len(atoms))]
            assert all(value >= 0 for value in residuals)
            assert record["exact_dual_ok"] is True
            assert F(record["minimum_residual"]) == min(residuals)
            assert isinstance(record["proposal"], (float, int)) and math.isfinite(record["proposal"])
            assert math.isclose(record["proposal"], float(beta), rel_tol=1e-9, abs_tol=1e-9)
            betas.append(beta)
            total_patterns += 1
            total_residuals += len(atoms)
            total_coefficients += len(atoms) * len(G)
            total_nonzero_multipliers += len(multipliers)
        worst = max(records, key=lambda r: r["proposal"])
        assert block["worst_path"] == worst["path"]
        assert block["worst_proposal"] == worst["proposal"]
        assert block["all_exact_dual_ok"] is True
        assert block["every_certificate_below_two"] == all(beta <= 2 for beta in betas)
        best_bound = max(betas)
        witnesses = [r for r in records if F(r["beta"]) == best_bound]
        summaries.append({"m": m, "ordered_words_after_relabeling": len(records),
                          "atoms_per_word": 4 * m + 3, "rows_per_word": 4 * m + 5,
                          "maximum_accepted_exact_beta": str(best_bound),
                          "all_certificates_at_most_two": best_bound <= 2,
                          "first_maximizing_word": witnesses[0]["path"],
                          "first_maximizing_dual": witnesses[0]["dual"],
                          "negative_residuals": 0})
    return {"full_schema_and_every_record_checked": True, "patterns": total_patterns,
            "rational_atom_residuals": total_residuals,
            "rational_row_coefficients_reconstructed": total_coefficients,
            "nonzero_rational_multipliers": total_nonzero_multipliers, "by_m": summaries}


def check_private(path):
    data = json.loads(path.read_text())
    assert set(data) == {"status", "audited_m_range", "cases", "m7_reduced"}
    assert data["status"] == (
        "No SPE counterexample: every proposed path is ruled out for all full-history pure SPE "
        "by the private-guard backward induction.")
    assert data["audited_m_range"] == [7, 50]
    assert [r["m"] for r in data["cases"]] == list(range(7, 51))
    row_checks = atom_coefficients = 0
    for record in data["cases"]:
        m = record["m"]
        a, b, c = 3*m*m-8*m+7, 2*(m-1)*(m-2), 6*(m-1)
        W, O = m*(b+c), m*(a+b+c)
        uB, uC = F(m*b, m-2), F(m*c, 2)
        atoms, welfare, optimum, G = rows(m, (0,) * (m-2) + (1, 1))
        masses = [m*a if atom == (0,0,1) else m*b if atom == (1,0,1)
                  else m*c if atom == (0,1,1) else 0 for atom in atoms]
        values = {name: sum(x*y for x,y in zip(row, masses)) for name,row in G.items()}
        assert all(value >= 0 for value in values.values())
        assert sum(x*y for x,y in zip(welfare,masses)) == W
        assert sum(x*y for x,y in zip(optimum,masses)) == O
        assert O > 2*W and a+b+c < 2*a and a > uB
        assert a+F(b,m-1)+F(c,2) == uC and F(m*c,3) == uB
        expected = {"m":m, "a":a, "b":b, "c":c, "W":W, "OPT":O,
                    "ratio_of_impossible_path":str(F(O,W)), "B_player_payoff":str(uB),
                    "C_player_payoff":str(uC), "private_guard_size_gap":a-b-c,
                    "strict_private_deviation_gap":str(a-uB),
                    "all_actual_floor_and_last_two_tax_rows_nonnegative":True,
                    "minimum_row_slack":str(min(values.values())),
                    "zero_rows":[name for name,value in values.items() if value == 0]}
        assert record == expected
        row_checks += len(G)
        atom_coefficients += len(G)*len(atoms)
    reduced = {"per_T_private":49,"per_T_B_shared":30,"per_T_C_shared":18,"T_size":97,
               "W":336,"OPT":679,"B_payoff":42,"C_payoff":63,"guard_gap":1,
               "deviation_private_gap":7}
    assert data["m7_reduced"] == reduced
    return {"full_schema_and_all_fields_checked":True, "cases":44, "m_range":[7,50],
            "exact_necessary_row_evaluations":row_checks,
            "rational_atom_row_coefficients_reconstructed":atom_coefficients,
            "m7_reduced":reduced,
            "meaning":"Necessary-row feasible proposed paths, excluded from every complete-history pure SPE by the separate analytic private-guard proof."}


def main():
    base = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent / "original"
    files = sorted(base.iterdir())
    hashes = {p.name:{"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
              for p in files if p.is_file()}
    result = {"checker":"independent exact reconstruction of every saved rational certificate; no generator imports or LP calls",
              "source_directory":base.name, "files":hashes,
              "two_support":check_two_support(base/"two_support_obstruction.json"),
              "private_guard":check_private(base/"private_guard_audit.json")}
    out = Path(sys.argv[2]) if len(sys.argv)>2 else Path(__file__).resolve().parent/"verification.json"
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({"status":"exact_checks_passed","patterns":result["two_support"]["patterns"],
                      "atom_residuals":result["two_support"]["rational_atom_residuals"],
                      "private_cases":result["private_guard"]["cases"],"output":str(out)}))


if __name__ == "__main__":
    main()
