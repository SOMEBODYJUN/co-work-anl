#!/usr/bin/env python3
"""Exact recovery from the sole returned support; no optimizer or old solver import."""
from fractions import Fraction as F
from math import isfinite, lcm
import json
import sys

sys.dont_write_bytecode = True
from contract import HERE, N, M, Q, digest, load_discovery, require, status, write_new


def main():
    if not (HERE / "single_lp_consumed.json").is_file():
        print(json.dumps(status(), indent=2))
        return 2
    context = {"stage": "load_released_discovery", "optimizer_calls_in_recovery": 0}
    try:
        bundle, discovery = load_discovery()
        import sympy as sp

        rational = lambda value: sp.Rational(value.numerator, value.denominator)
        fraction = lambda value: F(int(value.p), int(value.q))
        A, b, E, h = (bundle[key] for key in ["A", "b", "E", "h"])
        cost = [bundle["cost"].get(j, F(0)) for j in range(N)]
        dot = lambda row, vector: sum((value * vector[j] for j, value in row.items()), F(0))
        xnum = discovery["x"]
        marginal = discovery["inequality_marginals_scaled"]
        slacknum = discovery["inequality_residual_scaled"]
        require(len(xnum) == N and len(marginal) == len(slacknum) == M,
                "Incomplete sole numerical record")
        require(all(isfinite(value) for value in xnum + marginal + slacknum),
                "Nonfinite numerical record; cannot recover exact support")
        # Retain every strictly positive returned primal value, including tiny values.
        support = [j for j, value in enumerate(xnum) if value > 0]
        dual_candidates = [i for i, value in enumerate(marginal) if value < 0]
        numeric_tight = sorted(set(dual_candidates) |
                               {i for i, value in enumerate(slacknum) if abs(value) < 1e-10})
        context.update(
            input_sha256=bundle["release"]["input_sha256"],
            returned_positive_columns=support,
            returned_positive_scaled_dual_rows=dual_candidates,
            returned_numeric_tight_rows=numeric_tight,
            support_policy="All strictly positive returned values, not a new model restriction.",
        )

        def primal_matrix(indices):
            return sp.Matrix(
                [[rational(row.get(j, F(0))) for j in support] for row in E]
                + [[rational(A[i].get(j, F(0))) for j in support] for i in indices]
            )

        tight = list(dual_candidates)
        context["stage"] = "exact_primal_linear_algebra"
        pm = primal_matrix(tight)
        if pm.rank() < len(support):
            tight = numeric_tight
            pm = primal_matrix(tight)
        primal_rank = int(pm.rank())
        context.update(primal_rank=primal_rank, primal_unknowns=len(support),
                       primal_equation_raw_indices=tight)
        pb = sp.Matrix([rational(value) for value in h]
                       + [rational(b[i]) for i in tight])
        solutions = sp.linsolve((pm, pb))
        require(len(solutions) == 1, "Returned support does not solve the exact active equations")
        primal_values = next(iter(solutions))
        require(all(value.is_Rational and not value.free_symbols for value in primal_values),
                "Exact primal is not uniquely determined on the returned support")
        z = [F(0)] * N
        for j, value in zip(support, primal_values):
            z[j] = fraction(value)
        slacks = [dot(row, z) - rhs for row, rhs in zip(A, b)]
        eqres = [dot(row, z) - rhs for row, rhs in zip(E, h)]
        require(all(value >= 0 for value in z), "Recovered primal has a negative coordinate")
        require(all(value >= 0 for value in slacks), "Recovered primal fails a raw inequality")
        require(eqres == [F(0)] * Q, "Recovered primal fails an equality")
        objective = sum((value * mass for value, mass in zip(cost, z)), F(0))
        context["stage"] = "exact_raw_dual_linear_algebra"
        dm = sp.Matrix([
            [rational(A[i].get(j, F(0))) for i in dual_candidates]
            + [rational(row.get(j, F(0))) for row in E]
            for j in support
        ])
        db = sp.Matrix([rational(cost[j]) for j in support])
        dual_rank = int(dm.rank())
        context.update(dual_rank=dual_rank, dual_unknowns=len(dual_candidates) + Q)
        solutions = sp.linsolve((dm, db))
        require(len(solutions) == 1, "Returned dual support does not admit exact stationarity")
        dual_values = next(iter(solutions))
        require(all(value.is_Rational and not value.free_symbols for value in dual_values),
                "Exact dual is not uniquely determined on the returned support")
        y = [F(0)] * M
        for i, value in zip(dual_candidates, dual_values[:len(dual_candidates)]):
            y[i] = fraction(value)
        eta = [fraction(value) for value in dual_values[len(dual_candidates):]]
        require(len(eta) == Q and all(value >= 0 for value in y), "Invalid exact raw payments")
        residual = list(cost)
        for weight, row in zip(y, A):
            if weight:
                for j, value in row.items():
                    residual[j] -= weight * value
        for weight, row in zip(eta, E):
            for j, value in row.items():
                residual[j] -= weight * value
        require(all(value >= 0 for value in residual), "A full raw-column dual residual is negative")
        row_rhs_payment = sum((weight * rhs for weight, rhs in zip(y, b)), F(0))
        eq_rhs_payment = sum((weight * rhs for weight, rhs in zip(eta, h)), F(0))
        dual_objective = row_rhs_payment + eq_rhs_payment
        require(dual_objective == objective, "Exact primal-dual objective gap")
        require(all(weight * slack == 0 for weight, slack in zip(y, slacks)),
                "Raw-row complementarity failure")
        require(all(value * mass == 0 for value, mass in zip(residual, z)),
                "Column complementarity failure")
        context["stage"] = "write_verified_exact_certificate"
        positive = [i for i, value in enumerate(y) if value > 0]
        exact_support = [j for j, value in enumerate(z) if value > 0]
        divisor = bundle["divisors"]
        rows = bundle["rows"]
        common_denominator = lcm(*(value.denominator for value in z))
        scaling_checks = [{
            "raw_index": i, "name": rows[i]["name"], "positive_divisor": str(divisor[i]),
            "exact_raw_weight": str(y[i]), "exact_scaled_weight": str(y[i] * divisor[i]),
            "returned_scaled_weight": -marginal[i],
            "scaled_weight_numeric_error": float(y[i] * divisor[i]) + marginal[i],
        } for i in range(M)]
        certificate = {
            "schema": "visible_maximum_joint_exact_certificate_v4",
            "status": "PASS_EXACT_PRIMAL_DUAL_FULL1586",
            "input_sha256": bundle["release"]["input_sha256"],
            "discovery_sha256": digest(HERE / "discovery_output.json"),
            "optimizer_calls": 1, "optimizer_calls_in_recovery": 0,
            "variables": N, "raw_inequalities": M, "equality_count": Q,
            "objective": str(objective), "objective_decimal": float(objective),
            "half_gap": str(F(1, 2) - objective),
            "primal": [str(value) for value in z], "K": str(z[512]),
            "primal_support": exact_support, "common_denominator": str(common_denominator),
            "integer_scaled_primal": {
                str(j): str(z[j] * common_denominator) for j in exact_support
            },
            "dual": {
                "convention": "Raw A z>=b; E z=h; y>=0, eta free; r=c-A^T y-E^T eta>=0.",
                "raw_row_weights": [str(value) for value in y],
                "equality_multipliers": [str(value) for value in eta],
                "equality_names": [row["name"] for row in bundle["data"]["equalities"]],
                "objective": str(dual_objective),
                "affine_inequality_rhs_payment": str(row_rhs_payment),
                "equality_rhs_payment": str(eq_rhs_payment),
                "nonnegative_column_residual": [str(value) for value in residual],
                "positive_raw_indices": positive,
                "positive_raw_rows": [{
                    "index": i, "name": rows[i]["name"], "family": rows[i]["family"],
                    "weight": str(y[i]), "rhs": str(b[i]),
                    "prepared_positive_divisor": str(divisor[i]),
                    "source_metadata": {key: value for key, value in rows[i].items()
                                        if key not in {"a", "rhs"}},
                } for i in positive],
            },
            "raw_row_slacks": [str(value) for value in slacks],
            "equality_residuals": [str(value) for value in eqres],
            "active_raw_indices": [i for i, value in enumerate(slacks) if value == 0],
            "recovery": dict(
                context, method="Exact symbolic linear algebra on one returned support; no optimizer.",
                max_primal_numeric_error=max(abs(float(z[j]) - xnum[j]) for j in range(N)),
                scaled_to_raw_rule="raw_weight = -SciPy_scaled_marginal / prepared_positive_divisor",
                all_raw_weight_scaling_checks=scaling_checks,
            ),
            "scope_boundary": (
                "Exact necessary-cone optimality. The primal is not a complete ordered pure "
                "SPE realization; source validity is separately pinned and reviewed. "
                "The original six-player half problem remains OPEN unless separately proved."
            ),
        }
        write_new(HERE / "exact_certificate.json", certificate)
        write_new(HERE / "all1586_raw_row_checks.json", [{
            "raw_index": i, "name": rows[i]["name"], "family": rows[i]["family"],
            "rhs": str(b[i]), "primal_slack": str(slacks[i]), "raw_dual_weight": str(y[i]),
            "complementarity": str(slacks[i] * y[i]),
        } for i in range(M)])
        write_new(HERE / "all513_column_checks.json", [{
            "column": j, "bits_or_K": format(j, "09b") if j < 512 else "K",
            "primal": str(z[j]), "objective_coefficient": str(cost[j]),
            "dual_residual": str(residual[j]), "complementarity": str(z[j] * residual[j]),
        } for j in range(N)])
        summary = {
            "status": certificate["status"], "input_sha256": certificate["input_sha256"],
            "objective": str(objective), "objective_decimal": float(objective), "K": str(z[512]),
            "all_raw_rows_checked": M, "all_columns_checked": N, "equalities_checked": Q,
            "primal_rank": primal_rank, "dual_rank": dual_rank,
            "positive_primal_columns": exact_support, "positive_raw_indices": positive,
            "positive_raw_rows": certificate["dual"]["positive_raw_rows"],
            "zero_dual_residual_columns": [j for j, value in enumerate(residual) if value == 0],
            "equality_multipliers": certificate["dual"]["equality_multipliers"],
            "affine_rhs_payment": str(row_rhs_payment), "equality_rhs_payment": str(eq_rhs_payment),
            "optimizer_calls": 1, "new_optimizer_calls_in_recovery": 0,
        }
        write_new(HERE / "exact_recovery_summary.json", summary)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    except Exception as error:
        obstacle = dict(
            context, status="EXACT_RECOVERY_STOPPED_NO_RETRY", error_type=type(error).__name__,
            error=str(error),
            policy="Keep the sole numerical output; report this exact remaining obstacle. No new optimizer.",
        )
        if not (HERE / "recovery_obstacle.json").exists():
            write_new(HERE / "recovery_obstacle.json", obstacle)
        print(json.dumps(obstacle, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(main())
