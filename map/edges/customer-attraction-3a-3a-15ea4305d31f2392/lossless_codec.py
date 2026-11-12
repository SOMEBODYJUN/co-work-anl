"""Pure JSON/SHA reading codec; does not import or execute scientific code.
The view names every source field and value, using exact dictionaries and recipes.
Decoder must compare == parsed source JSON before views are treated as complete.
"""
import json,pathlib,hashlib,itertools,re,sys
ROOT=pathlib.Path('/workspace/scratch/1a53a6eb65ea/co-work-anl-boss1')
OUT=pathlib.Path(__file__).resolve().parent
contract=json.loads((OUT/'initial-contract.json').read_text())
REFS=contract['source_refs']; SRC=[json.loads((ROOT/x['path']).read_text()) for x in REFS[7:]]
def compact(v):return json.dumps(v,ensure_ascii=False,separators=(',',':'))
def rle(xs):
 out=[]
 for v,g in itertools.groupby(xs,key=compact):
  z=list(g);out.append(z[0] if len(z)==1 else {'repeat':len(z),'value':z[0]})
 return out
def unrle(xs):
 out=[]
 for x in xs:
  out.extend([x['value']]*x['repeat'] if isinstance(x,dict) and set(x)=={'repeat','value'} else [x])
 return out
class DictCodec:
 def __init__(self):self.q=[];self.d=[]
 def enc(self,x):
  if isinstance(x,str) and re.fullmatch(r'-?\d+(?:/\d+)?',x):
   if x not in self.q:self.q.append(x)
   return {'q':self.q.index(x)}
  if isinstance(x,list):return [self.enc(v) for v in x]
  if isinstance(x,dict):return {k:self.enc(v) for k,v in x.items()}
  return x
 def dec(self,x):
  if isinstance(x,dict) and set(x)=={'q'}:return self.q[x['q']]
  if isinstance(x,list):return [self.dec(v) for v in x]
  if isinstance(x,dict):return {k:self.dec(v) for k,v in x.items()}
  return x
 def viewq(self):
  lines=['Q dictionary: qN is the exact original canonical rational STRING; numerator@dN means numerator/denominator[dN]. Integers retain their string type.']
  for x in self.q:
   if '/' in x:
    d=x.split('/')[1]
    if d not in self.d:self.d.append(d)
  lines += [f'd{i}={d}' for i,d in enumerate(self.d)]
  lines += [f'q{i}='+ (x.split('/')[0]+'@d'+str(self.d.index(x.split('/')[1])) if '/' in x else '"'+x+'"') for i,x in enumerate(self.q)]
  return '\n'.join(lines)
# 8: every column, including zero columns, follows one of four exact schemas.
p=SRC[0]; C=p['columns']; point=DictCodec(); G=[]; blocks=[]
for i,c in enumerate(C):
 if c['kind']=='hist':
  block={'column':i,'hist':{k:v for k,v in c.items() if k!='weight'},'old_hist_column':None,'groups':[]};blocks.append(block)
 elif c['kind']=='joint-reply':
  g=c['group']
  if g not in G:G.append(g)
  block['old_hist_column']=c['hist_column_old']
  if c['state']==[0,1]:block['groups'].append(G.index(g))
P={'metadata':point.enc({k:v for k,v in p.items() if k!='columns'}),'group_dictionary':G,'hist_blocks':blocks,'weights_default':'0','nonzero_weights':[[i,point.enc(c['weight'])] for i,c in enumerate(C) if c['weight']!='0'], 'column_recipe':'K at 0; for each hist_block append its hist, then for each group in its listed order joint-reply with hist_column_old and states [0,1],[1,0],[1,1]; after all hist blocks append overlap columns by block order and itertools.combinations(block.groups,2) order, hist_column=current hist index. Assign weight 0 then sparse nonzero_weights. All original descriptor keys are explicit in decoder.'}
def decodepoint(P):
 cols=[{'kind':'K'}]
 for b in P['hist_blocks']:
  assert len(cols)==b['column'];cols.append(b['hist'].copy())
  for gi in b['groups']:
   for st in [[0,1],[1,0],[1,1]]:cols.append({'kind':'joint-reply','hist_column_old':b['old_hist_column'],'group':P['group_dictionary'][gi],'state':st})
 for b in P['hist_blocks']:
  for a,z in itertools.combinations(b['groups'],2):cols.append({'kind':'overlap','hist_column':b['column'],'groups':[P['group_dictionary'][a],P['group_dictionary'][z]]})
 for c in cols:c['weight']='0'
 for i,w in P['nonzero_weights']:cols[i]['weight']=point.dec(w)
 return {**point.dec(P['metadata']),'columns':cols}
assert decodepoint(P)==p
(OUT/'source08-codec.json').write_text(json.dumps({'rationals':point.q,'representation':P},ensure_ascii=False,indent=2)+'\n')
(OUT/'source08-full-view.txt').write_text('SOURCE08 complete parsed-JSON view. '+P['column_recipe']+'\n'+point.viewq()+'\n'+compact(P)+'\n')
# 9: exact row names; compress only two deterministic name families.
s=SRC[1]; rows=s['ordered_rows']; slack=DictCodec()
S={'metadata':slack.enc({k:v for k,v in s.items() if k!='ordered_rows'}),'row_name_blocks':[],'slack_ids':[]}
for a,z in [(0,1277),(3889,3967),(4927,4963)]:S['row_name_blocks'].append({'start_index':a,'names':[x['name'] for x in rows[a:z]]})
S['row_name_blocks'].append({'start_index':1277,'recipe':'for every point overlap column in ascending current index, emit overlap-upper:{column}:{repr((f,diag,tuple(w),tuple(v)))} for its first then second listed group; exactly 2612 names'})
S['row_name_blocks'].append({'start_index':3967,'recipe':'old-priced:'+str((0,1,0,'all','Fraction placeholders')),'cartesian_order':{'i':[0,1,2,3],'member':[1,2],'qi':[0,1,2],'mode':['all','last'],'aa':['0','1/8','1/4','1/2','1'],'mu':['0','1/2','1','2']},'format':"old-priced:({i}, {member}, {qi}, '{mode}', Fraction({aa_numerator}, {aa_denominator}), Fraction({mu_numerator}, {mu_denominator}))"})
for x in rows:S['slack_ids'].append(slack.enc(x['slack'])['q'])
S['slack_ids']=rle(S['slack_ids'])
def decodeslacks(S):
 names=[None]*4963
 for b in S['row_name_blocks']:
  a=b['start_index']
  if 'names' in b:ns=b['names']
  elif a==1277:
   ns=[]
   for i,c in enumerate(C):
    if c['kind']=='overlap':
     for f,d,w,v in c['groups']:ns.append(f'overlap-upper:{i}:'+repr((f,d,tuple(w),tuple(v))))
  else:
   from fractions import Fraction
   ns=[]
   for i,m,q,mode,aa,mu in itertools.product(*b['cartesian_order'].values()):ns.append('old-priced:'+repr((i,m,q,mode,Fraction(aa),Fraction(mu))))
  names[a:a+len(ns)]=ns
 ids=unrle(S['slack_ids'])
 return {**slack.dec(S['metadata']),'ordered_rows':[{'index':i,'name':n,'slack':slack.q[q]} for i,(n,q) in enumerate(zip(names,ids))]}
assert decodeslacks(S)==s
(OUT/'source09-codec.json').write_text(json.dumps({'rationals':slack.q,'representation':S},ensure_ascii=False,indent=2)+'\n')
parts=[slack.viewq()]
parts += ['S.metadata='+compact(S['metadata'])]
for b in S['row_name_blocks']:
 if 'names' in b:parts += ['NAME '+str(b['start_index']+i)+'='+v for i,v in enumerate(b['names'])]
 else:parts += [compact(b)]
parts += ['SLACK_IDS in row-index order; repeat has literal run semantics: '+compact(S['slack_ids'])]
(OUT/'source09-full-view.txt').write_text('\n'.join(parts)+'\n')
# 10: descriptors and repeated exact masses are references, not recomputations.
a=SRC[2]; audit=DictCodec(); H=[c for c in C if c['kind']=='hist']; JO=[(i,c) for i,c in enumerate(C) if c['kind']=='joint-reply'];OV=[(i,c) for i,c in enumerate(C) if c['kind']=='overlap']
A={'metadata':audit.enc({k:v for k,v in a.items() if k not in ['histograms','reply_groups','overlap_records','frechet_lower_violations']}),'histogram_extras':[],'reply_extras':[],'overlap_values':[],'frechet_lower_violation_columns':[x['column'] for x in a['frechet_lower_violations']]}
for x in a['histograms']:A['histogram_extras'].append([x['column'],x['old_hist_column'],x['reply_groups'],x['positive_joint_states']])
for x in a['reply_groups']:A['reply_extras'].append([x['ordered_edge_multiplicity'],audit.enc(x['implicit00']),audit.enc(x['R']),audit.enc(x['Z'])])
for x in a['overlap_records']:A['overlap_values'].append(audit.enc([x['overlap'],*x['R_masses'],*x['upper_slacks'],x['frechet_lower_slack'],x['nested_maximum_gap']]))
A['overlap_values']=rle(A['overlap_values'])
A['recipe']='histograms: point hist descriptor/weight plus column,old_hist_column,reply_groups,positive_joint_states extras. reply_groups: point hist/current/old/group order, first joint column j has state_columns 01:j,10:j+1,11:j+2, corresponding state_masses copied from point; extras supply ordered_edge_multiplicity,implicit00,R,Z. overlap_records: point overlap column index/hist/groups plus seven values in order overlap,R_masses[0,1],upper_slacks[0,1],frechet_lower_slack,nested_maximum_gap. frechet_lower_violations are exact full overlap_records selected by listed column, not recomputed.'
def decodeaudit(A):
 hs=[]
 for col,old,groups,pos in A['histogram_extras']:
  x=C[col];hs.append({'column':col,'old_hist_column':old,**{k:x[k] for k in ['actual_bits','hist','d','weight']},'reply_groups':groups,'positive_joint_states':pos})
 rs=[];groups=[(JO[i][0],JO[i][1]) for i in range(0,len(JO),3)]
 for (j,c),(m,iz,R,Z) in zip(groups,A['reply_extras']):
  hc=next(b['column'] for b in blocks if b['old_hist_column']==c['hist_column_old']);rs.append({'hist_column':hc,'hist_column_old':c['hist_column_old'],'group':c['group'],'ordered_edge_multiplicity':m,'state_columns':dict(zip(['01','10','11'],[j,j+1,j+2])),'state_masses':dict(zip(['01','10','11'],[C[k]['weight'] for k in [j,j+1,j+2]])),'implicit00':audit.dec(iz),'R':audit.dec(R),'Z':audit.dec(Z)})
 os=[]
 for (i,c),vals in zip(OV,unrle(A['overlap_values'])):
  v=audit.dec(vals);os.append({'column':i,'hist_column':c['hist_column'],'groups':c['groups'],'overlap':v[0],'R_masses':v[1:3],'upper_slacks':v[3:5],'frechet_lower_slack':v[5],'nested_maximum_gap':v[6]})
 by={x['column']:x for x in os}
 return {**audit.dec(A['metadata']),'histograms':hs,'reply_groups':rs,'overlap_records':os,'frechet_lower_violations':[by[i] for i in A['frechet_lower_violation_columns']]}
assert decodeaudit(A)==a
(OUT/'source10-codec.json').write_text(json.dumps({'rationals':audit.q,'representation':A},ensure_ascii=False,indent=2)+'\n')
(OUT/'source10-full-view.txt').write_text('SOURCE10 all fields/values via exact point links: '+A['recipe']+'\n'+audit.viewq()+'\n'+compact(A)+'\n')
# 11/12 direct compact JSON: every key/value, without omission.
for i,j in [(11,SRC[3]),(12,SRC[4])]:
 (OUT/f'source{i:02}-full-view.txt').write_text(json.dumps(j,ensure_ascii=False,indent=1)+'\n')
verification={'method':'parse JSON; decode representations; equality against complete original JSON. No scientific row/audit/LP/SPE execution.','results':[{'source':REFS[7+i],'decode_equals_original_json':True,'top_fields':len(x)} for i,x in enumerate(SRC)],'view_files':[{ 'path':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(OUT.glob('source*-full-view.txt'))]}
(OUT/'codec-verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(verification,ensure_ascii=False,indent=2))
