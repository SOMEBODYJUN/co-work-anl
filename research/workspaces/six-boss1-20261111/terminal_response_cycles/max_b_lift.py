"""One common maximum-B label, with all 17 single and 490 pair orbits.

The mathematical owner is the existing true-last-reply-common-potential-cap
lemma.  This is its new-point application, not a new game-theoretic theorem.
Build and audit all homogeneous rows before the single phase-I call.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import gzip
import json
import sys

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
POINT = WORK/'full624_augmented_lp/recovery/augmented_lp_exact.json'
PAIR = WORK/'actual_pair_20910/symbolic_rows.json.gz'
POINT_SHA = 'cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932'
PAIR_SHA = '423bf2c92d9c85c7e6086a193365ed80cd2427d7f7ee406972e1faf1813ea62f'
DESC_SHA = 'afce2dcdff01e9393c04e317ee6bd52f5c0b378daedd92816647412243362460'
OLD = 4849
WORDS = tuple(product((0,1),repeat=3))


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def serial(v):
    if isinstance(v,F): return str(v)
    if isinstance(v,dict): return {str(k):serial(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)): return [serial(x) for x in v]
    return v


def save(name,data):
    (HERE/name).write_text(json.dumps(serial(data),ensure_ascii=False,indent=2)+'\n')


def add(row,j,v):
    if v:
        row[j] = row.get(j,F())+v
        if not row[j]: del row[j]


def plus(row,other,scale=F(1)):
    for j,v in other.items(): add(row,j,scale*v)


def sparse(row):
    return [[j,str(v)] for j,v in sorted(row.items()) if v]


def decode(xs):
    return {int(j):F(v) for j,v in xs}


def evaluate(row,values):
    return sum((v*values[j] for j,v in row.items()),F())


def group(raw):
    return raw[0],raw[1],tuple(raw[2]),tuple(raw[3])


def parse():
    assert digest(POINT)==POINT_SHA and digest(PAIR)==PAIR_SHA
    point=json.loads(POINT.read_bytes())
    desc=[{k:v for k,v in c.items() if k!='weight'} for c in point['columns'][:OLD]]
    assert sha256(json.dumps(desc,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==DESC_SHA
    values=[F(c['weight']) for c in point['columns'][:OLD]]
    hist={}; own=defaultdict(dict); b4=defaultdict(dict)
    for j,c in enumerate(desc):
        if c['kind']=='hist':
            h=j;hist[h]=c
        elif c['kind']=='joint-reply':
            own[h].setdefault(group(c['group']),{})[tuple(c['state'])]=j
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            assert c['ell'] in (0,6)
            b4[c['hist_column']][tuple(c['hidden'])+(c['ell']//6,)]=j
    assert len(hist)==16 and sum(map(len,own.values()))==194
    for h in hist:
        assert set(b4[h])==set(product((0,1),repeat=3))
        assert sum(values[j] for j in b4[h].values())==values[h]
        for g,d in own[h].items():
            assert set(d)=={(0,1),(1,0),(1,1)}
            assert sum(values[j] for j in d.values())<=values[h]
    return point,desc,values,hist,own,b4


def build():
    point,desc,values,hist,own,b4=parse()
    nodes=[(f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j]
    actions=[('A',k) for k in range(6)]
    actions += [(k,i) for k in ('T','B','C') for i in range(6)]
    actions += [(k,)+e for k in ('R','Z') for e in nodes]
    actions += [('H',i) for i in range(2)]
    assert len(actions)==len(set(actions))==158
    orbit=defaultdict(list)
    for q in actions:
        if q[0] in ('A','H'): key=q
        elif q[0] in ('T','B','C'): key=(q[0],)
        else: key=(q[0],q[1],int(q[2]==q[3]))
        orbit[key].append(q)
    assert len(orbit)==17 and sum(map(len,orbit.values()))==158
    perms=tuple(permutations(range(6)))
    def move(q,pi):
        if q[0] in ('A','H'): return q
        if q[0] in ('T','B','C'): return q[0],pi[q[1]]
        return q[0],q[1],pi[q[2]],pi[q[3]]
    orbit_checks=[]
    for key,members in orbit.items():
        count=Counter(move(members[0],pi) for pi in perms)
        assert set(count)==set(members) and set(count.values())=={720//len(members)}
        orbit_checks.append({'orbit':key,'size':len(members),'representative':members[0],
                             'member_frequency':720//len(members),'members':members})

    cols=[]; x={}; y={}; masses={}; tokens={}; frequencies={}
    for h in hist:
        x[h]=OLD+len(cols)
        cols.append({'kind':'common-X-mass','hist_column':h})
    for h,c in hist.items():
        for g,d in own[h].items():
            for slot,kind in enumerate(('R','Z')):
                token=(kind,g)
                marginal={j:F(1) for s,j in d.items() if s[slot]}
                y[h,token]=OLD+len(cols);masses[h,token]=marginal
                cols.append({'kind':'X-query-overlap-upper','hist_column':h,
                             'query_token':token,'query_marginal':sparse(marginal)})
        for k in range(2):
            token=('H',k)
            marginal={j:F(1) for s,j in b4[h].items() if s[k]}
            y[h,token]=OLD+len(cols);masses[h,token]=marginal
            cols.append({'kind':'X-query-overlap-upper','hist_column':h,
                         'query_token':token,'query_marginal':sparse(marginal)})
        words=tuple(w for w,n in zip(WORDS,c['hist']) for _ in range(n))
        assert len(words)==6
        bits=tuple(map(int,c['actual_bits']))
        for key,members in orbit.items():
            ts=[]
            for q in members:
                if q[0]=='A': t=('bit',bits[q[1]])
                elif q[0] in ('T','B','C'): t=('bit',words[q[1]][('T','B','C').index(q[0])])
                elif q[0]=='H': t=q
                else:
                    kind,f,i,j=q
                    t=(kind,(f,int(i==j),words[i],words[j]))
                ts.append(t)
            tokens[h,key]=ts
            frequencies[h,key]=Counter(ts)
            full=Counter()
            rep=members[0]
            for pi in perms:
                q=move(rep,pi)
                if q[0]=='A': t=('bit',bits[q[1]])
                elif q[0] in ('T','B','C'):t=('bit',words[q[1]][('T','B','C').index(q[0])])
                elif q[0]=='H':t=q
                else:
                    kind,f,i,j=q;t=(kind,(f,int(i==j),words[i],words[j]))
                full[t]+=1
            assert full==Counter({t:n*(720//len(members)) for t,n in frequencies[h,key].items()})
    assert len(x)==16 and len(y)==420 and len(cols)==436

    income=[{} for _ in range(6)];tax={};BX={}
    for h,c in hist.items():
        bits=tuple(map(int,c['actual_bits']));p=sum(bits[:4]);total=sum(bits)
        for k in range(6):
            if bits[k]:income[k][h]=F(1,total)
        if bits[4]:tax[h]=F(1,(p+1)*(p+2))
        BX[x[h]]=F(1,p+1)
    wallet={};plus(wallet,income[4]);plus(wallet,income[5]);plus(wallet,tax)
    oldwallet=json.loads((WORK/'actual_pair_20910/hist_wallets.json').read_bytes())
    assert wallet==decode(oldwallet['wallet_sparse_original4849'])
    assert [evaluate(income[k],values) for k in (4,5)]==[F(oldwallet[k]) for k in ('u5','u6')]
    assert evaluate(tax,values)==F(oldwallet['self_tax'])

    rows=[]
    def row(name,r): rows.append({'name':list(name),'row':sparse(r)})
    for h in hist:row(('X-at-most-hist',h),{h:F(1),x[h]:F(-1)})
    for (h,t),j in y.items():
        row(('overlap-at-most-X',j),{x[h]:F(1),j:F(-1)})
        r=dict(masses[h,t]);r[j]=F(-1)
        row(('overlap-at-most-query',j),r)
    for key,members in orbit.items():
        maxrow=dict(BX);caprow=dict(income[4]);Bq={}
        for h,c in hist.items():
            p=sum(map(int,c['actual_bits'][:4]));d=(p+1)*(p+2)
            for t,n in frequencies[h,key].items():
                scale=F(n,len(members))
                if t[0]=='bit':
                    if t[1]:
                        add(Bq,h,scale/F(p+1));add(caprow,x[h],scale/F(d))
                else:
                    plus(Bq,masses[h,t],scale/F(p+1))
                    add(caprow,y[h,t],scale/F(d))
        plus(maxrow,Bq,F(-1));plus(caprow,Bq,F(-1))
        row(('maximum-B',)+key,maxrow);row(('X-caps-query',)+key,caprow)
    for k in range(6):
        r=dict(income[k])
        for h,c in hist.items():
            prefix=sum(map(int,c['actual_bits'][:k]));add(r,x[h],-F(1,prefix+6-k))
        row(('actual-safe-X',k+1),r)
    r={0:F(1)}
    for j in x.values():r[j]=F(-1)
    row(('capacity-X',),r)
    assert len(rows)==897
    pairdata=json.loads(gzip.decompress(PAIR.read_bytes()))
    assert pairdata['point_sha256']==POINT_SHA and len(pairdata['rows'])==490
    for src in pairdata['rows']:
        r=decode(src['sparse_original4849_row'])
        assert evaluate(r,values)==F(src['exact_slack'])
        plus(r,income[5],F(-1));plus(r,tax,F(-1));plus(r,BX)
        row(('common-B-pair',src['orbit_id']),r)
    assert len(rows)==1387

    # Universal literal scalar identities and upper-envelope directions.
    truth=0
    for p in range(5):
        for q,xx,r in product((0,1),repeat=3):
            literal=F(q,p+q+xx) if q else F()
            assert literal==F(q,p+1)-F(q*xx,(p+1)*(p+2))
            assert q*xx<=q and q*xx<=xx
            assert (F(q,p+1)-F(q*r,(p+1)*(p+2)))-(F(r,p+1)-F(q*r,(p+1)*(p+2)))==F(q-r,p+1)
            truth+=1
    payload={'scope':'One common unindexed maximum-B label; 17 single and all 490 frozen PAIR upper orbits. Necessary relaxation only.',
             'point_sha256':POINT_SHA,'pair_rows_sha256':PAIR_SHA,'descriptor_sha256':DESC_SHA,
             'original_columns':OLD,'point_columns':len(point['columns']),'new_columns':cols,
             'new_column_count':436,'row_count':1387,'rows':rows,'row_constants':0,
             'all_new_columns_nonnegative':True,'all_16_histograms_retained':True,
             'zero_histograms':[h for h in hist if not values[h]],
             'new_indices_in_full_extension':{'compressed_start':OLD,'full_start':len(point['columns'])},
             'incomes':[sparse(r) for r in income],'self_tax':sparse(tax),'B_X':sparse(BX),
             'family_counts':dict(Counter(r['name'][0] for r in rows))}
    save('max_b_symbolic_lift.json',payload)
    save('max_b_preflight.json',{'point_sha256':POINT_SHA,'pair_rows_sha256':PAIR_SHA,
             'all_17_orbits':orbit_checks,'all_720_permutations_checked':True,
             'hist_orbit_frequency_checks':16*17*720,'literal_scalar_cases':truth,
             'incomes':[evaluate(r,values) for r in income],'K':values[0],
             'pair_wallet_exactly_replaced':True,'old_auxiliary_coefficients_all_zero':True,
             'row_count':1387,'new_column_count':436,'symbolic_lift_sha256':digest(HERE/'max_b_symbolic_lift.json')})
    print(json.dumps({'status':'symbolic-built-and-preflight-passed','rows':len(rows),'new_columns':len(cols),
                      'hist':len(hist),'single_orbits':len(orbit),'pair_orbits':490},ensure_ascii=False))


def phase_one():
    # This guard prevents an accidental second optimization in this frozen task.
    assert not (HERE/'max_b_phase_I.json').exists(), 'The single phase-I call already exists.'
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    data=json.loads((HERE/'max_b_symbolic_lift.json').read_bytes())
    pre=json.loads((HERE/'max_b_preflight.json').read_bytes())
    assert pre['symbolic_lift_sha256']==digest(HERE/'max_b_symbolic_lift.json')
    point,desc,values,hist,own,b4=parse()
    n=data['new_column_count']; ii=[];jj=[];vv=[];rhs=[]
    for i,record in enumerate(data['rows']):
        constant=F()
        for j,v in decode(record['row']).items():
            if j<OLD:constant+=v*values[j]
            else:ii.append(i);jj.append(j-OLD);vv.append(-float(v))
        ii.append(i);jj.append(n);vv.append(-1.0);rhs.append(float(constant))
    A=coo_matrix((vv,(ii,jj)),shape=(len(rhs),n+1)).tocsr()
    cost=np.zeros(n+1);cost[n]=1
    result=linprog(cost,A_ub=A,b_ub=np.array(rhs),bounds=(0,None),method='highs-ds',
                   options={'time_limit':40,'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9})
    output={'scope':'Float discovery only; exact certificate still required.','linprog_calls':1,
            'point_sha256':POINT_SHA,'symbolic_lift_sha256':digest(HERE/'max_b_symbolic_lift.json'),
            'success':bool(result.success),'status':int(result.status),'message':result.message,
            'objective':None if result.fun is None else float(result.fun),
            'x':None if result.x is None else result.x.tolist(),
            'inequality_marginals':None if result.ineqlin.marginals is None else result.ineqlin.marginals.tolist(),
            'lower_marginals':None if result.lower.marginals is None else result.lower.marginals.tolist(),
            'inequality_residual':None if result.ineqlin.residual is None else result.ineqlin.residual.tolist()}
    save('max_b_phase_I.json',output)
    print(json.dumps({k:output[k] for k in ('success','status','message','objective','linprog_calls')}))


if __name__=='__main__':
    if sys.argv[1:] == ['phase-one']: phase_one()
    else: build()
