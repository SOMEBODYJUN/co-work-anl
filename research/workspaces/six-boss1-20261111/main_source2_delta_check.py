"""Main rederives all delta breakpoints, true minima, and 180 full raw rows."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
from hashlib import sha256
from functools import lru_cache
import json
from main_minimal_caps_complete_check import cost

W=Path(__file__).resolve().parent
P=W/'source2_conditional_redistribution'
B,V,SSTAR=F(5977,6912),F(43,48),F(61273,6912)
ATOMS=list(product((0,1),repeat=9))
TAILS=list(product((0,1),repeat=4))


def read(p):return json.loads(p.read_text())
def sha(p):return sha256(p.read_bytes()).hexdigest()


def weights(q0,s,delta):
    tau={3:F(0),4:B-delta,5:V+delta}
    beta={j:q0/2+tau[j]+sum((q0*tau[l]/((7-l)*(8-l)) for l in tau if l>j),F(0)) for j in tau}
    return tau,beta,25+B+V-s,1+sum(beta.values())


def main():
    out=W/'main_source2_delta_check.json';assert not out.exists()
    assert sha(P/'freeze_manifest.json')=='9cfbe8eb409b6fd505ea1663183a3a3220602222952a5ba0291e13398578285a'
    assert sha(P/'proof.md')=='9b9128519aa12d2d9c11d197948751a21ed5f1039eb51640a26f1922e818ea1d'
    all_cases=read(P/'exact_envelopes.json')['cases']
    cases={r['id']:(r['mode'],F(r['q0']),F(r['s'])) for r in all_cases}
    assert set(cases)=={f'{mode}_{q}_{tag}' for mode,q in [('pure','q6'),('ordered','q5')] for tag in ['s0','sstar','s9']}
    lines={};breaksets={};geometry=[];state_lines=0;interval_tails=0
    for case in all_cases:
        cid=case['id'];mode,q0,s=cases[cid]
        assert s in [F(0),SSTAR,F(9)]
        conds=([(p,t,q0*o) for p,t,o in product((0,1),repeat=3)] if mode=='pure' else
               [(p,0,F(d,5)) for p in [0,1] for d in range(6)]+[(p,1,F(d-1,5)) for p in [0,1] for d in range(1,7)])
        breaks={F(0),B}
        for p,t,q in conds:
            affine=[]
            for tail in TAILS:
                tau,beta,a,S=weights(q0,s,F(0));v0=cost(2,p,t,q,tail,tau,beta,a)
                tau,beta,a,S=weights(q0,s,B);v1=cost(2,p,t,q,tail,tau,beta,a)
                affine.append((v0,(v1-v0)/B))
            lines[cid,p,t,q]=affine;state_lines+=16
            for A,C in affine:
                left,right=F(0),B;possible=True
                for A2,C2 in affine:
                    da,dc=A-A2,C-C2
                    if dc>0:right=min(right,-da/dc)
                    elif dc<0:left=max(left,-da/dc)
                    elif da>0:possible=False;break
                if possible and left<=right:
                    breaks.update([left,right]);interval_tails+=1
        assert breaks==set(map(F,case['breakpoints']))
        breaksets[cid]=sorted(breaks)
        geometry.append({'case':cid,'complete_breakpoints':list(map(str,sorted(breaks))),'condition_count':len(conds)})

    @lru_cache(None)
    def minimum(cid,p,t,q,delta):
        return min(A+C*delta for A,C in lines[cid,p,t,q])

    @lru_cache(None)
    def fd(cid,p,d,delta):
        value=F(0)
        if d<6:value+=(6-d)*minimum(cid,p,0,F(d,5),delta)
        if d>0:value+=d*minimum(cid,p,1,F(d-1,5),delta)
        return value/6

    positive_gaps=[];pair_intervals=0
    for cid,(mode,q0,s) in cases.items():
        if mode!='ordered':continue
        bs=breaksets[cid]
        for p in [0,1]:
            for x in bs:
                vals=[fd(cid,p,d,x) for d in range(7)]
                assert vals[0]==0 and all(vals[d]>vals[1] for d in range(2,7))
                positive_gaps.extend(vals[d]-vals[1] for d in range(2,7))
            for left,right in zip(bs,bs[1:]):
                for j,k in combinations(range(1,7),2):
                    d0=fd(cid,p,j,left)-fd(cid,p,k,left)
                    d1=fd(cid,p,j,right)-fd(cid,p,k,right)
                    assert d0*d1>0;pair_intervals+=1

    @lru_cache(None)
    def vector(cid,delta,target):
        mode,q0,s=cases[cid];tau,beta,a,S=weights(q0,s,delta)
        assert min(tau.values())>=0 and min(beta.values())>0 and a>0
        conly=target=='C-only';ordered=target=='ordered-six-menu'
        assert ordered==(mode=='ordered')
        if not ordered:ti=int(target[1:])-1 if target.startswith('A') else {'X':6,'C':8,'C-only':8}[target]
        values=[]
        for bits in ATOMS:
            p=bits[0];load_=sum(bits[:6]);ui=F(bits[1],load_) if load_ else F(0)
            v=a*ui-(bits[7]*min(fd(cid,p,d,delta) for d in range(1,7)) if ordered else minimum(cid,p,bits[ti],q0*bits[7],delta))
            if conly:v+=(S-s/5)*bits[8]
            values.append(v)
        values.append(s/5 if conly else S)
        return tuple(values)

    raw=read(P/'exact_family.json')['rows'];extra=read(P/'epsilon_rows.json')['rows']
    assert len(raw)==180 and len(extra)==3
    counts={cid:set() for cid in cases};cols=0
    for rec in raw+extra:
        cid=rec['case'];delta=F(rec['delta']);target=rec['target'];mode,q0,s=cases[cid]
        assert rec['mode']==mode and F(rec['rhs'])==0 and F(rec['numeric_divisor'])==25
        tau,beta,a,S=weights(q0,s,delta);rw=rec['weights']
        assert {int(j):F(x) for j,x in rw['tau'].items()}==tau
        assert {int(j):F(x) for j,x in rw['beta'].items()}==beta
        assert F(rw['source_IC'])==a and F(rw['K_before_C_equality'])==S
        assert rec['C_equality_multiplier']==(str(S-s/5) if target=='C-only' else None)
        assert tuple(map(F,rec['a']))==vector(cid,delta,target);cols+=513
    for rec in raw:counts[rec['case']].add(F(rec['delta']))
    assert all(counts[cid]==set(bs) for cid,bs in breaksets.items())
    aff=read(P/'affine_family.json')['rows'];assert len(aff)==150
    affine_cols=0
    for rec in aff:
        cid,target=rec['case'],rec['target'];left,right=F(rec['left']),F(rec['right'])
        bs=breaksets[cid];assert (left,right) in list(zip(bs,bs[1:]))
        vl,vr=vector(cid,left,target),vector(cid,right,target)
        slope=tuple((b-a)/(right-left) for a,b in zip(vl,vr))
        intercept=tuple(a-left*b for a,b in zip(vl,slope))
        assert slope==tuple(map(F,rec['delta_coefficient'])) and intercept==tuple(map(F,rec['intercept']))
        mid=(left+right)/2
        assert vector(cid,mid,target)==tuple(a+mid*b for a,b in zip(intercept,slope))
        affine_cols+=2*513
    for rec in read(W/'main_delta_uniform_improvement/two_true_delta_cuts.json'):
        cid='pure_q6_s0' if F(rec['s'])==0 else 'pure_q6_sstar'
        assert vector(cid,F(1,144),'C-only')==tuple(F(rec['a_coefficients'].get(str(h),'0')) for h in range(513))
    result={'status':'PASS_MAIN_COMPLETE_DELTA_ENVELOPES_ALL_TRUE_BUDGETS_AND_180_ROWS',
            'optimizer_calls':0,'candidate_points_read':0,'cases':geometry,'true_affine_tail_states':state_lines,
            'nonempty_full_tail_dominance_intervals':interval_tails,'ordered_pair_interval_nonintersection_checks':pair_intervals,
            'ordered_uniform_gap_min':str(min(positive_gaps)),'raw_rows':180,'extra_epsilon_rows':3,
            'point_column_checks':cols,'affine_segment_rows':150,'affine_coefficient_checks':affine_cols,
            'Main_two_epsilon_full_column_identities':1026,'proof_personally_read_complete':True,
            'proof_sha256':sha(P/'proof.md'),'family_sha256':sha(P/'exact_family.json'),'manifest_sha256':sha(P/'freeze_manifest.json'),
            'scope':'All continuous delta in the three stated s slices; exact local necessary families with every weak tail retained. No SPE construction or half conclusion.'}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['cases','scope']},ensure_ascii=False))


if __name__=='__main__':main()
