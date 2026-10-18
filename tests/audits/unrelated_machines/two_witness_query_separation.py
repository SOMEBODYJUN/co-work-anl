#!/usr/bin/env python3
"""Exact finite audit of the general two-witness query-separation coloring.

No unit/home or arity assumption is made. Each changed job is a directed arc
from its sigma0 owner to its sigma1 owner, with its actual endpoint times.
The constructive algorithm uses a strict T/2 trigger and triggers each machine
at most once. Optional exhaustive enumeration is explicitly limited to at most
64 two-witness endpoint states and is evidence only for that listed instance.
Output files are created exclusively and are never overwritten.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import sys
from typing import Any


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def rat(value: Any) -> Fraction:
    require(isinstance(value, (str, int)) and not isinstance(value, bool),
            f"Rationals must be exact strings or integers: {value!r}")
    return Fraction(value)


class TwoWitnessColoring:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data
        self.case_id = data["id"]
        self.T = rat(data["T"])
        require(self.T >= 0, "T must be nonnegative")
        self.machines = list(data["machines"])
        require(bool(self.machines) and len(set(self.machines)) == len(self.machines),
                "Machine IDs must be nonempty and distinct")
        self.machine_set = set(self.machines)
        self.jobs = [record["id"] for record in data["jobs"]]
        require(len(set(self.jobs)) == len(self.jobs), "Job IDs must be distinct")
        require(all(isinstance(x, str) for x in self.machines + self.jobs),
                "Job and machine IDs must be strings")
        self.P: dict[str, dict[str, Fraction]] = {}
        for record in data["jobs"]:
            j = record["id"]
            self.P[j] = {m: rat(p) for m, p in record["processing"].items()}
            require(bool(self.P[j]), f"{j} has no finite endpoint")
            require(set(self.P[j]) <= self.machine_set, f"{j} has an unknown endpoint")
            require(all(p >= 0 for p in self.P[j].values()), f"{j} has a negative processing time")
        self.sigma0 = dict(data["sigma0"])
        self.sigma1 = dict(data["sigma1"])
        self.sigma0_report = self.check_schedule(self.sigma0)
        self.sigma1_report = self.check_schedule(self.sigma1)
        require(rat(self.sigma0_report["peak"]) <= self.T, "sigma0 exceeds T")
        require(rat(self.sigma1_report["peak"]) <= self.T, "sigma1 exceeds T")
        self.D_order = [j for j in self.jobs if self.sigma0[j] != self.sigma1[j]]
        self.D = set(self.D_order)
        self.query_order = list(data["queries"])
        self.Q = set(self.query_order)
        require(bool(self.Q) and len(self.Q) == len(self.query_order) and self.Q <= self.D,
                "Q must be nonempty, distinct and contained in changed jobs D")
        self.nonquery_order = [j for j in self.D_order if j not in self.Q]
        self.weights = {j: Fraction(0) for j in self.nonquery_order}
        for j, value in data.get("nonquery_move_weights", {}).items():
            require(j in self.weights, f"Weight on {j} lies outside D\\Q")
            self.weights[j] = rat(value)
            require(self.weights[j] >= 0, f"Negative move weight for {j}")
        self.W = sum(self.weights.values(), Fraction(0))
        self.a = {j: self.P[j][self.sigma0[j]] for j in self.D_order}
        self.b = {j: self.P[j][self.sigma1[j]] for j in self.D_order}
        self.fixed = {m: Fraction(0) for m in self.machines}
        self.outgoing = {m: [] for m in self.machines}
        for j in self.jobs:
            if j not in self.D:
                self.fixed[self.sigma0[j]] += self.P[j][self.sigma0[j]]
            elif j not in self.Q:
                self.outgoing[self.sigma0[j]].append(j)
        self._color()

    def check_schedule(self, schedule: dict[str, str]) -> dict[str, Any]:
        require(set(schedule) == set(self.jobs), "A schedule must assign every original job exactly once")
        loads = {m: Fraction(0) for m in self.machines}
        assignments: dict[str, list[dict[str, str]]] = {m: [] for m in self.machines}
        for j in self.jobs:
            m = schedule[j]
            require(m in self.P[j], f"Illegal original endpoint {j}->{m}")
            p = self.P[j][m]
            loads[m] += p
            assignments[m].append({"job": j, "processing_time": str(p)})
        peak = max(loads.values(), default=Fraction(0))
        return {
            "schedule": {j: schedule[j] for j in self.jobs},
            "loads": {m: str(loads[m]) for m in self.machines},
            "jobs_by_machine": assignments,
            "peak": str(peak),
            "peak_machines": [m for m in self.machines if loads[m] == peak],
            "all_original_jobs_checked": True,
            "all_original_machine_loads_checked": True,
        }

    def _color(self) -> None:
        self.threshold = self.T / 2
        self.color: dict[str, str | None] = {j: (j if j in self.Q else None) for j in self.D_order}
        self.inflow = {m: {q: Fraction(0) for q in self.query_order} for m in self.machines}
        for q in self.query_order:
            self.inflow[self.sigma1[q]][q] += self.b[q]
        self.machine_color: dict[str, str | None] = {m: None for m in self.machines}
        self.trace: list[dict[str, Any]] = []
        while True:
            # Fixed input machine order, then fixed input query order.
            candidate = next(((m, q) for m in self.machines
                              if self.machine_color[m] is None
                              for q in self.query_order
                              if self.inflow[m][q] > self.threshold), None)
            if candidate is None:
                break
            m, q = candidate
            trigger_inflow = self.inflow[m][q]
            self.machine_color[m] = q
            updates = []
            for j in self.outgoing[m]:
                require(self.color[j] is None, "A nonquery arc was assigned a second color")
                self.color[j] = q
                target = self.sigma1[j]
                self.inflow[target][q] += self.b[j]
                updates.append({"job": j, "target": target,
                                "added_inflow": str(self.b[j]),
                                "new_color_inflow_at_target": str(self.inflow[target][q])})
            self.trace.append({"step": len(self.trace) + 1, "machine": m, "color": q,
                               "inflow_at_trigger": str(trigger_inflow),
                               "strict_threshold": str(self.threshold),
                               "newly_colored_arcs": updates})
            require(len(self.trace) <= len(self.machines), "More than one trigger per machine")

        # Independently recompute the final inflow table from colored job arcs.
        recomputed = {m: {q: Fraction(0) for q in self.query_order} for m in self.machines}
        for j in self.D_order:
            q = self.color[j]
            if q is not None:
                recomputed[self.sigma1[j]][q] += self.b[j]
        require(recomputed == self.inflow, "Incremental inflow table is incorrect")
        for m in self.machines:
            require(self.fixed[m] + sum(self.inflow[m].values(), Fraction(0)) <= self.T,
                    "Colored inflows violate the strict sigma1 total")
            for q in self.query_order:
                if self.machine_color[m] == q:
                    require(self.inflow[m][q] > self.threshold, "A triggered color lost its strict majority")
                    require(all(self.color[j] == q for j in self.outgoing[m]),
                            "A triggered machine left a nonquery outgoing arc uncolored")
                else:
                    require(self.inflow[m][q] <= self.threshold, "A machine needs a second color trigger")
        require(all(self.color[q] == q for q in self.Q), "A query changed its own color")
        self.A = {q: {j for j in self.nonquery_order if self.color[j] == q} for q in self.query_order}
        seen: set[str] = set()
        for q in self.query_order:
            require(not (seen & self.A[q]), "A_q supports are not disjoint")
            seen |= self.A[q]
        self.c = {q: sum((self.weights[j] for j in self.A[q]), Fraction(0)) for q in self.query_order}
        require(sum(self.c.values(), Fraction(0)) <= self.W, "Total constructed fee exceeds W")
        expected = self.data.get("expected", {})
        for q, support in expected.get("A_q", {}).items():
            require(q in self.Q and self.A[q] == set(support), f"Manual A_q check failed for {q}")
        if "trigger_order" in expected:
            actual = [{"machine": e["machine"], "color": e["color"]} for e in self.trace]
            require(actual == expected["trigger_order"], "Manual deterministic trigger order failed")
        if "uncolored_nonquery" in expected:
            actual = {j for j in self.nonquery_order if self.color[j] is None}
            require(actual == set(expected["uncolored_nonquery"]), "Manual uncolored support check failed")

    def delta(self, q: str) -> Fraction:
        require(q in self.Q, "Unknown query")
        sums = {m: Fraction(0) for m in self.machines}
        for r in self.query_order:
            if r != q:
                sums[self.sigma0[r]] += self.a[r]
        return max(sums.values(), default=Fraction(0))

    def construct(self, q: str) -> dict[str, Any]:
        require(q in self.Q, "Requested query is outside Q")
        changed = {q} | self.A[q]
        schedule = {j: (self.sigma1[j] if j in changed else self.sigma0[j]) for j in self.jobs}
        report = self.check_schedule(schedule)
        actual_changed = {j for j in self.jobs if schedule[j] != self.sigma0[j]}
        require(actual_changed == changed, "Actual changed jobs differ from q union A_q")
        require(actual_changed & self.Q == {q}, "The output changed a second query")
        actual_fee = sum((self.weights[j] for j in actual_changed - self.Q), Fraction(0))
        require(actual_fee == self.c[q], "The actual nonquery fee differs from A_q fee")
        delta = self.delta(q)
        bound = max(3 * self.T / 2, self.T + delta)
        peak = rat(report["peak"])
        require(0 <= delta <= self.T, "delta_q is outside [0,T]")
        require(peak <= bound, "An original machine exceeds the theorem bound")
        expected = self.data.get("expected", {}).get("tau", {}).get(q, {})
        actual_values = {"peak": peak, "delta": delta, "bound": bound, "fee": actual_fee}
        for key, value in expected.items():
            require(key in actual_values and actual_values[key] == rat(value),
                    f"Manual tau_{q} {key} check failed")
        report.update({"query": q,
                       "changed_jobs": [j for j in self.jobs if j in actual_changed],
                       "A_q": [j for j in self.jobs if j in self.A[q]],
                       "delta_q": str(delta), "theorem_bound": str(bound),
                       "actual_nonquery_fee": str(actual_fee), "support_fee": str(self.c[q]),
                       "fee_equality_checked": True, "load_bound_checked": True,
                       "manual_values_checked": {k: str(v) for k, v in actual_values.items() if k in expected}})
        return report

    def enumerate_listed_two_endpoint_states(self, spec: dict[str, Any]) -> dict[str, Any]:
        # This bounded finite check is separate from the polynomial coloring algorithm.
        state_count = 2 ** len(self.D_order)
        limit = int(spec["state_limit"])
        require(0 < limit <= 64 and state_count <= limit, "The optional finite enumeration exceeds its explicit limit")
        require(state_count == int(spec["expected_state_count"]), "Unexpected finite state count")
        covers_all = all(set(self.P[j]) == {self.sigma0[j], self.sigma1[j]} for j in self.jobs)
        if spec.get("require_all_finite_endpoint_schedules_covered", False):
            require(covers_all, "The listed two endpoints do not cover all finite endpoint assignments")
        states: list[dict[str, Any]] = []
        for bits in product((0, 1), repeat=len(self.D_order)):
            changed = {j for j, bit in zip(self.D_order, bits) if bit}
            schedule = {j: (self.sigma1[j] if j in changed else self.sigma0[j]) for j in self.jobs}
            report = self.check_schedule(schedule)
            fee = sum((self.weights[j] for j in changed - self.Q), Fraction(0))
            report.update({"state_bits_in_D_order": list(bits),
                           "query_subset": [q for q in self.query_order if q in changed],
                           "changed_nonquery": [j for j in self.nonquery_order if j in changed],
                           "nonquery_move_fee": str(fee)})
            states.append(report)
        threshold_reports = []
        for check in spec.get("threshold_checks", []):
            subset = set(check["query_subset"])
            require(subset <= self.Q, "An enumeration query subset is invalid")
            cap = rat(check["cap"])
            feasible = [s for s in states if set(s["query_subset"]) == subset and rat(s["peak"]) <= cap]
            require(bool(feasible), "No state exists for a listed threshold check")
            best_fee = min(rat(s["nonquery_move_fee"]) for s in feasible)
            require(best_fee == rat(check["expected_min_fee"]), "Finite threshold minimum fee check failed")
            mandatory = set(feasible[0]["changed_nonquery"])
            for state in feasible[1:]:
                mandatory &= set(state["changed_nonquery"])
            require(set(check.get("mandatory_nonquery_contains", [])) <= mandatory,
                    "The requested fee job is not forced in every feasible singleton state")
            witness = next(s for s in feasible if rat(s["nonquery_move_fee"]) == best_fee)
            threshold_reports.append({"query_subset": check["query_subset"], "cap": str(cap),
                                      "feasible_state_count": len(feasible), "minimum_fee": str(best_fee),
                                      "mandatory_changed_nonquery": [j for j in self.nonquery_order if j in mandatory],
                                      "minimum_fee_witness_bits": witness["state_bits_in_D_order"],
                                      "minimum_fee_witness_peak": witness["peak"], "checked": True})
        minimum_peak_reports = []
        for check in spec.get("minimum_peak_checks", []):
            subset = set(check["query_subset"])
            require(subset <= self.Q, "A minimum-peak query subset is invalid")
            fee_cap = rat(check["fee_at_most"])
            feasible = [s for s in states if set(s["query_subset"]) == subset
                        and rat(s["nonquery_move_fee"]) <= fee_cap]
            require(bool(feasible), "No state exists for a minimum-peak check")
            best_peak = min(rat(s["peak"]) for s in feasible)
            require(best_peak == rat(check["expected_min_peak"]), "Finite minimum-peak check failed")
            witness = next(s for s in feasible if rat(s["peak"]) == best_peak)
            minimum_peak_reports.append({"query_subset": check["query_subset"], "fee_at_most": str(fee_cap),
                                         "minimum_peak": str(best_peak),
                                         "witness_bits": witness["state_bits_in_D_order"], "checked": True})
        return {"scope": "Only this explicit finite case; not a proof of the general separation theorem.",
                "D_bit_order": self.D_order, "state_count": len(states),
                "all_finite_endpoint_assignments_covered": covers_all,
                "threshold_checks": threshold_reports, "minimum_peak_checks": minimum_peak_reports,
                "states": states}

    def audit(self) -> dict[str, Any]:
        requested = list(self.data.get("requested_queries", self.query_order))
        require(len(set(requested)) == len(requested) and set(requested) <= self.Q,
                "Requested queries must be distinct and belong to Q")
        result = {"case_id": self.case_id, "purpose": self.data.get("purpose", ""), "T": str(self.T),
                  "original_machine_count": len(self.machines), "original_job_count": len(self.jobs),
                  "D": self.D_order, "Q": self.query_order,
                  "arcs": [{"job": j, "source": self.sigma0[j], "target": self.sigma1[j],
                            "source_time": str(self.a[j]), "target_time": str(self.b[j]),
                            "final_color": self.color[j]} for j in self.D_order],
                  "trigger_threshold": str(self.threshold), "trigger_trace": self.trace,
                  "machine_colors": self.machine_color,
                  "final_colored_inflow": {m: {q: str(v) for q, v in self.inflow[m].items()} for m in self.machines},
                  "stationary_loads": {m: str(self.fixed[m]) for m in self.machines},
                  "each_machine_triggered_at_most_once_checked": True,
                  "final_threshold_invariants_checked": True,
                  "A_q": {q: [j for j in self.jobs if j in self.A[q]] for q in self.query_order},
                  "A_q_pairwise_disjoint_checked": True,
                  "uncolored_nonquery": [j for j in self.nonquery_order if self.color[j] is None],
                  "c_q": {q: str(self.c[q]) for q in self.query_order},
                  "sum_c_q": str(sum(self.c.values(), Fraction(0))), "W": str(self.W),
                  "total_fee_inequality_checked": True,
                  "sigma0": self.sigma0_report, "sigma1": self.sigma1_report,
                  "requested_tau": [self.construct(q) for q in requested]}
        if "enumeration" in self.data:
            result["finite_enumeration"] = self.enumerate_listed_two_endpoint_states(self.data["enumeration"])
        return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path, help="Must not already exist; created with exclusive mode")
    args = parser.parse_args()
    require(not args.output.exists(), "Output already exists; exclusive creation forbids overwriting")
    input_bytes = args.input.read_bytes()
    raw = json.loads(input_bytes)
    results = [TwoWitnessColoring(case).audit() for case in raw["cases"]]
    result = {"audit": "General two-witness direct-job-arc monotone coloring; no unit/home assumptions",
              "claim_reference": raw.get("claim", {}),
              "evidence_scope": "Only the explicitly listed cases and optional bounded finite states are checked; these checks do not prove a general theorem.",
              "arithmetic": "fractions.Fraction only; exact string rational input",
              "python_version": sys.version.split()[0], "invocation": ["python3", *sys.argv],
              "input_filename": args.input.name, "input_sha256": hashlib.sha256(input_bytes).hexdigest(),
              "script_filename": Path(__file__).name,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "all_checks_passed": True, "case_count": len(results), "cases": results}
    # Exclusive mode also protects against a concurrent creator after the early check.
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps({"output": str(args.output), "all_checks_passed": True,
                      "cases": [{"id": case["case_id"], "A_q": case["A_q"],
                                 "tau": [{"q": t["query"], "peak": t["peak"],
                                          "delta": t["delta_q"], "bound": t["theorem_bound"],
                                          "fee": t["actual_nonquery_fee"]} for t in case["requested_tau"]],
                                 "finite_states": case.get("finite_enumeration", {}).get("state_count", 0)}
                                for case in results]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
