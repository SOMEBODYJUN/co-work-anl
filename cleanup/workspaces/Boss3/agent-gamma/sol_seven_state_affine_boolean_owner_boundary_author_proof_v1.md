# 七态原星：仿射 Boolean 分类与 unit owner 边界的作者证明

2026-10-18，scratch 作者 Proof。对应且不修改 statement-only `sol_seven_state_affine_boolean_owner_boundary_exact_v1.md`，SHA256 `a38dfcf05158f38d93f1a26c54591944b8a662174018ece9f81388d499bef250`。本 Proof 不应在 Exact-only 独立重构前交给该审查者。

## 1. 基础 law 与足够支持

沿 Exact 的 d、s、η、h、p、u0、e。由 0<η≤1/2，p≤1/8000、u0≤4p，所以 e≥4/5−5/8000>0.79。七个类别质量都正，各类别中的每个 H-subset 也正。

因此 Ω0={0,1}×({0^d,1^d}∪{|y|=h}) 的所有点都在 P 的正支持上。证明纯函数分类只用 Ω0；额外 C=0,H=d/2 slice 不需要。参数满足 1≤h≤d/4。

## 2. 先消去 C 与 Y 混合的可能性

设实仿射函数 f=a+bC+Σ_i c_iY_i 在 Ω0 上取 0/1。取 Y=0，有 a,a+b∈{0,1}，所以 b∈{−1,0,1}。

若 b=1，则 a=0。对每个 h-subset F，f(0,1_F) 与 f(1,1_F) 相差一且均为 Boolean，只能依次是 0、1，因此 Σ_{i∈F}c_i=0。任取 i≠j，选大小 h−1 的集合 Q⊆[d]\{i,j}，比较 Q∪{i} 与 Q∪{j}，得 c_i=c_j。所有系数相同再用 h≥1 得 c_i=0，故 f=C。

若 b=−1，则 a=1，同样比较每个 h-subset 得 Σ_{i∈F}c_i=0，故 f=1−C。

余下 b=0。若 a=1，将 f 替成 1−f；因此只需分类

\[
g(Y)=\sum_i c_iY_i,\qquad g(0)=0,
\]

它在全部 h-subsets 与全一向量上均为 Boolean。

## 3. h=1 的全部边界

每个 singleton 都在支持内，所以 c_i∈{0,1}。全一向量又给 Σ_i c_i∈{0,1}，故至多一个 c_i=1。于是 g=0 或 g=Y_i。恢复前面的常数补操作，得到 0、1、Y_i、1−Y_i。

这覆盖 h=1 的所有合法 d，也特别覆盖最小参数 d=4,s=2。不存在需要另假设 d>4 的分支。

## 4. h≥2 时的系数分类

仍任取 i≠j，比较共享 h−1 个索引的两个 h-subsets，得到

\[
c_i-c_j\in\{-1,0,1\}.\tag{1}
\]

若所有系数都相同 c，则 hc∈{0,1}、dc∈{0,1}。由于 d/h≥4，这迫 c=0。

若不全相同，令 c 为最小系数。由 (1)，全部系数恰落在 c、c+1 两层，且两层均非空。记高层索引数 m、低层数 d−m。h-subset 内高层数 k 的所有可能值恰为整数区间

\[
\max(0,h-(d-m))\le k\le\min(h,m).
\]

对应 g 值为 hc+k，均须属于 {0,1}，所以该整数区间宽度最多一。

若高、低两层都至少含两个索引，则该宽度至少二：当两层数都≥h 时宽度为 h≥2；当高层数<h 时低层数≥d−h+1>h，宽度为高层数≥2；低层数<h 时对称。这三种情形穷尽，因为 d≥4h。因此高、低层中至少一层只有一个索引。

若唯一高层为 i，则 h-subsets 的两值是 hc 与 hc+1，必须是 0、1，所以 c=0，g=Y_i。

若唯一低层为 i，则两值是 hc+h−1 与 hc+h，必须是 0、1，所以 c=1/h−1。此时

\[
g(Y)=H/h-Y_i.
\]

然而全一向量上的值为 d/h−1≥3，不是 Boolean，矛盾。唯一低层分支被排除。

结合 §2–§4，f 只能是 0、1、C、1−C、Y_i、1−Y_i。这是实系数的完整分类，不是枚举整数系数。

在上边界 h=d/4 时，排除唯一低层分支的值恰为三，故边界仍成立。上界假设不可从本论证中随意删除：若改为 h=d/2，函数 H/h−Y_i 在 0、h、d 三个 slice 上都 Boolean，却不是 literal。该例在本 Exact 参数域外。

## 5. 从线性 Gram 等式到支持上的 Boolean 函数

固定任一新原 endpoint X 及其仿射 f。令 G=X−f。共同 M3 中 Lhat(G²)=0，故 G 是零向量，与每个次数≤3 多项式 Q 正交：

\[
\widehat L(GQ)=0,\qquad\deg Q\le3.\tag{2}
\]

对 r=1,2,3,4，恒等式

\[
X^r-f^r=(X-f)\sum_{j=0}^{r-1}X^{r-1-j}f^j
\]

右侧第二因子次数≤3，所以 (2) 给 Lhat(f^r)=Lhat(X^r)。原 Boolean 矩等式支付到次数四，使这四个 X 矩都等于 Lhat(X)。基础次数≤4 与真实 P 一致，因此

\[
\mathbb E_P[(f^2-f)^2]
=\widehat L(X^4-2X^3+X^2)=0.\tag{3}
\]

被积函数逐点非负，P 每个支持点质量严格正，故 f 在整个 P 支持上 Boolean。§2–§4 分类立即适用。

本步只使用共同 M3 的明确零向量正交与原第四次 Boolean identities，没有假定新增 endpoints 已有真实联合 law，也没有给它们免费条件概率。仅一阶相等显然不足：独立 Bernoulli(μ) endpoint 与常数 f=μ（0<μ<1）一阶相等，但 f 不 Boolean；它们的 Gram 差范数为 μ(1−μ)>0。

对两个选定 endpoints X、X'，令各自仿射函数为 f、f'。式 (2) 用次数一乘子就给

\[
\widehat L(XX')-\mathbb E_P(ff')
=\widehat L((X-f)X')+\widehat L(f(X'-f'))=0.\tag{4}
\]

一阶替换同样成立。这里没有声称 M2 不能得到任何类似结论，只是不把本 Proof 使用的 degree-three 正交性免费记到 M2。

## 6. 不同 primitive bits 的 pair 支持

每个 t∈{C,Y_1,…,Y_d} 在 Ω0 上都取 0、1。任两个不同 primitive bits 的四种 joint pattern 在 Ω0 上也都出现：

* 对 C,Y_i，用 Y=0 或全一，并选择 C=0 或 1。
* 对 Y_i,Y_j（i≠j），00 用全零，11 用全一，10/01 分别选包含其一、不含另一的 h-subset；1≤h≤d−1 保证存在。

这些点在 P 下全有正质量。因此两个非零 literal/constant 的乘积期望为零，当且仅当它们是同一 primitive bit 的互补 literals。常数一与任意非零 literal/constant 的乘积期望都严格正。

## 7. 同机 unit owner 结论

对指定 unit head w 的 endpoints，§5 已将所有 pair 替换为真实 P 下的 literal pairs。原行 CONFIG(B) 在 B<2 时不能同时含两枚不同原 unit jobs，故它要求所有这些 pairs 为零；非负的其他处理时间不改变此事实。

由 §6，若有两个正 owners，它们必须是同一 bit 的互补 literals。任何第三个非零函数不可能同时与二者互斥，因为它们之和恒为一；常数一也只能单独出现。所以正 owners 至多两个。零一阶端点分类后只能是常数零，不限制其原数量。

原 one-hot 保留所有 jobs 的身份，但分类本身不需要利用同 job 的额外关系。结论只限制被仿射 Gram 关系覆盖的原 endpoints；不能忽略同 head 的非仿射 owner 后声称总数界。

## 8. 条件背景与原物理高 degree 反例

逐固定背景应用时，必须在那个背景下重新拥有 Ω0 全支持及相应的共同矩/仿射/pair 条件。若条件化缩小了支持，或者只给了一个未条件化 M3，不能免费复用上述前提。

Exact 的跨背景例子保留原七态星；新增 N 枚不同原 jobs J_alpha，各只可在 w、自己不同的 u_alpha 用时一。β 独立均匀选 [N]，仅 J_β 随 C 在 w/u_β 开关，其余 J_alpha 全留自己的 u_alpha。每枚 job 仍完整执行。

固定 β 后，所有新 endpoint 是 C、1−C、0、1，确实仿射。跨 β 的 w 边际为

\[
\Pr(J_\alpha\to w)=\Pr(C=1)/N=(1/10+p)/N>0.
\]

任两不同 J 的 w indicators 点态互斥，所以 pair 均为零；w 的 unit 总负载为 C，其余新增机器负载为一或 1−C，全部≤1。于是任意 N 个物理 unit 资格都可有正边际，而每个固定背景只有一个正 owner。

该全局函数还依赖 β，不能改称“只仿射依赖同一组 C,Y”的反例。它恰说明 fiber 内的分类不等于总物理 degree 界。也不能据此推任何 actual near-two gap；全部新增 jobs 回各自 private home，与原星峰一调度相容。

## 9. 最终范围

这是一个有限代数 lemma 与一个普通原 job scope 反例，不是 SDP finder、算法或一般不可能性。它解释固定完整七态背景下，仿射 Boolean 端点只会复制 primitive literals，真正同背景三 owner 的 unit 共享不能来自这种复制；但非仿射依赖、支持限制、跨背景路由及其全部共同预算仍是开放构造选项。

没有运行软件，没有改 repo，没有把其余七态或 growing-depth 文件的证据升级。本 Proof 与 statement-only 分开冻结，便于后续真正 Exact-only 重构。
