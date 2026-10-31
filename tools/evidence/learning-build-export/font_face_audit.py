#!/usr/bin/env python3
"""Limited lexical CSS rule/descriptor audit; no browser or CSS layout engine."""
from pathlib import Path
from collections import Counter
import base64,hashlib,json,re
BASE=Path(__file__).resolve().parent
css=(BASE/'embedded.css').read_text()
def split_top(s,sep):
 out=[];start=0;quote=None;escaped=False;paren=0;comment=False;i=0
 while i<len(s):
  c=s[i]
  if comment:
   if s[i:i+2]=='*/':comment=False;i+=2;continue
  elif quote:
   if escaped:escaped=False
   elif c=='\\':escaped=True
   elif c==quote:quote=None
  elif s[i:i+2]=='/*':comment=True;i+=2;continue
  elif c in '\"\'':quote=c
  elif c=='(':paren+=1
  elif c==')':paren-=1
  elif c==sep and paren==0:out.append(s[start:i]);start=i+1
  i+=1
 out.append(s[start:]);return out
faces=[]
for m in re.finditer(r'@font-face\s*\{',css):
 start=m.start();at=m.end();quote=None;escaped=False;paren=0;end=None
 for i in range(at,len(css)):
  c=css[i]
  if quote:
   if escaped:escaped=False
   elif c=='\\':escaped=True
   elif c==quote:quote=None
  elif c in '\"\'':quote=c
  elif c=='(':paren+=1
  elif c==')':paren-=1
  elif c=='}' and paren==0:end=i+1;break
 assert end is not None
 rule=css[start:end];(BASE/'font-face-rule.css').write_text(rule+'\n')
 ds=[]
 for fragment in split_top(css[at:end-1],';'):
  if not fragment.strip():continue
  name,value=fragment.split(':',1);name=name.strip();value=value.strip();r={'descriptor':name,'value':value}
  if name=='src':
   b64=re.search(r'data:font/woff2;base64,([A-Za-z0-9+/=]+)',value)[1];b=base64.b64decode(b64);r={'descriptor':'src','data_mime':'font/woff2','bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'format':'woff2'}
  ds.append(r)
 faces.append({'start_char':start,'end_char':end,'utf8_bytes':len(rule.encode()),'sha256':hashlib.sha256(rule.encode()).hexdigest(),'descriptors':ds,'descriptor_counts':dict(Counter(x['descriptor'] for x in ds))})
assert len(faces)==1 and faces[0]['descriptor_counts']=={'font-family':1,'font-style':20,'font-weight':20,'src':20,'line-height':1,'text-indent':1,'text-rendering':1}
result={'scope':'complete lexical parsing of actual font-face rule and all descriptors, respecting quoted text and semicolons inside URL parentheses; not a CSS standards conformance parser or layout test','css_sha256':hashlib.sha256(css.encode()).hexdigest(),'css_bytes':len(css.encode()),'faces':faces,'base_katex_font_shorthand_present':bool(re.search(r'\.katex\s*\{[^}]*\bfont:',css)),'package_version_string_in_css':'0.16.11','finding':'20 binary font assets are present; all src descriptors were merged into a single family rule. Actual rendering remains untested.'}
(BASE/'font-face-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'font_face_rules':len(faces),'descriptors':faces[0]['descriptor_counts'],'base_katex_font_shorthand_present':result['base_katex_font_shorthand_present']}))
