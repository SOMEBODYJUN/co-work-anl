"""Check frozen-byte bindings and reversible full-report views, without math runs.

Usage: python3 check_source_contracts.py --repo /path/to/results-repository
No original code is imported; no solver, LP, or SPE certificate is executed.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def decode(view: dict) -> dict:
    result = dict(view["root"])
    result["cases"] = []
    for case in view["cases"]:
        item = dict(case["fields"])
        item["attempts"] = []
        for start, iteration, index in case["attempts_start_iteration_payload"]:
            payload = dict(view["attempt_payloads"][index])
            message = view["messages"][payload.pop("message_id")]
            item["attempts"].append(dict(start=start, iteration=iteration,
                                          message=message, **payload))
        result["cases"].append(item)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    bindings = json.loads((here / "source-bindings.json").read_text())
    direct = {}
    for binding in bindings["bindings"]:
        raw = (args.repo / binding["preserved_path"]).read_bytes()
        assert len(raw) == binding["size"], binding["path"]
        assert hashlib.sha256(raw).hexdigest() == binding["sha256"], binding["path"]
        if binding["role"] == "direct":
            direct[Path(binding["path"]).name] = raw
    cases = attempts = 0
    for view_path in sorted((here / "lossless").glob("*.json")):
        raw_report = json.loads(direct[view_path.name])
        assert decode(json.loads(view_path.read_text())) == raw_report
        for case in raw_report["cases"]:
            starts = 5 if "name" in case else 4
            expected = list(itertools.product(range(starts), range(5)))
            rows = case["attempts"]
            assert [(a["start"], a["iteration"]) for a in rows] == expected
            assert all(a["status"] == 0 for a in rows)
            assert all(a["message"] == "Optimization terminated successfully. (HiGHS Status 7: Optimal)"
                       for a in rows)
            assert case["best_CCE_ratio"] <= 1 + 1e-6
            if "name" in case:
                assert case["best_CCE_ratio"] == max(a["CCE_ratio"] for a in rows)
            cases += 1
            attempts += len(rows)
    assert len(direct) == 6 and len(bindings["bindings"]) == 19
    assert cases == 32 and attempts == 660
    analysis = json.loads((here / "record-analysis.json").read_text())
    named_actions = {}
    for item in analysis["named_input_bindings"]:
        original_path = "evidence/certificates/customer_attraction/" + item["name"] + ".json"
        binding = next(b for b in bindings["bindings"] if b["path"] == original_path)
        pack = json.loads((args.repo / binding["preserved_path"]).read_text())
        actions = pack[item["key"]]["actions"]
        named_actions[item["name"]] = actions
        policy = {tuple(row["history"]): row["action"] for row in actions}
        n, k = item["players"], item["topics"]
        histories = {h for depth in range(n)
                     for h in itertools.product(range(k), repeat=depth)}
        assert len(actions) == len(policy) and set(policy) == histories
        assert all(isinstance(a, int) and not isinstance(a, bool) and 0 <= a < k
                   for a in policy.values())
        path = ()
        while len(path) < n:
            path += (policy[path],)
        assert list(path) == item["recovered_actual_path"]
        model_path = "examples/customer_attraction/" + item["name"] + ".json"
        model_binding = next(b for b in bindings["bindings"] if b["path"] == model_path)
        model = json.loads((args.repo / model_binding["preserved_path"]).read_text())
        masks = {}
        for customer in model["customers"]:
            mask = str(sum(1 << a for a in customer["topics"]))
            masks[mask] = masks.get(mask, 0) + customer.get("multiplicity", 1)
        assert masks == item["interest_mask_counts"]
        welfare = sum(count for mask, count in masks.items()
                      if any((int(mask) >> a) & 1 for a in path))
        assert welfare == item["recovered_actual_W"]
    assert named_actions["individual_security_failure"] == named_actions["local_security_increment"]
    print(json.dumps(dict(passed=True, frozen_byte_bindings=19, direct_sources=6,
                          complete_value_views=4, cases=cases, attempts=attempts,
                          scope="source/data/domain only; no mathematical certification",
                          original_imports=0, original_runs=0, LP_runs=0, BI_runs=0,
                          new_IC_checks=0), ensure_ascii=False))


if __name__ == "__main__":
    main()
