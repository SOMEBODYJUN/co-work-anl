#!/usr/bin/env python3
"""Exact constructive audit of the single-positive-home query cube normal form.

The algorithm outputs disjoint A_q and, for each explicitly requested query
subset, a complete schedule on the original jobs. It never enumerates the
Boolean cube itself. All input schedules and output machine loads are checked
from the original processing matrix using fractions.Fraction.

This is a finite construction audit, not a proof of the general theorem.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def frac(value: Any) -> Fraction:
    require(isinstance(value, (str, int)) and not isinstance(value, bool),
            f"Rationals must be strings or integers, received {value!r}")
    return Fraction(value)


def fstr(value: Fraction) -> str:
    return str(value)


class QueryCube:
    def __init__(self, raw: dict[str, Any]) -> None:
        self.raw = raw
        self.machines = list(raw["machines"])
        require(bool(self.machines) and len(set(self.machines)) == len(self.machines),
                "Machine names must be nonempty and unique")
        require(all(isinstance(m, str) for m in self.machines), "Machine names must be strings")
        self.machine_set = set(self.machines)
        self.unit_order = [j["id"] for j in raw["unit_jobs"]]
        self.home_order = [j["id"] for j in raw["home_jobs"]]
        self.job_order = self.unit_order + self.home_order
        require(len(set(self.job_order)) == len(self.job_order), "Original job IDs must be unique")
        require(all(isinstance(j, str) for j in self.job_order), "Job IDs must be strings")
        self.U = set(self.unit_order)
        self.J = set(self.home_order)
        self.P: dict[str, dict[str, Fraction]] = {}
        self.home: dict[str, str] = {}
        self.small: dict[str, Fraction] = {}
        for job in raw["unit_jobs"] + raw["home_jobs"]:
            j = job["id"]
            self.P[j] = {m: frac(v) for m, v in job["processing"].items()}
            require(bool(self.P[j]), f"{j} has no finite processing endpoint")
            require(set(self.P[j]) <= self.machine_set, f"{j} uses an unknown machine")
            require(all(v >= 0 for v in self.P[j].values()), f"{j} has a negative processing time")
            if j in self.U:
                require(all(v == 1 for v in self.P[j].values()), f"{j} is not unit-only")
            else:
                h = job["home"]
                require(h in self.P[j], f"{j} has no finite home endpoint")
                a = self.P[j][h]
                require(0 < a < 1, f"{j} must have a positive, strictly small home")
                require(all(v in (0, 1) for m, v in self.P[j].items() if m != h),
                        f"{j} has a second positive small endpoint")
                self.home[j], self.small[j] = h, a
        self.H = set(self.home.values())
        self.query_order = list(raw["queries"])
        self.Q = set(self.query_order)
        require(bool(self.Q) and len(self.Q) == len(self.query_order) and self.Q <= self.J,
                "Queries must be a nonempty list of distinct home-job IDs")
        self.sigma0 = dict(raw["sigma0"])
        self.sigma1 = dict(raw["sigma1"])
        self.base_report = self.check_schedule(self.sigma0)
        self.strict_report = self.check_schedule(self.sigma1)
        require(frac(self.base_report["peak"]) <= 1, "sigma0 is not strict")
        require(frac(self.strict_report["peak"]) <= 1, "sigma1 is not strict")
        require(all(self.sigma0[j] == self.home[j] for j in self.J),
                "sigma0 must put every home job at home")
        self.D = {j for j in self.J if self.P[j][self.sigma1[j]] == 1}
        self.Z = {j for j in self.J if self.P[j][self.sigma1[j]] == 0}
        require(self.Q <= self.D, "sigma1 must export every query to a unit endpoint")
        require(all(self.sigma1[j] == self.home[j] for j in self.J - self.D - self.Z),
                "A non-unit, nonzero sigma1 assignment must be the unique home")
        self.weights = {j: Fraction(0) for j in self.D - self.Q}
        for j, value in raw.get("nonquery_unit_weights", {}).items():
            require(j in self.weights, f"Weight for {j} is outside D\\Q")
            self.weights[j] = frac(value)
            require(self.weights[j] >= 0, f"Negative fee for {j}")
        self.W = sum(self.weights.values(), Fraction(0))
        self._construct_paths()
        self._construct_closures()

    def check_schedule(self, schedule: dict[str, str]) -> dict[str, Any]:
        require(set(schedule) == set(self.job_order), "A schedule must cover every original job exactly once")
        loads = {m: Fraction(0) for m in self.machines}
        per_machine: dict[str, list[dict[str, str]]] = {m: [] for m in self.machines}
        for j in self.job_order:
            m = schedule[j]
            require(m in self.P[j], f"Illegal original endpoint: {j} -> {m}")
            p = self.P[j][m]
            loads[m] += p
            per_machine[m].append({"job": j, "processing_time": fstr(p)})
        peak = max(loads.values(), default=Fraction(0))
        return {
            "schedule": {j: schedule[j] for j in self.job_order},
            "loads": {m: fstr(loads[m]) for m in self.machines},
            "jobs_by_machine": per_machine,
            "peak": fstr(peak),
            "peak_machines": [m for m in self.machines if loads[m] == peak],
            "all_original_jobs_checked": True,
            "all_original_machine_loads_checked": True,
        }

    def _construct_paths(self) -> None:
        # M0 covers U only; M1 covers U and the sigma1 unit exports D.
        self.M0 = {j: self.sigma0[j] for j in self.U}
        self.M1 = {j: self.sigma1[j] for j in self.U | self.D}
        require(len(set(self.M0.values())) == len(self.M0), "M0 is not a matching")
        require(len(set(self.M1.values())) == len(self.M1), "M1 is not a matching")
        require(not (set(self.M0.values()) & self.H), "M0 must avoid every positive small home")
        owner0 = {m: j for j, m in self.M0.items()}
        self.paths: dict[str, list[tuple[str, str]]] = {}
        self.endpoints: dict[str, str] = {}
        seen_global: set[tuple[str, str]] = set()
        for d in self.home_order:
            if d not in self.D:
                continue
            j = d
            edges: list[tuple[str, str]] = []
            vertices: set[tuple[str, str]] = set()
            while True:
                require(("job", j) not in vertices, "Unexpected cycle on a D-augmenting path")
                vertices.add(("job", j))
                m = self.M1[j]
                require(("machine", m) not in vertices, "Repeated machine on an augmenting path")
                vertices.add(("machine", m))
                edges.append((j, m))  # M1 edges; M0 edges are determined by owner0.
                if m not in owner0:
                    self.endpoints[d] = m
                    break
                j = owner0[m]
            require(not (vertices & seen_global), "D-augmenting paths must be vertex-disjoint")
            seen_global |= vertices
            self.paths[d] = edges
        require(len(set(self.endpoints.values())) == len(self.D), "D endpoints must be distinct")
        for d, h in self.endpoints.items():
            if h in self.H:
                require(all(j in self.D | self.Z for j in self.J if self.home[j] == h),
                        f"Strict sigma1 did not remove all positive small jobs at endpoint {h}")

    def _construct_closures(self) -> None:
        self.children = {d: [] for d in self.D}
        endpoint_owner = {m: d for d, m in self.endpoints.items()}
        self.cut_query_edges: list[dict[str, str]] = []
        for j in self.home_order:
            if j not in self.D:
                continue
            parent = endpoint_owner.get(self.home[j])
            if parent is not None:
                if j in self.Q:
                    self.cut_query_edges.append({"parent": parent, "query": j, "home": self.home[j]})
                else:
                    self.children[parent].append(j)
        self.B_q: dict[str, set[str]] = {}
        self.A_q: dict[str, set[str]] = {}
        seen: set[str] = set()
        for q in self.query_order:
            reached: set[str] = set()
            stack = [q]
            while stack:
                j = stack.pop()
                if j in reached:
                    continue
                reached.add(j)
                stack.extend(self.children[j])
            require(reached & self.Q == {q}, "A query closure crossed another query root")
            require(not (seen & reached), "Query-root closures must be disjoint")
            seen |= reached
            self.B_q[q] = reached
            self.A_q[q] = reached - {q}
        self.dropped_D = self.D - seen
        self.c_q = {q: sum((self.weights[j] for j in self.A_q[q]), Fraction(0))
                    for q in self.query_order}
        require(sum(self.c_q.values(), Fraction(0)) <= self.W, "Closure costs exceed sigma1 fee")
        for q, expected in self.raw.get("expected_A_q", {}).items():
            require(q in self.Q and self.A_q[q] == set(expected), f"Manual A_q check failed for {q}")
        if "expected_dropped_D" in self.raw:
            require(self.dropped_D == set(self.raw["expected_dropped_D"]), "Manual dropped-D check failed")
        for j, endpoint in self.raw.get("expected_endpoints", {}).items():
            require(self.endpoints.get(j) == endpoint, f"Manual endpoint check failed for {j}")

    def delta(self, subset: set[str]) -> Fraction:
        remaining = {m: Fraction(0) for m in self.machines}
        for q in self.Q - subset:
            remaining[self.home[q]] += self.small[q]
        return max(remaining.values(), default=Fraction(0))

    def construct(self, subset_values: list[str], expected: dict[str, Any] | None = None) -> dict[str, Any]:
        require(isinstance(subset_values, list), "A requested subset must be a JSON list")
        subset = set(subset_values)
        require(len(subset) == len(subset_values) and subset <= self.Q,
                "A requested subset must contain distinct query IDs only")
        selected: set[str] = set()
        for q in subset:
            selected |= self.B_q[q]
        schedule = {j: self.sigma0[j] for j in self.U}
        # Simultaneous flips of vertex-disjoint augmenting components.
        for d in selected:
            for j, m in self.paths[d]:
                schedule[j] = m
        for j in self.home_order:
            if j in self.Z:
                schedule[j] = self.sigma1[j]
            elif j in selected:
                schedule[j] = self.sigma1[j]
            else:
                schedule[j] = self.home[j]
        report = self.check_schedule(schedule)
        actual_exports = {j for j in self.J if self.P[j][schedule[j]] == 1}
        require(actual_exports == selected, "The constructed J unit set is incorrect")
        require(actual_exports & self.Q == subset, "The actual query pattern is incorrect")
        require(all(schedule[j] == self.home[j] for j in self.Q - subset), "An inactive query did not return home")
        require(all(schedule[j] == self.sigma1[j] for j in self.Z), "A zero-end job did not stay at its sigma1 zero endpoint")
        cost = sum((self.weights[j] for j in actual_exports - self.Q), Fraction(0))
        additive = sum((self.c_q[q] for q in subset), Fraction(0))
        require(cost == additive, "Actual fees are not equal to the additive closure fees")
        delta = self.delta(subset)
        peak = frac(report["peak"])
        require(peak <= 1 + delta, "The exact actual load exceeds 1+delta(S)")
        if not subset or subset == self.Q:
            require(peak <= 1, "The empty/full query pattern should be strict")
        checked_expected: dict[str, str] = {}
        for key, actual in (("expected_peak", peak), ("expected_delta", delta), ("expected_fee", cost)):
            if expected is not None and key in expected:
                require(actual == frac(expected[key]), f"Manual {key} check failed for {subset_values}")
                checked_expected[key] = fstr(actual)
        report.update({
            "subset": [q for q in self.query_order if q in subset],
            "unit_exports": [j for j in self.home_order if j in actual_exports],
            "nonquery_unit_exports": [j for j in self.home_order if j in actual_exports - self.Q],
            "delta_remaining_queries": fstr(delta),
            "load_bound": fstr(1 + delta),
            "actual_nonquery_fee": fstr(cost),
            "additive_fee": fstr(additive),
            "unit_only_jobs_moved_from_sigma0": [j for j in self.unit_order if schedule[j] != self.sigma0[j]],
            "load_bound_checked": True,
            "fee_additivity_checked": True,
            "manual_expectations_checked": checked_expected,
        })
        return report

    def summary(self) -> dict[str, Any]:
        return {
            "original_machine_count": len(self.machines),
            "original_job_count": len(self.job_order),
            "queries": self.query_order,
            "D": [j for j in self.home_order if j in self.D],
            "Z": [j for j in self.home_order if j in self.Z],
            "augmenting_paths_M1_edges": {
                d: [{"job": j, "machine": m} for j, m in self.paths[d]]
                for d in self.home_order if d in self.D
            },
            "augmenting_endpoints": {d: self.endpoints[d] for d in self.home_order if d in self.D},
            "children_after_query_cut": {d: self.children[d] for d in self.home_order if d in self.D},
            "cut_query_edges": self.cut_query_edges,
            "A_q": {q: [j for j in self.home_order if j in self.A_q[q]] for q in self.query_order},
            "A_q_pairwise_disjoint_checked": True,
            "c_q": {q: fstr(self.c_q[q]) for q in self.query_order},
            "sigma1_nonquery_unit_fee_W": fstr(self.W),
            "constructed_full_query_fee": fstr(sum(self.c_q.values(), Fraction(0))),
            "dropped_D": [j for j in self.home_order if j in self.dropped_D],
            "sigma0": self.base_report,
            "sigma1": self.strict_report,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--subset", action="append", help='One explicit JSON query list, e.g. \'["q1","q3"]\'; may be repeated')
    args = parser.parse_args()
    input_bytes = args.input.read_bytes()
    raw = json.loads(input_bytes)
    cube = QueryCube(raw)
    if args.subset is not None:
        patterns = [{"subset": json.loads(value)} for value in args.subset]
    else:
        patterns = raw.get("audit_patterns", [{"subset": cube.query_order}])
    results = [cube.construct(record["subset"], record) for record in patterns]
    result = {
        "audit": "UM-SINGLE-HOME-CASCADE-QUERY-SEPARATION-v2 exact construction",
        "evidence_scope": "Only the explicitly listed input and query subsets are audited; finite checks do not prove the general theorem.",
        "arithmetic": "fractions.Fraction; no floating point processing times",
        "python_version": sys.version.split()[0],
        "invocation": ["python3", *sys.argv],
        "construction": "M0/M1 vertex-disjoint augmenting paths; cut query children; fixed sigma1 zero endpoints",
        "input_filename": args.input.name,
        "input_sha256": hashlib.sha256(input_bytes).hexdigest(),
        "script_filename": Path(__file__).name,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "all_checks_passed": True,
        "pattern_count_explicitly_requested": len(results),
        "normal_form": cube.summary(),
        "patterns": results,
    }
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as output_file:
            output_file.write(encoded)
        print(json.dumps({
            "output": str(args.output),
            "all_checks_passed": True,
            "pattern_count": len(results),
            "patterns": [{"subset": r["subset"], "peak": r["peak"],
                          "delta": r["delta_remaining_queries"], "fee": r["actual_nonquery_fee"]}
                         for r in results],
        }, ensure_ascii=False, indent=2))
    else:
        sys.stdout.write(encoded)


if __name__ == "__main__":
    main()
