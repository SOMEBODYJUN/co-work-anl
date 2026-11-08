from __future__ import annotations
import json, hashlib, re, os
from pathlib import Path
ROOT=Path('/workspace/scratch/bfe3660cf3cd/p25-register-v2')
OUT=ROOT/'research/workspaces/p25-register-v2/Boss7/agent-remote-0002-0094-0102'
OUT.mkdir(parents=True,exist_ok=True)
BASELINE_FULL=json.load(open(ROOT/'research/registration/baseline.json'))
BASELINE={'path':'research/registration/baseline.json','sha256':hashlib.sha256((ROOT/'research/registration/baseline.json').read_bytes()).hexdigest()}
TASKS={
 'register-ab98f323ad-0002': ROOT/'research/operations/p25-register-v2/tasks/register-ab98f323ad-0002.json',
 'register-ab98f323ad-0094': ROOT/'research/operations/p25-register-v2/tasks/register-ab98f323ad-0094.json',
 'register-ab98f323ad-0102': ROOT/'research/operations/p25-register-v2/tasks/register-ab98f323ad-0102.json',
}
FRAGS={
 'register-ab98f323ad-0002':[ROOT/'research/registration/Boss2/0002/partial-batch.json'],
 'register-ab98f323ad-0094':[ROOT/'research/workspaces/p25-register-v2/Boss2/0094/pk-fragment.json'],
 'register-ab98f323ad-0102':[ROOT/'research/workspaces/p25-register-v2/Boss2/0102/root-fragment.json',ROOT/'research/workspaces/p25-register-v2/Boss2/0102/resume-review/closed-cycle-correction.json'],
}
NOTES={
 'register-ab98f323ad-0002':ROOT/'research/registration/Boss2/0002/handoff.md',
 'register-ab98f323ad-0094':ROOT/'research/workspaces/p25-register-v2/Boss2/0094/build_pk_fragment.py',
 'register-ab98f323ad-0102':ROOT/'research/workspaces/p25-register-v2/Boss2/0102/resume-review/independent-review.md',
}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def headings(p):
    out=[]
    try:
      for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
        s=line.strip()
        if re.match(r'^#{1,6}\s+',s) or re.match(r'^(?:[一二三四五六七八九十]+[、.]|\d+(?:\.\d+)*[、.)])\s*',s):
          out.append({'line':i,'text':s[:300]})
    except Exception: pass
    return out
def refdict(r):
    if isinstance(r,dict): return r
    return {'path':r}
def resolve_path(s):
    p=ROOT/s
    if p.exists(): return p
    # Candidate fragments may use archive-relative references.
    p=ROOT/'archives/customer-attraction/state'/s
    if p.exists(): return p
    p=ROOT/'archives/customer-attraction'/s
    if p.exists(): return p
    p=ROOT/'archives/unrelated-machines/state'/s
    if p.exists(): return p
    p=ROOT/'archives/positive-kernels'/s
    if p.exists(): return p
    return ROOT/s

def load_fragments(task):
    objs=[]; src=[]
    for f in FRAGS[task]:
      d=json.load(open(f)); src.append(str(f.relative_to(ROOT)))
      for o in d.get('objects',[]):
        # correction fragment supersedes root variant on same stable ID
        objs=[x for x in objs if x.get('object_id')!=o.get('object_id')]
        objs.append(o)
    return objs,[ROOT/x for x in src]

def obj_refs(o):
    rs=[]
    if isinstance(o.get('body'),dict): rs.append(('body',o['body']))
    for i,r in enumerate(o.get('evidence',[]) or []): rs.append((f'evidence[{i}]',r))
    return rs

def material_record(idx,m,objects,task):
    p=resolve_path(m['path']); actual=sha(p) if p.exists() and p.is_file() else None
    links=[]; roles=[]
    for o in objects:
      for role,r in obj_refs(o):
        rd=refdict(r)
        if rd.get('path')==m['path']:
          links.append(o['object_id']); roles.append({'object_id':o['object_id'],'role':role,'section':rd.get('section')})
    if task.endswith('0002'):
      read_state='candidate-partial-read' if idx in list(range(13))+[20,34,36] else 'deferred-unread'
    elif task.endswith('0094'):
      read_state='candidate-root-read' if 23<=idx<=29 else 'deferred-unread'
    else:
      read_state='boss2-root-claimed-read' if idx<=18 else 'deferred-or-partial'
    if links:
      disp='objects' if any(x['role']=='body' for x in roles) else 'attachment'
    else:
      disp='deferred'
    reason={
      'candidate-partial-read':'Boss2 handoff marks this index as continuously read; candidate is partial and not publishable.',
      'candidate-root-read':'Boss2 PK fragment explicitly reads task indices 23–29; candidate is an attachment/identity draft.',
      'boss2-root-claimed-read':'Boss2 root fragment/independent review claims root read through index 18; no complete final mapping in fragment.',
      'deferred-unread':'No complete candidate mapping in the available Boss2 fragment; do not infer disposition from location alone.',
      'deferred-or-partial':'No complete final mapping in the available Boss2 fragment; independent review records partial/targeted reading only.',
    }[read_state]
    return {
      'index':idx,'path':m['path'],'frozen_sha256':m['sha256'],'actual_sha256':actual,
      'sha_match':actual==m['sha256'],'bytes':p.stat().st_size if p.exists() else None,
      'line_count':len(p.read_text(encoding='utf-8').splitlines()) if p.exists() and p.is_file() else None,
      'headings':headings(p) if p.exists() and p.is_file() else [],
      'read_state':read_state,'disposition':disp,'object_ids':sorted(set(links)),
      'object_links':roles,'reason':reason,
    }

def make_batch(task,objects,mats):
  # preserve standard shape while retaining explicit draft status in object objections/material reasons.
  clean=[]
  for o in objects:
    x=json.loads(json.dumps(o,ensure_ascii=False))
    x.setdefault('version',1)
    x.setdefault('evidence',[]); x.setdefault('sources',[])
    clean.append(x)
  return {'schema':2,'baseline':BASELINE,'objects':clean,'materials':mats,'edge_files':[]}

def make_receipt(task,batch_rel,objects,mats,frag_paths,note_path):
  bpath=ROOT/batch_rel
  return {
    'batch_file':{'path':batch_rel,'sha256':sha(bpath)},
    'assets':[{'path':batch_rel,'sha256':sha(bpath)}],
    'status':'local-candidate-incomplete-not-pushed',
    'task_id':task,'owner':'Boss2','reviewer':'Boss7','source_fragments':frag_paths,
    'source_fragment_sha256':[{ 'path':p,'sha256':sha(ROOT/p)} for p in frag_paths],
    'handoff_note':{'path':str(note_path.relative_to(ROOT)),'sha256':sha(note_path)},
    'edge_files':[],
    'objects_count':len(objects),'materials_count':len(mats),
    'material_sha_mismatches':[m['path'] for m in mats if not m['sha_match']],
    'material_read_summary':{
      'candidate_mapped':sum(1 for m in mats if m['disposition'] in ('objects','attachment')),
      'deferred':sum(1 for m in mats if m['disposition']=='deferred'),
      'sha_matches':sum(1 for m in mats if m['sha_match']),
      'sha_total':len(mats),
    },
    'review_limits':[
      'Draft only: no official task-file mutation, no registry mutation, no queue action, no checkpoint/push.',
      'Boss2 fragments are preserved as candidate evidence; stable IDs are reused where present and conflicts are flagged.',
      'A deferred material has no inferred object identity; it must be read and routed before publish.',
    ],
  }

all_audit={'schema':1,'actor':'Boss7','workflow_run':'p25-register-v2','branch':'rebuild/research-v2','baseline':BASELINE,'tasks':[],'generated_from_commit':__import__('subprocess').check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()}
for task,tp in TASKS.items():
 d=json.load(open(tp)); definition=d['definition']; objs,frag_abs=load_fragments(task); frag_rel=[str(Path(x).relative_to(ROOT)) for x in frag_abs]
 mats=[material_record(i,m,objs,task) for i,m in enumerate(definition['materials'])]
 # add stable explicit sections from body/evidence refs to material links if candidate section is available.
 task_a={
  'task_id':task,'owner':d.get('owner'),'state':d.get('state'),'request_id':d.get('request_id'),
  'baseline':definition.get('baseline'),'goal':definition.get('goal'),'frozen_material_count':len(definition['materials']),
  'source_fragments':frag_rel,'handoff_note':str(NOTES[task].relative_to(ROOT)),
  'object_count':len(objs),'object_ids':[o.get('object_id') for o in objs],
  'objects':[], 'materials':mats,
  'read_scope_claims':{
   '0002':'Boss2 handoff: indices 0–12,20,34,36 plus shared definitions; all others not full-read.',
   '0094':'Boss2 build script and fragment: indices 23–29 only; remaining materials not read in this fragment.',
   '0102':'Boss2 root fragment: indices 0–18 claimed read; independent-review says M19–M41 partial/targeted and fragment is not final deliverable.'
  }[task[-4:]],
  'status':'local-audit-incomplete',
 }
 for o in objs:
   oa={'object_id':o.get('object_id'),'version':o.get('version'),'title':o.get('title'),'kind':o.get('kind'),'truth_status':o.get('truth_status'),'body':None,'evidence':[],'stable_id_route':'reuse-existing-or-new-candidate-needs-lead-dedup'}
   for role,r in obj_refs(o):
     rd=refdict(r); p=resolve_path(rd.get('path','')); rec={'role':role,'path':rd.get('path'),'section':rd.get('section'),'expected_sha256':rd.get('sha256'),'actual_sha256':sha(p) if p.exists() and p.is_file() else None,'sha_match':(p.exists() and p.is_file() and sha(p)==rd.get('sha256')),'headings':headings(p) if p.exists() and p.is_file() else []}
     if role=='body': oa['body']=rec
     else: oa['evidence'].append(rec)
   # direct existing canonical test
   reg=json.load(open(ROOT/'research/registry.json'))
   oa['already_in_registry']=any(x.get('object_id')==o.get('object_id') for x in reg.get('objects',[]))
   oa['notes']=o.get('objections')
   task_a['objects'].append(oa)
 all_audit['tasks'].append(task_a)
 # write batch first then receipt hash
 short=task.split('-')[-1]
 batch_rel=f'research/workspaces/p25-register-v2/Boss7/agent-remote-0002-0094-0102/candidate-{short}-batch.json'
 receipt_rel=f'research/workspaces/p25-register-v2/Boss7/agent-remote-0002-0094-0102/candidate-{short}-receipt.json'
 json.dump(make_batch(task,objs,mats),open(ROOT/batch_rel,'w'),ensure_ascii=False,indent=2); open(ROOT/batch_rel,'a').write('\n')
 json.dump(make_receipt(task,batch_rel,objs,mats,frag_rel,NOTES[task]),open(ROOT/receipt_rel,'w'),ensure_ascii=False,indent=2); open(ROOT/receipt_rel,'a').write('\n')
# write audit after all batches
json.dump(all_audit,open(OUT/'audit.json','w'),ensure_ascii=False,indent=2); open(OUT/'audit.json','a').write('\n')
print('wrote',OUT/'audit.json')
for p in sorted(OUT.glob('candidate-*')): print(p.name,sha(p))
