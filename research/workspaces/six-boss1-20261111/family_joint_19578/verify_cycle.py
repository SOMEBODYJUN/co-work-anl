"""Independent exact verifier for the general fourteen-query cyclic domain.

No constructor or optimization module is imported. Old-word orbit weights
are reconstructed from all 720 simultaneous label permutations, and costs
are evaluated directly from actual and hidden membership bits.
"""
from collections import Counter,defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations,product
from pathlib import Path
import argparse,json

def sha(path):return sha256(path.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--point',type=Path,required=True)
    ap.add_argument('--witness',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    point=json.loads(args.point.read_bytes());w=json.loads(args.witness.read_bytes())
    assert w['input_sha256']==sha(args.point)and w['exact_feasible']
    cols=point['columns'][:4849];mass=[F(c['weight'])for c in cols]
    hist={j:c for j,c in enumerate(cols)if c['kind']=='hist'}
    own=defaultdict(dict);h=None;family=defaultdict(dict)
    for j,c in enumerate(cols):
        if c['kind']=='hist':h=j
        elif c['kind']=='joint-reply':
            f,d,a,b=c['group'];g=f,d,tuple(a),tuple(b)
            own[h].setdefault(g,{})[tuple(c['state'])]=mass[j]
        elif c['kind']=='actual-B-family-state'and c['source']==4:
            family[c['hist_column']][j]=c
    for h in hist:
        assert sum((mass[j]for j in family[h]),F())==mass[h]
        assert len(family[h])==8
        for g,states in own[h].items():
            states[0,0]=mass[h]-sum(states.values(),F())
            assert set(states)==set(product((0,1),repeat=2))and min(states.values())>=0
    expected={};permutation_checks=0
    for h,c in hist.items():
        base=tuple(t for t,n in zip(product((0,1),repeat=3),c['hist'])for _ in range(n))
        counts=Counter()
        for pi in permutations(range(6)):
            moved=[None]*6
            for i in range(6):moved[pi[i]]=base[i]
            counts[moved[0],moved[1],moved[2]]+=1
            permutation_checks+=1
        assert sum(counts.values())==720 and all(n%6==0 for n in counts.values())
        for triple,n in counts.items():expected[h,triple]=n
    seen=set();costs=[F()for _ in range(14)];ue=F();uf=F();pair_min=F()
    marg_checks=0;positive_flow=0;zero_hist_blocks=0
    for block in w['blocks']:
        h=block['hist_column'];triple=tuple(tuple(x)for x in block['old_words']);key=h,triple
        assert key in expected and key not in seen;seen.add(key)
        assert block['multiplicity']*6==expected[key]
        omega=F(expected[key],720)
        wi,wj,wk=triple;ge=(0,0,wi,wj);gf=(1,0,wi,wk)
        assert block['e_group']==[0,0,list(wi),list(wj)]
        assert block['f_group']==[1,0,list(wi),list(wk)]
        re={s:F()for s in product((0,1),repeat=2)};rf=dict(re);ss={j:F()for j in family[h]}
        P=sum(map(int,hist[h]['actual_bits'][:4]));actual=tuple(map(int,hist[h]['actual_bits']))
        ue+=omega*sum((v*F(z,P+r+1)for(r,z),v in own[h][ge].items()),F())
        uf+=omega*sum((v*F(z,P+r+1)for(r,z),v in own[h][gf].items()),F())
        q=sum(v for(r,z),v in own[h][ge].items()if r);v=sum(v for(r,z),v in own[h][gf].items()if z)
        pair_min+=omega*(v/F(P+1)-min(q,v)/F((P+1)*(P+2)))
        distinct=set()
        for entry in block['positive_flow']:
            e=tuple(entry['e_state']);f=tuple(entry['f_state']);j=entry['family_state_column'];m=F(entry['mass'])
            assert e in re and f in rf and j in ss and m>0 and(e,f,j)not in distinct
            distinct.add((e,f,j));re[e]+=m;rf[f]+=m;ss[j]+=m;positive_flow+=1
            c=family[h][j];s=actual[:3]+(actual[5],)+tuple(c['hidden'])
            den=sum(s[:-1])+1;xe,ze=e;xf,zf=f
            xm=tuple(c['hidden'])+(F(c['ell'],6),)
            raw=[F(xe,den),F(ze,den),F(xf,den),F(zf,den)]
            raw += [F(x)/(P+xe+1)for x in xm]
            raw += [F(x)/(P+xf+1)for x in xm]
            raw += [F(xf,P+xe+1),F(zf,P+xe+1),F(xe,P+xf+1),F(ze,P+xf+1)]
            for k,cost in enumerate(raw):costs[k]+=omega*m*cost
        assert re==own[h][ge]and rf==own[h][gf]
        assert ss=={j:mass[j]for j in family[h]}
        marg_checks+=16
        zero_hist_blocks+=not mass[h]
    assert seen==set(expected)
    U=F()
    for h,states in family.items():
        actual=tuple(map(int,hist[h]['actual_bits']))
        for j,c in states.items():
            s=actual[:3]+(actual[5],)+tuple(c['hidden'])
            U+=mass[j]*F(s[-1],sum(s[:-1])+1)
    budgets=[U]*4+[ue]*3+[uf]*3+[ue]*2+[uf]*2
    records=[]
    assert len(w['queries'])==14
    for k,(b,c,old)in enumerate(zip(budgets,costs,w['queries'])):
        value=b-c
        assert b==F(old['budget'])and c==F(old['cost'])and value==F(old['slack'])and value>=0
        records.append({'query':old['query'],'budget':str(b),'cost':str(c),'slack':str(value)})
    result={'scope':'independent exact verification of the fourteen-query cyclic marginal domain only; no global 66-node gluing claim',
            'input_sha256':sha(args.point),'witness_sha256':sha(args.witness),'verifier_sha256':sha(Path(__file__)),
            'all_marginals_exact':True,'all_queries_nonnegative':True,'blocks':len(seen),
            'full_finite_cells':128*len(seen),'marginal_equalities':marg_checks,'zero_hist_blocks':zero_hist_blocks,
            'positive_flow_entries':positive_flow,'explicit_synchronized_permutation_checks':permutation_checks,
            'query_count':14,'positive_queries':sum(F(q['slack'])>0 for q in records),
            'zero_queries':sum(F(q['slack'])==0 for q in records),'minimum_slack':str(min(b-c for b,c in zip(budgets,costs))),
            'Ze_to_Zf_single_query_exact_maximum_slack':str(ue-pair_min),'queries':records}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print({k:v for k,v in result.items()if k not in('queries','minimum_slack')})

if __name__=='__main__':main()
