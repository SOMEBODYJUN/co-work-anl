---
id: "weighted-congestion/ordinal-potential-finite-checks-faulhaber-power-obstruction-three-source-review"
kind: "review"
type_tag: "审查"
title: "序势独立有限核验与 Faulhaber 幂目标障碍三源审查"
status: "finite-evidence-integrated"
summary: "整合三份 ordinal-potential 冻结 JSON：298 项独立 Fraction 核验、Faulhaber 方法失败的 170 项精确见证，以及幂目标把唯一最小点固定在坏状态的有限障碍族；不把方法障碍升级为 weighted-congestion 全类无均衡或近似定理。"
truth_status: "exact-finite-checks-and-explicit-method-obstruction-only"
review_level: "full-json-read-legacy-main-byte-equality-and-cross-review"
scope: "ordinal potential finite bundle bridge, Faulhaber failure witness, and power-objective bad-minimizer obstruction"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/weighted_congestion/ordinal_potentials/finite_bundle_independent_checks.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/weighted_congestion/ordinal_potentials/finite_bundle_independent_checks.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/weighted_congestion/ordinal_potentials/full_faulhaber_failure.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/weighted_congestion/ordinal_potentials/full_faulhaber_failure.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/weighted_congestion/ordinal_potentials/power_objective_exact_checks.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/weighted_congestion/ordinal_potentials/power_objective_exact_checks.json"
source_ids:
  - "0ea5ba04b51aaf4b9134"
  - "124e7e206a2e649e46cf"
  - "3536c2043d899ddccae1"
evidence:
  source_sha256:
    finite_bundle_independent_checks: "c2c594597b929bd99821a7c15ab69b66847fb0d0f9b6140f90edb567f8ba0422"
    full_faulhaber_failure: "4a05a49d0cfb80475053c6837002fe2f2f32c4d7f961f11031b78dc88ebe57f2"
    power_objective_exact_checks: "c2c97dc2c94dbd04e1f0b7ff25b1c369cdc52264d3fc9acf34dc9a917043a671"
  legacy_main_byte_equal: true
---

# 实读与对象分层

三份 JSON 的 legacy/main 同路径内容逐字节相同。本文逐字段读取 `finite_bundle_independent_checks`、`full_faulhaber_failure` 和 `power_objective_exact_checks`，并回读 weighted-congestion 的 ordinal-potential README、幂桥与共同幂混合审查、潜在用户密度势、线性全状态攻击和固定权重升幂障碍。三源承担不同角色：第一份是小范围精确核验，第二份是某种 Faulhaber/幂和证明路线的明确方法障碍，第三份是若干显式游戏中“总幂成本唯一最小点是坏状态”的精确有限障碍。它们不能合并成一个全类定理。

## 1. finite_bundle_independent_checks：298 项精确检查

源声明 Python `Fraction` 精确算术、无 seed、无数值容差，复现命令为 `verify_finite_bundle_bridge.py --repo .`，结果是 `PASS 298 independent exact finite checks`。细分为：path sums and monotonicity 180 项、finite bundle floor bounds 54 项、resource permutation averages 64 项。它还引用 `verify_multipliers.py` 作为依赖并记录两个 code SHA。

可采纳内容是：在脚本明确生成的有限 bundle、插入比率、资源置换平均和路径和对象上，精确等式/不等式通过。`not_checked` 明确排除巨大完整游戏展开、全类 `O(d/log d)` 界和新颖性认证；故该源可作为已有序势/幂桥正文的实现核验附件，不能代替“任意 degree/任意资源族”的证明。

## 2. full_faulhaber_failure：方法障碍而非目标结论

源使用 `fractions.Fraction` 和精确 Bernoulli recurrence，共 170 项检查，给出两个可复核负见证：degree 14、`x=3/2` 的 normalized derivative 为 `-19246442/43046721`；degree 20、`x=6/5` 的 Faulhaber value 为 `-19909582690061549/476837158203125`。这说明试图用该全幂和/Faulhaber 单调性路线时，候选单调性或正性在明确参数上失败。

正确处置是“该证明路线被有限精确反例击穿”：它不证明 weighted-congestion 无均衡、不证明任何近似下界，也不否定其他排序势、局部幂矩、线性重置或全状态编译方法。已有 `幂桥与共同幂混合` 审查中的尺度兼容和目标分层应保留；不能把方法失败改写成模型失败。

## 3. power_objective_exact_checks：幂目标的显式坏最小点

源 claim 为 `WC-R1-TOTAL-COST-POWER-OBSTRUCTION-v1`，使用 exact Fraction 与 radical squaring。第一族 `q=1/2`、`r=2,3,5,10` 分别有 19、73、289、1459 名玩家/资源，improvement ratio 为 `4,9,25,100`；坏状态目标值依次 `5,9,17,37`，好状态为 `1+3√2, 1+6√2, 1+12√2, 1+27√2`，正根比较平方给出 `16<18`、`64<72`、`256<288`、`1296<1458`。第二族 `q=2`、`R=2,3,10,100,1000` 保持 2 玩家/3 资源，improvement ratio 为 `2,3,10,100,1000`；坏/好目标差恒为 `7/4`。每一行都记录 `unique_objective_minimizer_is_bad=true` 和 `good_state_is_exact_PNE=true`。

这些行支持一个明确的目标障碍：只最小化所写总幂成本时，有限构造的唯一最小点可能是坏状态，即存在更好 PNE 但幂目标把搜索导向坏点。它不等于“游戏没有 PNE”，也不等于任意序势都会失败；`good_state_is_exact_PNE` 正好保留了这一差别。有限参数、给定资源模板和精确平方比较不能外推到所有 weighted-congestion 游戏。

# 关系、缺口与处置

* 第一源是实现/有限证据，第二源否定一条证明方法，第三源否定一种具体全局幂目标选择器；三者量词不同。
* 与已有“密度矩与幂桥有限审计”“幂桥与共同幂混合的版本和证明范围”“线性全状态族的三路独立攻击”相比，本批新增的是 298 项独立 finite bundle 检查、Faulhaber 的明确负见证和总幂目标坏最小点族。它们不应被重复写成同一个 `ordinal-potential` 定理。
* 固定有限正权向量的高次极限、局部幂矩证书、线性全状态负结果和本批 power-objective obstruction 必须保持各自模型/量词；不能从 `good_state_is_exact_PNE` 直接导出 CAG/SPE 覆盖结论。

三源均 `integrated` 到本审查。保留 SHA、精确数值、复现命令和未检查项；未删除失败路线，也未把有限检查、方法反例或目标选择器障碍升级为一般 weighted-congestion 无均衡/近似或硬度结论。
