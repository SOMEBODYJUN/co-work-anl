---
id: matroid-structures/equal-theta-independent-correlation-gap-audit
kind: calculation
type_tag: 计算
title: 等长多路theta相关间隙独立有限核验
status: finite-exact-and-lp-crosscheck-no-general-proof
truth_status: exact-rank-witnesses-with-sampled-concave-envelope-checks
review_level: source-read-script-run-and-related-object-comparison
summary: 实读并运行equal_theta_independent.py；用union-find枚举等长多路图的全部边子集，Fraction计算候选比值，再对28个样本做全凹延拓LP。六个(k,length)实例的精确候选比值与支持路径/active t均重现；浮点LP只作有限交叉检查，解析证明、全参数argmin分类和新颖性仍独立。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/retired_topic_selection/multi_lane/research/topic_selection/probes/equal_theta_independent.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/retired_topic_selection/multi_lane/research/topic_selection/probes/equal_theta_independent.py
evidence_paths:
  - archives/matroid-structures/tools/evidence/retired-topic-selection-20261031/equal_theta_independent.py
  - archives/matroid-structures/tools/evidence/retired-topic-selection-20261031/equal_theta_independent_output.json
related_objects:
  - ../资料/交换距离与等长theta相关间隙的独立接口--资料.md
  - ../审查/退役交换距离来源审查与应用边界--审查.md

# 等长多路theta相关间隙独立有限核验

## 程序身份和方法

equal_theta_independent.py 源文件大小4,843字节，SHA-256 36f6066cb90fb901edc38cbf698a77ae896cd10f9266def93cd0532e4a8eb09f；legacy-cleanup 与 main 内容相同。程序声明不使用路径完成公式，先枚举所有边子集并用 union-find 计算 graphic rank，再用 Fraction 计算独立边缘下的期望秩和候选比值。随后以全凹延拓的线性规划检查样本，LP 使用 NumPy/SciPy 浮点，仅作为独立交叉核验；程序明确不主张解析证明或新颖性。

完整图函数构造两端点之间的 \(k\) 条内部互不相交、每条长度为 length 的路径；参数要求 \(k\ge1,length\ge2\)。候选函数对 \(2\le s\le k\)、\(1\le q\le s\) 求有限最小值，并返回 ratio、attaining support paths \(s\) 和 active t \(q\)。非法 \((0,2),(2,1),(-1,3)\) 应抛 ValueError。

## 实际运行结果

运行环境 Python 3.12.14、NumPy 2.3.5、SciPy 1.17.0，随机种子20261020；6个实例每个28个LP样本，全部断言通过，最大等式残差约 \(2.98\times10^{-14}\)。

| \(k\) | length | 边子集 | candidate ratio | support \(s\) | active \(q\) | exact mass |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 4 | \(1\) | 1 | 1 | 2 |
| 2 | 2 | 16 | \(229/256\) | 2 | 2 | 3 |
| 3 | 2 | 64 | \(3565/4096\) | 3 | 2 | 4 |
| 4 | 2 | 256 | \(17/20\) | 4 | 1 | 5 |
| 2 | 3 | 64 | \(43531/46656\) | 2 | 2 | 5 |
| 3 | 3 | 512 | \(173/189\) | 3 | 1 | 7 |

每个实例都检查所有边子集的 rank upper bound、Fraction expectation 与候选比值相等。LP样本包括全零、全一、全一半、精确 witness 和24个随机有理边缘；所有观测比值不低于候选值（负 margin 仅为约 \(2.2\times10^{-16}\) 的浮点误差），等式残差最大 \(2.98\times10^{-14}\)。

## 结果含义和限制

有限输出支持已有等长多路 theta 公式候选中的六个小实例，也重现 \((k,\ell)=(3,2)\) 的 \(3565/4096\) 修订值；它不能给所有 \(k,\ell\) 的 argmin 分类，不能替代 source 中对最坏 support 取 \(s,q\) 的解析凸性证明，也不涵盖不等长路径。

全凹延拓 LP 样本不等于对所有边缘点或相关联合分布的证明，且其浮点数值不应与 Fraction 证书混为同一精度。程序结果不推出 graphic correlation gap 的外部新颖性，也不迁移到任意 matroid、EFX、Nash 或 GAP。

本次已将源码和新输出保存到 matroid-structures evidence；未修改冻结源，不扩大随机样本，不重跑文献检索。处置为 finite-exact-audit，解析对象和来源版本仍按[交换距离与等长theta相关间隙的独立接口](../资料/交换距离与等长theta相关间隙的独立接口--资料.md)保留候选状态。
