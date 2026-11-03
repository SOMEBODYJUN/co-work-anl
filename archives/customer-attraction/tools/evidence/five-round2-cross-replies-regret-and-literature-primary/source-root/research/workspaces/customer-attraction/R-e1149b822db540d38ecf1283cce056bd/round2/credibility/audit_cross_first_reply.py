"""Exact audit of cross-family first-reply menu IC; writes only beside itself.

The serialized old LP primal is a diagnostic projection, never an SPE instance.
Fractions are made from the serialized decimal coordinates, not recovered as a
claim about feasibility in the old necessary-condition system.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "customer_attraction/__init__.py").exists())
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, ExactSPESolver, verify_certificate

SOURCE = ROOT / "research/workspaces/customer-attraction/R-a27734a8bba345cbb5fad186c120d0bf/root_shared_max_copy_cg.json"
FAMS = {"AB": ("AB_hist", "AB", 3), "AE": ("AE_hist", "AE", 3),
        "S": ("second_hist", "A", 4)}
TYPES = {k: list(product((0, 1), repeat=k)) for k in (3, 4)}


def old_projection():
    data = json.loads(SOURCE.read_text())
    slacks = {}
    menu_sizes = {}
    copy_menu = {}
    root_profit = F(0)
    ds = {d: F(0) for d in range(6)}
    support = 0
    for atom, weight in zip(data["atoms"], data["primal_float"]):
        mass = F(str(weight))
        if not mass:
            continue
        assert mass > 0
        support += 1
        bits = dict(zip("ABCDEUVWXY", map(int, atom["bits"])))
        if bits["A"]:
            root_profit += mass*F(1, sum(bits[z] for z in "ABCDE"))
        d = sum(atom["AB_hist"][4:])
        ds[d] += mass
        features = {}
        for fam, (key, pre, k) in FAMS.items():
            hist = atom[key]
            assert sum(hist) == 5
            assert sum(n*t[0] for n, t in zip(hist, TYPES[k])) == d
            p = sum(bits[z] for z in pre)
            first = sum((n*F(t[1], p+sum(t)) for n, t in zip(hist, TYPES[k]) if t[1]), F(0))
            den = F(d, p+k) + F(5-d, p+k-1)
            counts = [sum(n*t[i] for n, t in zip(hist, TYPES[k])) for i in range(k)]
            features[fam] = (first, den, counts)
            for pos in range(1, k):
                count = counts[pos]
                mn = f"{fam}:{pos}"
                menu_sizes[mn] = menu_sizes.get(mn, F(0)) + mass*count
                for fixed, bit in bits.items():
                    n = f"menu-source:{mn}:fixed-query:{fixed}"
                    copy_menu[n] = copy_menu.get(n, F(0)) - mass*(F(16,3)*count+bit*(5-F(4,5)*count))
                    n = f"fixed-source:{fixed}:menu-query:{mn}"
                    copy_menu[n] = copy_menu.get(n, F(0)) - mass*(F(80,3)*bit+F(count,1+4*bit))
        for fi, pn in enumerate(("actual", "second", "third")):
            mn = f"L:{pn}"
            menu_sizes[mn] = menu_sizes.get(mn, F(0)) + mass*atom["menus_lh"][fi][0]
        for receiver in FAMS:
            first, den, _ = features[receiver]
            for source in FAMS:
                if source == receiver:
                    continue
                for pos in range(1, len(features[source][2])):
                    name = f"first:{receiver}:query:{source}:{pos}"
                    value = 5*first-features[source][2][pos]*den
                    slacks[name] = slacks.get(name, F(0)) + mass*value
        for receiver in FAMS:
            first, den, _ = features[receiver]
            for fi, pn in enumerate(("actual", "second", "third")):
                name = f"first:{receiver}:query:L:{pn}"
                value = 5*first-atom["menus_lh"][fi][0]*den
                slacks[name] = slacks.get(name, F(0)) + mass*value
    cap = F(str(data["shared_K_float"]))
    menu_caps = {n: 5*cap-v for n, v in menu_sizes.items()}
    copy_constant = 5*(F(44,3)*root_profit+F(13,5)*cap)
    copy_menu = {n: v+copy_constant for n,v in copy_menu.items()}
    def packed(values):
        return {n: {"exact": str(v), "decimal": float(v)} for n, v in sorted(values.items(), key=lambda z: z[1])}
    return {
        "status": "Exact evaluation of serialized decimal LP coordinates only; no game or primal-feasibility claim",
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "positive_support": support,
        "serialized_shared_K": str(cap),
        "root_profit": str(root_profit),
        "optimal_multiplicity_mass": {str(d): str(v) for d, v in ds.items()},
        "slacks": packed(slacks),
        "menu_size_cap_slacks": packed(menu_caps),
        "copy_m_menu_slacks": packed(copy_menu),
    }


def follow(instance, actions, history):
    history = tuple(history)
    while len(history) < instance.players:
        history += (actions[history],)
    return history


def finite_replay():
    # These are regression inputs for the universal row proof, not a size scan.
    coverages = [([], [], []), ([], [0], [0]),
                 ([0, 1], [1, 2], [2, 3], [0, 3]),
                 ([0, 1, 2, 3, 4], [5], [6], [7], [8])]
    results = []
    for coverage in coverages:
        ins = Instance.from_topic_sets(coverage, 5)
        solver = ExactSPESolver(ins)
        cert = solver.certificate(action_selector=lambda h, aa: aa[len(h) % len(aa)])
        verified = verify_certificate(ins, cert)
        verified.assert_valid()
        path = follow(ins, cert.actions, ())
        a, b, c, d, e = path
        tuples = list(combinations_with_replacement(range(ins.topic_count), 5))
        def cov(tt):
            return ins.welfare(ins.counts(tt, terminal=True))
        optimal = max(tuples, key=cov)
        prefixes = {"S": (a,), "AB": (a,b), "AE": (a,e)}
        indexed = {f: [follow(ins, cert.actions, pre+(t,)) for t in optimal]
                   for f, pre in prefixes.items()}
        menus = {}
        for f, pre in prefixes.items():
            for pos in range(len(pre)+1, 5):
                menus[f"{f}:{pos}"] = [tt[pos] for tt in indexed[f]]
        fixed_paths = {"actual": path,
                       "second": follow(ins, cert.actions, (a,e)),
                       "third": follow(ins, cert.actions, (a,b,e))}
        for f, tt in fixed_paths.items():
            menus[f"L:{f}"] = [follow(ins, cert.actions, tt[:3]+(t,))[-1] for t in optimal]
        minimum = None
        comparisons = 0
        for f, pre in prefixes.items():
            mover = len(pre)+1
            current = sum((ins.player_payoffs(tt)[mover] for tt in indexed[f]), F(0))
            for name, qs in menus.items():
                floor = F(0)
                for j, t in enumerate(optimal):
                    h = pre+(t,)
                    realized = ins.player_payoffs(indexed[f][j])[mover]
                    for q in qs:
                        deviating = follow(ins, cert.actions, h+(q,))
                        deviation_profit = ins.player_payoffs(deviating)[mover]
                        assert realized >= deviation_profit
                        local = F(0)
                        for customer in ins.customers:
                            if q in customer.topics:
                                p = sum(z in customer.topics for z in h)
                                local += F(customer.multiplicity, p+5-len(h))
                        assert deviation_profit >= local
                        floor += local
                        comparisons += 1
                slack = 5*current-floor
                assert slack >= 0
                minimum = slack if minimum is None else min(minimum, slack)
        results.append({"topics": ins.topic_count, "customers": ins.customer_count,
                        "verified_complete_histories": verified.checked_histories,
                        "verified_deviations": verified.checked_deviations,
                        "menu_action_comparisons": comparisons, "minimum_slack": str(minimum)})
    return results


if __name__ == "__main__":
    report = {"claim_status": "Author complete necessary-condition proof; no half-bound claim",
              "old_projection": old_projection(), "complete_SPE_regressions": finite_replay()}
    target = HERE / "audit_cross_first_reply.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"target": str(target.relative_to(ROOT)),
                      "negative_diagnostic_rows": {n: v for n, v in report["old_projection"]["slacks"].items() if v["decimal"] < 0},
                      "replays": report["complete_SPE_regressions"]}, ensure_ascii=False, indent=2))
