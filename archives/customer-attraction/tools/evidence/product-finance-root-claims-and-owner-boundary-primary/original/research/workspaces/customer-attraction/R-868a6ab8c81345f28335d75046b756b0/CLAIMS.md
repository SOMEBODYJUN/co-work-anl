# 本轮精确命题与真实状态

## Q-CAG-HALF（身份不变）
Objects/domain/quantifiers：CAG-MODEL全部有限单位客户、有限非空共同目录、任意m>=1、每个全部有序历史纯SPE。结论2W>=OPT_m。状态OPEN，本轮无一般证明或完整目标反例。所有下项均不是其替代版本。

## PRODUCT-TRANSFER-CLOSURE-v1
任意有限个两两不交客户组件、同一人数m、完整Cartesian共同目录、任意同长度有序产品前缀h。记组件L_k(h^k,A)=强制A后全部子SPE中的当前收益最小值，Theta_k=max_A L_k。对任意向量A以及每个组件强制A后的可实现子SPE终局z_k，若当前收益总和至少sum Theta_k，则这些终局可以由一份产品完整历史纯SPE在h实现。
结论是充分闭包，未声称一般产品SPE全部分解。全m严格推导、独立内审通过；源机制已见旧cartesian_efficiency_failure.md，不能认领首次跨组件补偿。正文dynamic_matching/product_transfer_lemma.md §1-2。

## PRODUCT-L-CONVEXIFICATION-v1
对任意上述组件、任意当前位置i<m、前缀g及强制A，将其后下一玩家行动B与B后的子SPE终局z映射成(d,v)=(u_i(z),u_{i+1}(z))。以平均v>=Theta(g,A)为约束所得有限有理LP最小平均d记barL_i(A)。任意可清分母的混合均可由有限相同组件产品的真实子SPE实现，因此L_product<=副本数乘barL。此处barL<=L，不声称相等。适用于任意总人数、任意合法背景；独立内审通过，外审/新颖性未认证。
严格单位客户见证：L_component(B)=3/2而L_product(BB)=5/2<3，完整产品SPE的全部有序历史已独立核验；实际W=OPT，非目标反例。正文同上§3-4，证据和三份独立审查见README。

## PRODUCT-SM-AMPLIFICATION-v1
固定任意组件实例和完整SPE，D=OPT-W。若M=max_{全部最优有序元组T}sum_i barL_i(T_i)<D，则足够多相同组件的Cartesian产品具有完整SPE且对每个产品最优有序元组都满足sum_i L_i(T_i)<OPT_product-W_product。结论是否定最弱SM-opt-exists，而非自动否定half。有限舍入误差C与所有OPT投影量词已独立核验。
当前没有满足M<D的真实组件，故这只是已证的条件归约，不是已得到SM反例。正文同上§5。

## SCALAR-COORD-SEPARATION-v1
旧generalized_child_routing.md称w=A_absorb/D的scalar flow等价于coordinate query-cover LP，此自动映射不成立。对任意整数t>=0，A=C_t并{a1,a2}、B=C_t并{x}，两人共同目录{A,B}，根A、末位恒A是完整SPE。遗漏一个客户；scalar最低费用1，coordinate-cover最低费用(t+2)/2。因此两接口有无界分离。独立Fraction核验和全参数解析通过；不反驳coordinate LP独立充分性，也不反驳half。正文source_reset/scalar_financial_law.md。

## THRESHOLD-ONLY-EXTENSION（FALSE，范围严格）
对全部根分支仅要求每个尾收益>=t且t<=v_{r+1}(b)，不能推出存在根收益>=t。旧环非SPE菜单机制在任意n>=13,t=3/2给反例；缺失的是末位真实IC。此项仅否定该组合加强，EO及原Q保持OPEN，不认领新的环机制。正文direct_proof/threshold_extension_boundary.md；独审path_menu/cycle_threshold_independent_review.md。

## 未闭合对象
H4存在最优排列、SM-opt-exists、Mpath<=W/m、arbitrary-child总金融预算均未证或反驳。本轮代数重写和有限阴性诊断不改变它们的真值状态。
