#!/usr/bin/env python3
"""Finite reconstruction of the frozen P_t exports; no universal inference.

Reconstruct all indexed states and actual finite job ends from the defining
equations, inspect every complementary-intersection certificate, and enumerate
the original t=1 matrix.  Never imports the historical audit implementation.
"""
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path
import hashlib
import json


REPO = Path(__file__).resolve().parents[5]
EVIDENCE = REPO / "archives/unrelated-machines/tools/evidence/cartesian-menu-reverse"
OUT = Path(__file__).with_name("um-transfer-finite-check.json")


def main():
    manifest = json.loads((EVIDENCE / "manifest.json").read_text())
    docs = {}
    for entry in manifest["items"]:
        data = (EVIDENCE / entry["raw_path"]).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert digest == entry["raw_sha256"] == entry["source_sha256"]
        assert len(data) == entry["size"]
        docs[Path(entry["source_path"]).name] = json.loads(data)
    results = []
    for t in range(1, 5):
        D = 2**t
        bits = list(product((0, 1), repeat=t))
        resources = list(product(range(4), repeat=t))
        sparse = docs[f"t{t}_sparse_P.json"]
        machines = {m["id"]: m for m in sparse["machines"]}
        jobs = {j["id"]: j for j in sparse["jobs"]}
        assert len(machines) == len(sparse["machines"]) == 2 * D**2
        assert len(jobs) == len(sparse["jobs"]) == D**3 + D
        assert sparse["t"] == t and sparse["time_denominator"] == D
        assert sparse["unlisted_processing_times"] == "infinity"
        private = {(tuple(m["g"]), tuple(m["ell"])): i for i, m in machines.items()
                   if m["kind"] == "private"}
        resource = {tuple(m["u"]): i for i, m in machines.items()
                    if m["kind"] == "resource"}
        assert set(private) == set(product(bits, bits))
        assert set(resource) == set(resources)
        support = {}
        for g, ell in product(bits, bits):
            support[g, ell] = {
                u for u in resources
                if all((u[i] % 2) ^ (g[i] & (u[i] // 2)) == ell[i]
                       for i in range(t))
            }
            assert len(support[g, ell]) == D
        states = {(tuple(s["g"]), tuple(s["ell"])): s for s in sparse["states"]}
        assert set(states) == set(support) and len(states) == len(sparse["states"])
        for key, s in states.items():
            assert s["private_machine"] == private[key]
            assert set(s["resource_machines"]) == {resource[u] for u in support[key]}
        seen_selectors, seen_incidence = set(), set()
        for job in jobs.values():
            g = tuple(job["g"])
            ends = {e["machine"]: e["time_units"] for e in job["finite"]}
            assert len(ends) == len(job["finite"])
            if job["kind"] == "selector":
                assert g not in seen_selectors
                seen_selectors.add(g)
                assert ends == {private[g, ell]: D for ell in bits}
            else:
                assert job["kind"] == "incidence"
                ell, u = tuple(job["ell"]), tuple(job["u"])
                key = (g, ell, u)
                assert key not in seen_incidence and u in support[g, ell]
                seen_incidence.add(key)
                assert ends == {private[g, ell]: 1, resource[u]: D}
        assert seen_selectors == set(bits)
        assert seen_incidence == {(g, ell, u) for (g, ell), us in support.items() for u in us}
        schedule = docs[f"t{t}_all_original_job_schedule.json"]
        assignments = {a["job"]: a for a in schedule["assignment"]}
        assert set(assignments) == set(jobs) and len(assignments) == len(schedule["assignment"])
        loads, intervals, exports = Counter(), defaultdict(list), Counter()
        selected = {tuple(s["g"]): tuple(s["ell"]) for s in schedule["selected_states"]}
        assert selected == {g: g[1:] + g[:1] for g in bits}
        for jid, a in assignments.items():
            j = jobs[jid]
            ends = {e["machine"]: e["time_units"] for e in j["finite"]}
            m = a["machine"]
            assert m in ends and a["time_units"] == ends[m]
            assert a["finish_units"] - a["start_units"] == ends[m]
            loads[m] += ends[m]
            intervals[m].append((a["start_units"], a["finish_units"]))
            g = tuple(j["g"])
            if j["kind"] == "selector":
                assert m == private[g, selected[g]]
            else:
                ell, u = tuple(j["ell"]), tuple(j["u"])
                should_export = ell == selected[g] and any(v // 2 == 0 for v in u)
                assert (machines[m]["kind"] == "resource") == should_export
                if should_export:
                    exports[g] += 1
        assert exports == Counter({g: D - 1 for g in bits})
        for intervals_m in intervals.values():
            intervals_m.sort()
            assert all(a[1] <= b[0] for a, b in zip(intervals_m, intervals_m[1:]))
        exported_loads = {row["machine"]: row["load_units"] for row in schedule["machine_load_units"]}
        assert exported_loads == {m: loads[m] for m in machines}
        assert max(loads.values()) == schedule["makespan_units"] == D + 1
        assert schedule["makespan_rational"] == {"numerator": D + 1, "denominator": D}
        certificates = docs[f"t{t}_all_complementary_intersections.json"]["certificates"]
        assert len(certificates) == D**3
        checked = set()
        for cert in certificates:
            g, h = tuple(cert["g"]), tuple(cert["complement_g"])
            ell, ell2 = tuple(cert["ell"]), tuple(cert["complement_ell"])
            assert h == tuple(1 ^ v for v in g)
            key = (g, ell, ell2)
            assert key not in checked
            checked.add(key)
            intersection = support[g, ell] & support[h, ell2]
            a = tuple(x ^ y for x, y in zip(ell, ell2))
            b = tuple(x ^ (z & y) for x, y, z in zip(ell, a, g))
            u = tuple(2 * x + y for x, y in zip(a, b))
            assert intersection == {u} == {tuple(cert["unique_resource"])}
            assert cert["resource_machine"] == resource[u]
        assert checked == set(product(bits, bits, bits))
        result = {"t": t, "jobs": len(jobs), "machines": len(machines),
                  "finite_ends": sum(len(j["finite"]) for j in jobs.values()),
                  "actual_support_equations_reconstructed": len(states),
                  "actual_complementary_certificates_recomputed": len(certificates),
                  "witness_peak": f"{D + 1}/{D}", "source_jobs_checked_once": len(jobs),
                  "optimization_enumerated": t == 1}
        if t == 1:
            histogram = Counter()
            for assignment in product(*(j["finite"] for j in jobs.values())):
                trial = Counter()
                for e in assignment:
                    trial[e["machine"]] += e["time_units"]
                histogram[max(trial.values())] += 1
            assert dict(histogram) == {3: 84, 4: 940}
            frozen = docs["t1_full_original_opt_enumeration.json"]
            assert {str(k): v for k, v in histogram.items()} == frozen["peak_units_histogram"]
            assert sum(histogram.values()) == frozen["complete_assignments_enumerated"] == 1024
            assert min(histogram) == frozen["exact_OPT_units"] == 3
            result["t1_full_assignment_histogram_units"] = dict(histogram)
        results.append(result)
    out = {"scope": "new finite reconstruction t=1..4 only; no universal theorem or normal-form optimization claim",
           "raw_files_hash_verified": len(docs), "source_manifest_sha256": hashlib.sha256((EVIDENCE / "manifest.json").read_bytes()).hexdigest(),
           "cases": results, "normal_form_equality_basis": "analytic proof in um-transfer-review.md, not this scan"}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
