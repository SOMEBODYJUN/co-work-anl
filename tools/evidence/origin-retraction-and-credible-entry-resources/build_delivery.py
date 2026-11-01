from pathlib import Path
import json,hashlib,re,posixpath
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-origin-retraction-and-credible-entry-resources';E=Path('tools/evidence/origin-retraction-and-credible-entry-resources');W=Path('cleanup/workspaces/Boss4/r3-origin-retraction-and-credible-entry-resources-next')
IDS=['0a621854a7b1cf92152b','831a6eb4d326021afaff','8cb7709f690938a25376','ae9d75160e3a4fb57045','dc85ffdd3aba54e0e944']
PL='archives/customer-attraction/state/引理/真实偏离枝的收益与覆盖范围--引理.md';PO='archives/customer-attraction/state/障碍/重复惩罚的末位外选项与无背景移植--障碍.md';PR='archives/customer-attraction/state/资源/来源回撤与异质修复入口的全树付款边界--资源.md'
PA='archives/customer-attraction/state/算法/固定来源路由的最大回撤与价格分离--算法.md';PH='archives/customer-attraction/state/定理/真实退出缺陷的统一与异质前缀修复--定理.md';PX='archives/customer-attraction/state/引理/最优首动作菜单与真实孩子损失--引理.md';PY='archives/customer-attraction/state/引理/最优动作真实尾的菜单损失与重置差--引理.md';PPB='archives/customer-attraction/state/障碍/PB大背景的最后单例偏离--障碍.md';PT='archives/customer-attraction/state/候选/真实门槛任意路径的累计预算与不可拼合边界--候选.md';PB='archives/customer-attraction/state/反例/笛卡尔银行目录的逐人分数门槛反族--反例.md';PTAX='archives/customer-attraction/state/引理/实际末两人的查询税余量--引理.md';PBETA='archives/customer-attraction/state/引理/Beta克隆的单次增益与复用上尾债务--引理.md'
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
# Actual claim guard is intentionally before every final primary/receipt export.
claimpath=R/'boss4-r3-next-jn-claim.json';claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(IDS)<=set(claim['ids'])
mp=C/'learning-is-next-origin-entry-inputs/local-export-manifest.json';m=json.loads(mp.read_text());primary=[];owners=[]
for i in IDS:
 x=next(x for x in m['rows'] if x['id']==i);v=inv[i];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];owner=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert owner['owner']=='Boss4' and owner['disposition']=='in-progress' and owner['source_sha256']==v['sha256'];owners.append(owner);q=E/'original'/i/x['path'];cp(x['local_path'],q);primary.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'headings':[l for l in b.decode().splitlines() if l.startswith('#')],'read_mode':'actual firstfull text/math reading inJN preclaim authorizedpreparation afterISseal; actualclaim/owner/sourceSHA verified beforefinalreceipt; frozen oldroles notinstructions'})
assert sum(x['size'] for x in primary)==14067
js(E/'source-manifest.json',primary);cp(mp,E/'actual-primary-local-export-manifest.json');cp(claimpath,E/'actual-unprojected-claim-receipt.json');js(E/'actual-primary-ownership-snapshot.json',owners)
relatedmp=C/'learning-jn-related-proof-inputs/local-export-manifest.json';rm=json.loads(relatedmp.read_text());assert len(rm['rows'])==4 and rm['missing']==[];related=[]
for x in rm['rows']:
 v=inv[x['id']];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'];q=E/'related'/x['id']/x['path'];cp(x['local_path'],q);related.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'read_mode':'JN actual complete source MD read in2untruncated batches; notadditionalprimary or code/JSON audit'})
assert sum(x['size'] for x in related)==35623
js(E/'related-source-manifest.json',related);cp(relatedmp,E/'actual-related-local-export-manifest.json');cp(C/'local_blob_export.py',E/'authorized-local-export-helper.py.txt')
contexts=[]
for p in [PA,PH,PX,PY,PPB,PT,PB,PTAX,PBETA]:
 b=(REPO/p).read_bytes();q=E/'context'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_mode':'JN actual complete current formal text read; broad initialsearch outputtruncated nottreatedasfullread; targetedfullreads above complete'})
js(E/'context-manifest.json',contexts)
def front(id,kind,tag,title,status,summary,ids):
 t='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in [('id',id),('kind',kind),('type_tag',tag),('title',title),('status',status),('summary',summary)])+'source_refs:\n'
 for i in ids:
  for v in inv[i]['sources']:t+='  - '+json.dumps('source:'+v['commit']+':'+v['path'],ensure_ascii=False)+'\n'
 return t+'---\n\n# '+title+'\n\n'
bl=r'''## 同一完整策略的真实偏离枝

有限单位客户、有限非空共同目录，m≥1名单位提供者，固定每个完整有序历史都定义的纯SPE σ；空主题、重复和任意离轨平局允许。令K=max_(T∈S)|T|。取原actual位置i，其最终收益u_i>0。保持原actual过去，在i强制任一合法主题A，后面执行**同一原σ**，得到完整偏离终局z_i(A)。写k=|A|和强制者真实最终利润d_A。SPE给d_A≤u_i；k>0时d_A>0。

则
\[
\boxed{W(z_i(A))\le2k+(m-1)K-\frac{k^2}{d_A}
\le2k+(m-1)K-\frac{k^2}{u_i}.}\tag{EXT}
\]
特别对任一最大主题A，k=K，
\[
W(z_i(A))\le(m+1)K-K^2/u_i.\tag{MAX}
\]
这适用于每个actual位置，过去m−r名玩家不被删除。它是偏离枝整体覆盖的**上界**；没有得到actual根福利下界、所有枝共同OPT付款或新的half范围。

## 完整逐客户证明

设c_x是偏离终局的覆盖重数。其余m−1个主题的总incidence至多(m−1)K，其中在A内的incidence恰Σ_(x∈A)(c_x−1)。A外并集客户数至多余下incidence，因此
\[
\begin{aligned}
W(z_i(A))
&=k+|\bigcup z_i(A)\setminus A|\\
&\le k+(m-1)K-\sum_{x\in A}(c_x-1)\\
&=2k+(m-1)K-\sum_{x\in A}c_x.
\end{aligned}
\]
强制者利润d_A=Σ_A1/c_x。Cauchy给(Σ_Ac_x)d_A≥k²，代入得EXT第一步。d↦−k²/d在d>0递增，而d_A≤u_i，给第二步。没有冻结任何未来动作；未来全改也只占m−1个其他主题。没有比较过去玩家在两枝的收入，因此不偷删旧玩家返还。

若k=0，直接用Wbranch≤(m−1)K，不含0/0。若u_i=0，任一最大主题的强制收益至少K/m（每客户终局重数≤m）；SPE迫K=0，全部合法主题为空，所有枝覆盖0。零客户、m1和相同覆盖的不同标签都包含；m1时d_A=k，公式退为Wbranch≤k。

## 静态额外槽与势饱和：不同的未证接口

同源旁读还定义m个竞争主题B的纯静态查询
\[
q_B(T)=\sum_{x\in T}\frac1{1+c_x(B)},\qquad
\vartheta_{m+1}=\min_{B\in\mathcal S^m}\max_Tq_B(T).
\]
下标含额外查询者，真实游戏仍m人。逐客户计数已有OPT_m≤2mϑ_(m+1)；这不等于当前每人u_i≥ϑ_(m+1)，也不等于完整真实菜单Mfull。

固定t>0的自由入场势Φ_t(q)=Σ_xH_(c_x(q))−t|q|在全部有限目录多重集（含空）有最大元：覆盖客户数L有限，Φ≤LH_|q|−t|q|→−∞，每个大小只有有限多重集。最大元一槽插入得max_Tq_q(T)≤t，一槽删除得每个已占槽收入≥t。若其大小≤m，补主题到m只降查询，故ϑ_(m+1)≤t；逆否即ϑ_(m+1)>t时**每个全局最大元**大小>m。不能据此排所有小局部饱和点，更不能把最大元当给定σ的后继。改变早期行动可重置整尾，单槽势改进没有控制此变化。

原“逐人extra theta floor仍未证”须按当前[银行完整族](../反例/笛卡尔银行目录的逐人分数门槛反族--反例.md)纠正：m4、根u4/3，而自由分数静态竞争质量4的值δ5=19/14。纯整数竞争背景是分数背景的特例，故ϑ5≥δ5>u，逐人候选已假。这是现行完整反族的定义级推论，不新增游戏或运行。银行W8、OPT10，不能由逐人失败推出聚合W≥mϑ_(m+1)或half失败；本页没有证明或反驳该聚合候选。

原八旧证书的theta阴性诊断只是当时有理背景枚举，非这次全IC审计或任意策略锥证据。代码/表完整保在[旁读原件](../../../../tools/evidence/origin-retraction-and-credible-entry-resources/related-source-manifest.json)的9106B稿，本批未取得/读或执行其原py与八输入闭包。原m5代入6K−K²/u只说明本引理，不影响另已证五人half；六人/一般共同付款仍未从EXT获得。
'''
put(PL,front('customer-attraction/true-deviation-branch-payoff-and-coverage-extent','lemma','引理','真实偏离枝的收益与覆盖范围','proved-branch-upperbound; no-aggregate-payment; individual-extra-theta-floor-refuted-separately','同一完整σ的偏离枝由其他主题incidence与Cauchy得2k+(m−1)K−k²/u上界，保零/空及过去；静态势饱和不支付动态后继，旧逐人theta候选按银行更新。',[IDS[0],'f3f1ec02ccbbf002fe96'])+bl)
bo=r'''## 两个精确移植障碍，不是一般不可能性

共同目录单位客户、单位提供者、每个有序历史纯SPE，保空/重复/平局。下面只排指定经济机制的直接版本。异质修复会将合法路径的旧差额g=OPT−2W减少2R+D；这些尝试尚未给g>2R+D的输入，不构成half反例。先定义各自目录和后继，不把一种toy中的主题默认加入另一完整目录。

## 重复同一punisher的真实末位外选项

碰撞自由目标C₁,…,C_k,D中，C_i两两不交、各p，D独立、大小t，遗漏Q_i各q且在actual并集外。若合法A_i=C_i∪Q_i，actual末位D成为BR至少要求p/2+q≤t。只在C_i上共享一次而不覆盖Q_i的惩罚不能把偏离者压到p，除非q≤p/2；这是这套构造渐近3/2天花板的来源，非所有SPE的比值上界。

改用H_i=A_i∪E_i，E_i⊆D且|E_i|=b，actual末位BR更要求
\[
p/2+q+b\le t.\tag{L}
\]
假设偏离A_i后有r≥1人重复H_i，末位做最后一次，且其他该枝动作避开A_i及D\E_i。末位留H_i得
\[
(p+q)/(r+1)+b/r,
\]
改D得(t−b)+b/r。q>0且r≥1时
\[
(p+q)/(r+1)\le(p+q)/2<p/2+q\le t-b,
\]
故规定的最后H_i严格不是BR。所有k/r均成立，不是有限扫描。修复方向必须用其他真实枝动作先覆盖D\E_i，或用不同punisher；它们仍须付actual末位外选项和完整离轨IC，不能任意分配continuation payoffs。

## 把原PB背景直接删去的两个充分IC冲突

原PB的regular动作每段选至多k≥2个real块并用dummy块补齐。原两类充分IC写为
\[
g(r)>2f(1)-f(2),\qquad
k f(k)>f(t)+(k-1)g(1).
\]
只删背景、real/dummy块大小a,b时f(c)=a/c、g(c)=b/c。因此Greedy迫b>(3/2)ar，Fill/Copy迫a>a/t+(k−1)b，进而b<a/(k−1)。对r≥1,k≥2不相容；t1第二式已不可能。仅排这套充分IC的literal无背景移植，不排其他构造或证明。

[Beta静态克隆](../引理/Beta克隆的单次增益与复用上尾债务--引理.md)亦不能白保旧Copy：其单位有限有理实现中，原客户背景M≥1的潜在包含率P密度M(1−p)^(M−1)，相关fresh标签条件独立。k个fresh标签按对称分享每人精确份额1/(M+k)；k人重复一个exact标签时，含该标签概率E P=1/(M+1)，于是每人只1/[k(M+1)]，大M约少k倍。所有有理型共同整数清分母后是确定单位客户，非真实博弈临时随机客户。沿拟定路径用不同fresh标签避开损失，仍须补全部重复标签历史的真SPE。另原PB大背景曲线f(c),g(c)=q/M+O(M⁻²)，r名实际总利润与r动作fresh-clone覆盖共同主项rdkq/M；局部前两人安全值分离本身不提供宏观正g，更不提供g>2R+D。这里是源解析尺度边界，不新验原PB程序或新全族反例。

[原PB实际前缀障碍](PB大背景的最后单例偏离--障碍.md)另在原参数证明最后D-singleton真获利，排特定背景在轨实现。这与这里去背景的互斥充分IC是两条不同障碍；合法背景子SPE本身仍有效。

## 合法共享遗漏路径：明确给目录，但威胁未构造

对每个k≥4，m=k+1；互不交X_i大小2、Q_i大小3及E₀,E₁各4。A_i=X_i∪Q_i，D=E₀⊔E₁。**完整共同目录恰为**
\[
C_i=X_i,\quad H_i^e=A_i\cup E_e\ (e=0,1),\quad
P_{ij}=A_i\cup A_j\ (i<j),\quad D.
\]
没有额外独立A_i动作。目标路径C₁,…,C_k,D的末位是真BR：D8，H_i^e为1+3+4=8，P_ij为2(1+3)=8，C_i为1。故它是j=m−1合法**真尾输入**，前面C_i尚未声称可信。

目标W=2k+8。以至多⌈k/2⌉个pair主题覆盖全部组，再D，槽数≤m，达到全部5k+8客户，所以OPT_m=5k+8、g=k−8，k≥9为正。拟定distinct威胁要覆盖残余reservoir并分享偏离Ai，但尚没有完整SPE；有fresh pair外选项时不能硬给低punisher收益。

事实上已有必须付的真倒二缺陷。在过去C₁,…,C_(k−1)强制P_(k,j)，j<k。当前从fresh组k得5，从旧组j得1+3=4；末位若碰这两组，任何合法主题收益至多13/2<8，而D总给8。因此**每个末位BR**都避开两组选中组（可选D），强制者最终恰9，无论平局如何。
\[
\ell_k(P_{kj})=9,\quad \delta_k\ge9-2=7,\quad 2R+D\ge21.
\]
所以k≤29时g=k−8≤21不能严格超过修复成本；k≥30只超过这个下界，更早的真实floor/成本仍未控，不构成反例。R可能线性增长，不能把k调大当完成。

## 精确去向与证据

2250B FAILED原文已全文读；8648B target checkpoint四节完整旁读，原字节与两冻结SHA见[清单](../../../../tools/evidence/origin-retraction-and-credible-entry-resources/related-source-manifest.json)。以上均解析复建，0新数学程序/LP/BI/扫描，未认证外审或新颖性；共享目录有用候选继续保留，不把失败直接退休或扩为一般不可能性。异质修复完整树和费用见[现定理](../定理/真实退出缺陷的统一与异质前缀修复--定理.md)。
'''
put(PO,front('customer-attraction/repeated-punisher-last-outside-option-and-no-background-transplant','obstruction','障碍','重复惩罚的末位外选项与无背景移植','proved-specific-obstructions; shared-omission-path-not-yet-SPE','完整保重复H末位D严格偏离、去PB背景两个充分IC冲突、Beta重复损失及共享遗漏全k目录与δ≥7/成本≥21；不升级一般不可能性或half反例。',[IDS[1],'89f64465d29696938faf'])+bo)
br=r'''## 原工作区的入口与当前时态

五原件4385/2250/2638/3069/1725B，共14067B，全部实际全文读，两个冻结版本同字节。原六名指定研究员、恢复clone、个人备份、旧清洗请求/work.py、停止同模板阴性扫描等只作2026-10-24来源历史；当前Boss4 cleaner不切换角色、不spawn、不执行旧命令。源称一般half OPEN，不撤销现行五人half；当前恰六人及一般人数并未由这些辅助构造闭合。

它们登记三项精确已证辅助对象：异质前缀修复、固定来源比例回撤、真实偏离枝范围。其余ξ/η跨孩子付款、Mpath、extra-slot逐人floor、共享角色容量当时均未升级；当前逐人extra floor另已被银行否定，另见[偏离枝引理](../引理/真实偏离枝的收益与覆盖范围--引理.md)。不将当前纠正反写成原作者当时已知道。

## CLAIMS与GENERAL：异质编译主数学完整duplicate

[现完整修复定理](../定理/真实退出缺陷的统一与异质前缀修复--定理.md)已逐式保全部承重步骤：任意m≥2、1≤j<m，目标z的前j位可不理性，但给定同前缀后完整真尾π。对每个早期i/A，ell_i(A)取**全部真正完整后继SPE**中的最小最终收益；有限树极值达到，δ_i=(max_Aell_i(A)−u_i(z))_+，D=maxδ_i、R=Σδ_i。

D>0时同人数、固定Cartesian共同目录、所有旧新客户共同整数清分母前，
\[
W'=W+mD+R,\quad OPT'=OPT+(2m-1)D,\quad
g'=g-(2R+D),\quad g=OPT-2W.
\]
D0从真尾逆推，正常孩子已修、其他主题贴最低真孩子，原路径本身可拼完整SPE，不建零银行。

标记I⊆{1,…,m−1}可任意交错，k=|I|、d=m−k。k个2s银行、一个ds蓄水Y、d−1个s叶块，正常标记选fresh银行，其余Y、末位Y。强制Y后填空银行再补Y；强制freshF后填其他银行、补d−1−q个Y、末位复制F，数目(k−p−1)+(d−1−q)+1=m−i。clean允许银行任意次序和提前未超cap的Y；第一次重复/叶/超cap raw≤s后永久BI，不能再回clean。d1无Y阶段不除d−1。按δ正高度固定分层，正常i保险D+δ_i、任意首退出保险≤D；**只改保险的联合异常也重置旧坐标到最低真孩子**。正常收益恰付旧≤u_i+δ_i与保险≤D，产品后续全坐标IC和逐槽OPT配对完整，非静态NE拼接。

GENERAL中的父方例旧A1/B4、路径AAB、δ=(5/6,3/2)、整体×6，两层{1,2}与{2}，75客户18主题、u'=(17,21,33)、W71、OPT75、343有序决策历史、6174联合比较、5832最优终局，均已在现定理按原MD报告保。当前没有读或运行父方py/json；不把该75回归冒新run、half反例或全m证明。原先盲重构再对稿、potential盲审/父方第三重构是历史不同证据身份，不新增独审人数/外审。

相较统一成本(2j+1)D节省2(jD−R)。但g≤2R+D全输入时真SPE的δ0已含half，不能循环假设该稳健式。代m5得到W'=W+5D+R、OPT'=OPT+9D，只是同一定理代入；原路线当时没证预算。**现五人half已另证，故由真编译可反推五人所有合法输入g≤2R+D；这不构造来源路由的四条cap，不证明更强任意路径M和预算或早期菜单债，也不扩六人。** GENERAL数学和全部数值/停止边界已完整覆盖，故按明确目标duplicate。

## 固定来源比例回撤：扩张证书类的精确性边界

[现算法](../算法/固定来源路由的最大回撤与价格分离--算法.md)完整保CLAIMS的合同：固定一个合法、来源标记且不要求ROLE成功的R流，b_i≥0，K_iℓ≥0仅ℓ>i，Σ_ℓK_iℓ=b_i。H/J固定，每来源保留y_i∈[0,b_i]在原角色并把其后代同比缩小，零b行按0：
\[
F'_\ell=F_\ell+y_\ell-\sum_{i<\ell}(K_{i\ell}/b_i)y_i.
\]
放松原INIT充分规范化d_i≤u_i，只核最终单一2u_i cap；每客户库存/来源齐次流守恒、严格未来、密度不增，绝非每context新付u。

令s_ℓ=2u_ℓ−F_ℓ、t_iℓ=K_iℓ/b_i，按正向z_ℓ=s_ℓ+Σ_i<ℓt_iℓy_i；负即失败，否则y=min(b,z)。非负t使其逐坐标最大，成功当且仅当**固定路由同比回撤族**可行。首次失败j的λ_j1、后0、前按饱和状态反推给λ∈[0,1]，q_i=Σ_ℓ>iλ_ℓt_iℓ，精确
\[
CUT=\sum_\ell\lambda_\ell(2u_\ell-F_\ell)
+\sum_i b_i(q_i-\lambda_i)_+=z_j<0.
\]
不是所有初始化/路由/比较元组的判据，更不是通用half算法。常数λ1仍只给原O≤2W，没有新IC付款保证cut非负。m5第一cap自动、仍四条未付款，不因五人half已证就说该固定路由总成功。任意同密度来源也不能重复花同角色的全部context。

原算法/本轮旧同SHA程序成功证据已正式保[精确重放](../计算/来源回撤原程序与有序策略的精确重放--计算.md)，本批0重复执行。先盲三角审查/应用审查是固定比例精确性、不是全部初始化或routing成功证明；未把同SHA旧PASS扩到新75银行、24/791或这里未读原输出。

## 六个失败机制与当前可用义务

| 原FAILED条目 | 保留内容、去向与真实停点 |
| --- | --- |
| 用低静态λ选择真实孩子 | [ξ/η菜单引理](../引理/最优首动作菜单与真实孩子损失--引理.md)及[重置差引理](../引理/最优动作真实尾的菜单损失与重置差--引理.md)完整保R_B=ρ_A−λ_B+(C_A−C_B)；同尾ξ、单枝η不控不同真尾reset。allbig λ0/η0仍reset1，非新例。 |
| 自由入场势推出逐人θ | 固定multiset插删不控制整组后继；有限最大元/枝Cauchy保[新引理](../引理/真实偏离枝的收益与覆盖范围--引理.md)，当前逐人theta已由银行否定，不能再写OPEN；聚合候选未因此解决。 |
| full终局push折扣付早期债 | FULL-DISCOUNT和真实末两人reserve是准确合并工具，另下节保原程序范围与未付早期债，不误判候选真假。 |
| 不交银行/重复punisher | [新障碍](../障碍/重复惩罚的末位外选项与无背景移植--障碍.md)给D末位严格偏离、distinct真实惩罚义务及完整共享遗漏目录。 |
| 删除PB背景保Greedy/Fill/Copy | 同障碍保b>(3/2)ar与b<a/(k−1)冲突、Beta重复标签损失/全部重复孩子新SPE义务，非普遍no-go。 |
| 回撤后仍必须d≤u | 原INIT只是充分规范化，扩张类可用单一2u cap；扩大类不证明ROLE总可行。 |

共享遗漏target原路径g=k−8、真倒二δ≥7、成本≥21，k≤29不能越成本，k≥30更早floor仍缺。没有找到例子不成修复路线不可能；停止同机制阴性扩样是历史研究决定，不是退休这些数学资产。

## 完整终局push资源：真实末两人reserve不等一般支付

10098B旁读原稿全文读，原定义完整强制枝Z_i(A)、删强制行动的B_i(A)、查询分布p及共同客户边际q_x。D_i=E_A d_i(A)≤u_i、C_i=E_AΣ_xq_x/[1+c_x(B_i(A))]、P_i=E_AΣ_xq_x/[1+c_x(Z_i(A))]。令e_i=u_i−D_i≥0、κ_i=D_i−C_i，
\[
R_i=E_A\sum_{x\in A}\frac{q_x}{c_x(Z_i(A))(c_x(Z_i(A))+1)}\ge0,
\quad C_i-P_i=R_i,
\quad P_i-u_i=-e_i-\kappa_i-R_i.
\]
这是源FULL-DISCOUNT，不由已假tail-Jensen预算否定另一sumP≤W候选。源没有给Σκ符号或付完所有债。

倒二j=m−1，过去负载b；真实末位回复ρ(A)。令U_b(X,Y)=Σ_(x∈X)1/[b_x+1+1_(x∈Y)]、η_x=Pr_(A~p)(x∈A∩ρ(A))、w_x=1/[(b_x+1)(b_x+2)]，并令A'为独立同p抽样，
\[
L=E_{A,A'}[U_b(\rho(A),A)-U_b(\rho(A'),A)]\ge0,
\quad V=\sum_x\frac{q_x^2}{(b_x+2)(b_x+3)},
\quad Q=\sum_x\frac{2w_xq_x(q_x-\eta_x)}{b_x+3}\ge0.
\]
L每项只用A后真末位BR，ρ(A')在该处仅为合法比较，不转移其最优性；η≤q保证Q非负。已有真实两人逐客户身份给D_j−P_j=L+V+Q。末位过去b'固定，V_m=Σq_x²/[(b'_x+1)(b'_x+2)]≥0、e_m≥0，P_m=u_m−e_m−V_m；actual完整叶查询g_p(z)=u_m−e_m−R_m^actual。P_m不必等actual查询，J_m=R_m^actual−V_m可正可负，不能双计两种折扣。

自由真实列菜单ψ_i(p)=min_AΣ_xq_x/[1+c_x(Z_i(A))]，G_i=P_i−ψ_i≥0。末位G_m≥max(0,J_m)，故V_m+G_m≥max(V_m,R_m^actual)，不许把V_m与R_m相加。早期H_i=P_i−u_i，
\[
\sum_i\psi_i-W
=\sum_{i\le m-2}H_i-[e_{m-1}+L+V+Q+e_m+V_m]-\sum_iG_i.
\]
另可用actual末列得同式上界，把V_m+G_m换R_m^actual。源把早期和≤这些reserve称未证EARLY-PAY；它若对每p成立给Σψ≤W、Mpath=max_pmin_iψ_i≤W/m，并与v_(m+1)≤Mpath及静态OPT≤2mv相合推出half。m5仍有H1+H2+H3三债，本辅助方法不提供新付款。完整L/V/Q的客户定义和证明保全文旁读，不假装本资源另发新的末两人定理；末两人安全值税池[另引理](../引理/实际末两人的查询税余量--引理.md)是不同冻结背景合同，不能混名或复用预算。

原probe只在三人六标签固定完整43节点/258IC策略锥、63非空客户类型、两p（δ2+δ5各半、uniform6）作浮点LP；sumP−W最大−1/8及约−0.09104938，sumψ−W最大−1/8及约−0.09722222。0精确对偶，不认证整个锥/一般候选，label可塌同覆盖。本批全文读的是这段和完整数学MD，未读或执行probe.py/json；0新LP/扫描/旧成功复跑，不将旧PB背景子SPE替换成root-actual Mpath反例。

## README全部文件与审查/实现身份

| 原入口 | 精确用途及本次范围 |
| --- | --- |
| GENERAL_WORKING / CLAIMS | 父方推导与辅助身份，完整原文保；旧个人canonical边界不否当前正式整合。 |
| credible/heterogeneous_prefix_repair | 已有完整解析定理；原marked-bank作者实现只有限核任意标记顺序，不替全m证明。 |
| potential/blind_repair_reconstruction | 原先未读作者稿重构后对稿，不冒本轮新盲审或新研究员。 |
| parent/audit_heterogeneous_product.py/json | 原父方不导作者/规范solver的独立联合产品回归，343历史/6174比较/5832最优终局按源文报告，不是本批代码全读/执行。 |
| optimal_gap/stopping_barrier | 本批完整7771B旁读；保同尾信用/重置差/eta候选及有限测试仅历史，现主引理已自足主数学。 |
| flow/origin_retraction / optimal_gap两审 | 固定来源回撤可行性与失败价格分离，原应用审查已正式保；未全输入成功，不因字面cap当已付款。 |
| direct/extent / reproduce_extra_theta | 本批9106B数学正文读，Cauchy独有引理补自足；八旧证书theta诊断无新输入/全IC认证，未新读py及八输入。 |
| menu/complete_push_reserved_debt | 全文10098B旁读，准确合并旧真实末两人reserve，早期债仍需支付。 |
| STATE / FAILED | 当前原工作区真实停止点与六类机制，不因没有反例当普遍不可能，外部清洗请求不表示当时清洗者已读。 |

原source文称checkpoint pushed才远端保存只是历史正确记录，本代理不执行Git或据本地草稿宣布已发布。实际原认领/owner/sourceSHA/完整阅读范围和逐源去向见[证据](../../../../tools/evidence/origin-retraction-and-credible-entry-resources/source-manifest.json)。不额外done四旁读、引用程序、JSON或下一源，不导第三阶段图，不认证外审/全球新颖性。新数学程序/原CLI/旧成功复跑全0；已知可用同SHA重放只准确复用。
'''
put(PR,front('customer-attraction/origin-retraction-and-heterogeneous-repair-entry-payment-boundaries','resource','资源','来源回撤与异质修复入口的全树付款边界','all5entrytexts-reviewed; finite-reports-source-only; global-payment-open','五入口全部数学/审查/程序与失败用途归位；异质修复/固定路由精确复用，新保真实偏离枝和两特定攻击障碍；旧m5方法边界与现已证五人分开，逐人extraθ按后源纠正。',IDS)+br)
js(E/'formal-resource-manifest.json',[{'path':p,'bytes':(S/p).stat().st_size,'sha256':sha((S/p).read_bytes())} for p in [PL,PO,PR]])
coverage=[
 {'id':IDS[0],'disposition':'integrated','targets':[PH,PA,PL,PR],'units':['fullgeneralmodel allm/fullhistories/ties/empty/zero oldOPENcurrent5vs6','heterogeneous truechildell maxdefects/D/R/actualoldpath/credibleonlytail/allmarkinterleaving/permanentBI/fixedlayerproduct/fullinteger scaling/D0separate','all W+ mD+R/OPT+(2m-1)D/gapcost2R+D equations alreadyfulltheorem no newrange/externalnovelty','fixedorigin rowconservation/futureonly/finalcap only/affinecurrent/scalingalltaggeddescendants/zero rows','forwardmaximalgreedy iff fixedproportionalrepair family/firstnegativecut z_j<0/constantpriceoriginaltarget notpaidIC','positiveui truebranch Cauchy extent fullproof/offpathsameoriginalsigma/fixedpast/Kmax/k0/ui0 correct','independentreview/parent analytic-andimplementation identities sourceonly no originalpy/json reread']},
 {'id':IDS[1],'disposition':'integrated','targets':[PO,PR,PX,PY,PA,PL],'units':['all6failuremechanisms exactsource-limited/notgeneralimpossibility','optimaloffspring lowlambda/staticcredits nottruechangedtail reset/fullxi eta retained','freeentrypotential insertiondeletion static notgiven SPE/individualextra-theta nowbankrefuted aggregate notautomatic','completefullpush owndiscount/actualtwotail reserve/early3debt m5 unpaid/currentcandidate notgloballyproof','repeatedH lastD outsideoption strictforqpositive anyr/distinctrealpunishercoverage obligation','literalPB b>1.5ar andb<a/(k-1) incompatible onlysufficientIC/Betaclone repeatedlabels harmed/futurecompleteSPE needed','INITdi<=ui onlyold sufficient normalization notnewroute success','allk>=4 realsharedomission catalog onlyCi,Hie,Pij,D/lastBR8/W2k+8/OPT5k+8/gk-8','penultforcedPkj truefloor9/alllastBRavoidsselectedgroups/delta>=7/cost>=21/k<=29notstrict/k>=30othersfloorunpaid','stoptemplatescanninghistorical notretiremathematics/no negativeevidenceasno-go']},
 {'id':IDS[2],'disposition':'duplicate','targets':[PH,PR,PX,PY],'units':['wholemodel/allomission-minusoutside OPT-W=|M|-|E| notfalse|M|<=W/pastplayerrefund','heterogeneous fulllayerconstruction andfreshF/Y matching/permanentBI allordered exits unchanged','sourceheightfixedoneCartesianinstance/profitD+deltai/exit<=D/fulljointreset evenonlyinsurance changed/cleardenominatorsbotholdnew','75unit18topics/fullscale6/layers{1,2},{2}/u17,21,33/W71/OPT75/343hist6174comparisons5832OPTtuples originalMDreport notnewcode','gapbudgetcannotassume circular/saving2(jD-R)/m5formula historical nowfivehalfimpliesrobustcompilerbudgetonly','xi eta /samequeryindependentmenu/sharedrole allcontexts density notsharedcapacity payment']},
 {'id':IDS[3],'disposition':'integrated','targets':[PR,PH,PA,PL,PO],'units':['all10directoryentryprogramreviewroles table complete/cloneorigin and6models history notnewrole execution','arbitrarym/commonnonempty/completeorderedSPE tieempty/repeat/zeroclients','bankauthormarkedordercheck finite notgeneralproof/parentindependentnoimportsolver product distinctfromauthorimplementations','blind-beforetext vsaftertext/thirdparent reconstruct historynotnewblindperson','stoppingbarrier/source-retraction2audits/directtheta replay/menu fullreserve/STATE/FAILED allusefuldestinations','pushedcheckpointonlyremotehistory notstageproofpublished/no originalprogramJSONclosedependencies invented','unconditionalfivehalfcurrent separatefromoldroutefailure/sixgeneralremainunpaid/noinspectionbycleanerpresumedfromoldrequest']},
 {'id':IDS[4],'disposition':'duplicate','targets':[PH,PA,PL,PO,PR],'units':['sixmodelparticipantsreturned frozenhistory andno targetproof/newrange/counterexamplethen','heterogeneous2j+1D reduced2sumdelta+D/allmarkbank/thirdindependentproduct no violatingseed','fixedroutecap/cutnotuniversal/constantcut originaltarget','lowprofitforcestruebranchwholecoverageextent notOPTactuallowerbound','menuoptchildfreeentry keeptails/refunds/xi eta notnumerictruthupgrade','m5W+5D+R/OPT+9D/4rolecaps/3earlymenu debts distinguishcurrent5theorem andfixedroutes','trueICnonnegativecut orcostexceedingpath nextinformation notduplicatecredit/allbranchesreusesamebudget forbidden','stoppednegativesamplingnotuniversalno-go/oldexternalcleanuprequestnotreadcert/no fakeformalupgrade']}
]
js(E/'semantic-coverage-map.json',coverage)
scope={'primary_sources':5,'primary_bytes':14067,'primary_lines':sum(x['lines'] for x in primary),'primary_first_full_read':'JN actualcomplete primary5 text/math afterISseal, beforeactualJNclaim withparentauthorizedpreparation; guard verifiesactualclaim beforewriting finalreceipts','related_sources':4,'related_bytes':35623,'related_complete_actual_read':True,'current_formals_actual_fullread':len(contexts),'initial_broad_rg_result':'truncated discoveryoutput only, notclaimedfullread; replaced bytargeted complete original/9formal reads','dispositions':{'integrated':3,'duplicate':2},'new_formals':3,'new_mathematical_results_claimed':0,'new_game_instances':0,'new_math_program_runs':0,'original_math_CLI_calls':0,'old_success_replays':0,'LP_BI_random_runs':0,'old_origin_retraction_success':'sameSHA evidencealreadyformal; notrerun/nottransferredto75bankor24/791','raw_program_or_JSON_fullread':False,'originalprogramroles':'onlyactualsourceMDandcurrentformal contracts, notallcode closedependency audit','helper_calls':2,'local_blob_attempts':9,'local_exports':9,'local_missing_blobs':0,'helper_scopes':['4necessaryrelated mathematicalMD','5nextentrybyteavailability only'],'next5_status':'actualbyteavailability only; nofullsemanticread orprimaryreceipt inJN','missing_retry_calls':0,'shared_Git_writes':0,'claim_done_checkpoint_show_calls':0,'network_or_lazy_fetch':0,'real_board_account_auth_operations':0,'phase3_graph_import':0,'raw_claim_ids':len(claim['ids']),'primary_claim_intersection':IDS,'claim_projection_performed':False,'derived_packaging_builder_calls':1,'derived_packaging_builder_failures':0}
js(E/'read-scope-and-evidence-status.json',scope)
notes=[
 ('4385B CLAIMS在JN授权预读期全部原文实读，三个精确ID的statement/domain/dependencies/evidence/status/counterevidence/files和未证项完整保，不以账本勾选代原证明。','与现完整异质编译/固定来源回撤全文比较，全部公式与限制准确复用；独有true-branch extent按必要9106B全文旁读逐客户重构Cauchy，包括过去/空/零收益，不误把上界当实际W下界。','integrated：新引理及资源吸收确切数学和审查时态，GENERAL具体银行组件不重认新发现。来源回撤只精确限定家族，lambda1仍原half，0新原代码/JSON/原CLI、0外审或新颖性认证。'),
 ('2250B FAILED表六行及尾共享遗漏段逐字全文读，另8648B target四节全部数学完整旁读，原所有停点/重试条件准确读。','静态λ与真实reset同ξ/η两引理比较，原INIT可放松与现回撤算法比较；重复H末位D严格偏离、去PB标量冲突、Beta重用收益以及合法k族目录/真倒二9/成本21均解析自足，不把有限扫描当证明。','integrated：新障碍只排精确机制，不误作一般no-go或half反例。k<=29不足和k>=30更早floor仍缺、旧未找到路径不成不可能性都保。fullpush准确reserve与三早期债保资源，0新BI/LP/旧成功复跑。'),
 ('2638B GENERAL全部目标/银行配方/首次退出与比例高度/父方75回归/五人压力/尾义务原文实读，不执行旧工作稿中的研究命令。','现异质编译定理已完整覆盖任意标记银行、永久BI、全部联合偏离、全坐标reset、统一整数清分母、三公式、75原记录和真实缺口；本资源逐项定位OPT-W净遗漏/过去返还/xi eta/菜单与角色容量停点。','duplicate：全数学有精确已存在自足目标，按同对象而非篇幅判断。现五人half可通过真编译反推五人稳健2R+D预算，但不倒填原研究当时结论、不外推六人或任意路径M/固定路由成功；原finite作者身份不算新run。'),
 ('3069B README所有十行入口及开头模型/6研究员/恢复时间、结尾明确下一义务/备案/远端保存逐段全文读，不以链接数量当语义完成。','逐项对现修复/回撤/枝范围/xi eta真重置与四必要related全文比较；作者marked-bank、盲重构、父方不导作者/solver产品检查、direct theta八旧证书、menu两p浮点诊断的实现/审查范围各自保。','integrated：保完整可用资源合同与最新真值边界，不把文件角色宣称成程序全文或新审计，不因原README个人canonical标签删除已整合数学。0旧角色/真实Git账号动作，0额外done全部引用程序/报告。'),
 ('1725B STATE六段/四条与m5代入/下一义务/清洗请求尾段全部实读，准确区分旧研究停止和当前cleaner任务。','现3个已证辅助对象与本资源把原异质损失、固定源cap、低收益枝、跨孩子/自由入场/菜单缺口全部覆盖；m5旧方法的四cap/三早期债不因当前half已证自动付款。','duplicate：准确归位所有内容，清洗请求不等当时已审，六名旧研究员不当本轮新spawn；停止相同阴性不当普遍不可能性。下一仍需真IC支付cut或坏路径越真实修复成本，0新原程序/旧成功复跑。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 原多组actualclaim原字节保，仅本5subset/现owner/sourceSHA核后填successreceipt。','comparison_note':b,'decision_note':c,'disposition':x['disposition'],'targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(E/'README.md',r'''# JN来源回撤与异质修复五入口

原五MD14067B全部JN授权预读期实际读完，正式claim/source-owner-SHA核后封包。四必要related数学MD35623B完整实读，9个现正式对象全文比较。初始宽搜索输出截断仅作定位，后完整目标读取承担阅读声明，不能把截断尾部计完成。

3integrated+2duplicate；3自足新对象是原证明的枝范围引理、两精确威胁机制障碍及入口资源，0新发现/一般half/实例或新数学程序。完整保k族目录/OPT与末位floor、异质成本/全树bank永久出口、固定来源greedy/cut的受限精确性、fullpush折扣与早期债及旧程序/审查用途。

当前银行反逐人extra theta，聚合仍另判断；五人half已证可反推真编译稳健预算，却不提供每固定路由cap或早期共同支付，不扩六人。冻结源与旧成功不改，原code/JSON未本批全读，0原CLI/LP/BI/随机/旧成功复跑。

两次安全helper9尝试：4必要related35623B、5次入口/审查字节8606B全齐，0missing/network。封包现owner核时，3920B blind审稿657caca9d3baac5508e2已有Boss4/in-progress，仅余4个入口4686B可提下一候选；原5次导出清单仍原字节保，不能把另有归属的稿接成本线新primary。四候选只byte未全文/未claim/无receipt。Root先推正文与依赖再done；代理0sharedGit/账号公屏/第三阶段mapper。
''')
put(W/'relation-review.md',r'''# 阶段二对象关系

异质编译是真尾输入的完整构造；同人数/固定Cartesian/任意标记/全整数清分母/永久BI出口与OPT配对均保，GENERAL全部精确duplicate到现证明。固定来源回撤是已定路由同比缩放族的精确判据，放松初始d cap不等一般ROLE成功；constantcut仍原目标，不能循环用half给缺失资金。

新枝引理为每真实强制主题的全枝W上界，固定过去计在其他m−1主题中。它不把互斥枝接成actual福利下界；自由入场静态插删也不控制given SPE的整尾reset。银行反逐人theta，不因此反聚合或half。

新障碍仅排重复punisher和PB literal无背景充分IC，不排任意非平稳威胁。共享遗漏全k目录提供合法真末位路径及真实缺陷下界，非完整SPE；k大不代完整floor。完整菜单tail reserve与最优孩子xi/eta是不同证明账本，真实早期亏损不能重复花同角色容量，也不允许移静态同尾信用去新真尾。

原有限回归数字/LP阴性仅源文证据，0原代码全读/新执行，旧同SHA成功只复用不移到新输入。0额外done四旁读或引用程序/JSON/下一5，不因图连通或已有目录强造第三阶段关系。
''')
nextmp=C/'learning-jn-next-entry-and-blind-review-inputs/local-export-manifest.json';nextm=json.loads(nextmp.read_text());assert len(nextm['rows'])==5 and nextm['missing']==[];cp(nextmp,E/'actual-next-byteavailability-local-export-manifest.json');nextrows=[]
for x in nextm['rows']:
 v=inv[x['id']];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'];q=REPO/'cleanup/progress'/f"{x['id']}.json";pr=json.loads(q.read_text()) if q.exists() else None
 if pr is None:nextrows.append({**v,'local_path':x['local_path'],'progress_observed':None,'read_status':'byteavailability only beforeJNseal; noactualfullsemanticread orprimaryreceipt yet; Root deconflicts actualnextclaim'})
assert sum(x['size'] for x in nextm['rows'])==8606
excluded=[]
for x in nextm['rows']:
 if x['id'] not in {a['id'] for a in nextrows}:
  p=REPO/'cleanup/progress'/f"{x['id']}.json";state=json.loads(p.read_text());excluded.append({'id':x['id'],'bytes':x['size'],'actual_progress':state,'scope':'exportbyteverified but alreadyowned; notwithinJNclaim, nofullread/receipt/newclaim bythisline'});cp(p,E/'next-excluded-ownership'/p.name)
scope['next5_status']='5exportedbytefiles, 1alreadyBoss4/in-progressexcluded; only4unclaimedentrycandidates4686B, nofullsemanticread orprimaryreceipt';scope['derived_packaging_builder_calls']=2;scope['derived_packaging_builder_failures']=0;scope['next_candidate_bytes']=sum(x['size'] for x in nextrows);js(E/'read-scope-and-evidence-status.json',scope);js(E/'next-export-owner-reconciliation.json',{'exported':5,'exported_bytes':8606,'proposed_candidate_ids':[x['id'] for x in nextrows],'proposed_candidate_bytes':scope['next_candidate_bytes'],'excluded':excluded,'revision':'firstsuccessfulbuilder producedpayload; beforedelivery actualnextownerreconciliation removed1ownedblindreview andcorrected4candidatebytecount; math/formalbody unchanged, 0mathruns'})
js(W/'next-candidates.json',nextrows);cp(Path(__file__),E/'build_delivery.py')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
def tex_balanced(s,left,right):
 def count(d):return sum(ord(s[i])==92 and s[i+1]==d and (i==0 or ord(s[i-1])!=92) for i in range(len(s)-1))
 return count(left)==count(right)
assert tex_balanced(chr(92)+'[x'+chr(92)+']','[',']') and not tex_balanced(chr(92)+'[x','[',']') and tex_balanced(chr(92)*2+'[2pt]','[',']')
for x in primary+related:
 b=(S/x['preserved_path']).read_bytes();ck('sourceexactsizeSHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('sourceexactblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('rawclaim byteidentical',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes());ck('actual5subsetownerSHA',set(IDS)&set(claim['ids'])==set(IDS) and all(x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[x['id']]['sha256'] for x in owners));ck('actualclaim pushedsynced',claim['status']=='pushed' and claim['local_sync']['status']=='synced' and claim['local_sync']['remote_tip']==claim['remote_tip']);ck('rawnotprojection',len(claim['ids'])>=len(IDS) and (S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes())
for x in contexts:ck('contextcurrentbytes '+x['path'],len((S/x['snapshot']).read_bytes())==x['bytes'] and sha((S/x['snapshot']).read_bytes())==x['sha256'])
links=[]
for p in [PL,PO,PR]:
 t=(S/p).read_text();ck('flatMATEK '+p,all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('nonLF C0zero '+p,not any(ord(c)<32 and c!='\n' for c in t));ck('trailingzero '+p,all(l==l.rstrip() for l in t.splitlines()));ck('actualTeXbalanced '+p,tex_balanced(t,'[',']') and tex_balanced(t,'(',')'))
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in dest or dest.startswith('#'):continue
  n=posixpath.normpath(str(Path(p).parent/dest.split('#',1)[0]));q=S/n if (S/n).exists() else REPO/n;ck('actualrelative link '+dest,q.exists());links.append({'source':p,'destination':dest,'resolved':n,'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())})
js(E/'formal-link-check.json',links)
lt=(S/PL).read_text();ot=(S/PO).read_text();rt=(S/PR).read_text();ck('extentactualnotlower','同一原σ' in lt and '过去m−r' in lt and '上界' in lt and 'u_i=0' in lt and 'K/m' in lt);ck('individualtheta correctedaggregateunrefuted','ϑ5≥δ5>u' in lt and '不能由逐人失败推出聚合' in lt);ck('fullpunisherscope','其他该枝动作避开A_i及D' in ot and 'q>0且r≥1' in ot);ck('allkpathnotSPEandcost',all(x in ot for x in ['完整共同目录恰为','P_{ij}','k≤29','k≥30','2R+D\\ge21','未声称可信']));ck('PBonlytwosufficientIC','Greedy迫' in ot and 'literal无背景移植' in ot and '1/[k(M+1)]' in ot);ck('fullproduct75notnewrun',all(x in rt for x in ['只改保险','永久BI','所有旧新客户共同整数','5832','0重复执行']));ck('fixedroutefamilyandcut','固定路由同比回撤族' in rt and 'z_j<0' in rt and '四条未付款' in rt);ck('m5currentandoldpressure separated','现五人half已另证' in rt and '不扩六人' in rt);ck('fullpush lastdiscountnotdouble','P_m不必等actual查询' in rt and '不能双计两种折扣' in rt and 'G_m≥max(0,J_m)' in rt);ck('fullpushprobeexactscope',all(x in rt for x in ['43节点/258IC','63非空客户类型','−0.09104938','−0.09722222','0精确对偶']));ck('codeandsourcehistorynotnewcert','原code/JSON未本批全读' in (S/E/'README.md').read_text() and '不认证外审/全球新颖性' in rt)
ck('5receipts3integrated2duplicate',len(receipts)==5 and {x['id'] for x in receipts}==set(IDS) and sum(x['disposition']=='integrated' for x in receipts)==3 and sum(x['disposition']=='duplicate' for x in receipts)==2)
for x in receipts:ck('complete semanticreceipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']) and all((S/p).exists() or (REPO/p).exists() for p in x['targets']))
ck('exact3newformal',set(str(p.relative_to(S)) for p in (S/'archives').rglob('*.md'))=={PL,PO,PR});ck('no mathbodyoroldreplays',scope['new_math_program_runs']==scope['original_math_CLI_calls']==scope['old_success_replays']==scope['LP_BI_random_runs']==0);ck('helper2calls9exports0missing',len(nextm['rows'])==5 and len(rm['rows'])==4 and nextm['missing']==rm['missing']==[] and scope['helper_calls']==2 and scope['local_blob_attempts']==9)
for x in nextrows:ck('actualnextavailable '+x['id'],Path(x['local_path']).exists() and len(Path(x['local_path']).read_bytes())==x['size'] and sha(Path(x['local_path']).read_bytes())==x['sha256'] and x['progress_observed'] is None)
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:u=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 rel=str(p.relative_to(S));frozen=any('/'+z+'/' in rel for z in ['original','related','context']);bad=[i+1 for i,l in enumerate(u.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(u) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':rel,'frozen':frozen,'trailing_lines':bad,'nonLF_C0':c0})
ck('allnewderivedC0trailingzero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observed':obs,'frozen_original_related_context_unchanged':True})
put(W/'delivery.md',f'''# JN交付

五primary14067B/{scope['primary_lines']}行全文实读，四related35623B及九现正式对象完整比较。3integrated+2duplicate，3新自足正式对象；原多组{len(claim['ids'])}ids claim {claim['remote_tip']} actualpushed/synced，原字节保仅本5subset/owner/sourceSHA。

Cauchy真实枝覆盖上界、重复punisher末位外选项/PB无背景条件冲突及合法k族未可信路径/真floor9成本21都自足保。异质全树/固定回撤精确duplicate复用，不认证一般half/固定路由总成功。旧逐人theta按银行更新，五人已证与本路线过去压力分开。

0新数学程序/原CLI/LP/BI/随机/旧成功复跑，未读原code/JSON不冒当前认证，旁读4源不额外done。下一{len(nextrows)}当前未领齐件共{sum(x['size'] for x in nextrows)}B，仅byte未全文，不预claim/receipt；5次入口导出8606B中的3920B blind稿现已有Boss4/in-progress，原清单保但不列下一候选。2helpers9尝试0missing/network。封包器2调用/0失败：首成功后仅校正下一归属/计数，正文数学未改。Root先推正文依赖再done，本代理0sharedGit/账号或phase3mapper。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'relative_links':len(links),'formal_nonLF_C0':0,'formal_trailing_whitespace':0,'math_checks':'analytic reconstruction/source comparison; no mathematical program executions; packaging counts do notprove universalhalf or originalunreadcode claims','scope':'actualoriginal/related fullread sourcebindings/currentformal/owner/rawclaim/coverage/links/format/transport'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':14067,'primary_lines':scope['primary_lines'],'related_bytes':35623,'new_formals':3,'formal_bytes':sum((S/p).stat().st_size for p in [PL,PO,PR]),'receipts':5,'dispositions':{'integrated':3,'duplicate':2},'checks':len(checks),'relative_links':len(links),'new_math_runs':0,'new_original_CLI_runs':0,'old_success_replays':0,'raw_claim_ids':len(claim['ids']),'claim_tip':claim['remote_tip'],'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
