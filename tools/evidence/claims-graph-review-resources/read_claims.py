"""Full-line semantics, only exact already-read catalog paths abbreviated."""
from pathlib import Path
import json,re,posixpath,sys
E=Path(__file__).resolve().parent
cat=json.loads((E/'related/research/catalog.json').read_text())
pi={z['path']:'C'+str(i) for i,z in enumerate(cat['entries'])}
lines=(E/'original/research/current/claims.md').read_text().splitlines()
start,end=map(int,sys.argv[1:3])
p=json.loads((E/'reading-progress.json').read_text())
if len(sys.argv)>3:
 p['claims_read_lines']=sorted(set(p['claims_read_lines'])|set(range(1,int(sys.argv[3])+1)))
 (E/'reading-progress.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
out=[f'CLAIMS full lines {start}..{end}; Cn=exact path in previously fully read catalog; all link labels, math and unmatched paths retained.']
for i in range(start-1,min(end,len(lines))):
 def sub(m):
  original=m.group(1);path=posixpath.normpath(posixpath.join('research/current',original.split('#',1)[0]))
  return ']('+pi.get(path,original)+('#'+original.split('#',1)[1] if '#' in original and path in pi else '')+')'
 out.append(str(i+1)+': '+re.sub(r'\]\(([^)]+)\)',sub,lines[i]))
s='\n'.join(out)+'\n'
(E/'reading-views'/f'claims-{start}-{end}.txt').write_text(s)
print(s,end='')
