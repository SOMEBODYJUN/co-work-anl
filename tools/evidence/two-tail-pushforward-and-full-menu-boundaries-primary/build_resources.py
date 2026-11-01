from pathlib import Path
import json,hashlib

R=Path('/workspace/scratch/37f0f9248cfc');C=R/'boss4-next-cache';REPO=R/'boss4-research';S=C/'r3-two-tail-pushforward-and-full-menu-boundaries-primary';E=Path('tools/evidence/two-tail-pushforward-and-full-menu-boundaries-primary')
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
def rd(p):return json.loads((S/p).read_text())
primary=rd(E/'source-manifest.json');related=rd(E/'related-source-manifest.json');byid={x['id']:x for x in primary+related};claim=rd(E/'actual-claim-receipt.json')
ids=['c7681bcaecb3e63137ff','7fd268a01ce3f10dcb2a','6c84043505685faee8ec','68ed7412ef2da880f80f','5ea43c826b2651fe9de7'];assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(claim['ids'])==set(ids)
for x in primary:
 p=json.loads((REPO/'cleanup/progress'/f"{x['id']}.json").read_text());assert p['owner']=='Boss4' and p['disposition']=='in-progress' and p['source_sha256']==x['sha256']
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def link(i):return '../../../../'+byid[i]['preserved_path']
def head(id,kind,typ,title,status,summary,sources):
 a=['---',f'id: "customer-attraction/{id}"',f'kind: "{kind}"',f'type_tag: "{typ}"',f'title: "{title}"',f'status: "{status}"',f'summary: "{summary}"','source_refs:']
 for i in sources:
  for z in inv[i]['sources']:a.append(f'  - "source:{z["commit"]}:{z["path"]}"')
 return '\n'.join(a)+'\n---\n\n'

P1=Path('archives/customer-attraction/state/引理/末位真实回复推送的锐曲率与双分支式--引理.md')
body1=r'''# 末位真实回复推送的锐曲率与双分支式

## 完整输入和独立审查身份

[6035B发现稿](SRC_MAIN)及[5009B实际独审](SRC_REVIEW)全部实读。后者先只据陈述盲重构、再读发现稿对照，是历史审查方法；本次读双方后归档不重新冒称盲证、外审或新颖性。此前DY已保存部分平均式；这里补全确定性双分支、全等号条件及逐参数锐族。

有限单位客户、有限非空共同目录，固定一个合法有序过去，其负载b_x为非负整数。恰有两位剩余；首位强制B后，原策略在该完整有序历史的末位最佳回复记rho(B)=R。任意平局可选不同主题。**不要求首位行动自身最优**，只要求每个相关末位节点真实BR。代数还允许任意实b_x≥0；这扩大数学接口，不把实b冒作原单位历史的合法前缀。

任取合法主题law p。B~p，A~p独立于产生竞争槽的(B,R)。定义

\[
D=\mathbb E_B\sum_{x\in B}\frac1{b_x+1+\mathbf1_R(x)},\quad
C=\mathbb E_{A,B}\sum_{x\in A}
\frac1{b_x+1+\mathbf1_B(x)+\mathbf1_R(x)}.
\]

D是真实根强制收益均值，C是独立查询面对**完整两槽**(B,R)的插入价。不能删B，不能把A=B同一次抽样，也不把R看成与B独立。令p_x=Pr(x∈B)、q_x=Pr(x∈R)、j_x=Pr(x∈B∩R)，w_x=1/[(b_x+1)(b_x+2)]。

## 精确非负分解

独立再抽B'~p，R'=rho(B')。共同目录使R'在固定B后的真实末位节点也可作为合法偏离。由逐节点BR，

\[
L=\mathbb E_{B,B'}[U_b(R,B)-U_b(R',B)]\ge0,
\quad U_b(X,Y)=\sum_{x\in X}\frac1{b_x+1+\mathbf1_Y(x)}.
\]

写f(X)=Σ_X1/(b+1)、g(X,Y)=Σ_{X∩Y}w，则U=f−g。R,R'同分布使裸值相消，B与R'独立，故

\[
L=\sum_xw_x(p_xq_x-j_x).
\]

非负性只对完整主题比较的**总和**成立，逐客户项可以为负，不假设每名客户负相关。二元membership直接展开得

\[
D_x=\frac{p_x}{b_x+1}-w_xj_x,
\quad C_x=p_x\left[\frac1{b_x+1}-w_x(p_x+q_x)
+\frac{2w_xj_x}{b_x+3}\right].
\]

相减、取出L并用0≤j_x≤p_x，得到

\[
\boxed{D-C=L+\sum_x\frac{p_x^2}{(b_x+2)(b_x+3)}
+\sum_x\frac{2w_xp_x(p_x-j_x)}{b_x+3}.}\tag{PUSH}
\]

所以D−C≥Σp_x²/[(b_x+2)(b_x+3)]≥0。空主题、p_x=0和零客户均不除零；有任何p_x>0时D−C严格正，p只支持空覆盖时D=C=0。若当前首位也满足SPE，则actual u≥D，才进一步给C≤u；首位最优性不是PUSH本身的前提。

## 等号条件和精确锐性

相对曲率下界取等，恰需L=0且每个p_x>0的客户j_x=p_x。后一条件指源覆盖的每个正概率客户几乎必然也被回复覆盖；L=0等价于每个正概率(B,B')的rho(B')在固定B后同样是BR，因为其单项均非负。不能把L=0误写为逐客户p_xq_x=j_x。

单客户x，目录{空主题,{x}}，任意实b≥0，两个首行动后末位均选{x}，且这是唯一BR。令p({x})=t∈[0,1]，其余为空，则p=t,q=1,j=t，L及PUSH末项都为0，

\[
D=\frac t{b+2},\quad
C=\frac{t(1-t)}{b+2}+\frac{t^2}{b+3},\quad
D-C=\frac{t^2}{(b+2)(b+3)}.
\]

每个b,t均取等，故一般量词下曲率系数不能统一增大。这是解析族，不是有限抽样锐性证据。

## 确定性的两条真实分支

取任意首主题A,T，真实回复R=rho(A)、S=rho(T)。定义G_X(Y,Z)=Σ_(x∈X)1/[b_x+1+1_Y(x)+1_Z(x)]，r_x=1_R(x)、s_x=1_S(x)。准确有

\[
U_b(A,R)+U_b(T,S)-G_T(A,R)-G_A(T,S)
=[U_b(R,A)-U_b(S,A)]+[U_b(S,T)-U_b(R,T)]
\]
\[
\qquad+\sum_{x\in A\cap T}\left[
\frac1{(b_x+1+r_x)(b_x+2+r_x)}
+\frac1{(b_x+1+s_x)(b_x+2+s_x)}\right]\ge0.\tag{PAIR}
\]

两个方括号分别是历史A、T下末位对另一个合法回复的真实BR松弛。逐客户分首membership00/10/01/11：00零，10及01给w乘对应回复membership差，11剩显示的正曲率项；所以是逐客户恒等式，不把一枝的回复搬到别枝当最佳。独立A,T~p后平均PAIR并除二，正好恢复PUSH。

[最大裸回复纯列](../引理/两名剩余完整终局菜单的纯列封顶--引理.md)则先取一个B*同时封顶全部行；这里对每个p用同p推送的Q=p并保锐余项。两者都是正确的恰一后继接口，抽样与结论不同，不能换名当一般人数证明。

## 三人强式失败及实际收益松弛

源引用的[7992B完整34客户输入](SRC_EMPTY)也全文读，包括13类型、七标签含空主题6、全部57有序动作及附带字段。它同SHA已由既有父方单位审计成功核342个非自身比较，本次[现行审计记录](../审查/额外槽扫描的实际强桥目标与两份定义级核验--审查.md)及其执行记录已完整比较，**不复跑全树**。

p只在主题2给1/10、空主题6给9/10。强制2叶(2,3,4)，根d2=29/3、自插入K22=13/2；强制空叶(6,0,1)，根0、查询2价K26=32/3。于是

\[
D=\frac1{10}\frac{29}3=\frac{29}{30},\quad
C=\frac1{10}\left[\frac1{10}\frac{13}2+\frac9{10}\frac{32}3\right]=\frac{41}{40},
\quad D-C=-\frac7{120}.
\]

actual u=29/3，因此u−C=1037/120>0。空行0不可能与正价行同时作为这一p的META-Nash正支持；它不是低值meta-Nash或Mfull失败证据。它只否定多后继无条件D≥C；源所说一般C≤u仍OPEN是历史状态，当前[银行完整根菜单](../反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)另已否定普遍实际u桥，不能从这个正松弛例反向恢复它。

本批只新增一次固定根算术，核原输入SHA及这些价/差，见[新报告](../../../../EVID/runs/new-branch-arithmetic-001/report.json)；原CLI/全历史复演0次。原较大的representation/terminal_pushforward_D_lt_C_exact.json仅按发现稿引用保其独立来源；本批未读取该较大输入，不把它与本34客户输入合并。一般half、实际路径聚合预算及可自由改选对手分布各有不同量词，未由PUSH或这个失败例解决。
'''
body1=body1.replace('SRC_MAIN',link('6c84043505685faee8ec')).replace('SRC_REVIEW',link('38f33a2ab903eb816fc8')).replace('SRC_EMPTY',link('f218c3c894b4635ecca2')).replace('EVID',str(E))
put(P1,head('true-final-reply-push-sharp-curvature-and-two-branch-identity','lemma','引理','末位真实回复推送的锐曲率与双分支式','proved-for-one-final-BR-with-arbitrary-real-background; multi-reply-extension-false','完整保任意p的精确余量、确定性两分支式、总BR而非逐客户符号、全等号条件和逐参数锐族；34客户强式失败与actual收益松弛分别核算，不扩到half。',['6c84043505685faee8ec','38f33a2ab903eb816fc8'])+body1)

P2=Path('archives/customer-attraction/state/反例/后继边际价格付款的两类尺度障碍--反例.md')
body2=r'''# 后继边际价格付款的两类尺度障碍

## 两份不同输入域的原件

[2057B合法前缀稿](SRC_PREFIX)和[3237B空背景反族](SRC_ZERO)均完整实读、两冻结位置同字节。以下把前者过去人数记h、后者单客户主题数记s，避免原稿都用k却对象不同。它们否定的是用真实后继平均主题价格替换最大查询价的加强支付，均非一般half反例。

给完整根矩阵K（行独立额外查询、列保当前根的真实完整终局），任意源/查询law p，D=Σp_a d(a)，C=p^TKp，v=Kp，M=max_a v(a)。被测TailPrice为2C≤D+v(q_tail)；原较弱2C≤D+M保留。p若是对称META-Nash，则v(q_tail)≤C，但不能因任意p的加强式失败就宣称META限定推送失败。

## 真实过去使固定正系数失配

取h≥0、正整数L，原m=h+2人，共同目录仅两个不交主题A/B，大小mL/L。所有有序历史规定：只有末位且此前全A才选B，其他都A。若此前有b≥1个B，当前A得mL/(m−b)>L/(b+1)的B偏离；全A的非末位A得mL/(m−1)>L；全A末位两行动均L，指定B合法。因此是完整SPE，实际A^(m−1)B且W=OPT_m=(m+1)L。

实际h次A之后余两人。强制A后末位B，强制B后末位A；此过去是真实原策略的实际前缀，不能将余2人当原m人。完整两列均含A/B，保背景h，

\[
K=\begin{pmatrix}L&L\\L/2&L/2\end{pmatrix},\quad
p=\delta_A\text{为严格纯META-Nash},\quad C=L,\quad D=\frac{(h+2)L}{h+1}.
\]

独立重查的q_tail=delta_B，q_full=(delta_A+delta_B)/2，故v(q_tail)=L/2、v(q_full)=3L/4，D−C=L/(h+1)。价差比准确为

\[
\frac{D-C}{C-v(q_{tail})}=\frac2{h+1},\qquad
\frac{D-C}{C-v(q_{full})}=\frac4{h+1}.
\]

尾版alpha1恰h≥2严格失败，全槽版恰h≥4失败；任意背景无关alpha>0取h+1>4/alpha就反驳D−C≥alpha(C−v(q_full))。这是同份完整SPE的合法实际过去，不是任意数值背景伪例。原候选M=C=L<D、全p C≤L≤D、自由菜单均在此族成立。

原稿h2,L2的十客户四人点给D8/3,C2,tail1，违反1/3，数值正确；但称它“最小本族例”不符合原文L≥1。取h2,L1已是五客户四人点A4/B1，D4/3,C1,tail1/2，违反1/6；一般完整策略证明直接适用，无须另造离轨补全。h的首个尾版违反为2，L最小1，所以五客户是**该显式参数族**的最小值，不声称全模型最小。保原十客户作历史展示，原件不改。全槽首个违反对应h4,L1、七客户六人，违反2−6/5−3/4=1/20，仍福利最优。

[完整全人数版本](../引理/完整槽插入税与跨角色价格恒等式--引理.md)还给任意2≤r≤m的精确必要alpha上限2r/(m−1)、尾版2(r−1)/(m−1)；没有证明这些上限对一般输入充分。本页保原两尾特化及范围勘误，不覆写旧全人数对象。

## 空背景、零真实激励松弛也会失败

现在恰两人、无过去。A含两个私有单位客户，B_1,…,B_s各一个不同且全不交客户，s≥1。根A，末位在每个首历史都A。首A后末位A得1、每singleton也1，允许平局；首B_i后A得2严格胜过其他最多1。根任何行动后都得d(a)=u=1，故完整SPE，任意p都有D=1、根真实松弛u−D=0。

取p(A)=t、各p(B_i)=(1−t)/s，0≤t≤1，唯一后继边际q_tail=delta_A。独立完整两槽查询直接为

\[
v(A)=1-t/3,\quad v(B_i)=1-(1-t)/(2s),\quad
C=1-t^2/3-(1-t)^2/(2s),
\]
\[
\boxed{2C-D-v(q_{tail})=\frac{t(1-2t)}3-\frac{(1-t)^2}s.}\tag{TAIL}
\]

t=1/3、s13给15单位客户/14标签，v(A)=8/9、v(B_i)=38/39，C332/351,D1，违反1/351。p正支持上两个收益不相等，故**不是META-Nash**。M38/39，原较弱2C≤D+M仍严格成立；C<u，实际W2、OPT2=3，half也成立。

## 族内参数阈值的解析证明

t=0或t≥1/2时TAIL≤0。0<t<1/2时，严格违反恰要求

\[
s>\frac{3(1-t)^2}{t(1-2t)}\ge12,
\quad 3(1-t)^2-12t(1-2t)=3(1-3t)^2\ge0.
\]

最小12仅t1/3取到。因此s≤12无严格违反，s≥13以t1/3给正差(s−12)/(27s)。这是原稿“本族阈值12”的完整因式证明，不依赖扫描，也不声称全体TailPrice例的最小主题/客户数。

两族的机制和量词分开：第一族合法背景、纯META-Nash，把当前A分母缩回一位的增益压小；第二族空背景、非META p，许多合法singleton查询抬C但真实后继始终A，无法代替max价格。两者都兼容[两人任意p正推送](../引理/末位真实回复推送的锐曲率与双分支式--引理.md)，后者仅比较C≤D，不给TAIL。由于C≤M且C≤D，两人较弱2C≤D+M确实成立，不能把其加强式失败扩成该结论失败。

本批只对已解析族作少量有理代入并存[固定算术报告](../../../../EVID/runs/new-branch-arithmetic-001/report.json)，无新策略搜索、原CLI或全SPE重跑。没有外审、新颖性或全模型最小性认证。
'''
body2=body2.replace('SRC_PREFIX',link('7fd268a01ce3f10dcb2a')).replace('SRC_ZERO',link('5ea43c826b2651fe9de7')).replace('EVID',str(E))
put(P2,head('tail-marginal-price-payment-two-scale-obstructions','counterexample','反例','后继边际价格付款的两类尺度障碍','proved-analytic-counterfamilies; parameter-family-minimum-wording-corrected; no-half-failure','区分合法实际过去的纯META-Nash比例失配与空背景任意p加强式失败，保全部策略/参数/阈值；原十客户是展示点，同族五客户已有违反，不认证全模型最小。',['7fd268a01ce3f10dcb2a','5ea43c826b2651fe9de7'])+body2)

P3=Path('archives/customer-attraction/state/资料/完整根菜单的联合势义务与排序边界--资料.md')
body3=r'''# 完整根菜单的联合势义务与排序边界

## 两份主源及时间范围

[5748B完整势身份稿](SRC_COL)与[6262B混合菜单稿](SRC_MENU)全部实读，含后者2026-10-25显式接续更正。两冻结位置分别同字节。头部已说逐位置Mfull≤u被零根保险反族否定；后面2026-10-22正文的“仍OPEN/仍可自由混合”保其历史用途，不能反向覆盖头部或当前[银行完整根反例](../反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)。本页保精确条件关系、真实正面组件和失败模板，不将一个被否定的普遍个体菜单继续列为已证或当前待证。

固定合法有序前缀b，余r≥1人，同一完整有序历史纯SPE，保空主题、重复和任意离轨平局。强制根A后真实后继Y_A长r−1，完整列Z(A)=(A,Y_A)。记d_A根实际收益、u=max_A d_A，

\[
K_{T,A}=\sum_{x\in T}\frac1{b_x+1+c_x(Z(A))},\quad
M_{full}=\min_{Q\in\Delta(\mathcal S)}\max_T(KQ)_T.
\]

查询与列随机化独立，竞争r槽含强制根自身。r−1尾菜单、所有静态对手、实际全路径菜单不能因都叫“菜单”就替换可行域。

## 完整联合势与真正的混合义务

令Phi_b(Y)=Σ_xΣ_(j=1)^(c_x(Y))1/(b_x+j)，F_A=Phi_b(Y_A)，

\[
R_{AB}=\Phi_b(A,Y_B)-\Phi_b(A,Y_A),\quad
\delta_{AB}=\sum_{x\in A\cap B}
\frac1{(b_x+1+c_x(Y_B))(b_x+2+c_x(Y_B))}.
\]

精确COL为K_AB=d_A+F_A−F_B+R_AB−delta_AB。证明先相加d_A+F_A−F_B+R得到A对Y_B的插入，再加源首位B减去正交集税；Y必须排除当前根。它是记账恒等式，不把后继组当共同最大化势的一个玩家。

固定行law p和列law Q，e(p)=u−Σp_A d_A≥0。将COL平均后，p^TKQ≤u**恰等价**

\[
\mathbb E_{p,Q}R_{AB}\le e(p)+\mathbb E_{p,Q}\delta_{AB}
+\mathbb E_QF_B-\mathbb E_pF_A.\tag{PAY}
\]

对这一固定实例的Mfull≤u，有限零和minimax等价于每p存在Q支付PAY；恒等式本身不证明这样的Q存在。Q=p时漂移抵消，C(p)−D(p)=E R−E delta，不能删去R或真实e(p)。当前普遍Mfull已假，PAY仍可作为明确固定输入/分布的准确条件，不另造一般存在性定理。

## 静态比较与低值META的不同量词

真正v_(r+1)(b)允许全部r个合法静态对手，而Mfull只用真实根列，故v_(r+1)(b)≤Mfull。若每actual节点都有Mfull≤u，固定实际过去加该节点的r槽恰成原m槽，条件上每位u_i≥v_(m+1)(0)。静态因子二比较OPT_m≤2m v_(m+1)(0)于是给half；这个蕴含有效，普遍前提没有因静态代数正确而成立。

这里对全局零背景的任意m槽背景B，定义f_B(T)=Σ_(x∈T)1/[1+c_x(B)]。静态因子二可自足看出：最优m元组的客户重数d_x和任意m槽背景重数c_x满足1_(d>0)≤(d+c)/(1+c)。故OPT≤Σ_j f_B(T_j)+Σ_(a∈B) f_B(a)。对任意随机背景Q，首项≤m max_T E f_B(T)；第二项ΣE[c/(1+c)]≤ΣE c E[1/(1+c)]，因倒数递减的协方差非正。后一项等于均匀随机背景槽边际作为独立查询的m倍价，也≤m同一max价。再对全部合法背景Q取min，有限minimax给上述v界。它没有保证真实菜单里有便宜Q。

对称META-Nash p有Kp≤lambda·1、正支持取等、lambda=p^TKp；低值lambda≤u足以取Q=p给Mfull≤u，但不是一般等价。抽象矩阵

\[
K=\begin{pmatrix}2&1\\3&0\end{pmatrix}
\]

唯一对称Nash p=(1/2,1/2)，值3/2；零和值却1，取第二纯列即达，且任何列混合的首行1+q≥1。两纯p均可被另一行动改进，混合行收益相等只在q1/2，故唯一性也明确。**没有声称这个矩阵可由真实CAG根菜单实现**，它只证明逻辑上低Nash比minimax更强；不能从一个低Nash寻找失败自动否定Mfull。

## 恰两人已闭合的正面接口

恰r2时R_AB是一个真实末位BR差，≤0。[最大裸回复纯列](../引理/两名剩余完整终局菜单的纯列封顶--引理.md)完整保存精确税、无环标量和取最大F_B的同时封顶。另一选择是取所有合法主题对的全局最大Phi_b(A,R)；该A后的任何原末位BR仍到同一全局势最大，故这份真实列是静态PNE，额外插入价≤替换根的价≤d_A≤u。

[任意p锐推送](../引理/末位真实回复推送的锐曲率与双分支式--引理.md)又给D−C的非负曲率，甚至不需当前根最优。不能把这些恰一后继事实说成一般SPE路径都是PNE、一般联合R≤0或普遍根菜单完成。

## 三人二环：无环与共同势排序确实失败

[7417B原348客户完整输入](SRC_CYCLE)的18类型、全部43有序动作、六根路径、矩阵和附带字段均全文读；同SHA已在[既有来源回撤审计](../计算/来源回撤原程序与有序策略的精确重放--计算.md)核完整SPE，执行记录/输入绑定本批实读复用，不重复258项全树比较。该旧审计只消费实例与策略，未核全部二环附带字段；因此本批新增一次根算术，直接重建六根K/Phi并核这些字段。

所有根d_A=u147/2、完整Phi304，K_(5,2)=K_(2,5)=159/2>u，所以按源a到查询t、阈值K_ta>u的图有2↔5二环；同势也否定“高插入边必严格提高共同完整势”。新算术在两边还得F漂移0、联合R12、正交集税6，COL恰159/2=147/2+12−6，给出多后继R真可正的同一SPE见证。

列cap依次69,159/2,159/2,69,159/2,159/2；列0和3都69<u，因此二环不否定这个实例的纯防御列或自由Mfull。六列势全相同又说明“任取最大势列”也不能保证cap；不能把存在好最大势列误当全部最大势列都好。

源另报告791客户的更强严格势下降：u187,d5=184,K_(5,1)=196，而Phi Z5=1505/2<Phi Z1=1511/2；还有K_(2,4)=409/2>u且两列均最大势1511/2。该phi_rise独审JSON本地缺，原实例/报告没有在本批取得，故这里只保**原稿明确有限断言**，不称本次已认证数值或新反例输入。实际已核348例足以停共同严格标量/无环加强，但不冒充重核791的严格下降。

旧八人两块纯列候选也仅按该稿当时“完整DAG仍在检查”保留，不能拿后来别族已否定Mfull回填成旧DAG已认证。

## 根最优加末位BR仍可只是非SPE伪菜单

三人三个不交singleton A/B/C，规定第二位复制首主题；末位在AA/BB/CC后分别B/C/A，其它二历史取缺失第三主题。这给全部末位BR，根三分支AAB/BBC/CCA的根收益均1/2。但第二位在首A后可从复制A的1/2改B，末位真续局C使其得1，所以计划不是SPE。

其完整列K每行每列为(1/3,1/2,1)的排列，uniform行/列均给11/18，故uniform是对称META-Nash、minimax值也11/18>根1/2。复制后的粗分母floor仍只见1/2。这个例子完整说明只用根IC、末位BR、粗floor和META条件不足；它是证明模板的非SPE反例，不是一个合法SPE菜单失败证书。

## 接续和运行边界

旧文提出用平均终局主题价v(q)支付D−C的想法，现有[两类TailPrice反族](../反例/后继边际价格付款的两类尺度障碍--反例.md)分别处理空背景任意p、非零实际背景META p，不能再将它当一般加强。若研究全路径或聚合版本，须重新给出具体背景可行域、查询独立性与一份actual预算，不能仅沿用“Mpath”名字就宣称本文旧OPEN已认证为现状。

[原独审稿](SRC_REVIEW)的真实一后继证明与本页多后继缺口分别保留；原tree公式审计摘要273B本地也缺，只存缺失回执，不把其16模式实现声称已读/重跑。原CLI、全SPE复演、solver和样本扫描本批0次；唯一新增是输入绑定的固定根算术及参数有理代入，[运行记录](../../../../EVID/runs/new-branch-arithmetic-001/run-metadata.json)为一次0.069458058秒、exit0/stderr空，[完整新报告](../../../../EVID/runs/new-branch-arithmetic-001/report.json)保6根矩阵、13根路径及正R。有限算术不替代解析全参数证明、外审或新颖性。
'''
body3=body3.replace('SRC_COL',link('c7681bcaecb3e63137ff')).replace('SRC_MENU',link('68ed7412ef2da880f80f')).replace('SRC_CYCLE',link('23b69044426c185f1653')).replace('SRC_REVIEW',link('38f33a2ab903eb816fc8')).replace('EVID',str(E))
put(P3,head('full-root-menu-joint-potential-obligations-and-order-boundaries','resource','资料','完整根菜单的联合势义务与排序边界','exact-conditional-menu-ledgers-and-r2-components; universal-individual-menu-refuted; missing791-reported-only','保任意r完整COL、混合PAY及minimax/META量词区别；复用旧SPE并新增根算术核348二环R12税6，791只保缺失证据的原稿断言，非SPE模板不升级真反例。',['c7681bcaecb3e63137ff','68ed7412ef2da880f80f'])+body3)

contexts=[
'archives/customer-attraction/state/引理/完整槽插入税与跨角色价格恒等式--引理.md',
'archives/customer-attraction/state/引理/两名剩余完整终局菜单的纯列封顶--引理.md',
'archives/customer-attraction/state/反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md',
'archives/customer-attraction/state/反例/笛卡尔银行目录的逐人分数门槛反族--反例.md',
'archives/customer-attraction/state/反例/同分布额外查询高于平均强制收益--反例.md',
'archives/customer-attraction/state/引理/完整终局查询的信用恒等式与末两位付款--引理.md',
'archives/customer-attraction/state/计算/响应恒等式与分支条件的精确回归--计算.md',
'archives/customer-attraction/state/反例/逐客户条件与完整推送桥的反例层级--反例.md',
'archives/customer-attraction/state/计算/来源回撤原程序与有序策略的精确重放--计算.md',
'archives/customer-attraction/state/审查/额外槽聚合桥独立单位审计--审查.md',
'archives/customer-attraction/state/审查/额外槽扫描的实际强桥目标与两份定义级核验--审查.md',
]
ctx=[]
for n in contexts:
 b=(REPO/n).read_bytes();cp(REPO/n,E/'context'/n);ctx.append({'path':n,'bytes':len(b),'sha256':sha(b),'snapshot':str(E/'context'/n),'read':'actual full current or prior exact formal read reused; no extra source done'})
js(E/'context-manifest.json',ctx)
js(E/'formal-resource-manifest.json',[{'path':str(p),'bytes':(S/p).stat().st_size,'sha256':sha((S/p).read_bytes())} for p in [P1,P2,P3]])
cp(Path(__file__),E/'build_resources.py')
print(json.dumps({'new_formals':3,'formal_bytes':sum((S/p).stat().st_size for p in [P1,P2,P3]),'paths':[str(p) for p in [P1,P2,P3]],'contexts':len(ctx)},ensure_ascii=False))
