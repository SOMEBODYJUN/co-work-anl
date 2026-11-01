from pathlib import Path
import json,hashlib,copy,itertools
C=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache');out=C/'jz-input-reading-prework';out.mkdir(exist_ok=True)
m=json.loads((C/'learning-jz-true-inputs-and-frozen-outputs/local-export-manifest.json').read_text());by={x['path']:x for x in m['rows']};summary=[]
for x in m['rows']:
 if not x['path'].startswith('examples/'):continue
 name=Path(x['path']).stem;cx=by['evidence/certificates/customer_attraction/'+name+'.json'];data=json.loads(Path(x['local_path']).read_text());raw=json.loads(Path(cx['local_path']).read_text());cert=raw.get('strategy',raw.get('certificate',raw));entries=cert['actions'];policy={tuple(e['history']):e['action'] for e in entries};p=len(data['topics']);n=data['players'];assert len(policy)==len(entries) and set(policy)=={h for k in range(n) for h in itertools.product(range(p),repeat=k)} and all(0<=a<p for a in policy.values())
 ids={};nodes=[]
 def build(h):
  if len(h)==n:return -1
  sig=(policy[h],tuple(build(h+(a,)) for a in range(p)))
  if sig not in ids:ids[sig]=len(nodes);nodes.append({'id':len(nodes),'action':sig[0],'children_by_label':list(sig[1])})
  return ids[sig]
 root=build(())
 reconstructed={}
 def expand(k,h):
  if k==-1:return
  node=nodes[k];reconstructed[h]=node['action']
  for a,child in enumerate(node['children_by_label']):expand(child,h+(a,))
 expand(root,());assert reconstructed==policy
 meta=copy.deepcopy(raw);dest=meta.get('strategy',meta.get('certificate',meta));dest['actions']={'lossless_read_representation':name+'-policy-dag.json','original_entries':len(entries),'unique_subtree_nodes':len(nodes),'roundtrip_all_history_action_pairs_equal':True}
 report={'schema':'lossless-policy-subtree-dedup-for-complete-reading-not-SPE-audit','name':name,'source_certificate_id':cx['id'],'source_sha256':cx['sha256'],'players':n,'topic_count':p,'root':root,'nodes':nodes,'all_history_entries':len(entries),'roundtrip_exact':True,'source_entry_extra_keys':sorted({k for e in entries for k in e if k not in ['history','action']})};assert report['source_entry_extra_keys']==[]
 (out/(name+'-policy-dag.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(out/(name+'-certificate-metadata.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');summary.append({'name':name,'input_id':x['id'],'certificate_id':cx['id'],'all_entries':len(entries),'DAG_nodes':len(nodes),'dag_bytes':(out/(name+'-policy-dag.json')).stat().st_size,'metadata_bytes':(out/(name+'-certificate-metadata.json')).stat().st_size,'actual_path_not_evaluated':True,'SPE_ICs_not_checked':True})
(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2))
