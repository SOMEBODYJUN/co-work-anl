"""Lossless field reading view. Exact repeated purpose strings are referenced by stable IDs.
Creating a view is not an acknowledgment of semantic reading; only later explicit ack
updates progress after untruncated tool output has actually been read.
"""
import json,sys,hashlib
from pathlib import Path
E=Path(__file__).resolve().parent
x=json.loads((E/'original/research/catalog.json').read_text())
p=json.loads((E/'reading-progress.json').read_text())
topic,start,end=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
rr=[(i,r) for i,r in enumerate(x['entries']) if r['topic']==topic]
if len(sys.argv)>4:
 ack=int(sys.argv[4]);p['catalog_complete_indices']=sorted(set(p['catalog_complete_indices'])|{i for i,r in rr[:ack]});p[topic+'_entries_read_positions']=[0,ack-1];(E/'reading-progress.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
assert set().union(*(r.keys() for r in x['entries']))=={'path','title','purpose','topic','role','package','related_paths','related'}
pi={r['path']:i for i,r in enumerate(x['entries'])};purposes=list(dict.fromkeys(r['purpose'] for r in x['entries']));pm={q:i for i,q in enumerate(purposes)}
seen={x['entries'][i]['purpose'] for i in p['catalog_complete_indices']};out=['Topic='+topic+' positions '+str(start)+'..'+str(end-1)+'; P identifiers mean exact complete purpose strings; prior P strings already actually read.','NEW FULL PURPOSE STRINGS:']
for i,r in rr[start:end]:
 q=r['purpose']
 if q not in seen:out.append('P'+str(pm[q])+' '+q);seen.add(q)
out.append('RECORDS: index | exact path | complete human title | purpose-id | role | optional package | optional related_paths as exact catalog indices; absent fields marked -')
for i,r in rr[start:end]:
 out.append(' | '.join([str(i),r['path'],r['title'],'P'+str(pm[r['purpose']]),r['role'],r.get('package','-'),str([pi[q] for q in r['related_paths']]) if 'related_paths' in r else '-',str([pi[q] for q in r['related']]) if 'related' in r else '-']))
s='\n'.join(out)+'\n';d=E/'reading-views';d.mkdir(exist_ok=True);f=d/(topic+'-'+str(start)+'-'+str(end-1)+'.txt');f.write_text(s);print(s,end='')
