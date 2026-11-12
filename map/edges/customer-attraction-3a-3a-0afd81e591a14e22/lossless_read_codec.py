"""Static lossless display only: no scientific evaluator is imported or run."""
import hashlib,json,re
from pathlib import Path
ROOT=Path('/workspace/scratch/1a53a6eb65ea/co-work-anl-boss1')
OUT=Path(__file__).resolve().parent
E=ROOT/'archives/customer-attraction/tools/evidence/shared-matching-and-full-pricing-primary'
P=E/'comparison/research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_pricing/exact_primal_overlap1.json'
R=E/'new-shared-matching-and-60point-check.json'
p=json.loads(P.read_text());r=json.loads(R.read_text())
q=[];qi={};den=[];di={}
def Q(s):
    assert isinstance(s,str)
    if s not in qi:
        qi[s]=len(q)
        if '/' in s:
            n,d=s.split('/')
            if d not in di:di[d]=len(den);den.append(d)
            q.append([n,di[d]])
        else:q.append(s)
    return qi[s]
# Complete primal: literal metadata, all atoms, all slack names/values, all basis names.
pmeta={k:v for k,v in p.items() if k not in ('atoms','slacks','basis_row_names')}
atomrows=[]
for a in p['atoms']:
    assert set(a)=={'bits','AB_hist','AE_hist','second_hist','menus_lh','exact_mass'}
    assert all(type(x) is int and 0<=x<=9 for k in ('AB_hist','AE_hist','second_hist') for x in a[k])
    assert all(type(x) is int and 0<=x<=9 for row in a['menus_lh'] for x in row)
    atomrows.append([a['bits'],''.join(map(str,a['AB_hist'])),''.join(map(str,a['AE_hist'])),''.join(map(str,a['second_hist'])),''.join(str(x) for row in a['menus_lh'] for x in row),Q(a['exact_mass'])])
slackrows=[[k,Q(v)] for k,v in p['slacks'].items()]
# Complete report: preserve every metadata scalar; factor its identical 557-value object.
rmeta={k:v for k,v in r.items() if k not in ('new60','cross_pairs','selected_joint_final')}
new60={k:v for k,v in r['new60'].items() if k!='all557_slacks_recomputed'}
assert r['new60']['all557_slacks_recomputed']==p['slacks']
c=r['cross_pairs'];cmeta={k:v for k,v in c.items() if k not in ('negative_rows','totals','atom_coefficients')}
rows=list(c['totals']);totals=[Q(c['totals'][k]) for k in rows]
neg=[[k,Q(v)] for k,v in c['negative_rows'].items()]
# 13200 exact records: common 220 row labels; repeated five-orbit vectors and repeated atoms.
coeff=c['atom_coefficients'];vectors=[];vi={};matrix=[];mi={};amap=[]
for ai in range(60):
    block=coeff[ai*220:(ai+1)*220]
    assert len(block)==220 and all(x['atom']==ai and x['row']==rows[j] and set(x)=={'atom','row','upper_coefficient'} for j,x in enumerate(block))
    vals=[Q(x['upper_coefficient']) for x in block];vr=[]
    for j in range(0,220,5):
        v=tuple(vals[j:j+5])
        if v not in vi:vi[v]=len(vectors);vectors.append(list(v))
        vr.append(vi[v])
    vk=tuple(vr)
    if vk not in mi:mi[vk]=len(matrix);matrix.append(vr)
    amap.append(mi[vk])
s=r['selected_joint_final'];smeta={k:v for k,v in s.items() if k!='atom_coefficients'}
srows=[]
for i,a in enumerate(s['atom_coefficients']):
    assert a['atom']==i and set(a)=={'atom','OO','M_offdiagonal','N_offdiagonal'}
    srows.append([Q(a[k]) for k in ('OO','M_offdiagonal','N_offdiagonal')])
encoded={'format':'Exact lexical fraction dictionary: q[i] string or [numerator,denominator-index]; no arithmetic normalization. Hist and menu strings retain one decimal digit per original integer. Vectors are consecutive groups of 5 cross row positions. Each atom-map entry selects its complete 44-vector (220-value) row.','denominators':den,'fractions':q,'primal_metadata':pmeta,'atom_columns':['bits','AB_hist','AE_hist','second_hist','menus_lh_flat','exact_mass_q'],'atoms':atomrows,'slacks':slackrows,'basis_row_names':p['basis_row_names'],'report_metadata':rmeta,'new60_metadata':new60,'new60_all557_alias':'primal.slacks; exact-object equality checked','cross_metadata':cmeta,'cross_rows':rows,'cross_total_q':totals,'cross_negative_q':neg,'cross_vectors5_q':vectors,'cross_atom_matrix44':matrix,'cross_atom_map':amap,'selected_joint_metadata':smeta,'selected_joint_atom_columns':['OO_q','M_offdiagonal_q','N_offdiagonal_q'],'selected_joint_atoms':srows}
def dq(i):
    v=q[i];return v if isinstance(v,str) else v[0]+'/'+den[v[1]]
dp=dict(pmeta)
dp['atoms']=[dict(bits=a[0],AB_hist=list(map(int,a[1])),AE_hist=list(map(int,a[2])),second_hist=list(map(int,a[3])),menus_lh=[list(map(int,a[4][j:j+2])) for j in range(0,6,2)],exact_mass=dq(a[5])) for a in atomrows]
dp['slacks']={k:dq(v) for k,v in slackrows};dp['basis_row_names']=encoded['basis_row_names']
dr=dict(rmeta);dr['new60']=dict(new60,all557_slacks_recomputed=dp['slacks'])
dc=dict(cmeta,negative_rows={k:dq(v) for k,v in neg},totals={k:dq(v) for k,v in zip(rows,totals)})
dc['atom_coefficients']=[dict(atom=ai,row=rows[j],upper_coefficient=dq(v)) for ai,mid in enumerate(amap) for j,v in enumerate([z for vid in matrix[mid] for z in vectors[vid]])];dr['cross_pairs']=dc
dr['selected_joint_final']=dict(smeta,atom_coefficients=[dict(atom=i,OO=dq(a[0]),M_offdiagonal=dq(a[1]),N_offdiagonal=dq(a[2])) for i,a in enumerate(srows)])
assert dp==p and dr==r
(OUT/'complete-records-lossless.json').write_text(json.dumps(encoded,ensure_ascii=False,indent=2)+'\n')
# One display record per line, separated into fully bounded reading parts.
parts=[('01-metadata-and-atoms', ['format','primal_metadata','atom_columns','atoms','basis_row_names','report_metadata','new60_metadata','new60_all557_alias','cross_metadata','selected_joint_metadata','selected_joint_atom_columns','selected_joint_atoms']),('02-denominators', ['denominators']),('03-fractions-000-399', []),('04-fractions-400-799', []),('05-fractions-800-end', []),('06-slacks', ['slacks']),('07-cross-row-names-and-totals', ['cross_rows','cross_total_q','cross_negative_q']),('08-cross-vector-dictionary', ['cross_vectors5_q']),('09-cross-matrices-and-atom-map', ['cross_atom_matrix44','cross_atom_map'])]
for name,keys in parts:
 lines=[]
 for k in keys:
  v=encoded[k]
  if isinstance(v,list):
   lines.append(k+':')
   lines.extend(str(i)+' '+json.dumps(x,ensure_ascii=False,separators=(',',':')) for i,x in enumerate(v))
  else:lines.append(k+': '+json.dumps(v,ensure_ascii=False,separators=(',',':')))
 if 'fractions-' in name:
  lo=0 if name.startswith('03') else 400 if name.startswith('04') else 800;hi=min(lo+400,len(q)) if lo<800 else len(q)
  lines=['fractions q[%d:%d]:'%(lo,hi)]+[str(i)+' '+json.dumps(q[i],ensure_ascii=False,separators=(',',':')) for i in range(lo,hi)]
 (OUT/(name+'.txt')).write_text('\n'.join(lines)+'\n')
report={'operation':'JSON-only reversible field/dictionary factoring; no scientific rerun','originals':[{'path':str(x.relative_to(ROOT)),'sha256':hashlib.sha256(x.read_bytes()).hexdigest(),'bytes':x.stat().st_size} for x in (P,R)],'decoded_primal_equals_original':dp==p,'decoded_report_equals_original':dr==r,'all_original_fields_preserved':True,'original_557_objects_equal':p['slacks']==r['new60']['all557_slacks_recomputed'],'complete_cross_records':len(dc['atom_coefficients']),'fractions':len(q),'denominators':len(den),'vectors5':len(vectors),'matrix_rows44':len(matrix),'atom_map':len(amap)}
(OUT/'lossless-read-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2));print('display_chars',sum((OUT/(name+'.txt')).stat().st_size for name,keys in parts))
