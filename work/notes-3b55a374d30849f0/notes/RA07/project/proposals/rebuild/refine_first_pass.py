from pathlib import Path
import json
P=Path(__file__).parent/'pages'
def read(n): return json.loads((P/f'p{n:03d}.json').read_text())
def save(n,d):
 q=P/f'p{n:03d}.json';temp=q.with_suffix('.json.tmp');temp.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temp.replace(q)
p1=read(1);p1['units'][12]['label']='无穷维平移测度的问句与圈问号'
s=p1['units'][12]['supplements'][0]
s=s.replace('则 $B(x_k,R/8)$ 两两不相交，并全在 $B(0,R)$ 内。','则 $\\|x_k-x_l\\|>R/4=2(R/8)$（$k\\ne l$），故 $B(x_k,R/8)$ 两两不相交；其中每个点的范数小于 $R/2+R/8=5R/8<R$，所以这些球全在 $B(0,R)$ 内。')
p1['units'][12]['supplements'][0]=s
p1['units'][12]['supplements'][1]=p1['units'][12]['supplements'][1].replace('且 $m((-1,2))\\le3$ 矛盾。','且 $m((-1,2))\\le3$ 矛盾。这里 $(-1,2)\\subset[-1,0)\\cup[0,1)\\cup[1,2)$，三个半开单位区间都是 $[0,1)$ 的平移，故测度总和为 $3$。')
save(1,p1)
p3=read(3)
p3['units'][8]['study']=p3['units'][8]['transcript']+'\n\n<span style="color:red">〔原稿提出覆盖对象是否可以替换的问题，所写 Proof 仅有下方起步条件，未完成结论。〕</span>'
save(3,p3)
p5=read(5)
p5['units'][3]['supplements']=[r'''> [!info] 补证：本节先备的开集、闭集可测性
> 先用矩形测试判据证明半空间 $H=\{x:x_j<a\}$ 可测：任意有界开矩形 $J$ 被超平面 $x_j=a$ 切成两个矩形（允许空或退化），两部分的外测度等于其体积，而体积之和是 $|J|$。所以 $H$ 满足矩形测试条件。闭半空间为其补，亦可测。
>
> 有界开矩形是有限个开半空间的交，故可测。每个开集 $G\subset\mathbb R^n$ 都等于包含于它的有理端点开矩形之并：对 $x\in G$ 先取小球包含于 $G$，再在球内围绕 $x$ 选有理端点矩形；全部有理端点矩形只有可数个。因此开集可测，闭集作为开集的补也可测，特别地紧集可测。这些结论只用前面已证的矩形外测度公式、矩形判据与可数并交封闭。''']
p5['units'][4]['supplements']=[r'''> [!info] 补证：外测度的开集外逼近
> 对任意 $S\subset\mathbb R^n$，有
> $$m^*(S)=\inf\{m(G):S\subset G,\ G\text{ 开}\}.$$
> 单调性给出左端不超过每个候选 $m(G)$。若 $m^*(S)<\infty$，取开矩形覆盖使总体积小于 $m^*(S)+\varepsilon$，令 $G$ 为这些矩形的并，则 $S\subset G$，且 $G$ 开、可测，$m(G)\le\sum_k|I_k|<m^*(S)+\varepsilon$。令 $\varepsilon\downarrow0$ 得反向。若 $m^*(S)=\infty$，每个含它的开集也有无限测度，公式仍成立。
>
> 因而原稿这里的 $G$ 不仅可以取开覆盖，也可使其测度尽量接近 $m^*(I\setminus E)$。''']
p5['units'][7]['supplements']=[r'''> [!info] 补证：内测度等于紧集内逼近，因而与外框无关
> 设 $E$ 有界，固定闭长方体 $I\supset E$。定义式中的两项有限，且 $0\le m^*(I\setminus E)\le|I|$。我们证明
> $$m_*(E)=\sup\{m(K):K\subset E,\ K\text{ 紧}\}.$$
> 若 $K\subset E$ 紧，则 $I\setminus E\subset I\setminus K$，单调性及有限差公式给 $m^*(I\setminus E)\le |I|-m(K)$，故 $m(K)\le m_*(E)$。
>
> 反向，给定 $\varepsilon>0$，按开集外逼近取 $G\supset I\setminus E$，使 $m(G)<m^*(I\setminus E)+\varepsilon$。则 $K=I\setminus G$ 是 $E$ 中紧集，且
> $$m(K)=|I|-m(I\cap G)\ge |I|-m(G)>m_*(E)-\varepsilon.$$
> 因而上确界不小于 $m_*(E)$，公式得证。右侧不提外框 $I$，所以定义与所选包含 $E$ 的闭长方体无关。又由各 $K\subset E$ 的单调性，$m_*(E)\le m^*(E)$。''']
p5['units'][8]['supplements']=[r'''> [!info] 补证：有界集合的内外测度判据与 Carathéodory 定义等价
> 若 $E$ 可测，则 $I\setminus E$ 也可测，有限可加性给 $|I|=m(E)+m(I\setminus E)$，所以 $m_*(E)=m(E)=m^*(E)$。
>
> 反之设 $m_*(E)=m^*(E)=s$，其中 $s<\infty$。由紧集内逼近，对每个 $j\ge1$ 取紧集 $K_j\subset E$，使 $m(K_j)>s-1/j$。令 $K=\bigcup_jK_j$，则 $K$ 可测且包含于 $E$。将任意 $K_j$ 的可测性用于测试集 $E$，有
> $$s=m^*(E)=m(K_j)+m^*(E\setminus K_j),$$
> 故 $m^*(E\setminus K)\le m^*(E\setminus K_j)<1/j$。令 $j\to\infty$，得到 $E\setminus K$ 零测，因完备性可测。于是 $E=K\cup(E\setminus K)$ 可测。取 $s=0$ 时同样成立，可取空紧集；没有遗漏零测情形。''']
p5['units'][13]['supplements'].append(r'''> [!info] 补证：局部判据的双向推导
> 若 $E$ 可测，则对每个有界闭长方体 $I$，交集 $E\cap I$ 可测。反之，若每个 $E\cap[-N,N]^n$ 可测，则
> $$E=\bigcup_{N=1}^{\infty}\bigl(E\cap[-N,N]^n\bigr)$$
> 是可数个可测集之并，故可测。因而原稿的无界局部描述与统一的 Carathéodory 定义一致。''')
save(5,p5)
# 自定义学习次序；每项为来源主体，所附蓝色单元紧随主体。
def seq(p,a,b):return [f'N-P{p:03d}-{i:03d}' for i in range(a,b+1)]
g=[]
def group(id,title,items):g.append({'id':id,'title':title,'anchor':id.lower(),'items':items})
group('N-SEC-01','一、测度公理与典型测度',seq(1,1,10))
group('N-SEC-02','二、基数记号与集合函数的数量',seq(9,10,13)+seq(1,11,12))
group('N-SEC-03','三、Jordan 内容、Darboux 判据与稠密有限覆盖',seq(1,14,16)+seq(2,1,7))
group('N-SEC-04','四、非负求和、Lebesgue 覆盖及两条存在性路线',seq(2,8,13)+seq(3,1,5))
group('N-SEC-05','五、Lebesgue 外测度及可列次可加性',seq(3,6,13)+seq(4,1,8))
group('N-SEC-06','六、矩形体积、可数点集与 Cantor 集',seq(5,1,2)+seq(4,9,13))
group('N-SEC-07','七、Carathéodory 可测性与切分图',seq(6,1,6))
group('N-SEC-08','八、矩形测试与跨内外加性：完整原证明',seq(7,1,13)+seq(8,1,7))
group('N-SEC-09','九、正距离加性与闭集、紧集的分离',seq(8,8,10))
group('N-SEC-10','十、可测族封闭运算：完整补证与原稿四块路线',seq(9,1,3)+seq(10,10,11)+seq(11,1,11))
group('N-SEC-11','十一、有限可加性与差集的有限性条件',seq(11,12,13)+seq(12,1,4))
group('N-SEC-12','十二、零测集、完备性与可测集合族的势',seq(9,4,9)+seq(9,14,15))
group('N-SEC-13','十三、内测度、开集外逼近与紧集内逼近',seq(5,4,14))
group('N-SEC-14','十四、不可测子集、并集问题与不可测集合族的势',seq(5,3,3)+seq(10,9,9)+seq(10,1,8))
group('N-SEC-15','十五、选择公理与 Solovay 模型旁注',seq(6,7,13))
group('N-SEC-16','十六、无穷维平移测度原问题及两个相关补证',seq(1,13,13))
group('N-SEC-17','十七、原件末页空白说明',['N-P013-BLANK'])
(P.parent/'study-order.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
