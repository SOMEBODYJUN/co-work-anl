from pathlib import Path
import json,hashlib,shutil,re
root=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
ws=root/'cleanup/workspaces/Boss4/resume-amount-family-20261101'
ev=root/'archives/customer-attraction/subarchives/six-providers/tools/evidence/amount-cap-one-family-primary'
old=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-amount-cap-one-family-certificate-and-reviews-primary')
oldev=old/'archives/customer-attraction/tools/evidence/amount-cap-one-family-certificate-and-reviews-primary'
meta=json.loads(Path('/workspace/scratch/37f0f9248cfc/boss4-active-resume.json').read_text())
ids=['44ac5a996de190a8da48','110a1ed1af682948ed17','c98e8355f192f5614a31','a4a99bb614912c545bd9','877bcf0bef8f85435968']
rows=[next(x for x in meta if x['id']==sid) for sid in ids]
for r in rows:
    tail='/'.join(r['path'].split('/')[-2:])
    p=ev/'original'/tail
    data=p.read_bytes()
    assert len(data)==r['size'] and hashlib.sha256(data).hexdigest()==r['sha256']
    q=oldev/'original'/r['path']
    assert data==q.read_bytes()
shutil.copyfile(oldev/'certificate-structural-readout.json',ev/'prior-certificate-structural-readout.json')
prior=json.loads((oldev/'execution-and-review-scope.json').read_text())
(ev/'prior-execution-and-review-scope.json').write_text(json.dumps(prior,ensure_ascii=False,indent=2)+'\n')
(ev/'source-manifest.json').write_text(json.dumps([{**{k:r[k] for k in ('id','path','sha256','size','blob','sources')},'local_path':str((ev/'original'/'/'.join(r['path'].split('/')[-2:])).relative_to(root)),'prior_cached_original_same_bytes':True} for r in rows],ensure_ascii=False,indent=2)+'\n')
refs=[]
for r in rows:
    refs += ['source:'+s['commit']+':'+s['path'] for s in r['sources']]
front='---\nid: "customer-attraction/amount-cap1-family-400-node-certificate-and-review-reading-order"\nkind: "program"\ntype_tag: "程序"\ntitle: "金额cap1完整策略锐族的原程序、四百动作证书与双审查"\nstatus: "complete-source-and-certificate-reading;no-new-mathematical-run"\ntruth_status: "analytic-all-n-family;fixed-six-person-corollary;frozen-n3-certificate"\nreview_level: "five-frozen-primary-full-read;informed-analytic-reconstruction;prior-same-SHA-structural-evidence-reused"\nscope: "有限单位客户和共同目录；全n≥3、m=n+1；存在一份全部有序历史纯SPE；六人取n=5"\nsummary: "保完整全n策略与金额反合同、原3332B生成器、n3全部400动作、双原审查和六人列比3/2；统一cap2锐性不冒固定六人锐性，有限记录不冒一般证明。"\ncleanup_primary_ids: '+json.dumps(ids)+'\nsource_refs:\n'+''.join('  - '+json.dumps(x,ensure_ascii=False)+'\n' for x in refs)+'---\n\n'
intro=r'''# 金额cap1完整策略锐族的原程序、四百动作证书与双审查

本对象保存一个精确辅助合同的反族及其实际研究资源。作者稿的全n数学此前已完整进入父档[末层多孩子金额预算的锐两倍列容量](../../../../state/定理/末层多孩子金额预算的锐两倍列容量--定理.md)；本次不把它重认作新发现。这里把原3332B程序、36652B完整动作证书及两篇原审查正式连回该数学，并明确六人子问题可复用的代入值。

五件冻结主源共54013B：作者稿6880B、代码3332B、JSON36652B、credible审3622B、independent审3527B。本次均用`work.py clean show`实际读取并各自导出；JSON全部16字段、三请求和400动作已逐条读到，不把首轮截断的show当全文。全部原件链接在[证据说明](../../tools/evidence/amount-cap-one-family-primary/README.md)，十个冻结提交/路径引用见frontmatter。另核对同SHA旧缓存原件及其已经通过的结构readout；本次不再重复该结构遍历或原有数学运行。

## 精确候选、完整条件与被反驳的量词

模型是有限单位客户集N、有限非空共同目录S、m名单位权提供者依次观察全部有序历史各选一次主题；重复选择允许，利润是所选主题每客户的1/最终覆盖人数，福利为覆盖客户数。完整纯SPE要求**每个**有序历史h、每个合法当前主题T，规定行动沿同一策略σ的真实后继利润不小于强制T后沿同一σ的真实后继利润。以下只构造存在的一份合法σ，不声称所有平局都产生预定叶。通用模型允许空主题与零客户；反族本身选用下述非空正客户输入。

固定该σ的实际根叶P。分枝α=(iα,Tα)在P的真实前缀P_<iα处强制主题Tα，随后沿同一σ完成Wα；同一cut允许多个不同forced主题。对j<iα≤l定义

\[
q_{\alpha,jl}=\sum_{x\in P_j\cap(P_l\setminus W_{\alpha,l})}
\frac1{c_P(x)c_{W_\alpha}(x)},\qquad
p_j(F)=\sum_{x\in F_j}\frac1{c_F(x)}.
\]

sender j在cut前主题不变，故q中的两个分母均正。非负λ的**共同金额预算**是

\[
\sum_{\alpha:j<i_\alpha}\lambda_{\alpha,j}p_j(W_\alpha)\le p_j(P)
\qquad\text{对每个sender }j.\tag{AMOUNT}
\]

被否定的AMOUNT-CAP1声称对所有这样的输入、完整σ及λ，每个recipient l均有

\[
\sum_{\alpha:i_\alpha\le l}\sum_{j<i_\alpha}
\lambda_{\alpha,j}q_{\alpha,jl}\le p_l(P).\tag{CAP1?}
\]

本族使用不同sender的不同孩子，并有λ>1。它不反驳固定**同一个W**且每个sender系数≤1的旧列次随机合同：对x∈P_l\W_l，cut前含x的sender数k_x≤c_W(x)，故其共同贡献≤k_x/[c_P(x)c_W(x)]≤1/c_P(x)，求和仍≤p_l(P)。不能把金额预算擅自改成系数逐项≤1，也不能把同cut不同主题删成只剩一个孩子。

## 全n构造及全部有序历史的自足证明

任取整数n≥3，m=n+1。客户块X₁,…,X_n,Y₁,…,Y_n两两不交，|X_j|=2、|Y_j|=2(n−1)，每客户价值一。共同目录恰2n+1个主题

\[
A_j=X_j\cup Y_j,\quad T_j=Y_j\ (1\le j\le n),\qquad D=\bigcup_jX_j.
\]

故|A_j|=|D|=2n，|T_j|=2n−2，总客户2n²。预定实际叶P=(A₁,…,A_n,D)。称有序历史fresh-A，当且仅当全部已选主题是两两不同的A_j，空历史也算。按有限树从叶向根构造σ：长度t<n的fresh历史选最小未用A；长度n的fresh历史选D；其它历史在已构造的真实孩子中选当前利润最大的行动，平局选固定标签序最小者。

历史一旦出现T、D或重复A，该缺陷在所有后代永久保留，因此非fresh节点构成封闭子树，逆向构造在全部这类节点满足IC。必须核验fresh override也最优。

长度n的fresh历史中所有A已各一次；末位D得n，任意A重复得|A|/2=n，任意T得n−1，所以D为允许的最佳回复，与A平局，并非严格最佳。

长度t<n的fresh历史，按规定选新A后仍fresh，最后全部A各一次、末位D，当前得2n−1。所有偏离类型分别为：

- 另一未用A：仍沿fresh路径补齐，收益同为2n−1。
- 已用A：已有同主题旧玩家，任何最终后继下每客户份额至多1/2，总收益≤n。
- 任意T：无论后继如何总收益≤|T|=2n−2。
- t≥1时选D：至少一块X已被旧A覆盖，当前在该两客户块至多得1；其余n−1块各至多得2，合计≤2n−1。
- t=0根选D：进入上述已由BI完整补全的非fresh子树。其真实末位不可能选T_j，因为同一末位历史下选A_j保留完全相同的Y_j收益并从正X_j份额严格增益。末位只能选某A或D，必再覆盖至少一块X，根D在该块至多得1，余块各至多2，仍≤2n−1。

根D一项调用真实离轨末位的最佳回复，不冻结后继，也不假定偏离后平局有利。全部fresh override最优，其它节点按BI最优，所以σ确为全部有序历史纯SPE，覆盖任意重复、T和D历史。

P中每个sender j≤n的X份额1、Y份额2n−2，故p_j(P)=2n−1；末位D在每块X得1，p_m(P)=n。前n个A已覆盖全部2n²名客户，因而

\[
W(P)=\mathrm{OPT}_m=2n^2.
\]

对每个sender j单独取同末位cut的合法forced孩子α_j=(m,T_j)，Wαj=(A₁,…,A_n,T_j)。forced动作不要求本身是最佳回复；σ只须使规定D不劣于它。孩子中X_j由A_j独占得2，Y_j由A_j,T_j均分得n−1，故p_j(Wαj)=n+1。标准q仅有X_j两名客户，c_P=2、c_W=1，所以q_{α_j,jm}=1。

仅令λ_{α_j,j}=(2n−1)/(n+1)，其它系数零，则每个sender的AMOUNT恰满额，而同一末位收到

\[
\sum_j\lambda_{\alpha_j,j}q_{\alpha_j,jm}
=\frac{n(2n-1)}{n+1}
=\left(2-\frac3{n+1}\right)p_m(P)>p_m(P).
\]

故CAP1?全称被否定。列比随n趋二，配合父档已证TERMINAL-CAP2，只证明**跨全部人数的统一常数二**不能减小；不证明任意固定m的最佳常数二。本族W=OPT，因此没有目标half反例。

## 六人代入及更深分支的接续边界

透明代入n=5即给六人、11主题、50名单位客户的完整策略实例：各X块2客户、Y块8客户，实际利润(9,9,9,9,9,5)。每个对应孩子的sender利润6，λ=3/2、q=1，五个sender满额各花9，末位正价15/2>5，列比3/2；W=OPT₆=50。这由上节一般证明直接代入，未运行n5全树，也不将n3证书叫六人证书；它表明六人AMOUNT-CAP1也失败，而恰六人half仍未被本族反驳。

父档TERMINAL-CAP2的上界允许任意合法父叶、不需SPE：只变末位有p_j(W)≥p_j(P)/2，故非零sender的Σλ≤2；对末位覆盖且原负载c≥2的客户，离开的末位使孩子负载c−1，prefix coverer恰c−1个，合计≤2/c。零sender主题无客户，q=0，不除零。该一般上界和本族锐性是不同承重证明。

实际读过的后续[deep交接](../../tools/evidence/amount-cap-one-family-primary/related/deep_amount_handoff.md)保持DEEP-CAP2开放：允许任意cut及真实多位后继时，“负载最多增一”“移走即c_W=c_P−1”均不再保证。固定实例/σ/列l的金额最大值确为

\[
\sum_{j<l}p_j(P)\max_{\alpha:j<i_\alpha\le l}
\frac{q_{\alpha,jl}}{p_j(W_\alpha)},
\]

空最大值取0；零分母时sender主题无客户，q亦零而略去。不同列可以由不同λ取最大，不能说有同一λ同时实现所有列最坏。一般仍需真实后继IC的联合关系。

已读[粗界原稿](../../tools/evidence/amount-cap-one-family-primary/related/deep_amount_bound_check.md)只用c_P≥2给q≤p_j(W)/2，于是列输出≤(1/2)Σ_{j<l}p_j(P)。它不需SPE；仅当该prefix总利润≤4p_l(P)时足够列cap2，原模型没有这项一般已证比例。AMOUNT本身还给所有recipient总正价≤Σ_jp_j(P)≤W(P)，不是一笔新的总资金。即使DEEP-CAP2后来成立，仍须将真实覆盖债务初始化进AMOUNT，并扣除direct/suffix已有支出，不能从列系数二直接推half。

'''
oldtext=(old/'archives/customer-attraction/state/程序/金额cap1锐族的四百节点原证书与审查读序--程序.md').read_text()
a=oldtext.index('## 原3332B生成器的全部输入与执行顺序')
b=oldtext.index('## 本批处置与当前限度')
body=oldtext[a:b]
body=body.replace('[父方原筛查合同](跨枝金额列容量原筛查的完整策略与输入过滤合同--程序.md)','[父方原筛查合同](../../../../state/程序/跨枝金额列容量原筛查的完整策略与输入过滤合同--程序.md)')
body=body.replace('本批结构核对这些动作的history键域','此前同SHA结构核对记录显示这些动作的history键域')
body=body.replace('当前没有另生一次数学成功日志','本次没有另生一次数学成功日志')
last=r'''## 逐源处置、实际运行与关系证据

作者稿主数学在父档定理已有完整去向，本次再逐式重构以核一般条件和六人适用性，处置为duplicate；原3332B程序、36652B完整证书与双原审查处置为retained，由本程序对象及五份原件保存独有输入、全动作表和证据身份。没有修改旧定理或他人文件。双review均是同actor内部解析重构；independent明示先重构后对照，可信先后仅按原稿记录，不补造收题日志、严格盲审或外审。independent的历史n3运行是原样脚本重放，父方同字节重放也只按作者陈述保存，不叫独立实现。

本次实读五源后，完整比较父档模型、末层锐cap2定理、父方原筛查程序合同、两份后续deep原稿和后续wallet_review.md。未发现它们对本族的数学纠错；后续审查仍确认末层容量，明确初始化/共同钱包/deep未付。源码和JSON同SHA旧缓存已定位：旧结构PASS只验证400动作键域、标签、排序、实际链，旧execution记录明确入口/import/payoff/IC均为0。现原件逐文件大小/SHA及与该缓存全字节相等已重新核；故精确复用[原结构readout](../../tools/evidence/amount-cap-one-family-primary/prior-certificate-structural-readout.json)，不再跑同一遍结构扫描，也没有声称400/2800项当前数学复验。

本次原入口0、import0、payoff/IC重算0、新数学实现0、LP/SPE搜索0；只运行取源、字节/链接/清洗记录检查。冻结JSON没有代码SHA、argv、环境和exit日志，不能倒填这类运行绑定。全部一般数学由上述完整证明和父档定理承担，n3有限证据只证明它实际保存的一份表及报告，六人代入由n5解析特化承担。

关系已逐项判断：共同目录完整历史模型提供精确策略量词；父档terminal定理提供不需SPE的上界，本族提供统一锐性；原程序实现本族定义，JSON保存其n3完整动作和金额数据；双review审查全n构造并限定历史同实现复跑身份；后续deep原稿保留尚未付的不同命题；六人问题只取一般构造的n5推论。本对象不与WA、同context净券或其它付款接口造蕴含边。详细证据与暂不更新阶段三投影的理由在工作区relation-evidence.json；稳定ID保持此资源对象原缓存标识，路径改变不改身份。
'''
out=root/'archives/customer-attraction/subarchives/six-providers/state/程序/金额cap1完整策略锐族的原程序与四百动作证书--程序.md'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(front+intro+body+last)
print(out.relative_to(root))
