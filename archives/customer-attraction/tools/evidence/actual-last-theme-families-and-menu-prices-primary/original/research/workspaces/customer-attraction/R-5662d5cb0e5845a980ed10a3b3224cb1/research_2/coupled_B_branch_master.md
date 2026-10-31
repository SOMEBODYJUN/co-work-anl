# 实际B第四枝与显式Ti第四枝的Q/R身份联合

状态：原始行解析语义与发现程序，尚未独立数学审查。这里只对旧16直方图支持
进行联合必要条件优化；任何低于half的点不是SPE，任何该支持上的不可行或
到达half也不是普适六人证明。

## 同一原σ的两种第四位真枝

在原完整六人SPE实际前三主题 `h=(A1,A2,A3)` 后：

- 第四位强制最优比较Ti，原σ续局为 `(Ti,Bi,Ci)`，保留六个旧词
  `(ti,bi,ci)` 的完整八格直方图。
- 第四位强制实际末主题 `B=A6`，原σ续局为 `(B,Q,R)`。

本图不识别这些不同历史的回复。原37条单B枝真实行、CAP和末两人菜单使用
`max_branch_lp.branch_rows`，语义同本区 `tail3_B_projection.md`；
这里保留Q/R会员本身，故比单个ψ(actual,d)投影提供更多相关性。

每个旧hist列质量x分成8种条件状态质量：`q,r∈{0,1}`、`ell∈{0,6}`。
其中ell是B枝第五位对六Ti查询产生的**新**真末回复计数，与旧Ci不同。
状态质量和强制等于x。因末两人消去查询/回复交集后对ell仿射，端点凸组合
包含全部真实ell=0,...,6。旧hist的全部Ti/Bi/Ci会员与q/r相关性被保留。

## 十条跨枝合法报价

对固定客户，记 `p=sum_(j<=3)1_Aj`、`b=1_B`、`q=1_Q`、`r=1_R`，
`vQ=q/(p+b+q+r)`、`vR=r/(p+b+q+r)`，零分子约定为零。
写 `mu_T=sum_i ti/6`、`mu_B=sum_i bi/6`、`mu_C=sum_i ci/6`。

在B枝真实第五位节点 `(h,B)`，Q行动者可改选任何Ti/Bi/Ci，后继末位任意，
故每族平均给

`vQ−mu_J/(p+b+2)≥0`，`J∈{T,B,C}`。

B枝真实末位节点 `(h,B,Q)` 的R可精确查询相同三族，给

`vR−mu_J/(p+b+q+1)≥0`，`J∈{T,B,C}`。

另一方面，在每个旧Ti枝上，第五位Bi和末位Ci可以查询共同目录合法主题Q/R。
定义逐客户

`vBbar=sum_i [bi/(p+ti+bi+ci)]/6`，

`vCbar=sum_i [ci/(p+ti+bi+ci)]/6`，

`thetaB=sum_i [1/(p+ti+2)]/6`，

`thetaC=sum_i [1/(p+ti+bi+1)]/6`。

第五位Bi的真实偏离后续不冻结，只取两名剩余者的安全分母；第六位Ci是精确
最佳回复比较。由此给四行

`vBbar−q*thetaB≥0`、`vBbar−r*thetaB≥0`，

`vCbar−q*thetaC≥0`、`vCbar−r*thetaC≥0`。

上面所有不等号都是**全客户求和后**的非负真实slack；单客户系数可为负。
不同枝利润始终分别保留，没有换成实际福利。六个比较主题允许重复、为空，
所有历史和任意平局仍由同一份原σ定义。

## 联合实现与证据边界

`coupled_B_branch_master.py` 只读调用 research_5 的
`combined_branch_master.build()`（`--latest`），在原1905列后添加128个条件状态
列。原16个hist质量与8状态之和的相等关系逐项保持。新增37条B枝行与上述10条
跨枝行。K使用原master同一个K列。

这些新行只同时涉及旧hist和新Q/R，不含原新回复R_e/Z_e与新Q/R的乘积。
所以给定hist后，将原图隐藏联合分布与新Q/R条件分布作条件独立积即可联合
实现这些所有矩；没有把任意两两矩误当成共同分布。

脚本只写本research_2目录，`coupled_B_master_status.json`记录发现结果。
若获得低于half点，尝试用旧exact_solve对全部原行、新行和边缘等号恢复精确点，
保存为 `coupled_B_master_exact.json`。后续如要声称普适结论，仍须覆盖全部
旧直方图域；本支持压力测试不承担该义务。
