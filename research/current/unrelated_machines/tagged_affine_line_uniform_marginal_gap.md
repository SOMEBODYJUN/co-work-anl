# 单标签边际均匀的仿射线菜单仍有趋二实际间隙

## 精确身份与读取目的

- **ID/version**：`UM-TAGGED-AFFINE-LINE-BALANCED-MARGINAL-TINY-VALUE-v1`。
- **Objects / Domain / Definitions**：prime R≥3、域F_R、每变量独立tagged资源块F_R²；每group/state在其每个变量取一条slope label/intercept固定的完整line，同变量各group的intercepts互异。完整非负有理state权总1，所有零incidences仍在实际矩阵中。
- **Quantifiers / Exact Statement / Conclusion**：对每个R有下述显式菜单，所有groups均R个states、均匀选state使每个incidence的slope label均匀，变量degree≤R，但任意state/partial选择的最优值精确V=1/(R−1)。完整普通UM实际OPT=2−1/(R−1)，可确定性显式位多项式输出达界全调度。可加零权fresh变量使共同arity R、R-partite而精确保值。
- **Assumptions / Dependencies**：无复杂度假设；`UM-MODEL-v1`与完整矩阵。上下界自足计数，不依赖CONFIG gap、未知actualYES或有限实验。
- **Scope**：反驳“tagged affine LINE几何+单坐标uniform marginals足以对任意state-dependent norm1权保统一正常数actual partial值”。不是cube反例；main diagonal/helper permutation关系非pairwise independent，不声称是Chan/LST原PCP hard image，不给源CSP满足比例或NP-hardness。
- **Evidence / Objections**：rank先仅Exact独立全证，root实际全文读后才解封作者Proof，再实际作者读后与最终正文指定scope审；root先听口头策略不记盲审。任意helper自由选态、全部非main块helpers、未选states额外exports和zero jobs均在上下界中。来源见[审查](../../reviews/unrelated_machines/tagged_affine_line_uniform_marginal_gap_review.md)。
- **Status**：限定构造与精确上下界证明完整，独立重构/作者读后/最终正文审查各记实际范围；无软件/外审/全球新颖性认证；主目标`UM-TARGET-v1`仍OPEN。
- **Related Files**：[任意权下的并行关系半保留](weighted_affine_parallel_relation_reweighting_obstruction.md)、[原uniform line接口](line_set_packing_and_take_continue_compilation_obstructions.md)、[审查](../../reviews/unrelated_machines/tagged_affine_line_uniform_marginal_gap_review.md)。

## 1. 真正的完整tagged LINE对象

变量为不同tags u_a,v_a，a∈F_R；资源是每变量x的全部(x,z,y)，z,y∈F_R。line L_x(ℓ,j)含所有(x,z,ℓz+j)。Groups为main M及H_(a,j)，j≠0。

M参加全部u_a，intercepts皆0。它有R个states t，在每个u_a上label皆为t；state t的正权只在

\[
B_t=\{(u_t,z,tz):z\ne0\},
\]

每点权1/(R−1)。其它完整line incidences权0。

H_(a,j)参加u_a和v_a，intercepts皆j。它有R个states ℓ，在u_a的label为ℓ，在v_a为ℓ−a−j。若ℓ≠a，唯一正权1放在

\[
\left(u_a,\frac{j}{a-\ell},\frac{aj}{a-\ell}\right);
\]

若ℓ=a，唯一正权1放在P_a=(v_a,1,0)。其它完整line incidences皆0。分母非零，且ℓ·j/(a−ℓ)+j=aj/(a−ℓ)，所以第一点在原u_a line及B_a；fallback时v_a slope为−j，P_a也在原line。每state总权1。

u_a的intercepts为main的0及全部非零j，degree恰R；v_a仅非零j，degreeR−1，均注入。均匀选M的t或helper的ℓ，各incidence labels均为F_R上的置换，故边际均匀。这是输入显式local分布，不是从actualYES得来。

## 2. 任意partial选择的精确值

对固定helper H_(a,j)，ℓ≠a时j/(a−ℓ)遍历全部非零元素，因此其正资源选择恰为B_a的任一点，或fallback P_a。没有把helper预绑某个B点。

任意min质量>0的partial allocation，所有helper都必须取得其selected state的唯一unit正点。若main选state t，block t的R−1个helpers须在B_t∪{P_t}的R点中领取R−1个不同点；至多一个用fallback，故main至多取得一枚B_t点。于是V≤1/(R−1)，质量0的情形也满足此界。

达界可选t=0（或任意t），main领取(u_t,1,t)。H_(t,1)选ℓ=t领取P_t；其余所有H_(a,j)选ℓ=a−1，领取(u_a,j,aj)。对a≠t，这些helpers匹配B_a全部点；对a=t，它们避开main的z=1点。不同tags不交，所有helpers质量1，main质量1/(R−1)，因此精确达界。全部非main blocks也已分配，R=3同样有效。

## 3. 完整普通UM的全部任务与真实最优值

每indexed state一台private，每tagged resource一台resource机；每group一枚selector在本组各private耗时1。每完整line incidence一枚不同原job，只可在自身private耗原权p，或在其resource机耗1；其余∞。所有未选states及全部zero private jobs均保留。

上界把selectors放上述selected states，仅外送所领正点jobs，所有其它原incidences留自身private。selected main负载1+(R−2)/(R−1)=2−1/(R−1)，selected helpers负载1，未选private总权1，resources至多一unit。每原job恰执行一次。

下界看任意完整调度。峰C≥2时已够；C<2时每helper实际selector所在state的唯一positive incidence不能与selector同private，必须外送。unit resource在C<2时至多一job。若main实际选state t，block t的helpers占用至少R−2枚不同B_t点，main至多外送一枚positive job；其selected private仍有selector1及至少(R−2)/(R−1)正工作。故C≥2−1/(R−1)。未选states的额外exports只占更多容量，zero exports不减main正质量。上下界覆盖同一完整原矩阵的全部任务。

## 4. 共同arity、partite结构与显式位长

Parts c∈F_R，u_a放part a，v_a放part a+1。对每helper与每个其它part c，添只属它的fresh变量w_(a,j,c)，intercept0、state ℓ的label为ℓ，整条line新增权全0。每group此时共同arity R且每part一变量；fresh degree1，标签边际仍均匀。

新增点质量0，partial allocation双向忽略它们不改V。原调度扩展时全部新zero jobs留其private，新增resources空；新调度投影删新jobs不增负载，故实际OPT也精确保留。这不是从原输入删除零jobs。

记g=1+R(R−1)，S=Rg。基础变量2R、resources2R³、incidences I=R³(2R−1)，机器S+2R³、jobs g+I、finite条目S+2I。padding后变量数V'=2R+R(R−1)(R−2)，resources V'R²、incidences I'=R³g；机器S+V'R²、jobs g+I'、finite S+2I'，dense为相应机器数乘jobs数。有限时间仅0、1/(R−1)、1；均按显式poly(R)规模构造，不声称仅binary R时poly(logR)输出。有限域运算和达界assignment无需优化oracle。root以Fraction反算R=3/5/7的计数与负载只作数字核对，不作一般证明依据。

main不同变量labels恒相等，helper两旧labels恒相差常数，两坐标joint只支持R对而非R²对；zero padding也不改变这个相关性。因此本反例准确排除单边际充分性，保留额外pairwise-independent关系、真正hard image与全局source decoder的未解义务，没有把趋二实例当作近二计算困难性。
