#!/usr/bin/env python3
"""New source-binding/semantic-preservation audit, deliberately not a proof checker.

Run render_structure.mjs first. This reads the frozen final HTML and all 33
frozen Markdown inputs, validates its math-token syntax tree, inventories every
embedded asset, and writes a complete editable Markdown reading resource.
It does not execute build_reading.mjs, render_reading.py, or a browser.
"""
from pathlib import Path
from lxml import html, etree
from collections import Counter
import base64, copy, hashlib, json, re, struct, subprocess

BASE=Path(__file__).resolve().parent
STAGE=BASE.parents[2]
OUT=STAGE/'archives/facility-games/state/资源/完整阅读导出的逐章数学正文--资源.md'
def sha(b):return hashlib.sha256(b).hexdigest()
def cls(e,c):return c in (e.get('class') or '').split()
def dump(name,obj):
 p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
raw=(BASE/'original/learning/export/学习和演讲-学习定稿.html').read_bytes()
doc=html.fromstring(raw)
audit=json.loads((BASE/'original/learning/export/学习和演讲-学习定稿.html.audit.json').read_text())
manifest=json.loads((BASE/'original/learning/manifest.json').read_text())
rendered=json.loads((BASE/'syntax-render.json').read_text())
checks=[]
def require(ok,name,detail=None):
 checks.append({'check':name,'pass':bool(ok),'detail':detail})
 if not ok:raise AssertionError((name,detail))

def canon(e,preserve=False):
 if not isinstance(e.tag,str):return None
 if cls(e,'math-token'):return ('math',e.get('data-display'),e.get('data-tex'))
 preserve=preserve or e.tag in ('pre','code')
 def text(s):return s if preserve else re.sub(r'\s+',' ',s or '').strip()
 out=[e.tag,text(e.text)]
 for child in e:
  out.extend([canon(child,preserve),text(child.tail)])
 return out

def normalize_math(section):
 s=copy.deepcopy(section)
 for n in list(s.xpath('.//div[@class="source-note"]')):n.drop_tree()
 for n in list(s.xpath('.//span[contains(concat(" ",normalize-space(@class)," ")," katex-display ")]')):
  aa=n.xpath('.//annotation[@encoding="application/x-tex"]');assert len(aa)==1
  token=html.Element('span',{'class':'math-token','data-display':'true','data-tex':(aa[0].text or '').strip()});token.tail=n.tail;n.getparent().replace(n,token)
 for n in list(s.xpath('.//span[contains(concat(" ",normalize-space(@class)," ")," katex ")]')):
  aa=n.xpath('.//annotation[@encoding="application/x-tex"]');assert len(aa)==1
  token=html.Element('span',{'class':'math-token','data-display':'false','data-tex':(aa[0].text or '').strip()});token.tail=n.tail;n.getparent().replace(n,token)
 s.tag='div';return s

annotations=doc.xpath('//annotation[@encoding="application/x-tex"]')
katex=doc.xpath('//span[contains(concat(" ",normalize-space(@class)," ")," katex ")]')
require(len(katex)==len(annotations)==audit['equations']==9782,'one annotation per complete formula stream')
for n in katex:
 require(len(n.xpath('./span[@class="katex-mathml"]/math/semantics/annotation'))==1 and len(n.xpath('./span[@class="katex-html"][@aria-hidden="true"]'))==1,'formula dual representation structure')
section_records=[]
for i,(source,expected) in enumerate(zip(audit['sources'],rendered)):
 b=(BASE/'related'/source['path']).read_bytes();require(len(b)==source['bytes'] and sha(b)==source['sha256'],'source hash '+source['path'])
 sec=doc.xpath(f'//section[@id="source-{i}"]');require(len(sec)==1,'source section '+str(i))
 actual=normalize_math(sec[0]);wanted=html.fragment_fromstring(expected['html'],create_parent='div')
 require(canon(actual)==canon(wanted),'entire marked semantic syntax tree '+source['path'])
 section_records.append({'section':f'source-{i}','path':source['path'],'sha256':source['sha256'],'bytes':len(b),'formulas':len(sec[0].xpath('.//annotation')),'headings':len(sec[0].xpath('.//*[self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or self::h6]')),'tables':len(sec[0].xpath('.//table')),'code_blocks':len(sec[0].xpath('.//pre')),'all_text_and_math_syntax_equal':True})
require(len(section_records)==33,'33 source sections')
require({x['path'] for x in manifest['modules']}=={x['path'] for x in audit['sources']},'manifest source set equals audit')
ids=Counter(doc.xpath('//*[@id]/@id'));require(all(v==1 for v in ids.values()),'unique ids',len(ids))
links=doc.xpath('//a/@href');missing=[x for x in links if x.startswith('#') and x[1:] not in ids];require(not missing,'all internal link targets',missing)
css='\n'.join(doc.xpath('//style/text()'));urls=re.findall(r'url\(([^)]+)\)',css)
require(all(x.strip('"\' ').startswith('data:') for x in urls),'all CSS resource urls embedded')
require(not doc.xpath('//script[@src]|//link[@href]|//img|//image|//object|//iframe|//video|//canvas|//embed'),'no other visible binary media')
require(not audit['mathErrors'] and audit['sectionFallbacks']==0,'recorded render errors and heading fallbacks empty')
fonts=[]
face_rules=re.findall(r'@font-face\s*\{[^}]+\}',css)
for i,m in enumerate(re.finditer(r'data:font/woff2;base64,([A-Za-z0-9+/=]+)',css)):
 prefix=css[:m.start()]
 data=base64.b64decode(m[1]);require(data[:4]==b'wOF2','woff2 signature '+str(i))
 p=BASE/f'assets/font-{i:02}.woff2';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 identity=subprocess.check_output(['fc-scan','--format','%{family}\n%{style}\n%{fontversion}\n',str(p)],text=True).strip().splitlines()
 fonts.append({'path':str(p.relative_to(STAGE)),'sha256':sha(data),'bytes':len(data),'css_declared_family':re.findall(r'font-family:([^;]+)',prefix)[-1],'css_preceding_style':re.findall(r'font-style:([^;]+)',prefix)[-1],'css_preceding_weight':re.findall(r'font-weight:([^;]+)',prefix)[-1],'fc_scan_family':identity[0],'fc_scan_style':identity[1],'fc_scan_version':identity[2],'woff2_declared_length':struct.unpack('>I',data[8:12])[0]})
require(len(fonts)==20 and len({x['sha256'] for x in fonts})==20,'20 distinct embedded KaTeX font assets')
require(len(face_rules)==1 and face_rules[0].count('src:')==20,'actual CSS font-face collapse detected')
svg_groups={}
for n in doc.xpath('//svg'):
 outer=next((a for a in n.iterancestors() if cls(a,'katex')),None);require(outer is not None,'SVG is inside formula')
 b=html.tostring(n);h=sha(b);g=svg_groups.setdefault(h,{'sha256':h,'bytes':len(b),'count':0,'width':n.get('width'),'height':n.get('height'),'viewbox':n.get('viewbox'),'sample_tex':[],'raw':b})
 g['count']+=1;tex=outer.xpath('.//annotation')[0].text
 if tex not in g['sample_tex'] and len(g['sample_tex'])<4:g['sample_tex'].append(tex)
for i,g in enumerate(svg_groups.values()):
 b=g.pop('raw');p=BASE/f'assets/math-decoration-{i:02}.svg';p.write_bytes(b);g['path']=str(p.relative_to(STAGE));g['scope']='deduplicated exact HTML serialization; radical, wide accent, or scalable delimiter; no independent diagram'
dump('assets/manifest.json',{'fonts':fonts,'css_font_face_rules':len(face_rules),'src_descriptors_in_single_face':20,'font_safety_pass':False,'font_finding':'All 20 WOFF2 byte payloads exist and fc-scan identifies 12 different internal families, but their 20 src/style/weight descriptor groups occur in one KaTeX_AMS font-face rule. The intended separate face declarations and base KaTeX font declaration are not present; this is not a correctly wired embedded-font stylesheet.','svg_total':sum(g['count'] for g in svg_groups.values()),'unique_svg':list(svg_groups.values()),'external_images':[],'cjk_font_boundary':'CJK prose fonts are system fallbacks, not embedded. SVG serialization was parsed as HTML and keeps HTML-lowercased viewbox/preserveaspectratio; exact original bytes remain in original HTML.'})

formula_emissions=[]
def contents(e,table=False):return (e.text or '')+''.join(md(c,table)+(c.tail or '') for c in e)
def math_tex(e,table):
 a=e.xpath('.//annotation[@encoding="application/x-tex"]');assert len(a)==1
 t=(a[0].text or '').strip();formula_emissions.append(t)
 # A raw table separator is spelling, not a changed mathematical bar.
 if table:t=re.sub(r'(?<!\\)\|',r'\\vert ',t)
 return t
def md(e,table=False):
 if not isinstance(e.tag,str):return ''
 tag=e.tag
 if cls(e,'source-note'):return ''
 if cls(e,'katex'):
  return '$'+math_tex(e,table)+'$'
 if cls(e,'katex-display'):
  return '\n\n$$\n'+math_tex(e,table)+'\n$$\n\n'
 if tag=='div' and cls(e,'equation'):
  return '\n\n$$\n'+math_tex(e,table)+'\n$$\n\n'
 if tag=='table':
  rows=[]
  for tr in e.xpath('./thead/tr|./tbody/tr|./tr'):
   row=[]
   for cell in tr:
    v=contents(cell,True);v=re.sub(r'\s+',' ',v).strip();v=re.sub(r'(?<!\\)\|',r'\\|',v);row.append(v)
   rows.append(row)
  width=max(map(len,rows));rows=[x+['']*(width-len(x)) for x in rows]
  result=['| '+' | '.join(rows[0])+' |','| '+' | '.join(['---']*width)+' |']+['| '+' | '.join(x)+' |' for x in rows[1:]]
  return '\n\n'+'\n'.join(result)+'\n\n'
 if tag=='pre':
  code=e.text_content();fence='`'*max(3,max([len(x) for x in re.findall(r'`+',code)]+[0])+1)
  c=e.find('code');lang=(c.get('class','').replace('language-','') if c is not None else '')
  return '\n\n'+fence+lang+'\n'+code.rstrip('\n')+'\n'+fence+'\n\n'
 if tag=='code':
  v=e.text_content();fence='`'*max(1,max([len(x) for x in re.findall(r'`+',v)]+[0])+1);return fence+v+fence
 if tag=='a':return '['+contents(e,table)+']('+e.get('href','')+')'
 if tag in ('strong','b'):return '**'+contents(e,table)+'**'
 if tag in ('em','i'):return '*'+contents(e,table)+'*'
 if re.fullmatch(r'h[1-6]',tag):
  anchor='<a id="'+e.get('id')+'"></a>\n\n' if e.get('id') else ''
  return '\n\n'+anchor+'#'*min(6,int(tag[1])+2)+' '+contents(e,table)+'\n\n'
 if tag=='li':return '\n- '+contents(e,table).strip().replace('\n','\n  ')+'\n'
 if tag in ('ul','ol'):return '\n\n'+contents(e,table)+'\n\n'
 if tag=='blockquote':return '\n\n'+''.join('> '+x+'\n' for x in contents(e,table).strip().splitlines())+'\n'
 if tag in ('p','div','section'):return '\n\n'+contents(e,table)+'\n\n'
 if tag=='br':return '<br>' if table else '\n'
 if tag=='hr':return '\n\n---\n\n'
 return contents(e,table)

front='''---
id: facility-complete-reading-export-text
kind: resource
type_tag: 资源
title: 完整阅读导出的逐章数学正文
status: 完整语义整理；数学结论保持各自审查状态；未新增视觉或软件认证
summary: 从最终HTML逐节恢复全部正文、9782个TeX公式、表格、代码与练习，并明确当前状态及版本边界。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:learning/export/学习和演讲-学习定稿.html
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:learning/export/学习和演讲-学习定稿.html
---

# 完整阅读导出的逐章数学正文

这份资源把最终 HTML 的实际数学阅读内容转成可编辑正文：17个主阅读模块、15份数学附录及1份审读附录全部连续保留。全部模型、量词、计算、证明分支、独有例、练习解答与代码均在下文，不以导出元数据代替证明。

版本判断先于使用：原导出日期为2026-10-10；文件SHA-256为`1077ce9ee86601a3f31f5c7893a57563793e9ecc73e116d2593a90c90a1286aa`。原件中的“本次”“当前仓库”“已内部证明”等措辞描述该版本的叙述时间，不能独立升级现行登记。新的比对和导出合同在[构建与分页资源](学习定稿构建与分页导出的实际合同--资源.md)及[绑定审查](../审查/学习定稿清单与公式审计的证据边界--审查.md)。

当前数学身份须保留以下修正：

- 黄金比例上界的菜单/局部构造/坏环推导完整保留，但现行[五处修订与待审证明域](../审查/双设施黄金比稿的五处修订与待审证明域--审查.md)仍要求针对修订后长环运输及构造位长的新审读；本资源没有另作这项独立审读，不把旧教学PASS当成解除义务。N≥5稀疏阈值及二次费用的全局φ迁移相应保持条件依赖。
- 一般异构因子二的四种子及任意长偶环全文保持内部候选；详细展开和有限证书都不提升为外部审查结论。
- 任意设施数完整贪心盒存在与有限构造已有证明，一般位多项式在轨选择仍开放。等权流、两类结构DP各保留本身的参数条件。数学上的多项式离轨完成调用公开受限同链调度器；仓库有限纯改善程序不是该调度器的规范实现。
- 外部RANGE导入现有[双端负载保持引理](../../subarchives/common-many/state/引理/受限同链Nash化的双端负载保持导入--引理.md)：已读STOC2004 §4 Cor4.3/Th4.7及作者2009版本§2/Th6.5。Cor4.3是子程序性质；全流程极值保持是对真实分配变更逐调用的明确归纳。它没有给一般盒选择器或未交付软件认证。
- A11–A15的数学与教学/软件身份分开。A12/A13原件关于当时取不到非线性源码的陈述保留历史身份；现已整理出自足数学页，不据此宣称存在规范非线性实现。四地点无FPTAS不否定PTAS/EPTAS；近带补全不是完整EPTAS。A14的NO算例`6136/4695`是所展示规则的实际倍率，不充当未经证明的实例最优值。
- 原研讨页“十三份附录”是旧数字；本实际导出含十五份数学附录和一份审读记录。下文明确校正这处计数，原件仍保留原字样。
- 本批新增导出纠错：20枚WOFF2字节确实存在，但实际CSS只有1条KaTeX_AMS的font-face规则，混入20组src/style/weight；独立字体族及基础KaTeX字体声明被吞并。不能从“外部显示资源为零”推出字体接线正确，也不能声称原HTML公式已获得正确字体显示。机制、精确资产及未作用于冻结版的最小修正建议见构建资源。

下面的公式来自实际HTML的TeX annotation；删去的是同一公式的KaTeX视觉/MathML重复展开，不删数学。表格中原始竖线写成等价`\\vert`以避免Markdown分列。内部锚点沿用实际导出ID；外链保持原版本目标，不能保证离线可取代码或外部网站。正文CJK字体并未由原文件内嵌，具体字体依赖见构建资源。没有声称新PDF、浏览器交互或全书逐页视觉PASS。

'''
parts=[front]
for i,s in enumerate(audit['sources']):
 sec=doc.xpath(f'//section[@id="source-{i}"]')[0]
 chunk=md(sec)
 if i==11:chunk=chunk.replace('十三份附录继续作为完整阅读内容','十五份数学附录继续作为完整阅读内容')
 parts+=['\n\n<a id="source-'+str(i)+'"></a>\n\n## '+s['path']+'\n\n',chunk]
parts.append('\n\n<a id="appendix-list"></a>\n\n## 附录目录与页面外壳\n\n')
parts.append(md(doc.xpath('//section[@id="appendix-list"]')[0]))
parts.append('\n页面标题为“学习和演讲：学习定稿与完整推导”；页首主题为“两阶段设施选址：从客户选择到完整稳定构造”，副题“人类团队 · 两周研讨会 · 完整阅读版”。导航先列17个主模块，再链接“规范长附录”；页首三条入口指向技术分析、黄金比例及任意设施数主线。页首说明与下文相同：先成本与量词，再连续主证明；15份数学附录全文；版本2026-10-10；未内嵌代码及专题链接指向GitHub。打印按钮调用`window.print()`。这些是阅读和显示功能，不是数学证明。\n')
OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(re.sub(r'\n{3,}','\n\n',''.join(parts)))
require(formula_emissions==[(a.text or '').strip() for a in annotations],'complete ordered TeX stream emitted into new resource',len(formula_emissions))
dump('source-binding-audit.json',{'scope':'new limited source/HTML semantic syntax binding; not mathematical proof, KaTeX rerender, PDF, or browser test','html_bytes':len(raw),'html_sha256':sha(raw),'sections':section_records,'formula_count':len(annotations),'ids':len(ids),'links':len(links),'internal_links':sum(x.startswith('#') for x in links),'external_links':sorted(set(x for x in links if not x.startswith('#'))),'tables':len(doc.xpath('//table')),'code_blocks':len(doc.xpath('//pre')),'details':len(doc.xpath('//details')),'svg_count':len(doc.xpath('//svg')),'unique_svg':len(svg_groups),'fonts':len(fonts),'font_bytes':sum(x['bytes'] for x in fonts),'checks_count':len(checks),'failed_checks':[x for x in checks if not x['pass']],'resource':str(OUT.relative_to(STAGE)),'resource_bytes':OUT.stat().st_size,'resource_sha256':sha(OUT.read_bytes()),'formula_emissions':len(formula_emissions)})
print(json.dumps({'sources':len(section_records),'formulas':len(annotations),'tables':len(doc.xpath('//table')),'checks':len(checks),'resource_bytes':OUT.stat().st_size,'svg':len(svg_groups),'fonts':len(fonts)},ensure_ascii=False))
