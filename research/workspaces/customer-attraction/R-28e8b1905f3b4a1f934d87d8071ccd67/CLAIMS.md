# 本轮精确身份与状态

## Q-CAG-HALF

Exact Statement与Objects/Domain/Quantifiers/Assumptions/Definitions/Scope均沿共享model.md及目标文件，不改变。Conclusion：每个完整历史依赖纯SPE都有2W≥OPT_m。Status：OPEN；本轮没有主目标证明或反例。

## LOCAL-TAIL-CYCLE-7-WITNESS-v1

Objects：三个目录主题A,B,C、七个单位客户、m=3；客户兴趣类型A:1、AB:1、BC:3、ABC:2。完整策略：根C；第二位在首A/B/C后分别B/B/C；第三位除CC后A外一律B。每个有序历史都指定动作。令q^s为根强制s后同策略的两个真实后继主题，R(t;q)=Σ_(x∈t)1/(1+c_x(q))。
Conclusion：该策略为完整纯SPE，而R(B;q^B)+R(C;q^C)=25/6<26/6=R(B;q^C)+R(C;q^B)。实际CCA，W=OPT3=7。
Dependencies：原均分定义与逐历史比较，不导入外部定理。
Evidence：作者与blind_tail_cycle_audit.py独立精确重构；独审13节点39比较。
Counterevidence/Objections：现行continuation_security_barriers.md已有同类失败，故不是新接口否定；该小例仍有纯BB列cap2<13/6，不能反驳自由菜单。
Status：小型见证独立内审通过；外审、新颖性、最小性均未认证。Related Files：potential_induction/、independent_audit/blind_tail_cycle_review.md。

## EMPTY-DILUTION-ENDPOINT-HOMOGENEITY-v1

Objects：任一有限非空完整端点菜单Z，目录含空主题E；K(T,Z)=Σ_(x∈T)1/(1+c_x(Z))，F(p)=min_Z Σ_T p_T K(T,Z)。Quantifiers：任意q查询分布、任意ε∈[0,1]。Conclusion：F((1−ε)δE+εq)=εF(q)。
Evidence：K(E,Z)=0的线性代数，含最小值的精确齐次性。Status：解析恒等式，非动态支付定理。
Related Files：certificate/empty_dilution_and_free_endpoint_menu.md及独立单位客户audit。

## BACKGROUND-EXTRA-ONE-ES-v1（已有候选的本轮重构）

固定任意合法有序前缀h，其客户负载b，余r≥1人；对所有该子博弈完整纯SPE，首位最终收益u是否至少max_p min_(q∈S^r)Σ_T p_TΣ_(x∈T)1/(1+b_x+c_x(q))？对手不能观察查询实现，q保留r个目录槽。Status：OPEN充分桥，不是Q-CAG-HALF的等价命题；此前已有其他团队立项，本文不认领新候选。
