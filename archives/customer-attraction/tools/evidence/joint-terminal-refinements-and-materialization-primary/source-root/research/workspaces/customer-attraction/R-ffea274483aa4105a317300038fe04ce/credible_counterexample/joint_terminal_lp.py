"""Exact joint-index refinements of the frozen 64 histogram atoms.
All designated terminal nodes compare every fixed/indexed topic in the template.
This remains a finite support relaxation, never a real SPE assertion.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,permutations,combinations
import importlib.util,json
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5];HERE=Path(__file__).resolve().parent

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
old=load('known_old_closure_joint',ROOT/'research/workspaces/customer-attraction/R-d7f409d6a5914bdeb09875ab32618466/credible_counterexample/frozen_support_closure.py')
new=load('new_coupling_joint',HERE/'coupling_envelope_check.py')

def expanded(hist,types):
    return tuple(bits for n,bits in zip(hist,types) for _ in range(n))

def aligned_lists(hist,types,t):
    slots=[expanded([n if bits[0]==value else 0 for n,bits in zip(hist,types)],types) for value in (0,1)]
    for p0,p1 in product(*(sorted(set(permutations(slot))) for slot in slots)):
        iters=[iter(p0),iter(p1)]
        yield tuple(next(iters[value]) for value in t)

def old_assignments(ell,h,t):
    z0=[i for i,v in enumerate(t) if v==0];z1=[i for i,v in enumerate(t) if v==1]
    for c0,c1 in product(combinations(z0,ell-h),combinations(z1,h)):
        ones=set(c0+c1);yield tuple(int(i in ones) for i in range(5))

def terminal_rows(bits,menus):
    a,b,c,d,e,u,v,w,x,y=bits
    source={
      'L_actual':(tuple(a+b+c+t+1 for t in menus['T']),menus['L_actual']),
      'L_second':(tuple(a+e+u+t+1 for t in menus['T']),menus['L_second']),
      'L_third':(tuple(a+b+e+t+1 for t in menus['T']),menus['L_third']),
      'AB_S':(tuple(a+b+t+r+1 for t,r in zip(menus['T'],menus['AB_R'])),menus['AB_S']),
      'AE_S':(tuple(a+e+t+r+1 for t,r in zip(menus['T'],menus['AE_R'])),menus['AE_S']),
      'second_J':(tuple(a+t+h+i+1 for t,h,i in zip(menus['T'],menus['second_H'],menus['second_I'])),menus['second_J'])}
    rows={}
    for label,(denoms,own) in source.items():
        actual=sum((F(s,d) for s,d in zip(own,denoms)),F(0));iv=sum((F(1,d) for d in denoms),F(0))
        for target,m in menus.items():
            diag=sum((F(z,d) for z,d in zip(m,denoms)),F(0));total=sum(m)
            rows[f'joint:{label}:vs:{target}:diag']=actual-diag
            rows[f'joint:{label}:vs:{target}:offdiag']=4*actual-total*iv+diag
        for q,member in enumerate(bits):rows[f'joint:{label}:fixed:{q}']=actual-member*iv
    assert len(rows)==192
    return rows

columns=[];refinements=[]
for atom_id,atom in enumerate(new.atoms):
    bits=tuple(map(int,atom['bits']));hist=[atom[field] for field in ('AB_hist','AE_hist','second_hist')]
    base=old.namespace['evaluate'](bits,hist,atom['menus_lh'],include_second_correlations=True);assert len(base)==437
    base.update(old.module.rows(atom));assert len(base)==447
    base.update({'cross_envelope:'+k:v for k,v in new.rows(atom).items()})
    for g in ('AB','AE','second'):
        own,inv=new.source_terms(atom,g);iv=sum(inv[0]+inv[1],F(0))
        for target,counts in new.target_counts(atom).items():
            if target.startswith(g+'_'):continue
            base['cross_full:'+g+':'+target]=5*own-sum(counts)*iv
    assert len(base)==516
    AB=expanded(atom['AB_hist'],new.triples);t=tuple(slot[0] for slot in AB)
    for AE,second,*Ls in product(aligned_lists(atom['AE_hist'],new.triples,t),aligned_lists(atom['second_hist'],new.quads,t),*(old_assignments(ell,h,t) for ell,h in atom['menus_lh'])):
        menus={'T':t,'AB_R':tuple(z[1] for z in AB),'AB_S':tuple(z[2] for z in AB),'AE_R':tuple(z[1] for z in AE),'AE_S':tuple(z[2] for z in AE),'second_H':tuple(z[1] for z in second),'second_I':tuple(z[2] for z in second),'second_J':tuple(z[3] for z in second)}
        menus.update({label:tuple(L) for label,L in zip(('L_actual','L_second','L_third'),Ls)})
        row=base.copy();row.update(terminal_rows(bits,menus));columns.append(row)
        refinements.append({'parent_atom':atom_id,'AE':AE,'second':second,'L':Ls})
assert len(columns)==427,len(columns)
names=tuple(columns[0]);G=np.array([[col[name] for col in columns] for name in names],dtype=object)
w=np.array([int(any(int(b) for b in new.atoms[r['parent_atom']]['bits'][:5])) for r in refinements],dtype=object)
obj=np.array([int(any(expanded(new.atoms[r['parent_atom']]['AB_hist'],new.triples)[i][0] for i in range(5))) for r in refinements],dtype=object)
fg=np.array(G,dtype=float)
res=linprog(-np.array(obj,dtype=float),A_ub=-fg,b_ub=np.zeros(len(names)),A_eq=[np.array(w,dtype=float)],b_eq=[1],bounds=(0,None),method='highs')
assert res.success,res.message
report={'scope':'Joint-index refinements of only the frozen original 64 histogram atoms; not a full atom-space or SPE result','columns':len(columns),'rows':len(names),'floating_optimum':float(-res.fun)}
active=np.abs(fg@res.x)<1e-7
A=np.concatenate([w[None,:],G[active]]);b=[1]+[0]*int(sum(active))
primal=old.recover(A,b,res.x)
if primal is not None:
    assert min(primal)>=0 and sum(x*y for x,y in zip(w,primal))==1
    slacks=[sum(G[i,j]*primal[j] for j in range(len(primal))) for i in range(len(names))];assert min(slacks)>=0
    value=sum(x*y for x,y in zip(obj,primal))
    report.update({'exact_primal_value':str(value),'exact_primal_float':float(value),'gap_above_two':str(value-2),'positive_refinements':sum(x>0 for x in primal),'positive_projected_atoms':len({refinements[i]['parent_atom'] for i,x in enumerate(primal) if x}),'minimum_slack':str(min(slacks)),'exact_reweighting':[str(x) for x in primal],'refinements':refinements,'new_row_slacks':{name:str(v) for name,v in zip(names,slacks) if name.startswith('joint:')}})
report['exact_optimality_claimed']=False
HERE.joinpath('joint_terminal_lp.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('exact_reweighting','new_row_slacks','refinements')},indent=2))
