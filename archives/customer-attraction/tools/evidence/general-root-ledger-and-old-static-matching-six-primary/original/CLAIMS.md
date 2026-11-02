# 本轮精确身份与真实状态

## LOCAL-ADM-CREDIBLE-UNION-v1

- **Domain/quantifiers：** 每个原CAG-MODEL实例、任意m≥1、每份完整有序历史纯SPE的实际有序经济路径z；全部空/零/重复/任意平局保留。
- **Definitions：** h_i=z_<i，D_iA为R(h_i,A)中使强制当前收益≤原u_i的全部经济终局，经济A=S_i同样放开。M_adm是在全部D端点联合菜单上的独立额外查询minmax值。
- **Conclusion：** 有足够多个有限经济别名的完整SPE同时实现整张D菜单且保留z；反向每个这种信号完成的端点属于D，故M_adm等于这些有利可信完成的最小Mpath。m≥2时由已有末两人去相关得M_adm≤min最后两人收益。
- **Dependencies：** 原完整SPE子博弈拼合、已有经济重复标签商定理、有限minimax、既有末两人去相关。没有新福利付款。
- **Evidence/status：** root提出精确候选并重构可行性，normal_form逐历史证明和量词检查，tree_dual另逐量词独立内部重构通过；个人区表示引理，无外审或新颖性认证。待证M_adm≤W/m与原half均OPEN；旧MAX包络不等于这里MIN完成。审查见tree_dual/review_admissible_union_menu.md。
- **Files：** normal_form/{reset_normal_form,admissible_union_menu}.md，MAIN_PROOF_WORKING.md。

## LOCAL-I-COMPLEMENT-COORD-v1

- **Domain/quantifiers：** 原模型任意人数、任意完整SPE、任意比较主题元组T及同一次合法坐标初始化；令I=O∩C。
- **Conclusion：** 保留原current d和固定父叶券H不动，全部I-future库存可显式由同一第二份actual I客户券的未用部分支付。逐客户J_lx=A_x(w_lx−H_lx)/(1−H_x)，零分母取0；Σ_lJ_lx=A_x且H_lx+J_lx≤w_lx。
- **Interface limitation：** 可向源owner以前的actual角色支付而不调用其IC；这是直接实际券出口，不证明原限定full-SAFE路由版本RESIDUAL-CAP。只R入口从头接已有ν=fresh利润分母核是合法的，新的非负净券K仍未获共同cap。
- **Evidence/status：** global_credit给出一般解析构造，root逐客户重构，credible先按陈述独立重构再对旧ν正文核域/资金，通过内部检查。无外审或新颖性认证；不登记为新的全输入福利下界。
- **Remaining：** 存在同一次最优T/剪枝/直接付款/fresh路由使K_l≤2u_l−d_l−H_l−J_l，仍OPEN。R-only极大current另可由旧source scalarCLIP得到，不认领新机制、不声称对全部路由支配。
- **Files：** global_credit/coordinate_residual_attack.md、credible/coordinate_support_attack.md§0；原坐标与ν核按正文链接归原作者。

## LOCAL-SWAP-ASCENT-CAP-NO-v1

- **Refuted statement：** 任意合法背景与完整SPE实际首对AB，α<β时，无祖先承诺最小首利μ_(b+B,r−1)≤β；以及用任意固定倍β−α支付δ=(μ_B−α)_+。
- **Objects/domain：** 四不交单位客户块X,Y,Z,E，大小2k,k,k,e，整数k>2e>0；共同四主题A=X、B=YZE、C=XY、D=XZ，m=2。
- **Complete strategy：** 根A，末位依A/B/C/D分别选B/C/D/C。全部历史与偏离均由参数IC表证明。
- **Conclusion：** α=2k、β=2k+e、μ_B=5k/2；δ/(β−α)=k/(2e)无界。原actual及固定B后的全部子SPE福利均4k+e=OPT2。另有10客户严格见证。
- **Evidence/status：** normal_form一般解析证明；price未读稿先独立核全部参数IC；root展开客户运行Fraction审计并核定义。内部检查通过；无外审或全球新颖性认证。这是辅助交换付款反例，不是Q-CAG-HALF反例。
- **Files：** normal_form/swap_ascent_payment_counterexample.md、audit_swap_ascent_counterexample.py、冻结JSON；direct原尝试应按此改FALSE。

## LOCAL-PAIR-ONE-SECURITY-v1

- **Exact candidate：** 对每个原模型合法前缀背景b、每个余r≥2、每份完整历史纯SPE，首两名实际终局利润和≥v_r(b)。静态对手有r−1主题槽且不观察所抽查询。
- **Status：** OPEN候选，未证明、未被本轮反驳；没有有限阴性升级。不同于已FALSE的2v_(r+1)任意背景候选。
- **Conditional use：** 若对全部背景成立，则根W≥ceil(m/2)v_m(0)，从已知OPT_m≤(2m−1)v_m(0)得全人数比率小于4；仍非half。具体定义与条件推导见MAIN_PROOF_WORKING.md§3。

## 同行第七轮更新的去重，不是新反例

FOMA-EXISTS（存在最优主题组合及静态冻结匹配，查询收益和≤W）已由旧 `B10-STATIC-OPTIMAL-ASSIGNMENT-NO-v1` 否定，不能沿同行round7的OPEN标签继续正面使用。原资产在 `R-a0bb57fa24044a8794bc7991918a19c6/static_matching/optimal_static_matching_counterexample.md`。root重跑原独立实现确认W=47、OPT=52、唯一最优支持0145、全部匹配minK=48；这不是新独立实现或新数学发现。详细出处及准确剩余候选见 [更新校对](peer_update_reconciliation.md)。这不否定RESIDUAL-CAP、ADM?或Q-CAG-HALF。
