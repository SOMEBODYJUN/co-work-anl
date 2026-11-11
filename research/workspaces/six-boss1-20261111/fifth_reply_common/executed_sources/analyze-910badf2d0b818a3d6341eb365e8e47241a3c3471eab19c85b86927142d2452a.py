"""Exact zero-face implications in the unrestricted R/Z/B4/D Boolean domain.

This phase uses only fixed marginals and zero payoff upper bounds.  It does
not assume the 92-atom construction, phase orientations, or common thresholds.
"""
from __future__ import annotations
from collections import defaultdict, deque
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product, combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
ROOT = WORK.parents[2]
POINT = WORK / 'union_augmented_lp/augmented_lp_exact.json'
MARGINALS = WORK / 'fifth_reply_interface/D_marginals.json'
NETWORK = WORK / 'common_network_19662/common_atoms.json'
POINT_SHA = 'b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'
NODES = [(f,j,k) for f,j,k in product(range(2),range(6),range(6)) if f or j != k]
WORDS = list(product(range(2),repeat=3))

def sha(p): return sha256(p.read_bytes()).hexdigest()
def serial(v):
    if isinstance(v,Q): return str(v)
    if isinstance(v,dict): return {str(k):serial(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)): return [serial(x) for x in v]
    return v
def dump(p,obj): p.write_text(json.dumps(serial(obj),ensure_ascii=False,indent=2)+'\n')
def canon(xs):
    seen={}
    return ''.join(str(seen.setdefault(x,len(seen))) for x in xs)
def read():
    assert sha(POINT)==POINT_SHA
    raw=json.loads(POINT.read_bytes()); cols=raw['columns']; values=[Q(c['weight']) for c in cols]
    hist={}; groups=defaultdict(dict); b4=defaultdict(dict); current=None
    for j,c in enumerate(cols[:4849]):
        if c['kind']=='hist': current=j;hist[j]=c
        elif c['kind']=='joint-reply':
            f,diag,wi,wj=c['group'];g=(f,diag,tuple(wi),tuple(wj))
            groups[current].setdefault(g,{})[tuple(c['state'])]=values[j]
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            s=tuple(c['hidden'])+(c['ell']//6,);b4[c['hist_column']][s]=values[j]
    dm=json.loads(MARGINALS.read_bytes()); assert dm['point_sha256']==POINT_SHA
    x={r['hist_column']:{tuple(d['word']):Q(d['value']) for d in r['D']} for r in dm['hist_and_D_marginals']}
    data={}
    for h,c in hist.items():
        H=values[h]; a=tuple(map(int,c['actual_bits']))
        words=[w for w,n in zip(WORDS,c['hist']) for _ in range(n)]
        assert len(words)==6
        for m in groups[h].values():
            m[0,0]=H-sum(m.values(),Q());assert min(m.values())>=0
        own=[groups[h][(f,int(j==k),words[j],words[k])] for f,j,k in NODES]
        assert set(b4[h])==set(product(range(2),repeat=3))
        assert sum(b4[h].values(),Q())==H
        assert all(0<=xx<=H for xx in x[h].values())
        data[h]=dict(H=H,a=a,words=words,own=own,b4=b4[h],x=x[h],hist=c)
    assert len(hist)==16 and sum(d['H'] for d in data.values())==1
    return data,cols

def implication_graph(d):
    H=d['H'];own=d['own'];x=d['x'];words=d['words'];b4=d['b4']
    names=['H1','H2','Y']+[f'{kind}:{f},{j},{k}' for kind in ('R','Z') for f,j,k in NODES]+[f'D:{i}' for i in range(6)]
    nv=len(names);assert nv==141
    masses=[sum((v*s[k] for s,v in b4.items()),Q()) for k in range(3)]
    masses += [m[1,0]+m[1,1] for m in own]+[m[0,1]+m[1,1] for m in own]
    masses += [x[w] for w in words]
    edges=defaultdict(list);clauses=[]
    def add_clause(l1,l2,reason):
        cid=len(clauses);clauses.append(dict(literals=[l1,l2],reason=reason))
        edges[l1^1].append((l2,cid));edges[l2^1].append((l1,cid))
    def force(v,bit,reason): add_clause(2*v+bit,2*v+bit,reason)
    def inclusion(a,b,reason): add_clause(2*a,2*b+1,reason)
    def saturated(a,b,reason):
        if masses[a]<=masses[b]:inclusion(a,b,dict(**reason,relation='left-in-right'))
        if masses[b]<=masses[a]:inclusion(b,a,dict(**reason,relation='right-in-left'))
    for v,m in enumerate(masses):
        if m==0: force(v,0,dict(kind='zero-marginal',variable=names[v]))
        if m==H: force(v,1,dict(kind='full-marginal',variable=names[v]))
    for e,m in enumerate(own):
        for (r,z),v in m.items():
            if v==0:add_clause(2*(3+e)+(1-r),2*(3+66+e)+(1-z),dict(kind='own-zero-cell',node=NODES[e],state=[r,z]))
    for a,b in combinations(range(3),2):
        for aa,bb in product(range(2),repeat=2):
            if sum((m for s,m in b4.items() if s[a]==aa and s[b]==bb),Q())==0:
                add_clause(2*a+(1-aa),2*b+(1-bb),dict(kind='B4-zero-pair-projection',slots=[a,b],state=[aa,bb]))
    for e,(f,j,k) in enumerate(NODES):
        if j!=k:saturated(3+66+e,0,dict(kind='F-to-Z-zero-upper',node=NODES[e]))
    for i in range(6):saturated(3+132+i,0,dict(kind='F-to-D-zero-upper',index=i))
    for i in range(6):
        for e,(f,j,k) in enumerate(NODES):
            o=(f,canon((i,j,k)))
            if o in ((0,'012'),(1,'010')):
                saturated(3+e,3+132+i,dict(kind='Z-to-D-zero-upper',orbit=o,index=i,node=NODES[e]))
    size=2*nv
    reach=[(1<<i)|sum(1<<j for j in {j for j,cid in edges[i]}) for i in range(size)]
    for k in range(size):
        bit=1<<k;row=reach[k]
        for i in range(size):
            if reach[i]&bit:reach[i]|=row
    literal_mass=[H-m if bit==0 else m for m in masses for bit in range(2)]
    contradictions=[names[v] for v in range(nv) if reach[2*v]&(1<<(2*v+1)) and reach[2*v+1]&(1<<(2*v))]
    order_bad=[];inclusions=[];equalities=[];seen=set()
    for i,row in enumerate(reach):
        for j in range(size):
            if i!=j and row&(1<<j):
                inclusions.append([i,j])
                if literal_mass[i]>literal_mass[j]:order_bad.append(dict(source=i,target=j,source_mass=literal_mass[i],target_mass=literal_mass[j]))
        if i not in seen:
            component=[j for j in range(size) if row&(1<<j) and reach[j]&(1<<i)]
            seen.update(component)
            if len(component)>1:equalities.append(component)
    forced=[dict(variable=names[v],bit=bit) for v in range(nv) for bit in range(2) if reach[2*v+1-bit]&(1<<(2*v+bit))]
    branches=[]
    for s,m in sorted(b4.items()):
        if m==0:continue
        seeds=[2*k+s[k] for k in range(3)]
        enabled=0
        for v in seeds:enabled|=reach[v]
        conflicts=[names[v] for v in range(nv) if enabled&(1<<(2*v)) and enabled&(1<<(2*v+1))]
        branches.append(dict(state=s,mass=m,satisfiable=not contradictions and not conflicts,conflicts=conflicts))
    return dict(names=names,masses=masses,literal_encoding='2*v+b means variable v equals b; complement is xor 1',clauses=clauses,
                closure_inclusions=inclusions,equality_components=equalities,forced=forced,boolean_contradictions=contradictions,
                marginal_order_violations=order_bad,B4_positive_state_extensions=branches,
                counts=dict(variables=nv,clauses=len(clauses),direct_implication_edges=sum(map(len,edges.values())),
                            closure_inclusions=len(inclusions),equality_components=len(equalities),forced=len(forced))),reach

def main():
    data,cols=read();rows={};F=Q()
    triple=defaultdict(list)
    for i in range(6):
        for e,(f,j,k) in enumerate(NODES):triple[f,canon((i,j,k))].append((i,e))
    for h,d in data.items():
        a=d['a'];p3=sum(a[:3]);P=sum(a[:4]);s0=p3+a[5]+1
        F+=sum((m*Q(s[1],s0+s[0]) for s,m in d['b4'].items()),Q())
    rows['F-to-D-upper']=F
    for o in ((0,0),(1,0)):rows[f'F-to-Z-upper:{o[0]}:{o[1]}']=F
    for o in triple:rows[f'Z-to-D-upper:{o[0]}:{o[1]}']=Q()
    for h,d in data.items():
        a=d['a'];p3=sum(a[:3]);P=sum(a[:4]);s0=p3+a[5]+1
        C=sum((m*s[0] for s,m in d['b4'].items()),Q())
        for i,w in enumerate(d['words']):
            xx=d['x'][w];rows['F-to-D-upper']-=(xx/Q(s0)-min(xx,C)/Q(s0*(s0+1)))/6
        for f in (0,1):
            ids=[e for e,(ff,j,k) in enumerate(NODES) if f==ff and j!=k]
            for e in ids:
                own=d['own'][e];v=own[0,1]+own[1,1]
                rows[f'F-to-Z-upper:{f}:0']-=(v/Q(s0)-min(v,C)/Q(s0*(s0+1)))/len(ids)
        for o,members in triple.items():
            for i,e in members:
                own=d['own'][e];q=own[1,0]+own[1,1];v=own[0,1]+own[1,1];t=own[1,1];xx=d['x'][d['words'][i]]
                rows[f'Z-to-D-upper:{o[0]}:{o[1]}']+=((v-xx)/Q(P+1)+(min(q,xx)-t)/Q((P+1)*(P+2)))/len(members)
    expected={'F-to-D-upper','F-to-Z-upper:0:0','F-to-Z-upper:1:0','Z-to-D-upper:0:012','Z-to-D-upper:1:010'}
    assert {k for k,v in rows.items() if v==0}==expected
    assert all(v>=0 for v in rows.values())
    records=[]
    for h,d in data.items():
        if d['H']==0:records.append(dict(hist_column=h,mass='0',vacuous=True));continue
        report,reach=implication_graph(d)
        records.append(dict(hist_column=h,mass=d['H'],vacuous=False,**report))
    bad=[r['hist_column'] for r in records if not r['vacuous'] and (r['boolean_contradictions'] or r['marginal_order_violations'] or not all(b['satisfiable'] for b in r['B4_positive_state_extensions']))]
    report=dict(scope='Unrestricted 141-bit per-hist Boolean zero-face domain; exact 2SAT closure and necessary marginal-order tests, not a proof of full measure feasibility',
                point_sha256=POINT_SHA,marginals_sha256=sha(MARGINALS),script_sha256=sha(Path(__file__)),
                zero_upper_rows=rows,expected_zero_upper_rows=sorted(expected),hist_records=records,
                obstructed_hist=bad,status='NO_BOOLEAN_OR_MARGINAL_ORDER_OBSTRUCTION' if not bad else 'OBSTRUCTION')
    dump(HERE/'boolean_analysis.json',report)
    sources=[POINT,MARGINALS,NETWORK,WORK/'main_fifth_reply_contract.md',WORK/'fifth_reply_interface.md',
             WORK/'fifth_reply_interface/exact_lift.json',WORK/'fifth_reply_interface/symbolic_lift.json',
             WORK/'fifth_reply_interface/independent_verification.json',WORK/'common_network_19662.md',
             WORK/'common_network_19662/independent_verification.json',WORK/'common_network_19662/verify_common.py',
             ROOT/'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
             ROOT/'archives/customer-attraction/subarchives/six-providers/问题--问题.md',ROOT/'AGENTS.md',ROOT/'research/GITHUB_RESOURCES.md']
    dump(HERE/'source_reading.json',dict(sources=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p),bytes=p.stat().st_size) for p in sources]))
    print(json.dumps(serial(dict(status=report['status'],obstructed_hist=bad,zero_upper_rows={k:v for k,v in rows.items() if v==0},
                                hist_counts=[dict(hist_column=r['hist_column'],**r['counts']) for r in records if not r['vacuous']]))))

if __name__=='__main__': main()
