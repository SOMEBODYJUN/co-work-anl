"""Joint reply atoms for the 16 frozen old histograms, including all Z->Z.

An atom sets a common R and Z membership bit for every reply orbit.  This is
a valid restricted subset of joint distributions, not a full-domain model.
Thus an exact sub-half feasible point is an obstruction for these row families;
an infeasible atom search is not a half proof.  No game/SPE is constructed.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import argparse, json, sys, time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack, hstack

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
SOURCE=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra'
sys.path.insert(0,str(SOURCE))
import attractive_nested as at
import full_new_reply_closure as cl
import new_reply_budget as nr
from six_stress import exact_solve

ZZ_NAMES=[('Z-Z',f,g,pat) for f,g,pat in product(range(2),range(2),cl.P4)]
ZI={n:i for i,n in enumerate(ZZ_NAMES)}

def model():
    started=time.time()
    data=json.loads((SOURCE/'attractive_nested_exact.json').read_text())
    hc=[c for c in data['columns'] if c['kind']=='hist']
    cols,names,m,obj,norm=at.build(hc)
    print('built original lifted matrix',len(m),len(cols),'seconds',time.time()-started,flush=True)
    keep=[i for i,n in enumerate(names) if not n.startswith(('joint-state-upper:','overlap-upper:'))]
    names=[names[i] for i in keep]+[str(n) for n in ZZ_NAMES]
    # Store exact local multilinear row coefficients. The last two axes on Q
    # are R,Z for mixed terms and R,R for overlap terms respectively.
    kcol=[m[i][0] for i in keep]+[F()]*len(ZZ_NAMES)
    nold=len(keep); nrows=len(names); locals=[]
    hi=None;details={}
    for j,c in enumerate(cols):
        if c['kind']=='hist':hi=j;details[hi]={'hist':c,'groups':{},'overlaps':{}}
        elif c['kind']=='joint-reply':
            f,diag,wi,wj=c['group'];g=(f,diag,tuple(wi),tuple(wj))
            details[hi]['groups'].setdefault(g,{})[tuple(c['state'])]=j
        elif c['kind']=='overlap':details[c['hist_column']]['overlaps'][j]=c['groups']
    for hi,dd in details.items():
        gs=sorted(dd['groups']); gi={g:i for i,g in enumerate(gs)};n=len(gs)
        c=[m[i][hi] for i in keep]+[F()]*len(ZZ_NAMES)
        r=[[F()]*n for _ in names];z=[[F()]*n for _ in names]
        rz={};rr={}
        for g,st in dd['groups'].items():
            j=gi[g];rz[j,j]=[F()]*nrows
            for ii,i in enumerate(keep):
                r[ii][j]=m[i][st[1,0]];z[ii][j]=m[i][st[0,1]]
                rz[j,j][ii]=m[i][st[1,1]]-r[ii][j]-z[ii][j]
        for j,pair in dd['overlaps'].items():
            g,h=[(x[0],x[1],tuple(x[2]),tuple(x[3])) for x in pair]
            rr[gi[g],gi[h]]=[m[i][j] for i in keep]+[F()]*len(ZZ_NAMES)
        h=dd['hist'];a=tuple(map(int,h['actual_bits']));pa=sum(a[:4]);D=(pa+1)*(pa+2)
        words=[w for w,nw in zip(nr.PAT,h['hist']) for _ in range(nw)]
        edges=[(f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j]
        group=lambda e:(e[0],int(e[1]==e[2]),words[e[1]],words[e[2]])
        for e in edges:
            f,i,j=e;ge=gi[group(e)]
            for ee in edges:
                g,k,l=ee;gf=gi[group(ee)];row=nold+ZI['Z-Z',f,g,cl.partition((i,j,k,l))]
                z[row][ge]+=F(1,pa+1);z[row][gf]-=F(1,pa+1)
                if (ge,gf) not in rz:rz[ge,gf]=[F()]*nrows
                rz[ge,ge][row]-=F(1,D)
                rz[ge,gf][row]+=F(1,D)
        loc={'hist':h,'groups':gs,'c':c,'r':r,'z':z,'rz':rz,'rr':rr,
             'obj':F(int(any(a))),'norm':F(int(h['d']>0))}
        loc['fc']=np.array(c,dtype=float);loc['fr']=np.array(r,dtype=float);loc['fz']=np.array(z,dtype=float)
        loc['frz']={k:np.array(v,dtype=float) for k,v in rz.items()}
        loc['frr']={k:np.array(v,dtype=float) for k,v in rr.items()}
        locals.append(loc)
        print('built joint polynomial',len(locals),'groups',n,'seconds',time.time()-started,flush=True)
    return names,kcol,locals

def atom(loc,r,z,exact=False):
    if exact:
        v=list(loc['c'])
        for j,b in enumerate(r):
            if b:v=[x+y[j] for x,y in zip(v,loc['r'])]
        for j,b in enumerate(z):
            if b:v=[x+y[j] for x,y in zip(v,loc['z'])]
        for (i,j),row in loc['rz'].items():
            if r[i] and z[j]:v=[x+y for x,y in zip(v,row)]
        for (i,j),row in loc['rr'].items():
            if r[i] and r[j]:v=[x+y for x,y in zip(v,row)]
        return v
    v=loc['fc']+loc['fr']@r+loc['fz']@z
    for (i,j),row in loc['frz'].items():
        if r[i] and z[j]:v+=row
    for (i,j),row in loc['frr'].items():
        if r[i] and r[j]:v+=row
    return v

def pricing(loc,dual,rng,restarts=96):
    n=len(loc['groups']);b=np.r_[dual@loc['fr'],dual@loc['fz']]
    q=np.zeros((2*n,2*n))
    for (i,j),v in loc['frz'].items():q[i,n+j]+=dual@v
    for (i,j),v in loc['frr'].items():q[i,j]+=dual@v
    # The coordinate ascent is only a column discovery heuristic. Its failure
    # never establishes optimality or full-domain infeasibility.
    q=q+q.T
    starts=rng.integers(0,2,size=(restarts,2*n),dtype=np.int8)
    starts[:4,:]=np.array([[0]*n+[0]*n,[0]*n+[1]*n,[1]*n+[0]*n,[1]*n+[1]*n])
    for sweep in range(30):
        changed=False
        for j in rng.permutation(2*n):
            new=(b[j]+starts@q[j]>1e-12).astype(np.int8)
            changed|=bool(np.any(new!=starts[:,j]));starts[:,j]=new
        if not changed:break
    values=starts@b+np.einsum('bi,ij,bj->b',starts,q,starts)/2
    order=np.argsort(values)[::-1]
    out=[];seen=set()
    for ix in order:
        key=tuple(map(int,starts[ix]));
        if key not in seen:seen.add(key);out.append((float(values[ix]+dual@loc['fc']),key[:n],key[n:]))
    return out

def solve(args):
    started=time.time();names,kcol,locs=model();nrw=len(names);rng=np.random.default_rng(args.seed)
    keys=[];vectors=[];objectives=[];normal=[];seen=set()
    def add(hi,r,z):
        key=(hi,tuple(map(int,r)),tuple(map(int,z)))
        if key in seen:return False
        seen.add(key);keys.append(key);loc=locs[hi];vectors.append(atom(loc,r,z))
        objectives.append(float(loc['obj']));normal.append(float(loc['norm']));return True
    for hi,loc in enumerate(locs):
        n=len(loc['groups'])
        for r0,z0 in product(range(2),repeat=2):add(hi,(r0,)*n,(z0,)*n)
        for _ in range(args.initial):add(hi,rng.integers(0,2,n),rng.integers(0,2,n))
    phase=1;sol=None
    for iteration in range(args.rounds):
        a=np.column_stack([np.array(kcol,dtype=float),*vectors])
        scale=np.max(abs(a),axis=1);scale[scale==0]=1
        eq=np.array([[0,*normal]],dtype=float)
        objective=np.array([0,*objectives],dtype=float)
        if phase==1:
            a=np.column_stack([a,scale]);eq=np.column_stack([eq,[0]])
            objective=np.r_[np.zeros(len(objective)),1.0]
        sol=linprog(objective,A_ub=csr_matrix(-a/scale[:,None]),b_ub=np.zeros(nrw),A_eq=eq,b_eq=[1],bounds=(0,None),method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
        if not sol.success:raise RuntimeError(sol.message)
        dual=-sol.ineqlin.marginals/scale;rho=float(sol.eqlin.marginals[0]);added=0;best=0
        if phase==1 and sol.fun<1e-9:
            phase=2;print('PHASE2',iteration,flush=True);continue
        for hi,loc in enumerate(locs):
            for score,r,z in pricing(loc,dual,rng,args.restarts):
                rc=float(loc['obj']) if phase==2 else 0
                rc-=rho*float(loc['norm'])+score
                best=min(best,rc)
                if rc < -1e-8:added+=add(hi,r,z)
        print(json.dumps({'iteration':iteration,'phase':phase,'objective':float(sol.fun),'columns':len(keys)+1,'added':added,'minimum_discovered_rc':best,'seconds':time.time()-started}),flush=True)
        # Store every current support; all data needed for exact replay resides
        # in this new directory. Successful exact recovery is a separate step.
        np.savez_compressed(HERE/'joint_atoms_float.npz',x=sol.x,keys=np.array([json.dumps(k) for k in keys[:len(sol.x)-1-(phase==1)]]),phase=phase)
        (HERE/'joint_atoms_status.json').write_text(json.dumps({'scope':'16 fixed old histograms; full explicit joint atoms inside each orbit-equality restriction; floating discovery only','phase':phase,'objective':float(sol.fun),'columns':len(keys)+1,'iteration':iteration,'seconds':time.time()-started},indent=2)+'\n')
        if phase==2 and sol.fun<.5-1e-8:
            report=exact_recover(names,kcol,locs,keys[:len(sol.x)-1],sol.x)
            (HERE/'joint_atoms_exact.json').write_text(json.dumps(report,indent=2)+'\n')
            print('EXACT',report['W'],'positive',len(report['atoms']),flush=True);return
        if not added:break

def exact_recover(names,kcol,locs,keys,solution):
    keep=[j for j,v in enumerate(solution) if v>1e-8]
    cols=[kcol if j==0 else atom(locs[keys[j-1][0]],keys[j-1][1],keys[j-1][2],True) for j in keep]
    mat=list(map(list,zip(*cols)));vals=solution[keep]
    equations=[]
    for row in mat:
        scale=max([float(abs(x)) for x in row]+[1e-50])
        if abs(np.dot(np.array(row,dtype=float),vals))<1e-9*scale:equations.append(row+[F()])
    norm=[F(0) if j==0 else locs[keys[j-1][0]]['norm'] for j in keep]
    equations.append(norm+[F(1)])
    exact=exact_solve(equations,len(keep));assert min(exact)>=0
    slacks=[sum(x*y for x,y in zip(row,exact)) for row in mat];assert min(slacks)>=0,(names[slacks.index(min(slacks))],min(slacks))
    w=sum(v*(F() if j==0 else locs[keys[j-1][0]]['obj']) for j,v in zip(keep,exact));assert w<F(1,2)
    atoms=[];K=F()
    for j,v in zip(keep,exact):
        if j==0:K=v
        else:
            hi,r,z=keys[j-1];atoms.append({'hist_index':hi,'R':list(r),'Z':list(z),'weight':str(v)})
    return {'scope':'exact joint atom feasible obstruction for specified raw families; not a game or SPE; no full-domain half claim','rows':len(names),'O':'1','W':str(w),'strict_half_gap':str(1-2*w),'minimum_slack':str(min(slacks)),'K':str(K),'histograms':[loc['hist'] for loc in locs],'groups':[[[g[0],g[1],list(g[2]),list(g[3])] for g in loc['groups']] for loc in locs],'atoms':atoms}

def verify():
    data=json.loads((HERE/'joint_atoms_exact.json').read_text());names,kcol,locs=model()
    total=[F(data['K'])*v for v in kcol];w=F();o=F()
    for atomdata in data['atoms']:
        hi=atomdata['hist_index'];loc=locs[hi];v=F(atomdata['weight']);assert v>=0
        r=atomdata['R'];z=atomdata['Z'];assert all(b in (0,1) for b in r+z)
        row=atom(loc,r,z,True);total=[x+v*y for x,y in zip(total,row)]
        w+=v*loc['obj'];o+=v*loc['norm']
    assert F(data['K'])>=0 and min(total)>=0 and o==1 and w==F(data['W']) and w<F(1,2)
    print(json.dumps({'verified_rows':len(names),'minimum_slack':str(min(total)),'W':str(w),'O':str(o),'joint_atoms':len(data['atoms'])},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');p.add_argument('--seed',type=int,default=91);p.add_argument('--initial',type=int,default=12);p.add_argument('--rounds',type=int,default=120);p.add_argument('--restarts',type=int,default=96);args=p.parse_args()
    verify() if args.verify else solve(args)
