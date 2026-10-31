from pathlib import Path
import json,gzip,hashlib,collections
C=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache')
x=json.loads((C/'low-tail-required-packet-local-input/local-export-manifest.json').read_text())['rows'][0]
b=Path(x['local_path']).read_bytes();raw=gzip.decompress(b);d=json.loads(raw);nodes=d['nodes'];root=d['root'];m=d['instance']['players']
branches=[]
for a in range(len(d['instance']['topics'])):
 i=nodes[root]['children'][a];path=[a];visited=[root,i]
 while len(path)<m:
  t=nodes[i]['action'];path.append(t);i=nodes[i]['children'][t];visited.append(i)
 branches.append({'root_topic_index':a,'path':path,'selected_node_ids':visited,'terminal_counts':nodes[i]['counts']})
schemas=collections.Counter(tuple(sorted(v)) for v in nodes)
report={'kind':'input reading snapshot only; no payoff/IC/reachability verification or original audit execution','compressed_sha256':hashlib.sha256(b).hexdigest(),'compressed_bytes':len(b),'decoded_sha256':hashlib.sha256(raw).hexdigest(),'decoded_bytes':len(raw),'all_nonnode_fields':{k:v for k,v in d.items() if k!='nodes'},'node_field_schemas':[{'fields':list(k),'count':v} for k,v in schemas.items()],'node_value_types':{k:dict(collections.Counter(type(v[k]).__name__ for v in nodes if k in v)) for k in sorted(set().union(*(v.keys() for v in nodes)))},'node_count':len(nodes),'root_node':nodes[root],'six_selected_branch_paths_from_actual_input':branches,'original_math_runs':0}
(C/'tail-gap-and-low-deletion-audit-drafts/input-reading-snapshot.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'saved':'input-reading-snapshot.json','nodes_structural_metadata':len(nodes),'paths_read':len(branches),'new_IC_checks':0},ensure_ascii=False))
