from pathlib import Path
import json, hashlib, shutil

ROOT=Path('/workspace/scratch/37f0f9248cfc')
REPO=ROOT/'boss4-research'
CACHE=ROOT/'boss4-next-cache'
STAGE=CACHE/'r3-first-saturation-and-insertion-credit-primary'
E=Path('tools/evidence/first-saturation-and-insertion-credit-primary')
W=Path('cleanup/workspaces/Boss4/r3-first-saturation-and-insertion-credit-primary-next')
IDS=['37817148989a4881cf37','9782838c9e2bbf41d23b','37b0cc25eda54afa70b8','a11c622290a703a0f463','3d12877308be29ef502c']
CLAIM=ROOT/'boss4-r3-next-dm-claim.json'
claim=json.loads(CLAIM.read_text())
assert claim['status']=='pushed' and claim['actor']=='Boss4'
assert claim['local_sync']['status']=='synced' and set(claim['ids'])==set(IDS)
inv={d['id']:d for d in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b): return hashlib.sha256(b).hexdigest()
def put(p,s):
    p=STAGE/p;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(s,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def copy(p,q):
    q=STAGE/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
owners={}
for i in IDS:
    d=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text())
    assert d['owner']=='Boss4' and d['disposition']=='in-progress' and d['source_sha256']==inv[i]['sha256']
    owners[i]=d
copy(CLAIM,E/'actual-claim-receipt.json')
js(E/'primary-ownership-snapshot.json',owners)
allrows=[]
for folder,role in [('learning-dm-local-inputs','original'),('learning-dm-related-local-inputs','related'),('learning-dm-security-definition-inputs','related')]:
    mp=CACHE/folder/'local-export-manifest.json';m=json.loads(mp.read_text());assert not m['missing']
    copy(mp,E/f'{folder}-manifest.json')
    for r in m['rows']:
        b=Path(r['local_path']).read_bytes();d=inv[r['id']]
        assert len(b)==d['size']==r['size'] and sha(b)==d['sha256']==r['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==d['blob']==r['blob']
        dst=E/role/r['id']/r['path'];copy(r['local_path'],dst)
        allrows.append({**r,'role':role,'preserved_path':str(dst),'lines':len(b.splitlines())})
assert {r['id'] for r in allrows if r['role']=='original'}==set(IDS)
js(E/'source-manifest.json',[r for r in allrows if r['role']=='original'])
js(E/'related-source-manifest.json',[r for r in allrows if r['role']=='related'])
copy(CACHE/'learning-dm-preread-analysis.json',E/'actual-preread-comparison.json')
copy(CACHE/'local_blob_export.py',E/'authorized-local-export-helper.py.txt')

CONTEXTS=[
'archives/customer-attraction/state/候选/最优并集税与平均真实菜单的付款接口--候选.md',
'archives/customer-attraction/state/引理/整数完整负载的三八源去相关界--引理.md',
'archives/customer-attraction/state/资料/首次饱和前沿的审查层次与共同付款边界--资料.md',
'archives/customer-attraction/state/反例/笛卡尔银行目录的逐人分数门槛反族--反例.md',
'archives/customer-attraction/state/反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md',
'archives/customer-attraction/state/引理/笛卡尔目录的最优查询缺陷与三倍根修复--引理.md',
'archives/customer-attraction/state/定理/两名剩余三比较任意背景半覆盖--定理.md',
'archives/customer-attraction/state/问题/自由extra-one与iid安全值边界--问题.md',
'archives/customer-attraction/state/定义/自由分数背景安全门槛--定义.md',
'archives/customer-attraction/state/反例/成员平稳但根收益不可交换的三人见证--反例.md',
'archives/customer-attraction/state/反例/唯一根成员平稳核的弱封顶失败--反例.md',
'archives/customer-attraction/state/反例/根回复成员平稳核封顶--反例.md',
]
contexts=[]
for n in CONTEXTS:
    b=(REPO/n).read_bytes();copy(REPO/n,E/'context'/n)
    contexts.append({'path':n,'bytes':len(b),'sha256':sha(b),'snapshot':str(E/'context'/n),'scope':'full actual formal context read; no additional primary done'})
js(E/'context-manifest.json',contexts)
DD=CACHE/'r3-optimal-union-menu-and-source-covariance-primary'
reuse=[]
for i in IDS[:3]:
    n=inv[i]['path'];old=DD/'tools/evidence/optimal-union-menu-and-source-covariance-primary/related'/i/n
    new=STAGE/E/'original'/i/n
    assert old.read_bytes()==new.read_bytes()
    reuse.append({'id':i,'sha256':inv[i]['sha256'],'old_full_read_role':'DD related-only; never counted as previous primary completion','old_path':str(old),'new_path':str(E/'original'/i/n),'byte_identical':True,'read_reuse':'complete prior full reading and comparison reused; present source passages also checked; no fictitious independent reread/run'})
js(E/'prior-full-read-reuse.json',reuse)
def link(i,role='original'):
    return '../../../../'+str(E/role/i/inv[i]['path'])
def header(id,kind,typ,title,status,summary,ids):
    x=['---',f'id: "customer-attraction/{id}"',f'kind: "{kind}"',f'type_tag: "{typ}"',f'title: "{title}"',f'status: "{status}"',f'summary: "{summary}"','source_refs:']
    for i in ids:
        for s in inv[i]['sources']:
            x.append(f'  - "source:{s["commit"]}:{s["path"]}"')
    return '\n'.join(x)+'\n---\n\n'

P1=Path('archives/customer-attraction/state/引理/完整槽插入税与跨角色价格恒等式--引理.md')
body1=r'''# 完整槽插入税与跨角色价格恒等式

## 对象、来源和结论级别

主源是[7390B完整原文](SOURCE_D22)，两个冻结分支字节相同。本页保留其一般背景、所有完整槽、同列与独立重抽、全角色和根/后继两种总账、平稳核及跨深度断点；不以此前作为DD相关材料已读，冒充它此前已完成primary处置。来源自称独立机制接续，是2026-10-23的研究身份；本页没有外审或新颖性结论。

单位客户、有限非空共同主题目录，允许空主题、重复标签和零客户。固定一个合法有序过去，客户负载为非负整数b_x；还剩r≥1个真实槽。Q是有限概率分布，每列Z均含恰r个合法主题。以下静态代数不要求Q来自SPE，不能因使用“真实槽”就假设其列有激励兼容性。记n_x=c_x(Z)，n'_x为独立同分布副本，

\[
w_x=\mathbb E_Q\frac1{b_x+1+n_x},\qquad
v_Q(T)=\sum_{x\in T}w_x.
\]

分母的1属于一个独立额外查询。定义q_Q为先抽完整列、再从r槽均匀抽一个主题所得的**主题边际**，然后独立于竞争列重抽查询。因此

\[
v_Q(q_Q)=\frac1r\sum_x\mathbb E n_x\,
\mathbb E\frac1{b_x+1+n_x}.
\]

这不同于在同一列上抽槽后直接算价。当前原模型用全部有序历史纯SPE及任意平局；本页末段调用真实策略时保留这一完整身份，不把负载相同当成历史可合并。

## 插入税、负载分散和精确恒等式

原r名玩家的平均收益、同列插入税与负载分散分别为

\[
\bar U_Q=\frac1r\mathbb E\sum_x\frac{n_x}{b_x+n_x},\qquad
T_Q=\frac1r\mathbb E\sum_x
\frac{n_x}{(b_x+n_x)(b_x+1+n_x)},
\]
\[
\Gamma_Q=\frac1{2r}\sum_x\mathbb E
\frac{(n_x-n'_x)^2}{(b_x+1+n_x)(b_x+1+n'_x)}\ge0.
\]

n_x=0的两处项均定义为0；即使b_x=0也不产生0/0。有过去玩家时r Ubar只是剩余玩家总利润，不是全部覆盖福利，过去仍分享其覆盖的客户。

同一列内均匀抽槽再额外插入，其平均价恰为

\[
\frac1r\mathbb E\sum_x\frac{n_x}{b_x+1+n_x}
=\bar U_Q-T_Q.
\]

独立重抽竞争列的增量，逐客户用独立副本交换得

\[
\mathbb E n\,\mathbb E f(n)-\mathbb E[nf(n)]
=\frac12\mathbb E[(n-n')(f(n')-f(n))]
=\frac12\mathbb E\frac{(n-n')^2}{(b+1+n)(b+1+n')}.
\]

因此全输入准确成立

\[
\boxed{v_Q(q_Q)=\bar U_Q-T_Q+\Gamma_Q.}\tag{INS}
\]

Gamma=0当且仅当每一客户在Q的正概率支持中负载恒定；各槽的有序主题仍可不同。这是同一**完整r槽**背景上的恒等式，不通过删去当前槽得到r−1槽。

## 一个一般下界，不是价格封顶

n≥1时1/(b+n+1)≤1/(b+2)，故从同列价保留

\[
v_Q(q_Q)\ge\frac1r\sum_x\frac{b_x+1}{b_x+2}
\mathbb E\frac{n_x}{b_x+n_x}+\Gamma_Q
\ge\frac12\bar U_Q+\Gamma_Q.
\]

q_Q是合法主题分布，所以

\[
\boxed{\max_{A\in\mathcal S}v_Q(A)
\ge v_Q(q_Q)\ge\tfrac12\bar U_Q+\Gamma_Q.}\tag{LOW}
\]

空背景时r Ubar=E W，因子二下界完全不需要SPE。要证明某个根完整菜单存在价格上界M_full≤u，必须另构造一份便宜的Q；不能把LOW反读成它的上界。一般M_full的旧OPEN现已有[银行完整根菜单反例](../反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)，而本页静态恒等式保持成立。

## 全人数真实背景例：插入税并不由当前增量统一支付

主源引用的[6504B全人数重构](SOURCE_META)也实际完整读过，仅作本批相关来源、不额外done。它给每个m≥2、正整数L的一份完整SPE，而不只是任意大背景的形式例。目录只有不交主题A、B，大小分别mL、L。策略在全部有序历史规定：已经出现B则以后全选A；此前全A时，非末位选A，末位选B。

若历史已含h≥1次B，当前选A后A终数m−h，收益mL/(m−h)；选B后收益L/(h+1)，前者严格大。此前全A且不是末位时，选A得到mL/(m−1)>L，选B只得L；全A的末位两行动都得L，指定B合法。因此重复、离轨和平局全包含，得到完整SPE。实际覆盖W=OPT_m=(m+1)L，不是half反例。

固定实际前缀k次A，余r=m−k≥2。当前强制A或B的完整剩余列都含r−1个A和一个B；过去背景A负载k、B负载0。根真实收益

\[
d_A=\frac{mL}{m-1},\quad d_B=L,\quad u=d_A;
\qquad K=\begin{pmatrix}L&L\\L/2&L/2\end{pmatrix}.
\]

K列是当前强制A/B后的完整r槽，行是额外查询A/B，**保留当前槽**。唯一对称META-Nash为p=delta_A，C=p^TKp=L，D=d_A。完整槽/后继槽的主题边际分别为

\[
q_{full}=\frac{r-1}{r}A+\frac1rB,\qquad
q_{tail}=\frac{r-2}{r-1}A+\frac1{r-1}B,
\]
\[
v_Q(q_{full})=L\left(1-\frac1{2r}\right),\qquad
v_Q(q_{tail})=L\left(1-\frac1{2(r-1)}\right).
\]

所有列负载相同，Gamma=0。INS的另外两项精确为

\[
\bar U_Q=\frac{r-1}{r}\frac{mL}{m-1}+\frac Lr,
\qquad T_Q=\frac{(r-1)L}{r(m-1)}+\frac L{2r}.
\]

B槽插入税L/(2r)不会随实际过去k增大消失，但根真实收益增量D−C=L/(m−1)会消失。因此

\[
\frac{D-C}{C-v_Q(q_{full})}=\frac{2r}{m-1},\qquad
\frac{D-C}{C-v_Q(q_{tail})}=\frac{2(r-1)}{m-1}.\tag{RATIO}
\]

固定r、增大m的合法实际前缀使两比都趋0；不存在仅依赖固定r的正统一系数alpha，能在这类输入总令D−C≥alpha(C−v_Q(q_full))。若允许alpha依赖m,r，则全槽必要alpha≤2r/(m−1)，尾槽≤2(r−1)/(m−1)，不是充分性定理。特别alpha=1的旧2C≤D+v(q_tail)恰在m−1>2(r−1)失败，全槽对应m−1>2r；r=2即分别k≥2、k≥4。

这里最大完整查询恒为L<u；任意根行分布p的价格C≤L且D≥L，所以全p强推送、M_full以及half在**此族**都没有失败。失败的是要求当前增量支付整个槽边际插入亏损的特定桥。给任意Q和行分布p的一般剩余量只有

\[
C-v_Q(q_Q)=C-\bar U_Q+T_Q-\Gamma_Q,\qquad C=p^TKQ.
\]

代数不给C−Ubar符号。即使Q=p且p是K的对称Nash，只由v_Q(q_Q)≤C知道左边非负，也不推出D≥C。

## 同一列分布的全角色总账

对完整列中的角色j，定义

\[
D_j=\mathbb E\sum_{x\in Z_j}\frac1{b_x+n_x},\qquad
C_j=\sum_x\Pr(x\in Z_j)w_x.
\]

C_j把该角色主题按其**无条件边际**独立重抽，再查完整r槽；不是第j个实际子博弈可取得的续局收益。由sum_j Pr(x∈Z_j)=E n_x和INS直接得到

\[
\boxed{\sum_{j=1}^r(D_j-C_j)=r(T_Q-\Gamma_Q).}\tag{ROLE}
\]

此式可以同时核所有角色的总负债，不能把每个C_j重新认作其各自真实历史的IC右端。它没有控制根与其他角色之间如何分配总收益。

## 根/后继分离：另一协方差身份

现在固定原完整纯SPE，根源B按p随机强制，之后原策略确定。记a_x=1_B(x)，真实后继负载k_x**排除根B**，因此该列n_x=a_x+k_x。设

\[
v_x=\frac1{b_x+1+k_x},\quad
t_x=\frac{a_x}{(b_x+1+k_x)(b_x+2+k_x)},\quad p_x=\mathbb E a_x.
\]

独立完整列的额外查询价使用E(v_x−t_x)，真实根利润使用E(a_xv_x)，所以

\[
\boxed{D-C(p,p)=\sum_x\operatorname{Cov}(a_x,v_x)
+\sum_xp_x\mathbb E t_x.}\tag{ROOT}
\]

这不是把完整负载n直接代入v=1/(1+n)的旧SRC身份：ROOT先移走根自身，税项有p_x；[平均菜单](../候选/最优并集税与平均真实菜单的付款接口--候选.md)的完整源税是E[a_x/(n_x(1+n_x))]。两个精确坐标均可用，但不能只保一个“协方差”名称就交换其负载、税或抽样。

## 平稳主题边际不等于角色收益或META分布

定义source到随机完整槽的有限Markov核

\[
P^{full}_{BA}=\frac1r\#\{j:Z_j(B)=A\}.
\]

它总有平稳主题分布p：任取p_0，Cesaro平均q_N=N^{-1}sum_{k=0}^{N-1}p_0P^k在紧单纯形有收敛子列，且q_NP−q_N=(p_0P^N−p_0)/N趋0；极限即平稳。此为本页补全的有限存在性说明，不导入外部论文或算法复杂度。

r>1时，随机真实后继槽核P_tail满足

\[
P^{full}=\frac{I+(r-1)P^{tail}}r,
\]

所以二者平稳分布集合完全相同。r=1时P_full=I，尾核不存在，不使用除r−1的式子。平稳p使q_full=p，于是INS化成

\[
\boxed{D-C(p,p)=D-\bar U_p+T_p-\Gamma_p.}\tag{STAT}
\]

要由此支付stationary strong-push仍需真实SPE证明D−Ubar≥Gamma−T。平稳性没有该符号，也没有说这份p同时是矩阵K的对称Nash。不能把“存在平稳p”和“存在META p”拼为同一个分布。当前[36客户平稳收益见证](../反例/成员平稳但根收益不可交换的三人见证--反例.md)更具体给唯一平稳p下根收益10<34/3平均槽收益，说明单独D≥Ubar已失败；它没有直接决定带T/Gamma的STAT符号。其现存同SHA成功审计不重复运行，本页不将其报告冒称本次新证据。

## 已揭示历史之后不能直接望远镜

只有根源随机、之后完整纯策略确定时，任意非空真实有序历史已揭示其首行动B。给定该历史，后续以及根成员均确定，条件协方差与条件Gamma为0。但全协方差公式还保留

\[
\operatorname{Cov}(a,v)=
\mathbb E\operatorname{Cov}(a,v\mid H)
+\operatorname{Cov}(\mathbb E[a\mid H],\mathbb E[v\mid H]).
\]

第二项是不同根历史之间的相关性，并未因深层的第一项为0而消失。深层SPE只能比较各自已揭示历史下的真实行动和后继；将这些零条件量相加，不能领取跨根历史的新付款。

本页至此是精确代数、LOW下界、RATIO特定桥障碍和明确未付角色/跨历史义务。与[三八源界](../引理/整数完整负载的三八源去相关界--引理.md)接入时必须映射同一整数完整负载、同一指定源和同一分布；裸3/8系数不替代保负源税的完整INT。一般m/当前六人half、META共同付款、首次饱和B≤E+U都没有由这些恒等式闭合。本批无原数学程序、新策略复演或有限扫描运行。
'''
body1=body1.replace('SOURCE_D22',link('37b0cc25eda54afa70b8')).replace('SOURCE_META',link('ef21819792cb2a9aac5f','related'))
put(P1,header('complete-slot-insertion-tax-cross-role-price-identities','lemma','引理','完整槽插入税与跨角色价格恒等式','proved-static-identities-and-lower-bound; specified-current-increment-bridge-refuted; common-payment-open','一般整数过去与完整r槽的INS、角色总账、根后继税和平稳身份全部自足保留；真实全人数SPE给固定r当前增量无正统一付款系数。主题平稳不支付跨已揭示历史的相关性。',['37b0cc25eda54afa70b8'])+body1)

P2=Path('archives/customer-attraction/state/资料/首次饱和与独立审查的版本路由--资料.md')
body2=r'''# 首次饱和与独立审查的版本路由

## 五份原件及其实际去向

五份均2026-10-23工作材料，legacy/main分别同字节，原件未改。当前清洗只把其数学、用途、审查范围和状态准确归位，不执行其中旧角色或研究路线命令。

| 源及实际全文范围 | 有用内容去向 |
| --- | --- |
| [first_saturation_frontier，11507B](SOURCE_FRONT) | [完整首次饱和对象](../资料/首次饱和前沿的审查层次与共同付款边界--资料.md)已经保存全部八节、SOURCE-NET/HIT、随机cut、财务law、质量law和owner槽lottery。本批核同SHA后按该准确去向去重，不覆写或重立同义对象。 |
| [三八独审，3966B](SOURCE_REVIEW) | [完整整数三八引理](../引理/整数完整负载的三八源去相关界--引理.md)已吸收两个逐对恒等式、辅助实a扩展、固定m≥2锐族、实n反界及对角严格项。本批按该准确去向去重。 |
| [D22插入税，7390B](SOURCE_D22) | [完整槽插入税对象](../引理/完整槽插入税与跨角色价格恒等式--引理.md)补全此前DD仅局部使用的任意背景、角色总账、真实全人数诊断、平稳与跨深度内容。 |
| [tree_credit路由，1005B](SOURCE_TREE_README) | 本页保其源预付/重置/完整后继付款用途和旧审查状态，核心构造链接既有完整正文。 |
| [independent路由，925B](SOURCE_INDEP_README) | 本页保root-only候选、有限锥及独立三八审查的不同级别，并与当前反例/定理比较，不把旧OPEN重新认证为现状。 |

前三份曾在DD仅作related全读，没有因此成为primary done；本批实际认领后另保逐源处置。复用完整实读和同SHA证据不虚增独立阅读或运行次数。下面给两路由可接续的对象合同，而不把表格计数当数学完成。

## 首次饱和：同一钱包中的准确余额

原模型是有限单位客户、共同有限非空目录、m名单位玩家、任意完整有序历史纯SPE，保重复、空主题、零客户及离轨平局。固定一份actual Z、最优m元组与薄owner分配。真实取消γ、残源rho=1−γ及SOURCE-NET钱包eta必须固定同一份，sum eta=W，源费用K_src≤eta；captured重置不能另领一份源付款。

主稿对**全部query客户**用r_ia(x)=1/c_x(Z_i(a))，只在actual未覆盖的R客户上才简化为1/(1+更深coverer数)。统一整行theta_i接纳incoming、源流不缩减，whole-IC仅乘总吸收/完整查询利润；同一行多个action/客户不得各花一次剩余钱包。按角色严格增加的有限分流给

\[
A_{abs}+B_{stop}=OPT_m-W,\quad A_{abs}\le K\le W,
\quad E=K-A_{abs},\quad U=W-K,
\]
\[
\boxed{B_{stop}-E-U=OPT_m-2W.}
\]

所以B_stop≤E+U对这份有效共同构造恰是half付款义务，尚未证明。STOP-HIT只给客户先命中停止行的概率上界k/(k+1)，source行不拒绝；不能把多行各自rho/2累加，也不能由HIT单独宣称付款。

RANDOM-CUT每比较槽只放一个合法query，对保留的薄owner只用其可扩充到合法T_s，不对薄Q_s调用IC。财务law p_fin(a)=lambda_ia/L_i中lambda=A_stop/D与whole-IC一致；COV-STOP给带真实r的聚合抵消，不给逐客户B_i(x)≤L_ip_fin(x)。质量law p_mass(a)=b_ia/B_i给覆盖支配，却需显式转换

\[
p_i^{mass}(a)=\lambda_{ia}v_{ia}/B_i,\qquad
v_{ia}=b_{ia}D_i(a)/A_{ia}^{stop}.
\]

不能保其覆盖优势、同时继续按未转换的lambda领旧eta费用。owner槽与真实付款role可分离，但每owner的lottery行和≤1；按源标签拆lambda后这一行容量仍未证明，合法抽样本身也不付B_stop。改owner还要同步γ、运输和eta，不能重置已取消库存。

1005B路由的“未独立审查”只保其当时说法：DD已读8916B真实存储审查，现也核到它，不能再称现在取不到审查。反过来，stored review的实际重构/核对主要覆盖早期构造、HIT、cut与COV-STOP；当前主稿新增质量law和ownerlottery**没有因同一文件名而获得当时通过状态**。r的全客户定义意见已被当前主稿吸收，不发重复纠错。完整各式和零分母处理均见既有首次饱和对象。

## 三八审查与负源税：不同付款对象不互代

3966B独审原件自称只见陈述、未读原证明后独立重构；这是该历史审查的方式，本次已读双方后整理不能重新冒称盲证或外审。其输入是任意有限(a,n)，a∈{0,1}、n∈{0,…,m}、a≤n，0/0项按0，结论

\[
C=(\mathbb Ea)\mathbb E\frac1{1+n},\quad
D=\mathbb E\frac an,\quad
V=(\mathbb En)\mathbb E\frac1{1+n}-\mathbb E\frac n{1+n},
\]
\[
C-D\le\frac38V-\sum_{k=1}^m\frac{\Pr(n=k)\mathbb E[a\mathbf1_{n=k}]}{k(k+1)}.
\]

完整成对证明及合法AA/空主题极限族已在三八对象自足保留。a可辅助推广到[0,1]，但整数n承重；实n=sqrt(3)的两点极限超过3/8。m≥2的锐性属于合法联合负载代数类，不证明真实SPE子类也锐，更不等于cross-history付款。

既有平均菜单的旧完整INT另有负源税

\[
C-D\le V-T_{src},\qquad
T_{src}=\mathbb E\sum_x\frac{a_x}{n_x(1+n_x)}.
\]

裸3/8降低V系数但丢了负税，两条完整上界无逐点支配，宜同时保留。已交DD直接有理例a恒1、n各半2/3，C−D=−1/8、V=1/48、T_src=1/8；旧INT为−5/48，带对角1/16的三八上界为−7/128，旧INT反更低。此为合法非SPE列分布的代入，不是新程序或half反例。D22的T_Q是**全槽平均插入税**，也不能与指定源T_src不经映射互换。

## root-only：候选合同、精确表示与有限证据

925B independent路由引用的[4419B root-only检查点](SOURCE_ROOT_ONLY)也已完整读，仅作本批related。它允许根行动不理性，要求每个正深度子博弈完整纯SPE；根强制A后的真实根收益f_A、总覆盖W_A，M=max_A f_A，actual A0的根后悔Delta=M−f_A0。候选R?为

\[
OPT_m\le2W_{A0}+3(M-f_{A0}),
\]

要求每个合法actual根行动A0均成立等价于

\[
\min_A(2W_A-3f_A)+3\max_Af_A\ge OPT_m.
\]

这是同一菜单的精确重述，不是新付款。不同分支的min和max之间仍需合法真实偏离信用，不能通过混合后继免费保旧玩家收益。现有[三倍根修复对象](../引理/笛卡尔目录的最优查询缺陷与三倍根修复--引理.md)保存完整可信保险与缺陷同减3s；它支持root-only鲁棒接口的准确量词，不把所有同名fresh候选当原half本身。特别对任一已证half的人数m，取保险s=Delta修复成完整SPE，再用新半覆盖缺陷等于旧缺陷减3Delta，就给同人数的R?；Delta=0时原计划已是完整SPE。这里是现有修复与现有定理的条件接入，不把旧笼统OPEN覆盖到已有五人及更少的已证人数。

更强FREE-ROOT把Delta系数改为0：所有正深度理性、根任意的计划也要half。强制根空主题后，得到一个必要测试：r名真正尾部SPE的覆盖须至少OPT_(r+1)/2，比较元组多一槽。源给紧例：A含r名客户，另有r个与A及彼此不交的单客户主题，且目录有空主题；r名尾部在所有历史都选A，每人最终A收益≥1、单客户偏离≤1，故是完整SPE。根选空，W=r，而A加r个单客户主题给OPT_(r+1)=2r，恰取等。这是边界例，不是一般FREE-ROOT证明；其它根分支可各取完整逆向归纳续局，保正深度理性。原检查点还提出任意固定合法非空前缀、余r人完整SPE的更强背景式：包括过去在内的总覆盖W≥OPT_(r+1)/2；它不是剩余r人利润和的同名命题。

源中“FREE-ROOT仍OPEN”还要与当前确有的[两名剩余、三比较、任意整数背景定理](../定理/两名剩余三比较任意背景半覆盖--定理.md)分开：该定理已对实际固定过去、两名完整SPE尾部和任意三合法比较主题给O≤2W，不需要根理性；它没有解决一般r或当前六人归约。

原检查点还只报告一个三人六主题X/Y、43有序历史策略域、63兴趣型有限锥的最大比较值7/4。该程序/锥输入本批没有执行或另行认证；这里只保源作者的明确有限结论，不把有限锥当普遍证据、不扩成新的扫描结果。单实际列逐人query上界也有原AAAF终局前三人各9、未用B额外价10的失败；这只停止单列逐人cap，不能据它停止所有混合或静态背景。

## 整数extra-one旧OPEN的当前纠正

root-only检查点和[4830B共同静态分布尝试](SOURCE_AGG)说的v是查询独立的**整数合法对手混合**：

\[
v_{r+1}(b)=\min_{Q\in\Delta(\mathcal S^r)}
\max_T\mathbb E_Q\sum_{x\in T}\frac1{b_x+1+c_x(B)}.
\]

分数背景值t_(r+1)则把r个主题质量连续摊在目录边际上，不与v相等。两者仍有关键的单向关系：任取整数混合Q，其均值负载属于r conv{1_A}，倒数凸性逐查询给

\[
\mathbb E_Q\sum_{x\in T}\frac1{b_x+1+c_x(B)}
\ge\sum_{x\in T}\frac1{b_x+1+\mathbb E_Qc_x(B)}.
\]

先max_T再min_Q，即t_(r+1)(b)≤v_(r+1)(b)。此关系与当前[分数门槛定义](../定义/自由分数背景安全门槛--定义.md)、[extra-one边界](../问题/自由extra-one与iid安全值边界--问题.md)逐式核对；不是偷换两种值的身份。

[银行完整SPE反族](../反例/笛卡尔银行目录的逐人分数门槛反族--反例.md)对每m≥4，根u=m/(m−1)，自由extra值

\[
t_{m+1}(0)=\frac12+\frac{2(m-1)}{2m-1}
=\frac{6m-5}{4m-2},
\qquad t_{m+1}-u=\frac{2m^2-9m+5}{(4m-2)(m-1)}>0.
\]

m4时u=4/3<19/14=t5≤v5；一般m≥4包括恰六人也成立。因此旧“自由extra-one首位”和**整数F_r首位**OPEN均已过时，不能把它们继续列为当前待证一般桥。反族W=2m、OPT_m=3m−2，half保有余量，且原件给真正v_m≤2；它不否定聚合W≥m v_m或弱聚合W≥(m−1/2)v_m，也不决定一般FREE-ROOT。

共同静态分布尝试的合法步骤仍可保留：若孩子全背景聚合界已证，可对每孩子A选r−2槽查询独立Q_A，将固定A加回形成父r−1槽合法Q。真实孩子利润下界不能反向给这些价向量混合的低cap，也不能将f_A(A)替换成根真d_A；后者既复制根又换了对手。旧extra-one正规形作为条件归约可保存，但一般首位目标已被上述反族否定。该related尝试不在本批额外done。

## stationary构造、已知失败与仍欠的一份付款

security路由及[3963B指定分数stationary边界](SOURCE_STAT_FRAC)均实际全读。后者仅把真实尾成员核的某个平稳pi直接当作确定分数负载r pi，再要求全部纯查询cap≤根u；源给1274客户、三人六主题、唯一pi=(1,1,0,1,1,0)/4的一次严格分离。它报告查询2价123652/455=541/2+1149/910>根541/2；同例自由均匀分数背景及合法整数背景(0,5)均有更低cap。这里仅保该相关原文的有限计算断言；其audit源码/JSON不在本批已读输入或新运行，不称本次独立重核43历史。

它的固定均值背景与D22的完整随机列Q不同；[根成员静态cap](../反例/根回复成员平稳核封顶--反例.md)、[弱根核cap](../反例/唯一根成员平稳核的弱封顶失败--反例.md)又是r−1真实尾背景与实际W阈值的合同，不混成同一核/人数/收益。D22 STAT仍需其精确带税关系，不能从“根低于槽均值”或“指定cap失败”直接推出每个stationary quadratic bridge都败。反过来，平稳存在也未支付任何这一关系。

本批保留的接续对象是：首次饱和的一份共同运输/钱包及合法联合law、平均META的V/S/真实slack付款、整数静态聚合价格向量的跨真实子树支付。这些接口的存在量词、查询law和预算不同，不能互相自动替代。当前五人half已有独立定理，六人及一般人数目标不因本批整理而解决；旧工作区“不要某路线”等只存历史用途，不成为新cleaner命令。

本批完整原件5份24793B/488行，相关原件5份20908B。实际只调用安全本地导出helper三次读10个已在本地的blob；无网络、懒加载、shared Git写入、clean show、原数学CLI、新SPE复演或扫描。既有同SHA成功证据没有重复运行，未将其次数合进本批；清洗格式/绑定自查不是数学或外审认证。
'''
repl={'SOURCE_FRONT':link(IDS[0]),'SOURCE_REVIEW':link(IDS[1]),'SOURCE_D22':link(IDS[2]),'SOURCE_TREE_README':link(IDS[3]),'SOURCE_INDEP_README':link(IDS[4]),'SOURCE_ROOT_ONLY':link('43fcfd09b6d0ae5d96b5','related'),'SOURCE_AGG':link('62fadc53e30b4b1c856b','related'),'SOURCE_STAT_FRAC':link('c57e4ec366e7af1be467','related')}
for a,b in repl.items():body2=body2.replace(a,b)
put(P2,header('first-saturation-independent-review-version-routing','resource','资料','首次饱和与独立审查的版本路由','full-sources-disposed; historical-review-and-current-counterexamples-separated; common-payment-open','五源逐源去向与两旧README的独有用途自足保留；stored review不覆盖后加质量/ownerlottery，3/8不抹负源税，Jensen把银行分数失败正确转成整数extra-one失败，而不否定聚合与FREE-ROOT。',IDS)+body2)

js(E/'formal-resource-manifest.json',[{'path':str(p),'bytes':len((STAGE/p).read_bytes()),'sha256':sha((STAGE/p).read_bytes())} for p in [P1,P2]])
print(json.dumps({'stage':str(STAGE),'actual_ids':IDS,'primary_bytes':sum(r['size'] for r in allrows if r['role']=='original'),'new_formal_paths':[str(P1),str(P2)],'formal_bytes':sum(len((STAGE/p).read_bytes()) for p in [P1,P2]),'context_snapshots':len(contexts)},ensure_ascii=False))
