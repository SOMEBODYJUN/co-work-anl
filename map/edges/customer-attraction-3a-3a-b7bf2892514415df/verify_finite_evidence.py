"""Current fixed-certificate reading, not a discovery or a general theorem test.

Reads the entire saved nine-label ordered policy; checks the complete key domain,
all prescribed and deviating continuations, and the four optimal query matrices.
Also independently recomputes every terminal table cell of the four tiny P0
interface examples.  It does not rerun the original discovery programs.
"""
from pathlib import Path
from functools import cache
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from collections import Counter
import json, hashlib, math

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).with_name('finite-evidence-check.json')
E=ROOT/'archives/customer-attraction/tools/evidence'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p,x):
    tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');tmp.replace(p)

def banks():
    folder=E/'six-optimal-query-decorrelation-primary/new-independent-audit/outputs'
    p=folder/'actual-banks.policy.json';raw=json.loads(p.read_text())
    policy={tuple(map(int,k.split(','))) if k else ():v for k,v in raw.items()}
    expected={h for d in range(6) for h in product(range(9),repeat=d)}
    assert len(raw)==len(policy)==len(expected)==66430 and set(policy)==expected
    assert all(isinstance(a,int) and 0<=a<9 for a in policy.values())
    types=list(zip([4,27,29,30,31,32,43,45,46,51,53,54,59],[1,4,3,3,2,1,3,3,3,3,3,3,2]))+[(1<<a,18)for a in (6,7,8)]
    units=[mask for mask,w in types for _ in range(w)];assert len(units)==88
    @cache
    def end(h):return h if len(h)==6 else end(h+(policy[h],))
    @cache
    def pay(z):
        # Independent expanded-unit evaluator, with 60 exactly clearing 1..6.
        c=Counter(z);u=[0]*9
        for mask in units:
            load=sum(n for a,n in c.items() if mask>>a&1)
            if load:
                assert 60%load==0
                for a in c:
                    if mask>>a&1:u[a]+=60//load
        return tuple(u)
    hist=checks=strict=tied=0
    for h,a in policy.items():
        hist+=1;v=pay(end(h))[a]
        for b in range(9):
            w=pay(end(h+(b,)))[b];assert v>=w,(h,a,b,v,w);checks+=1
            if b!=a:strict+=v>w;tied+=v==w
    actual=end(());assert actual==(6,7,8,0,3,4)
    def cover(t):return sum(any(mask>>a&1 for a in t)for mask in units)
    tuples=list(combinations_with_replacement(range(9),6));opt=max(map(cover,tuples));best=[t for t in tuples if cover(t)==opt]
    assert opt==88 and len(best)==4 and cover(actual)==86
    def U(a,tail):
        return sum((F(1,1+sum(mask>>b&1 for b in (6,7,8)+tuple(tail)))for mask in units if mask>>a&1),F(0))
    report=json.loads((folder/'independent-audit.payload.json').read_text())
    saved=next(x for x in report['cases'] if x['mode']=='actual-banks')
    queries=[]
    for t,q in zip(best,saved['queries']):
        pairs=[end((6,7,8,a))[4:]for a in t]
        matrix=[[U(a,pair)for pair in pairs]for a in t]
        diagonal=sum(matrix[j][j]for j in range(6))/6
        independent=sum((v for row in matrix for v in row),F(0))/36
        I=J=ret=F(0)
        for j,a in enumerate(t):
            B,C=pairs[j]
            for l,aa in enumerate(t):
                BB,CC=pairs[l];chat=policy[(6,7,8,a,BB)]
                ell1=U(B,(a,C))-U(BB,(a,chat));ell2=U(chat,(a,BB))-U(CC,(a,BB))
                assert ell1>=0 and ell2>=0
                I+=ell1;J+=ell2;ret+=U(C,(a,))-U(chat,(a,))
        I/=36;J/=36;ret/=36
        assert diagonal-independent==I+J+ret
        assert list(t)==q['tuple'] and [[str(v)for v in row]for row in matrix]==q['cross_query_matrix']
        assert [str(x)for x in [diagonal,independent,diagonal-independent,I,J,ret]]==[q[k]for k in ['diagonal_mean','independent_mean','Delta','first_successor_IC','cross_last_IC','deleted_middle_return']]
        queries.append(dict(tuple=t,D=str(diagonal),Q=str(independent),Delta=str(diagonal-independent),I=str(I),J=str(J),signed_return=str(ret)))
    assert (hist,checks,strict,tied)==(66430,597870,477287,54153)
    return dict(policy_path=str(p.relative_to(ROOT)),policy_sha256=digest(p),full_policy_keys=hist,all_actions_including_self=checks,nonself=checks-hist,strictly_losing=strict,tied=tied,actual=actual,W=86,OPT6=opt,multisets_checked=len(tuples),queries=queries,scope='This one saved policy, all ordered histories, all nine deviations; no original discovery or other policy replay.')

def tiny():
    p=E/'r70-potential-probe-program/new-interface-event/interface-audit.json';d=json.loads(p.read_text());out=[]
    for case in d['cases']:
        m,k=case['m'],case['k'];ws=case['weights_in_low_bit_mask_order'];H=[F(0)]
        for j in range(1,m+1):H.append(H[-1]+F(1,j))
        vals=[];cnt=0
        for row in case['terminal_table']:
            z=row['profile'];U=[F(0)]*m;phi=safe=F(0);W=0
            for mask,w in enumerate(ws,1):
                load=sum(mask>>a&1 for a in z)
                if load:
                    W+=w;phi+=w*H[load]
                    for i,a in enumerate(z):
                        if mask>>a&1:U[i]+=F(w,load)
                prior=0
                for i,a in enumerate(z):
                    if mask>>a&1:safe+=F(w,prior+m-i);prior+=1
            assert list(map(str,U))==row['utilities'] and str(phi)==row['phi'] and W==row['W'] and str(safe)==row['safe'] and str(phi-safe)==row['C']
            vals.append((row,phi,W,safe));cnt+=1
        P=max(v[1]for v in vals)
        for row,phi,W,safe in vals:assert str(W+phi-safe-P)==row['margin']
        least=min(F(row['margin'])for row,_,_,_ in vals if row['root_SPE'])
        assert str(least)==case['minimum_unscaled_margin']
        out.append(dict(label=case['label'],m=m,k=k,terminal_rows_recomputed=cnt,P=str(P),minimum_on_reported_root_SPE=str(least),scope='All saved terminal arithmetic checked; root_SPE flags and historical complete-policy enumeration are read, not independently re-enumerated.'))
    return dict(path=str(p.relative_to(ROOT)),sha256=digest(p),cases=out)

def certificates():
    d=E/'fourcopy-root-and-reset-swap-primary/related-original/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_1'
    rows=[]
    for name in ['fourcopy_exact_cuts.json','fourcopy_exact_check.json','fourcopy_threshold_exact.json','fourcopy_threshold_check.json']:
        p=d/name;x=json.loads(p.read_text());items=x if isinstance(x,list)else[x]
        for c in items:
            if 'multipliers'in c:
                lm={k:F(v)for k,v in c['multipliers'].items()};assert all(v>=0 for v in lm.values());assert sum((v for k,v in lm.items() if k.startswith(('PAIR:','LAST:'))),F(0))==1
                assert 'PAIR:4'not in lm and not any(k.startswith('FLOOR:4:')for k in lm)
            if 'base_minima'in c:assert len(c['base_minima'])==64 and all(int(v)>=0 for v in c['base_minima'].values())
        rows.append(dict(path=str(p.relative_to(ROOT)),sha256=digest(p),records=len(items),scope='Entire JSON parsed; all stored nonnegative multipliers, coverage normalizations and semantic row guards checked; all stored base minima checked. No new 65536-type replay.'))
    return rows

if __name__=='__main__':
    result=dict(status='passed',script_sha256=digest(Path(__file__)),banks=banks(),tiny_interface=tiny(),fourcopy_json=certificates(),limits='Finite evidence only; no solver, LP, original discovery or general theorem test.')
    atomic(OUT,result);print(json.dumps(result,ensure_ascii=False,indent=2))
