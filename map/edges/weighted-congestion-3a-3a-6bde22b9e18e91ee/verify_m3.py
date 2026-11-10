#!/usr/bin/env python3
"""Independent exact replay from the finite-game definition; no author imports.
Only the m=3 member is certified here, not any infinite-m statement.
"""
import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path
import sys

sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "archives/weighted-congestion/tools/evidence/crossover/original/evidence/certificates/weighted_congestion/crossover/limit_evidence/retuned_m3_certificate.json"
DEFINITION = ROOT / "archives/weighted-congestion/state/定义/十四资源缩权多项式族与布尔极限--定义.md"
MASKS = ("0101", "0112", "1022", "1100", "1120", "1122", "1211")
T = tuple(map(Q, ("49/100", "11/10", "49/100", "3/5", "1/50", "3/100", "1")))
M = 3
W = (Q(1), Q(1,10*M), Q(1,20*M), Q(1,50*M))
DEGREE = 32*M*M
ALPHA = Q(2)
TEMPLATE = {"0000":2, "0001":2, "0010":3, "0011":0, "0100":3, "0101":2, "0110":3, "0111":1}
TEMPLATE.update({"".join(str(1-int(b)) for b in s): i for s,i in list(TEMPLATE.items())})
STATES = tuple("".join(map(str,s)) for s in itertools.product((0,1), repeat=4))


def costs(state):
    out = [Q(0) for _ in range(4)]
    for j,mask in enumerate(MASKS):
        support = sum((W[i] for i,c in enumerate(mask) if c != "0"), Q(0))
        for side in (0,1):
            # side=1 is the distinct resource with all nonzero mask digits exchanged.
            users = [i for i,c in enumerate(mask) if c != "0" and int(state[i]) == (int(c)-1)^side]
            load = sum((W[i] for i in users), Q(0))
            fee = T[j] * (load/support)**(DEGREE if j < 6 else 2)
            for i in users:
                out[i] += fee
    return tuple(out)


def main():
    certificate = json.loads(CERT.read_text())
    assert certificate["m"] == M
    assert certificate["degree"] == DEGREE
    assert tuple(map(Q,certificate["coefficients_exact"])) == T
    assert Q(certificate["comparison_alpha_exact"]) == ALPHA
    records = certificate["records"]
    assert len(records) == len(STATES) == 16
    by_state = {r["state"]:r for r in records}
    assert set(by_state) == set(STATES)
    all_costs = {s: costs(s) for s in STATES}
    maxima, margins, detail = {}, {}, []
    comparisons = {"current_costs":0, "deviation_costs":0, "flip_ratios":0, "template_margins":0, "template_players":0}
    all_positive = True
    for s in STATES:
        r = by_state[s]
        current = all_costs[s]
        dev = tuple(all_costs[s[:i]+str(1-int(s[i]))+s[i+1:]][i] for i in range(4))
        assert all(c > 0 for c in current+dev)
        ratios = tuple(current[i]/dev[i] for i in range(4))
        witness = TEMPLATE[s]
        margin = current[witness] - ALPHA*dev[witness]
        assert tuple(map(Q,r["costs_exact"])) == current
        assert tuple(map(Q,r["deviation_costs_exact"])) == dev
        assert tuple(map(Q,r["flip_ratios_exact"])) == ratios
        assert r["template_witness_player_zero_based"] == witness
        assert Q(r["template_witness_alpha_margin_exact"]) == margin
        assert r["template_witness_strict_alpha_margin_positive"] is (margin > 0)
        assert margin > 0
        maxima[s] = max(Q(1), *ratios)
        margins[s] = margin
        for k in ("current_costs", "deviation_costs", "flip_ratios"):
            comparisons[k] += 4
        comparisons["template_margins"] += 1
        comparisons["template_players"] += 1
        detail.append({"state":s, "template_player_zero_based":witness, "positive_costs":True,
                       "current_costs_exact_equal":True, "deviation_costs_exact_equal":True,
                       "flip_ratios_exact_equal":True, "template_margin_exact_equal":True,
                       "strict_template_margin_positive":True,
                       "max_flip_ratio_decimal_informational":float(maxima[s]),
                       "template_margin_decimal_informational":float(margin)})
    best = min(maxima.values())
    minimum_margin = min(margins.values())
    minimizing = [s for s in STATES if maxima[s] == best]
    assert Q(certificate["best_equilibrium_factor_exact"]) == best
    assert certificate["minimizing_states"] == minimizing
    assert certificate["strict_alpha_obstruction_all_states"] is all(v > ALPHA for v in maxima.values())
    assert certificate["template_witnesses_strict_all_states"] is all(v > 0 for v in margins.values())
    assert certificate["all_current_and_deviation_costs_positive"] is True
    assert Q(certificate["minimum_template_witness_margin_exact"]) == minimum_margin
    report = {"schema":1, "method":"independent Fraction reconstruction from seven masks, both complementary resources, normalized monomial fees, and all sixteen action states; no author-code imports",
              "certificate":{"path":str(CERT.relative_to(ROOT)), "sha256":hashlib.sha256(CERT.read_bytes()).hexdigest(),
                             "bytes":len(CERT.read_bytes()), "all_fields_structurally_loaded":True},
              "definition":{"path":str(DEFINITION.relative_to(ROOT)), "sha256":hashlib.sha256(DEFINITION.read_bytes()).hexdigest()},
              "coverage":{"m":M, "degree":DEGREE, "states":16, "real_unilateral_flips":64,
                          "resources":14, "exact_field_comparisons":comparisons},
              "all_exact_comparisons_pass":True, "all_current_and_deviation_costs_positive":True,
              "all_sixteen_states_have_strict_two_improvement":True,
              "all_sixteen_prescribed_template_margins_positive":True,
              "best_equilibrium_factor_exact_matches_certificate":True,
              "best_equilibrium_factor_gt_two":best > ALPHA,
              "best_equilibrium_factor_decimal_informational":float(best),
              "minimizing_states":minimizing,
              "minimum_template_margin_exact_matches_certificate":True,
              "minimum_template_margin_decimal_informational":float(minimum_margin),
              "details":detail,
              "scope":"Complete verification of the m=3 finite certificate only. Infinite-m convergence, m>=52, m>=20, and template threshold require their mathematical proofs."}
    target = Path(__file__).with_name("m3-verification.json")
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k != "details"},ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
