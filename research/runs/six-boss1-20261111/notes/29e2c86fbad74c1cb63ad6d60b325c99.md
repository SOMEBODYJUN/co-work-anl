# 可见真最大 C 联合层 v2：1003行输入准备

Boss1；RUN `six-boss1-20261111`。状态 **PREPARED_NO_OPTIMIZER**。本轮新优化器调用为 **0**；只准备全域输入，不消费未来求解授权。

## 输入合同

原冻结1002 raw行按原顺序、全部系数字符串、rhs及元数据忠实复制，保留零行与重复行；全部512客户型及K共513非负列、目标、两等式原样保留。唯一追加的是Main已证明的

\[
\boxed{300u_2+K-288B-12M-5N\ge0,}
\]

\[
B=\sum_v\frac{c_vz_v}{a_{1,v}+5},\quad
M=\sum_v\frac{o_vz_v}{6(a_{1,v}+4c_v+1)},\quad
N=\sum_v\frac{o_vz_v}{6(a_{1,v}+3c_v+2)}.
\]

行名为`SOURCE2_MAXIMUM_C_NESTED_SOURCE5_SAFE`，位于raw index1002；原整数尺度不变，数值正除数300。最终尺寸 **1003 raw / 513 nonnegative columns / 2 equalities**。

## 来源与精确准备检查

完整实读Main新proof。该行从actual第二源强制合法真最大C后的同一真实分支支付：源IC25，三个中间尾大小帽各1/2，末尾大小帽1，同一真实末节点BR平均1，以及内部真实第五源SAFE平均5/12。内部收益始终是该真实分支的v5，没有替换为actual u5或u2。

构建和独立预检分别核128个完整隐藏态、8个准确最小值、4096个真实六查询会员平均，以及新行全部513列。旧1002行、目标、两等式、列路由及旧数值正除数逐项保持；未用旧点支持、K值或最优面缩小新输入。

## 旧全最优面只作诊断

准确全513列身份是

\[
R_{NS5}=12R_{P25(C,Omean)}+(K-5N)+30(\sum c-K).
\]

因此旧全最优面上的新行恒为

\[
-\frac{15981204499895866953854050884598865236619}
{86426960107246755980438461555855802597096}
\approx-0.1849099456936224.
\]

完整新输入先独立构建，之后才读取旧点/全最优面并做上述诊断。这不是新最优值或SPE实现声明。原六人half仍为 **OPEN**。

## 文件入口与绑定

- [完整新输入](visible_maximum_joint_v2/exact_input.json)
- [来源审查](visible_maximum_joint_v2/source_review.md)
- [新行全态与全列检查](visible_maximum_joint_v2/new_row_checks.json)
- [独立预检](visible_maximum_joint_v2/independent_precheck_result.json)
- [旧全最优面分离诊断](visible_maximum_joint_v2/old_face_diagnostic.json)
- [冻结manifest](visible_maximum_joint_v2/freeze_manifest.json)

新input SHA `0d80f56ac0b1f82350ae5e307370d9860b21382c7059b688904230a3b80f20a4`；原1002input SHA `b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33`；Main新行SHA `a852e9f8c16fa8fd8a2785034d220de1b90193036d1d4ceb9d0fe431481cd4ba`。

本包冻结后等待Main另行明确授权未来唯一LP；没有求解入口、消费标记或重试路径。旧input/result均保持字节原样。
