"""Static test of whether the open P6<=W+C candidate would imply half.

This script imposes every six-slot harmonic potential comparison using the six
actual topics and six comparison topics. It is not a SPE search. Optimal topic
labels are symmetrized, preserving all ordered actual membership information.
"""
from itertools import combinations
from math import comb
from fractions import Fraction
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

M = 6
H60 = [0,60,90,110,125,137,147]

def comps(n,k):
    if k==1:
        yield (n,)
    else:
        for q in range(n+1):
            for tail in comps(n-q,k-1): yield (q,)+tail

def partitions(n,slots=6,cap=None):
    if slots==0:
        if n==0: yield ()
        return
    if cap is None: cap=n
    for q in range(min(n,cap),-1,-1):
        for tail in partitions(n-q,slots-1,q): yield (q,)+tail

def copy60(a):
    p=0; ans=Fraction(0)
    for i in range(M):
        if a>>i&1:
            ans+=Fraction(1,p+1)-Fraction(1,p+M-i)
            p+=1
    assert (ans*60).denominator==1
    return int(ans*60)

def build(extra=False,suffix=False):
    cols=[(a,k) for a in range(64) for k in range(7) if a or k]
    subsets={k:list(combinations(range(6),k)) for k in range(7)}
    W=np.array([bool(a) for a,k in cols],dtype=int)
    O=np.array([bool(k) for a,k in cols],dtype=int)
    B=np.array([60*(60*bool(a)+copy60(a)) for a,k in cols],dtype=int)
    rows=[]; names=[]
    for d in range(7):
        for ac in comps(d,6):
            for oc in partitions(6-d):
                pot=[]
                for a,k in cols:
                    z=sum(ac[i] for i in range(6) if a>>i&1)
                    v=sum(H60[z+sum(oc[j] for j in sub)] for sub in subsets[k])
                    assert (60*v)%comb(6,k)==0
                    pot.append(60*v//comb(6,k))
                rows.append(np.array(pot,dtype=int)-B)
                names.append((ac,oc))
    if suffix:
        for i in range(1,4):
            r=6-i
            for d in range(r+1):
                for ac in comps(d,6):
                    for oc in partitions(r-d):
                        row=[]
                        for a,k in cols:
                            c=a.bit_count(); p=(a&((1<<i)-1)).bit_count()
                            own=Fraction((a>>i).bit_count(),c) if c else Fraction(0)
                            for l in range(i,6):
                                if a>>l&1:
                                    z=(a&((1<<l)-1)).bit_count()
                                    own+=Fraction(1,z+1)-Fraction(1,z+6-l)
                            z=sum(ac[j] for j in range(6) if a>>j&1)
                            pot=sum(H60[p+z+sum(oc[j] for j in sub)]-H60[p] for sub in subsets[k])
                            value=Fraction(pot,60*comb(6,k))-own
                            assert (value*3600).denominator==1
                            row.append(int(value*3600))
                        rows.append(row); names.append(('open_suffix_potential',i,ac,oc))
    if extra:
        # Existing true-path guarantees, valid without assuming the open root
        # potential candidate. Rows are query value minus actual budget <=0.
        for i in range(6):
            for query in range(7):
                row=[]
                for a,k in cols:
                    c=a.bit_count(); p=(a&((1<<i)-1)).bit_count()
                    own=Fraction(bool(a>>i&1),c) if c else Fraction(0)
                    target=Fraction(k,6) if query==6 else Fraction(bool(a>>query&1))
                    value=target/(p+6-i)-own
                    assert (value*3600).denominator==1
                    row.append(int(value*3600))
                rows.append(row); names.append(('safe',i,query))
        for d in range(3):
            for ac in comps(d,6):
                for oc in partitions(2-d):
                    row=[]
                    for a,k in cols:
                        c=a.bit_count(); p=(a&15).bit_count()
                        own=Fraction(bool(a&16)+bool(a&32),c) if c else Fraction(0)
                        own+=Fraction(bool(a&16),(p+1)*(p+2))
                        z=sum(ac[i] for i in range(6) if a>>i&1)
                        pot=sum(H60[p+z+sum(oc[j] for j in sub)]-H60[p] for sub in subsets[k])
                        value=Fraction(pot,60*comb(6,k))-own
                        assert (value*3600).denominator==1
                        row.append(int(value*3600))
                    rows.append(row); names.append(('strong_pair',ac,oc))
    return cols,W,O,B,np.array(rows,dtype=int),names

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--extra',action='store_true');parser.add_argument('--suffix',action='store_true');parser.add_argument('--exact',action='store_true');parser.add_argument('--verify',type=Path);args=parser.parse_args()
    if args.verify:
        record=json.loads(args.verify.read_text())
        cols,W,O,B,A,names=build(record['extra_valid_path_rows'],record['open_suffix_potential_rows'])
        x=[Fraction(0)]*len(cols)
        for item in record['exact']['support']:
            x[cols.index((item['a'],item['k']))]=Fraction(item['mass'])
        support=[i for i,v in enumerate(x) if v]
        assert all(v>=0 for v in x)
        assert sum(int(W[i])*x[i] for i in support)==1
        exact_O=sum(int(O[i])*x[i] for i in support)
        assert exact_O==Fraction(record['exact']['O'])>2
        slacks=[-sum(int(row[i])*x[i] for i in support) for row in A]
        assert min(slacks)>=0
        assert all(cols[i][1]==1 for i in support)
        print(json.dumps({'status':'exact_static_point_verified_not_SPE','columns':len(cols),'rows':len(A),'support':len(support),'W':'1','O':str(exact_O),'minimum_scaled_slack':str(min(slacks))}),flush=True)
        raise SystemExit
    cols,W,O,B,A,names=build(args.extra,args.suffix)
    res=linprog(-O,A_ub=A/3600.,b_ub=np.zeros(len(A)),A_eq=[W],b_eq=[1],bounds=(0,None),method='highs')
    print({'columns':len(cols),'rows':len(A),'success':res.success,'max_O':-res.fun if res.success else None,'message':res.message},flush=True)
    if res.success:
        support=[{'a':a,'k':k,'mass':float(x)} for (a,k),x in zip(cols,res.x) if x>1e-9]
        output={'status':'static_relaxation_only_not_SPE','extra_valid_path_rows':args.extra,'open_suffix_potential_rows':args.suffix,'max_O':-res.fun,'support':support,'C':float((B@res.x)/3600-1),'active_constraints':[names[i] for i,v in enumerate(A@res.x) if abs(v)<1e-6]}
        if args.exact:
            support_indices=np.where(res.x>1e-9)[0]
            active_indices=np.where(np.abs(A@res.x)<1e-6)[0]
            system=[(W[support_indices],1)]+[(A[i,support_indices],0) for i in active_indices]
            basis=[]
            for raw,rhs in system:
                row=list(map(lambda x:Fraction(int(x)),raw))+[Fraction(rhs)]
                for pivot,old in basis:
                    if row[pivot]:
                        factor=row[pivot]
                        row=[x-factor*y for x,y in zip(row,old)]
                nz=[j for j,x in enumerate(row[:-1]) if x]
                if nz:
                    pivot=nz[0];factor=row[pivot]
                    row=[x/factor for x in row]
                    basis.append((pivot,row));basis.sort()
                else:
                    assert row[-1]==0
                if len(basis)==len(support_indices):break
            assert len(basis)==len(support_indices)
            sol=[Fraction(0)]*len(support_indices)
            for pivot,row in reversed(basis):
                sol[pivot]=row[-1]-sum(x*y for x,y in zip(row[pivot+1:-1],sol[pivot+1:]))
            assert all(x>=0 for x in sol)
            for row in A[:,support_indices]:
                assert sum(int(c)*x for c,x in zip(row,sol))<=0
            assert sum(int(c)*x for c,x in zip(W[support_indices],sol))==1
            exact_O=sum(int(c)*x for c,x in zip(O[support_indices],sol))
            output['exact']={'O':str(exact_O),'support':[{'a':cols[j][0],'k':cols[j][1],'mass':str(x)} for j,x in zip(support_indices,sol)],'checks':len(A),'min_slack':str(min(-sum(int(c)*x for c,x in zip(row,sol)) for row in A[:,support_indices]))}
            print({'exact_O':str(exact_O),'exact_support':len(sol)},flush=True)
        dest=Path(__file__).with_name(Path(__file__).stem+('_extra' if args.extra else '')+('_suffix' if args.suffix else '')+'.json');dest.write_text(json.dumps(output,indent=2))
        print(json.dumps(support),flush=True)
