import json
from pathlib import Path
P=Path(__file__).parent
p=json.loads((P/'pages/p001.json').read_text());u=p['units'][12]
u['transcript']=r'''无穷维，不存在〔疑字 RA07-Q001：量词样符号近似“$\wedge m$”〕平移正规性、非平凡测度，？（右端有蓝色圈问号。）'''
u['study']=r'''原稿问题：“无穷维，不存在〔疑字 RA07-Q001：量词样符号〕平移正规性、非平凡测度，？”

<span style="color:red">原稿明确留问号，未在此处作答。</span>'''
u['supplements'].insert(0,r'''> [!info] 补充与补证：无限维空间中的平移测度（协调编辑补充，作者核验）
> 原稿句首经回图比较更接近“无穷维”；中间量词样符号尚未唯一恢复。下面明确给出一个适用范围，不把补入前提冒充原字迹：**无限维可分赋范空间上，非零、平移不变的 Borel 测度不可能局部有限。**
>
> 先证明所需的 Riesz 引理：若 $Y$ 是赋范空间中的真闭线性子空间，$0<\theta<1$，取 $z\notin Y$，令 $d=d(z,Y)>0$；由距离下确界定义，选 $y_0\in Y$ 使 $\|z-y_0\|<d/\theta$。则单位向量 $u=(z-y_0)/\|z-y_0\|$ 满足 $d(u,Y)=d/\|z-y_0\|>\theta$。
>
> 假设这样的测度 $\mu$ 局部有限。取 $R>0$ 使 $\mu(B(0,R))<\infty$。有限维线性子空间是闭的，逐次对已选向量的线性包应用 Riesz 引理（$\theta=1/2$），得到两两距离大于 $1/2$ 的单位向量列 $u_k$。令 $x_k=(R/2)u_k$，则 $B(x_k,R/8)$ 两两不相交，并全在 $B(0,R)$ 内。由平移不变性，每个小球测度同为 $c=\mu(B(0,R/8))$；故任意 $N$ 都有 $Nc\le\mu(B(0,R))<\infty$，从而 $c=0$。可分性保证全空间能由可列个半径 $R/8$ 的球覆盖，于是 $\mu(X)=0$，矛盾。
>
> 命题范围已由 [USC 大学讲义《Wiener Measure》](https://dornsife.usc.edu/sergey-lototsky/wp-content/uploads/sites/211/2023/06/Week8-ByDiogo.pdf) 中的无限维说明核验；上面的固定半径详证由协调编辑提供并在本稿核算。仅“平移不变、非平凡”仍允许计数测度，局部有限性不能省略。''')
u['supplements'][1]=u['supplements'][1].replace('下面给出可独立验证的相关命题，不把它认作疑字的唯一逐字恢复。','下面是另一个可独立验证的相关命题，讨论有限维实直线的全幂集；它不是前面无限维原问题的答案，也不是其逐字恢复。')
u['extra_evidence'].append('artifact:ra07-q001-root')
p['issues'][0]['description']='物理第1页问题句首经作者回图与/root局部复读更接近无穷维；其后量词样符号仍不能唯一恢复。可读词为不存在、平移、正规性、非平凡测度及圈问号。'
p['issues'][0]['resolution']='已撤销把全幂集问题当作黑色原题的推断；原位分别给无限维可分赋范空间命题及独立的有限维Vitali相关例，均蓝色标明补充。中间字迹保留Q001待第二遍复核。'
p['observation']+=' 随后收到/root的实际局部复读，作者再次实际查看p0001-question.png，句首改读为无穷维；中间量词仍未决。'
(P/'pages/p001.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
(P/'extra-evidence.json').write_text(json.dumps([{'id':'ra07-q001-root','path':'evidence/ra07-q001-root.md','kind':'evidence','format':'text'}],ensure_ascii=False,indent=2)+'\n')
(P/'participants.json').write_text(json.dumps([{'agent_id':'/root/ra07_rebuild','session_id':'/root/ra07_rebuild','role':'REBUILD','scope':'整份13页作者首遍，按实际完成页记录','context':'根任务完整合同；无旧稿'},{'agent_id':'/root','session_id':'/root','role':'COORDINATOR_LOCAL_READ_AND_SUPPLEMENT','scope':'p0001全页与p0001-question局部复读；Q001无限维命题补证','independent_second_or_final_review':False,'evidence':'evidence/ra07-q001-root.md'}],ensure_ascii=False,indent=2)+'\n')
