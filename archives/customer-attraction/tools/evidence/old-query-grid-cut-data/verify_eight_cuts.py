"""Independent literal-edge reconstruction of the eight frozen grid cuts.

No old-query discover/row, mixed-row generator, projected_by_count, LP, or
full graph build is imported. The singleton hidden follower is enumerated.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict, Counter
import argparse
import hashlib
import json

PAT=tuple(product((0,1),repeat=3))
INPUT_PATH='research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_3/all_reply_floors_exact.json'
PRIMARY_SHA='755ba74498e07b2372630b165885055529776434c96c8c64a1eed20943923884'
POINT_SHA='f6f4d5c28857e8e6350bdc8528daa6109122bce8a6fb00e8ac5c3150ffc42314'


def share(member,background):
    return F(member,background+member) if member else F(0)


def branch(a,t,q,g):
    p,ell=sum(a[:4]),sum(a[:5])
    return share(t,p+g)+F(g,ell+1)-share(g,p+t)+F(q,p+t+1)


def projected(a,t,q):
    return min(branch(a,t,q,g) for g in (0,1))


def pair_coefficient(a,t,q):
    p=sum(a[:4]);D=(p+1)*(p+2)
    u5=share(a[4],sum(a)-a[4]);u6=share(a[5],sum(a)-a[5])
    return u5+u6+F(a[4],D)-F(t+q,p+1)+F(t*q,D)


def read(path,expected):
    raw=path.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    assert digest==expected,(path,digest)
    return json.loads(raw),{'bytes':len(raw),'sha256':digest}


def main():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    here=Path(__file__).resolve().parent
    ap=argparse.ArgumentParser()
    ap.add_argument('--cuts',type=Path,default=here/'original/old_query_cuts.json')
    ap.add_argument('--point',type=Path,default=here.parent/'all-reply-actual-floors-program/related/all_reply_floors_exact.json')
    ap.add_argument('--output',type=Path,default=here/'independent-report.json')
    args=ap.parse_args()
    data,primary=read(args.cuts,PRIMARY_SHA);point,point_meta=read(args.point,POINT_SHA)
    assert set(data)=={'scope','input','W','candidates_checked','negative_candidates','selected'}
    assert data['scope']=='finite rational-grid separation only; necessary graph, not SPE'
    assert data['input']==INPUT_PATH and data['W']==point['W']
    assert len(data['selected'])==8 and all(set(item)=={'cut','slack'} for item in data['selected'])
    assert data['negative_candidates']==8
    price_grid=(F(0),F(1,8),F(1,4),F(1,2),F(1),F(2))
    query_grid=(F(0),F(1,2),F(1),F(2),F(4))
    candidate_count=5*2*3*6*(2*len(price_grid)-1)*len(query_grid)
    assert candidate_count==data['candidates_checked']==9900
    expected_structure=[(0,4,'all'),(0,4,'last'),(0,2,'all'),(0,2,'last'),
                        (1,1,'all'),(1,1,'last'),(1,4,'all'),(1,4,'last')]
    for item,structure in zip(data['selected'],expected_structure):
        i,member,f,diag,qi,mode,aa,mu=item['cut']
        assert (i,member,f,aa,mu)==(4,1,1,'1','1')
        assert (diag,qi,mode)==structure
    local_cases=0
    for a in product((0,1),repeat=6):
        p=sum(a[:4]);D=(p+1)*(p+2)
        u5=share(a[4],sum(a)-a[4]);u6=share(a[5],sum(a)-a[5])
        for t,q in product((0,1),repeat=2):
            v0,v1=branch(a,t,q,0),branch(a,t,q,1)
            assert v0-v1==F(a[4],D)
            assert projected(a,t,q)==v1==F(t+q,p+1)-F(t*q+a[4],D)
            assert u5+u6-projected(a,t,q)==pair_coefficient(a,t,q)
            local_cases+=1
    columns=point['columns'];assert len(columns)==1905
    weights=[F(c['weight']) for c in columns];assert min(weights)>=0
    positive_columns=sum(w>0 for w in weights)
    assert positive_columns==point['positive_columns']==168
    hist={};current=None
    for j,c in enumerate(columns):
        if c['kind']=='hist':
            current=j;hist[j]={'column':c,'groups':{}}
            assert len(c['actual_bits'])==6 and set(c['actual_bits'])<=set('01')
            assert len(c['hist'])==8 and sum(c['hist'])==6 and min(c['hist'])>=0
            assert sum(n*w[0] for n,w in zip(c['hist'],PAT))==c['d']
        elif c['kind']=='joint-reply':
            f,d,wi,wj=c['group'];key=f,d,tuple(wi),tuple(wj)
            states=hist[current]['groups'].setdefault(key,{})
            assert tuple(c['state']) not in states
            states[tuple(c['state'])]=j
        else:assert c['kind'] in ('K','overlap')
    assert len(hist)==16
    for hi,h in hist.items():
        for key,states in h['groups'].items():
            assert set(states)=={(0,1),(1,0),(1,1)}
            assert sum(weights[j] for j in states.values())<=weights[hi]
    normal=sum(weights[j] for j,h in hist.items() if h['column']['d']>0)
    welfare=sum(weights[j] for j,h in hist.items() if '1' in h['column']['actual_bits'])
    assert normal==F(point['O'])==1 and welfare==F(data['W'])
    assert normal-2*welfare==F(point['strict_half_gap'])>0
    utilities=[sum(weights[j]*share(int(h['column']['actual_bits'][i]),
                                   sum(map(int,h['column']['actual_bits']))-int(h['column']['actual_bits'][i]))
                   for j,h in hist.items()) for i in range(6)]
    assert sum(utilities)==welfare
    all_rows=[];records=[]
    for index,item in enumerate(data['selected']):
        i,member,f,diag,qi,mode,aa,mu=item['cut'];row=[F(0)]*1905;pairrow=[F(0)]*1905
        for hi,h in hist.items():
            a=tuple(map(int,h['column']['actual_bits']))
            words=tuple(w for w,n in zip(PAT,h['column']['hist']) for _ in range(n))
            edges=[(j,k) for j,k in product(range(6),repeat=2) if int(j==k)==diag]
            assert len(edges)==(6 if diag else 30)
            u5=share(a[4],sum(a)-a[4]);u6=share(a[5],sum(a)-a[5])
            for j,k in edges:
                q=(words[j]+words[k])[qi]
                base=u5+u6-projected(a,0,q)
                delta=projected(a,0,q)-projected(a,1,q)
                row[hi]+=base;pairrow[hi]+=pair_coefficient(a,0,q)
                states=h['groups'][f,diag,words[j],words[k]]
                for (r,z),column_index in states.items():
                    row[column_index]+=z*delta
                    pairrow[column_index]+=pair_coefficient(a,z,q)-pair_coefficient(a,0,q)
        assert row==pairrow
        assert all(v==0 for v,c in zip(row,columns) if c['kind'] in ('K','overlap'))
        slack=sum(x*y for x,y in zip(row,weights))
        assert slack==F(item['slack'])<0
        canonical=json.dumps(list(map(str,row)),separators=(',',':')).encode()
        records.append({'record':index+1,'cut':item['cut'],'slack':str(slack),
                        'mixed_pair_key':[member,f,diag,qi+6],
                        'coefficient_count':len(row),'coefficient_vector_sha256':hashlib.sha256(canonical).hexdigest()})
        all_rows.append(tuple(row))
    equivalence=defaultdict(list)
    for i,row in enumerate(all_rows,1):equivalence[row].append(i)
    classes=list(equivalence.values())
    assert classes==[[1,2],[3,4],[5,6,7,8]]
    # Source selection is ordered by exact slack then the full parameter tuple.
    assert [(F(x['slack']),tuple(x['cut'])) for x in data['selected']]==sorted((F(x['slack']),tuple(x['cut'])) for x in data['selected'])
    assert len({tuple(x['cut'][:6]) for x in data['selected']})==8
    report={'scope':'new independent literal-edge eight-cut audit; no 9900-candidate rescan, original CLI, LP, full graph or SPE enumeration',
            'primary':primary,'point':point_meta,'all_six_primary_fields_read':True,
            'grid_size_from_program_product':candidate_count,
            'negative_candidates_8_scope':'verified by companion original full-grid replay, not inferred from selected length by this script',
            'singleton_follower_cases':local_cases,'branch_values_checked':2*local_cases,
            'closed_form_equals_existing_strong_PAIR':True,
            'columns_read':len(columns),'column_kinds':dict(Counter(c['kind'] for c in columns)),
            'histograms':len(hist),'reply_groups':sum(len(h['groups']) for h in hist.values()),
            'point_weights_nonnegative':True,'joint_00_nonnegative':True,
            'positive_columns':positive_columns,'actual_utilities':list(map(str,utilities)),
            'point_O':str(normal),'point_W':str(welfare),'point_original_verified_rows_metadata_only':point['verified_rows'],
            'selected_rows':records,'all_selected_slacks_exact_and_negative':True,
            'coefficient_comparisons_between_literal_projection_and_PAIR':8*1905,
            'distinct_coefficient_vectors':len(equivalence),'equal_vector_record_classes':classes,
            'source_eight_record_order_preserved':True,
            'coefficient_digest_encoding':'sha256(json.dumps([str(Fraction) for each of 1905 columns],separators=(comma,colon)).encode())',
            'limits':'Original 8 records retained despite 3 vector classes. No exact rank assertion, full-parameter separation completeness, full 4963-row verification or complete finite-game realization.'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('singleton_follower_cases','coefficient_comparisons_between_literal_projection_and_PAIR','distinct_coefficient_vectors','equal_vector_record_classes','all_selected_slacks_exact_and_negative')},indent=2))


if __name__=='__main__':main()
