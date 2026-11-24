from pathlib import Path
p=Path('work/notes-fc2ba28a26cd495f/notes/RA07/project/proposals/integration-v2')

def replace_unit(path, uid, body):
 s=path.read_text(); marker='<!-- unit: '+uid+' -->'; start=s.index(marker); nxt=s.find('\n<!-- unit:', start+len(marker)); end=len(s) if nxt<0 else nxt+1
 s=s[:start]+marker+'\n'+body.rstrip()+'\n\n'+s[end:]; path.write_text(s)

T={
'T-P002-013':r'''$\forall x\in(x_1,\ldots,x_n)$〔原笔为 ∈ 样弯笔；规范坐标等号见蓝色补充〕，
$$x\in\prod\bigl([x_1]-1,\ldots,[x_n]+1\bigr).$$
（此处保留原稿压缩的乘积记号。）''',
'T-P003-002':r'''2. $\overline{\overline{LC(E)}}$：所有覆盖的族，记为 $LC_E$。
〔$LC(E)$ 上方原有两条横笔；含义暂不强定。〕''',
'T-P004-007':r'''$$\sum_{(k,j)}|I_{k,j}|<\sum_km^*(E_k)+\sum_{k=1}^{\infty}\frac{\varepsilon}{2k}.$$
〔原笔中此处分母 $k$ 与 $2$ 同基线；上文首次预算写为 $2^k$。〕''',
'T-P005-007':r'''旁写：$|I|-|I\,/\,G|$。
〔第二项中 $I$ 后为单斜杠样笔画，差集/交集读法未决；不是单独的 $|G|$。〕''',
'T-P006-002':r'''**Def.** 设 $E\subset\mathbb R^n$，若 $\forall T\subset\mathbb R^n$ 有
$$m^*(T)=m^*(T\cap E)+m^*(T\cap\cdots).$$
〔本行扫描右缘截断；根据本页中部完整复写，可恢复末项为 $m^*(T\cap E^c)$；测试字母原笔呈 T 样。〕''',
'T-P006-006':r'''一般：
$$m^*(T)=m^*(T\cap E)+m^*(T\cap E^c).$$
〔本页完整复写中的测试字母原笔呈 T 样。〕''',
'T-P007-004':r'''$\Leftarrow$：由外测度次可加性，仅证
$$m^*(I)\ge m^*(T\cap E)+m^*(T\cap E^c).$$
〔左端原笔为 I 样，右端两项为 T；数学规范补充见学习稿蓝色块。〕''',
'T-P007-006':r'''（2）$\forall\varepsilon>0$，$\exists\{I_k\}\in LC(T)$，s.t.
$$\sum_{k=1}^{\infty}(I_k)<m^*(T)+\varepsilon.$$
〔原笔求和项两侧为圆括号样笔画；体积双竖线是蓝色数学说明。〕''',
'T-P009-014':r'''$$\overline{\overline{2^c}}\le\overline{\overline{\mathcal M}}\le2^c.$$
〔左端 $2$ 上方原有两条短横；上标 C/c 形仍按原笔保留。〕'''
}
for u,b in T.items(): replace_unit(p/'source-transcript.md',u,b)
N={
'N-P002-013':T['T-P002-013'],
'N-P003-002':T['T-P003-002'],
'N-P004-007':T['T-P004-007'],
'N-P005-007':r'''旁写：$|I|-|I\,/\,G|$。
〔第二项中 $I$ 后为单斜杠样笔画，差集/交集读法未决；不是单独的 $|G|$。〕''',
'N-P006-002':r'''**Carathéodory 条件。** 设 $E\subset\mathbb R^n$。若对每个测试集合 $T\subset\mathbb R^n$，都有
$$m^*(T)=m^*(T\cap E)+m^*(T\cap E^c),$$
则称 $E$ 为 Lebesgue 可测集。

（测试字母原笔呈 T 样；定义行末项由本页后面的完整复写恢复。）''',
'N-P006-006':r'''一般：
$$m^*(T)=m^*(T\cap E)+m^*(T\cap E^c).$$
〔本页完整复写中的测试字母原笔呈 T 样。〕''',
'N-P007-004':r'''$\Leftarrow$：由外测度次可加性，仅证
$$m^*(I)\ge m^*(T\cap E)+m^*(T\cap E^c).$$
〔左端原笔为 I 样，右端两项为 T；数学规范补充见下方蓝色块。〕''',
'N-P007-006':T['T-P007-006'],
'N-P009-014':T['T-P009-014']
}
for u,b in N.items(): replace_unit(p/'study-notes.md',u,b)
# replace the old supplement under N-P005-007 with an explicitly conditional candidate discussion
f=p/'study-notes.md';s=f.read_text();a='<!-- unit: N-P005-007-S1 -->';start=s.index(a);nxt=s.find('\n<!-- unit:',start+len(a));end=len(s) if nxt<0 else nxt+1
body=r'''> [!info] 补充：孤立差式的两种字形解释
> 原笔第二项不是单独的 $|G|$，而是在 $G$ 前出现 $I$ 样笔画及斜杠。若将其读作差集 $I\setminus G$，则在 $I$ 有限可测、$G$ 开时
> $$m(I\setminus G)=|I|-m(I\cap G).$$
> 若局部斜杠实际意在表示交集，也只能在补全该交号后得到相应的交集公式；原图没有足够拱顶笔画让两者唯一。无论哪一候选，都不能把原笔静默改写成 $|I|-|G|$。'''
s=s[:start]+a+'\n'+body+'\n\n'+s[end:];f.write_text(s)
print('repaired targeted RA07 v2 units')
