# 跨源共享侧资源平方根预算：独立重构与真实资源攻击

审查对象：原较弱冻结稿 `cross_source_shared_side_candidate.md`，SHA256 `f69fba0b27e07068b44f9d8090f69078ac78e825ace8ade7b91ed420a840c336`；平方根加强冻结稿 `cross_source_shared_side_sqrt_candidate.md`，SHA256 `3f5c2025275b0f4dc186425427840c6100816307de58deba4bb530fb0a9f6711`。本审查已逐式检查两稿；第二稿只需 `alpha >= 1 + sqrt(d)`，保留第一稿第1节全部模型和UFmulti假设。最终canonical正文 `research/current/weighted_congestion/shared_side_truncated_potential.md` 的整稿SHA256为 `4701e82866195aa6e5b90aa22eb1a88d1d857f022369b6dd0e05537db4cc1b1b`。其第八节首登ID为 `WC-MULTISOURCE-SHARED-SIDE-ROSENTHAL-v1`：临时v1/v2未曾进入共同账本，故这里为新身份首登，不是静默改写旧Claim。已核查接入diff：8.1—8.6数学正文与平方根冻结稿1—6节在标题级别和“本候选/本Claim”规范替换后逐字一致；新增身份/状态/审计合同没有改变对象、量词、假设或结论。

## 1 独立重构先识别的瓶颈

未读候选推导前，从策略集合重构得到：全anti状态中，side副本b的真实负载是同位hub数量乘u，加上该side中source位为b的所有light权重。hub单独偏离保持所有light不动；重新anti化则移动该source的全部light，可能扰动该hub不使用的其他side。因此必须把真实hub偏离与source reset区分，并按每个light全部side之和收费，否则跨source或多side会重复领取UF预算。含外source light但自身没有light的hub也不能直接靠自己的UF支付它所见的所有背景成本。

## 2 已逐式重构的解决链

固定light时，各side两副本具有共同等权hub增量u，有限Rosenthal求和的边际恰为hub真实普通side成本差。定义anti点势E后，先做真实hub偏离，再只重置其source的light；移出副本降低势，移入副本的增加可逐light支付。

逐light重置上界中的kappa(t)=min(dt,t+1)有两个独立来源：单项式导数上界给dt；间距u的积分区间覆盖次数给t+1。`n=0`或`m=0`、常数或零多项式均被原不等式直接覆盖。每条side全部中间负载仍不超过T_j+m_j u，不要求source在H_j中。

UFmulti对每名light只使用一次，且包含其全部side之和，给出(B0)。此时跨source、多light/source和light多side均不产生重复预算。

## 3 加强版源预算的独立证明

将u缩放入单项式系数，写t_l=w_l/u，T=sum t_l，kappa(t)=min(dt,t+1)，F非负系数次数不超过d。需要证明

    S=sum_l kappa(t_l)[F(u(1+t_l))-alpha F(uT)]
      <=(alpha-1)[alpha F(u(1+T))-F(u)].

若T<=1，kappa(t)<=dt且F单调，丢负项得S<=dT F(u(1+T))<=dF(u(1+T))。

若T>=1，逐单项式次数k处理。kappa凹、kappa(0)=0，故sum kappa(t_l)>=kappa(T)。函数f_k(t)=kappa(t)[(1+t)^k-1]满足f_k(t)/t不减：小t段为d[(1+t)^k-1]；大t段为sum_{r=1}^k binom(k,r)(t^r+t^(r-1))；接点连续。故sum f_k(t_l)<=f_k(T)。由于1-alpha T^k<=0，得到

    S_k <= kappa(T)[(1+T)^k-alpha T^k] = kappa(T) Q.

Q<=0时S_k<=0。Q>0时，使用alpha>=1和kappa(T)<=T+1，

    S_k <=(T+1)[(1+T)^k-T^k]
         <=k(1+T)^k <=d(1+T)^k.

k=0时Q=1-alpha<=0，无需导数式。逐非负系数组合得所有T均有S<=dF(u(1+T))。另一方面M=alpha F(u(1+T))-F(u)>=(alpha-1)F(u(1+T))。因此(alpha-1)^2>=d即足够，无需A_d或alpha>=3。

势local minimum存在于有限hub状态空间。其真实hub alpha成本差由负主预算-M加上不超过R_v的reset误差控制；R_v<=S/(alpha-1)<=M。light当前主负载W_v、偏离后u+w_l；side当前<=T_j+m_j u、偏离后>=w_l；UF给更强的alpha C_current<=C_deviation。因此所有玩家满足目标alpha-PNE不等式，无0/0。

## 4 真实资源Fraction攻击

本审查没有调用作者核心或仓库验证器。独立源 `tests/audits/weighted_congestion/independent_multisource_shared_side.py`（当前scratch同名稿），SHA256 `a1f218f9ecd38462ad84076002eb91ae4a5367adb00ef3dd94d7a6f3f927e745`，从资源集合和两合法策略直接计算全部负载与成本，核验UF、固定light Rosenthal恒等式、真实source reset界、源预算，以及每个anti势local minimum处每个玩家真实偏离。命令为 `python3 tests/audits/weighted_congestion/independent_multisource_shared_side.py`，输出stdout JSON。同名JSON明列每个游戏全部输入、命令、Python版本、源码hash、两份审查冻结稿hash和参数生成规则；seed=706241，无外部依赖或本会话绝对路径。

有理(d,alpha)为(2,121/50),(3,41/15),(4,3),(6,69/20),(9,4),(10,833/200),(16,5)，精确检查(alpha-1)^2>=d。87个游戏、600个anti状态、428个local minima、2696项玩家偏离、1920项reset检查通过，其中三个平方数为阈值端点。覆盖空H/L/side、无source light、source属于H、多side、跨source、零/常数/混合多项式；额外手工零费用案例有权100的light，不依赖随机生成器的小light范围。

这些有限结果仅检查实现和边界，不替代上述一般证明。

## 5 范围攻击与结论

现有增长奇环下界无scope冲突：`odd_ring/cohort_lower_bound_and_envelope.md`第2节允许且第5节实际使用不等hub权u_0=R^ell、u_i=R^(2i-1)，R>1。新定理严格依赖共同hub权u建立Rosenthal边际；不可外推异权hub。UF本身也强限制实例。二元对称副本、唯一主source、相同hub权全部承重。

未发现本次精确范围内仍成立的fatal objection。可将平方根阈值作为内部独立审查支持的一般子类结论；没有全类判定、算法复杂度、全局新颖性或外部同行评审结论。

## 主研究者最终规范核对

接入旧两Claim边界的读取提示后，最终正文整稿SHA256为`9660ed3b13aa178a49d402bcf457f93d5019539c452afeb0a2ae4844961542fc`。这次仅将旧§6的“跨source开放”改为“旧两Claim未覆盖，第八节仅UFmulti下闭合”；第八节数学未变，原独立审查范围保持。独立审计代码按原字节复制后以规范路径重跑，最终run的源码hash须与本审查所列相同。
