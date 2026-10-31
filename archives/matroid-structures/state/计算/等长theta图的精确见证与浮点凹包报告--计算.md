---
id: matroid-structures/equal-theta-exact-witnesses-and-floating-concave-envelope-report
kind: computation-resource
type_tag: 计算
title: 等长theta图的精确见证与浮点凹包报告
status: finite-exact-witnesses-plus-sampled-floating-denominators; no-universal-proof-or-novelty
summary: 六图全部报告字段、916子集秩与六有理见证和168次浮点LP分别保全；候选有限公式和全参数证明义务不由数值margin替代。
legacy_ids: [CS-THETA-EXACT-v1]
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/probes/results/equal_theta_independent_20261020.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/probes/results/equal_theta_independent_20261020.json
---

# 等长theta图的精确见证与浮点凹包报告

## 模型、分母与不同计算途径

图有两端点及$k$条内部互不相交、各长$\ell$的路径，$k\ge1,\ell\ge2$，共$m=k\ell$边、$n=2+k(\ell-1)$点。graphic rank为$r$，独立取边概率$x$的$F(x)=\mathbb E r(R_x)$；$r^+(x)$是所有同边缘联合分布中的最大秩期望，ratio $F/r^+$，$0/0=1$。正式theta候选的非平凡域为$k\ge2$；报告$k=1$只是forest控制。

方法字段为“union-find subset ranks + exact Fraction expectation + full concave-envelope LP”。对应4843B生成器全文读：不以路径完成闭式算子集秩，而以union-find对全部$2^m$子集逐边算秩；用Fraction逐乘独立概率算期望。**候选值**仍由下面的解析候选公式枚举得到，故不是完全不知候选陈述的盲审。

设$b=((\ell-1)/\ell)^\ell$、$a_q=((\ell-1+1/q)/\ell)^\ell$，在$2\le s\le k,1\le q\le s$中枚举

$$C_{s,q,\ell}=1-\frac{q a_q+(s-q)b-1+(1-a_q)^q(1-b)^{s-q}}{s(\ell-1)+1}.$$

精确见证取前$q$条路径边概率$(\ell-1+1/q)/\ell$，后$s-q$条取$(\ell-1)/\ell$，其余路径全零。代码对这个$x$检查**每个边子集**的$x(A)\le r(A)$，并用独立枚举期望确认候选ratio；$\sum x=s(\ell-1)+1$为支持核心秩，$k=1$控制取全一。

对拟阵独立多面体的$x$，标准独立集分解给$r^+(x)=\sum x$（上界$r(S)\le|S|$，下界由同marginal的独立集分布达到）。此接口支撑exact witness denominator，不把任意域$x$分母都换成$\sum x$。

## 六行报告的全部精确字段

case字段“attaining_support_paths”为$s$，“attaining_active_t”为$q$，不是激活边数；minimum按(ratio,s,q)字典序取一个见证。

| $(k,\ell)$ | subsets | candidate_ratio | $(s,q)$ | exact_witness_mass | exact_witness_ratio |
|---|---:|---:|---:|---:|---:|
| (1,2) | 4 | 1 | (1,1) | 2 | 1 |
| (2,2) | 16 | 229/256 | (2,2) | 3 | 229/256 |
| (3,2) | 64 | 3565/4096 | (3,2) | 4 | 3565/4096 |
| (4,2) | 256 | 17/20 | (4,1) | 5 | 17/20 |
| (2,3) | 64 | 43531/46656 | (2,2) | 5 | 43531/46656 |
| (3,3) | 512 | 173/189 | (3,1) | 7 | 173/189 |

共916个子集秩值和六个有理见证。报告$k=3,\ell=2$见证的路径边概率为$(3/4,3/4)$、$(3/4,3/4)$、$(1/2,1/2)$，不是全对称。独立秩公式也可核此一个值：
$F=\sum x-\sum_i p_i+1-\prod_i(1-p_i)$，$p=(9/16,9/16,1/4)$，除质量四得$3565/4096$；这一展示不是生成器union-find路径的替代。

原[候选公式与范围](../资料/交换距离与等长theta相关间隙的独立接口--资料.md)还说明旧全对称$637/729$较大、必须允许支持restriction的$s$。六行均$s=k$不证明所有参数都如此，也不证明$q$永远只需1、2或s。

## 168次浮点凹包LP的实际覆盖

完整凹包LP对每个子集$T$设概率$y_T\ge0$，最大化$\sum_T r(T)y_T$，约束$\sum_Ty_T=1$和$\sum_{T:e\in T}y_T=x_e$。这是每个查询$x$的**全子集**LP，但$x$只取有限样本；“full”不等全连续概率域。

每图28个查询：全零、全一、全$1/2$、精确见证，再加24个边概率从$\{0,1/4,1/2,3/4,1\}$抽取的向量。样本可能重复，不能称28个互异点；一个random.Random(20261020)贯穿六图，不逐图重新seed。故共168次LP，含独立多面体外的样本（如全一）。

| $(k,\ell)$ | lp_samples | min_numeric_margin | max_lp_equality_residual |
|---|---:|---:|---:|
| (1,2) | 28 | 0 | 0 |
| (2,2) | 28 | 0 | 0 |
| (3,2) | 28 | 0 | 0 |
| (4,2) | 28 | 0 | $2.220446049250313\cdot10^{-16}$ |
| (2,3) | 28 | $-1.1102230246251565\cdot10^{-16}$ | $2.220446049250313\cdot10^{-16}$ |
| (3,3) | 28 | $-2.220446049250313\cdot10^{-16}$ | $2.9753977059954195\cdot10^{-14}$ |

margin是浮点观测$F(x)/(-lp.fun)$减候选值；分母$\le10^{-12}$时代码按一处理零比值控制。每次要求HiGHS success、等式残差$<10^{-8}$、margin$>-10^{-8}$。小负margin不是精确反例或严格下界证明。JSON没有全部样本向量、最优$y_T$/对偶或各次solver状态；仅有seed/版本/概要，不能独靠该JSON当精确LP证书。

## 来源、独立性与接续

冻结报告记录Python3.12.14、NumPy2.3.5、SciPy1.17.0；这是历史生成环境，不是本批新run。与已有equal_theta_independent_output.json全部字段/字节相同，SHA
65b21a0adc1fa5d4bbb509ea924efdbf8feae0f6fb31b502b74f95ce3b5c2594；
复用已有输出，无额外生成器done或重复run。

“独立”指子集秩用union-find、分母另以全分布LP，未导入原scout求值公式；candidate函数仍用待核公式，故不是statement-blind、外部评审或新颖性认证。main的三个非法(k,length)控制不在JSON另存；不把scope文字扩大为任意加权拟阵、不等长路径、一般argmin相图或全参数证明。

对应完整理论笔记已全文比较：support-tight定位不等全图base；桥删去、路径内AM–GM、两坐标平方差凸性负责普遍公式；这些数学与外部定位定理导入/文献覆盖仍有独立义务，916子集和168LP不替代。报告scope明确finite cross-checks only，analytic proof与literature novelty separate。[原件/生成器读域和逐字段去向](../../../../tools/evidence/retired-final-independent-reports/README.md)。
