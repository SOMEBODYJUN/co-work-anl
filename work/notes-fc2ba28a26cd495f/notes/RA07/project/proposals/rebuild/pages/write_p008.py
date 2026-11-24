import json
from pathlib import Path
P=Path(__file__).parent;U=[]
def u(label,bbox,t,supp=None,study=None):
 d={'label':label,'bbox':bbox,'transcript':t}
 if supp:d['supplements']=supp
 if study is not None:d['study']=study
 U.append(d)
u('承接加性判据的正向证明取测试集',[145,315,1065,505],r'$\Rightarrow$：令 $T=A\cup B$，则')
u('正向证明的第一交集',[355,590,770,720],r'$$T\cap E=A.$$')
u('正向证明的第二交集',[355,805,810,960],r'$$T\cap E^c=B.$$')
u('正向证明调用可测性',[235,945,1800,1125],r'因 $E\in\mathcal M$，$m^*(T)=m^*(A)+m^*(B)$。')
u('反向证明任取测试集',[130,1155,860,1340],r'$\Leftarrow$：任取 $T\subset\mathbb R^n$。')
u('反向证明的两子集选择',[155,1325,1235,1485],r'令 $A=T\cap E$，$B=T\cap E^c$。',supp=[r'''> [!info] 补证：原稿省略的最后代回
> 两集合满足 $A\subset E$、$B\subset E^c$，且 $A\cup B=T$。把它们代入前页所列的加性条件，得到 $m^*(T)=m^*(T\cap E)+m^*(T\cap E^c)$。由于 $T$ 任意，$E$ 可测。本页是前页定理的原稿证明，虽与编者前附的解释相同，仍按原有路线完整保留。'''])
u('不交并不必外测度可加的注意',[150,1540,2185,2000],r'''注意：$A\cap B=\varnothing$，
$$m^*(A\cup B)\ne m^*(A)+m^*(B),$$
$A,B$ 可测成立。''',supp=[r'''> [!info] 纠错：原稿的不等号表示“不保证等号”
> 不能把此处 $\ne$ 理解为“任意两个不交集合都严格不等”；例如 $A=\varnothing$ 时必相等。准确说法是：仅知 $A\cap B=\varnothing$，不能推出外测度可加；若 $A,B$ 可测则等号成立。实际上只要其中一个可测，取 $T=A\cup B$ 使用它的 Carathéodory 条件就足够。
>
> 若存在不可测集 $E$，按定义存在测试集 $T$ 使分割等式失败。令 $A=T\cap E$、$B=T\cap E^c$，它们不交，而次可加性结合“不相等”给出 $m^*(A\cup B)<m^*(A)+m^*(B)$，这说明条件不能省掉。'''])
u('正距离保证外测度可加',[215,2060,1620,2245],r'若 $d(A,B)>0$，则上式成立。',supp=[r'''> [!info] 补充：此处“上式成立”指等号成立
> 对 $d(A,B)=\inf\{|a-b|:a\in A,b\in B\}>0$，结论是
> $$m^*(A\cup B)=m^*(A)+m^*(B).$$
> 这是 Lebesgue 外测度的度量可加性，$A,B$ 均不必可测。原稿上一行写了 $\ne$，这里按上下文恢复成欲说明的加性结论，纠正单独标出。''',r'''> [!info] 补证：小直径覆盖给出度量可加性
> 设 $\delta=d(A,B)>0$。若 $m^*(A\cup B)=\infty$，次可加性已迫使两外测度的和为 $\infty$，等式成立。以下设有限。给定 $\varepsilon>0$，取 $A\cup B$ 的开矩形覆盖，其体积和小于 $m^*(A\cup B)+\varepsilon/2$。
>
> 可将覆盖中的第 $k$ 个有界矩形细分成有限个直径小于 $\delta/2$ 的闭小矩形；这些小矩形总体积等于原矩形体积，再各自微量放大成直径小于 $\delta$ 的开矩形，使第 $k$ 组新增总体积小于 $\varepsilon/2^{k+1}$。这样得到全部直径小于 $\delta$、总体积小于 $m^*(A\cup B)+\varepsilon$ 的可数开覆盖。
>
> 每个小矩形不可能同时碰到 $A$ 与 $B$，否则其中两点距离小于 $\delta$。把相交于 $A$ 的矩形和相交于 $B$ 的矩形分为互不重叠的两组，分别覆盖 $A,B$；完全不相交的矩形可弃去。因此
> $$m^*(A)+m^*(B)\le\sum_{I\text{ 属于两组}}|I|<m^*(A\cup B)+\varepsilon.$$
> 令 $\varepsilon\downarrow0$，再结合次可加性，等式得证。这里分的是覆盖的指标组，并未假定覆盖矩形彼此不交。'''])
u('不交闭集与紧集距离正',[160,2310,1880,2515],r'$$A\cap B=\varnothing\quad(A\text{ 闭，}\ B\text{ 紧})\ \Rightarrow\ d(A,B)>0.$$')
u('原稿独立Proof标题及随后留白',[150,2565,435,2745],r'''**Proof：**

〔本页该标题以下未写推导，余下大段为空白。〕''',supp=[r'''> [!info] 补证：闭集与紧集的正距离
> 若其中一个集合为空，按 $\inf\varnothing=\infty$ 结论成立。否则，对每个 $b\in B$，因为 $A$ 闭且 $b\notin A$，存在 $r_b>0$ 使 $B(b,r_b)\cap A=\varnothing$，故 $d(b,A)>0$。函数 $b\mapsto d(b,A)$ 为 $1$-Lipschitz：由三角不等式有 $d(b,A)\le|b-b'|+d(b',A)$，交换 $b,b'$ 即得绝对值估计。它在非空紧集 $B$ 上取得最小值；取得该值的点也不在 $A$，故最小值严格正，即 $d(A,B)>0$。
>
> 紧性不可随意去掉：$A=\{n:n\ge1\}$ 与 $B=\{n+1/(n+1):n\ge1\}$ 都是 $\mathbb R$ 中的闭集且不交，但两者距离为 $0$。'''])
p={'page':8,'title':'加性判据原证明与正距离加性','anchor':'distance-additivity','units':U,
'layout':'上半承接前页末定理，依次写正向取T=A∪B、两交集及测度式，反向任取T并令A、B为切片；中下部是注意、不交外测度不必可加、正距离加性、闭集与紧集正距离。最后Proof标题后大块空白。',
'observation':'已按整页后六高清区逐一阅读。注意行明确写不等号，后文却说上式成立，故保留原符号并蓝色校正其语义；闭、紧两个条件与d(A,B)>0核对。Proof后本页没有笔迹，不把空白当作已完成原证明。',
'regions':[
'首为⇒令T=(A∪B)则，末为因E∈M及m*(T)式左部；核对T∩E=A、T∩Ec=B。上缘普通空白较宽。',
'只有下部正向证明的m*(A)+m*(B)右半，其余右上区域空白；与左区完整拼接，未遗漏旁注。',
'首为⇐任取T⊂Rn，末为A∩B=∅(A闭,B紧)开头。看到A=T∩E、B=T∩Ec、不等号注意、d(A,B)>0。',
'首为B=T∩Ec的c边缘，末为闭紧条件的推出d(A,B)>0；中间A,B可测成立与“上式成立”均清晰，确认后者所指加性等号需说明。',
'首为不交闭紧集合条件，末为Proof标题。标题以下至页末为大块普通白纸，没有原写的推导、答案或图形。',
'仅顶端有⇒d(A,B)>0的公式尾部，余下到页末全白；与左区共同确认Proof后无正文。']}
(P/'p008.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
