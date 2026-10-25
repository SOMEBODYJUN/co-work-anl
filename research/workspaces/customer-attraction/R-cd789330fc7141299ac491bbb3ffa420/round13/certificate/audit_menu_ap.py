"""Original-unit-customer replay of the new menu-AP row contract.

Checks full ordered-history IC, reconstructs every indexed reply from one
original strategy, and compares the compressed coefficients with direct
pairwise AP payments. This finite replay does not prove AP or HALF(5).
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import sys,json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists())
sys.path[:0]=[str(HERE),str(ROOT)]
from customer_attraction import Instance,ExactSPESolver
import menu_ap_pricing as mp

def check(sets):
    themes=tuple(frozenset(s) for s in sets);N=set().union(*themes)
    sol=ExactSPESolver(Instance.from_topic_sets(themes,5));target=min(sol.worst_outcomes())
    sigma=sol.certificate(target,action_selector=lambda h,a:a[sum((i+1)*x for i,x in enumerate(h))%len(a)]).actions
    def finish(h):
        while len(h)<5:h=h+(sigma[h],)
        return h
    def utility(z,i):return sum((F(1,sum(x in themes[t] for t in z)) for x in themes[z[i]]),F(0))
    ic=0
    for d in range(5):
        for h in product(range(len(themes)),repeat=d):
            u=utility(finish(h),d)
            for t in range(len(themes)):assert u>=utility(finish(h+(t,)),d);ic+=1
    actual=finish(());A,B,C,D,E=actual;second=finish((A,E));third=finish((A,B,E));paths=dict(zip(('actual','second','third'),(actual,second,third)))
    labels=dict(zip(mp.LABELS,(*actual,*second[2:],*third[3:])))
    opt=max(combinations_with_replacement(range(len(themes)),5),key=lambda ts:len(set().union(*(themes[t] for t in ts))))
    replies={'AB':[finish((A,B,t)) for t in opt],'AE':[finish((A,E,t)) for t in opt],'Sbranch':[finish((A,t)) for t in opt]}
    menus={g:{'opt':opt,**{m:tuple(z[j] for z in replies[g]) for m,j in zip(mp.MENUS[g],(3,4) if g!='Sbranch' else (2,3,4))}} for g in replies}
    specs=mp.menu_specs();sums={n:F(0) for n,*_ in specs};atoms=[]
    for x in N:
        def bit(t):return int(x in themes[t])
        atom={'bits':''.join(str(bit(labels[t])) for t in mp.LABELS)}
        for g,field in mp.FIELDS.items():
            ty=mp.TYPES[4 if g=='Sbranch' else 3];hist=[0]*len(ty)
            for i,t in enumerate(opt):
                state=(bit(t),)+tuple(bit(menus[g][m][i]) for m in mp.MENUS[g]);hist[ty.index(state)]+=1
            atom[field]=hist
        bits=tuple(map(int,atom['bits']));d=sum(atom['AB_hist'][4:])
        counts={g:{'opt':d,**{m:sum(n*t[j] for n,t in zip(atom[field],mp.TYPES[4 if g=='Sbranch' else 3])) for j,m in enumerate(mp.MENUS[g],1)}} for g,field in mp.FIELDS.items()}
        for name,g,node,c,e in specs:
            p,k,u=mp.source(bits,node);cc=counts[g][c] if c in counts[g] else bits[mp.LABELS.index(c)];dd=counts[g][e] if e in counts[g] else bits[mp.LABELS.index(e)]
            sums[name]+=mp.ap_value(u,p,k,cc,dd,5 if c in counts[g] else 1,5 if e in counts[g] else 1)
    # Independent action-pair expansion, without histogram count products.
    direct={};minimum=None;pairs=0
    for name,g,(pn,i),c,e in specs:
        z=paths[pn];h=z[:i];k=5-i;u=utility(z,i)
        cs=menus[g][c] if c in menus[g] else (labels[c],);ds=menus[g][e] if e in menus[g] else (labels[e],)
        value=F(0)
        for ct,dt in product(cs,ds):
            Cset,Dset=themes[ct],themes[dt]
            s=F(0);f=F(0)
            for x in Cset:
                b=sum(x in themes[t] for t in h);s+=F(1,b+k)
            for x in Cset&Dset:
                b=sum(x in themes[t] for t in h);f+=F(1,b+k)
            for x in Dset-Cset:
                b=sum(x in themes[t] for t in h);f+=F(1,b+1)
            gap=mp.aa(k)*u-(mp.aa(k)-2)*s-2*f
            assert gap>=0,(name,ct,dt,gap)
            value+=gap;pairs+=1
        assert value==sums[name],(name,value,sums[name]);direct[name]=value;minimum=value if minimum is None else min(minimum,value)
    return {'themes':[sorted(t) for t in themes],'actual':actual,'full_IC':ic,'new_menu_rows':len(specs),'expanded_legal_AP_pairs':pairs,'minimum_new_slack':str(minimum)}

if __name__=='__main__':
    cases=[check(ts) for ts in [[set()],[set(),{0},{0,1},{1,2}],[set(range(5)),{5},{6},{7},{8}],[{0,1},{1,2},{0,2,3},{3,4},{0,2,4}]]]
    report={'status':'passed','scope':__doc__,'code_sha256':hashlib.sha256((HERE/'menu_ap_pricing.py').read_bytes()).hexdigest(),'cases':cases,'total_full_IC':sum(c['full_IC'] for c in cases),'total_expanded_AP_pairs':sum(c['expanded_legal_AP_pairs'] for c in cases)}
    (HERE/'audit_menu_ap.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
