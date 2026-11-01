"""Exact verification of the named fixed-T joint-payment candidate on two old SPE packets.

This is not a scan or general evidence.  scipy chooses a point; every retained
feasible point is reconstructed over Fraction and checked against every row.
All original complete-history IC rows and the stated optimum are checked exactly.
"""
from collections import defaultdict, deque
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import hashlib
import json
import scipy.optimize as so

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[2]


class LP:
    def __init__(self):
        self.keys=[];self.ids={};self.bounds=[];self.eq=[];self.ub=[]
    def var(self,key,cap=None):
        assert key not in self.ids
        self.ids[key]=len(self.keys);self.keys.append(key)
        self.bounds.append((F(),cap));return self.ids[key]
    def equality(self,row,rhs=F()):self.eq.append((dict(row),F(rhs)))
    def upper(self,row,rhs):self.ub.append((dict(row),F(rhs)))
    def solve(self):
        def mat(rows):
            out=[]
            for row,rhs in rows:
                r=[0.]*len(self.keys)
                for j,v in row.items():r[j]=float(v)
                out.append(r)
            return out
        out=so.linprog([0.]*len(self.keys),A_eq=mat(self.eq) or None,
              b_eq=[float(b) for _,b in self.eq] or None,
              A_ub=mat(self.ub) or None,b_ub=[float(b) for _,b in self.ub] or None,
              bounds=[(float(a),None if b is None else float(b)) for a,b in self.bounds],
              method='highs')
        if not out.success:return None,{'numerical_status':out.message}
        for denominator in (10**4,10**6,10**9,10**12):
            v=[F(float(x)).limit_denominator(denominator) for x in out.x]
            ok=all(a<=x and (b is None or x<=b) for x,(a,b) in zip(v,self.bounds))
            ok &= all(sum((q*v[j] for j,q in row.items()),F())==b for row,b in self.eq)
            ok &= all(sum((q*v[j] for j,q in row.items()),F())<=b for row,b in self.ub)
            if ok:return v,{'exact_point_verified':True,'denominator_limit':denominator}
        return None,{'numerical_status':out.message,'exact_point_verified':False}


def audit(name,path,T):
    raw=path.read_bytes();obj=json.loads(raw);I=obj['instance']
    m=I['players'];K=len(I['topics']);types=[frozenset(t['topics']) for t in I['customers']]
    mult=[t.get('multiplicity',1) for t in I['customers']]
    sigma={tuple(t['history']):t['action'] for t in obj['certificate']['actions']}
    assert set(sigma)=={h for j in range(m) for h in product(range(K),repeat=j)}
    def finish(h):
        h=tuple(h)
        while len(h)<m:h+=(sigma[h],)
        return h
    def counts(z):return [sum(a in s for a in z) for s in types]
    def payoff(z,i):
        c=counts(z)
        return sum((F(mult[x],c[x]) for x,s in enumerate(types) if z[i] in s),F())
    def welfare(z):return sum(mult[x] for x,s in enumerate(types) if any(a in s for a in z))
    ic=0
    for h in sigma:
        z=finish(h)
        for a in range(K):assert payoff(z,len(h))>=payoff(finish(h+(a,)),len(h));ic+=1
    B=finish(());cb=counts(B);ct=counts(T);u=[payoff(B,i) for i in range(m)]
    opt=max(welfare(z) for z in combinations_with_replacement(range(K),m))
    assert welfare(T)==opt
    O=[x for x in range(len(types)) if ct[x]]
    II=[x for x in O if cb[x]];RR=[x for x in O if not cb[x]]
    H=[[F() for x in types] for i in range(m)]
    P={};r={};edges={};W={};cW={}
    for i in range(m):
        W[i]=finish(B[:i]+(T[i],));cW[i]=counts(W[i])
        for x in O:
            if T[i] not in types[x]:continue
            p=F(mult[x],ct[x]);delta=cb[x]+1-int(B[i] in types[x])
            paid=F()
            for l in range(m):
                if l!=i and B[l] in types[x] and T[l] not in types[x]:
                    q=p/delta;H[l][x]+=q;paid+=q
            P[i,x]=p;r[i,x]=p-paid
            edges[i,x]={j:min(p,F(mult[x],delta))/cW[i][x] for j in range(i+1,m)
                        if W[i][j] in types[x] and B[j] not in types[x]}
    for l in range(m):
        for x in II:assert H[l][x]<= (F(mult[x],cb[x]) if B[l] in types[x] else 0)
    lp=LP();c={};a={};J={};h={};L={};z={};initial=defaultdict(list)
    for (i,x),p in P.items():
        c[i,x]=lp.var(('c',i,x))
        row={c[i,x]:F(1)}
        for j,cap in edges[i,x].items():
            a[i,j,x]=lp.var(('a',i,j,x),cap);row[a[i,j,x]]=F(1)
            if x in RR:initial[W[i][:j],x].append(a[i,j,x])
        lp.equality(row,r[i,x])
    for i in range(m):lp.upper({j:F(1) for (ii,x),j in c.items() if ii==i},u[i])
    for x in II:
        row={}
        for l in range(m):
            cap=(F(mult[x],cb[x]) if B[l] in types[x] else 0)-H[l][x]
            J[l,x]=lp.var(('J',l,x),cap);row[J[l,x]]=F(1)
        for (i,j,xx),idx in a.items():
            if xx==x:row[idx]=F(-1)
        lp.equality(row)
    # Exact fixed data for the complete closure of all optional R edges.
    queue=deque(initial);seen=set(initial);dat={}
    while queue:
        g,x=queue.popleft();k=len(g);act=sigma[g];assert act in types[x]
        V=finish(g);A=finish(B[:k]+(act,));ca=counts(A)[x]
        Q=[j for j in range(k+1,m) if A[j] in types[x]]
        dat[g,x]=(A,ca,Q,{j for j in Q if V[j] not in types[x]})
        for j in Q:
            target=(A[:j],x)
            if target not in seen:seen.add(target);queue.append(target)
    for g,x in sorted(dat,key=lambda q:(len(q[0]),q[0],q[1])):
        h[g,x]=lp.var(('h',g,x));L[g,x]=lp.var(('L',g,x))
        A,ca,Q,N=dat[g,x]
        for j in Q:z[g,j,x]=lp.var(('z',g,j,x))
    incoming=defaultdict(list)
    for (g,j,x),idx in z.items():incoming[dat[g,x][0][:j],x].append(idx)
    for g,x in dat:
        row={h[g,x]:F(1)}
        for idx in initial[g,x]+incoming[g,x]:row[idx]=row.get(idx,F())-1
        lp.equality(row)
        A,ca,Q,N=dat[g,x]
        row={L[g,x]:F(1),h[g,x]:F(-1)}
        for j in Q:
            idx=z[g,j,x];row[idx]=F(1)
            erow={idx:F(1),h[g,x]:-F(1,ca)}
            if j in N:lp.equality(erow)
            else:lp.upper(erow,0)
        lp.equality(row)
    role=[]
    for l in range(m):
        row={idx:F(1) for (i,x),idx in c.items() if i==l}
        row.update({idx:F(1) for (ll,x),idx in J.items() if ll==l})
        row.update({idx:F(1) for (g,x),idx in L.items() if len(g)==l})
        fixed=sum(H[l],F());role.append((row,fixed));lp.upper(row,2*u[l]-fixed)
    point,status=lp.solve()
    result={'fixture':name,'source_sha256':hashlib.sha256(raw).hexdigest(),'players':m,
            'T':T,'actual':B,'actual_profit':list(map(str,u)),'W':welfare(B),'OPT':opt,
            'full_history_IC_checked':ic,'variables':len(lp.keys),'equalities':len(lp.eq),
            'inequalities':len(lp.ub),'R_types':len(RR),'R_context_client_pairs':len(dat),**status}
    if point is not None:
        loads=[fixed+sum((q*point[idx] for idx,q in row.items()),F()) for row,fixed in role]
        assert sum(loads,F())==opt
        result['role_load']=list(map(str,loads));result['role_slack']=list(map(str,[2*u[i]-loads[i] for i in range(m)]))
        result['nonzero_point']=[{'variable':key,'amount':str(v)} for key,v in zip(lp.keys,point) if v]
    return result


if __name__=='__main__':
    fixtures=[('old_static_assignment_52',BASE/'R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json',(0,1,4,5)),
              ('high_insertion_2cycle_348',BASE/'R-d22a706a03c5499d941a6a97f94128a8/representation/high_insertion_2cycle_348_exact.json',(5,2,4))]
    out={'candidate':'For every original instance/full-history pure SPE, an optimal T has feasible round8 fixed-T payment primal.',
         'scope':'Two named old exact SPE fixtures only, not a scan and not general feasibility evidence.',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'fixtures':[audit(*args) for args in fixtures]}
    target=HERE/'named_primal_exact.json'
    with target.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({**{k:v for k,v in out.items() if k!='fixtures'},'fixtures':[
        {k:v for k,v in z.items() if k!='nonzero_point'} for z in out['fixtures']]},indent=2))
