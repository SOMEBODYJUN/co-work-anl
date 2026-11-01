from pathlib import Path
import json,hashlib
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-two-theme-repetition-and-security-route-primary';E=Path('tools/evidence/two-theme-repetition-and-security-route-primary');W=Path('cleanup/workspaces/Boss4/r3-two-theme-repetition-and-security-route-primary-next')
P1='archives/customer-attraction/state/定理/重复首主题终局的严格二倍界--定理.md';P2='archives/customer-attraction/state/资源/两覆盖结构与成对安全工作区的准确接续--资源.md';IDS=['b874ab55470546ce897b','0ceafe0cf6073351cde8','cae0027749fb8ec7bd95','24a3ec78bc2dfa4cd31f']
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
rows=[]
for mp in [C/'learning-ft-frequency-filter-context/local-export-manifest.json',C/'learning-ft-next-readable-contexts/local-export-manifest.json']:
 for x in json.loads(mp.read_text())['rows']:
  b=Path(x['local_path']).read_bytes();v=inv[x['id']];assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];q=E/'original'/x['id']/x['path'];cp(x['local_path'],q);rows.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'read_status':'7711B full math read FT related then sameSHA reused FU' if x['id']==IDS[0] else 'first actual full mathematical reading FU; previous FT availability only'})
assert {x['id'] for x in rows}==set(IDS);js(E/'source-manifest.json',rows)
for mp,n in [(C/'learning-ft-frequency-filter-context/local-export-manifest.json','actual-theorem-local-supply.json'),(C/'learning-ft-next-readable-contexts/local-export-manifest.json','actual-three-README-local-supply.json'),(C/'learning-fu-related-probe-inputs/local-export-manifest.json','actual-related-probe-local-supply.json'),(C/'learning-fu-next-readable-programs/local-export-manifest.json','next-four-program-absence.json')]:cp(mp,E/n)
raw=json.loads((C/'learning-fu-related-probe-inputs/local-export-manifest.json').read_text());related=[]
for x in raw['rows']:
 b=Path(x['local_path']).read_bytes();v=inv[x['id']];assert len(b)==v['size'] and sha(b)==v['sha256'];q=E/'related'/x['id']/x['path'];cp(x['local_path'],q);related.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'read_status':'complete actual new source code reading FU, not extra primary done or execution'})
js(E/'related-source-manifest.json',related);cp(C/'local_blob_export.py',E/'authorized-local-export-helper.py.txt')
contexts=[]
fresh=[
'archives/customer-attraction/state/反例/任意合法背景的前两人额外槽安全值--反例.md',
'archives/customer-attraction/state/反例/实际均匀缩放负载的弱付款桥--反例.md',
'archives/customer-attraction/state/候选/全位置成对安全值候选与有限锥判别范围--候选.md',
'archives/customer-attraction/state/资源/完整终局税候选的策略锥浮点反例搜索合同--资源.md',
'archives/customer-attraction/state/反例/独立同分布福利支付--反例.md',
]
for n in fresh:
 b=(REPO/n).read_bytes();q=E/'context'/n;cp(REPO/n,q);contexts.append({'path':n,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_status':'full actual current formal math freshly read FU'})
for manifest in ['r3-monochromatic-tax-and-full-menu-contracts-primary/tools/evidence/monochromatic-tax-and-full-menu-contracts-primary/context-manifest.json','r3-monochromatic-tax-and-full-menu-contracts-primary/tools/evidence/monochromatic-tax-and-full-menu-contracts-primary/formal-resource-manifest.json','r3-static-matching-and-induction-route-primary/tools/evidence/static-matching-and-induction-route-primary/context-manifest.json']:
 for x in json.loads((C/manifest).read_text()):
  n=x['path']
  if not any(t in n for t in ['两种实际覆盖且末两位不同','单色真实后缀','弱匹配与分区','最优补全账本']):continue
  if any(y['path']==n for y in contexts):continue
  b=(REPO/n).read_bytes();assert sha(b)==x['sha256'];q=E/'context-reused'/n;cp(REPO/n,q);contexts.append({'path':n,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_status':'previous full FT/FJ mathematical reading reused honestly; exact currentSHA checked','previous_manifest':manifest})
js(E/'context-manifest.json',contexts)
x=next(x for x in rows if x['id']==IDS[0]);before=(S/x['preserved_path']).read_text();old1=r'\lambda_m=\frac{2(m-1)(m^2-m-1)}{D_m}';new1=r'\lambda_m=\frac{2(m-1)(m^2-m+1)}{D_m}';old2=r'D_m-2(m-1)(m^2-m-1)=3m^2+m-4';new2=r'D_m-2(m-1)(m^2-m+1)=m(3m-1)';assert before.count(old1)==before.count(old2)==1;proposed=before.replace(old1,new1).replace(old2,new2);put(E/'correction/proposed-unapplied-source.md',proposed)
js(E/'correction/minimal-replacements.json',{'source_id':IDS[0],'original_path':x['path'],'before_sha256':x['sha256'],'before_bytes':x['size'],'applied_to_original_or_shared_page':False,'proposed_path':str(E/'correction/proposed-unapplied-source.md'),'proposed_sha256':sha(proposed.encode()),'changes':[{'original_line':143,'before':old1,'after':new1},{'original_line':149,'before':old2,'after':new2}],'scope':'two derived replacement proposals only; frozen original unchanged, source target gamma/beta and old AB theorem do not change','why':'old coefficients fail already at m2: (13/16,29/16) versus claimed common23/16; corrected positive lambda gives(23/16,23/16)','new_exact_check':'runs/new-convex-correction-001/stdout.json; one new polynomial check, not old audit/SPE/LP replay'})
p1=r'''---
id: "customer-attraction/repeated-first-theme-terminal-strict-two-bound"
kind: "theorem"
type_tag: "定理"
title: "重复首主题终局的严格二倍界"
status: "analytic-structural-proof-reconstructed-with-explicit-convex-weight-source-correction"
summary: "任意m≥2完整有序历史SPE实际A^(m−1)B有显式β_m<2；原λ末项−1改+1及区间余式同时更正，保原γ/β，频次充分筛选与BB不同范围。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/credible_search/two_theme_terminal.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/credible_search/two_theme_terminal.md"
---

# 重复首主题终局的严格二倍界

## 模型与结构定理

有限单位客户、共同有限非空目录、m名单位提供者依次观察全部有序历史，客户在最终覆盖者中均分。策略覆盖每个有序历史，允许空主题、同覆盖异标签、重复及任意平局。对任意整数m≥2，若一份完整纯SPE实际路径为A^(m−1)B，A/B合法且可同覆盖或相同，记实际福利W，则
\[
OPT_m\le\beta_m W,\qquad
\beta_m=\max\left\{2-\frac1m,
\frac{4m^3-3m^2+2m-1}{2m^3-m^2+3m-2}\right\}<2.\tag{THM}
\]
W>0时严格OPT<2W；W0则任何正大小主题偏离至少保大小/m，与实际根0矛盾，故目录全空、OPT0。m1由唯一玩家最优给OPT=W，无须比值。

[7711B原稿](../../../../tools/evidence/two-theme-repetition-and-security-route-primary/original/b874ab55470546ce897b/research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/credible_search/two_theme_terminal.md)此前FT已related全文实读，本批核同SHA诚实复用。原Claim A和目标β保留；其凸合权重及紧随的区间等式有两处明确代数笔误，下面给完整最小更正。原件冻结不改，不能只因末段写“精确审计已核”就复制错误等式。

## 两个真实末节点的共同目录闭包

设a=|A\B|、b=|B\A|、c=|A∩B|，W=a+b+c。固定真实前缀P=A^(m−2)，倒二实际A、末位实际B。二者真实收益u=a/(m−1)+c/m，v=b+c/m。

任意合法T后原策略真末回复为R。R也能在原实际末位PA作为合法偏离，这是共同目录作用，未冻结回复或合并同计数历史。令E_R=|R\A|+|R∩A|/m，为PA处末位改R利润。设T在A/B外、A私块、B私块及公共块大小为s,t_A,t_B,t_C，D=m(m−1)。两条真实分支中当前/末位利润U_T,U_R，T后末位改B利润U_B，SPE给
\[
u-U_T\ge0,\qquad U_R-U_B\ge0,\qquad v-E_R\ge0.
\]
逐客户直接有
\[
U_R=E_R-\frac{|R\cap T\setminus A|}2
+\frac{|(R\cap A)\setminus T|}D,\quad
U_B=v-\frac{t_B}2+\frac{c-t_C}D,
\]
\[
U_T=|T\setminus A|-\frac{|R\cap T\setminus A|}2
+\frac{|T\cap A|}{m-1}-\frac{|R\cap T\cap A|}D.
\]
代入消元得到完整精确余式
\[
\frac{a(m+1)}D+\frac cm
-\left(s+\frac{t_B}2+\frac{t_A}{m-1}+\frac{t_C}m\right)
=(u-U_T)+(U_R-U_B)+(v-E_R)+\frac{|A\setminus R|}D\ge0.\tag{CLOSE}
\]
m2空前缀仍合法，所有分母正。此式继承原two_remaining_tax三比较并保非负重叠余项，不是把SPE当静态PNE。

## 对m个最优主题的两份共同预算

取恰m个最优合法主题，少于m个以重复补齐。将(CLOSE)的不等式求和；最优并集四块覆盖X_o,X_A,X_B,X_C，每客户至少出现一次、权非负，故
\[
X_o+X_B/2+X_A/(m-1)+X_C/m\le a(m+1)/(m-1)+c.
\]
利用X_A≤a、X_B≤b、X_C≤c补并集余量得到
\[
OPT_m\le P=\frac{2m-1}{m-1}a+\frac b2+
\left(2-\frac1m\right)c.\tag{P}
\]
实际末位B的最优性又给任意T：|T\A|+|T∩A|/m≤v。对m个最优主题求和并补A内余量，得到
\[
OPT_m\le L=\frac{m-1}m a+mb+\left(2-\frac1m\right)c.\tag{L}
\]
这两式支付的是最优并集，不把同客户的重复出现再算新增福利。

## 原式的可定位错误与正确凸合

原源第143行写λ_old=2(m−1)(m²−m−1)/D_m，D_m=2m³−m²+3m−2，第149行又写D_m−2(m−1)(m²−m−1)=3m²+m−4。这两式不能支持其声称的等系数凸合：m2时λ_old=1/8，λ_old P+(1−λ_old)L的(a,b)系数为(13/16,29/16)，并非源γ2=23/16；第二等式两边之差为2m。

由两系数相等直接解出正确权重
\[
\lambda_m=\frac{m-(m-1)/m}
{(2m-1)/(m-1)-1/2-(m-1)/m+m}
=\frac{2(m-1)(m^2-m+1)}{D_m}.\tag{WEIGHT}
\]
只有末项−1改+1；配套区间计算应为
\[
D_m-2(m-1)(m^2-m+1)=m(3m-1)>0.
\]
m≥2时分子正、D_m=m²(2m−1)+3m−2>0，故0<λ_m<1。代入(P)/(L)并跨乘展开：
\[
\lambda_mP+(1-\lambda_m)L
=\gamma_m(a+b)+(2-1/m)c,\quad
\gamma_m=\frac{4m^3-3m^2+2m-1}{D_m},
\quad 2-\gamma_m=\frac{m^2+4m-3}{D_m}>0.\tag{MIX}
\]
原γ、β本身不改，所以OPT≤min(P,L)≤(MIX)≤β_mW，证得(THM)。m2修正λ=3/8确给两系数23/16；β2=3/2、β3=5/3、β5=217/119。这里只证给定结构常数，不称最优或锐。

[最小原文替换提案](../../../../tools/evidence/two-theme-repetition-and-security-route-primary/correction/minimal-replacements.json)含源SHA、原两行、正确式和未应用派生整稿SHA；**未作用于冻结原件或共享旧页**。当前[末两位不同的一般两覆盖定理](两种实际覆盖且末两位不同的严格二倍界--定理.md)取k=m−1,l1的正确凸合也化为(WEIGHT)，它原数学保持正确，不把这次来源笔误扩大为旧done整体错误。

## Claim B：频次筛选的准确充分性

原稿另对实际只用两个不同覆盖A/B、末位B、频次k,l≥1给充分条件l(2k+1)≥k²−1⇒OPT≤2W。最后一次A若真改B，各B私客户最终至多l+1覆盖、公共客户至多m，所以(l+1)a≥kb。末位最优给
\[
OPT_m\le\frac{k}{k+1}a+
\left(2+\frac{k-1}l\right)b+(2-1/m)c.
\]
右端减2W≤[−(k+2)/(k+1)+(k−1)(l+1)/(kl)]a−c/m，在上述频次条件下非正。a0时迫b0也成立。完整推导已在[单色VA与频次对象](../候选/单色真实后缀的虚拟相邻税--候选.md)保存；该筛选不要求VA，不是所有两主题SPE的必要频次。

五人两覆盖且l≥2时(k,l)为(3,2),(2,3),(1,4)，条件均满足；l1则路径A^4B，用(THM)。一个覆盖可视A=B；同覆盖不同标签只按实际覆盖几何计数，不匿名化原策略。这是原稿的五人结构结论，当前五人一般half另已有定理。任意m的两覆盖BB收尾未被本两条完全覆盖，大m小l可不满足筛选且此前顺序不为A^(m−1)B；不可挪更早A到倒二。

## 证据与新核验的准确范围

原文称saturation独立重构、global_proof攻击另行进行，并指audit_two_theme_terminal.py / two_theme_terminal_audit.json核16客户会员模式、凸合、多项式和边界/指定SPE。当前inventory及正式证据树未找到这两个同名原件，本批未读/执行它们，不拿一句“已核”认证错误λ，也不补造原运行次数。已有AB定理、VA及当前源分别实读比较；来源指针terminal_load_rank/last_theme_containment只保同一几何背景，真实回复闭包链有自己的作用。

为此新发现纠错，新增[标准库精确多项式检查](../../../../tools/evidence/two-theme-repetition-and-security-route-primary/new-convex-correction-check.py)实际执行**一次**，输入绑定原7711B SHA；0.030863576秒、exit0、stderr空。报告记录原式m2失败、原区间等式残差2m、修正两系数的全多项式跨乘恒等、D−分子=m(3m−1)及2D−γ分子=m²+4m−3。它不是有限m样本外推，符号恒等式通过系数精确比对；整数域正性由上述解析证明承担。没有核任何SPE历史、游戏、旧audit、LP/Nash或主目标一般证明，[实际运行身份](../../../../tools/evidence/two-theme-repetition-and-security-route-primary/runs/new-convex-correction-001/run-metadata.json)和[完整输出](../../../../tools/evidence/two-theme-repetition-and-security-route-primary/runs/new-convex-correction-001/stdout.json)保原捕获。

原CLI、旧成功SPE/优化器复跑均0；这一新增检查不扩大到root背景可达性或六人一般half。原稿内部候选/审查、新颖性未认证身份保留，目标结论由本页完整结构证明与显式纠错而非有限PASS承担。
'''
put(P1,p1)
p2=r'''---
id: "customer-attraction/two-coverage-and-pair-security-workspace-accurate-continuation"
kind: "resource"
type_tag: "资源"
title: "两覆盖结构与成对安全工作区的准确接续"
status: "all-three-README-contracts-preserved; arbitrary-background-pair-and-actual-load-tax-open-labels-corrected; no-repeated-old-run"
summary: "完整保R31总入口/260锥成对探针/共同单主题付款，区分根真v、任意背景PB、iid福利及实际缩放M；补13人精确税桥反驳，软件只读不把浮点计数当证明。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/aggregate_security/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/aggregate_security/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/global_proof/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/global_proof/README.md"
---

# 两覆盖结构与成对安全工作区的准确接续

## 三入口及历史身份

[总README3148B](../../../../tools/evidence/two-theme-repetition-and-security-route-primary/original/0ceafe0cf6073351cde8/research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/README.md)、[聚合README1976B](../../../../tools/evidence/two-theme-repetition-and-security-route-primary/original/cae0027749fb8ec7bd95/research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/aggregate_security/README.md)、[全局README827B](../../../../tools/evidence/two-theme-repetition-and-security-route-primary/original/24a3ec78bc2dfa4cd31f/research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/global_proof/README.md)在FU首次完整实读；FT只核可用原字节，不冒前次已数学全读。两冻结提交各自同SHA，三个身份不同。

旧发布R31、Boss10、恢复clone/读本地origin/main/程序生成新身份、旧R-a0bb已推数学复用、六内部研究员gpt配置、主代理交流、私聊和checkpoint可见性均作历史。当前清洗Boss4，不执行旧私聊/start/生成身份/外部通信/找凭据或旧停止规则。总入口泛指任意人数half是原研究问题时态；当前五人已有定理，六人完整SPE half未由本批解决。

## 真正背景安全值、已否普遍pair及有效条件推论

共同有限非空目录、单位客户和提供者、全有序历史纯SPE，保空/重复/零客户/任意平局。余r≥2、给定合法沉没前缀b，真正静态安全值
\[
v_r(b)=\max_p\min_{B\in\mathcal S^{r-1}}
E_{T\sim p}\sum_{x\in T}\frac1{b_x+1+c_x(B)}.
\]
竞争元组不观察查询实现。聚合README提出任意此背景子SPE首两位u1+u2≥2v_r(b)。若普遍成立，实际按相邻两位分组；一步嵌入v_(r−1)(b+1_A)≥v_r(b)，两步同理，各对都≥2v_m(0)，奇数剩一末位最佳回复也≥v_m(0)，所以条件上W≥m v_m(0)。这是有效条件推论，不是前提证明。

总README顶部2026-10-25已纠正：更弱PB-extra用r个竞争槽的v_(r+1)(b)也已被[任意合法背景完整解析反例](../反例/任意合法背景的前两人额外槽安全值--反例.md)否定。该例r2475、合法singleton背景已覆盖全部48,495,120客户，前两各u但同一查询保证s>u，2u<2s≤2v_(r+1)(b)≤2v_r(b)。所以正文旧“首两人前提OPEN”不能沿用。补齐为整个博弈子SPE不保证这个背景在根实际可达，不能因此反实际前缀专用弱化、根强聚合W≥m v_m或六人half。

另一[全位置pair候选](../候选/全位置成对安全值候选与有限锥判别范围--候选.md)用原零根全局v_m约束任意实际位置u_i+u_j；它与任意沉没背景的前两人不同，亦不因个体extra-one银行反例自动被否定。iid对称Nash福利Z_m也不是真v：已发表[强/弱iid反例](../反例/独立同分布福利支付--反例.md)分别反W≥Z及W≥(1−1/(2m))Z，仍保其真v聚合及half。总README的这条状态纠正保留，不拿iid替代真静态安全值。

## 260策略锥的真实软件合同

实际取齐并全文读必要[5375B background_pair_probe.py](../../../../tools/evidence/two-theme-repetition-and-security-route-primary/related/2db24df0ce02d6fd610c/research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/aggregate_security/background_pair_probe.py)，只读取不执行。它仅导标准库、NumPy、SciPy/HiGHS，无规范CAG模块依赖；本批未认证这些库的历史版本/环境。

representation按所有非空兴趣mask构造member，sunk=背景主题计数×member，对全部r−1主题多重集形成1/[1+sunk+竞争负载]矩阵。policy_cone遍历所有有序h，为最初整数重数用覆盖分母公倍数的整数收益逆向归纳，真平局随机选；保actions[h]，各真行动偏离Γ行最后仅去重完全相同行，不匿名化策略。固定pair行是两实际行动的真实终局均分之和。

cone_step固定查询p、取非负实重数w和安全下界z，约束Γw≥0、全部合法静态列收益≥z，并归一pair·w=1，浮点LP最大化z。security再固定w解真正静态零和LP的最优查询p；交替所得ratio=2v。新w为浮点实客户质量，非原单位整数证书；代码没有自动有理恢复/逐单位完整核验，负/正输出均不认证全锥或全模型。

CLI默认--trials160，--output必填、--large可选，seed310102181。普通(r,k)实际列表为(3,5),(3,6),(4,5),(4,6),(5,6)；large列表(5,7),(6,6),(6,7)。背景长从1,2,3,5,8随机、每主题独立均匀，非空兴趣mask按密度0.15/0.4/0.7/1保留、正重数1…15。每锥两个起点：初始真安全LP查询与均匀查询；最多7轮，改善<1e−9可提前停。ratio>1+1e−7才存浮点candidate含w/p/actual/全部actions并返回；每10trial及末尾写output，状态始终numerical_only。

聚合README说background_pair_numerical.json已完成260锥、最大观察ratio1未严格候选；260不是CLI默认160，不凭默认值复原原argv。其312B报告本地缺，另330Blarge记录、4041B SSR代码/914B SSR结果也缺；“较大r/SSR孤立探索另见结果”不能算作已完成参数。无逐锥真实输入、运行日志、浮点对偶或有理全树证书，本批只能保存作者有限260记录与已读源码的真实实现边界，不补造运行/全LP次数。

## 共同单主题精确税桥的后续纠错

global_proof README固定actual负载c，α=(m−1)/m，g(T)=Σ_T1/(1+αc)、M=max_Tg(T)、G=Σ_(c>0)1/(1+αc)。任意最优比较负载d逐客户有1_(d>0)≤(d+αc)/(1+αc)，故
\[
OPT_m\le mM+\sum_{c>0}\frac{\alpha c}{1+\alpha c}=mM+W-G.
\]
若mM≤W+G便推出half；这是合法静态代数与条件推论，**候选付款本身现已被反例否定**，不能按827B旧文继续当当前OPEN。原文也明确来自已有fractional_actual_load_counterexample.md，非新命题。

[实际缩放弱桥对象](../反例/实际均匀缩放负载的弱付款桥--反例.md)保四主题每m≥4反W≥(m−1/2)M，但那一族仍满足mM≤W+G；反精确税桥的是另一个完整13人证书：W33、OPT36、M3、G708669/123025，13M−W−G=29481/123025>0。其13玩家/36单位客户全历史自动机已有112050比较旧真核验，依该正式对象证据复用，不在本批重演。该例v13≤5/2、W−13v13≥1/2、half余额30；不能把固定actual缩放M叫真正v。α1的另一算术修复也已败，非本批新SPE构造。

## 总入口七类资产的准确去向

| 原目录/入口 | 数学/资源作用与保留边界 |
| --- | --- |
| terminal_tax/probe.py | 全终局税候选OPT≤W+Σ_(c>0)c/(c+1)，固定完整策略、非负类型质量、任意m主题并集的浮点攻击；候选要有理恢复及全树核验。原替代schema报错后改明确跳过，无数学含义。本437?源码实际7437B本地缺，不声称读/跑；完整终局税不是上述actual缩放精确M税桥，后者败不代前者。 |
| aggregate_security | 真v根聚合、任意背景pair、固定安全最优面数值攻击分别保；本页已校正PB并保存已读5375B实现。 |
| weak_matching | 旧52客户强冻结Q≤W已失败后，更弱支付及最优组合添加价Σ_TΣ_(x∈T)1/(c+1)≤W；源均未证明，本批不以52Q失败或14分区R失败直接判添加价。 |
| credible_search | 完整可信构造、两实际覆盖结构，成熟7711B原稿现按[纠错完整证明](../定理/重复首主题终局的严格二倍界--定理.md)保；大m小l/BB尾未由该结构结论关闭。 |
| global_proof | 独立真实分支尝试、两覆盖重构；共同单主题候选已按13人例更新，不能把源码/样本当一般证明。 |
| saturation | 旧合法背景近饱和交换、跨节点误差支付，未交付一般共同预算；不自动从局部误差推广。 |
| tree_transport | 全树收益图/逐客户稀释、包含闭包、跨SCC支付探索，原未闭合half；不导成第三阶段旧图或造付款。 |

该一般full-terminal-tax与当前[完整终局税搜索合同](完整终局税候选的策略锥浮点反例搜索合同--资源.md)中的候选同类；那里保存的有限阴性扫描不是普遍证明。weak matching的Q/R/真实V边界见[精确资源](../计算/弱匹配与分区查询的精确核验--计算.md)。源“局部结果不作终点、先全树义务、共享前需独立审查”仅是历史研究安排，不变成当前额外审批要求。

## 本次读取与执行边界

三个README总5951B首次全文读，7711B作者稿同SHA复用，相关5375B代码首次全读；五份当前正式后续对象全文比较，另复用已完整读的AB/VA/Q-R等同SHA上下文。源原audit文件无inventory匹配，不冒读取。数学新执行仅一次修正凸合多项式恒等式，原CLI/SPE/LP/优化器/旧成功复跑0。原件、缺失回执、最小纠错与准确运行见[本批证据](../../../../tools/evidence/two-theme-repetition-and-security-route-primary/README.md)，关系限阶段二，无新网络、外部通信、图导入或一般half认证。
'''
p2=p2.replace('本437?源码实际7437B','其7437B源码')
put(P2,p2)
js(E/'formal-resource-manifest.json',[{'path':p,'bytes':(S/p).stat().st_size,'sha256':sha((S/p).read_bytes())} for p in [P1,P2]])
put(E/'README.md',r'''# 两覆盖结构、原凸合纠错及安全入口

四primary总13662B：7711B原稿FT已全文实读同SHA复用，三README3148/1976/827首次FU全读；相关5375B背景pair源码全文新读。两新自足对象保真实三比较、两个覆盖预算、修正凸合与β目标、频次充分性，以及PB/actualM/真v/iid/fulltax各量词和后续状态。

原权重末项−1实际应+1，配套区间余式应m(3m−1)；原γ/β不变。原bytes保original；correction给两处精确替换及未应用派生稿，未覆冻结源或旧AB定理。新标准库多项式检查只有一次，原捕获/哈希/版本/时间/exit完整保存；0旧原CLI/SPE/LP复跑。

新probe相关helper6尝试1齐5缺，下批4程序可用性尝试均缺；不网络、不重试这些缺件。源所指两主题audit原件无inventory同名绑定，不能冒认证。成功receipt等实际claim pushed/synced与owner后生成；Root依赖正文先推再done。只独立staging，0sharedGit/claim/done/checkpoint/show/身份公屏操作。
''')
cp(Path(__file__),E/'build_resources.py')
print(json.dumps({'stage':str(S),'primary_bytes':sum(x['size'] for x in rows),'primary_lines':sum(x['lines'] for x in rows),'related_bytes':sum(x['size'] for x in related),'formal_bytes':sum((S/p).stat().st_size for p in [P1,P2]),'new_math_runs':1,'status':'resources prepared; no success receipt before actual claim'},ensure_ascii=False,indent=2))
