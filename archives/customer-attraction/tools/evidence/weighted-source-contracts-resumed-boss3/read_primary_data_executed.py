from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib,collections,ast
r=Path('/workspace/scratch/cd4305a146e6/co-work-anl-boss3');s=Path('/workspace/scratch/cd4305a146e6/boss3-session');e=r/'archives/customer-attraction/tools/evidence/weighted-source-contracts-resumed-boss3';c=r/'cleanup/workspaces/Boss3/resume-20261102/c5';e.mkdir(parents=True,exist_ok=True);c.mkdir(parents=True,exist_ok=True);m=json.loads((s/'c5-sources.json').read_text());files={}
for q in m:
 b=(s/'source-root'/q['path']).read_bytes();assert len(b)==q['size'] and hashlib.sha256(b).hexdigest()==q['sha256'];z=e/'original'/q['path'];z.parent.mkdir(parents=True,exist_ok=True);z.write_bytes(b);files[Path(q['path']).name]=z
(e/'source-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');(c/'readonly-export-record.json').write_bytes((s/'c5-agent-exports.json').read_bytes())
def leaves(v,p='$'):
 if isinstance(v,dict):
  for k,w in v.items():yield from leaves(w,p+'.'+k)
 elif isinstance(v,list):
  for i,w in enumerate(v):yield from leaves(w,p+'['+str(i)+']')
 else:yield p,type(v).__name__,v
fields=[];reports={};compact=[]
for name,path in files.items():
 if path.suffix=='.py':ast.parse(path.read_text());continue
 if path.suffix!='.json':continue
 v=json.loads(path.read_text());zz=list(leaves(v));fields.append({'file':name,'scalar_leaves':len(zz),'types':dict(collections.Counter(t for p,t,v in zz)),'zero_numeric_leaves':sum(x==0 for p,t,x in zz if t in ('int','float')),'scalar_record':[{'path':p,'type':t,'value':x,'float_hex':x.hex() if t=='float' else None} for p,t,x in zz]});rec={'keys':list(v),'scope':v['scope'],'scalar_leaves':len(zz)}
 if 'row_names' in v:
  nn=v['row_names'];assert len(set(nn))==len(nn);rec['rows']={'count':len(nn),'families':dict(collections.Counter(x.split(':')[0] for x in nn)),'complete_indexed_names':[{'index':i,'name':x} for i,x in enumerate(nn)]}
 if 'atoms' in v:
  atoms=v['atoms'];pp=v.get('primal_float');stats=[];W=F(0);O=F(0);eW=F(0);eO=F(0);histcounts=collections.Counter()
  for i,a in enumerate(atoms):
   assert set(a)<=set(['bits','AB_hist','AE_hist','second_hist','menus_lh','exact_mass','max_bits','H_bit']);assert len(a['bits'])==10 and set(a['bits'])<=set('01') and len(a['max_bits'])==5 and set(a['max_bits'])<=set('01');ds=[];hn=[]
   for field,k in [('AB_hist',3),('AE_hist',3),('second_hist',4)]:
    z=a[field];assert len(z)==2**k and all(type(n)==int and n>=0 for n in z) and sum(z)==5;ds.append(sum(n for n,t in zip(z,product((0,1),repeat=k)) if t[0]));histcounts[field+':zero']+=sum(n==0 for n in z);histcounts[field+':nonzero']+=sum(n!=0 for n in z);hn.append(','.join(str(j)+'='+str(n) for j,n in enumerate(z) if n))
   assert ds[0]==ds[1]==ds[2];d=ds[0];assert len(a['menus_lh'])==3 and all(len(z)==2 and all(type(x)==int for x in z) and 0<=z[1]<=min(d,z[0]) and z[0]-z[1]<=5-d and 0<=z[0]<=5 for z in a['menus_lh']);assert type(a.get('H_bit',0))==int and a.get('H_bit',0) in (0,1)
   exact=F(a['exact_mass']) if 'exact_mass' in a else None;mass=F(str(pp[i])) if pp is not None else exact;assert mass is not None and mass>=0;w=int(any(map(int,a['bits'][:5])));o=int(d>0);W+=mass*w;O+=mass*o
   if exact is not None:eW+=exact*w;eO+=exact*o
   z={'index':i,'bits':a['bits'],'max_bits':a['max_bits'],'H_bit':a.get('H_bit'),'d':d,'histograms':{f:a[f] for f in ['AB_hist','AE_hist','second_hist']},'menus_lh':a['menus_lh'],'stored_exact_mass':str(exact) if exact is not None else None,'active_mass':str(mass),'active_mass_float':float(mass),'active_mass_float_hex':pp[i].hex() if pp is not None else None,'covered_actual':bool(w),'covered_comparison':bool(o),'positive_active_mass':mass>0};stats.append(z);compact.append(name+' '+str(i)+' '+a['bits']+' '+a['max_bits']+' H='+str(a.get('H_bit','-'))+' d='+str(d)+' AB['+hn[0]+'] AE['+hn[1]+'] S['+hn[2]+'] lh='+str(a['menus_lh'])+' active='+str(float(mass))+' exactdigits='+str(len(str(exact)))+' sign='+str((mass>0)-(mass<0)))
  rec['atoms']={'count':len(atoms),'positive_mass_count':sum(t['positive_active_mass'] for t in stats),'zero_mass_indices':[t['index'] for t in stats if not t['positive_active_mass']],'actual_uncovered_positive_indices':[t['index'] for t in stats if t['positive_active_mass'] and not t['covered_actual']],'stored_exact_mass_count':sum(t['stored_exact_mass'] is not None for t in stats),'W_from_active_masses':str(W),'O_from_active_masses':str(O),'O_float':float(O),'gap_O_minus_2W':str(O-2*W),'W_from_carried_exact_fields':str(eW),'O_from_carried_exact_fields':str(eO),'all_histogram_fields':dict(histcounts),'full_atoms':stats}
  if pp is None:assert len(atoms)==v['positive_atoms'] and all(t['positive_active_mass'] for t in stats) and W==1
 if 'history' in v:rec['history']=v['history'];rec['dual_multipliers_float']=v.get('dual_multipliers_float');assert set(v.get('dual_multipliers_float',{}))<=set(v['row_names'])
 if 'diagnostic_atom_bounds_float' in v:rec['full_diagnostic_fields']=v
 reports[name]=rec
(e/'json-all-fields-reviewed.json').write_text(json.dumps(fields,ensure_ascii=False,indent=2)+'\n');(e/'saved-data-review.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n');(e/'all-atom-fields-compact.txt').write_text('\n'.join(compact)+'\n')
a=json.loads(files['coupled_discovery.json'].read_text());b=json.loads(files['weighted_discovery.json'].read_text());print('ROW PREFIX DIFF',[{'index':i,'coupled':x,'weighted':y} for i,(x,y) in enumerate(zip(a['row_names'],b['row_names'])) if x!=y]);print('NEW63',b['row_names'][5421:])
for n,z in reports.items():
 t=z.get('atoms',{});print(n,'leaves',z['scalar_leaves'],'rows',z.get('rows',{}).get('count'),'atoms',t.get('count'),'positive',t.get('positive_mass_count'),'zero',t.get('zero_mass_indices'),'W',str(t.get('W_from_active_masses'))[:120],'O_float',t.get('O_float'),'gap_sign',('positive' if F(t['gap_O_minus_2W'])>0 else 'nonpositive') if t else None);print('HISTORY',z.get('history'));print('FAMILIES',z.get('rows',{}).get('families'))
