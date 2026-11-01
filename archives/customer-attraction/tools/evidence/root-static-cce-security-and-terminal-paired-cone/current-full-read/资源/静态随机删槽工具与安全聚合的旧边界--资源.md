---
id: "customer-attraction/static-slot-deletion-and-security-aggregate-boundary-resource"
kind: "resource"
type_tag: "资源"
title: "静态随机删槽工具与安全聚合的旧边界"
status: "complete"
review_level: "full-primary-reading-self-contained-reconstruction-and-new-exact-check"
summary: "自足重构带固定背景的安全值人数预算及空背景精确式，保其旧来源；合法对数查询设计不等于自由分数背景minmax的KKT。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/general_proof/potential_attack/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/general_proof/potential_attack/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/security_bridge/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/security_bridge/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/general_proof/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-29b83efed6b045678e3b7ee11dffb7b3/general_proof/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/round4_security/security_population_limit.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/round4_security/security_population_limit.md"
---

# 静态随机删槽工具与安全聚合的旧边界

## 静态值、槽重数与完整证明

有限单位客户、有限非空共同目录，固定非负整数背景b；v_r(b)=max_p min_(B∈S^(r−1))E_(T∼p)Σ_(x∈T)1/(b_x+1+c_x(B))。B可以联合相关，但不观察抽到的T。静态r下标指竞争r−1槽加一个查询者，不是沿SPE删一个真实玩家重均衡。

对r≥2，取v_r(b)有限minimax最优对手Q，先抽r−1个**带标签槽**的B，再独立均匀删一槽得到r−2槽合法Q'；重复主题不去重。对固定查询中的客户，原覆盖槽c、d=b_x+1+c。c=0时删除不变；c>0时
\[
 E\,[1/(b+1+c^-)]={1\over d}+{c\over(r-1)d(d-1)}
 \le {r\over r-1}{1\over d},
\]
因为c≤d−1。逐客户/对Q平均，每个查询对Q'的期望≤r v_r/(r−1)，取最大后再用Q'可行，得到
\[
 \boxed{(r-1)v_{r-1}(b)\le r v_r(b).}
\]
c=0、b=0分开所以没有除0。空背景s≥1槽的精确式为
\[
 sE[f_{B^-}(T)]=(s+1)f_B(T)-|T\setminus\cup B|.
\]
有覆盖客户取等(s+1)/(1+c)，无覆盖客户左s、右(s+1)−1=s。

源potential_attack独立重构后，父方核到旧112d22eb05d66119dd8f的security_population_limit.md已证这些结果；本批全文读该旧稿**仅related无额外done**，保旧成果身份。新Fraction仅核b=0,1,2,1000、s=1,…,12、c=0,…,s共360标量；普遍结论由带槽删除证明承担，不靠有限回归。它没有支付任何真实SPE首位或跨位置IC。

## 旧全目录极限的准确静态身份

旧稿还给空背景a_n=n v_n单调、a_n≤OPT_n≤U且a_n→U，U是整个有限目录可覆盖客户数。为自足固定接口：静态调和势Φ=ΣH_c的全局最大终局z是静态纯NE；均匀删其一个玩家，每个查询A都有f_(z_-i)(A)≤u_i(z)，平均得v_n≤W(z)/n≤OPT_n/n。这只用静态NE构造安全值对偶，**没有声称SPE福利受最差静态NE支配**，不受本批54尾反例排除。

若U>0，最大化L(p)=Σ_x log t_x(p)，t_x=Pr_p[x∈A]，存在所有t_x>0的最优p*。方向导数给每主题g(A)=Σ_(x∈A)1/t_x≤U，支持主题等号。若正支持ℓ个，则Σ_x1/t_x≤ℓU；任意n−1竞争槽满足Σ_xh_x/t_x≤(n−1)U。Cauchy给同一查询p*的每个竞争背景收益
\[
 \sum_x{t_x\over1+h_x}\ge{U^2\over\sum_x(1+h_x)/t_x}
 \ge{U\over n+\ell-1}.
\]
故nU/(n+ℓ−1)≤n v_n≤U，固定目录夹逼得极限。支持关联向量位于Σ_x z_x/t_x=U的暴露面，维数≤U−1，Carathéodory可取ℓ≤min(|S|,U)。U=0直接全部0，不用对数。该旧静态解析工具本批没有原程序新run，更没有从目录随n变化时作统一覆盖比保证。

## 两种log用法和自由分数minmax的KKT不同

上述log(t_x)是**构造一个查询分布的下界**，没有宣称它最优于所有n的安全博弈。general_proof曾误把普通Σ log(1+load_x)背景KKT当作自由分数minmax最优认证，后来已撤回；不能因这一误用而否定前一正确查询设计。

固定查询p，自由背景w质量s时目标K=Σ_x α_x(p)/(b_x+1+load_w(x))。对主题A的梯度为−Σ_(x∈A)α_x(p)/(b+1+load)^2；单纯形最小化要求这些非负平方分母和在支持上等于全目录最大值。若还要完整minimax鞍点，p必须支持于背景下最大查询主题。log(1+load)梯度只有一阶倒数，不是这个条件；一个log驻点、均匀背景或指定支持背景不自动认证自由值最小。已全文比较[凸对偶与切线价格界](../定理/自由分数门槛的凸对偶与覆盖价格界--定理.md)，不复活源已撤回错误。

## 不被静态工具支付的安全聚合

已证OPT_m≤(2m−1)v_m(0)是静态下界；逐人u_i≥v_m已否。W≥m v_m或较弱W≥(m−1/2)v_m仍需独立跨枝支付，不能从随机删槽或a_n单调得出。[真实路径安全链](../定理/真实路径安全值链的嵌入与债务恒等式--定理.md)的ΣD_i=W−m v_m是精确恒等式，局部负项已有原模型反例；弱链另保末位u_m/2，不能丢掉。

原security_bridge报告一个只满足每位稳健floor的精确放宽点，且倒二真实IC失败；本批未读其原程序/输出，只按README保“放宽而非SPE”报告，不重新认证该点或将其当新half反例。强弱iid、PI、全p去相关、实际均匀删槽核与旧背景直方图信用也只按源确认的旧失败范围导航，不自动合成新负模板。

任意合法背景的尾总利润P≥F_r(b)/2是另一个一般候选，F_r比较Σ d/(b+d)而非根覆盖。本批没有证明或反驳它；DIRECT、extra-one或静态尾替换已假不在逻辑上否定它。真正总安全值聚合亦未被本批有限例或银行逐人失败否定。
