"""Repair Z marginals on a genuine common-threshold R completion.

The old histograms, their masses, K, and every R marginal are fixed to the
latest 3889-row exact point.  Z marginals may change.  Each old histogram
is split into exact deterministic R modes by the common threshold.  Conditional
Z marginals are then affine; independent conditional bits give a genuine common
distribution.  All old rows and all sixty Z->Z index classes are imposed.
This is an extension test on this one chosen R completion, never a full-domain
half certificate or an SPE construction.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib,json,sys
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix,vstack,eye

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
OLD=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra'
sys.path.insert(0,str(OLD))
import attractive_nested as att
import full_new_reply_closure as cl
import new_reply_budget as nr
from six_stress import exact_solve

SOURCE=OLD/'attractive_nested_exact.json'
NAMES=[('Z-Z',f,g,pat) for f,g,pat in product(range(2),range(2),cl.P4)]
NI={k:i for i,k in enumerate(NAMES)}

def group_key(c):
    f,d,wi,wj=c['group'];return f,d,tuple(wi),tuple(wj)

def build():
    data=json.loads(SOURCE.read_text());histcols=[c for c in data['columns'] if c['kind']=='hist']
    cols,names,m,obj,normal=att.build(histcols)
    assert json.dumps(cols)==json.dumps([{k:v for k,v in c.items() if k!='weight'} for c in data['columns']])
    vals=[F(c['weight']) for c in data['columns']]
    byhist={};hi=None
    for j,c in enumerate(cols):
        if c['kind']=='hist':hi=j;byhist[hi]={}
        if c['kind']=='joint-reply':byhist[hi].setdefault(group_key(c),{})[tuple(c['state'])]=j
    modes=[];variables=[];constant=[F()]*len(cols);constant[0]=vals[0]
    # Variable columns are represented sparsely in old-column coordinates.
    transform=[]
    for hi,groups in byhist.items():
        mass=vals[hi];constant[hi]=mass
        if not mass:continue
        q={g:vals[s[1,0]]+vals[s[1,1]] for g,s in groups.items()}
        thresholds=sorted({F(),mass,*q.values()})
        overlap_cols=[(j,c) for j,c in enumerate(cols) if c['kind']=='overlap' and c['hist_column']==hi]
        for lo,up in zip(thresholds,thresholds[1:]):
            if lo==up:continue
            weight=up-lo;r={g:int(q[g]>=up) for g in groups}
            mi=len(modes);modes.append({'hist_column':hi,'mass':str(weight),'r':[list(g) for g in groups if r[g]]})
            for g,s in groups.items():
                if r[g]:constant[s[1,0]]+=weight
                transform.append({s[1,1]:F(1),s[1,0]:-F(1)} if r[g] else {s[0,1]:F(1)})
                variables.append({'mode':mi,'hist_column':hi,'group':g,'mass':weight,'r':r[g]})
            for j,c in overlap_cols:
                def conv(g):return g[0],g[1],tuple(g[2]),tuple(g[3])
                if all(r[conv(g)] for g in c['groups']):constant[j]+=weight
    n=len(variables)
    # Every new column is the exact coefficient vector of one conditional Z bit.
    exact=[[sum(row[j]*v for j,v in tr.items()) for tr in transform] for row in m]
    rhs=[-sum(v*x for v,x in zip(row,constant)) for row in m]
    names=list(names)+list(map(str,NAMES));extra=[[F()]*n for _ in NAMES]
    pos={}
    for j,v in enumerate(variables):pos.setdefault(v['mode'],{})[v['group']]=j
    for mi,mode in enumerate(modes):
        hi=mode['hist_column'];hc=cols[hi];a=tuple(map(int,hc['actual_bits']));pa=sum(a[:4])
        words=[w for w,count in zip(nr.PAT,hc['hist']) for _ in range(count)]
        r={g:variables[j]['r'] for g,j in pos[mi].items()}
        def group(e):return e[0],int(e[1]==e[2]),words[e[1]],words[e[2]]
        edges=[e for e in product(range(2),range(6),range(6)) if e[0] or e[1]!=e[2]]
        for e in edges:
            ge=group(e);den=pa+r[ge]+1
            for ee in edges:
                gg=group(ee);ri=NI['Z-Z',e[0],ee[0],cl.partition((*e[1:],*ee[1:]))]
                extra[ri][pos[mi][ge]]+=F(1,den)
                extra[ri][pos[mi][gg]]-=F(1,den)
    exact+=extra;rhs += [F()]*len(extra)
    return data,cols,modes,variables,names,exact,rhs

def exact_recover(mat,rhs,variables,x):
    # Active bound rows fix most columns. Eliminate those first.
    fixed={j:(F() if v<1e-9 else d['mass']) for j,(v,d) in enumerate(zip(x,variables)) if v<1e-9 or abs(v-float(d['mass']))<1e-9}
    free=[j for j in range(len(x)) if j not in fixed]
    equations=[]
    for row,bound in zip(mat,rhs):
        gap=sum(float(v)*xx for v,xx in zip(row,x))-float(bound)
        scale=max([abs(float(v)) for v in row]+[abs(float(bound)),1.])
        if abs(gap)<1e-9*scale:
            equations.append([row[j] for j in free]+[bound-sum(row[j]*v for j,v in fixed.items())])
    if free:
        got=exact_solve(equations,len(free))
        fixed.update(zip(free,got))
    z=[fixed[j] for j in range(len(x))]
    assert all(0<=v<=d['mass'] for v,d in zip(z,variables))
    slacks=[sum(v*xx for v,xx in zip(row,z))-bound for row,bound in zip(mat,rhs)]
    assert min(slacks)>=0,min(slacks)
    return z,slacks

def main():
    data,cols,modes,variables,names,exact,rhs=build()
    print('fixed R repair',len(exact),'rows',len(variables),'Z variables',len(modes),'R modes',flush=True)
    if '--verify' in sys.argv:
        saved=json.loads((HERE/'repair_zz_exact.json').read_text())
        assert saved['source_sha256']==hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        assert json.dumps(saved['modes'])==json.dumps(modes)
        assert len(saved['variables'])==len(variables)
        z=[]
        for v,s in zip(variables,saved['variables']):
            assert v['mode']==s['mode'] and json.dumps(v['group'])==json.dumps(s['group'])
            assert v['mass']==F(s['mass']);q=F(s['z_mass']);assert 0<=q<=v['mass'];z.append(q)
        slacks=[sum(v*q for v,q in zip(row,z))-b for row,b in zip(exact,rhs)]
        assert min(slacks)>=0
        out={k:saved[k] for k in ('source_sha256','fixed_W','rows','Z_variables','R_modes')}
        out['minimum_exact_slack']=str(min(slacks));out['all_rows_exactly_verified']=True
        print(json.dumps(out,indent=2));return
    a=csr_matrix(np.array(exact,dtype=float));scale=np.asarray(abs(a).max(axis=1).toarray()).ravel();scale[scale==0]=1
    sol=linprog(np.zeros(len(variables)),A_ub=-a.multiply((1/scale)[:,None]),b_ub=-np.array(rhs,dtype=float)/scale,bounds=[(0,float(v['mass'])) for v in variables],method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
    out={'scope':__doc__,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'status':sol.message,'success':bool(sol.success),'rows':len(exact),'Z_variables':len(variables),'R_modes':len(modes),'fixed_W':data['W']}
    print(json.dumps(out,indent=2),flush=True)
    if sol.success:
        z,slacks=exact_recover(exact,rhs,variables,sol.x)
        out['minimum_exact_slack']=str(min(slacks));out['modes']=modes
        out['variables']=[{'mode':v['mode'],'group':v['group'],'mass':str(v['mass']),'z_mass':str(q)} for v,q in zip(variables,z)]
        (HERE/'repair_zz_exact.json').write_text(json.dumps(out,indent=2)+'\n')
        print('exact reconstruction passes',min(slacks),flush=True)
    else:(HERE/'repair_zz_status.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
