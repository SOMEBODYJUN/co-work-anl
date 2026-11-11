"""Exact-row separation of a fixed master point by shared-C + cross-PAIR.

Discovery uses scipy LP. Every returned cut is rebuilt with Fraction over all
six actual indices and all sixteen shared hidden states, then exactly dotted
against the SHA-bound input. No mutation of the master or original evidence.
"""
from fractions import Fraction as F
from itertools import product
from collections import Counter,defaultdict
from pathlib import Path
from functools import lru_cache
import hashlib,json,sys,time
from explore_projection import features,solve,BASE_NAMES,ALL_NAMES,div,hidden_configs

HERE=Path(__file__).resolve().parent
WORDS=tuple(product((0,1),repeat=3))
ORBITS=((0,0),(1,0),(1,1))


def blocks_from_columns(columns):
    blocks=[];current=None
    for ci,c in enumerate(columns):
        if c['kind']=='hist':
            a=tuple(map(int,c['actual_bits']))
            words=tuple(w for w,n in zip(WORDS,c['hist']) for _ in range(n))
            assert len(words)==6
            current={'ci':ci,'a':a,'words':words,'column':c,'joint':[]}
            blocks.append(current)
        elif c['kind']=='joint-reply':
            current['joint'].append((ci,c))
    assert len(blocks)==16
    return blocks


def query(a,words,left,right,t,qindex):
    other=[i for i in range(6) if i not in {left,right}]
    qs=a+words[left]+words[right]+(t,)+tuple(F(sum(words[i][j] for i in other),len(other)) for j in range(3))
    return F(qs[qindex])


def visible_distribution(blocks,member,orb,qi,source_index=3):
    out=defaultdict(F)
    family,diag=orb
    ct=6 if diag else 30
    for block in blocks:
        mass=F(block['column']['weight']);a=block['a'];words=block['words']
        one=defaultdict(F)
        for ci,col in block['joint']:
            ff,dd,wi,wj=col['group']
            if (ff,dd)==orb and col['state'][member]:one[(tuple(wi),tuple(wj))]+=F(col['weight'])
        for left in range(6):
            for right in range(6):
                if (left==right)!=bool(diag):continue
                tmass=one[(words[left],words[right])]
                assert 0<=tmass<=mass
                for t,w in ((0,mass-tmass),(1,tmass)):
                    if w:
                        state=(sum(a[:source_index]),sum(a[:5]),t,query(a,words,left,right,t,qi))
                        out[state]+=w/ct
    return [(*state,w) for state,w in sorted(out.items()) if w]


def exact_weights(res,names,denmax):
    weights={n:F(float(-v)).limit_denominator(denmax) for n,v in zip(names,res.ineqlin.marginals) if v < -1e-8}
    total=weights.get('sourceT',F(0))+weights.get('sourceC',F(0))
    if not total:return None
    return {n:w/total for n,w in weights.items() if w}


def make_row(columns,blocks,member,orb,qi,theta,source_index=3):
    k=6-source_index
    @lru_cache(None)
    def psi(p,ell,t,q):
        return min(sum((w*features(p,ell,t,q,*h,k)[0][n] for n,w in theta.items()),F(0)) for h in hidden_configs(k))
    _,bud=features(0,0,0,0,0,0,0,0,0,0,k)
    a_u=sum(w*bud[n][1] for n,w in theta.items())
    a_K=sum(w*bud[n][2] for n,w in theta.items())
    assert theta.get('sourceT',0)+theta.get('sourceC',0)==1
    row=[F(0)]*len(columns);row[0]=a_K
    family,diag=orb;ct=6 if diag else 30
    for block in blocks:
        a,words=block['a'],block['words'];p,ell=sum(a[:source_index]),sum(a[:5])
        baseline=F(0);deltas=defaultdict(F)
        for left in range(6):
            for right in range(6):
                if (left==right)!=bool(diag):continue
                vals=[psi(p,ell,t,query(a,words,left,right,t,qi)) for t in (0,1)]
                baseline+=vals[0]/ct
                deltas[(family,diag,words[left],words[right])]+=(vals[1]-vals[0])/ct
        row[block['ci']]=div(a[source_index],sum(a))+a_u*div(a[5],sum(a))-baseline
        for ci,col in block['joint']:
            ff,dd,wi,wj=col['group']
            if (ff,dd)==orb and col['state'][member]:
                row[ci]=-deltas[(ff,dd,tuple(wi),tuple(wj))]
    return row,a_u,a_K,psi


def main():
    started=time.monotonic()
    source=Path(sys.argv[1]) if len(sys.argv)>1 else HERE.parent/'master_cuts/merged_5716_exact.json'
    raw=source.read_bytes();data=json.loads(raw);columns=data['columns'];blocks=blocks_from_columns(columns)
    actual=[sum(F(b['column']['weight'])*div(b['a'][i],sum(b['a'])) for b in blocks) for i in range(6)]
    K=F(columns[0]['weight']);u=actual[5]
    out={'scope':'Fixed-point exact necessary-cut separation only; no SPE or half certificate.','source_path':str(source),'source_sha256':hashlib.sha256(raw).hexdigest(),'columns':len(columns),'u4':str(actual[3]),'u6':str(u),'actual_utilities':list(map(str,actual)),'K':str(K),'cuts':[],'scans':[]}
    target=HERE/f"master_{data.get('verified_rows','point')}_separation.json"
    sources=tuple(map(int,sys.argv[2].split(','))) if len(sys.argv)>2 else (3,)
    for source_index in sources:
        assert source_index in range(4)
        k=6-source_index;r=actual[source_index]
        for member in (0,1):
            for orb in ORBITS:
                for qi in range(16):
                    visible=visible_distribution(blocks,member,orb,qi,source_index)
                    res,_,names=solve(visible,u,K,ALL_NAMES,k)
                    scan={'i':source_index,'k':k,'member':member,'orb':orb,'query':qi,'visible_states':len(visible),'success':bool(res.success),'message':res.message}
                    if res.success:
                        scan['minimum_r_float']=res.fun;scan['gap_float']=res.fun-float(r)
                    out['scans'].append(scan)
                    if not res.success or res.fun<float(r)+1e-9:continue
                    for denmax in (1000,10000,100000,1000000,10000000):
                        theta=exact_weights(res,names,denmax)
                        if theta is None:continue
                        row,au,aK,psi=make_row(columns,blocks,member,orb,qi,theta,source_index)
                        slack=sum((F(col['weight'])*value for col,value in zip(columns,row)),F(0))
                        if slack<0:
                            direct=r+au*u+aK*K-sum(w*psi(p,ell,t,q) for p,ell,t,q,w in visible)
                            assert direct==slack
                            cut={'i':source_index,'k':k,'member':member,'orb':orb,'query':qi,'weights':{n:str(w) for n,w in theta.items()},'source_weight_sum':'1','u6_coefficient':str(au),'K_coefficient':str(aK),'exact_slack':str(slack),'slack_float':float(slack),'uses_new_PAIR':any(n.startswith('pair') for n in theta),'denominator_limit':denmax,'sparse_row':[[i,str(x)] for i,x in enumerate(row) if x], 'row_sha256':hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest(),'visible':[{'state':[p,ell,t,str(q)],'mass':str(w),'minimum':str(psi(p,ell,t,q))} for p,ell,t,q,w in visible]}
                            out['cuts'].append(cut)
                            target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
                            print(json.dumps({key:cut[key] for key in ('i','k','member','orb','query','slack_float','uses_new_PAIR','u6_coefficient','K_coefficient')},ensure_ascii=False),flush=True)
                            break
                out['elapsed_seconds']=time.monotonic()-started
                target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
        features.cache_clear()
    out['elapsed_seconds']=time.monotonic()-started
    target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'done':True,'scans':len(out['scans']),'cuts':len(out['cuts']),'new_PAIR_cuts':sum(c['uses_new_PAIR'] for c in out['cuts']),'elapsed':out['elapsed_seconds']},ensure_ascii=False))


if __name__=='__main__':main()
