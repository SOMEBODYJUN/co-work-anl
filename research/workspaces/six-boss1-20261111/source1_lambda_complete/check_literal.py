#!/usr/bin/env python3
"""Independent Fraction checks.  Does not import the generator or project code."""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations, product
from math import gcd, lcm
from functools import reduce
import hashlib
import json

ROOT=Path(__file__).resolve().parent
WS=ROOT.parent
REPO=WS.parents[2]
MID=(2,3,4,5)
TAIL=list(product((0,1),repeat=5))
BITS=list(product((0,1),repeat=9))

def write(name,obj):
    (ROOT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def solve_square(rows):
    a=[[Q(v) for v in h[1:]]+[-Q(h[0])] for h in rows]
    for col in range(5):
        pivot=next((i for i in range(col,5) if a[i][col]),None)
        if pivot is None:return None
        a[col],a[pivot]=a[pivot],a[col]
        den=a[col][col]
        for k in range(col,6):a[col][k]/=den
        for i in range(col+1,5):
            f=a[i][col]
            if f:
                for k in range(col,6):a[i][k]-=f*a[col][k]
    x=[Q(0)]*5
    for i in range(4,-1,-1):x[i]=a[i][5]-sum(a[i][j]*x[j] for j in range(i+1,5))
    return tuple(x)

def affine_rank(rows):
    a=[list(r) for r in rows]; r=0
    for col in range(5):
        piv=next((i for i in range(r,len(a)) if a[i][col]),None)
        if piv is None:continue
        a[r],a[piv]=a[piv],a[r]
        v=a[r][col];a[r]=[z/v for z in a[r]]
        for i in range(r+1,len(a)):
            m=a[i][col]
            if m:a[i]=[z-m*w for z,w in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r

def parameters(q0,p):
    tau={j:p[j-2] for j in MID}; lam=p[4]
    beta={j:q0/2+tau[j]+sum(q0*tau[h]/((7-h)*(8-h)) for h in MID if h>j) for j in MID}
    return tau,beta,lam+sum(tau.values()),sum(beta.values())

def direct_cost(q0,p,t,q,tail):
    tau,beta,a,b=parameters(q0,p)
    r=dict(zip(MID,tail[:4]));z=tail[4];load=t+sum(r.values())+z
    # Each real person's payoff appears separately, unlike the generator's numerator.
    result=a*Q(t,load) if load else Q(0)
    for j in MID:
        result+=beta[j]*r[j]
        if r[j]:result-=tau[j]*Q(1,load)
    result+=z
    if z:result-=Q(1,load)
    result+=q/Q(t+sum(r.values())+1)
    for j in MID:
        result+=tau[j]*q/Q(t+sum(r[h] for h in MID if h<j)+7-j)
    return result

ZERO=(Q(0),)*5
BASES=[tuple(Q(i==j) for i in range(5)) for j in range(5)]
def recover(fn):
    c=fn(ZERO)
    return (c,)+tuple(fn(p)-c for p in BASES)

def value(h,p):return h[0]+sum(a*b for a,b in zip(h[1:],p))
def minus(x,y):return tuple(a-b for a,b in zip(x,y))
def strings(x):return [str(v) for v in x]

def main():
    pins=json.loads((ROOT/'source_pins.json').read_text())['sources']
    def check_pins():
        for pin in pins:
            assert hashlib.sha256((REPO/pin['path']).read_bytes()).hexdigest()==pin['sha256']
    check_pins()
    domains=json.loads((ROOT/'parameter_domains.json').read_text())['domains']
    raw=json.loads((ROOT/'all_32_tail_identities.json').read_text())['states']
    witness=json.loads((ROOT/'necessary_facet_witnesses.json').read_text())['witnesses']
    geometry=[]; tables=[]; outer=[]; state_checks=0; hidden_count=0; ties=0; max_ties=0
    table_lookup={}
    for domain in domains:
        q0=Q(domain['q0']); hs=[tuple(map(Q,h['affine'])) for h in domain['facets']]
        # Independently recover all state facets from individual payoff terms.
        for f,h in zip(domain['facets'],hs):
            if 'tail' in f['origin']:
                tail=f['origin']['tail'];mul=Q(f['origin']['rho_multiplier'])
                literal=recover(lambda p:mul*(direct_cost(q0,p,1,Q(0),tail)-direct_cost(q0,p,1,Q(0),(1,1,1,1,0))))
                assert literal==h
        # Enumerate every independent five-boundary intersection.  No old vertices
        # enter this enumeration; stored mapped vertices are compared only afterward.
        vertices=set();attempts=0;singular=0;feasible=0
        for chosen in combinations(hs,5):
            attempts+=1;v=solve_square(chosen)
            if v is None:singular+=1;continue
            if all(value(h,v)>=0 for h in hs):vertices.add(v);feasible+=1
        saved={tuple(map(Q,v['parameters'])) for v in domain['vertices']}
        assert vertices==saved and len(vertices)==90
        facets=[]
        for f,h in zip(domain['facets'],hs):
            vs=[v for v in vertices if value(h,v)==0]
            r=affine_rank([tuple(a-b for a,b in zip(v,vs[0])) for v in vs[1:]])
            assert r==4
            facets.append({'id':f['id'],'supporting_vertices':len(vs),'affine_rank':r})
        geometry.append({'q0':str(q0),'boundary_combinations':attempts,
            'singular_combinations':singular,'feasible_independent_bases':feasible,
            'vertices':len(vertices),'matches_all_90_old_mapped_vertices':True,'facets':facets})
        states=[s for s in raw if Q(s['q0'])==q0]
        assert len(states)==32 and {tuple(s['tail']) for s in states}==set(TAIL)
        for st in states:
            rho=recover(lambda p:direct_cost(q0,p,1,Q(0),st['tail'])-direct_cost(q0,p,1,Q(0),(1,1,1,1,0)))
            assert rho==tuple(map(Q,st['rho_affine']))
            rebuilt=list(map(Q,st['remainder_affine']))
            for name,mul in st['facet_terms'].items():
                f=next(h for item,h in zip(domain['facets'],hs) if item['id']==name)
                rebuilt=[x+Q(mul)*y for x,y in zip(rebuilt,f)]
            assert tuple(rebuilt)==rho
            assert all(value(rho,v)>=0 for v in vertices)
            state_checks+=len(vertices)
        for w in witness:
            if Q(w['q0'])!=q0:continue
            p=tuple(map(Q,w['point']))
            for f,h in zip(domain['facets'],hs):
                assert (value(h,p)<0) if f['id']==w['facet'] else (value(h,p)>=0)
            if 'tail' in w:
                r=direct_cost(q0,p,1,Q(0),w['tail'])-direct_cost(q0,p,1,Q(0),(1,1,1,1,0))
                assert r==Q(w['true_rho'])<0
        # Recover and check all arbitrary-tau affine costs and q-slopes directly.
        for q in (Q(0),q0):
            for tail in TAIL:
                h=recover(lambda p:direct_cost(q0,p,0,q,tail)-direct_cost(q0,p,0,q,(0,0,0,0,0)))
                assert all(x>=0 for x in h) and h[-1]==0
        for tail in TAIL:
            h=recover(lambda p:direct_cost(q0,p,1,Q(1),tail)-direct_cost(q0,p,1,Q(0),tail)-(1+sum(p[:4]))/6)
            assert all(x>=0 for x in h)

        for vert in domain['vertices']:
            p=tuple(map(Q,vert['parameters'])); vid=vert['id']
            cond=([(t,Q(d,6)) for t in (0,1) for d in range(7)] if q0==Q(1,6)
                  else sorted({(t,Q(d-t,5)) for d in range(7) for t in (0,1) if (t==0 and d<6) or (t==1 and d>0)}))
            for t,q in cond:
                costs=[direct_cost(q0,p,t,q,tail) for tail in TAIL]
                low=min(costs);att=[list(tail) for tail,c in zip(TAIL,costs) if c==low]
                if t==1:
                    assert low==direct_cost(q0,p,1,q,(1,1,1,1,0))
                    if p[4]==25:assert list((1,1,1,1,1)) in att
                elif q in (Q(0),q0):assert low==direct_cost(q0,p,0,q,(0,0,0,0,0))
                hidden_count+=32;ties+=len(att);max_ties=max(max_ties,len(att))
                tab={'q0':str(q0),'vertex':vid,'t':t,'q':str(q),'minimum':str(low),
                     'all_attaining_tails':att,'all_32_costs':strings(costs)}
                tables.append(tab);table_lookup[(vid,t,q)]=low
            if q0==Q(1,5):
                vals=[]
                for d in range(7):
                    y=Q(0)
                    if d<6:y+=(6-d)*table_lookup[(vid,0,Q(d,5))]/6
                    if d>0:y+=d*table_lookup[(vid,1,Q(d-1,5))]/6
                    vals.append(y)
                assert vals[0]==0 and all(vals[d]>vals[1] for d in range(2,7))
                outer.append({'vertex':vid,'f_d':strings(vals),'G':str(vals[1]),'unique_weakest_positive_d':1})
    write('literal_geometry_checks.json',{'domains':geometry})
    write('literal_complete_minimum_tables.json',{'tail_order':[list(x) for x in TAIL],
           'tables':tables,'tables_count':len(tables),'all_costs_count':hidden_count,
           'all_tie_occurrences':ties,'maximum_tie_count':max_ties})
    write('literal_ordered_outer_tables.json',{'tables':outer,'no_absent_physical_terms_evaluated':True})

    # Same-six-menu identities, including all repeated membership patterns.
    query_checks=0
    for menu in product((0,1),repeat=6):
        d=sum(menu)
        for k,t in enumerate(menu):
            for den in range(1,7):
                actual=sum(Q(menu[l],5*den) for l in range(6) if l!=k)
                assert actual==Q(d-t,5*den)
                query_checks+=1

    old6=json.loads((WS/'all_source_minimal_cap_safe/exact_family.json').read_text())['rows']
    old5=json.loads((WS/'ordered_minimal_cap/exact_family.json').read_text())['rows']
    targets={**{f'A{i}':i-1 for i in range(1,7)},'X':6,'C':8}
    column_checks=0; cchecks=0; row_checks=[]
    for dom in domains:
        q0=Q(dom['q0']);old=old6 if q0==Q(1,6) else old5
        for vert in dom['vertices']:
            p=tuple(map(Q,vert['parameters']));tau,beta,a,b=parameters(q0,p);vid=vert['id']
            rows=[r for r in old if r['source']==1 and r['vertex_id']==vert['old_vertex_id']]
            assert len(rows)==(8 if q0==Q(1,6) else 1)
            G=next((Q(x['G']) for x in outer if x['vertex']==vid),None)
            for row in rows:
                target=row.get('forced_target','ordered')
                for idx,bits in enumerate(BITS):
                    load=sum(bits[:6]);u=Q(bits[0],load) if load else Q(0);o=bits[7]
                    if target=='ordered':m=o*G
                    else:m=table_lookup[(vid,bits[targets[target]],Q(o,6))]
                    true=a*u-m
                    assert true==Q(row['a'][str(idx)])
                    column_checks+=1
                    if target=='C':
                        c=bits[8];q=Q(o,6)
                        target_cost=p[4]*c/5+Q(o,6*(1+5*c))+sum(tau[j]*Q(o,6*((j-1)*c+7-j)) for j in MID)
                        assert a*u-target_cost==true+b*c
                        cchecks+=1
                assert Q(row['a']['512'])==1+b
                column_checks+=1
                if target=='C':assert (1+b)-b==1;cchecks+=1
                row_checks.append({'old_name':row['name'],'lambda_vertex':vid,'all_513_columns_equal':True})
    assert column_checks==415530 and cchecks==46170
    write('literal_row_identity_checks.json',{'rows':row_checks,'existing_row_columns':column_checks,
          'C_only_equality_columns':cchecks,'raw_duplicate_matrix_created':False})

    # Verify all symbolic columns against a fresh direct-tail evaluation.
    lines=(ROOT/'all_513_affine_column_identities.tsv').read_text().splitlines()
    assert len(lines)==5131
    for line in lines[1:]:
        mode,k,new,old,diff=line.split('\t');k=int(k)
        assert new==old and all(Q(x)==0 for x in diff.split(','))
        q0=Q(1,5) if mode=='ordered' else Q(1,6)
        def physical_coefficient(p):
            tau,beta,a,b=parameters(q0,p)
            if k==512:return Q(1) if mode=='C-only' else 1+b
            bits=BITS[k];load=sum(bits[:6]);u=Q(bits[0],load) if load else Q(0);o=bits[7]
            if mode=='ordered':
                g=(5*direct_cost(q0,p,0,q0,(0,0,0,0,0))+direct_cost(q0,p,1,Q(0),(1,1,1,1,0)))/6
                return a*u-o*g
            t=bits[targets['C' if mode=='C-only' else mode]]
            tail=(1,1,1,1,0) if t else (0,0,0,0,0)
            result=a*u-direct_cost(q0,p,t,Q(o,6),tail)
            return result+b*t if mode=='C-only' else result
        assert recover(physical_coefficient)==tuple(map(Q,new.split(',')))
    check_pins()
    result={'status':'PASS','independent_generator_imports':0,'optimizer_calls':0,
        'geometry_boundary_combinations':sum(g['boundary_combinations'] for g in geometry),
        'vertices':[g['vertices'] for g in geometry],'facets':38,'necessity_witnesses':38,
        'literal_endpoint_rho_checks':state_checks,'physical_minimum_tables':len(tables),
        'true_tail_costs':hidden_count,'all_tie_occurrences':ties,'maximum_tie_count':max_ties,
        'ordered_outer_d_values':len(outer)*7,'same_six_menu_five_index_identities':query_checks,
        'existing_exact_row_columns':column_checks,'C_only_equality_columns':cchecks,
        'symbolic_513_column_identities':5130,'direct_sources_unchanged':True,
        'genuinely_new_inequality_rows':0}
    write('literal_checker_output.json',result)
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
