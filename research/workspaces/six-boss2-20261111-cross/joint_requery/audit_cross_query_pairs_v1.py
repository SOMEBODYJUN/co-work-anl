"""Exact audits of the new old-query coupling coordinates, no master mutation.

The expected overlaps are obtained by literal ordered old-index sums, without
using the moment formulas under audit. Existing 332-row evidence embeds by
zeroing the 284 newly introduced weights.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib,json,time
import cross_query_pairs_v1 as new
import portfolio_master as old
from separate_master import blocks_from_columns,div

HERE=Path(__file__).resolve().parent


def literal_query(a,words,left,right,r,z,qi):
    if qi<6:return [(F(1),a[qi])]
    if qi<9:return [(F(1),words[left][qi-6])]
    if qi<12:return [(F(1),words[right][qi-9])]
    if qi<14:return [(F(1),(r,z)[qi-12])]
    rest=[i for i in range(6) if i not in {left,right}]
    return [(F(1,len(rest)),words[i][qi-14]) for i in rest]


def literal_pair(a,words,left,right,r,z,config):
    ql,qr,mode=config
    ml=literal_query(a,words,left,right,r,z,ql)
    mr=literal_query(a,words,left,right,r,z,qr)
    if mode=='product':
        return tuple((wl*wr,x,y) for wl,x in ml for wr,y in mr)
    rest=[i for i in range(6) if i not in {left,right}];d=len(rest)
    if mode=='same':
        return tuple((F(1,d),words[i][ql-14],words[i][qr-14]) for i in rest)
    return tuple((F(1,d*(d-1)),words[i][ql-14],words[j][qr-14]) for i in rest for j in rest if i!=j)


def main():
    start=time.monotonic()
    source=HERE.parent/'master_cuts/dynamic_5752_exact.json'
    raw=source.read_bytes();data=json.loads(raw);blocks=blocks_from_columns(data['columns'])
    pair_checks=0;formula_checks=0;seen=set();gap_checks=0
    for block in blocks:
        a,words=block['a'],block['words']
        for left in range(6):
            for right in range(6):
                d=5 if left==right else 4
                for r,z in product((0,1),repeat=2):
                    qs,mu=new.queries_and_moments(a,words,left,right,r,z)
                    key=(qs,mu,d)
                    if key in seen:continue
                    seen.add(key)
                    values=new.pair_values(qs,mu,d)
                    for config,(sm,rho) in zip(new.PAIR_CONFIGS,values):
                        pairs=literal_pair(a,words,left,right,r,z,config)
                        assert sum(w for w,x,y in pairs)==1
                        assert sum(w*(x+y) for w,x,y in pairs)==sm
                        assert sum(w*x*y for w,x,y in pairs)==rho
                        pair_checks+=1
                        # The difference from half the two old same-query
                        # diagonals is the exact disagreement premium.
                        assert (sm/2-rho)==sum(w*(x-y)**2 for w,x,y in pairs)/2
                        gap_checks+=1
                    # All possible beta values in six-player complete histories;
                    # exact strongPAIR averaging checks each endpoint membership.
                    for bg in range(6):
                        D=(bg+1)*(bg+2)
                        for fst,last in product((0,1),repeat=2):
                            coefficient=(F(1,bg+1),-F(1,D),-F(fst,D)-div(fst+last,bg+fst+last))
                            # Every coupling has the same affine coefficients;
                            # check the full menu on the first 24 visible types,
                            # plus every coefficient/atom pattern exhaustively.
                            if len(seen)<=24:
                                for config,(sm,rho) in zip(new.PAIR_CONFIGS,values):
                                    pairs=literal_pair(a,words,left,right,r,z,config)
                                    direct=sum(w*(F(x+y,bg+1)-F(x*y+fst,D)-div(fst+last,bg+fst+last)) for w,x,y in pairs)
                                    assert direct==coefficient[0]*sm+coefficient[1]*rho+coefficient[2]
                                    formula_checks+=1
    compressed_checks=0
    for k in range(3,7):
        for p in range(7-k):
            for t in (0,1):
                for hidden,co in zip(new.hidden_configs(k),new.hidden_pair_coefficients(p,t,k)):
                    b,c,j,v,s,ss=hidden
                    for br,(bg,fst,last) in enumerate(((p+t+s,b,c),(p+c+ss,j,v))):
                        for x,y in product((0,1),repeat=2):
                            literal=F(x+y,bg+1)-F(x*y+fst,(bg+1)*(bg+2))-div(fst+last,bg+fst+last)
                            assert co[3*br]*(x+y)+co[3*br+1]*x*y+co[3*br+2]==literal
                            compressed_checks+=1
    # Equal first moments, genuinely different same/off second moments.
    a=(0,0,0,1,1,1);examples=[]
    for tail in (((0,0,0),(0,0,0),(1,1,0),(1,1,0)),((1,0,0),(1,0,0),(0,1,0),(0,1,0))):
        words=((0,0,0),(0,0,0))+tail
        qs,mu=new.queries_and_moments(a,words,0,1,0,1)
        vals=dict(zip(new.PAIR_CONFIGS,new.pair_values(qs,mu,4)))
        examples.append({'q':list(map(str,qs)),'mu':list(map(str,mu)),'same_TB':str(vals[14,15,'same'][1]),'off_TB':str(vals[14,15,'off'][1])})
    assert examples[0]['q']==examples[1]['q'] and examples[0]['mu']!=examples[1]['mu']
    # Full 4849-coordinate old-cone embedding, including all four R/Z states.
    pack_raw=(HERE/'portfolio_selected_5752.json').read_bytes();pack=json.loads(pack_raw)
    embeddings=[]
    selected=[]
    for cut in pack['cuts']:
        tag=(cut['i'],tuple(cut['orb']))
        if tag not in [x[0] for x in selected]:selected.append((tag,cut))
    for tag,cut in selected:
        theta={n:F(w) for n,w in cut['weights'].items()}
        row,au,aK,psi=new.make_row(data['columns'],blocks,cut['member'],tuple(cut['orb']),cut['i'],theta)
        expected=[F(0)]*len(row)
        for i,v in cut['sparse_row']:expected[i]=F(v)
        assert row==expected
        visible=new.visible_distribution(blocks,cut['member'],tuple(cut['orb']),cut['i'])
        direct=sum(F(c['weight'])*v for c,v in zip(data['columns'],row))
        assert direct==F(cut['exact_slack'])
        oldvis=old.visible_distribution(blocks,cut['member'],tuple(cut['orb']),cut['i'])
        from collections import defaultdict
        coarsened=defaultdict(F)
        for p,ell,t,qs,mu,mass in visible:coarsened[p,ell,t,qs]+=mass
        assert dict(coarsened)=={(p,ell,t,qs):mass for p,ell,t,qs,mass in oldvis}
        embeddings.append({'i':cut['i'],'member':cut['member'],'orb':cut['orb'],'exact_slack':str(direct),'coordinates':len(row),'row_sha256':cut['row_sha256']})
    out={'result':'PASS','source_sha256':hashlib.sha256(raw).hexdigest(),'old_pack_sha256':hashlib.sha256(pack_raw).hexdigest(),'feature_count':len(new.NAMES),'new_pairs_per_branch':len(new.PAIR_CONFIGS),'distinct_visible_query_types':len(seen),'literal_overlap_checks':pair_checks,'literal_pair_average_checks':formula_checks,'disagreement_identity_checks':gap_checks,'compressed_hidden_formula_checks':compressed_checks,'moment_counterexample':examples,'old_332_embeddings':embeddings,'elapsed_seconds':time.monotonic()-start}
    target=HERE/'cross_query_pairs_v1_audit.json';target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(out,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
