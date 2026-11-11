"""Exact forced overlap directions at the 19621 Ze-to-Zf saturated orbit.

This records the equality consequences of an exactly zero Frechet upper
bound. The saved local witness confirms the equality in every positive
block; necessity applies to any common realization of these margins and ICs.
"""
from collections import Counter,defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse,json

def sha(p):return sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--point',type=Path,required=True)
    ap.add_argument('--witness',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();p=json.loads(args.point.read_bytes());w=json.loads(args.witness.read_bytes())
    assert w['input_sha256']==sha(args.point)
    cols=p['columns'][:4849];mass=[Q(c['weight'])for c in cols]
    hist={j:c for j,c in enumerate(cols)if c['kind']=='hist'};own=defaultdict(dict);hi=None
    for j,c in enumerate(cols):
        if c['kind']=='hist':hi=j
        elif c['kind']=='joint-reply':
            f,d,wi,wj=c['group'];g=f,d,tuple(wi),tuple(wj)
            own[hi].setdefault(g,{})[tuple(c['state'])]=mass[j]
    records=[];counts=defaultdict(Counter);upper=Q();actual=Q()
    for b in w['blocks']:
        h=b['hist_column'];wi,wj,wk=map(tuple,b['old_words']);ge=(0,0,wi,wj);gf=(1,0,wi,wk)
        q=own[h][ge][1,0]+own[h][ge][1,1];v=own[h][gf][0,1]+own[h][gf][1,1]
        P=sum(map(int,hist[h]['actual_bits'][:4]));omega=Q(b['multiplicity'],120)
        uz=own[h][ge][0,1]/(P+1)+own[h][ge][1,1]/(P+2)
        overlap=sum((Q(e['mass'])for e in b['positive_flow']if e['e_state'][0]and e['f_state'][1]),Q())
        upper+=omega*(uz-v/(P+1)+min(q,v)/((P+1)*(P+2)))
        actual+=omega*(uz-v/(P+1)+overlap/((P+1)*(P+2)))
        if not mass[h]:continue
        assert overlap==min(q,v)
        direction='Re_subset_Zf'if q<v else'Zf_subset_Re'if v<q else'Re_equals_Zf'
        counts[h][direction]+=1
        records.append({'hist_column':h,'actual_bits':hist[h]['actual_bits'],'old_words':b['old_words'],
                        'multiplicity':b['multiplicity'],'e_group':b['e_group'],'f_group':b['f_group'],
                        'hist_mass':str(mass[h]),'R_e_mass':str(q),'Z_f_mass':str(v),
                        'intersection':str(overlap),'required_intersection':str(min(q,v)),
                        'forced_direction':direction})
    assert upper==actual==0
    result={'input_sha256':sha(args.point),'witness_sha256':sha(args.witness),'source_sha256':sha(Path(__file__)),
            'scope':'forced almost-sure implications in any S6-symmetrized common realization of the saved own margins and the complete literal ZZ IC orbit; conditional on hist and old-word triple',
            'orbit':{'kind':'Z-Z','class':[0,1,[0,1,0,2]],'e':[0,'i','j'],'f':[1,'i','k'],'indices':'i,j,k pairwise distinct','literal_queries':120},
            'exact_Frechet_upper_bound':'0','saved_local_witness_slack':'0','positive_blocks':len(records),
            'hist_summaries':[{'hist_column':h,'actual_bits':hist[h]['actual_bits'],'directions':dict(counts[h])}for h in sorted(counts)],
            'records':records,
            'caution':'the implications are necessary consistency restrictions, not a completed global implication graph or a full common measure'}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result['hist_summaries'],ensure_ascii=False))

if __name__=='__main__':main()
