---
id: "customer-attraction/full-tree-flow-source-review"
kind: "obstruction"
type_tag: "障碍"
title: "完整策略树流模板、节点平均与终局删除的源级清洗"
status: "source-read-draft"
truth_status: "exact-template-obstructions; positive-two-player-interface-only"
review_level: "exact-Fraction-replay-and-cross-source-comparison"
scope: "固定有序历史纯策略、静态分布及指定流/节点平均/终局删除接口；不量化任意SPE福利桥"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/customer_attraction/security_gluing_2026-10-10/full_tree_flow_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/customer_attraction/security_gluing_2026-10-10/full_tree_flow_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:archives/customer-attraction/tools/evidence/continuation-security/tests/audits/customer_attraction_full_tree_flow.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:archives/customer-attraction/tools/evidence/continuation-security/replay-flow.json"
legacy_source_id: "b7f04317df5985395714"
source_sha256: "67cbb7def1f7a26addec377e84ba02db8553f15086d763e768c8050ca4f39be8"
---

# 清洗结论

该源是一个**固定策略、固定静态分布下的证书模板审查**，不是六人半覆盖命题的反例，也不是一般 $W\ge n v_n$ 的反例。它给出三层精确障碍和一个两人正接口：

1. 对自然 iid 前缀流，完整树势恒等式中有删除位置余项，余项没有由 SPE 保证的非负号；固定单位流与固定 $n$ 倍流都被同一个真实 36 客户三人 SPE 点否定为“可由静态非负乘子支付”的模板。
2. 即使允许每个深度任意非负权，或保留每个历史节点但先把该节点全部偏离用同一 $q$ 平均，六类型/十五类型整数分离向量仍否定线性证书。
3. 从实际终局均匀删除一位构造静态背景并不总能 cap 聚合查询；这是两人三主题五客户的精确障碍，但其真实静态安全值仍为 $v_2=2$，所以不否定聚合安全桥。
4. 两玩家时，若末位响应映射 $b$ 取任一周期的平稳分布 $\pi$，则固定静态背景 $Q=\pi$ 对该完整策略的全部根查询给出一个点态安全接口；这只是两人机制，不能把 $b$ 机械推广到多层后继。

源中所有“分离向量”都不是完整 SPE：它们具有负的真实逐节点偏离行。应把“否定指定证书锥”与“否定游戏命题”分开记录。

## 1. 模型和完整树行

有 $m$ 个主题，$n$ 个按顺序行动的提供者，单位客户兴趣集合为非空 $T\subseteq[m]$，质量 $w_T\ge0$。固定完整有序历史纯策略 $\sigma$，对历史 (h) 及动作 (a) 令 $z_h$ 为依 $\sigma$ 从 (h) 完成的终局，$z_{ha}$ 为先取 $a$ 再依同一完整策略续行的终局。客户的单次覆盖收益按最终覆盖者均分，因此每一行

\[
\Gamma_{h,a;T}=
\frac{\mathbf1_{\sigma(h)\in T}}{|\{i:z_{h,i}\in T\}|}
-
\frac{\mathbf1_{a\in T}}{|\{i:z_{ha,i}\in T\}|}
\]

（分子为零时该项约定为零）是真实、不冻结后继的激励差。策略是 SPE 的客户锥为
\({w\ge0:\Gamma w\ge0}\)。固定静态混合 (q) 时，令静态 Nash 行矩阵为 (E(q))，根覆盖行向量为 $c$，iid 终局福利向量为 $\psi(q)$。固定 $(\sigma,q)$ 的 Farkas 证书精确形式是

\[
c-\psi(q)=\Gamma^\top\lambda+E(q)^\top\eta+r,
\qquad \lambda,\eta,r\ge0.
\]

此式允许每个历史、每个偏离独立乘子；源的负面结果只排除把 $\Gamma$ 先压缩后再加权的模板。

## 2. iid 前缀流恒等式和删除位置余项

令 $Z_k$ 的前 $k$ 个动作按 $q$ 独立抽取，剩余位置依原 $\sigma$ 真实续行；$Z_0$ 为实际终局，$Z_n$ 为 iid 终局。调和势

\[
\Phi(z)=\sum_Tw_TH_{\ell_T(z)},
\]

其中 $\ell_T$ 为主题 $T$ 的最终负载。删除位置 (i) 后的势记为 $\Phi(z\setminus i))，并定义

\[
\Delta_{k,i}=\mathbb E\Phi(Z_{k-1}\setminus i)-\mathbb E\Phi(Z_k\setminus i).
\]

第 $k$ 层的完整偏离流 $G_k$ 满足

\[
G_k=\mathbb E\Phi(Z_{k-1})-\mathbb E\Phi$Z_k$-\Delta_{k,k}.
\]

对每个终局逐客户使用 (\ell(H_\ell-H_{\ell-1})=1)，得

\[
W(z)=n\Phi(z)-\sum_i\Phi(z\setminus i),
\]

从而

\[
W$Z_0$-\mathbb EW$Z_n$=n\sum_{k=1}^{n}G_k+
\sum_k\left[(n-1)\Delta_{k,k}-\sum_{i\ne k}\Delta_{k,i}\right].
\]

单位流版本也可写成
\[
W$Z_0$-\mathbb EW$Z_n$=\sum_kG_k+\mathcal R,\qquad
\mathcal R=\sum_k\Delta_{k,k}-L$Z_0$+F_n(q)-\Psi_n(q),
\]
其中 $L=\Phi-W$，(F_n=\mathbb E\Phi$Z_n$)。完整 SPE 只保证每个 $G_k\ge0$，不保证删除位置余项同号。

## 3. 36 客户真实 SPE：固定流模板的精确失败

采用既有 36 客户、三玩家、六主题完整策略：根取 0；第二位在相反组中取最小主题；末位在第二位所在组取最小未用主题。均匀 $q$ 下，258 条真实全树比较及六条静态 Nash 行均满足非负/为零，实际终局为 $(0,3,4)$。Fraction 重放给出

\[
W=34,\quad\Psi_3(q)=97/3,\quad (G_1,G_2,G_3)=(0,1/2,31/18).
\]

因此
\[
W-\Psi_3(q)-\sum_kG_k=-5/9,
\qquad
W-\Psi_3(q)-3\sum_kG_k=-5.
\]

所以固定单位 iid 前缀流或其三倍流后，余项不可能仅由非负静态 Nash 乘子与非负客户残差表示。该实例的福利差 $W-\Psi_3=5/3>0$，故它不是强 iid 福利桥反例；它只否定预先固定流系数的证书模板。

## 4. 任意深度权和节点平均权仍不能替代逐偏离

若允许任意 $a_k\ge0$，模板
\[
c-\psi=\sum_ka_kG_k+E(q)^\top\eta+r
\]
仍被以下非负整数质量分离：

| 兴趣掩码 | 4 | 25 | 26 | 29 | 34 | 37 |
|---|---:|---:|---:|---:|---:|---:|
| 质量 |11988|17316|12481|7312|19357|12481|

总质量 80935，且
\[
E(q)w=0,\quad(G_1w,G_2w,G_3w)=(0,0,607489/216),\quad
(c-\psi)w=-472195/36.
\]

内积立即矛盾。该向量有 57 条负的完整 $\Gamma$ 行，根改选 1、2 分别增益 2827、6216，故不是 SPE。

更强地，记每个历史节点的平均行 $M_h=6^{-1}\sum_a\Gamma_{h,a}$，允许 43 个 (h) 独立赋非负权。十五类型整数向量满足所有 $M_hw\ge0$（最小为 0）、$E(q)w=0$，却有
\[
(c-\psi)w=-1085816540911589/12.
\]

这再次只排除“节点内用同一 $q$ 平均全部偏离”的线性锥。它不排除逐偏离 $\Gamma$ 证书、改用别的静态背景或非线性构造。

## 5. 实际终局均匀删除障碍

两玩家、三主题、兴趣质量
\({w_2=1,w_5=2,w_6=2})，策略根取 0，根为 0 时末位取 1，否则取 2。所有 12 条完整比较通过，实际终局 $(0,1)$，$W=5$，玩家收益 $(2,3)$。从实际终局均匀删除一位，查询主题 2 的收益为 3，超过 $W/2=5/2$。然而纯查询/纯背景的 minimax 值均为 2，故 $v_2=2$，且 $W=5\ge2v_2$。这不是聚合安全桥反例，而是删除对偶背景的障碍。

## 6. 两玩家平稳映射的正接口

仅在 $n=2$ 时，令 $b(a)$ 为根取 $a$ 后末位的指定响应。取映射 $b$ 的任一周期并令 $\pi$ 为其上的平稳分布，即 (b_\#(\pi)=\pi)。对任意根查询 $t$，把根/末位在终局 $(a,b(a))$ 的收益相减并对 (a\sim\pi) 平均：逐客户差为 $|a|-|b(a)|$，平稳性使其平均为零。因此

\[
u_{\mathrm{root}-\pi}$t$=
\sum_a\pi_a\Gamma_{\mathrm{root},a}+
\sum_a\pi_a\Gamma_{(a),t}.
\]

这给出一个固定静态 $Q=\pi$ 同时 cap 全部根查询的两人接口；实际末位可用集中在实际根行动的背景。两种背景平均后有 $r=0$ 的聚合证书。该论证依赖只有一层末位映射；多玩家把 (b) 换成后续响应元组时，动作边际平稳不再等同角色收益，不能直接推广。

## 7. 证据、复现和与已有对象的关系

精确重放程序：

```text
python3 -E -B archives/customer-attraction/tools/evidence/continuation-security/tests/audits/customer_attraction_full_tree_flow.py
```

本地重放输出与冻结 `replay-flow.json` 一致：258 条完整比较；原 36 客户点 $W=34,(G_k)=(0,1/2,31/18)$；深度分离向量 57 条负行；节点平均分离向量严格负；终局删除查询为 3 而 $W/2=5/2$。

该源与已存在对象 `customer-attraction/full-tree-averaging-obstruction` 高度重叠，建议正式处置为**同一障碍对象的增量来源**，不要新建重复主对象：

- 在该对象 `source_refs` 中追加本源两版本路径及本次审计脚本/冻结输出；
- 将本源第 6 节两玩家平稳接口作为“有限正接口”附加小节，明确不推广；
- 保留源版本差异：当前源的 hybrid-flow 单位恒等式、终局删除和两玩家接口比 `iid_benchmark_source` 更完整；
- `full_tree_flow_source` 的分离向量并非SPE，不能标为 welfare/half 反例；
- 与已有真实 SPE iid welfare 反例、静态安全值障碍、四人尾部提升分别保持对象边界。

推荐本源语义处置：`integrated`（已吸收到同一障碍对象；证据程序和输出另以 `retained`/`integrated` 依现有清单字段登记）。
