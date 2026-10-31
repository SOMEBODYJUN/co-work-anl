"""Independent raw-input/saved-output arithmetic; no original module imports."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from itertools import product
import ast
import hashlib
import json
import math

HERE = Path(__file__).resolve().parent
STAGE = HERE.parents[4]

def read(path):
    return json.loads((HERE / path).read_text())

def save(path, value):
    p = HERE / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + "\n")

def actual(input_, macro, private):
    groups, Z = input_["groups"], input_["sinks"]
    H = len(groups)
    assert len(macro) == len(input_["macros"]) and len(private) == H
    home, sink = [F(0)] * H, [F(0)] * Z
    for b, h in enumerate(macro):
        assert str(h) in input_["macros"][b]
        home[h] += F(input_["macros"][b][str(h)])
    jobs = len(macro)
    for h, (g, row) in enumerate(zip(groups, private)):
        assert len(row) == len(g["w"])
        for j, (kind, dest) in enumerate(row):
            if kind == "h":
                assert dest == h
                home[h] += F(g["w"][j])
            else:
                assert kind == "z" and dest in g["E"]
                sink[dest] += F(g["p"][str(dest)][j])
            jobs += 1
    return home, sink, jobs

def check_distorted():
    fixtures = read("original/examples/unrelated_machines/distorted_group_joint_slot_cases.json")
    outputs = read("comparison/evidence/certificates/unrelated_machines/distorted_group_joint_slot_witness.json")
    old = read("comparison/evidence/runs/unrelated_machines/distorted_group_joint_slot_audit.json")
    assert len(fixtures["cases"]) == len(outputs["cases"]) == 16
    assert old["normative_replay"]["fixtures_sha256"] == hashlib.sha256(
        (HERE / "original/examples/unrelated_machines/distorted_group_joint_slot_cases.json").read_bytes()).hexdigest()
    source_count = source_jobs = output_jobs = 0
    for ci, (case, out) in enumerate(zip(fixtures["cases"], outputs["cases"])):
        a = case["input"]
        T, delta, kappa, Bbar, r = map(F, (a["T"], a["delta"], a["kappa"], a["Bbar"], a["r"]))
        H, Z = len(a["groups"]), a["sinks"]
        W = [sum(map(F, g["w"]), F(0)) for g in a["groups"]]
        d = [max(F(0), w-r*T) for w in W]
        for h, g in enumerate(a["groups"]):
            assert W[h] <= T and all(0 <= F(w) <= delta*T for w in g["w"])
            assert set(map(int, g["b"])) == set(g["E"]) == set(map(int, g["p"]))
            for z in g["E"]:
                b = F(g["b"][str(z)])
                assert 0 <= b <= Bbar
                assert len(g["p"][str(z)]) == len(g["w"])
                for w, p in zip(g["w"], g["p"][str(z)]):
                    assert b*F(w) <= kappa*F(p) and F(p) <= b*F(w)
        source = case["source_schedules"]
        af = [defaultdict(F) for _ in a["macros"]]
        yf = [defaultdict(F) for _ in range(H)]
        mass = F(1, len(source))
        for macro, private in source:
            home, sink, jobs = actual(a, macro, private)
            assert len(set(macro)) == len(macro)
            assert max([F(0)] + home + sink) <= T
            for b, h in enumerate(macro):
                af[b][h] += mass
            for h in macro:
                if d[h] == 0:
                    yf[h][None] += mass
                else:
                    volume = defaultdict(F)
                    for w, (kind, z) in zip(a["groups"][h]["w"], private[h]):
                        if kind == "z":
                            volume[z] += F(w)
                    total = sum(volume.values(), F(0))
                    assert total > 0 and total >= d[h]
                    for z, v in volume.items():
                        yf[h][z] += mass*v/total
            source_count += 1
            source_jobs += jobs
        A = [{int(h): F(v) for h, v in row.items()} for row in case["LP_macro_flow"]]
        Y = [{None if z == "None" else int(z): F(v) for z, v in row.items()}
             for row in case["LP_token_flow"]]
        assert len(A) == len(af) and len(Y) == H
        for x, y in zip(A, af):
            assert all(x.get(k, 0) == y.get(k, 0) for k in set(x) | set(y))
        for x, y in zip(Y, yf):
            assert all(x.get(k, 0) == y.get(k, 0) for k in set(x) | set(y))
        occupation = [sum((row.get(h, F(0)) for row in A), F(0)) for h in range(H)]
        for h in range(H):
            assert occupation[h] <= 1 and sum(Y[h].values(), F(0)) == occupation[h]
            for z, v in Y[h].items():
                assert v >= 0
                assert (d[h] == 0 if z is None else z in a["groups"][h]["E"])
        budget, allowed, slot_set = [], [set() for _ in range(H)], set()
        for z in range(Z):
            costs = [F(g["b"].get(str(z), 0))*d[h] for h, g in enumerate(a["groups"])]
            budget.append(sum((costs[h]*Y[h].get(z, 0) for h in range(H)), F(0)))
            assert budget[-1] <= kappa*T
            at = F(0)
            for h in sorted(range(H), key=lambda h: (-costs[h], h)):
                end = at + Y[h].get(z, F(0))
                for k in range(math.floor(at), math.ceil(end)):
                    if min(end, k+1) > max(at, k):
                        allowed[h].add((z, k))
                        slot_set.add((z, k))
                at = end
        chosen = {int(h): tuple(slot) for h, slot in out["selected_slots"].items()}
        assert set(chosen) == set(out["macro_assignment"])
        assert len(out["macro_assignment"]) == len(chosen)
        used = set()
        token = [F(0)] * Z
        for h, (z, k) in chosen.items():
            if z is None:
                assert d[h] == 0 and Y[h].get(None, 0) > 0
            else:
                assert (z, k) in allowed[h] and (z, k) not in used
                used.add((z, k))
                token[z] += F(a["groups"][h]["b"][str(z)])*d[h]
        assert len(slot_set) == out["slot_count"]
        assert list(map(F, out["demand"])) == d
        assert list(map(F, out["fractional_sink_costs"])) == budget
        assert list(map(F, out["token_loads"])) == token
        for z in range(Z):
            maxcost = max([F(0)] + [F(g["b"].get(str(z), 0))*d[h]
                                    for h, g in enumerate(a["groups"])])
            assert token[z] <= budget[z]+maxcost <= (kappa+Bbar*(1-r))*T
        oldout = case["output"]
        oldmacro = [h for h, _slot in oldout["macro_home_slot"]]
        assert list(map(F, oldout["demand"])) == d
        assert list(map(F, oldout["token_loads"])) == token
        old_used = set()
        for h, (z, k) in oldout["macro_home_slot"]:
            if z is None:
                assert d[h] == 0 and Y[h].get(None, 0) > 0
            else:
                assert (z, k) in allowed[h] and (z, k) not in old_used
                old_used.add((z, k))
        for rec, macro in [(out, out["macro_assignment"]), (oldout, oldmacro)]:
            home, sink, jobs = actual(a, macro, rec["private_assignment"])
            assert home == list(map(F, rec["home_loads"]))
            assert sink == list(map(F, rec["sink_loads"]))
            assert all(v <= (1+r+delta)*T for v in home)
            assert all(v <= (kappa+Bbar*(1-r))*T for v in sink)
            if "makespan" in rec:
                assert F(rec["makespan"]) == max([F(0)] + home + sink)
            output_jobs += jobs
        assert out["macro_assignment"] == oldmacro
        assert out["private_assignment"] == oldout["private_assignment"]
        assert old["normative_replay"]["replays"][ci]["home_loads"] == out["home_loads"]
        assert old["normative_replay"]["replays"][ci]["sink_loads"] == out["sink_loads"]
    assert source_count == 86 and output_jobs == 184
    return {"fixtures": 16, "stored_real_source_schedules": source_count,
            "source_job_eligibility_and_load_checks": source_jobs,
            "all_original_job_output_checks_two_routes": output_jobs,
            "original_jobs_per_route": output_jobs//2,
            "source_average_LP_and_actual_slot_costs_reconstructed": True}

def check_exception():
    bundle = read("comparison/evidence/runs/unrelated_machines/dual_rail_threshold_soundness_boundary_audit.json")
    run = bundle["root_actual_runs"]["boss11_dual_rail_one_exception_actual.json"]
    assert run["random_cases"] == 2000 and run["independent_full_matrix_optimum_cases"] == 2079
    assert run["full_assignments"] == 597223 and run["binary_capacity_unit_augmentations"] == 3920
    assert run["independent_full_matrix_optimum_cases"] - 14*3**4 == 945
    assert 14*3**4*2**6 == 72576
    expected = [
        {"N":1,"C":2,"A":1,"rho":"1","ports":[[0,0,0,"1"],[0,1,1,"1"]],"exception":[[0,1]],"arity_slack":1},
        {"N":1,"C":1,"A":2,"rho":"1","ports":[[0,0,0,"1/3"]]*3,"exception":[[None,None]],"arity_slack":1},
        {"N":0,"C":0,"A":1,"rho":"1","ports":[],"exception":[],"arity_slack":1}]
    total_jobs = 0
    for inp, cert in zip(expected, run["certificates"]):
        N, C, A = inp["N"], inp["C"], inp["A"]
        matrix = [[None]*(N+len(inp["ports"])) for _ in range(max(1,2*N+C))]
        for v in range(N):
            matrix[2*v][v] = matrix[2*v+1][v] = F(1)
        for e, (v, rail, clause, w) in enumerate(inp["ports"]):
            matrix[2*v+rail][N+e] = F(w)
            matrix[2*N+clause][N+e] = F(1,A)
        assert matrix == [[None if x is None else F(x) for x in row] for row in cert["p"]]
        loads = [F(0)]*len(matrix)
        assert len(cert["sigma"]) == len(matrix[0])
        for j, i in enumerate(cert["sigma"]):
            assert matrix[i][j] is not None
            loads[i] += matrix[i][j]
            total_jobs += 1
        assert loads == list(map(F, cert["loads"])) and max(loads) <= 1
    save("fixtures/one-exception-hardcoded-inputs.json", expected)
    save("reused-runs/one-exception-extracted-record.json", {
        "origin":"comparison/evidence/runs/unrelated_machines/dual_rail_threshold_soundness_boundary_audit.json",
        "json_path":"root_actual_runs.boss11_dual_rail_one_exception_actual.json",
        "event_is_historical":True,"record":run})
    return {"historical_cases":2079,"random_cases":2000,"random_small_optimum_cases":945,
            "exhaustive_incidence_weight_cases":1134,"stored_complete_matrices":3,
            "stored_original_jobs_checked":total_jobs}

def check_arity():
    d = read("comparison/evidence/runs/unrelated_machines/fixed_arity_overload_witness_audit.json")
    assert sum(24**n for n in range(1,4)) == d["triple_full_matrix_oracle"]["matrices"] == 14424
    assert sum(40**n for n in range(1,4)) == d["triple_full_matrix_oracle"]["actual_schedules"] == 65640
    assert 3*14424 == 21093+22179
    assert sum(4**n for n in range(1,5))*16 == d["finite_local_row_distributions"] == 5440
    assert 4*(120+1) == d["given_big_only_full_certificates"] == 484
    assert sum(4**n for n in range(5))*4*3 == d["tuple_CSP_equivalence_checks"] == 4092
    slacks = {1:F(1),2:F(1,2)}
    slacks.update({r:F(1,6**(math.factorial(r-1)//2)) for r in range(3,9)})
    assert {str(r):str(slacks[r]) for r in range(1,6)} == d["slacks"]
    for r in range(4,9):
        assert slacks[r] == slacks[r-1]**(r-1)
    sharp = [[F(1),F(1,2),F(1,3)],[F(1),None,None],
             [None,F(1),None],[None,None,F(1)]]
    best = None
    count = 0
    for assignment in product(*[[i for i in range(4) if sharp[i][j] is not None] for j in range(3)]):
        loads = [F(0)]*4
        for j,i in enumerate(assignment):
            loads[i] += sharp[i][j]
        peak = max(loads)
        best = peak if best is None else min(best,peak)
        count += 1
    assert (best,count) == (F(1),8) and sum(sharp[0]) == F(11,6)
    save("fixtures/arity-full-matrix-boundaries.json", {
        "flow_envelope_sharp":{"matrix":sharp,"legal_bad_sigma":[0,0,0],"OPT":best,"assignments":count},
        "ordinary_vs_top4":{"matrix":[["1/4"]*5],"only_sigma":[0]*5,"ordinary_OPT":"5/4","top4_OPT":"1"},
        "local_distribution_actual_support":"two configuration atoms with masses1/3,2/3; repeated selected configurations retained"})
    return {"matrix_count":14424,"legal_complete_assignments":65640,"row_distribution_cases":5440,
            "row_atoms_per_generated_distribution":2,"big_certificate_cases":484,"tuple_checks":4092}

def check_sink():
    old = read("comparison/evidence/runs/unrelated_machines/fixed_sink_occupation_audit.json")
    assert sum(4**(m*j) for m in (1,2) for j in range(4)) == 4454
    assert sum(4**(m*j)*m**j for m in (1,2) for j in range(4)) == 33910
    assert 4*(2**12-1) == old["one_sided_bisection"]["acceptance_tables"] == 16380
    assert sum(2*a-1 for a in range(1,33)) == 1024
    cases = []
    for K in (1,2):
        H, beta = 2*K, F(1,8*K)
        matrix = [[None]*(K+H) for _ in range(H+K)]
        for k in range(K):
            matrix[2*k][k] = matrix[2*k+1][k] = F(1)
        for h in range(H):
            matrix[h][K+h] = F(3,4)
            matrix[H+h//2][K+h] = beta if h%2 == 0 else F(0)
        points = []
        for active_bits in product((0,1),repeat=K):
            macros = [2*k+(0 if active_bits[k] else 1) for k in range(K)]
            private = []
            home, sink = [F(0)]*H, [F(0)]*K
            for h in macros:
                home[h] += 1
            for h in range(H):
                k=h//2
                if h%2:
                    private.append(("sink",k))
                elif h in macros:
                    private.append(("sink",k));sink[k] += beta
                else:
                    private.append(("home",h));home[h] += F(3,4)
            assert all(x<=F(3,2) for x in home)
            assert all(x<=beta/2+2*K*beta for x in sink)
            sigma = macros + [dest if kind == "home" else H+dest for kind,dest in private]
            physical_loads = [F(0)]*(H+K)
            for j,i in enumerate(sigma):
                assert matrix[i][j] is not None
                physical_loads[i] += matrix[i][j]
            assert physical_loads == home+sink
            points.append({"occupied_even_choices":active_bits,"macro_assignment":macros,
                           "private_assignment":private,"sigma":sigma,
                           "home_loads":home,"sink_loads":sink})
        rounds = 0
        for vertex in product((F(0),F(1,2)),repeat=K):
            rounds += sum(all(x==F(1,2) or bit==0 for x,bit in zip(vertex,p["occupied_even_choices"]))
                          for p in points)
        assert rounds == 3**K and len(points) == 2**K
        assert old["occupation_faces"]["tight_count_examples"][K-1]["actual_schedules_restored"] == rounds
        cases.append({"K":K,"beta":beta,"T":"1","full_original_matrix":matrix,
                      "job_order":"K macros then one private job per home",
                      "macro_home_options":[[2*k,2*k+1] for k in range(K)],
                      "budgets":[beta/2]*K,"vertices_x_even":list(product((F(0),F(1,2)),repeat=K)),
                      "mode_pattern_rounding_events":rounds,"distinct_complete_schedules":points,
                      "note":"odd home's zero-time sink dominates home for both occupation tags in the actual DP"})
    save("fixtures/fixed-sink-two-tight-actual-cases.json",cases)
    return {"zero_target_matrices":4454,"full_machine_choices_examined_including_illegal":33910,
            "tight_real_instances":2,"tight_restoration_events":12,"distinct_tight_complete_schedules":6,
            "nonmonotone_acceptance_tables":16380,"macro_grid_contracts":1024}

def main():
    sources = read("primary-inventory.json") + read("comparison-inventory.json")
    by_path = {d["path"]:d for d in sources}
    for d in sources:
        p = STAGE/d["preserved_repo_path"]
        assert p.stat().st_size == d["size"]
        assert hashlib.sha256(p.read_bytes()).hexdigest() == d["sha256"]
        if p.suffix == ".py":
            ast.parse(p.read_text())
    distorted_run = read("comparison/evidence/runs/unrelated_machines/distorted_group_joint_slot_audit.json")
    for name in ["distorted_group_joint_slot.py", "distorted_group_software_review.py"]:
        path = "tests/audits/unrelated_machines/"+name
        assert distorted_run["sha256"][path] == by_path[path]["sha256"]
    dual_run = read("comparison/evidence/runs/unrelated_machines/dual_rail_threshold_soundness_boundary_audit.json")
    path = "tests/audits/unrelated_machines/dual_rail_one_exception_independent.py"
    assert dual_run["source_hashes"][path] == by_path[path]["sha256"]
    for name in ["fixed_arity_overload_witness", "fixed_sink_occupation"]:
        path = "tests/audits/unrelated_machines/"+name+"_audit.py"
        old = read("comparison/evidence/runs/unrelated_machines/"+name+"_audit.json")
        assert old["source_sha256"] == by_path[path]["sha256"]
    report = {"status":"passed","verification":"raw input/saved output arithmetic, source SHA/AST and explicit finite boundary checks",
              "original_program_new_runs":0,"original_algorithm_imports":0,"inventory_files":len(sources),
              "distorted":check_distorted(),"one_exception":check_exception(),
              "fixed_arity":check_arity(),"fixed_sink":check_sink()}
    save("saved-data-selfcheck.json",report)
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__ == "__main__":
    main()
