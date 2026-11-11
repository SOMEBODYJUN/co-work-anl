"""Independent literal verification of the new E/B4 zero-face diagnostic.

No constructor or solver import.  Reads exact point/E data independently,
uses EB3 for the upper bound, and computes query income from all saved
literal (Z,E,H1) transport cells at both zero faces.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip
import json

HERE=Path(__file__).resolve().parent
POINT=HERE.parent/'full624_augmented_lp/recovery/augmented_lp_exact.json'

def sha(p):return sha256(p.read_bytes()).hexdigest()
def share(n,d):
    if not d:assert not n;return F()
    return F(n,d)

def main():
    diagnostic=json.loads((HERE/'conditional_B4_diagnostic.json').read_bytes())
    point=json.loads(POINT.read_bytes());cert=json.loads((HERE/'exact_certificate.json').read_bytes())
    desc=json.loads(gzip.decompress((HERE/'symbolic_lift.json.gz').read_bytes()))['new_columns'][:776]
    assert diagnostic['point_sha256']==sha(POINT)
    assert diagnostic['E_certificate_sha256']==sha(HERE/'exact_certificate.json')
    assert diagnostic['source_sha256']==sha(HERE/'conditional_B4.py')
    hist={};old=defaultdict(dict);eta=defaultdict(dict);xe=defaultdict(dict)
    for j,c in enumerate(point['columns'][:4849]):
        if c['kind']=='hist':h=j;hist[h]=c
        elif c['kind']=='joint-reply':
            f,d,wi,wj=c['group'];g=f,d,tuple(wi),tuple(wj)
            old[h,g][tuple(c['state'])]=F(c['weight'])
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            eta[c['hist_column']][tuple(c['hidden'])+(c['ell']//6,)]=F(c['weight'])
    for c,v in zip(desc,cert['E_values']):
        f,d,wi,wj=c['group'];g=f,d,tuple(wi),tuple(wj)
        xe[c['hist_column'],g][tuple(c['old_state'])]=F(v)
    income=F()
    for h,c in hist.items():
        a=tuple(map(int,c['actual_bits']));background=sum(a[:3])+a[5]
        for (h1,h2,y),v in eta[h].items():income+=v*share(h2,background+h1+h2)
    assert str(income)==diagnostic['true_H2_income']
    rows=[];cell_count=0;block_count=0
    for saved in diagnostic['rows']:
        f,diag=saved['orbit'];nodes=[(f,i,j) for i in range(6) for j in range(6) if int(i==j)==diag]
        assert len(nodes)==saved['nodes']
        assert {(b['hist'],tuple(b['node'])) for b in saved['blocks']}=={(h,e) for h in hist for e in nodes}
        oldupper=income;plain=income;literal=income;strict=0
        for block in saved['blocks']:
            h=block['hist'];f,i,j=block['node'];c=hist[h]
            words=[w for w,n in zip(product((0,1),repeat=3),c['hist']) for _ in range(n)]
            g=f,int(i==j),words[i],words[j]
            ss=old[h,g];E=xe[h,g];H=F(c['weight'])
            z=ss[0,1]+ss[1,1];e=sum(E.values(),F());k=E[0,1]+E[1,1]
            high=sum((mass*h1 for (h1,h2,y),mass in eta[h].items()),F())
            a=tuple(map(int,c['actual_bits']));background=sum(a[:3])+a[5];d=background+1
            assert [str(H),str(z),str(e),str(k),str(high)]==[block[t] for t in ('H','Z','E','EZ','H1')]
            oldupper-=F(1,len(nodes))*(z/d-min(z,high)/F(d*(d+1)))
            plain-=F(1,len(nodes))*(e/d-min(e,high)/F(d*(d+1)))
            if saved['saturation_certified']:
                bystate={}
                for Z in (0,1):
                    layer=list(map(F,block['layer'+str(Z)]))
                    for (eb,hb),mass in zip(product((0,1),repeat=2),layer):
                        assert mass>=0;bystate[Z,eb,hb]=mass;cell_count+=1
                assert sum(bystate.values(),F())==H
                marg=lambda fn:sum((mass for s,mass in bystate.items() if fn(*s)),F())
                assert (marg(lambda Z,E,H1:Z),marg(lambda Z,E,H1:E),marg(lambda Z,E,H1:H1),
                        marg(lambda Z,E,H1:Z and E),marg(lambda Z,E,H1:Z and H1))==(z,e,high,k,min(z,high))
                maximum=min(e,high,k+max(high-z,F()))
                assert marg(lambda Z,E,H1:E and H1)==maximum==F(block['nested_overlap'])
                # Literal terminal price, using each H1 bit in the actual B4 prefix.
                query=sum((mass*share(eb,background+hb+eb) for (Z,eb,hb),mass in bystate.items()),F())
                literal-=query/len(nodes)
                strict+=maximum<min(e,high);block_count+=1
            else:
                assert block['forced_ZH1'] is None and block['nested_overlap'] is None
        assert str(oldupper)==saved['old_H2_to_Z_upper']
        assert str(plain)==saved['plain_H2_to_E_upper']
        if saved['saturation_certified']:
            assert oldupper==0 and str(literal)==saved['conditional_H2_to_E_upper']
            assert plain-literal==F(saved['improvement']) and strict==saved['strict_blocks']
            rows.append({'orbit':saved['orbit'],'conditional_value':str(literal),'conditional_float':float(literal),
                         'plain_value':str(plain),'improvement':str(plain-literal),'strict_blocks':strict})
        else:assert oldupper>0 and saved['conditional_H2_to_E_upper'] is None
    assert block_count==960 and cell_count==7680 and len(rows)==2
    report={'scope':'Independent exact literal audit of one conditional B4 diagnostic on the new E certificate; not a universal old-column cut.',
            'point_sha256':sha(POINT),'E_certificate_sha256':sha(HERE/'exact_certificate.json'),
            'diagnostic_sha256':sha(HERE/'conditional_B4_diagnostic.json'),
            'verifier_sha256':sha(Path(__file__)),'histograms':len(hist),
            'all_66_nodes_and_16_histograms_checked':True,'zero_face_blocks_checked':block_count,
            'literal_transport_cells_checked':cell_count,'rows':rows,
            'negative_conditional_rows':sum(F(r['conditional_value'])<0 for r in rows),
            'optimization_calls':0,'passed':True}
    (HERE/'conditional_B4_independent_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
