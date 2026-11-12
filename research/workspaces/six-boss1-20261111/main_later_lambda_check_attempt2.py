"""Main independent entire later-source lambda domains, true minima, 550 rows."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
from hashlib import sha256
from math import gcd, lcm, comb
import json
from main_minimal_caps_complete_check import cost, rank, solve

W=Path(__file__).resolve().parent
P=W/'later_sources_lambda_cells'
ATOMS=list(product((0,1),repeat=9))


def read(p): return json.loads(p.read_text())
def sha(p): return sha256(p.read_bytes()).hexdigest()
def ev(form,x): return form[0]+sum((a*b for a,b in zip(form[1:],x)),F(0))


def primitive(form):
    den=lcm(*(v.denominator for v in form));ints=[int(v*den) for v in form]
    common=gcd(*ints)
    return tuple(v//common for v in ints) if common else tuple(ints)


def weights(i,q0,x):
    tau={j:x[j-i-1] for j in range(i+1,6)}
    beta={j:q0/2+tau[j]+sum((q0*tau[l]/((7-l)*(8-l)) for l in tau if l>j),F(0)) for j in tau}
    return tau,beta,x[-1]+sum(tau.values()),1+sum(beta.values())


def build_planes(i,q0,lo,hi):
    dim=6-i;basis=[(F(0),)*dim]+[tuple(F(k==j) for k in range(dim)) for j in range(dim)]
    forms=[];mid=(lo+hi)/2
    for p in range(i):
        D=p+7-i;anchor_z=int(mid>(D-1)**2)
        for tail in product((0,1),repeat=6-i):
            values=[]
            for x in basis:
                tau,beta,a,S=weights(i,q0,x)
                w=1+(x[-1]-1)/D if anchor_z else x[-1]/(D-1)
                values.append(cost(i,p,1,F(0),tail,tau,beta,a)-(S-1+w))
            forms.append(primitive([values[0]]+[v-values[0] for v in values[1:]]))
    for j in range(dim-1):
        forms.append((0,)+tuple(int(k==j) for k in range(dim)))
    forms += [primitive([-lo]+[F(0)]*(dim-1)+[F(1)]),primitive([hi]+[F(0)]*(dim-1)+[F(-1)])]
    return sorted(set(forms))


def main():
    out=W/'main_later_lambda_check.json';assert not out.exists()
    assert sha(P/'proof.md')=='5dfb6e1ed29cd2955461bc15f8184246230de302ef43b6755c907c1b4173195a'
    assert sha(P/'exact_family.json')=='22fb5d0f5af953ac6a7c74faadca5ab9ba5703e30d83445b27085a26900de0e6'
    domains=read(P/'parameter_domains.json')['cells']
    family=read(P/'exact_family.json')['rows']
    vertices={};minima={};gs={};geometry=[]
    states=tables=ties=menus=cols=combos=0
    for cell in domains:
        i=cell['source'];q0=F(cell['q0']);lo,hi=map(F,cell['window']);dim=6-i
        pl=build_planes(i,q0,lo,hi)
        assert set(pl)=={tuple(h['primitive_form']) for h in cell['halfspaces']}
        nonconstant=[h for h in pl if any(h[1:])]
        candidates=set()
        for basis in combinations(nonconstant,dim):
            x=solve([(F(h[0]),tuple(map(F,h[1:]))) for h in basis]);combos+=1
            if x is not None and all(ev(h,x)>=0 for h in pl): candidates.add(x)
        supplied={v['id']:tuple(map(F,v['coordinates'])) for v in cell['vertices']}
        assert candidates==set(supplied.values())
        facets=set()
        for h in nonconstant:
            on=[x for x in candidates if ev(h,x)==0]
            if on and rank([[a-b for a,b in zip(x,on[0])] for x in on[1:]])==dim-1:facets.add(h)
        assert facets=={tuple(h['primitive_form']) for h in cell['facets']}
        assert all(ev(h,tuple(map(F,cell['strict_interior_point'])))>0 for h in facets)
        geometry.append({'cell':cell['id'],'facets':len(facets),'vertices':len(candidates),'raw_primitive_planes':len(pl)})
        for vid,x in supplied.items():
            vertices[vid]=(i,q0,x)
            tau,beta,a,S=weights(i,q0,x);assert a>=0 and min(beta.values(),default=F(0))>=0
            for p in range(i):
                D=p+7-i;ww=min(x[-1]/(D-1),1+(x[-1]-1)/D);Wv=S-1+ww
                Zv=q0*(F(1,p+1)+sum((tau[j]/(p+7-j) for j in tau),F(0)))
                conditions=([(t,F(d,6)) for t in [0,1] for d in range(7)] if q0==F(1,6)
                            else [(0,F(d,5)) for d in range(6)]+[(1,F(d-1,5)) for d in range(1,7)])
                for t,q in conditions:
                    vals=[cost(i,p,t,q,tail,tau,beta,a) for tail in product((0,1),repeat=6-i)]
                    mv=min(vals);minima[vid,p,t,q]=mv;states+=len(vals);tables+=1;ties+=vals.count(mv)
                    if t:assert mv==Wv+(1+sum(tau.values()))*q/D
                    elif q in [F(0),q0]:assert mv==(Zv if q else F(0))
                if q0==F(1,5):
                    fs={d:((6-d)*minima[vid,p,0,F(d,5)] if d<6 else F(0))/6
                           +(d*minima[vid,p,1,F(d-1,5)] if d>0 else F(0))/6 for d in range(7)}
                    G=(5*Zv+Wv)/6
                    assert fs[0]==0 and fs[1]==G and all(fs[d]>G for d in range(2,7))
                    gs[vid,p]=G
                    for menu in product((0,1),repeat=6):
                        d=sum(menu);val=sum((minima[vid,p,t,F(d-t,5)] for t in menu),F(0))/6
                        assert val==fs[d] and val>=bool(d)*G;menus+=1
    for k,row in enumerate(family):
        vid=row['vertex_id'];i,q0,x=vertices[vid];tau,beta,a,S=weights(i,q0,x)
        assert row['raw_row_index']==k and F(row['source_IC_weight'])==a and F(row['numeric_positive_divisor'])==25
        assert F(row['rhs'])==0 and F(row['terminal_CAP_weight'])==F(row['terminal_query_average_weight'])==1
        assert {int(j):F(v) for j,v in row['middle_CAP_weights'].items()}==beta
        conly=row['kind']=='six_C_only';ordered=row['kind']=='ordered_five'
        if not ordered:
            T=row['forced_target'];ti=int(T[1:])-1 if T.startswith('A') else {'X':6,'C':8}[T]
        for h in range(513):
            if h==512:val=S-(S-1 if conly else 0)
            else:
                bits=ATOMS[h];p=sum(bits[:i-1]);load_=sum(bits[:6]);ui=F(bits[i-1],load_) if load_ else F(0)
                val=a*ui-(bits[7]*gs[vid,p] if ordered else minima[vid,p,bits[ti],q0*bits[7]])
                if conly:val+=(S-1)*bits[8]
            assert val==F(row['a'].get(str(h),'0')),(row['id'],h)
            cols+=1
        assert F(row['free_C_equality_multiplier'])==(S-1 if conly else 0)
    assert len(domains)==24 and len(vertices)==110 and sum(x['facets'] for x in geometry)==96
    assert len(family)==550 and cols==282150
    report={'status':'PASS_MAIN_LATER_LAMBDA_COMPLETE_DOMAINS_TRUE_STATES_AND_550_FULL_ROWS',
            'optimizer_calls':0,'candidate_points_read':0,'domain_cells':24,'facet_count':96,'vertex_window_occurrences':110,
            'complete_boundary_combinations':combos,'geometry':geometry,'true_state_costs':states,'physical_minimum_tables':tables,
            'all_weak_minimum_occurrences':ties,'ordered_full_menus':menus,'raw_rows':550,'full_column_checks':cols,
            'proof_personally_read_complete':True,'proof_sha256':sha(P/'proof.md'),'family_sha256':sha(P/'exact_family.json'),
            'manifest_sha256':sha(P/'freeze_manifest.json'),'main_elementary_routines_sha256':sha(W/'main_minimal_caps_complete_check.py'),
            'scope':'Specified complete true-budget anchor domains over lambda in [0,25], with all raw window duplicates. No LP improvement or SPE construction.'}
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['geometry','scope']},ensure_ascii=False))


if __name__=='__main__':main()
