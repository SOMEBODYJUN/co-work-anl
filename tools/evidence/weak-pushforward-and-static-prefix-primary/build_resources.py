from pathlib import Path
import json,hashlib

R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';S=C/'r3-weak-pushforward-and-static-prefix-primary';E=Path('tools/evidence/weak-pushforward-and-static-prefix-primary');W=Path('cleanup/workspaces/Boss4/r3-weak-pushforward-and-static-prefix-primary-next')
IDS=['666061ceda2882cfd25d','71bdd0dc3ec8f127e59b','b82223f1516f80533ccd']
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())};claimpath=R/'boss4-r3-next-ex-claim.json';claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(claim['ids'])==set(IDS)
cp(claimpath,E/'actual-claim-receipt.json');owners={}
for i in IDS:
 x=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());assert x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==inv[i]['sha256'];owners[i]=x
js(E/'primary-ownership-snapshot.json',owners)
mp=C/'learning-eo-next-local-candidates/local-export-manifest.json';m=json.loads(mp.read_text());cp(mp,E/'actual-local-supply-manifest.json');rows=[]
for x in m['rows']:
 assert x['id'] in IDS;b=Path(x['local_path']).read_bytes();assert len(b)==x['size'] and sha(b)==x['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'];dest=E/'original'/x['id']/x['path'];cp(x['local_path'],dest);rows.append({**x,'preserved_path':str(dest),'lines':len(b.splitlines()),'read_scope':'first full original mathematical reading in EX; prior EO only availability bytes checked'})
assert {x['id'] for x in rows}==set(IDS);js(E/'source-manifest.json',rows);byid={x['id']:x for x in rows}
def link(i):return '../../../../'+byid[i]['preserved_path']
missing=[]
for n in ['learning-ex-related-local-inputs','learning-ex-next-local-candidates']:
 p=C/n/'local-export-manifest.json';x=json.loads(p.read_text());cp(p,E/(n+'-manifest.json'));missing+=x['missing']
js(E/'missing-local-inventory-bindings.json',[{'inventory':inv[x['id']],'reason':x['reason'],'scope':'unread local absent code/report/candidate, no network, no primary claim or done'} for x in missing])
cp(C/'learning-eo-next-local-candidates/local-export-manifest.json',E/'prior-two-missing-JSON-supply.json')
contexts=['archives/customer-attraction/state/反例/三人逐人混合安全值--反例.md','archives/customer-attraction/state/反例/笛卡尔银行目录的逐人分数门槛反族--反例.md','archives/customer-attraction/state/反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md','archives/customer-attraction/state/定义/自由分数背景安全门槛--定义.md','archives/customer-attraction/state/引理/末位真实回复推送的锐曲率与双分支式--引理.md','archives/customer-attraction/state/资料/完整根查询证书的字段与审计范围--资料.md','archives/customer-attraction/state/资料/完整根菜单的联合势义务与排序边界--资料.md','archives/customer-attraction/state/审查/额外槽扫描的实际强桥目标与两份定义级核验--审查.md']
ctx=[]
for n in contexts:
 b=(REPO/n).read_bytes();cp(REPO/n,E/'context'/n);ctx.append({'path':n,'bytes':len(b),'sha256':sha(b),'snapshot':str(E/'context'/n),'scope':'full mathematical current/prior actual reading, exact bytes reused; no extra source done'})
js(E/'context-manifest.json',ctx)
rawpaths={'46b1b3c7907ee8c886ce':'archives/customer-attraction/tools/evidence/continuation-security/examples/customer_attraction/individual_security_failure.json','f218c3c894b4635ecca2':'tools/evidence/complete-menu-certificates-and-review-primary/original/f218c3c894b4635ecca2/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_34_D_lt_C_exact.json'}
related=[]
for i,n in rawpaths.items():
 b=(REPO/n).read_bytes();x=inv[i];assert len(b)==x['size'] and sha(b)==x['sha256'];dest=E/'related'/i/x['path'];cp(REPO/n,dest);related.append({**x,'preserved_path':str(dest),'local_path':str(REPO/n),'read_reuse':'previous actual full EO input read; same original bytes, no source done'})
js(E/'related-source-manifest.json',related)
old='archives/customer-attraction/tools/evidence/extra-slot-programs-primary/runs/parent-aggregate/stdout.txt';cp(REPO/old,E/'reused-evidence'/old)
old='archives/customer-attraction/tools/evidence/extra-slot-programs-primary/runs/EXECUTIONS.json';cp(REPO/old,E/'reused-evidence'/old)
def head(id,kind,typ,title,status,summary,sources):
 a=['---',f'id: "customer-attraction/{id}"',f'kind: "{kind}"',f'type_tag: "{typ}"',f'title: "{title}"',f'status: "{status}"',f'summary: "{summary}"','source_refs:']
 for i in sources:
  for z in inv[i]['sources']:a.append(f'  - "source:{z["commit"]}:{z["path"]}"')
 return '\n'.join(a)+'\n---\n\n'

P1=Path('archives/customer-attraction/state/引理/合法前缀的静态额外槽预算与条件归约--引理.md')
body1=r'''# 合法前缀的静态额外槽预算与条件归约

## 来源、真值与原模型

[2167B弱推送归约](SRC_REDUCE)及[2590B历史路由](SRC_README)全文实读。静态下界、有限minimax条件推导及附属LP表示正确；原文“只剩WP仍OPEN/继续攻WP”是历史状态，普遍WP现在已被反例否定。保留有效条件蕴含，不把假前提误记为一般half证明，也不把整份静态数学随旧状态退休。

有限单位客户N、有限非空共同目录S、m≥1位单位提供者，全部有序历史纯SPE和任意平局；空主题、重复主题、零客户都保留。固定长度k的合法原主题前缀，负载b，r=m−k≥1名剩余。强制当前行动B后按同一原策略得完整r槽Z(B)，当前actual最优收益u。查询A与产生Z(B)的B独立同law p，

\[
C(p)=\mathbb E_{A,B\text{ iid }p}
\sum_{x\in A}\frac1{1+b_x+c_x(Z(B))},\qquad
D(p)=\mathbb E_B u_{current}(Z(B))\le u.
\]

强式为D(p)≥C(p)，弱式WP为每个p都有u≥C(p)。后者没有要求强制根的平均收益本身付款；但它仍是一个普遍个体节点命题，不等于总福利half。

## 合法前缀的静态下界

定义查询独立的r个合法静态对手安全值

\[
v_{r+1}(b)=\max_p\min_{z\in S^r}\sum_Ap_A
\sum_{x\in A}\frac1{1+b_x+c_x(z)}
=\min_{Q\in\Delta(S^r)}\max_T\mathbb E_Q f_{b,z}(T),
\]

其中f_(b,z)(T)=Σ_(x∈T)1/[1+b_x+c_x(z)]，等号用有限零和minimax。单纯形紧且收益连续，最优p和Q都取到。每个r槽Z(B)合法、查询A独立，所以对安全最优p*，C(p*)≥v_(r+1)(b)，不要求真实推送分布是静态最优对手。

任取Q，置L_x=b_x+E_Qc_x(z)，g(T)=Σ_(x∈T)1/(1+L_x)，M_Q=max_Tg(T)。倒数凸性逐查询给max_T E_Q f_(b,z)(T)≥M_Q。固定一个最优m元组，其客户重数d_x满足

\[
\mathbf1_{d_x>0}\le\frac{d_x+L_x}{1+L_x},\quad
OPT_m\le\sum_x\frac{d_x}{1+L_x}+\sum_x\frac{L_x}{1+L_x}.
\]

首项是m个合法比较主题的g值之和，≤mM_Q。第二项也≤mM_Q，关键不是任意b，而是b确由k个原合法主题组成：若mu_T为这k个主题计数加Q中r槽的期望主题计数，则mu≥0、Σmu=k+r=m且L_x=Σ_(T含x)mu_T，因此

\[
\sum_x\frac{L_x}{1+L_x}=\sum_T\mu_Tg(T)\le mM_Q.
\]

对所有Q得OPT_m≤2m max_T E_Q f，取min_Q便得到准确静态结果

\[
\boxed{v_{r+1}(b)\ge OPT_m/(2m).}\tag{STATIC}
\]

它不需要SPE，但**需要合法k主题前缀且k+r=m**。不能因为两人代数允许实背景，就把任意非负b代入这个按m付款的计数预算。

## WP若成立的条件蕴含

若所有合法节点及每个p均有WP，取各节点静态最优p*，便有u_i≥C(p*)≥v_(r+1)(b)≥OPT_m/(2m)。沿原实际路径求和给W≥OPT_m/2。全零客户时全式为0；前缀固定主题/真实完整后继和同目录没有被删去。

这是正确条件归约，非WP证明。定义K_(T,B)=Σ_(x∈T)1/[1+b_x+c_x(Z(B))]、Mfull=min_Q max_T(KQ)_T，则C(p)=p^TKp。弱WP对每个p是自由Q完整根Mfull的充分条件：这里调用有限对称两人博弈的对称混合Nash存在定理（Brouwer固定点，不是构造算法承诺）；在该p上max_T(Kp)_T=p^TKp；若全p WP则这个值≤u，取Q=p即给Mfull≤u。这里只用该充分方向，不把不同量词的合同写成等价。[菜单资料](../资料/完整根菜单的联合势义务与排序边界--资料.md)保完整合同及抽象矩阵的逻辑区别。

## 当前WP和逐人结论都已有一般反驳

已证[银行完整SPE族](../反例/笛卡尔银行目录的逐人分数门槛反族--反例.md)使用m个经济客户、m−1个各含两客户的银行块、完整乘积主题T_ab={e_a}∪B_b；其全历史控制器给

\[
u_1=\frac m{m-1},\quad W=2m,\quad OPT_m=3m-2,
\quad t_{m+1}(0)=\frac12+\frac{2(m-1)}{2m-1}.
\]

这里t是自由**分数均值**值，真正整数静态v另由Jensen满足t_(m+1)≤v_(m+1)，不宣称相等。m4时u4/3<19/14=t5≤v5；安全最优p*使其真实完整推送C(p*)≥v5>u，故全p WP已假，无需求出p*或运行新搜索。零背景根节点即可失败，也就不能以“仍欠任意合法背景”保留普遍WP。

更强的逐人OPT/(2m)结论本身也不是一般真命题。该同一族给

\[
\frac{OPT_m}{2m}-u_1
=\frac{m^2-5m+2}{2m(m-1)}>0\quad(m\ge5).
\]

m5为5/4<13/10、差1/20；m6为6/5<4/3、差2/15。它不反驳half，因为W2m而2W−OPT=m+2>0；个体保底与总体补偿不同。旧“WP充分half”的蕴含仍有效，但假前提和这个过强逐人目标不能继续当作待证普遍步骤。

## 覆盖采购预算的精确LP表示

附属表示单独取v≥0（应用v=u_i确满足），A_(x,T)=1_(x∈T)，z_T≥0为辅助**实采购量**，不要求Σz=m、也不是原玩家分数承诺。令

\[
B(v)=\max_{z\ge0}\left[\sum_x\min(1,(Az)_x)-v\sum_Tz_T\right].
\]

用s_x∈[0,1]、s≤Az写成有限LP：max Σs−vΣz。其对偶minΣbeta_x，约束alpha,beta≥0、alpha_x+beta_x≥1、A^Talpha≤v。任一alpha>1可截成1，保后一个约束且不增加所需beta，故可取0≤alpha≤1、beta=1−alpha。有限LP强对偶遂给

\[
\boxed{B(v)=|N|-\max\{\sum_xy_x:0\le y_x\le1,
\ \sum_{x\in T}y_x\le v\ \forall T\}.}\tag{DELETE}
\]

v≥0时z0和y0都可行，0≤B(v)≤|N|；保留质量多面体紧，最优y取到。因此B(u_i)≤W恰等价于存在一份**可分数删除**，总删除质量Σ(1−y_x)≤W，使所有原主题保留容量≤u_i。不是要求删除整数个客户，也没有从SPE构造这份y。v0时没人接受的客户可全部保留，不误把B0一概等于|N|；零客户全式0。

DELETE是精确表示，不自动给WP、早期玩家付款或一般half。这里的z域也不同于STATIC中恰m槽的目录计数，不能因都写覆盖预算而共用费用或量词。

## 历史搜索和缺失实现的范围

README称search_individual_floor.py从合法SPE路径转固定策略锥作浮点LP交替，原记号p7/m5、8seed×10轮最低比1/9未到1/10；没有其代码/完整输出，不把80当真实LP调用数或有限阴性当普遍floor证明。search_terminal_pushforward.py分别攻击D≥C及--weak的u≥C，浮点candidate_*不自动认证；exact标签也须有实际输入/完整SPE和精确算式，不能只看文件名。

原路由2026-10-22记k2复制的弱推送“阳性”因额外查询漏+1而撤销，保其软件错误历史，不当真实反例。后来的Mfull替换、后继价格比较、270/348势排序是不同接口；270和381原JSON本地未取得，README数字/发现叙述只保作者范围。已核348及其他当前反例见菜单资料，不回填成这两缺件已认证。

本批无新数学CLI/LP/全SPE或样本扫描；完整静态/对偶与当前真值的比较均为解析推导。四个被引用代码/报告和两旧JSON的本地缺失有真实回执，不补网络、不冒读/复现；旧角色/下一步路线只存历史，不成为本轮cleaner命令。
'''
body1=body1.replace('SRC_REDUCE',link(IDS[2])).replace('SRC_README',link(IDS[0]))
put(P1,head('legal-prefix-static-extra-slot-budget-and-conditional-reduction','lemma','引理','合法前缀的静态额外槽预算与条件归约','static-bound-and-LP-duality-proved; conditional-half-implication-valid; universal-WP-and-individual-floor-refuted','完整合法前缀预算v>=OPT/(2m)、安全最优查询接入及可分数删除LP对偶；保原条件归约却纠正旧WP开放状态，银行反族否定过强逐人保底而不否定half。',[IDS[0],IDS[2]])+body1)

P2=Path('archives/customer-attraction/state/反例/空根稀释的强推送失败与弱桥范围--反例.md')
body2=r'''# 空根稀释的强推送失败与弱桥范围

## 原件、比较对象和准确命题

[3569B主稿](SRC_MAIN)和[2590B路由](SRC_README)全文实读。它补充原JSON之外的14个空历史解析延伸与一般小概率机制；不只复述D−C负值。原作者定义级核验、root独立核验是其历史证据身份，无外审/新颖性。本批未取得其3051B audit_integer_push_34.py和5246B同名报告，不能把现有另一个3119B独立程序冒作这两个原件。

三名单位提供者、34个不同单位客户、七个共同主题0,…,5,E6，E为空。固定完整SPE，强制根B~p后沿同σ得含全部三槽的Z(B)。真实根收益均值D(p)=E_Bu_1(Z(B))；额外第四位查询A~p独立，C(p)=E_(A,B)Σ_(x∈A)1/[1+c_x(Z(B))]。被否定的是每个完整SPE、每p均D≥C，不是每p实际最优u≥C。

## 数据与完整策略

前六主题为X0,X1,X2,Y0,Y1,Y2，客户mask及不同单位数为

| mask | 数量 | mask | 数量 |
| --- | ---: | --- | ---: |
| 4 | 1 | 27 | 4 |
| 29 | 3 | 30 | 3 |
| 31 | 2 | 32 | 1 |
| 43 | 3 | 45 | 3 |
| 46 | 3 | 51 | 3 |
| 53 | 3 | 54 | 3 |
| 59 | 2 | — | — |

基础六主题/34客户的[完整43节点SPE](../反例/三人逐人混合安全值--反例.md)已逐表证明。根0，第二人见首主题在X={0,1,2}取3，否则0；两非空历史(a,b)后末位取b所属组三标签最小未出现者。加入E后，首E的第二人取0；末位恰有一个非空a时用rho=(1,0,0,4,3,3)，双空取0。前述规则与[7992B全部57动作](DATA_JSON)逐条一致，尤其(a,E)不能误用全局最小标签；EO结构绑定已准确保该区别。

## 新增空历史的解析SPE检查

令U(t,a)=|T_t|−|T_t∩T_a|/2，为一个非空旧主题a加一个空行动之后，末位选择t的真实收益。六主题大小(23,23,21,23,23,21)，普通标签指0,1,3,4，特殊指2,5；同组普通对交14、普通/特殊对交11，跨组普通对交17、普通/特殊交14、特殊/特殊交12；这些由上表直接求和。故一空历史的rho及两名理性尾部首位收益为

| 非空a（或E） | rho(a) | 最后位最大收益 | 尾部首位选a后自身收益 |
| --- | ---: | ---: | ---: |
| 0 | 1 | 16 | 16 |
| 1 | 0 | 16 | 16 |
| 2 | 0 | 35/2 | 31/2 |
| 3 | 4 | 16 | 16 |
| 4 | 3 | 16 | 16 |
| 5 | 3 | 35/2 | 31/2 |
| E | 0 | 23 | 0 |

最后一行对应双空、最大主题0大小23。表中一空收益只依赖那个非空a，所以同时覆盖(a,E)与(E,a)共12个末位历史，双空再一，共13。空根后的第二人面对七个行动的真实收益为(16,16,31/2,16,16,31/2,0)，规定0最优，新增的第14个节点亦最佳。

旧43节点仍由原SPE控制所有非空偏离；新偏离E给当前收益0，不会改善非负的规定收益。根六个非空行动仍各得29/3，空根自身0，因此根0最优。此解析合并覆盖完整57历史，不要求匿名化一般SPE或排除离轨平局。actual(0,3,4)，利润(29/3,67/6,67/6)，W32；E不新增覆盖，原OPT3=34不变。

## 两条完整真实分支的精确负差

p(2)=1/10,p(E)=9/10。空根分支(E,0,1)中根收益0；主题2根分支(2,3,4)中根29/3。独立查询2对这两个**完整三槽**的价分别32/3和13/2，因此

\[
D=\frac1{10}\frac{29}3=\frac{29}{30},\quad
C=\frac1{10}\frac9{10}\frac{32}3+\frac1{100}\frac{13}2=\frac{41}{40},
\quad D-C=-\frac7{120}.
\]

u=29/3，u−C=1037/120>0，实际顺序D<C<u；原JSON kind中的NOT-C-LT-U不作数学真值，字段绑定/纠正在[完整证书资料](../资料/完整根查询证书的字段与审计范围--资料.md)。此例不否定实际u封顶、平均负载分数背景、自由额外槽值或half；一般WP另有不同银行输入反例，见[合法前缀归约](../引理/合法前缀的静态额外槽预算与条件归约--引理.md)，不能互相错认。

## 任意空根稀释的精确机制

任一允许空主题的完整原策略，固定合法T，令p(E)=1−epsilon,p(T)=epsilon，0<epsilon≤1。空源自身收益0、空查询价0，记g_T(Z)=Σ_(x∈T)1/[1+c_x(Z)]，则只剩三项

\[
D-C=\varepsilon[d_T-g_T(Z(E))]
+\varepsilon^2[g_T(Z(E))-g_T(Z(T))].\tag{EMPTY}
\]

所以a=g_T(Z(E))−d_T>0时，T必非空。其原根自身覆盖T的客户，使d_T−g_T(Z(T))=Σ_(x∈T)1/[c_x(Z(T))(1+c_x(Z(T)))]严格正；故二次系数b=g_T(Z(E))−g_T(Z(T))=a+[d_T−g_T(Z(T))]>a>0。负差恰发生在0<epsilon<a/b<1。空根后的真实尾本身是完整SPE，但根空行动一般非最优，不能删掉u−D这笔真实激励松弛。

本输入a1,b25/6，根部多项式−epsilon+25epsilon²/6，选1/10给−7/120。与三个actual位置合计的强预算多项式−epsilon+12epsilon²是不同目标；后者旧审计在1/24给−1/48，同1/10却+1/50。不能把根差值冒作整体失败值，更不能把强ΣG≤ΣD换成弱ΣG≤W。

## 发现轨迹与证据可复用范围

README称先有381客户JSON，后据空主题机制缩到34；381只为发现轨迹，本批本地未取得，不重构成新已证实例。原始搜索的浮点候选不凭exact文件名自获认证。k2复制弱例曾因少分母+1撤销，不能与这个保完整三槽再加查询1的真强反例合并。

本34输入同SHA的[既有3119B单位审计](../审查/额外槽扫描的实际强桥目标与两份定义级核验--审查.md)已真实成功核57节点399含自身/342非自身，EG又一次固定根算术核本节D/C。EO完整读其代码/旧执行/所有字段，EX字节复用而不重跑；这不是恢复本稿引用的另外3051B原程序。正文的新增空节点表与EMPTY是固定数据/双抽样的解析说明，不新增CLI、solver或SPE扫描。

强式失败不使源的弱式假设自动失败；当前WP普遍状态由独立银行反族决定，而一般half不因两者失败被否定。源README的下一步路线与未正式入库身份仅作历史；本轮完成的是完整保全证明、量词、发现/审查/实际已交证据之分，没有外审或新颖性认证。
'''
body2=body2.replace('SRC_MAIN',link(IDS[1])).replace('SRC_README',link(IDS[0])).replace('DATA_JSON','../../../../'+next(x['preserved_path'] for x in related if x['id']=='f218c3c894b4635ecca2'))
put(P2,head('empty-root-dilution-strong-push-failure-and-weak-bridge-scope','counterexample','反例','空根稀释的强推送失败与弱桥范围','complete-57-history-analytic-extension-and-general-two-point-identity; not-half-failure','保34客户加入空主题后的14新节点解析SPE论证、全部收益/真实分支与一般epsilon恒等式；固定强反例仍有u−C正松弛，旧搜索/缺失独审与已成功同SHA程序分开。',[IDS[0],IDS[1]])+body2)
js(E/'formal-resource-manifest.json',[{'path':str(p),'bytes':(S/p).stat().st_size,'sha256':sha((S/p).read_bytes())} for p in [P1,P2]]);cp(Path(__file__),E/'build_resources.py')
print(json.dumps({'claim_tip':claim['remote_tip'],'primary_bytes':sum(x['size'] for x in rows),'primary_lines':sum(x['lines'] for x in rows),'new_formals':2,'formal_bytes':sum((S/p).stat().st_size for p in [P1,P2]),'new_math_runs':0},ensure_ascii=False))
