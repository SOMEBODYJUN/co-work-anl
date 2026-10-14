#!/usr/bin/env python3
"""PDF visual-review renderer. Requires WeasyPrint 70 and lxml.

Use the same KaTeX release as build_reading.mjs. Its TTF files preserve
font metrics when the PDF renderer cannot register embedded WOFF2 fonts.
Negation overlays are replaced with the identical Unicode relation in
this PDF DOM only. The HTML and its TeX annotations remain unchanged.
The layout JSON records this rendering adaptation explicitly.
"""
from lxml import html
from pathlib import Path
from weasyprint import HTML,CSS
from weasyprint.text.fonts import FontConfiguration
import re,logging,json,hashlib,sys,shutil
logging.getLogger("weasyprint").setLevel(logging.ERROR)
import argparse
parser=argparse.ArgumentParser(description="Render the offline manuscript for paginated visual review.")
parser.add_argument("html",type=Path)
parser.add_argument("katex_dist",type=Path)
parser.add_argument("cjk_font",type=Path)
parser.add_argument("pdf",type=Path)
args=parser.parse_args()
source=args.html.resolve();assets=args.katex_dist.resolve();font=args.cjk_font.resolve();output=args.pdf.resolve()
output.parent.mkdir(parents=True,exist_ok=True)
s=source.read_text();tree=html.fromstring(s)
# WeasyPrint cannot overlay KaTeX's private-use negation slash reliably.
# Substitute the exact Unicode relation only in this PDF DOM; HTML stays untouched.
negations=[]
negated={"=":"≠","∈":"∉","∋":"∌","≤":"≰","≥":"≱","<":"≮",">":"≯","⊂":"⊄","⊃":"⊅","⊆":"⊈","⊇":"⊉","∣":"∤","∥":"∦","≈":"≉","≡":"≢","~":"≁","∼":"≁"}
for slash in list(tree.xpath("//span[contains(text(), '\ue020')]")):
 outer=next((n for n in slash.iterancestors() if "mrel" in n.get("class", "").split() and len(n)>=2 and "mrel" in n[-1].get("class", "").split()),None)
 if outer is None:
  # KaTeX can place a standalone \\not and its relation in adjacent bases.
  # This is a PDF-only adaptation; the annotated HTML stays unchanged.
  groups=[n for n in slash.iterancestors() if "mrel" in n.get("class", "").split()]
  outer=groups[-1] if groups else None
  relation=outer.getnext() if outer is not None else None
  if relation is None and outer is not None and "base" in outer.getparent().get("class", "").split():
   next_base=outer.getparent().getnext()
   if next_base is not None and "base" in next_base.get("class", "").split():
    relation=next((n for n in next_base if "mrel" in n.get("class", "").split()),None)
  if relation is None:raise ValueError("Unrecognized negation overlay")
  base=relation.text_content()
  if base not in negated:raise ValueError("Unknown standalone negated relation: "+repr(base))
  relation.getparent().remove(relation)
 else:
  base=outer[-1].text_content()
 if base not in negated:raise ValueError("Unknown negated relation: "+repr(base))
 negations.append({"base":base,"relation":negated[base]})
 for child in list(outer):outer.remove(child)
 outer.text=negated[base]
 outer.set("style",'font-family:"Noto Serif CJK SC";font-style:normal')
# KaTeX also builds not-in with an llap slash; use its exact Unicode relation.
for slash in list(tree.xpath("//span[contains(concat(' ',normalize-space(@class),' '),' llap ')]")):
 outer=next((n for n in slash.iterancestors() if "mrel" in n.get("class", "").split() and len(n)>=2),None)
 if outer is None:continue
 base=outer[0].text_content().strip()
 if base not in negated:continue
 if "/" not in slash.text_content():continue
 negations.append({"base":base,"relation":negated[base],"method":"llap"})
 for child in list(outer):outer.remove(child)
 outer.text=negated[base]
 outer.set("style",'font-family:"Noto Serif CJK SC";font-style:normal')
css=(assets/"katex.css").read_text()
css=re.sub(r"src:[^;]+;",lambda m:"src:url("+(assets/re.search(r"url\((fonts/[^ )]+\.ttf)\)",m.group()).group(1)).as_uri()+") format(\"truetype\");",css)
style=tree.xpath("//style")[0].text
custom=style[style.index(":root{"):]
fontcss='@font-face{font-family:"Noto Serif CJK SC";src:url('+font.as_uri()+');font-weight:100 900}'
f=FontConfiguration();c=CSS(string=css+custom+fontcss,font_config=f)
tree.xpath("//style")[0].text=""
d=HTML(string=html.tostring(tree,encoding="unicode"),base_url=source.parent.as_uri()).render(stylesheets=[c],font_config=f)
print("rendered",len(d.pages),flush=True)
# Record actual heading page positions and boxes protruding beyond printable width.
headings=[];overflows=[]
for page_index,page in enumerate(d.pages,1):
 for box in page._page_box.descendants():
  element=getattr(box,"element",None)
  if element is not None and element.tag in ("h1","h2","h3") and box.__class__.__name__=="BlockBox":
   headings.append({"page":page_index,"id":element.get("id"),"title":"".join(element.itertext())})
  if box.__class__.__name__=="LineBox" and box.position_x+box.width>730:
   overflows.append({"page":page_index,"x":round(box.position_x,1),"width":round(box.width,1),"text":" ".join(getattr(b,"text","") for b in box.descendants())[:160]})
d.write_pdf(output)
Path(str(output)+".layout.json").write_text(json.dumps({"html_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"pages":len(d.pages),"headings":headings,"lineOverflows":overflows,"font_source":"Noto Serif CJK SC + KaTeX 0.16.11 TTF equivalents of embedded WOFF2","unicodeNegationAdapters":negations},ensure_ascii=False,indent=2))
print("pdf ready",str(output),flush=True)

# Remove only the font cache created by this renderer.
if f._folder:
 shutil.rmtree(f._folder,ignore_errors=True)
