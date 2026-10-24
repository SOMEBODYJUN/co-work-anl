"""One targeted mixed-SC payment attack in the known six-topic policy cone.

The query is fixed at (e2+e5)/2. Unlike the prior all-p attacks, this probe
imposes the complete SC support conditions g2=g5 >= every gA. No scan.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd, lcm
from functools import reduce
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

M, K = 3, 6
TYPES = range(1, 1 << K)
P = (F(0), F(0), F(1, 2), F(0), F(0), F(1, 2))


def action(h):
    if not h:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(3) if h[1] < 3 else range(3, 6)
    return next(a for a in group if a not in h)


def finish(h):
    while len(h) < M:
        h += (action(h),)
    return h


def client_pay(mask, z, i):
    if not mask >> z[i] & 1:
        return F(0)
    return F(1, sum(mask >> a & 1 for a in z))


def dot(row, weights):
    return sum((a * b for a, b in zip(row, weights)), F(0))


def exact_dual_from_active_set(objective, inequalities, sc_eq, raw_lam, raw_gamma):
    """Reconstruct exact basic equalities, rather than round each multiplier."""
    active = [i for i, v in enumerate(raw_lam) if v > 1e-8]
    raw = [raw_lam[i] for i in active] + [raw_gamma]
    columns = [[row[j] for row in [inequalities[i] for i in active]] + [sc_eq[j]]
               for j in range(len(objective))]
    tight = [j for j, row in enumerate(columns)
             if abs(float(-objective[j]) - sum(float(a) * v for a, v in zip(row, raw))) < 1e-7]
    matrix = [columns[j] + [-objective[j]] for j in tight]
    pivot_cols, rank = [], 0
    n = len(raw)
    for col in range(n):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        value = matrix[rank][col]
        matrix[rank] = [v / value for v in matrix[rank]]
        for i in range(len(matrix)):
            if i != rank and matrix[i][col]:
                value = matrix[i][col]
                matrix[i] = [a - value * b for a, b in zip(matrix[i], matrix[rank])]
        pivot_cols.append(col)
        rank += 1
    assert all(any(row[j] for j in range(n)) or row[-1] == 0 for row in matrix)
    solution = [F(v).limit_denominator(10 ** 6) for v in raw]
    free = [j for j in range(n) if j not in pivot_cols]
    for row, col in zip(matrix, pivot_cols):
        solution[col] = row[-1] - sum((row[j] * solution[j] for j in free), F(0))
    lam = [F(0)] * len(inequalities)
    for i, value in zip(active, solution[:-1]):
        lam[i] = value
    return lam, solution[-1], rank, len(free)


def main():
    actual = finish(())
    ic = []
    ic_labels = []
    for i in range(M):
        for h in product(range(K), repeat=i):
            y = finish(h)
            for a in range(K):
                z = finish(h + (a,))
                ic.append([client_pay(t, y, i) - client_pay(t, z, i)
                           for t in TYPES])
                ic_labels.append({"history": list(h), "deviation": a})
    q = [F(0)] * K
    for i in range(M):
        for a, pa in enumerate(P):
            z = finish(actual[:i] + (a,))
            for j in range(M):
                if j != i:
                    q[z[j]] += pa / (M * (M - 1))
    mu = {t: (M - 1) * sum(q[a] for a in range(K) if t >> a & 1)
          for t in TYPES}
    gs = [[F(int(t >> a & 1), 1) / (1 + mu[t]) for t in TYPES]
          for a in range(K)]
    welfare = [F(any(t >> a & 1 for a in actual)) for t in TYPES]
    objective = [M * gs[2][j] - welfare[j] for j in range(len(welfare))]
    sc_ineq = [[gs[2][j] - gs[a][j] for j in range(len(welfare))]
               for a in range(K)]
    sc_eq = [gs[2][j] - gs[5][j] for j in range(len(welfare))]
    inequalities = ic + sc_ineq
    result = linprog(-np.array(objective, dtype=float),
                     A_ub=-np.array(inequalities, dtype=float),
                     b_ub=np.zeros(len(inequalities)),
                     A_eq=np.array([[1.] * len(welfare), list(map(float, sc_eq))]),
                     b_eq=[1., 0.], bounds=(0, None), method="highs")
    report = {
        "candidate": "m G(p) <= W for self-consistent p",
        "query": list(map(str, P)),
        "policy": "known six-topic group policy; complete ordered histories",
        "scope": "one fixed query and one fixed policy cone; no general conclusion from negative result",
        "solver_status": result.message,
        "ic_rows_including_self": len(ic),
        "sc_constraints": "g2=g5 and g2>=gA for all six actions",
    }
    if result.success:
        report["numerical_max_gap_per_customer"] = -result.fun
        weights = [F(float(x)).limit_denominator(10 ** 7) if x > 1e-9 else F(0)
                   for x in result.x]
        den = lcm(*(v.denominator for v in weights))
        counts = [int(v * den) for v in weights]
        common = reduce(gcd, counts)
        counts = [v // common for v in counts]
        report.update({
            "proposed_counts": {str(t): n for t, n in zip(TYPES, counts) if n},
            "unit_clients": sum(counts),
            "exact_ic_minimum": str(min(dot(row, counts) for row in ic)),
            "exact_sc_equality_gap": str(dot(sc_eq, counts)),
            "exact_sc_bestresponse_gaps": [str(dot(row, counts)) for row in sc_ineq],
            "exact_payment_gap": str(dot(objective, counts)),
            "exact_actual_welfare": str(dot(welfare, counts)),
            "exact_pooled_values": [str(dot(row, counts)) for row in gs],
        })
        report["exact_SC_SPE_payment_counterexample"] = (
            min(dot(row, counts) for row in ic) >= 0 and dot(sc_eq, counts) == 0
            and min(dot(row, counts) for row in sc_ineq) >= 0
            and dot(objective, counts) > 0)
        # Exact reconstruction of this solver's finite-cone dual, if available.
        lam, gamma, rank, free = exact_dual_from_active_set(
            objective, inequalities, sc_eq,
            [-float(v) for v in result.ineqlin.marginals],
            float(result.eqlin.marginals[1]))
        nu = F(float(result.eqlin.marginals[0])).limit_denominator(10 ** 7)
        residual = [-objective[j] - nu - gamma * sc_eq[j]
                    - sum((v * row[j] for v, row in zip(lam, inequalities)), F(0))
                    for j in range(len(welfare))]
        report["reconstructed_dual"] = {
            "identity": "-payment_gap = sum lambda_r*row_r + gamma*(g2-g5) + nu*total_mass + nonnegative_type_residual",
            "lambda_nonnegative": min(lam) >= 0,
            "normalization_coefficient": str(nu),
            "SC_equality_coefficient": str(gamma),
            "minimum_exact_type_residual": str(min(residual)),
            "exact_dual_verified": min(lam) >= 0 and min(residual) >= 0 and nu == 0,
            "exact_active_system_rank": rank,
            "free_active_multipliers": free,
            "IC_terms": [{**label, "coefficient": str(v)}
                         for label, v in zip(ic_labels, lam[:len(ic)]) if v],
            "SC_terms": [{"challenger": a, "coefficient": str(v)}
                         for a, v in enumerate(lam[len(ic):]) if v],
            "type_residuals": {str(t): str(v) for t, v in zip(TYPES, residual) if v},
        }
    path = Path(__file__).with_name("mixed_sc_fixed_query_probe.json")
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
