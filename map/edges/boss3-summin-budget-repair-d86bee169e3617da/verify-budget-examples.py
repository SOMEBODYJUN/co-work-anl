#!/usr/bin/env python3
"""Exact, standard-library replay of two fixed SUMmin-full budget examples.

Run from any working directory.  This file only writes its sibling JSON report.
The original 36-customer formula policy is rebuilt without importing a solver.
For n=6 both Mobius inversions are rebuilt; no unit-customer expansion or full
12-action, six-player SPE enumeration is attempted.  The all-p statements are
analytic inequalities explained in the report, not sampled-distribution tests.
"""

from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
from math import comb
from pathlib import Path
import json
import platform
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUTPUT = HERE / "budget-example-results.json"
TASK = "boss3-summin-budget-repair-d86bee169e3617da"
BASE = "archives/customer-attraction/"
SOURCE_PATHS = {
    "rules": "AGENTS.md",
    "implementation": "research/IMPLEMENTATION.md",
    "worker": "prompts/03-map-worker.md",
    "task": f"research/operations/map-v2/tasks/{TASK}.json",
    "registry": "research/registry.json",
    "model": BASE + "state/定义/共同目录完整历史模型--定义.md",
    "summin": BASE + "state/候选/全槽逐行最小价格的共同预算与有限报告--候选.md",
    "small_body": BASE + "state/反例/三人聚合末位保底--反例.md",
    "all_n_body": BASE + "state/反例/三人及以上聚合末位保底--反例.md",
    "mobius": BASE + "state/定理/子集调和势的Möbius反演--定理.md",
    "compiler": BASE + "state/定理/无重复辅助博弈的完整历史编译--定理.md",
    "small_input": BASE + "tools/evidence/aggregate-security/original/examples/customer_attraction/aggregate_theta_failure.json",
    "small_certificate": BASE + "tools/evidence/aggregate-security/original/evidence/certificates/customer_attraction/aggregate_theta_failure.json",
}
FROZEN_SHA = {
    "model": "cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88",
    "summin": "e952c73849b2ac561ac4ebb761b3ae0c1af06d61f27e743c593ea0103c52698a",
    "small_body": "f2ff6b486d46f5e05d9acb2497ec1114ac8ab4698460fb46656d320e640fe4c0",
    "all_n_body": "d316702ecc98a5976769d1d2e0094341474e0c4655deaac825bc208ae81d36e7",
    "mobius": "9c7e58e4642077607ce2b49c67e7598c97b47b4cdb1b43a34cf335dd2aec5629",
    "compiler": "e6e06a43973f7c37673b498074475fdf8aa37338d448aff53b2bf9b2e7fa0dd4",
    "small_input": "be0e1a54d3a7ddfeba327c03ce1975932e8fd1018926147b9c555fe6af180aaf",
    "small_certificate": "cf08edab0813de8eccee8d5466d15b40bd42c980da9b0b68c925f4ae80991010",
}


def digest(data):
    return sha256(data).hexdigest()


def canonical_digest(value):
    return digest(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def exact(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): exact(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [exact(v) for v in value]
    return value


def source_binding():
    data = {name: (ROOT / path).read_bytes() for name, path in SOURCE_PATHS.items()}
    for name, expected in FROZEN_SHA.items():
        assert digest(data[name]) == expected, (name, "frozen source changed")
    registry = json.loads(data["registry"])
    objects = registry["objects"]
    if isinstance(objects, dict):
        objects = [dict(obj, object_id=key) for key, obj in objects.items()]
    selected = {obj["object_id"]: obj for obj in objects if obj["object_id"] in {
        "CA-AGGREGATE-LAST-FLOOR-NO",
        "customer-attraction/three-player-aggregate-last-floor-counterexample",
        "customer-attraction/e7-summin-full-common-budget-exact-discount-and-finite-tests",
    }}
    assert len(selected) == 3
    for obj in selected.values():
        body = obj["body"]
        assert digest((ROOT / body["path"]).read_bytes()) == body["sha256"]
    task = json.loads(data["task"])
    assert task["owner"] == "Boss3"
    # Normal delivery changes queue state, not any mathematical premise or
    # source/endpoint binding; preserve replay after this task is marked done.
    assert task["state"] in {"claimed", "done"}
    assert task["definition"]["task_id"] == TASK
    return data, {
        "sources": [{"name": name, "path": path, "sha256": digest(data[name]),
                     "bytes": len(data[name])} for name, path in SOURCE_PATHS.items()],
        "selected_registry_objects": [{"object_id": key, "version": obj["version"],
                                       "truth_status": obj["truth_status"], "body": obj["body"]}
                                      for key, obj in selected.items()],
        "task_queue_state": task["state"],
        "task_queue_state_scope": "Claimed or normally delivered done is accepted; queue stage is not a mathematical premise. Owner, definition identity, frozen-source hashes and registered body bindings remain checked.",
        "formula_translation": "Source-bound hand translation of the complete 36-customer formula policy and all-n equations (2),(3),(5); no repository solver or prior numeric report is imported.",
    }


def small_example(data):
    # Interest types are reconstructed from the definition, then checked against
    # the original input; the latter is not used as the computational type table.
    X, Y = range(3), range(3, 6)
    types = [(frozenset((x, y)), 1) for x in X for y in Y]
    types += [(frozenset(I + J), 3) for I in combinations(X, 2) for J in combinations(Y, 2)]
    game = json.loads(data["small_input"])
    original_types = Counter({frozenset(t["topics"]): t["multiplicity"] for t in game["customers"]})
    assert original_types == Counter(dict(types))
    assert game["players"] == 3 and len(game["topics"]) == 6
    customers = [B for B, multiplicity in types for _ in range(multiplicity)]
    assert len(customers) == 36 and len(types) == 18
    topics, m = range(6), 3

    def policy(history):
        if not history:
            return 0
        if len(history) == 1:
            return 3 if history[0] < 3 else 0
        assert len(history) == 2
        group = X if history[1] < 3 else Y
        return next(a for a in group if a not in history)

    histories = [h for depth in range(m) for h in product(topics, repeat=depth)]
    actions = {h: policy(h) for h in histories}
    certificate = json.loads(data["small_certificate"])
    cert_actions = certificate["strategy"]["actions"]
    assert len(cert_actions) == len(actions) == 43
    assert {tuple(row["history"]): row["action"] for row in cert_actions} == actions

    def continue_policy(prefix):
        h = tuple(prefix)
        while len(h) < m:
            h += (policy(h),)
        return h

    def payoffs(terminal):
        loads = [sum(a in B for a in terminal) for B in customers]
        return tuple(sum((Q(1, load) for B, load in zip(customers, loads) if a in B), Q())
                     for a in terminal)

    all_terminals = list(product(topics, repeat=m))
    terminal_payoffs = {z: payoffs(z) for z in all_terminals}
    welfares = {z: sum(any(a in B for a in z) for B in customers) for z in all_terminals}
    for z in all_terminals:
        assert sum(terminal_payoffs[z]) == welfares[z]

    comparisons = []
    for h in histories:
        own = terminal_payoffs[continue_policy(h)][len(h)]
        for a in topics:
            alt = terminal_payoffs[continue_policy(h + (a,))][len(h)]
            assert own >= alt, (h, a, own, alt)
            comparisons.append({"history": h, "specified_action": policy(h), "tested_action": a,
                                "own": str(own), "alternative": str(alt), "slack": str(own-alt)})
    assert len(comparisons) == 258
    genuine = [c for c in comparisons if c["specified_action"] != c["tested_action"]]
    assert len(genuine) == 215
    z = continue_policy(())
    assert z == (0, 3, 4) and tuple(certificate["root_history"]) == z
    assert [z.count(a) for a in topics] == certificate["strategy"]["terminal_counts"]
    profits, W, OPT = terminal_payoffs[z], welfares[z], max(welfares.values())
    assert (profits, W, OPT) == ((Q(10), Q(12), Q(12)), 34, 36)
    assert list(map(str, profits)) == certificate["root_payoffs"]
    backgrounds = list(product(topics, repeat=m-1))
    theta_values = [max(terminal_payoffs[B+(a,)][-1] for a in topics) for B in backgrounds]
    theta = min(theta_values)
    assert theta == Q(12) and str(theta) == certificate["theta"]
    assert certificate["welfare"] == W and certificate["optimum"] == OPT

    def query_price(terminal, topic):
        return sum((Q(mult, 1 + sum(a in B for a in terminal))
                    for B, mult in types if topic in B), Q())

    Qz = [query_price(z, t) for t in topics]
    # Separate computation from the explicit unit-customer table.
    assert Qz == [sum((Q(1, 1 + sum(a in B for a in z)) for B in customers if t in B), Q())
                  for t in topics]
    assert Qz == list(map(Q, ["20/3", "35/4", "35/4", "22/3", "22/3", "19/2"]))
    rows = []
    for i in range(m):
        forced = [continue_policy(z[:i] + (a,)) for a in topics]
        assert forced[z[i]] == z
        # Matrix orientation is queries T by forced actions A.
        matrix = [[query_price(terminal, t) for terminal in forced] for t in topics]
        assert [matrix[t][z[i]] for t in topics] == Qz
        rows.append({"player": i+1, "actual_prefix": z[:i], "actual_action": z[i],
                     "forced_terminals_by_action": forced, "K_queries_by_actions": matrix})
    U = m * max(Qz)
    assert U == Q(57, 2) and W-U == Q(11, 2)
    return {
        "scope": "One source-bound fixed 36-unit-customer instance and the original formula complete pure SPE; all-p follows analytically after the finite replay.",
        "interest_types": [{"topics": sorted(B), "multiplicity": mult} for B, mult in types],
        "complete_formula_policy": "root 0; after (a), smallest label of opposite group; after (a,b), smallest unused label in b's group, including repeated/off-path histories.",
        "strategy_equals_frozen_certificate": True,
        "complete_actions": [{"history": h, "action": actions[h]} for h in histories],
        "actual_terminal": z, "payoffs": profits, "W": W, "OPT_3": OPT, "theta_3": theta,
        "theta_background_best_reply_distribution": Counter(map(str, theta_values)),
        "complete_deviation_comparisons": comparisons,
        "all_spe_comparisons_nonnegative": True,
        "full_rows": rows, "query_prices_at_actual_terminal_by_label": Qz,
        "all_p_proof": [
            "For each i the actual action z_i is one legal column and, after the original actual prefix z_<i, the same fixed complete policy returns Z_i(z_i)=z.",
            "Thus for every probability vector p on the six original labels, R_i(p)=min_A sum_T p_T K_i(T,A) <= sum_T p_T Q_T(z). This chooses one action before T is drawn and never exchanges min and expectation.",
            "Summing the three inequalities gives sum_i R_i(p) <= 3 sum_T p_T Q_T(z) <= 3 max_T Q_T(z)=57/2 < W=34. This is uniform over the whole probability simplex; zero query distributions are enumerated.",
        ],
        "uniform_all_p_budget_bound": U, "W_minus_uniform_bound": W-U,
        "dimensions_and_actual_work": {
            "topics": 6, "players": 3, "interest_types": len(types), "expanded_unit_customers": len(customers),
            "ordered_terminals": len(all_terminals), "complete_decision_nodes": len(histories),
            "node_action_comparisons_including_self": len(comparisons), "self_comparisons": len(histories),
            "genuine_different_action_deviations": len(genuine), "theta_backgrounds_including_repeats": len(backgrounds),
            "actual_prefix_forced_terminals": 18, "complete_K_entries": 108,
            "actual_query_values_two_methods": 6, "query_distributions_enumerated": 0,
        },
    }


def submasks(mask):
    a = mask
    while True:
        yield a
        if a == 0:
            return
        a = (a-1) & mask


def compiled_six_example():
    n, p = 6, 12
    size, X = 1 << p, (1 << n)-1
    FULL, Y = size-1, (size-1) ^ X
    F = [0] * size
    for S in range(size):
        cardinality = S.bit_count()
        if cardinality == n and (not S & X or not S & Y):
            F[S] = 1
        elif cardinality == n-1 and S & X and S & Y:
            F[S] = -1

    # Fast lower Mobius transform, then coefficient conversion.
    c = F.copy()
    lower_fast_operations = 0
    for bit in range(p):
        for A in range(size):
            if A & (1 << bit):
                c[A] -= c[A ^ (1 << bit)]
                lower_fast_operations += 1
    coeff = [0] + [((-1) ** (A.bit_count()+1)) * A.bit_count() * c[A] for A in range(1, size)]
    # Fast upper Mobius transform.  The empty coordinate is discarded, as in M1.
    x_fast = coeff.copy()
    upper_fast_operations = 0
    for bit in range(p):
        for B in range(size):
            if not B & (1 << bit):
                x_fast[B] -= x_fast[B | (1 << bit)]
                upper_fast_operations += 1
    x_fast[0] = 0

    # Independent explicit alternating subset/superset sums, not another call to
    # the fast transforms.  3^12 terms are small; no giant customer list is made.
    lower_direct_terms, upper_direct_terms = 0, 0
    c_direct = []
    for A in range(size):
        total = 0
        for T in submasks(A):
            total += (-1) ** ((A ^ T).bit_count()) * F[T]
            lower_direct_terms += 1
        c_direct.append(total)
    assert c_direct == c
    direct_coeff = [0] + [(-1) ** (A.bit_count()+1) * A.bit_count() * c_direct[A]
                          for A in range(1, size)]
    x_direct = [0] * size
    for B in range(1, size):
        total = 0
        for extra in submasks(FULL ^ B):
            total += (-1) ** extra.bit_count() * direct_coeff[B | extra]
            upper_direct_terms += 1
        x_direct[B] = total
    assert x_direct == x_fast
    M = sum(abs(v) for v in x_fast[1:])
    M_direct = sum(abs(v) for v in x_direct[1:])
    K = 6*M + 4
    r = [0] + [v+K for v in x_fast[1:]]
    assert M == M_direct == 476544 and K == 2859268
    assert all(isinstance(v, int) and v > 0 for v in r[1:])
    assert K >= 4*M+1

    # Verify both inversion identities on every relevant Boolean coordinate.
    recovered_coeff = x_fast.copy()
    for bit in range(p):
        for A in range(size):
            if not A & (1 << bit):
                recovered_coeff[A] += recovered_coeff[A | (1 << bit)]
    assert recovered_coeff[1:] == coeff[1:]
    recovered_F = c.copy()
    for bit in range(p):
        for A in range(size):
            if A & (1 << bit):
                recovered_F[A] += recovered_F[A ^ (1 << bit)]
    assert recovered_F == F

    actual = (0, 6, 7, 8, 9, 10)
    Z = sum(1 << a for a in actual)
    C = size - (1 << n)
    b = Q(C, n)
    beta = Q((1 << (p-n-1)) * ((1 << (n+1))-1), n+1)
    beta_in = (1 << (p-n)) * sum((Q(comb(n-1, j), j+2) for j in range(n)), Q())
    assert (C, b, beta, beta_in) == (4032, Q(672), Q(4064, 7), Q(3424, 7))
    covered_types = [B for B in range(1, size) if B & Z]
    signed_W = sum(x_fast[B] for B in covered_types)
    W = sum(r[B] for B in covered_types)
    assert len(covered_types) == C and signed_W == n-1
    assert W == K*C+n-1 == 11528568581
    theta = K*b+1
    assert theta == 1921428097 and n*theta-W == 1
    profits = [sum((Q(r[B], (B & Z).bit_count()) for B in range(1, size) if B & (1 << a)), Q())
               for a in actual]
    assert profits == [K*b] + [K*b+1] * (n-1) and sum(profits) == W

    query_rows, query_transform_terms = [], 0
    for t in range(p):
        bit = 1 << t
        direct_positive = sum((Q(r[B], 1+(B & Z).bit_count())
                               for B in range(1, size) if B & bit), Q())
        direct_signed = sum((Q(x_fast[B], 1+(B & Z).bit_count())
                            for B in range(1, size) if B & bit), Q())
        uniform_direct = sum((Q(1, 1+(B & Z).bit_count())
                             for B in range(1, size) if B & bit), Q())
        uniform_closed = beta_in if Z & bit else beta
        assert uniform_direct == uniform_closed
        # Expand t^k as product(1+(t-1)1_(a in B)) and use sum_(B sup A)x_B=coeff[A].
        # The integral kernels are (-1)^j/(j+1) off Z and
        # (-1)^j/((j+1)(j+2)) on Z; this avoids the x_B sum entirely.
        signed_from_coeff = Q()
        for A in submasks(Z & ~bit):
            j = A.bit_count()
            denominator = (j+1)*(j+2) if Z & bit else j+1
            signed_from_coeff += Q((-1)**j * coeff[A | bit], denominator)
            query_transform_terms += 1
        assert signed_from_coeff == direct_signed
        assert direct_positive == K*uniform_closed + signed_from_coeff
        assert abs(direct_signed) <= M
        if not Z & bit:
            assert direct_signed == F[Z | bit]-F[Z] == 0
        query_rows.append({"label": t, "in_actual_terminal": bool(Z & bit),
                           "direct_positive_type_query": direct_positive,
                           "signed_type_query": direct_signed, "signed_coefficient_integral": signed_from_coeff,
                           "uniform_direct_type_sum": uniform_direct, "uniform_closed": uniform_closed,
                           "closed_decomposition_query": K*uniform_closed + signed_from_coeff})
    U = n*(K*beta+M)
    assert U == Q(69740405760, 7) and W-U == Q(10959574307, 7)
    max_query = max(row["direct_positive_type_query"] for row in query_rows)
    assert max_query == K*beta == Q(11620065152, 7)
    assert all(row["direct_positive_type_query"] < K*beta for row in query_rows if row["in_actual_terminal"])
    tight_U = n*max_query
    assert tight_U == Q(69720390912, 7) and W-tight_U == Q(10979589155, 7)
    assert tight_U <= U < W
    return {
        "scope": "A finite n=6 arithmetic regression of the original all-n K=6M+4 family; the analytic all-n argument is separate.",
        "input_formula": {"n": n, "topic_labels": list(range(p)), "X": list(range(n)), "Y": list(range(n, p)),
                          "F": "1 for a pure-group n-subset, -1 for a mixed (n-1)-subset, 0 otherwise; F(empty)=0",
                          "c_A": "sum_(T subset A) (-1)^(|A|-|T|) F(T)",
                          "z_A": "(-1)^(|A|+1) |A| c_A for A nonempty",
                          "x_B": "sum_(A superset B) (-1)^(|A|-|B|) z_A for B nonempty",
                          "r_B": "x_B + K, K=6 sum_(B nonempty)|x_B|+4"},
        "F_value_counts": Counter(map(str, F)),
        "all_4096_c_coordinates_match_direct_subset_sums": True,
        "all_4095_nonempty_x_coordinates_match_direct_superset_sums": True,
        "both_inverse_zeta_identities_hold": True,
        "signed_x_vector_sha256_json_array_mask_order": canonical_digest(x_fast),
        "signed_x_nonempty_value_counts": Counter(map(str, x_fast[1:])),
        "M_fast": M, "M_direct": M_direct, "K": K,
        "r_B_min": min(r[1:]), "r_B_max": max(r[1:]), "every_r_B_is_positive_integer": True,
        "compressed_total_unit_customer_count": sum(r), "unit_customers_expanded": 0,
        "actual_terminal": actual, "actual_terminal_policy_source": "The source formula takes root X0, then Y0, then fresh labels of the second label's Y group. Only this path is evaluated here.",
        "positive_payoffs_direct_type_sums": profits,
        "C": C, "b": b, "beta_off_actual": beta, "beta_in_actual": beta_in,
        "signed_welfare": signed_W, "W": W,
        "theta_formula_value": theta, "n_theta_minus_W": n*theta-W,
        "theta_scope": "K*b+1 is evaluated from the original theorem. Exact minimization over all repeated n-1 backgrounds is not enumerated; the original repeated-background splitting proof supplies equality to theta_n.",
        "query_prices_by_label": query_rows,
        "uniform_all_p_budget_bound_U": U, "W_minus_U": W-U,
        "tight_max_actual_terminal_query": max_query,
        "max_query_labels": [row["label"] for row in query_rows if row["direct_positive_type_query"] == max_query],
        "tight_uniform_all_p_budget_bound": tight_U, "W_minus_tight_bound": W-tight_U,
        "tight_bound_numeric_verification": "All six unused labels have signed query 0 and total query K*beta; all six used labels have strictly smaller direct positive-type queries. Thus this n=6 type table has max_T Q_T(z)=K*beta, checked independently by coefficient integrals.",
        "all_p_budget_bridge": "For the original fixed complete compiled SPE, choose the actual action in each row, giving R_i(p)<=E_p Q_T(z). The all-type uniform query contribution is at most beta, while the signed contribution is at most M in absolute value. Therefore sum_i R_i(p)<=n(K beta+M)=U<W for every p. The finite script checks n=6 constants; the proof for every n>=3 is separate.",
        "full_SPE_legality_scope": "The existing analytic compiler and the source auxiliary complete distinct-history policy establish a full original SPE, including all repeated off-path histories. This program recomputes exact quantities and neither builds nor exhaustively certifies that enormous complete strategy.",
        "dimensions_and_actual_work": {
            "players": n, "topics": p, "Boolean_F_coordinates": size, "nonempty_interest_types": size-1,
            "lower_fast_mobius_add_subtract_operations": lower_fast_operations,
            "upper_fast_mobius_add_subtract_operations": upper_fast_operations,
            "lower_direct_subset_terms": lower_direct_terms, "upper_direct_superset_terms": upper_direct_terms,
            "complete_inverse_zeta_checks": 2, "positive_type_query_sums": p,
            "signed_type_query_sums": p, "uniform_type_query_sums": p,
            "coefficient_integral_query_checks": p, "coefficient_integral_terms": query_transform_terms,
            "query_distributions_enumerated": 0, "full_SPEs_enumerated": 0,
            "n_values_numerically_checked": [n], "LP_calls": 0, "external_solver_imports": 0,
        },
    }


def main():
    started = time.monotonic()
    prior_runs = json.loads(OUTPUT.read_text())["execution"]["successful_script_executions_in_this_report_lineage"] if OUTPUT.exists() else 0
    data, binding = source_binding()
    report = {
        "schema": 1, "task_id": TASK, "owner": "Boss3",
        "purpose": "Independent exact arithmetic evidence for fixed examples, with analytic all-p column bounds distinguished from finite computation.",
        "input_binding": binding,
        "small_36_customer_example": small_example(data),
        "all_n_family_n6_regression": compiled_six_example(),
        "execution": {
            "script": str(Path(__file__).resolve().relative_to(ROOT)),
            "script_sha256": digest(Path(__file__).read_bytes()),
            "command_from_repo_root": "python " + str(Path(__file__).resolve().relative_to(ROOT)),
            "python": platform.python_version(), "standard_library_only": True,
            "successful_script_executions_in_this_report_lineage": prior_runs+1,
            "started_and_completed_invocations_scope": "This count increments on every successful invocation preserving the sibling report; no hidden solver or prior report is executed.",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "wall_seconds": round(time.monotonic()-started, 6),
            "LP_calls": 0, "network_calls": 0, "repository_solver_imports": 0,
            "write_scope": "Only the sibling budget-example-results.json; source files and all shared registries/edges/receipts are read-only.",
        },
        "conclusion_limits": [
            "The two explicit source-bound examples have a uniform all-p SUMmin-full budget bound; this is not a proof of general SUMmin-full.",
            "The 36-customer formula policy agrees at all 43 nodes with its own original frozen certificate. It is not replaced by the separate onpath_budget_failure policy used in the older finite-query report.",
            "The n=6 arithmetic regression checks 4095 positive interest types in compressed form, not a unit expansion, not a complete SPE enumeration, and not an all-n computational proof.",
            "Both aggregate-theta counterexamples remain counterexamples to W>=n theta_n, and neither is a half-coverage counterexample.",
        ],
    }
    OUTPUT.write_text(json.dumps(exact(report), ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), "sha256": digest(OUTPUT.read_bytes()),
                      "small_Q": exact(report["small_36_customer_example"]["query_prices_at_actual_terminal_by_label"]),
                      "n6_M": report["all_n_family_n6_regression"]["M_fast"],
                      "n6_U": exact(report["all_n_family_n6_regression"]["uniform_all_p_budget_bound_U"]),
                      "successful_executions": prior_runs+1}, ensure_ascii=False))


if __name__ == "__main__":
    main()
