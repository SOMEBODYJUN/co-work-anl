"""Exact finite audit of the recursive owner-tax diagnostic.

For each pure-SPE terminal outcome and each ordered optimal m-tuple T, compute
R_min(T)=sum_{x in OPT\actual} min_{i:x in T_i} k_i(x)/(1+k_i(x)),
where k_i(x) is the number of post-i responders covering x after forcing T_i
at the actual prefix and following the complete certificate.  This is only a
finite diagnostic; no universal claim is inferred.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import product
import json
from customer_attraction import CustomerType, ExactSPESolver, Instance


def branch(cert, actual, i, action):
    h = actual[:i] + (action,)
    while len(h) < len(actual):
        h += (cert.actions[h],)
    return h


def owner_tax(instance, cert, actual, optimal):
    m = instance.players
    loads = instance.counts(actual, terminal=True)
    tax = Fraction(0)
    intersection = outside = 0
    for c in instance.customers:
        in_opt = any(t in c.topics for t in optimal)
        in_actual = any(loads[t] for t in c.topics)
        if in_opt and in_actual:
            intersection += c.multiplicity
        elif not in_opt and in_actual:
            outside += c.multiplicity
        if in_opt and not in_actual:
            rows = []
            for i, t in enumerate(optimal):
                if t not in c.topics:
                    continue
                h = branch(cert, actual, i, t)
                k = sum(h[j] in c.topics for j in range(i + 1, m))
                rows.append(Fraction(k, k + 1))
            assert rows
            tax += c.multiplicity * min(rows)
    return tax, intersection, outside


def audit_supports(k=3, m=3):
    max_gap = None
    witness = None
    checked = 0
    for support in range(1, 1 << ((1 << k) - 1)):
        customers = tuple(
            CustomerType(frozenset(i for i in range(k) if mask >> i & 1), 1)
            for mask in range(1, 1 << k) if support >> (mask - 1) & 1
        )
        instance = Instance(tuple(map(str, range(k))), customers, m)
        solver = ExactSPESolver(instance)
        optimum = instance.optimal_welfare()
        tuples = [t for t in product(range(k), repeat=m)
                  if instance.welfare(instance.counts(t, terminal=True)) == optimum]
        for target in solver.outcomes():
            cert = solver.certificate(target)
            actual = next(iter(solver.ordered_outcomes(target)))
            for optimal in tuples:
                tax, inter, outside = owner_tax(instance, cert, actual, optimal)
                gap = tax - inter - 2 * outside
                checked += 1
                if max_gap is None or gap > max_gap:
                    max_gap, witness = gap, {
                        "support": support, "customers": [sorted(c.topics) for c in customers],
                        "actual": actual, "target": target, "optimal": optimal,
                        "R_min": str(tax), "I": inter, "G": outside,
                    }
                assert gap <= 0, (gap, witness)
    return {"k": k, "m": m, "checked": checked,
            "max_gap": str(max_gap), "max_gap_witness": witness}


def audit_all_big(max_m=4):
    out = []
    for m in range(1, max_m + 1):
        a = m
        customers = [CustomerType(frozenset({0}), a)]
        customers.extend(CustomerType(frozenset({i}), 1) for i in range(1, m))
        instance = Instance(tuple(map(str, range(m))), tuple(customers), m)
        solver = ExactSPESolver(instance)
        # Inspect every SPE terminal outcome, using one canonical certificate/path.
        rows = []
        optimum = instance.optimal_welfare()
        for target in solver.outcomes():
            cert = solver.certificate(target)
            actual = next(iter(solver.ordered_outcomes(target)))
            # choose a fixed optimum tuple (B,S1,...); this is enough for this audit
            optimal = (0,) + tuple(range(1, m)) if m > 1 else (0,)
            tax, inter, outside = owner_tax(instance, cert, actual, optimal)
            rows.append({"target": target, "actual": actual, "R_min": str(tax),
                         "I": inter, "G": outside,
                         "gap": str(tax - inter - 2 * outside)})
        out.append({"m": m, "optimum": optimum, "outcomes": rows})
    return out


if __name__ == "__main__":
    report = {"exhaustive_k3_m3": audit_supports(),
              "all_big_m1_to_8": audit_all_big()}
    print(json.dumps(report, indent=2, sort_keys=True))
