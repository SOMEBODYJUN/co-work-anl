"""Definition-level exact audit of the five-site reduction.

The oracle below does not import the repository's equilibrium solvers.
It enumerates every closed three-state support, including one-mixer intervals.
For small cases it also enumerates every diagonal and optimizes all 25
labelled layouts using the true coordinate minima. Larger cases use the
proved diagonal normalization, with diagonal exclusions checked separately.
Finite results are regression evidence, not the proof of the reduction.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from facility_spe.shared.five_site_hardness import (
    constants, reduction, integer_instance, serial,
)


def local(instance, s, t, forced_probabilities=None):
    w = list(map(F, instance["weights"]))
    S, T = set(instance["locations"][s]), set(instance["locations"][t])
    shared = sorted(S & T)
    A = sum((w[i] for i in S-T), F(0))
    B = sum((w[i] for i in T-S), F(0))
    ww = [w[i] for i in shared]
    # All audit instances have been uniformly scaled to integers.
    assert all(x.denominator == 1 for x in [A, B] + ww)
    A, B = int(A), int(B)
    ww = list(map(int, ww))
    V = A+B+sum(ww)
    pieces = {}
    forced = [(shared.index(i), F(p))
              for i, p in (forced_probabilities or {}).items()]
    accepted = 0
    for state in product((-1, 0, 1), repeat=len(ww)):
        m = state.count(0)
        num = A-B
        lo, hi = -V, V
        for x, sign in zip(ww, state):
            num += x*sign
            if sign <= 0:
                lo = max(lo, -x)
            if sign >= 0:
                hi = min(hi, x)
        if lo > hi:
            continue
        if m == 1:
            if num:
                continue
            dl, dh = F(lo), F(hi)
        else:
            den = 1-m
            if den < 0:
                num, den = -num, -den
            if not lo*den <= num <= hi*den:
                continue
            dl = dh = F(num, den)
        xl, xh = (V+dl)/2, (V+dh)/2
        for index, expected in forced:
            sign = state[index]
            for delta in (dl, dh):
                p = (F(0) if sign == -1 else F(1) if sign == 1
                     else (1+delta/ww[index])/2)
                assert p == expected, ('forced probability failed', state, delta)
        accepted += 1
        pieces.setdefault((xl, xh), state)
    assert pieces, ("empty equilibrium set", s, t)
    return dict(s=s, t=t, shared=shared, A=F(A), B=F(B), ww=ww,
                V=F(V), pieces=pieces, accepted=accepted)


def witness(rec, piece, x):
    lo, hi = piece
    assert lo <= x <= hi
    delta = 2*x-rec["V"]
    state = rec["pieces"][piece]
    p = [F(0) if z == -1 else F(1) if z == 1 else (1+delta/w)/2
         for w, z in zip(rec["ww"], state)]
    return dict(layout=[rec["s"], rec["t"]], shared=rec["shared"],
                prob_first=p, loads=[x, rec["V"]-x])


def validate_ne(instance, cert):
    """Recompute conditional costs, without using support-cell inequalities."""
    w = list(map(F, instance["weights"]))
    s, t = cert["layout"]
    S, T = set(instance["locations"][s]), set(instance["locations"][t])
    shared = sorted(S & T)
    assert shared == cert["shared"]
    p = list(map(F, cert["prob_first"]))
    assert len(p) == len(shared) and all(0 <= q <= 1 for q in p)
    A = sum((w[i] for i in S-T), F(0))
    B = sum((w[i] for i in T-S), F(0))
    X = A+sum((w[i]*q for i, q in zip(shared, p)), F(0))
    Y = B+sum((w[i]*(1-q) for i, q in zip(shared, p)), F(0))
    assert [X, Y] == list(map(F, cert["loads"]))
    for i, q in zip(shared, p):
        cost1 = X+w[i]*(1-q)
        cost2 = Y+w[i]*q
        if q > 0:
            assert cost1 <= cost2
        if q < 1:
            assert cost2 <= cost1
    return X, Y


def all_records(instance, diagonals):
    records = {}
    for s in range(5):
        for t in range(s if diagonals else s+1, 5):
            forced = {4: F(0)} if (s, t) == (3, 4) else None
            rec = local(instance, s, t, forced)
            records[s, t] = rec
            for piece in rec["pieces"]:
                for x in set((piece[0], piece[1], sum(piece)/2)):
                    validate_ne(instance, witness(rec, piece, x))
    return records


def bounds(rec):
    return min(x[0] for x in rec["pieces"]), max(x[1] for x in rec["pieces"])


def min_payoff(records, s, t):
    rec = records[min(s, t), max(s, t)]
    low, high = bounds(rec)
    return low if s <= t else rec["V"]-high


def best_on_interval(V, lo, hi, D1, D2):
    if V == 0:
        return F(1) if D1 == D2 == 0 else None
    x = V*D1/(D1+D2) if D1+D2 else lo
    x = max(lo, min(hi, x))
    if (x == 0 and D1 > 0) or (V == x and D2 > 0):
        return None
    return max(F(1), D1/x if x else F(0),
               D2/(V-x) if V != x else F(0))


def optimum(instance, records, full):
    reach = [sum((F(instance["weights"][i]) for i in S), F(0))
             for S in instance["locations"]]
    threat = [
        max(min_payoff(records, s, t) for s in range(5) if full or s != t)
        for t in range(5)
    ]
    candidates = {}
    if not full:
        for t in range(5):
            candidates[f"{t+1},{t+1}"] = max(F(1), 2*threat[t]/reach[t])
    for (s, t), rec in records.items():
        vals = [best_on_interval(rec["V"], lo, hi, threat[t], threat[s])
                for lo, hi in rec["pieces"]]
        vals = [v for v in vals if v is not None]
        if vals:
            candidates[f"{s+1},{t+1}"] = min(vals)
    best = min(candidates.values())
    return best, candidates, threat


def min_witness(records, s, t, coordinate):
    rec = records[min(s, t), max(s, t)]
    # coordinate is zero-based in the requested labelled layout.
    original_coordinate = coordinate if s <= t else 1-coordinate
    low, high = bounds(rec)
    x = low if original_coordinate == 0 else high
    piece = next(k for k in rec["pieces"] if k[0] <= x <= k[1])
    cert = witness(rec, piece, x)
    if s > t:
        cert = dict(layout=[s, t], shared=cert["shared"],
                    prob_first=[1-p for p in cert["prob_first"]],
                    loads=list(reversed(cert["loads"])))
    return cert


def balanced(instance, s):
    shared = sorted(instance["locations"][s])
    h = sum((F(instance["weights"][i]) for i in shared), F(0))/2
    return dict(layout=[s, s], shared=shared,
                prob_first=[F(1, 2)]*len(shared), loads=[h, h])


def certificate(instance, records, a):
    # On path: sites (1,4), i.e. zero-based (0,3).
    rule = {}
    for s in range(5):
        for t in range(5):
            rule[s, t] = (balanced(instance, s) if s == t
                          else min_witness(records, s, t, 0))
    rule[0, 3] = min_witness(records, 0, 3, 0)  # unique local NE
    for r in range(5):
        if r != 0:
            rule[r, 3] = (balanced(instance, 3) if r == 3
                          else min_witness(records, r, 3, 0))
        if r != 3:
            rule[0, r] = (balanced(instance, 0) if r == 0
                          else min_witness(records, 0, r, 1))
    for cert in rule.values():
        validate_ne(instance, cert)
    X, Y = rule[0, 3]["loads"]
    for r in range(5):
        if r != 0:
            assert rule[r, 3]["loads"][0] <= a*X
        if r != 3:
            assert rule[0, r]["loads"][1] <= a*Y
    return {"on_path": [0, 3], "factor": a,
            "continuations": [rule[s, t] for s in range(5) for t in range(5)]}


def source_answer(numbers, target):
    return any(sum(b for b, chosen in zip(numbers, choices) if chosen) == target
               for choices in product((False, True), repeat=len(numbers)))


def audit_case(numbers, target, a, full):
    rational, pars = reduction(numbers, target, a)
    instance, scale = integer_instance(rational)
    records = all_records(instance, full)
    best, candidates, threat = optimum(instance, records, full)
    yes = source_answer(numbers, target)
    T = pars["T"]*scale
    hard = records[3, 4]
    mu = min_payoff(records, 4, 3)
    assert mu >= T
    assert (mu == T) == yes
    assert (best == a) if yes else (best > a)

    # Macro z is forced to site 5 in *every* enumerated hard support,
    # including every endpoint of one-mixer continua.
    macro_index = hard["shared"].index(4)
    for piece in hard["pieces"]:
        for x in set((piece[0], piece[1], sum(piece)/2)):
            assert witness(hard, piece, x)["prob_first"][macro_index] == 0

    # General proofs exclude the other 14 unordered on-path classes.
    R = [r*scale for r in pars["reach"]]
    v1, v2, v3 = [pars[k]*scale for k in ("v1", "v2", "v3")]
    H = pars["H"]*scale
    strict_margins = {
        "11": R[1]-a*R[0]/2,
        "22": R[2]-a*R[1]/2,
        "33": R[3]-a*R[2]/2,
        "44": mu-a*R[3]/2,
        "55": R[0]-a*R[4]/2,
        "12": R[2]-a*v1,
        "13": R[3]-a*v1,
        "23": R[3]-a*v2,
        "24": mu-a*v2,
        "34": mu-a*v3,
        "15": R[1]-a*R[4],
        "25": R[0]-a*H,
        "35": R[0]-a*H,
        "45": R[0]-a*bounds(hard)[1],
    }
    assert len(strict_margins) == 14
    assert all(v > 0 for v in strict_margins.values())
    if full:
        off = {k: v for k, v in records.items() if k[0] != k[1]}
        normal_best, _, _ = optimum(instance, off, False)
        assert normal_best == best

    gap_lower = pars["scale"]*scale/(2*(len(pars["raw_micro"])-1))
    if not yes:
        assert mu-T >= gap_lower
    cert = certificate(instance, records, a) if yes else None
    # Make sure the original and complemented bounded instances agree.
    bounded_yes = any(sum(t*x for t, x in zip(ts, pars["bounded"]))
                      == pars["bounded_target"]
                      for ts in product(range(3), repeat=len(pars["bounded"])))
    assert bounded_yes == yes
    result = dict(numbers=numbers, target=target, a=a, source_yes=yes,
                  full_diagonal_enumeration=full, customer_count=len(instance["weights"]),
                  alpha_star=best, normalized_mu=mu/scale,
                  normalized_T=pars["T"], normalized_gap=(mu-T)/scale,
                  max_integer_bits=max(w.bit_length() for w in instance["weights"]),
                  distinct_support_load_pieces=sum(len(r["pieces"]) for r in records.values()),
                  accepted_closed_supports=sum(r["accepted"] for r in records.values()),
                  all_other_layouts_min_additive_margin=min(strict_margins.values())/scale,
                  factors_by_unordered_layout=candidates)
    return result, instance, pars, cert




def verify_complete_certificate(instance, certificate):
    a = F(certificate["factor"])
    assert a >= 1
    entries = certificate["continuations"]
    rule = {tuple(rec["layout"]): rec for rec in entries}
    assert len(entries) == len(rule) == 25
    assert set(rule) == set(product(range(5), repeat=2))
    loads = {key: validate_ne(instance, rec) for key, rec in rule.items()}
    s, t = certificate["on_path"]
    X, Y = loads[s, t]
    for r in range(5):
        if r != s:
            assert loads[r, t][0] <= a*X
        if r != t:
            assert loads[s, r][1] <= a*Y
    return True


def local_instance(A, B, common):
    weights = list(common)
    sites = [list(range(len(common))), list(range(len(common)))]
    for side, background in enumerate((A, B)):
        if background:
            sites[side].append(len(weights))
            weights.append(background)
    return dict(weights=weights, locations=sites)


def merged_intervals(rec):
    answer = []
    for lo, hi in sorted(rec["pieces"]):
        if answer and lo <= answer[-1][1]:
            answer[-1][1] = max(answer[-1][1], hi)
        else:
            answer.append([lo, hi])
    return answer


def audit_forced_macro():
    count = 0
    for micro in ((1,), (1, 2), (1, 1, 2)):
        for extra in (1, 2):
            delta = sum(micro)+extra
            for macro in range(1, 9):
                for B in (0, 3):
                    A = B+delta
                    full_inst = local_instance(A, B, [macro]+list(micro))
                    full = local(full_inst, 0, 1, {0: F(0)})
                    reduced = local(local_instance(A, B+macro, list(micro)), 0, 1)
                    assert merged_intervals(full) == merged_intervals(reduced)
                    for piece in full["pieces"]:
                        cert = witness(full, piece, sum(piece)/2)
                        validate_ne(full_inst, cert)
                        assert cert["prob_first"][0] == 0
                    count += 1
    # Strictness attack: at delta = W the macro need not be forced.
    boundary = local_instance(1, 0, [3, 1])
    cert = dict(layout=[0, 1], shared=[0, 1],
                prob_first=[F(1, 2), F(0)], loads=[F(5, 2), F(5, 2)])
    validate_ne(boundary, cert)
    assert cert["prob_first"][0] != 0
    return count

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", required=True)
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    start = time.perf_counter()
    tested = 0
    for den in range(2, 61):
        for num in range(den+1, 2*den):
            a = F(num, den)
            if a*a < a+1:
                constants(a)
                tested += 1
    for a in (F(1000001,1000000), F(161803398874989,100000000000000)):
        constants(a)
        tested += 1
    macro_checks = audit_forced_macro()
    for invalid in (F(1), F(2), F(1618034, 1000000)):
        try:
            constants(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("out-of-domain multiplier accepted")
    cases = []
    rates = [F(7,5), F(3,2), F(8,5), F(809,500)]
    if args.quick:
        rates = [F(3,2)]
    for a in rates:
        for target in (1,2):
            row, _, _, _ = audit_case([2], target, a, True)
            cases.append(row)
    if not args.quick:
        for a in (F(3,2), F(809,500)):
            for target in (2,4,5):
                row, _, _, _ = audit_case([2,3], target, a, False)
                cases.append(row)
    payload = serial(dict(
        claim="SC-FIVE-DECa-HARD",
        scope="Finite exact regression, not a universal proof.",
        parameter_search_tests=tested, forced_macro_tests=macro_checks,
        strict_boundary_counterexample_verified=True,
        invalid_factor_inputs_rejected=3, cases=cases,
        all_assertions_passed=True,
        elapsed_seconds=round(time.perf_counter()-start, 3),
        repository_checks_run=False,
    ))
    with open(args.output, "x", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
