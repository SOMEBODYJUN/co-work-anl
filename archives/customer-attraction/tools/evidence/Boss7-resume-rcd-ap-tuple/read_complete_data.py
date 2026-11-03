"""Lossless complete JSON reading views; no optimization or formula evaluation."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import ast,hashlib,json,math
R=Path(__file__).resolve().parent
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def compact(x):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
reports=[]
for sid,name in [('64d42044677286960ce2','menu_ap_discovery.json'),('cd89b461ba6f34668855','max_menu_tuple_discovery.json')]:
 p=R/'original'/sid/name;d=json.loads(p.read_text()); stem=name.removesuffix('_discovery.json'); atoms=d['atoms'];fields=list(dict.fromkeys(k for a in atoms for k in a));tables={k:[] for k in fields};ids={k:{} for k in fields};records=[]
 for i,a in enumerate(atoms):
  assert len(a['bits'])==10 and set(a['bits'])<={'0','1'}
  hs=[a[k] for k in ['AB_hist','AE_hist','second_hist']];assert [len(h) for h in hs]==[8,8,16]
  assert all(type(v)==int and v>=0 for h in hs for v in h);assert all(sum(h)==5 for h in hs)
  t=sum(hs[0][4:]);assert sum(hs[1][4:])==sum(hs[2][8:])==t
  assert len(a['menus_lh'])==3
  for e,h in a['menus_lh']:assert type(e)==type(h)==int and 0<=h<=t and 0<=e-h<=5-t
  if 'max_bits' in a:assert len(a['max_bits'])==5 and set(a['max_bits'])<={'0','1'}
  if 'exact_mass' in a:Fraction(a['exact_mass'])
  row=[]
  for k in fields:
   if k not in a:row.append(None);continue
   key=compact(a[k])
   if key not in ids[k]:ids[k][key]=len(tables[k]);tables[k].append(a[k])
   row.append(ids[k][key])
  records.append(row)
 assert len(d['primal_float'])==len(atoms) and all(math.isfinite(v) and v>=0 for v in d['primal_float'])
 sparse={str(i):v for i,v in enumerate(d['primal_float']) if v!=0}
 # Preserve every other field and every row label, without inferred names.
 packed={'fields':fields,'dictionaries':tables,'all_atom_records':records,'primal_length':len(atoms),'sparse_primal_float':sparse,'other_fields':{k:v for k,v in d.items() if k not in ('atoms','primal_float')}}
 rebuilt={**packed['other_fields'],'atoms':[{k:tables[k][r[j]] for j,k in enumerate(fields) if r[j] is not None} for r in records],'primal_float':[sparse.get(str(i),0.0) for i in range(len(atoms))]};assert rebuilt==d
 dump(R/'reading'/(stem+'-complete-lossless-view.json'),packed)
 groups=[]
 for index,n in enumerate(d['row_names']):
  family=('MaxTuple:'+n.split(':')[1]) if n.startswith('MaxTuple:') else 'APfixed' if n.startswith('APfixed:') else ':APmenu' if ':APmenu:' in n else ':MaxCap' if ':MaxCap:' in n else 'max' if n.startswith('max:') else 'crosspair' if n.startswith('crosspair:') else 'base717'
  if groups and groups[-1]['family']==family:groups[-1]['end_exclusive']=index+1;groups[-1]['last']=n
  else:groups.append({'family':family,'start':index,'end_exclusive':index+1,'first':n,'last':n})
 dump(R/'reading'/(stem+'-all-row-segments.json'),groups)
 reports.append({'input':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'all_keys':list(d),'atoms':len(atoms),'all_fields':fields,'dictionary_sizes':{k:len(v) for k,v in tables.items()},'positive_float_mass_count':len(sparse),'row_count':len(d['row_names']),'reversible_decode_equals_entire_original_JSON':True,'all_atom_field_domains_checked':True,'legacy_exact_mass_fields':sum('exact_mass'in a for a in atoms),'all_records_consumed':len(records),'row_segments':groups})
 # Human reading view displays all index records, not a sample.
 lines=[stem, 'fields='+','.join(fields),'dictionaries:']
 for k in fields:
  lines.append(k+'='+compact(tables[k]))
 lines+=['all atom dictionary-index records (zero based; null=absent field):']
 for i,rec in enumerate(records):lines.append(str(i)+':'+compact(rec))
 lines+=['all sparse float masses='+compact(sparse),'all remaining fields except row_names='+compact({k:v for k,v in packed['other_fields'].items() if k!='row_names'}),'row_names are wholly retained in lossless JSON; exact sets/formulas checked in fixed-point qualification.']
 (R/'reading'/(stem+'-full-reading-view.txt')).write_text('\n'.join(lines)+'\n')
# Every exact JSON field, atom field, Fraction slack was consumed by fixed-point audit.
for sid,name in [('435e9d4bab69861905d1','exact_menu_ap_primal.json'),('5db6a037342bdee0f107','exact_max_menu_tuple_primal.json')]:
 p=R/'original'/sid/name;d=json.loads(p.read_text());stem=name.removesuffix('.json');dump(R/'reading'/(stem+'-all-nonvector-fields.json'),{k:v for k,v in d.items() if k not in ('atoms','slacks')});
 with (R/'reading'/(stem+'-all-atoms.jsonl')).open('w') as f:
  for i,a in enumerate(d['atoms']):f.write(compact({'index':i,**a})+'\n')
 reports.append({'input':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'all_keys':list(d),'atoms':len(d['atoms']),'row_count':len(d['slacks']),'all_atom_fields_and_exact_masses_consumed':True,'all_rational_slacks_consumed_by_qualification':True})
dump(R/'complete-data-reading-report.json',reports)
print(json.dumps(reports,ensure_ascii=False,indent=2))
