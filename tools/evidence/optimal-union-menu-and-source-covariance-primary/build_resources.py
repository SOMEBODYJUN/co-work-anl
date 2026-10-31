from pathlib import Path
import json,hashlib,os
S=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-optimal-union-menu-and-source-covariance-primary')
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
E=S/'tools/evidence/optimal-union-menu-and-source-covariance-primary'
W=S/'cleanup/workspaces/Boss4/r3-optimal-union-menu-and-source-covariance-primary-next';W.mkdir(parents=True,exist_ok=True)
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
primary=json.loads((E/'source-manifest.json').read_text());related=json.loads((E/'related-source-manifest.json').read_text());contexts=json.loads((E/'context-manifest.json').read_text());byid={d['id']:d for d in primary+related}
paths=[
'archives/customer-attraction/state/候选/最优并集税与平均真实菜单的付款接口--候选.md',
'archives/customer-attraction/state/引理/整数完整负载的三八源去相关界--引理.md',
'archives/customer-attraction/state/资料/首次饱和前沿的审查层次与共同付款边界--资料.md']
def relative(t,p):return os.path.relpath(t,Path(p).parent).replace(os.sep,'/')
def write(i,ident,kind,tag,title,status,summary,ids,body):
 p=paths[i];refs=[]
 for sid in ids:
  for d in byid[sid]['sources']:
   ref=f"source:{d['commit']}:{d['path']}"
   if ref not in refs:refs.append(ref)
 head='---\n'+''.join(f'{k}: {json.dumps(v,ensure_ascii=False)}\n' for k,v in dict(id=ident,kind=kind,type_tag=tag,title=title,status=status,summary=summary).items())+'source_refs:\n'+''.join('  - '+json.dumps(x,ensure_ascii=False)+'\n' for x in refs)+'---\n\n'
 text=body.replace('§',chr(92))
 for sid,d in byid.items():text=text.replace('@'+sid,relative(d['saved_path'],p))
 for j,t in enumerate(paths):text=text.replace('@P'+str(j),relative(t,p))
 for d in contexts:text=text.replace('@CTX'+d['path'],relative(d['path'],p))
 text=text.replace('@E',relative(E.relative_to(S),p))
 out=S/p;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(head+text)
write(0,'customer-attraction/optimal-union-tax-average-menu-payment-interface','candidate','候选','最优并集税与平均真实菜单的付款接口','exact-static-identities-and-meta-existence; common-tree-payment-open',
'完整m槽的最优并集预算、平均实际位置菜单的对称Nash及联合后继势身份全部自足保留；付款PAY仅是未证充分条件。明确源槽边际与全槽边际、后继尾部排除当前行动、旧mΓ去重及后续3/8系数界仍不足。',
['5d12b9ba337060130d26','c0ca00d7195e1370c7d7','37b0cc25eda54afa70b8'],
r"""# 最优并集税与平均真实菜单的付款接口

## 原件、对象和真实状态

[1190B menus路由](@5d12b9ba337060130d26)与[5801B主稿](@c0ca00d7195e1370c7d7)完整实读，legacy/main各同字节。研究是单位客户、单位玩家、有限非空共同目录、全部有序历史纯SPE，保空主题、重复行动、零客户及任意历史依赖平局。m≥1，固定完整策略σ及实际路径Z，最终收益u_i和福利W=Σ_i u_i。

已证部分是完整列的精确代数、有限对称均衡存在及条件推导；真正的共同树付款尚未证明。原稿“个人一般探索”“无固定人数扩展任务”“未git/外发”均是历史研究身份，不是本轮执行指令或一般half完成状态。本页不把静态恒等式重排登记为新增SPE福利关系。

对每个实际位置i，固定实际过去h_i。若当前强制A，沿同一σ得到完整m槽Z_i(A)，固定过去也包含在内。定义

§[
K_i(T,A)=§sum_{x§in T}§frac1{1+c_x(Z_i(A))},\qquad
d_i(A)=u_i(Z_i(A)),\qquad
§overline K=§frac1m§sum_iK_i.
§]

K是独立额外查询对完整m槽的价格，不能删去当前A。原当前IC给d_i(A)≤u_i；相同计数历史并不因此可在策略核验时合并。

## 任意完整列分布的精确最优并集预算

固定达到OPT_m的一份合法m元组(T_1,…,T_m)，并集O，客户覆盖重数d_x，p_O是均匀抽该元组一槽的主题边际。任取由合法完整m槽组成的终局分布Q，不要求列来自SPE。令

§[
n_x=c_x(Z),\quad L_x=§mathbb E_Q n_x,\quad
h_x=§mathbb E_Q§frac1{1+n_x},\quad
k_Q(T)=§sum_{x§in T}h_x.
§]

q_Q是先按Q抽完整列、再均匀抽其中一槽的主题边际；随后查询与竞争列独立重抽。因此m k_Q(q_Q)=Σ_xL_xh_x，而不是同列Σ_xE[n_x/(1+n_x)]。定义

§[
V_Q=§sum_x§left(L_xh_x-§mathbb E_Q§frac{n_x}{1+n_x}§right)
=§frac12§sum_x§mathbb E_{Q§otimes Q}
§frac{(n_x-n'_x)^2}{(1+n_x)(1+n'_x)}§ge0,
§]
§[
S_O(Q)=§sum_{x§in O}(d_x-1)h_x+
§sum_{x§notin O}§mathbb E_Q§frac{n_x}{1+n_x}§ge0.
§]

逐客户得

§[
§boxed{§operatorname{OPT}_m
=m k_Q(p_O)+m k_Q(q_Q)-V_Q-S_O(Q).}
§tag{COV}
§]

因为第一项为Σd_xh_x，第二项减V后变为ΣE[n/(1+n)]；O内再减(d−1)h后恰h+E[n/(1+n)]=1，O外被S完全消去。令M(Q)=max_Tk_Q(T)，于是

§[
§operatorname{OPT}_m§le2mM(Q)-V_Q-S_O(Q).
§tag{CAP}
§]

保留两个价格时COV右端对每Q恒为同一OPT；只调Q、而没有真实IC价格上界，并不产生新福利约束。

V_Q正是[已实读D22原文7390B](@37b0cc25eda54afa70b8)在空额外背景、r=m时的mΓ，不重新认领其发现。D22的同列插入税T_Q还给k_Q(q_Q)=平均实际槽收益−T_Q+Γ及max-query的下界；这是下界，不能反读成所需价格上界。完整m槽与m−1槽、同列取槽与独立重抽均保留。

## 平均菜单的内生对称Nash与同一分布

把矩阵Kbar作为有限对称两人博弈的行收益，列收益为转置。有对称混合Nash p，记C=p^T Kbar p，则

§[
(§overline Kp)_T§le C\quad§forall T,\qquad
p_T>0§Longrightarrow(§overline Kp)_T=C.
§tag{META}
§]

自足存在性说明：令g_T(p)=((Kbar p)_T−p^TKbar p)_+，映射
F_T(p)=(p_T+g_T)/(1+Σg)是连续单纯形自映射。由有限维Brouwer固定点取p。若G=Σg>0，固定点给g_T=p_TG，所以每个正p_T的收益差严格正，违背Σp_T[(Kbar p)_T−C]=0；故G=0，全部行≤C且正support取等。这里的唯一标准导入是Brouwer固定点；不是求解器或多项式构造承诺，也不提供C的福利上界。

定义Q_p：独立均匀抽实际位置i，再抽A~p，执行真实完整Z_i(A)，并保留第i槽为指定源。则k_{Q_p}(T)=(Kbar p)_T，CAP变成

§[
§operatorname{OPT}_m§le2mC-V_{Q_p}-S_O(Q_p).
§tag{MCAP}
§]

Q_p的指定源行动边际是p，但从其完整列再随机抽任意槽的q_{Q_p}一般不等于p。不能把“源分布”“完整槽边际”“最优元组分布p_O”混成同一对象。即使多个(i,A)产生相同终局负载，算价格可合并终局边际，算真实d_i及后继遗憾仍须保留指定角色与真实历史。

令

§[
D=§frac1m§sum_i§mathbb E_{A§sim p}d_i(A),\qquad
e_i=u_i-§mathbb E_pd_i(A)§ge0,\qquad mD=W-§sum_i e_i.
§]

对这一p及固定最优元组，若能证明

§[
§boxed{2m(C-D)§le V_{Q_p}+S_O(Q_p)+2§sum_i e_i,}
§tag{PAY?}
§]

便由MCAP得OPT≤2W。删去右侧IC slack是更强充分条件，原稿不要求它。PAY是尚未证明的充分条件，不是已证预算，也不与half自动等价；MCAP的两个最大价格替换可能严格。一般证明可以选择适当最优元组和META的p，尚未证明总能选择；一个坏纯列、坏p或坏最优元组不能直接反驳这种存在版本。

## 联合后继势：尾部必须排除当前A

为消除原文“真实尾部”的潜在歧义，本页明确

§[
Z_i(A)=(h_i,A,Y_i(A)),\qquad |Y_i(A)|=m-i.
§]

Y只含当前以后的真实后继，不含当前A；b_i是h_i的客户负载。剩余r=m−i+1槽是(A,Y)，不能把r槽整体塞进Y，否则所列重叠税分母会偏一。这个约定与[既有完整根菜单身份](@CTXarchives/customer-attraction/state/反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)一致。

定义Phi_b(Y)=Σ_xΣ_{j=1}^{c_x(Y)}1/(b_x+j)、F_i(A)=Phi_{b_i}(Y_i(A))，

§[
R_i(T,A)=§Phi_{b_i}(T,Y_i(A))-§Phi_{b_i}(T,Y_i(T)),
§]
§[
§delta_i(T,A)=§sum_{x§in T§cap A}
§frac1{(b_i(x)+1+c_x(Y_i(A)))(b_i(x)+2+c_x(Y_i(A)))}§ge0.
§]

先对后继Y_i(A)加入查询T，收益为Σ_T1/(b_i+1+cY_A)；再把完整列中已有当前A保回，重叠客户价格恰少δ。又d_i(T)=Phi_b(T,Y_i(T))−F_i(T)，故严格有

§[
§boxed{K_i(T,A)=d_i(T)+F_i(T)-F_i(A)+R_i(T,A)-§delta_i(T,A).}
§tag{COL}
§]

R也等于Phi_{b_i+1_T}(Y_i(A))−Phi_{b_i+1_T}(Y_i(T))，因为两式中Phi_b(T)相消。一个简单边界检查：m=1、单客户且目录只有其主题A，正确Y为空，K(A,A)=1/2=d(A)−1/2；若误把Y含A，会给δ=1/6和错误5/6，说明上述排除约定不可省略。这是记号检查，不是对正确COL的原模型反例。

独立T,A同分布p时，在每个相同位置i上E[F_i(T)−F_i(A)]=0，不能跨位置拼漂移。因此

§[
m(C-D)=§sum_i§mathbb E_{p§otimes p}(R_i-§delta_i).
§tag{REG}
§]

PAY对同一p/O等价于

§[
2§sum_i§mathbb E(R_i-§delta_i)
§le V_{Q_p}+S_O(Q_p)+2§sum_i e_i.
§tag{TREE-PAY?}
§]

它仍只是half的充分系统。恰一位后继时R_i≤0来自真实末位最佳回复；多后继的R是联合势替换，后继各自最优不等于共同最大化Phi。V、S是一份共同Q的税，不能每个位置复制一份。

## 后续三八界、旧反例及没有闭合的系数

指定源客户指示a_x=1_{x∈A}，完整负载n_x≥a_x。Q_p上有

§[
D-C=§sum_x§operatorname{Cov}(a_x,1/(1+n_x))
+§mathbb E§sum_x§frac{a_x}{n_x(1+n_x)}.
§]

零负载项按0。记T_src=EΣ_x a_x/[n_x(1+n_x)]，原整数差界完整写为C−D≤V−T_src。后续[三八代数引理](@P1)把“不保源税”的V系数降至3/8，并可扣其对角余项；两条带不同负项的完整上界并不逐点有统一强弱，应该保留后取较小值，不能用“3/8加强”一句丢掉T_src。

例如一个客户、m=3、合法主题A含该客户/B为空，Q各半取(A,A,B)与(A,A,A)，均指定A为源，则a恒1、n为2或3。C=7/24、D=5/12、V=1/48、T_src=1/8；旧INT上界−5/48，带对角1/16的三八上界−7/128，前者反而更低。这是本页为比较两条界作的直接有理代入，不是SPE反例或新运行。三八改善的是分散项系数，不能自动抹除旧源插入负信用。

但即使代入3/8，仅有

§[
§operatorname{OPT}_m§le
2W-2§sum_i e_i+(3m/4-1)V_{Q_p}-S_O(Q_p)
§le2W+(3m/4-1)V_{Q_p}-S_O(Q_p).
§]

m≥2时V系数为正，仍无一般消去关系；三八最优常数不是SPE付款定理。原README“三八独审待办”是较早路由状态，后续独审原件已存在并实读，不改其历史字节，也不称外审。

[银行完整根菜单反例](@CTXarchives/customer-attraction/state/反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)已经否定一般根矩阵的低值对称Nash/Mfull和全p强桥；那是根矩阵K、值与一个当前收益u的合同。此处平均实际位置Kbar加V/S/Σe的选择性PAY不同，不能仅移用旧root反例就称本候选已否定。反过来，META固定点存在也没有支付其值。

D22的stationary核只平衡主题边际，不保证同时是META的p。真实根历史揭示源后，条件协方差可为0，却仍留下不同根历史之间的总协方差；不能把深层条件式望远镜相加宣布联合R债务已付。

可接续的是在这一准确平均真实菜单的META分布上，构造TREE-PAY的合法真实IC支付或真正完整SPE的候选反例。它与[首次饱和前沿](@P2)共享原模型，但两套查询law/钱包不自动兼容。没有程序源、本批原程序或有限扫描运行0次，未导第三阶段图或给出一般half证明。
""")
write(1,'customer-attraction/integer-complete-load-three-eighths-source-decorrelation','lemma','引理','整数完整负载的三八源去相关界','proved-pairwise-integer-load-bound; sharp-without-SPE; no-welfare-payment',
'逐对证明合法完整整数负载分布的C−D≤3V/8，保最优极限常数、指定源槽与独立查询、对角严格余项和实负载sqrt3边界；常数不因锐性而成为真实SPE子类锐界或一般half付款。',
['0f6deaf27382917e1003','9782838c9e2bbf41d23b'],
r"""# 整数完整负载的三八源去相关界

## 输入、原件与精确量词

[3869B原解析文](@0f6deaf27382917e1003)和仅作比较的[3966B独审原件](@9782838c9e2bbf41d23b)全部实读。原证明、独立成对证明、极限锐性及独审补充的对角余项均在下文自足保留；不将本次读两文重新称作“只见陈述盲证”，也不把内部审稿升成外审。

Q是有限分布，每样本含一个合法完整m槽终局Z和其中一指定源槽，其行动A。对单位客户x定义a_x=1_A(x)∈{0,1}、n_x=c_x(Z)∈{0,…,m}，所以a≤n。查询T从源主题边际p独立于竞争终局重抽。定义

§[
D=§mathbb E_Q§sum_x§frac{a_x}{n_x},\qquad
C=§sum_x§mathbb E_Qa_x§mathbb E_Q§frac1{1+n_x},
§]
§[
V=§sum_x§left[§mathbb E_Qn_x§mathbb E_Q§frac1{1+n_x}
-§mathbb E_Q§frac{n_x}{1+n_x}§right]§ge0.
§]

n=0时a=0，a/n及a/[n(1+n)]均约定0。源槽不必是从全部槽均匀抽到，但必须属于该终局。分布可以不是SPE，下面只需每客户a二值、n非负整数及a≤n。

§[
§boxed{C-D§le(3/8)V.}
§tag{1}
§]

V是既有完整槽分散项mΓ，非本源首次发现。3/8是此代数类的最小普遍常数，任意固定m≥2也锐；不声称原SPE平均菜单子类内仍锐。m=1更强有C≤D，不能把“固定m≥2锐”错扩到m=1。

## 两个逐对恒等式及完整证明

先固定一客户，取独立同分布副本(a',n')，f(n)=1/(1+n)，Δ=n−n'。令

§[
J=§frac{(a-a')§Delta}{(1+n)(1+n')}
-§frac a{n(1+n)}-§frac{a'}{n'(1+n')},\qquad
H=§frac{§Delta^2}{(1+n)(1+n')}.
§]

直接展开协方差给

§[
C_x-D_x=-§operatorname{Cov}(a,f(n))
-§mathbb E§frac a{n(1+n)}
=§frac12§mathbb EJ,\qquad
V_x=§frac12§mathbb EH.
§]

证明每个合法状态对J≤3H/8即可。a=a'时J≤0；交换样本不改J、H，故剩余只需a=1,a'=0，此时n≥1。

* Δ≤0时J<0。
* Δ=1时直接相消J=0。
* 整数Δ≥2时，

§[
§frac JH=§frac1§Delta-§frac{1+n'}{n§Delta^2}
=§frac{(§Delta-1)(1+1/n)}{§Delta^2}
§le§frac{§Delta^2-1}{§Delta^3}§le§frac38.
§]

第一不等式用n≥Δ；最后用
3Δ³−8Δ²+8=(Δ−2)(3Δ²−2Δ−4)≥0。
所有零分母情况已由a=0约定处理，Δ=0不需除H。先取期望，再对有限客户求和得(1)，不需要任何SPE激励或数值扫描。

独审另用K(a,n;n')=a/(1+n')−a/n，直接有J=K(a,n;n')+K(a',n';n)。按n>n'排序，低负载项K(a',n';n)≤0，高项至多(Δ−1)/[n(1+n')]；除H得到同一(Δ−1)(n+1)/(nΔ²)。因此只需0≤a≤1及n=0⇒a=0，公式也可作辅助实a的代数扩展，n仍必须整数。这不改变原单位玩家/单位客户模型。

## 对角严格余项

令p_{x,k}=Pr[n_x=k]、r_{x,k}=E[a_x1_{n_x=k}]。n=n'=k>0的逐对J精确为−(a+a')/[k(k+1)]，它的V贡献0。保留这些对角贡献，而非丢作≤0，得到

§[
§boxed{C-D§le§frac38V-
§sum_x§sum_{k=1}^m§frac{p_{x,k}r_{x,k}}{k(k+1)}.}
§tag{2}
§]

因为半个对角期望正好−p_k r_k/[k(k+1)]。这个更强式来自已实际读到的独审补充，不追改原3869B文本的历史范围，也不额外done独审源。负余项还不是可付给SPE的福利，调用时须保同一联合分布和其a/n意义。

## 最优常数的合法主题实现

一名客户x、合法A={x}与B=空主题，m=2。以概率ε取完整(A,A)、指定一个A为源；以1−ε取(B,B)、指定B为源，0<ε<1。m>2可用B补足槽。两状态(a,n)=(1,2)/(0,0)满足输入，但没有声称来自完整SPE。

§[
D=§varepsilon/2,\qquad
C=§varepsilon-(2/3)§varepsilon^2,\qquad
V=(4/3)§varepsilon(1-§varepsilon),
§]
§[
§frac{C-D}{V}
=§frac{3-4§varepsilon}{8(1-§varepsilon)}
=§frac38-§frac§varepsilon{8(1-§varepsilon)}
§longrightarrow§frac38.
§]

故任何更小统一常数都会被足够小ε否定。原界是极限锐，不是一个非退化分布必取等；对角项在此为ε²/6，强化式(2)恰取等。这个合法但非SPE的列分布不反驳half，也不认证真实Q_p能实现同样极限。

整数条件承重：若错误地允许实n，改两点高负载为sqrt(3)，仍a=1≤n，极限比为2/(3sqrt(3))>3/8（等价256>243）。这只否定直接迁移到实质量尾部；不是原整数模型反例。没有删n=0约定或用连续最大值掩盖整数差Δ≥2。

## 平均真实菜单接入及仍欠的支付

在[平均实际菜单接口](@P0)中，先均匀选实际位置i、再选A~p，执行完整Z_i(A)，指定i槽为源；各样本a≤n，故对每个p都合法应用本引理。D=(1/m)Σ_iE_p d_i(A)，C=p^TKbar p，V=V_{Q_p}。引理不用SPE；SPE仅另给D≤W/m及真实当前slack。

p若是平均矩阵的对称META-Nash，静态预算还给OPT≤2mC−V−S_O。因此仅能推出

§[
§operatorname{OPT}_m§le
2W+(3m/4-1)V-S_O
§]

（保IC slack和对角项还可更强），不能一般消掉m≥2时的正V系数。PAY要求同一分布的联合后继债务由V、最优税及实际slack共同支付；一个3/8代数常数没有提供这种跨历史关系。原源/独审的“没有新half/没有外审”范围保持，有限程序/扫描本批运行0次，正式图留第三阶段。
""")
write(2,'customer-attraction/first-saturation-review-layers-common-payment-boundary','resource','资料','首次饱和前沿的审查层次与共同付款边界','reviewed-flow-and-cut-identities; frontier-payment-open; later-laws-separated',
'完整实读8916B阶段审查与11507B当前主稿，核SOURCE-NET、整行接纳、HIT、随机cut、COV-STOP及两种law的不同归一；主稿已吸收全客户r定义修正，旧审查不自动覆盖后续质量law/owner槽lottery，也未付half前沿。',
['f8b0639179fa0be8698a','37817148989a4881cf37'],
r"""# 首次饱和前沿的审查层次与共同付款边界

## 两份真实文本及版本次序

主源[8916B独立审查](@f8b0639179fa0be8698a)明确有两个阶段：先只见摘要独立重构，后读主文及SOURCE-NET/HIT引用，核具体定义。该记录不声称盲证全部maxflow资产，也没有读取作者程序或用有限实验作证明。

本批另实际读[11507B当前冻结主稿](@37817148989a4881cf37)全文，并完整比较现[SOURCE-NET](@CTXarchives/customer-attraction/state/定理/实际取消的同时源付款与入流余额--定理.md)、[等份HIT](@CTXarchives/customer-attraction/state/定理/递增等份捕获的角色命中与残源协方差界--定理.md)。原审查§2.6要求把r定义扩到全体x∈a；当前主稿§1已经明确r=1/c完整原终局，仅R客户简化为1/(1+更深人数)。所以这是已吸收的历史定义意见，不再声称当前仍缺此定义或给重复补丁。

当前主稿还含§6质量抽样、§7 owner槽lottery和§8未采用税势。原审查的通过范围主要是§§1–4及§5 COV-STOP，不能将其“未发现异议”自动扩到后加章节。本页对后加代数分别解释，不把它登记为当时已经独审，也不因主稿旧页首“未获独审”就忽略现有8916B记录。

## 原模型、同一owner与SOURCE-NET钱包

单位客户、共同有限非空目录、m名单位玩家、同一完整有序历史纯SPE及实际叶Z。最优合法m槽T的并集O由互不交薄owner Q_i⊆T_i分割；actual覆盖C=I∪G，O=I∪R，故OPT−W=|R|−|G|≥0。

承接同一实际I/G取消流γ/f：

§[
0§le§gamma_x§le1\ (x§in R),\quad
§sum_x§gamma_x=|G|,\quad
§rho_x=1-§gamma_x,\quad
§eta_i=u_i(I)+§gamma_i,\quad §sum_i§eta_i=W.
§]

这里γ_i=Σ_{x∈Q_i∩R}γ_x，u_i(I)、u_i(G)分别是同一actual叶给角色i的I、G份额。实际I角色运输f满足γ_i+out_f(i)−in_f(i)=u_i(G)、in_f(i)≤u_i(I)；Σ_i u_i(I)=|I|使Ση_i=|I|+|G|=W。存在量来自最优元组合法替换/Hall；不得在未来query处重选一份γ或重新领G容量。预送δ_i=min(u_i(G),|Q_i∩R|)可在同一Hall网络同时扩充。每owner只用其一个原合法source主题T_i：源吸收A_i^src≤D_i(T_i)，费用K_i^src=u_i A_i^src/D_i≤u_i。若u_i(G)≤|Q_i∩R|，γ_i≥u_i(G)使η_i≥u_i；反之owner的R全部取消，源费用0。所以同一构造同时K_i^src≤η_i。D0时源吸收亦0，费用置0。这是已证source预付，不是incoming已付。

状态(i,a,x)只查原actual前缀强制a后的真实完整叶Z_i(a)，query完整利润D_i(a)，对全部x∈a定义r_{ia}(x)=1/c_x(Z_i(a))。x∈R时actual前缀零，当前query加更深coverer共c个，吸收1/c、向每个更深coverer各送1/c，合计1；role严格增加，末端全吸收。被捕获后是重置到actual-prefix新query，不能沿用旧离轨前缀收入。

## 统一整行接纳与零分母

按role i递增处理，source全部进入、费用K_i^src先预留。当前captured到达量q_{ia}(x)的完整原需求为

§[
F_i=u_i§sum_a
§frac{§sum_{x§in R§cap a}q_{ia}(x)r_{ia}(x)}{D_i(a)},\qquad
e_i=§eta_i-K_i^{src}§ge0.
§]

若F_i=0置θ_i=1；否则θ_i=min(1,e_i/F_i)。同一θ_i作用于该role所有incoming状态，拒绝部分第一次就停止，不再分流；source不减。最终每条完整IC唯一系数为

§[
w_{ia}=§frac{A_{ia}^{src}+§theta_iA_{ia}^{in}}{D_i(a)},\qquad
K_i=K_i^{src}+§theta_iF_i§le§eta_i.
§]

F_i由更早已处理流确定，没有循环自定义；不能每状态各花一次η_i−K_i^src。正R流状态必含该客户，D_i(a)≥1/m>0。若u_i=0，原SPE迫使全部D_i(a)=0，故无正R流，零约定合法。

令J={i:θ_i<1}，这些role恰K_i=η_i。同(i,a)先合并source/incoming及全部客户吸收再取A/D，不按客户重加权整条IC，也不因多个分支合流重复钱包。

## 守恒、首次命中及与half的准确等价

记Aabs为全部接纳query吸收、B_i首次拒绝质量、Bstop=ΣB_i。由有限严格future分流，

§[
Aabs+Bstop=§sum_x§rho_x=|R|-|G|=§operatorname{OPT}_m-W.
§]

SPE给每条A_s=w_sD_s≤w_su_i，求和Aabs≤K=ΣK_i≤W。令E=K−Aabs≥0、U=W−K≥0，则

§[
§boxed{Bstop-E-U=§operatorname{OPT}_m-2W.}
§tag{FRONTIER}
§]

所以对这份有效共同构造，Bstop≤E+U恰等价half；它是待证明的原目标余额，不是已付incoming的新一般不等式。J空时Bstop0是立即闭合的结构特例；J非空时没有付款证明。

去掉全部接纳抛币，得到同一raw等份capture链。停止只可在source之后的J，故对源s(x)

§[
B_x§le§rho_x§frac{k_x}{k_x+1},\qquad
k_x=|J§cap§{s(x)+1,§ldots,m§}|.
§tag{STOP-HIT}
§]

完整流算完后J是固定role集，HIT允许代入，不是对随机粒子事后选J。逆归纳中，当前未来t个目标、n个非目标，命中至多[t+n k/(k+1)]/(1+t+n)≤k/(k+1)，差为(k−t)/[(k+1)(1+t+n)]。source自身即便在J仍无条件接纳，不计入k。单非source行总到达≤ρ_x/2，但多行是一份首次命中概率，不能累加多个ρ/2钱包。

## 一个合法随机hybrid cut，不是已付前沿

任取固定J及各i∈J合法主题law p_i；独立抽a_i，保留其它薄Q_i。扩保留Q_i为合法T_i后是合法m槽，覆盖≤OPT。owner不在J的O客户必保留，owner在J时恰在全部query漏掉x才丢，O外新增恰在至少一个query覆盖时出现，因此

§[
§sum_{x§notin O}§left[1-§prod_{i§in J}(1-p_i(x))§right]
§le§sum_{x§in O:o(x)§in J}§prod_{i§in J}(1-p_i(x)).
§tag{RANDOM-CUT}
§]

任意联合law时把乘积换成联合未覆盖事件即可；该cut不用SPE、不对非法薄Q_i调用IC，保重复主题、空owner、零客户、J空。承重缺口仍是同一law如何把其库存漏失/覆盖量与原停止质量Bstop、whole-IC费用相接。

## 财务law与COV-STOP：完整r定义为何必要

拒绝incoming b_{ia}(x)=(1−θ_i)q_{ia}(x)，令

§[
A_{ia}^{stop}=§sum_{x§in R§cap a}b_{ia}(x)r_{ia}(x),\quad
§lambda_{ia}=A_{ia}^{stop}/D_i(a),\quad
L_i=§sum_a§lambda_{ia}.
§]

i∈J时F_i>0、u_i>0及某正吸收被拒，故L_i>0，可取p_i^fin(a)=λ_{ia}/L_i。R外b取0，对全部x∈a写χ_{ia}(x)=(b_{ia}(x)−λ_{ia})r_{ia}(x)，则

§[
§sum_x§chi=Astop-§lambda D=0,\qquad
§sum_{x§in R}§chi=§lambda D_i^{N§setminus R}(a)§ge0.
§tag{COV-STOP}
§]

非R客户的r必须用完整负载，不能误用R才成立的1/(1+更深人数)；否则第一等式会漏过去覆盖者。当前主稿已正确给全客户定义。

p_i^fin(x)=Σ_{a∋x}λ_{ia}/L_i，而真实停止B_i(x)=Σ_ab_{ia}(x)。带r的聚合恒等不推出无权逐客户B_i(x)≤L_ip_i^fin(x)。改用max_xb作IC系数可强制支配，却丢掉非R收益分母的稀释、可能超η；不能同时领取两种归一化好处。

## 旧审查之外的主稿补充

主稿§6取每action总停止质量b_{ia}=Σ_xb_{ia}(x)，B_i=Σ_ab_{ia}，对正B_i定义p_i^mass(a)=b_{ia}/B_i。按质量抽一个停止粒子、取其query，逐客户

§[
p_i^{mass}(x)§ge B_i(x)/B_i,\qquad
§Pr(x§text{全被遗漏})§le
§prod_{i:B_i>0}[1-B_i(x)/B_i].
§tag{MASS}
§]

这是合法覆盖耦合，可直接喂RANDOM-CUT，但归一量是B_i不是L_i。与财务law的精确转换为

§[
p_i^{mass}(a)=§lambda_{ia}v_{ia}/B_i,\qquad
v_{ia}=b_{ia}D_i(a)/A_{ia}^{stop}.
§]

正b使Astop>0；零项置0。改变整体IC系数后的费用未获原η界，不能保覆盖优势却仍按旧λ算钱。上述代数本次逐式核过，未将它称为stored review当时的通过范围。

主稿§7还允许真实付款role i与被替换的OPT owner槽s不同。非负z_{s,i,a}若每s有Σ_{i,a}z≤1，就是每owner槽至多一个合法query的lottery，余概率留T_s/薄Q_s；各槽可联合耦合。同一真实role的不同query能放进不同比较槽，IC依旧按其真实role收费，不假设玩家同时执行多行动。

按源标签拆分停止吸收λ_{s,i,a}=A_{s,i,a}^{stop}/D_i(a)，有Σ_sλ_{s,i,a}=λ_{ia}。若能使每owner Σ_{i,a}λ_{s,i,a}≤1，则z=λ兼容lottery和财务系数，免PRICE-CONVERT债；这一条件尚未证明，即使合法lottery也仍要付FRONTIER。改owner配对时γ/f、η及已取消库存必须同步，不能保旧SOURCE-NET而免费重置owner。

§8的缩尾税g_{b,λ}(c)=1/(b+c)−λ/(b+λc)在相同客户的真实连续前缀增长时可讨论库存；本流对R每次重置actual前缀，前缀负载始终0，不具有那种进度。原稿据此未采用该方向，非证明任何税方法一般不可能。

## 本批结论与证据级别

原审查先抽象重构时的五个待核点，已由实际原定义分别落到：整行F合并、F0置θ1、有限守恒无逃逸、whole-IC给Aabs≤K、真实OPT差及严格source后目标HIT。它的r定义意见在当前冻结主稿已修，不能继续标当前bug。主稿更新的mass/ownerlottery合法性及付款缺口另按上文保留。

没有证明Bstop≤E+U，也没有从HIT和RANDOM-CUT各自正确推出共同耦合。与[平均META付款](@P0)的查询law、方差及最优税是不同接口；此处FRONTIER恰等价half，META的PAY仅是更强充分条件，不能偷换两者量词。source/routing/取消都必须同一套。

四原主源和三个相关全文无程序，本批原CLI/有限实验运行0次；内部审查、清洗解析检查和外审分开。相关原件仅比较、无额外done；正式超图由第三阶段逐边建立，不复制旧图或强制连通。
""")
dump(E/'formal-resource-manifest.json',[dict(path=p,bytes=(S/p).stat().st_size,sha256=sha((S/p).read_bytes())) for p in paths])
notes={
'5d12b9ba337060130d26':('1190B路由全文，最优税/META/3/8/支付断点与已避路线、旧任务身份全部读；不把旧指令作本轮操作。','与同目录三文、独审3966B/当前主稿及现银行NQ反例比较；README三八独审待办为较早路由，已见后续原审稿，不再声称现在无审。',0),
'c0ca00d7195e1370c7d7':('5801B全部COV/CAP/META/MCAP/PAY/COL/REG/SRC/INT推导实读，完整m槽/三个边际/IC slack与真实联合后继身份逐式重构。','核V为旧D22 mGamma；明确Y排除当前A才与δ分母一致，既有银行COL已核；后续3/8系数改进不付TREE-PAY，root NQ已否定不自动否定平均菜单候选。',0),
'f8b0639179fa0be8698a':('8916B先摘要/后正文两个审查阶段全文，五抽象待查点与SOURCE-NET、统一接纳、守恒、A<=K、HIT、随机cut及COV-STOP每步实读。','11507B当前主稿及现SOURCE-NET/HIT全文比较，r全客户定义已修；stored review不涵盖后加mass law/ownerlottery，另保其归一债及开放付款；未盲称重证全部旧maxflow。',2),
'0f6deaf27382917e1003':('3869B完整成对证明、整数Δ分类/因式、合法AA/空主题锐族、固定m>=2/非SPE边界与META系数不足全文读。','3966B独审真实全文读，保K对证明等价、辅助实a扩展、对角严格余项和实n=sqrt3越界；非外审/新半覆盖/未跑有限扫描。',1)}
receipts=[]
for d in primary:
 rn,cn,i=notes[d['id']]
 receipts.append(dict(id=d['id'],full_file_reviewed=True,related_material_checked=True,unique_content_accounted_for=True,read_note=rn+' 4源19776B/307行总范围及两refs同字节/size/SHA256/blobSHA1已核；actual13原回执交集4与owner吻合。',comparison_note=cn,decision_note='独有数学/历史审查/条件与开放义务完整归入自足对象及原件；不把静态代数或内部审查当一般SPE付款，不额外done三个相关源，不sharedGit/clean show/网络或图导入。',disposition='integrated',targets=[paths[i]]))
dump(W/'semantic-receipts.json',receipts)
units=[
('COV','Per-customer h+E[n/(1+n)]=1; optimal multiplicity and O-outside taxes exact.'),
('mGamma','V is old empty-background r=m dispersion; independent full-slot marginal not same-column insertion.'),
('META','Continuous gain fixed-point proof gives support-best-response, no value/payment bound or algorithm.'),
('three-marginals','pO, full-slot qQ, and designated source p kept distinct.'),
('PAY','Same p/O gives sufficient condition only; REG equivalent to PAY, not to half.'),
('successor-Y','Y excludes current A; extra slot and overlap tax derived, one-player notation check included.'),
('variance','Binary source, integer n, pair J/H, sharp legal non-SPE family and real n counter-boundary.'),
('diagonal','Diagonal pairs give -sum p_k r_k/[k(k+1)], from actual read independent note.'),
('SOURCE-NET','Same owner/gamma/f source prepayment, not duplicated actual wallets.'),
('whole-row','One theta for whole role, D0/F0 handling, finite increasing flow and one IC coefficient.'),
('FRONTIER','Stopped mass conservation and E/U definitions give exact OPT-2W balance, not new paid inequality.'),
('HIT','Source role excluded from targets; first/ever hit bound not sum of per-role halves.'),
('RANDOM-CUT','Thin owners expanded to legal OPT topics; independent products or joint miss events; no IC for illegal Q.'),
('COV-STOP','All-client full r already in current source; weighted aggregate not unweighted client domination.'),
('laws','Financial lambda/L, mass b/B, and owner-slot lottery have distinct fee/coupling requirements.'),
('versions','README/stored reviews/source updates kept at actual scope; no repeated r fix or automatic review extension.')]
dump(E/'analytic-obligations.json',[dict(unit=u,reviewed=True,reason=t,method='complete analytic reconstruction, no original CLI or finite scan') for u,t in units])
(W/'relation-review.md').write_text("""# 第二阶段关系判断

COV把既有mGamma与最优并集重复/外覆盖税合账，是所有合法完整列的静态恒等式；META仅用标准Brouwer固定点使平均Kbar的所有行价格封顶，值的TREE-PAY仍未付。root银行反例否定的NQ/Mfull不同，不向新平均候选乱移反驳。

3/8为同一Q指定源的整数代数强化；独审的对角负余项与实负载越界完整保存。非SPE锐族只证明代数最优常数，不证明原SPE子类锐性或一般half。

first-saturation review是阶段性内部审查，当前主文已吸收全客户r定义修正；后加mass/ownerlottery另核并保费用缺口。SOURCE-NET/HIT/CUT正确不合起来自动付款。FRONTIER是half等价余额，META PAY是充分系统，不混作相同定理。

三个相关原文只比较无额外done，原路线/日期/角色和待审标签为历史对象，不执行其命令。当前四主源已实际pushed认领后才写receipt，原13capture完整保留。正文关系已解释，正式超图留第三阶段，无旧图导入/强制连通或mapper。
""")
inventory={x['id']:x for x in map(json.loads,(R/'cleanup/inventory.jsonl').read_text().splitlines())}
wanted=['37817148989a4881cf37','9782838c9e2bbf41d23b','37b0cc25eda54afa70b8','a11c622290a703a0f463','3d12877308be29ef502c']
cand=[]
for sid in wanted:
 d=inventory[sid];pr=R/'cleanup/progress'/f'{sid}.json'
 cand.append(dict(id=sid,path=d['path'],bytes=d['size'],sha256=d['sha256'],local_progress_exists=pr.exists(),scope='candidate only; first3 were full related reads, no primary receipt/done; last2 metadata only',eligibility='root must verify authoritative owner and actual claim before primary completion'))
dump(W/'next-candidates.json',cand)
(W/'delivery.md').write_text("""# DD4交付

原13claim全文和本地供给manifest完整保留；只做learning_dd真实交集4且ownerBoss4。四文19776B/307行全文预读经明确授权，receipt在实际pushed/synced后才写。三个必要只读比较22863B、三现正式对象25736B全文实读，三自足正式对象和4receipt待Root先推正文再done。

原CLI/有限扫描/新SPE策略执行0；本代理Git读写、helper执行、clean show、网络/懒加载全0。Root纯本地提供比较文件，逐size/SHA256/blobSHA1核后复制，不另领或done它们。

META Y明确仅后继，不把当前A再算进尾部；当前first-saturation已修r定义不重复提补丁；对角余项与sqrt3边界来自实际读到的独审，状态/版本各自保清。候选付款不伪装half进展。

copy-files.json只列本批三个新canonical与E/W，根transport文件不自列。冻结原文/已有页未修改，第三阶段无图/mapper操作。
""")
print(json.dumps(dict(formal=[dict(path=p,bytes=(S/p).stat().st_size) for p in paths],receipts=4,original_runs=0),ensure_ascii=False))
