# Boss7 3D 数学复核：SUMmin 联合前提与六人 half；二元尾利润的局部边界

日期：2026-11-16。复核范围限于题定两个已 done 的 3B 任务及它们的当前登记端点、正文和必要证据；未重领任务，未更改 canonical 边、registry 或 receipt，未执行 Git/队列写入、公屏或 work.py 同步。

## 结论

**没有发现必须修复的数学错误。** `boss7-summin-conditionally-pays-six-half-3b-3b-17d90d43aa54c665` 的条件蕴含完整成立：同一实例、同一完整纯 SPE 的 SUMmin-full 若对所有混合查询分布成立，则该 SPE 满足 half；对所有六人实例及 SPE 作全称量化即得到目标的完整条件结论。边保留了唯一尚开放的动态付款前提，没有从纯查询或有限探针推出混合查询预算，没有缺失另一个需要加入 ALL 的独立未证前提。

近邻 `cag-degree-two-tail-route5-threshold-gap` 只成立为指定二元共享族的局部贡献：每个固定根背景中全部可重复 q 槽的聚合利润最大值为真实尾利润 qH。该标量上界不能转成 route5 的逐动作最低收益下界。现边使用 `contribution`，未填 `whole_result`，明确保留实现性、跨枝付款和净需求下界，范围恰当。

这两个结论均不证明一般 SUMmin，也不证明或反驳六人一般目录 half。负驻留差、交换不等式的严格间隙和某种付款模板的失败，只是相应模板的障碍。

## 当前端点与精确阅读位置

当前 `research/registry.json` 四条记录已实际读取：

| 对象 | 版本、真值 | 实际陈述 |
| --- | --- | --- |
| `customer-attraction/e7-summin-full-common-budget-exact-discount-and-finite-tests` | v2，open | 全部 m≥1 完整 SPE，对同一个合法 p，Σ_i min_A E_p K_i(T,A)≤W；一般混合预算开放。 |
| `customer-attraction/six-providers/exact-six-full-history-half-cover` | v1，open | 任意有限共同标签目录、每份六人完整历史纯 SPE，2W≥OPT_6；保空覆盖、别名、重复、零客户及所有离轨弱平局。 |
| `customer-attraction/degree-two-exact-root-tail-profit` | v1，proved | 指定二元共享族及指定完整 SPE，每根 Z、全部可重复 q 槽比较的 max R_Z=qH 及精确取等支持。 |
| `customer-attraction/closeout-67a92b6751929baa34cc1de3` | v1，unassessed source | 保全完整孩子子 SPE 终局集合、正确门槛递归和有额外需求下界时的 half 接口；并未声称该下界已证。 |

实读文件与标题（下文简称对应本表）：

1. `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md`：全文，尤其《策略、真实续局与全部历史量词》《合法背景和剩余利润》。同覆盖异标签不能直接商掉；非零背景未来利润不等于新增覆盖。
2. `archives/customer-attraction/state/候选/全槽逐行最小价格的共同预算与有限报告--候选.md`：全文，尤其《真完整列、逐行最小与开放付款》《静态充分关系与完整槽数》《原m−1槽账与额外完整槽折扣》。
3. `archives/customer-attraction/state/引理/完整槽末位最小价格的精确折扣与静态充分桥--引理.md`：全文，尤其《完整槽的静态比较常数恰按2m计》《从未证全路径预算到half的条件推导》《早期位置仍缺什么》。
4. `archives/customer-attraction/state/程序/五人全槽行最小价格与三尾混合整数探针--程序.md`：全文，尤其《2. 行最小搜索的完整合同》《4. 三尾 MILP 的较强任意背景问题》《5. 一份完整三尾策略的精确核验》。这里只借用其证据边界，未读/运行冻结优化器或原证书树。
5. `archives/customer-attraction/subarchives/six-providers/state/问题/六人完整历史半覆盖目标--问题.md`：全文，尤其《精确定义》《当前可确立的边界》《已有证据与未决缺口》；并全文读 `archives/customer-attraction/subarchives/six-providers/问题--问题.md` 的《恰六人半覆盖》。
6. `archives/customer-attraction/state/资源/完整后继门槛的阶段接口与选中枝边界--资源.md`：全文，尤其《精确门槛递归及两向证明》《选中枝最低值的原中间误写》《正确half条件和粗份额的不同集合》。
7. `archives/customer-attraction/state/定理/二元共享客户完整策略的精确根后尾利润--定理.md`：全文，《端点 (a=0,b=1)》《端点 (a=b=1)》《同一组取等与六人接口》《取等支持》。
8. `archives/customer-attraction/state/构造/二元共享客户的完整均衡负驻留族--构造.md`：全文，尤其《全有序历史IC证明》《θ是纯背景最坏最佳回复，不是混合安全值》《actual最优福利及共享遗漏》《严格门槛与历史审查边界》。
9. 两任务 JSON、两边 JSON 及各自 `review.md` 已实读：
   - `research/operations/map-v2/tasks/Boss7-summin-six-half-3b-3b-17d90d43aa54c665.json`；`map/edges/Boss7-summin-six-half-3b-3b-17d90d43aa54c665/{summin-conditionally-pays-six-half.json,review.md}`，后者《2. 已证明的条件边》。
   - `research/operations/map-v2/tasks/Boss7-degree-two-tail-3b-3b-f3ae5b2ec578da03.json`；`map/edges/Boss7-degree-two-tail-3b-3b-f3ae5b2ec578da03/{degree-two-tail-route5-threshold-gap.json,review.md}`，后者《只能得到的局部 contribution》。

两边当前 SHA256 分别是 `699209dd36c7bc2c5f7b5e040bb2adffe481cea5a35bd52188447b03b7974a5f`、`89aaa0a782692656e2a23aa6b07d0a02baaf6733abcfac34e4e49f83fc4d230b`。逐个重算两边全部 evidence 文件 SHA，与边内绑定均相同。当前对象版本与边的端点版本相符。

## 独立重推 SUMmin 到 half

固定一个有限标签目录模型、m≥1 和一份在所有有序历史定义的完整纯 SPE σ。实际叶为 z，收益 u_i，W=Σ_i u_i。对实际第 i 位前缀强制 A，沿**同一 σ 在改变后的历史**真实续行到完整 m 槽 Z_i(A)。定义

\[
K(T,y)=\sum_{x\in T}\frac1{1+c_x(y)},\quad
R_i(p)=\min_A\mathbb E_{T\sim p}K(T,Z_i(A)).
\]

每列都是合法 m 槽静态背景；没有删强制者，没有重选子 SPE，没有冻结原在轨后继。重复列可合并为相同终局，重复/同覆盖标签仍留在原策略定义域，不影响矩阵论证。

假设此固定实例、σ 的开放前提

\[
(U_\sigma)\quad\forall p\in\Delta(\mathcal S),\quad\sum_{i=1}^mR_i(p)\le W.
\]

则每个 p 均有 min_i R_i(p)≤W/m。这里必须是**同一个 p** 出现在全部行；各行的最小列 A 可以依 i,p 改变，但不能依实际抽到的 T 改变。因此

\[
M_{\rm path}:=\max_p\min_{i,A}\mathbb E_pK(T,Z_i(A))\le W/m.
\]

有限矩阵 minimax 给

\[
M_{\rm path}=\min_{Q\in\Delta(\mathcal M_\sigma)}\max_T\mathbb E_QK(T,y),
\qquad\mathcal M_\sigma=\{Z_i(A):i,A\}.
\]

接下来不需要 Q 来自顺序均衡。对任意合法 m 槽静态背景分布 Q，令

\[
\ell_x=\mathbb E_Qc_x(y),\quad a_A=\frac1m\mathbb E_Q\#\{j:y_j=A\},\quad
f_\ell(T)=\sum_{x\in T}\frac1{1+\ell_x},\quad M_\ell=\max_Tf_\ell(T).
\]

有 Σ_A a_A=1 及 ℓ_x=mΣ_{A∋x}a_A。对任意 m 比较槽 T_j 的并集 O，逐客户用 1=(1+ℓ_x)⁻¹+ℓ_x/(1+ℓ_x)，并把第二项扩大到所有客户，得到

\[
\begin{aligned}
|O|&\le\sum_{j=1}^m f_\ell(T_j)+\sum_{x\in N}\frac{\ell_x}{1+\ell_x}\\
&=\sum_{j=1}^mf_\ell(T_j)+m\sum_Aa_Af_\ell(A)\le2mM_\ell.
\end{aligned}
\]

重叠客户在第一项多算只会使不等式更宽；重复比较标签合法。倒数函数凸，逐客户 Jensen 给 f_ℓ(T)≤E_Q K(T,y)，故每个 Q 都满足

\[
\operatorname{OPT}_m\le2m\max_T\mathbb E_QK(T,y).
\]

取所有合法 m 槽 Q 上的最小值，得到 OPT_m≤2m v_{m+1}(0)。路径菜单是所有合法背景的子集，最小化域变小使值上升，因此方向为 v_{m+1}(0)≤M_path。合并为

\[
\operatorname{OPT}_m\le2m v_{m+1}(0)\le2mM_{\rm path}\le2W.
\]

于是 m=6 给 OPT_6≤12(W/6)=2W。其实在 minimax 后直接把静态不等式用于菜单最优 Q 也能得到相同结论；中间 v 不增加任何未证桥。m>0 是唯一所用除法条件，不除 W 或 OPT，零覆盖实例原样成立。

ALL 与 whole_result 核定：源 conjecture 的全称陈述提供全部 (U_σ)，对其六人子域逐 σ 应用即可得到目标完整的全称结论。静态计数、Jensen、有限 minimax 和菜单包含关系在正文中已证明，是边的内部证明，不是漏列的开放来源。故单源 `premises_mode:all`、`relation_mode:conditional` 和条件性的 `whole_result` 都准确；并无从“存在好 SPE”跳到“每份 SPE”的量词升级。

## 纯查询与混合查询间确实未闭合的步骤

纯 p=δ_T 时，以 A=T 可得

\[
R_i(\delta_T)\le K(T,Z_i(T))\le
\sum_{x\in T}\frac1{c_x(Z_i(T))}=u_i(Z_i(T))\le u_i(z).
\]

强制者本人覆盖 T，故该处 c≥1；末步依实际节点的完整 SPE IC。混合时仅有

\[
\min_A\mathbb E_pK(T,Z_i(A))\ge
\mathbb E_p\min_AK(T,Z_i(A)),
\]

方向不能用于把纯点预算扩成 (U_σ)。一个完全合法的小例已经严格：m=1、两个不交单客户主题，任取主题都是完整纯 SPE，W=1。K 矩阵对角为 1/2、非对角为 1；均匀 p 下 min_A E K=3/4，而 E min_A K=1/2。它证明交换确可严格；SUMmin 仍有 3/4≤1，half 仍成立。这不是六人反例，也不是 SUMmin 反例。

末位 R_m=G_b−max_A D_b^p(A) 的固定背景式确实支付末行；早期 A 改变整份真实后继，不能递推该结构到全部行。证据中五个保存 p、固定策略浮点锥和一个合法背景的三尾子博弈各有自己的有限范围，不能替代 (U_σ) 的所有 p 和全部完整 σ。静态账中恰有 m 个竞争槽，当前推导也不能直接换成 m−1 或 2m−1。

## 独立重推二元尾利润与 route5 边界

固定 q≥2，整数 b≥1、0≤a≤b，根 Z∈X。q 个比较槽的主题重数为 n_v，边负载 d_{ij}=n_i+n_j，根背景指示 e_{ij}=1_{Z∈{i,j}}。聚合尾利润为

\[
R_Z(T)=\sum_{ij}\mu_{ij}\frac{d_{ij}}{d_{ij}+e_{ij}},
\quad\mu_{ij}=b\text{（跨组）或 }a\text{（组内）},
\]

零分子取零。它优化任意合法 q 槽静态比较，尚不要求该比较能作孩子子 SPE。

在 (a,b)=(0,1) 时，支持分属两组且命中 x,y≥1 个顶点，s=x+y≤q，命中跨边 qs−xy≤(q−1)s+1≤q²−q+1≤q²−q/2；每边利润至多一。支持单组不足 q 个时至多 q(q−1)。整组各一次则 q(q−1) 条满份边加 q 条半份根边，正好 q²−q/2。q>2 时混合支持由上界严格排除；q=2 的混合支持若命中三条边，至少一条是被根占用的边，故仍严格落后。

在 (a,b)=(1,1) 时，设 n=2q−1、k 为非根支持数，非根满份边恰 f(k)=C(n,2)−C(n−k,2)。若根不在比较支持，根边和≤q/2，因为 t/(1+t)≤t/2 对整数 t≥0 成立。k=q 且各一次达到 f(q)+q/2，其它 k 严格落后。若根在支持且 k≤q−2，根边和≤2q−1=f(q)−f(q−2)，故总和≤f(q)，严格小于目标；若 k=q−1，则所有选中标签各一次，值 f(q−1)+2(q−1)/3+q/2，比目标小 (q−1)/3。该证明覆盖比较重复及比较含根两种边界。

每个固定 T 的 R_Z 对 a,b 线性，(a,b)=(b−a)(0,1)+a(1,1) 为非负组合，两端由相反整组同时取等，所以

\[
\max_T R_Z(T)=q\bigl[(q-1/2)b+(q-1)a/2\bigr]=qH=V_Z.
\]

取等支持也正确：a=0 时两整组；0<a<b 时两个端点取等集的交仅相反整组；a=b>0 时任意 q 个不同非根标签。指定构造的完整历史 IC 用 F(s) 对组内最终人数的单调性处理新动作，用收益≤S/2≤L 处理重复偏离，再在每个首次重复历史的互斥子树接一份完整 BI 策略；因此它不是只认证根菜单的在轨构造。其根收益 L=qb/2+(q−1)a，尾 H=(q−1/2)b+(q−1)a/2；L−H=−(q−1)(b−a)/2，W=OPT=q²b+(q−1)(q+2)a/2。q=5,a=1,b=2 给 L=9,H=11,V=55、负差 −2、W=OPT=64。这一负差没有反驳 half。

route5 中 R_h(A) 却是**所有完整孩子子 SPE** 可实现的完整终局集合，L_h(A)=min_{z∈R_h(A)}u_i(z)，Θ_h=max_A L_h(A)。固定 σ 只从每个 R_h(A) 选一个元素；它的收益不能直接等同这些集合的最小值。父可实现集的必要性由每个真实离轨收益≥其分支最小值给出；充分性由对每个离轨动作独立选取达到最小值的孩子子 SPE 并在互斥子树拼合给出。因此正确链是 u_i(z_h)≥Θ_h≥L_h(a)，绝非 L_h(a)≥Θ_h。

沿 actual 路径 Σ_i Θ_{h_i}≤W 已成立；half 仍需一个最优带位置元组满足 Σ_i L_{h_i}(T_i)≥OPT_m−W。固定根 R_Z 的聚合**上界**没有提供这个逐人**下界**，也没有证明任意比较槽可实现为相应孩子子 SPE。构造的 θ=L 是纯静态背景最坏最佳回复值，不是 route5 的 Θ_h，也不是混合安全值。现边的 `contribution.result` 正确落在精确族的固定根比较，`remaining` 保留了这些差异；没有把目标资源整条说成被源定理证明。

## 新计算及开放缺口

本轮执行一次独立标准库精确有理枚举，程序及结果在同目录：`cag-joint-exact-check.py`、`cag-joint-exact-check.json`。对 q=2,…,6 的每个 q 槽重数向量（共 14,774 个），分别取 (a,b)=(0,1),(1,1),(1,2)，共 44,322 个参数/向量组合；15 个设置的精确最大值及**全部取等支持**都与解析式相符。q=5 的六人数字及上述交换严格例也已精确核算。这个新计算只核固定根有限目标，没有枚举或认证全部完整 SPE，没有运行 LP/MILP，也不被用来代替一般 q 的两端点证明。

本轮无最小修补需要。尚开放且不能由两边消去的具体义务是：(1) 对每份完整 SPE 和同一混合 p 的 SUMmin 全路径共同预算；(2) 若走 route5，则为最优位置元组支付净需求 OPT−W 的逐动作下界和互斥枝共同账；(3) 恰六人一般目录、每份完整历史纯 SPE 的原 half 命题。负驻留差或某个上界/分母模板不够强，只否定该模板的无条件使用，均不构成原题反例。
