"""Exact all-orbit ZZ saturation and literal 2-CNF face at the 19621 point.

No constructor/parser imports.  Literal code 2*v+b means X_v=b;
X_(2*e)=R_e and X_(2*e+1)=Z_e.  The 66 old nodes stay distinct
until a saved implication path proves an almost-sure identity.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import json

EXPECTED_SHA = 'd70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f'

def sha(path):
    return sha256(Path(path).read_bytes()).hexdigest()

def canonical(seq):
    d = {}; out = []
    for x in seq:
        if x not in d: d[x] = len(d)
        out.append(d[x])
    return tuple(out)

def orbit(e, f):
    return e[0], f[0], canonical(e[1:] + f[1:])

def parse_point(path):
    raw = json.loads(Path(path).read_text())
    assert sha(path) == EXPECTED_SHA
    assert raw['verified_rows'] == 19621 and len(raw['columns']) == 15593
    cols = raw['columns'][:4849]
    hist = {}; groups = defaultdict(dict); family = defaultdict(dict)
    for j, c in enumerate(cols):
        if c['kind'] == 'hist':
            h = j; hist[h] = c
        elif c['kind'] == 'joint-reply':
            # hist_column_old predates the joint-reply column expansion;
            # original 4849 order, as in the archived verifier, fixes h.
            f, same, wi, wj = c['group']
            groups[h].setdefault((f, same, tuple(wi), tuple(wj)), {})[tuple(c['state'])] = Q(c['weight'])
        elif c['kind'] == 'actual-B-family-state' and c['source'] == 4:
            family[c['hist_column']][tuple(c['hidden']) + (c['ell']//6,)] = Q(c['weight'])
            assert c['ell'] in (0, 6)
    nodes = [n for n in product(range(2), range(6), range(6)) if n[0] or n[1] != n[2]]
    data = {}
    for h, hc in hist.items():
        H = Q(hc['weight'])
        words = [w for w, n in zip(product(range(2), repeat=3), hc['hist']) for _ in range(n)]
        assert len(words) == 6
        own = []; ng = []
        for f, i, j in nodes:
            g = (f, int(i == j), words[i], words[j]); ng.append(g)
            d = groups[h][g]
            vals = [H-d[0,1]-d[1,0]-d[1,1], d[0,1], d[1,0], d[1,1]]
            assert min(vals) >= 0
            own.append(vals)
        assert set(family[h]) == set(product(range(2), repeat=3))
        assert sum(family[h].values()) == H
        data[h] = dict(H=H, actual=tuple(map(int, hc['actual_bits'])), words=words,
                       groups=ng, own=own, B4=family[h], hist=hc['hist'])
    return raw, nodes, data

def closure(adj):
    n=len(adj); reach=[(1<<i) | sum(1<<j for j in adj[i]) for i in range(n)]
    for k in range(n):
        bit=1<<k; rk=reach[k]
        for i in range(n):
            if reach[i]&bit:reach[i]|=rk
    return reach

def derive_graph(own, H, saturated_pairs):
    n = 132; adj=[set() for _ in range(2*n)]; clauses=[]
    def forbid(x, a, y, b, why):
        l=2*x+a; m=2*y+b
        adj[l].add(m^1); adj[m].add(l^1)
        clauses.append(dict(forbidden=[l,m], reason=why))
    for e, vals in enumerate(own):
        for s, mass in enumerate(vals):
            if mass == 0: forbid(2*e, s//2, 2*e+1, s%2, ['own-zero', e, s])
    for e, f, ci in saturated_pairs:
        q=own[e][2]+own[e][3]; v=own[f][1]+own[f][3]
        if q<=v:forbid(2*e,1,2*f+1,0,['ZZ-saturation',ci,e,f,'R-subset-Z'])
        if q>=v:forbid(2*e,0,2*f+1,1,['ZZ-saturation',ci,e,f,'Z-subset-R'])
    reach=closure(adj)
    assigned=set();scc=[];comp=[None]*(2*n)
    for i in range(2*n):
        if i in assigned:continue
        cc=[j for j in range(2*n) if (reach[i]>>j)&1 and (reach[j]>>i)&1]
        cid=len(scc)
        for j in cc:comp[j]=cid
        assigned.update(cc);scc.append(cc)
    assert all(comp[2*v]!=comp[2*v+1] for v in range(n)), '2-CNF contradiction'
    mass=[]
    for m in own:
        r=m[2]+m[3];z=m[1]+m[3]
        mass.extend([H-r,r,H-z,z])
    violations=[]
    for i in range(2*n):
        for j in range(2*n):
            if (reach[i]>>j)&1 and mass[i]>mass[j]:
                violations.append([i,j,str(mass[i]),str(mass[j])])
    forced={}
    for v in range(n):
        for b in (0,1):
            if (reach[2*v+(1-b)]>>(2*v+b))&1:
                forced[v]=b
                assert mass[2*v+b]==H
    free_classes=[];representative={}
    for v in range(n):
        if v in forced:continue
        ci,cj=comp[2*v],comp[2*v+1]
        key=min(ci,cj),max(ci,cj)
        if key not in representative:
            representative[key]=v;free_classes.append(dict(variable=v, zero_component=ci, one_component=cj))
    free_map=[]
    for v in range(n):
        if v in forced: free_map.append(dict(constant=forced[v]));continue
        ci,cj=comp[2*v],comp[2*v+1];rep=representative[min(ci,cj),max(ci,cj)]
        idx=next(i for i,x in enumerate(free_classes) if x['variable']==rep)
        free_map.append(dict(free_variable=idx, flip=int(comp[2*v]!=comp[2*rep])))
    return dict(clauses=clauses, adjacency=[sorted(x) for x in adj],
                transitive_reach_hex=[hex(x) for x in reach], scc=scc,
                variable_constants={str(k):v for k,v in forced.items()},
                free_classes=free_classes, variable_map=free_map,
                marginal_implication_violations=violations,
                literal_masses=[str(x) for x in mass],
                summary=dict(clauses=len(clauses), directed_edges=sum(map(len,adj)),
                             scc=len(scc), forced_variables=len(forced),
                             free_boolean_classes=len(free_classes),
                             implication_marginal_violations=len(violations)))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--point',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    raw,nodes,data=parse_point(args.point)
    orbits=defaultdict(list)
    for e, ne in enumerate(nodes):
        for f,nf in enumerate(nodes):orbits[orbit(ne,nf)].append((e,f))
    orbit_records=[];saturated=[]
    for cl, pairs in sorted(orbits.items()):
        self_query=all(e==f for e,f in pairs);contrib={}
        for h,d in data.items():
            own=d['own'];P=sum(d['actual'][:4]);value=Q()
            for e,f in pairs:
                qe=own[e][2]+own[e][3];ve=own[e][1]+own[e][3]
                vf=own[f][1]+own[f][3];te=own[e][3]
                value+=(ve-vf)/Q(P+1)+(min(qe,vf)-te)/Q((P+1)*(P+2))
            contrib[h]=value/len(pairs)
        upper=sum(contrib.values(),Q())
        rec=dict(orbit=cl,literal_queries=len(pairs),self_query=self_query,
                 Frechet_upper=str(upper),upper_float=float(upper),
                 hist_contributions={str(h):str(v) for h,v in contrib.items()},
                 literal_pairs=pairs)
        orbit_records.append(rec)
        if upper==0 and not self_query:
            ci=len(saturated);saturated.append(dict(orbit=cl,literal_pairs=pairs))
    assert len(orbit_records)==42
    assert sum(not r['self_query'] for r in orbit_records)==39
    assert all(Q(r['Frechet_upper'])>=0 for r in orbit_records)
    satpairs=[(e,f,ci) for ci,c in enumerate(saturated) for e,f in c['literal_pairs']]
    hist_records=[]
    for h,d in data.items():
        rec=dict(hist_column=h,actual=d['actual'],hist=d['hist'],old_words=d['words'],
                 mass=str(d['H']),own=[[str(x) for x in m] for m in d['own']],
                 node_groups=d['groups'],B4_states=[dict(state=s,mass=str(m)) for s,m in sorted(d['B4'].items())])
        if d['H']:
            rec['face']=derive_graph(d['own'],d['H'],satpairs)
            # Stabilizer-equivariance checks do not identify any distinct node.
            stabilizer=[p for p in permutations(range(6)) if all(d['words'][p[i]]==d['words'][i] for i in range(6))]
            lookup={e:i for i,e in enumerate(nodes)}
            edges=set((i,j) for i,v in enumerate(rec['face']['adjacency']) for j in v)
            checks=0
            for p in stabilizer:
                nodeperm=[lookup[f,p[i],p[j]] for f,i,j in nodes]
                litperm=[4*nodeperm[v//4]+v%4 for v in range(264)]
                assert all((litperm[i],litperm[j]) in edges for i,j in edges)
                assert all(d['own'][i]==d['own'][nodeperm[i]] for i in range(66))
                checks+=len(edges)+66
            rec['stabilizer_order']=len(stabilizer);rec['stabilizer_equivariance_checks']=checks
        hist_records.append(rec)
    out=dict(scope='All 39 nonself ZZ orbit upper budgets and exact common literal zero-cell face, not a full SPE',
             point_path=str(args.point),point_sha256=sha(args.point),source_sha256=sha(Path(__file__)),
             literal_node_order=nodes,variable_order='X[2e]=R_e; X[2e+1]=Z_e; literal 2v+b means X_v=b',
             orbit_records=orbit_records,saturated_nonself_orbits=saturated,hist_records=hist_records,
             summary=dict(nonself_orbits=39,saturated_nonself_orbits=len(saturated),
                          saturated_literal_queries=len(satpairs),positive_hist=sum(d['H']>0 for d in data.values())))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(out['summary']))
    for r in hist_records:
        if 'face' in r:print(r['hist_column'],r['face']['summary'])

if __name__=='__main__':main()
