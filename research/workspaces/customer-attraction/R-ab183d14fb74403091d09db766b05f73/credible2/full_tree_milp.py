"""Discovery MILP selecting every ordered-history credible subtree simultaneously.

For a fixed root count vector and root action, this is a union of *all* full
pure SPE strategy cones, not a sampled fixed policy. Floating MIP results never
certify a universal result. Accepted witnesses are rationalized and checked by
the independent canonical definition-level verifier and outcome-set solver.
"""
from __future__ import annotations
from pathlib import Path
from itertools import product
from fractions import Fraction as F
from functools import lru_cache
import argparse, json, sys, time
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint, linprog
from scipy.sparse import coo_matrix
BASE=Path(__file__).resolve().parent
ROOT=next(p for p in BASE.parents if (p/'customer_attraction/__init__.py').is_file())
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits'),str(BASE.parent/'credible')]
from customer_attraction import Instance, CustomerType, ExactSPESolver, StrategyCertificate, verify_certificate
from customer_attraction_strategy_lp import StrategyCone, payoff_row, integer_clones, dot
from fractional_query_vertices import enumerate_vertices


@lru_cache(None)
def compositions(total,p):
    if p==1:return ((total,),)
    return tuple((a,)+b for a in range(total+1) for b in compositions(total-a,p-1))


class Model:
    def __init__(self,p,m,q,root_action,kind,queries=None,root_hull=False,min_distance=0,objective_rows=None):
        self.p=p;self.m=m;self.q=tuple(q);self.root_action=root_action;self.kind=kind;self.min_distance=min_distance
        if p<2 or m<1 or not 0<=root_action<p or len(q)!=p or any(x<0 for x in q) or sum(q)!=m or q[root_action]<1:raise ValueError('invalid fixed root')
        self.n=(1<<p)-1;self.lb=[0.]*self.n;self.ub=[1.]*self.n;self.integrality=[0]*self.n
        self.obj=[0.]*self.n;self.row=[];self.col=[];self.val=[];self.cl=[];self.cu=[]
        self.A={};self.T={};self.Q={};self.histories=[h for d in range(m) for h in product(range(p),repeat=d)]
        for h in self.histories:
            counts=tuple(h.count(a) for a in range(p))
            self.Q[h]=tuple(tuple(x+y for x,y in zip(counts,s)) for s in compositions(m-len(h),p))
            if not h:self.Q[h]=(self.q,)
            for a in range(p):self.A[h,a]=self.new(0,1,1) if h else int(a==root_action)
            for t in self.Q[h]:
                # At the last layer the chosen action already specifies terminal.
                if len(h)==m-1:
                    a=next(a for a in range(p) if t[a]>counts[a]);self.T[h,t]=self.A[h,a]
                elif h:self.T[h,t]=self.new(0,1,1)
                else:self.T[h,t]=1
        self.add({i:1 for i in range(self.n)},1,1)
        # Guaranteed without any rationality of later responses: choose a theme
        # and every one of its customers has final load at most m.
        root_u=payoff_row(p,self.q,root_action)
        for a in range(p):
            self.add({k:float(F(bool((k+1)>>a&1),m)-root_u[k]) for k in range(self.n)},-np.inf,0)
        if min_distance:
            for a in range(p):
                for b in range(a):
                    self.add({k:1 for k in range(self.n) if bool((k+1)>>a&1)!=bool((k+1)>>b&1)},min_distance,np.inf)
        for h in self.histories:
            if h:self.add({self.A[h,a]:1 for a in range(p)},1,1)
            if h and len(h)<m-1:self.add({self.T[h,t]:1 for t in self.Q[h]},1,1)
            if len(h)<m-1:
                for a in range(p):
                    child=h+(a,)
                    # If a is chosen, node terminal equals terminal of child a.
                    for t in self.Q[h]:
                        terms=[(self.T[h,t],1),(self.A[h,a],1)]
                        if t in self.Q[child]:terms.append((self.T[child,t],-1))
                        self.indicator_row(terms,1)
            # Every true deviation compares the selected node terminal with the
            # selected alternative child terminal; no terminal is frozen.
            for a in range(p):
                if not h and a!=root_action:continue
                actual=[t for t in self.Q[h] if t[a]>h.count(a)]
                for b in range(p):
                    if b==a:continue
                    child=h+(b,)
                    alt=(tuple(child.count(c) for c in range(p)),) if len(child)==m else self.Q[child]
                    for t in actual:
                        u=payoff_row(p,t,a)
                        for v in alt:
                            d=tuple(x-y for x,y in zip(u,payoff_row(p,v,b)))
                            # Under sum(r)=1 both payoffs lie in [0,1], so M=1.
                            indicators=[(self.A[h,a],1),(self.T[h,t],1)]
                            if len(child)<m:indicators.append((self.T[child,v],1))
                            self.indicator_row(indicators,len(indicators),{k:-float(x) for k,x in enumerate(d) if x})
        self.hull_variables={}
        if root_hull and m>1:
            # Exact simplex disaggregation of r times each first-child terminal
            # selector. Its LP relaxation strengthens root comparisons, while
            # binary points project to exactly the same complete-strategy set.
            for b in range(p):
                h=(b,)
                for t in self.Q[h]:
                    for k in range(self.n):self.hull_variables[h,t,k]=self.new(0,1,0)
                for k in range(self.n):
                    self.add({**{self.hull_variables[h,t,k]:1 for t in self.Q[h]},k:-1},0,0)
                for t in self.Q[h]:
                    self.add({**{self.hull_variables[h,t,k]:1 for k in range(self.n)},self.T[h,t]:-1},0,0)
                if b!=root_action:
                    coeffs={k:-float(root_u[k]) for k in range(self.n)}
                    for t in self.Q[h]:
                        for k,x in enumerate(payoff_row(p,t,b)):
                            if x:coeffs[self.hull_variables[h,t,k]]=float(x)
                    self.add(coeffs,-np.inf,0)
        self.queries=tuple(queries) if queries is not None else enumerate_vertices(p)[0]
        self.g=self.new(-float(m+2),1,0);self.obj[self.g]=-1
        self.Z=[];self.objectives=[]
        w=tuple(F(any(q[a] and mask>>a&1 for a in range(p))) for mask in range(1,1<<p))
        u=payoff_row(p,self.q,root_action)
        for zi,z in enumerate(self.queries):
            tau=sum(z);cover=tuple(min(F(1),sum(z[a] for a in range(p) if mask>>a&1)) for mask in range(1,1<<p))
            if objective_rows is not None:c=tuple(map(F,objective_rows[zi]))
            elif kind=='tstar':c=tuple(x-(m-1+tau)*y for x,y in zip(cover,u))
            elif kind=='price_plus_u':c=tuple(x-(tau-1)*y-v for x,y,v in zip(cover,u,w))
            elif kind=='weakfloor':
                # Queries for this target are indicator optimal portfolios.
                c=tuple(x-(2*m-1)*y for x,y in zip(cover,u))
            elif kind=='half':c=tuple(x-2*v for x,v in zip(cover,w))
            else:raise ValueError('unknown target')
            self.objectives.append(c);j=self.new(0,1,1);self.Z.append(j)
            # max c.r is at most 1 and at least -(m+p); chosen query controls g.
            M=1+max(F(0),-min(c))
            self.add({**{k:-float(x) for k,x in enumerate(c) if x},self.g:1,j:float(M)},-np.inf,float(M))
        self.add({j:1 for j in self.Z},1,1)

    def new(self,lo,hi,integer):
        i=len(self.lb);self.lb.append(float(lo));self.ub.append(float(hi));self.integrality.append(integer);self.obj.append(0.);return i

    def add(self,coefs,lo,hi):
        i=len(self.cl)
        for j,x in coefs.items():
            if x:self.row.append(i);self.col.append(j);self.val.append(x)
        self.cl.append(float(lo));self.cu.append(float(hi))

    def indicator_row(self,indicators,upper,coefs=None):
        coefs=dict(coefs or {})
        for variable,coefficient in indicators:
            # Root indicators are literal 0/1; other indicators are indices n+.
            if variable in (0,1):upper-=coefficient*variable
            else:coefs[variable]=coefs.get(variable,0)+coefficient
        self.add(coefs,-np.inf,upper)

    def solve(self,seconds=60,gap=1e-7):
        mat=coo_matrix((self.val,(self.row,self.col)),shape=(len(self.cl),len(self.lb))).tocsc()
        start=time.monotonic()
        out=milp(np.array(self.obj),integrality=np.array(self.integrality),bounds=Bounds(self.lb,self.ub),
                 constraints=LinearConstraint(mat,self.cl,self.cu),options={'time_limit':seconds,'mip_rel_gap':gap})
        result={'scope':'fixed root counts and root action; all ordered-history pure policies; floating discovery only',
                'p':self.p,'m':self.m,'root':self.q,'root_action':self.root_action,'kind':self.kind,
                'variables':len(self.lb),'binaries':sum(self.integrality),'constraints':len(self.cl),'queries':len(self.queries),
                'root_hull':bool(self.hull_variables),
                'min_pairwise_physical_distance_per_total':self.min_distance,
                'status':int(out.status),'message':out.message,'elapsed':time.monotonic()-start,'universal_proof':False}
        if getattr(out,'mip_dual_bound',None) is not None:result['floating_upper_bound']=-out.mip_dual_bound
        if out.x is None:return result
        result['floating_gap']=-out.fun
        actions={h:max(range(self.p),key=lambda a:float(self.A[h,a]) if not h else out.x[self.A[h,a]]) for h in self.histories}
        cone=StrategyCone(self.p,self.m,actions)
        if cone.root!=self.q:raise AssertionError('MILP selected inconsistent root')
        # Re-optimize selected exact cone/query, then recover its rational vertex.
        j=max(range(len(self.Z)),key=lambda j:out.x[self.Z[j]])
        c=self.objectives[j]
        A=list(-cone.matrix);rhs=[0.]*len(A)
        if self.min_distance:
            for a in range(self.p):
                for b in range(a):
                    A.append([-float(bool((k+1)>>a&1)!=bool((k+1)>>b&1)) for k in range(self.n)])
                    rhs.append(-self.min_distance)
        lp=linprog(-np.array(c,float),A_ub=A,b_ub=rhs,A_eq=[np.ones(self.n)],b_eq=[1],bounds=(0,None),method='highs')
        if not lp.success:raise AssertionError('selected MILP policy has no nonzero SPE cone')
        vals=tuple(F(float(x)).limit_denominator(10**8) for x in lp.x)
        if not cone.verify(vals):result['recovery']='rational direct recovery failed';return result
        clones=integer_clones(vals)
        game=Instance(tuple(f'T{a}' for a in range(self.p)),tuple(CustomerType(frozenset(a for a in range(self.p) if mask>>a&1),n) for mask,n in enumerate(clones,1) if n),self.m)
        cert=StrategyCertificate(actions,cone.root);check=verify_certificate(game,cert);check.assert_valid()
        if cone.root not in ExactSPESolver(game).outcomes():raise AssertionError('canonical solver rejects selected policy root')
        gap=dot(c,clones);topic_sets=[frozenset(i for i,t in enumerate(game.customers) if a in t.topics) for a in range(self.p)]
        result['candidate']={'instance':game.to_dict(),'strategy':cert.to_dict(),'query':[str(x) for x in self.queries[j]],'gap':str(gap),
            'gap_per_total':str(gap/sum(clones)),'u':str(game.topic_payoffs(cone.root)[self.root_action]),'W':game.welfare(cone.root),
            'OPT':game.optimal_welfare(),'physical_topics':len(set(topic_sets)),'histories':check.checked_histories,'deviations':check.checked_deviations,
            'canonical_solver_root_checked':True,'accepted_counterexample':gap>0 and len(set(topic_sets))==self.p}
        return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--p',type=int,default=4);ap.add_argument('--m',type=int,default=3)
    ap.add_argument('--root',default='1,0,0,2');ap.add_argument('--root-action',type=int,default=0)
    ap.add_argument('--kind',choices=['tstar','price_plus_u','weakfloor','half'],default='tstar')
    ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--root-hull',action='store_true');ap.add_argument('--min-distance',type=float,default=0);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();q=tuple(map(int,args.root.split(',')))
    queries=None
    if args.kind in ('weakfloor','half'):
        queries=tuple(tuple(F(bool(mask>>a&1)) for a in range(args.p)) for mask in range(1,1<<args.p) if mask.bit_count()<=args.m)
    model=Model(args.p,args.m,q,args.root_action,args.kind,queries,args.root_hull,args.min_distance)
    result=model.solve(args.seconds);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='candidate'},indent=2),flush=True)
    if 'candidate' in result:print(json.dumps({k:v for k,v in result['candidate'].items() if k not in ('instance','strategy')},indent=2))

if __name__=='__main__':main()
