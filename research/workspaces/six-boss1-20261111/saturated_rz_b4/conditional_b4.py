"""Necessary conditional first-moment LP on the complete saturated face.

One own-RZ/B4-state table per stabilizer group is a symmetry reduction of
moments, not an identification of the literal events.  All 600 saturated
literal implications are imposed conditional on the SAME B4 state.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
import argparse, json
from extract_face import parse_point, sha, orbit

def serial(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [serial(v) for v in x]
    return x

def row_add(row,j,c):
    row[j]=row.get(j,Q())+c
    if not row[j]:del row[j]

def build(point,face):
    raw,nodes,data=parse_point(point)
    f=json.loads(Path(face).read_text());assert f['point_sha256']==sha(point)
    gorbits=((0,0),(1,0),(1,1))
    specs=[sp for o in gorbits for sp in [('F-to-R',o),('F-to-Z',o),*(('Z-to-X',o,k) for k in range(3))]]
    variables=[];vmap={};hgroups={};node_groups={}
    for h,d in data.items():
        if not d['H']:continue
        gg=[];index={};nodeg=[]
        for e,g in enumerate(d['groups']):
            if g not in index:index[g]=len(gg);gg.append(dict(group=g,own=d['own'][e],nodes=[]))
            nodeg.append(index[g]);gg[index[g]]['nodes'].append(e)
        hgroups[h]=gg;node_groups[h]=nodeg
        for gi,g in enumerate(gg):
            for s,eta in sorted(d['B4'].items()):
                if not eta:continue
                for a,rho in enumerate(g['own']):
                    if not rho:continue
                    key=(h,gi,s,a);vmap[key]=len(variables);variables.append(key)
    n=len(variables);equalities=[];inequalities=[]
    def eq(row,rhs,label):equalities.append(dict(row=row,rhs=rhs,label=label))
    def ub(row,rhs,label,slack=False):
        if slack:row[n]=Q(1)
        inequalities.append(dict(row=row,rhs=rhs,label=label))
    for h,gg in hgroups.items():
        for gi,g in enumerate(gg):
            states=[s for s,m in data[h]['B4'].items() if m]
            for a,m in enumerate(g['own']):
                if m:eq({vmap[h,gi,s,a]:Q(1) for s in states},m,['own',h,gi,a])
            for s in states:
                eq({vmap[h,gi,s,a]:Q(1) for a,m in enumerate(g['own']) if m},data[h]['B4'][s],['B4',h,gi,s])
    satpairs=[(e,g) for r in f['saturated_nonself_orbits'] for e,g in r['literal_pairs']]
    for h,gg in hgroups.items():
        d=data[h];directions=set()
        for e,g in satpairs:
            q=sum(d['own'][e][2:]);v=d['own'][g][1]+d['own'][g][3]
            ge=node_groups[h][e];gf=node_groups[h][g]
            if q<=v:directions.add((ge,gf,1))
            if q>=v:directions.add((ge,gf,-1))
        for ge,gf,sgn in sorted(directions):
            for s,eta in sorted(d['B4'].items()):
                if not eta:continue
                row={}
                for a,m in enumerate(gg[ge]['own']):
                    if m and a//2:row_add(row,vmap[h,ge,s,a],Q(sgn))
                for a,m in enumerate(gg[gf]['own']):
                    if m and a%2:row_add(row,vmap[h,gf,s,a],Q(-sgn))
                ub(row,Q(),['saturation',h,ge,gf,sgn,s])
    bF=sum((eta*Q(s[1],sum(d['actual'][:3])+d['actual'][5]+s[0]+1)
            for d in data.values() for s,eta in d['B4'].items()),Q())
    bZ={o:Q() for o in gorbits}
    for h,d in data.items():
        P=sum(d['actual'][:4])
        for e,(fam,i,j) in enumerate(nodes):
            o=(fam,int(i==j));size=6 if o==(1,1) else 30
            m=d['own'][e]
            bZ[o]+=(m[1]/Q(P+1)+m[3]/Q(P+2))/size
    for sp in specs:
        row={}
        for vi,(h,gi,s,a) in enumerate(variables):
            g=hgroups[h][gi];d=data[h];P=sum(d['actual'][:4]);o=g['group'][:2]
            if tuple(o)!=sp[1]:continue
            size=6 if sp[1]==(1,1) else 30;factor=Q(len(g['nodes']),size)
            den=sum(d['actual'][:3])+d['actual'][5]+s[0]+1
            cost=Q(a//2,den) if sp[0]=='F-to-R' else Q(a%2,den) if sp[0]=='F-to-Z' else Q(s[sp[2]],P+a//2+1)
            if cost:row[vi]=factor*cost
        ub(row,bZ[sp[1]] if sp[0]=='Z-to-X' else bF,['IC',sp],True)
    return dict(variables=variables,hgroups=hgroups,node_groups=node_groups,equalities=equalities,inequalities=inequalities,
                specs=specs,slack_variable=n,point_sha256=sha(point),face_sha256=sha(face)),data,nodes

def solve_linear(equations,n,seed=None):
    pivots={}
    for initial,rhs in equations:
        row={j:c for j,c in initial.items() if c};rhs=Q(rhs)
        while row:
            lead=min(row)
            if lead not in pivots:
                fac=row[lead];pivots[lead]=({j:c/fac for j,c in row.items()},rhs/fac);break
            old,b=pivots[lead];fac=row[lead];rhs-=fac*b
            for j,c in old.items():
                val=row.get(j,Q())-fac*c
                if val:row[j]=val
                elif j in row:del row[j]
        else:
            if rhs:return None,dict(rank=len(pivots),inconsistent=True)
    ans=list(seed) if seed is not None else [Q()]*n
    for lead,(row,rhs) in sorted(pivots.items(),reverse=True):
        ans[lead]=rhs-sum((c*ans[j] for j,c in row.items() if j!=lead),Q())
    return ans,dict(rank=len(pivots),inconsistent=False)

def add_old_envelopes(model,data,nodes,mode,strict=False):
    """General necessary conditional Frechet bounds, never true overlaps."""
    own_n=model['slack_variable'];old=model['variables'];vmap={v:i for i,v in enumerate(old)}
    orbs=defaultdict(list)
    for e,ne in enumerate(nodes):
        for f,nf in enumerate(nodes):orbs[orbit(ne,nf)].append((e,f))
    yr={};extra=[]
    def margin(h,gi,s,which):
        row={}
        for a,m in enumerate(model['hgroups'][h][gi]['own']):
            if m and ((a//2) if which=='R' else (a%2)):
                row[vmap[h,gi,s,a]]=Q(1)
        return row
    def envelope(h,ge,gf,s,kind):
        if kind=='Z-R' and ge>gf:ge,gf=gf,ge
        first=margin(h,ge,s,'R');second=margin(h,gf,s,'R' if kind=='Z-R' else 'Z')
        if not first or not second:return None
        key=h,ge,gf,s,kind
        if key in yr:return yr[key]
        col=len(model['variables']);yr[key]=col
        model['variables'].append(dict(aux='conditional-Frechet-upper',hist=h,e_group=ge,f_group=gf,B4_state=s,kind=kind))
        for tag,mm in [('first',first),('second',second)]:
            rr={j:-c for j,c in mm.items()};rr[col]=Q(1)
            extra.append(dict(row=rr,rhs=Q(),label=['conditional-upper',key,tag]))
        return col
    old_rows=[]
    for kind in (('Z-Z',) if mode=='ZZ' else ('Z-R','Z-Z')):
        for cl,pp in sorted(orbs.items()):
            if kind=='Z-Z' and all(e==f for e,f in pp):continue
            if strict and kind=='Z-Z' and cl in ((0,1,(0,1,0,2)),(0,1,(0,1,2,2)),(0,1,(0,1,2,3))):
                # Already enforced by all conditional saturation implications.
                continue
            row={};base=Q()
            for h,d in data.items():
                if not d['H']:continue
                own=d['own'];P=sum(d['actual'][:4]);D=(P+1)*(P+2)
                for e,f in pp:
                    ve=own[e][1]+own[e][3];te=own[e][3]
                    target=own[f][2]+own[f][3] if kind=='Z-R' else own[f][1]+own[f][3]
                    base+=((ve-target)/Q(P+1)-te/Q(D))/len(pp)
                    ge=model['node_groups'][h][e];gf=model['node_groups'][h][f]
                    for s,eta in d['B4'].items():
                        if not eta:continue
                        col=envelope(h,ge,gf,s,kind)
                        if col is not None:row_add(row,col,-Q(1,len(pp)*D))
            old_rows.append(dict(row=row,rhs=base,label=['old-conditional-Frechet',kind,cl]))
    n=len(model['variables'])
    for rr in model['equalities']+model['inequalities']:
        if own_n in rr['row']:rr['row'][n]=rr['row'].pop(own_n)
    if strict:
        for rr in old_rows:rr['row'][n]=Q(1)
    model['inequalities'].extend(extra+old_rows)
    model['slack_variable']=n;model['own_variables']=own_n;model['conditional_envelope_mode']=mode
    model['strict_old_envelope_slack']=strict
    return model

def discover(model):
    import numpy as np
    from scipy.sparse import coo_matrix
    from scipy.optimize import linprog
    n=model['slack_variable'];rows=model['equalities'];urs=model['inequalities']
    def mat(rr):
        i=[];j=[];v=[]
        for k,r in enumerate(rr):
            for col,c in r['row'].items():i.append(k);j.append(col);v.append(float(c))
        return coo_matrix((v,(i,j)),shape=(len(rr),n+1)).tocsc()
    c=np.zeros(n+1);c[n]=-1
    result=linprog(c,A_eq=mat(rows),b_eq=[float(r['rhs']) for r in rows],
                   A_ub=mat(urs),b_ub=[float(r['rhs']) for r in urs],
                   bounds=[(0,None)]*n+[(None,None)],method='highs',
                   options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
    report=dict(status=int(result.status),message=result.message,variables=n,equalities=len(rows),inequalities=len(urs))
    if not result.success:return report
    report.update(maximum_common_slack=float(result.x[n]),floating_solution=result.x.tolist(),
                  floating_equality_duals=result.eqlin.marginals.tolist(),floating_inequality_duals=result.ineqlin.marginals.tolist())
    support=[i for i,x in enumerate(result.x) if x>1e-10 or i==n];local={v:i for i,v in enumerate(support)}
    active=[i for i,r in enumerate(urs) if abs(float(r['rhs'])-sum(float(c)*result.x[j] for j,c in r['row'].items()))<1e-8]
    eqs=[]
    for r in rows+[urs[i] for i in active]:eqs.append(({local[j]:c for j,c in r['row'].items() if j in local},r['rhs']))
    seed=[Q(str(result.x[i])).limit_denominator(10**12) for i in support]
    exact,info=solve_linear(eqs,len(support),seed)
    report['recovery']=dict(support=len(support),active_inequalities=active,**info)
    if exact is None:return report
    x=[Q()]*(n+1)
    for i,v in zip(support,exact):x[i]=v
    eqok=all(sum((c*x[j] for j,c in r['row'].items()),Q())==r['rhs'] for r in rows)
    slacks=[r['rhs']-sum((c*x[j] for j,c in r['row'].items()),Q()) for r in urs]
    report['recovery'].update(equality_check=eqok,minimum_variable=min(x[:n]),minimum_row_slack=min(slacks),exact_objective=x[n])
    if eqok and min(x[:n])>=0 and min(slacks)>=0:
        report['exact_solution']=[str(v) for v in x]
    return report

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--point',type=Path,required=True);ap.add_argument('--face',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--old-envelopes',choices=['ZZ','all'])
    ap.add_argument('--strict-old-slack',action='store_true');args=ap.parse_args()
    model,data,nodes=build(args.point,args.face)
    if args.old_envelopes:add_old_envelopes(model,data,nodes,args.old_envelopes,args.strict_old_slack)
    report=discover(model)
    out=dict(scope='General necessary own-RZ / common B4 conditional moment relaxation; no event identification by stable group',
             point_path=str(args.point),face_path=str(args.face),source_sha256=sha(Path(__file__)),model=model,discovery=report)
    args.output.write_text(json.dumps(serial(out),indent=2,ensure_ascii=False)+'\n')
    compact={k:v for k,v in report.items() if not k.startswith('floating') and k not in ('exact_solution','recovery')}
    compact['recovery']={k:v for k,v in report.get('recovery',{}).items() if k!='active_inequalities'}
    print(json.dumps(serial(compact)))

if __name__=='__main__':main()
