#!/usr/bin/env python3
"""Independent Fraction precheck of the visible-maximum v2 preparation.

No builder/recovery module is imported and no optimizer is invoked. The sole
new raw row is reconstructed from Main's same-branch nested SAFE payment.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys


HERE = Path(__file__).resolve().parent
RUN = HERE.parent
REPO = HERE.parents[3]
OLD = RUN / "visible_maximum_joint"
MAIN = RUN / "main_source2_maximum_nested_safe"
ROW_NAME = "SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE"
OLD_INPUT_SHA = "b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33"
OLD_CERT_SHA = "8dd66c5c1cd3d729d262b64d6874ca9c7090952f0100c97d5ccc5397c6465347"
NEW_INPUT_SHA = "0d80f56ac0b1f82350ae5e307370d9860b21382c7059b688904230a3b80f20a4"
MAIN_MANIFEST_SHA = "3bdfeadb2ad2a48a2f9e0452bdb35dc4fe9002ec86d5aa9679950ca49188f269"
MAIN_ROW_SHA = "a852e9f8c16fa8fd8a2785034d220de1b90193036d1d4ceb9d0fe431481cd4ba"
MAIN_PROOF_SHA = "1264073e7d41a827f91031fe07d5b3138245d5590b57b3c393d06326c2986067"
THETA = F(5, 12)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def literal(value):
    # Retain dictionary insertion order and every rational coefficient string.
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def coeff(row, j):
    return F(row["a"].get(str(j), "0"))


def row_value(row, point):
    return sum((F(v) * point[int(j)] for j, v in row["a"].items()), F(0)) - F(row["rhs"])


def share(numerator, load):
    if load == 0:
        need(numerator == 0, "Nonzero numerator at zero load")
        return F(0)
    return F(numerator, load)


def psi(p, c, d, r, theta=THETA):
    r3, r4, r5, r6 = r
    load = p + c + sum(r)
    return (share(25 * c - r6 - theta * r5, load)
            + F(r3 + r4 + r5, 2) + r6
            + F(d, 6 * (p + c + r3 + r4 + r5 + 1))
            + theta * F(d, 6 * (p + c + r3 + r4 + 2)))


def minimum_parts(p, c, o):
    base = F(5 * c, 2) + F(24 * c, p + 5) + F(o, 6 * (p + 4 * c + 1))
    slope = F(o, 6 * (p + 3 * c + 2)) - F(c, 5)
    return base, slope


def bits(j):
    return [(j >> (8 - k)) & 1 for k in range(9)]


def required_row_coefficient(j):
    if j == 512:
        return F(1)
    b = bits(j)
    a, o, c = b[:6], b[7], b[8]
    p = a[0]
    return (300 * share(a[1], sum(a)) - F(288 * c, p + 5)
            - F(12 * o, 6 * (p + 4 * c + 1))
            - F(5 * o, 6 * (p + 3 * c + 2)))


def check_source_manifest():
    need(sha(MAIN / "manifest.json") == MAIN_MANIFEST_SHA, "Main manifest pin changed")
    need(sha(MAIN / (ROW_NAME + ".json")) == MAIN_ROW_SHA, "Main raw row pin changed")
    need(sha(MAIN / "proof.md") == MAIN_PROOF_SHA, "Main proof pin changed")
    manifest = read(MAIN / "manifest.json")
    checked = {}
    for name, expected in manifest["artifacts"].items():
        actual = sha(MAIN / name)
        need(actual == expected, "Main artifact hash mismatch: " + name)
        checked[str((MAIN / name).relative_to(REPO))] = actual
    for source in manifest["sources"]:
        actual = sha(REPO / source["path"])
        need(actual == source["sha256"], "Main underlying source hash mismatch")
        checked[source["path"]] = actual
    need(manifest["optimizer_calls"] == 0, "Main source is not declared zero optimizer")
    return checked


def hidden_envelope():
    source_states = read(MAIN / "hidden_state_checks.json")
    source_minima = read(MAIN / "minimum_table.json")
    need(len(source_states) == 128 and len(source_minima) == 8, "Main finite domain count mismatch")
    state_map = {(r["p"], r["c"], r["o"], tuple(r["r"])): r for r in source_states}
    minimum_map = {(r["p"], r["c"], r["o"]): r for r in source_minima}
    need(len(state_map) == 128 and len(minimum_map) == 8, "Main finite state keys repeat")
    records, minima = [], []
    endpoint_checks = 0
    for p, c, o in product((0, 1), repeat=3):
        base, slope = minimum_parts(p, c, o)
        claimed = base + THETA * slope
        observed = []
        for r in product((0, 1), repeat=4):
            cost = psi(p, c, o, r)
            residual = cost - claimed
            need(residual >= 0, "Negative independently reconstructed hidden residual")
            source = state_map[(p, c, o, r)]
            need(F(source["cost"]) == cost and F(source["minimum"]) == claimed
                 and F(source["residual"]) == residual, "Stored hidden residual differs")
            need(F(source["base"]) == psi(p, c, o, r, F(0)), "Stored hidden base differs")
            unit_increment = psi(p, c, o, r, F(1)) - psi(p, c, o, r, F(0))
            need(F(source["increment"]) == unit_increment, "Stored hidden increment differs")
            for theta in (F(0), THETA):
                need(psi(p, c, o, r, theta) >= base + theta * slope,
                     "Affine interval endpoint envelope fails")
                endpoint_checks += 1
            observed.append((r, cost))
            records.append({"p": p, "c": c, "o": o, "r": list(r),
                            "cost": str(cost), "minimum": str(claimed), "residual": str(residual)})
        actual_min = min(value for _, value in observed)
        attainers = [list(r) for r, value in observed if value == actual_min]
        need(actual_min == claimed, "Closed minimum not attained on complete hidden domain")
        source = minimum_map[(p, c, o)]
        need(F(source["m0"]) == base and F(source["slope"]) == slope
             and F(source["minimum"]) == actual_min
             and source["zero_states"] == attainers, "Stored minimum table differs")
        minima.append({"p": p, "c": c, "o": o, "minimum": str(actual_min),
                       "attaining_tail_states": attainers})
    menu_checks = 0
    for p, c in product((0, 1), repeat=2):
        for r in product((0, 1), repeat=4):
            r3, r4, r5, r6 = r
            D6, D5 = p + c + r3 + r4 + r5 + 1, p + c + r3 + r4 + 2
            for q in product((0, 1), repeat=6):
                d, o = sum(q), int(any(q))
                difference = psi(p, c, d, r) - psi(p, c, o, r)
                literal_difference = sum((F(qj, 6 * D6) + THETA * F(qj, 6 * D5)
                                          for qj in q), F(0)) - F(o, 6 * D6) - THETA * F(o, 6 * D5)
                expected = F(d - o, 6) * (F(1, D6) + THETA * F(1, D5))
                need(difference == literal_difference == expected and expected >= 0,
                     "Literal six-query weakening fails")
                menu_checks += 1
    need(menu_checks == 4096, "Six-query domain is incomplete")
    # This endpoint diagnostic is exact; it is not a parameter optimization.
    critical = (0, 0, 1, (0, 0, 1, 0))
    p, c, o, r = critical
    base, slope = minimum_parts(p, c, o)
    need(psi(p, c, o, r) == base + THETA * slope, "Critical endpoint not tight")
    need(psi(p, c, o, r, THETA + 1) - (base + (THETA + 1) * slope) == -1,
         "Critical endpoint slope mismatch")
    return {"hidden_states": 128, "minimum_types": 8, "endpoint_checks": endpoint_checks,
            "literal_six_query_checks": menu_checks, "minimum_table": minima,
            "all_hidden_residuals": records,
            "query_partition_assumed": False, "independent_query_marginals_assumed": False}


def check_new_sources(data):
    pins_path = HERE / "source_pins.json"
    need(pins_path.exists(), "New source_pins.json is not prepared")
    pins = read(pins_path)
    need(data["source_pins_sha256"] == sha(pins_path), "New source pin digest differs")
    sources = pins.get("sources", pins)
    need(isinstance(sources, dict), "New source pin map has wrong schema")
    checked = {}
    for relative, expected in sources.items():
        need(isinstance(expected, str) and len(expected) == 64, "Malformed source pin")
        actual = sha(REPO / relative)
        need(actual == expected, "New source pin hash mismatch: " + relative)
        checked[relative] = actual
    required = {
        str((OLD / "exact_input.json").relative_to(REPO)): OLD_INPUT_SHA,
        str((RUN / "visible_maximum_joint_solve/exact_certificate.json").relative_to(REPO)): OLD_CERT_SHA,
        str((MAIN / "manifest.json").relative_to(REPO)): MAIN_MANIFEST_SHA,
        str((MAIN / (ROW_NAME + ".json")).relative_to(REPO)): MAIN_ROW_SHA,
        str((MAIN / "proof.md").relative_to(REPO)): MAIN_PROOF_SHA,
    }
    for name, expected in required.items():
        need(checked.get(name) == expected, "Required source pin is absent: " + name)
    if "source_review_sha256" in data:
        need(sha(HERE / "source_review.md") == data["source_review_sha256"],
             "New source review hash mismatch")
    return checked


def run():
    need(sha(OLD / "exact_input.json") == OLD_INPUT_SHA, "Old input pin changed")
    need(sha(HERE / "exact_input.json") == NEW_INPUT_SHA, "Prepared v2 input pin changed")
    old_cert_path = RUN / "visible_maximum_joint_solve/exact_certificate.json"
    need(sha(old_cert_path) == OLD_CERT_SHA, "Old exact certificate pin changed")
    source_hashes = check_source_manifest()
    hidden = hidden_envelope()
    old, data = read(OLD / "exact_input.json"), read(HERE / "exact_input.json")
    mainrow = read(MAIN / (ROW_NAME + ".json"))
    need(data["status"] == "PREPARED_NO_OPTIMIZER" and data["optimizer_calls"] == 0,
         "New input is not preparation only")
    need(data["variables"] == 513 and data["raw_inequality_count"] == 1003
         and data["equality_count"] == 2, "New dimension contract fails")
    need(len(data["raw_rows"]) == 1003, "New raw list has wrong length")
    need(literal(data["raw_rows"][:1002]) == literal(old["raw_rows"]),
         "Old 1002 raw rows were not literally retained")
    need(literal(data["raw_rows"][1002]) == literal(mainrow),
         "Appended raw row is not literal Main source row")
    for key in ("variables", "bit_order", "atom_columns", "K_column", "nonnegative_columns",
                "objective", "equalities", "equality_count", "inequality_convention"):
        need(literal(data[key]) == literal(old[key]), "Old model field changed: " + key)
    need(data["nonnegative_columns"] == list(range(513)) and data["K_column"] == 512,
         "All nonnegative columns or independent K missing")
    need(len(data["atom_columns"]) == 512 and len(data["equalities"]) == 2,
         "Complete visible atom domain or equalities missing")
    newrow = data["raw_rows"][1002]
    need(newrow["name"] == ROW_NAME and F(newrow["rhs"]) == 0
         and F(newrow["numerical_divisor"]) == 300, "New row metadata or raw scale changed")
    need(set(newrow["a"]) == {str(j) for j in range(513)}, "New raw row does not store every column")
    coefficient_checks, elimination_checks = 0, 0
    for j in range(513):
        expected = required_row_coefficient(j)
        need(coeff(newrow, j) == expected, "Independent coefficient formula fails at " + str(j))
        if j < 512:
            b = bits(j)
            a, x, o, c = b[:6], b[6], b[7], b[8]
            atom = data["atom_columns"][j]
            need(atom == {"index": j, "old_index": j // 2, "a": a, "x": x, "o": o, "c": c},
                 "Visible type routing changed at " + str(j))
            base, slope = minimum_parts(a[0], c, o)
            minimum = base + THETA * slope
            projected_payment = 25 * share(a[1], sum(a)) - minimum
            c_equality_coefficient = F(c)
        else:
            projected_payment = F(5, 2)
            c_equality_coefficient = F(-1)
        need(expected == 12 * projected_payment + 29 * c_equality_coefficient,
             "C-size equality elimination fails at " + str(j))
        coefficient_checks += 1
        elimination_checks += 1
    need(all(coeff(newrow, j) == coeff(newrow, j ^ 4) for j in range(512)),
         "New row accidentally depends on the preserved X bit")

    old_scaling, scaling = read(OLD / "numerical_scaling.json"), read(HERE / "numerical_scaling.json")
    old_names = [r["name"] for r in old["raw_rows"]]
    new_names = [r["name"] for r in data["raw_rows"]]
    need(scaling["raw_order"] == new_names == old_names + [ROW_NAME], "Scaling/raw row order differs")
    need(len(scaling["raw_scales"]) == 1003, "Incomplete positive scaling map")
    for name in old_names:
        need(scaling["raw_scales"][name] == old_scaling["raw_scales"][name],
             "Inherited positive divisor changed: " + name)
    need(scaling["raw_scales"][ROW_NAME] == "300", "New prepared divisor is not exactly 300")
    need(all(F(value) > 0 for value in scaling["raw_scales"].values()), "Nonpositive divisor")
    source_hashes.update(check_new_sources(data))

    oldcert = read(old_cert_path)
    point = [F(v) for v in oldcert["primal"]]
    need(len(point) == 513, "Old exact point has wrong dimension")
    new_value = row_value(newrow, point)
    old_p25 = old["raw_rows"][927]
    need(old_p25["name"] == "PORTFOLIO25_i2_TC_QOmean", "Old reference P25 row changed")
    old_value = row_value(old_p25, point)
    C_size_residual = row_value(data["equalities"][1], point)
    N = sum((point[j] * F(bits(j)[7], 6 * (bits(j)[0] + 3 * bits(j)[8] + 2))
             for j in range(512)), F(0))
    K = point[512]
    need(new_value == 12 * old_value + K - 5 * N + 30 * C_size_residual,
         "Old-point direct nested diagnostic identity fails")
    markers = [p.name for p in HERE.iterdir() if p.is_file()
               and ("consumed" in p.name or p.name == "single_lp_started.txt")]
    need(not markers, "A numerical consumption marker appeared in preparation")
    return {
        "status": "PASS_PREPARED_1003_RAW_513_COLS_2_EQUALITIES",
        "optimizer_calls": 0, "optimizer_or_builder_imported": False,
        "new_input_sha256": sha(HERE / "exact_input.json"),
        "old_input_sha256": OLD_INPUT_SHA, "old_exact_certificate_sha256": OLD_CERT_SHA,
        "main_source_manifest_sha256": MAIN_MANIFEST_SHA,
        "new_row_sha256": MAIN_ROW_SHA,
        "dimensions": {"old_raw_rows_literal": 1002, "new_raw_rows": 1,
                       "total_raw_rows": 1003, "full_atom_types": 512,
                       "nonnegative_columns": 513, "equalities": 2},
        "preservation": {"all_old_raw_metadata_and_coefficient_strings": True,
                         "all_old_objective_equalities_and_column_routes": True,
                         "all_old_positive_divisors": 1002,
                         "new_positive_divisor": "300", "new_raw_row_literal_Main_copy": True,
                         "support_restriction": False, "fixed_K": False,
                         "point_completion": False, "consumption_marker_present": False},
        "independent_new_coefficient_checks": coefficient_checks,
        "independent_C_size_elimination_checks": elimination_checks,
        "C_size_elimination": "NS5 = 12*(25u2 + 5K/2 - sum minPsi) + 29*(sum c - K)",
        "hidden_envelope_and_query_checks": hidden,
        "old_exact_point_diagnostic": {
            "scope": "Evaluation only; not a feasibility completion or a new optimality claim",
            "old_objective": oldcert["objective"], "old_P25_C_Omean_slack": str(old_value),
            "C_size_equality_residual": str(C_size_residual), "K": str(K), "N": str(N),
            "new_NS5_raw_slack": str(new_value), "old_point_excluded": new_value < 0},
        "source_sha256_verified": source_hashes,
        "source_review_read": "Main proof.md, including true source2 branch, nested source5 SAFE, same terminal query budgets, and complete hidden minimum formula.",
        "scope": "Preparation only. The new necessary row is universal under its frozen source proof; no new cone optimum or SPE existence is claimed. Six-player half remains OPEN.",
    }


def main():
    try:
        result = run()
    except Exception as error:
        result = {"status": "FAIL", "error_type": type(error).__name__, "error": str(error),
                  "optimizer_calls": 0, "optimizer_or_builder_imported": False}
        (HERE / "independent_precheck_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        print(json.dumps(result, ensure_ascii=False))
        return 1
    (HERE / "independent_precheck_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    report = ["# 全可见最大 C 联合层 v2：独立准备预检", "",
              "**PASS_PREPARED_1003_RAW_513_COLS_2_EQUALITIES**；零优化器、未导入 builder 或恢复脚本。", "",
              "旧1002条原始行（含原始顺序、字段顺序、系数字符串、显式零、rhs与其余元数据）逐字面结构保留；只在原始序号1002追加 Main 冻结的新行。全部512型、独立K列、两等式和目标均原样保留。", "",
              "新行按独立公式逐列重建，513项全部匹配：", "",
              "\\[300u_2+K-288B-12M-5N\\ge0.\\]", "",
              "另外逐列验证 `NS5 = 12*(25u2+5K/2−ΣminPsi)+29*(Σc−K)`；新原行保持整数尺度，唯一新增数值正除数为300，旧1002个除数不变。", "",
              "## 真实隐藏域与六查询平均", "",
              "全部128个 `(p,c,o;r3,r4,r5,r6)` 状态重算 Psi 与精确余项，全部非负；八个类型都达到闭式最小值。对 θ=0 和 θ=5/12 的256个端点检查通过。另枚举4096个真实六查询会员状态，验证 d到o的准确非负弱化差；没有假设查询分割或独立边际。", "",
              "| p | c | o | 精确最小值 | 达到的尾状态 |", "|---:|---:|---:|---:|---|"]
    for item in result["hidden_envelope_and_query_checks"]["minimum_table"]:
        tails = ", ".join("".join(str(b) for b in r) for r in item["attaining_tail_states"])
        report.append(f"| {item['p']} | {item['c']} | {item['o']} | {item['minimum']} | {tails} |")
    d = result["old_exact_point_diagnostic"]
    report += ["", "## 已有精确点的直接代入", "",
               f"旧点在新增原行的余量为 `{d['new_NS5_raw_slack']}`。旧 P25(C,Omean) 余量为 `{d['old_P25_C_Omean_slack']}`；C大小等式余量为 `{d['C_size_equality_residual']}`。", "",
               "这只是已有精确点的代入诊断；没有求解、补全或证明新锥最优值。", "",
               "## 来源与范围", "",
               f"新准备输入 SHA256：`{result['new_input_sha256']}`。Main 新行 SHA256：`{MAIN_ROW_SHA}`；Main 来源清单 SHA256：`{MAIN_MANIFEST_SHA}`。所有声明来源哈希均已复核。", "",
               "来源付款保留同一个第二源强制C分支及其真实第五源、末源；O仅作六个合法查询并。弱平局、空覆盖、重复行动、同覆盖别名和完整有序历史范围保留。所有文件仍为 PREPARED_NO_OPTIMIZER，原六人 half 仍 OPEN。"]
    (HERE / "independent_precheck_report.md").write_text("\n".join(report) + "\n")
    print(json.dumps({k: result[k] for k in ("status", "optimizer_calls", "new_input_sha256", "dimensions")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
