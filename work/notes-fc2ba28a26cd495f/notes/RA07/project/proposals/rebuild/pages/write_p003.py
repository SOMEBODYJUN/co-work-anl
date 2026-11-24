import json
from pathlib import Path
P=Path(__file__).parent;U=[]
def u(label,bbox,t,supp=None,status='resolved',ev=None):
 d={'label':label,'bbox':bbox,'transcript':t,'status':status}
 if supp:d['supplements']=supp
 if ev:d['extra_evidence']=ev
 U.append(d)
u('Lindelof性质的另一条覆盖路线',[110,315,2220,485],r'''或：$\mathbb R^n$ 是 Lindelöf，有遗传性。导出相应区间放大，来证明。''',ev=['artifact:p0003-lindelof'],supp=[r'''> [!info] 补证：保留的第二条覆盖路线
> 欧氏空间有可数拓扑基：端点为有理数的开长方体。任意子空间 $E\subset\mathbb R^n$ 也有由这些基元素与 $E$ 的交组成的可数基，所以 $E$ 的任意相对开覆盖有可列子覆盖。证明是：对每个包含于某个覆盖成员的基元素，选一个这样的覆盖成员；最多选可列多个，且覆盖全部 $E$。
>
> 对每个 $x\in E$ 先选一个包含 $x$ 的有界开长方体；上述性质给出可列子覆盖，于是 $LC(E)\ne\varnothing$。若从相对开集出发，可将它们写成环境开集与 $E$ 的交，再在环境开集中选小开长方体。这补全原稿的“相应区间”提示。
>
> 这里遗传性来自欧氏空间的第二可数性；一般 Lindelöf 空间的任意子空间未必 Lindelöf。'''])
u('覆盖族的记号',[110,580,1190,755],r'''2. $LC(E)$：所有覆盖的族，记为 $LC_E$。''')
u('开区间族基数及端点编码',[100,815,2360,995],r'''$\mathcal I=$“$\mathbb R^n$ 中全体开区间”，原稿简记其大小为 $\mathfrak c$，并写
$$\longrightarrow (\mathfrak c\times\cdots\times\mathfrak c),\qquad \mathfrak c^{\mathbb N}.$$''',supp=[r'''> [!info] 补充：基数与对象区分
> 一个开长方体由 $2n$ 个实数端点编码，因此 $|\mathcal I|\le\mathfrak c^{2n}=\mathfrak c$；仅改变一条边的一个端点已给出连续统多个不同长方体，故 $|\mathcal I|=\mathfrak c$。覆盖族 $LC(E)$ 是可列开长方体序列空间 $\mathcal I^{\mathbb N}$ 的子族。原稿用族本身代写基数，以下加绝对值以分清两者。'''])
u('可列开区间序列族的基数',[225,1050,1285,1260],r'''$$\mathcal I^{\mathbb N}=\mathfrak c^{\mathbb N}=(2^{\aleph_0})^{\aleph_0}=\mathfrak c.$$''',supp=[r'''> [!info] 补充：规范算式
> 上式按基数理解为 $|\mathcal I^{\mathbb N}|=\mathfrak c^{\aleph_0}=2^{\aleph_0\cdot\aleph_0}=\mathfrak c$。因此全部可列覆盖构成一个集合，并且其基数不超过连续统。'''])
u('由覆盖存在性选取一列',[195,1340,1100,1495],r'''由（1）可取 $\{I_k\}\in LC(E)$。''')
u('可覆盖文字与外测度映射',[135,1565,1605,1850],r'''$\{I_k\}$ 可覆盖。

**Def（2）** 定义
$$m^*:2^{\mathbb R^n}\longrightarrow[0,+\infty].$$''')
u('外测度下确界定义与名称',[425,1820,2070,2090],r'''$$E\longmapsto\inf\sum_{k=1}^{\infty}|I_k|,\qquad I_k\in LC_E.$$
约为外测度。''',supp=[r'''> [!info] 补全记号：Lebesgue 外测度
> $$m^*(E)=\inf_{(I_k)\in LC(E)}\sum_{k=1}^{\infty}|I_k|,\qquad |I_k|=\prod_{j=1}^n(b_{kj}-a_{kj}).$$
> 下确界遍历整个覆盖序列 $(I_k)$；原稿 $I_k\in LC_E$ 是省略族括号的写法。每项体积非负，允许总和为 $+\infty$。因为覆盖族非空，该定义给出 $[0,+\infty]$ 中的确定数值。'''])
u('覆盖允许空集',[80,2100,465,2335],r'''**Remark**

（1）$I_n$ 可为 $\varnothing$。''',supp=[r'''> [!info] 补充：空项约定
> 约定 $|\varnothing|=0$，允许用空集补齐有限覆盖，使其成为可列序列。这里不要求每一个编号都对应非空长方体。'''])
u('替代矩形覆盖的问题',[75,2335,1600,2490],r'''（2）$I_n$ 是否可为〔疑字 RA07-Q002：字形候选“闭矩形”〕，可证明。Proof：''',status='unresolved',ev=['artifact:p0003-rectangle'])
u('替代覆盖证明的epsilon和覆盖条件',[80,2475,770,2715],r'''$\forall\varepsilon$，$\forall\{B_i\}\in\overline{\mathcal B}$，
$$I\subset\bigcup_iB_i.$$''')
u('替代覆盖体积控制',[275,2710,875,2875],r'$$\sum_i|B_i|<|I|+\varepsilon.$$' ,supp=[r'''> [!info] 补证：以闭长方体替代开长方体的版本
> 原问题中形状的逐字读法尚待复核。以下完成候选“闭矩形”对应的命题，并保留上面的覆盖与体积控制路线。
>
> 记 $m_o^*$ 为开长方体覆盖定义的外测度，$m_c^*$ 为闭长方体覆盖定义的数值。任一开长方体可用自己的闭包覆盖，体积不变，所以 $m_c^*(E)\le m_o^*(E)$。反方向，给定闭长方体覆盖 $(B_i)$ 和 $\varepsilon>0$，逐个把边向外扩大，得到开长方体 $J_i\supset B_i$，并使 $|J_i|<|B_i|+\varepsilon2^{-i}$；这由有限乘积对边长的连续性保证。于是 $E\subset\bigcup_iJ_i$ 且 $\sum_i|J_i|\le\sum_i|B_i|+\varepsilon$，故 $m_o^*(E)\le m_c^*(E)+\varepsilon$。令 $\varepsilon\downarrow0$，得两种定义相同；若相应下确界为无穷，按上述不等式直接处理。
>
> 更一般地，只要两类基本覆盖对象能按原稿所示方式互相覆盖，并把总体积误差分配成 $\varepsilon2^{-i}$，就能以同一比较论证证明定义相同。'''])
u('外测度性质标题与空集性质',[120,2950,770,3215],r'''### 外测度性质

（1）$m^*(\varnothing)=0$。''')
u('外测度单调性',[190,3205,1365,3375],r'''（2）$E\subset F\ \Rightarrow\ m^*(E)\le m^*(F)$。''')
p={'page':3,'title':'覆盖族、外测度定义及其初步性质','anchor':'outer-measure-definition','units':U,
'layout':'上部继续覆盖存在性的 Lindelöf 备选路线和覆盖族基数；中央定义外测度；其后 Remark 允许空项及更换覆盖形状，三行证明提示；底部开始列外测度性质。定义公式与第一页顶行横跨两栏。',
'observation':'全页和六区均实际查看，并对 Lindelöf 行与 Remark(2) 生成有坐标局部图后实际查看。确认开长方体族、序列的连续统基数、inf 的可列体积和、空项允许、外测度空集及单调性。Remark(2)形状字迹仍暂列 Q002，相关证明以候选版本蓝色补全。',
'regions':[
'首为“或 R^n 是 Lindelöf，有遗传性”，末为 I^N=c^N=(2^{aleph0})^{aleph0}=c；核对覆盖族记号及全体开区间。上部行和端点编码跨右区，页顶普通留白。',
'首为 Lindelöf 行后半“相应区间放大，来证明”，末为基数等式的 c；核对端点乘积与 c^N，右侧无额外注记。',
'首为基数式下部，末为 Remark(2)开头；确认由(1)选覆盖、m*:2^{R^n}定义域、可覆盖提示及 I_n可为空。定义的下确界求和在右区。',
'首为基数 c 的尾部，末为 Remark(2)的 proof；正文核对值域[0,∞]、inf Σ_{k=1}∞|I_k|、覆盖族条件。大片留白无内容。',
'首为 Remark(1)尾部，末为单调性 m*(E)≤m*(F)；核对替代覆盖的 epsilon、I⊂并B_i 和体积和<|I|+epsilon。底部从此开始外测度性质，接下页。',
'首为 Remark(2)的“可证明 proof”，末为单调式右端 m*(F)；其余为普通空白。左区公式的右尾皆完整，未漏条件。'],
'issues':[{'id':'RA07-Q002','status':'open','description':'物理第3页 Remark(2)“I_n是否可为…”后覆盖对象的字形不够明确，候选为闭矩形；需第二遍独立视觉确认。','related_ids':['RA07-P003-U009','T-P003-009','N-P003-009'],'evidence_ids':['image:p0003','image:p0003-r3c1','image:p0003-r3c2','artifact:p0003-rectangle'],'resolution':'保存原片段与局部图。保留原三行证明提示；学习稿把闭长方体候选的完整证明明确标为补证，不冒充原问题唯一读法。'}]}
(P/'p003.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
