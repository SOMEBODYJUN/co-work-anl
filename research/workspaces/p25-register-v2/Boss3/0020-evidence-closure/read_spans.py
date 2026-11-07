from pathlib import Path
import sys,json,hashlib
out=Path(__file__).parent
for spec in sys.argv[1:]:
 path,start,end=spec.rsplit(':',2);p=Path(path);b=p.read_bytes();ls=b.splitlines(keepends=True);start=int(start);end=len(ls) if end=='end' else int(end)
 seg=b''.join(ls[start-1:end]);entry={'path':path,'sha256':hashlib.sha256(b).hexdigest(),'line_start':start,'line_end':end,'byte_start':sum(map(len,ls[:start-1])),'byte_end':sum(map(len,ls[:end])),'bytes':len(seg),'fresh_read':True}
 with (out/'reading-spans.jsonl').open('a') as f:f.write(json.dumps(entry,ensure_ascii=False)+'\n')
 print('\nFRESH_READ',json.dumps(entry,ensure_ascii=False))
 for n,l in enumerate(seg.decode().splitlines(),start):print(f'{n}: {l}')
