"""Full frontier lines; abbreviate only exact previously read catalog paths.

Requires formally claimed primary original to have been materialized first.
No primary export, Git, network or source mutation.
"""
from pathlib import Path
import json, posixpath, re, sys

E=Path(__file__).resolve().parent
catalog=json.loads((E/'context/catalog.json').read_text())
path_ids={z['path']:'C'+str(i) for i,z in enumerate(catalog['entries'])}
lines=(E/'original/2f4a0833cc651ca428c8/research/weighted_congestion_frontier/CLAIMS.md').read_text().splitlines()
start,end=map(int,sys.argv[1:3])
if len(sys.argv)>3:
    p=E/'reading-progress.json'
    data=json.loads(p.read_text())
    data['claims_lines']=sorted(set(data['claims_lines'])|set(range(1,int(sys.argv[3])+1)))
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
out=[f'FRONTIER CLAIMS full lines{start}..{end}; Cn=exact previously fully read catalog path; all labels/math/unmatched paths retained.']
for i in range(start-1,min(end,len(lines))):
    def replace(m):
        original=m.group(1)
        path=posixpath.normpath(posixpath.join('research/weighted_congestion_frontier',original.split('#',1)[0]))
        return ']('+path_ids.get(path,original)+('#'+original.split('#',1)[1] if '#' in original and path in path_ids else '')+')'
    out.append(str(i+1)+': '+re.sub(r'\]\(([^)]+)\)',replace,lines[i]))
text='\n'.join(out)+'\n'
(E/'reading-views').mkdir(exist_ok=True)
(E/'reading-views'/f'claims-{start}-{end}.txt').write_text(text)
print(text,end='')
