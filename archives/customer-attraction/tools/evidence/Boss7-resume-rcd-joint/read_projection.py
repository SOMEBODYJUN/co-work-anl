import json,pathlib,itertools,collections,hashlib
from fractions import Fraction as F
S=pathlib.Path(__file__).resolve().parent;P=S/'original'
d=json.loads((P/'max_menu_joint_discovery.json').read_text());e=json.loads((P/'exact_max_menu_joint_primal.json').read_text())
fields=['bits','AB_hist','AE_hist','second_hist','menus_lh','exact_mass']
pools={};look={}
for k in fields:
 vals=[]; ix={}
 for a in d['atoms']+e['atoms']:
  v=a.get(k);key=json.dumps(v,separators=(',',':'))
  if key not in ix:ix[key]=len(vals);vals.append(v)
 pools[k]=vals;look[k]=ix
enc=lambda a:[look[k][json.dumps(a.get(k),separators=(',',':'))] for k in fields]
runs=[]
for key,g in itertools.groupby(enumerate(d['atoms']),key=lambda ia:enc(ia[1])):
 items=list(g);mb=[a['max_bits'] for _,a in items];runs.append({'start':items[0][0],'n':len(items),'old_indices':key,'max_bits':'all32lex' if mb==[f'{i:05b}' for i in range(32)] else mb})
rebuilt=[]
for run in runs:
 base={k:pools[k][i] for k,i in zip(fields,run['old_indices']) if k!='exact_mass' or pools[k][i] is not None}
 mb=[f'{i:05b}' for i in range(32)] if run['max_bits']=='all32lex' else run['max_bits']
 rebuilt += [dict(base,max_bits=m) for m in mb]
assert rebuilt==d['atoms']
assert list(e['slacks'])==d['row_names']
float_nonzero=[[i,v] for i,v in enumerate(d['primal_float']) if v!=0]
assert len(float_nonzero)==66 and len(d['primal_float'])==2434
ext=[{'indices':enc(a),'max_bits':a['max_bits']} for a in e['atoms']]
assert [{**{k:pools[k][i] for k,i in zip(fields,a['indices'])},'max_bits':a['max_bits']} for a in ext]==e['atoms']
out={'encoding':'Zero-based field pools. Original atoms recovered by run expansion; all coordinates not in float_nonzero are explicitly zero. Exact slacks retained losslessly in original and separately parsed as Fractions, not summarized-away.','pools':pools,'discovery_other_fields':{k:v for k,v in d.items() if k not in ['atoms','row_names','primal_float']},'discovery_runs':runs,'float_coordinate_count':2434,'float_nonzero':float_nonzero,'exact_atoms':ext,'row_names':d['row_names'],'exact_other_fields':{k:v for k,v in e.items() if k not in ['atoms','slacks']},'slacks':e['slacks'],'roundtrip_atom_equality':True}
(S/'complete-field-projection.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('POOLS')
for k,v in pools.items():
 if k=='exact_mass':continue
 print(k, json.dumps(v,separators=(',',':')))
print('RUNS start,n,old_indices,max_bits')
for r in runs:print(r['start'],r['n'],r['old_indices'],r['max_bits'])
print('NONZERO_FLOATS')
for z in float_nonzero:print(z)
print('EXACT66 indices,max_bits,mass')
for a in e['atoms']:print(enc(a)[:5],a['max_bits'],a['exact_mass'])
print('EXACT_SLACKS parsed',len([F(v) for v in e['slacks'].values()]),'min',min(map(F,e['slacks'].values())),'zero',sum(F(v)==0 for v in e['slacks'].values()))
print('TOPLEVEL',out['exact_other_fields'],out['discovery_other_fields'])
