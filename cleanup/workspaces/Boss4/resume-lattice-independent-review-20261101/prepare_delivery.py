from pathlib import Path
import json,hashlib
B=Path('/workspace/scratch/37f0f9248cfc/lattice-independent-review-staging')
R=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
W=B/'cleanup/workspaces/Boss4/resume-lattice-independent-review-20261101'
E=B/'archives/customer-attraction/subarchives/six-providers/tools/evidence/lattice-independent-review-primary'
S=B/'archives/customer-attraction/subarchives/six-providers/state'
ids=['9e3fb9dac56e91215d76','1c9328ee2dd9c1421567','76307e651db964a863ac']
rids=['3fb17764a6930667e3a2','b2cc74c6caa0cb212eb3','0d2f5d5b27d611918123']
inv=[json.loads(x) for x in (R/'cleanup/inventory.jsonl').read_text().splitlines()]
rows=[next(x for x in inv if x['id']==i) for i in ids+rids]
for d in rows:
 p=E/('original' if d['id'] in ids else 'related')/Path(d['path']).name
 z=p.read_bytes();assert len(z)==d['size'] and hashlib.sha256(z).hexdigest()==d['sha256']
 d['local_path']=str(p.relative_to(B));d['role']='primary' if d['id'] in ids else 'required-related'
(E/'source-manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(W/'owner-snapshot.json').write_text(json.dumps({'parent_claim_commit':'a72ad6703f2a236682cd365a764db3be92f77c6e','parent_reported_push':'pushed','parent_reported_local_sync':'synced','actual_clean_list_read':'--owner self --prefix research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/independent_review/ --full --limit 30','sources':[{'id':r['id'],'owner':'Boss4','disposition':'in-progress','source_sha256':r['sha256'],'request_id':'96c13c61ed3149d5ab3bb1bcc9ed1fc3','updated':1793522590} for r in rows if r['id'] in ids]},ensure_ascii=False,indent=2)+'\n')

def front(i,kind,tag,title,status,summary,legacy=[]):
 fs={'id':i,'kind':kind,'type_tag':tag,'title':title,'status':status,'review_level':'primary-independent-review-full-read;required-discovery-originals-compared;informed-analytic-reconstruction;no-current-math-rerun','summary':summary,'cleanup_primary_ids':ids}
 if legacy:fs['legacy_ids']=legacy
 text='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in fs.items())+'source_refs:\n'
 for r in rows:
  for x in r['sources']:text+='  - '+json.dumps('source:'+x['commit']+':'+x['path'],ensure_ascii=False)+'\n'
 return text+'---\n\n'
lemma=S/'引理/两层计数势端点配平的真实行双向支付--引理.md'
construction=S/'构造/十五客户完整策略的势循环严格扩大收益SCC空间--构造.md'
review=S/'审查/计数势格循环的独立Floyd审计与冻结证据--审查.md'
for p in [lemma,construction,review]:p.parent.mkdir(parents=True,exist_ok=True)
lemma.write_text(front('customer-attraction/potential-lattice-circulation-signed-real-row-payment','lemma','引理','两层计数势端点配平的真实行双向支付','proved-universal-row-algebra;not-global-half-payment','完整形式策略的真实行只要在总计数m及m−1两层势端点非负配平，正系数涉及行均可在原锥双向支付；包含收益SCC像空间，但不宣称穷尽lineality。',['LC-POTENTIAL-CIRCULATION-v1'])+r'''# 两层计数势端点配平的真实行双向支付

## 论域、真实行与两个表示层

固定任意m≥1、有限非空目录标签集[p]、一份定义于全部有序历史的完整形式策略σ。这里形式策略不预设已经由某份非负客户数据实现为SPE。每个有序历史h的当前规定行动a与强制行动b，分别沿**同一σ的真实后继**完成终局，得到总计数q、q′（均总和m）。不能把后继冻结，也不能自由添加没有原策略来源的比较边。标签可重复选择；同计数的不同历史仍可有不同续局。

类型坐标是所有非空兴趣集合B⊆[p]。记q(B)=Σ_{a∈B}q_a。若q_a>0，定义终局收益型向量

\[
F_{q,a}(B)=\begin{cases}1/q(B),&a\in B,\\0,&a\notin B.\end{cases}
\]

含a时q(B)≥q_a>0，不含a时直接取零而不是0/0。对非负整数客户类型重数w_B，角色行动a的利润为Σ_Bw_BF_{q,a}(B)。真实比较行为Γ_{h,b}=F_{q,a}−F_{q′,b}；σ若在w上是SPE，才另外有Γ_{h,b}·w≥0。以下相消恒等式是整个类型向量空间中的事实，比某一w上恰好收益平局更强。

令H₀=0、H_s=Σ_{j=1}^s1/j，势型向量P_q(B)=H_{q(B)}。逐类型有

\[
F_{q,a}=P_q-P_{q-e_a}.\tag{1}
\]

含a时是H_d−H_{d−1}=1/d；不含a时两负载相同，两边零。因此收益是同一个势的删除边际。

另在**未映射**的计数端点空间，以所有|q|=m与|r|=m−1的非负整数计数为两层基向量顶点，置

\[
I_{q,a}=e_q-e_{q-e_a},\qquad
\widetilde\Gamma_{h,b}=I_{q,a}-I_{q′,b}.
\]

线性映射L:e_v↦P_v满足L(I_{q,a})=F_{q,a}、L(\widetildeΓ)=Γ。未映射势端点的平衡，与映射后的型函数相消，以及收益顶点(q,a)本身的净流平衡，是三个不同层次。

## 非负势端点配平给原行锥双向方向

对全部有限个真实行编号j，设λ_j≥0且

\[
\sum_j\lambda_j\widetilde\Gamma_j=0.\tag{2}
\]

施L得到Σ_jλ_jΓ_j=0，逐类型恒成立。对任意λ_j>0的行移项：

\[
-\Gamma_j=\sum_{k\ne j}\frac{\lambda_k}{\lambda_j}\Gamma_k.\tag{3}
\]

右边只用原真实行且系数非负；Γ_j本身也在C=cone{Γ}中，所以Γ_j∈C∩(−C)。所有这种正系数涉及行的线性span，均包含于C的lineality（可双向线性子空间）；零行无需特殊除法。λ_j=0的行不能由该次组合取得负向。

该一般结论只依赖有限性、同一真实行集和共同删除势表示，不要求选定某份客户数据预先使σ为SPE；若要用于原客户吸引福利证明，仍须把这些行与该σ在实际输入上的全部激励及实际覆盖共同保持。相消不创造新的非负客户，不支付尚未进入证书的覆盖债务。

## 旧收益图SCC像空间为何被包含

旧收益图的顶点为(q,a)，真实行Γ_j给一条从偏离端点(q′,b)指向规定端点(q,a)的有向边。任何有向循环在这些收益顶点的形式基向量处净流零，映射(q,a)↦I_{q,a}后仍净流零，故满足(2)。SCC内每条边都处于某个有向循环，因而其映射行及负向均可由上述机制取得；同一SCC内任意两收益顶点之差又可沿真实有向路径表示。因此旧空间

\[
S_{\rm SCC}=\operatorname{span}\{F_v-F_w:v,w\text{在同一收益SCC}\}
\]

包含于该势配平机制得到的双向空间。

反向不自动成立：若不同收益顶点具有共用上下计数端点，它们可在I层再次抵消，而不在收益顶点自身配平。严格实例见[十五客户完整策略](../构造/十五客户完整策略的势循环严格扩大收益SCC空间--构造.md)。也不声称(2)穷尽全部lineality：L本身的核、即谐势型向量P_v间的额外依赖，可能使映射后的Γ再出现未在端点基空间抵消的相消。

## 六边三角源及真实嵌入限制

当m≥2、p≥3时，任取非负整数背景r，|r|=m−2，以及三个不同标签a,b,c。令q_ab=r+e_a+e_b，类似定义q_bc、q_ca。式(1)给

\[
\begin{aligned}
F_{q_{ab},a}-F_{q_{ab},b}&=P_{r+e_a}-P_{r+e_b},\\
F_{q_{bc},b}-F_{q_{bc},c}&=P_{r+e_b}-P_{r+e_c},\\
F_{q_{ca},c}-F_{q_{ca},a}&=P_{r+e_c}-P_{r+e_a}.
\end{aligned}
\]

三项和为零。这在两计数层形成六边循环；实际上对这些端点任意共同势Ψ，定义删除边际后同样望远镜。m=1或p<3不使用此三标签构造，一般机制(2)仍有效。

但这三个同终局收益差**未必各自是σ的真实比较行**。福利证书不能因为型函数相等就凭空加入行，必须把整项相消嵌入同一完整策略的真实节点。本档十五客户构造用四条真实行实现该三角源，且所有客户类型均为正整数。

## 接续义务、来源和证据身份

对任意σ、任意至多m个比较主题，half证书仍需共同选择λ,r≥0，使型向量2c−o=Γᵀλ+r；c、o分别是实际覆盖与比较覆盖指标。新双向空间只增加重选真实行乘子的自由度，未证明这种证书对任意σ总存在，也不因收益图凝聚为DAG就使映射行锥pointed。

原7624B发现稿与2948B独立审稿均全文读；后者明示先独立重建谐势差分后读稿，承认机制普遍性与非穷尽边界。本页为知情自足重构，未把原内部先后扩称外审或新颖性认证。三主源的原字节及独立实现实际范围见[独立Floyd审查](../审查/计数势格循环的独立Floyd审计与冻结证据--审查.md)。本次未运行原审计或新数学实现。

与父档[共同删除势全域效率](../../../../state/定理/共同删除势的全域效率与单调次模提升--定理.md)共享删除边际表示，但本引理只需固定两层，既不证明共同客户非负表示，也不依赖其全域效率/DR刻画；与[全树收益流表示边界](../../../../state/资料/全树收益流与势类攻击的共同表示边界--资料.md)的势四端点投影相容。覆盖矩signed span的维数也不等于本页非负真实行锥的lineality，不能混为同一结论。
''')
# This is a lossless table reformat of already-read frozen data, not a payoff/IC computation.
discovery=json.loads((E/'related/lattice_circulation_audit.json').read_text())
slackrows=[]
for i in range(0,len(discovery['all_exact_slacks']),3):
 part=discovery['all_exact_slacks'][i:i+3]
 h=''.join('ABC'[x] for x in part[0]['history']) or '∅'
 slackrows.append('| '+h+' | '+' | '.join(x['slack'] for x in part)+' |')
slacktable='\n'.join(slackrows)
construction.write_text(front('customer-attraction/fifteen-customer-SPE-potential-circulation-strict-SCC-expansion','construction','构造','十五客户完整策略的势循环严格扩大收益SCC空间','proved-complete-pure-SPE-and-strict-inclusion;not-half-counterexample','三主题15单位客户完整13历史策略，39真实比较均非负；四行逐类型零和，根行AB坐标不在唯一非平凡SCC的一维像空间，严格扩张但不求完整维数。',['LC-SCC-STRICT-v1'])+r'''# 十五客户完整策略的势循环严格扩大收益SCC空间

## 单位客户、全部策略与实际福利

三名单位权提供者，按顺序从共同目录{A,B,C}各选一次，观察全部有序历史。七个非空兴趣类型按(A,B,AB,C,AC,BC,ABC)排列，重数

\[
w=(3,2,3,2,3,1,1).
\]

每份重数表示不同单位客户，总15名；三标签均有正私有客户，覆盖两两不同，不是把相同覆盖标签当不同主题。重复行动保留。构造只证存在这份完整纯SPE，不声称所有平局产生相同实际路径。

根选A；第二人见A、B、C后分别选C、A、A。末位全部九历史的规定动作是：

| 第一 / 第二 | A | B | C |
|---|---|---|---|
| A | C | A | A |
| B | A | A | A |
| C | B | A | A |

连根和三个第二层节点共13个有序决策历史；不是匿名计数策略替代全部历史。实际路径ACA，总计数q₁=(2,0,1)。两个选A者各得

\[
3/2+3/2+3/3+1/3=13/3;
\]

选C者得2+3/3+1+1/3=13/3。因此W=13，恰漏B私有两客户。选择A,B,C覆盖全部15客户，故OPT₃=15，且2W−OPT₃=11>0。本例严格扩张付款空间，不是half反例，更不是直接的六人实例。

## 全部39项真实比较的有限解析证书

记Zσ(h)为给定历史后沿上表真实完成，角色i=|h|+1。对每个h、每个b∈{A,B,C}，真实松弛

\[
\delta_{h,b}=u_i(Z_\sigma(h))-u_i(Z_\sigma(h,b))
=\sum_{D\ne\varnothing}w_D\,[F_{q,a}(D)-F_{q',b}(D)],
\]

其中a是h的规定动作，q,q′从同一表完成获得；F的定义与正分母见[势配平引理](../引理/两层计数势端点配平的真实行双向支付--引理.md)。下表逐行列完13×3项（含自身），是冻结发现证书完整39值的无损重排；每项均可按上式直接复核，并非新程序运行结果。

| 历史h | 改A松弛 | 改B松弛 | 改C松弛 |
|---|---:|---:|---:|
'''+slacktable+r'''

所有值非负，故每个有序子博弈当前规定行动相对全部合法动作均最优。每人只在自己的层移动一次，完整策略于是为纯SPE。最小松弛零；根三个行动、若干离轨行动确有平局，不能改写为严格唯一均衡。有限39项证书只认证这一个固定输入，不承担普遍机制的所有m,p量词。

## 四条原真实行与势端点平衡

以下所有行均指同一完整策略；按七兴趣类型顺序：

\[
\begin{aligned}
g_0=\Gamma_{\varnothing,B}&=(1/2,-1,1/6,0,1/3,-1,0),\\
g_1=\Gamma_{A,A}&=(-1/2,0,-1/2,1,0,1,0),\\
g_2=\Gamma_{B,C}&=(1/2,0,1/3,-1,0,-1/2,0),\\
g_3=\Gamma_{CA,A}&=(-1/2,1,0,0,-1/3,1/2,0).
\end{aligned}
\]

设q₂=(2,1,0)、q₃=(1,1,1)。逐个真实完成对应为：

| 行 | 规定完成与当前行动 | 偏离完成与当前行动 |
|---|---|---|
| g₀：根改B | ACA，A，q₁ | BAA，B，q₂ |
| g₁：A后改A | ACA，C，q₁ | AAC，A，q₁ |
| g₂：B后改C | BAA，A，q₂ | BCA，C，q₃ |
| g₃：CA后改A | CAB，B，q₃ | CAA，A，q₁ |

所以g₀=F_{q₁,A}−F_{q₂,B}，g₁=F_{q₁,C}−F_{q₁,A}，g₂=F_{q₂,A}−F_{q₃,C}，g₃=F_{q₃,B}−F_{q₁,A}，且

\[
g_0+g_1+g_2+g_3=0\quad\text{逐类型恒成立}.\tag{4}
\]

每行在w上也取零。其总和重排为

\[
[F_{q_1,C}-F_{q_1,A}]+[F_{q_2,A}-F_{q_2,B}]+[F_{q_3,B}-F_{q_3,C}],
\]

正是势配平引理取背景r=e_A、三角标签顺序(C,A,B)的六边源。因此所有未映射势端点精确配平，λ₀=λ₁=λ₂=λ₃=1合法；收益顶点本身却未净流配平。由(4)，−g₀=g₁+g₂+g₃，故根行的负向能由三条原真实行非负支付。

## 完整收益图的十八端点与唯一非平凡SCC

收益顶点(q,a)中的q是终局计数，不是当前历史计数；真实边从偏离端点指向规定端点。下面以三位计数串q_Aq_Bq_C:a表示顶点，列出由全部39比较合并所得邻接，省略所有自环与重复边。该表可直接由13动作表的真实完成逐项获得，不用把程序的SCC断言当唯一理由。

| 收益顶点 | 非自环后继 |
|---|---|
| 300:A | 201:C |
| 210:A | ∅ |
| 210:B | 201:A，201:C |
| 201:A | 201:C，111:B |
| 201:C | ∅ |
| 120:A | ∅ |
| 120:B | 210:A |
| 111:A | ∅ |
| 111:B | 201:A，111:A |
| 111:C | 201:A，210:A |
| 102:A | ∅ |
| 102:C | 201:A，111:A，111:B |
| 030:B | 120:A |
| 021:B | 111:A |
| 021:C | 120:A |
| 012:B | 102:A |
| 012:C | 111:A |
| 003:C | 102:A |

201:A与111:B互相可达，外出仅达汇点201:C或111:A；其余非汇点只指向汇点或这两个顶点，且没有回到自身的非平凡路径。因此唯一非单点SCC恰为{((2,0,1),A),((1,1,1),B)}。其收益像空间是span{F_{q₃,B}−F_{q₁,A}}=span{g₃}；g₃的A坐标−1/2非零，故维数恰一。

但g₀的AB坐标1/6，而g₃的AB坐标零，所以g₀不在旧SCC像空间。g₀本身是原非负行锥C=cone{Γ}的生成行，(4)又给−g₀∈C，因此g₀∈C∩(−C)。结合[一般包含](../引理/两层计数势端点配平的真实行双向支付--引理.md)，得到旧SCC像空间严格包含于完整真实行锥的lineality，至少新增一个独立方向。

本页不声称完整lineality精确维数等于二；“SCC空间秩1、加入根行秩2”只给严格扩张见证。也不称势端点循环已穷尽所有双向方向。

## 原独立审查、发现工具和接续边界

2948B原审稿独立重建差分后读发现稿，再跟随四个真实节点核上述端点及逐类型行；4138B独立实现以Floyd–Warshall闭包区别于发现审计逐节点DFS，940B冻结报告给同一非平凡SCC、四行、13/39和W13/OPT15。实际代码/JSON范围详见[独立Floyd审查资源](../审查/计数势格循环的独立Floyd审计与冻结证据--审查.md)；本次不重复已成功有限原程序、未造新运行日志。

两个浮点发现探针仅提供候选来源，见[两种发现探针](../程序/真实行锥额外双向空间的两种发现探针--程序.md)。相关原稿称distinct探针seed840013、trial29找到本例，这是母稿历史而非本次运行；二主题先前候选迫同覆盖，不承担本页三主题两两不同覆盖的结论。probe程序是否精确后验、上限与实际字段按其自己的资源对象判断，不借本页实现认证全部搜索。

本例适用于一般全树付款机制，但不因归在六人子档就改成六人SPE，也不能无证明加dummy提供者迁移。一般half仍需任意真实σ上对实际与比较覆盖共同寻找非负行组合和逐类型非负余项。额外有符号自由度本身不提供这一全称付款。

来源：主独立审稿及三required-related发现稿/代码/全slack JSON均全文实读；本页完整保策略、客户、39比较、四行、十八端点、严格性及状态。原新颖性和外审未认证；源ref与版本见frontmatter。
''')
review.write_text(front('customer-attraction/lattice-circulation-independent-Floyd-review-original-evidence','review','审查','计数势格循环的独立Floyd审计与冻结证据','complete-three-primary-review;historical-finite-success-preserved;zero-current-math-runs','保独立重构先后、4138B独立单位客户/Floyd实现和940B全部报告字段；与5825B发现审计的111三角回归/秩/势端点检查分开。')+r'''# 计数势格循环的独立Floyd审计与冻结证据

## 三主源和当前完整阅读

本批实际正式owner为Boss4；parent claim commit a72ad6703f2a236682cd365a764db3be92f77c6e返回pushed/local_sync=synced，随后实际clean list全文读取三ID的owner、request_id与source SHA。原件共8026B：

| 源ID | 文件 | 字节 | 本对象中的用途 |
|---|---|---:|---|
| 9e3fb9dac56e91215d76 | lattice_review.json | 940 | 独立原实现冻结报告全部字段 |
| 1c9328ee2dd9c1421567 | lattice_review.md | 2948 | 独立谐势重构、严格实例审查及边界 |
| 76307e651db964a863ac | lattice_review.py | 4138 | 单位客户真实IC/Floyd闭包独立实现 |

均通过正常clean show实际全文读并独立导出到[证据目录](../../tools/evidence/lattice-independent-review-primary/README.md)，大小/SHA按冻结inventory核实。required-related另全文读7624B发现主稿、5825B发现审计、6400B完整输出（含13动作和全部39松弛），不额外为它们receipt/done。此前入口写“已保全”不能代替这些完整数学；全仓检索未见此前完整势配平或严格实例对象，故本次将一般证明与实例独立落成[引理](../引理/两层计数势端点配平的真实行双向支付--引理.md)及[构造](../构造/十五客户完整策略的势循环严格扩大收益SCC空间--构造.md)。

## 2948B审稿的实质和先验范围

原审稿明示“独立重建谐势差分后读稿”，之后逐真实节点核实例；它从H_d−H_{d−1}=1/d重构F=P−P删除式、未映射势端点非负配平、正系数行移项成为其他真实行非负和，说明旧SCC像空间包含于新机制，而谐势P本身依赖仍可能造成更多lineality。三标签、总背景m−2的三角源只在m≥2存在；任意势的代数源仍须嵌入原真实策略行。

实例审查保七类型重数(3,2,3,2,3,1,1)、全部13有序节点、根B/A后A/B后C/CA后A四真实行，以及根行AB坐标1/6与SCC生成行AB零。准确结论是存在一份真实SPE，完整行锥双向空间严格大于旧SCC像空间；没有完整精确维数、一般half付款或外审/新颖性结论。

本次先读该稿再对照发现稿，是知情重构；不把原作者自述读序冒成本次盲审，不补造收题日志。其“未见致命异议”只覆盖机制与该严格实例，不代替全仓目标的真值。

## 4138B独立实现的全部计算合同

代码只import标准库Fraction、product、Path、argparse、json；不导入发现审计、规范模型、solver或优化器。run()内独立抄入A=0,B=1,C=2的完整13动作表与七客户类型，按重数展开15个不同单位客户。histories生成所有长度0/1/2的有序词，assert键域等于动作表；follow沿同一表补到长度3。

utility逐单位客户对当前行动喜欢者加1/最终覆盖次数；分母因该行动确在终局而正。endpoint(history,action)先强制当前动作再follow，回传最终计数q与**当前强制标签**；不能把标签换成末位动作。type_row对非空位掩码1…7取指示/总覆盖，含当前标签才取倒数。

遍历每个history及三个行动（含自身），直接核规定真实续局效用≥强制后的真实效用，收39个slack；同时记录型行target−source和收益边source→target。正利润比较只针对这份明确三人输入与动作映射，不是穷尽所有SPE。

它把所有收益端点排序，reach初值含零长可达和真实边，然后三重Floyd–Warshall闭包；以双向可达分组SCC，assert唯一非平凡组为[((1,1,1),1),((2,0,1),0)]。该实现和发现审计逐起点DFS不同，确有独立代码路径，不是复制同一源码重放。

随后选根改B、A后改A、B后改C、CA后改A四型行，逐坐标assert和为零；取SCC两顶点型函数差，assert其非零、AB坐标零而根行AB=1/6。这无需另调用秩库，已构成一维旧空间外新向量的充分见证；没有计算完整lineality精确维数，也没有构造两层势incidence或普遍三角回归。

最后assert实际三个角色各13/3，直接计算实际覆盖13；枚举全部3³=27个合法终局行动组合求最优覆盖15。枚举27元组不是枚举全部完整策略。程序输出最小slack0及下节报告，未输出全部39松弛或完整动作表；这些完整有限表只在related发现输出另保。

CLI有main guard。默认仅stdout打印紧凑JSON；可给--output路径，使用open('x')排他创建，再缩进写JSON并加换行。目标已存在会失败，不静默覆盖。import只定义run，不自动运行；但本次也未import。CLI及输出副作用与amount族顶层直接写同目录JSON的程序不同，不能类推。

## 原940B报告的全部字段

| 字段 | 冻结原值 |
|---|---|
| status | independently verified; no fatal objection |
| unit_customers | 15 |
| ordered_histories | 13 |
| all_action_comparisons | 39 |
| minimum_slack | 0（分数字符串） |
| only_nontrivial_payoff_SCC | [[((1,1,1),1),((2,0,1),0)]]，JSON中tuple为list |
| zero_combination_rows | 下列四个七维分数字符串向量 |
| root_row_outside_SCC_space | AB coordinate root=1/6, SCC generator=0 |
| welfare / OPT | 13 / 15 |
| general_half | OPEN（当时一般目标状态） |

四行完整为：

\[
\begin{aligned}
&(1/2,-1,1/6,0,1/3,-1,0),\\
&(-1/2,0,-1/2,1,0,1,0),\\
&(1/2,0,1/3,-1,0,-1/2,0),\\
&(-1/2,1,0,0,-1/3,1/2,0).
\end{aligned}
\]

共11根字段全部保留，没有另藏完整策略、全slacks、代码SHA、argv、环境或exit日志。status是冻结报告原字符串，不是本次重新执行的认证标签。文件内容与4138B源码返回字段及原审稿一致；当前未重新运行以宣称这两件刚刚逐字节配对产生。

## 与发现审计的真实差别

5825Brelated audit_lattice_circulation.py也不import规范包，从真实终局算型行后，另展开15客户把每次单位效用差与型行内积相等核一次；DFS逐顶点求可达/SCC，精确有理消元核旧像空间rank1、加入根行rank2；还显式核四行对应势incidence全端点平衡。它对p=3…5、m=2…5、|r|=m−2的背景计数，固定三标签测试普遍三角公式，原输出111个有限回归。111不是全部p,m证明，后者由引理承担。

6400B发现输出额外有actual ACA、三个13/3、13完整动作、39全部松弛、两项rank、空potential_endpoint_balance与triangle_regressions111。独立940B报告没有这些字段；不能把发现审计的秩/势端点/三角检查或39松弛输出加到独立实现的实际运行范围。两份输出相互一致，但不是相同字节或同一个脚本版本。

本次数学general proof、十八收益端点邻接和严格空间判断通过正文自足推导呈现；已有成功有限原记录无新疑点，因此不重复原审计、发现程序、独立run、全39算术或新SPE/LP搜索。当前运行只为取源、字节/链接/记录核查；没有新数学成功stdout/exit日志可声称。

## 关系判断与未付义务

共同模型提供完整历史/真实续局；一般势配平引理解释新机制；十五客户构造把三角嵌入四真实行；独立代码和冻结JSON分别是实现与历史有限证据；双探针只供候选来源。与覆盖矩signed span、共同势全域效率/DR同享表示，但没有相互推出非负真实付款锥。三级超图留父Boss/阶段三串行判断，本批只保存逐关系证据，不因有链接自动造推导边。

三人实例不能无证明迁移成六人。一般half仍缺对任意σ共同控制2c−o的非负余项；更大lineality不自动完成它。原主稿“独审待回执”是较早状态，2948B后续审稿确已给内部无实质异议；外审和新颖性始终未认证。一般任意人数OPEN不覆盖现已另有五人定理的状态，本对象未继承旧入口作为当前全人数状态表。
''')
(E/'README.md').write_text('''# 计数势格循环的独立审查原件

正式资源见[独立Floyd审查](../../../state/审查/计数势格循环的独立Floyd审计与冻结证据--审查.md)，数学见[势配平引理](../../../state/引理/两层计数势端点配平的真实行双向支付--引理.md)和[十五客户构造](../../../state/构造/十五客户完整策略的势循环严格扩大收益SCC空间--构造.md)。

三primary共8026B：[940B报告](original/lattice_review.json)、[2948B审稿](original/lattice_review.md)、[4138B独立程序](original/lattice_review.py)，均正常show全文读/导出、大小与SHA核实，所有冻结版本定位见source-manifest.json。程序有main guard和可选--output排他新建路径；本次未运行/import。

三required-related共19849B：[7624B发现稿](related/count_lattice_circulation.md)、[5825B发现审计](related/audit_lattice_circulation.py)、[6400B全策略/39slack输出](related/lattice_circulation_audit.json)均完整读并留原字节，只作比较，不在本3源receipt/done。

原940B报告为历史成功有限记录，不含代码SHA、argv、环境或exit日志。本次未造新运行；发现审计的111三角回归/秩/势端点检查不能算进独立Floyd实现范围。全部一般量词由解析引理证明，实例完整SPE由13动作与39非负松弛表呈现；严格SCC由完整18端点邻接表呈现。
''')
(E/'execution-scope.json').write_text(json.dumps({'primary_full_reads':3,'primary_bytes':8026,'required_related_full_reads':3,'required_related_bytes':19849,'current_original_cli_runs':0,'current_original_imports':0,'current_new_math_implementations':0,'current_IC_or_payoff_replays':0,'current_LP_or_SPE_searches':0,'current_checks':'size/SHA, records, source refs and links only','data_reformat':'39 already-read frozen discovery slacks copied losslessly into Markdown; no recomputation','historical_independent_audit':'15 clients,13 histories,39 comparisons,Floyd SCC,four row sum,AB separation,profits13/3 and OPT over27 paths','historical_discovery_audit':'different DFS,exact ranks,potential endpoint balance,111 triangle regressions,complete strategy/slacks','analytical_addition':'explicit 18-payoff-endpoint adjacency table proves unique SCC without invoking original code','new_external_stage_only':True},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'formal_paths':[str(p.relative_to(B)) for p in [lemma,construction,review]],'primary_bytes':8026,'original_runs':0},ensure_ascii=False))
