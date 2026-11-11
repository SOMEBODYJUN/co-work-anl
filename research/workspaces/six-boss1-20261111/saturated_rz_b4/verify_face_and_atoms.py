"""Independent Fraction verifier: no imports from discovery/construction code.

Rebuild the 42 pair orbits by the actual S6 action, all upper budgets, every
literal zero cell, the complete implication closure, the order-domain change
of Boolean coordinates, and all direct terminal payoffs of the common atoms.
"""
from __future__ import annotations
from collections import Counter,defaultdict,deque
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations,product
from math import lcm
from pathlib import Path
import argparse,json
import numpy as np

POINT_SHA='d70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f'

def digest(p):return sha256(Path(p).read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--point',type=Path,required=True)
    ap.add_argument('--face',type=Path,required=True);ap.add_argument('--atoms',type=Path,required=True)
    ap.add_argument('--domain-output',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    point=json.loads(args.point.read_text());face=json.loads(args.face.read_text());wit=json.loads(args.atoms.read_text())
    assert digest(args.point)==face['point_sha256']==wit['point_sha256']==POINT_SHA
    assert wit['face_sha256']==digest(args.face)
    col=point['columns'][:4849];hist={};gm=defaultdict(dict);b4=defaultdict(dict)
    for k,c in enumerate(col):
        if c['kind']=='hist':hist[k]=c;h=k
        elif c['kind']=='joint-reply':
            f,b,u,v=c['group'];g=(f,b,tuple(u),tuple(v))
            gm[h].setdefault(g,{})[tuple(c['state'])]=F(c['weight'])
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            assert len(c['hidden'])==2 and c['ell'] in (0,6)
            b4[c['hist_column']][tuple(c['hidden'])+(c['ell']//6,)]=F(c['weight'])
    ns=[e for e in product(range(2),range(6),range(6)) if e[0] or e[1]!=e[2]];ni={e:k for k,e in enumerate(ns)}
    assert face['literal_node_order']==wit['literal_node_order']==[list(e) for e in ns]
    pp=list(permutations(range(6)))
    actions=[[ni[f,p[i],p[j]] for f,i,j in ns] for p in pp]
    # Build pair orbits directly; record uniform action multiplicities.
    unseen=set(product(range(66),repeat=2));orbits=[];orbit_index={};permutation_counts=0
    while unseen:
        e,f=min(unseen);counts=Counter((a[e],a[f]) for a in actions);members=sorted(counts)
        assert len(counts)*next(iter(counts.values()))==720 and len(set(counts.values()))==1
        assert set(members)<=unseen
        for pair in members:orbit_index[pair]=len(orbits)
        orbits.append(members);unseen.difference_update(members);permutation_counts+=720
    assert len(orbits)==42
    saved_orbits={tuple(sorted(tuple(x) for x in r['literal_pairs'])):r for r in face['orbit_records']}
    assert len(saved_orbits)==42 and set(saved_orbits)==set(tuple(o) for o in orbits)
    data={};hmap={r['hist_column']:r for r in face['hist_records']}
    for h,c in hist.items():
        mass=F(c['weight']);ws=[w for w,n in zip(product(range(2),repeat=3),c['hist']) for _ in range(n)]
        own=[];groups=[]
        for f,i,j in ns:
            g=(f,int(i==j),ws[i],ws[j]);m=gm[h][g];groups.append(g)
            own.append([mass-sum(m.values()),m[0,1],m[1,0],m[1,1]])
        assert all(x>=0 for m in own for x in m)
        assert sum(b4[h].values())==mass and set(b4[h])==set(product(range(2),repeat=3))
        r=hmap[h]
        assert list(map(tuple,r['old_words']))==ws and F(r['mass'])==mass
        assert [[F(x) for x in row] for row in r['own']]==own
        assert {tuple(s['state']):F(s['mass']) for s in r['B4_states']}==b4[h]
        data[h]=dict(H=mass,words=ws,own=own,groups=groups,actual=tuple(map(int,c['actual_bits'])))
    upper=[];zero_pairs=[];nonself=0
    for members in orbits:
        saved=saved_orbits[tuple(members)];total=F();selfq=all(e==f for e,f in members)
        assert saved['self_query']==selfq and saved['literal_queries']==len(members)
        if not selfq:nonself+=1
        for h,d in data.items():
            P=sum(d['actual'][:4]);m=d['own'];value=F()
            for e,f in members:
                qr=m[e][2]+m[e][3];vz=m[f][1]+m[f][3];ve=m[e][1]+m[e][3]
                value+=(ve-vz)/F(P+1)+(min(qr,vz)-m[e][3])/F((P+1)*(P+2))
            value/=len(members);total+=value
            assert value==F(saved['hist_contributions'][str(h)])
        assert total==F(saved['Frechet_upper'])>=0
        upper.append(total)
        if not selfq and not total:zero_pairs.extend(members)
    assert nonself==39 and len(zero_pairs)==600
    assert set(zero_pairs)==set(tuple(p) for r in face['saturated_nonself_orbits'] for p in r['literal_pairs'])
    domains=[];edge_checks=0;prefix_checks=0;closure_checks=0
    for h,d in data.items():
        if not d['H']:
            domains.append(dict(hist_column=h,mass='0',domain='zero measure; no positive atoms'));continue
        rec=hmap[h];fc=rec['face'];own=d['own'];H=d['H']
        forbidden=set()
        for e,m in enumerate(own):
            for st,x in enumerate(m):
                if not x:forbidden.add(tuple(sorted((4*e+st//2,4*e+2+st%2))))
        for e,f in zero_pairs:
            q=own[e][2]+own[e][3];v=own[f][1]+own[f][3]
            if q<=v:forbidden.add(tuple(sorted((4*e+1,4*f+2))))
            if q>=v:forbidden.add(tuple(sorted((4*e,4*f+3))))
        assert forbidden==set(tuple(sorted(c['forbidden'])) for c in fc['clauses'])
        ad=[set() for _ in range(264)]
        for u,v in forbidden:ad[u].add(v^1);ad[v].add(u^1)
        assert [sorted(x) for x in ad]==fc['adjacency']
        reach=[]
        for l in range(264):
            seen={l};todo=[l]
            while todo:
                x=todo.pop()
                for y in ad[x]-seen:seen.add(y);todo.append(y)
            assert sum(1<<x for x in seen)==int(fc['transitive_reach_hex'][l],16)
            reach.append(seen);closure_checks+=264
        assert all((l^1) not in reach[l] or l not in reach[l^1] for l in range(264))
        cid={l:k for k,comp in enumerate(fc['scc']) for l in comp}
        assert len(cid)==264
        for l in range(264):
            assert set(fc['scc'][cid[l]])=={j for j in reach[l] if l in reach[j]}
        forces={v:int(2*v+1 in reach[2*v]) for v in range(132) if 2*v+1 in reach[2*v] or 2*v in reach[2*v+1]}
        assert forces=={int(v):b for v,b in fc['variable_constants'].items()}
        lm=[]
        for m in own:
            q=m[2]+m[3];v=m[1]+m[3];lm.extend([H-q,q,H-v,v])
        assert list(map(F,fc['literal_masses']))==lm
        assert all(lm[i]<=lm[j] for i in range(264) for j in reach[i])
        mapping=fc['variable_map'];free=fc['free_classes'];nf=len(free)
        for v,mm in enumerate(mapping):
            if v in forces:assert mm==dict(constant=forces[v])
            else:
                f=mm['free_variable'];rep=free[f]['variable'];flip=mm['flip']
                assert cid[2*v]==cid[2*rep+flip] and cid[2*v+1]==cid[2*rep+(1-flip)]
        # Signed-graph balance: every clause becomes a simple order inequality.
        reduced=set()
        for pair in forbidden:
            rr=[];taut=False
            for l in pair:
                mm=mapping[l//2];b=l%2
                if 'constant' in mm:
                    if mm['constant']!=b:taut=True
                else:rr.append((mm['free_variable'],b^mm['flip']))
            if taut:continue
            assert len(rr)==2
            if rr[0][0]==rr[1][0]:assert rr[0][1]!=rr[1][1];continue
            reduced.add(tuple(sorted(rr)))
        parity=[set() for _ in range(nf)]
        for (u,a),(v,b) in reduced:
            parity[u].add((v,1^a^b));parity[v].add((u,1^a^b))
        flip={};components=[]
        for root in range(nf):
            if root in flip:continue
            flip[root]=0;stack=[root];component=[]
            while stack:
                u=stack.pop();component.append(u)
                for v,b in parity[u]:
                    if v in flip:assert flip[v]==flip[u]^b
                    else:flip[v]=flip[u]^b;stack.append(v)
            components.append(sorted(component))
        order=set()
        for (u,a),(v,b) in reduced:
            a^=flip[u];b^=flip[v];assert a!=b
            order.add((u,v) if a else (v,u))
        # Edges u->v mean Y_u <= Y_v.  The SCC quotient must be acyclic.
        deg=[0]*nf;oa=[set() for _ in range(nf)]
        for u,v in order:oa[u].add(v);deg[v]+=1
        todo=deque(u for u in range(nf) if not deg[u]);top=[]
        while todo:
            u=todo.popleft();top.append(u)
            for v in oa[u]:
                deg[v]-=1
                if not deg[v]:todo.append(v)
        assert len(top)==nf
        full_own_leaves=[]
        for e,(fam,i,j) in enumerate(ns):
            if not all(own[e]):continue
            core=2*e+int(bool(fam));leaf=2*e+int(not fam)
            assert not ad[2*leaf] and not ad[2*leaf+1]
            full_own_leaves.append(dict(node=e,core_variable=core,leaf_variable=leaf))
        stabilizer=0
        for p,a in zip(pp,actions):
            moved=[None]*6
            for i in range(6):moved[p[i]]=d['words'][i]
            for e,(fam,i,j) in enumerate(ns):
                ee=a[e];ff,ii,jj=ns[ee]
                assert ff==fam and moved[ii]==d['words'][i] and moved[jj]==d['words'][j]
                assert sum(d['actual'][:3])+moved[ii][0]+moved[jj][1+fam]+1==sum(d['actual'][:3])+d['words'][i][0]+d['words'][j][1+fam]+1
                prefix_checks+=1
            if moved==d['words']:
                stabilizer+=1
                for u,vs in enumerate(ad):
                    for v in vs:
                        assert 4*a[u//4]+u%4 in range(264)
                        assert 4*a[v//4]+v%4 in ad[4*a[u//4]+u%4]
                        edge_checks+=1
        assert stabilizer==rec['stabilizer_order']
        domains.append(dict(hist_column=h,mass=str(H),constants={str(v):b for v,b in forces.items()},
                            old_variable_map=mapping,free_representatives=free,orientation=[flip[i] for i in range(nf)],
                            order_edges=sorted(order),topological_order=top,components=components,
                            component_sizes=sorted(map(len,components),reverse=True),full_own_leaves=full_own_leaves,
                            B4_allowed_states=[list(s) for s,m in b4[h].items() if m],
                            free_boolean_classes=nf,stabilizer_order=stabilizer))
    domain=dict(scope='Exact full Boolean domain of all own zero cells and all zero-budget ZZ cells at this point; old nonzero-budget IC and prescribed positive margins remain additional constraints',
                point_sha256=digest(args.point),face_sha256=digest(args.face),verification_source_sha256=digest(Path(__file__)),
                coordinates='X_v = constant or Y_free XOR map.flip XOR orientation[free]. All order_edges u,v mean Y_u<=Y_v. One common B4 state from the allowed list.',
                literal_node_order=ns,hist_domains=domains)
    args.domain_output.write_text(json.dumps(domain,indent=2,ensure_ascii=False)+'\n')
    # Atom-only verification: no interval-construction assumptions are needed.
    om={h:[[F()]*4 for e in ns] for h in hist};bm={h:defaultdict(F) for h in hist}
    values=[[F() for _ in orbits] for k in range(4)];bv=defaultdict(F)
    idx=[(np.array([e for e,f in m]),np.array([f for e,f in m])) for m in orbits]
    count=0;scale=1;clause_checks=0;total=F()
    for b in wit['blocks']:
        h=b['hist_column'];s=tuple(b['B4_state']);d=data[h];assert b4[h][s]>0
        P=sum(d['actual'][:4]);den=np.array([sum(d['actual'][:3])+d['words'][i][0]+d['words'][j][1+f]+1 for f,i,j in ns])
        fd=sum(d['actual'][:3])+d['actual'][5]+s[0]+1
        local=F()
        for at in b['atoms']:
            m=F(at['mass']);assert m>0
            states=np.array(at['states'],dtype=int);assert len(states)==66 and ((0<=states)&(states<4)).all()
            r=states//2;z=states%2;bits=np.empty(132,dtype=int);bits[0::2]=r;bits[1::2]=z
            for c in hmap[h]['face']['clauses']:
                assert not all(int(bits[l//2])==l%2 for l in c['forbidden']);clause_checks+=1
            for e,st in enumerate(states):om[h][e][int(st)]+=m
            bm[h][s]+=m;local+=m;total+=m;count+=1;scale=lcm(scale,(m/720).denominator)
            for k,(source,target,ds) in enumerate(((r,r,den),(r,z,den),(z,r,P+r+1),(z,z,P+r+1))):
                for dval in set(map(int,ds)):
                    mat=(ds==dval)[:,None]*(source[:,None]-target[None,:])
                    for oi,(ii,jj) in enumerate(idx):
                        coef=int(mat[ii,jj].sum())
                        if coef:values[k][oi]+=m*F(coef,len(ii)*dval)
            for o in ((0,0),(1,0),(1,1)):
                es=[e for e,(f,i,j) in enumerate(ns) if (f,int(i==j))==o];n=len(es)
                bv['F-to-R',o]+=m*F(n*s[1]-int(r[es].sum()),n*fd)
                bv['F-to-Z',o]+=m*F(n*s[1]-int(z[es].sum()),n*fd)
                for k in range(3):bv['Z-to-X',o,k]+=m*sum((F(int(z[e])-s[k],P+1+int(r[e])) for e in es),F())/n
        assert local==F(b['mass'])==b4[h][s]
    assert total==sum(d['H'] for d in data.values())==1
    for h,d in data.items():
        assert om[h]==d['own']
        assert all(bm[h][s]==eta for s,eta in b4[h].items())
    kindnames=('R-R','R-Z','Z-R','Z-Z');oldrows=[];literal=[];summary={}
    savedvalues={(r['kind'],json.dumps(r['orbit'])):F(r['slack']) for r in wit['audit']['old_rows']}
    for ki,kind in enumerate(kindnames):
        counts=Counter()
        for oi,members in enumerate(orbits):
            value=values[ki][oi];cl=saved_orbits[tuple(members)]['orbit']
            assert value==savedvalues[kind,json.dumps(cl)]
            oldrows.append(dict(kind=kind,orbit=cl,literal_queries=len(members),slack=str(value)))
            counts['positive' if value>0 else 'negative' if value<0 else 'zero']+=len(members)
            for e,f in members:literal.append(dict(kind=kind,source=ns[e],query=ns[f],slack=str(value)))
        summary[kind]=dict(queries=4356,**{k:counts[k] for k in ('positive','zero','negative')})
    savedb={json.dumps(r['query']):F(r['slack']) for r in wit['audit']['B4_rows']}
    brows=[]
    for k,v in sorted(bv.items()):
        assert v==savedb[json.dumps(k)];brows.append(dict(query=k,slack=str(v)))
    out=dict(point_sha256=digest(args.point),face_sha256=digest(args.face),atoms_sha256=digest(args.atoms),
             verifier_sha256=digest(Path(__file__)),domain_sha256=digest(args.domain_output),
             exact_face_verification='PASS',exact_atom_marginals_verification='PASS',
             upper_budget_orbits=42,nonself_upper_budget_orbits=39,saturated_nonself_orbits=3,saturated_literal_queries=600,
             permutation_orbit_action_counts=permutation_counts,true_prefix_checks=prefix_checks,
             stabilizer_edge_checks=edge_checks,implication_closure_entries=closure_checks,
             atom_zero_cell_checks=clause_checks,base_atoms=count,expanded_positive_atoms=720*count,
             unit_customer_scale=str(scale),unit_scale_digits=len(str(scale)),total_mass=str(total),
             old_query_summary=summary,B4_queries=15,B4_minimum_slack=str(min(bv.values())),
             all_B4_queries_strictly_positive=all(v>0 for v in bv.values()),
             full_old_plus_B4_completion=all(v>=0 for row in values for v in row) and all(v>=0 for v in bv.values()),
             old_orbit_rows=oldrows,B4_rows=brows,literal_old_queries=literal)
    args.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('old_orbit_rows','B4_rows','literal_old_queries','unit_customer_scale')}))

if __name__=='__main__':main()
