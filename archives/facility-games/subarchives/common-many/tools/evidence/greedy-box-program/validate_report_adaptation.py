#!/usr/bin/env python3
"""Validate only report-bound-decimal/v1 and the previously failing zero-step input.

The original constructor is not called. No equal-flow, complete-certificate,
off-path or default evaluation is performed. All source hashes are checked.
"""
from __future__ import annotations

import argparse
import ast
from decimal import Decimal
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import time

ORIGINAL_SHA = "b3b391f6e4c1efd8e56c036d3d588f191959504aede58e686c3bfcb291f6ef35"
ADAPTED_SHA = "a50ea29a2506d9890d0773e69747a18e4127516d781a4750b1f757af3462f91c"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--core-root", type=Path, required=True)
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--adapted", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not __debug__:
        raise ValueError("Ordinary Python without -O is required")
    if args.output.exists():
        raise FileExistsError("Refusing to overwrite an existing validation report")
    if digest(args.original) != ORIGINAL_SHA or digest(args.adapted) != ADAPTED_SHA:
        raise ValueError("Unexpected source version")
    manifest = json.loads(Path(__file__).with_name("snapshot_manifest.json").read_text())
    verified = []
    for entry in manifest["files"]:
        path = args.core_root / entry["path"]
        if path.stat().st_size != entry["size_bytes"] or digest(path) != entry["sha256"]:
            raise ValueError("Fixture does not match the four pinned source versions")
        verified.append(entry["path"])

    before = ast.parse(args.original.read_text())
    after = ast.parse(args.adapted.read_text())
    helpers = [node for node in after.body
               if isinstance(node, ast.FunctionDef) and node.name == "_bound_decimal_text"]
    if len(helpers) != 1:
        raise AssertionError("Expected exactly one new helper")
    after.body.remove(helpers[0])
    changed = 0
    for node in ast.walk(after):
        if isinstance(node, ast.keyword) and node.arg == "assignment_move_bound":
            value = node.value
            if (not isinstance(value, ast.Call) or not isinstance(value.func, ast.Name)
                    or value.func.id != "_bound_decimal_text"
                    or len(value.args) != 1 or not isinstance(value.args[0], ast.Name)
                    or value.args[0].id != "bound" or value.keywords):
                raise AssertionError("Unexpected report expression")
            value.func.id = "str"
            changed += 1
    if changed != 1 or ast.dump(before) != ast.dump(after):
        raise AssertionError("The adapted module changes additional original executable AST")

    sys.dont_write_bytecode = True
    sys.path.insert(0, str(args.core_root.resolve()))
    from multi_facility_spe.two_exists import Instance
    spec = importlib.util.spec_from_file_location(
        "multi_facility_spe.greedy_box_decimal_bound", args.adapted.resolve())
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load adapted module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    limit_before = (sys.get_int_max_str_digits()
                    if hasattr(sys, "get_int_max_str_digits") else None)
    values = [0, 1, 10**9 - 1, 10**9, 10**9 + 1,
              10**18, 10**18 + 1000, 2**15000 - 1]
    comparisons = []
    for value in values:
        actual = module._bound_decimal_text(value)
        independent = format(Decimal(value), "f")
        if actual != independent:
            raise AssertionError("Mismatch with independent Decimal conversion")
        comparisons.append(dict(binary_bits=value.bit_length(),
                                decimal_characters=len(actual),
                                matches_decimal=True))

    count = 15000
    inst = Instance(
        (Fraction(3), Fraction(2)) + (Fraction(1, count),) * count,
        (frozenset({0}), frozenset({1})) + (frozenset({0, 1}),) * count,
        2, 3)
    started = time.monotonic()
    layout, assignment, audit = module.construct_on_path(inst)
    elapsed = time.monotonic() - started
    if layout != (0, 0, 1) or assignment != (0, 1) + (0,) * count:
        raise AssertionError("Unexpected zero-step assignment")
    for key in ("strict_improvements", "home_returns", "batches", "microsteps"):
        if audit[key] != 0:
            raise AssertionError("The zero-step regression unexpectedly moved")
    bound_text = audit["assignment_move_bound"]
    if bound_text != format(Decimal(2**count - 1), "f"):
        raise AssertionError("The reported movement bound is not exact")
    checked = audit["final_verification"]
    if any(checked[key] is not True for key in
           ("exact_ne", "full_boxes", "frozen_clients", "home_inequality")):
        raise AssertionError("Final mathematical verification failed")
    try:
        int(bound_text)
    except ValueError as exc:
        downstream = dict(outcome="ValueError", message=str(exc))
    else:
        downstream = dict(outcome="returned")
    limit_after = (sys.get_int_max_str_digits()
                   if hasattr(sys, "get_int_max_str_digits") else None)
    if limit_before != limit_after or digest(args.original) != ORIGINAL_SHA:
        raise AssertionError("Global limit or original source changed")

    report = dict(
        adaptation="report-bound-decimal/v1",
        python=platform.python_version(),
        integer_decimal_digit_limit_before=limit_before,
        integer_decimal_digit_limit_after=limit_after,
        original_source_sha256=ORIGINAL_SHA,
        adapted_source_sha256=ADAPTED_SHA,
        validation_helper_sha256=digest(Path(__file__)),
        verified_fixture_files=verified,
        ast_scope_check="After deleting the one new helper and restoring the one report call to str, all original executable AST nodes match.",
        formatter_comparisons=comparisons,
        original_constructor_calls=0, adapted_constructor_calls=1,
        complete_constructor_calls=0, equal_light_flow_calls=0,
        off_path_calls=0, default_evaluations=0,
        zero_step_regression=dict(
            mobile_clients=count, layout=list(layout), gamma=audit["gamma"],
            strict_improvements=audit["strict_improvements"],
            home_returns=audit["home_returns"], batches=audit["batches"],
            microsteps=audit["microsteps"], final_verification=checked,
            decimal_bound_characters=len(bound_text),
            decimal_bound_sha256=hashlib.sha256(bound_text.encode()).hexdigest(),
            exact_bound_matches_decimal=True, elapsed_seconds=elapsed),
        existing_downstream_int_conversion=downstream,
        original_source_modified=False,
        limits=[
            "Only assignment_move_bound formatting is adapted.",
            "Large Fraction formatting and input parsing are unchanged.",
            "An existing downstream int(very_long_decimal_text) may still fail.",
            "No claim that all methods or complete continuations were run.",
            "No change to the mathematical general-time bound.",
        ])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps(dict(output=str(args.output), original_constructor_calls=0,
                          adapted_constructor_calls=1,
                          exact_bound_characters=len(bound_text),
                          downstream_int_outcome=downstream["outcome"])))


if __name__ == "__main__":
    main()
