# 本轮精确命题与证据等级

## Q-CAG-HALF：不变，OPEN

有限单位客户、任意有限非空共同目录、任意人数、每份完整有序历史纯SPE，结论2W>=OPT_m。空主题、重复选择、零客户及任意历史平局均保留。本轮没有完整一般证明、目标反例或新增无条件half范围。

## CA-UNIFORM-CREDIBLE-DEFECT-PRICES-v1：精确表示

- **Exact statement / quantifiers：** 对每个固定m>=2，原人数m上全实例全SPE的half成立，当且仅当存在只依赖m的实向量lambda>=0，使每个原模型实例的每条末位为BR的任意有序目标路径z都满足 `2W(z)-OPT_m+sum_(i<m)lambda_i(M_i-u_i(z))>=0`。每个M_i在真实目标前缀上取当前行动max、真实完整子SPE最低当前利润min；不冻结后继。统一价格可限制在 `sum_i(lambda_i-2)_+<=1`。
- **Objects / domain：** 原模型全部有限共同目录、单位客户、任意目标路径，前m-1位不必可信；全部有序历史子SPE，不限制匿名或平局。m1目标直接成立，不调用空人数策略。零客户直接适用。
- **Conclusion / scope：** 仅为与主目标等价的跨实例通用证书存在性表示；没有构造lambda，非新福利界、算法复杂度结果、外审或新颖性认证。不能把只依m误读成已知lambda。
- **Dependencies：** 已有有符号Cartesian首次退出拼合、任意marked位置银行完整子SPE、产品覆盖可加；有限维凸集与开凸集分离。旧产品菜单位置分离为机制先例，旧TB/MP为特定价格候选。
- **Proof / objections：** 作者解析证明；credible先盲重构基本表示，最终全文及新增marked紧域/BAL正补审。父方独立重构开锥分离、beta>0及有理复制。无限生成锥不要求闭；价格只保证实数；产品M并未使用可加等式。
- **Evidence：** [作者全文](construction/uniform_signed_defect_prices.md)、[盲独立审查](credible/universal_signed_certificate_independent_review.md)、[银行与代数定义级核验](parent/audit_uniform_bank_domain.py)、[输出](parent/audit_uniform_bank_domain.json)。有限核验不承担普遍证明。
- **Remaining obligation：** 构造统一价格并证明对所有路径的付款；或以有限个真实组件给精确不可行证书，经银行回拉、清分母和全树拼合产生真正反例。主目标仍OPEN。

## CA-UNIFORM-PRICE-BAL-ROW-v1：通用证书的必要半空间

任意m>=2及j<m，任一上述统一价格必须 `sum_(i!=j)lambda_i-lambda_j>=m-5`。自足组件：不交A大小2，m-1个不交singleton Q，空E；目标j位A、末位Q1、其余E。全部正常M_i=1，g_j=-1、其余早位g_i=1，B=5-m。强制A后的完整子SPE可直接用“仅一A时选A，否则选未用Q”，并验证全部有序历史。它不要求目标路径自身是SPE。

状态：作者解析构造与父方独立定义级Fraction重算，最终全文独立补审中。它是统一价格的必要约束，不是half反例或福利下界。代码及输出：[审计](parent/audit_uniform_price_rows.py)、[输出](parent/audit_uniform_price_rows.json)。

## 删除归纳接口方向审计

原m人SPE删i后的回放福利W-e_i；任意真正删后SPE eta记W_eta=W-e_i+d_i。若子人数已知OPT_(m-1)<=alpha W_eta，准确需付 `Delta_m+alpha*d_i<=alpha*e_i+(2-alpha)W`，其中Delta_m=OPT_m-OPT_(m-1)。向下修复损失并非该方向的直接obstruction；不能把独占客户e_i换成总收益u_i。

作者一般解析、global独立全文审查、父方定义级Fraction审计完成；只是正确归纳接点，没有支付修复后的新叶。详见[正文](deletion/induction_direction_and_rooted_budget.md)、[独审](global/deletion_independent_review.md)、[核验](parent/audit_deletion_contract.py)、[输出](parent/audit_deletion_contract.json)。
