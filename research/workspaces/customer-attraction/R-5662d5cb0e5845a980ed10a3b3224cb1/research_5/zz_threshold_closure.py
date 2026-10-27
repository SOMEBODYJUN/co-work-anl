"""All Z_e->Z_f IC on the exact 3889-point common-threshold R realization.

This is a fixed finite sub-support feasibility test, not a full-domain proof.
Outputs stay in this workspace. Original files are only read/imported.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,sys,time,hashlib
import numpy as np
from scipy.sparse import coo_matrix,csr_matrix
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
OLD=ROOT/'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra'
sys.path.insert(0,str(OLD))
import attractive_nested as an
import full_new_reply_closure as cl
import new_reply_budget as nr
ZZ=[(f,g,pat) for f,g,pat in product(range(2),range(2),cl.P4)]
ZI={x:i for i,x in enumerate(ZZ)}
MASTER_MODE='--master' in sys.argv
CROSS_MODE='--cross' in sys.argv
SPLIT_MODE='--split' in sys.argv
SOURCE=(HERE/'combined_branch_master_exact.json') if MASTER_MODE else ((HERE/'cross_source_priced_optimum_exact.json') if CROSS_MODE else ((HERE/'split_basic_exact.json') if SPLIT_MODE else (OLD/'attractive_nested_exact.json')))
PREFIX='zz_master' if MASTER_MODE else ('zz_cross' if CROSS_MODE else ('zz_split' if SPLIT_MODE else 'zz_threshold'))

def build():
    old=json.loads(SOURCE.read_text())
    histcols=[c for c in old['columns'] if c['kind']=='hist']
    if MASTER_MODE:
        import combined_branch_master
        cols,names,m,obj,norm=combined_branch_master.build()
    elif CROSS_MODE:
        import cross_source_graph
        cols,names,m,obj,norm=cross_source_graph.build()
    elif SPLIT_MODE:
        import split_basic_graph
        cols,names,m,obj,norm=split_basic_graph.build()
    else:cols,names,m,obj,norm=an.build(histcols)
    assert json.dumps(cols)==json.dumps([{k:v for k,v in c.items() if k!='weight'} for c in old['columns']])
    vals=[F(c['weight']) for c in old['columns']]
    byhist={};hi=None
    for j,c in enumerate(cols):
        if c['kind']=='hist':hi=j;byhist[j]={}
        elif c['kind']=='joint-reply':
            f,diag,wi,wj=c['group'];g=(f,diag,tuple(wi),tuple(wj))
            byhist[hi].setdefault(g,{})[tuple(c['state'])]=j
    variables=[];bounds=[];base=[F()]*len(cols);base[0]=vals[0]
    mapping=[[] for c in cols];details=[]
    for hi,gs in byhist.items():
        hmass=vals[hi];base[hi]=hmass
        if not hmass:continue
        rm={g:vals[st[1,0]]+vals[st[1,1]] for g,st in gs.items()}
        cuts=sorted({F(),hmass,*rm.values()})
        slabs=[]
        for l,u in zip(cuts,cuts[1:]):
            mass=u-l
            if not mass:continue
            rs={g:int(u<=r) for g,r in rm.items()};vis={}
            for g,st in gs.items():
                v=len(variables);variables.append({'hist_column':hi,'left':str(l),'right':str(u),'group':[g[0],g[1],list(g[2]),list(g[3])],'r':rs[g]});bounds.append(mass);vis[g]=v
                if rs[g]:
                    base[st[1,0]]+=mass
                    mapping[st[1,0]].append((v,F(-1)));mapping[st[1,1]].append((v,F(1)))
                else:mapping[st[0,1]].append((v,F(1)))
            slabs.append((l,u,rs,vis))
        for j,c in enumerate(cols):
            if c['kind']=='overlap' and c['hist_column']==hi:
                def cv(g):return (g[0],g[1],tuple(g[2]),tuple(g[3]))
                g,h=map(cv,c['groups']);base[j]=min(rm[g],rm[h])
        details.append((hi,gs,slabs))
    # Exact sparse affine rows, expressed as const + A z >= 0.
    exrows=[];constants=[]
    for name,row in zip(names,m):
        out={};const=F()
        for j,c in enumerate(row):
            if not c:continue
            const+=c*base[j]
            for v,q in mapping[j]:out[v]=out.get(v,F())+c*q
        exrows.append({v:q for v,q in out.items() if q});constants.append(const)
    zrows=[{} for _ in ZZ]
    for hi,gs,slabs in details:
        c=cols[hi];a=tuple(map(int,c['actual_bits']));pa=sum(a[:4]);h=c['hist']
        words=[w for w,n in zip(nr.PAT,h) for _ in range(n)]
        edges=[(f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j]
        def group(e):return (e[0],int(e[1]==e[2]),words[e[1]],words[e[2]])
        for l,u,rs,vis in slabs:
            for e in edges:
                f,i,j=e;ge=group(e);ve=vis[ge];coef=F(1,pa+1+rs[ge])
                for ee in edges:
                    g,k,ll=ee;gf=group(ee);vf=vis[gf];row=zrows[ZI[f,g,cl.partition((i,j,k,ll))]]
                    row[ve]=row.get(ve,F())+coef;row[vf]=row.get(vf,F())-coef
    exrows += [{v:q for v,q in row.items() if q} for row in zrows]
    constants += [F() for _ in ZZ];names += ['Z-Z:'+str(x) for x in ZZ]
    return old,variables,bounds,names,exrows,constants,cols,base,mapping

def main():
    start=time.time();data=build();old,vs,bounds,names,rows,bs,cols,base,mapping=data
    if '--verify' in sys.argv:
        report=json.loads((HERE/(PREFIX+'_exact.json')).read_text());ys=[F(z['weight']) for z in report['variables']]
        assert len(ys)==len(vs) and all(F(0)<=y<=b for y,b in zip(ys,bounds))
        slacks=[b+sum(q*ys[j] for j,q in row.items()) for row,b in zip(rows,bs)]
        assert min(slacks)>=0
        print(json.dumps({'verified_rows':len(rows),'variables':len(vs),'minimum_slack':str(min(slacks)),'W':old['W']},indent=2));return
    print('built',len(rows),'rows',len(vs),'vars','seconds',time.time()-start,flush=True)
    ri=[];ci=[];vv=[]
    for i,row in enumerate(rows):
        for j,v in row.items():ri.append(i);ci.append(j);vv.append(float(v))
    a=coo_matrix((vv,(ri,ci)),shape=(len(rows),len(vs))).tocsr();bf=np.array([float(b) for b in bs])
    scale=np.asarray(abs(a).max(axis=1).toarray()).ravel();scale=np.maximum(scale,np.abs(bf));scale[scale==0]=1
    sol=linprog(np.zeros(len(vs)),A_ub=-a.multiply(1/scale[:,None]),b_ub=bf/scale,bounds=[(0,float(b)) for b in bounds],method='highs',options={'dual_feasibility_tolerance':1e-9,'primal_feasibility_tolerance':1e-9})
    report={'scope':'fixed exact 3889 hist/R common-threshold sub-support; not full type domain, not SPE','source_W':old['W'],'source_point':str(SOURCE.relative_to(ROOT)),'rows':len(rows),'variables':len(vs),'success':bool(sol.success),'status':sol.message,'seconds':time.time()-start}
    if sol.success:
        report['minimum_float_scaled_slack']=float(min((a@sol.x+bf)/scale));report['float_variables']=[{**v,'weight':float(x)} for v,x in zip(vs,sol.x)]
        np.savez(HERE/(PREFIX+'_float.npz'),x=sol.x)
        # Recover an exact vertex: 0/upper-bound variables are fixed first.
        exact=[None]*len(vs);free=[]
        for j,(y,b) in enumerate(zip(sol.x,bounds)):
            if y<1e-9:exact[j]=F()
            elif float(b)-y<1e-9:exact[j]=b
            else:free.append(j)
        equations=[]
        residual=(a@sol.x+bf)/scale
        for i,(row,b) in enumerate(zip(rows,bs)):
            if abs(residual[i])>1e-9:continue
            const=b+sum(q*exact[j] for j,q in row.items() if exact[j] is not None)
            eq=[row.get(j,F()) for j in free]+[-const]
            if any(eq):equations.append(eq)
        values=cl.exact_solve(equations,len(free))
        for j,y in zip(free,values):exact[j]=y
        assert all(F()<=y<=b for y,b in zip(exact,bounds))
        slacks=[b+sum(q*exact[j] for j,q in row.items()) for row,b in zip(rows,bs)]
        assert min(slacks)>=0,(names[slacks.index(min(slacks))],min(slacks))
        er={'scope':'exact feasible complete-cube lifted necessary-condition point for old 3889 graph plus all 60 Z->Z classes; not an SPE or a game',
            'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'W':old['W'],'O':'1','rows':len(rows),'variables_count':len(vs),'minimum_slack':str(min(slacks)),
            'positive_variables':sum(y>0 for y in exact),'free_vertex_variables':len(free),
            'variables':[{**v,'weight':str(y)} for v,y in zip(vs,exact)]}
        (HERE/(PREFIX+'_exact.json')).write_text(json.dumps(er,indent=2)+'\n')
        report['exact_verified']=True;report['minimum_exact_slack']=str(min(slacks));report['free_vertex_variables']=len(free)
    (HERE/(PREFIX+'_status.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='float_variables'},indent=2),flush=True)
if __name__=='__main__':main()
