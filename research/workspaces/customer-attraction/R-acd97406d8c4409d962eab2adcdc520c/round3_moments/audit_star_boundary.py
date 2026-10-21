"""Independent standard-library Fraction audit of the star pseudo-moment family.

The signed customer table below is an arithmetic device, not a legal instance.
All universal assertions have a symbolic proof in local_positive_boundary.md.
"""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path


def submasks(s):
    e=s
    while True:
        yield e
        if not e: break
        e=(e-1)&s


def moment(s, m, a, v):
    A=1<<m
    if s==A: return F(1)
    if s.bit_count()==1: return a
    if s.bit_count()==2 and s&A: return v
    return F(0)


def local_audit(m,a,v):
    p=m+1; count=0; zero=0
    for positive in range(1,1<<p):
        for negative in range(1<<p):
            if positive&negative or (positive|negative).bit_count()>m: continue
            value=sum(((-1)**e.bit_count())*moment(positive|e,m,a,v) for e in submasks(negative))
            assert value>=0,(m,positive,negative,value)
            count+=1;zero+=value==0
    return {'rows':count,'zero_rows':zero}


def signed_types(m,a,v):
    A=1<<m
    return {A:1-m*v, **{1<<i:a-v for i in range(m)},
            **{A|(1<<i):v for i in range(m)}}


def share(q,b,types):
    ans=F(0)
    for typ,mass in types.items():
        if not typ>>b&1: continue
        load=sum(x for j,x in enumerate(q) if typ>>j&1)
        assert load>0
        ans+=mass/load
    return ans


def full_spe_audit(m,a,v):
    types=signed_types(m,a,v); p=m+1; A=m
    histograms=0; comparisons=0; strict_offpath=0; offpath=0
    minimum=None
    for k in range(m):
        for h in combinations_with_replacement(range(p),k):
            pref=[h.count(j) for j in range(p)]
            q=pref[:];q[A]+=m-k
            current=share(q,A,types)
            r=q[A]
            formula=F(1,r)*(1-v*sum(F(x,r+x) for x in pref[:m]))
            assert current==formula
            for j in range(m):
                alt=q[:];alt[A]-=1;alt[j]+=1
                deviation=share(alt,j,types)
                n=pref[j]
                closed=(a-v)/(n+1)+v/(r+n) if r>1 else a/(n+1)
                assert deviation==closed
                slack=current-deviation
                assert slack>=0,(m,h,j,slack)
                comparisons+=1
                minimum=slack if minimum is None else min(minimum,slack)
                if any(pref[:m]):
                    offpath+=1;strict_offpath+=slack>0
            histograms+=1
    return {'histograms':histograms,'nonself_comparisons':comparisons,
            'minimum_slack':str(minimum),'offpath_comparisons':offpath,
            'strict_offpath_comparisons':strict_offpath}


def positivity_and_identity(m):
    """Truth tables also permit coinciding labels, since they are polynomial identities."""
    count=0
    for A in (0,1):
        for z in product((0,1),repeat=m):
            r=sum(z);o=int(r>0);E=r-o
            R=F(A)-F(m-1,m)*A*r+E
            terms=[]
            for i in range(m):
                others=z[:i]+z[i+1:]
                nohit=int(not any(others));ei=sum(others)-int(any(others))
                terms.append(A*nohit+(1-A)*ei+z[i]*(1-nohit))
            assert all(x>=0 for x in terms)
            assert R==F(sum(terms),m)
            assert R-F(A,m)>=0
            Q=A-A*r+sum(z[i]*z[j] for i in range(m) for j in range(i+1,m))
            assert Q>=0
            count+=1
    return count


def main():
    results=[]
    for m in range(2,9):
        if m==2:a,v=F(3,4),F(1,2)
        elif m==3:a,v=F(3,5),F(2,5)
        else:a,v=F(2,m),F(1,m-1)
        row={'m':m,'leaf_size':str(a),'overlap':str(v),
             'root_W':'1','OPT_m':str(max(m*a,1+(m-1)*(a-v))),
             'signed_center_private':str(1-m*v),
             'boolean_separator_value':str(1-m*v)}
        row['local']=local_audit(m,a,v)
        row['full_SPE']=full_spe_audit(m,a,v)
        row['boolean_identity_assignments']=positivity_and_identity(m)
        if m>=5:
            assert row['full_SPE']['strict_offpath_comparisons']==row['full_SPE']['offpath_comparisons']
        results.append(row)
    report={'status':'finite exact implementation audit; universal proof is in companion note',
            'not_an_original_model_counterexample':True,'rows':results}
    output=Path(__file__).with_name('star_boundary_exact_audit.json')
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__': main()
