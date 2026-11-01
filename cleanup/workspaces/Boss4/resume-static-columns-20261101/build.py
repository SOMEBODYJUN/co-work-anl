from pathlib import Path
import json
base=Path('archives/customer-attraction/subarchives/six-providers/state')
commit='68fad804ec5946cb296f77dc5b336308a66abf12'
prefix='research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round7/'
def save(rel,id,title,summary,sources,body,review=False):
 p=base/rel; assert not p.exists(),p; p.parent.mkdir(parents=True,exist_ok=True)
 meta=dict(id='customer-attraction/six-providers/'+id,kind='review' if review else 'lemma',type_tag='审查' if review else '引理',title=title,status='five-source-informed-reconciliation;historical-status-corrected;no-new-mathematical-run' if review else 'proved-stated-local-identities-and-capacities;global-common-payment-open',truth_status='historical-review-and-current-scope-reconciled' if review else 'analytic-all-finite-inputs-under-stated-hypotheses',review_level='historical-internal-reconstructions-compared;current-informed-analytic-reconstruction;no-external-review',scope='有限单位客户、有限非空共同目录、任意m≥1；叶代数不需SPE；使用IC处固定同一完整有序历史纯SPE',summary=summary,source_refs=['source:'+commit+':'+prefix+s for s in sources])
 lines=['---']
 for k,v in meta.items():
  if isinstance(v,list): lines.append(k+':'); lines.extend('  - '+json.dumps(x,ensure_ascii=False) for x in v)
  else: lines.append(k+': '+json.dumps(v,ensure_ascii=False))
 p.write_text('\n'.join(lines+['---','',body.strip(),'']))

save('引理/静态分母返回恒等式与同父双边容量--引理.md','static-denominator-return-and-fixed-parent-two-sided-capacity','静态分母返回恒等式与同父双边容量','真实off-history返回IC保留整行松弛；同B第一类正运输同时受实际行和受限父列控制，精确密度保公共客户余量。',['global/static_denominator_off_ic.md#1-对象','global/static_denominator_off_ic.md#8-固定-b-的全部静态正拥挤共同容量','coupling/fixed_parent_static_column_capacity.md','coupling/static_denominator_and_query_projection_review.md#2-独立推导与逐边利润界'],r'''
# 静态分母返回恒等式与同父双边容量

采用[共同目录完整历史模型](../../../../state/定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空共同目录，m≥1名单位玩家依次观察有序历史并选主题，终局覆盖者均分价值。保留空主题、重复动作、零客户及任意离轨平局。本页的返回身份使用同一完整纯SPE，后面的矩阵容量仅用合法完整叶，不依赖均衡。放在六人子档是为[六人目标](../问题/六人完整历史半覆盖目标--问题.md)保存任意人数工具，不收窄其数学范围。

## 原真实返回与静态中间层

固定σ，实际叶Z=(S₁,…,Sₘ)、实际覆盖C、实际收益uᵢ=uᵢ(Z)。对任意长度i−1的合法有序历史g，置
\[
B=\operatorname{finish}_\sigma(g),\quad a=B_i,\quad
W=\operatorname{finish}_\sigma(g,S_i),\quad
v=u_i(B),\quad z=u_i(W),\quad\ell=v-z\ge0.
\]
ℓ是g节点原规定动作对合法Sᵢ的**整条真实IC**；W后继仍沿原σ。对x∈Sᵢ定义
\[
d_i(x)=c_B(x)+1-\mathbf1_{x\in B_i}
=1+\sum_{j\ne i}\mathbf1_{x\in B_j},\qquad
\vartheta_i=\sum_{x\in S_i}1/d_i(x).
\]
d≥1且d≥c_B；x∈Sᵢ还保证c_Z,c_W≥1。d只是一层替当前动作而暂冻B其它动作的静态分母，**不是**原σ的真实偏离完成叶。
\[
T_B=\sum_{x\in S_i}\sum_{j\ne i}
\frac{\mathbf1_{x\in B_j}-\mathbf1_{x\in S_j}}{c_Z(x)d_i(x)},\quad
T_W=\sum_{x\in S_i}\sum_{j>i}
\frac{\mathbf1_{x\in W_j}-\mathbf1_{x\in B_j}}{d_i(x)c_W(x)}.
\]
保留原角色/客户标签，分正负为T_B=P_B−N_B、T_W=P_W−N_W，四量非负。逐客户倒数差给
\[
u_i-\vartheta_i=T_B,\qquad\vartheta_i-z=T_W,
\qquad\boxed{u_i=v-\ell+T_B+T_W.}\tag{SD}
\]
第二步使用B/W过去相同、静态层/W当前都为Sᵢ，故c_W−d只由j>i产生。于是任意整行系数β≥0有
\[
\beta(u_i-v)=\beta(P_B+P_W-N_B-N_W-\ell).
\]
这是signed账本；ℓ≥0给uᵢ≤v+P_B+P_W−N_B−N_W，不使联合正出口自动成为sub-Markov行。

第一类正边为
\[
q^B_{il}=\sum_{x\in S_i\cap(B_l\setminus S_l)}\frac1{c_Z(x)d_i(x)}.\tag{Q}
\]
支持自动排除i=l，每项≤1/[c_Zc_B]≤1/c_B，故qᴮᵢₗ≤uₗ(B)。第二类qᵂᵢₗ=Σ_{x∈Sᵢ∩(Wₗ\Bₗ)}1/[dᵢc_W]只在l>i，且≤uₗ(W)。两者分别支配于B、W的同角色利润，**不是**实际uₗ已经支付。

## 同一B跨全部行的共同列容量

现在只固定合法完整叶Z、B及同一张(Q)。不同i的真实孩子Wᵢ可以完全不同；矩阵不使用Wᵢ。对每行给合并后总系数0≤θᵢ≤L，未使用行设0，则每个l同时满足
\[
\boxed{\sum_i\theta_iq^B_{il}
\le L\,u_l\bigl(B;(C\cap B_l)\setminus S_l\bigr)
\le L u_l(B).}\tag{COLUMN}
\]
固定x∈(C∩Bₗ)\Sₗ，z=c_Z(x)≥1、b=c_B(x)≥1。恰z个实际角色覆盖x，各dᵢ≥b，所以发送合计≤Lz/(zb)=L/b，求和即得。x∉C无发送项，不定义1/c_Z；空列及L0均零。θᵢ必须是同B同角色**所有来源/上下文合计**，不能因每个来源分别≤L就重复使用z个coverer。

令Zₓ={i:x∈Sᵢ}、Bₓ={i:x∈Bᵢ}、r=|Zₓ∩Bₓ|。对新增B接收者l∈Bₓ\Zₓ，其收到的x金额除以B份额1/b，精确为
\[
\Lambda_{l,x}(\theta)=
\frac{\sum_{i\in Z_x\cap B_x}\theta_i+
\frac b{b+1}\sum_{i\in Z_x\setminus B_x}\theta_i}{z}
\le L\left(1-\frac{z-r}{z(b+1)}\right)\le L.\tag{DENSITY}
\]
common发送者dᵢ=b，actual-only发送者dᵢ=b+1，故所有θᵢ=L时中间上界取等；特别L=1、θ全1时精确密度为1−(z−r)/[z(b+1)]。密度与新增接收者l无关。只在b,z>0且有新增接收者时使用该式，精确保留B丢失实际coverer产生的余量。

## 同一显式矩阵的实际行界

固定i、x∈Sᵢ，正recipient数nₓ=|Bₓ\Zₓ|。因i∈Zₓ，若i∈Bₓ则n≤b−1=dᵢ−1，否则n≤b=dᵢ−1。因此
\[
\sum_lq^B_{il}=\sum_{x\in S_i}\frac{n_x}{c_Z(x)d_i(x)}
\le\sum_{x\in S_i}1/c_Z(x)=u_i(Z).\tag{ROW}
\]
非空Sᵢ时每项n/d<1，行界严格；空行0。b0时n0、d1亦合法。ROW和COLUMN对**同一张**显式矩阵同时实现，不是两份存在性运输。

## 支持兼容与不能重复收款的范围

COLUMN只占(C∩Bₗ)\Sₗ；它与fresh Bₗ\C、own-intersection Bₗ∩Sₗ三块两两不交。若既有请求在后二块保持相对份额密度≤L，可与COLUMN共同占≤L uₗ(B)。whole-profit重采未证明保持这个支持合同。

此界不含direct θᵢvᵢ(B)、Wᵢ第二类正边、已占actual-new支持的请求或另一个B′的请求。不能把direct和COLUMN各≤L相加还称≤L。restricted profit也不能直接当作ℓ：规定Bₗ改Sₗ的whole-IC还有共同客户负载变化及Sₗ\Bₗ收入，不许擅自按客户改权。

[真实查询投影](强制未来利润的真实查询投影与反向分裂--引理.md)解决强制未来利润的使用域；[单孩子前缀回推](同子枝前缀利润的非负共同回推--引理.md)是不同联合接口，不可免费相加。[坐标初始化](../../../../state/引理/全客户坐标库存的双预算初始化--引理.md)也用静态分母和联合列计数，但reference=T、actual=B，不能将其初始化或后加强密度守卫倒填为本整网共同容量。历史内审和全部五原件见[审查资源](../审查/静态列与查询投影的历史审查及强菜单停界--审查.md)。本页不证吸收、actual cap或half。
''')
save('引理/强制未来利润的真实查询投影与反向分裂--引理.md','synthetic-profit-real-query-projection-and-reverse-split','强制未来利润的真实查询投影与反向分裂','任意合法叶角色利润非负守恒地表示为真current/future利润；局部PRICE不能穿透重复current层，保B边反向核方向仍为actual到off-history。',['coupling/static_denominator_and_query_projection_review.md#3-一般-synthetic-profit-的-query-projection-接口','coupling/static_denominator_and_query_projection_review.md#5-投影-price源时间与不能自动继承的-hit','coupling/static_denominator_and_query_projection_review.md#6-保留第一类正边的-sd-反向非负-kernelroot合同独立核查','global/static_denominator_off_ic.md#4-单-reset-初始域及迭代域的区别','global/static_denominator_off_ic.md#5-强制未来利润的合法-query-projection'],r'''
# 强制未来利润的真实查询投影与反向分裂

在[共同目录完整历史模型](../../../../state/定义/共同目录完整历史模型--定义.md)固定任意m≥1、同一完整有序历史纯SPEσ、实际叶Z=(S₁,…,Sₘ)。保空主题、重复、零客户及任意平局。本页是[静态返回分解](静态分母返回恒等式与同父双边容量--引理.md)的域修复和局部非负分裂，不提供全树共同付款。

## 一次重置的真利润域不能无证迭代

若B=finishσ(Z_{<k},Aₖ)且i>k，第一类B正边到j<k为零；j=k是actual-prefix真query，可由原actual k的整条IC支配；j>k都是B上的真prescribed context，含k<j<i的过去角色。因此初次使用这些B过去利润合法。

返回W=finishσ(B_{<i},Sᵢ)后可能有k、i两次强制。若再从W更晚节点用SD，其第一类过去利润可能含该过去角色之后的强制行动；它不是该角色的规定完成利润，不能购买其IC。一般对合法叶F定义
\[
\mathcal F(F)=\{j:F_j\ne\sigma_j(F_{<j})\}.
\]
若r=max𝔽(F)，j>r时finishσ(F_{<j})=F；j=r是真强制query，可用同节点整条IC；j<r须保synthetic利润或另作域修复。𝔽空时所有角色真规定。

## 任意合法叶的QUERY-PROJECTION

给任意合法完整叶F和角色j，不要求F沿σ、仅一次强制或本身SPE。记a=Fⱼ、h=F_{<j}，
\[
R=\operatorname{finish}_\sigma(h,a),\quad H=\operatorname{finish}_\sigma(h),\quad
f=u_j(F),\quad d=u_j(R),\quad V=u_j(H)\ge d.
\]
V≥d是h上规定动作对a的原whole-IC。F/R过去及当前相同，差异只在l>j。对x∈a，令J_F(x)、J_R(x)是两叶除j外的coverer集，并定义
\[
q_l=\sum_{x\in a:\ l\in J_R(x)\setminus J_F(x)}\frac1{c_F(x)c_R(x)},\quad P=\sum_lq_l,
\quad N=\sum_{x\in a}\frac{|J_F(x)\setminus J_R(x)|}{c_F(x)c_R(x)},
\]
\[
J=\sum_{x\in a}\frac1{c_F(x)c_R(x)},\qquad
L=\sum_{x\in a}\frac{|J_F(x)\cap J_R(x)|}{c_F(x)c_R(x)}.
\]
分母均正，qₗ>0只可能l>j。逐客户coverer差给
\[
f=d+P-N,\qquad d-N=J+L,
\qquad\boxed{f=(d-N)+\sum_{l>j}q_l.}\tag{PROJ}
\]
a非空时J>0、d−N>0、V≥d>0；a空时f=d=P=N=J=L=0，全系数取0。所以
\[
\boxed{f=\alpha V+\sum_{l>j}q_l,\qquad
\alpha=(d-N)/V\in[0,1].}
\]
current金额进真规定context(h,j)的完整利润V；每个future qₗ进(R_{<l},l)的真规定利润uₗ(R)，且qₗ≤uₗ(R)。输入wf时以同一w输出w(d−N)、wqₗ，非负且恰守恒，current whole-profit系数wα≤w。较小请求z≤f取w=z/f。合并同context输入后须重算其同一whole-IC系数，不能每个projection另领actual钱包。

## 局部PRICE、源时间支持及HIT组合缺口

逐个future qₗ≤J≤J+L=d−N。以f归一化，current量≥任一future量，故该行属于“包含current角色j的非空角色子集均匀分布”的凸包。它与[净券角色HIT](../../../../state/定理/净券跨节点角色命中与来源后缀界--定理.md)的局部行形状相同，但这里current进入**另一natural context**，不是actual终点。

若F在k以前匹配Z且待投影j≥k，则h/R保该前缀，future全>j；SD第一类边也无j<k，第二类只向未来。这些局部支持保“不早于fresh源k”的候选不变量；谈最终实际角色前仍需整体图守恒且可吸收。

旧GLOBAL-HIT证明对目标集外current使用终点命中值0；此处只能把同角色续节点界成h，不能原封套用。抽象两层：第一层1/2去同角色继续、1/2去目标；第二层同角色再1/2终止、1/2去目标，最终命中3/4，而每层都满足二元uniform-subset合同。这只证明**局部PRICE合同不足推出原HIT**，未声称真实coverer可实现该抽象合成；真实约束须另证。

## 保留第一类正边的反向SD核

沿用SD单行u=uᵢ(Z)、v、P_B、P_W、N_B、N_W、ℓ。ROW给P_B≤u。置
\[
r=u-P_B\ge0,\quad F_*=\ell+N_B+N_W\ge0,\qquad r=v+P_W-F_*.
\]
保留全部B正边，从W正边删总额c=min(P_W,F_*)，可任取固定分数子容量。于是
\[
v-F_*+c=\min(v,r)\ge0,\quad P_W-c=(r-v)_+,
\quad\boxed{u=P_B+\min(v,r)+(r-v)_+.}\tag{REVERSE}
\]
r≥v时删F_*、current留v；r≤v时删全部W正边、current留r，故无需误设F_*≤v。current完整B利润系数min(v,r)/v≤1，v0时金额与系数0。W出口仍是原正边子容量，全部B边保留ROW/COLUMN；负项与ℓ只在该行F_*参与一次。

方向是**actual u输入→off-history利润**，不是fresh/OPT已回到实际钱包。第一类若在多强制叶中仍需PROJ或[前缀回推](同子枝前缀利润的非负共同回推--引理.md)，current B也可能与COLUMN占同客户支持。反向核、正向SAFE、投影可形成同角色/反向环；没有证明吸收、有限访问成本/累计IC系数、actual cap1/cap2或六人half。身份、域合法、局部守恒与最终容量必须分开。

原父方反向核是收到COLUMN/ROW后的推导，coupling§6从合同复核；本次知情清洗不重演其历史盲审。见[审查与证据](../审查/静态列与查询投影的历史审查及强菜单停界--审查.md)。
''')

save('引理/同子枝前缀利润的非负共同回推--引理.md','one-child-prefix-profit-joint-nonnegative-pushback','同子枝前缀利润的非负共同回推','同B/W共同前缀的全部过去利润请求用非负列次随机算子回推；角色系数无穷范数不增，ancestry域修复有限，不许叠多孩子或旧请求。',['credible/joint_prefix_claim_pushback.md'],r'''
# 同子枝前缀利润的非负共同回推

在[单位客户共同目录模型](../../../../state/定义/共同目录完整历史模型--定义.md)取任意m≥1、1≤i≤m和两个合法完整叶B,W，满足Bⱼ=Wⱼ对所有j<i。叶代数不需SPE，不限制目录、客户数或平局。记pⱼ(B)=Σ_{x∈Bⱼ}1/c_B(x)，同样定义pⱼ(W)。同一个W的每个prefix角色j<i给0≤λⱼ≤L，输入F=Σ_{j<i}λⱼpⱼ(W)。

## 单角色安全退款与整束列容量

对j<i、l≥i定义
\[
q^+_{jl}=\sum_{x\in B_j\cap(B_l\setminus W_l)}\frac1{c_B(x)c_W(x)},\quad
q^-_{jl}=\sum_{x\in B_j\cap(W_l\setminus B_l)}\frac1{c_B(x)c_W(x)},\quad
N_j=\sum_{l\ge i}q^-_{jl}.
\]
x∈Bⱼ=Wⱼ保证原分母正。负载差只来自后缀l≥i，因此
\[
p_j(W)-p_j(B)=\sum_{l\ge i}q^+_{jl}-N_j.
\]
对x∈Bⱼ，设rₓ为B/W全部共同coverer数、aₓ为W新增数；c_W=rₓ+aₓ且rₓ≥1。于是
\[
p_j(B)-N_j=\sum_{x\in B_j}\frac{r_x}{c_B(x)c_W(x)}\in[0,p_j(B)],
\]
\[
\boxed{p_j(W)=[p_j(B)-N_j]+\sum_{l\ge i}q^+_{jl}.}\tag{POS}
\]
退款来自同一B角色完整利润；未按客户重权使用IC、未假配到另一个actual钱包。

设bₓ=# {j<i:x∈Bⱼ}。同前缀使bₓ≤c_W(x)，交换有限求和得
\[
Q_l:=\sum_{j<i}q^+_{jl}
=\sum_{x\in B_l\setminus W_l:\ b_x>0}\frac{b_x}{c_B(x)c_W(x)}
\le p_l(B).\tag{COLUMN}
\]
显示式须限制bₓ>0，或按无原项贡献0，避免c_W0时0/0。这是同一W**所有prefix**共同占一次B后段容量，不能把每个j单边界分别领一份。

## 完整利润系数共同上界与价格推论

定义
\[
\kappa_j=\lambda_j\frac{p_j(B)-N_j}{p_j(B)}\ (j<i),\qquad
\kappa_l=\frac{\sum_{j<i}\lambda_jq^+_{jl}}{p_l(B)}\ (l\ge i).
\]
零利润主题无客户，相应分子0，系数取0。POS/COLUMN给
\[
\boxed{F=\sum_{l=1}^m\kappa_lp_l(B),\qquad0\le\kappa_l\le L\ \forall l.}\tag{PUSH}
\]
可写非负矩阵T：Tⱼⱼ=(pⱼ(B)−Nⱼ)/pⱼ(B)，Tⱼₗ=q⁺ⱼₗ/pₗ(B)当l≥i，其余0，κ=λT。每列和≤1，故系数无穷范数不增；**单输入行系数总和未必≤1**。i1时incoming空、im时一后段列、m1/空客户/空题均按零约定成立。

每份输入金额只留j或进l≥i>j。任意非负非减角色价格z满足
\[
\sum_{j<i}z_j\lambda_jp_j(W)
\le\sum_lz_l\kappa_lp_l(B)\le L\sum_lz_lp_l(B).
\]
λ全1且zₗ=1_{l≥k}，每个k<i有
\[
\sum_{j=k}^{i-1}p_j(W)\le\sum_{l=k}^mp_l(B).
\]
其输入≤输出价格方向来自向未来移动，与fresh源[非增价格界](../../../../state/定理/净券跨节点角色命中与来源后缀界--定理.md)不同；这里还用输出共同系数界，不能两份资金分开相加。

## SPE分枝栈的有限域修复

若B是最后强制位置k后沿σ完成的叶、i>k，W=finishσ(B_{<i},d)，则W过去j<i利润带未来强制d，不能购买j的IC。PUSH不买假IC：新增l≥i>k在B是真规定context；保留j>k也真；j≤k须继续向B父叶回推。

对递增强制位置栈
\[
L^0=Z,\quad L^r=\operatorname{finish}_\sigma(L^{r-1}_{<i_r},d_r),\quad
 i_1<\cdots<i_s,
\]
一次纯ancestry规范化中，待修复同角色项每次减少一栈层；新增recipient在其parent最后强制位置后已真规定；到Z全部实际利润合法。因此这次**域修复有限**。真context若再进入off-IC展开可重造原W，不推出整体网络终止或无环。

## 不可免费叠加是实质边界

本合同固定一W、一B、一组prefix。已有B后缀请求须与κ相加，多个孩子分别κ≤L不推出和≤L，叶容量也不是actual钱包。[独立审查](../../tools/evidence/static-column-and-query-primary/comparison/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round7/independent/review_prefix_pushback.md)给两个明确SPE叶例：

- 两人，目录X={x}和空题，全历史规定X；B=(X,X)、W=(X,empty)。prefix收益1送回B两角色各1/2，κ=(1,1)。另加系数1的已有B第二角色请求，总3/2>W(B)=1，不可能全B cap1。
- 两人，X有2客户，Y、Z各含不交单客户；全历史选X是完整弱SPE。B=(X,X)，孩子(X,Y)、(X,Z)各prefix收益2，单独恰占parent福利2；两份总4不能共享parent cap1。

只反免费叠加，不反本引理、half或其它共同预算。独审另有H-overlap complement和允许混过去标签的共同客户表示，均未支付新W客户或全部future利润，不能无证换掉本页同角色保留合同。与[共同覆盖者投影](共同覆盖者请求的逐客户联合投影--引理.md)一样，本引理尚无全树共同容量、吸收或actual cap2。
''')

save('引理/共同覆盖者请求的逐客户联合投影--引理.md','common-coverer-requests-clientwise-joint-projection','共同覆盖者请求的逐客户联合投影','任意两叶共同coverer的同客户请求联合投影到目标份额，最大密度乘r/c_F；不含原叶exclusive incidences，重采须另保支持。',['global/static_denominator_off_ic.md#7-与共同客户出口兼容的一条容量不等式','global/static_denominator_off_ic.md#8-固定-b-的全部静态正拥挤共同容量'],r'''
# 共同覆盖者请求的逐客户联合投影

采用[共同目录模型](../../../../state/定义/共同目录完整历史模型--定义.md)，取任意合法完整叶F,R和一个客户x。固定叶代数无需SPE或IC。

设Cₓ=cover(F,x)∩cover(R,x)、rₓ=|Cₓ|、Dₓ=cover(R,x)\cover(F,x)。每个共同coverer j∈Cₓ给0≤λⱼ(x)≤Lₓ，输入金额λⱼ(x)/c_F(x)。r0时无输入；有输入时c_F,c_R均正。将每份请求拆为
\[
\text{同角色 }j:\ \frac{\lambda_j(x)r_x}{c_F(x)c_R(x)},\qquad
\text{每个新增 }l\in D_x:\ \frac{\lambda_j(x)}{c_F(x)c_R(x)}.
\]
因rₓ+|Dₓ|=c_R，逐份守恒。以R份额1/c_R为券单位，输出密度
\[
\Lambda_{j,x}=\lambda_j(x)r_x/c_F(x)\ (j\in C_x),\qquad
\Lambda_{l,x}=\sum_{j\in C_x}\lambda_j(x)/c_F(x)\ (l\in D_x)
\]
支持不交，故
\[
\boxed{\max_{l\in\operatorname{cover}(R,x)}\Lambda_{l,x}
\le L_x r_x/c_F(x)\le L_x.}\tag{COMMON-CAP}
\]
R未覆盖x时C空，无请求，不用无关零分母式。

同客户的共同过去券和共同未来券可**先合并λ再投影**，一次占目标份额；不能prefix先领一次cap，又让common future全额独占相同券。[前缀共同回推](同子枝前缀利润的非负共同回推--引理.md)保过去同角色、只向丢失后段coverer运输，是另一表示；本页F/R任意，但输入严格限共同coverer。

F独占coverer请求（x∈Fⱼ、x∉Rⱼ）不在输入域，且可能含R全未覆盖的新客户；COMMON-CAP没有支付它们。R角色是否真prescribed须另核，份额容量不证明可购买该角色IC。

与[同父静态列](静态分母返回恒等式与同父双边容量--引理.md)的兼容是：固定B的正静态边只占(C∩Bₗ)\Sₗ；既有fresh Bₗ\C和own-intersection Bₗ∩Sₗ若密度≤L，三块不交，可共同占L uₗ(B)。但后续whole-profit IC重采未被证明维持逐客户λ≤L、common支持或三块分离。因此局部共同容量未关闭SD+PROJ环图、实际钱包或六人half。
''')
save('审查/静态列与查询投影的历史审查及强菜单停界--审查.md','static-column-query-projection-review-and-stopped-full-menu-scope','静态列与查询投影的历史审查及强菜单停界','保存五原件解析新增、原内审先验与导航；分开六证书有限阴性和已知强桥反例，追读银行反族更新Mfull/extra-one状态。',['coupling/README.md','coupling/fixed_parent_static_column_capacity.md','coupling/static_denominator_and_query_projection_review.md','credible/joint_prefix_claim_pushback.md','global/static_denominator_off_ic.md'],r'''
# 静态列与查询投影的历史审查及强菜单停界

五份主源共37731B逐字全文读取，由本次`work.py clean show ID --out`实际取得冻结字节；size/SHA256/Git blob与metadata逐项核同。[原件及原show输出](../../tools/evidence/static-column-and-query-primary/README.md)保全。主源均Markdown，本次原程序main/import、收益/IC重算、数学扫描均0；静态YAML、链接及指纹核对不叫数学PASS。

## 五源全部内容去向

| 源ID／文件／字节 | 独有内容和正文 |
|---|---|
|09e88a6b11f6264a6a83，coupling/README.md，4094|fresh源因果序、坐标初始化、同父列、prefix内审、query投影/反向核导航；六旧证书强菜单测试停止和三条旧失败边界，本页保导航和时态，不冒未领链接为done。|
|9c613946f6641758cb8e，fixed_parent_static_column_capacity.md，5515|同B/同Z、不同Wᵢ的COLUMN、精确密度、同一q的ROW、合计θ守卫及direct/第二类/旧请求禁叠，见[静态分母与双边容量](../引理/静态分母返回恒等式与同父双边容量--引理.md)。|
|36b9bc7cc4211abd8d56，static_denominator_and_query_projection_review.md，9922|合同后未读证明的历史重构；两步SD、单重置/多强制域、synthetic PROJ、PRICE/时间与HIT组合障碍、保B边反向核，见[投影与反向分裂](../引理/强制未来利润的真实查询投影与反向分裂--引理.md)。|
|c51f7faac28bb42e7a8c，joint_prefix_claim_pushback.md，6728|单W整组prefix安全退款/共同列/列次随机系数，非减价格及后缀利润，递增分枝栈有限修复，多个孩子/旧请求/循环限制，见[前缀共同回推](../引理/同子枝前缀利润的非负共同回推--引理.md)。|
|71ba6b57cc3e3d8e6cb5，static_denominator_off_ic.md，11472|SD/EXCESS、两类利润支配/真实域、PROJ接合与未付义务；§7共同coverer逐客户投影及§8精确密度/fresh-own-static不交支持，见上述页及[共同覆盖者投影](../引理/共同覆盖者请求的逐客户联合投影--引理.md)。|

一般证明在四页按完整条件重写，没有把审查通过、报告字段或有限回归升为共同付款。

## 原内部审查的先验与独有接续

coupling投影稿记载先收global_budget7的精确对象/公式/支持域/closure异议，在未读其证明正文时重构SD、利润支配和QUERY-PROJECTION；其§6另收到root保B边反向核合同后独立核查。global稿反过来接入coupling投影。credible前缀稿记root按陈述核恒等式/非负退款/列和，coupling按合同未读作者正文重构；固定列稿记root、independent7以及global的密度推导。

本次正常旁读并原样保全parent/reverse_sd_and_joint_review.md、independent/review_fixed_parent_first_positive.md、independent/review_prefix_pushback.md、coupling/joint_prefix_claim_transfer_blind_review.md，均确认这些主断言，并给精确余量、两个不可叠加叶例及0/0校正。它们是历史内部审查，不是外审、新颖性或当前重演盲审；作为related读取不替其owner提交done。父审所称原348客户脚本/数值只保为其历史说明，本次未读那份程序/输出就不冒认证其执行细节，也不重复旧成功实验。

README的fresh_source_order_and_suffix_hits.md已全文旁读，对应正式[净券角色命中与来源后缀界](../../../../state/定理/净券跨节点角色命中与来源后缀界--定理.md)。SOURCE-ORDER、后缀HIT、PREFIX-CUT、价格是原固定SAFE/CLIP图、current为actual终点的关系；本PROJ current是另一个natural节点，不能直接继承HIT。full-O源也可能初始化就落在更早actual角色，不能冒用fresh时间界。

README的optimal_coordinate_inventory_blind_review.md导航已与正式[坐标库存双预算初始化](../../../../state/引理/全客户坐标库存的双预算初始化--引理.md)全文比较：reference=T、actual=B，rₓ≥0、正部缺额经一条whole-IC付款，同点future同时受库存/原边容量，客户对recipient actual新鲜而非必然全局fresh。其full-SAFE余量付款未证，后加强密度守卫不能倒填旧实现。本批不将该导航再做一次primary处置。

## 已停止的强全菜单候选与六份原报告

在合法前缀h固定原完整SPE，强制当前A后的完整叶Z_A保留全部过去/玩家。d_A是当前真收益，定义
\[
K_{T,A}=\sum_{x\in T}\frac1{1+c_x(Z_A)},\qquad
D(p)=\sum_Ap_Ad_A,\qquad C(p)=p^\mathsf TKp.
\]
测试要求**每个h、每个p都有D(p)≥C(p)**，还试pair加强d_A+d_B≥K_{A,B}+K_{B,A}。SPE仅给D(p)≤u，所以D<C不推出C>u。

3355B audit_diagonal_full_menu.py和10478B冻结JSON均全文旁读保于comparison，未执行。代码只用Fraction，读取固定六个example/完整strategy，在全部有序history核全部含self IC；p测试为全部非空均匀支持，以及每个两点支持二次型的严格内部极小点。它不穷尽全部实p、不搜索新游戏、无随机性，仅stdout而不写邻接报告。原报告完整保留history/p/diagonal/K/forced-leaf字段；其统计为：

|case|m/k|complete IC|tested p|negative pair|min gap|
|---|---:|---:|---:|---:|---:|
|portfolio_matching_failure|2/5|30|245|0|299/150|
|root_tax_failure|4/6|1554|20169|0|5/11|
|individual_security_failure|3/6|258|3326|0|23/14|
|eight_cce_welfare_gap|3/4|84|393|0|2/13|
|coverage_opportunity_failure|3/5|155|1260|0|3/14|
|prefix_balance_failure|4/6|1554|20172|0|5/22|

这是原报告身份，不绑定当前运行，也不以表格删除原witness。README已明确六份pass不能支持早已失败的普遍候选，因此停止追加。

两剩余推送原稿6c84043505685faee8ec、完整根菜单稿68ed7412ef2da880f80f和round7/security/cross_pair_scope.md均全文旁读，精确比较为：

1. **三人**34单位客户、六主题加空主题、完整57历史SPE，p(X2)=1/10、p(empty)=9/10给D=29/30、C=41/40，差−7/120。题名“两剩余”稿内同时含r2正定理与这个r3停界；不是r2反例，且C<u。正式[非空主题强聚合反例](../../../../state/反例/完整强制终局聚合去相关的非空主题反例--反例.md)另保同34原策略及私有填充，量词是实际路径所有节点聚合D比较，不能与本单根读数混为同一计算。
2. 旧348客户、六主题、三人完整43历史策略有d₂=d₅=u=147/2、K₂₅=K₅₂=159/2，pair亏空12。但半半p的C=737/12<u、原第0列cap69<u；只反pair，不反较弱C≤u或Mfull。本次没有重跑旧258项IC或称新游戏。
3. 原任意背景PB-extra已排任意背景Mfull；当时不能直接外推到空根或实际SPE前缀。README保这一范围区别正确。

当前[八客户额外查询例](../../../../state/反例/同分布额外查询高于平均强制收益--反例.md)还纠正另一原脚本把G−平均D误叫G−actual u。本页保持同样区别；有限pass及强桥失败都不决定half。

## 后来的状态校正不能沿用历史OPEN

原round7 README/security将空根Mfull和根extra-one保OPEN是当时状态。旁读完整根菜单稿开头已有2026-10-25逐位置桥被真正零根反族否定的更正。当前全文比较[笛卡尔银行完整根菜单反例](../../../../state/反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)与[extra-one边界](../../../../state/问题/自由extra-one与iid安全值边界--问题.md)：四人10客户12主题完整SPE根u=4/3，保根四槽矩阵Mfull=59/36>u；r槽自由分数Jensen下界B₄=19/14>u亦否真正整数extra-one逐人桥。一般银行m≥4成立，含恰六人，不是任意背景外推。

因此一般Mfull、全p-WP、低值对称meta-Nash及整数extra-one逐人桥不能在本页继续称当前开放。银行W8、OPT₄10仍过half；全路径共同支付等较弱合同须独立判断。SD/COLUMN/PROJ/PUSH这些局部真关系没有因此失效，也没有自动成为six-half证明。五人half已有他证；当前恰六人主目标仍按子档接续。

## 关系审查与剩余义务

四数学对象已逐项查关系：SD产生第一类显式q；同一q的ROW使REVERSE的r≥0，COLUMN只控制固定B第一列；PROJ修复强制未来利润域，PUSH共同合计同孩子全部prefix，COMMON-CAP合计同客户common incidences。它们是身份、容量、域修复和有限祖先规范化关系，不是已经吸收的共同钱包。与SAFE/HIT保current终点差异，与坐标初始化只共享计数机制，不共享免费资金。

仍须用同一来源/同一实际预算合计direct、B正边、不同W未来请求、负项/whole-IC松弛，处理环/有限总访问成本，持续保持必要支持和系数。尚无该普遍定理或本机制反例。本批按Root指令不改共享map/总目录，第三阶段可据[关系清单](../../tools/evidence/static-column-and-query-primary/relations.json)逐边登记，不能由导航链接自动造推导边。
''',review=True)
print('wrote five self-contained objects')
