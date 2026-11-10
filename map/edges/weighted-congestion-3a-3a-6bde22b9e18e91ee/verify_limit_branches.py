#!/usr/bin/env python3
"""Exact finite Boolean table and rational tail arithmetic; no author imports."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

MASKS = ("0101","0112","1022","1100","1120","1122","1211")
T = tuple(map(Q,("49/100","11/10","49/100","3/5","1/50","3/100","1")))
STATES = tuple("".join(map(str,s)) for s in product((0,1),repeat=4))
TEMPLATE = {"0000":2,"0001":2,"0010":3,"0011":0,"0100":3,"0101":2,"0110":3,"0111":1}
TEMPLATE.update({"".join(str(1-int(b)) for b in s):i for s,i in list(TEMPLATE.items())})


def limit_costs(state):
    out = [Q(0)]*4
    for j,mask in enumerate(MASKS):
        support = [i for i,c in enumerate(mask) if c != "0"]
        for side in (0,1):
            users = [i for i in support if int(state[i]) == ((int(mask[i])-1)^side)]
            active = len(users) == len(support) if j < 6 else 0 in users
            if active:
                for i in users:
                    out[i] += T[j]
    return tuple(out)


def main():
    table = {s:limit_costs(s) for s in STATES}
    rows = []
    maxima = {}
    margins = []
    for s in STATES:
        current = table[s]
        dev = tuple(table[s[:i]+str(1-int(s[i]))+s[i+1:]][i] for i in range(4))
        assert all(v > 0 for v in current+dev)
        ratios = tuple(current[i]/dev[i] for i in range(4))
        maxima[s] = max(Q(1),*ratios)
        i = TEMPLATE[s]
        margin = current[i]-2*dev[i]
        margins.append(margin)
        assert margin > 0
        rows.append({"state":s,"current_costs_exact":list(map(str,current)),
                     "deviation_costs_exact":list(map(str,dev)),"flip_ratios_exact":list(map(str,ratios)),
                     "max_ratio_exact":str(maxima[s]),"template_player_zero_based":i,
                     "template_alpha2_margin_exact":str(margin)})
    best = min(maxima.values())
    assert best == Q(100,49)
    assert min(margins) == Q(1,50)
    minimizing = [s for s in STATES if maxima[s] == best]
    assert minimizing == ["0100","0101","1010","1011"]
    old = Q(1,50)-3*(Q(273,100)*Q(3,8)**28+Q(17,2600))
    new = Q(1,50)-Q(17,1000)-Q(289,2000000)-Q(112,25)*Q(3,8)**10
    assert old == Q(9671406313347824129679641,25145657047984286833888460800) > 0
    assert new == Q(2735869393,1048576000000) > 0
    support_sums = [sum((T[j] for j,mask in enumerate(MASKS[:6]) if mask[i]!="0"),Q(0)) for i in range(4)]
    assert support_sums == [Q(57,50),Q(56,25),Q(41,25),Q(211,100)]
    report = {"schema":1,"method":"independent finite Boolean table reconstructed from all complementary masks; exact rational arithmetic for both tail margins",
              "states":16,"real_unilateral_flips":64,"positive_all_current_and_deviation_costs":True,
              "best_limit_equilibrium_factor_exact":str(best),"minimizing_states":minimizing,
              "minimum_alpha2_template_margin_exact":str(min(margins)),
              "first_six_total_amplitude_exact":str(sum(T[:6])),
              "first_six_amplitude_incident_to_players_exact":list(map(str,support_sums)),
              "old_m52_absolute_error_margin_exact":str(old),"new_m20_directional_error_margin_exact":str(new),
              "all_exact_checks_pass":True,"rows":rows,
              "scope":"The finite table and rational arithmetic are fully checked; infinite-m conclusions additionally use the analytic inequalities stated in reading-and-proof.md."}
    target = Path(__file__).with_name("limit-and-tail-verification.json")
    target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k != "rows"},ensure_ascii=False,indent=2))
    for row in rows[:8]:
        print(row["state"],row["flip_ratios_exact"],row["max_ratio_exact"])

if __name__ == "__main__":
    main()
