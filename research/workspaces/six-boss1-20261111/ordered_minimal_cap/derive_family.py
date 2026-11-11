#!/usr/bin/env python3
"""Exact q0=1/5 ordered-menu minimal-cap family. No optimization or LP input.

Writes only beside this file. The source formulas are reconstructed here;
check_literal.py must not import this module or any other project Python file.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
from math import comb
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
Q0 = F(1, 5)


def js(value):
    assert not isinstance(value, float), 'Floating point is forbidden in exact artifacts'
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): js(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [js(v) for v in value]
    return value


def write(name, obj):
    (HERE / name).write_text(json.dumps(js(obj), ensure_ascii=False, indent=2) + '\n')


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def rank(rows):
    if not rows:
        return 0
    a = [list(row) for row in rows]
    r = 0
    for c in range(len(a[0])):
        pivot = next((k for k in range(r, len(a)) if a[k][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        v = a[r][c]
        a[r] = [x/v for x in a[r]]
        for k in range(r+1, len(a)):
            v = a[k][c]
            if v:
                a[k] = [x-v*y for x, y in zip(a[k], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def solve(rows, rhs):
    n = len(rows)
    a = [list(row)+[b] for row, b in zip(rows, rhs)]
    for c in range(n):
        pivot = next((k for k in range(c, n) if a[k][c]), None)
        if pivot is None:
            return None
        a[c], a[pivot] = a[pivot], a[c]
        v = a[c][c]
        a[c] = [x/v for x in a[c]]
        for k in range(n):
            if k == c:
                continue
            v = a[k][c]
            if v:
                a[k] = [x-v*y for x, y in zip(a[k], a[c])]
    return tuple(row[-1] for row in a)


def cap(i, point):
    mids = list(range(i+1, 6))
    tau = dict(zip(mids, point[:-1]))
    beta = {j: F(1,10)+tau[j]+sum((tau[l]/(5*(7-l)*(8-l)) for l in mids if l>j), F(0)) for j in mids}
    return tau, beta, 1+sum(beta.values(), F(0)), 25+sum(tau.values(), F(0))-point[-1]


def faces(i):
    mids = list(range(i+1,6))
    dim = 6-i
    ans = []
    def add(name, normal, rhs, witness=None):
        ans.append({'id':name,'normal':tuple(map(F,normal)),'rhs':F(rhs),'necessary_state':witness})
    for h,j in enumerate(mids):
        v=[F(0)]*dim; v[h]=-1
        add('tau%d_nonnegative'%j,v,0,{'kind':'wallet_weight'})
    v=[F(0)]*dim; v[-1]=-1
    add('s_nonnegative',v,0,{'p':i-1,'missing':[],'z':1,'rho_equals_slack_times':'1/30'})
    if i>=2:
        v=[F(0)]*dim;v[-1]=1
        add('s_at_most_9',v,9,{'p':i-2,'missing':[],'z':0,'rho_equals_slack_times':'1/20'})
    for h,j in enumerate(mids):
        v=[F(0)]*dim;v[h]=F(4,5)
        for e,l in enumerate(mids):
            if l>j:v[e]=F(1,5*(7-l)*(8-l))
        add('A%d'%j,v,F(7,10),{'p':i-1,'missing':[j],'z':1,'rho_equals_slack_times':'1'})
    for h,j in enumerate(mids):
        v=[F(0)]*dim;v[h]=F(3,4);v[-1]=F(1,20)
        for e,l in enumerate(mids):
            if l>j:v[e]=F(1,5*(7-l)*(8-l))
        add('B%d'%j,v,F(23,20) if i==1 else F(11,10),{'p':0 if i==1 else i-2,'missing':[j],'z':0 if i==1 else 1,'rho_equals_slack_times':'1'})
    if i==1:
        for missing in combinations(mids,2):
            v=[F(0)]*dim;v[-1]=F(1,20)
            for e,l in enumerate(mids):
                if l in missing:v[e]+=F(3,4)
                for j in missing:
                    if l>j:v[e]+=F(1,5*(7-l)*(8-l))
            add('PAIR_%d_%d'%missing,v,F(9,5),{'p':0,'missing':list(missing),'z':1,'rho_equals_slack_times':'1'})
    return ans


def affine(i, fn):
    dim=6-i
    zero=(F(0),)*dim
    constant=fn(zero)
    coefficients=[]
    for j in range(dim):
        point=list(zero);point[j]=F(1)
        coefficients.append(fn(tuple(point))-constant)
    return {'constant':constant,'coefficients':coefficients}


def evaluate(form, point):
    return form['constant']+dot(form['coefficients'],point)


def rho(i,p,missing,z,point):
    tau,beta,S,a=cap(i,point)
    D=p+7-i
    L=D-1-len(missing)+z
    assert L>0
    return ((25-point[-1]-z+sum((tau[j] for j in missing),F(0)))/L
            +z-1-sum((beta[j] for j in missing),F(0))-F(24,D)+point[-1]/min(D,5))


def psi(i,p,t,q,tail,point):
    tau,beta,S,a=cap(i,point)
    mids=list(tau)
    middle=dict(zip(mids,tail[:-1]));z=tail[-1]
    L=p+t+sum(tail)
    numerator=a*t-z-sum((tau[j]*middle[j] for j in mids),F(0))
    assert L or numerator==0
    return ((numerator/L if L else F(0))+dot(list(beta.values()),tail[:-1])+z
            +q/(p+t+sum(tail[:-1])+1)
            +sum((tau[j]*q/(p+t+sum(middle[h] for h in mids if h<j)+7-j) for j in mids),F(0)))


def z_anchor(i,p,point):
    tau,_,_,_=cap(i,point)
    return Q0*(F(1,p+1)+sum((tau[j]/(p+7-j) for j in tau),F(0)))


def w_anchor(i,p,point):
    _,_,S,_=cap(i,point)
    D=p+7-i
    return S+F(24,D)-point[-1]/min(D,5)


def g_closed(i,p,point):
    return (5*z_anchor(i,p,point)+w_anchor(i,p,point))/6


def enumerate_geometry():
    domains=[];state_forms=[];counts=[]
    for i in range(1,6):
        fs=faces(i);dim=6-i;mids=list(range(i+1,6))
        combinations_count=0;singular=0;feasible_bases=0;vs={}
        for chosen in combinations(range(len(fs)),dim):
            combinations_count+=1
            point=solve([fs[h]['normal'] for h in chosen],[fs[h]['rhs'] for h in chosen])
            if point is None:singular+=1;continue
            if any(dot(f['normal'],point)>f['rhs'] for f in fs):continue
            feasible_bases+=1
            vs.setdefault(point,[]).append(chosen)
        vertices=[]
        for k,point in enumerate(sorted(vs)):
            active=[f['id'] for f in fs if dot(f['normal'],point)==f['rhs']]
            vertices.append({'id':f'I{i}_V{k:03d}','parameters':point,'active_facets':active,'all_independent_active_bases':[[fs[h]['id'] for h in basis] for basis in vs[point]]})
        strict=tuple([F(1,100)]*(dim-1)+[F(1)])
        assert all(dot(f['normal'],strict)<f['rhs'] for f in fs)
        facet_checks=[]
        for f in fs:
            fv=[v for v in vertices if f['id'] in v['active_facets']]
            base=fv[0]['parameters']
            fr=rank([[x-y for x,y in zip(v['parameters'],base)] for v in fv[1:]])
            assert fr==dim-1,(i,f['id'],fr)
            facet_checks.append({'facet':f['id'],'vertices':[v['id'] for v in fv],'affine_rank':fr})
        source_forms=[]
        for p in range(i):
            for m in range(len(mids)+1):
                for missing in combinations(mids,m):
                    for z in [0,1]:
                        f=affine(i,lambda point:rho(i,p,missing,z,point))
                        values=[evaluate(f,v['parameters']) for v in vertices]
                        assert min(values)>=0,(i,p,missing,z,min(values))
                        rec={'source':i,'p':p,'missing':missing,'z':z,**f,'minimum_over_vertices':min(values),'all_minimizing_vertices':[v['id'] for v,value in zip(vertices,values) if value==min(values)]}
                        source_forms.append(rec)
        for f in fs:
            w=f['necessary_state']
            if w.get('kind')=='wallet_weight':continue
            form=affine(i,lambda point:rho(i,w['p'],w['missing'],w['z'],point))
            scale=F(w['rho_equals_slack_times'])
            assert form['constant']==scale*f['rhs']
            assert form['coefficients']==[-scale*x for x in f['normal']]
        minima={
            'source_IC':min(cap(i,v['parameters'])[3] for v in vertices),
            'S':min(cap(i,v['parameters'])[2] for v in vertices),
            'W_minus_Z':min(w_anchor(i,p,v['parameters'])-z_anchor(i,p,v['parameters']) for v in vertices for p in range(i)),
            's_maximum':max(v['parameters'][-1] for v in vertices)}
        assert minima['source_IC']>0 and minima['W_minus_Z']>0
        count={'source':i,'dimension':dim,'facets':len(fs),'all_boundary_combinations':combinations_count,'singular_combinations':singular,'feasible_independent_bases':feasible_bases,'vertices':len(vertices),'rho_affine_forms':len(source_forms),'rho_vertex_evaluations':len(source_forms)*len(vertices),'minimum_values':minima}
        counts.append(count);state_forms+=source_forms
        domains.append({'source':i,'coordinate_order':[f'tau{j}' for j in mids]+['s'],'dimension':dim,'facets':fs,'strict_interior_point':strict,'vertices':vertices,'facet_checks':facet_checks,'enumeration':count,'boundedness':{'tau_j_upper_bound':'7/8','s_upper_bound':'23' if i==1 else '9','source_IC_analytic_lower_bound':'2' if i==1 else '16'}})
        print(json.dumps(js(count)),flush=True)
    write('parameter_domains.json',{'schema':'ordered_minimal_cap_domains_v1','q0':Q0,'halfspace_convention':'normal dot parameters <= rhs','domains':domains,'candidate_is_exact_full_rho_domain':True,'source_IC_nonnegative_constraint_is_automatic':True,'optimizer_calls':0})
    write('state_halfspaces.json',{'schema':'all_t1_q0_zero_rho_forms_v1','forms':state_forms,'count':len(state_forms)})
    write('geometry_counts.json',{'sources':counts,'total_vertices':sum(c['vertices'] for c in counts),'total_boundary_combinations':sum(c['all_boundary_combinations'] for c in counts),'all_facets_have_dimension_minus_one_rank':True,'optimizer_calls':0})
    return domains


def source_pins():
    paths=[
        BASE/'main_minimal_cap_ordered_seed'/'proof_seed.md',
        BASE/'all_source_ordered_joint_menu'/'proof.md',
        BASE/'all_source_ordered_joint_menu'/'freeze_manifest.json',
        BASE/'all_source_ordered_menu_cells'/'proof.md',
        BASE/'all_source_ordered_menu_cells'/'freeze_manifest.json',
        BASE/'source2_minimal_cap_safe'/'proof.md',
        BASE/'source2_minimal_cap_safe'/'freeze_manifest.json',
        BASE.parent.parent.parent/'archives'/'customer-attraction'/'state'/'定义'/'共同目录完整历史模型--定义.md']
    out={str(p.relative_to(BASE)) if p.is_relative_to(BASE) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert out['source2_minimal_cap_safe/freeze_manifest.json']=='d63c117b0adf2353f70ffaf7d959dd91e8c4ee378838f7e5f4af6e99c86861ec'
    return out


def analytic_checks():
    zero_tail=[];query_comparisons=[];minimal_caps=[]
    for i in range(1,6):
        mids=list(range(i+1,6));tails=list(product([0,1],repeat=6-i))
        for p in range(i):
            for tail in tails:
                for q in [F(0),Q0]:
                    form=affine(i,lambda point:psi(i,p,0,q,tail,point)-(z_anchor(i,p,point) if q else 0))
                    assert form['constant']>=0 and all(v>=0 for v in form['coefficients'])
                    zero_tail.append({'source':i,'p':p,'q':q,'tail':tail,**form})
                qform=affine(i,lambda point:psi(i,p,1,F(1),tail,point)-psi(i,p,1,F(0),tail,point)-(1+sum(point[:-1],F(0)))/F(p+7-i))
                assert qform['constant']>=0 and all(v>=0 for v in qform['coefficients'])
                query_comparisons.append({'source':i,'p':p,'tail':tail,**qform})
        for j in mids:
            tail=tuple(int(k==j) for k in mids)+(0,)
            f=affine(i,lambda point:psi(i,0,0,Q0,tail,point)-z_anchor(i,0,point))
            assert not f['constant'] and not any(f['coefficients'])
            minimal_caps.append({'source':i,'single_middle_member':j,'p':0,'z':0,'required_beta_constant':'1/10','tau_coefficients':{str(l):F(1) if l==j else F(1,5*(7-l)*(8-l)) if l>j else F(0) for l in mids},'chosen_beta_remainder':f})
    write('analytic_state_checks.json',{'t0_all_nonnegative_affine_remainders':zero_tail,'t1_query_slope_minus_anchor':query_comparisons,'coordinate_minimal_caps':minimal_caps,'all_coefficients_nonnegative':True})


def build_family(domains):
    rows=[];conditional=[];hidden=[];outer=[];projection=[];menus=[];catalog=[]
    bits9=list(product([0,1],repeat=9));bits6=list(product([0,1],repeat=6))
    for domain in domains:
        i=domain['source'];mids=list(range(i+1,6));tails=list(product([0,1],repeat=6-i))
        for v in domain['vertices']:
            ident=v['id'];point=v['parameters'];tau,beta,S,a=cap(i,point);G={}
            for p in range(i):
                minimum={};fvalues={}
                for d in range(7):
                    valid_t=[0] if d==0 else [1] if d==6 else [0,1]
                    for t in valid_t:
                        q=F(d-t,5)
                        costs=[psi(i,p,t,q,tail,point) for tail in tails]
                        minimum[d,t]=mn=min(costs)
                        attained=[tail for tail,cost in zip(tails,costs) if cost==mn]
                        conditional.append({'vertex_id':ident,'source':i,'p':p,'d':d,'t':t,'q':q,'minimum':mn,'all_minimizing_tails':attained})
                        hidden.append({'vertex_id':ident,'p':p,'d':d,'t':t,'tail_order':'lexicographic','all_tail_costs':costs,'all_tail_minus_minimum':[cost-mn for cost in costs]})
                    fv=sum(((6-d if t==0 else d)*minimum[d,t] for t in valid_t),F(0))/6
                    fvalues[d]=fv
                    outer.append({'vertex_id':ident,'source':i,'p':p,'d':d,'f':fv})
                G[p]=min(fvalues[d] for d in range(1,7))
                assert G[p]==g_closed(i,p,point)
                assert fvalues[0]==0
                assert [d for d in range(1,7) if fvalues[d]==G[p]]==[1]
                Z=z_anchor(i,p,point);W=w_anchor(i,p,point)
                assert minimum[1,0]==Z and minimum[1,1]==W
                for d in range(2,7):
                    assert fvalues[d]-G[p]>=F(d-1,6)*(W-Z)>0
                for d in range(1,7):
                    assert minimum[d,1]==W+(1+sum(tau.values(),F(0)))*F(d-1,5*(p+7-i))
                projection.append({'vertex_id':ident,'source':i,'p':p,'Z':Z,'W':W,'G':G[p],'unique_minimizing_d':1,'gap_lower_bound_per_d_minus_1':(W-Z)/6})
                for menu in bits6:
                    d=sum(menu);qvalues=[sum(menu[l] for l in range(6) if l!=k)/F(5) for k in range(6)]
                    assert qvalues==[F(d-t,5) for t in menu]
                    per_outer=[minimum[d,t] for t in menu]
                    avg=sum(per_outer,F(0))/6
                    assert avg==fvalues[d]
                    assert avg-(G[p] if d else 0)>=0
                    menus.append({'vertex_id':ident,'p':p,'menu':menu,'d':d,'inner_five_means':qvalues,'six_conditional_minima':per_outer,'outer_average':avg,'union_projection_remainder':avg-(G[p] if d else 0)})
            coeff={}
            for c,bits in enumerate(bits9):
                total=sum(bits[:6]);share=F(bits[i-1],total) if total else F(0);p=sum(bits[:i-1]);o=bits[7]
                coeff[str(c)]=a*share-o*G[p]
            coeff['512']=S
            name=f'ORDERED_MINIMAL_CAP_{ident}'
            row={'name':name,'family':'ORDERED_OUTER6_INNER5_TRUE_BRANCH_MINIMAL_CAP','source':i,'vertex_id':ident,'tau_by_source':tau,'s':point[-1],'source_IC_weight':a,'middle_CAP_weights':beta,'terminal_CAP_weight':'1','terminal_BR_average_weight':'1','K_weight':S,'G_by_prefix_load':G,'outer_average_divisor':'6','inner_average_divisor':'5','inner_excludes_same_index':True,'uses_C_size_equality':False,'a':coeff,'rhs':'0','numerical_divisor':'25'}
            rows.append(row)
            catalog.append({'name':name,'source':i,'vertex_id':ident,'parameters':point,'source_IC_weight':a,'K_weight':S,'G_by_prefix_load':G,'active_facets':v['active_facets']})
        print(f'source {i}: built {len(domain["vertices"])} full rows',flush=True)
    pins=source_pins()
    write('source_pins.json',{'pins':pins,'no_numeric_candidate_points_loaded':True,'frozen_inputs_verified':True})
    family={'schema':f'ordered_minimal_cap_{len(rows)}x513_v1','status':'GENERATED_NO_SOLVE_NO_POINT_INPUT','raw_row_count':len(rows),'variables':513,'K_column':512,'bit_order':['a1','a2','a3','a4','a5','a6','x','o','c'],'inequality_convention':'a dot z >= 0','numerical_positive_divisor':'25','complete_finite_generator_for_specified_affine_domain':True,'source_vertex_counts':{str(d['source']):len(d['vertices']) for d in domains},'all_root_vertices_retained':True,'row_pruning':False,'no_C_size_equality':True,'rows':rows,'source_bindings':pins,'optimizer_calls':0,'point_values_loaded_or_bound':False,'half_status':'OPEN'}
    write('exact_family.json',family)
    write('row_catalog.json',catalog)
    write('conditional_minimum_tables.json',{'conditions':conditional,'all_ties_retained':True,'only_physical_d_t_conditions':True})
    write('hidden_state_checks.json',{'records':hidden,'all_tail_states_retained':True})
    write('outer_average_tables.json',outer)
    write('union_projection_tables.json',projection)
    write('all_64_menu_checks.json',{'records':menus,'all_64_menus_for_every_vertex_and_p':True})
    duplicate_groups={}
    for row in rows:
        key=tuple(row['a'].values())
        duplicate_groups.setdefault(key,[]).append(row['name'])
    duplicates=[names for names in duplicate_groups.values() if len(names)>1]
    write('raw_duplicate_report.json',{'raw_rows':len(rows),'distinct_exact_rows':len(duplicate_groups),'duplicate_groups':duplicates,'deleted_rows':0,'zero_rows':[r['name'] for r in rows if not any(r['a'].values())]})
    columnmap=[{'column':k,'bits':bits,'type_string':''.join(map(str,bits))} for k,bits in enumerate(bits9)]+[{'column':512,'kind':'independent_K'}]
    write('coordinate_contract.json',{'variables':513,'bit_order':['a1','a2','a3','a4','a5','a6','x','o','c'],'all_512_types_lexicographic':True,'columns':columnmap,'K_is_independent':True,'uses_C_equality':False,'raw_scale_terminal_BR_average':'1','numeric_positive_divisor':'25','forced_source_IC_weight':'25+sum(tau)-s','middle_cap':'1/10+tau_j+sum_later tau_l/[5(7-l)(8-l)]','K_coefficient':'1+sum(beta_j)','column_formula':'a*a_i/sum(a1..a6)-o*G_i(sum(a1..a_(i-1))); share=0 when total=0'})
    totals={'rows':len(rows),'columns_per_row':513,'full_row_coefficients':513*len(rows),'hidden_states':sum(len(h['all_tail_costs']) for h in hidden),'physical_condition_minima':len(conditional),'outer_averages':len(outer),'G_contexts':len(projection),'menu_contexts':len(menus),'literal_inner_five_means':6*len(menus),'all_tied_tail_occurrences':sum(len(r['all_minimizing_tails']) for r in conditional),'duplicate_groups_retained':len(duplicates),'optimizer_calls':0,'LP_points_read':0}
    write('derivation_result.json',totals)
    print(json.dumps(totals),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--geometry-only',action='store_true');args=parser.parse_args()
    domains=enumerate_geometry()
    if not args.geometry_only:
        analytic_checks();build_family(domains)
