import json
from pathlib import Path
P=Path(__file__).parent;U=[]
def u(label,bbox,t,supp=None,ev=None,study=None):
 d={'label':label,'bbox':bbox,'transcript':t}
 if supp:d['supplements']=supp
 if ev:d['extra_evidence']=ev
 if study is not None:d['study']=study
 U.append(d)
u('空集与全空间可测',[175,315,1145,495],r'（1）$\varnothing\in\mathcal M$，$\mathbb R^n\in\mathcal M$。',supp=[r'''> [!info] 补证：空集与全空间
> 对任意测试集 $T$，用 $\varnothing$ 切分时得到 $\varnothing$ 与 $T$，用 $\mathbb R^n$ 切分时得到 $T$ 与 $\varnothing$。因为 $m^*(\varnothing)=0$，两次都满足定义中的等式。'''])
u('提纲式不可测可测两词',[180,485,840,620],r'（2）不可测，可测。',ev=['artifact:p0009-list'],supp=[r'''> [!info] 补充：提纲式原文
> 本行只有“不可测，可测”两个词，没有写关系或完整命题，故按提纲片段保留；后面关于封闭运算的完整表述另补如下。'''])
u('并交补及上下极限提纲',[180,595,1055,740],r'（3）并、交、补，上下极限。',supp=[r'''> [!info] 补充：可测集族的封闭运算
> 精确命题是：$\mathcal M$ 对补、可数并、可数交封闭，从而对可测集列的上极限、下极限也封闭。任意不可数并、交一般不能由这条命题推出。下面给出全部步骤，原稿此处仅列关键词。''',r'''> [!info] 补证：补与有限运算
> 若 $E$ 可测，把分割等式中的 $E,E^c$ 交换即知 $E^c$ 可测。若 $E,F$ 可测，对任意 $T$ 先用 $E$ 分割，再用 $F$ 分割 $T\cap E$，得到
> $$m^*(T)=m^*(T\cap E\cap F)+m^*(T\cap E\cap F^c)+m^*(T\cap E^c).$$
> 因为后两块并成 $T\cap(E\cap F)^c$，次可加性使上式右端不小于 $m^*(T\cap E\cap F)+m^*(T\cap(E\cap F)^c)$。再结合通常的相反不等式，即得 $E\cap F$ 可测。由 De Morgan 律，有限并和差集也可测。整个推导没有作 $\infty-\infty$。''',r'''> [!info] 补证：可数并与可数可加性
> 先设 $E_k$ 两两不交且可测，令 $E=\bigcup_{k\ge1}E_k$、$F_N=\bigcup_{k=1}^NE_k$。反复使用有限次分割等式，并用 $T\setminus E\subset T\setminus F_N$，得
> $$m^*(T)=\sum_{k=1}^Nm^*(T\cap E_k)+m^*(T\setminus F_N)
> \ge\sum_{k=1}^Nm^*(T\cap E_k)+m^*(T\setminus E).$$
> 对非负部分和取上确界，结合 $m^*(T\cap E)\le\sum_{k\ge1}m^*(T\cap E_k)$，得到 $m^*(T)\ge m^*(T\cap E)+m^*(T\setminus E)$。次可加性给另一方向，所以 $E$ 可测。一般可测集列 $A_k$ 可改写成不交列 $E_1=A_1$、$E_k=A_k\setminus\bigcup_{j<k}A_j$，并集不变，故可数并封闭；可数交再由补和 De Morgan 律得到。
>
> 在两两不交的情形中取 $T=E$，上述有限部分和估计给出 $m(E)\ge\sum_km(E_k)$；次可加性给反向，故 $m(E)=\sum_km(E_k)$。这同时证明 $m=m^*|_{\mathcal M}$ 是测度。''',r'''> [!info] 补证：上下极限
> 对集合列 $E_k$，
> $$\limsup_{k\to\infty}E_k=\bigcap_{N=1}^{\infty}\bigcup_{k\ge N}E_k,\qquad
> \liminf_{k\to\infty}E_k=\bigcup_{N=1}^{\infty}\bigcap_{k\ge N}E_k.$$
> 前者由“无穷多次属于”这些集合的点组成，后者由“从某项起每次属于”的点组成。两式都只用可数并交，因此当各 $E_k$ 可测时，上下极限可测。'''])
u('零测集定义',[125,695,1415,925],r'**Def.** 外测度为 $0$ 之集，称为零测集。')
u('零测集必可测命题',[110,945,880,1110],r'**Prop.** 零测集必可测。')
u('零测证明中的夹逼零',[150,1180,1235,1340],r'$$0\le m^*(T\cap E)\le m^*(E)=0.$$')
u('零测证明第二行原写E',[185,1335,1070,1495],r'因 $m^*(T)\ge m^*(T\cap E)$。',ev=['artifact:p0009-nullproof'],supp=[r'''> [!info] 纠错及补证：第二行还需补集部分
> 原稿第二行末项确写 $T\cap E$，没有可辨的补集上标。该不等式虽真，只能说明 $m^*(T)\ge0$，尚不足以得到分割等式。正确收尾是由单调性
> $$m^*(T)\ge m^*(T\cap E^c)=m^*(T\cap E)+m^*(T\cap E^c),$$
> 其中最后一步用已证的 $m^*(T\cap E)=0$。再由次可加性得到相反不等式，故 $E$ 可测。对 $m^*(T)=\infty$ 仍合法，因为没有作减法。'''])
u('零测集子集仍零测',[150,1560,1180,1740],r'（2）零测集子集是零测集。',supp=[r'''> [!info] 补证：完备性
> 若 $A\subset E$ 且 $m^*(E)=0$，单调性给出 $0\le m^*(A)\le0$，所以 $A$ 也是零测集；上一命题又说明 $A$ 可测。Lebesgue 测度因而是完备测度，即每个可测零测集的任意子集仍可测。'''])
u('至多可数个零测集并',[145,1790,1550,1985],r'（3）至多个可数个零测集并是零测集。',supp=[r'''> [!info] 补证：可数并
> 把“至多个可数个”整理为“至多可数个”。若 $m^*(E_k)=0$，则 $0\le m^*(\bigcup_kE_k)\le\sum_km^*(E_k)=0$。有限并可补上空集成为可数列；空并也是空集。不可数并不能照此推出，例如所有单点的并可为整个 $[0,1]$。'''])
u('基数运算的集合及记号',[130,2150,1465,2400],r'**Def.** $A\cap B=\varnothing$，$\overline{\overline A}=\alpha$，$\overline{\overline B}=\beta$。',supp=[r'''> [!info] 补充：双横线表示基数
> 这里 $\overline{\overline A}=|A|$ 表示集合的势，不是拓扑闭包。设 $\alpha=|A|$、$\beta=|B|$，以下三式定义基数的加法、乘法与幂。为定义加法可先取不交的带标记副本，故 $A\cap B=\varnothing$ 不限制可定义的两个基数。'''])
u('基数加法',[175,2400,805,2580],r'（1）$\overline{\overline{A\cup B}}=\alpha+\beta$。')
u('基数乘法',[150,2565,775,2730],r'（2）$\alpha\cdot\beta=\overline{\overline{A\times B}}$。')
u('基数幂及函数集',[145,2700,1280,2870],r'（3）$\alpha^\beta=\overline{\overline{A^B}}=\{f:B\to A\}$。',supp=[r'''> [!info] 纠错：函数集与其基数
> 原稿把函数集合直接接在基数的等号之后。应分为 $A^B=\{f\mid f:B\to A\}$ 和 $\alpha^\beta=|A^B|$。例如幂集 $\mathcal P(B)$ 与 $\{0,1\}^B$ 由特征函数一一对应，所以 $|\mathcal P(B)|=2^{|B|}$。'''])
u('可测集族势的上下界',[210,2905,975,3140],r'$$2^c\le\overline{\overline{\mathcal M}}\le2^c.$$')
u('Cantor任意子集可测的基数说明',[205,3175,1195,3335],r'Cantor（上方标 $c$）：任意子集可测，$2^c$。',supp=[r'''> [!info] 补证：为什么可测集族有 $2^c$ 个元素
> 三分 Cantor 集 $C$ 的外测度是 $0$、势为 $c$，前面已分别证明。因此 $\mathcal P(C)\subset\mathcal M$，而 $|\mathcal P(C)|=2^c$，给出下界。另一方面 $\mathcal M\subset\mathcal P(\mathbb R^n)$，且有限维欧氏空间的势为 $c$，故 $|\mathcal M|\le2^c$。由两边夹逼，$|\mathcal M|=2^c$。
>
> 这里说的是“可测集本身所组成的集合族”有多大；并不表示每个可测集都具有相同的势，也不把所有 $\mathbb R^n$ 的子集都判为可测。'''])
p={'page':9,'title':'可测族运算、零测集与可测族的势','anchor':'null-and-cardinality','units':U,
'layout':'顶部三条提纲后转零测集定义及性质；中部有两行极短可测性证明、子集和可数并命题；下半列基数三运算，页底以Cantor零测集说明可测族的势。右侧空白较多。',
'observation':'整页后六区和两局部裁图均实际查看。顶部第二条只有不可测、可测两词，未自行加关系。零测证明第二行末E没有补集c，照录并纠错。第8页Proof没有在本页接续；本页直接另起性质清单。基数幂原式把函数集等同基数的问题已保留并校正。',
'regions':[
'首为(1)空集、Rn属于M，末为Prop零测集必可测。中间(2)不可测，可测为碎片，(3)并交补上下极限；零测集定义右端跨到右区。',
'仅中部有定义尾部“零测集”，底缘有首个0的曲线边缘；其余右侧全白。没有额外条件或旁注。',
'首为零测证明夹逼式，末为Def A∩B=∅及α、β基数记号。第二证明行写m*(T)≥m*(T∩E)；其后零测子集与至多可数并性质均清晰。',
'首为夹逼式末0边缘，末为基数β记号；中间有“零测集”句末，其余右侧大块留白。',
'首为基数Def残尾，末为Cantor任意子集可测2^c。三项依次为不交并、积、函数幂；双横线与幂的上下标都核对，最后上下界同为2^c。',
'仅左缘出现β、函数集右括号及页底2^c的边缘，其余空白；没有独立内容。']}
(P/'p009.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p8=P/'p008.json';d=json.loads(p8.read_text());d['units'][9]['study']='**Proof：**\n\n<span style="color:red">〔原稿待填：该 Proof 标题后未写证明；下一物理页已转入零测集等新主题。〕</span>'
p8.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
