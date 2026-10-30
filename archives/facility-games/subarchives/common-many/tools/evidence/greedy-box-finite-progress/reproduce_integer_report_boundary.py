#!/usr/bin/env python3
"""Reproduce one integer-report boundary without modifying the frozen source.

--check-dependencies hashes and compiles source only; it does not import or
execute a constructor. Normal mode makes exactly one construct_on_path call.
The historical evidence JSON records two earlier direct calls, not this wrapper.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
from fractions import Fraction

FROZEN = "68fad804ec5946cb296f77dc5b336308a66abf12"
CORE = {
    "multi_facility_spe/__init__.py":
        ("3185703b41c7540715bc",
         "14e0072f1de3ea824867d37a3f4b98f80847bc4676d224485cb7a1a4b8a133b7"),
    "multi_facility_spe/two_exists.py":
        ("a7a1f7d850e620474411",
         "85835c6481c7755a1bca0668c22dd8390578661ee34afdaa83bc31e1d909eb3e"),
}
GREEDY_ID = "4e4efdb8c30ab03aee8b"
GREEDY_SHA = "b3b391f6e4c1efd8e56c036d3d588f191959504aede58e686c3bfcb291f6ef35"


def verify(path, source_id, expected):
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected:
        raise ValueError(f"Frozen source hash mismatch: {path}")
    compile(raw, str(path), "exec")
    return dict(id=source_id, sha256=actual, bytes=len(raw))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--core-root", required=True, type=Path)
    parser.add_argument("--greedy-source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--check-dependencies", action="store_true")
    args = parser.parse_args()
    if not __debug__:
        raise ValueError("Use ordinary Python, not -O")
    if args.output.exists():
        raise FileExistsError("Refusing to overwrite an existing report")
    root = args.core_root.resolve()
    source = args.greedy_source.resolve()
    checked = {
        rel: verify(root / rel, ident, digest)
        for rel, (ident, digest) in CORE.items()
    }
    checked["multi_facility_spe/greedy_box.py"] = verify(
        source, GREEDY_ID, GREEDY_SHA)
    report = dict(
        frozen_commit=FROZEN, python=platform.python_version(),
        integer_decimal_digit_limit=(
            sys.get_int_max_str_digits()
            if hasattr(sys, "get_int_max_str_digits") else None),
        source_files=checked,
        helper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        constructor_calls=0,
        original_source_modified=False, global_digit_limit_modified=False,
        mode=("dependency-hash-and-syntax-only" if args.check_dependencies
              else "one-zero-step-constructor-call"),
    )
    if not args.check_dependencies:
        sys.dont_write_bytecode = True
        sys.path.insert(0, str(root))
        from multi_facility_spe.two_exists import Instance
        spec = importlib.util.spec_from_file_location(
            "multi_facility_spe.greedy_box", source)
        if spec is None or spec.loader is None:
            raise RuntimeError("Could not load the pinned module")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        count = 15000
        inst = Instance(
            (Fraction(3), Fraction(2)) + (Fraction(1, count),) * count,
            (frozenset({0}), frozenset({1}))
            + (frozenset({0, 1}),) * count,
            2, 3)
        report.update(
            mobile_clients=count, each_mobile_weight="1/15000",
            private_weights=["3", "2"],
            canonical_layout_expected=[0, 0, 1],
            assignment_bound_bit_length=count, constructor_calls=1)
        try:
            layout, assignment, audit = module.construct_on_path(inst)
        except ValueError as exc:
            frames = []
            tb = exc.__traceback__
            while tb is not None:
                if Path(tb.tb_frame.f_code.co_filename).resolve() == source:
                    local = tb.tb_frame.f_locals
                    frame = dict(
                        function=tb.tb_frame.f_code.co_name,
                        source_line=tb.tb_lineno)
                    if frame["function"] == "construct_on_path":
                        frame.update(
                            improvements=local.get("improvements"),
                            home_returns=local.get("repairs"),
                            batches=local.get("batches"),
                            final_verification=local.get("checked"))
                    frames.append(frame)
                tb = tb.tb_next
            report.update(outcome="ValueError", exception_message=str(exc),
                          frozen_source_frames=frames)
        else:
            report.update(
                outcome="returned",
                note="This interpreter/configuration permitted the conversion.",
                layout=list(layout),
                strict_improvements=audit["strict_improvements"],
                home_returns=audit["home_returns"], batches=audit["batches"],
                final_verification=audit["final_verification"],
                decimal_bound_characters=len(audit["assignment_move_bound"]),
            )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps(dict(output=str(args.output), mode=report["mode"],
                          constructor_calls=report["constructor_calls"])))


if __name__ == "__main__":
    main()
