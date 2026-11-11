"""Independent literal reconstruction; does not import max_b_lift."""
from collections import defaultdict, Counter
from fractions import Fraction as Q
from itertools import product
from hashlib import sha256
from pathlib import Path
import gzip
import json

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
OLD=4849


def freeze(a):
    return tuple(map(freeze,a)) if isinstance(a,list) else a


def add(r,j,v):
    r[j]=r.get(j,Q())+v
    if not r[j]:del r[j]


def read(path):
    return json.loads(gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_bytes())


def main():
    d=read(HERE/'max_b_symbolic_lift.json')
    pointpath=WORK/'full624_augmented_lp/recovery/augmented_lp_exact.json'
    pairpath=WORK/'actual_pair_20910/symbolic_rows.json.gz'
    assert sha256(pointpath.read_bytes()).hexdigest()==d['point_sha256']
    assert sha256(pairpath.read_bytes()).hexdigest()==d['pair_rows_sha256']
    old=read(pointpath)['columns'];hist={};own=defaultdict(dict);B4=defaultdict(dict)
    for j,c in enumerate(old[:OLD]):
        if c['kind']=='hist':h=j;hist[h]=c
        elif c['kind']=='joint-reply':own[h][freeze(c['group']),tuple(c['state'])]=j
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            B4[c['hist_column']][tuple(c['hidden'])+(c['ell']//6,)]=j
    xc={};yc={};mass={}
    for k,c in enumerate(d['new_columns'],OLD):
        h=c['hist_column']
        if c['kind']=='common-X-mass':xc[h]=k
        else:
            t=freeze(c['query_token']);yc[h,t]=k
            if t[0]=='H':r={j:Q(1) for s,j in B4[h].items() if s[t[1]]}
            else:
                slot=int(t[0]=='Z');g=t[1]
                r={j:Q(1) for (gg,s),j in own[h].items() if gg==g and s[slot]}
            assert r=={j:Q(v) for j,v in c['query_marginal']}
            mass[h,t]=r
    assert set(xc)==set(hist) and len(yc)==420
    actions=[('A',k) for k in range(6)]+[(k,i) for k in ('T','B','C') for i in range(6)]
    for k in ('R','Z'):
        actions += [(k,f,i,j) for f in range(2) for i in range(6) for j in range(6) if f or i!=j]
    actions += [('H',0),('H',1)]
    byorbit=defaultdict(list)
    for q in actions:
        orb=q if q[0] in ('A','H') else (q[0],) if q[0] in ('T','B','C') else (q[0],q[1],int(q[2]==q[3]))
        byorbit[orb].append(q)
    rebuilt={}
    for h in hist:rebuilt['X-at-most-hist',h]={h:Q(1),xc[h]:Q(-1)}
    for (h,t),k in yc.items():
        rebuilt['overlap-at-most-X',k]={xc[h]:Q(1),k:Q(-1)}
        r=dict(mass[h,t]);r[k]=Q(-1);rebuilt['overlap-at-most-query',k]=r
    income=[{} for _ in range(6)];tax={};BX={}
    for h,c in hist.items():
        bits=tuple(map(int,c['actual_bits']));P=sum(bits[:4]);n=sum(bits)
        for k in range(6):
            if bits[k]:income[k][h]=Q(1,n)
        if bits[4]:tax[h]=Q(1,(P+1)*(P+2))
        BX[xc[h]]=Q(1,P+1)
    literal_query_terms=0
    for orb,qs in byorbit.items():
        maximum=dict(BX);cap=dict(income[4]);scale=Q(1,len(qs))
        for h,c in hist.items():
            bits=tuple(map(int,c['actual_bits']));P=sum(bits[:4]);D=(P+1)*(P+2)
            words=[w for w,n in zip(product((0,1),repeat=3),c['hist']) for _ in range(n)]
            for q in qs:
                if q[0]=='A':t=('bit',bits[q[1]])
                elif q[0] in ('T','B','C'):t=('bit',words[q[1]][('T','B','C').index(q[0])])
                elif q[0]=='H':t=q
                else:
                    k,f,i,j=q;t=(k,(f,int(i==j),words[i],words[j]))
                if t[0]=='bit':
                    if t[1]:
                        add(maximum,h,-scale/Q(P+1));add(cap,h,-scale/Q(P+1));add(cap,xc[h],scale/Q(D))
                else:
                    for j,v in mass[h,t].items():
                        add(maximum,j,-scale*v/Q(P+1));add(cap,j,-scale*v/Q(P+1))
                    add(cap,yc[h,t],scale/Q(D))
                literal_query_terms+=1
        rebuilt[('maximum-B',)+orb]=maximum;rebuilt[('X-caps-query',)+orb]=cap
    for k in range(6):
        r=dict(income[k])
        for h,c in hist.items():add(r,xc[h],-Q(1,sum(map(int,c['actual_bits'][:k]))+6-k))
        rebuilt['actual-safe-X',k+1]=r
    r={0:Q(1)}
    for j in xc.values():r[j]=Q(-1)
    rebuilt['capacity-X',]=r
    for p in read(pairpath)['rows']:
        r={j:Q(v) for j,v in p['sparse_original4849_row']}
        for j,v in income[5].items():add(r,j,-v)
        for j,v in tax.items():add(r,j,-v)
        for j,v in BX.items():add(r,j,v)
        rebuilt['common-B-pair',p['orbit_id']]=r
    assert len(rebuilt)==1387
    coefficient_checks=0
    for record in d['rows']:
        key=tuple(record['name']);r={j:Q(v) for j,v in record['row']}
        assert r==rebuilt[key],key
        coefficient_checks+=len(r)
    answer={'status':'passed','scope':'All 1387 rows reconstructed literally; frozen 490 pair-envelope rows reused at their verified SHA.',
            'rows_checked':len(rebuilt),'nonzero_coefficients_checked':coefficient_checks,
            'literal_label_hist_query_terms':literal_query_terms,
            'all_16_histograms':True,'all_158_labels':True,'all_17_single_orbits':True,
            'all_490_pair_orbits':True,'point_sha256':d['point_sha256'],
            'symbolic_lift_sha256':sha256((HERE/'max_b_symbolic_lift.json').read_bytes()).hexdigest()}
    (HERE/'max_b_independent_preflight.json').write_text(json.dumps(answer,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(answer,ensure_ascii=False))
    certpath=HERE/'max_b_exact_certificate.json'
    if certpath.exists():
        cert=read(certpath);acc={}
        assert cert['symbolic_lift_sha256']==answer['symbolic_lift_sha256']
        for rec in cert['row_multipliers']:
            i=rec['row_index'];weight=Q(rec['multiplier'])
            assert weight>=0 and rec['name']==d['rows'][i]['name']
            for j,v in rebuilt[tuple(rec['name'])].items():add(acc,j,weight*v)
        for rec in cert['new_nonnegativity_multipliers']:
            weight=Q(rec['multiplier']);j=rec['column']
            assert weight>=0 and OLD<=j<OLD+436
            assert rec['descriptor']==d['new_columns'][j-OLD]
            add(acc,j,weight)
        assert all(j<OLD for j in acc)
        assert acc=={j:Q(v) for j,v in cert['sparse_original4849_row']}
        small={j:v/3 for j,v in acc.items()}
        assert small=={j:Q(v) for j,v in cert['sparse_original4849_row_K_normalized']}
        direct={0:Q(1)}
        for h,c in hist.items():
            bits=list(map(int,c['actual_bits']));p=sum(bits[:4]);total=sum(bits);D=(p+1)*(p+2)
            dB=sum(n*w[1] for w,n in zip(product((0,1),repeat=3),c['hist']))
            dC=sum(n*w[2] for w,n in zip(product((0,1),repeat=3),c['hist']))
            dBC=sum(n*w[1]*w[2] for w,n in zip(product((0,1),repeat=3),c['hist']))
            u=Q(bits[4],total) if bits[4] else Q();v=Q(bits[5],total) if bits[5] else Q()
            rho=Q(12*bits[5]+24*bits[4]+6*dC-(p+2)*(p+9),D)
            coefficient=64*u+24*v-Q(12*bits[5],p+1)-Q(8*dB+26*dC,3*(p+1))+Q(8*dBC,3*D)+max(Q(),rho)
            add(direct,h,coefficient)
        assert direct==small
        value=sum((v*Q(old[j]['weight']) for j,v in acc.items()),Q())
        assert value==Q(cert['exact_point_value'])<0
        assert value/3==Q(cert['K_normalized_point_value'])
        assert -value/331==Q(cert['exact_phase_I_lower_bound'])
        result={'status':'PASS','scope':'Exact nonnegative Farkas combination plus independent direct all-type formula; no optimizer call.',
                'point_sha256':d['point_sha256'],'certificate_sha256':sha256(certpath.read_bytes()).hexdigest(),
                'row_count':1387,'new_columns_canceled':436,'original_nonzero_columns':len(acc),
                'all_old_auxiliary_coefficients_zero':True,'normalized_row_field':'sparse_original4849_row_K_normalized',
                'K_normalized_exact_value':str(value/3),'K_normalized_value_float':float(value/3)}
        (HERE/'max_b_independent_certificate_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
