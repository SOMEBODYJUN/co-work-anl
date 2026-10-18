# Working Exact-only：共享UD叶与 O(1/k) home 上界候选

2026-10-18，/root/sol_general_repair。独立于冻结v4的后续working对象，未独立审查，无正式canonical Claim ID，不升级v4域、算法或审票。此文件只给候选精确合同，作者机制和证明另冻；任何新审者应先只看本文件。

## Objects / Domain

完整typed normalized-flat Q有任意输入正整数k个outers，每outer恰一个非空normalized indexed state，正系数为它的homes g_j上的w_j>0，各outer Σw_j=1。全部homes全局物理互异，每home恰一个helper，其own indexed state为该home的unit singleton。helper其余所有fallback indexed states是B上的任意完整显式normalized非负二进制有理向量，B与homes不交；可没有fallback，fallback supports可任意共享。

k=1时没有额外home-weight上界。k≥2时要求

    ν=max_j w_j ≤1/(1024k).

还允许任意多个额外leaf groups，全部正支持只在B。固定ε=15/16，令E_l={u∈B:max_s p_lsu≥ε}，要求b_l=max_s Σ_(u∈B outside E_l)p_lsu<ε，即leaf值≥ε iff拿到E_l中至少一个资源。所有group菜单非空、所有states normalized；别无groups。叶图可以没有完整matching，仍在输入域。

每个indexed state/resource pair至多一个listed incidence；显式零incidences、重复indexed states、unused resources完整保留。正支持条件不约束零incidences的资源位置。结构呈现随Q给出，不要求从一般矩阵识别。

## 全部ordinary jobs

每state建不同private machine，每资源建resource machine。每group一枚unit selector只去该group全部原state privates；每listed incidence一枚原不可拆job，private time为原系数、resource time精确1，其他∞。若groups、states、incidences、resources数为G,S,I,U，则有S+U台机器、G+I枚原jobs、S+2I个finite endpoints。全部selectors、未选state payload及zero jobs必须运行。

## Exact Statement / Quantifiers

候选声称存在固定确定性worst-case总位多项式算法，输入只有上述完整Q，显式生成完整P(Q)并输出每枚原job在原有限端点上的合法assignment σ，满足C_max(σ)≤(19/10)OPT(P(Q))。k、helper数、leaf数、state数、资格度、支持宽度和分母数值均为输入，次数为绝对多项式。

没有OPT、target、profile、joint law、feasible LP/PSD point或精度oracle输入。不用随机运行时间、指数joint profile枚举、exact transcendental/SDP oracle或隐藏的state optimization oracle。允许标准确定性有理LP、matching/mincostflow、整数circulation及多项式位有理算术。

## Scope / Status

此域严格包含冻结v4在k≥2的ν≤1/(16384k²)域，k1域相同；这是新候选，旧v4原件和审查不变。没有覆盖multi-state outers、重合homes、homes上的额外leaf、一般nonUD extras或一般ordinary UM。无端到端软件、外审、新颖性或已完成独立证明审查声称。一般UM-TARGET-v1仍OPEN。
