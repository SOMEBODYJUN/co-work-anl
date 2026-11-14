# 数学支撑与精确证书

## 1. 固定策略锥的可行域

给定四份完整有序策略及指定根 (a)，程序从完整 `StrategyCone` 构造所有真实终局和 IC 后，将 `rows/matrix` 覆盖为正深度行。对每个正深度历史 (h) 和可选行动 (c)，若原策略行动为 τ(h)，使用

\[
f_{h,c}(S)=\frac{\mathbf 1_{c\in S}}{q(h)(S)},\qquad
\gamma_{h,c}=f_{h,\tau(h)}-f_{h+c,c},
\]

仅在相应叶负载非零时取分母。于是 \(\Gamma z\ge0\) 是所有正深度真实 IC；根行动的 IC 被有意删除。归一化为 (w_a^Tz=1) 后，比较支持 (P) 的目标是 (v_P^Tz)。这是一个“固定后继、任意非负类型质量”的有理锥，而不是完整目录/策略空间。

程序按 (a=0,\ldots,p-1) 和 (P\subseteq[p]) 的字典序枚举，(k=\min(p,m))。`dual_support` 行号只属于去零、去重复、排序后的正深度 \(\Gamma\)，不属于原完整锥。原报告保存每条 primal、dual 和 support；本批没有重建矩阵或重新运行 HiGHS。

## 2. 230 条记录的无损核对

原 JSON 四族记录数分别 90、16、120、4。`report-interned-reading.json` 的 dictionary 解码规则为：

- 记录列顺序：`status, certified, value, dual_bound, dual_optimal, actual_root, support, values_length, nonzero_mask_values, dual_support`；
- `values_length=2^p-1`，mask 为一基索引，未列位置值为字符串 `0`；
- dictionary 仅复用完全相同字段值。

逐条展开后，四族所有记录与原 JSON 深比较相等，且 best 索引依次为 0、3、15、2。每条记录均有 `value == dual_bound`，均 `exact_primal/certified/dual_optimal`。最大值和精确达到点如下：

```text
root_tax_failure:             max 7/4, root=0, P=[0,1,2,3]
  nonzero z: mask2=1/4, mask4=1/4, mask8=1/4, mask49=1

eight_cce_welfare_gap:        max 2,   root=0, P=[1,2,3]
  nonzero z: mask2=1, mask4=1/2, mask8=1/2

aggregate_theta_failure:      max 149/103, root=0, P=[1,4,5]
  nonzero z: mask2=25/103, mask11=12/103, mask14=6/103,
             mask16=21/103, mask17=2/103, mask29=30/103,
             mask32=8/103, mask33=2/103, mask36=13/103,
             mask41=18/103, mask45=12/103

fractional_actual_load_failure: max 5/4, root=2, P=[0,1,2,3]
  nonzero z: mask1=1/4, mask14=1
```

原始四族所有值范围分别为 \([5/4,7/4]\)、\([1,2]\)、\([1,149/103]\)、\([30/29,5/4]\)。其中 `eight_cce_welfare_gap` 的 2 是固定三人后继锥内的精确等号，不是 (O>2W)。

## 3. 任意背景两尾接口的检查

独立实读的两尾定理固定任意旧背景 (p_x\in\mathbb Z_{\ge0})、两名剩余者完整纯 SPE 和三个合法比较目录。设实际两尾覆盖 (W)，比较并集 (O)，真实末位回复 (R_i)，则四类真实 IC 余量 (S,Z,V,L\ge0)，共同支付

\[
G=\frac{6S+Z+2V+5L}{11}.
\]
逐客户 (a,b,d,\ell,h) 系数代入后

\[
2W-O=G+\sum_xQ_x,
\]

其中 (Q_x\ge0) 在零背景和正整数背景分别按穷尽的 (d,a) 分支成立。因此任意三比较 (O\le2W)。对固定 (m=3) 后继树，取第一位实际行动为旧前缀，剩余两位的正深度真实 IC 正好满足两尾定理前提，故报告中的 16+120 条三人记录都应 ≤2；精确报告给出 2 与 149/103，和该解析检查一致。

这只是“定理 ⇒ 固定三人锥上界”的兼容性检查。反方向（固定 230 条 LP 记录 ⇒ 任意背景定理）不成立，(m=4) 两族也不在两尾三比较接口的量词内。

## 4. 迁移边界与反例边界

- 一尾基底的证明对象是“任意背景 + 一名末位真 BR + 两比较”，不支付两名余者的第三个不同标签；因此与本核心只形成量词边界，不能直接 `implies`。
- 根可任意意味着 (w_a) 依赖指定根，根 IC 被删除；不能将报告中的 (W=1) 归一化记录解读为完整 SPE 福利证书。
- 付费 (3\Delta) 根修复和不付遗憾的 FREE-ROOT 不是同一个目标；报告没有 Δ，也没有保险构造。
- 有限 LP 点即使整体清分母成为单位客户，也只实现该固定策略锥的类型质量；它不提供任意目录、任意历史策略或六人全称实例。
- 本包没有精确 (O>2W) 真实完整 SPE 反例；因此不写 `refutes`。唯一的固定等号值 (O/W=2) 也不反驳 half。
