import json, hashlib
from pathlib import Path
p=Path('work/notes-fc2ba28a26cd495f/notes/RA07/project')
b=p/'proposals/integration-v2'; t=b/'source-transcript.md'; n=b/'study-notes.md'
for f in [t,n]:
 s=f.read_text()
 reps={
  r'''$\\forall x=(x_1,\\ldots,x_n)$，''':r'''$\\forall x\\in(x_1,\\ldots,x_n)$〔原笔为 ∈ 样弯笔；规范坐标等号见蓝色补充〕，''',
  r'''2. $LC(E)$：所有覆盖的族，记为 $LC_E$。''':r'''2. $\\overline{\\overline{LC(E)}}$：所有覆盖的族，记为 $LC_E$。〔LC(E) 上方原有两条横笔；含义暂不强定。〕''',
  r'''\\sum_{k=1}^{\\infty}\\frac{\\varepsilon}{2^k}''':r'''\\sum_{k=1}^{\\infty}\\frac{\\varepsilon}{2k}〔原笔中此处分母 k 与 2 同基线；上文首次预算为 2^k〕''',
  r'''旁写：$|I|-|G|$。''':r'''旁写：$|I|-|I\\,/\\,G|$〔第二项中 I 后为单斜杠样笔画，差集/交集读法未决；不是单独的 $|G|$。〕''',
  r'''m^*(I)=m^*(I\\cap E)+m^*(I\\cap E^c).''':r'''m^*(T)=m^*(T\\cap E)+m^*(T\\cap E^c)〔本页两处测试字母原笔呈 T 样；第一处右缘仍截断〕.''',
  r'''仅证 $$m^*(T)\\ge m^*(T\\cap E)+m^*(T\\cap E^c).$$''':r'''仅证 $$m^*(I)\\ge m^*(T\\cap E)+m^*(T\\cap E^c).$$〔左端原笔为 I 样，右端两项为 T；数学规范补充见蓝色。〕''',
  r'''$$\\sum_{k=1}^{\\infty}|I_k|<m^*(T)+\\varepsilon.$$''':r'''$$\\sum_{k=1}^{\\infty}(I_k)<m^*(T)+\\varepsilon.$$〔原笔求和项两侧为圆括号样笔画；体积双竖线是蓝色数学说明。〕''',
  r'''$$2^c\\le\\overline{\\overline{\\mathcal M}}\\le2^c.$$''':r'''$$\\overline{\\overline{2^c}}\\le\\overline{\\overline{\\mathcal M}}\\le2^c.$$〔左端 2 上方原有两条短横；上标 C/c 形仍按原笔保留。〕''',
 }
 for a,bb in reps.items():
  s=s.replace(a,bb)
 f.write_text(s)
s=t.read_text(); marker='<!-- unit: T-P007-HEAD -->'; assert marker in s and '<!-- unit: T-P006-014 -->' not in s
s=s.replace(marker,'''<!-- unit: T-P006-014 -->
页左缘另有一段右括号样残弧（约 x=0–25、y=2475–2570）；无法据残笔恢复前文，保留为未定页边残笔。

'''+marker);t.write_text(s)
s=n.read_text(); marker='<!-- unit: N-SEC-09 -->'
if marker not in s: marker='<!-- unit: N-SEC-10 -->'
assert marker in s and '<!-- unit: N-P006-014 -->' not in s
s=s.replace(marker,'''<!-- unit: N-P006-014 -->
> [!info] 页边残笔（原图位置：第6页左缘）
> 可见一段右括号样弧线，约在 x=0–25、y=2475–2570；无法从残笔唯一恢复其配对或公式，故仅作来源记录，不解释为数学符号。

'''+marker);n.write_text(s)
su=b/'source-units.json'; m=b/'mapping.json'; sources=json.loads(su.read_text()); assert not any(x['id']=='RA07-P006-U014' for x in sources)
sources.append({'id':'RA07-P006-U014','page_id':'p0006','bbox_px':[0,2400,120,2630],'label':'第6页左缘未定括号样残弧','status':'unresolved','evidence_ids':['image:p0006','image:p0006-r3c1','artifact:visual-second-p0006-left-margin']});su.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
md=json.loads(m.read_text());md['targets'].extend([{'id':'T-P006-014','artifact_id':'transcription','source_ids':['RA07-P006-U014'],'status':'unresolved','origin':'source','old_ids':[],'evidence_ids':['image:p0006','image:p0006-r3c1','artifact:visual-second-p0006-left-margin'],'explanation':'第二读者实际重开页边裁图发现未映射残弧；仅保存位置与不可唯一恢复说明。'},{'id':'N-P006-014','artifact_id':'study','source_ids':['RA07-P006-U014'],'status':'unresolved','origin':'source','old_ids':[],'evidence_ids':['image:p0006','image:p0006-r3c1','artifact:visual-second-p0006-left-margin'],'explanation':'普通页边残笔仅作来源记录，不造数学内容。'}]);m.write_text(json.dumps(md,ensure_ascii=False,indent=2)+'\n')
print('bodies',hashlib.sha256(t.read_bytes()).hexdigest(),hashlib.sha256(n.read_bytes()).hexdigest(),'sources',len(sources),'targets',len(md['targets']))
