"""Independent exact audit of two frozen saved files; no original module import or LP.

Rebuilds every saved DP/cone/menu, and derives exact saddles from saved supports.
Outputs audit.json beside this file. This is a fixed-input audit, not random search.
"""
from pathlib import Path
from itertools import combinations_with_replacement
from fractions import Fraction as F
from math import lcm, isfinite
from collections import Counter
import json,hashlib
HERE=Path(__file__).resolve().parent
SRC=HERE/'source-root/research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/round4_security'

def solve(A,b):
    A=[[F(x) for x in r]+[F(y)] for r,y in zip(A,b)];n=len(A[0])-1;piv=[];r=0
    for c in range(n):
        z=next((i for i in range(r,len(A)) if A[i][c]),None)
        if z is None:continue
        A[r],A[z]=A[z],A[r];v=A[r][c];A[r]=[x/v for x in A[r]]
        for i in range(len(A)):
            if i!=r:
                v=A[i][c];A[i]=[x-v*y for x,y in zip(A[i],A[r])]
        piv.append(c);r+=1
    assert all(any(row[:n]) or not row[n] for row in A)
    assert len(piv)==n,('nonunique',piv,n)
    ans=[F(0)]*n
    for i,c in enumerate(piv):ans[c]=A[i][-1]
    return ans

def vectors(n,k):
    return [tuple(t.count(a) for a in range(k)) for t in combinations_with_replacement(range(k),n)]
class Exact:
    def __init__(self,n,k,w):
        self.n=n;self.k=k;self.w=tuple(w);self.L=lcm(*range(1,n+1));self.cts=[vectors(d,k) for d in range(n+1)];self.final=self.cts[n];self.fi={q:i for i,q in enumerate(self.final)}
        self.co=[];self.u=[];self.W=[]
        for q in self.final:
            loads=[sum(q[a] for a in range(k) if mask>>a&1) for mask in range(1,1<<k)]
            co=[tuple(self.L//max(1,load) if mask>>a&1 else 0 for mask,load in enumerate(loads,1)) for a in range(k)]
            self.co.append(co);self.u.append([sum(x*y for x,y in zip(row,w)) for row in co]);self.W.append(sum(x for x,l in zip(w,loads) if l))
        self.O={q:[i] for q,i in self.fi.items()}
        for d in reversed(range(n)):
            for q in self.cts[d]:
                C=[self.O[self.child(q,a)] for a in range(k)];floor=max(min(self.u[j][a] for j in child) for a,child in enumerate(C))
                self.O[q]=sorted({j for a,child in enumerate(C) for j in child if self.u[j][a]>=floor})
        self.root=min(self.O[(0,)*k],key=lambda j:self.W[j])
    def child(self,q,a):return tuple(c+int(j==a) for j,c in enumerate(q))
    def choose(self,q,t):
        C=[self.O[self.child(q,a)] for a in range(self.k)];floor=max(min(self.u[j][a] for j in child) for a,child in enumerate(C));a=next(a for a,child in enumerate(C) if t in child and self.u[t][a]>=floor)
        return a,[t if b==a else min(child,key=lambda j:self.u[j][b]) for b,child in enumerate(C)]
    def menu(self):
        q=(0,)*self.k;t=self.root;path=[];menus=set()
        while sum(q)<self.n:
            a,D=self.choose(q,t);path.append(a)
            for b,j in enumerate(D):menus.add(tuple(c-int(z==b) for z,c in enumerate(self.final[j])))
            q=self.child(q,a)
        return path,sorted(menus)
    def cone(self):
        stack=[((0,)*self.k,self.root)];seen=set();rows=set();nodes=[]
        while stack:
            q,t=stack.pop()
            if (q,t) in seen or sum(q)==self.n:continue
            seen.add((q,t));a,D=self.choose(q,t);nodes.append({'counts':q,'target':self.final[t],'action':a,'children_targets':[self.final[j] for j in D]})
            for b,j in enumerate(D):
                stack.append((self.child(q,b),j));row=tuple(x-y for x,y in zip(self.co[t][a],self.co[j][b]))
                if any(row):rows.add(row)
        return sorted(rows),nodes
    def pay(self,h,a):return sum((F(w,1+sum(h[b] for b in range(self.k) if mask>>b&1)) for mask,w in enumerate(self.w,1) if mask>>a&1),F(0))
    def saddle(self,p0,Q0,H=None):
        H=H if H is not None else self.cts[self.n-1];I=[a for a,p in enumerate(p0) if p>1e-9];J=[tuple(z['counts']) for z in Q0 if z['probability']>1e-9]
        P=[self.pay(h,a) for h in J for a in I]
        p=solve([[self.pay(h,a) for a in I]+[-1] for h in J]+[[1]*len(I)+[0]],[0]*len(J)+[1]);v=p[-1];p=p[:-1]
        Q=solve([[self.pay(h,a) for h in J]+[-1] for a in I]+[[1]*len(J)+[0]],[0]*len(I)+[1]);assert Q[-1]==v;Q=Q[:-1]
        assert min(p)>=0 and min(Q)>=0 and sum(p)==sum(Q)==1
        assert all(h in H for h in J)
        for a,t in zip(I,p):near(p0[a],t)
        for h,t in zip(J,Q):near(next(z['probability'] for z in Q0 if tuple(z['counts'])==h),t)
        low=min(sum(t*self.pay(h,a) for t,a in zip(p,I)) for h in H);high=max(sum(t*self.pay(h,a) for t,h in zip(Q,J)) for a in range(self.k));assert low==v==high
        return {'value':str(v),'query':{str(a):str(t) for a,t in zip(I,p)},'backgrounds':[{'counts':h,'probability':str(t)} for h,t in zip(J,Q)],'backgrounds_checked':len(H),'pure_queries_checked':self.k}

def walk(x):
    """Visit every scalar (including every matrix coefficient), reject nonfinite floats."""
    c=Counter()
    def f(y):
        c[type(y).__name__]+=1
        if isinstance(y,dict):
            for k,v in y.items():f(k);f(v)
        elif isinstance(y,list):
            for v in y:f(v)
        elif isinstance(y,float):assert isfinite(y)
    f(x);return dict(c)

def near(a,b):assert abs(float(a)-float(b))<1e-8,(a,b)

def base_check(z,e):
    assert len(z['weights'])==(1<<e.k)-1 and all(isinstance(w,int) and w>=0 for w in z['weights'])
    rootset=e.O[(0,)*e.k];m=min(e.W[j] for j in rootset);assert m==z['min_welfare'];assert max(e.W)==z['max_welfare'];assert [list(e.final[j]) for j in rootset if e.W[j]==m]==z['worst_counts']
    saddle=e.saddle(z['query'],z['rivals']);v=F(saddle['value']);near(z['value'],v);near(z['gap'],m-e.n*v);near(z['relative_gap'],F(m,e.n)/v-1)
    excess=max([0]+[e.u[e.fi[tuple(c-int(t==a)+int(t==b) for t,c in enumerate(e.final[j]))]][b]-e.u[j][a] for j in rootset if e.W[j]==m for a in range(e.k) if e.final[j][a] for b in range(e.k)])
    near(z['static_deviation_excess'],F(excess,e.L));assert z['has_nonPNE_worst_outcome']==(excess>0)
    return saddle

def main():
    paths=[SRC/'menu_n4k6.json',SRC/'menu_cone_n5k6.json'];xs=[json.loads(p.read_text()) for p in paths]
    report={'scope':'fixed saved inputs only; no original import/main, RNG or numerical LP','files':[{'name':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'all_scalar_traversal':walk(x)} for p,x in zip(paths,xs)],'n4_records':[],'n5_records':[]}
    cache={};cones={}
    def get(z):
        key=(z['n'],z['k'],tuple(z['weights']))
        if key not in cache:cache[key]=Exact(*key[:2],key[2])
        return cache[key]
    x=xs[0]
    for label,z in [('best',x['best'])]+[(f'bank/{i}',z) for i,z in enumerate(x['bank'])]:
        e=get(z);saddle=base_check(z,e);path,menu=e.menu();assert path==z['actual_path'];assert menu==list(map(tuple,z['menu_counts']));restricted=e.saddle(z['restricted_query'],z['restricted_Q'],menu);v=F(restricted['value']);W=z['min_welfare'];near(z['restricted_value'],v);near(z['restricted_gap'],W-e.n*v);near(z['restricted_weak_gap'],W-(F(e.n)-F(1,2))*v);near(z['restricted_relative_gap'],(W-e.n*v)/W)
        report['n4_records'].append({'record':label,'weights_sha256':hashlib.sha256(json.dumps(z['weights']).encode()).hexdigest(),'customers':sum(z['weights']),'W':W,'OPT':z['max_welfare'],'path':path,'menu':menu,'security_saddle':saddle,'restricted_saddle':restricted,'strong_gap':str(W-e.n*v),'weak_gap':str(W-(F(e.n)-F(1,2))*v)})
    for i,z in enumerate(xs[1]['results']):
        e=get(z['initial']);initial=base_check(z['initial'],e);path,menu=e.menu();rows,nodes=e.cone();assert path==z['actual_path'];assert menu==list(map(tuple,z['menu_counts']));assert list(e.final[e.root])==z['root_counts'];assert rows==list(map(tuple,z['rows']));assert len(nodes)==z['policy_subproblems'];w=[F(str(t)) for t in z['weights']];assert all(t>=0 for t in w);assert all(sum(a*b for a,b in zip(row,w))>=0 for row in rows)
        assert sum(w[mask-1] for mask in range(1,1<<e.k) if any(e.final[e.root][a] and mask>>a&1 for a in range(e.k)))==1
        endpoint=Exact(e.n,e.k,w);B=[[endpoint.pay(h,a) for a in range(e.k)] for h in menu];p=list(map(lambda t:F(str(t)),z['query']));assert min(p)>=0 and sum(p)==1;v=min(sum(a*b for a,b in zip(row,p)) for row in B);assert v==F(1,5);assert all(max(row)==v for row in B)
        for t,j in enumerate(z['trace']):assert j['iteration']==t;near(j['value'],v);near(j['gap'],1-e.n*v);near(j['weak_gap'],1-(F(e.n)-F(1,2))*v);near(j['spe_margin'],min(sum(a*b for a,b in zip(row,w)) for row in rows))
        # Exact final point has one unit type; keep its mathematical identity separate from float search status.
        assert sum(t!=0 for t in w)==1 and sum(w)==1
        rec={'record':i,'seed_weights_sha256':hashlib.sha256(json.dumps(z['initial']['weights']).encode()).hexdigest(),'seed_customers':sum(z['initial']['weights']),'seed_W':z['initial']['min_welfare'],'seed_OPT':z['initial']['max_welfare'],'initial_security_saddle':initial,'policy_subproblems':len(nodes),'rows':len(rows),'all_row_coefficients':len(rows)*len(w),'endpoint_nonzero_types':[(mask,str(t)) for mask,t in enumerate(w,1) if t],'endpoint_W':'1','endpoint_menu_value':str(v),'strong_gap':str(1-e.n*v),'weak_gap':str(1-(F(e.n)-F(1,2))*v),'trace_entries':len(z['trace'])}
        report['n5_records'].append(rec);cones[str(i)]={'nodes':nodes}
    report['unique_integer_saved_inputs']=len(cache);report['n4_unique_records']=len({tuple(z['weights']) for z in [xs[0]['best']]+xs[0]['bank']});report['n5_unique_integer_seeds']=len({tuple(z['initial']['weights']) for z in xs[1]['results']});report['all_checks_passed']=True
    (HERE/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(HERE/'reconstructed-policy-dags.json').write_text(json.dumps(cones,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'passed':True,'unique_integer_inputs':len(cache),'n4_unique':report['n4_unique_records'],'n5_unique_seeds':report['n5_unique_integer_seeds'],'n4_records':len(report['n4_records']),'n5_records':len(report['n5_records']),'all_rows':sum(z['rows'] for z in report['n5_records']),'all_coefficients':sum(z['all_row_coefficients'] for z in report['n5_records'])}))
if __name__=='__main__':main()
