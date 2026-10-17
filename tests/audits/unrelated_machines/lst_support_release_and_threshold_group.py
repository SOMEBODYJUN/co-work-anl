#!/usr/bin/env python3
"""Exact Fraction audit for the threshold-cover interface and LST-support obstruction.

This is a finite arithmetic audit only. It does not implement a general LP/FPTAS.
"""
from fractions import Fraction as F
from itertools import product
import json


def loads(assign, p, m):
    out = [F(0) for _ in range(m)]
    for j, i in enumerate(assign):
        q = p[j][i]
        if q is None:
            return None
        out[i] += q
    return out


def enumerate_feasible(p, T, fixed=None):
    m = len(p[0])
    choices = []
    for j, row in enumerate(p):
        choices.append([i for i, q in enumerate(row) if q is not None])
    ans = []
    for a in product(*choices):
        if fixed and any(a[j] != i for j, i in fixed.items()):
            continue
        ls = loads(a, p, m)
        if ls is not None and max(ls, default=F(0)) <= T:
            ans.append((a, ls))
    return ans


def lst_support_obstruction():
    # m core machines, m+1 small jobs, m heavy jobs, and one extension machine.
    rows = []
    checked = []
    for m in range(2, 8):
        s = F(49 * m, 100 * (m + 1))
        p = []
        # A_i has 51/100 on every core machine and is unavailable on extension.
        for _ in range(m):
            p.append([F(51, 100)] * m + [None])
        # B_j has s on every machine, including extension. The chosen LST point
        # gives zero mass to the extension for every B_j.
        for _ in range(m + 1):
            p.append([s] * (m + 1))
        # Exact LST row loads under the stated fractional point.
        core_load = F(51, 100) + F(m + 1, m) * s
        assert core_load == 1
        assert F(0) <= s < F(49, 100)
        # OPT=1 is witnessed by A_i on distinct core machines, m B's on cores,
        # and one remaining B on the extension machine.
        witness = tuple(range(m)) + tuple(list(range(m)) + [m])
        assert max(loads(witness, p, m + 1)) < 1
        # Any matching of the heavy A jobs must occupy every core, one each.
        # Under the LST positive support, all B jobs then remain on core machines,
        # each with residual capacity 49/100; two B's exceed it for m>=2.
        residual_cap = [F(49, 100)] * m
        residual_choices = [list(range(m)) for _ in range(m + 1)]
        feasible_residual = False
        for a in product(*residual_choices):
            cnt = [0] * m
            for i in a:
                cnt[i] += 1
            if all(cnt[i] * s <= residual_cap[i] for i in range(m)):
                feasible_residual = True
                break
        assert not feasible_residual
        rows.append({"m": m, "small": str(s), "lst_row_load": str(core_load),
                     "opt_witness_max": str(max(loads(witness, p, m + 1))),
                     "support_residual_feasible": feasible_residual})
    return rows


def threshold_formula_audit():
    # Exact arithmetic for the balanced threshold. eta is positive because the
    # FPTAS cover is multiplicative; the theorem is a given-T interface.
    rows = []
    for delta, eta in [(F(1, 20), F(1, 100)), (F(1, 5), F(1, 100)),
                       (F(2, 5), F(1, 100)), (F(1, 2), F(1, 100))]:
        assert delta + eta + delta * eta < 1
        tau = ((1 + eta) * (2 + delta) - 1) / (2 + eta)
        ratio = (1 + eta) * (3 + delta) / (2 + eta)
        assert F(1, 2) <= tau < 1
        assert ratio < 2
        assert ratio == 1 + tau
        assert ratio == (1 + eta) * (2 - tau + delta)
        rows.append({"delta": str(delta), "eta": str(eta), "tau": str(tau),
                     "ratio": str(ratio), "ratio_lt_2": ratio < 2})
    return rows


def eligibility_counterexample():
    # A group with per-job sink eligibility cannot be compressed to one token.
    # Every selected cover of demand 2/5 contains two jobs with disjoint sinks.
    jobs = [
        {"h": F(3, 10), "z": [0], "sink_cost": F(1, 10)},
        {"h": F(3, 10), "z": [1], "sink_cost": F(1, 10)},
        {"h": F(3, 10), "z": [2], "sink_cost": F(1, 10)},
    ]
    demand = F(2, 5)
    covers = []
    for mask in range(1, 1 << len(jobs)):
        chosen = [i for i in range(len(jobs)) if mask >> i & 1]
        w = sum((jobs[i]["h"] for i in chosen), F(0))
        if w >= demand:
            covers.append(chosen)
    assert covers == [[0, 1], [0, 2], [1, 2], [0, 1, 2]]
    assert all(len({jobs[i]["z"][0] for i in c}) >= 2 for c in covers)
    # Full exact scheduling instance: h,z1,z2,z3; macro=.7 at h; each private
    # job has .3 at h and .1 only at its own sink. Enumerate all legal schedules.
    p = [[F(7, 10), None, None, None],
         [F(3, 10), F(1, 10), None, None],
         [F(3, 10), None, F(1, 10), None],
         [F(3, 10), None, None, F(1, 10)]]
    schedules = enumerate_feasible(p, F(1))
    assert schedules
    return {"cover_count": len(covers), "feasible_schedule_count": len(schedules),
            "single_sink_recovery": False}


def varying_endpoint_counterexample():
    # Common eligibility but endpoint-dependent costs invalidate scalar token load.
    costs = [[F(1, 10), F(100)], [F(100), F(1, 10)],
             [F(100), F(100)]]
    chosen = [0, 1]
    scalar = [sum((costs[i][z] for i in chosen), F(0)) for z in range(2)]
    assert scalar == [F(1001, 10), F(1001, 10)]
    # Full exact instance: h,h2,z1,z2; macro=.7 at h; private jobs are .3 at
    # h and have the two sink costs above. Enumerate its T=1 schedules.
    p = [[F(7, 10), None, None, None],
         [F(3, 10), None, costs[0][0], costs[0][1]],
         [F(3, 10), None, costs[1][0], costs[1][1]],
         [F(3, 10), None, costs[2][0], costs[2][1]]]
    schedules = enumerate_feasible(p, F(1))
    assert schedules == [((0, 2, 3, 0), [F(1), F(0), F(1, 10), F(1, 10)])]
    return {"scalar_sink_costs": [str(x) for x in scalar],
            "minimum_cover_jobs": chosen, "feasible_schedule_count": len(schedules),
            "single_sink_recovery": False}


def main():
    out = {
        "audit": "lst_support_release_and_threshold_group",
        "arithmetic": "fractions.Fraction",
        "threshold": threshold_formula_audit(),
        "lst_support_obstruction": lst_support_obstruction(),
        "eligibility_counterexample": eligibility_counterexample(),
        "varying_endpoint_counterexample": varying_endpoint_counterexample(),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
