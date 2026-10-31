"""New complete ordered policy cones, exact integer Gamma candidate search.

Float LP is only exploratory. Frozen promising candidates are replayed exactly.
This does not import the repository's equilibrium solver.
"""
from __future__ import annotations
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, product
from math import lcm
from pathlib import Path
import argparse, hashlib, json, random, time
import numpy as np
from scipy.optimize import linprog
from scipy import sparse

OUT=Path(__file__).resolve().parent

def plain(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,np.generic):return x.item()
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [plain(v) for v in x]
    return x

def counts(z,m):return tuple(z.count(a) for a in range(m))

def exact_solve(rows,rhs,width):
    basis={}
    for r,b in zip(rows,rhs):
        z=list(map(F,r))+[F(b)]
        for j in sorted(basis):
            if z[j]:
                k=z[j];z=[x-k*y for x,y in zip(z,basis[j])]
        j=next((j for j in range(width) if z[j]),None)
        if j is None:
            if z[-1]:return None
            continue
        k=z[j];basis[j]=[x/k for x in z]
        if len(basis)==width:break
    if len(basis)!=width:return None
    x=[F(0)]*width
    for j in sorted(basis,reverse=True):
        x[j]=basis[j][-1]-sum(basis[j][k]*x[k] for k in range(j+1,width))
    return tuple(x)

class Space:
    def __init__(self,n,m):
        self.n,self.m=n,m;self.k=(1<<m)-1;self.L=lcm(*range(1,n+1))
        self.masks=np.arange(1,1<<m,dtype=np.int64)
        self.inc=np.array([[(mask>>a)&1 for a in range(m)] for mask in self.masks],dtype=np.int64)
        self.histories=tuple(h for d in range(n) for h in product(range(m),repeat=d))
        self.ids={h:i for i,h in enumerate(self.histories)}
        self.tc=tuple(counts(z,m) for z in combinations_with_replacement(range(m),n))
        self.tids={c:i for i,c in enumerate(self.tc)}
        self.den=np.array(self.tc,dtype=np.int64)@self.inc.T
        self.cover=(self.den>0).astype(np.int64)
        inv=np.zeros_like(self.den)
        for d in range(1,n+1):inv[self.den==d]=self.L//d
        self.pay=inv[:,None,:]*self.inc.T[None,:,:]
        self.B=tuple(combinations_with_replacement(range(m),n-1))
        self.Bc=np.array([counts(B,m) for B in self.B],dtype=np.int64)
        self.static_den=1+self.Bc@self.inc.T
        self.static=self.inc.T[None,:,:]/self.static_den[:,None,:]
        self.J=tuple(combinations(range(m),min(m,n)))
        self.Jcover=np.array([np.any(self.inc[:,J],axis=1) for J in self.J],dtype=np.int64)

    def full_policy(self,actions):
        if isinstance(actions,dict):pol=np.array([actions[h] for h in self.histories],dtype=np.int16)
        else:pol=np.asarray(actions,dtype=np.int16)
        assert len(pol)==len(self.histories) and min(pol)>=0 and max(pol)<self.m
        terminal={}
        for z in product(range(self.m),repeat=self.n):terminal[z]=self.tids[counts(z,self.m)]
        branch=np.empty((len(pol),self.m),dtype=np.int64)
        realized=np.empty(len(pol),dtype=np.int64)
        for i in range(len(pol)-1,-1,-1):
            h=self.histories[i];branch[i]=[terminal[h+(a,)] for a in range(self.m)]
            realized[i]=branch[i,pol[i]];terminal[h]=int(realized[i])
        # Histories are all retained above. Deduplicate only identical exact
        # payoff-row pairs before materializing their coefficient differences.
        keys=np.column_stack([np.repeat(realized,self.m),np.repeat(pol,self.m),branch.ravel(),np.tile(np.arange(self.m),len(pol))])
        keys=np.unique(keys,axis=0)
        raw=self.pay[keys[:,0],keys[:,1]]-self.pay[keys[:,2],keys[:,3]]
        gamma=np.unique(raw,axis=0)
        gamma=gamma[np.any(gamma,axis=1)]
        c=self.cover[realized[0]]
        digest=hashlib.sha256(pol.tobytes()).hexdigest()
        return dict(policy=pol,branch=branch,realized=realized,gamma=gamma,c=c,digest=digest)

    def outcomes(self,w):
        u=self.pay@np.array(w,dtype=np.int64)
        menus={};floor={}
        @lru_cache(None)
        def solve(q):
            if sum(q)==self.n:
                result=(self.tids[q],)
            else:
                children=[solve(q[:a]+(q[a]+1,)+q[a+1:]) for a in range(self.m)]
                f=max(min(u[t,a] for t in child) for a,child in enumerate(children));floor[q]=int(f)
                result=tuple(sorted(set(t for a,child in enumerate(children) for t in child if u[t,a]>=f)))
            menus[q]=result;return result
        roots=solve((0,)*self.m)
        return roots,menus,floor,u

    def synthesize(self,w,seed,mode='random',target=None):
        roots,menus,floor,u=self.outcomes(w);rng=random.Random(seed)
        welfare=self.cover@np.asarray(w,dtype=np.int64)
        if target is None:target=min(roots,key=lambda t:(welfare[t],tuple(u[t])))
        pol={}
        def pick(cands,h,action=False):
            if mode=='random':return rng.choice(cands)
            if action:return min(cands)
            if mode=='root_min':return min(cands,key=lambda t:(sum(u[t,a] for a in h),welfare[t],t))
            if mode=='root_max':return max(cands,key=lambda t:(sum(u[t,a] for a in h),-welfare[t],t))
            if mode=='welfare_min':return min(cands,key=lambda t:(welfare[t],t))
            if mode=='welfare_max':return max(cands,key=lambda t:(welfare[t],-t))
            return min(cands)
        def expand(h,q,target):
            if len(h)==self.n:return
            children=[q[:a]+(q[a]+1,)+q[a+1:] for a in range(self.m)]
            cands=tuple(a for a,c in enumerate(children) if target in menus[c] and u[target,a]>=floor[q])
            a=pick(cands,h,True);pol[h]=a
            for b,c in enumerate(children):
                t=target if b==a else pick(tuple(t for t in menus[c] if u[t,b]==min(u[s,b] for s in menus[c])),h+(b,))
                expand(h+(b,),c,t)
        expand((),(0,)*self.m,target)
        cone=self.full_policy(pol)
        assert np.min(cone['gamma']@np.array(w,dtype=np.int64))>=0
        return cone,dict(seed=seed,mode=mode,root_menus=len(roots),retained=sum(map(len,menus.values())),target=target,seed_welfare=int(welfare[target]))

    def security(self,w):
        M=self.static@np.asarray(w)
        Aub=np.column_stack([-M,np.ones(len(self.B))])
        res=linprog([0]*self.m+[-1],A_ub=Aub,b_ub=np.zeros(len(self.B)),A_eq=[[1]*self.m+[0]],b_eq=[1],bounds=[(0,None)]*self.m+[(None,None)],method='highs')
        assert res.success
        return res.x[:-1],float(res.x[-1]),M,res

    def cone_security(self,cone,p,extra=None):
        beta=np.einsum('bak,a->bk',self.static,p)
        G=cone['gamma']/self.L
        Aub=np.vstack([np.column_stack([-G,np.zeros(len(G))]),np.column_stack([-beta,np.ones(len(beta))])])
        res=linprog([0]*self.k+[-self.n],A_ub=Aub,b_ub=np.zeros(len(Aub)),A_eq=[list(cone['c'])+[0]],b_eq=[1],bounds=[(0,None)]*self.k+[(None,None)],method='highs')
        return res,beta

    def cone_half(self,cone,J=None):
        portfolios=range(len(self.J)) if J is None else [J]
        best=None
        for j in portfolios:
            res=linprog(-self.Jcover[j],A_ub=-cone['gamma']/self.L,b_ub=np.zeros(len(cone['gamma'])),A_eq=[cone['c']],b_eq=[1],bounds=(0,None),method='highs')
            if res.success and (best is None or res.fun<best[0].fun):best=(res,j)
        return best

    def rational_point(self,cone,res,p=None,j=None):
        floating=res.x;support=np.flatnonzero(floating[:-1]>1e-8) if p is not None else np.flatnonzero(floating>1e-8)
        width=len(support)+(p is not None)
        eq=[[F(int(cone['c'][k])) for k in support]+([F(0)] if p is not None else [])];rhs=[F(1)]
        for row in cone['gamma']:
            if abs(row@floating[:self.k])<1e-6:
                eq.append([F(int(row[k])) for k in support]+([F(0)] if p is not None else []));rhs.append(F(0))
        if p is not None:
            for B,den in zip(self.B,self.static_den):
                row=[sum(p[a]*int(self.inc[k,a]) for a in range(self.m))/int(den[k]) for k in support]
                if abs(sum(float(x)*floating[k] for x,k in zip(row,support))-floating[-1])<1e-7:
                    eq.append(row+[F(-1)]);rhs.append(F(0))
        solved=exact_solve(eq,rhs,width)
        if solved is None:return None
        w=[F(0)]*self.k
        for k,x in zip(support,solved):w[k]=x
        if min(w)<0 or sum(F(int(c))*x for c,x in zip(cone['c'],w))!=1:return None
        if any(sum(F(int(g))*x for g,x in zip(row,w))<0 for row in cone['gamma']):return None
        if p is not None:
            t=solved[-1]
            for den in self.static_den:
                z=sum(w[k]*sum(p[a]*int(self.inc[k,a]) for a in range(self.m))/int(den[k]) for k in range(self.k))
                if z<t:return None
        return w

    def freeze(self,cone,w,label,source):
        scale=lcm(*(x.denominator for x in w));clones=[int(x*scale) for x in w]
        pol=[dict(history=h,action=int(a)) for h,a in zip(self.histories,cone['policy'])]
        game=dict(players=self.n,topics=list(range(self.m)),customers=[dict(mask=k+1,multiplicity=c) for k,c in enumerate(clones) if c])
        security=self.exact_security(clones)
        packet=dict(label=label,source=source,game=game,policy=pol,ordered_histories=len(pol),all_comparisons=len(pol)*self.m,policy_sha256=cone['digest'],normalization_scale=scale,security=security)
        path=OUT/(label+'.json');path.write_text(json.dumps(plain(packet),indent=2)+'\n')
        return path

    def exact_security(self,w):
        p,v,M,res=self.security(w)
        support=np.flatnonzero(p>1e-8)
        Mf=[]
        for den in self.static_den:
            Mf.append([sum((F(int(w[k]),int(den[k])) for k in range(self.k) if self.inc[k,a] and w[k]),F(0)) for a in range(self.m)])
        eq=[[F(1)]*len(support)+[F(0)]];rhs=[F(1)]
        for B,row in enumerate(Mf):
            if abs(sum(float(row[a])*p[a] for a in range(self.m))-v)<1e-6:
                eq.append([row[a] for a in support]+[F(-1)]);rhs.append(F(0))
        x=exact_solve(eq,rhs,len(support)+1)
        if x is None:return None
        primary=[F(0)]*self.m
        for a,k in zip(support,x):primary[a]=k
        value=x[-1]
        if min(primary)<0 or sum(primary)!=1:return None
        if any(sum(pa*y for pa,y in zip(primary,row))<value for row in Mf):return None
        fq=-res.ineqlin.marginals;qs=np.flatnonzero(fq>1e-8)
        deq=[[F(1)]*len(qs)];drhs=[F(1)]
        for a in range(self.m):
            if abs(sum(fq[B]*M[B,a] for B in qs)-v)<1e-6:
                deq.append([Mf[B][a] for B in qs]);drhs.append(value)
        q=exact_solve(deq,drhs,len(qs))
        if q is None or min(q)<0 or sum(q)!=1:return None
        if max(sum(Q*Mf[B][a] for B,Q in zip(qs,q)) for a in range(self.m))!=value:return None
        return dict(primary=primary,dual=[dict(rivals=self.B[B],probability=Q) for B,Q in zip(qs,q) if Q],value=value)

def grouped_seeds(m):
    groups=((0,1),(2,3),tuple(range(4,m)))
    allmask=(1<<m)-1
    seeds=[]
    def record(name,terms):
        w=np.zeros((1<<m)-1,dtype=np.int64)
        for mask,k in terms:w[mask-1]+=k
        seeds.append((name,w))
    record('three_group_transversal_complements',[(allmask-sum(1<<a for a in z),3) for z in product(*groups)])
    record('three_group_cross_edges',[(sum(1<<a for a in z),3) for i,j in ((0,1),(1,2),(2,0)) for z in product(groups[i],groups[j])])
    record('three_group_directed_reply',[(sum(1<<a for a in (x,)+tuple(b for b in groups[(i+1)%3] if b!=y)),3) for i,G in enumerate(groups) for x in G for y in groups[(i+1)%3]])
    record('group_core_plus_transversal',[(sum(1<<a for a in G),4) for G in groups]+[(sum(1<<a for a in z),2) for z in product(*groups)])
    record('complement_pairs',[(allmask-(1<<a)-(1<<b),1) for a,b in combinations(range(m),2)])
    for factor in (1,2,4):
        record('three_group_asymmetric_'+str(factor),[(allmask-sum(1<<a for a in z),3+factor*(z[0]==1)+factor*(z[1]==3)) for z in product(*groups)]+[(1<<a,1) for a in range(m)])
    return seeds

def rule_policy(s,pattern,pickmode):
    groups=((0,1),(2,3),tuple(range(4,s.m))) if pattern!=3 else ((0,1,2),tuple(range(3,s.m)))
    gi={a:i for i,G in enumerate(groups) for a in G}
    def pick(g,h):
        G=groups[g]
        if pickmode=='repeat':return G[0]
        if pickmode=='fresh':return min(G,key=lambda a:(h.count(a),a))
        if pickmode=='cycle':return G[sum(gi[a]==g for a in h)%len(G)]
        return max(G,key=lambda a:(h.count(a),-a))
    def action(h):
        d=len(h)
        if not d:return 0
        if pattern==1:
            if d==1:g=(gi[h[0]]+1)%len(groups)
            elif d==2:
                available=[g for g in range(len(groups)) if g not in {gi[a] for a in h}]
                g=available[0] if available else (gi[h[-1]]+1)%len(groups)
            else:g=gi[h[2]]
        elif pattern==2:
            g=(gi[h[0]]+d)%len(groups) if d<3 else gi[h[1]]
        else:g=1-gi[h[0]] if d==1 else gi[h[0]] if d==2 else gi[h[1]]
        return pick(g,h)
    return {h:action(h) for h in s.histories}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=5);ap.add_argument('--topics',type=int,default=7);ap.add_argument('--limit',type=int,default=16);args=ap.parse_args()
    s=Space(args.players,args.topics);records=[];seen=set();t0=time.time();best=0
    proposals=[]
    for pattern in (1,2,3):
        for pick in ('repeat','fresh','cycle','most'):
            proposals.append((s.full_policy(rule_policy(s,pattern,pick)),dict(kind='rule',pattern=pattern,pick=pick)))
    for name,w in grouped_seeds(s.m):
        for i,mode in enumerate(('random','root_min','root_max','welfare_min','welfare_max')):
            cone,meta=s.synthesize(w,817+31*i,mode);meta.update(kind='full_menu_synthesis',seed_family=name)
            proposals.append((cone,meta))
    for cone,meta in proposals:
        if cone['digest'] in seen:continue
        seen.add(cone['digest'])
        r=dict(source=meta,digest=cone['digest'],gamma_rows=len(cone['gamma']),root_counts=s.tc[cone['realized'][0]])
        res,beta=s.cone_security(cone,np.ones(s.m)/s.m)
        r['uniform_fixed_p_ratio']=float(-res.fun) if res.success else res.message
        half,j=s.cone_half(cone)
        r['max_OPT_over_W_float']=float(-half.fun);r['portfolio']=s.J[j]
        p,v,M,sec=s.security(half.x)
        r['half_vertex_nv_over_W_float']=s.n*v
        r['half_vertex_security_primary_float']=p
        for iteration in range(4):
            new,beta=s.cone_security(cone,p)
            if not new.success:break
            r.setdefault('alternate_ratios',[]).append(float(-new.fun))
            p2,v2,_,_=s.security(new.x[:s.k])
            if s.n*v2>1+1e-7:
                qp=tuple(F(float(x)).limit_denominator(10**6) for x in p)
                qp=qp[:-1]+(F(1)-sum(qp[:-1]),)
                point=s.rational_point(cone,new,p=qp)
                if point is not None:
                    path=s.freeze(cone,point,'candidate_'+cone['digest'][:10],r);r['candidate_file']=str(path)
            if np.max(np.abs(p2-p))<1e-7:break
            p=p2
        if r['max_OPT_over_W_float']>best+1e-6:
            best=r['max_OPT_over_W_float'];point=s.rational_point(cone,half,j=j)
            if point is not None:
                r['best_exact_half_packet']=str(s.freeze(cone,point,'half_best_'+cone['digest'][:10],r))
        records.append(r)
        print(json.dumps(plain(dict(index=len(records),source=meta,uniform=r['uniform_fixed_p_ratio'],OPT_over_W=r['max_OPT_over_W_float'],nv_over_W=r['half_vertex_nv_over_W_float'],alternate=r.get('alternate_ratios'),seconds=round(time.time()-t0,2)))),flush=True)
        (OUT/'search_report.json').write_text(json.dumps(plain(dict(parameters=vars(args),records=records,scope='finite new policy cones only; float LP candidate generator')),indent=2)+'\n')
        if len(records)>=args.limit:break


"""Candidate full-cone common-Q certificates, all queries and all Gamma rows."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, numpy as np
from scipy import sparse
from scipy.optimize import linprog


def common_q(s,cone,recover=True):
    G=cone['gamma']/s.L;r=len(G);nb=len(s.B)
    left=sparse.csr_matrix(s.static.transpose(1,2,0).reshape(s.m*s.k,nb))
    right=sparse.block_diag([sparse.csr_matrix(G.T)]*s.m)
    A=sparse.hstack([left,right],format='csr');b=np.tile(cone['c']/s.n,s.m)
    eq=sparse.csr_matrix(([1.]*nb,([0]*nb,list(range(nb)))),shape=(1,nb+s.m*r))
    # A random linear functional picks a vertex without changing feasibility.
    cost=np.concatenate([np.linspace(0,1,nb),np.zeros(s.m*r)])
    res=linprog(cost,A_ub=A,b_ub=b,A_eq=eq,b_eq=[1],bounds=(0,None),method='highs')
    out=dict(status=res.message,feasible=bool(res.success),variables=len(cost),coordinate_rows=len(b))
    if not res.success or not recover:return out
    support=np.flatnonzero(res.x>1e-8);out['positive_variables']=len(support)
    def verify(x):
        if min(x)<0 or sum(x[:nb])!=1:return False
        for a in range(s.m):
            for k in range(s.k):
                Q=sum((x[B]*F(int(s.inc[k,a]),int(s.static_den[B,k])) for B in range(nb) if x[B]),F(0))
                gamma=sum((x[nb+a*r+i]*F(int(cone['gamma'][i,k]),s.L) for i in range(r) if x[nb+a*r+i]),F(0))
                if F(int(cone['c'][k]),s.n)-Q-gamma<0:return False
        return True
    x=None
    for den in (1000,10000,100000,1000000,10000000):
        y=[F(0)]*len(cost)
        for j in support:y[j]=F(float(res.x[j])).limit_denominator(den)
        if verify(y):x=y;break
    if x is None:
        # Exact active equations restricted to the positive support.
        rows=[[F(int(j<nb)) for j in support]];rhs=[F(1)]
        active=np.flatnonzero(np.abs(A@res.x-b)<1e-7)
        for row in active:
            a,k=divmod(int(row),s.k);exact=[]
            for j in support:
                if j<nb:exact.append(F(int(s.inc[k,a]),int(s.static_den[j,k])))
                else:
                    query,i=divmod(int(j)-nb,r)
                    exact.append(F(int(cone['gamma'][i,k]),s.L) if query==a else F(0))
            rows.append(exact);rhs.append(F(int(cone['c'][k]),s.n))
        solved=exact_solve(rows,rhs,len(support))
        if solved is not None:
            y=[F(0)]*len(cost)
            for j,v in zip(support,solved):y[j]=v
            if verify(y):x=y
    out['exact_certified']=x is not None
    if x is not None:
        out['Q']=[dict(rivals=s.B[B],probability=x[B]) for B in range(nb) if x[B]]
        out['lambda']=[[dict(row=list(map(int,cone['gamma'][i])),coefficient=x[nb+a*r+i]) for i in range(r) if x[nb+a*r+i]] for a in range(s.m)]
        out['Gamma_scale']=s.L
    return out


from pathlib import Path
from fractions import Fraction as F
import json,time
import numpy as np


from policy_patterns import candidates

OUT=Path(__file__).resolve().parent

def batch():
    spaces={};results=[];cases=[];seen=set();t0=time.time()
    def get(n,m):
        if (n,m) not in spaces:spaces[n,m]=Space(n,m)
        return spaces[n,m]
    proposals=[]
    for P in candidates():
        s=get(P.n,P.m);proposals.append((s,s.full_policy(P.actions()),dict(kind='ordered_group_rule',name=P.name,n=P.n,m=P.m),None))
    s=get(5,7)
    for name,w in grouped_seeds(7):
        if name not in ('three_group_transversal_complements','three_group_cross_edges','three_group_directed_reply','group_core_plus_transversal'):continue
        for i,mode in enumerate(('random','root_min','root_max')):
            cone,meta=s.synthesize(w,817+31*i,mode);meta.update(kind='full_menu_synthesis',seed_family=name)
            proposals.append((s,cone,meta,w))
    for s,cone,source,seed in proposals:
        if cone['digest'] in seen:continue
        seen.add(cone['digest']);q=common_q(s,cone)
        r=dict(source=source,digest=cone['digest'],Gamma_rows=len(cone['gamma']),ordered_histories=len(s.histories),all_comparisons=len(s.histories)*s.m,root_counts=s.tc[cone['realized'][0]],joint_q={k:v for k,v in q.items() if k not in ('Q','lambda')})
        if q.get('exact_certified'):
            case=dict(name=cone['digest'][:12],source=source,players=s.n,topics=s.m,policy=[dict(history=h,action=int(a)) for h,a in zip(s.histories,cone['policy'])],certificate=q)
            cases.append(case)
        else:
            p=np.ones(s.m)/s.m
            trial=[]
            for k in range(8):
                if k==1 and seed is not None:p,_,_,_=s.security(seed)
                res,beta=s.cone_security(cone,p);trial.append(float(-res.fun))
                p,_,_,_=s.security(res.x[:s.k])
            r['fixed_p_float_ratios']=trial
            path=OUT/('unresolved_'+cone['digest'][:12]+'.json')
            path.write_text(json.dumps(plain(dict(source=source,game=dict(players=s.n,topics=list(range(s.m)),customers=[]),policy=[dict(history=h,action=int(a)) for h,a in zip(s.histories,cone['policy'])])),indent=2)+'\n')
            r['full_policy_file']=str(path)
        results.append(r)
        print(json.dumps(plain(dict(index=len(results),source=source,Gamma=len(cone['gamma']),Q=r['joint_q'],elapsed=round(time.time()-t0,2)))),flush=True)
        (OUT/'cone_batch_results.json').write_text(json.dumps(plain(dict(scope='specified new complete policy cones, all type weights and all query distributions for certified cases',results=results)),indent=2)+'\n')
        (OUT/'new_cone_certificate_pack.json').write_text(json.dumps(plain(dict(scope='new specified full policy cones only; no universal SPE theorem',cases=cases)),indent=2)+'\n')
    return results


if __name__=='__main__':
    ap=argparse.ArgumentParser(description='Floating candidate regeneration; independent exact checker is authoritative.')
    ap.add_argument('--output',required=True,type=Path);args=ap.parse_args()
    OUT=args.output;OUT.mkdir(parents=True,exist_ok=True);batch()
