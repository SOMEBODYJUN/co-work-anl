#!/usr/bin/env python3
"""Decode a supplied equal-coverage CONFIG point by one existing slot call.

No CONFIG finder, LP solver, or matching implementation is provided here.
Default dependency: rounding_and_gap.py in this script's directory.
Scratch usage: --baseline /absolute/path/to/rounding_and_gap.py --audit
Input usage: --baseline ... --input supplied_point.json

JSON input keys are p, target, configs, delta, k. Each configs[i] is a list
of [nonnegative rational weight, list of original zero-based job indices].
Use integers/rational strings, never floats or bools, for exact numbers.
"""

from fractions import Fraction as F
from pathlib import Path
from types import SimpleNamespace
import argparse
import copy
import hashlib
import importlib.util
import json
import sys
import platform


class CertificateError(ValueError):
    """The supplied matrix, parameters, or explicit CONFIG point is invalid."""


def load_baseline(path=None):
    path = Path(path) if path is not None else Path(__file__).with_name("rounding_and_gap.py")
    if not path.is_file():
        raise FileNotFoundError("rounding_and_gap.py not found; supply --baseline /absolute/path")
    spec = importlib.util.spec_from_file_location("_tiny_work_classical_round_slots", path)
    baseline = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    try:
        # Reading a dependency must not create __pycache__ in the source repo.
        sys.dont_write_bytecode = True
        spec.loader.exec_module(baseline)
    finally:
        sys.dont_write_bytecode = previous
    return baseline, path


def _exact(value, baseline, label):
    try:
        return baseline.rational(value)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError) as exc:
        raise CertificateError(f"Invalid exact rational for {label}: {exc}") from exc


def _power_at_least(base, exponent, threshold):
    """Compare base**exponent to threshold, saturating before large powers.

    This never materializes K**(K-1). All running products have at most twice
    the bit length of the comparison threshold; iterations are O(log K).
    """
    if threshold <= 1:
        return True, 0
    if exponent == 0:
        return False, 0
    if base >= threshold:
        return True, 0
    result, factor, steps = 1, base, 0
    while exponent:
        steps += 1
        if exponent & 1:
            result = min(threshold, result * factor)
            if result == threshold:
                return True, steps
        exponent >>= 1
        if exponent:
            factor = min(threshold, factor * factor)
    return result >= threshold, steps


def _alpha_bound_check(actual, capacity, k):
    """Check actual <= alpha_k*capacity without constructing alpha_k."""
    if capacity < 0:
        return False, {"mode": "negative_capacity"}
    if k == 1:
        return actual <= capacity, {"mode": "alpha_1=1"}
    if k == 2:
        return 2 * actual <= 3 * capacity, {"mode": "alpha_2=3/2"}
    if k == 3:
        return 6 * actual <= 11 * capacity, {"mode": "alpha_3=11/6"}
    if not capacity:
        return actual <= 0, {"mode": "zero_capacity; alpha_not_constructed"}
    slack = 2 * capacity - actual
    if slack <= 0:
        return False, {"mode": "symbolic_alpha; nonpositive_slack"}
    numerator = capacity.numerator * slack.denominator
    denominator = capacity.denominator * slack.numerator
    threshold = (numerator + denominator - 1) // denominator
    valid, steps = _power_at_least(k, k - 1, threshold)
    return valid, {"mode": "symbolic_alpha; capped_power_comparison", "threshold_bits": threshold.bit_length(), "power_steps": steps}


def decode(p, target, configs, delta, k, *, baseline=None):
    """Return a complete actual assignment for a validated explicit point.

    The same original job is one column across all 2m virtual rows. Global
    zero-edge jobs are assigned first and removed from every configuration.
    The input certificate is validated before this deletion, so a bad zero-
    job coverage or illegal original column cannot be hidden by preprocessing.
    """
    # Exact rational-string API calls have the same unbounded encoding domain.
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)
    if baseline is None:
        baseline, _ = load_baseline()
    try:
        p = baseline.matrix(p)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError) as exc:
        raise CertificateError(f"Invalid processing matrix: {exc}") from exc
    target = _exact(target, baseline, "target")
    delta = _exact(delta, baseline, "delta")
    if target < 0 or not 0 <= delta <= 1:
        raise CertificateError("Require target>=0 and 0<=delta<=1")
    if type(k) is not int or k < 1:
        raise CertificateError("k must be an integer >=1, not bool")
    m, n = len(p), len(p[0])
    if not isinstance(configs, (list, tuple)) or len(configs) != m:
        raise CertificateError("CONFIG row count differs from machine count")
    parsed, coverage = [], [F(0) for _ in range(n)]
    for i, choices in enumerate(configs):
        if not isinstance(choices, (list, tuple)):
            raise CertificateError(f"CONFIG row {i} is not an explicit list")
        atoms, mass = [], F(0)
        for column, atom in enumerate(choices):
            if not isinstance(atom, (list, tuple)) or len(atom) != 2:
                raise CertificateError(f"CONFIG atom {i},{column} must be [weight,jobs]")
            weight, jobs = atom
            weight = _exact(weight, baseline, f"weight[{i},{column}]")
            if weight < 0:
                raise CertificateError(f"Negative CONFIG weight at {i},{column}")
            if not isinstance(jobs, (list, tuple)):
                raise CertificateError(f"CONFIG jobs at {i},{column} must be a list")
            if any(type(j) is not int or not 0 <= j < n for j in jobs):
                raise CertificateError(f"Invalid original job index at {i},{column}")
            if len(set(jobs)) != len(jobs):
                raise CertificateError(f"Duplicate original job in CONFIG atom {i},{column}")
            if any(p[i][j] is None for j in jobs):
                raise CertificateError(f"Forbidden edge in CONFIG atom {i},{column}")
            if sum((p[i][j] for j in jobs), F(0)) > target:
                raise CertificateError(f"CONFIG load exceeds target at {i},{column}")
            mass += weight
            for j in jobs:
                coverage[j] += weight
            atoms.append((weight, tuple(jobs)))
        if mass != 1:
            raise CertificateError(f"CONFIG probability mass is not one on row {i}")
        parsed.append(atoms)
    if any(value != 1 for value in coverage):
        raise CertificateError("Original job coverage is not exactly one")

    assignment, zero_jobs = [None] * n, []
    for j in range(n):
        zeros = [i for i in range(m) if p[i][j] == 0]
        if zeros:
            assignment[j] = zeros[0]
            zero_jobs.append(j)
    remaining = [j for j in range(n) if assignment[j] is None]
    reduced_index = {j: q for q, j in enumerate(remaining)}
    nr = len(remaining)
    virtual_p = [[None] * nr for _ in range(2 * m)]
    virtual_x = [[F(0)] * nr for _ in range(2 * m)]
    stats = []
    threshold = delta * target
    for i, atoms in enumerate(parsed):
        for j in remaining:
            if p[i][j] is not None:
                role = 1 if p[i][j] <= threshold else 0
                virtual_p[2 * i + role][reduced_index[j]] = p[i][j]
        tiny_values, tiny_mean, big_max = [], F(0), 0
        for weight, jobs in atoms:
            kept = [j for j in jobs if j in reduced_index]
            big = [j for j in kept if p[i][j] > threshold]
            tiny = [j for j in kept if p[i][j] <= threshold]
            tiny_work = sum((p[i][j] for j in tiny), F(0))
            if weight > 0:
                if len(big) > k:
                    raise CertificateError(f"Positive CONFIG atom exceeds big-job k on row {i}")
                big_max = max(big_max, len(big))
                tiny_values.append(tiny_work)
                tiny_mean += weight * tiny_work
            for j in kept:
                role = 1 if p[i][j] <= threshold else 0
                virtual_x[2 * i + role][reduced_index[j]] += weight
        # Row mass=1 guarantees at least one strictly positive atom.
        r = min(tiny_values)
        b = max((p[i][j] for j in remaining if p[i][j] is not None and p[i][j] <= threshold and virtual_x[2 * i + 1][reduced_index[j]] > 0), default=F(0))
        stats.append({"r": r, "s": tiny_mean, "b": b, "big_config_count_max": big_max, "big_capacity": target - r})

    # One global matching: a job cannot be independently selected in its two roles.
    virtual_assignment, virtual_loads = baseline.round_slots(virtual_p, virtual_x, target)
    for q, virtual_machine in enumerate(virtual_assignment):
        assignment[remaining[q]] = virtual_machine // 2
    actual_loads = baseline.loads(p, assignment)
    for i, stat in enumerate(stats):
        big_load, tiny_load = virtual_loads[2 * i:2 * i + 2]
        big_fractional_load = sum(((virtual_p[2 * i][q] or F(0)) * virtual_x[2 * i][q] for q in range(nr)), F(0))
        tiny_fractional_load = sum(((virtual_p[2 * i + 1][q] or F(0)) * virtual_x[2 * i + 1][q] for q in range(nr)), F(0))
        if big_fractional_load > stat["big_capacity"] or tiny_fractional_load != stat["s"]:
            raise AssertionError(f"Virtual-row projection is inconsistent on row {i}")
        big_valid, alpha_check = _alpha_bound_check(big_load, stat["big_capacity"], k)
        tiny_valid = tiny_load <= stat["s"] + stat["b"]
        if not big_valid or not tiny_valid or actual_loads[i] != big_load + tiny_load:
            raise AssertionError(f"Supplied-point bound failed after the existing slot rounding on row {i}")
        stat.update({"big_fractional_load": big_fractional_load, "tiny_fractional_load": tiny_fractional_load, "big_load": big_load, "tiny_load": tiny_load, "actual_load": actual_loads[i], "tiny_bound_verified": tiny_valid, "big_bound_verified": big_valid, "alpha_check": alpha_check})
    return {"assignment": assignment, "loads": actual_loads, "zero_jobs": zero_jobs, "remaining_jobs": remaining, "virtual_rows": 2 * m, "slot_calls": 1, "k_bits": k.bit_length(), "rows": stats}


def _json_default(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(f"Not JSON serializable: {type(value).__name__}")


def audit(baseline):
    fixtures = []
    calls = []

    def counted_round_slots(p, x, target):
        role_support = [[i % 2 for i in range(len(p)) if x[i][j] > 0] for j in range(len(p[0]))]
        calls.append({"rows": len(p), "jobs": len(p[0]), "mixed_role_columns": [j for j, roles in enumerate(role_support) if 0 in roles and 1 in roles]})
        return baseline.round_slots(p, x, target)

    counted = SimpleNamespace(matrix=baseline.matrix, rational=baseline.rational, loads=baseline.loads, round_slots=counted_round_slots)

    def run(name, p, target, configs, delta, k):
        before = len(calls)
        result = decode(p, target, configs, delta, k, baseline=counted)
        assert len(calls) - before == 1
        assert len(result["assignment"]) == len(p[0])
        fixtures.append({"name": name, "status": "passed", "slot_call": calls[-1], "result": result})
        return result

    mixed = run("mixed_roles_one_original_job_column", [["3/4", "1/4", "1/4"], ["1/4", "3/4", "1/4"]], 1,
                [[["1/2", [0, 1]], ["1/2", [2]]], [["1/2", [0, 1]], ["1/2", [2]]]], "1/4", 1)
    assert all(row["r"] == F(1, 4) for row in mixed["rows"])
    assert calls[-1]["mixed_role_columns"] == [0, 1]

    tiny = run("tiny_count_exceeds_k_and_zero_big_capacity", [[F(1, 14)] * 14], 1, [[[1, list(range(14))]]], F(1, 14), 1)
    assert tiny["rows"][0]["big_capacity"] == 0 and tiny["rows"][0]["big_config_count_max"] == 0

    zero_p = [[0, "2/5"], ["3/5", "2/5"]]
    zero_y = [[["1/2", [0, 1]], ["1/2", []]], [["1/2", [0, 1]], ["1/2", []]]]
    zero = run("global_zero_deletion_precedes_big_cardinality", zero_p, 1, zero_y, 0, 1)
    assert zero["zero_jobs"] == [0] and zero["assignment"][0] == 0

    empty = run("empty_jobs_and_zero_target", [[], []], 0, [[[1, []]], [[1, []]]], 1, 1)
    assert empty["assignment"] == [] and empty["loads"] == [0, 0]

    huge_y = [[["1/2", [0]], ["1/2", [1, 2]]] for _ in range(2)]
    huge = run("binary_huge_k_without_alpha_denominator", [[1, "1/2", "1/2"]] * 2, 1, huge_y, 0, 1 << 8192)
    assert huge["k_bits"] == 8193 and huge["rows"][0]["alpha_check"]["power_steps"] == 0
    assert huge["rows"][0]["big_load"] == F(3, 2)

    d = (1 << 257) + 1
    large = run("large_denominators_k2", [[1, F(d - 1, 2 * d), F(d + 1, 2 * d)]] * 2, 1, huge_y, 0, 2)
    assert all(row["alpha_check"]["mode"] == "alpha_2=3/2" for row in large["rows"])
    assert large["rows"][0]["big_load"] > large["rows"][0]["big_capacity"]

    positive_r = run("positive_r_k3_ignore_zero_weight_empty_atom", [["5/16", "5/16", "5/16", "1/16"]], 1,
                     [[[1, [0, 1, 2, 3]], [0, []]]], "1/16", 3)
    assert positive_r["rows"][0]["r"] == F(1, 16) and positive_r["rows"][0]["big_config_count_max"] == 3

    rejected = []
    base_case = {"p": [["1/2"]], "target": 1, "configs": [[[1, [0]]]], "delta": 0, "k": 1}

    def reject(name, **updates):
        case = copy.deepcopy(base_case)
        case.update(updates)
        before = len(calls)
        try:
            decode(**case, baseline=counted)
        except CertificateError as exc:
            assert len(calls) == before
            rejected.append({"name": name, "status": "rejected_before_rounding", "error": str(exc)})
        else:
            raise AssertionError(f"Invalid certificate accepted: {name}")

    reject("bad_coverage", configs=[[[1, []]]])
    reject("bad_coverage_on_zero_job_not_hidden", p=[[0]], configs=[[[1, []]]])
    reject("forbidden_config_edge", p=[[None], [1]], configs=[[[1, [0]]], [[1, []]]])
    reject("overload", p=[[2]])
    reject("negative_weight", configs=[[[-1, [0]], [2, []]]])
    reject("negative_processing_time", p=[[-1]])
    reject("float_weight", configs=[[[1.0, [0]]]])
    reject("float_processing_time", p=[[0.5]])
    reject("duplicate_job_identity", configs=[[[1, [0, 0]]]])
    reject("row_probability_mass", configs=[[["1/2", [0]]]])
    reject("positive_atom_big_count_exceeds_k", p=[["1/2", "1/2"]], configs=[[[1, [0, 1]]]])
    reject("zero_weight_illegal_configuration", p=[["1/2", 2]], configs=[[[1, [0]], [0, [1]]]])
    reject("invalid_delta", delta="3/2")
    reject("bool_k", k=True)
    reject("zero_k", k=0)

    # T=0 with nonempty jobs is decoded solely via original zero endpoints.
    zero_target = decode([[0, None], [0, 0]], 0,
                         [[["1/2", [0]], ["1/2", []]], [["1/2", [0, 1]], ["1/2", [1]]]],
                         0, 1, baseline=counted)
    assert zero_target["assignment"] == [0, 1] and zero_target["remaining_jobs"] == []

    # A zero-weight legal column may exceed K: only positive columns are bounded.
    zero_weight = decode([["1/3"] * 3 for _ in range(3)], 1,
                         [[[1, [i]], [0, [0, 1, 2]]] for i in range(3)], 0, 1, baseline=counted)
    assert all(row["big_config_count_max"] == 1 for row in zero_weight["rows"])

    capped_checks = []
    for name, actual, capacity, bound_k, expected in [
        ("k4_exact_boundary", F(127, 64), F(1), 4, True),
        ("k4_just_above_boundary", F(255, 128), F(1), 4, False),
        ("huge_k_strictly_below_two", F(3, 2), F(1), 1 << 8192, True),
        ("huge_k_at_two_rejected", F(2), F(1), 1 << 8192, False),
        ("zero_capacity", F(0), F(0), 1 << 8192, True),
    ]:
        valid, diagnostics = _alpha_bound_check(actual, capacity, bound_k)
        assert valid == expected
        capped_checks.append({"name": name, "expected": expected, "observed": valid, "check": diagnostics})

    return {"kind": "supplied_CONFIG_constructor_audit_only", "success_fixture_count": len(fixtures), "fixtures": fixtures,
            "additional_zero_target": zero_target, "additional_legal_zero_weight_large_column": zero_weight,
            "rejection_count": len(rejected), "rejections": rejected, "round_slots_total_calls": len(calls),
            "capped_bound_arithmetic_checks": capped_checks, "alpha_denominator_constructed": False, "new_matching_or_LP_solver": False}


def main():
    # The mathematical input permits arbitrarily long exact encodings.
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--audit", action="store_true")
    modes.add_argument("--input", type=Path)
    args = parser.parse_args()
    baseline, baseline_path = load_baseline(args.baseline)
    if args.audit:
        result = audit(baseline)
    else:
        with args.input.open() as stream:
            supplied = json.load(stream)
        result = decode(**supplied, baseline=baseline)
    result["arithmetic"] = "fractions.Fraction; deterministic exact certificate construction"
    result["python_version"] = platform.python_version()
    if args.audit:
        result["command"] = "python3 tests/audits/unrelated_machines/tiny_work_stability_joint_rounding.py --audit"
    result["implementation_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["baseline_sha256"] = hashlib.sha256(baseline_path.read_bytes()).hexdigest()
    print(json.dumps(result, ensure_ascii=False, indent=2, default=_json_default))


if __name__ == "__main__":
    main()
