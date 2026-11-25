import json
from pathlib import Path
P=Path("/workspace/scratch/5eb228b78d49/co-work-anl-notes/work/notes-fc2ba28a26cd495f/notes/RA09/project")
ledger=json.loads((P/"ledger.json").read_text())
src=ledger["source_units"]
pages=[f"p{i:04d}" for i in range(1,13)]
regions=["r1c1","r1c2","r2c1","r2c2","r3c1","r3c2"]
page_obs={
"p0001":"第二遍逐式核对 Gδ/Fσ 定义、五项例示、距离函数开球交式与两条 Borel 命题；U005 实字为“补集”，当前两稿写“不一定”需高优先恢复。右下注记仍有未唯一字形。",
"p0002":"第二遍核对 Borel 基数、Cantor 非 Borel 子集、任意外测度反例及边界分解。外测度蓝证分开 μ*(T)=∞ 与有限两案；末尾完备化/局部逼近旁注仍有两串连笔未唯一恢复。",
"p0003":"第二遍核对有限/无限测度逼近、B_i 关系号、G_i 并集与取补收尾；回图支持 B_i 闭球写≤i，且并集公式下方两字为“即可”。",
"p0004":"第二遍核对 Gδ 外壳、原稿 Fδ 及重复 m(G\\E)=0 字面和蓝色 Fσ 订正；外/内正则定理与有界内外测度判据均有独立验证，(1) pf 后原留白真实存在。",
"p0005":"第二遍核对积分分层草式、逆像族及两组 σ 拓扑命题；积分单项确无求和号，第一组底空间字形为 f，蓝色将其说明为应为 X。",
"p0006":"第二遍核对可测映射定义、生成族判别和 R̄ 序拓扑入口；Σ_f 的中间疑字及全序旁注短字不能由标准理论唯一恢复，蓝色只补可验证公理与端点邻域。",
"p0007":"第二遍核对扩展 Borel 首式、等号后红色空白、[a,+∞] 两端方括号、四种半直线概称及 trace 代数；规范四族公式仅在蓝色补证。",
"p0008":"第二遍核对迹等价、两次 Th 起笔、E_f/Σ_f 记号、扩展值域生成族及蓝箭头图；D 原式两端为圆括号，蓝色订正含+∞右端点。",
"p0009":"第二遍核对四种可测组合、端点反例和有限区间生成族旁式；四组合链及两个中间反例独立成立，原式端点集合和不规范 σ(I) 简写均保留为来源。",
"p0010":"第二遍核对示性函数三段水平集和连续性两路线；原稿遗漏 a=0、1 已确认，孤立点旁注与结论行额外 M 字样保留并分层解释。",
"p0011":"第二遍核对 τ_{R/E} 下标和未完成证明；原下标斜线状真实存在，蓝色另定义 τ_R、τ_E 后补 τ_f⊂Σ_f，整页其余为空白。",
"p0012":"全页为空白；没有可登记的数学、文字、箭头、删线或待填对象。"
}
region_obs={
"p0001":[
"上左看见 Def、可数交/并两列和第1项开 Gδ、闭 Fσ；公式边界完整。",
"上右接续定义与第1项右端，未见额外删线或待填。",
"中左含第4、5项及“补集”语境的左半；右注与下方单点式相邻。",
"中右实际复核第5项旁注，疑字仍不能唯一定为某个拓扑术语。",
"下左见单点开球交、一般距离空间旁注及 U_n 距离写法。",
"下右见 F=∩U_n、箭头开集逆像及 Borel/严格包含命题的右端。"],
"p0002":[
"上左含开集最小σ代数、Borel基数上下界起句与 Cantor 集开头。",
"上右延续 Cantor 非Borel子集；未见独立删除或箭头。",
"中左含超限上界、Cantor 反证、Carathéodory 外测度断言及 Lebesgue 限制。",
"中右回看外测度断言右端和 Borel 测度说明，公式没有缩窄到Lebesgue外测度。",
"下左见 Borel 集上旁题、内部/边界分解和可测性等价。",
"下右为边界可测性行、完备化/局部逼近旁注及 Lemma 起句；旁注两处连笔未唯一。"],
"p0003":[
"上左见开集外逼近、闭集内逼近和蓝圈问号，层次顺序未变。",
"上右仅接两条逼近式右端，无越界笔画。",
"中左见有限测度覆盖、I_i 族、并集体积估计和无限分支起句。",
"中右见 B_i、E_i 及右侧(j>i)短注；B_i关系号回看支持≤。",
"下左见 G=∪G_i、差集包含链、下方“即可”及取补引理。",
"下右见跨页接续的差集末端与空白，未有额外证明段。"],
"p0004":[
"上左见 E∈M、Gδ外壳和第二项F下标原笔；原式右端重复G\\E。",
"上右接续两项零差公式，省略横划位置真实可见。",
"中左见外测度等价说明、方法说明、Th.(1)和开集下确界。",
"中右见闭集上确界、有界内外测度判据；数学补证未混入原黑字。",
"下左仅见(1)pf:后自然留白，红色待填边界清楚。",
"下右整区为空白，没有另造证明对象。"],
"p0005":[
"上左见边界零测推论、勒贝格积分标题、E[y_{i−1}≤f<y_i)草式及单项开头。",
"上右单项 f(ξ_i)m(E)右侧无求和号，下方逆像闭性文字接续。",
"中左见连续性基判别、f逆像交并补及命题起式。",
"中右见Σ_f定义和第一/第二σ拓扑性质，第一底空间字形仍像f。",
"下左见新拓扑前提、重复σ拓扑行和最大性起句。",
"下右见最大拓扑尾端，无额外图形或删除线。"],
"p0006":[
"上左见可测题头、定义映射和∀U逆像条件。",
"上右接续可测条件与生成族 D⊂Σ_Y，未见缺失关系号。",
"中左见生成族等价式、仅证←、Σ_f疑字和Σ_Y⊂Σ_f。",
"中右见疑字右侧σ代数收尾及Σ_Y变动未完旁注。",
"下左见R̄拓扑题头、开区间和半直线两项。",
"下右见全序旁注末端和线序拓扑，短字仍候选均可/同样。"],
"p0007":[
"上左见开集生成σ代数、B(O(R))首式、等号后空白和R→R̄箭头。",
"上右接续首式右端及(2)生成式左半，括号位置清楚。",
"中左见[ a,+∞ ]生成式、四种广半直线概称、同胚句和端点闭集。",
"中右见端点单点Borel结论与trace小标题起头。",
"下左见E⊂R^n、Lebesgue σ、Σ_E交集定义和trace名称。",
"下右见trace特例Σ_E={F∈M:F⊂E}，无额外续写。"],
"p0008":[
"上左见B⊂E承接、迹等价和可测函数定义。",
"上右见水平集严格大于条件和M_f(E)记号。",
"中左见第一次Th不充分起笔、第二次Th的E_f候选和结论。",
"中右见Σ_f包含B(R̄)、⇐/⇒证明提要和D生成族。",
"下左见D原式圆括号、D⊂B(R̄)、f:(R^n,Σ)映射及蓝箭头起点。",
"下右见蓝箭头指向B(R̄)以及B(R̄)⊂M(R̄)⊂Σ_f链。"],
"p0009":[
"上左见(M→B)Leb、(M→M)和四组合红色问题。",
"上右见有限层集条件及不推出箭头，未见箭头被擦除。",
"中左见σ(I)旁式、不可测E设定和±∞分段函数左侧。",
"中右见分段函数右侧及空层集反例。",
"下左见端点集合层集、E[f≥a]候选不等号和常值例起头。",
"下右见常值可测句尾，区域边界无额外反例。"],
"p0010":[
"上左见示性函数设定、1/0两分支、等价结论和proof。",
"上右见三段水平集原条件，0<a与a>1端点缺漏清楚。",
"中左见连续标题、孤立点旁注和f:E→R连续条件。",
"中右见E∈M(R^n)尾端及下一行结论左侧。",
"下左见结论行额外M字样、孤立Σ_f、τ_f两行和黑点。",
"下右仅见空白中的短斜笔，不能读成箭头或新公式。"],
"p0011":[
"上左唯一内容为连续等价式，R/E下标斜线状可见。",
"上右仅接等价式右端τ_f句点。",
"中左空白，无待填或箭头。",
"中右空白，无隐藏文字。",
"下左空白延伸至页底。",
"下右空白延伸至页底。"],
"p0012":[
"全区为空白，无内容单元。",
"全区为空白，无内容单元。",
"全区为空白，无内容单元。",
"全区为空白，无内容单元。",
"全区为空白，无内容单元。",
"全区为空白，无内容单元."]
}
# derive exact geometry/source IDs from ledger
source_by_page={p:[u for u in src if u["page_id"]==p] for p in pages}
pc_by_page={x["page_id"]:x for x in ledger["page_checks"] if x["pass"]==1}
page_checks=[]; region_checks=[]
for p in pages:
    us=source_by_page[p]
    ids=[u["id"] for u in us]
    unresolved=any(u.get("status")=="unresolved" for u in us)
    assessment="blank" if not us else ("unresolved" if unresolved else "content")
    ev=[f"image:{p}"]+[f"image:{p}-{r}" for r in regions]
    page_checks.append({
      "id":f"visual-second-p2-{p}","page_id":p,"pass":2,
      "reviewer_id":"/root/ra09_visual_second","session_id":"/root/ra09_visual_second",
      "assessment":assessment,"source_unit_ids":ids,"evidence_ids":ev,
      "observation":page_obs[p],
      "cross_region_unit_ids":pc_by_page[p]["cross_region_unit_ids"] if p in pc_by_page else [],
      "layout_observation":("空白页，六个重叠区均无内容。" if not us else "已按整页及六个重叠区核对；"+("含跨区公式、旁注或图形，" if any(len(u["region_ids"])>1 for u in us) else "内容集中在单一区，")+"边角未见漏写。")
    })
    for j,r in enumerate(regions):
      rid=f"{p}-{r}"
      ru=[u["id"] for u in us if rid in u["region_ids"]]
      rast="blank" if not ru else ("unresolved" if any(x.get("status")=="unresolved" for x in us if rid in x["region_ids"]) else "content")
      region_checks.append({
       "id":f"visual-second-p2-{rid}","region_id":rid,"pass":2,
       "reviewer_id":"/root/ra09_visual_second","session_id":"/root/ra09_visual_second",
       "assessment":rast,"source_unit_ids":ru,
       "evidence_ids":[f"image:{p}",f"image:{rid}"],
       "observation":region_obs[p][j]
      })
out={"page_checks":page_checks,"region_checks":region_checks}
(P/"reviews/visual-second/observations-second.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
print("wrote",len(page_checks),len(region_checks))
