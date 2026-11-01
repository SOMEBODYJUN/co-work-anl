from pathlib import Path
import json,hashlib
R=Path('/workspace/scratch/37f0f9248cfc');REPO=R/'boss4-research';C=R/'boss4-next-cache';S=C/'r3-monochromatic-tax-and-full-menu-contracts-primary';E=Path('tools/evidence/monochromatic-tax-and-full-menu-contracts-primary');W=Path('cleanup/workspaces/Boss4/r3-monochromatic-tax-and-full-menu-contracts-primary-next')
P1='archives/customer-attraction/state/候选/单色真实后缀的虚拟相邻税--候选.md';P2='archives/customer-attraction/state/资料/完整真实菜单的条件对偶与旧实例账本--资料.md';P3='archives/customer-attraction/state/审查/四人冻结匹配独审的报告与复用边界--审查.md'
IDS=['a78d96dc6f303010aea7','1b9335bec700624bc143','276852a177c7326ea276'];inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
mp=C/'learning-fj-related-local-inputs/local-export-manifest.json';raw=json.loads(mp.read_text());rows=[]
for x in raw['rows']:
 assert x['id'] in IDS;b=Path(x['local_path']).read_bytes();v=inv[x['id']];assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];q=E/'original'/x['id']/x['path'];cp(x['local_path'],q);rows.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'read_status':'full actual FJ related reading reused honestly after current same-SHA check; source now separately primary'})
assert {x['id'] for x in rows}==set(IDS);js(E/'source-manifest.json',rows);cp(mp,E/'actual-primary-local-supply-manifest.json')
rmp=C/'learning-ft-frequency-filter-context/local-export-manifest.json';rr=json.loads(rmp.read_text());related=[]
for x in rr['rows']:
 b=Path(x['local_path']).read_bytes();v=inv[x['id']];assert len(b)==v['size'] and sha(b)==v['sha256'];q=E/'related'/x['id']/x['path'];cp(x['local_path'],q);related.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'read_status':'full actual new reading FT; only ClaimB needed for frequency-filter direction; not extra primary done'})
js(E/'related-source-manifest.json',related);cp(rmp,E/'actual-related-local-supply-manifest.json');cp(C/'learning-ft-menu-audit-local-inputs/local-export-manifest.json',E/'actual-two-missing-menu-audit-supply.json');cp(C/'local_blob_export.py',E/'authorized-local-export-helper.py.txt')
cp(C/'r3-weak-pushforward-and-static-prefix-primary/tools/evidence/weak-pushforward-and-static-prefix-primary/prior-two-missing-JSON-supply.json',E/'prior-two-missing-JSON-supply-reused.json');cp(C/'learning-fj-related-local-inputs/local-export-manifest.json',E/'prior-missing-independent-audit-and-probe-reused.json')
js(E/'missing-inventory-bindings.json',[{**inv[i],'actual_attempt':'new FT once' if i.startswith(('e15c','5c25')) else 'prior actual manifest reused; no new retry'} for i in ['e15c507bf9936c1cd1c8','5c25af511b4e5ef5ee70','912d0cefccf4466d1e31','4638f7b82684049fdae6','1894bab391f4c921d293','b03448e16b1090d7a08f']])
contexts=[]
fresh='archives/customer-attraction/state/定理/两种实际覆盖且末两位不同的严格二倍界--定理.md'
b=(REPO/fresh).read_bytes();q=E/'context'/fresh;cp(REPO/fresh,q);contexts.append({'path':fresh,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_status':'current full mathematical text freshly read FT'})
for manifest in ['r3-static-matching-and-induction-route-primary/tools/evidence/static-matching-and-induction-route-primary/formal-resource-manifest.json','r3-static-matching-and-induction-route-primary/tools/evidence/static-matching-and-induction-route-primary/context-manifest.json','r3-weak-pushforward-and-static-prefix-primary/tools/evidence/weak-pushforward-and-static-prefix-primary/formal-resource-manifest.json']:
 for x in json.loads((C/manifest).read_text()):
  n=x['path']
  if not any(t in n for t in ['最优组合冻结匹配的一单位缺口','双尾推送与单色续局','笛卡尔银行','末位真实回复推送','后继边际价格付款','完整根菜单的联合势','合法前缀的静态','空根稀释的强推送']):continue
  if any(y['path']==n for y in contexts):continue
  b=(REPO/n).read_bytes();assert sha(b)==x['sha256'];q=E/'context-reused'/n;cp(REPO/n,q);contexts.append({'path':n,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_status':'previously full math read FJ/EX/EG, current exactSHA reused, no pretended fresh first read','previous_manifest':manifest})
js(E/'context-manifest.json',contexts)
p1=r'''---
id: "customer-attraction/virtual-adjacency-tax-for-real-monochromatic-suffix"
kind: "candidate"
type_tag: "候选"
title: "单色真实后缀的虚拟相邻税"
status: "r1-identity-and-static-monochromatic-potential-proved; general-VA-not-certified; conditional-BB-interface"
summary: "保完整VA(r)域、r1三真实比较和残余，推导其对两覆盖BB尾部的条件预算；频次筛选是half充分条件，单色PNE全局势只在同背景，不代真实跨背景后继。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/tree/virtual_adjacency_handoff.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/tree/virtual_adjacency_handoff.md"
---

# 单色真实后缀的虚拟相邻税

## 精确未付合同

[3843B全部原稿](../../../../tools/evidence/monochromatic-tax-and-full-menu-contracts-primary/original/276852a177c7326ea276/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/tree/virtual_adjacency_handoff.md)在FJ作related已全文读，本批核同SHA后正式保全；不虚称重新第一读。原2026-10-22“未证明/未反驳、一般half OPEN”是历史身份，本批不靠有限阴性样本认证一般VA真值。

有限单位客户、共同有限非空目录、单位权顺序玩家、每个有序历史规定动作的纯SPE，允许空主题、同覆盖标签、重复及任意平局。固定一个合法原有序前缀h，过去整数客户负载b_x；其后实际r+1人路径为A B^r，r≥1。定义
\[
u_A=\sum_{x\in A}\frac1{b_x+1+r\mathbf1_B(x)},\quad
q(T)=\sum_{x\in T}\frac1{b_x+1+r\mathbf1_B(x)},\quad
\tau_A=\sum_{x\in A\setminus B}\frac1{(b_x+1)(b_x+2)}.
\]
VA(r)要求对每个合法目录主题T都有q(T)≤u_A+τ_A。q把当前A换成T并把后继**冻结**为B^r，不是原策略在hT后的真实收益。实际SPE只比较后者，正缺真实多玩家子树到冻结B^r的付款。空/重复只产生空和或同动作，没有删去离轨历史。下述代数和静态势也能用于固定实b≥0的带背景游戏，但这不将任意实b假定为原单位游戏可达前缀。

## r=1的完整真实三比较证明

恰剩两人时，令F为给定原策略在hT后的真末位回复，实际末位为B。写
\[
f(X)=\sum_{x\in X}\frac1{b_x+1},\quad
g(X,Y)=\sum_{x\in X\cap Y}\frac1{(b_x+1)(b_x+2)},\quad
U(X,Y)=f(X)-g(X,Y).
\]
U就是两位追加玩家选X/Y时X的真实利润。三条比较为
\[
s_1=U(A,B)-U(T,F)\ge0,\quad
s_2=U(F,T)-U(B,T)\ge0,\quad
s_3=U(B,A)-U(F,A)\ge0.
\]
分别用当前actual最优、改变后节点末位BR、原actual末位可改F；最后一步靠共同目录。τ_A=g(A,A)−g(A,B)。将U=f−g及g对称代入逐项相消，得到精确
\[
u_A+\tau_A-U(T,B)
=s_1+s_2+s_3+g(A,A)-g(A,F)
=s_1+s_2+s_3+\sum_{x\in A\setminus F}
\frac1{(b_x+1)(b_x+2)}\ge0.\tag{VA1}
\]
因此VA(1)成立，保留明确非负残余而非把末回复当成B。r≥2时原真实后继是多个玩家，不可作为一个合法主题放到另一个末位节点；(VA1)没有给一般VA(r)。

## 对两覆盖终局的条件用途及频次方向

假设完整终局只出现两个不同覆盖集合A/B，次数k,l≥1、k+l=m，末位为B。取最后一次实际A，其后恰r个B，1≤r≤l，过去负载为(k−1)1_A+(l−r)1_B。记a=|A\B|、b=|B\A|、c=|A∩B|，W=a+b+c；这里小写b是块大小，只在本节使用，区别于前节b_x。将VA(r)应用到这个节点，任何主题T在实际并集外、A私块、B私块、公共块量t_o,t_A,t_B,t_C满足
\[
t_o+\frac{t_A}k+\frac{t_B}{l+1}+\frac{t_C}m
\le\frac{k+2}{k(k+1)}a+\frac cm.\tag{AB-IF}
\]
分母来自旧k−1个A、l−r个B加当前查询和r个冻结B；右端是u_A=a/k+c/m加τ_A=a/[k(k+1)]。因此若一般VA已证，(AB-IF)就把已有[实际末两位不同的两覆盖定理](../定理/两种实际覆盖且末两位不同的严格二倍界--定理.md)所用预算推进到更早最后A、BB收尾。这个推进仍有VA前提，不能把更早A移到倒二来删除原历史。

另一个无需VA的旧充分筛选必须把方向写清。最后A若真实改B，每个B私块客户负载至多l+1、公共块至多m，故其真实偏离保底b/(l+1)+c/m，SPE给
\[
(l+1)a\ge kb.\tag{LAST-A}
\]
末位B的实际最优性给任何T：t_o+t_A/(k+1)+t_B/l+t_C/m≤b/l+c/m。将m个最优合法主题求和，再以a,b,c各付并集余量，得到
\[
OPT_m\le L=\frac{k}{k+1}a+
\left(2+\frac{k-1}l\right)b+\left(2-\frac1m\right)c.
\]
于是
\[
L-2W=-\frac{k+2}{k+1}a+\frac{k-1}l b-\frac cm
\le\left[-\frac{k+2}{k+1}
+\frac{(k-1)(l+1)}{kl}\right]a-\frac cm.
\]
方括号非正恰等价l(2k+1)≥k²−1；所以该频次条件**足以**得到half，不是每个两主题SPE都必须满足的必要频次限制。a=0时(LAST-A)迫b=0，只余公共块，也直接成立。对可能未被该预算排除的坏例，只能要求相反严格区间l(2k+1)<k²−1，仍不保证可实现。

这一段在原稿已明确与R31 Claim B重复。为核方向，本批实际全文读[7711B R31原稿](../../../../tools/evidence/monochromatic-tax-and-full-menu-contracts-primary/related/b874ab55470546ce897b/research/workspaces/customer-attraction/R-31bbb6cfd6594bc8bb076db7b2950993/credible_search/two_theme_terminal.md)；它的Claim B正是上述充分结论，不新冠定理或额外done该源。其另有A^(m−1)B结构界，不由本页代领；旧五人一般OPEN也不能覆盖当前已发布五人定理。

## 独立有效的同背景全局势引理

任意固定实b_x≥0、整数r≥1，若r名同时静态玩家全选B为PNE，则B^r在所有r个合法主题元组中全局最大化
\[
\Phi_b(Z)=\sum_x\sum_{j=1}^{d_x(Z)}\frac1{b_x+j}.
\]
整数b可写调和差，实b用此有限和。证明：单人改T的PNE条件消去公共客户，恰为
\[
\sum_{x\in T\setminus B}\frac1{b_x+1}
\le\sum_{x\in B\setminus T}\frac1{b_x+r}.
\]
对任意Z的r个主题相加，得
\[
\sum_{x\notin B}\frac{d_x(Z)}{b_x+1}
\le\sum_{x\in B}\frac{r-d_x(Z)}{b_x+r}.\tag{PNE}
\]
B外势增量≤左，B内从r减至d的势损失≥右，所以Φ_b(Z)≤Φ_b(B^r)。重复/空行动与r1都包括。

一个真实SPE的单色B^r后缀，在它自己的固定过去背景（包括此前A若有）下，末位对任意T的比较正给该静态PNE条件，所以引理能用。当前A改T却改变过去背景，并进入另一份原策略子SPE；新尾玩家不必共同最大化旧Φ。该引理不证明VA，不把SPE叶一般化成静态PNE，更不支持跨背景偷换。

## 有限探索、状态和接续

原稿报告两种探索：小单位目录完整SPE可行终局集递归，以及固定完整有序策略的兴趣类型重加权LP；后者先重构每个有序历史，再用全部真实SPE行限制重数。典型目录5、m3…5、实际A^(m−2)BB及末段BBB，另目录4、m7、A^5BB；未得反例。这些是浮点递归/LP且无完整冻结重放证书，不能宣称精确排除或一般VA成立。原停止同模板阴性样本只保历史，不发新求解任务。

本页没有解一般VA(2)双后继闭包。静态PNE势、VA1、频次充分筛选、条件AB预算各有准确前提；与[完整真实菜单](../资料/完整真实菜单的条件对偶与旧实例账本--资料.md)的r槽可行域不同，银行个体菜单反例也不直接反驳实际单色后缀VA。本批新数学程序/LP/SPE运行0，完整来源与关系见[证据](../../../../tools/evidence/monochromatic-tax-and-full-menu-contracts-primary/README.md)；无外审、新颖性或最优常数声明。
'''
put(P1,p1)
p2=r'''---
id: "customer-attraction/full-real-terminal-menu-conditional-dual-and-old-witness-ledger"
kind: "resource"
type_tag: "资料"
title: "完整真实菜单的条件对偶与旧实例账本"
status: "finite-minimax-and-conditional-half-implication-valid; universal-individual-FM-refuted; 381-record-not-replayed"
summary: "保完整r槽/SEP精确量词、静态安全因子二、循环及META充分条件；381原始对偶/纯列数值完整保存为缺输入作者记录，顶部2026-10-25更正优先于旧OPEN。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/tree/full_terminal_menu_interface.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/tree/full_terminal_menu_interface.md"
---

# 完整真实菜单的条件对偶与旧实例账本

## 冻结原文的两时态和当前真值

[4790B全文原件](../../../../tools/evidence/monochromatic-tax-and-full-menu-contracts-primary/original/1b9335bec700624bc143/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/tree/full_terminal_menu_interface.md)在FJ已作related全文实读，本批核同SHA复用。开头2026-10-25已经说明逐位置FM/Mfull≤u由真正零过去背景银行反族否定，不是旧任意背景例外推；后面2026-10-22的OPEN、较弱extra-one和继续攻击路线保其历史。原指令不切换本轮清洗。全路径Mpath/聚合与个体分开，不借一个旧名字替代可行域定义。

模型为有限单位客户/共同有限非空目录/单位玩家、完整有序历史纯SPE，保重复、空主题、零客户、全部离轨历史和平局。固定合法节点过去负载b、余r≥1；强制当前B后沿同一策略的真实完整终局为Z(B)，长r且含B自身，当前利润d_B、actual u=max_B d_B。定义
\[
K_{A,B}=\sum_{x\in A}\frac1{b_x+1+c_x(Z(B))},\qquad
M_{full}=\min_{Q\in\Delta(\mathcal S)}\max_A(KQ)_A.\tag{FM}
\]
查询A与列随机化独立；Q只随机**真实r槽根分支列**，不是任意r槽、r−1真实尾或确定分数均值。旧强式D(p)=Σp_Bd_B≥C(p)=p^TKp和弱式u≥C(p)也有不同量词。

## 精确零和对偶和反例应达到的强度

有限minimax给Mfull=max_p min_B Σ_Ap_AK_(A,B)。故Mfull≤u恰等价
\[
\forall p\in\Delta(\mathcal S)\ \exists B\in\mathcal S:
\sum_Ap_AK_{A,B}\le u.\tag{SEP}
\]
固定p可选不同B，线性对Q最小值由纯列达到。要反驳FM，需要同一个p使**所有**根列都严格大于u；一个列某查询大于该列d_B、或某p的D<C，均不足。r1/r2的真实强推送对每p给C≤D≤u，取Q=p再用对偶即可推出FM。r≥3强式已有真反例但不是这个逻辑推论的逆向；34客户就D<C<u。

当前普遍FM、全p弱推送及低值对称Nash已由[银行完整菜单真反例](../反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)另行否定。个体真正整数extra-one也失败：m4根4/3<19/14=t5≤v5；其中t≤v是Jensen单向比较，不能称二值相等。该结论不反聚合W≥m v_m或six-player half，也不从非SPE伪菜单推出。

## 静态因子二及条件归约的完整承重

真正v_(r+1)(b)允许全部r个静态目录竞争主题元组，完整真实根菜单只是其中一族，故v_(r+1)(b)≤Mfull。若每actual节点FM都成立，第i名角色过去i−1个合法主题可嵌入自由m个对手槽，得到
\[
u_i\ge v_{m-i+2}(b_i)\ge v_{m+1}(0).
\]
静态v_(m+1)(0)≥OPT_m/(2m)可直接证：任意查询独立的m主题元组分布Q，令z_x为期望客户负载、a_x=1/(1+z_x)、M=max_TΣ_(x∈T)a_x。最优m主题的并集O逐客户满足1=a_x+z_xa_x，所以第一份Σ_Oa由最优m主题覆盖付≤mM。Q的m个合法主题线性期望又给Σ_Oz_xa_x≤Σ_xz_xa_x=E_QΣ_(B∈元组)Σ_(x∈B)a_x≤mM。Jensen使每行真实随机对手价E1/(1+c_x)≥a_x，所以任意Q的最大真实查询≥OPT/(2m)。对全部Q取min，并用有限minimax，得真正静态安全值下界。

若个体FM前提成立，上两式相加会给W≥m v_(m+1)(0)≥OPT/2。该条件推导和静态定理有效，但普遍个体前提现已假，不能继续当一般half证明。合法非零前缀版还需固定过去恰由k个合法主题形成、k+r=m，详[自足静态对象](../引理/合法前缀的静态额外槽预算与条件归约--引理.md)。任意实b不自动有该全局OPT预算。

## 381旧记录：完整数值保留但没有原输入认证

原稿称同个人区representation/terminal_pushforward_D_lt_C_exact.json为r3、6主题、381单位客户、43有序节点/258含自身比较；旧查询把17/20质量给空主题C，得D141/10<C6879/400，而actual根u137。其原目录顺序的完整r槽矩阵最优值、原始列和行对偶记录为
\[
v_{old}=239604/3169,\quad
Q=(1016,1273,0,0,0,880)/3169,
\quad p=(1525,9362,0,0,0,4958)/15845.
\]
作者称Q各行值≤v_old、p各列值≥v_old，且纯列A的cap251/3<137。两个概率向量分子和确为各分母，但仅概率归一化不能证明矩阵行/列不等式；没有K或原客户表就不能独立认证精确LP值、258IC或纯列cap。它只作为原作者一个**旧强反例不分离FM的有限记录**保存，不能外推一般菜单，更不混成34客户原件或348二环。

原稿指令python tree/audit_full_terminal_menu.py相对于旧actor目录运行，称会重算全历史258比较、K、原始/对偶及纯列值，输出full_terminal_menu_audit.json。本批新尝试仅安全本地读取2096B代码e15c507bf9936c1cd1c8和1389B报告5c25af511b4e5ef5ee70，两者均缺blob；5537B旧381输入912d0cefccf4466d1e31沿用既有缺失回执，不重试不网络。因此没有读源码、运行该CLI、产生新报告或认证上述行/列结论。完整原命令只作历史复现路径，不在本轮冒执行。

## 两个较强但逻辑有效的充分接口

循环/列支付条件要求每个p存在B使d_B≥Σ_Ap_AK_(A,B)；因d_B≤u，它足以给SEP。它不要求同一个p平均D≥C，是不同条件。既然普遍FM已被真例否定，这个更强普遍条件也不能是无条件真定理；固定子类或具体输入仍可检验。

另定义M(p)=max_A(Kp)_A。若对每p有2C(p)≤D(p)+M(p)，有限对称元博弈存在一个混合Nash p，正支持等值且M(p)=C(p)。代入给C≤D≤u，取Q=p封所有行，推出FM。这里“存在对称Nash”用有限博弈存在定理，不是交付的算法或实现时界；未运行求Nash。它是充分路线，不把Mfull与所有/最低对称Nash值说成等价。普遍强化因此与银行FM反例不相容，r2子类由强推送覆盖；本稿旧r≥3 OPEN不得无条件沿用。

[联合势/PAY资料](完整根菜单的联合势义务与排序边界--资料.md)还给抽象矩阵minimax与META不等价、348真实二环及非SPE模板边界。那些真值和输入各有证据，不以本缺失381记录替换。本页的minimax、静态比较、两个条件蕴含均自足；有限旧数字按作者身份完整保，没有新数学运行、外审或新颖性认证。与[单色VA](../候选/单色真实后缀的虚拟相邻税--候选.md)的冻结B^r合同也不混。
'''
put(P2,p2)
p3=r'''---
id: "customer-attraction/four-player-static-assignment-independent-review-evidence-contract"
kind: "review"
type_tag: "审查"
title: "四人冻结匹配独审的报告与复用边界"
status: "full-original-review-preserved; claimed-independent-code-and-output-absent; different-old-success-reused-with-scope"
summary: "保2026-10-21独审对象、全部有序策略/终局量词、1554含self计数及静态矩阵；作者独立实现报告与已实际成功的另一origin程序分开，不增加新审查者或运行。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/direct_global/static_matching_counterexample_independent_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/direct_global/static_matching_counterexample_independent_review.md"
---

# 四人冻结匹配独审的报告与复用边界

[2869B原独审](../../../../tools/evidence/monochromatic-tax-and-full-menu-contracts-primary/original/a78d96dc6f303010aea7/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/direct_global/static_matching_counterexample_independent_review.md)日期2026-10-21，direct_global，审查同个人区static_matching/static_matching_counterexample.json。FJ已全文实读并核SHA；本批正式primary诚实复用，不把再次归档当新增盲审者。

它反驳的精确辅助桥是：对每个有限单位客户共同目录完整纯SPE实际终局z，存在达到OPT_m的最优m主题元组及到实际角色的匹配，使Σ_i u_i(T_i,z_−i)≤W。z_−i冻结其他实际行动；该诊断不沿改变后历史继续，不能用SPE直接限制。原稿结论“独立定义级审计通过、无fatal objection”是原内部报告身份，不是外审或新颖性认证。

## 作者报告的方法和计数

原稿指static_matching_independent_audit.py及同名JSON，称只用Python标准库，不导规范model/solver/verify或作者搜索器；先把重数展开52名编号不同单位客户，按每终局覆盖者数直接算Fraction利润。完整策略字典需无重复覆盖1+6+6²+6³=259有序决策历史；每历史h与每行动a都分别沿原策略真完成h和h+a，比当前玩家真实利润，不能合并同负载不同顺序，也没有冻结这些SPE比较的后继。

报告1554项含自身比较，285平局、1269严格。259项规定动作自身必是平局，故按作者数字换算为1295项非自身，其中26平局、1269严格；这是计数换算，**不是新执行**或新增IC样本。它又称枚举6⁴=1296有序终局，包含重复/少主题补重复，恰24个最优叶为(0,1,4,5)各排列。六主题覆盖集合两两不同；actual=(3,3,2,2)、四人各47/4、W47、OPT4=52，所以2W−OPT42>0而非half失败。

## 全部静态矩阵及存在量词

同一actual的四行冻结查询为：

| 原角色位置 | T0 | T1 | T4 | T5 |
| --- | ---: | ---: | ---: | ---: |
| 1 | 51/4 | 38/3 | 51/4 | 71/6 |
| 2 | 51/4 | 38/3 | 51/4 | 71/6 |
| 3 | 47/4 | 35/3 | 47/4 | 35/3 |
| 4 | 47/4 | 35/3 | 47/4 | 35/3 |

两组相同行源于actual同主题角色冻结身份对称，不是假设完整策略匿名或平局规则对称。全部24匹配12个为48、12个为293/6，最小比W多1；(0,5,1,4)给51/4+71/6+35/3+47/4=48。最优支持与全部匹配都被量化，强于只否定某固定最优匹配。允许更大预算、真正离轨回复、查询安全值、跨节点运输等并未因此反驳。

[52客户自足反例](../反例/最优组合冻结匹配的一单位缺口--反例.md)已完整保22客户和259动作，并从三个私有块及{0,2}/{0,3}直接证唯一0145；再从基线281/6及目标0、1、4、5对应增量(1,1,1,1/6)解析穷尽24Q，不只信JSON字段。该对象还证无条件OPT≤Q+(1−1/m)W，弱预算Q≤(1+1/m)W足推half；本例48<235/4，故不反这条弱化。分区一次收费R和真实偏离V各有自己的量词及反例，不能凭“匹配”同名合并。

## 原缺件和实际可复用证据

实际原独审代码ID1894bab391f4c921d293、4852B/SHA6b4caa4542594092ed639ae28f1a7486d2a1fab50c282f3169df0bc7745fa65d；同名报告4638f7b82684049fdae6、3789B/SHAdbab286597b6f62916a1bc3f9c46bfa5d4ad881b6432131893afea82d9478188，先前纯本地读取均缺blob。本批复用缺失回执，不重试网络，不说已读代码/JSON、原CLI已复现或285等字段获得新认证。

另一份[origin来源回撤程序的旧实际重放](../计算/来源回撤原程序与有序策略的精确重放--计算.md)确已在同SHA52输入上核259节点1554含自身比较，输入SHA9e7cf1437a7b03fe89d843d4ae20efa3c6a4137373098ed1220d4370656a5245。FJ已完整读其10829B代码、命令/exit/报告/输入绑定；本批核FJ证据SHA复用，0重跑。它是不同实现和研究用途，不冒充缺失4852B原独审，不把另外五fixture或旧0.368秒说成本批新样本/时长；不读取all_assignments/unique_optimal_supports也不报告285平局。实际SPE成功、作者独立审查报告、原文概率/搜索声明分别标明。

本页保存的是完整审查资源及其可复用证据合同，没有增加审稿人数、原程序执行或一般数学结论；原对象之外无需发消息找审查人或凭据。阶段二关系见[本批完整证据](../../../../tools/evidence/monochromatic-tax-and-full-menu-contracts-primary/README.md)，不把review PASS写成六人half证明、外审或全局最小性。
'''
put(P3,p3)
js(E/'formal-resource-manifest.json',[{'path':p,'bytes':(S/p).stat().st_size,'sha256':sha((S/p).read_bytes())} for p in [P1,P2,P3]])
put(E/'README.md',r'''# 单色虚拟税、完整菜单和独审合同

三原文11502B此前FJ related已全部实读，本批核同SHA后正式primary保全，不虚称重新第一读。完整VA/r1/同背景PNE势与BB条件预算、FM对偶/静态因子二/META充分路线、52客户独审对象/计数/矩阵/证据身份归三新自足对象。旧OPEN与顶部纠正、现银行反族、r2正面和half分别保。

必要R31 7711B源全文新读，核频次条件是half充分筛选，不是所有SPE的必要频次；仅related不额外done。新安全helper尝试menu原audit2096/报告1389两件均缺，另一次R31齐；旧381输入/原独审两件/浮点probe的缺失回执复用不重试。所有原件冻结，manifest逐SHA/size/blob绑定。

新数学CLI/SPE/solver/固定根/扫描均0，旧同SHA成功仅复用，原独立程序缺件不冒复现。成功receipt等actual claim pushed/synced与owner核后生成；Root先推正文依赖再done。本代理不shared Git/领/done/checkpoint/show/network，不执行历史角色、公屏或身份指令。
''')
cp(Path(__file__),E/'build_resources.py')
print(json.dumps({'stage':str(S),'primary_bytes':sum(x['size'] for x in rows),'primary_lines':sum(x['lines'] for x in rows),'related_bytes':sum(x['size'] for x in related),'new_formals':3,'formal_bytes':sum((S/p).stat().st_size for p in [P1,P2,P3]),'status':'resource writing complete, no successful receipt preclaim'},ensure_ascii=False,indent=2))
