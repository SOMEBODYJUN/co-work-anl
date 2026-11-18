"""Check the tau=6 relaxation witness independently of the discovery LP."""

from collections import defaultdict
from fractions import Fraction
import json
from pathlib import Path

from probe_glued_branches import anchors, rows, returns


def verify():
    path = Path(__file__).with_name("tau-six-marginal-relaxation-witness.json")
    record = json.loads(path.read_text())
    tau = Fraction(record["tau"])
    assert tau == 6
    branches = {tuple(pair) for pair in record["branches"]}
    assert branches == ({(i,6) for i in range(4)} |
                        {(i,j) for i in range(4) for j in (4,5)})
    marginals = defaultdict(Fraction)
    aggregates = defaultdict(Fraction)
    seen = set()
    welfare = Fraction(0)
    optimum_target = Fraction(0)
    for [branch, anchor_index, tail], value in record["mass"]:
        group = tuple(branch) if branch is not None else None
        mass = Fraction(value)
        assert mass > 0 and 0 <= anchor_index < len(anchors)
        atom = (group, anchor_index, tuple(tail))
        assert atom not in seen
        seen.add(atom)
        anchor, member = anchors[anchor_index]
        e, maximum = anchor[:6], anchor[6]
        if group is None:
            assert not tail
            value_rows = rows(tau, e, anchor, member, 0)
            value_rows["CAP-C"] = tau*maximum-member
            value_rows["W-opt"] = member-int(any(e))
            for j, bit in enumerate(anchor):
                value_rows[f"CAP{j}"] = maximum-bit
                value_rows[f"OPT{j}"] = member*(1-bit)-6*(1-member)*bit
            welfare += int(any(e))*mass
            optimum_target += member*mass
        else:
            assert group in branches
            index, label = group
            assert len(tail) == 5-index and set(tail) <= {0,1}
            path_bits = e[:index]+(anchor[label],)+tuple(tail)
            value_rows = rows(tau, path_bits, anchor+tuple(tail), member, index+1)
            value_rows["IC-own"] = returns(e)[index]-returns(path_bits)[index]
            for j, bit in enumerate(tail):
                value_rows[f"CAP{j}"] = maximum-bit
                value_rows[f"OPT{j}"] = member*(1-bit)-6*(1-member)*bit
        marginals[group, anchor_index] += mass
        for key, value in value_rows.items():
            aggregates[group,key] += value*mass
    for i in range(len(anchors)):
        for group in branches:
            assert marginals[None,i] == marginals[group,i]
    assert min(aggregates.values()) >= 0
    assert optimum_target == 1 and welfare == Fraction(record["welfare"]) < Fraction(1,2)
    return {"status":"exact relaxation witness", "atoms":len(seen), "branches":len(branches),
            "minimum_row":str(min(aggregates.values())), "W":str(welfare),
            "target":str(optimum_target), "exact_half_gap":str(1-2*welfare)}

if __name__=="__main__":
    print(json.dumps(verify(),indent=2))
