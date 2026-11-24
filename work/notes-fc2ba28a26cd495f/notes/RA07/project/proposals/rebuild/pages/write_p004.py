import json
from pathlib import Path
P=Path(__file__).parent;U=[]
def u(label,bbox,t,supp=None):
 d={'label':label,'bbox':bbox,'transcript':t}
 if supp:d['supplements']=supp
 U.append(d)
u('外测度可列次可加性',[165,345,1550,470],r'''（3）$\{E_k\}$：
$$m^*\!\left(\bigcup_kE_k\right)\le\sum_km^*(E_k).$$''')
u('epsilon与逐集合选择近最优覆盖',[180,445,2410,645],r'''Proof：$\forall\varepsilon>0$，$\exists\{I_{k,j}\}\in LC(E_k)$（有限时）。''',supp=[r'''> [!info] 补充：有限与无穷分支
> 先补上两个初步性质的证明。空集可由全为空集的序列覆盖，总体积为零，故 $m^*(\varnothing)=0$。若 $E\subset F$，每个 $F$ 的覆盖也是 $E$ 的覆盖，即 $LC(F)\subseteq LC(E)$，下确界遂满足 $m^*(E)\le m^*(F)$。
>
> 对次可加性，若 $\sum_km^*(E_k)=+\infty$，待证不等式直接成立。否则每个 $m^*(E_k)<\infty$，因此能按下确界的定义选择下面的近最优覆盖。“有限时”应在这个总和有限的分支使用。'''])
u('每个E_k的覆盖包含',[590,685,1270,860],r'$$E_k\subset\bigcup_{j=1}^{\infty}I_{k,j}.$$')
u('下确界误差epsilon除2的k次',[650,890,2210,1165],r'''$$\sum_{j=1}^{\infty}|I_{k,j}|<m^*(E_k)+\frac{\varepsilon}{2^k}\qquad\text{（下确界）}.$$''')
u('合并双指标覆盖',[610,1160,1450,1400],r'$$\bigcup_kE_k\subset\bigcup_{k=1}^{\infty}\bigcup_{j=1}^{\infty}I_{k,j}.$$' ,supp=[r'''> [!info] 补充：可列覆盖仍合法
> $\mathbb N\times\mathbb N$ 是可列集，所以全部 $I_{k,j}$ 可以排成一个序列；这个序列属于 $LC(\bigcup_kE_k)$。此处只使用开长方体覆盖的定义，没有预先假设可列次可加性。'''])
u('由合并覆盖求外测度上界',[610,1395,1725,1630],r'''$$m^*\!\left(\bigcup_{k=1}^{\infty}E_k\right)\le\sum_{(k,j)}|I_{k,j}|.$$
首个不等式下旁注：“下界”。''')
u('双重和的总误差上界',[1640,1390,2450,1635],r'''$$\sum_{(k,j)}|I_{k,j}|<\sum_km^*(E_k)+\sum_{k=1}^{\infty}\frac{\varepsilon}{2^k}.$$''')
u('Tonelli换序与epsilon趋零',[270,1630,1405,1970],r'''Tonelli：可交换顺序。

$\varepsilon\to0$，取“$\le$”。''',supp=[r'''> [!info] 补证：非负双重和的换序及结论
> 对 $a_{k,j}=|I_{k,j}|\ge0$，把总和定义为所有有限指标子集部分和的上确界，则
> $$\sum_{(k,j)}a_{k,j}=\sum_k\sum_ja_{k,j}.$$
> 一方面每个有限指标子集只涉及有限个 $k$，其和不超过右侧；另一方面，任取有限个 $k$，各行和都可用有限部分和从下逼近，故这些行和的总和不超过左侧，再对有限个 $k$ 取上确界。这个初等非负求和论证就是此处调用 Tonelli 的具体内容。
>
> 因为 $\sum_{k=1}^{\infty}2^{-k}=1$，可得 $m^*(\bigcup_kE_k)\le\sum_km^*(E_k)+\varepsilon$。对任意 $\varepsilon>0$ 成立，遂得所列性质（3）。'''])
u('可列点集外测度为零',[170,2065,1585,2245],r'''**Prop.** $\{x_k\}\subset\mathbb R^n$，$m^*(\{x_k\})=0$。''',supp=[r'''> [!info] 补证：单点与可列点集
> 固定 $x\in\mathbb R^n$，用以 $x$ 为中心、边长 $2r$ 的开立方体覆盖它，得 $0\le m^*(\{x\})\le(2r)^n$。令 $r\downarrow0$ 得单点外测度为零。然后用可列次可加性：
> $$0\le m^*(\{x_k:k\ge1\})\le\sum_{k=1}^{\infty}m^*(\{x_k\})=0.$$'''])
u('有理数区间交的推论',[175,2310,1130,2495],r'**Cor.** $m^*(\mathbb Q\cap[0,1])=0$。')
u('Cantor集与递降逼近',[135,2575,865,2990],r'''Cantor：$C\subset[0,1]$。
$$C=\bigcap_{n=0}^{\infty}C_n.$$''',supp=[r'''> [!info] 补充：Cantor 构造与所需体积上界
> $C_0=[0,1]$，每一步从保留的每个闭区间中删去中间三分之一开区间。于是 $C_n$ 由 $2^n$ 个长度为 $3^{-n}$ 的闭区间组成。对任何有限个闭区间，可把它们略微扩大为开区间，总长度只增加任意给定的 $\eta>0$；因此其并的外测度不超过原总长度。此上界可直接从定义得到，先于后文的“区间外测度等于长度”定理使用，不发生依赖循环。'''])
u('Cantor外测度的估计',[390,2980,1445,3205],r'$$m^*(C)\le m^*(C_n)=\left(\frac23\right)^n.$$' ,supp=[r'''> [!info] 补充：此处只需不等式
> 原稿写了 $m^*(C_n)=(2/3)^n$，该等式将在区间测度与有限可加性建立后成立。当前证明只需已说明的 $m^*(C_n)\le 2^n3^{-n}$。故对每个 $n$，$0\le m^*(C)\le(2/3)^n$；让 $n\to\infty$ 即得结论。'''])
u('Cantor零测与基数问答',[410,3180,2050,3390],r'''$$m^*(C)=0.$$
旁注：“势是多少？”答：$\mathfrak c$。''',supp=[r'''> [!info] 补证：零外测度不等于可数
> 每个二进制序列 $(a_j)_{j\ge1}\in\{0,1\}^{\mathbb N}$ 给出 Cantor 点 $x=\sum_{j=1}^{\infty}2a_j3^{-j}$，因为其每一步都落在保留的闭区间中。若两个序列首次在第 $j$ 位不同，则主项差为 $2\cdot3^{-j}$，其后尾和差的绝对值至多 $3^{-j}$，所以所得两点不同。这给出 $\{0,1\}^{\mathbb N}$ 到 $C$ 的单射，故 $|C|\ge2^{\aleph_0}=\mathfrak c$；又 $C\subset\mathbb R$，故 $|C|=\mathfrak c$。'''])
p={'page':4,'title':'可列次可加性及零外测度例子','anchor':'subadditivity-and-null-sets','units':U,
'layout':'顶端黑字列性质(3)，大段原蓝笔写覆盖证明，含两处右伸长式与“下界”“Tonelli”旁注；下方黑笔给可列集、有理点集和 Cantor 集。无几何图，页底有 Cantor 势的问答。',
'observation':'先全页后六区逐行实际查看。所有蓝笔证明作为原稿内容转成普通正文，新增补证另用 info。识出近最优覆盖误差 epsilon/2^k、双重并、双重和、Tonelli及epsilon→0。Cantor末问已有 c 答案，不标红待填。',
'regions':[
'首为(3)及 m*(并E_k)≤Σm*(E_k)，末为近最优覆盖和式的 j=1；核对 epsilon>0、E_k⊂并_j I_kj。右边继续有限时与误差，顶部普通空白。',
'首为 Σm*(E_k)，末为下确界旁注及 epsilon/2^k；确认原括号写“有限时”。下边有双重并的重叠笔画，右边界未截断关键分母。',
'首为前行求和下标，末为有理数推论开头；核对双重并、m*上界旁的下界、Tonelli可交换顺序、epsilon→0及可列点集命题。长总误差公式在右区续接。',
'首为双重并右半，末为 m*{x_k}=0；中部完整核对 Σ_(k,j)|I_kj|<Σm*(E_k)+Σepsilon/2^k，右端仍在页内。',
'首为 m*(Q∩[0,1])=0，末为 m*(C)=0；核对 C=交_{n=0}∞C_n 和 m*(C_n) 的等号。无 Cantor 构造图，故以原公式及文字保存。',
'首为 (2/3)^n 的右端，末为“势是多少？c”；右侧和底边为普通空白。该问句已带答案，未增加红色任务。']}
(P/'p004.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
