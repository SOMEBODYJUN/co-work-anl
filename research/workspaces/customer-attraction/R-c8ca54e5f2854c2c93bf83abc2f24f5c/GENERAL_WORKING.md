# 一般证明工作稿

2026-10-24。Q-CAG-HALF仍OPEN；原单位客户、共同目录、任意人数和全部有序历史纯SPE量词不变。固定实际并集C、比较并集O，L=|O\C|、E=|C\O|，准确需求是L−E≤W。L≤W已有71客户完整SPE反例；本轮一项重复探索及时撤回。

## 父方直接推导及停点

父方复核既有 [共享前缀cap回收](../../R-d3981c0168644971803a9c3380ed687c/round4_general/menu/shared_prefix_cap_salvage.md)。在全部SPE中先最小化W，再于同W最大化u1，实际前缀强制一行动后的完整尾SPE端点y若W(y)≤W，就可回收到cap合法端点并集。否则全部前缀玩家严格改善，可向上拼成根SPE，与极值矛盾。

但是静态高插入替换可能增加W、破坏尾SPE；尚未构造同时保尾理性、控制前缀总利润且不增覆盖的交换。端点极值本身不是新的矛盾或定理。竞争的根个体路线2m u_i≥OPT_m仍未证；其合法前缀版本必须保留原总m和OPT_m，不得换成任意背景剩余r的门槛。

## 逐初始客户边回撤：内部已核对的条件工具

见 [正文](common_capacity/atom_retraction_and_dispersion_rebate.md)。同一真实固定flow按初始客户边a全额分裂后代，质量b_a、owner i(a)、终端K_al满足Σ_lK_al=b_a；A固定，F_l=A_l+Σ_aK_al。取0≤y_a≤b_a，缩放全部后代并把撤回量留给owner，得到

    F'_l=F_l+Σ_{owner(a)=l}y_a−Σ_a(K_al/b_a)y_a。

这保留库存、mandatory/common及密度；新初始d可能超过旧u，所以输出明确使用扩展终局合同，只检查同一F'_l≤2u_l。置q_a(λ)=Σ_lλ_lK_al/b_a，成功iff对全部λ≥0有

    Σ_a b_a min(λ_owner(a),q_a(λ))≤Σ_lλ_l(2u_l−A_l)。

按owner合并的旧需求减该细需求恰为Σ_i min(D_i,E_i)，定义见正文。它回收来源价格分散的粗化损失，不增加资金；λ恒1时返还全零，仍需|O|≤2W。m=5同样没有无条件half。

independent未读稿重构盒分离，指出转述若只保总质量会漏固定余流；正文明确逐角色全追踪及含余流修正式。父方另独立推导并回放真实流/抽象严格包含审计。没有外审或新颖性认证。

## 连续分数背景没有绕开旧可信威胁

任意合法背景个体候选u≥f_r(b)，f_r用r个分数竞争槽定义，已由 [旧PB-extra的直接推论](potential_dual/fractional_background_floor_corollary.md)否定。每real客户层总负载≤rk、每dummy负载≤r均是逐主题线性界，对分数凸包仍成立；固定查询的Jensen给f_r(b)≥s>u。原完整SPE证明继承来源，本轮不是新反例族。

正确条件用途仍是：合法总槽嵌入给f_r(b_i)≥f_m(0)，静态同目录给OPT≤2m f_m(0)。但任意背景保底已FALSE。仅在根实际路径成立的u_i≥f_m(0)、根聚合W≥m f_m(0)、2m u_i≥OPT_m都未被该例否定。父方独立Fraction核对严格差并加回u反算，不将标量核验称为重做全树证明。

## 继续义务

没有新无条件福利界、一般证明或目标反例。继续攻击真实return-IC、适当查询、根覆盖地板及低成本可信构造；不以细化cut、审查通过或有限阴性冒充一般闭合。
