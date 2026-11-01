"""Independent four-cut PAIR/endpoint audit; no original function or LP call."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path


def frac(n,d):
    return F(n,d) if n else F()


def endpoint(a,t,q):
    b=sum(a[:4]);ell=sum(a[:5])
    values=[frac(t-z,b+t+z)+F(z,ell+1) for z in (0,1)]
    return frac(q,b+t+q)+min(values),values


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cuts',type=Path,required=True)
    p.add_argument('--point',type=Path,required=True)
    p.add_argument('--author-functions',type=Path,required=True)
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    data=json.loads(args.cuts.read_text());point=json.loads(args.point.read_text())
    assert args.cuts.stat().st_size==1671
    assert hashlib.sha256(args.cuts.read_bytes()).hexdigest()=='bcc5d334bfd6e8f9d1be71620a00fc8bf13e053420aa9bd7bd3ed2240d01d606'
    assert args.point.stat().st_size==815400
    assert hashlib.sha256(args.point.read_bytes()).hexdigest()==data['source_sha256']=='78e3a89cf01a62ea2a4d2768043e09027e0b3dd920984d3f9591b0c0a1e0fe2e'
    assert set(data)=={'best_float','selected','scope','source','source_sha256','source_W'}
    assert len(data['selected'])==4
    cols=point['columns'];assert len(cols)==1905
    weights=[F(c['weight']) for c in cols]
    assert min(weights)>=0 and sum(v>0 for v in weights)==point['positive_columns']==169
    kinds=Counter(c['kind'] for c in cols)
    assert kinds=={'K':1,'hist':16,'joint-reply':582,'overlap':1306}
    words8=list(product((0,1),repeat=3));hs={};hi=None
    for j,c in enumerate(cols):
        if c['kind']=='hist':
            hi=j;hs[j]={'column':c,'groups':{}}
            assert len(c['hist'])==8 and sum(c['hist'])==6
            assert all(isinstance(n,int) and n>=0 for n in c['hist'])
            assert len(c['actual_bits'])==6 and set(c['actual_bits'])<=set('01')
            assert sum(n*w[0] for n,w in zip(c['hist'],words8))==c['d']
        elif c['kind']=='joint-reply':
            f,d,wi,wj=c['group'];key=(f,d,tuple(wi),tuple(wj));st=tuple(c['state'])
            assert st in {(0,1),(1,0),(1,1)}
            assert st not in hs[hi]['groups'].setdefault(key,{})
            hs[hi]['groups'][key][st]=(j,F(c['weight']))
    group_read=[]
    for hi,h in hs.items():
        H=F(h['column']['weight'])
        for key,states in h['groups'].items():
            assert set(states)=={(0,1),(1,0),(1,1)}
            zero=H-sum(v for _,v in states.values())
            assert zero>=0
            group_read.append({'hist_column':hi,'group':key,'implicit_00':str(zero),
                               'explicit':[{'state':st,'column':j,'weight':str(v)} for st,(j,v) in sorted(states.items())]})
    assert len(group_read)==194
    O=sum(F(h['column']['weight']) for h in hs.values() if h['column']['d']>0)
    W=sum(F(h['column']['weight']) for h in hs.values() if '1' in h['column']['actual_bits'])
    u5=sum(F(h['column']['weight'])*frac(int(h['column']['actual_bits'][4]),sum(map(int,h['column']['actual_bits']))) for h in hs.values())
    u6=sum(F(h['column']['weight'])*frac(int(h['column']['actual_bits'][5]),sum(map(int,h['column']['actual_bits']))) for h in hs.values())
    assert O==F(point['O'])==1 and str(W)==point['W']==data['source_W']
    assert 1-2*W==F(point['strict_half_gap'])
    endpoint_cases=0
    for a,t,q in product(product((0,1),repeat=6),(0,1),(0,1)):
        b=sum(a[:4]);D=(b+1)*(b+2);value,terms=endpoint(a,t,q)
        assert terms[0]-terms[1]==F(a[4],D)
        assert value==F(t+q,b+1)-F(t*q,D)-F(a[4],D)
        endpoint_cases+=1
    author=json.loads(args.author_functions.read_text())['records']
    assert len(author)==4
    rows=[];records=[]
    mixed_keys=[(1,0,0,5),(1,1,0,5),(1,1,0,10),(1,1,1,5)]
    for number,(cut,expected,mixed) in enumerate(zip(data['selected'],author,mixed_keys),1):
        assert set(cut)=={'i','member','orb','q','alpha','gamma','slack'}
        assert cut==expected['cut'] and cut['i']==4 and cut['member']==1
        assert cut['alpha']==cut['gamma']=='1'
        family,diagonal=cut['orb'];n=6 if diagonal else 30
        literal=[F() for c in cols];pair=[F() for c in cols]
        state_masses=defaultdict(F);contributions=[]
        for hi,h in hs.items():
            c=h['column'];H=F(c['weight']);a=tuple(map(int,c['actual_bits']))
            b=sum(a[:4]);D=(b+1)*(b+2);ell=sum(a[:5]);whole=sum(a)
            words=[w for w,count in zip(words8,c['hist']) for _ in range(count)]
            edges=[(i,j) for i in range(6) for j in range(6) if int(i==j)==diagonal]
            assert len(edges)==n
            literal[hi]+=frac(a[4]+a[5],whole)
            pair[hi]+=frac(a[4]+a[5],whole)+F(a[4],D)
            for i,j in edges:
                key=(family,diagonal,words[i],words[j]);states=h['groups'][key]
                q=a[5] if cut['q']=='actual5' else words[j][1]
                assert cut['q'] in ('actual5','wj1')
                v0,_=endpoint(a,0,q);v1,_=endpoint(a,1,q)
                literal[hi]-=v0/n
                pair[hi]-=F(q,n*(b+1))
                one=sum(value for state,(_,value) in states.items() if state[1])
                for state,(col,value) in states.items():
                    if state[1]:
                        literal[col]-=(v1-v0)/n
                        pair[col]-=(F(1,b+1)-F(q,D))/n
                state_masses[b,ell,0,q]+=(H-one)/n
                state_masses[b,ell,1,q]+=one/n
            relevant=[hi]+[j for states in h['groups'].values() for j,_ in states.values()]
            contributions.append({'hist_column':hi,'value':str(sum(pair[j]*weights[j] for j in relevant))})
        state_masses={k:v for k,v in state_masses.items() if v}
        assert literal==pair==[F(v) for v in expected['coefficients']]
        value=sum(v*w for v,w in zip(pair,weights))
        assert value==F(cut['slack'])==F(expected['row_value'])<0
        assert str(u5)==expected['u_source'] and str(u6)==expected['u6']
        assert sum(state_masses.values())==1 and len(state_masses)==expected['state_count']
        expected_states={(s['b'],s['ell'],s['t'],s['q_count']):F(s['mass']) for s in expected['states']}
        assert state_masses==expected_states
        assert all(pair[j]==0 for j,c in enumerate(cols) if c['kind'] in ('K','overlap'))
        rows.append(pair)
        records.append({'number':number,'cut':cut,'mixed_key':mixed,'normalization_divisor':n,
                        'value':str(value),'raw_mixed_row_value':str(n*value),
                        'nonzero_coefficients':sum(v!=0 for v in pair),'coefficients':[str(v) for v in pair],
                        'state_masses':[{'state':k,'mass':str(v)} for k,v in sorted(state_masses.items())],
                        'histogram_contributions':contributions})
    assert len({tuple(row) for row in rows})==4
    best_value,best_cut=data['best_float']
    assert {k:best_cut[k] for k in ('i','member','orb','q')}=={k:data['selected'][0][k] for k in ('i','member','orb','q')}
    assert best_cut['float_alpha']==best_cut['float_gamma']==1.0
    best_discrepancy=abs(best_value-float(F(data['selected'][0]['slack'])))
    assert best_discrepancy < 1e-14
    comparisons=[]
    for relative in ['archives/customer-attraction/tools/evidence/all-reply-actual-floors-program/related/all_reply_floors_exact.json',
                     'archives/customer-attraction/tools/evidence/mixed-pair-reply-necessary-point/original/all_reply_mixed_pair_exact.json']:
        path=args.repo/relative;q=json.loads(path.read_text());qc=q['columns']
        assert len(qc)==1905
        assert all({k:v for k,v in x.items() if k!='weight'}=={k:v for k,v in y.items() if k!='weight'} for x,y in zip(cols,qc))
        changed=[j for j,(x,y) in enumerate(zip(cols,qc)) if F(x['weight'])!=F(y['weight'])]
        comparisons.append({'path':relative,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                            'same_nonweight_descriptors':True,'same_W':W==F(q['W']),
                            'changed_coordinates':len(changed),'changed_by_kind':dict(Counter(cols[j]['kind'] for j in changed)),
                            'changed_indices':changed,
                            'four_cut_values':[str(sum(v*F(c['weight']) for v,c in zip(row,qc))) for row in rows]})
    report={'status':'PASS-independent-four-selected-cuts','primary_sha256':hashlib.sha256(args.cuts.read_bytes()).hexdigest(),
            'source_point_sha256':data['source_sha256'],'all_primary_fields':data,
            'source_point_metadata':{k:v for k,v in point.items() if k!='columns'},
            'column_counts':dict(kinds),'positive_columns':169,'histograms':16,
            'positive_histograms':sum(F(h['column']['weight'])>0 for h in hs.values()),
            'groups':194,'implicit_00_checks':194,'u5':str(u5),'u6':str(u6),'O':str(O),'W':str(W),
            'histogram_descriptors':[{'column':hi,**h['column']} for hi,h in hs.items()],
            'complete_four_state_input':group_read,'endpoint_cases':endpoint_cases,
            'original_function_output_sha256':hashlib.sha256(args.author_functions.read_bytes()).hexdigest(),
            'original_coefficient_comparisons':4*1905,'distinct_vectors':4,
            'best_float_to_first_exact_absolute_difference':best_discrepancy,
            'records':records,'other_point_comparisons':comparisons,
            'new_original_function_calls':0,'main_calls':0,'discover_calls':0,'LP_calls':0,
            'scope':'Four exact selected rows, their mean-normalized strongPAIR identity and one source point; not all 216 LP discovery directions or whole 5287 graph.'}
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'endpoint_cases':endpoint_cases,'coefficient_comparisons':4*1905,
                      'groups':194,'distinct_vectors':4,'best_float_difference':best_discrepancy,
                      'comparisons':[{k:v for k,v in c.items() if k not in ('changed_indices',)} for c in comparisons]},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
