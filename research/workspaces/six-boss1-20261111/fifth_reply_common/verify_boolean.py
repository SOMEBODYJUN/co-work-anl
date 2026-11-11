"""Independent reconstruction of zero clauses and complete literal entailments.

Each positive full B4 state reduces the general support domain to 2SAT.
Breadth-first implication closures certify all literal inclusions, including
vacuous antecedents and forced consequents, without using network atoms.
"""
from collections import Counter,defaultdict,deque
from fractions import Fraction as Q
from itertools import product,combinations
from pathlib import Path
from hashlib import sha256
import json,time
HERE=Path(__file__).resolve().parent;WORK=HERE.parent
def sha(p):return sha256(p.read_bytes()).hexdigest()
def canon(xs):
    seen={};return ''.join(str(seen.setdefault(x,len(seen))) for x in xs)
def main():
    start=time.perf_counter()
    point=json.loads((WORK/'union_augmented_lp/augmented_lp_exact.json').read_bytes())
    saved=json.loads((HERE/'boolean_analysis.json').read_bytes());records={r['hist_column']:r for r in saved['hist_records']}
    assert sha(WORK/'union_augmented_lp/augmented_lp_exact.json')==saved['point_sha256']
    marg=json.loads((WORK/'fifth_reply_interface/D_marginals.json').read_bytes())
    D={r['hist_column']:{tuple(v['word']):Q(v['value']) for v in r['D']} for r in marg['hist_and_D_marginals']}
    cols=point['columns'];values=[Q(c['weight']) for c in cols]
    hist={};own=defaultdict(dict);b4=defaultdict(dict);cur=None
    for j,c in enumerate(cols[:4849]):
        if c['kind']=='hist':cur=j;hist[j]=c
        elif c['kind']=='joint-reply':
            f,diag,wi,wj=c['group'];g=(f,diag,tuple(wi),tuple(wj));own[cur].setdefault(g,{})[tuple(c['state'])]=values[j]
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            b4[c['hist_column']][tuple(c['hidden'])+(c['ell']//6,)]=values[j]
    nodes=[e for e in product(range(2),range(6),range(6)) if e[0] or e[1]!=e[2]]
    triple=defaultdict(list)
    for i in range(6):
        for e,(f,j,k) in enumerate(nodes):triple[f,canon((i,j,k))].append((i,e))
    F=sum((m*Q(s[1],sum(map(int,hist[h]['actual_bits'][:3]))+int(hist[h]['actual_bits'][5])+s[0]+1) for h in hist for s,m in b4[h].items()),Q())
    upper={'F-to-D-upper':F,'F-to-Z-upper:0:0':F,'F-to-Z-upper:1:0':F,'Z-to-D-upper:0:012':Q(),'Z-to-D-upper:1:010':Q()}
    hist_checks=[];total_clauses=0;total_inclusions=0;branch_count=0;reverse_equal_checks=0
    for h,hc in hist.items():
        H=values[h];a=tuple(map(int,hc['actual_bits']));P=sum(a[:4]);s0=sum(a[:3])+a[5]+1
        words=[w for w,n in zip(product(range(2),repeat=3),hc['hist']) for _ in range(n)]
        for m in own[h].values():m[0,0]=H-sum(m.values(),Q())
        ms=[own[h][(f,int(j==k),words[j],words[k])] for f,j,k in nodes]
        q=[m[1,0]+m[1,1] for m in ms];v=[m[0,1]+m[1,1] for m in ms];x=[D[h][w] for w in words]
        C=sum((m*s[0] for s,m in b4[h].items()),Q())
        upper['F-to-D-upper']-=sum((xx/Q(s0)-min(xx,C)/Q(s0*(s0+1)) for xx in x),Q())/6
        for f in (0,1):
            ids=[e for e,(ff,j,k) in enumerate(nodes) if ff==f and j!=k]
            upper[f'F-to-Z-upper:{f}:0']-=sum((v[e]/Q(s0)-min(v[e],C)/Q(s0*(s0+1)) for e in ids),Q())/len(ids)
        for f,pattern in ((0,'012'),(1,'010')):
            ids=triple[f,pattern]
            upper[f'Z-to-D-upper:{f}:{pattern}']+=sum(((v[e]-x[i])/Q(P+1)+(min(q[e],x[i])-ms[e][1,1])/Q((P+1)*(P+2)) for i,e in ids),Q())/len(ids)
        if H==0:assert records[h]['vacuous'];continue
        rr=records[h];names=['H1','H2','Y']+[f'{kind}:{f},{j},{k}' for kind in ('R','Z') for f,j,k in nodes]+[f'D:{i}' for i in range(6)]
        masses=[sum((m*s[k] for s,m in b4[h].items()),Q()) for k in range(3)]+q+v+x
        assert names==rr['names'] and masses==list(map(Q,rr['masses']))
        clauses=[]
        def clause(a,b):clauses.append(tuple(sorted((a,b))))
        def sat(a,b):
            if masses[a]<=masses[b]:clause(2*a,2*b+1)
            if masses[b]<=masses[a]:clause(2*b,2*a+1)
        for k,m in enumerate(masses):
            if m==0:clause(2*k,2*k)
            if m==H:clause(2*k+1,2*k+1)
        for e,m in enumerate(ms):
            for (r,z),mass in m.items():
                if mass==0:clause(2*(3+e)+1-r,2*(69+e)+1-z)
        for i,j in combinations(range(3),2):
            for u,vv in product(range(2),repeat=2):
                if sum((m for s,m in b4[h].items() if s[i]==u and s[j]==vv),Q())==0:clause(2*i+1-u,2*j+1-vv)
        for e,(f,j,k) in enumerate(nodes):
            if j!=k:sat(69+e,0)
        for i in range(6):sat(135+i,0)
        for pattern in ((0,'012'),(1,'010')):
            for i,e in triple[pattern]:sat(3+e,135+i)
        assert Counter(clauses)==Counter(tuple(sorted(c['literals'])) for c in rr['clauses'])
        total_clauses+=len(clauses);logical=[set(range(282)) for _ in range(282)]
        for s,mass in b4[h].items():
            if not mass:continue
            edges=[set() for _ in range(282)]
            for u,vv in clauses:edges[u^1].add(vv);edges[vv^1].add(u)
            for k in range(3):edges[2*k+1-s[k]].add(2*k+s[k])
            reach=[]
            for source in range(282):
                found={source};todo=deque([source])
                while todo:
                    u=todo.popleft()
                    for vv in edges[u]-found:found.add(vv);todo.append(vv)
                reach.append(found)
            assert all(not (2*k+1 in reach[2*k] and 2*k in reach[2*k+1]) for k in range(141))
            forced={u for u in range(282) if u in reach[u^1]}
            for u in range(282):logical[u] &= set(range(282)) if u^1 in reach[u] else reach[u]|forced
            branch_count+=1
        closure={(u,vv) for u,targets in enumerate(logical) for vv in targets if u!=vv}
        assert closure==set(map(tuple,rr['closure_inclusions']))
        total_inclusions+=len(closure)
        literal_mass=[H-m if b==0 else m for m in masses for b in range(2)]
        for u,vv in closure:
            assert literal_mass[u]<=literal_mass[vv]
            if literal_mass[u]==literal_mass[vv]:assert (vv,u) in closure;reverse_equal_checks+=1
        forced=[]
        for k in range(141):
            for bit in range(2):
                if 2*k+bit in logical[2*k+1-bit]:assert masses[k]==H*bit;forced.append(dict(variable=names[k],bit=bit))
        assert forced==rr['forced']
        seen=set();components=[]
        for u in range(282):
            if u in seen:continue
            comp=tuple(vv for vv in sorted(logical[u]) if u in logical[vv]);seen.update(comp)
            if len(comp)>1:components.append(comp)
        assert set(components)==set(map(tuple,rr['equality_components']))
        hist_checks.append(dict(hist_column=h,clauses=len(clauses),literal_inclusions=len(closure),equality_components=len(components),forced_variables=len(forced)))
    assert all(v==0 for v in upper.values())
    assert {k:str(v) for k,v in upper.items()}=={k:saved['zero_upper_rows'][k] for k in upper}
    report=dict(status='PASS',scope='Complete literal implications of the stated zero-face clauses on the unrestricted per-hist Boolean domain, plus exact marginal order; no phase or 92-atom support assumption',
                point_sha256=saved['point_sha256'],analysis_sha256=sha(HERE/'boolean_analysis.json'),verifier_sha256=sha(Path(__file__)),
                independently_recomputed_zero_upper_rows={k:str(v) for k,v in upper.items()},
                clauses=total_clauses,complete_literal_inclusions=total_inclusions,positive_B4_state_2SAT_checks=branch_count,
                equal_marginal_inclusions_already_reversible=reverse_equal_checks,hist_checks=hist_checks,
                boolean_contradictions=0,marginal_order_violations=0,forced_marginal_violations=0,
                elapsed_seconds=time.perf_counter()-start)
    (HERE/'boolean_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
