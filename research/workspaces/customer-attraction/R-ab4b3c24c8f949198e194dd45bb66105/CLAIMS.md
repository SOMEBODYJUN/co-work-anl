# 本轮精确命题与证据等级

## Q-CAG-HALF：不变，OPEN

有限单位客户、任意有限非空共同目录、任意人数、每份完整有序历史纯SPE，结论2W>=OPT_m。空主题、重复选择、零客户及任意历史平局均保留。本轮没有完整一般证明、目标反例或新增无条件half范围。

## CA-UNIFORM-CREDIBLE-DEFECT-PRICES-v1：精确表示

- **Exact statement / quantifiers：** 对每个固定m>=2，原人数m上全实例全SPE的half成立，当且仅当存在只依赖m的实向量lambda>=0，使每个原模型实例的每条末位为BR的任意有序目标路径z都满足 `2W(z)-OPT_m+sum_(i<m)lambda_i(M_i-u_i(z))>=0`。每个M_i在真实目标前缀上取当前行动max、真实完整子SPE最低当前利润min；不冻结后继。统一价格可限制在 `sum_i(lambda_i-2)_+<=1`。
- **Objects / domain：** 原模型全部有限共同目录、单位客户、任意目标路径，前m-1位不必可信；全部有序历史子SPE，不限制匿名或平局。m1目标直接成立，不调用空人数策略。零客户直接适用。
- **Conclusion / scope：** 仅为与主目标等价的跨实例通用证书存在性表示；没有构造lambda，非新福利界、算法复杂度结果、外审或新颖性认证。不能把只依m误读成已知lambda。
- **Dependencies：** 已有有符号Cartesian首次退出拼合、任意marked位置银行完整子SPE、产品覆盖可加；有限维凸集与开凸集分离。旧产品菜单位置分离为机制先例，旧TB/MP为特定价格候选。
- **Proof / objections：** 作者解析证明；credible先盲重构基本表示，后完成最终全文及新增marked紧域/BAL/安全延伸补审，绑定作者SHA见审查§9。父方独立重构开锥分离、beta>0及有理复制。无限生成锥不要求闭；价格只保证实数；产品M并未使用可加等式。
- **Evidence：** [作者全文](construction/uniform_signed_defect_prices.md)、[盲独立审查](credible/universal_signed_certificate_independent_review.md)、[银行与代数定义级核验](parent/audit_uniform_bank_domain.py)、[输出](parent/audit_uniform_bank_domain.json)。有限核验不承担普遍证明。
- **Remaining obligation：** 构造统一价格并证明对所有路径的付款；或以有限个真实组件给精确不可行证书，经银行回拉、清分母和全树拼合产生真正反例。主目标仍OPEN。

## CA-UNIFORM-PRICE-BAL-ROW-v1：通用证书的必要半空间

任意m>=2及j<m，任一上述统一价格必须 `sum_(i!=j)lambda_i-lambda_j>=m-5`。自足组件：不交A大小2，m-1个不交singleton Q，空E；目标j位A、末位Q1、其余E。全部正常M_i=1，g_j=-1、其余早位g_i=1，B=5-m。强制A后的完整子SPE可直接用“仅一A时选A，否则选未用Q”，并验证全部有序历史。它不要求目标路径自身是SPE。

状态：作者解析构造与父方独立定义级Fraction重算，独立解析审查已完成，见credible/universal_signed_certificate_independent_review.md §9。它是统一价格的必要约束，不是half反例或福利下界。代码及输出：[审计](parent/audit_uniform_price_rows.py)、[输出](parent/audit_uniform_price_rows.json)。

## 删除归纳接口方向审计

原m人SPE删i后的回放福利W-e_i；任意真正删后SPE eta记W_eta=W-e_i+d_i。若子人数已知OPT_(m-1)<=alpha W_eta，准确需付 `Delta_m+alpha*d_i<=alpha*e_i+(2-alpha)W`，其中Delta_m=OPT_m-OPT_(m-1)。向下修复损失并非该方向的直接obstruction；不能把独占客户e_i换成总收益u_i。

作者一般解析、global独立全文审查、父方定义级Fraction审计完成；只是正确归纳接点，没有支付修复后的新叶。详见[正文](deletion/induction_direction_and_rooted_budget.md)、[独审](global/deletion_independent_review.md)、[核验](parent/audit_deletion_contract.py)、[输出](parent/audit_deletion_contract.json)。

## CA-PRICE-LOWER-CUTS-v1 与统一价格域 v2

- **Exact statement：** 任意m>=2的任一通用half价格必须对所有非空I⊆[m-1]满足sum_I lambda_i>=|I|-1，等价sum(1-lambda_i)_+<=1。与原v1上域合并，主half等价于在K_pm（上下两正部和均<=1）内存在统一证书；这是加强版本v2，原v1上域结论及身份保留。
- **Domain / definitions：** 原任意共同目录；用于推导约束的明确全参数组件B大小m-|I|、m-1个单客户Q、唯一空E，I位置选E，其余全B；目标末位BR，M_i都是真实全历史门槛1，g=1_I，B_half=1-|I|。
- **Evidence/status：** 父方全参数证明；deletion及credible先盲重构、独立攻击通过；Fraction实现57条组件目标、价格域边界及ramp反算通过。仅表示的必要域，无half付款/外审/新颖性认证。正文[price_lower_cuts.md](parent/price_lower_cuts.md)，[独审](credible/lower_price_domain_independent_review.md)，[代码](parent/audit_price_lower_cuts.py)、[输出](parent/audit_price_lower_cuts.json)。
- **Refuted candidate：** lambda_i=2i/m并非通用证书；m7 I={1,2,3}的合法目标给价格余量-2/7。不是SPE目标或half反例；同候选五人必要条件通过不允许外推。

## CA-SIGNED-CREDIBLE-REPAIR-v1：双侧构造及有限字典成本

- **Exact statement：** 任意m>=2原组件及末位BR目标，g_i=M_i-u_i、B=2W-OPT_m。令P=sum g+、N=sum(-g)+、p=max g+、n=max(-g)+。存在同人数有限单位客户Cartesian实例及完整有序历史纯SPE，其half差额为Q[B+C(g)]，Q为清分母整数，C=2P-N+p+n。故严格负预算可编成真正half反例；没有这样的种子。
- **Dependencies/construction：** 正g的superlevel层用marked银行，负g的层用LOW；所有系数非负有理，sum真实g<=0，全部坐标首次异常永久进真正子SPE。W及OPT精确可加。C可以为负，负的是half差额而非客户或复制系数。
- **Support/cost scope：** C=max_(lambda∈K_pm)lambda·g；已有私有席位归纳补证marked g=-1_I精确，故C为此有限marked/LOW字典、sum组件g<=0这套线性规则内的最小LP成本。不是所有可能产品策略/任意修复器的全局最优成本。
- **Relation to Q：** 主half等价于对所有上述目标B+C>=0。该普遍标量预算仍未证，不能由构造本身推出；真实SPE g<=0时C=n-N<=0。
- **Status/evidence：** mixed作者一般解析、root独立层账及支撑函数重构、credible盲核后全文独审；[正文](mixed/signed_credible_repair.md)、[独审](credible/signed_repair_independent_review.md)、[父方系数核验](parent/audit_signed_repair.py)、[输出](parent/audit_signed_repair.json)。无外审/新颖性认证，无新无条件half范围。

## CA-STRONG-SECURITY-EXACT-M-EQUIV-v1

- **Exact statement：** 固定m>=2，原全实例全SPE的W>=m v_m，当且仅当全实例每条末位BR目标路径的sum_i M_i>=m v_m。M_m为末位最大回应值，改末位为BR不改任何前缀，故可显式推广为任意路径版本。v_m始终为真正整数不观察查询安全值。
- **Mechanism：** 任意大的k-unit主题加空E给全normal M1、v=1-(m-1)/(2k)，统一安全价格被迫全1；singleton-marked银行结合正供给给任意累计违例的有限显式编译，t=max(0,-min g)、a_i=g_i+t，t>0选k>=m且k>t*m*(m-1)/(2D)，总安全差为Q[-D+t*m*(m-1)/(2k)]<0。t0省正供给。
- **Scope/status：** 强辅助目标仍OPEN；没有违例种子，没有half反例或普遍付款。是既有exact-M累计候选的等价证明，不重新认领候选。作者解析、credible全文独审、potential非盲逐式核验及root系数Fraction核验通过。[正文](mixed/next_general.md)、[独审](credible/strong_security_exact_M_independent_review.md)。

## 原根全菜单的末位BR规范化付款

任意原真实根孩子T,H,A，b为中间负载；删T后A到最佳回应B的利润增加ell（不是与旧未删收益比较）满足2ell<=2P<=d_T<=u_root，P=sum_(x∈T\A)1/[(b+1)(b+2)]。对任意根菜单分布仍只用一份u_root。更早真实M、价格转移Omega及最优减员边际尚未支付。作者一般证明、global先盲terminal后全文独审通过；旧DR公式的末位推论，不称新全树修复。[正文](deletion/next_general.md)、[独审](global/next_general.md)。

补充：双侧修复只需要各正常位置的有理可信退出上界U_i：对每个合法强制主题（含正常主题）提供一份真实完整尾SPE使当前收益<=U_i即可。令g_hat=U-u，则真实g<=g_hat；按g_hat分层仍总真实g<=0，half差精确Q[B+C(g_hat)]。因此严格负的有证U表就是合法seed，无需证明每个U=M。credible已将此推论纳入最终全文审查；没有这样的实际严格seed。
