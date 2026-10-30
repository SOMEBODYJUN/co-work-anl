---
id: "unrelated-machines/nearflat-hs-interface-finite-review-20261030"
kind: "review"
type_tag: "审查"
title: "近平坦 HS 矩提取与负接口有限审计"
status: "finite-audits-classified"
truth_status: "exact-fraction-conditional-extractor-with-explicit-rejection-boundary"
review_level: "full-json-read-and-cross-archive-comparison"
scope: "near-flat HS independent audit, self-contained moment extraction fixtures, and negative-interface reproducibility scope"
source_refs:
  - "source:6e5b68e01092324cf1e7:evidence/runs/unrelated_machines/near_flat_hs_independent_audit.json"
  - "source:984f155725e45efa0b41:evidence/runs/unrelated_machines/nearflat_moment_extraction_audit.json"
  - "source:f411848d34f2ee35abca:evidence/runs/unrelated_machines/negative_interface_reproduction_scope.json"
evidence_manifest: "../../tools/evidence/nearflat-hs-interface-20261030/source-manifest.json"
---

# 1. 对象身份和共同量词

本批三源研究同一类矩/PSD/HS 接口的不同层次：第一源在给定 exact distribution 上运行独立 G-HS 贪心并只对小缺陷给出条件 extractor；第二源把若干 rational matrix primitives 内置到 self-contained moment extractor，逐行检查 Schur PSD 和实际调度；第三源只保存四个相关脚本的 hash/命令元数据。

共同边界是：程序接收实际分布或 moments，不负责从任意 unrelated-machines 输入生成近平坦分布，也没有 SDP/通用 LP solver。`certificate_rejected` 或“大缺陷”只表示充分条件未满足，不能推出原输入不可行或算法失败。结果与《前缀原子有限精度与相对 Gram 审计》《重型匹配凸化与逃逸残余审计》《固定阶向量贪心与 q=13 线性缺口增量审计》相邻，但变量、矩阶和输入合同不同。

# 2. 独立 near-flat HS：21 个给定分布实例

## 2.1 算法和条件常数

`6e5b68e01092324cf1e7` 状态为 `all exact certificate-conditional assertions passed`，Fraction 精确算术，使用独立实现的“每个 job 选最大 G-HS product”贪心；不求根、不求特征值、不调用 SDP。充分条件阈值为

[
\delta\le \min\left\{\frac1{64ndR},\frac\eta{16}\right\}.
]

冻结的常数检查为 (h_{\rm lower}=961/1024)、loss numerator upper (=37/32)、loss coefficient (=1184/961<3)、at-(T) generator ratio (=67/64<3/2)。边界包括 empty jobs、(T=0) private-zero 和 (T=0) zero-effect 三个 fixture。

## 2.2 精确计数和结论

总计 21 cases，其中 2 个 `certificate_pass_cases`，且均是 genuinely nonflat certificate pass；19 个 ordinary large-defect cases。所有 ordinary large-defect outputs above (T) 的计数为 0，观察到的最大 makespan ratio 为 1，代表实例为 `macro_micro_nonflat_q_2minus30`。

两项通过的 macro/micro fixtures 是 (q=2^{-30}) 和 (q=2^{-80}) 的非平坦分布，均 (T=1,eta=1/10)，rank (M_1=6,M_2=8)，实际负载为 ((1,1/2,1/2,1/4))，精确 makespan=1；第一项阈值为 (1/19200)，第二项同样为 (1/19200)。这证明的是在两份明确 support atoms 和小 defect 条件下，所选 G-HS 贪心给出实际调度不超过 (T)。

`balanced_optimal_large_defect` 是大缺陷而非通过项：T=2、certificate_passed=false，但给定 assignment 的 loads=(2,2)，makespan=2；`general_true_T_0` 等其他大缺陷行同样不能被解读为不可能。源 scope 明确写明：small-defect conditional extractor only；large-defect runs are finite attacks，既不是一般保证也不是任意 SDP initialization 的反例。

## 2.3 数学用途和缺口

可保留的数学内容是：在给定 distribution、(T,eta,delta,n,d,R) 和 threshold 条件下，exact Schur/G-HS 计算可以验证某个实际 assignment；2 个 nonflat 通过项和 19 个大缺陷拒绝项共同把“证书适用域”与“输入不可行”分开。

未完成义务包括：near-flat distribution 的通用生成器、从 moments 反推出 support atoms、任意输入的 PSD/Schur 证书、以及 G-HS 贪心对所有 order/tie 的复杂度和近似比。不能把 21 行或两个通过项升级成 universal SDP initialization theorem。

# 3. Self-contained nearflat moment extraction：六个矩 fixture

## 3.1 运行范围

`984f155725e45efa0b41` 状态为 `all exact checks passed`，Fraction exact PSD Schur，不求特征值或 SDP；`self_contained=true`，原始矩阵 primitive 已复制到运行时。六个 cases 的 limits 明确写出：没有 general moment/nearflat generator；所有 fixtures 都是 actual distributions，extractor 接收的只是 moments；大缺陷 rejection 不是 T infeasibility certificate；有限 examples 不是 universal proof。

## 3.2 六项结果

逐项结果保留如下：

| case | T | eta | n,d,R | trace defect | ranks | 状态 |
|---|---:|---:|---|---:|---|---|
| three_point_flat_eta_half | 1 | 1/2 | 10,20,3 | 0 | (3,3) | certified actual schedule，HS²=1 |
| rare_fourth_eta_half | 1 | 1/2 | 10,20,3 | (833333333335/6944444444555555555556) | (3,4) | certified actual schedule |
| rare_fourth_eta_tenth_zero_job | 1 | 1/10 | 11,21,3 | (83333333333335/69444444444455555555555556) | (3,4) | certified actual schedule |
| rare_fourth_large_denominators | (10000000000000000000000000000000000000007/10000000000000000000000000000000000000009) | 1/10 | 10,20,3 | exact large-denominator fraction | (3,4) | certified actual schedule |
| all_zero_T | 0 | 1/10 | 4,8,3 | (5333333333552/111111111121555555555801) | (3,4) | certified actual schedule |
| uniform_nonflat_rejected | — | — | 10,20,3 | 5 | (3,4) | certificate rejected; trace defect exceeds sufficient threshold |

前五行的 `status` 都明确是“certified actual schedule; no universal small-defect generation claim”。最后一行的 reason 明确是 trace defect 超过 sufficient threshold，**no infeasibility conclusion**。因此可复用的结论是五个给定矩 fixture 的 exact schedule/Schur 证书，不能把 rejected 行写成 NO 实例。

## 3.3 与独立 HS 审计的关系

第一源运行 21 个 cases、以完整 distribution 和 G-HS product 贪心为输入；第二源运行 6 个 self-contained moment fixtures，补充 zero-T、大分母和 uniform nonflat rejection。两者不能相互替代：前者验证独立实现的条件 extractor，后者验证 primitive/moment 层的 exact Schur/PSD 计算。共同限制是没有一般矩生成器，不能从有限 fixtures 推出任意输入。

# 4. Negative interface reproduction scope

`f411848d34f2ee35abca` 不是新的数学运行，而是可复现元数据：Python 3.12.14、SciPy 1.17.0、Fraction exact（SciPy 只负责 proposal，最终由 exact primal/dual certificate 检查）、seed=20261018；列出 `normalized_gated_menu_welfare.py`、其 independent 版本、`actual_kronecker_product.py` 和 `multiwitness_shared_job_fee.py` 四条命令及 SHA-256。scope 明确为 reproducibility metadata only，不能从 finite outputs 推一般 theorem。

其独有去向是：把四个相关脚本的版本、运行命令和“无 general theorem inferred”边界固定到本批 manifest；它不重复任何一个 gated-menu、Kronecker 或 multiwitness 源的数学数据，也不能作为这些源的独立复核。后续若处理对应脚本，需另行 clean claim/show 和正文，不可把本元数据当成已处理来源的替代。

# 5. 与全仓对象、处置和接续

1. 与《前缀原子有限精度与相对 Gram 审计》：两者都使用 exact Gram/PSD 和有限精度边界，但本批的 G-HS extractor 只在给定 moments/distribution 上运行；不把相对 Gram 的 rank 失败或通过行迁移为本批的 Schur 结论。
2. 与《重型匹配凸化与逃逸残余审计》：重型批的 path-only/global filter 研究资格/配置耦合；本批研究 moments 到 assignment 的条件提取。两者都保留“局部证书不自动给全局算法”的量词，不合并 ratio。
3. 与《固定阶向量贪心与 q=13 线性缺口增量审计》：均有给定 source 和 job order 的贪心；本批的 2 个通过项和大缺陷 rejection 不产生 q/6 或一般贪心下界。
4. 与 CAG 六人目标：矩、机器和 assignment 语义与客户目录/SPE 不同，保持 unrelated-machines 隔离。

逐源处置：

- `6e5...`：集成 21 cases、2 个 conditional pass、19 个 large-defect finite attacks 和阈值常数；分类为 integrated finite conditional extractor。
- `984f...`：集成六个 self-contained moment fixtures、五个 actual-schedule certificates、一个 rejection boundary；分类为 integrated finite exact evidence。
- `f411...`：集成脚本 hash/命令的 reproducibility metadata；分类为 retained metadata，不把元数据升级为数学 theorem。

接续应先建立一般 near-flat generator 和 moment-to-support 解码，补全 certificate failure 的 fallback，再讨论统一 G-HS 调度算法。当前本批没有给出通用 SDP/LP 近似、不可行性判定或 hardness。
