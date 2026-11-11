#!/usr/bin/env python3
"""Independent JSON-only audit: literal budgets, clipping, menus, and 513 columns.

Imports no generator or project code; reads only named JSON inputs in this folder.
No optimization, numerical candidate points, or outside project data are used.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from collections import Counter
from functools import lru_cache
from math import gcd, lcm
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent


def read(name):
    assert name.endswith('.json') and '/' not in name
    return json.loads((ROOT/name).read_text())


def encode(obj):
    assert not isinstance(obj,float)
    if isinstance(obj,Q):return str(obj)
    if isinstance(obj,dict):return {str(k):encode(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)):return [encode(v) for v in obj]
    return obj


def save(name,obj):
    (ROOT/name).write_text(json.dumps(encode(obj),ensure_ascii=False,indent=2)+'\n')


def scalar(xs,ys):
    return sum((x*y for x,y in zip(xs,ys)),Q(0))


def integer_rank(rows):
    """Fraction-free row elimination, independent of the generator's RREF."""
    a=[]
    for row in rows:
        denominator=lcm(*(Q(x).denominator for x in row))
        integer=[int(Q(x)*denominator) for x in row]
        g=gcd(*integer)
        a.append([x//g for x in integer] if g else integer)
    if not a:return 0
    r=0
    for c in range(len(a[0])):
        k=next((k for k in range(r,len(a)) if a[k][c]),None)
        if k is None:continue
        a[r],a[k]=a[k],a[r]
        for k in range(r+1,len(a)):
            if a[k][c]:
                aa,bb=a[r][c],a[k][c]
                a[k]=[aa*x-bb*y for x,y in zip(a[k],a[r])]
                g=gcd(*a[k])
                if g:a[k]=[x//g for x in a[k]]
        r+=1
        if r==len(a):break
    return r


def weights(source,point):
    internal=list(range(source+1,6))
    safe={j:Q(point[h]) for h,j in enumerate(internal)}
    caps={}
    for j in internal:
        amount=Q(1,10)+safe[j]
        for later in range(j+1,6):
            amount+=safe[later]/Q(5*(7-later)*(8-later))
        caps[j]=amount
    source_ic=Q(25)-Q(point[-1])
    for j in internal:source_ic+=safe[j]
    return safe,caps,source_ic


def literal_cost(source,p,tail,point,menu,outer=0,free_caps=None):
    """Pay each real player's share, cap, terminal query, and internal SAFE."""
    assert len(menu)==6 and len(tail)==6-source
    safe,caps,source_ic=weights(source,point)
    if free_caps is not None:caps=free_caps
    member={source:menu[outer]}
    member.update({source+h+1:bit for h,bit in enumerate(tail)})
    total=p+sum(member.values())
    payoff={j:Q(1,total) if member[j] else Q(0) for j in member}
    amount=source_ic*payoff[source]
    for j in safe:
        amount+=caps[j]*member[j]
        amount-=safe[j]*payoff[j]
    amount+=member[6]
    amount-=payoff[6]
    terminal_prefix=p+sum(member[j] for j in range(source,6))
    queries=[l for l in range(6) if l!=outer]
    amount+=sum((Q(menu[l],terminal_prefix+1) for l in queries),Q(0))/5
    for j in safe:
        actual_prefix=p+sum(member[h] for h in range(source,j))
        last_possible_load=actual_prefix+1+(6-j)
        amount+=safe[j]*sum((Q(menu[l],last_possible_load) for l in queries),Q(0))/5
    return amount


def canonical_menu(d,t):
    assert 0<=d-t<=5
    return (t,)+(1,)*(d-t)+(0,)*(5-d+t)


def anchor(source,p,point):
    safe,caps,_=weights(source,point)
    D=p+7-source
    S=Q(1)+sum(caps.values(),Q(0))
    return S+Q(24,D)-Q(point[-1])/min(D,5)


def extract_form(source,fn):
    dimension=6-source
    origin=tuple(Q(0) for _ in range(dimension))
    constant=fn(origin);coefficients=[]
    for axis in range(dimension):
        unit=list(origin);unit[axis]=Q(1)
        coefficients.append(fn(tuple(unit))-constant)
    return constant,tuple(coefficients)


def remainder(source,p,missing,last,point):
    tail=tuple(int(j not in missing) for j in range(source+1,6))+(last,)
    return literal_cost(source,p,tail,point,(1,0,0,0,0,0))-anchor(source,p,point)


def derive_constraints(source):
    dimension=6-source;internal=list(range(source+1,6));out=[]
    for axis,j in enumerate(internal):
        row=[Q(0)]*dimension;row[axis]=Q(-1)
        out.append({'id':f'tau{j}_nonnegative','normal':tuple(row),'rhs':Q(0),'state':None})
    def recover(name,p,missing,last,multiplier):
        constant,coefs=extract_form(source,lambda point:remainder(source,p,missing,last,point))
        out.append({'id':name,'normal':tuple(-multiplier*c for c in coefs),'rhs':multiplier*constant,'state':{'p':p,'missing':tuple(missing),'z':last,'rho_multiplier':multiplier}})
    recover('s_nonnegative',source-1,(),1,Q(30))
    if source>=2:recover('s_at_most_9',source-2,(),0,Q(20))
    for j in internal:recover(f'A{j}',source-1,(j,),1,Q(1))
    for j in internal:recover(f'B{j}',0 if source==1 else source-2,(j,),0 if source==1 else 1,Q(1))
    if source==1:
        for missing in combinations(internal,2):
            recover('PAIR_%d_%d'%missing,0,missing,1,Q(1))
    return out


def clip_domain(source,constraints):
    dimension=6-source
    upper=[Q(7,8)]*(dimension-1)+[Q(23 if source==1 else 9)]
    verts=set(product(*[(Q(0),u) for u in upper]))
    imposed=[]
    for axis,u in enumerate(upper):
        row=[Q(0)]*dimension;row[axis]=Q(-1)
        imposed.append((tuple(row),Q(0)))
        row=[Q(0)]*dimension;row[axis]=Q(1)
        imposed.append((tuple(row),u))
    stages=[]
    for constraint in constraints:
        normal,rhs=constraint['normal'],constraint['rhs']
        before=len(verts)
        slacks={v:rhs-scalar(normal,v) for v in verts}
        positive=[v for v in verts if slacks[v]>0]
        negative=[v for v in verts if slacks[v]<0]
        newverts={v for v in verts if slacks[v]>=0}
        crossing_edges=0;tested=0
        if negative:
            active={v:frozenset(k for k,(n,b) in enumerate(imposed) if scalar(n,v)==b) for v in verts}
            rank_cache={}
            for u in positive:
                for v in negative:
                    common=tuple(sorted(active[u]&active[v]))
                    if len(common)<dimension-1:continue
                    if common not in rank_cache:rank_cache[common]=integer_rank([imposed[k][0] for k in common])
                    tested+=1
                    if rank_cache[common]!=dimension-1:continue
                    crossing_edges+=1
                    fraction=slacks[u]/(slacks[u]-slacks[v])
                    w=tuple(a+fraction*(b-a) for a,b in zip(u,v))
                    assert scalar(normal,w)==rhs
                    assert all(scalar(n,w)<=b for n,b in imposed)
                    newverts.add(w)
        verts=newverts;imposed.append((normal,rhs))
        stages.append({'facet':constraint['id'],'before':before,'removed':len(negative),'crossing_edges':crossing_edges,'rank_tests':tested,'after':len(verts)})
    return verts,stages


def geometry(domains):
    all_checks=[];necessity=[];independent={};state_count=0
    serialized_forms=read('state_halfspaces.json')['forms']
    forms_by_key={(r['source'],r['p'],tuple(r['missing']),r['z']):r for r in serialized_forms}
    for domain in domains:
        source=domain['source'];dimension=6-source
        constraints=derive_constraints(source)
        assert len(constraints)==len(domain['facets'])
        for fresh,stored in zip(constraints,domain['facets']):
            assert fresh['id']==stored['id']
            assert fresh['normal']==tuple(map(Q,stored['normal']))
            assert fresh['rhs']==Q(stored['rhs'])
        verts,stages=clip_domain(source,constraints)
        expected={tuple(map(Q,v['parameters'])) for v in domain['vertices']}
        assert verts==expected,(source,verts-expected,expected-verts)
        independent[source]=verts
        interior=tuple(map(Q,domain['strict_interior_point']))
        assert all(scalar(c['normal'],interior)<c['rhs'] for c in constraints)
        rank_checks=[]
        for face in constraints:
            fv=[v for v in verts if scalar(face['normal'],v)==face['rhs']]
            base=fv[0]
            facet_rank=integer_rank([tuple(x-y for x,y in zip(v,base)) for v in fv[1:]])
            assert facet_rank==dimension-1
            center=tuple(sum((v[k] for v in fv),Q(0))/len(fv) for k in range(dimension))
            direction=face['normal']
            limits=[Q(1)]
            for other in constraints:
                if other['id']==face['id']:continue
                slack=other['rhs']-scalar(other['normal'],center)
                assert slack>0
                velocity=scalar(other['normal'],direction)
                if velocity>0:limits.append(slack/(2*velocity))
            # Keep the genuine source IC nonnegative in every facet witness.
            ic_normal=tuple([Q(-1)]*(dimension-1)+[Q(1)])
            velocity=scalar(ic_normal,direction)
            if velocity>0:limits.append((25-scalar(ic_normal,center))/(2*velocity))
            step=min(limits)
            witness=tuple(x+step*y for x,y in zip(center,direction))
            violated=[c['id'] for c in constraints if scalar(c['normal'],witness)>c['rhs']]
            assert violated==[face['id']]
            assert weights(source,witness)[2]>=0
            record={'source':source,'facet':face['id'],'facet_rank':facet_rank,'witness':witness,'only_candidate_facet_violated':face['id'],'violation':scalar(face['normal'],witness)-face['rhs'],'source_IC':weights(source,witness)[2]}
            if face['state'] is not None:
                st=face['state'];value=remainder(source,st['p'],st['missing'],st['z'],witness)
                assert value<0
                record.update({'necessary_true_state':st,'true_rho':value})
            necessity.append(record);rank_checks.append({'facet':face['id'],'rank':facet_rank})
        remainders_checked=0;lowest=None
        mids=list(range(source+1,6))
        for p in range(source):
            for size in range(len(mids)+1):
                for missing in combinations(mids,size):
                    for last in [0,1]:
                        constant,coefs=extract_form(source,lambda point:remainder(source,p,missing,last,point))
                        stored=forms_by_key[source,p,missing,last]
                        assert constant==Q(stored['constant']) and coefs==tuple(map(Q,stored['coefficients']))
                        vals=[]
                        for point in verts:
                            actual=remainder(source,p,missing,last,point)
                            assert actual==constant+scalar(coefs,point)
                            assert actual>=0
                            vals.append(actual);remainders_checked+=1
                        assert min(vals)==Q(stored['minimum_over_vertices'])
                        lowest=min(vals) if lowest is None else min(lowest,min(vals))
                        state_count+=1
        for point in verts:
            safe,caps,a=weights(source,point)
            assert a>=Q(2 if source==1 else 16)
            assert all(w>=0 for w in safe.values()) and all(w>=Q(1,10) for w in caps.values())
        all_checks.append({'source':source,'dimension':dimension,'recovered_facets':len(constraints),'independent_clipped_vertices':len(verts),'vertex_sets_identical':True,'clipping_stages':stages,'facet_rank_checks':rank_checks,'all_rho_vertex_checks':remainders_checked,'minimum_rho':lowest,'source_IC_legality_verified':True})
        print(f'literal geometry I{source}: {len(verts)} vertices and all rho verified',flush=True)
    assert state_count==len(serialized_forms)
    save('literal_geometry_checks.json',{'algorithm':'exact edge clipping from an analytically necessary bounding box; true-state-derived facets','sources':all_checks,'all_sets_equal':True,'all_rho_forms':state_count,'optimizer_calls':0})
    save('necessary_facet_witnesses.json',{'records':necessity,'every_facet_indispensable':True,'witnesses_are_local_affine_state_witnesses_not_full_SPE_realizations':True})
    return independent


def analytic_verification():
    raw=read('analytic_state_checks.json');t0=0;t1=0;minimal=0
    for rec in raw['t0_all_nonnegative_affine_remainders']:
        source,p=rec['source'],rec['p'];q=Q(rec['q']);tail=tuple(rec['tail'])
        menu=(0,1,0,0,0,0) if q else (0,0,0,0,0,0)
        empty=(0,)*(6-source)
        form=extract_form(source,lambda point:literal_cost(source,p,tail,point,menu)-literal_cost(source,p,empty,point,menu))
        assert form==(Q(rec['constant']),tuple(map(Q,rec['coefficients'])))
        assert form[0]>=0 and all(c>=0 for c in form[1])
        t0+=1
    for rec in raw['t1_query_slope_minus_anchor']:
        source,p=rec['source'],rec['p'];tail=tuple(rec['tail'])
        def diff(point):
            safe,_,_=weights(source,point)
            return (literal_cost(source,p,tail,point,(1,1,1,1,1,1))
                    -literal_cost(source,p,tail,point,(1,0,0,0,0,0))
                    -(1+sum(safe.values(),Q(0)))/Q(p+7-source))
        form=extract_form(source,diff)
        assert form==(Q(rec['constant']),tuple(map(Q,rec['coefficients'])))
        assert form[0]>=0 and all(c>=0 for c in form[1]);t1+=1
    minimal_records=[]
    for rec in raw['coordinate_minimal_caps']:
        source,j=rec['source'],rec['single_middle_member'];mids=list(range(source+1,6));dim=6-source
        point=tuple(Q(0) for _ in range(dim));empty=(0,)*(6-source)
        one=tuple(int(k==j) for k in mids)+(0,);menu=(0,1,0,0,0,0)
        def free_remainder(point,free):
            return literal_cost(source,0,one,point,menu,free_caps=free)-literal_cost(source,0,empty,point,menu,free_caps=free)
        no_caps={h:Q(0) for h in mids}
        c=free_remainder(point,no_caps);tau_coefs={};beta_coefs={}
        assert c==Q(-1,10)
        for axis,h in enumerate(mids):
            unit=list(point);unit[axis]=Q(1)
            tau_coefs[h]=free_remainder(tuple(unit),no_caps)-c
            required=Q(1) if h==j else Q(1,5*(7-h)*(8-h)) if h>j else Q(0)
            assert tau_coefs[h]==-required
            assert required==Q(rec['tau_coefficients'][str(h)])
            free=dict(no_caps);free[h]=Q(1)
            beta_coefs[h]=free_remainder(point,free)-c
            assert beta_coefs[h]==int(h==j)
        minimal_records.append({'source':source,'j':j,'constant':c,'tau_coefficients':tau_coefs,'free_beta_coefficients':beta_coefs,'exact_coordinate_minimum_reconstructed':True})
        minimal+=1
    identities=[]
    for menu in product([0,1],repeat=6):
        d=sum(menu)
        for outer in range(6):
            t=menu[outer]
            for denominator in range(1,7):
                actual=sum((Q(menu[l],denominator) for l in range(6) if l!=outer),Q(0))/5
                expected=Q(d-t,5*denominator)
                assert actual==expected
                identities.append({'menu':menu,'outer_index':outer+1,'denominator':denominator,'five_query_sum':actual})
    save('literal_analytic_checks.json',{'t0_nonnegative_affine_forms':t0,'t1_nonnegative_query_slope_forms':t1,'coordinate_minimal_cap_checks':minimal_records,'literal_five_query_fraction_identities':len(identities),'all_passed':True})
    save('literal_five_query_identities.json',identities)
    return {'t0_affine_forms':t0,'t1_slope_forms':t1,'minimal_caps':minimal,'five_query_identities':len(identities)}


def check_family(domains):
    family=read('exact_family.json');coordinates=read('coordinate_contract.json')
    cond=read('conditional_minimum_tables.json')['conditions'];hidden=read('hidden_state_checks.json')['records']
    outer=read('outer_average_tables.json');projection=read('union_projection_tables.json');menus=read('all_64_menu_checks.json')['records']
    cidx={(r['vertex_id'],r['p'],r['d'],r['t']):r for r in cond}
    hidx={(r['vertex_id'],r['p'],r['d'],r['t']):r for r in hidden}
    oidx={(r['vertex_id'],r['p'],r['d']):r for r in outer}
    pidx={(r['vertex_id'],r['p']):r for r in projection}
    midx={(r['vertex_id'],r['p'],tuple(r['menu'])):r for r in menus}
    assert len(cidx)==len(cond) and len(hidx)==len(hidden) and len(oidx)==len(outer) and len(pidx)==len(projection) and len(midx)==len(menus)
    rows_by_vertex={r['vertex_id']:r for r in family['rows']}
    assert len(rows_by_vertex)==len(family['rows'])==family['raw_row_count']
    assert family['variables']==513 and family['K_column']==512
    assert family['bit_order']==['a1','a2','a3','a4','a5','a6','x','o','c']
    assert family['numerical_positive_divisor']=='25' and family['no_C_size_equality']
    types=list(product([0,1],repeat=9))
    for column,bitvec in enumerate(types):
        assert coordinates['columns'][column]['column']==column
        assert coordinates['columns'][column]['bits']==list(bitvec)
        assert coordinates['columns'][column]['type_string']==''.join(map(str,bitvec))
    assert coordinates['columns'][512]=={'column':512,'kind':'independent_K'}
    counters=Counter();source_counts=[];max_tie=0;allrows=[];contexts=[]
    column_lines=['row\tcolumn\tliteral_raw_coefficient\tnumerical_coefficient_divided_by_25\tresidual']
    for domain in domains:
        source=domain['source'];tails=list(product([0,1],repeat=6-source));before=Counter(counters)
        for vertex in domain['vertices']:
            ident=vertex['id'];point=tuple(map(Q,vertex['parameters']));safe,caps,a=weights(source,point);S=1+sum(caps.values(),Q(0))
            row=rows_by_vertex[ident]
            assert row['source']==source and Q(row['source_IC_weight'])==a and Q(row['K_weight'])==S
            assert {int(j):Q(w) for j,w in row['middle_CAP_weights'].items()}==caps
            assert {int(j):Q(w) for j,w in row['tau_by_source'].items()}==safe
            assert Q(row['s'])==point[-1] and row['numerical_divisor']=='25' and not row['uses_C_size_equality']
            all_G={}
            for p in range(source):
                minimum={};f={};full_costs={}
                for d in range(7):
                    present=[0] if d==0 else [1] if d==6 else [0,1]
                    for t in present:
                        key=(ident,p,d,t);menu=canonical_menu(d,t)
                        costs=[literal_cost(source,p,tail,point,menu) for tail in tails]
                        full_costs[d,t]=costs;value=min(costs);minimum[d,t]=value
                        attaining=[tail for tail,cost in zip(tails,costs) if cost==value]
                        record=cidx[key];hrec=hidx[key]
                        assert Q(record['q'])==Q(d-t,5)
                        assert value==Q(record['minimum'])
                        assert attaining==[tuple(v) for v in record['all_minimizing_tails']]
                        assert costs==list(map(Q,hrec['all_tail_costs']))
                        assert [v-value for v in costs]==list(map(Q,hrec['all_tail_minus_minimum']))
                        assert all(v>=value for v in costs)
                        counters['hidden_states']+=len(tails);counters['physical_condition_minima']+=1
                        counters['all_tied_tail_occurrences']+=len(attaining);max_tie=max(max_tie,len(attaining))
                    if d==0:value=minimum[0,0]
                    elif d==6:value=minimum[6,1]
                    else:value=((6-d)*minimum[d,0]+d*minimum[d,1])/6
                    f[d]=value;assert value==Q(oidx[ident,p,d]['f']);counters['outer_averages']+=1
                G=min(f[d] for d in range(1,7));all_G[p]=G
                Z=literal_cost(source,p,(0,)*(6-source),point,(0,1,0,0,0,0))
                W=anchor(source,p,point);D=p+7-source
                anchortail=(1,)*(5-source)+(int(D<=5),)
                assert literal_cost(source,p,anchortail,point,(1,0,0,0,0,0))==W
                assert minimum[1,0]==Z and minimum[1,1]==W and f[0]==0
                assert G==(5*Z+W)/6
                assert [d for d in range(1,7) if f[d]==G]==[1]
                tau_sum=sum(safe.values(),Q(0))
                analytic_gap_bound=Q(3,5)+Q(33,20)*tau_sum if source==1 else 3+Q(5-source,10)+Q(9,10)*tau_sum
                assert W-Z>=analytic_gap_bound>0
                for d in range(2,7):assert f[d]-G>=Q(d-1,6)*(W-Z)>0
                for d in range(1,7):assert minimum[d,1]==W+(1+tau_sum)*Q(d-1,5*D)
                pr=pidx[ident,p]
                assert (Z,W,G)==tuple(Q(pr[k]) for k in ['Z','W','G'])
                assert Q(row['G_by_prefix_load'][str(p)])==G
                closed=(S+Q(24,D)-point[-1]/min(D,5)+Q(1,p+1)+sum((safe[j]/(p+7-j) for j in safe),Q(0)))/6
                assert G==closed
                counters['G_contexts']+=1
                contexts.append({'vertex_id':ident,'p':p,'Z':Z,'W':W,'W_minus_Z':W-Z,'analytic_W_minus_Z_lower_bound':analytic_gap_bound,'G':G,'all_d_gaps':[f[d]-G for d in range(1,7)]})
                for menu in product([0,1],repeat=6):
                    d=sum(menu);means=[];outer_terms=[]
                    for k in range(6):
                        actual_membership=sum((Q(menu[l]) for l in range(6) if l!=k),Q(0))/5
                        assert actual_membership==Q(d-menu[k],5)
                        means.append(actual_membership);outer_terms.append(minimum[d,menu[k]])
                        # Evaluate one independently chosen attaining tail with the actual
                        # menu indices, after all denominators have passed the identities.
                        costs=full_costs[d,menu[k]];chosen=tails[costs.index(minimum[d,menu[k]])]
                        assert literal_cost(source,p,chosen,point,menu,k)==minimum[d,menu[k]]
                        counters['actual_menu_attaining_costs']+=1
                    avg=sum(outer_terms,Q(0))/6
                    remainder_value=avg-(G if d else 0)
                    assert avg==f[d] and remainder_value>=0
                    mr=midx[ident,p,menu]
                    assert means==list(map(Q,mr['inner_five_means']))
                    assert outer_terms==list(map(Q,mr['six_conditional_minima']))
                    assert avg==Q(mr['outer_average']) and remainder_value==Q(mr['union_projection_remainder'])
                    counters['menu_contexts']+=1;counters['literal_inner_five_means']+=6
            raw=[]
            assert set(row['a'])=={str(c) for c in range(513)}
            for column,bitvec in enumerate(types):
                membership=bitvec[:6];load=sum(membership)
                actual_payoffs=[Q(1,load) if member else Q(0) for member in membership]
                prefix=sum(membership[:source-1]);union=bitvec[7]
                value=a*actual_payoffs[source-1]-union*all_G[prefix]
                assert value==Q(row['a'][str(column)])
                raw.append(value)
                column_lines.append(f'{row["name"]}\t{column}\t{value}\t{value/25}\t0')
                counters['full_row_coefficients']+=1
            assert Q(row['a']['512'])==S
            raw.append(S);column_lines.append(f'{row["name"]}\t512\t{S}\t{S/25}\t0')
            counters['full_row_coefficients']+=1;counters['rows']+=1
            allrows.append((row['name'],tuple(raw)))
        source_counts.append({'source':source,**dict(counters-before)})
        print(f'literal family I{source}: all states, ties, 64 menus, and 513 columns passed',flush=True)
    assert counters['physical_condition_minima']==len(cond)==len(hidden)
    assert counters['outer_averages']==len(outer) and counters['G_contexts']==len(projection) and counters['menu_contexts']==len(menus)
    expected=read('derivation_result.json')
    for field in ['rows','full_row_coefficients','hidden_states','physical_condition_minima','outer_averages','G_contexts','menu_contexts','literal_inner_five_means','all_tied_tail_occurrences']:
        assert counters[field]==expected[field]
    counts=Counter(values for name,values in allrows)
    dup=read('raw_duplicate_report.json')
    assert len(counts)==dup['distinct_exact_rows']
    assert len(allrows)==dup['raw_rows'] and dup['deleted_rows']==0
    save('literal_domain_checks.json',{'contexts':contexts,'continuous_gap_bounds_checked_at_all_vertices':True,'continuous_validity_comes_from_analytic_proof_not_only_vertex_testing':True})
    (ROOT/'full_column_checks.tsv').write_text('\n'.join(column_lines)+'\n')
    return {'status':'PASS','sources':source_counts,**dict(counters),'largest_tie_set':max_tie,'all_513_columns_exact':True,'all_vertex_rows_retained':True,'exact_duplicate_rows':sum(v-1 for v in counts.values()),'no_C_equality':True,'generator_imported_or_executed':False,'input_files_all_local_JSON':True,'optimizer_calls':0,'LP_points_read':0}


if __name__=='__main__':
    domains=read('parameter_domains.json')['domains']
    geometry(domains)
    analytic=analytic_verification()
    result=check_family(domains)
    result['analytic']=analytic
    save('literal_checker_output.json',result)
    print(json.dumps(result,ensure_ascii=False),flush=True)
