# 父方独立重构记录

2026-10-24。内部复核，无外审或全球新颖性认证。

逐边回撤：父方独立把每条atom贡献写为(b_a−y_a)t_a+y_ae_owner，对λ≥0盒上最小化得b_a min(λ_owner,λ·t_a)，紧凸像与cap分离给iff。未追踪余流f必须保留λ·f，不能只保总质量。independent盲审也指出此点，主文已明确。写Q_i−b_iλ_i=E_i−D_i，粗减细为E_i−(E_i−D_i)_+=min(E_i,D_i)。零行/零价格合法，常价格返还零。固定每节点原输出比例后逐atom缩放保mandatory/common及库存，密度只降不增；新初始d上限可能失效，必须使用明示扩展终局合同。

父方重跑audit_atom_retraction.py，另用Fraction反向核对利润和W=47、两套cost和OPT=52、IC项数1554及抽象差1/4，回放JSON完全一致。真实fixture只是旧完整SPE，严格分离仅为抽象流合同。

分数背景推论：父方阅读原pair_attack.md目录/策略及§6，核对逐real客户层总负载≤rk、dummy逐客户≤r均为逐主题线性限制，对全部分数凸包成立；固定合法查询p逐层Jensen后min_q max_T≥s。原完整SPE身份继承来源，不由本轮标量核验替代。另独写audit_fractional_background.py，不导入旧审计，用Fraction重算GPF/singleton与严格差，以加回u反算；全部通过。总槽嵌入及OPT≤2mf_m(0)方向正确，但任意背景保底已FALSE；根弱化与聚合未被否定。

这些复核没有证明真实SPE通过全部cuts，尤其未付常价格方向；m5仍无无条件half。
