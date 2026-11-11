"""Independent standard-library exact verifier, importing no construction code.

Reconstructs all homogeneous coefficients from literal ordered-history payoff
formulas, including the six zero-mass hist.  The recovered auxiliaries certify
only per-query envelopes.  No intersections or common D realization are inferred.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path
import gzip
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
POINT = WORK/'union_augmented_lp/augmented_lp_exact.json'
MATRIX = WORK/'union_augmented_lp/exact_matrix.json.gz'


class Linear(dict):
    def __add__(self,other):
        out=Linear(self)
        for j,v in other.items():
            out[j]=out.get(j,F())+v
            if not out[j]:del out[j]
        return out
    def __sub__(self,other):
        return self + other.scale(-1)
    def scale(self,q):
        q=F(q)
        return Linear({j:v*q for j,v in self.items() if v*q})


def basis(j):
    return Linear({j:F(1)})


def plus(seq):
    out=Linear()
    for r in seq:out=out+r
    return out


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fraction_share(n,d):
    return F(n,d) if n else F()


def canon(seq):
    distinct=[]
    answer=[]
    for k in seq:
        if k not in distinct:distinct.append(k)
        answer.append(str(distinct.index(k)))
    return ''.join(answer)


def main():
    start=time.perf_counter()
    lift=json.loads((HERE/'symbolic_lift.json').read_bytes())
    exact=json.loads((HERE/'exact_lift.json').read_bytes())
    point=json.loads(POINT.read_bytes())
    matrix=json.loads(gzip.decompress(MATRIX.read_bytes()))
    assert sha(POINT)==lift['point_sha256']==exact['point_sha256']=='b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'
    assert sha(MATRIX)==lift['matrix_sha256']=='99253e05bfe4c5705619777a5989ec9fab5c38dc7e56f934bbe8d9c071040ded'
    assert sha(HERE/'symbolic_lift.json')==exact['symbolic_lift_sha256']
    assert lift['old_descriptors']==matrix['columns']
    assert lift['row_constants']==0 and lift['nonnegative_new_columns']
    old=lift['fixed_old_columns'];assert old==15593
    assert all(c=={k:v for k,v in p.items() if k!='weight'}
               for c,p in zip(matrix['columns'],point['columns']))
    weights=[F(c['weight']) for c in point['columns']]
    new=[F(v) for v in exact['new_values']]
    values=weights+new
    assert len(new)==578 and all(v>=0 for v in values)
    hist={};own=defaultdict(dict);branch=defaultdict(list)
    for j,c in enumerate(matrix['columns'][:4849]):
        if c['kind']=='hist':
            h=j;hist[j]=c
        elif c['kind']=='joint-reply':
            f,s,u,v=c['group'];g=(f,s,tuple(u),tuple(v))
            own[h].setdefault(g,{})[tuple(c['state'])]=j
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            branch[c['hist_column']].append((j,tuple(c['hidden']),c['ell']))
    assert len(hist)==16
    xs={};ys={};zs={}
    for local,c in enumerate(lift['new_columns']):
        key=(c['hist_column'],tuple(c['word']))
        if c['kind']=='D-membership-marginal':xs[key]=old+local
        elif c['kind']=='virtual-H1-D-min-upper':zs[key]=old+local
        elif c['kind']=='virtual-R-D-min-upper':
            f,s,u,v=c['group'];ys[key[0],(f,s,tuple(u),tuple(v)),key[1]]=old+local
        else:raise AssertionError(c)
    assert (len(xs),len(ys),len(zs))==(38,502,38)

    rebuilt=defaultdict(Linear)
    def add(name,v):
        k=tuple(name);rebuilt[k]=rebuilt[k]+v
    def members(h,g,slot):
        return plus(basis(j).scale(st[slot] if slot<2 else st[0]*st[1]) for st,j in own[h][g].items())

    nodes=[(f,j,k) for f in (0,1) for j in range(6) for k in range(6) if f==1 or j!=k]
    triples=defaultdict(list)
    pairs=defaultdict(list)
    for i in range(6):
        for j in range(6):pairs[int(i==j)].append((i,j))
        for f,j,k in nodes:triples[f,canon((i,j,k))].append((i,f,j,k))
    assert len(nodes)==66 and len(triples)==8
    allperms=list(permutations(range(6)))
    orbit_permutation_checks=0
    for orb,items in triples.items():
        i,f,j,k=items[0]
        derived={(perm[i],f,perm[j],perm[k]) for perm in allperms}
        assert derived==set(items)
        orbit_permutation_checks+=len(allperms)
    assert lift['triple_orbits']==[
        {'orbit':list(o),'size':len(ms),'members':[[i,f,j,k] for i,f,j,k in ms]}
        for o,ms in sorted(triples.items())]
    assert lift['pair_orbits']==[
        {'same':s,'size':len(ms),'members':[list(pair) for pair in ms]}
        for s,ms in sorted(pairs.items())]

    old_margin_checks=0
    hist_summary=[]
    for h,c in hist.items():
        H=basis(h);mass=weights[h]
        bits=tuple(int(v) for v in c['actual_bits'])
        p3=sum(bits[:3]);P=sum(bits[:4]);ell=sum(bits[:5]);total=sum(bits)
        words=[w for w,n in zip(product((0,1),repeat=3),c['hist']) for _ in range(n)]
        assert len(words)==6 and len(branch[h])==8
        assert sum(weights[j] for j,st,yy in branch[h])==mass
        assert {(st,yy) for j,st,yy in branch[h]}==set(product(product((0,1),repeat=2),(0,6)))
        old_margin_checks+=8
        for g,states in own[h].items():
            assert set(states)=={(0,1),(1,0),(1,1)}
            assert mass-sum(weights[j] for j in states.values())>=0
            old_margin_checks+=4
        b4first=plus(basis(j).scale(st[0]) for j,st,yy in branch[h])
        b4second=plus(basis(j).scale(st[1]) for j,st,yy in branch[h])
        h1value=sum(q*values[j] for j,q in b4first.items())
        Fpay=plus(basis(j).scale(fraction_share(st[1],p3+bits[5]+sum(st))) for j,st,yy in branch[h])
        H1pay=plus(basis(j).scale(fraction_share(st[0],p3+bits[5]+sum(st))) for j,st,yy in branch[h])
        X=[basis(xs[h,w]) for w in words]
        H1min=[basis(zs[h,w]) for w in words]
        s=p3+bits[5]+1
        for w in set(words):
            x=xs[h,w];z=zs[h,w]
            assert 0<=values[x]<=mass and values[z]==min(values[x],h1value)
            add(('D-at-most-hist',h,*w),H-basis(x))
            add(('H1-D-min-at-most-D',z),basis(x)-basis(z))
            add(('H1-D-min-at-most-H1',z),b4first-basis(z))
        add(('D-source',),H.scale(fraction_share(bits[4],total)))
        for k in range(1,7):
            add(('A-to-D-safe' if k<6 else 'A6-to-D',k),H.scale(fraction_share(bits[k-1],total)))
        add(('F-to-D-upper',),Fpay)
        add(('H1-safe-to-D',),H1pay)
        for i,(t,b,cc) in enumerate(words):
            # Direct expectation of t/(P+t+d), not the builder's expansion.
            dsource=(H-X[i]).scale(F(t,P+1))+X[i].scale(F(t,P+2))
            add(('D-source',),dsource.scale(F(-1,6)))
            add(('capacity-D',),X[i].scale(F(-1,6)))
            for k in range(1,7):
                add(('A-to-D-safe' if k<6 else 'A6-to-D',k),X[i].scale(F(-1,6*(sum(bits[:k-1])+7-k))))
            den=P+t+1
            for k,ak in enumerate(bits,1):add(('D-to-A',k),(X[i]-H.scale(ak)).scale(F(1,6*den)))
            for k,M in enumerate((b4first,b4second),1):add(('D-to-H',k),(X[i]-M).scale(F(1,6*den)))
            add(('F-to-D-upper',),(X[i].scale(F(-1,s))+H1min[i].scale(F(1,s*(s+1)))).scale(F(1,6)))
            add(('H1-safe-to-D',),X[i].scale(F(-1,6*(p3+bits[5]+2))))
        for same,items in pairs.items():
            scale=F(1,len(items))
            for i,j in items:
                d=P+words[i][0]+1
                for slot,kind in enumerate(('T','B','C')):
                    add(('D-to-'+kind,same),(X[i]-H.scale(words[j][slot])).scale(scale/d))
                add(('D-to-D',same),(X[i]-X[j]).scale(scale/d))
                t,b,cc=words[j]
                add(('C-to-D',same),(H.scale(cc)-X[i]).scale(scale/(p3+t+b+1)))
                bpay=H.scale(fraction_share(b,p3+t+b+cc))
                add(('B-safe-to-D',same),(bpay-X[i].scale(F(1,p3+t+2))).scale(scale))
        for orb,items in triples.items():
            scale=F(1,len(items))
            for i,f,j,k in items:
                g=(f,int(j==k),words[j],words[k])
                R,Z,T=[members(h,g,slot) for slot in range(3)]
                den=P+words[i][0]+1
                add(('D-to-R',*orb),(X[i]-R).scale(scale/den))
                add(('D-to-Z',*orb),(X[i]-Z).scale(scale/den))
                rden=p3+words[j][0]+words[k][1+f]+1
                add(('R-to-D',*orb),(R-X[i]).scale(scale/rden))
                Y=basis(ys[h,g,words[i]])
                zupper=(Z-X[i]).scale(F(1,P+1))+(Y-T).scale(F(1,(P+1)*(P+2)))
                add(('Z-to-D-upper',*orb),zupper.scale(scale))
        hist_summary.append({'hist_column':h,'mass':str(mass),'zero_mass':not mass,
                             'D':[{'word':list(w),'value':str(values[xs[h,w]]),'fraction_of_hist':None if not mass else str(values[xs[h,w]]/mass)}
                                  for w in sorted(set(words))]})
    add(('capacity-D',),basis(0))
    for (h,g,w),y in ys.items():
        R=members(h,g,0);rvalue=sum(v*values[j] for j,v in R.items());x=xs[h,w]
        assert values[y]==min(values[x],rvalue)
        add(('R-D-min-at-most-R',y),R-basis(y))
        add(('R-D-min-at-most-D',y),basis(x)-basis(y))

    assert len(rebuilt)==len(lift['rows'])==1180
    rows=[]
    for r,desc in enumerate(lift['rows']):
        name=tuple(desc['name'])
        saved={j:F(v) for j,v in desc['row']}
        assert saved==rebuilt[name],('coefficient mismatch',name)
        assert all(j<4849 or j>=old for j in saved)
        slack=sum(v*values[j] for j,v in rebuilt[name].items())
        assert slack>=0,(name,slack)
        assert exact['rows'][r]['name']==desc['name'] and F(exact['rows'][r]['slack'])==slack
        rows.append({'index':r,'name':list(name),'slack':str(slack),'approx':float(slack)})

    # Scalar truth tables certify the identities and SAFE denominator directions.
    checks=Counter()
    for P in range(5):
        for t,d,q,r,z in product((0,1),repeat=5):
            assert fraction_share(t,P+t+d)==F(t,P+1)-F(t*d,(P+1)*(P+2));checks['D-source']+=1
            actual=fraction_share(d,P+t+d)-fraction_share(q,P+t+q)
            assert actual==F(d-q,P+t+1);checks['D-last']+=1
            zactual=fraction_share(z,P+r+z)-fraction_share(d,P+r+d)
            zexpand=F(z-d,P+1)+F(r*d-r*z,(P+1)*(P+2))
            assert zactual==zexpand;checks['Z-to-D']+=1
    for k in range(1,7):
        for p in range(k):
            for future in range(7-k):
                for d in (0,1):
                    assert fraction_share(d,p+d+future)>=F(d,p+7-k)
                    checks['D-early-and-A6']+=1
    for p in range(4):
        for t,b,r,d in product((0,1),repeat=4):
            actual=fraction_share(r,p+t+b+r)-fraction_share(d,p+t+b+d)
            assert actual==F(r-d,p+t+b+1);checks['R-to-D']+=1
        for a6,h1,h2,d in product((0,1),repeat=4):
            s=p+a6+1
            assert fraction_share(d,p+a6+h1+d)==F(d,s)-F(d*h1,s*(s+1))
            checks['F-to-D-expansion']+=1
    # Every orbit is obtained by the same S6 action on all three indices.
    # A row's uniform average sums to one globally, including F->D's 1/6.
    assert 6*F(1,6)==1
    assert all(len(ms)*F(1,len(ms))==1 for ms in triples.values())
    assert all(len(ms)*F(1,len(ms))==1 for ms in pairs.values())

    # All inherited old coordinates stay exactly fixed; their certified identity
    # is bound by both input SHA and a fresh complete original-row evaluation.
    old_slacks=[]
    oldstart=time.perf_counter()
    for r,coeff in enumerate(matrix['rows']):
        slack=sum(F(v)*weights[j] for j,v in coeff)
        assert slack>=0,('old row',r,slack)
        old_slacks.append(str(slack))
    oldtime=time.perf_counter()-oldstart
    assert len(old_slacks)==19662
    obj=sum(F(c)*w for c,w in zip(matrix['objective'],weights))
    norm=sum(F(c)*w for c,w in zip(matrix['normalization'],weights))
    assert obj==F(point['W']) and norm==F(1)
    report={
        'status':'PASS',
        'scope':'Exact necessary single-D-marginal/min lift only. No shared D/R/Z/B4 customer measure and no SPE claimed.',
        'point_sha256':sha(POINT),'matrix_sha256':sha(MATRIX),
        'symbolic_lift_sha256':sha(HERE/'symbolic_lift.json'),'exact_lift_sha256':sha(HERE/'exact_lift.json'),
        'verifier_sha256':sha(Path(__file__)),
        'all_15593_original_coordinates_fixed':True,'all_16_hist_retained':True,
        'zero_mass_hist_columns':[h for h in hist if weights[h]==0],
        'all_1180_symbolic_rows_independently_reconstructed':True,
        'coefficient_comparison_covers_zero_mass_hist':True,
        'all_old_auxiliary_coefficients_zero':True,
        'all_new_columns_nonnegative':True,'all_min_auxiliaries_canonical':True,
        'new_row_count':len(rows),'new_zero_rows':sum(F(r['slack'])==0 for r in rows),
        'new_positive_rows':sum(F(r['slack'])>0 for r in rows),
        'new_minimum_slack':str(min(F(r['slack']) for r in rows)),
        'literal_payoff_truth_table_counts':dict(checks),
        'synchronous_S6_permutation_checks':orbit_permutation_checks,
        'old_own_and_B4_margin_state_checks':old_margin_checks,
        'old_row_count':len(old_slacks),'old_row_zero_count':sum(F(v)==0 for v in old_slacks),
        'old_row_minimum_slack':str(min(F(v) for v in old_slacks)),
        'old_row_evaluation_seconds':oldtime,'old_W':str(obj),'normalization':str(norm),
        'hist_and_D_marginals':hist_summary,'new_rows':rows,
        'old_row_slacks':old_slacks,
        'elapsed_seconds':time.perf_counter()-start,
    }
    (HERE/'independent_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('hist_and_D_marginals','new_rows','old_row_slacks')},ensure_ascii=False))


if __name__=='__main__':
    main()
