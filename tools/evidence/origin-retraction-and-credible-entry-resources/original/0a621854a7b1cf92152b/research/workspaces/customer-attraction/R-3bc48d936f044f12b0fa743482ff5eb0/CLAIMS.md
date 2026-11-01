# 精确辅助命题账本

Q-CAG-HALF原身份不变，仍OPEN，无一般证明或真正反例。本账本是个人资产，不是共享canonical升级。

## CA-HETEROGENEOUS-CREDIBLE-REPAIR-v1

- **Exact statement:** 任意原CAG实例、m≥2、1≤j<m，路径z及长度j前缀后的完整纯SPE π实现其尾部。以真正完整后继SPE定义ℓ_i(A)，δ_i=(max_Aℓ_i(A)−u_i(z))_+，D=maxδ，R=Σδ。D>0时存在同人数单位提供者、单位客户、有限共同Cartesian目录的完整纯SPE，旧路径为z，Wnew=W+mD+R，OPTnew=OPT+(2m−1)D，gapnew=gapold−(2R+D)。有理块共同整数缩放后所有式同倍数成立。
- **Objects/domain/quantifiers:** 任意有限单位客户、有限非空共同目录、合法m,j,z,π；全部有序历史，任意平局，重复/空主题保留。前j位不要求可信，尾部π必须完整SPE。
- **D=0:** 原路径可用真正最低偏离孩子和π拼为完整SPE，不引入零保险。
- **Dependencies:** 可信续局全集/极值取得；旧同质银行clean/永久BI机制；Cartesian完整IC及OPT可加；共同清分母。
- **New construction:** 银行位置任意交错，非标记选Y且末位Y；逐缺陷高度叠加固定组件，不是随历史改权。
- **Evidence:** 作者完整解析稿；父方先独立重构后读稿；potential先盲重构再逐式对稿的独立解析检查完成，无fatal objection；作者有限银行核验及父方另实现联合产品回归通过。
- **Counterevidence/scope:** 暂无fatal objection。修复不证明O≤2W+2R+D；真SPE上该式就是half。没有超过成本的路径，未外审或认证新颖性。
- **Status:** 完整解析辅助构造，独立内审通过；不是新half范围，外审/新颖性未认证。
- **Related files:** credible/heterogeneous_prefix_repair.md；credible/audit_marked_bank.py/json；potential/blind_repair_reconstruction.md；parent/audit_heterogeneous_product.py/json；GENERAL_WORKING.md。

## 未证保持未证

全部ξ/η跨孩子付款、Mpath、额外槽θ逐人floor、共享角色current容量均未因讨论而升级。

## CA-FIXED-ORIGIN-RETRACTION-v1

- **Statement/objects:** 固定任意合法来源标记R-flow，不要求最终ROLE成功。来源量b_i≥0，终端角色矩阵K_il≥0只在l>i有值，Σ_lK_il=b_i。保留y_i∈[0,b_i]于来源角色，同时按来源比例缩小全部后代，则F'_l=F_l+y_l−Σ_i<l(K_il/b_i)y_i，零b行按零。
- **Conclusion:** 固定路由的F'_l≤2u_l可行，当且仅当正向最大保留贪心成功。首次失败j产生显式λ≥0，CUT=Σλ(2u−F)+Σb(q−λ)_+=z_j<0。这是该固定比例回撤族的精确可行判据，不是所有路由的判据。
- **Assumptions/dependencies:** 原来源库存与homogeneous流方程、严格递增角色；H/J固定，放松原INIT的d_i≤u_i，保留最终单一2u_i cap。来源密度受原流支配，不把每个context各付u。
- **Evidence/status:** 解析证明，optimal_gap先盲重构再应用审查及父方检查通过；真实完整SPE/零/空/全主题/有序历史平局的精确回归通过。未证明通用成功，未认证外审/新颖性。
- **Target gap:** 常数价格λ=1仍给原目标O≤2W；没有新增全输入IC付款来保证cut非负。
- **Files:** flow/origin_retraction_shared_capacity.md；flow/audit_origin_retraction.py、flow/origin_retraction_exact_audit.json；optimal_gap/triangular_retraction_blind_audit.md、origin_retraction_application_audit.md。

## CA-TRUE-BRANCH-EXTENT-v1

- **Exact statement:** 任意CAG实例、m及完整纯SPE，K=max_T|T|，实际角色i收益u_i>0。强制任意非空主题A，k=|A|，真实完整偏离枝z_i(A)当前利润d_A≤u_i。则W(z_i(A))≤2k+(m−1)K−k²/d_A≤2k+(m−1)K−k²/u_i。
- **Definitions/domain:** 过去实际主题固定，未来沿原完整σ，全部历史/平局保留。k=0另用Wbranch≤(m−1)K；u_i=0时根/真实偏离raw界迫使全部主题为空，直接零界。
- **Proof/evidence:** 其他m−1主题总incidence≤(m−1)K；其中A内incidence为Σ_A(c_x−1)；Cauchy给Σ_A c_x≥k²/d_A；SPE给d_A≤u_i。作者推导、父方独立代数检查通过，未认证新颖性/外审。
- **Scope:** 偏离枝福利的上界，不是实际福利下界；未接通OPT付款，不新增half范围。
- **Files:** direct/extra_slot_saturation_and_branch_extent.md。
