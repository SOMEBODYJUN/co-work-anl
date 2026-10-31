---
id: "customer-attraction/root-reset-pair-and-auxiliary-tail-covariance"
kind: "lemma"
type_tag: "引理"
title: "根重置对恒等式与辅助尾份额协方差的正确税项"
status: "proved-algebraic-identities; original-unconditional-tax-factor-corrected"
summary: "在任意合法有序历史比较同一完整策略的真实强制分支，保留额外查询槽；精确分解独立同分布查询预算，并修正原稿多写的p_x及尾份额解释。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-24e40cab6b8d43ecbbf1c15c4d0edcd5/dynamic_flow/covariance_reset_criterion.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-24e40cab6b8d43ecbbf1c15c4d0edcd5/dynamic_flow/cartesian_pair_obstruction.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2f6cae284faf43fea7a09c0a4fe7c679/relay/aggregate_extra_slot_gap.md"
---

# 根重置对恒等式与辅助尾份额协方差的正确税项

## 精确域及两个不同分母

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)：有限单位客户N，有限非空共同主题目录，单位提供者依次观察全部有序历史各选一次主题，客户价值在最终覆盖者间均分。固定一份完整有序历史纯SPE、任意合法前缀h及余下r≥2人，包含当前决策者。目录可含空主题，允许重复行动、零客户及任意离轨历史依赖平局。

前缀对客户x的负载为b_x≥0。对每个合法当前行动A，强制A后沿**同一份给定策略**的真实后继完成；n_A(x)∈{0,…,r−1}只数其后玩家对x的覆盖。置
\[
c_x=b_x+1,\quad a_A(x)=\mathbf1_{x\in A},\quad d_A(x)=c_x+n_A(x).
\]
当前人的强制收益与真实SPE松弛为
\[
D(A)=\sum_x\frac{a_A(x)}{d_A(x)},\qquad e(A)=u-D(A)\ge0,
\]
其中u是该历史按原策略的当前人最终收益。a_A=0时该客户对D贡献零，d_A仍是正的辅助分母。

额外槽查询T面对完整强制分支（保留当前行动者）得到
\[
K(T,A)=\sum_x\frac{a_T(x)}{c_x+a_A(x)+n_A(x)}.
\tag{K}
\]
其分母是原全部玩家负载再加查询者一单位。K只是静态比较量；真实游戏仍只有原人数，查询不成为隐藏随机玩家。

定义辅助尾份额
\[
F_A(x)=\frac{n_A(x)}{c_x+n_A(x)}.
\tag{F}
\]
当x∈A时，F_A正好等于该强制分支中后继玩家在x的总份额。x∉A时实际尾总份额的分母是b_x+n_A(x)，而F_A带有额外一单位占位；它不能无条件解释为真实尾利润。实际分母为零时实际尾份额定义为零。以下代数始终用(F)，没有把两种分母互换。

## 重置对恒等式

对任意A,T定义对称的有符号重置量及非负共同客户税
\[
R(A,T)=\sum_x\frac{(a_A(x)-a_T(x))(n_A(x)-n_T(x))}{d_A(x)d_T(x)},
\]
\[
J(A,T)=\sum_{x:a_A(x)=a_T(x)=1}
\left[\frac1{d_A(x)(d_A(x)+1)}+
      \frac1{d_T(x)(d_T(x)+1)}\right]\ge0.
\]
则有全输入恒等式
\[
\boxed{K(T,A)+K(A,T)-D(A)-D(T)=R(A,T)-J(A,T).}
\tag{RESET}
\]
证明逐客户分四种membership：

| a_A,a_T | 左端逐客户差 | 右端 |
| --- | --- | --- |
| 0,0 | 0 | 0 |
| 1,0 | 1/d_T−1/d_A | (n_A−n_T)/(d_Ad_T) |
| 0,1 | 1/d_A−1/d_T | (n_T−n_A)/(d_Ad_T) |
| 1,1 | 1/(d_A+1)+1/(d_T+1)−1/d_A−1/d_T | −1/[d_A(d_A+1)]−1/[d_T(d_T+1)] |

所有分母正，逐客户相加即得。它也等价于
\[
2u-K(T,A)-K(A,T)=e(A)+e(T)+J(A,T)-R(A,T).
\tag{P}
\]
这是一个历史中两个真实强制分支的比较；无需两个分支有相同后继，也无需相同负载历史采用相同策略。

由F_A−F_T=c_x(n_A−n_T)/(d_Ad_T)另有
\[
R(A,T)=\sum_{x\in A\setminus T}\frac{F_A(x)-F_T(x)}{c_x}
       +\sum_{x\in T\setminus A}\frac{F_T(x)-F_A(x)}{c_x}.
\tag{T}
\]
所以重置来自当前membership与诱发的辅助尾覆盖之间的响应差。令V_A,V_T为两分支**真实后继总利润**，则R_+≤V_A+V_T：逐客户只保正项，A\T一侧至多F_A/c_x≤F_A，T\A一侧至多F_T/c_x≤F_T；这些保留分支恰都覆盖该客户，辅助尾份额等于实际尾份额。该粗界使用两条离轨分支的利润，未将它们支付为原实际路径福利。

## 独立同分布抽样与税项勘误

取任意目录分布p，A,T独立同分布于p，p_x=E_p a_A(x)。定义
\[
\bar D=E_pD(A),\quad\bar e=u-\bar D\ge0,
\quad G(p)=E_{A,T}K(T,A)=p^{\mathsf T}Kp.
\]
由(T)和独立性，
\[
\boxed{E R=2\sum_x\frac{\operatorname{Cov}_p(a_A(x),F_A(x))}{c_x}.}
\tag{C}
\]
例如逐客户展开E[(a_A−a_T)(F_A−F_T)]，同分支两项各给E[a_AF_A]，交叉两项各给p_xE[F_A]，恰为两倍协方差。

共同税的正确无条件期望是
\[
\boxed{E J=2\sum_x p_x\,E_A\left[
\frac{a_A(x)}{d_A(x)(d_A(x)+1)}\right].}
\tag{J}
\]
第一份税含a_Aa_T而仅d_A依赖A；独立T贡献**一次**p_x。另一份交换A,T相同。也可写作
\[
2\sum_{x:p_x>0}p_x^2 E_A\left[
\frac1{d_A(x)(d_A(x)+1)}\,\middle|\,a_A(x)=1\right].
\]
p_x=0的项取零，不形成未定义条件期望。

原`covariance_reset_criterion.md`式(5)在无条件期望内仍含a_A，却写了p_x²，因而多一个p_x。后续原稿`aggregate_extra_slot_gap.md`§3已明确给出同一修正，并在§2说明F_A的占位含义；本次实读比较后按正确式(J)入库，原字节保持不变。原(RESET)、协方差式以及含EJ符号的预算等式不受影响；代入错误税值的数值计算须另核。例如八人基例取p_3=p_7=1/2，直接EJ=29/30，错误式只给29/60。

平均(P)得到
\[
\boxed{u-G(p)=\bar e+\tfrac12EJ-\tfrac12ER}
\tag{B}
\]
\[
=\bar e+\sum_xp_xE_A\frac{a_A(x)}{d_A(x)(d_A(x)+1)}
 -\sum_x\frac{\operatorname{Cov}_p(a_A(x),F_A(x))}{c_x}.
\]
因此固定p的真实收益封顶有准确等价条件
\[
G(p)\le u\quad\Longleftrightarrow\quad
ER\le2\bar e+EJ.
\tag{CAP}
\]
逐对R(A,T)≤e(A)+e(T)+J(A,T)足够，但比(CAP)更强；[八人局部账本障碍](../障碍/根重置局部账本的笛卡尔放大--障碍.md)给逐对条件失败而特定p仍满足(CAP)的明确分离。

## 范围、比较与接续

代数身份本身适用于任意强制分支映射，SPE仅在e≥0处使用。它没有证明(CAP)对全部SPE及全部p成立，也没有提供满足它的p。较强的G(p)≤\bar D等价于ER≤EJ，删掉了可用的真实激励松弛；[三人八客户反例](../反例/同分布额外查询高于平均强制收益--反例.md)只否定这一较强比较。

K保留强制当前玩家；既有[跨分支预算定义](../定义/跨分支去相关与激励补偿总预算--定义.md)的C_i则先删去该玩家，二者差一真实槽，不能搬用已失败的全p删除槽结论。既有[完整终局推送协方差恒等式](完整终局推送的协方差响应恒等式--引理.md)先平均负载再取倒数；本页G先对各整数分支取倒数再平均，也不是那个F的同名重写。

在实际路径每节点可分别应用(B)。若另外证明Σ_iG_i(p)≤W并取适当静态安全查询，就能连接半覆盖的充分预算；后续比较源明确把相应协方差总支付留作未决，不从恒等式推出非负性。自由列分布的Mfull在每节点另问是否存在Q使max_T(KQ)_T≤u；固定源分布为p的本页不是对自由Q的无损刻画。路径级Mpath亦未由本页判定。

[精确资源](../../tools/evidence/dynamic-flow-workspace/README.md)保存四主源、六执行依赖、四比较稿及本轮一次原程序/一次原DAG核验。定义级补核1280个标量RESET情形、三人前两层150对与八人根64对，并直接对比正确/错误税期望；普遍身份由上述代数证明承担。各源双冻结定位及SHA完整保留，不以有限检查、内部审读或程序PASS冒称外审、新颖性或一般六人结论。对象关系已解释，正式超图留第三阶段。
