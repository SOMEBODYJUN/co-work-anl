#!/usr/bin/env python3
"""Generate all137 parameter vertices times8 legal targets, without a solver.

Read only point-free mathematical sources. Source2's frozen28 vertices are
reused, not rediscovered. The original K and |T| terms remain separate.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SOURCE2 = HERE.parent / "source2_minimal_cap_safe"
TARGETS = ["A" + str(j) for j in range(1, 7)] + ["X", "C"]
PINS = {
    "freeze_manifest.json": "d63c117b0adf2353f70ffaf7d959dd91e8c4ee378838f7e5f4af6e99c86861ec",
    "proof.md": "e0686cf9db0ab9611eea9852a2e56141e24d9011d124ec2a881a10c8dc5f48d6",
    "exact_family.json": "dfdadf4dec0cc1b135cb015fc60ba92f2208a8678a02835003213faefdc3161f",
    "parameter_polytope.json": "a7e0cd2a4aa0622538fd9f5bcc31d0c007d38a7e3b6e0977aac221f4058075f6",
    "coordinate_contract.json": "e644b3e2d24379432684361168fa4313b41e9452a8dc68348881a9dd86fbb0e1",
    "literal_checker_output.json": "687b71d5f7a42d5df2c866e6bbae0f46f49a892ab38d0dcf6ba53f2401d12fe5",
}


def read(path):
    return json.loads(path.read_text())


def write(name, value):
    with (HERE / name).open("x") as out:
        out.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def parameters(source, vector):
    tau = dict(zip(range(source + 1, 6), vector[:-1]))
    s = vector[-1]
    beta = {j: F(1, 12) + tau[j] + sum((tau[k] / (6 * (7-k) * (8-k))
                                      for k in tau if k > j), F(0)) for j in tau}
    a = 25 + sum(tau.values(), F(0)) - s
    S = 1 + sum(beta.values(), F(0))
    return tau, s, beta, a, S


def main():
    for name, expected in PINS.items():
        assert sha256((SOURCE2 / name).read_bytes()).hexdigest() == expected, name
    owned = read(HERE / "parameter_domains.json")
    frozen = read(SOURCE2 / "parameter_polytope.json")
    frozen_family = read(SOURCE2 / "exact_family.json")
    source_families = {item["source"]: item for item in owned["sources"]}
    imported = []
    for position, old in enumerate(frozen["vertices"]):
        vector = list(map(F, old["tau3_tau4_tau5"] + [old["s"]]))
        tau, s, beta, a, S = parameters(2, vector)
        assert a == F(old["source_IC_weight"])
        assert S == F(old["true_tail_K_weight"])
        assert list(beta.values()) == list(map(F, old["beta3_beta4_beta5"]))
        assert S-s/5 == F(old["C_size_free_multiplier"])
        imported.append({
            "id": "MINCAP_I2_V" + format(position, "03d"),
            "frozen_source2_vertex_id": old["id"],
            "parameters": list(map(str, vector)),
            "tau_by_true_source": {str(j): str(tau[j]) for j in tau},
            "s": str(s), "source_IC_weight": str(a),
            "middle_CAP_weights": {str(j): str(beta[j]) for j in beta},
            "terminal_CAP_weight": "1", "terminal_BR_average_weight": "1",
            "total_K_weight": str(S), "active_halfspaces": old["active_facets"],
        })
    source_families[2] = {
        "source": 2, "middle_sources": [3, 4, 5],
        "parameter_order": frozen["parameter_order"], "dimension": 4,
        "D_values": [5, 6], "complete_domain_halfspaces": frozen["facets"],
        "all_listed_halfspaces_are_facets": True,
        "strict_interior": frozen["strict_interior"],
        "vertices": imported, "enumeration_reused_from_frozen_source": True,
        "frozen_parameter_polytope_sha256": PINS["parameter_polytope.json"],
        "explicit_source_IC_nonnegative_condition": {
            "formula": "25+sum(tau)-s>=0", "included_in_original_contract": True,
            "redundant_on_complete_domain": True, "exact_minimum": "16"},
    }
    write("parameter_families.json", {
        "status": "FIVE_COMPLETE_PARAMETER_DOMAINS_ALL137_VERTICES_NO_POINT",
        "sources": [source_families[i] for i in range(1, 6)],
        "source2_domain_reused_not_rediscovered": True,
        "nonnegative_source_IC_condition_retained": True,
        "optimizer_calls": 0,
    })

    atoms = []
    for index, bits in enumerate(product([0, 1], repeat=9)):
        atoms.append({"index": index, "old_index": index // 2,
                      "a": list(bits[:6]), "x": bits[6], "o": bits[7], "c": bits[8]})
    frozen_coordinates = read(SOURCE2 / "coordinate_contract.json")
    assert atoms == frozen_coordinates["atom_columns"]
    ceq = {str(atom["index"]): str(atom["c"]) for atom in atoms}
    ceq["512"] = "-1"
    assert ceq == frozen_coordinates["C_size_equality"]["a"]
    coordinate_contract = {
        "variables": 513, "K_column": 512,
        "bit_order": ["a" + str(j) for j in range(1, 7)] + ["x", "o", "c"],
        "atom_columns": atoms, "C_size_equality": {"a": ceq, "rhs": "0"},
        "full_domain_including_zero_and_o0": True,
        "no_fixed_support_or_fixed_K": True,
        "C_equality_not_used_in_general_rows": True,
        "legal_forced_targets": TARGETS,
        "query": "Mean of six legal labels; o is their union, not a legal action assumption.",
        "numerical_divisor": "25", "raw_scale": "terminal BR mean and terminal CAP each weight1",
    }
    write("coordinate_contract.json", coordinate_contract)

    rows, catalogue, identity, endpoint_lines = [], [], [], []
    seen = {}
    duplicates = []
    per_source = {}
    frozen_by_id = {row["vertex_id"]: row for row in frozen_family["rows"]}
    for source in range(1, 6):
        family = source_families[source]
        per_source[str(source)] = {
            "dimension": family["dimension"],
            "facets": len(family["complete_domain_halfspaces"]),
            "vertices": len(family["vertices"]), "raw_rows": 8 * len(family["vertices"]),
        }
        for vertex in family["vertices"]:
            vector = list(map(F, vertex["parameters"]))
            tau, s, beta, a, S = parameters(source, vector)
            assert a >= 0 and all(value >= 0 for value in tau.values())
            assert all(value >= 0 for value in beta.values())
            endpoint_lines.append("| " + " | ".join([
                str(source), vertex["id"], ", ".join(map(str, vector[:-1])) or "—",
                str(s), str(a), str(S)]) + " |")
            for target in TARGETS:
                coefficients = {}
                for atom in atoms:
                    actual = atom["a"]
                    actual_load = sum(actual)
                    actual_share = F(actual[source-1], actual_load) if actual_load else F(0)
                    p = sum(actual[:source-1])
                    n = 6-source
                    D = p+n+1
                    t = actual[int(target[1:])-1] if target.startswith("A") else atom[target.lower()]
                    o = atom["o"]
                    value = a * actual_share - S*t - F(24*t, D) + s*F(t, min(D, 5))
                    value -= F(o, 6*(p+1+n*t))
                    value -= sum((tau[j] * F(o, 6*(p+(j-source)*t+7-j)) for j in tau), F(0))
                    coefficients[str(atom["index"])] = str(value)
                coefficients["512"] = str(S)
                position = len(rows)
                name = "SOURCE" + str(source) + "_MINIMAL_CAP_INTERNAL_SAFE_" + vertex["id"].split("_")[-1] + "_T_" + target + "_Q_OMEAN"
                metadata = {
                    "raw_row_index": position, "name": name,
                    "family": "ALL_SOURCE_MINIMAL_CAP_TRUE_INTERNAL_SAFE",
                    "source": source, "vertex_id": vertex["id"], "forced_target": target,
                    "query": "six_legal_query_union_mean", "parameters": vertex["parameters"],
                    "tau_by_true_source": vertex["tau_by_true_source"], "s": str(s),
                    "source_IC_weight": str(a), "middle_CAP_weights": vertex["middle_CAP_weights"],
                    "terminal_CAP_weight": "1", "terminal_BR_average_weight": "1",
                    "total_K_weight": str(S), "rhs": "0", "numerical_divisor": "25",
                    "H_denominator": "min(p+7-source,5)", "C_size_equality_eliminated": False,
                }
                rows.append({**metadata, "a": coefficients})
                catalogue.append(metadata)
                signature = tuple(coefficients[str(j)] for j in range(513))
                if signature in seen:
                    duplicates.append({"retained_row": position, "equal_to_prior_row": seen[signature]})
                else:
                    seen[signature] = position
                if source == 2 and target == "C":
                    old = frozen_by_id[vertex["frozen_source2_vertex_id"]]
                    mu = S-s/5
                    residuals = [F(coefficients[str(j)])-F(old["a"][str(j)])+mu*F(ceq[str(j)]) for j in range(513)]
                    assert not any(residuals)
                    identity.append({"new_row": name, "old_row": old["name"],
                                     "frozen_vertex_id": old["vertex_id"], "mu": str(mu),
                                     "identity": "R_general=R_C_only-mu*(|C|-K)",
                                     "all513_residuals": list(map(str, residuals))})
    assert len(rows) == 1096 and len(identity) == 28
    assert sum(1 for item in identity if F(item["mu"]) < 0) == 1
    assert any(item["mu"] == "-11/20" for item in identity)
    write("exact_family.json", {
        "schema": "five_source_minimal_cap_safe_1096x513_v1",
        "status": "POINT_FREE_FULL_FAMILY_GENERATED_NO_OPTIMIZER",
        "raw_rows": len(rows), "variables": 513, "K_column": 512,
        "inequality_convention": "a dot z >=rhs", "numerical_divisor": "25",
        "complete_finite_generator_for_specified_affine_domains_and_eight_targets": True,
        "per_source": per_source, "rows": rows,
        "target_selection_or_point_filtering": False, "optimizer_calls": 0,
    })
    write("row_catalogue.json", catalogue)
    write("source2_C_identity.json", {
        "status": "PASS", "identity": "R_general=R_C_only-(S-s/5)*E_C",
        "C_equality_convention": "E_C=|C|-K", "free_multiplier_may_be_negative": True,
        "signed_identity_columns": 28*513, "rows": identity,
    })
    write("raw_duplicate_report.json", {
        "raw_rows": len(rows), "distinct_vectors": len(seen),
        "duplicates": duplicates, "all_rows_retained": True,
        "linear_independence_not_claimed": True,
    })
    write("H_denominator_contract.json", {
        str(i): [{"p": p, "D": p+7-i, "denominator": min(p+7-i, 5),
                  "excess_above_t_over5": str(F(1, min(p+7-i, 5))-F(1, 5))}
                 for p in range(i)] for i in range(1, 6)
    })
    (HERE / "endpoint_tables.md").write_text(
        "# 全部 137 个参数顶点\n\n所有顶点均用于 A1,...,A6,X,C 八个合法纯目标。S 是未消元的真实大小帽总额。\n\n"
        "| 源 | 顶点 | τ（按真实内部源递增） | s | 源 IC 权 a | 原 K 权 S |\n"
        "|---:|---|---|---:|---:|---:|\n" + "\n".join(endpoint_lines) + "\n")
    source_paths = [SOURCE2 / name for name in PINS]
    source_paths += [SOURCE2 / "derivation_result.json", SOURCE2 / "source_manifest.json",
                     HERE.parent / "all_source_joint_reweighted_safe/proof.md",
                     REPO / "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md"]
    write("family_source_manifest.json", {
        "sources": {str(path.relative_to(REPO)): sha256(path.read_bytes()).hexdigest() for path in source_paths},
        "authorization": "Main expressly released all eight legal pure targets for source2 and the full five-source family before this generation.",
        "source2_import": "Frozen28 parameter vertices; generalized from pre-C-equality budget, never by relabelling a reduced C-only row.",
        "numeric_input_or_candidate_read": False, "optimizer_calls": 0,
    })
    result = {"status": "PASS_GENERATED_ALL1096_RAW_ROWS_NO_SOLVE", "sources": 5,
              "vertices": 137, "raw_rows": len(rows), "columns": 513,
              "raw_coefficients": len(rows)*513, "numerical_divisor": "25",
              "per_source": per_source, "source2_C_signed_identity_columns": 28*513,
              "source2_domain_reenumerated": False, "optimizer_calls": 0,
              "numeric_input_or_candidate_read": False}
    write("family_build_result.json", result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
