"""Data-only reversible JSON policy views; no payoff, IC, or static computation."""
from pathlib import Path
import json,copy,itertools,hashlib
B=Path('/workspace/scratch/37f0f9248cfc');C=B/'boss4-next-cache';D=Path(__file__).resolve().parent
root=B/'boss4-research/archives/customer-attraction/tools/evidence/endogenous-padding-and-security-primary/original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/tail'
paths=dict(literal=C/'resumed-next-disjoint_reservation_literal_audit_four-originals/e1d49d2def95b9ad40a2/disjoint_reservation_literal_certificate.json',input_BI=C/'literal-reservation-required/e0c5edd8647cbfbf42c0/positive_depth_floor_certificate.json',previous_canonical=root/'endogenous_53_strategy.json')
values={k:json.loads(p.read_text()) for k,p in paths.items()}
def unpack(v):return v['strategy']['actions'] if 'strategy' in v else v['actions']
def meta(v):
 x=copy.deepcopy(v)
 if 'strategy' in x:del x['strategy']['actions']
 else:del x['actions']
 return x
maps={k:{tuple(r['history']):r['action'] for r in unpack(v)} for k,v in values.items()}
hs=[h for d in range(4) for h in itertools.product(range(7),repeat=d)]
for k,v in values.items():assert len(unpack(v))==len(maps[k])==400 and set(maps[k])==set(hs) and all(type(a) is int and 0<=a<7 for a in maps[k].values())
metadata={k:meta(v) for k,v in values.items()};(D/'all-nonaction-fields.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
lines=['Each row: prefix => seven actions for last topic0..6. depth0 root separately; depth1 empty-prefix row. Columns input_BI | literal | previous_canonical. All400 actions per object; original row order retained.'];blocks={}
for d in range(4):
 lines.append('DEPTH '+str(d));block=[]
 if d==0:
  row=dict(prefix=[],**{k:str(m[()]) for k,m in maps.items()});block.append(row);lines.append('root => '+' | '.join(row[k] for k in ['input_BI','literal','previous_canonical']))
 else:
  for p in itertools.product(range(7),repeat=d-1):
   row=dict(prefix=list(p),**{k:''.join(str(m[p+(a,)]) for a in range(7)) for k,m in maps.items()});block.append(row);lines.append((''.join(map(str,p)) or '_')+' => '+' | '.join(row[k] for k in ['input_BI','literal','previous_canonical']))
 blocks[str(d)]=block
(D/'all-actions-paired-view.txt').write_text('\n'.join(lines)+'\n')
view=dict(metadata=metadata,blocks=blocks,original_row_order={k:[r['history'] for r in unpack(v)] for k,v in values.items()})
for k,v in values.items():
 decoded={}
 for d,block in blocks.items():
  for row in block:
   if d=='0':decoded[()]=int(row[k])
   else:
    for a,ch in enumerate(row[k]):decoded[tuple(row['prefix'])+(a,)]=int(ch)
 restored=copy.deepcopy(metadata[k]);actions=[dict(history=h,action=decoded[tuple(h)]) for h in view['original_row_order'][k]]
 if 'strategy' in restored:restored['strategy']['actions']=actions
 else:restored['actions']=actions
 assert restored==v
(D/'reversible-action-view.json').write_text(json.dumps(view,ensure_ascii=False,indent=2)+'\n')
im,lm,cm=(maps[k] for k in ['input_BI','literal','previous_canonical'])
diffs=[dict(history=list(h),input_action=im[h],literal_action=lm[h]) for h in hs if im[h]!=lm[h]]
result=dict(scope='data-only exact action maps and JSON-object roundtrip; no payoff/IC/LP/static computation',all400_domains_equal=True,input_BI_equals_previous_canonical_policy=im==cm,literal_equals_previous_canonical_policy=lm==cm,input_to_literal_changed_actions=diffs,count=len(diffs),all_changes_in_root6_noextra6_domain=all(d['history'] and d['history'][0]==6 and 6 not in d['history'][1:] for d in diffs),metadata_equality={k:metadata['literal'].get(k)==metadata['input_BI'].get(k) for k in set(metadata['literal'])|set(metadata['input_BI'])},inputs={k:str(p) for k,p in paths.items()},sha256={k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in paths.items()})
(D/'structural-comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
