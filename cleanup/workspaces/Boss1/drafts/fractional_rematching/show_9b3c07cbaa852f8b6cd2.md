# Fractional rematching：rank v2增量独立Exact审查

审查者：rank_deficiency_fee，2026-10-18。仅clone外scratch；不改repo、Work/Git、v1/v2 statement或既有冻结记录。

## 1. 对象与真实来源

实际全文读取v2：

`/workspace/scratch/038d9dcc4cac/fractional_rematching_extension_statement_only_v2.md`

whole SHA256：`6acd2c44963d9312ade20efed5128048b81f35b8391b5bc09875ec60ed0205de`。

在此次读取前已冻结v1完整独立审查：

`/workspace/scratch/038d9dcc4cac/fractional_rematching_extension_rank_exact_first_review_v1.md`

SHA256：`b7f8fe124eed85643dda4e48251da3a794b2869b7b22128c55f899198774d5fa`。

实际逐字节比较v1/v2从“## A.”至“## B.”前的全部段落，完全相同。v1中A的完整独立证明与精确bit算法因此原样适用，不改旧记录。本次仍未读作者Proof、其它children新推导。Root已先提示source常数和max/sum安全因子，本记录的v2数值复核不标作盲态发现。

## 2. 范围结论

**A已由v1记录独立证明；v2 B–C保持清楚的E1–E3条件蕴含，其60000、1125000、2250000、1/3000000及rho=2^24的算术与floor-grid损失均通过。未发现v2条件陈述的standing fatal。**

本记录未将source的全部Relaxation Solver/rounding/support/numerical implementation从头审完，故不把条件结论升级为无条件log-CONFIG gap theorem。下列对source末段的核查只说明60000是正确保守吸收该步的因子；仍需外部证明E1–E3的完整有限位实现。

## 3. 正确的source末段比较因子

本次独立访问primary arXiv:2309.04656v1 PDF，实际读取§2.5的Lemma 8/9及末尾列式、Lemma 7检索片段、Theorem 10及§3所列参数；URL https://arxiv.org/pdf/2309.04656 。不把paper主定理相对integral NSW optimum的approximation直接当fractional-benchmark保证。

为核max-to-sum，记w_i=v_i(T_i)、s_i=v_i({π(i)})、nu_i为residual最大singleton。设source同一成功事件已给

    GM_{i∈A''} V_i/(w_i+nu_i) ≤ 10000 d²，

且A''上w_i+nu_i≤2V_i，其余agents T_i空且V_i≤6nu_i。则对任意comparison matching且其Π(V_i+s_i)>0：

    Π_i (V_i+s_i)/(w_i+nu_i+s_i) ≤ (20000 d²)^n。

这是逐项估计加同一成功事件所得，关于π的选择不改变该事件。若某comparison乘积为0，则目标E2不等式本来平凡，无需构造0/0。

Rematching lemma及最终最优matching只给实际输出至少GM_i max(w_i,s_i,nu_i)。正确转为sum的式子是

    GM_i max(w_i,s_i,nu_i)
      ≥ (1/3) GM_i(w_i+nu_i+s_i)
      ≥ GM_i(V_i+s_i)/(60000 d²)。

中间sum必须使用实际w_i=v_i(T_i)，不能凭空换成V_i。因子1/3也不能在下一行丢弃。因此v2用60000是这一套保守核算的正确结果，不依赖paper末尾所印更小常数。这里没有声称原paper无法以更精细分析获得更好常数；只不沿用未经本链证明的小因子。

对c=2、d=5/2，与A的c+1相乘得到

    60000 × 3 × 25/4 = 1125000。

E3若另有至多2的安全slack，则总factor≤2250000。关于所有π的同时保证仍需如E2所述在同一成功事件成立；不是对指数多π作union bound。Paper的成功事件、source lemmas以及数值/位实现仍属待完整验证的external backend，不由以上末段代数单独替代。

## 4. Floor-grid的逐集合误差与编码

设m=|U|≥1、delta=1/(4m)。对每条原normalized clause，

    0 ≤ p_j−tilde p_j < delta。

因此对每个原item子集S，clause损失小于|S|/(4m)≤1/4；总clause质量满足

    3/4 < Σ_j tilde p_j ≤ 1，

故statement写闭区间[3/4,1]安全。逐坐标tilde p≤p，最大化clause后仍tilde v_i(S)≤v_i(S)≤1。每个tilde p为delta的非负整数倍，故tilde v_i(S)为delta整数倍；positive时至少delta。乘4m后单坐标和全部utility均为整数且≤4m。

Floor计算对原binary rational分子分母乘4m后作整数除法即可，按原输入位长和log m多项式，不按1/min p或原分母数值展开。Internal菜单保留原indexed states，可有某些原positive坐标变0，但没有改变原P、原任务或原输入菜单；最终真实utility取原v。

Grid只消除了这类过小value的数值尺度，不单独证明任意backend所有内部步骤都bitpoly；E3仍是明确条件。原rational输入和每条clause原编码必须照计。

## 5. 两种3/4前件不能混淆

Unit-FSLP路由：对原positive支持P_{i,s}，tilde系数的positive支持包含于P_{i,s}，因此

    tilde v_i(P_{i,s}) ≥ Σ_{j∈P_{i,s}}tilde p_{i,s,j} ≥ 3/4。

原lambda定义的y行和/原item容量完全不变，全部positive entries在tilde v下也positive，故B_tilde(y)≥3/4。此route只用了显式fractional certificate，不假设原integral min V=1，也不把独立configuration当真实allocation。

ActualYES路由：若原普通disjoint allocation使每agent v_i(S_i)=1（即这里的normalized actual V=1 promise），为每S_i取一条达到1的原indexed clause。Floor后该同一S_i的tilde价值至少3/4。故存在同一disjoint actual allocation使tilde NSW≥3/4。这是存在性证明，不需要算法收到未知YES allocation；算法若使用原paper integral approximation，比较optimum即可。但它不是unit-FSLP route的替身，原unit-FSLP也不自动给actual V=1。

Internal valuations的positive singleton matching前件仍可由原lambda直接推出：每条原支持内有tilde positive坐标（总质量≥3/4），选一枚作lambda质量的edge，容量仍由原支持证书控制，整数性得full positive injection。因此E1所需positive matching不是额外未知allocation输入。

## 6. Safe rho与实际输出

对internal valuations在E1–E3成立、c2/d5/2且slack≤2时，A+B的fractional route给实际internal NSW至少

    (3/4)/2250000 = 1/3000000。

原v≥tilde v逐集合成立，故同一原items实际allocation在原菜单的NSW也至少这个值。因3000000<16777216=2^24，得到严格大于2^(−24)，statement放宽为rho=2^24的保证正确。这里rho固定且数值slack已明确量化，不再依赖“任意未知固定常数也小于某安全值”的推断。

对原actual S_i查原菜单的最大clause，得到原indexed state；floor只在内部算法用，未拿floor state值冒作原值。原utility仍全≤1，所以v1记录对(C1)的严格bad-agent计数与fixed eta结论逐字适用：每成功输出m_bad<n/K，不保证所有groups的minimum为常数。

## 7. 最终边界

上述statement中的B–C确为条件性质，未把Theorem 10原文声称为log-CONFIG gap，也未把XOS偷换成submodular。A的fractional residual前件比integral welfare界更强；source E1若要落地，必须保留对所有fractional残余families的界与poly-support rational实现。实际找Vi、residual support、iterated rounding全量bit控制和constant success probability均须由backend正式验证。

未读作者新Proof，未执行finite audit。未修改v1或将v2结论倒填到v1来源。后续任何更强v3/unconditional formal corollary仍需另行读其指定完整Exact与实际依赖，不能由本次条件检查自动认证。
