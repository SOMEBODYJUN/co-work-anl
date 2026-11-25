import json
from pathlib import Path
P=Path(__file__).parent
U=[]
def u(label,bbox,t,supp=None,study=None):
 d={'label':label,'bbox':bbox,'transcript':t}
 if supp:d['supplements']=supp
 if study is not None:d['study']=study
 U.append(d)
u('原写Riemann可积判据上确界下确界互换',[185,315,1780,545],r'''$$\sup_P U(f,P)=\inf_P L(f,P)\quad\Rightarrow\quad\text{Rm 可积}. $$''',supp=[r'''> [!info] 纠错：Darboux 判据中的上下确界
> 原稿把标准判据的 $\inf$ 与 $\sup$ 对调了。对于闭区间上的有界函数，正确的充要条件是
> $$\inf_P U(f,P)=\sup_P L(f,P).$$
> 左侧是上积分，右侧是下积分。对任意两个分割 $P,Q$，取共同加细 $R$ 得 $L(f,P)\le L(f,R)\le U(f,R)\le U(f,Q)$，故下积分不大于上积分；若相等，则可选分割分别使上、下和离共同值小于 $\varepsilon/2$，再共同加细，得到 $U-L<\varepsilon$。反过来，存在任意小的上、下和差时，二者的差只能为零。
>
> 原写的等式是过强的条件，仍能推出可积，但不能用作一般可积函数的判据。例如 $f(x)=x$ 在 $[0,1]$ 上可积，而单区间分割给出 $U=1,L=0$，所以 $\sup_PU=1\ne0=\inf_PL$。'''])
u('内外测度对应',[155,585,900,725],r'可以对应：内外测度。')
u('Jordan边界判据',[180,810,2100,1010],r'''$E\subset\mathbb R^n$，则
$$E\text{ Jordan 可测}\iff m_J^*(\partial E)=0.$$''',supp=[r'''> [!info] 补充：有界性与判据说明
> Jordan 可测通常限定在有界集合。精确命题是：有界 $E\subset\mathbb R^n$ Jordan 可测，当且仅当其边界 $\partial E$ 的 Jordan 外内容为零。
>
> 取包含 $\overline E$ 的闭长方体 $R$。$E$ 的 Jordan 可测性等价于 $1_E$ 的上、下 Darboux 积分相等。网格中同时接触 $E$ 与 $E^c$ 的小长方体使 $1_E$ 的振幅为 $1$，其他小长方体使振幅为 $0$，因而上、下和之差就是这些混合小长方体体积的和。
>
> 若边界可被总体积任意小的有限个开长方体覆盖，由 $\partial E$ 的紧致性，可以选择足够细的网格，使每个接触边界的小长方体都留在这些开长方体的并中。混合小长方体必接触边界，故上、下和差任意小。
>
> 反过来，若上、下和差任意小，则混合小长方体覆盖除网格分割面外的全部边界。有限个网格分割面可用总体积任意小的薄长方体覆盖；再把混合小长方体略微扩大成开长方体，总体积仍可任意小。因此 $m_J^*(\partial E)=0$。'''])
u('Jordan外内容与积分的孤立提示',[140,1030,755,1240],r'''原稿另写提示：$m_J^*:\ \displaystyle\int_a^b f(x)$。''',supp=[r'''> [!info] 补充：提示的规范含义
> 对有界 $E\subset[a,b]$，Jordan 外内容对应示性函数的上 Darboux 积分 $\overline{\int_a^b}1_E(x)\,dx$；内内容对应下积分。原稿此行未写被积函数应取 $1_E$、上下积分标记及 $dx$，这里补明对应关系。'''])
u('稠密集有限开覆盖引理条件',[110,1290,2180,1505],r'''**Lemma.** 若 $S$ 在 $[0,1]$ 中稠密，且
$$S\cap[0,1]\subset\bigcup_{i=1}^{n}(a_i,b_i),$$''')
u('稠密集有限覆盖引理结论',[160,1535,1110,1755],r'''则
$$[0,1]\subset\bigcup_{i=1}^{n}[a_i,b_i].$$''')
u('引理原证明关键词',[110,1730,455,1980],r'''Proof：内逼外包。''',supp=[r'''> [!info] 补证：有限性的作用
> 因为 $S\cap[0,1]$ 在 $[0,1]$ 中稠密，$[0,1]\subseteq\overline{S\cap[0,1]}$。有限个闭区间的并是闭集，而
> $$S\cap[0,1]\subseteq\bigcup_{i=1}^n(a_i,b_i)\subseteq\bigcup_{i=1}^n[a_i,b_i].$$
> 对包含关系取闭包即可得到结论。这里不能把有限并未经检验换成可列并，因为可列个闭集的并不必闭。'''])
u('对无限集求和的网旁注',[120,2085,1020,2235],r'对无限集定义求和（网）。',supp=[r'''> [!info] 补充：非负族的求和
> 对任意指标集 $I$ 上的非负数族 $(a_i)$，定义 $\sum_{i\in I}a_i=\sup\{\sum_{i\in F}a_i:F\subset I\text{ 有限}\}$。有限子集按包含关系构成有向集，这些有限部分和构成递增网。此说明只补足“网”的含义，不给原稿额外附加一个未写出的定理。'''])
u('Lebesgue覆盖定义',[110,2310,1360,2720],r'''**Def（1）** $E\subset\mathbb R^n$，有开区间 $(I_k)$，使得
$$E\subset\bigcup_{k=1}^{\infty}I_k,$$
则称一个 Lebesgue 覆盖。''',supp=[r'''> [!info] 补充：高维区间和覆盖族
> 在 $\mathbb R^n$ 中，“开区间”指有界开长方体 $I=\prod_{j=1}^n(a_j,b_j)$，$a_j<b_j$。将 $E$ 的全部可列此类覆盖组成的族记作 $LC(E)$；一个族中的元素本身是一列开长方体。'''])
u('每个集合存在Lebesgue覆盖',[115,2715,1125,2845],r'''1. $LC(E)\ne\varnothing$，$\forall E\subset\mathbb R^n$。''')
u('整数端点开长方体族',[205,2845,1360,2990],r'''$$I_\alpha=(a_1,b_1)\cdots(a_n,b_n),\qquad a_i,b_i\in\mathbb Z.$$''',supp=[r'''> [!info] 补充：可列性
> 只取 $a_i<b_i$。每个长方体由一个整数 $2n$ 元组确定，而 $\mathbb Z^{2n}$ 可列，因此全部这类开长方体可列。原稿的并集下标仅为简记，这里用 $\alpha$ 表示枚举指标。'''])
u('整数端点长方体覆盖全空间',[220,2990,590,3100],r'$$\mathbb R^n=\bigcup_\alpha I_\alpha.$$')
u('选点与取整构造',[170,3100,1060,3385],r'''$\forall x=(x_1,\ldots,x_n)$，
$$x\in\prod\bigl([x_1]-1,\ldots,[x_n]+1\bigr).$$
（此处保留原稿压缩的乘积记号。）''',supp=[r'''> [!info] 补全记号：逐坐标选取开区间
> $[x_j]$ 表示取整 $\lfloor x_j\rfloor$。准确地说，
> $$x\in\prod_{j=1}^{n}\bigl(\lfloor x_j\rfloor-1,\lfloor x_j\rfloor+1\bigr).$$
> 因为 $\lfloor x_j\rfloor\le x_j<\lfloor x_j\rfloor+1$，每个坐标都严格落在所选开区间内。所选端点为整数，故该长方体属于上述可列族。这样证明了它们覆盖 $\mathbb R^n$，也就覆盖任意 $E\subset\mathbb R^n$。'''])
p={'page':2,'title':'Jordan 判据、稠密覆盖引理与 Lebesgue 覆盖','anchor':'jordan-and-coverings','units':U,
'layout':'单列从上向下：接上页上下和判据；中上为 Jordan 边界判据；中部 Lemma 横跨左右区，Proof 仅关键词；下部是无限求和旁注及 Lebesgue 覆盖定义和存在性构造。最下行靠页底但未被裁断。',
'observation':'先整页后六区已实际查看。顶行确为 sup U=inf L，原错误保留并蓝色订正。引理前件用开区间，结论用闭区间且有限并；底部整数端点与取整构造完整可读。原稿的 Proof 后仅“内逼外包”，没有隐藏证明。',
'regions':[
'首为 sup_P U=inf_P L，末为 m_J^* 与积分提示；确认原写上下确界顺序及 E⊂R^n。右区接“Rm可积”和边界判据右半。页顶为普通空白。',
'首为箭头 Rm可积，末为 iff m_J^*(∂E)=0；核对偏导形符号实际为边界 ∂。右侧余部空白，无额外条件补在边缘。',
'首为积分提示残部，末为 Lebesgue 定义开头；主体核对 S在[0,1]中稠密、结论有限闭区间并、Proof 内逼外包以及无限集求和（网）。开覆盖条件在右区续完。',
'首为且 S∩[0,1]⊂并_{i=1}^n(a_i,b_i)，末在下边缘出现 (I_k)；中间及右侧大片空白。确认上界为有限 n，非∞。',
'首为 Def(1) 与 E⊂R^n，末为逐坐标取整乘积；核对可列并、LC(E)≠空、整数端点、R^n等于并集。最后乘积为压缩写法，学习稿另补完整逐坐标记号。',
'首为定义中 (I_k) 的右端，末为 a_i,b_i∈Z 的 Z；其余无笔迹。所有右侧表达与左区相接，不产生独立空白待填。']}
(P/'p002.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
