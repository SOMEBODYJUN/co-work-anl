"""Independent literal-payoff reconstruction; imports no builder or solver.

All E=0 and E=1 masses are expanded from complete 0/1 states.  All literal
orbit frequencies are checked under 720 permutations with repetitions.
Run before discovery and again on the final exact primal or Farkas record.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import argparse
import json

HERE=Path(__file__).resolve().parent
POINT=HERE.parent/'full624_augmented_lp/recovery/augmented_lp_exact.json'
EXPECTED='cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932'


def sha(p):return sha256(p.read_bytes()).hexdigest()


def save(n,x):(HERE/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')


def fraction(n,d):
    if d==0:
        assert n==0
        return Q()
    return Q(n,d)


def canonical(indices):
    distinct=[];out=[]
    for k in indices:
        if k not in distinct:distinct.append(k)
        out.append(str(distinct.index(k)))
    return ''.join(out)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',action='store_true');args=ap.parse_args()
    lift=json.loads((HERE/'symbolic_lift.json').read_bytes())
    point=json.loads(POINT.read_bytes())
    assert sha(POINT)==EXPECTED==lift['point_sha256']
    assert lift['row_constants']==0 and lift['nonnegative_new_columns']
    cols=point['columns'][:4849]
    assert lift['old_descriptors']==[{k:v for k,v in c.items() if k!='weight'} for c in cols]
    w=[Q(c['weight']) for c in cols]
    hist={};old=defaultdict(dict)
    for j,c in enumerate(cols):
        if c['kind']=='hist':h=j;hist[h]=c
        elif c['kind']=='joint-reply':
            f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj))
            old[h].setdefault(g,{})[tuple(c['state'])]=j
    nodes=[(f,i,j) for f in (0,1) for i in range(6) for j in range(6) if f or i!=j]
    nodeorbits=defaultdict(list);triples=defaultdict(list);pairs=defaultdict(list)
    for f,i,j in nodes:
        nodeorbits[f,int(i==j)].append((f,i,j))
        for k in range(6):triples[f,canonical((i,j,k))].append((f,i,j,k))
        for ff,k,l in nodes:pairs[f,ff,canonical((i,j,k,l))].append((f,i,j,ff,k,l))
    allperms=list(permutations(range(6)))
    orbit_checks=[]
    for typ,collection in [('node',nodeorbits),('query-index',triples),('R-E-pair',pairs)]:
        for key,items in sorted(collection.items()):
            f,i,j,*tail=items[-1]
            if not tail:images=[(f,p[i],p[j]) for p in allperms]
            elif len(tail)==1:images=[(f,p[i],p[j],p[tail[0]]) for p in allperms]
            else:
                ff,k,l=tail;images=[(f,p[i],p[j],ff,p[k],p[l]) for p in allperms]
            frequency=Counter(images)
            assert frequency==Counter({item:720//len(items) for item in items})
            orbit_checks.append({'kind':typ,'orbit':list(key),'size':len(items),
                                 'frequency':720//len(items)})
    assert len(orbit_checks)==53
    xs={}
    for j,c in enumerate(lift['new_columns'],4849):
        assert c['kind']=='E-given-own-RZ-state'
        f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj));s=tuple(c['old_state'])
        key=(c['hist_column'],g,s);assert key not in xs;xs[key]=j
    assert len(xs)==776 and set(xs)=={(h,g,s) for h in old for g in old[h] for s in product((0,1),repeat=2)}

    rebuilt=defaultdict(lambda:defaultdict(Q))
    def insert(name,vector,scale=Q(1)):
        rr=rebuilt[tuple(name)]
        for j,v in vector.items():rr[j]+=scale*v
    def base(j):return {j:Q(1)}
    def mass(h,g,s):
        if s!=(0,0):return base(old[h][g][s])
        return {h:Q(1),**{j:Q(-1) for j in old[h][g].values()}}
    def fullmass(h,g,s,e):
        x=xs[h,g,s]
        if e:return base(x)
        out=mass(h,g,s);out[x]=Q(-1);return out
    def target(h,g):return {xs[h,g,s]:Q(1) for s in product((0,1),repeat=2)}
    def gp(ws,node):
        f,i,j=node;return f,int(i==j),ws[i],ws[j]

    boxchecks=0;literal_states=0
    for h,c in hist.items():
        a=tuple(int(ch) for ch in c['actual_bits'])
        p3=sum(a[:3]);P=sum(a[:4]);total=sum(a)
        words=[word for word,n in zip(product((0,1),repeat=3),c['hist']) for _ in range(n)]
        assert len(words)==6
        expectedgroups=defaultdict(list)
        for e in nodes:expectedgroups[gp(words,e)].append(list(e))
        for g in old[h]:
            assert set(old[h][g])=={(0,1),(1,0),(1,1)}
            for s in product((0,1),repeat=2):
                j=xs[h,g,s]
                assert lift['new_columns'][j-4849]['named_nodes']==expectedgroups[g]
                M=mass(h,g,s)
                assert sum(v*w[i] for i,v in M.items())>=0
                insert(('E-at-most-old-state',j),M)
                insert(('E-at-most-old-state',j),base(j),-1);boxchecks+=1
        for orbit,indices in nodeorbits.items():
            weight=Q(1,len(indices))
            insert(('A5-force-Z-with-E',*orbit),base(h),fraction(a[4],total))
            for k in range(1,7):
                name=('A-safe-to-E',k,*orbit) if k<6 else ('A6-to-E',*orbit)
                insert(name,base(h),fraction(a[k-1],total))
            for f,i,j in indices:
                g=gp(words,(f,i,j))
                for r,z,e in product((0,1),repeat=3):
                    atom=fullmass(h,g,(r,z),e);literal_states+=1
                    # Terminal actions are (Z_e,E_e) after actual A1..A4.
                    insert(('A5-force-Z-with-E',*orbit),atom,-weight*fraction(z,P+z+e))
                    epay=fraction(e,P+z+e)
                    for k,q in enumerate(a,1):
                        insert(('E-to-A',k,*orbit),atom,weight*(epay-fraction(q,P+z+q)))
                    for kind,q in [('R',r),('Z',z)]:
                        insert(('E-to-own-'+kind,*orbit),atom,weight*(epay-fraction(q,P+z+q)))
                    # The old Z is selected at the distinct history (A1..A4,R_e).
                    insert(('own-Z-to-E',*orbit),atom,weight*(fraction(z,P+r+z)-fraction(e,P+r+e)))
                    insert(('capacity-E',*orbit),atom,-weight*e)
                    for k in range(1,7):
                        name=('A-safe-to-E',k,*orbit) if k<6 else ('A6-to-E',*orbit)
                        insert(name,atom,-weight*fraction(e,sum(a[:k-1])+e+6-k))
        for orbit,indices in triples.items():
            weight=Q(1,len(indices))
            for f,i,j,k in indices:
                g=gp(words,(f,i,j))
                for r,z,e in product((0,1),repeat=3):
                    atom=fullmass(h,g,(r,z),e)
                    for kind,q in zip(('T','B','C'),words[k]):
                        insert(('E-to-'+kind,*orbit),atom,weight*(fraction(e,P+z+e)-fraction(q,P+z+q)))
        for orbit,indices in pairs.items():
            weight=Q(1,len(indices));name=('old-R-to-E',*orbit)
            for f,i,j,ff,k,l in indices:
                gs=gp(words,(f,i,j));gt=gp(words,(ff,k,l))
                prefix=p3+words[i][0]+words[j][1+f]
                for r,z in product((0,1),repeat=2):
                    insert(name,mass(h,gs,(r,z)),weight*fraction(r,prefix+r))
                # E's payoff at this old R history has denominator prefix+1.
                insert(name,target(h,gt),-weight*fraction(1,prefix+1))
    for orbit in nodeorbits:insert(('capacity-E',*orbit),base(0))
    rebuilt={name:{j:v for j,v in row.items() if v} for name,row in rebuilt.items()}
    assert len(rebuilt)==len(lift['rows'])==893
    allcoefs=0
    for saved in lift['rows']:
        row={j:Q(v) for j,v in saved['row']}
        assert row==rebuilt[tuple(saved['name'])],('literal coefficient mismatch',saved['name'])
        assert all(0<=j<5625 for j in row)
        allcoefs+=len(row)

    # These truth tables prove literal-history identities also outside the
    # positive support of this point and include zero numerator conventions.
    truth=Counter()
    for P in range(5):
        for z,e,q,r in product((0,1),repeat=4):
            assert fraction(z,P+z+e)==fraction(z,P+1)-fraction(z*e,(P+1)*(P+2));truth['force-Z']+=1
            assert fraction(e,P+z+e)-fraction(q,P+z+q)==fraction(e-q,P+z+1);truth['E-last']+=1
            assert fraction(z,P+r+z)-fraction(e,P+r+e)==fraction(z-e,P+r+1);truth['old-Z-last']+=1
    for p in range(6):
        for r,e in product((0,1),repeat=2):
            assert fraction(r,p+r)-fraction(e,p+e)==fraction(r-e,p+1);truth['old-R-last']+=1
    for k in range(1,7):
        for p in range(k):
            for e in (0,1):
                for future in range(7-k):
                    assert fraction(e,p+e+future)>=fraction(e,p+7-k);truth['actual-SAFE']+=1

    wallets=[]
    for saved in lift['rows']:
        name=saved['name'];kind=name[0]
        if kind=='E-at-most-old-state':continue
        wallet={'row':name,'global_fixed_weights':True,'hist_dependent_weight_selection':False}
        if kind=='A5-force-Z-with-E':
            orbit=tuple(name[1:]);items=nodeorbits[orbit]
            wallet.update(source='Actual player 5 at (A1,A2,A3,A4)',forced='Z_e',successor='sigma6(A1,A2,A3,A4,Z_e)=E_e',budget='u5 exactly once',weight=str(Q(1,len(items))),named_comparisons=len(items))
        elif kind in ('A-safe-to-E','A6-to-E'):
            k=name[1] if kind=='A-safe-to-E' else 6;orbit=tuple(name[2:] if k<6 else name[1:]);items=nodeorbits[orbit]
            wallet.update(source=f'Actual player {k} at actual length-{k-1} prefix',budget=f'u{k} exactly once',quote='Exact last price' if k==6 else 'SAFE with at most 6-k future coverings',weight=str(Q(1,len(items))),named_comparisons=len(items))
        elif kind=='capacity-E':
            orbit=tuple(name[1:]);items=nodeorbits[orbit]
            wallet.update(source='Common maximum topic cardinality',budget='K exactly once',weight=str(Q(1,len(items))),named_comparisons=len(items))
        elif kind=='old-R-to-E':
            orbit=tuple(name[1:]);items=pairs[orbit]
            count=Counter((f,i,j) for f,i,j,ff,k,l in items)
            assert len(set(count.values()))==1
            wallet.update(source='Player 6 at (A1,A2,A3,T_i,B_j) for f=0; (A1,A2,A3,T_i,C_j) for f=1',budget='True old R income averaged once over its source orbit',weight=str(Q(1,len(items))),named_comparisons=len(items),source_multiplicity=next(iter(count.values())),source_count=len(count))
        elif kind=='own-Z-to-E':
            orbit=tuple(name[1:]);items=nodeorbits[orbit]
            wallet.update(source='Player 6 at (A1,A2,A3,A4,R_e)',budget='True Z income averaged once',weight=str(Q(1,len(items))),named_comparisons=len(items))
        elif kind.startswith('E-to-'):
            if kind in ('E-to-T','E-to-B','E-to-C'):
                orbit=tuple(name[1:]);items=triples[orbit]
                count=Counter(tuple(t[:3]) for t in items);assert len(set(count.values()))==1
                wallet.update(source_count=len(count),source_multiplicity=next(iter(count.values())))
            else:
                orbit=tuple(name[2:] if kind=='E-to-A' else name[1:]);items=nodeorbits[orbit]
            wallet.update(source='Player 6 at (A1,A2,A3,A4,Z_e)',budget='True E income averaged once',weight=str(Q(1,len(items))),named_comparisons=len(items))
        else:raise AssertionError(kind)
        wallets.append(wallet)
    assert len(wallets)==117

    report={'scope':'Independent full-domain literal payoff and symbolic coefficient audit, including all zero histograms; no common-E or SPE conclusion.',
            'point_sha256':sha(POINT),'symbolic_lift_sha256':sha(HERE/'symbolic_lift.json'),
            'audit_source_sha256':sha(Path(__file__)),'histograms':len(hist),'groups':sum(map(len,old.values())),
            'new_columns_checked':len(xs),'box_rows_checked':boxchecks,'global_rows_checked':len(wallets),
            'all_rows_checked':len(rebuilt),'all_nonzero_coefficients_checked':allcoefs,
            'literal_joint_state_evaluations_in_node_rows':literal_states,
            'orbit_types':len(orbit_checks),'full_permutation_images':720*len(orbit_checks),
            'all_orbit_weights_exact':True,'truth_table_counts':dict(truth),
            'zero_mass_histograms':[h for h in hist if w[h]==0],
            'old00_symbolic_identity_rebuilt':True,'every_source_wallet_global_and_paid_once':True}
    save('wallet_audit.json',{'wallets':wallets,'orbit_audits':orbit_checks,'truth_table_counts':dict(truth)})
    if args.certificate:
        exact=json.loads((HERE/'exact_certificate.json').read_bytes())
        assert exact['point_sha256']==sha(POINT)
        assert exact['symbolic_lift_sha256']==sha(HERE/'symbolic_lift.json')
        if exact['kind']=='primal':
            x=[Q(t) for t in exact['new_values']];values=w+x
            assert len(x)==776 and min(x)>=0
            slacks=[]
            for row in lift['rows']:
                s=sum(v*values[j] for j,v in rebuilt[tuple(row['name'])].items())
                assert s>=0,(row['name'],s);slacks.append(s)
            assert [str(s) for s in slacks]==exact['row_slacks']
            report.update(kind='primal',phase_I='0',minimum_slack=str(min(slacks)),minimum_x=str(min(x)),negative_rows=0,
                          all_776_rational_values_and_893_rows_verified=True)
        else:
            assert exact['kind']=='Farkas'
            lam=[Q(t) for t in exact['lambda']];mu=[Q(t) for t in exact['nonnegative_x_multipliers']]
            assert len(lam)==893 and len(mu)==776 and min(lam)>=0 and min(mu)>=0
            comb=defaultdict(Q)
            for multiplier,row in zip(lam,lift['rows']):
                for j,v in rebuilt[tuple(row['name'])].items():comb[j]+=multiplier*v
            for j,multiplier in enumerate(mu,4849):comb[j]+=multiplier
            assert all(comb[j]==0 for j in range(4849,5625))
            oldrow={j:v for j,v in comb.items() if j<4849 and v}
            assert oldrow=={j:Q(v) for j,v in exact['old_necessary_row']}
            val=sum(v*w[j] for j,v in oldrow.items());assert val<0
            assert val==Q(exact['old_point_value'])
            report.update(kind='Farkas',old_necessary_row=sparse(oldrow),old_point_value=str(val),old_point_value_float=float(val),
                          all_new_variables_eliminated=True,all_multipliers_nonnegative=True,
                          positive_lambda_count=sum(t>0 for t in lam),positive_nonnegative_x_count=sum(t>0 for t in mu))
        save('independent_certificate_audit.json',report)
    else:save('preflight_literal_audit.json',report)
    print(json.dumps(report,ensure_ascii=False))


def sparse(r):return [[j,str(v)] for j,v in sorted(r.items()) if v]


if __name__=='__main__':main()
