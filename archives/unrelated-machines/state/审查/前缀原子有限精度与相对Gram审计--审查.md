---
id: "unrelated-machines/review-prefix-atomic-relative-gram"
kind: "review"
type_tag: "审查"
title: "前缀原子有限精度与相对 Gram 审计"
status: "complete"
truth_status: "finite-exact-audit-with-sharpness-boundaries"
review_level: "full-source-read-and-independent-fraction-comparison"
scope: "三份 prefix_atomic finite precision、independent sharpness 和 relative-Gram 冻结输出"
summary: "三源均以精确 Fraction 读全。主审计覆盖500个随机树、零质量深度1..8、30个full-interval degree runs、dummy-job稀释至4096并得到tau=2^-(dummy+1)、大隐式树n=1000和四类边界；独立审计记录2377个非负截断等式、1705个精度常数检查、12152个局部极端对手。relative-Gram审计完成512个满行秩等价与512个可逆基变换核验，同时保留rank omission与absolute identity basis反例。所有源明确没有一般oracle构造、近似守恒或低阶Gram推断。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/prefix_atomic_finite_precision_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/prefix_atomic_finite_precision_independent_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/prefix_atomic_relative_gram_independent_audit.json"
evidence_manifest: "../../tools/evidence/prefix-atomic-20261030/source-manifest.json"
---

# 前缀原子有限精度与相对 Gram 审计

## 1. 对象和边界

本批研究 prefix-atomic 的局部化、根归一化、质量稀释和相对 Gram 表示。它把一个稀疏树或前缀对象拆成原子、局部器和相对基，再以精确分数检查守恒/截断恒等式。三源都把自己的身份限制为有限审计：没有一般 (P,T) oracle 构造、没有 polynomial full-promise verifier、没有 sound FAIL procedure，也没有 approximate conservation/root normalization。

原始 JSON、指纹、冻结提交和大小在 [source-manifest.json](../../tools/evidence/prefix-atomic-20261030/source-manifest.json)。本轮实际读取所有字段，并把主审计的随机/网格/大整数边界、独立截断等式和 relative-Gram 的秩反例分开归类。

## 2. 主 finite-precision 审计

`26e9...` 的 claim 是 `UM-PREFIX-ATOMIC-FINITE-PRECISION-v1`，seed=7711803，Python 3.12、Fraction。它的主要计数为：

* 500 个 random trees；
* zero-mass sharp depths 1 到 8 全列；
* 30 个 full-interval sharp runs，degree lists 包括 `[2]`, `[2,2,2]`, `[3,2]`, `[1,3,1,2]`, `[2,3,2,1]`, `[3,3,3]`；
* absolute localizer dilution 的 dummy jobs 从 0 到 12，(N=2^{d})，(	au=2^{-(d+1)})；
* 网格精确性三组 (B=0,7/11,1)，每组40 runs；另有 (n=1000) 的 large implicit tree，(N) 的二进制长度1001、alpha 分母1003、tau 分母2587；
* rare weight exponents 1、5、20、100，non-orthogonal basis `[1,2]` 和 `[3,7]`；空对象、零 optimum、一个可用端点和 unavailable edge 四个边界 fixture。

这里最清楚的可迁移算术是质量稀释：每增加一个 dummy job，(N) 翻倍、(	au) 减半，从 (1/2) 开始到 (1/8192)。它提示任何“绝对根质量自动保持”的论证都必须显式控制 dummy/zero-mass 分支；但主审计没有给出近似守恒定理。

## 3. 独立 sharpness 和极端对手

`88c...` 是独立 `Exact-statement-first` 审计，状态 `all exact finite audits passed`。它记录：

* 2,377 个带非负截断的 sharp equalities；
* 1,705 个 precision-grid constant checks；
* 12,152 个 local-extreme-error adversaries；
* 18 个 dilution examples；
* largest uniform leaf count (2^{100})（1267650600228229401496703205376）。

该源明确 `author_proof_read=False` 且 `oracle_generated_or_validated=False`。因此它是独立有限 Fraction 审计，不是对作者证明的独立认证，也不是一般 oracle 构造。它的独有价值在于把“截断保持等式”和“局部极端误差”分离记录；后续若要写普遍 bound，必须先说明这些 adversary 是否被模型排除，而不能从 `all exact finite audits passed` 直接推断。

## 4. 相对 Gram：满秩等价和两个反例

`77d...` 做了 512 个 `full_row_rank_relative_gram_equivalences` 和 512 个 `invertible_basis_congruence_checks`，并确认 `canonical_uniform_other_leaves_equals_independent_path_law` 1,023 次。它同时将两个反例布尔值设为真：`rank_omission_counterexample` 与 `absolute_identity_basis_counterexample`。

这两个反例的含义应按表示层理解：

1. 删除相对 Gram 的某些行/列可能丢掉必要的满行秩条件；低阶或删行的矩阵不能自动代表完整相对对象。
2. 把绝对 identity basis 当作所有非正交基的通用规范会失败；必须用可逆基变换下的 congruence，而不是把不同基的系数逐项相等。

512 个等价/变换检查支持有限输入的表示不变性；两个反例则阻止“只看一个简化 Gram”或“直接删 rank 行”成为一般算法。该源 scope 仍明确没有 general oracle generation/verification。

## 5. 关系、用途和未完成义务

* 与固定阶向量贪心审计的联系是“压缩表示可能丢信息”：向量贪心批次的 q/r Gram 只在列明阶数和源族上核验；本批的 rank omission 与 non-orthogonal basis 反例说明不能把低阶/绝对基证书直接推广。
* 与森林边界、配置和菜单审计的联系是边界保护：zero mass、unavailable edge、empty fixture 和 dummy dilution 都必须在配置/取整前后保持定义一致；本批没有给这些对象的联合算法。
* 与一般 approximation 的关系是负面约束：当前没有 approximate conservation、low-degree Gram inference、general (P,T) oracle 或 polynomial full-promise verifier。任何把 (	au=2^{-(d+1)}) 或 512 次 rank check 写成普遍精度/复杂度结论都超出源范围。

后续若继续，需要先给出规范化对象的完整域（包括零质量与不可用边）、证明相对 Gram 的秩条件可由输入多项式构造，再说明近似误差如何穿过 localizer dilution。当前可接续内容是有限 sharpness 和表示层障碍，不是已完成定理。

## 6. 处置

三源均已全文读取、原字节保全并与全仓矩/配置/菜单对象比较。主审计保留随机树、深度、稀释、网格和大整数边界；独立审计保留 sharp equalities、precision checks 和 local adversaries；relative-Gram 审计保留满秩/可逆变换核验及两个反例。三者合并为本审查对象，所有有限范围和一般化缺口都显式登记。
