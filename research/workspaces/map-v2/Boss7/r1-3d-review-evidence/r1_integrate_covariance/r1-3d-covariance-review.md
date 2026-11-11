# r1-3d-covariance：同一原source的净cap、逆鞅前缀及RESET定向审读

## 范围与结论

仅比较已done包 `customer-attraction-3a-3a-816758d461ee52fb` 的四条指定相连边。没有新主覆盖认领，没有修改clone、Git、队列、registry或integration，没有重跑有限扫描、完整SPE树或LP实验。精确边文件SHA256、八个端点registration_pin、正文/证据文件SHA256及逐项绑定检查保存在同目录 `r1-3d-covariance-pins.json`。

四边在其当前作用范围内均可清：`global-net-source-ledger-static-half`、`single-query-reverse-energy-prefix`、`signed-reset-real-edge-pair` 完整覆盖各自目标的已证合同；`orthogonal-prefix-payment-reduction` 仅为开放PAY对象的已证局部贡献。没有发现需要修正的公式方向、遗漏承重前提或失效pin。第四边的 `relation_mode:unconditional` 只描述其不附加付款假设的局部正交/Cauchy归约，不能解释成无条件证明PAY。

## 实读承重正文

1. `research/IMPLEMENTATION.md`：第三阶段关系、whole_result/contribution、条件支持、整合及定向替代规则（172–221、276–299行）；根 `AGENTS.md` 全文。
2. `archives/customer-attraction/state/问题/真实重放协方差的定量付款--问题.md` 全文，特别是“真实未来边的规范门槛重置”“切线EDGE与不同主题同叶残差”“raw坐标流的逆鞅式与累计前缀”“一个自足的half充分金额接口”。
3. `archives/customer-attraction/state/算法/固定进入槽的真实后继重放与一次势预算--算法.md` 全文：规范门槛等价、源可行、REPLAY、FLOW/TELE及共同μ的GLOBAL-NET银行。
4. `archives/customer-attraction/state/引理/规范门槛均值域与复制偏离的精确成本--引理.md` 全文，特别是“三种期望域及其各自银行”。
5. `archives/customer-attraction/state/引理/固定中间动作的末位需求运输与单查询信息预算--引理.md` 全文，信息预算章条件塔与正交证明为本次承重部分；末位运输部分未用于新增边。
6. `archives/customer-attraction/state/引理/规范门槛单次重置与非统一价格复制残差--引理.md` 全文。
7. `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` 全文；`archives/customer-attraction/state/资料/可信端点共同付款的接口合同与停界--资料.md` 全文，用于模型量词及区分旧行均值银行。
8. 当前registry八个精确source/target完整记录；四条边的全部文字、endpoint_pins及evidence_pins。

## 1. GLOBAL-NET源账、静态信用与half充分合同

边：`boss6-r50-cag816-global-net-source-ledger-static-half`。

在固定同一完整σ、actual有序前缀及原source `z_A=finish_σ(h_i,A)` 上，原当前角色IC给 `I=W−Σ_i E_p d_i(z_A)≥0`，严格未来沿原σ给 `S_total=Σ_i E_p S_i(z_A)≥0`。GLOBAL-NET只有 `Σ_i E_Q B_i≤W` 一条净cap，`B_i=d_i−S_i`，因此有限LP对偶具有共同μ≥0、自由η_i和对全部允许raw列非负的 `r_i=η_i+μB_i−w·ell_i`。它不是把MF的λ或ROW-NET的μ_i正规化。

Q为同一shadow `w=ρt²` 的最优点时，强对偶/互补性使 `H_Q=Ση_i+μW=Σ_i E_Q(w·ell_i)=m w·L`。原source代入对偶定义，精确给 `G=H_Q−H_source=μI+μS_total+Σ_i E_p r_i(z_A)≥0`。三项是同一G的分拆，不能额外叠加。

逐客户倒数恒等式在 `t=1/(1+L)` 下成立；p支持最大主题t价格给常数 `mγ`。将源权 `1_A t²` 分为w与中心化部分，得到 `Σ_i E_p d_i=mγ+D−Cov+G`；再加I，恰是 `W−mγ=I+G+D−Cov`。此处Q、L、t、p、μ、G、D、Cov必须来自同一个接口，不可更换为对齐源或别的query点。

每个删除同一i槽的合法raw叶有m−1个目录行动，所以L是总质量m−1的合法分数负载，`Σ_x L_x t_x≤(m−1)γ`，即 `Qstat≥0`。最优覆盖重数c*逐客有 `1_{c*>0}≤(c*+L)/(1+L)`，故 `OPT_m≤mγ+ΣLt=(2m−1)γ−Qstat`。

若再证明同一接口的PAY `Cov≤I+G+D+(γ+Qstat)/2`，则 `2W≥(2m−1)γ−Qstat≥OPT_m`。该边完整证明的是包含这一“若……则……”的C1对象，未证明PAY前件、未证明自洽最优接口存在，也未把六人全称half提升为已证。零客户/γ=0无需除法，m=1同式有效。

## 2. 单查询逆鞅与完整累计前缀

边：`boss6-r50-cag816-single-query-reverse-energy-prefix`。

全部行共用一个A∼p；联合Y独立于A，各行边际为原先选定Q_i，Y行间不要求独立。未来源单元均是原σ在各自actual前缀强制A后的确定函数。`G_k=σ(Y,第k步后未擦除源单元)` 是递减信息链；因此M_k也是逆时间条件期望过程。每个正概率Y=y fiber内A仍为p，可反向应用INFO。末端 `G_N=σ(Y)`，独立性给 `M_N=v`。

`δ_k=M_{k−1}−M_k` 满足 `E[δ_k|G_k]=0`，不同增量正交，所以 `Σ E||δ_k||²=E||M_0−v||²≤V_p`。源INFO仅写非负t，目标的任意实t可用固定对角符号等距J延拓：对v_A、v、b、c及条件期望同时乘J，范数和内积保持。零坐标取J_x=1即可，无须缩域。

同一源查询下，actual固定过去的贡献对中心化源权期望为零；终端删除负载只依赖Y，亦为零。因此 `Cov=Σ_k E〈v_A−v,b_k−c_k〉`。`b_k−c_k` 对 `G_{k−1}` 可测，条件期望给第一等式；`M_{k−1}−v=Σ_{l≥k}δ_l` 再有限换序，得到 `Cov=Σ_l E〈δ_l,P_l〉`，其中 `P_l=Σ_{k≤l}(b_k−c_k)`。累计前缀不可删，也不可为同一增量影响多个单元重复领取V_p。

raw与真实重放逐(A,Y)有相同起点和最终Q端点，固定源权的总有符号线性功只依赖端点，故两总功相等。该等号既不赋予raw边真实IC，也不许可交换逐边银行。m=1时N=0，所有前缀和为空、Cov=0。

## 3. 正交前缀Cauchy归约与平方充分条件

边：`boss6-r50-cag816-orthogonal-prefix-payment-reduction`；目标PAY对象仍open。

在上述同一信息链上 `E[δ_l|G_l]=0`，所以 `E〈δ_l,E[P_l|G_l]〉=0`。令 `P_l^perp=P_l−E[P_l|G_l]`、`Xi_perp=Σ_l E||P_l^perp||²`，精确得 `Cov=Σ_l E〈δ_l,P_l^perp〉`。有限直和L²的Cauchy给更强的绝对值式 `|Cov|≤sqrt((Σ_l E||δ_l||²) Xi_perp)≤sqrt(V_p Xi_perp)`。

设付款右端 `R_pay=I+G+D+(γ+Qstat)/2`。C1接口中I/G/D/Qstat逐项非负，t=1/(1+L)>0使γ≥0，因此 `R_pay≥0` 已经付清。于是额外同接口数量条件 `V_p Xi_perp≤R_pay²` 蕴含 `sqrt(V_p Xi_perp)≤R_pay`，继而PAY及上述half链。平方方向正确，非负右端并非隐藏假设；无需除V_p，故V_p=0或N=0亦有效。

这只是PAY的充分条件，不是等价条件：有符号Cov可因抵消很小，而Xi_perp仍大。能量式没有控制Xi_perp。目前既没有 `V_p Xi_perp≤R_pay²` 的通用证明，也没有支付同一Cov的替代有符号配对界。因此该边的contribution/result成立，remaining必须保留；若下游将其作为whole PAY支持或把额外数量前件视为已证，则构成误用。

## 4. RESET/EDGE/PAIR与最后enter的实际抵消

边：`boss6-r50-cag816-signed-reset-real-edge-pair`。

每条真未来j边的旧端在精确有序历史g_j之后沿原σ规定行动，新端强制y_j后仍沿原σ；当前分支差 `Γ_j=u_j(z)−u_j(z′)≥0`。j以前M相同，然而祖先的终局收益会变，故直接相减B给 `ΔB_i=Δd_i+Γ_j+Σ_{i<k<j}[u_k(z)−u_k(z′)]+S_desc(z)−S_desc(z′)`。只有严格后继两端的S_desc均非负；中途已强制祖先不重新享有原source全部floor。旧MF的DIFF同理保留祖先带λ损失，且只能使用其固定旧对偶。

未来边始终保持原A，`E_A=d_i−2Σ_A t+w_A·c`，且Δc=Δell_i，故 `−w_A·Δell_i=Δd_i−ΔE_A`。同一GLOBAL-NET对偶相减给 `w·Δell_i=μΔB_i+r_i(z)−r_i(z′)`，相加即EDGE，符号正确。任意目标的PAIR是加减同一新叶u_j(z′)的恒等式；仅y_j=A时单位同主题保证 `d_i(z′)=u_j(z′)`，否则方括号没有符号。旧MF copy另保 `(μ−λ_h)d_i(z′)`；新GLOBAL-NET共同μ由改变约束产生，不能回头免费消除旧残差。

最后静态enter将 `(h_i,A,y_{>i})` 改为y并冻结尾，删除同一槽i给 `Δell_i=0`，但一般 `ΔB_i≠0`。同一对偶定义精确给 `μ[B_i(y)−B_i(pre)]=r_i(y)−r_i(pre)`，所以 `μΔB_i+r_i(pre)−r_i(y)=0`。这两个通常非零项在最后边实际抵消，必须共同加入：未来边合计原先止于pre的 `μ(B_pre−B_source)+r_source−r_pre`，加该零项后才改写为到原Q端点的 `μ(B_y−B_source)+r_source−r_y`。删除最后边会使银行端点错误。最后边无进入者IC，也不能套固定A的切线E_A，因为进入标签已变。

## 可直接并入3D审读的段落

在原完整σ及同一GLOBAL-NET最优Q、共享p/L/t/shadow/μ上，源对偶差G只有一份，`W−mγ=I+G+D−Cov` 与非负静态信用Qstat准确给出PAY⇒half的充分链，未证明PAY本身。单一共享A和独立目标Y形成递减信息链；一次能量预算及完整累计前缀给 `Cov=Σ_l E〈δ_l,P_l〉`，正交化后 `Cov≤sqrt(V_p Xi_perp)`。付款右端R_pay由同一C1接口非负，故同接口 `V_p Xi_perp≤R_pay²` 是有效但尚未支付的充分数量条件；不能跨query合并预算。真未来RESET保全部祖先损失，任意目标PAIR保同叶不同主题差；最后enter虽删除功零，μΔB与约化成本差须抵消并保留以到达原Q。四边分别为三个完整已证合同和一个对open PAY的局部贡献，不推出六人全称half。

## 开放义务及集成边界

- 在同一原source、同一GLOBAL-NET最优Q及同一query链证明Xi_perp足量上界，或给直接控制有符号Cov的另一合法配对。不能叠加不同query的V_p、γ、G或不同域银行。
- 任意目标同叶残差、中间祖先损失、source/arrival容量及跨行前缀势兼容，必须在同一预算内支付；局部IC、固定势望远镜与正部金额不可混用。
- 若研究目标需从“每个满足接口的对象”推进到“所有实例”，还须另行提供所需自洽最优/共享支持接口的存在与原问题映射；本次四边没有这项主张。
- C1的truth_status:proved只覆盖源账/静态界/条件half引理，C3及RESET为恒等式合同；PAY维持open。集成可复用现有边，无需替代任务或新增覆盖。
