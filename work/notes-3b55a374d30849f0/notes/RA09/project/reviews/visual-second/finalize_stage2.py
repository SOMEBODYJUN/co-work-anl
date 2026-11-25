import json,hashlib,os
from datetime import datetime,timezone
base='work/notes-fc2ba28a26cd495f/notes/RA09/project'
review=os.path.join(base,'reviews/visual-second')
# append six successful recovery reopens, preserving previous records and exact paths
p=os.path.join(review,'revision-tasks.json'); d=json.load(open(p,encoding='utf-8'))
existing={(x.get('path'),x.get('sha256')) for x in d.get('reopened_images',[])}
new=[
 ('regions/p0008-r3c1.png','p0008','cee6155ea42e7b0adc6248fa658f9f56d5ee9d6ad9f077da4dc28ab32156bf9c'),
 ('regions/p0008-r3c2.png','p0008','8cfdb1de94cc238065b8ccb6774bd93ee71fdf454e12badf6626c8423d188a86'),
 ('regions/p0010-r1c1.png','p0010','e6188524decd2fbec0269c1de14a2b98e3047d74a1c4531925a56ef1a2835b49'),
 ('regions/p0010-r1c2.png','p0010','819049c2f96b1eaf071fe9c03e3eef039d5dfd97f4f8ebd58bf0b813e30c1a5d'),
 ('regions/p0010-r2c1.png','p0010','b2a0c4b148efad731230fad83e16186540a372ea24393ca7d857aaa3d77d453e'),
 ('regions/p0010-r2c2.png','p0010','052dff25f028cb7290420449506e4fc36be9cafe5cc4b124273b2c3331317630'),
]
for path,page,sha in new:
 if (path,sha) not in existing:
  d['reopened_images'].append({'path':path,'page_id':page,'sha256':sha,'reason':'恢复候选回图：核对端点/分段实际字形与候选差异。','tool':'tools.view_image; image(...)'})
# unchanged inputs are same as start hashes; add own completion hashes for traceability
sha=lambda fn: hashlib.sha256(open(fn,'rb').read()).hexdigest()
d['status']='complete_nonfinal'
d['end_hashes']=dict(d['start_hashes'])
for fn in ['comparison-report.md','revision-tasks.json','observations-second.json','recovery-proposals.json']:
 fp=os.path.join(review,fn)
 if os.path.exists(fp): d['end_hashes']['reviews/visual-second/'+fn]=sha(fp)
# revision-tasks self hash must be computed after write; temporarily omit then write, recalc and rewrite
# write normalized one final time
with open(p,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2); f.write('\n')
# set self hash to final bytes and write again (second write changes only same value length; hash converges? do not self-reference)
d=json.load(open(p,encoding='utf-8')); d['end_hashes'].pop('reviews/visual-second/revision-tasks.json',None)
with open(p,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2); f.write('\n')
print('reopened',len(d['reopened_images']),'status',d['status'])
