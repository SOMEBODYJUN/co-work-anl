# One-time authoring history; use build.py to regenerate from the final page-data files.
import json
from pathlib import Path
base=Path(__file__).resolve().parent/'page-data'
def save(n,d):
 p=base/f'p{n:03d}.json';tmp=p.with_suffix('.json.tmp');tmp.write_text(json.dumps(d,ensure_ascii=False,indent=2).rstrip()+'\n');tmp.replace(p)
def t(i,txt,src=(),origin='source',explanation='按本页原图保留本单元。',**kw):
 return dict(id=i,text=txt,source_ids=list(src),origin=origin,explanation=explanation,status='resolved',**kw)
s=[dict(id='RA09-P011-U001',bbox_px=[270,310,1235,545],label='连续性的原拓扑包含式及R/E下标',status='resolved',extra_evidence_ids=['artifact:crop-p0011-subscript']),dict(id='RA09-P011-U002',bbox_px=[225,565,875,750],label='只证逆像开集族包含于逆像可测族',status='resolved')]
a=[t('T-P011-H','## 物理第 11 页',origin='editorial',explanation='物理页标签。'),t('N-P011-H','## 11. 连续蕴含可测：保留原稿的第二条证明路线',origin='editorial',explanation='把本页的拓扑路线接到前页连续函数定理之后，保留与水平集证明不同的原稿路线。')]
for prefix in ['T','N']:
 a.append(t(prefix+'-P011-U001',r'$f$ 连续 $\Longleftrightarrow\tau_{\mathbb R/E}\subset\tau_f$。'+'\n\n〔原稿下标写作 $R/E$，中间为斜线状分隔笔画。〕',['RA09-P011-U001']))
a.append(t('N-P011-S01',r'''> [!info] 纠错：区分定义域拓扑与值域拓扑
> 延续前页 $f:E\to\mathbb R$、$E\in\mathcal M(\mathbb R^n)$ 的条件，令 $\tau_E=\{E\cap U:U\subset\mathbb R^n\text{ 开}\}$ 为定义域的相对拓扑，$\tau_{\mathbb R}$ 为值域的通常拓扑，并令
> $$\tau_f=\{B\subset\mathbb R:f^{-1}(B)\in\tau_E\},\qquad\Sigma_f=\{B\subset\mathbb R:f^{-1}(B)\in\Sigma_E\}.$$
> 此时连续性的正确判据是 $f\text{ 连续}\Longleftrightarrow\tau_{\mathbb R}\subset\tau_f$。左边必须是值域 $\mathbb R$ 的拓扑。若原稿 $\tau_{\mathbb R/E}$ 意在表示 $E$ 上的相对拓扑，它就不能放在这个包含式的左侧：$\tau_E$ 的元素是 $E$ 的子集，而 $\tau_f$ 的元素是 $\mathbb R$ 的子集。原稿没有解释该下标，故保留原写法，并用上面的明确定义完成论证。''',['RA09-P011-U001','RA09-P010-U010','RA09-P010-U012','RA09-P010-U013'],origin='supplement',explanation='新增原下标的类型辨析和严格连续性判据；不把纠正后的下标冒充原字迹。'))
for prefix in ['T','N']:
 a.append(t(prefix+'-P011-U002',r'只证 $\tau_f\subset\Sigma_f$。'+'\n\n<span style="color:red">原稿待证：此句之后未写推导；下一物理页为空白。</span>',['RA09-P011-U002']))
a.append(t('N-P011-S02',r'''> [!info] 补充证明：沿原稿的拓扑包含路线逐步完成
> **第一步，定义域的相对开集可测。** 任取 $V\in\tau_E$，有开集 $U\subset\mathbb R^n$ 使 $V=E\cap U$。开集是 Borel 集，从而 Lebesgue 可测；$E$ 也可测，所以 $V\in\mathcal M$ 且 $V\subset E$。由前述迹 $\sigma$ 代数的表达式，$V\in\Sigma_E$。因此 $\tau_E\subset\Sigma_E$。
>
> **第二步，证明原稿留下的包含式。** 任取 $B\in\tau_f$，由定义 $f^{-1}(B)\in\tau_E$，再由第一步 $f^{-1}(B)\in\Sigma_E$，故 $B\in\Sigma_f$。这就证明了 $\tau_f\subset\Sigma_f$。此步只使用定义域的可测性，无须先假定 $f$ 连续。
>
> **第三步，使用连续性。** 对每个值域开集 $U\in\tau_{\mathbb R}$，连续性给出 $f^{-1}(U)\in\tau_E$，即 $\tau_{\mathbb R}\subset\tau_f$。与第二步合并，得 $\tau_{\mathbb R}\subset\Sigma_f$。
>
> **第四步，从开集推进到 Borel 集。** 前文已证明 $\Sigma_f$ 是 $\mathbb R$ 上的 $\sigma$ 代数；它包含所有开集，故按生成 $\sigma$ 代数的最小性，$\mathcal B(\mathbb R)=\sigma(\tau_{\mathbb R})\subset\Sigma_f$。于是每个 Borel 集 $B\subset\mathbb R$ 的原像 $f^{-1}(B)$ 都在 $\Sigma_E$ 中。
>
> **第五步，回到本课的水平集定义。** 对任意有限实数 $a$，$(a,+\infty)$ 是 $\mathbb R$ 中的 Borel 集，故 $E[f>a]=f^{-1}((a,+\infty))\in\Sigma_E\subset\mathcal M$。因此 $f\in\operatorname{MF}(E)$。这是原稿所提示的“拓扑包含—生成 $\sigma$ 代数”路线；前页直接验证水平集的路线也完整保留。''',['RA09-P011-U002','RA09-P011-U001','RA09-P010-U010','RA09-P010-U011'],origin='supplement',explanation='新增原稿只写目标而未展开的五步证明；条件、逆像族和生成族工具均先行说明。'))
save(11,dict(page_id='p0011',source_units=s,target_units=a,layout_observation='整页仅左上方两行黑色手写。第一行f连续的等价式从x约270延至1235，下标R/E位于等价式中部；第二行只证τ_f⊂Σ_f在其下。上缘约300像素、右侧大部及750像素以下全为空白。由前页底端Σ_f、τ_f引入本页；下一页空白，没有后续推导。',page_observation='实际先看全页，识得f连续⇔τ_{R/E}⊂τ_f及只证τ_f⊂Σ_f两行；随后六区检查与下标裁图确认斜线状分隔及R、E字形，未将其默改成τ_R。源单元为两个独立数学句；下方普通留白未虚构成内容单元。',region_observations=['本区先有上部约300像素留白；首行是f连续⇔τ_{R/E}⊂τ_f，末行是只证τ_f⊂Σ_f。下标R/E有清楚斜线，第二式左τ右Σ；约750以下留白。两行均在此区，首行最右的f与右区重叠。','本区左边缘约y320—500可见第一行τ_f中的f尾部及句点，接左区的连续性等价式；其余从上缘、右侧到下缘为空白，没有旁注或新公式。','整个中左区实际观察为空白；上缘已低于上一行文字终点，没有上一行延伸、淡字或证明续行。','整个中右区实际观察为空白，没有首末文字、符号或旁注；与中左区的白色区域连续。','整个下左区实际观察为空白，未见书写、页码、待填标记或接续箭头。','整个下右区实际观察为空白，右下角没有页码或续页提示；本页最后可读内容仍在左上两行。'],crops=[dict(id='crop-p0011-subscript',path='crops/p0011-subscript.png',page_id='p0011',bbox_px=[860,310,1100,550])],issues=[dict(id='RA09-C011',status='resolved',description='原连续判据的左侧拓扑下标写作R/E，若读作定义域的相对拓扑，则与τ_f所含值域子集类型不合；原稿未释此记号。',related_ids=['RA09-P011-U001','N-P011-S01'],evidence_ids=['image:p0011','image:p0011-r1c1','artifact:crop-p0011-subscript'],resolution='黑色正文原样保留下标R/E；蓝色辨析明确τ_E、τ_R、τ_f的所属集合，并把正确判据及完整证明独立列出。不将原记号含义确认为作者原意。')],recoveries=[]))
save(12,dict(page_id='p0012',assessment='blank',source_units=[],target_units=[t('T-P012-H','## 物理第 12 页\n\n〔本页为空白页，无可读文字、公式或图形。〕',origin='editorial',explanation='首遍实际全页及六区观察后的空白页说明，不虚构原稿单元。'),t('N-P012-H','## 12. 原件终页\n\n〔物理第 12 页为空白页。上一节已保留第 11 页的最后两行及其补充证明。〕',origin='editorial',explanation='记录原件终页为空白并说明前页的内容接续，不将留白标为原稿习题。')],layout_observation='整张白页，四角、边缘、中央均无可读笔迹；没有页码、图形、栏线或待填标记。前页两行之后没有此页续证。',page_observation='实际先看2480×3509整页图，再依次看六张高清重叠区域。全页与各区域均为空白，未见淡笔、边注或公式残端；按物理页保留空白说明，不建立虚假的整页内容单元。',region_observations=['上左区完全空白，左上角及下方没有首末字迹、公式或图形。','上右区完全空白，右上角及与左区重叠带没有笔迹、页码或标题。','中左区完全空白，未见上一行接续或淡色文字。','中右区完全空白，与中左区及上下重叠带均为普通留白。','下左区完全空白，无页码、待填标记、图形或收尾笔画。','下右区完全空白，含右下角及底边，无署名、页码或接续提示。'],crops=[],issues=[],recoveries=[]))
