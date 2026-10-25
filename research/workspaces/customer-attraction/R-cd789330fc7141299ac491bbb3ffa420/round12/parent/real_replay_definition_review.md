# 真重放与坐标重放：root按定义独立核查

原half仍OPEN。本审查核[真流](../tree/real_replay_covariance_flow.md)与[几何流](../geometry/conservative_raw_tail_replay.md)的系数、端点、IC及一次银行范围，不证明缺失的乘子上界。非外审/新颖性认证。

固定actual行i、query标签A~p、独立目标y~Q_i。先取X0=原σ在(h_i,A)后的完整叶。对j=i+1,...,m，固定目标未来前缀y_(i+1)..y_j，余尾每次执行原σ。每步之前的叶确为原σ在当前历史的规定叶，强制y_j后亦执行原σ，故Γ_j≥0是原完整策略在真实有序历史上的IC。最终叶(h_i,A,y_>i)与目标y只差进入槽；最后改A为y_i使端点恰为y。

给每路径质量p_A Q_i(y)，所有层单位质量守恒，给定A起点质量恰p_A。删除固定query槽i的负载在最后改tag时不变。令psi_A(z)=Σ_x(1_(x∈A)−ρ_x)t_x² ell_i(z)，它沿每条路径是真正固定的终局函数。源平均是Cov_i，目标因A与y独立平均为0。因此Cov_i恰为全部future边负的psi增量；最后tag边贡献0。合流仍只用原p_A source质量一次，不能另取各边正部和。

固定row-i的F_i/B_i/r_i也逐路径望远镜。分开rootcap与meanfloor的域可分别用E_Qd≤ui、E_QF_i≤0。新uniform-net域只有合并E_QB≤ui（或所有行总≤W），不能再引用两个分开的端点银行。代回对偶恒等式给一次原source银行；这只支付common-shadow/signed潜势工作，不自动支付diagonal项。

几何坐标流可以冻结原suffix而逐格替换，具有完全相同逐label起终点，故psi及fixed势的总工作相同。但该坐标边之前不一定是原σ规定叶，不能逐边给Γ≥0。Doob恒等式可以与真流的总工作等同，却没有逐边相同银行或前缀乘子范数控制。

BUBBLE链的后续child策略可按counts搬运而改变；其Γ属于对应真正child见证，不可自动叫作原actual-prefix σ行或重复领取原source slack。当前未付仍是signed tangent余项、任意目标与query不同主题的同叶收益差、以及source/arrival容量平衡。
