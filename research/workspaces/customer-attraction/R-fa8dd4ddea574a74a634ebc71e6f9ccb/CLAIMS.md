# 本轮精确身份：探索资产，不自动进入共享canonical状态

共同模型为仓库 CAG-MODEL；本轮一般目标 Q-CAG-HALF 仍 OPEN。
本文不改变共享现行命题账本，外审及新颖性均未认证。

## B9-JOINT-HIGH-BACKGROUND-v1

**Exact statement / quantifiers.** 任意有限单位客户、有限非空共同目录、任意合法有序历史产生的整数背景b，若恰剩k≥12人，且每个可被目录覆盖的客户满足b_x≥k−5，则任意完整有序历史纯SPE的剩余利润P满足2P≥F_k(b)。允许空主题、重复选择、零客户、任意历史平局。

**Objects / definitions.** 比较元组T∈S^k的客户计数为d_x，F_k(b)=max_TΣ_(d_x>0)d_x/(b_x+d_x)；P为实际剩余k人的收益和。非零背景下这两个对象均不是全部玩家的覆盖福利。

**Dependencies / mechanism.** 每个实际玩家的K=max_TΣ_T1/(b+k)保证，真实末两人各有theta=min_(H∈S^(k−1))max_TΣ_T1/(b+1+h_H)保证；新的联合逐客户有理证书给F≤2(k−2)K+4theta≤2P。

**Evidence / status.** 自足解析证明、发现者Fraction实现审计、另一分支独立整系数多项式重构和续局量词攻击均完成；未发现未解决致命异议。身份为个人内部已独立检查的条件定理。

**Counterevidence / scope boundary.** 根b=0、k≥12不满足假设。对每个k≥6，k个不交等大q客户主题、每主题预选k−6次的合法背景满足F−2(k−2)K−4theta=2q/((k−5)(k−3))>0；它只反驳再降一背景的同预算桥，不反驳半利润。

**Related files.** [正文](background_induction/joint_baseline_half_profit.md)、[发现者审计](background_induction/audit_joint_baseline.py)、[独审](credible_counterexample/background_independent_review.md)、[独审符号代码](credible_counterexample/independent_background_review.py)。正文异质背景有符号误差扩展另按其精确加性结论使用，不将它当作无条件半利润。

## B9-COMMON-SUPPORT-CONSERVATION-NO-v1

**Exact statement / objects.** 对[正文](tree_coupling/support_conservation_obstruction.md)固定的三人六主题完整形式策略σ，存在126维非负有理抽象收益向量y，满足全部258有序历史图比较、2520锋利同主题稀释及全部同支持总支付守恒，但根034总支付为1，比较124总支付为9/4>2。

**Assumptions / definitions.** y_(q,a)是独立抽象顶点值；同支持C_A=Σ_a q_a y_(q,a)。本命题没有假设y来自共同客户重数。

**Conclusion / scope.** 上述必要条件模板不能普证half。该y违反共同有符号客户的二支持分配身份，故不是合法游戏、更不是SPE反例。

**Dependencies / evidence / status.** 精确有理文件、发现者定义级核验及另一研究员独立重建全部约束均通过；个人内部已独立检查的模板反例。没有对放松的最优值作声明。

**Objections / related files.** 不能据此否定原Q-CAG-HALF；缺少跨主题共同分配耦合。[证书](tree_coupling/support_conservation_obstruction.json)、[独审](global_proof/potential_probe/support_conservation_independent_review.md)。

## B9-TWO-SUPPORT-CIRCUIT-v1 与 B9-SPECIFIED-GRAPH-REPAIR-v1

**Exact identity / quantifiers.** 对任意两个不同目录主题a,b、任意整数r≥s≥1、m=r+s及任意有限客户资料（身份允许有符号质量），有

rs U_a(ra+sb)+r(r−s)U_b(sa+rb)=s² U_a(sa+rb)+(r−s)|b|。

这里U_a(q)是终局q中一名选择a提供者的收益，|b|是主题b的客户质量；同一字母b此处是主题标签，不是背景。

**Specified repair.** 对上一命题的固定σ和比较124，加入r=2,s=1的两条回路（a,b）=(2,4),(3,4)，可由三条真实末层激励和五条普遍稀释，以非负不等式乘子严格推出C124≤2C034。

**Dependencies / assumptions.** 身份由客户在a,b的四种会员模式逐项证明；稀释不等式依赖客户质量非负。两个身份可带任意符号乘子；不将线性span冒充非负激励锥。

**Evidence / status.** 发现者126坐标精确行证书和根代理独立稀疏重构均通过；身份是普遍代数引理，支付只对指定图及比较组合。未见致命异议，未认证新颖性。

**Scope / objections / related files.** 没有证明全部双支持回路能支付任意σ；没有重新改善已知三人常数。[正文](tree_coupling/pair_circuit_repair.md)、[根代理独审](audits/pair_circuit_review.md)、[独立审计](audits/pair_circuit_review.py)。

## B9-CROSS-FAMILY-1284-RELAXATION-NO-v1

**Exact statement / objects.** 对[生成器](credible_counterexample/cross_family_closure.py)定义的五人旧64原子支持、1284条线性必要行，存在[冻结证书](credible_counterexample/cross_family_closure.json)所给非负有理质量，W=1且O>2；全部行的Fraction slack非负。

**Domain / assumptions / dependencies.** 原447行加跨族菜单、末两人界及共享最优索引条件对齐行；所有新增行的具体对象与量词在[自足README](credible_counterexample/README.md)定义。O是辅助比较覆盖，不是真实OPT证书。

**Evidence / status.** 显式逐索引重建、有限条件对齐穷举及全部1284行精确核验完成；这是指定必要条件模板的新可行障碍，不是完整SPE。

**Objections / scope / next step.** 没有全部主题的共同标签对齐和完整可信续局，不能用其O/W反驳Q-CAG-HALF。继续寻找真实全树补全或改表示；不无限追加同类平均行。
