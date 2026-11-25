import json
from pathlib import Path
P=Path(__file__).parent;U=[]
def u(label,bbox,t,supp=None,ev=None,study=None):
 d={'label':label,'bbox':bbox,'transcript':t}
 if supp:d['supplements']=supp
 if ev:d['extra_evidence']=ev
 if study is not None:d['study']=study
 U.append(d)
u('矩形测试等价定理',[145,470,2000,775],r'''**Th.**
$$E\in\mathcal M\iff m^*(I)=m^*(I\cap E)+m^*(I\cap E^c),$$
$\forall I\subset\mathbb R$ 区间（矩形）。''',supp=[r'''> [!info] 补充：定理的精确范围
> 在 $\mathbb R^n$ 中，只对所有有界开矩形（开长方体）$I=\prod_{j=1}^n(a_j,b_j)$ 检查分割等式，就足以推出对任意测试集 $T\subset\mathbb R^n$ 的 Carathéodory 条件。原稿在条件行写 $\mathbb R$，并附“矩形”；以下覆盖证明对任意维数 $n$ 同样适用。必要性直接来自定义。'''])
u('左缘独立残留公式',[0,565,145,725],r'〔左边缘另有被裁切的公式尾段，能读出 $E^c)$；没有足够图像恢复其前项。〕')
u('必要性显然',[130,815,710,1020],r'**pf.** $\Rightarrow$：显然。')
u('由次可加性归约反向不等式',[330,970,1875,1245],r'''$\Leftarrow$：由外测度次可加性，仅证
$$m^*(T)\ge m^*(T\cap E)+m^*(T\cap E^c).$$''',supp=[r'''> [!info] 补证：固定任意测试集
> 任取 $T\subset\mathbb R^n$。因为 $T=(T\cap E)\cup(T\cap E^c)$，次可加性已给出 $m^*(T)\le m^*(T\cap E)+m^*(T\cap E^c)$；所以下面只需得到相反方向，不能把 $T$ 预先假设为矩形。'''])
u('无限外测度分支',[105,1320,1010,1490],r'（1）若 $m^*(T)=+\infty$，成立。',supp=[r'''> [!info] 补充：扩展实数的这一分支
> 当 $m^*(T)=+\infty$ 时，所需“$\ge$”自动成立；已有的“$\le$”又迫使右端也是 $+\infty$，因此得到等式。后面的取覆盖步骤是在 $m^*(T)<\infty$ 的分支中进行。'''])
u('有限分支的近最优覆盖',[105,1450,2195,1650],r'''（2）$\forall\varepsilon>0$，$\exists\{I_k\}\in LC(T)$，s.t.
$$\sum_{k=1}^{\infty}|I_k|<m^*(T)+\varepsilon.$$''')
u('与E相交的覆盖关系',[160,1660,900,1880],r'$$T\cap E\subset\bigcup_{k=1}^{\infty}(E\cap I_k).$$')
u('与补集相交的覆盖关系',[160,1930,1040,2140],r'$$T\cap E^c\subset\bigcup_{k=1}^{\infty}(E^c\cap I_k).$$')
u('第一部分单调次可加及有限性',[150,2190,2020,2410],r'''$$m^*(T\cap E)\le m^*\left(\bigcup_{k=1}^{\infty}(E\cap I_k)\right)
\le\sum_{k=1}^{\infty}m^*(E\cap I_k)<+\infty.$$''',supp=[r'''> [!info] 补证：最后一个严格界与补集对应式
> 每个 $E\cap I_k\subset I_k$，所以 $\sum_km^*(E\cap I_k)\le\sum_km^*(I_k)=\sum_k|I_k|<m^*(T)+\varepsilon<\infty$。同样，$m^*(T\cap E^c)\le\sum_km^*(E^c\cap I_k)<\infty$。这里使用了上一节“矩形的外测度等于体积”，没有先用待证的可测性。'''])
u('两部分估计相加',[140,2440,2445,2675],r'''$$m^*(T\cap E)+m^*(T\cap E^c)
\le\sum_{k=1}^{\infty}m^*(E\cap I_k)+\sum_{k=1}^{\infty}m^*(E^c\cap I_k).$$''')
u('由题设逐项合并及覆盖估计',[1090,2670,2480,2885],r'''（“题设”标在下一等号处。）
$$=\sum_{k=1}^{\infty}m^*(I_k)=\sum_{k=1}^{\infty}|I_k|<m^*(T)+\varepsilon.$$''',supp=[r'''> [!info] 补证：等号为何合法
> 非负级数可逐项相加，故两串和合成 $\sum_k[m^*(E\cap I_k)+m^*(E^c\cap I_k)]$。每个 $I_k$ 是题设允许检验的矩形，方括号内恰等于 $m^*(I_k)$。再用矩形体积定理与近最优覆盖估计，即得所需的 $\varepsilon$ 上界。'''])
u('令误差趋零完成证明',[155,2840,520,2975],r'$\varepsilon\to0^+$。',supp=[r'''> [!info] 补证：收尾
> 左端 $m^*(T\cap E)+m^*(T\cap E^c)$ 与 $\varepsilon$ 无关；对每个 $\varepsilon>0$ 它都不超过 $m^*(T)+\varepsilon$，故令 $\varepsilon\downarrow0$ 得到反向不等式。与次可加性合并，任意 $T$ 都满足分割等式，所以 $E\in\mathcal M$。'''])
u('跨内外子集的加性刻画',[105,3075,1740,3380],r'''**Th.** $E\in\mathcal M\iff\forall A\subset E$，且 $B\subset E^c$，有
$$m^*(A\cup B)=m^*(A)+m^*(B).$$''',supp=[r'''> [!info] 补证：与定义双向等价
> 若 $E$ 可测，取测试集 $T=A\cup B$；由于 $A\subset E$、$B\subset E^c$，有 $T\cap E=A$、$T\cap E^c=B$，即得等式。反之，对任意 $T$ 取 $A=T\cap E$、$B=T\cap E^c$，题设恰给出 Carathéodory 等式。本页原稿只列定理，故此处将两步直接补全。'''])
p={'page':7,'title':'矩形测试判据与跨内外加性','anchor':'rectangle-test','units':U,
'layout':'顶部矩形测试等价定理，左页缘另有Ec)尾段；中部至下部完整证明，以无限外测度与有限外测度分支展开，两个覆盖式及两次级数估计跨左右分区；最下另起跨内外子集加性的等价定理。上方留白宽，页末定理下有普通空白。',
'observation':'已先看整页，再实际看六个高清区域（因前次批量输出超长，重新以三图一批看完六区）。矩形题设逐项合并、题设标在等号处、eps→0+均核对。保留左缘Ec)孤立尾段与顶部R没有n的写法，学习稿标明n维版本。',
'regions':[
'首为Th E∈M，末为仅证m*(T)反向不等式左部。看到∀I⊂R 区间(矩形)、pf⇒显然和⇐由外测度次可加性；左缘Ec)尾段独立，无前文可补。上部大块留白。',
'首为顶端分割等式右半m*(I∩E)+m*(I∩Ec)，末为目标反向式的补集项；中段右侧空白。核对两处补集c均在E上方。',
'首为目标不等式左半，末为m*(T∩E)≤外测度并集≤求和。中部依次为m*(T)=∞分支、∀eps取LC(T)、T∩E与T∩Ec两个包含式；包含不是等号。',
'首为反向式末项，末为Σm*(E∩Ik)<∞；中部看到近最优覆盖Σ|Ik|<m*(T)+eps，右侧余白。核对严格小于号及∞。',
'首为前式跨区残段，末为新Th的m*(A∪B)=m*(A)+…左半。两和估计下方有“题设”并指等号，随后eps→0+；没有写第二定理证明。',
'首为Σm*(E∩Ik)<∞尾部，末为新定理B⊂Ec与m*(B)。核对两和合成Σm*(Ik)=Σ|Ik|<m*(T)+eps，所有k从1至∞；页底普通留白。']}
(P/'p007.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
