# 实际前缀覆盖信用：独立内部重构

审查来源：本轮 independent_bottleneck 研究员。父方只发送对象与待审公式，研究员未读 query_row 的推导稿，先独立重构后回报。本文件保留其实际结论；不是外审、新颖性认证或一般 half 审查。

令 p=m-r，r>=1 包括当前玩家。对客户 x，旧负载 b_x、实际剩余 r 人负载 a_x，P={b>0}、C={b+a>0}、F=|C\P|。任意比较并集 O，

    Omega=sum_(x in O)1/(b_x+1),
    A=|C|-|O|+Omega,
    V=sum_(x:a_x>0) a_x/(b_x+a_x).

独立逐客户重构得到

    A=F+sum_(x in P intersect O)1/(b_x+1)+|P\O|.

旧覆盖外，O 对 Omega 的一单位与 -|O| 相消；旧覆盖内，在 O 中剩 1/(b+1)，在 O 外剩一。

对 1<=a<=r、1<=b<=p，

    (b+a)/[a(b+1)] >= (b+r)/[r(b+1)]
                      >= (p+r)/[r(p+1)]=beta.

a=0 不需要除以 a，只给非负信用。旧覆盖且 O 外的系数一不小于 1/(b+1)。p=0 时 A=V=F，beta=1。故 A>=beta V+(1-beta)F，全范围包括零客户、空主题与重复主题。

达到性也独立重构：m>r，单客户单主题，所有玩家被迫选同主题，整个有序历史树均 SPE。非空比较并集给 A=1/(p+1)、V=r/m、F=0，故 A/V=beta。这只认证该静态信用合同的最佳系数。

后续独立核对符号式：

    A-V=sum_(old intersect O) b(1-a)/[(b+1)(b+a)]
        +sum_(old outside O) b/(b+a).

负项只在 old intersect O 且 a>=2 出现，等于把 a 个实际后缀覆盖代数压到一个时旧玩家返还的相反数。它不能变成删除玩家后仍 SPE 的断言。

审查边界：未证明 ROW、RETURN?、最低收益 ROW、全局安全值付款或 Q-CAG-HALF。审查特别要求 V 包括当前 i；若只指严格后继，此文件没有审查那个不同命题。
