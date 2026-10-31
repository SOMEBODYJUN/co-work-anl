---
id: "unrelated-machines/review-uniform-cardinality-sparse-support-author-proof-read-after"
kind: "review"
type_tag: "审查"
title: "均匀定基数稀疏支撑作者证明 read-after 审查"
status: "reviewed-no-fatal-gap-in-scoped-proof"
truth_status: "scope-confirmed"
review_level: "full-source-read-author-proof-attack"
summary: "对均匀定基数 first/pair 稀疏支撑递归证明的完整读后审查：候选列始终显式，超几何分块给出可行见证，基本有理 LP/消列与缓存递归承担 poly(d) 位复杂度；未发现其声明范围内的致命缺口。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_uniform_pair_sparse_root_proof_read_after_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_uniform_pair_sparse_root_proof_read_after_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/boss11_uniform_cardinality_pair_sparse_support_proof_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/boss11_uniform_cardinality_pair_sparse_support_proof_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_uniform_cardinality_pair_design_independent_reconstruction_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_uniform_cardinality_pair_design_independent_reconstruction_v1.md"
legacy_ids:
  - "UM-UNIFORM-CARDINALITY-PAIR-SPARSE-SUPPORT-READ-AFTER-v1"
---

# 审查对象与版本

本文件审查冻结源 `sol_uniform_pair_sparse_root_proof_read_after_v1.md`（源 ID `ba98d4f6d89c0be1ecf2`，SHA-256 `b5d61a931c29de5fc10be789d972a7750ba343311968e9b5807228304e690d57`）。该源明确记载：先独立读取 statement，随后完整读取作者 Proof，再逐段攻击其正确性、递归规模和位复杂度；它不是作者原证明的摘要，也没有运行软件。作者 Proof 的被审对象为 `boss11_uniform_cardinality_pair_sparse_support_proof_v1.md`，SHA-256 `f3d759b4a0e147ab215f2aa1c09f72aca5aeda687426a3adac3ce2643fc28274`。与之比较的独立 statement-first Fisher–Yates 重构为 `sol_uniform_cardinality_pair_design_independent_reconstruction_v1.md`，源 ID `b8137e324aa77306db69`。

现有 canonical theorem《均匀定基数 first/pair 稀疏支撑》已经给出同一稳定对象的量词、递归、基本解和 scope 边界。本审查不另造一个定理，也不把 read-after 攻击升格为新的构造；其独有内容是对作者 Proof 的完整阅读、潜在隐式 oracle/位长漏洞的逐点核对，以及与 Fisher–Yates 路线的范围比较。

## 被核对的精确声明

给定显式正整数 \(d\) 和 \(0\le h\le d\)，令
\[
D_d=1+d+\binom d2.
\]
在按显式 \(d\) 的输入规模计量的 `poly(d)` 时间内，算法应输出至多 \(D_d\) 个实际 \(h\)-子集及非负有理权，使每个 singleton 边际为 \(h/d\)，每个 pair 边际为 \(h(h-1)/(d(d-1))\)（\(d=1\) 时没有 pair 约束）。输出必须显式列出集合和权；声明不包含 `poly(log d)` 复杂度、高阶矩、共同跨行 law 或一般调度算法。

## 读后核验

### 1. 候选列没有隐藏的指数 oracle

作者 Proof 对父状态 \( (d,h) \) 作显式二分，块大小为 \( (a,b) \)。对每个合法局部基数 \(u\)（至多 \(d+1\) 个），只把两个递归支持中的集合做笛卡儿积并合并为父候选。若 \(D_a,D_b\) 是递归支持上界，候选列数至多
\[
(d+1)D_aD_b=O(d^5).
\]
对固定 \(u\)，左右 law 独立；块内 first/pair 由归纳假设给出，跨块 pair 是两个 singleton 边际的乘积 \(u/a\cdot(h-u)/b\)。再按超几何权
\[
\Pr(U=u)=\binom au\binom b{h-u}/\binom dh
\]
混合，正好得到均匀父 \(h\)-子集的 first/pair 向量。因而父目标位于**已显式列出的**候选列凸包内。审查没有发现把未列出的 \(h\)-子集交给分离 oracle 或隐含搜索二次基数优化的问题；可行见证也可直接由子权和超几何权写出，再在显式列系统上做有理消列。

### 2. 递归状态与缓存承担了总时间界

固定二分树后，每层块大小总和为 \(d\)，深度为 \(O(\log d)\)。若对同一块和局部基数不缓存而反复递归，复杂度论证确实会失败；作者 Proof 明确缓存每个块/局部基数状态。由此状态数为 \(O(d\log d)\)（用更粗的 \(O(d^2)\) 也足够），每个状态的候选列和 LP 均为多项式规模，强归纳给出总 `poly(d)` 时间。该结论仍以显式 \(d\) 为参数，不能改读为 `poly(log d)`。

### 3. 基本解、分母和中间位长没有失控

父特征向量的共同分母可取 \(q=d(d-1)\)（边界 \(d=1\) 单独处理）。从显式 \(0/1\) 候选矩阵取秩至多 \(D_d\) 的基本可行解，或沿有理零空间消列，正列数至多 \(D_d\)。对独立的 \(0/1\) 行列式用 Hadamard/Cramer 界，权的位长为多项式级；消列时一次只乘一个基本整数 nullvector 的系数，最多处理多项式数量的候选列，故中间共同分母和分子位长仍是 `poly(d)`。审查未发现把整棵递归树的所有子分母无控制相乘的步骤。该位长核验支持“能输出显式小支撑”同时“能在声明的总位复杂度内计算”的两部分，而非只给存在性证明。

### 4. 边界条件与七态使用范围

`d=1` 没有 pair 分母；`h=0` 或 `h=d` 可输出唯一集合；非平凡分块有 \(a,b\ge1\)，跨块分母不为零。固定基数保证每个输出配置的实际行负载不因支撑压缩而改变。若七态 \(K_v\) 的某一类别只使用固定 \(h\) 的 first/pair 证书，可把该均匀 slice 换成稀疏支持（按类别数给出如 \(6D_d\) 的支持粗界），但这只保 first/pair：不保三阶及更高矩，不生成共同 \(L\)，不替换全局 \(q^2\) 或 degree\(\le6\) 证据，也不推出一般 unrelated-machines 调度算法、近二界、硬度或主目标结论。

## 与独立重构的关系

Fisher–Yates 独立重构从均匀标签置换开始，在每轮只显式列出当前支持经有限交换得到的候选，再以保持 first/pair 特征的整数依赖压到 \(D_d\) 列。作者 Proof 的二分递归改为局部基数分块和超几何混合；二者都只操作显式候选，均输出有理权并明确不保存高阶 law。二者因此是同一稳定数学对象的两条构造/证明路线，而不是互相自动证明的一般化。Fisher–Yates 源没有读取作者 Proof；本 read-after 源补足的是作者路线的完整范围审查。

## 结论、限制与后续

在作者 statement 所给的 `poly(d)`、first/pair、固定基数 scope 内，完整读后未发现 fatal gap，建议把本源作为 canonical theorem 的作者 Proof read-after 审查证据整合。它不是软件复现，不能声称运行作者程序；也没有外部文献新颖性认证。后续若要把稀疏支持接入七态全局共同 law、共享 owner、递归 growing-depth 或实际调度 sigma，必须另行证明相应耦合和复杂度，不能从本审查外推。

## 建议处置回执

```json
{
  "id": "ba98d4f6d89c0be1ecf2",
  "full_file_reviewed": true,
  "related_material_checked": true,
  "unique_content_accounted_for": true,
  "read_note": "全文读取 read-after 源；逐段核对作者 Proof 的显式候选列、超几何父见证、递归缓存、基本有理 LP、消列和位长边界；比较 Fisher–Yates 独立重构及 canonical theorem。",
  "comparison_note": "作者二分递归和 Fisher–Yates 压缩是同一 first/pair 稳定对象的不同显式构造路线；本源独有的是作者 Proof 的隐式 oracle、总状态和位复杂度攻击，未发现声明范围内致命缺口。",
  "decision_note": "整合为 canonical theorem 的 read-after 审查证据；保留 poly(d) 而非 poly(log d)、只保 first/pair、无软件复现、无高阶 law/一般调度外推的边界。",
  "disposition": "integrated",
  "targets": [
    "archives/unrelated-machines/state/定理/均匀定基数first-pair稀疏支撑--定理.md",
    "archives/unrelated-machines/state/审查/均匀定基数稀疏支撑作者证明read-after审查--审查.md"
  ]
}
```
