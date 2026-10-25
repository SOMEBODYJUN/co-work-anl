"""Exact scalar versus floating vector block, plus real full-SPE replay.

The 32-state maximum-branch domain is complete by binary membership. Finite
tests validate the coefficient implementation; they do not prove HALF(5).
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import json,sys,random,hashlib
import numpy as np
import max_menu_joint_pricing as mm
import menu_ap_pricing as mp
import lift_maximum_branch as lm
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(mp.ROOT))
from customer_attraction import Instance,ExactSPESolver

def vectors():
    src=json.loads((HERE/'exact_menu_ap_primal.json').read_text());atoms=src['atoms'];U=object.__new__(mm.Universe);U.B=np.asarray(list(product((0,1),repeat=10)),dtype=float);U.SMB=np.asarray(mm.STATES,dtype=float);U.dd=np.arange(6)[None,:,None];U.m=U.SMB[:,0][None,None,:]
    names=list(mm.new_rows(atoms[0],mm.STATES[0]));rng=random.Random(130071);samples=[(rng.randrange(len(atoms)),rng.randrange(32)) for _ in range(128)];exact=[mm.new_rows(atoms[i],mm.STATES[s]) for i,s in samples]
    checks=0;maximum=0.
    for name in names:
        arr=np.broadcast_to(U.block_coeff(name),(1024,6,32))
        for k,(i,s) in enumerate(samples):
            a=atoms[i];b=int(a['bits'],2);d=sum(a['AB_hist'][4:]);val=exact[k][name]
            if ':MaxCap:' in name:
                g,_,menu=name.split(':');pos=mp.MENUS[g].index(menu)+1;ty=mp.TYPES[4 if g=='Sbranch' else 3];val+=sum(n*t[pos] for n,t in zip(a[mp.FIELDS[g]],ty))
            elif name.startswith('max:cap:oldmenu'):val+=a['menus_lh'][int(name[-1])][0]
            diff=abs(float(val)-arr[b,d,s]);maximum=max(maximum,diff);assert diff<1e-10,(name,a['bits'],d,mm.STATES[s],val,arr[b,d,s]);checks+=1
    return {'sample_states':len(samples),'rows':len(names),'scalar_vector_comparisons':checks,'maximum_absolute_error':maximum}

def original(sets):
    themes=tuple(frozenset(s) for s in sets);N=set().union(*themes);sol=ExactSPESolver(Instance.from_topic_sets(themes,5));sig=sol.worst_certificate().actions
    def finish(h):
        while len(h)<5:h=h+(sig[h],)
        return h
    def util(z,i):return sum((F(1,sum(x in themes[t] for t in z)) for x in themes[z[i]]),F(0))
    ic=0
    for dep in range(5):
        for h in product(range(len(themes)),repeat=dep):
            for t in range(len(themes)):assert util(finish(h),dep)>=util(finish(h+(t,)),dep);ic+=1
    ac=finish(());A,B,C,D,E=ac;sec=finish((A,E));third=finish((A,B,E));labels=dict(zip(mp.LABELS,(*ac,*sec[2:],*third[3:])))
    opt=max(combinations_with_replacement(range(len(themes)),5),key=lambda ts:len(set().union(*(themes[t] for t in ts))))
    paths={'AB':[finish((A,B,t)) for t in opt],'AE':[finish((A,E,t)) for t in opt],'Sbranch':[finish((A,t)) for t in opt]}
    oldlast=[[finish(pref+(t,))[-1] for t in opt] for pref in (ac[:3],sec[:3],third[:3])]
    maxroot=max(range(len(themes)),key=lambda t:len(themes[t]));mz=finish((maxroot,));sums={}
    for x in N:
        def bit(t):return int(x in themes[t])
        atom={'bits':''.join(str(bit(labels[t])) for t in mp.LABELS),'menus_lh':[(sum(bit(t) for t in men),sum(bit(t)*bit(q) for t,q in zip(men,opt))) for men in oldlast]}
        for g,field in mp.FIELDS.items():
            ty=mp.TYPES[4 if g=='Sbranch' else 3];hist=[0]*len(ty);positions=(3,4) if g!='Sbranch' else (2,3,4)
            for t,z in zip(opt,paths[g]):hist[ty.index((bit(t),)+tuple(bit(z[j]) for j in positions))]+=1
            atom[field]=hist
        rr=mm.new_rows(atom,tuple(bit(t) for t in mz))
        for n,v in rr.items():sums[n]=sums.get(n,F(0))+v
    assert min(sums.values(),default=F(0))>=0,[(n,str(v)) for n,v in sums.items() if v<0]
    return {'themes':[sorted(t) for t in themes],'actual':ac,'true_max_branch':mz,'full_IC':ic,'rows':len(sums),'minimum_exact_slack':str(min(sums.values(),default=F(0)))}

if __name__=='__main__':
    vec=vectors();cases=[original(t) for t in [[set()],[set(),{0},{0,1},{1,2}],[set(range(5)),{5},{6},{7},{8}],[{0,1},{1,2},{0,2,3},{3,4},{0,2,4}]]]
    report={'status':'passed','scope':__doc__,'vector_contract':vec,'real_SPE_cases':cases,'code_sha256':hashlib.sha256((HERE/'max_menu_joint_pricing.py').read_bytes()).hexdigest()};(HERE/'audit_max_block.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'passed','vector_contract':vec,'real_cases':len(cases),'full_IC':sum(c['full_IC'] for c in cases)},indent=2))
