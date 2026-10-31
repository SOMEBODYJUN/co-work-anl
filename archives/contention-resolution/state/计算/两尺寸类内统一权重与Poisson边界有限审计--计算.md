---
id: contention-resolution/two-size-uniformization-and-poisson-boundary-finite-audit
kind: computation
type_tag: 计算
title: 两尺寸类内统一权重与Poisson边界有限审计
status: finite-numeric-evidence-retained
truth_status: fixed-x-obstruction-supported; no-global-theorem
review_level: full-json-read-field-and-scope-audit
scope: "two_class_attack.json 的60个两尺寸固定激活LP案例、3个统一权重违反例和Poisson边界网格最小值"
summary: "冻结 JSON 记录 seed=20261020、scipy.optimize.linprog HiGHS、60个有限案例；3个固定x类内统一权重违反例的ratio差异，以及Poisson边界网格最小值约0.4323323584。所有数值为有限浮点实验，不能替代Fraction全域证明或一般CRS定理。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/probes/gap_tools/two_class_attack.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/probes/gap_tools/two_class_attack.json"
---

# 两尺寸类内统一权重与Poisson边界有限审计

本文完整读取冻结 two_class_attack.json（33,520 bytes，SHA-256 77cb6669ef733ebf74c1a8484d2c670696e1dd962679a2ffa8d06057283c8712）。JSON 明确写出 seed=20261020、solver=scipy.optimize.linprog HiGHS、cases=60、uniformization_violations=3、poisson_boundary_grid_min 和警告 “Finite numeric experiments; not a theorem.” 本页保留该计算证据，并与[两尺寸固定激活的类内统一权重障碍](../资料/两尺寸固定激活的类内统一权重障碍--资料.md)和第二轮 GAP 候选边界对照。

## 1. 60 个有限案例

所有记录均使用两尺寸 \(a=0.7,b=0.4\)，并按 \(na=1\) 或 \(na=2\) 生成有限激活向量。每个 case 包含：

* 激活概率向量 \(x\)；
* 自然 LP 值 lp；
* 一组一般物品权重 \(w\)；
* 类内统一正权、允许零权 sub-support 下的最小值 class_uniform_subsupport；
* 达到该统一权的 uniform_w 向量。

JSON 中的数字是 scipy/HiGHS 浮点输出，没有给出 Fraction 输入、LP basis、容差或代码 hash；本文不把小数精度升级为精确有理证书。60 个 case 的作用是搜索和展示障碍，不能替代对所有 \(x,w\) 的证明。

## 2. 三个固定 \(x\) 统一化违反例

JSON 的 uniformization_violations 有三项，均 \(a=0.7,b=0.4,na=2\)。它们分别记录一般权重下的 lp ratio 与类内统一权下的 ratio：

| case | 一般权重 \(w\) | 一般 ratio | 统一权 ratio | 差值方向 |
|---|---|---:|---:|---|
| 1 | \((0.6287492445869991,0.6287492445869991,0.31437462229349955,0.3143746222934996,0.6287492445869991)\) | 0.6223869665566326 | 0.6237423913580311 | 统一化更高 |
| 2 | \((0.6216019952614107,0.6216019952614107,0.6216019952614107,0.31080099763070534,0.3108009976307054,0.31080099763070534)\) | 0.6136396938775959 | 0.6140944166301745 | 统一化更高 |
| 3 | \((0.6422295834470457,0.6422295834470457,0.32111479172352286,0.32111479172352286,0.3211147917235229,0.6422295834470457)\) | 0.6056800554818468 | 0.6069754722974093 | 统一化更高 |

为避免把“违反”抽象成只剩一个比值，原 JSON 的对应激活向量和类内统一权向量也逐项保留：

| case | 激活向量 \(x\) | `uniform_w` |
|---|---|---|
| 1 | \((0.6039587419285117,0.26501347199634,0.1742916514030521,0.34133169306622746,0.4636752811622301)\) | \((2,2,1,1,1)\) |
| 2 | \((0.5705298163278757,0.32543818271130415,0.4935008899773312,0.37008628516901304,0.030363338671663635,0.03810548786342725)\) | \((1,1,1,0,0,0)\) |
| 3 | \((0.49257240930888635,0.4541765470550515,0.09537920410924455,0.22372149956851803,0.14662470532324684,0.3774639173620994)\) | \((1,1,1,1,1,1)\) |

三项违反例的统一权向量允许零坐标（即 sub-support），和一般权向量长度分别为 5、6、6；因此它们是同一固定激活向量上的直接 LP 比较，而不是在不同物品数之间的比较。

这些数值与现有 exact 资料对象中的 Fraction 反例方向一致，但 JSON 本身只提供有限浮点搜索。现有资料的连续权比端点论证和完整 sub-support 枚举承担固定 \(x\) 族的精确证明；本 JSON 不新增全域量词，也不反驳同时改变 \(x\) 的全局 uniformization 猜想。

## 3. Poisson 边界网格

poisson_boundary_grid_min 为：

\[
\text{minimum}=0.4323323583816936,\qquad
(X,Y,na,nb)=(2.0,0.0,1,1).
\]

这里的 \(X,Y\) 和 \(na,nb\) 是该有限网格实验的边界参数。JSON 未提供网格全集、步长、LP 容差或随机种子之外的生成代码，因此只能把该最小值作为记录的有限边界观察。它不能证明 \(0.4323\) 的全局下界、Poisson 化极限、或两尺寸 knapsack 的近似比。

## 4. 证据边界和处置

本 JSON 的 solver、seed、60 case、3 violation 和 boundary minimum 已逐字段保存。它与现有固定 \(x\) Fraction 障碍的关系是“独立有限数值支持”，不是替代关系；两者都不能推出一般 CRS、monotone CRS、改变 \(x\) 的全局近似定理或新颖性。JSON 警告本身要求把结果标为 finite numeric experiments。

本源处置为 retained 计算证据。第三阶段可将本页连接到固定 \(x\) 类内统一权重障碍和 C08 候选边界，关系类型应标为“有限搜索/反例线索”；不能把浮点 ratio 或 Poisson 网格最小值写成精确理论常数。
