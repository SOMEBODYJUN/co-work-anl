# 六人独立攻击共同材料

状态 OPEN。唯一成功：证明任意六人原模型每份完整历史纯 SPE 有 2W≥OPT6；或给出完整反例，全部有序历史策略及独立精确核验。这里 n=6 指六名提供者，不是六客户/六主题。一般人数证明当然也算成功。

模型：有限单位客户 N，共同有限非空目录 S⊆2^N。玩家顺序 1..6，看到全部有序历史，选主题，可空可重复。终局客户负载 c_x，玩家收益 Σ_(x∈S_i)1/c_x，W=Σu_i=覆盖数。OPT6 是六个目录主题最大并集。纯 SPE 在每个有序历史 h 的当前原收益 ≥ 强制任意合法主题后沿同一原策略继续的当前收益。被强制者不在强制枝要求最优，真实后继均须最优。同计数历史可不同平局。计数缓存可存全体可实现续局集合，不能固定匿名选择。

每个研究员收到同一目标，无路线分工，方法不限。先自己重构瓶颈，再按需读取材料。只写自己的 agent 子目录；不运行 git/checkpoint/sync，不动共享文件。每次回复必须给 exact claim/status、可核验证据、致命缺口、下一条具体可验证问题。发现重要结果及时通知父方，继续研究。不能以第一批结束、有限无反例或辅助桥失败停工。不要再派子代理（槽位已满）。

## 当前可靠地基

- 根 AGENTS.md；精确模型 research/current/customer_attraction/model.md；当前前沿 research/customer_attraction/RESEARCH_STATE.md；失败表 research/customer_attraction/FAILED_ROUTES.md。
- 恰五人已证明，任意客户与目录且全部历史。research/current/customer_attraction/five_player_half.md；完整包 customer_attraction/proofs/half5_exact_v1/。从五人工具取启发，不机械用五人乘子打六人。
- 任意六个不同极大覆盖以内已有一般人数 half。因此潜在目标反例至少七极大主题，不要大规模重复小目录无反例扫描。
- 实际前缀安全行：r=7−i，p_i为原实际前缀负载，任意T有 u_i≥Σ_T1/(p_i+r)。有限比较不能替代真实后继。
- 实际末位给每个目录主题同一价格 P_l(T)=Σ_T1/(l+1)≤u6；共同 K=max|T|。K必须共同付款，不能每枝独立重置。
- 真末两人：背景b，原C,D，f(T)=Σ_T1/(b+1)，g(T,Q)=Σ_(T∩Q)1/((b+1)(b+2))，H=u_C+u_D+g(C,C)。对任意T,Q有 H≥f(T)+f(Q)−g(T,Q)。这是三条真IC和非负余项的强PAIR，不是普通两利润比较。
- 任意余k≥2真源，原收益r，背景b，有 r+K≥Σ_x[t/(b+k−1)+q/(b+k−1+t)]。可用一般投影保留实际末价、K、末位查询及隐藏位；research/current/customer_attraction/priced_hidden_reply_projection.md。
- 同源回复再查询七行与计数消元：research/current/customer_attraction/same_source_reply_requery.md。源强制T产末C，回同一源强制C，保留两个末主题共享身份；不是已闭合付款。
- 真正静态安全值 v_m=max_p min_(m−1主题元组B) E_(T∼p)Σ_T1/(1+c_B)，对手B不观察抽样。OPT_m≤(2m−1)v_m 已证；动态总付款 W≥(m−1/2)v_m 仍OPEN，逐人版本和强弱iid桥均FALSE。

## 已失败的具体机制

逐人安全值、末位收益倍差、SPE=静态NE/最差PNE/最差CCE福利比较、仅终局负载f(c)且f(1)=1付款、冻结实际前缀 P+λ新增覆盖≥freshOPT、每步机会亏损≤当步收益、实际均匀缩放背景精确税、免费promotion、源regret支付势reset 等均已有完整反例。不要原样复活。净差 OPT−W=L−E，L遗漏、E实际覆盖在最优外，不能丢E。

最新势候选 P6≤W+C(A) 仍OPEN，C=Σ_iΣ_(x∈Ai)[1/(p_i+1)−1/(p_i+7−i)]。即使它成立，C≤W已FALSE，不能自动收尾。局部ESM已FALSE、BRANCH-MONO已FALSE，last-promotion源regret付款已被7客户3人完整SPE反驳（Gamma=0，势9→8）；对应研究员 R-23ab27f8efb44f1faca2699d45886250/general_n/zero_regret_promotion_reset.md。势候选可自由攻击，但不是给你指定路线。

## 最新必要行边界（非SPE）

research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/parent/FRONTIER.md 与 six_astra/README.md：第四位强制Ti产Bi,Ci，新末Rij=σ6(h,Ti,Bj)、Sij=σ6(h,Ti,Cj)；全部同层互查，回实际倒二选R再产Z，跨R共同阈值等3889行仍有精确O=1、W<1/2点。最新同行 R-c37d9a1010c64b649a1f8a0368eaf54d/README.md 及 six_query/README：改变Z后，连全部60类Z→Z也可完成为42个确定(R,Z)原子，满足3949行；经字面独审，不是完整SPE。继续只调该图乘子不能成功，必须增加本质信息或换表示。

## 保存与成功审查

只在本轮工作区自己目录写有研究价值的资产；代码须保存seed、输入、版本及精确核验。不给没有新数学信息的阴性扫描写长报告。普遍证明可为全类型系数域精确有理证书，但需语义合法、全域不漏、所有预算列非负且独立重构。反例必须实际单位客户可实现，目录全部合法，完整有序历史表/自动机与所有IC精确核验，且2W<OPT6。

Repo: /workspace/scratch/a4dce90970e8/co-work-anl
Parent workspace: research/workspaces/customer-attraction/R-70d2119f50a642dc94b386eb142f1f2d/
