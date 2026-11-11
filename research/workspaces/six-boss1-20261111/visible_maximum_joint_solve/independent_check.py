#!/usr/bin/env python3
"""Independent exact arithmetic verification of the visible-C LP certificate.

This file uses only Python's standard library. It does not import the builder,
recovery routine, scipy, or any optimizer. All raw rows and all columns are read
directly from the frozen input, including redundant and identically zero rows.
"""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import sys


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "visible_maximum_joint"
EXPECTED_INPUT = "b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33"
EXPECTED_SCALING = "b29bb0136b9153a14d223ba44eee51f5b94b607705e16b952ee147b7e2fec31c"
EXPECTED_PREPARATION = "31af8bc9ddfa35fd0a62b546cdf095fbd2cc76dfde76fc5ccfc010967f735966"
EXPECTED_SOURCE_REVIEW = "e69440b5e52b528f540605a1fd3ddc833be99a48779b265e6389a9d615067b3a"
ZERO = Fraction(0)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_vector(value, length, label):
    require(isinstance(value, list), label + " must be a full list")
    require(len(value) == length, label + " has wrong length")
    require(all(isinstance(x, str) for x in value), label + " must contain exact strings")
    return [Fraction(x) for x in value]


def sparse(value, n, label):
    require(isinstance(value, dict), label + " must be a coefficient object")
    result = {}
    for key, coefficient in value.items():
        j = int(key)
        require(str(j) == key and 0 <= j < n, label + " has invalid column")
        require(isinstance(coefficient, str), label + " contains an inexact coefficient")
        result[j] = Fraction(coefficient)
    return result


def dot(row, vector):
    return sum((value * vector[j] for j, value in row.items()), ZERO)


def run():
    hashes = {
        "exact_input.json": digest(SOURCE / "exact_input.json"),
        "numerical_scaling.json": digest(SOURCE / "numerical_scaling.json"),
        "preparation_freeze_manifest.json": digest(SOURCE / "freeze_manifest.json"),
        "source_review.md": digest(SOURCE / "source_review.md"),
        "exact_certificate.json": digest(HERE / "exact_certificate.json"),
        "independent_check.py": digest(Path(__file__)),
    }
    require(hashes["exact_input.json"] == EXPECTED_INPUT, "Frozen input hash mismatch")
    require(hashes["numerical_scaling.json"] == EXPECTED_SCALING, "Scaling hash mismatch")
    require(hashes["preparation_freeze_manifest.json"] == EXPECTED_PREPARATION,
            "Preparation manifest hash mismatch")
    require(hashes["source_review.md"] == EXPECTED_SOURCE_REVIEW,
            "Source review hash mismatch")
    data = json.loads((SOURCE / "exact_input.json").read_text())
    cert = json.loads((HERE / "exact_certificate.json").read_text())
    scaling = json.loads((SOURCE / "numerical_scaling.json").read_text())
    n, m, k = 513, 1002, 2
    require(data["variables"] == n and data["raw_inequality_count"] == m
            and data["equality_count"] == k, "Frozen dimension contract changed")
    require(data["nonnegative_columns"] == list(range(n)), "Column domain changed")
    require(data["K_column"] == 512, "K is not the independent last column")
    require(data["bit_order"] == ["a1", "a2", "a3", "a4", "a5", "a6", "x", "o", "c"],
            "Unexpected atom routing")
    require(data["inequality_convention"] == "a dot z >= rhs", "Wrong row orientation")
    require(len(data["raw_rows"]) == m and len(data["equalities"]) == k,
            "Frozen list dimensions differ")
    require(cert["input_sha256"] == EXPECTED_INPUT, "Certificate input binding mismatch")
    require(cert["optimizer_calls"] == 1, "Certificate does not declare one optimizer call")
    require(cert["variables"] == n and cert["raw_inequalities"] == m
            and cert["equality_count"] == k, "Certificate dimension mismatch")

    raw = data["raw_rows"]
    names = [row["name"] for row in raw]
    require(len(set(names)) == m, "Raw row names unexpectedly repeat")
    require(scaling["raw_order"] == names, "Scaling order mismatch")
    scales = [Fraction(scaling["raw_scales"][name]) for name in names]
    require(len(scaling["raw_scales"]) == m and all(s > 0 for s in scales),
            "Numerical scaling is not a full positive row divisor list")
    A = [sparse(row["a"], n, "raw row " + str(i)) for i, row in enumerate(raw)]
    b = [Fraction(row["rhs"]) for row in raw]
    E = [sparse(row["a"], n, "equality " + str(i))
         for i, row in enumerate(data["equalities"])]
    h = [Fraction(row["rhs"]) for row in data["equalities"]]
    require(h == [Fraction(1), ZERO], "Equality affine constants changed")
    c = sparse(data["objective"], n, "objective")
    x = exact_vector(cert["primal"], n, "primal")
    y = exact_vector(cert["dual"]["raw_row_weights"], m, "raw row dual weights")
    eta = exact_vector(cert["dual"]["equality_multipliers"], k, "free equality weights")
    stored_slacks = exact_vector(cert["raw_row_slacks"], m, "stored raw row slacks")
    stored_residual = exact_vector(cert["dual"]["nonnegative_column_residual"], n,
                                   "stored full column residuals")
    stored_eq = exact_vector(cert["equality_residuals"], k, "stored equality residuals")
    require(all(v >= 0 for v in x), "Negative primal coordinate")
    require(all(v >= 0 for v in y), "Negative raw inequality dual weight")
    # eta has no sign restriction: both normalizations are true equalities.

    slacks = [dot(row, x) - rhs for row, rhs in zip(A, b)]
    equality_residuals = [dot(row, x) - rhs for row, rhs in zip(E, h)]
    require(slacks == stored_slacks, "Stored primal slacks differ from direct raw-row sums")
    require(equality_residuals == stored_eq, "Stored equality residuals differ")
    require(all(v >= 0 for v in slacks), "A raw primal inequality is violated")
    require(all(v == 0 for v in equality_residuals), "A primal equality is violated")

    residuals = [c.get(j, ZERO) for j in range(n)]
    for weight, row in zip(y, A):
        if weight:
            for j, coefficient in row.items():
                residuals[j] -= weight * coefficient
    for weight, row in zip(eta, E):
        for j, coefficient in row.items():
            residuals[j] -= weight * coefficient
    require(residuals == stored_residual, "Stored dual residuals differ from direct raw-column sums")
    require(all(v >= 0 for v in residuals), "A raw-column dual inequality is violated")

    primal_objective = dot(c, x)
    row_rhs_objective = sum((weight * rhs for weight, rhs in zip(y, b)), ZERO)
    equality_rhs_objective = sum((weight * rhs for weight, rhs in zip(eta, h)), ZERO)
    dual_objective = row_rhs_objective + equality_rhs_objective
    require(isinstance(cert["objective"], str), "Objective must be exact")
    require(isinstance(cert["dual"]["objective"], str), "Dual objective must be exact")
    require(primal_objective == Fraction(cert["objective"]), "Primal objective mismatch")
    require(dual_objective == Fraction(cert["dual"]["objective"]), "Dual objective mismatch")
    require(primal_objective == dual_objective, "Exact primal-dual gap is nonzero")
    row_products = [weight * slack for weight, slack in zip(y, slacks)]
    column_products = [mass * residue for mass, residue in zip(x, residuals)]
    require(all(v == 0 for v in row_products), "Raw-row complementarity fails")
    require(all(v == 0 for v in column_products), "Full-column complementarity fails")
    identity_difference = (primal_objective - dual_objective
                           - sum(row_products, ZERO) - sum(column_products, ZERO)
                           - sum((a * r for a, r in zip(eta, equality_residuals)), ZERO))
    require(identity_difference == 0, "Affine dual identity fails")

    positive_rows = [{"raw_index": i, "name": names[i], "family": raw[i]["family"],
                      "raw_multiplier": str(y[i]), "raw_rhs": str(b[i]),
                      "raw_rhs_contribution": str(y[i] * b[i]),
                      "prepared_positive_divisor": str(scales[i]),
                      "equivalent_scaled_multiplier": str(y[i] * scales[i]),
                      "primal_slack": str(slacks[i])}
                     for i in range(m) if y[i] > 0]
    result = {
        "status": "PASS_FULL_RAW_EXACT_PRIMAL_DUAL",
        "arithmetic": "Python fractions.Fraction only; no tolerance-based proof checks",
        "optimizer_calls_by_this_checker": 0,
        "hashes": hashes,
        "dimensions": {"all_raw_inequalities": m, "all_nonnegative_columns": n,
                       "free_equality_multipliers": k},
        "objective": str(primal_objective), "objective_approximation": float(primal_objective),
        "dual_affine_row_rhs_contribution": str(row_rhs_objective),
        "dual_affine_equality_rhs_contribution": str(equality_rhs_objective),
        "duality_gap": "0", "affine_identity_difference": "0",
        "minimum_primal_coordinate": str(min(x)), "minimum_raw_row_slack": str(min(slacks)),
        "minimum_dual_weight": str(min(y)), "minimum_column_residual": str(min(residuals)),
        "primal_positive_columns": [j for j in range(n) if x[j] > 0],
        "dual_positive_raw_rows": positive_rows,
        "zero_column_residual_indices": [j for j in range(n) if residuals[j] == 0],
        "strictly_positive_column_residuals": sum(v > 0 for v in residuals),
        "tight_raw_inequalities": sum(v == 0 for v in slacks),
        "all_raw_row_slacks": [str(v) for v in slacks],
        "all_column_dual_residuals": [str(v) for v in residuals],
        "equality_residuals": [str(v) for v in equality_residuals],
        "free_equality_multipliers": [str(v) for v in eta],
        "raw_row_complementarity": {"checked": m, "all_zero": True},
        "column_complementarity": {"checked": n, "all_zero": True},
        "nonzero_affine_rhs_rows": [{"raw_index": i, "name": names[i], "rhs": str(b[i])}
                                    for i in range(m) if b[i] != 0],
        "scope": "Exact optimality of the frozen full necessary cone only. This is not a complete pure SPE existence certificate, and it does not settle the six-player half conjecture.",
    }
    return result


def main():
    try:
        result = run()
    except Exception as error:
        result = {"status": "FAIL", "error_type": type(error).__name__, "error": str(error),
                  "optimizer_calls_by_this_checker": 0}
        (HERE / "independent_check_result.json").write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        print(json.dumps(result, ensure_ascii=False))
        return 1
    (HERE / "independent_check_result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    report = [
        "# 可见真最大 C 联合必要锥：独立精确证书核验", "",
        "状态：**PASS_FULL_RAW_EXACT_PRIMAL_DUAL**。本核验器只使用 Python 标准库与 Fraction；未导入 builder、recover 或任何优化器。", "",
        "## 全域与仿射核验", "",
        f"逐项重算全部 **1002** 原始不等式、**513** 非负列、**2** 自由等式付款。所有原始零行、重复行、rhs=-1 的上帽和 K 独立列均保留。", "",
        f"精确原始/对偶共同目标：`{result['objective']}`，约 `{result['objective_approximation']:.17g}`。", "",
        f"对偶原始行 rhs 贡献为 `{result['dual_affine_row_rhs_contribution']}`；等式 rhs 贡献为 `{result['dual_affine_equality_rhs_contribution']}`。两自由等式付款为 `{result['free_equality_multipliers']}`。", "",
        "对每行重算 a_i·z-b_i；对每列重算 c_j-Σ_i y_i a_ij-Σ_k η_k e_kj。前者、非负原始变量、原始行付款、后者均非负；两等式余量均为零。所有1002个行互补积和513个列互补积均精确为零。", "",
        f"正付款原始行数 `{len(result['dual_positive_raw_rows'])}`；正原始坐标数 `{len(result['primal_positive_columns'])}`；零列余量数 `{len(result['zero_column_residual_indices'])}`；紧原始不等式数 `{result['tight_raw_inequalities']}`。", "",
        "## 原尺度付款", "",
        "数值层若以正除数 d_i 除完整原行，则其非负付款为 λ_i=d_i y_i；因此原始付款 y_i=λ_i/d_i。本检查以未经缩放的 frozen raw 系数直接重建对偶，正付款表同时列出两尺度以免混用。", "",
        "| 原始序号 | 原始名称 | 原始付款 y_i | 正除数 d_i |", "|---:|---|---:|---:|",
    ]
    for row in result["dual_positive_raw_rows"]:
        report.append(f"| {row['raw_index']} | `{row['name']}` | {row['raw_multiplier']} | {row['prepared_positive_divisor']} |")
    report += ["", "## 结论边界", "",
               "本结果建立冻结全必要锥的精确最优性。其对原模型的普遍下界用途仍依赖已冻结且另行审查的真实来源推导。本检查没有构造完整有序历史纯 SPE，也没有把最优点的有理原子重数解释为一份可实现 SPE。原六人 half 仍为 OPEN。", "",
               "## 文件绑定", "", "| 文件 | SHA256 |", "|---|---|"]
    report += [f"| `{name}` | `{sha}` |" for name, sha in result["hashes"].items()]
    (HERE / "independent_checker_report.md").write_text("\n".join(report) + "\n")
    print(json.dumps({key: result[key] for key in ["status", "objective", "objective_approximation",
                       "duality_gap", "dimensions", "optimizer_calls_by_this_checker"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
