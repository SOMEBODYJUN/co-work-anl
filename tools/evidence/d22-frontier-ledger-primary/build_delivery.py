from pathlib import Path
import json,hashlib,re,posixpath
R=Path('/workspace/scratch/37f0f9248cfc'); REPO=R/'boss4-research'; C=R/'boss4-next-cache'; S=C/'r3-d22-frontier-ledger-primary'; E=Path('tools/evidence/d22-frontier-ledger-primary'); W=Path('cleanup/workspaces/Boss4/r3-d22-frontier-ledger-primary-next')
IDS=['45e100f077a8140e075a','2af13b75b47002b37dd9','f0a5782a749aa4578fc7','844fdc7b457c263049cf']
P1='archives/customer-attraction/state/资源/真实分支十项合同与菜单可实现性账本--资源.md'
P2='archives/customer-attraction/state/障碍/最优剩余利润的局部系数与共享负载信用--障碍.md'
P3='archives/customer-attraction/state/引理/单色真实后缀的饱和查询与剩余税--引理.md'
P4='archives/customer-attraction/state/障碍/双向隔离惩罚的福利上限与逃逸预算--障碍.md'
PS=[P1,P2,P3,P4]
inv={x['id']:x for x in map(json.loads,(REPO/'cleanup/inventory.jsonl').read_text().splitlines())}
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,t):
 q=S/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(t,encoding='utf-8')
def js(p,d):put(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def cp(p,q):
 q=S/q;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(Path(p).read_bytes())
def rawman(mp,kind):
 m=json.loads(mp.read_text());out=[]
 for x in m['rows']:
  v=inv[x['id']];b=Path(x['local_path']).read_bytes();assert len(b)==v['size'] and sha(b)==v['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==v['blob'];q=E/kind/x['id']/x['path'];cp(x['local_path'],q);out.append({**v,'preserved_path':str(q),'lines':len(b.splitlines()),'reading':'GS complete actual text, every section/definition/quantifier/update/numerical contract; related sources not additional primary/done'})
 cp(mp,E/f'actual-{kind}-local-export-manifest.json');js(E/f'{kind}-source-manifest.json',out);return out
primary=rawman(C/'learning-gm-next-d22-root-entries/local-export-manifest.json','original');assert {x['id'] for x in primary}==set(IDS)
related=rawman(C/'learning-gs-related-mathematics/local-export-manifest.json','related')

def front(id,kind,tag,title,status,summary):
 s='---\n'+''.join(k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in [('id',id),('kind',kind),('type_tag',tag),('title',title),('status',status),('summary',summary)])+'source_refs:\n'
 for x in primary:
  for y in x['sources']:s+='  - '+json.dumps('source:'+y['commit']+':'+y['path'],ensure_ascii=False)+'\n'
 return s+'---\n\n# '+title+'\n\n'

b2=r'''## 对象与所排除的台阶

采用有限单位客户、有限共同非空目录、单位提供者、全部有序历史纯SPE，允许重复、空主题、零客户和任意平局。合法前缀的过去负载为整数b，余r人。定义
\[
F_r(b)=\max_{Z\in\mathcal S^r}\sum_x\frac{c_x(Z)}{b_x+c_x(Z)},\quad F_0(b)=0,
\]
零分子项取零。这是**剩余提供者利润**，不是已覆盖集合的总覆盖补全，也不是额外查询静态安全值。节点实际行动A、当前最终收益u、真实尾部利润V时，P=u+V。若对全部节点有F_r(b)≤2u+F_{r-1}(b+1_A)，再用尾部F≤2V，确实足够推出F_r≤2P及根half。下面否定的是这个局部充分台阶，不是F_r≤2P本身。

## 不交大主题族：每个有限局部系数均失败

每个n≥2，A有n名客户，B_1,…,B_{n-1}各有一名客户，所有客户池不交；恰n人，目录恰这n主题。策略在**每个**长度t<n的有序历史都选A。若过去a次A，当前照做、未来全A，其收益n/(a+n−t)≥1；改任一B_j后未来仍全A，收益1/(1+过去B_j次数)≤1。因此所有历史/再次偏离都最优，是真完整纯SPE，不只实际全A路径。

实际每人u=1，W=n。A及全部单例用n槽覆盖2n−1名客户，所以F_n(0)=OPT_n=2n−1。固定第一名A，若余n−1人中k人选A，其余槽换成不同单例不减利润，且足够单例可用。全部候选的精确最优值故为
\[
F_{n-1}(1_A)=\max_{0\le k\le n-1}\left[\frac{nk}{k+1}+n-1-k\right]
=2n-h_n,\quad h_n=\min_{j\in\{1,\ldots,n\}}(j+n/j).
\]
这包括k=0与重复单例，不是连续松弛。AM-GM给h_n≥2√n；取j=⌈√n⌉给h_n≤2√n+1。根台阶
\[
F_n(0)-F_{n-1}(1_A)=h_n-1\ge2\sqrt n-1
\]
无界。给定任意有限实α，取整数q≥2且q>(α+1)/2，n=q²，则h_n=2q，台阶2q−1>αu。故不存在人数无关有限α能支付所有局部台阶，空根已足够。α=2在n=3时台阶5/2失败，n≥4由下界≥3失败；n2不冒严格失败。

实际尾部V=n−1，余量2V−Ftail=h_n−2；根系数二债h_n−3，两者相差1，恰2W−OPT=1。尾部信用按√n增长而当前收益恒1；不能把本族称half反例，也不能只把2调成更大固定系数。已知实例族的新内容是此F的精确分析，不认证原实例新颖性。

## 交叠族：17/6是另一目标的精确工具值

每个n≥4令x=n−2，目录A,B,L_1,…,L_n。每个普通j<n有类型{L_j}:x、{A,L_j}:1、{B,L_j}:x；特殊叶有{L_n}:x、{B,L_n}:x、{A,B,L_n}:n−1。各重数为不同单位客户。

完整策略：空历史A；非空历史长≤n−2，若过去全B则A，否则B；末位精确BR、平局序B,A,L_1,…,L_n。其全部有序历史分类证明见[任意人数首步补全余额](../反例/任意人数首步补全余额--反例.md)，这里实际重读全证明后复用，不把在轨激励当完整性。该旧页的F是**总覆盖补全**；本页以下重新优化利润F。

实际A B^(n−1)，u_A=n−1/n，u_B=n−1/n−1/(n−1)，W=n²−2；每叶有私有x>0，全n叶是唯一无序最优支持，OPT=2n²−2n−2。表达n−1/n始终是n减1/n。

背景一名A，余n−1槽计数a,b,ℓ_j，d为不同正叶数。精确利润
\[
P=x d+x\sum_j\mathbf1_{b+\ell_j>0}
+\sum_{j<n}\frac{a+\ell_j}{1+a+\ell_j}
+(n-1)\frac{a+b+\ell_n}{1+a+b+\ell_n}.
\]
对f(c)=c/(1+c)，移走一个正覆盖者损失1/[c(c+1)]。

若b=0，有A或重复叶时，换一槽为未用普通叶；总槽n−1保证至少两叶缺失，普通叶存在。移A的所有背景内损失≤n−1，移重复叶更小；A外不失覆盖，新叶增加2x=2n−4>n−1，因此严格改善。最优恰n−1个不同叶，含特殊叶，得到P_0=2(n−1)x+(2n−3)/2。

若b≥1，保留一个B，把A、额外B或重复叶依次换为未用普通叶。不会减少A外旧覆盖，新增至少x私有客户。移A背景内损失≤(n−1)/2+(n−1)/6=2(n−1)/3≤x；移额外B≤(n−1)/6，移重复普通叶≤1/6，移重复特殊叶≤(n−1)/12，均≤x。新叶背景内贡献非负，故可不减至a=0,b=1、n−2个不同叶。用特殊叶替换普通叶的利润增量(n−1)(2/3−1/2)−1/2=(n−4)/6≥0。故可含特殊叶和n−3普通叶，得P_1=2(n−1)x+(7n−13)/6。P_1−P_0=(n−4)/6≥0，所以
\[
F_{n-1}(1_A)=2(n-1)(n-2)+(7n-13)/6.
\]
全部整数多重集合已消元，n4等号包括在内。根差与余额为
\[
\Delta=(17n-23)/6,\quad 2u_A+Ftail-OPT=(23-5n)/6-2/n.
\]
n4余额0；每个n≥5为负，n5为−11/15。必要局部系数R_n=n(17n−23)/[6(n²−1)]→17/6；任意α<17/6最终失败（ε=17/6−α，n≥5,n>4/ε时17/6−R_n=(23n−17)/[6(n²−1)]<4/n<ε）。但17/6不是通用候选，被前节无界族加强。

实际V=n²−n−2+1/n，其2V−Ftail=(17n−35)/6+2/n；减根债仍2W−OPT=2(n−1)>0。不能以局部余额负否定整体利润half或原half。作者及独审所报n4…8合15501计数候选只核有限实现；本批没有读其程序/报告或新跑该回归，全n结论由上述消元及既有SPE证明承担。

## 共同负载可加信用的精确不可能性

一个充分信用合同是
\[
F_r(b)\le2P_h+C_h,\quad
\Delta_h+C_{hA}-C_h\le2u_h,\quad C_{terminal}\ge0,\quad C_{empty}\le0.
\]
从终端0≤C_terminal开始用局部式和尾部界可递推第一式，根边界才给half。这不是所有half证明的必要形式。循环取C_h=F_r−2P_h只把局部式化等式，根条件重述主问题，不能算证明。

排除的模板严格为C_r(b,c)=Σ_x f_r(b_x,c_x)，其中c是真实剩余r人负载，同一函数族仅依r及该客户两个非负整数负载；不依实例、客户总数、目录、其他客户或策略信息，且f_r(0,c)=f_r(b,0)=0。可负、无连续/单调/凸性假设。

all-big根后n个A客户的(b,c)=(1,n−1)，由尾部界强制
\[
f_{n-1}(1,n-1)\ge(2-h_n)/n.
\]
交叠族根后仅n−1名特殊共享客户同为(1,n−1)；普通A客户为(1,0)，其他背景0，全消失。空根信用0，由根递推强制
\[
f_{n-1}(1,n-1)\le\frac{(23-5n)/6-2/n}{n-1}.
\]
当n≥16，前界≥1/n−2/√n>−1/2；后界在n≥10已严格<−1/2，因为其分子减−(n−1)/2为(10−n)/3−2/n<0。于是同r的同一个f(1,r)上下界冲突。两个输入均真完整SPE，非抽象非均衡负载分离。

all-big第一子节点更精确要求2−h_n≤C_A≤3−h_n。这说明负信用及独占/主题替代结构的信息承重，不说明放开c=0就足够。允许背景独占项、实例或目录信息、非可加信用、全真实菜单等未被排除。尚缺独立于未知half差额的可计算状态及真实分支信用转移证明。

## 来源和接续

以上解析完整读并比较两份发现/两份独审及信用稿：related IDs5807ac87276a9bc80ce0、efb09bff2fbae18ba384、0efa8da260f6c6ee8015、c9ccc7817c179b3b1396、9bf8a294ee059185147e，全部原字节见[相关源清单](../../../../tools/evidence/d22-frontier-ledger-primary/related-source-manifest.json)。原“先盲重构再对照”是当时审查先验，当前知情清洗不新增独立审稿人。无新数学程序、无旧成功重跑、无外审/新颖性认证。上述三障碍互相加强/合用，不反驳真安全聚合、自由静态门槛或六人half。
'''
put(P2,front('customer-attraction/profit-bellman-unbounded-and-overlap-credit-obstructions','obstruction','障碍','最优剩余利润的局部系数与共享负载信用','proved-analytic-two-full-SPE-families; exact-template-only','精确算两个完整SPE族的背景最优利润，排除任意固定局部系数及只计共同负载的实例无关可加信用；保整体half余量与剩余信用义务。')+b2)

b4=r'''## 假设及真正结论

固定k≥1，m=k+1，单位客户全集恰为两两不交D及X_i,Y_i之并。有限共同目录含C_i=X_i、A_i=X_i∪Y_i、B_i⊆X_i∪Y_i∪D及D，也可含N的任意其他子集。给定一份**完整有序历史纯SPE**，实际路径C_1,…,C_k,D。

每个实际i前缀保留过去C_j。改A_i后的同一策略真实分支末位B_i，改B_i后的真实分支末位A_i；两枝中间所有主题均避开X_i∪Y_i∪D，彼此其他动作可不同。其他离轨历史不作额外限制。这是条件性架构，不是每个SPE必有的结构。

记x_i=|X_i|,y_i=|Y_i|,d=|D|,S=Σx_i,Y=Σy_i。则
\[
2(k+1)OPT_{k+1}\le(3k+2)W,\qquad W=S+d.
\]
W>0才取比值OPT/W≤(3k+2)/(2k+2)；零实例不除零。

## 三条真实比较与锐性

令v_i=|B_i∩(X_i∪Y_i)|/2+|B_i∩D|。在A_i分支末位的B_i，以及B_i分支早期偏离者本人，局部均只同A_i分摊，D部分独占，故完整收益同为v_i。旧C_j避开局部池、中间避开条件均承重；没有改写过去。

A_i分支末位可改D取得d，给v_i≥d；实际第i位可改B_i得v_i，给x_i≥v_i。实际末位D可改A_i得x_i/2+y_i，给d≥x_i/2+y_i。因此
\[
x_i\ge v_i\ge d\ge x_i/2+y_i,\quad S\ge kd,\quad Y\le kd-S/2.
\]
k个A_i加D恰k+1槽覆盖N，故OPT=S+Y+d≤S/2+(k+1)d。代入
\[
(3k+2)(S+d)-2(k+1)[S/2+(k+1)d]=(2k+1)(S-kd)\ge0
\]
即证。额外目录不改变全集上界与满覆盖见证。d=0时迫所有x_i=y_i=0。k1无需无固定点置换，界5/4。正等号强制每个x_i=d、y_i=d/2，因此单位客户d必须正偶数。既有全人数无拥挤族x_i=d=2,y_i=1实现；其**存在**和全历史Q/B递归来自[无拥挤族资源](../资源/无拥挤完整均衡族原稿与有限探索的准确范围--资源.md)，不能仅凭本页必要条件造完整策略或宣称该比率约束所有SPE。

## 撤销隔离后的可量化缺口

仍保同一无拥挤实际路径及全客户池，取消两枝中间避开。假设改A_i后的真实末位B_i；令v_i是该末位收益，b_i是实际i改B_i后的本人最终收益，d_i^Q是A_i枝末位改D的收益。定义
\[
\Delta_i=v_i-b_i,\quad T_i=d-d_i^Q,\quad E=\sum_i(\Delta_i+T_i).
\]
T_i≥0，Δ_i可负。由x_i≥b_i、v_i≥d_i^Q，得S≥kd−E。实际末位仍给Y≤kd−S/2，故同代数给
\[
2(k+1)OPT\le(3k+2)W+(2k+1)E.
\]
这是待支付缺额，未证由W统一控制。若真有OPT>2W，上界OPT≤S/2+(k+1)d先迫S<2(k−1)d/3，结合S≥kd−E得
\[
E>(k+2)d/3.
\]
必要但非充分；小局部不对称不足。多个后继拥挤B_i、跨组主题、A_i枝提前覆盖D都是可能逃逸机制，各须重新完整验证。

## 相同追随者方案的具体冲突

设局部核心a=|X_i|+|Y_i|>0，B_i=X_i∪Y_i∪Z，实际末端为r次同D=Z∪R；拟在A_i枝用r次B_i稀释。实际末位从D改B_i，公共Z份额相同，所以D最佳要求|R|/r≥|X_i|/2+|Y_i|≥a/2。拟惩罚分支末位B_i可改尚未覆盖R的D，其最佳要求a/(r+1)≥|R|。合并r(r+1)≤2；r≥2不可能，r1还迫Y_i为空。只算早期a/(r+1)会漏末位改D。拆Z或异质奖励须另证，不被这里概括排除。

## 原件与审查身份

实际全文读bdd683848aab07c77142、73e78b9e31ec4e9518da、4fa30e438229f7d5436d，精确原件在[related清单](../../../../tools/evidence/d22-frontier-ledger-primary/related-source-manifest.json)。原独审先盲重构再核对非均匀等号/零边界，这是内部解析审查历史，不新增当前外审。全部k量词由上面解析承担，0随机或枚举新run。下一对象必须保真实分支收益、D被预覆盖量及总E，而不是给必要条件点就称half反例。
'''
put(P4,front('customer-attraction/reciprocal-isolation-welfare-and-escape-budget','obstruction','障碍','双向隔离惩罚的福利上限与逃逸预算','proved-conditional-architecture-bound; escape-budget-unpaid','任意k双向真实隔离惩罚的锐上限、正整数等号和撤销隔离后的E必要阈值，含重复追随者末位冲突；不约束所有SPE。')+b4)

b3=r'''## 合法有序前缀与饱和端点

有限单位客户、共同有限非空目录、单位提供者、全部有序历史纯SPE。固定一个合法过去负载b，实际r+1人路径A B^r，r≥1。定义
\[
u_A=\sum_{x\in A}\frac1{b_x+1+r\mathbf1_B(x)},\quad
q(T)=\sum_{x\in T}\frac1{b_x+1+r\mathbf1_B(x)},\quad
\tau(E)=\sum_{x\in E}\frac1{(b_x+1)(b_x+2)},\ E\subseteq A\setminus B,
\quad M=u_A-q(B).
\]
q(T)是把当前A换T后**冻结**尾部B^r的查询，不是原策略hT后的真实收益。根改B后未来r人至多全覆盖每个B客户，故真实根B收益v_B≥q(B)，SPE给u_A≥v_B，因而M≥0。

**饱和定理。** 若精确M=0，则每个合法T均有q(T)≤u_A，强于[VA候选](../候选/单色真实后缀的虚拟相邻税--候选.md)的q(T)≤u_A+τ(A\B)。

证明：q(B)≤v_B≤u_A=q(B)且每个B客户的单项下界均正、差非负，故每个B客户在真实改B枝都被全部r个未来主题Y_i覆盖，即B⊆Y_i。原实际末位B可改合法Y_i；公共B收益抵消，若Y_i有B外客户必带严格正收益，矛盾。因此每个Y_i与B覆盖相同。改B枝末节点已有r份B覆盖、末位也B，其任一T偏离收益正q(T)，BR给q(T)≤q(B)=u_A。空B时同样：原末位空收益0已迫全部合法主题覆盖为空；零客户乘法结论成立。用的是同一策略真实两个末节点，无需连续性或唯一标签。

饱和必须是等式，M>0哪怕很小也未由这段刚性证明控制，不能直接推广稳定估计。

## 空背景福利推论及已知范围去重

m≥2、空根实际A B^(m−1)，若u_A=|B|/m，则上节给每个T
\[
|T\setminus B|+|T\cap B|/m\le |B|/m.
\]
把m个最优主题相加，O为其并，则|O\B|+|O∩B|/m≤|B|，所以
\[
OPT_m\le |B|+(1-1/m)|O\cap B|\le(2-1/m)|B|\le(2-1/m)W.
\]
重复/未覆盖客户均只使求和上界松弛。此为饱和查询推论，不宣称新增已知半界人数或结构：既有两覆盖充分筛选l(2k+1)≥k²−1在k=1已成立，故AB^(m−1)整体half已有覆盖；这里更强查询结论和相对|B|的系数另有用途。

## M>0的精确剩余税

原实际末位B对任意T的BR，消去交集得
\[
\sum_{T\setminus B}\frac1{b_x+1+\mathbf1_A(x)}
\le\sum_{B\setminus T}\frac1{b_x+r+\mathbf1_A(x)}.
\]
对q(T)−q(B)逐客户减去此式，A外B外分母相同；A∩T\B引入一次税；B内A外且不在T产生另一税；其余为非正。因此
\[
q(T)-u_A\le\tau((A\cap T)\setminus B)
+\sum_{B\setminus(A\cup T)}\frac1{(b_x+r)(b_x+r+1)}-M.\tag{RES}
\]
于是VA的充分支付义务恰可写
\[
\sum_{B\setminus(A\cup T)}\frac1{(b_x+r)(b_x+r+1)}
\le M+\tau(A\setminus(B\cup T)).
\]
尚未从一般真实SPE证明；正税来自B内、A与查询外客户，需真实根B分支外部性支付。不能把充分条件的未证当VA失败。

所有相关客户背景同一d≥0，令a=|A\B|,a_T=|(A\B)∩T|,b_T=|(B\A)∩T|。M=a/(d+1)−|B\A|/(d+r+1)，将其代入RES得
\[
q(T)-u_A\le\frac{a_T}{(d+1)(d+2)}+\frac a{(d+1)(d+r)}
-\left(1+\frac1{d+r}\right)M-\frac{b_T}{(d+r)(d+r+1)}.
\]
若VA对T失败，必有
\[
a_T>\left(1-\frac{d+2}{d+r}\right)a
+(d+1)(d+2)\left(1+\frac1{d+r}\right)M
+\frac{(d+1)(d+2)b_T}{(d+r)(d+r+1)}.
\]
特别d0,r≥2，失败查询须含超过1−2/r比例A\B；若T与A\B不交，此式已排失败。这是查询定位，非整个VA定理。

## 静态弱支配与动态势的差别

固定背景d_x≥0，若r名同时静态玩家全B为PNE，则每个C满足
\[
\sum_{C\setminus B}\frac1{d_x+1}\le\sum_{B\setminus C}\frac1{d_x+r}.
\]
对任意r−1个固定对手Y，U(B;Y)−U(C;Y)≥Σ_(B\C)1/(d+r)−Σ_(C\B)1/(d+1)≥0。因此B在同背景静态博弈弱占优。任意真实前缀P的第i活跃玩家改B，仍有合法最坏收益保底Σ_B1/(d_x+c_P(x)+1+r−i)。这不说偏离后未来不变，也不说完整SPE动态共同最大化调和势。

五客户完整反例：X,Y互不交各2人，另z1人；B=X∪Y,C=Y∪{z},D=X，两人。B²静态PNE且弱占优。末位在首B,C,D后分别B,B,C，根D。末位(B,C,D)收益行分别(2,2,1)、(3,3/2,2)、(3,3,1)；根三个真实收益皆2，故全7? 此处恰1+3=4个决策节点，含自身12比较，全树SPE由表直接可见，不称七节点。实际D,C福利5调和势5，B²福利4势6。故静态弱占优不强迫任一SPE共同势最优；不是half或VA反例。

## 必要条件点不能冒完整策略

零背景r2，兴趣类型{T,Y1}:1、{B,Y2}:2、{B,Y1}:1、{A,T,Y2}:1，共5客户；指定actualA,B,B与离轨T,Y1,Y2。u_A=1,τ_A=1/2,q(T)=2，离轨rootT收益1、Y1收益3/2、Y2收益5/2。实际末位BR、root所有无条件安全保底、指定T枝各前缀安全保底均可成立，仍有VA缺口−1/2。但根改B后的**所有真两人SPE**使根≥3/2>1，故不可能补成指定actual的完整SPE。原稿给这一完整可实现性排除；本批不冒已运行BI，保存为作者诊断，当前无新增代码核验。

具体互补块尝试A=Z,B=X∪Y,T=Z∪V,Y1=X∪V,Y2=Y∪Z，大小x,y,z,v。原B²末位至少要求v≤y/2,z≤x,2v+z≤x+y。T枝Y1为避免被改B且末位仍B击败，须v+x≥y。若根B枝以B,Y2压低root，root收益x/2+y/3，第二人可抢Y1得v+x/2，故须v≤y/3；最紧x=y−v时，VA违反加root保底又须v>y/3，冲突。仅排这套分支设计，未穷尽参数/额外目录，不包装一般VA2证明。

## 来源与状态

本页主解析实读related86390a643a36ea35f311全文，原“root独立重算”保其当时身份；与已完成VA3843B原稿及其[现页](../候选/单色真实后缀的虚拟相邻税--候选.md)完整比较。RES与M0可用于接续，未付M>0和真正多后继信用仍开放。原必要松弛程序和冻结报告本批未读/未运行，0新SPE/LP测试，不把作者数值认证为当前run；无外审或新颖性。
'''
b3=b3.replace('故全7? 此处恰','故此处恰')
put(P3,front('customer-attraction/monochromatic-saturated-query-and-residual-tax','lemma','引理','单色真实后缀的饱和查询与剩余税','M0-query-theorem-proved; positive-M-tax-open; static-dynamic-separated','全背景实际AB^r的精确饱和强查询端点及福利推论，定位M>0正税；保静态支配动态反例与必要松弛非SPE边界。')+b3)
b1=r'''## 四份入口的时间层与数学对象

四主源CLAIMS14468B、FAILED_ROUTES5462B、README11939B、RESEARCH_STATE4092B，共35961B/319行均实际全文实读。CLAIMS是主Q加**10项**辅助合同，共11二级节；失败稿是6机制。不是11项辅助或7失败机制。原Boss10角色、六指定研究员、恢复clone/公屏107核同证书、一般机制/停止调参数指令只保历史身份，不换当前Boss4或发研究任务。

模型始终为有限单位客户、有限共同非空目录、单位顺序提供者、每个合法有序历史规定动作的完整纯SPE，容许空主题、重复、同覆盖标签、零客户及离轨任意平局。原任意人数Q未解不表示每个人数仍未解：现有五人half定理，六人half仍目标。没有从以下辅助障碍造half反例。

README开头2026-10-25已明确逐位置FM/Mfull≤u被**零根银行族**反驳，正文旧表、CLAIMS和STATE仍保OPEN。它们是同一冻结文件中的不同时间层，应校正当前真值而不改原件。其“未提升canonical/个人资产”也是历史；下列已有正式对象不继续沿用未归档断言。

## 十项辅助合同逐项归位

| 原ID后缀 | 全量词、结论与实际去向 |
| --- | --- |
| UNIQUE-OPTIMUM-OMISSION-OBSTRUCTION-v1 | 存在m2、6不同主题、71客户完整7节点SPE，W35、唯一无序最优TQ覆盖38、交集2、遗漏36>W。允许重复组合，唯一性不排有序排列。原14客户类型/42含自身比较/21无序对的完整证书已归[唯一遗漏反例](../反例/唯一最优组合的全遗漏支付--反例.md)。B_D(16)=4>19−16=3否定相应价格差预算；净OPT−W=3与half余量32保留，不能推广为所有价格/聚合失败。 |
| TWO-PLAYER-INTEGER-PUSH-SHARP-v1 | 所有合法背景、恰两剩余、任意p和每首主题真实末位BRρ，B~p,R=ρ(B)，独立A~p。D为原B本人真实收益均值，C为完整两槽后额外A查询。D−C≥Σ_x p_x²/[(b_x+2)(b_x+3)]≥0，仅末位BR足够，不需首人最优。实b≥0仅代数扩展；单客户{空,{x}}末位总{x}取等。[锐曲率与双分支证明](../引理/末位真实回复推送的锐曲率与双分支式--引理.md)。 |
| THREE-PLAYER-INTEGER-PUSH-AVERAGE-NO-v1 | 34客户7主题含空，3人完整57节点，p(X2)=1/10,p空=9/10；D29/30<C41/40，差−7/120。原u29/3,u−C1037/120>0,W32OPT34；只否强D≥C，不由该例否弱C≤u。[空根稀释完整证书](../反例/空根稀释的强推送失败与弱桥范围--反例.md)保399含自身/342真正偏离的旧成功证据。 |
| RECIPROCAL-ISOLATION-SHARP-v1 | 对所有k≥1，但仅指定双向真实隔离分支的完整SPE，2(k+1)OPT≤(3k+2)W，k1/零/正偶d等号以及撤隔离E阈值，完整推导见[隔离障碍](../障碍/双向隔离惩罚的福利上限与逃逸预算--障碍.md)。非一般SPE架构定理。 |
| PURE-FULL-ROOT-MENU-NO-v1 | 存在m8、8主题、32客户完整DAG，u13/4，每个强制root真8槽列有额外查询37/10；W=OPT32，同菜单mixed精确851/280<u。原MD已报告完整DAG，不沿用较早稿“仍核验”的现在断言；本批未读原DAG/代码/report，不冒当前机器认证，具体合同见下文。 |
| MIXED-FULL-ROOT-MENU-v1 | 原全称：每个合法b、余r≥1及每份完整SPE，存在不观察独立查询的列分布Q，使max_T E_Q Σ_T1/(b+c_Z+1)≤u；Z含原root共r槽，u为所有真根收益最大。r≤2解析仍真；一般全称现在**假**，银行零根m≥4已反驳，不再OPEN。保条件minimax/half归约但不将充分假设当真。 |
| PROFIT-BELLMAN-LOCAL-NO-v1 | 原交叠完整SPE族n≥4，精确Ftail=2(n−1)(n−2)+(7n−13)/6；2u+Ftail−OPT=(23−5n)/6−2/n，n≥5负；α<17/6最终失败。F为剩余利润不是总覆盖。完整消元、n4边界、尾信用见[利润障碍](../障碍/最优剩余利润的局部系数与共享负载信用--障碍.md)。 |
| PROFIT-BELLMAN-ANY-FIXED-NO-v1 | 对每个有限实α存在全A完整SPE的n，u1，根F台阶h_n−1≥2√n−1>α；h_n=min整数j(j+n/j)，Ftail2n−h_n。WnOPT2n−1，half余量1。已知族的新利润分析，非新底层游戏；同上自足证明。 |
| MONOCHROME-SATURATED-QUERY-v1 | 所有合法b/r≥1/完整SPE实际AB^r，若精确u_A=q(B)，则每个合法T有q(T)≤u_A，含空B/零客户。空根饱和时OPT_m≤(2−1/m)|B|，不称新增已知half范围。[饱和查询与剩余税](../引理/单色真实后缀的饱和查询与剩余税--引理.md)保全证明及M>0未付范围。 |
| OVERLAP-ONLY-ADDITIVE-CREDIT-NO-v1 | 不存在实例无关f_r(b,c)，f(0,c)=f(b,0)=0，使C=Σf同时对所有完整SPE满足F≤2P+C与Δ+C_child−C≤2u。两完整族同r=n−1对同f(1,r)在n≥16冲突，函数可负/依r，禁其他实例信息。只否该模板，[两族上下界证明](../障碍/最优剩余利润的局部系数与共享负载信用--障碍.md)，不否独占项/主题信息/非可加状态。 |

## 当前菜单真值、弱推送与静态门槛

令Z(B)是强制rootB后同一完整策略的r槽终局，d_B=Σ_B1/(b+c_Z)，u=max_B d_B；核K_AB=Σ_A1/(b+c_Z(B)+1)。原root仍在列，查询是额外一位，不得混淆两个分母。C(p)=pᵀKp，D(p)=Σp_Bd_B；强D≥C已经三人失败。弱∀p C(p)≤u若真，可取K的对称meta-NE p（有限博弈存在）使所有行Kp≤C(p)≤u，从而FM；又FM列可作为自由r槽竞争背景，u≥真实整数v_(r+1)(b)。对合法前缀，静态OPT_m≤2m v_(r+1)(b)给逐人及half条件归约。定义与全部正性/独立性见[静态额外槽预算](../引理/合法前缀的静态额外槽预算与条件归约--引理.md)和[完整菜单旧接口](../资料/完整真实菜单的条件对偶与旧实例账本--资料.md)。没有将数学存在Nash转成已交付算法。

当前[银行完整根列](../反例/银行完整根列的两查询最小分离--反例.md)的真正零根完整控制器在每个m≥2给u=1+1/(m−1)、W2m、OPT3m−2。对m≥4，两个合法query分布p2已使**每个真列**平均至少c2=4/3+1/(2m)>u；其支持两列也取等，所以C(p2)=c2>u，弱WP与FM都真失败。全菜单精确值2−1/m−1/[3(m−1)]也>u。m4为u4/3、c2 35/24、Mfull59/36；不混同自由分数值t5=19/14≤真正整数v5。后者也>4/3，由Jensen t≤v即可更新旧整数逐人OPEN。m2此异银行二query未定义，m3无严格缺口。

[银行逐人族](../反例/笛卡尔银行目录的逐人分数门槛反族--反例.md)的u≥OPT/(2m)在m≥5失败，故STATE旧OPT−W≤m u_i一般候选也不能据旧OPEN当当前真；若需这个**不同**机会缺口的真值，必须逐源查其实际反例，不能单凭更弱逐人下界失败推出OPT−W≤m u_i失败。本资源不作该逻辑跳跃。B(u_i)≤W、B(W/m)≤W、真aggregate各有独立定义/证据，不能由遗漏、FM或个体门槛失败一锅否定。银行本族仍2W−OPT=m+2>0，且W≥m v_m。

## 八人纯菜单：输入、完整DAG合同与混合匹配

完整读related66007ee43711768dbc97的9014B数学。两不交16客户块j0/1，各四主题A,B,C,D，类型{A}:2,{B,D}:4,{A,C}:6,{C,D}:3,{A,B,C,D}:1。计数q0=(2,1,1,0),qA=(2,0,1,1),qB=(1,1,1,1),qC=(1,0,2,1),qD=(1,0,1,2)。root选T_j的真目标应为本块qT、另一块q0，root收益(A,B,C,D)=(13/4,9/4,13/4,13/4)，actualD0。

原MD给schema CA_COMPLETE_SPE_DAG_v1：每节点counts/target/action/每合法动作children。边counts只加对应e_a、深度增一；规定action子节点target同父；叶depth8、counts=target；所有非终端对全部8动作须验U_a(target)≥U_b(child_b.target)。由叶向根归纳每子博弈SPE；按任意有序历史沿边行走，使共享DAG节点不删历史量词。原MD报告13872节点、6435叶、(13872−6435)×8=59496含自身比较和最小松弛0；原报告覆盖决策历史Σ_(i=0)^7 8^i=2396745。这两项算术在此展示，不冒当前实际读遍DAG或运行核验。原代码/JSON/独立重造DAG均未在GS取得/全文读；**作者报告的有限认证**与本批已解析读懂的证明合同区分。

每列的另一块q0被额外D查询取得4/2+3/2+1/5=37/10>13/4，纯列阻断失败。原报告actual路径(D0,A0,C0,D0,A1,A1,B1,C1)，逐人(13/4,21/4,17/4,13/4,13/4,13/4,17/4,21/4)，总32；四主题A_j,D_j已满覆盖、重复补8槽，故W=OPT32。

这里单块额外查询完整矩阵L及根在别块的查询h为

| query | 本块A列 | B列 | C列 | D列 | h(别块q0) |
| --- | ---: | ---: | ---: | ---: | ---: |
| A |71/30|16/5|27/10|16/5|71/30|
| B |11/5|23/15|11/5|23/15|11/5|
| C |27/10|16/5|49/20|59/20|16/5|
| D |16/5|38/15|59/20|137/60|37/10|

均匀两D列Q给query向量(167/60,28/15,123/40,359/120)两份，最大123/40<u。均匀D也作独立query时C=359/120，不是rootD收益13/4。同块额外D为137/60，旧弱阳性因遗漏+1撤销，不可复活。

更优Q每块C1/14,D3/7，queryp每块C2/7,D3/14，其余0。按上表有KQ=(577/210,67/35,851/280,851/280)两份，pᵀK=(443/140,443/140,851/280,851/280)两份。前者最大与后者最小同851/280，原始/对偶匹配给本菜单混合值精确851/280，u差59/280。不依赖浮点最优状态；本批解析核公式，不造原报告run。

较早[根菜单联合势](../资料/完整根菜单的联合势义务与排序边界--资料.md)保当时八人DAG仍待验的事实；GS不覆写其历史。新9014B已报告完成则保新时点，既不因早期缺材料否认后续报告，也不由后续一句认证当前未读完整报告。

## 条件n块矩阵与真实可实现性的分界

完整读related be35ac9e54f0b79a4117、fb08b92429fc3b32a751、729c23b4e89e761e0043。n块、4n人、4n主题、16n客户，条件菜单R_n为根T_j后本块qT，余n−1块q0；必须由同一完整SPE同时实现，n2的证书不是一般直和。

K[S_i,T_j]=L[S,T]若同块，异块为h[S]。n≥3令Q均匀各D列，四query期望为71/30+5/(6n)、11/5−2/(3n)、16/5−1/(4n)、M_n=37/10−17/(12n)。D项分别比C/A/B大1/2−7/(6n)、4/3−9/(4n)、3/2−3/(4n)，均非负。再取独立queryp均匀D，对任列T_j有pᵀK≥M_n，因D行本块最小137/60。上下匹配得**条件矩阵**精确minimax M_n。

n3为581/180<u13/4；n4为803/240，gap23/240>0，是本菜单族首个静态严格失败，n1纯A cap16/5<u、n2值851/280。若R4实现，它会反FM/弱WP却仍W=OPT64；自由静态每块qB可把所有查询压到16/5<u，所以真实菜单内与自由背景严格不同。这里不提供R4完整SPE。

原C++集合BI报告n3共有2704156计数状态、1352078叶、3207136保留outcomes，root门槛13/4、200root终局。四根A/B/C/D的指定目标均不可实现，last-low截面192/384/192/192，全部门槛最小37/10。**这全部截面结论仅一C++实现，GS未读源码/报告或新运行**；不称全部截面已独立审完。有限n1/2/3可选root终局为单块6集合Q的n次积中至多一个q0，数量6/35/200=5^n+n5^(n−1)。任意n延伸仍猜想。

解析last-low引理自足：目标终局z，低收益支持L={a:z_a>0,U_a(z)≤u}，R(p)是给定前缀后的全部真SPE终局，F(p)=max_b min_(q∈R(p+e_b))U_b(q)。若每个p≤z且尚余恰一个L行动的相容非终端截面都有F(p)>u，则z不能实现：取真实路径最后L行动，其本人最终≤u却可保证F(p)>u，矛盾。集合BI可用R(p)=∪_a{q∈R(p+e_a):U_a(q)≥F(p)}，因每个不同有序子历史可独立选最坏续局，计数缓存的是所有可选终局而非强制历史共用选择器。引理不自动给任意n门槛。

独立解析只核一个合法余3人代表p=(1,0,1,1)|(2,1,0,0)|(2,1,0,0)。若此刻规定D0，其最终13/4；当前可改D1。改后各块(A,B,C,D)即时插入表分别(13/4,9/4,13/4,13/4)、(43/15,23/15,37/10,91/30)、(35/12,9/4,21/4,21/4)。余两人首选C1可保证37/10，末位严格C2或D2；首选其他非C1/C2/D2即时≤13/4，不能最优。首C2的末BR恰C1/D2，首D2恰C1/C2。因此两人SPE新增多重集只可能{C1,C2},{C1,D2},{C2,D2}，当前D1最终前两种37/10、第三21/4，保证严格高于13/4。它排**当前D0**，不排先C1/C2的其他排序，不能替代全部截面证明。

原三块替代诊断只固定p均匀D,u13/4；真实子局终局中筛根自身≤u，各A/B/C/D剩60/39/35/35个，最大p查询101/30、283/90、197/60、551/180，B/D不足。最优展示qT|qE|q0，qE=(1,1,2,0)，其D额外16/5，比q0少1/2。以上最优/可实现性为原单实现报告，本批仅读解析展示与数字；不声称穷尽所有p，更不由诊断失败证FM。

## 6286客户完整槽平稳核：指定选择失败

独立审查related d51be5e16b588a9c5b11全文4495B给三人、六主题0…5，共6286单位客户；全部兴趣mask/重数如下：

|mask|重数|mask|重数|mask|重数|
|---:|---:|---:|---:|---:|---:|
|1|361|2|770|4|550|
|9|587|10|185|12|229|
|13|99|16|1078|26|33|
|29|396|33|360|34|72|
|35|99|36|380|42|369|
|43|132|44|237|46|132|
|48|19|49|99|50|99|

完整策略规则：根0；第二位在root0/1/2后3，否则0；末位在第二行动所属三主题组{0,1,2}或{3,4,5}中取未出现最小编号。43有序节点已由规则定义；原独审报告258含自身/215真偏离全非负，GS未取得原43动作JSON/程序/report，不冒当前重算。这不同于DY的1274客户**真实尾槽**平稳例。

强制根菜单三槽分别(0,3,4),(1,3,4),(2,3,4),(3,0,1),(4,0,1),(5,0,1)。root收益d=(2821/2五次,2557/2)，u2821/2。source→均匀**完整3槽**核P_BA=count_A(Z(B))/3，原独审有理秩rank(Pᵀ−I)=5给唯一平稳p=(1,1,0,1,1,0)/4。原额外矩阵Kp=(23615/24,45415/48,5765/4,49835/48,14435/16,4735/4)，transient query2超u123/4。

但C(p,p)=185785/192<D(p)=2821/2，差85031/192>0；p非内生K对称NE，平稳不代meta最佳回复。预算Ubar9149/6,T98063/144,Γ71303/576满足C=Ubar−T+Γ；D−Ubar=−343/3<0，不给角色可交换。各纯列cap=(1361,2777/2,2777/2,1372,3287/2,1379)，0/1/2/3/5列均安全；仅纯0已得Mfull≤1361<u，余99/2，无需计算精确minimax。W4514OPT3=5189,half余3839为原216三元组枚举报告。

故只否定“任取source→完整槽平稳分布必逐查询安全”，不反stationary self强推送、自由mixed、真安全聚合或half。唯一性/全部IC/OPT的机器证据本批只读审查报告**文字**，未读其引用原JSON/code，不把本页数字当新run结果。

## 六种失败、可回收机制及真实下一义务

1. 选择最优组合最大交集仍遗漏36>35，须支付双向交换/完整OPT−W；原R171相同证书仅独立重现不新颖。
2. 两人锐D≥C不能直接推广多后继；需根u−D或另选静态背景。旧两块分母纠错不复活。
3. 24客户等势、791严格降势、348二环排势排序/无环，纯8人菜单排纯列；这些具体例不自己反mixed。原791报告未取得保持旧边界，不复跑旧348成功。
4. 利润Bellman系数2/α<17/6失败，但真实tail信用支付局部债，非F≤2P或half失败。
5. all-big使所有有限α失败，不能只继续调大常数；需跨深度状态。
6. 只计共同覆盖的实例无关可加信用又被两族冲突排除；须真正区分独占/目录/分支信息。放宽模板本身仍非证明。

通用充分minimax归约、联合势遗憾身份、两剩余最大裸回复纯列、VA1、M0端点、last-low截断、隔离E与精确F消元均有独立接续价值。当前缺口是非循环信用/真实分支替代支付，不把旧管理“六路研究/停止小扫描”执行为本轮指令，不给phase3图造边。

## 读取与计算的责任边界

[四原件](../../../../tools/evidence/d22-frontier-ledger-primary/original-source-manifest.json)与[14必要数学原稿](../../../../tools/evidence/d22-frontier-ledger-primary/related-source-manifest.json)完整字节冻结；原解析证明全部已读。已归档对象按同SHA旧全文阅读诚实复用，交叠族完整SPE和VA当前页本批再逐段核；[读取范围](../../../../tools/evidence/d22-frontier-ledger-primary/read-scope-and-evidence-status.json)列具体身份。GS新增原CLI/SPE/LP/枚举/随机/旧成功重跑均0。作者计数/独立历史、解析普遍量词、未取得代码报告互不替代。没有外审或全球新颖性、实现算法时间界或当前未交付canonical认证。
'''
put(P1,front('customer-attraction/true-branch-ten-contracts-and-menu-realizability-ledger','resource','资源','真实分支十项合同与菜单可实现性账本','all-four-entry-sources-reviewed; historical-open-corrected; author-computation-scope-retained','保D22主Q及10辅助合同、6失败机制、八人DAG报告、条件多块矩阵与单实现/局部独审分界、6286完整槽平稳例，纠正当前FM真值但不冒未读程序认证。')+b1)
extra=rawman(C/'learning-gs-omission-input-comparison/local-export-manifest.json','related-supplement');related+=extra;js(E/'related-source-manifest.json',related)
addition=r'''## “同一71客户证书”的输入与平局版本边界

为核原README的来源断言，GS另实际全文读D22遗漏正文aa188e3cd37022c8cb39（5359B），并逐项对照当前[两份输入等价](../等价/两份最优遗漏输入的二人收益等价--等价.md)。D22的14类型为A9,B9,T13,Q8,AR1,BR4,QR5,AS1,BS4,QS5,ARS5,TRS5,BTRS1,BQRS1，恰与现等价页发现JSON那一列相同。D22完整回复按首A/B/T/Q/R/S为(B,R,R,R,S,R)；现12类参数证明族k3的回复是(B,S,R,S,S,R)。B/Q分支R或S均合法最佳平局，根六种真实收益仍16，但**选择器并不逐字相同**。

两表主题大小(16,19,19,19,22,22)及全部两两交集相同，二人收益|X|−|X∩Y|/2、两主题并集都由这些数决定，故该二人反例接口等价。D22 14类B∩R∩S为2，12类为6；固定三人(B,R,S)的B收益分别41/3和15，不能推广为高阶客户表/所有人数完全同一。原“独立重现/同证书”只在此精确数学对象意义保存，不冒输入SHA、客户incidence或策略字节完全相同，也不重复增加原游戏新颖性。

D22保护价格完整证明亦已实读：遗漏D中各主题大小(0,0,18,18,10,10)，总权τ的截断覆盖≤min(18τ,36)，所以B_D(16)≤max_τ[min(18τ,36)−16τ]=4；T,Q各权1达到4>3。不是只引用旧PASS状态。

'''
b1=b1.replace('## 当前菜单真值、弱推送与静态门槛\n',addition+'## 当前菜单真值、弱推送与静态门槛\n')
b1=b1.replace('[14必要数学原稿]','[15必要数学原稿]')
put(P1,front('customer-attraction/true-branch-ten-contracts-and-menu-realizability-ledger','resource','资源','真实分支十项合同与菜单可实现性账本','all-four-entry-sources-reviewed; historical-open-corrected; author-computation-scope-retained','保D22主Q及10辅助合同、6失败机制、八人DAG报告、条件多块矩阵与单实现/局部独审分界、6286完整槽平稳例，纠正当前FM真值但不冒未读程序认证。')+b1)

contexts=[];external_links=set()
for p in PS:
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',(S/p).read_text()):
  if '://' in dest or dest.startswith('#'):continue
  n=posixpath.normpath(str(Path(p).parent/dest.split('#',1)[0]));q=REPO/n
  if not (S/n).exists() and q.exists() and n.startswith('archives/'):external_links.add(n)
newfull={'任意人数首步补全余额--反例.md','单色真实后缀的虚拟相邻税--候选.md','唯一最优组合的全遗漏支付--反例.md','两份最优遗漏输入的二人收益等价--等价.md'}
for n in sorted(external_links):
 b=(REPO/n).read_bytes();matches=[]
 for q in list(C.glob('r3-*/'+n))+list(C.glob('r3-*/tools/evidence/*/context/'+n)):
  if q.is_file() and q.read_bytes()==b and S not in q.parents:matches.append(str(q))
 mode='GS entire actual current formal text read, no unread tail' if Path(n).name in newfull else 'prior fully read original-derived formal honestly reused after actual identical byte check'
 assert Path(n).name in newfull or matches, n
 q=E/'context'/n;cp(REPO/n,q);contexts.append({'path':n,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_mode':mode,'actual_samebyte_prior_snapshots':matches,'publication':'actual working-copy bytes only; no new source claim or assumption of unrelated body push'})
js(E/'context-manifest.json',contexts)
# Read the R275 alternate claims ledger was GS context, no extra primary/done.
p='archives/customer-attraction/state/资源/跨分支付款命题账本的精确对象与约束层次--资源.md'
if (REPO/p).exists():
 b=(REPO/p).read_bytes();q=E/'context'/p;cp(REPO/p,q);contexts.append({'path':p,'snapshot':str(q),'bytes':len(b),'sha256':sha(b),'read_mode':'GS entire actual alternate-workspace ledger full mathematical reading; no B10 round5 profit/M0 proof inferred from shared ledger title'});js(E/'context-manifest.json',contexts)

claimpath=R/'boss4-r3-next-gs-claim.json';claim=json.loads(claimpath.read_text());assert claim['status']=='pushed' and claim['actor']=='Boss4' and claim['local_sync']['status']=='synced' and set(IDS)<=set(claim['ids']);owners=[]
for i in IDS:
 x=json.loads((REPO/'cleanup/progress'/f'{i}.json').read_text());v=inv[i];assert x['owner']=='Boss4' and x['disposition']=='in-progress' and x['source_sha256']==v['sha256'];owners.append(x)
cp(claimpath,E/'actual-unprojected-claim-receipt.json');js(E/'actual-primary-ownership-snapshot.json',owners)
cp(C/'local_blob_export.py',E/'authorized-local-export-helper.py.txt')
js(E/'formal-resource-manifest.json',[{'path':p,'bytes':(S/p).stat().st_size,'sha256':sha((S/p).read_bytes())} for p in PS])
scope={'primary_sources':4,'primary_bytes':sum(x['size'] for x in primary),'primary_lines':sum(x['lines'] for x in primary),'primary_read':'every actual byte/section/claim definition/domain/quantifier/update/evidence/failure mechanism and numerical contract read; first read before writer, explicit final source comparison in GS; not counts standing in for semantic reading','claims_sections':{'main_question':1,'auxiliary_contracts':10,'total_secondary_sections':11},'failed_routes_sections':6,'related_full_mathematical_sources':len(related),'related_bytes':sum(x['size'] for x in related),'related_primary_done':0,'related_full_read':'all15 MD files read in full, including later supplementary5359omission source; no unread tail','context_count':len(contexts),'context_read':'four actual full current source-independent math pages plus alternateR275ledger fully read GS; remaining prior fully read mathematical outputs reused only after actual whole-byte equality','new_original_CLI_calls':0,'new_math_program_runs':0,'old_success_replays':0,'new_SPE_or_LP_or_BI_audits':0,'new_numerical_or_random_checks':0,'helper_calls':2,'local_blob_attempts':15,'local_exports':15,'local_missing':0,'source_raw_program_or_report_materialization':'none in GS; referenced DAG/strategies/code/rawJSON not newly acquired/read, not asserted missing or codeSHA-matched; only full mathematical MD and current canonical evidence objects read','historical_report_claims_not_newruns':['13872DAGnodes/6435leaves/59496comparisons/2396745orderedhistories','15501n4to8countcandidates and allbig n2to8','threeblock2704156states/1352078leaves/3207136outcomes/alllastlowcuts from oneC++ implementation','6286client43nodes/258comparisons/rank5/216terminaltuples'],'raw_claim_ids':len(claim['ids']),'primary_claim_intersection':IDS,'claim_projection_performed':False,'new_formal_objects':4,'derived_builder_calls':1,'new_full_book_or_external_paper_read_claim':False,'network_or_lazy_fetch':0,'shared_Git_writes':0,'clean_show_claim_done_checkpoint_calls':0,'real_board_account_or_auth_operations':0,'phase3_graph_or_mapper_operations':0,'evidence_distinctions':['10auxiliary plusmainQ and6failedroutes actual counts','originalD2214types/ties differsfrom canonical12types/selector though exacttwo-player-equivalence','FM oldOPEN now false by actualzero-root bank; conditionalduality preserved','eightplayer later completedDAG report does not rewrite earlier unavailablehistorical page nor certifyunreadrawreport','conditionalreplicatedmatrix notSPE and allcuts singleimplementation versus oneindependentlocal witness','6286fullslotP differsfrom1274tailstationary example; transient queryfailure notselfpush orfreeFM','profitFnotcoveragecompletion; twoexplicitSPEfamilies/nohalf failure','credittemplate instanceindependence and bothzeroaxes vanish conditions essential','M0rigidity notpositiveMstability; positiveRES tax unpaid','isolation applies onlyprescribed two realbranches; Enecessarynot sufficient']}
assert scope['primary_bytes']==35961 and scope['primary_lines']==319 and len(related)==15;js(E/'read-scope-and-evidence-status.json',scope)
coverage=[
{'id':IDS[0],'units':['mainQ original/allhistoricalgeneralmodel and currentfive/sixseparation','all10aux IDs exactquantifier definitions assumptions dependencies evidence counterevidence scope/status relatedfiles','allfinite counts/dimension sources ratherthan recreatedprogram certification','FM crossfiletime-layer oldOPEN correction withoutfrozenrewrite','twoBellman exactF differentfromcoverage andunboundedfixedalpha plusoverlapcreditn16','M0allbackground/empty boundary andisolationk1/d0/equality'],'targets':PS},
{'id':IDS[1],'units':['all6attempts/criticalmechanisms/exactfailure/excludedrange/reusableproof/retryobligations','uniqueomissionvsnetgap and price4vs3','strongr3notweak andtwo-block137/60not13/4 correction','24equal/791down/348cycle/puremenu8 outcomes notmixed failure','Bellman2 thenalpha<17/6thenanyfinitealpha noadjustconstant','overlapcredittwofamilies instancelesszeroaxes contract notallcredit'],'targets':[P1,P2,P4]},
{'id':IDS[2],'units':['2026-10-25actualzero-rootFMcorrection vsoldbodyOPEN','historicalrecoveredclone/roles/publicscreen/sixagents instructionsnotexecuted','allfiletable maths assetroles/readtiming andclaimaudit independence historical','source107samecertificate precise14types and differentties vs12formal family','allfinite numericalcontracts omission/sharp/strong/isolation/menu/mixed/VA','conditionalreplicatednminimax andlastlow singleimplementation/localreview','17/6strongerunbounded andexacttailcredit','6286fullslotstationarynot1274tail','M0andM>0VAterms andnewnoncircularcredit duties'],'targets':PS},
{'id':IDS[3],'units':['oldgeneralOPEN versusactualfiveproof/sixquestion','allnamed opportunitygap/price/aggregatecandidates retainseparatecontracts','two-copywrongdenominator correction','historicalAGENTSactivecoordination instructionsnotoverridecurrentcleaner','fullrslotmenucolumn includesroot/queries independent/currentfalse update','24/791/348/8menu bookkeeping exactoldsource evidence','profitlocal thenanyconstant thenoverlapf successiveupdates','threeblocksingleBI versuslocalindependentwitness andfixedstationaryroute limit','M0query true/M>0unpaid/noncirculartailcredit F-2Pnotproof'],'targets':PS}]
js(E/'semantic-coverage-map.json',coverage)
notes=[
('14468B/116行全文实读主Q及10辅助合同（共11二级节），逐一保域/量词/定义/依赖/证据/异议/状态/去向；不以标题或合同数量替代阅读。','读15必要数学原稿与现行对象，核两无限族利润F消元/完整SPE、M0和隔离真实分支；FM旧OPEN用真正银行零根反例更新。八人完整DAG后时点报告保身份，但未读rawcode/report不冒认证。','integrated为四自足对象；当前正式存在性/反例/模板/条件/未付税分开，旧个人canonical状态不抄；不把局部负债或纯菜单/定核失败当half失败。'),
('5462B/47行六个失败机制全部实读，含尝试、承重机制、精确失败、排除范围、回收与重新研究条件。','比较三人强桥与弱桥、两块额外+1分母、纯/混合、覆盖补全/剩余利润、17/6/无界及共享负载模板；保原791报告未读和原348旧成功不重跑。','六机制按实际范围归位，失败只排写定合同；不执行原“停止参数”历史命令，不以原OPEN否认后续银行反例，0新程序运行。'),
('11939B/106行全部段落/表格/最后信用段全文实读，顶端2026-10-25纠错和旧主体同存，全部资源用途/读取时机/恢复与来源声明保全。','安全本地补读5359B D22遗漏正文并对照现12类proof/14类发现等价表，确认14客户类型恰同发现列但B/Q的R/S回复不同；不是相同字节输入或selector。还完整读条件块矩阵、lastlow和6286独审全文，分单实现与局部独核。','保有用数学和当前真正缺口；完整DAG原作者报告不反向覆写先前未取得事实，也不向未读原件扩认证；不重计新颖性、外审、独立人数或数学run。'),
('4092B/50行全部正文和所有新增尾段实际读完，包含旧OPEN、sharp与强桥失败、两块纠错、菜单和势、17/6→无界→共享信用、stationary及VA。','与同目录README顶端更新/真实银行控制器、现五人/六人范围和四自足数学对象比对；明确旧AGENTS/六研究员是研究历史，非当前规则。','完整保存 successive更新的精确强弱层次，不停在17/6旧边界，不把F−2P循环定义当证明；全路径/aggregate/VApositiveM仍各保其独立未付义务，未做第三阶段图导入。')]
receipts=[]
for x,(a,b,c) in zip(coverage,notes):receipts.append({'id':x['id'],'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':a+' 原4ID真实claim pushed/synced及当前Boss4 owner/sourceSHA已核，回执原字节保留。','comparison_note':b,'decision_note':c,'disposition':'integrated','targets':x['targets']})
js(W/'semantic-receipts.json',receipts)
put(E/'README.md',r'''# D22四总入口的数学与时态清洗

4primary35961B/319行全部正文完整读；主Q+10辅助合同、6失败机制。15必要数学MD原稿完整读（含补5359B遗漏原表），每件原字节/SHA256/blobSHA1保全，不额外done引用源。

四自足对象保存两无限SPE族F精确消元、任意固定局部系数和共享负载信用障碍、M0强查询/正M税、隔离锐界/逃逸E，以及全部菜单/数值/版本合同。原14类遗漏与现12类族、两套R/S平局选择器区分；完整二人接口相同不外推三人。

新原CLI/数学程序/SPE/BI/LP/随机/旧成功重跑全0。原8人DAG/三块全部截面/6286报告文字已读，原code/JSON在本批未取得全文实读，不冒运行或认证、也不误报为已尝试缺失。普遍解析结论与单实现有限枚举/独立局部审查分别记载。2次纯本地helper共15exports0missing，无网络/lazyfetch/sharedGit/真实身份操作。

copy-files.json是完整白名单，Root串行复制并先推正文再done；本代理不checkpoint/done/claim。当前形式检查不替代数学阅读和推导，也不导入phase3旧图。
''')
put(W/'relation-review.md',r'''# 阶段二关系核对

真实分支账本是资源，不把各旧状态自动继承为证明。主Q与十辅助合同逐条指向已有对象或本批三个解析对象：利润障碍合用两个完整SPE族的精确F，并由同r共享f值排模板；单色引理从两个真实末节点和根饱和取等推出查询界，RES正税仍待支付；隔离障碍仅由指定两枝真实收益相等得到锐界，撤假设后保E缺额。

原14类遗漏与现12类族二人等价由同一大小/两两交集决定；B/Q处R/S平局选择不同，三重交集2/6不同，不能据来源“同证书”推字节或高阶等价。8人DAG后时点声称完整与旧页当时缺证据可同时为真；当前未读其原报告不新增认证。条件n块矩阵的minimax不创造SPE，lastlow解析通用引理与单C++全部截面/一个独立局部代表保持三层范围。6286完整槽平稳反例只排指定核选择，DY1274尾核是不同输入/核。

FM旧OPEN现由真正银行零根SPE反驳，弱推送/逐人threshold也各有独立反例；条件minimax与静态OPT归约仍真，不能据此前提失败否定结论half。Bellman局部亏损既不否F≤2P又不否aggregate；孤立谱/势/必要LP点不冒完整策略。

本批关系已人工逐条说明，第三阶段mapper/超图导入为0，不为连通造边。引用源未额外领/done，不覆写其他owner的历史页。
''')
nextids=['5807ac87276a9bc80ce0','0efa8da260f6c6ee8015','9bf8a294ee059185147e','86390a643a36ea35f311','bdd683848aab07c77142'];nextrows=[]
for i in nextids:
 v=next(v for v in related if v['id']==i);q=REPO/'cleanup/progress'/f'{i}.json';pr=json.loads(q.read_text()) if q.exists() else None
 if pr is None:nextrows.append({**v,'local_path':str(S/v['preserved_path']),'progress_observed':None,'read_status':'already fully read GS as necessary related; primary completion not claimed, can honestly reuse sameSHA after actualclaim','next_hint':'source main text and allmath already related-read; Root deconflict/actualclaim required before any new primaryreceipt'})
js(W/'next-candidates.json',nextrows)
# Preserve the exact generator; no mathematical program executions are hidden in this packaging step.
cp(Path(__file__),E/'build_delivery.py')
checks=[]
def ck(n,v):checks.append({'check':n,'passed':bool(v)});assert v,n
for x in primary+related:
 b=(S/x['preserved_path']).read_bytes();ck('source exactsize/SHA '+x['id'],len(b)==x['size'] and sha(b)==x['sha256']);ck('source exactblob '+x['id'],hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'])
ck('rawclaim unchanged',(S/E/'actual-unprojected-claim-receipt.json').read_bytes()==claimpath.read_bytes());ck('actual4IDs ownergate',set(claim['ids'])==set(IDS) and len(owners)==4 and all(x['owner']=='Boss4' for x in owners))
for x in contexts:ck('context exactbytes '+x['path'],len((S/x['snapshot']).read_bytes())==x['bytes'] and sha((S/x['snapshot']).read_bytes())==x['sha256'])
links=[]
for p in PS:
 t=(S/p).read_text();ck('flatMATEK '+p,all(re.search('^'+f+':',t,re.M) for f in ['id','kind','type_tag','title','status','summary','source_refs']));ck('nonLF C0zero '+p,not any(ord(c)<32 and c!='\n' for c in t));ck('trailingwhitespacezero '+p,all(l==l.rstrip() for l in t.splitlines()));ck('displayTeXbalanced '+p,t.count('\\[')==t.count('\\]'))
 for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)',t):
  if '://' in dest or dest.startswith('#'):continue
  n=posixpath.normpath(str(Path(p).parent/dest.split('#',1)[0]));q=S/n if (S/n).exists() else REPO/n;ck('actual relative link '+dest,q.exists());links.append({'source':p,'destination':dest,'resolved':n,'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())})
js(E/'formal-link-check.json',links)
t=(S/P1).read_text();ck('all10auxIDs present',all(x in t for x in ['UNIQUE-OPTIMUM-OMISSION-OBSTRUCTION-v1','TWO-PLAYER-INTEGER-PUSH-SHARP-v1','THREE-PLAYER-INTEGER-PUSH-AVERAGE-NO-v1','RECIPROCAL-ISOLATION-SHARP-v1','PURE-FULL-ROOT-MENU-NO-v1','MIXED-FULL-ROOT-MENU-v1','PROFIT-BELLMAN-LOCAL-NO-v1','PROFIT-BELLMAN-ANY-FIXED-NO-v1','MONOCHROME-SATURATED-QUERY-v1','OVERLAP-ONLY-ADDITIVE-CREDIT-NO-v1']))
ck('14versus12andselector explicitlypreserved','(B,R,R,R,S,R)' in t and '(B,S,R,S,S,R)' in t and '三人(B,R,S)' in t and '41/3和15' in t)
ck('DAGauthor notcurrentmachinecertification','未读原DAG/代码/report' in t and '59496' in t and '2396745' in t);ck('allcuts andlocal witness scope','仅一C++实现' in t and '不排先C1/C2' in t);ck('distinct6286fullkernel not1274tail','6286' in t and 'DY的1274' in t and '258' in t and '123/4' in t)
ck('FMcurrentfalse conditionnotproof','一般全称现在**假**' in t and '条件归约' in t);ck('exact source count andlines',scope['primary_bytes']==35961 and scope['primary_lines']==319 and len(primary)==4 and len(related)==15)
ck('allnewmathrunszero',all(scope[k]==0 for k in ['new_original_CLI_calls','new_math_program_runs','old_success_replays','new_SPE_or_LP_or_BI_audits','new_numerical_or_random_checks']))
ck('unbounded andsharedcredit precision','q>(α+1)/2' in (S/P2).read_text() and 'n≥16' in (S/P2).read_text() and '不依实例' in (S/P2).read_text());ck('M0 notpositiveM stability','M>0' in (S/P3).read_text() and '饱和必须是等式' in (S/P3).read_text());ck('isolation exactdomain Enecessity','E>(k+2)d/3' in (S/P4).read_text() and '必要但非充分' in (S/P4).read_text())
ck('4complete receipts',len(receipts)==4 and {x['id'] for x in receipts}==set(IDS))
for x in receipts:ck('complete semantic receipt '+x['id'],all(x[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','targets']) and all((S/p).exists() for p in x['targets']))
for x in json.loads((S/E/'formal-resource-manifest.json').read_text()):ck('exactderivedformalhash '+x['path'],len((S/x['path']).read_bytes())==x['bytes'] and sha((S/x['path']).read_bytes())==x['sha256'])
for x in nextrows:ck('actualnext local '+x['id'],len(Path(x['local_path']).read_bytes())==x['size'] and sha(Path(x['local_path']).read_bytes())==x['sha256'] and x['progress_observed'] is None)
obs=[]
for p in S.rglob('*'):
 if not p.is_file():continue
 try:u=p.read_bytes().decode('utf-8')
 except UnicodeDecodeError:continue
 frozen=any('/'+z+'/' in str(p.relative_to(S)) for z in ['original','related','related-supplement','context'])
 bad=[i+1 for i,l in enumerate(u.splitlines()) if l!=l.rstrip()];c0=[{'offset':i,'code':ord(c)} for i,c in enumerate(u) if ord(c)<32 and c!='\n']
 if bad or c0:obs.append({'path':str(p.relative_to(S)),'trailing_lines':bad,'nonLF_C0':c0,'frozen':frozen})
ck('all derived C0/whitespace zero',not any(not x['frozen'] for x in obs));js(E/'transport-format-observations.json',{'observations':obs,'frozen_inputs_unchanged':True})
put(W/'delivery.md',f'''# GS交付

4源35961B/319行全文数学实读，主Q+10辅助合同、6失败机制；15必要数学原稿完整读原字节保全。4新自足正式对象、4semantic receipts，不额外done related或规范页。

真实claim {claim['remote_tip']} pushed/synced原4IDs回执未改，当前owner及sourceSHA核齐。两无限族精确利润/无界系数/共享信用、M0查询和正税、隔离E、自足菜单矩阵/lastlow与6286定核边界均保全。D2214类与现12类/两套R-S平局选择器不同，只二人接口等价。

原8人完整DAG、三块单实现全部截面和6286报告仅按实际MD证据身份，不冒未读rawcode/JSON的新认证；0新数学/原CLI/旧成功重跑。2纯本地helper15exports0missing，无网络/lazyfetch/sharedGit/真实账号行为。Root先checkpoint正文依赖再done。下一{len(nextrows)}件实际本地related原稿已全读可诚实复用，但须Root新claim及owner核才新primary。
''')
js(W/'self-check.json',{'passed':True,'checks':len(checks),'details':checks,'relative_links':len(links),'formal_nonLF_C0':0,'formal_trailing_whitespace':0,'mathematics_not_certified_by_checker':'checks only bind bytes/owner/manifest, precise coverage and formatting; analytic arguments full actual reading and derivation, no program PASS extends mathematical scope'})
files=[]
for p in sorted(S.rglob('*')):
 if p.is_file() and str(p.relative_to(S)) not in ['copy-files.json','copy-paths.txt','delivery-summary.json']:
  b=p.read_bytes();files.append({'path':str(p.relative_to(S)),'bytes':len(b),'sha256':sha(b)})
js(Path('copy-files.json'),files);put(Path('copy-paths.txt'),'\n'.join(x['path'] for x in files)+'\n');summary={'stage':str(S),'copy_files':len(files),'copy_bytes':sum(x['bytes'] for x in files),'copy_manifest_sha256':sha((S/'copy-files.json').read_bytes()),'primary_ids':IDS,'primary_bytes':scope['primary_bytes'],'primary_lines':scope['primary_lines'],'related_sources':len(related),'related_bytes':scope['related_bytes'],'new_formals':4,'formal_bytes':sum((S/p).stat().st_size for p in PS),'receipts':4,'checks':len(checks),'relative_links':len(links),'new_math_runs':0,'claim_tip':claim['remote_tip'],'next_candidates':[x['id'] for x in nextrows]};js(Path('delivery-summary.json'),summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
