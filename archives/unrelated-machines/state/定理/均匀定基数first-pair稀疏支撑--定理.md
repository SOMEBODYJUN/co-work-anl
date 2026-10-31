---
id: "unrelated-machines/uniform-cardinality-first-pair-sparse-support"
kind: "theorem"
type_tag: "定理"
title: "均匀定基数 first/pair 稀疏支撑"
status: "scoped-complete-proof-reconstructed-no-software"
truth_status: "complete-scoped-mathematical-claim"
review_level: "full-source-read-with-related-ledger-and-audit-comparison"
summary: "对显式 d 和 h，确定性 poly(d) 构造至多 D_d=1+d+binom(d,2) 个实际 h-subsets 及有理权，使 singleton/pair 边际等于均匀 h-subset；只保 first/pair，不保高阶矩或全局共同 law。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/boss11_uniform_cardinality_pair_sparse_support_exact_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/boss11_uniform_cardinality_pair_sparse_support_proof_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/boss11_uniform_cardinality_pair_sparse_support_exact_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/boss11_uniform_cardinality_pair_sparse_support_proof_v1.md"
legacy_ids:
  - "UM-UNIFORM-CARDINALITY-PAIR-SPARSE-SUPPORT-v1"
---

# 均匀定基数 first/pair 稀疏支撑

## 精确对象与量词

给定显式正整数 \(d\) 以及 \(0\le h\le d\)，令
\[
D_d=1+d+\binom d2.
\]
存在固定确定性算法，按显式 \(d\) 的总位输入规模在 poly(\(d\)) 时间内输出
\[
(A_1,\alpha_1),\ldots,(A_t,\alpha_t),\qquad t\le D_d,
\]
其中每个 \(A_i\subseteq[d]\) 且 \(|A_i|=h\)，每个 \(\alpha_i\ge0\) 是二进制有理数，\(\sum_i\alpha_i=1\)，并且
\[
\sum_{i:r\in A_i}\alpha_i=\frac hd\quad(r\in[d]),
\]
以及（\(d>1\) 时）
\[
\sum_{i:\{r,s\}\subseteq A_i}\alpha_i
=\frac{h(h-1)}{d(d-1)}
\quad(r\ne s).
\]
\(d=1\) 没有 pair 约束。输出必须显式列出实际 subsets 和权，不是只给存在性或抽样 oracle。复杂度是 poly(\(d\))，不宣称 poly(\(\log d\))。

## 构造和证明承重

对 \(d=1\) 及 \(h=0,d\) 直接输出唯一合法集合。对其余 \(d\)，固定拆分
\([d]=L\mathbin{\dot\cup}R\)，\(|L|=a=\lfloor d/2\rfloor\)，\(|R|=b=d-a\)。递归为每个块和每个合法局部基数生成稀疏支持 \(S_{a,u}\)、\(S_{b,v}\)。对
\[
\max(0,h-b)\le u\le\min(a,h)
\]
枚举 \(A\in S_{a,u}\)、\(B\in S_{b,h-u}\)，形成候选列 \(A\cup B\)，并去重。递归支持的每个列都满足局部 cardinality、first、pair 条件；候选列数至多
\[
(d+1)D_aD_b=O(d^5).
\]

令
\[
v(A)=\bigl(1,(1_{r\in A})_r,(1_{\{r,s\}\subseteq A})_{r<s}\bigr)\in\{0,1\}^{D_d},
\]
目标 \(b_{d,h}\) 为均匀 h-subset 的该特征向量期望。目标在候选列的凸包内：先按超几何权
\[
\Pr(U=u)=\frac{\binom au\binom b{h-u}}{\binom dh}
\]
混合局部基数，再在两块内独立使用递归分布。块内 first/pair 和跨块 pair 均因此与均匀 h-subset一致。于是存在 \(\alpha\ge0\) 使
\[
\sum_A\alpha_Av(A)=b_{d,h},\qquad \sum_A\alpha_A=1.
\]
对这个显式 \(0/1\) 列系统求确定性有理可行 LP，取基本可行解（或沿有理零空间消列），正列数不超过秩 \(D_d\)。矩阵 entry 为 0/1，目标分母整除 \(d(d-1)\)；基本解行列式的位长由 Hadamard/Cramer 给出 poly(\(d\))，因此权的表示长度与递归构造均为多项式。按固定拆分缓存所有块/局部基数状态；状态数和每次候选/LP规模均为多项式，强归纳给出总 poly(\(d\)) 时间。该方法不枚举全部 \(\binom dh\) 子集，也不调用二次定基数优化 oracle。

## 七态星应用的承重边界

在七态星的逐行配置中，若某一 uniform-cardinality 类别只需要固定基数 \(h\) 的 first/pair 边际，可将该类的均匀 slice 替换为上述稀疏支持；每个子集基数固定，故 row-load 与该行 first/pair 量不变，六类合计支持可取至多 \(6D_d\)（按实际类别数缩减）。权仍为有理数。

这个替换只认证 row CFG 的 first/pair 证书。它不保三阶及更高矩，不生成原七态共同 law \(L\)，不替换 \(L\) 对 degree \(\le6\) 矩或 global-\(q^2\) 证明的用途，也不提供一般 unrelated-machines 调度算法、近二 gap、复杂度硬度或 SDP finder。有限七态 Fraction 审计只验证列出的参数，不能反向证明此一般构造。

## 与已读材料的比较和处置

Exact 源（939 bytes，SHA-256 'bf45e8b182f2dd69908c9a923ed0f8b41f4341c32f36700007b1f4d87e451535'）给出完整量词、输出规模和 scope 边界；配套 Proof 源（2728 bytes，SHA-256 'f3d759b4a0e147ab215f2aa1c09f72aca5aeda687426a3adac3ce2643fc28274'）给出递归列生成、超几何存在性见证、有理 LP 基本解和位长/状态缓存论证。本轮也核对了两个冻结提交、source crosswalk、七态星有限 audit/replay 对象和已有 Boss6 provisional reviews。既有 canonical ledger 已将此 ID 作为七态星总对象的一个独立 scope，并把 finite audit 与该解析构造分开；因此本处置不另造全局 law 或软件对象，而把本源作为该稳定 ID 的解析 theorem 证据补齐。

## 未覆盖和待接续

- 没有实际运行作者程序；没有程序可作为本定理实现证据。
- 没有 poly(\(\log d\)) 复杂度，也没有隐式大 \(d\) 输出压缩承诺。
- 没有三阶/高阶矩、共同跨行耦合、共享 owner、递归 growing-depth 接线或 payload 扩展结论。
- 与七态星全局二次、affine Boolean owner、忠实 AND localizer 是独立量词，关系只能由既有 canonical review 接续。
- 未作外部文献新颖性或同行评审认证。

## 建议语义处置

对源 7f31a7e15c84adcfbdf4 建议 integrated，目标为本文件（若根沿用旧 canonical 路径，则目标应指向其对应“七态共同二次局部核及原端点延拓边界”正文中的该 scope）；Exact 是 statement-first 的唯一精确接口，Proof 是承重证明来源，不能把 Exact 误记为 duplicate。若系统要求按历史版本分别保留，可对 Exact 标 retained、Proof 标 integrated，但两者都应链接同一稳定 ID；本次源本身没有独立 finite-audit 输出。

### 建议 receipt

    {
      "id": "7f31a7e15c84adcfbdf4",
      "full_file_reviewed": true,
      "related_material_checked": true,
      "unique_content_accounted_for": true,
      "read_note": "全文读取 Exact 源；核对配套 Proof、source crosswalk、七态星有限 audit/replay 对象及既有 Boss6 provisional review。确认量词为显式 d 的 poly(d) 递归稀疏支持，输出 <= D_d 且只保 first/pair。",
      "comparison_note": "Proof 补齐 Exact 的递归列生成、超几何凸包见证、基本有理 LP 与位长/状态复杂度；canonical ledger 已有同一稳定 ID，finite audit 与全局 law scope 分开。",
      "decision_note": "将该 Exact 源整合到均匀定基数 first/pair 稀疏支撑 theorem；保留不保高阶矩、共同 law、一般调度算法与 hardness 的边界。",
      "disposition": "integrated",
      "targets": [
        "archives/unrelated-machines/state/定理/均匀定基数first-pair稀疏支撑--定理.md"
      ]
    }
