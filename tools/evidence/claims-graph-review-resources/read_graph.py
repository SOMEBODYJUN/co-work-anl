"""Lossless full-node/edge reading view. Only exact already-read strings reused."""
from pathlib import Path
import json,sys
E=Path(__file__).resolve().parent
g=json.loads((E/'original/research/graph.json').read_text())
cat=json.loads((E/'related/research/catalog.json').read_text())
claims=(E/'original/research/current/claims.md').read_text()
group,start,end=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
p=json.loads((E/'reading-progress.json').read_text())
field={'nodes':'graph_nodes_read_indices','hyperedges':'graph_edges_read_indices'}[group]
if len(sys.argv)>4:
 p[field]=sorted(set(p[field])|set(range(int(sys.argv[4]))))
 (E/'reading-progress.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
known={}
for i,z in enumerate(cat['entries']):
 known.setdefault(z['path'],'C'+str(i))
 known.setdefault(z['title'],'CT'+str(i))
def take(x,where):
 if isinstance(x,str):known.setdefault(x,where)
 elif isinstance(x,list):
  for i,z in enumerate(x):take(z,where+'['+str(i)+']')
 elif isinstance(x,dict):
  for k,z in x.items():take(z,where+'.'+k)
for name,tag in [('assets.json','A'),('review_status.json','V')]:
 data=json.loads((E/'related/research'/name).read_text())
 for i,z in enumerate(data['entries']):take(z,tag+str(i))
values=[]
def strings(z):
 for k,v in z.items():
  if k in ['id','kind','track','premises','conclusion']:continue
  if isinstance(v,str):yield v
  elif isinstance(v,list):
   for t in v:yield t
for grp in ['nodes','hyperedges']:
 for z in g[grp]:
  for s in strings(z):
   if s not in known and s not in values:
    if len(s)>=20 and s in claims:
     n=claims.index(s);known[s]='L'+str(claims[:n].count('\n')+1)+'@'+str(n)+':'+str(len(s))
    else:values.append(s)
um={s:'U'+str(i) for i,s in enumerate(values)}
allknown={**um,**known}
seen=set()
for grp,fld in [('nodes','graph_nodes_read_indices'),('hyperedges','graph_edges_read_indices')]:
 for i in p[fld]:
  for s in strings(g[grp][i]):seen.add(s)
out=[f'GRAPH {group} {start}..{end-1}; full fields per record. Cn/CTn=exact previously read catalog path/title; A/V=full exact prior asset/review field; L=exact substring of completely read claims with line/character locator; Un new strings printed full before reuse.','NEW STRINGS:']
for z in g[group][start:end]:
 for s in strings(z):
  if s in um and s not in seen:out.append(um[s]+' '+json.dumps(s,ensure_ascii=False));seen.add(s)
out.append('FULL RECORDS:')
for i,z in list(enumerate(g[group]))[start:end]:
 d={}
 for k,v in z.items():
  if k in ['id','kind','track','premises','conclusion']:d[k]=v
  elif isinstance(v,str):d[k]=allknown[v]
  elif isinstance(v,list):d[k]=[allknown[t] for t in v]
  else:d[k]=v
 out.append(str(i)+' '+json.dumps(d,ensure_ascii=False,separators=(',',':')))
s='\n'.join(out)+'\n'
(E/'reading-views'/f'graph-{group}-{start}-{end-1}.txt').write_text(s)
if not (E/'graph-string-dictionary.json').exists():
 (E/'graph-string-dictionary.json').write_text(json.dumps({'known_exact':known,'new_strings':um,'scope':'codes only exact previously fully-read human strings; U first use actually printed and read'},ensure_ascii=False,indent=2)+'\n')
print(s,end='')
