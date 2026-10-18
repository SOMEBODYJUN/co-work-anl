# 七态原星的仿射 Boolean 端点与同机 unit owner 边界：Exact-only

ClaimVersion: UM-SEVEN-STATE-STAR-AFFINE-BOOLEAN-BOUNDARY-v1

2026-10-18，scratch statement-only 作者合同，不含证明。可作为七态局部星的另一 scope lemma；未登记，未独立审查，不声称一般不可能性。

## 1. 原七态 law 的全部参数与支持

任取正偶数 d、s，2≤s≤d/2。令

    eta=s/d, h=s/2, p=eta^3/1000,
    u0=4p(1-eta), e=4/5-p-u0.

基础 Boolean 坐标为 C,Y_1,…,Y_d，H=ΣY_i。P 按以下类别选取 (C,H)，每类内均匀选择 H-subset 作为 Y=1 的位置：

| C | H | 概率 |
|---|---|---:|
| 1 | d | p |
| 1 | 0 | 1/20 |
| 1 | h | 1/20 |
| 0 | 0 | 1/20 |
| 0 | h | 1/20 |
| 0 | d/2 | u0 |
| 0 | d | e |

所有类别及类别内每个集合均有严格正质量。d≥4、1≤h≤d/4；包括 h=1、h=d/4（当该整数端点存在）和 d=4,s=2。

记 S_h={0^d,1^d}∪{y∈{0,1}^d:|y|=h}。P 的支持包含 Ω0={0,1}×S_h；实际支持另含 C=0、|Y|=d/2 的整个 slice。下述分类只需 Ω0 的全部点有正质量，不依赖七个具体概率大小。

## 2. 纯函数分类

对任意实系数 a,b,c_1,…,c_d，令

    f(C,Y)=a+bC+Σ_i c_iY_i.

如果 f 在 P 的每个正支持点均取值于 {0,1}，则 f 必为以下函数之一：

    0, 1, C, 1-C, Y_i, 1-Y_i  (某个 1≤i≤d).

结论也适用于只要求 f 在 Ω0 上 Boolean。没有对系数的符号、整数性或位长作额外限制。

## 3. 共同 M3 扩展中的线性 Gram 等式版本

任取有限个普通原 jobs 及其有限机器端点变量 X_e；每个 e 指定一枚原 job 和一台机器。允许与基础变量重合。设同一个实线性泛函 Lhat 定义在这些变量和 C,Y 的次数≤6 多项式上，满足：

1. Lhat(1)=1，全部次数≤3 monomials 的共同 M3(Lhat) PSD。
2. 对每个只含 C,Y、次数≤4 的多项式 r，Lhat(r)=E_P[r]。
3. 原端点满足 Boolean 及每枚原 job one-hot 的全部总次数≤6 矩等式。特别 Boolean 等式支付到次数四。该条件是在 ordinary original-job 系统中陈述，不增加 logical side constraints。
4. 对某个选定端点集合 A，给出任意实仿射 f_e(C,Y)，并逐个满足线性 Gram 等式

       Lhat[(X_e-f_e(C,Y))^2]=0,  e∈A.

则每个 f_e 都属于 §2 的 literal/constant 清单。对 e∈A，Lhat(X_e)=E_P f_e；对 e,e'∈A，Lhat(X_eX_e')=E_P[f_ef_e']。不要求新增端点先存在真实联合 assignment law；本段是上述共同矩条件的结论。

本段不是仅有一阶等式 Lhat(X_e)=E_P f_e 的陈述，也不声称共同 M2 已足以支付该线性 Gram 版本。

## 4. 同机 unit owner 的精确结论

在 §3 的任意满足假设的扩展中，固定一台物理机器 w，取 A_w⊆A，其中每个 e∈A_w 是不同原 job 在 w 的时间一端点。假设这些原 endpoints 满足同行 pair 零：

    Lhat(X_eX_e')=0,  e≠e' in A_w.

若该行原 CONFIG(B) first/pair 与 Lhat 一致，且 B<2，以上 pair 零自动是必要条件。

称 Lhat(X_e)>0 的端点为此点中的正 owner。则 A_w 中最多两个正 owners。若恰有两个，则存在同一个基础 bit t∈{C,Y_1,…,Y_d}，两个对应 f 分别为 t、1−t；它们在 P 的支持上之和恒为一。如果唯一的正 owner 是常数一，其余全部为零。

该结论只计 A_w 中被仿射 Gram 等式覆盖的端点；若要限制 w 的全部 unit owners，必须将该行全部 unit endpoints 都纳入 A。零一阶端点可以有任意多个；不把正 owner 数误称为原资格度。

## 5. 固定外部背景的条件量词

以上结论可逐固定背景 β 使用，前提是该背景下基础 law 仍对 Ω0 全支持，且该背景下共同矩/仿射等式/pair 零仍满足各自假设。系数、原端点身份及互补 bit 可依 β 变化。

不能仅因未条件化系统满足上述某些条件，就免费给任意背景条件点一个 M3。对真实联合 law，若条件基础 law 对 Ω0 全支持且端点为条件仿射 Boolean 函数，则可直接使用 §2/§4 的函数版本。

结论允许固定背景下互补的两个原 jobs 在同一 unit head 轮换；不声称所有逐背景仿射 gluing 的全局物理 unit 入度≤2，也不声称全局所有 owner 的原身份相同。

## 6. 跨背景物理高入度的明确 scope 例子

对任意整数 N≥1，可保留原七态星并新增机器 w,u_1,…,u_N 及 N 枚原 unit jobs J_1,…,J_N。J_alpha 的两个有限端为 w、u_alpha，时间均为一；其余无穷。

取 β∈[N] 均匀、独立于七态 P，完整分配新增 jobs：

    X_(J_alpha,w)=1_{β=alpha} C,
    X_(J_alpha,u_alpha)=1-X_(J_alpha,w).

对每个固定 β，这些原 endpoints 都仿射于 C,Y；同 head w 此时只有一个可能的正 owner。跨 β 积分后，w 的 N 个原 unit endpoints 全有正一阶，且 pair 均为零。所有新增机器逐样本负载≤1，全部 jobs 完整执行。此例不矛盾于 §4，也没有实际 near-two gap；它只排除将条件 owner 界扩大为无条件物理 degree 界。

## 7. 不包含的结论与状态

本合同不声称任何新扩展必然存在，不声称新增全局 quadratic load localizers 自动保留，不输出调度或 SDP finder，不给一般 UM 算法、hardness 或所有共同 law 必须非仿射的结论。

准确含义是：若坚持同一个完整七态支持、固定背景以及所有有关新原端点的仿射 Gram 关系，则真正的同背景三 owner unit 共享不可能；要越过此边界必须改变至少一项假设，不能把新增非仿射依赖、支持限制或跨背景路由当成已付款。

作者 Proof 将另冻，未包含在本 Exact。只据本文件独立攻击者不应先读作者 Proof。
