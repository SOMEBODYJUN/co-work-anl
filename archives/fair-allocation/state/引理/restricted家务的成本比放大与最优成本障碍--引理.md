---
id: fair-allocation/restricted-chores-binary-scaling-and-optimal-cost
kind: lemma
type_tag: 引理
title: restricted家务的成本比放大与最优成本障碍
status: proved-conditional-transfer; exact-obstruction-family
---

# 条件性binary放大接口

有限可加chores，每件g有公共正成本c_g，各代理评价c_i(g)∈{0,c_g}。令0<c_min≤c_g≤c_max，Δ=c_max/c_min；全零物品可先归零单列，不进入该比值。binary代理成本为b_i(g)=1_{c_i(g)>0}。

若给定一个完整分配X，在binary实例中同时EFX和PO，则原成本下X为Δ-EFX且社会成本最优。这里是对已给binary解的条件转移；binary EFX+PO的存在/构造须另用已审定结果，不能由有限三物品例代替。

证明：对全部i,j及自身g∈X_i（包括c_i(g)=0），
\[
c_i(X_i\setminus\{g\})\le c_{max}b_i(X_i\setminus\{g\})
\le c_{max}b_i(X_j)\le Δc_i(X_j).
\]
若某物品被分给binary成本1的人而另一人成本0，移给后者会Pareto改善，违反binary PO。因此只有所有人都评正的不可避免物品承担成本，每件成本恰为c_g；其他物品均以0承担。社会成本恰为不可避免物品的成本和，是全体分配的下界。右侧为0时上式仍成立，无需以0作除数。

# 最优社会成本约束下的精确障碍

两人三件，取任意C≥c>0，成本矩阵
\[
\begin{pmatrix}C&c&0\\C&0&c\end{pmatrix}.
\]
社会最优值C。达到该值必须把第二件给第2人、第三件给第1人，第一件任给一人；恰有两个最优分配。拿第一件的人也拿一件自己成本0的物品。删除该零物品后自身仍成本C，而评价对方包成本c，故EFX因子至少C/c=Δ；其余比较均满足Δ，故该约束下最佳因子恰为Δ。来源C=5,c=1只是此解析族的一个特例。

这不否定无社会最优约束的更好公平因子，也不构成一般chores不存在性。原三物品记录及有限配额MMS另见[rank玩具与MMS审查](../审查/退役公平家务rank玩具与三值MMS三源处置--审查.md)。
