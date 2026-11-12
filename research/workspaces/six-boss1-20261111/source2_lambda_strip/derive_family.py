#!/usr/bin/env python3
"""Exact local source-2 lambda strip; no optimizer or global LP input.

Only this package is written. Sources are pinned explicit model/proof/contracts.
Every number used for a matrix, a cost, or geometry is fractions.Fraction.
The independent checker does not import this file.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
WS = HERE.parent
J = (3, 4, 5)
ZERO = (F(0),) * 4
TAILS = tuple(product((0, 1), repeat=4))
BITS = tuple(product((0, 1), repeat=9))
VAR_NAMES = ['tau3', 'tau4', 'tau5', 'lambda']
PINS = {
    'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md': 'cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88',
    'research/workspaces/six-boss1-20261111/source2_minimal_cap_safe/proof.md': 'e0686cf9db0ab9611eea9852a2e56141e24d9011d124ec2a881a10c8dc5f48d6',
    'research/workspaces/six-boss1-20261111/ordered_minimal_cap/proof.md': 'db6dd7c970ff5a525ad8b86f23640025ec5f66b250eccc85ad48f522e9fe401d',
    'research/workspaces/six-boss1-20261111/source2_minimal_cap_safe/coordinate_contract.json': 'e644b3e2d24379432684361168fa4313b41e9452a8dc68348881a9dd86fbb0e1',
    'research/workspaces/six-boss1-20261111/ordered_minimal_cap/coordinate_contract.json': '10ccdb56e9af65d3d6a4587cd5066a989387ffb3242befbc41b99898e106472f',
}


def clean(v):
    if isinstance(v, F):
        return str(v)
    if isinstance(v, dict):
        return {str(k): clean(x) for k, x in v.items()}
    if isinstance(v, (tuple, list)):
        return [clean(x) for x in v]
    return v


def write(name, obj):
    (HERE / name).write_text(json.dumps(clean(obj), ensure_ascii=False, indent=2) + '\n')


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def rank(rows):
    if not rows:
        return 0
    m = [list(row) for row in rows]
    out = 0
    for col in range(len(m[0])):
        pivot = next((i for i in range(out, len(m)) if m[i][col]), None)
        if pivot is None:
            continue
        m[out], m[pivot] = m[pivot], m[out]
        scale = m[out][col]
        m[out] = [x / scale for x in m[out]]
        for i in range(len(m)):
            if i != out and m[i][col]:
                scale = m[i][col]
                m[i] = [x - scale * y for x, y in zip(m[i], m[out])]
        out += 1
        if out == len(m):
            break
    return out


def solve(rows, rhs):
    m = [list(a) + [b] for a, b in zip(rows, rhs)]
    n = len(rows)
    for col in range(n):
        pivot = next((i for i in range(col, n) if m[i][col]), None)
        if pivot is None:
            return None
        m[col], m[pivot] = m[pivot], m[col]
        scale = m[col][col]
        m[col] = [v / scale for v in m[col]]
        for i in range(n):
            if i != col:
                scale = m[i][col]
                m[i] = [v - scale * w for v, w in zip(m[i], m[col])]
    return tuple(row[-1] for row in m)


def affine(fn):
    c = fn(ZERO)
    out = [c]
    for i in range(4):
        e = list(ZERO)
        e[i] = F(1)
        out.append(fn(tuple(e)) - c)
    return tuple(out)


def eval_aff(a, x):
    return a[0] + dot(a[1:], x)


def weights(q0, x):
    tau, lam = x[:3], x[3]
    beta = tuple(q0 / 2 + tau[i] + sum((q0 * tau[h] / ((7-J[h])*(8-J[h])) for h in range(i+1, 3)), F(0)) for i in range(3))
    return lam + sum(tau), beta, F(1) + sum(beta)


def actual_cost(q0, x, p, t, q, r, z):
    """Reconstruct source share, caps, actual last share and actual inner shares."""
    a, beta, S = weights(q0, x)
    load = p + t + sum(r) + z
    source = F(t, load) if load else F(0)
    last = F(z, load) if load else F(0)
    middle = [F(bit, load) if load else F(0) for bit in r]
    value = a * source - last - dot(x[:3], middle)
    value += dot(beta, r) + z
    value += q / (p + t + sum(r) + 1)
    for i, j in enumerate(J):
        value += x[i] * q / (p + t + sum(r[:i]) + 7-j)
    return value


def anchor(q0, x, p, t, q):
    _, beta, _ = weights(q0, x)
    if t:
        return sum(beta) + x[3]/(p+4) + q*(1+sum(x[:3]))/(p+5)
    assert q in (0, q0)
    return q * (F(1, p+1) + sum((x[i]/(p+7-j) for i, j in enumerate(J)), F(0)))


def rho(q0, x, p, missing, z):
    r = tuple(int(j not in missing) for j in J)
    return actual_cost(q0, x, p, 1, F(0), r, z) - anchor(q0, x, p, 1, F(0))


def candidate_facets(q0):
    fs = []
    for i, j in enumerate(J):
        a = list(ZERO); a[i] = F(-1)
        fs.append({'id': 'tau%d_nonnegative' % j, 'normal': tuple(a), 'rhs': F(0), 'origin': 'nonnegative_true_wallet_weight'})
    fs.append({'id':'lambda_lower', 'normal':(F(0),F(0),F(0),F(-1)), 'rhs':F(-9), 'origin':'specified_research_window'})
    fs.append({'id':'lambda_upper', 'normal':(F(0),F(0),F(0),F(1)), 'rhs':F(16), 'origin':'true_state', 'state':{'p':0,'missing':[],'z':1}, 'rho_equals_slack_times':F(1,20)})
    for cap in ('A', 'B'):
        for i, j in enumerate(J):
            a = list(ZERO); a[i] = F(3,4)
            for h in range(i+1,3):
                a[h] = q0 / ((7-J[h])*(8-J[h]))
            if cap == 'A':
                a[3] = F(-1,20); rhs = -q0/2; p = 1; z = 0
            else:
                rhs = F(3,4)-q0/2; p = 0; z = 1
            fs.append({'id':cap+str(j),'normal':tuple(a),'rhs':rhs,'origin':'true_state','state':{'p':p,'missing':[j],'z':z},'rho_equals_slack_times':F(1)})
    return fs


def slack(f, x):
    return f['rhs'] - dot(f['normal'], x)


def geometry(q0):
    fs = candidate_facets(q0)
    vertices = {}
    combinations_count = 0
    for ids in combinations(range(len(fs)), 4):
        combinations_count += 1
        x = solve([fs[i]['normal'] for i in ids], [fs[i]['rhs'] for i in ids])
        if x is not None and all(slack(f,x) >= 0 for f in fs):
            vertices.setdefault(x, ids)
    xs = sorted(vertices, key=lambda x:(x[3],x[:3]))
    assert len(xs) == 23
    vs = [{'id':'v%02d'%n,'point':x,'active_facets':[f['id'] for f in fs if slack(f,x)==0], 'independent_active_basis':[fs[i]['id'] for i in vertices[x]]} for n,x in enumerate(xs)]
    witnesses = []
    for f in fs:
        on = [v for v in vs if slack(f,v['point']) == 0]
        base = on[0]['point']
        affine_rank = rank([[a-b for a,b in zip(v['point'],base)] for v in on[1:]])
        assert affine_rank == 3
        f['vertex_ids'] = [v['id'] for v in on]
        f['affine_rank'] = affine_rank
        center = tuple(sum((v['point'][i] for v in on),F(0))/len(on) for i in range(4))
        direction = f['normal']
        bounds = [F(1)]
        for g in fs:
            if g is f:
                continue
            assert slack(g,center)>0
            motion = dot(g['normal'],direction)
            if motion>0:
                bounds.append(slack(g,center)/(2*motion))
        eps = min(bounds)
        out = tuple(a+eps*b for a,b in zip(center,direction))
        assert slack(f,out)<0 and all(slack(g,out)>=0 for g in fs if g is not f)
        rec = {'facet':f['id'],'facet_relative_interior':center,'outward_step':eps,'point_violating_only_this_facet':out,'all_facet_slacks':{g['id']:slack(g,out) for g in fs},'source_IC_weight':weights(q0,out)[0]}
        assert rec['source_IC_weight']>0
        if f['origin']=='true_state':
            st=f['state']; rr=rho(q0,out,st['p'],tuple(st['missing']),st['z'])
            assert rr<0
            rec['corresponding_true_rho']=rr
        witnesses.append(rec)
    for f in fs:
        if f['origin']=='true_state':
            st=f['state']; mult=f['rho_equals_slack_times']
            assert affine(lambda x:rho(q0,x,st['p'],tuple(st['missing']),st['z'])) == affine(lambda x:mult*slack(f,x))
    interior = (F(1,100),F(1,100),F(1,100),F(10))
    assert all(slack(f,interior)>0 for f in fs)
    return {'q0':q0,'dimension':4,'variable_order':VAR_NAMES,'facets':fs,'vertices':vs,'all_boundary_combinations':combinations_count,'strict_interior_point':interior,'tau_coordinate_upper_bound':1-F(2,3)*q0,'lambda_layers':{str(l):sum(v['point'][3]==l for v in vs) for l in (9,15,16)}}, witnesses


def rho_decomposition(q0,x,p,missing,z,high=False):
    lam=x[3];U=sum((x[J.index(j)] for j in missing),F(0));k=len(missing)
    _,beta,_=weights(q0,x)
    A=sum((lam/20+x[J.index(j)]/4-beta[J.index(j)] for j in missing),F(0))
    B=sum((F(3,4)+x[J.index(j)]/4-beta[J.index(j)] for j in missing),F(0))
    if k==0:
        return F(0) if z==0 else ((16-lam)/20 if p==0 else (25-lam)/30)
    if (k,z)==(1,0):
        return A+lam/30+U/12 if p==0 else A
    if (k,z)==(1,1):
        return B if p==0 else B+(1-U)/20
    if (k,z)==(2,0):
        return A+3*lam/20+U/4 if p==0 else A+lam/30+U/12
    if (k,z)==(2,1):
        if p==0:return A+F(2,3)-lam/60+U/12
        return B+lam/20-F(3,4) if high else A+F(3,4)-lam/20
    if (k,z)==(3,0):
        return A+3*lam/5+3*U/4 if p==0 else A+3*lam/20+U/4
    assert (k,z)==(3,1)
    return A+lam/10+F(1,2)+U/4 if p==0 else A+F(2,3)-lam/60+U/12


def make_analytic(q0):
    states=[];t0=[];slopes=[];necessity=[]
    for p in (0,1):
        for tail in TAILS:
            r,z=tail[:3],tail[3];missing=tuple(j for j,bit in zip(J,r) if not bit)
            co=affine(lambda x:rho(q0,x,p,missing,z))
            co2=affine(lambda x:rho_decomposition(q0,x,p,missing,z))
            assert co==co2
            if p==1 and len(missing)==2 and z==1:
                assert co==affine(lambda x:rho_decomposition(q0,x,p,missing,z,True))
            states.append({'p':p,'D':p+5,'tail':tail,'missing':missing,'affine_coefficients':co,'decomposition_checked':True})
            for q in (F(0),q0):
                delta=affine(lambda x:actual_cost(q0,x,p,0,q,r,z)-anchor(q0,x,p,0,q))
                assert all(c>=0 for c in delta[:4]) and delta[4]==0
                t0.append({'p':p,'q':q,'tail':tail,'coefficients':delta})
            slope=affine(lambda x:actual_cost(q0,x,p,1,F(1),r,z)-actual_cost(q0,x,p,1,F(0),r,z)-(1+sum(x[:3]))/(p+5))
            assert all(c>=0 for c in slope[:4]) and slope[4]==0
            slopes.append({'p':p,'tail':tail,'coefficients':slope})
    for i,j in enumerate(J):
        # beta_j is kept independent here. Variables: constant, tau3..5, beta3..5.
        coeff=[-q0/2,F(0),F(0),F(0),F(0),F(0),F(0)]
        coeff[1+i]=-1;coeff[4+i]=1
        for h in range(i+1,3):coeff[1+h]=-q0/((7-J[h])*(8-J[h]))
        necessity.append({'j':j,'p':0,'t':0,'z':0,'single_middle_member':j,'free_variable_order':['constant','tau3','tau4','tau5','beta3','beta4','beta5'],'coefficients':coeff})
    return {'state_halfspaces':states,'t0_nonnegative_coefficients':t0,'t1_query_slope_nonnegative_coefficients':slopes,'independent_beta_necessity':necessity}


def minimum(q0,x,p,t,q):
    values=[actual_cost(q0,x,p,t,q,tail[:3],tail[3]) for tail in TAILS]
    m=min(values)
    return m,[tail for tail,v in zip(TAILS,values) if v==m],values


def main():
    pins=[]
    for rel,sha in PINS.items():
        data=(ROOT/rel).read_bytes();assert hashlib.sha256(data).hexdigest()==sha,rel
        pins.append({'repository_relative_path':rel,'sha256':sha,'bytes':len(data)})
    old=json.loads((WS/'source2_minimal_cap_safe/coordinate_contract.json').read_text())
    ordered_old=json.loads((WS/'ordered_minimal_cap/coordinate_contract.json').read_text())
    assert old['variables']==ordered_old['variables']==513
    for col,bits in enumerate(BITS):
        rec=old['atom_columns'][col]
        assert tuple(rec['a'])+(rec['x'],rec['o'],rec['c'])==bits
        assert tuple(ordered_old['columns'][col]['bits'])==bits
    write('source_pins.json',{'sources':pins,'initial_and_final_bytes_must_match':True,'allowed_reads':'only five explicitly pinned files; no global LP, point, or optimum face'})
    domains={};witnesses={};analytics={};tables=[];hidden=[];outer=[];menus=[];rows=[];catalog=[]
    pure_min={};ordered_min={};counts={'optimizers':0,'global_LP_inputs_or_points_read':0}
    for name,q0 in (('six_mean',F(1,6)),('ordered_five',F(1,5))):
        dom,wit=geometry(q0);domains[name]=dom;witnesses[name]=wit;analytics[name]=make_analytic(q0)
        for v in dom['vertices']:
            x=tuple(v['point']);vid=v['id'];a,beta,S=weights(q0,x)
            for p in (0,1):
                contexts=[(t,q0*o,{'o':o}) for t in (0,1) for o in (0,1)] if name=='six_mean' else [(t,F(d-t,5),{'d':d}) for d in range(7) for t in (0,1) if (t==0 and d<6) or (t==1 and d>0)]
                for t,q,context in contexts:
                    m,attainers,values=minimum(q0,x,p,t,q)
                    if t==1 or q in (0,q0):assert m==anchor(q0,x,p,t,q)
                    row={'family':name,'vertex':vid,'p':p,'t':t,'q':q,**context,'minimum':m,'all_attaining_tails':attainers}
                    tables.append(row)
                    if name=='six_mean':pure_min[(vid,p,t,context['o'])]=m
                    else:ordered_min[(vid,p,t,context['d'])]=m
                    for tail,value in zip(TAILS,values):
                        assert value>=m
                        hidden.append({'family':name,'vertex':vid,'p':p,'t':t,'q':q,**context,'tail':tail,'cost':value,'minimum':m,'slack':value-m})
                if name=='ordered_five':
                    f=[]
                    for d in range(7):
                        avg=((6-d)*ordered_min[(vid,p,0,d)] if d<6 else F(0))+(d*ordered_min[(vid,p,1,d)] if d>0 else F(0))
                        avg/=6;f.append(avg)
                    Z=anchor(q0,x,p,0,q0);W=anchor(q0,x,p,1,F(0));G=(5*Z+W)/6
                    assert W-Z>=2+F(19,20)*sum(x[:3])
                    assert f[0]==0 and f[1]==G and all(f[d]>G for d in range(2,7))
                    for d in range(7):
                        bound=(d-1)*(W-Z)/6 if d>=1 else F(0)
                        assert f[d]-(G if d else 0)>=bound
                        outer.append({'vertex':vid,'p':p,'d':d,'f':f[d],'G':G,'Z':Z,'W':W,'projection_slack':f[d]-(G if d else 0),'strict_gap_bound':bound})
                    for menu in product((0,1),repeat=6):
                        d=sum(menu);branch=[]
                        for k,t in enumerate(menu):
                            actual_q=sum((F(menu[l],5) for l in range(6) if l!=k),F(0))
                            assert actual_q==F(d-t,5)
                            branch.append({'outer_index':k+1,'t':t,'inner_q':actual_q,'minimum':ordered_min[(vid,p,t,d)]})
                        avg=sum((b['minimum'] for b in branch),F(0))/6
                        assert avg==f[d]
                        menus.append({'vertex':vid,'p':p,'six_membership_bits':menu,'d':d,'branches':branch,'average':avg,'union_bound':G if d else F(0),'slack':avg-(G if d else 0)})
            if name=='six_mean':
                targets=[('A%d'%(i+1),i) for i in range(6)]+[('X',6),('C',8)]
                for target,idx in targets:
                    coeff=[]
                    for bits in BITS:
                        total=sum(bits[:6]);share=F(bits[1],total) if total else F(0)
                        p,t,o=bits[0],bits[idx],bits[7]
                        coeff.append(a*share-pure_min[(vid,p,t,o)])
                    coeff.append(S)
                    rid='six_general_%s_%s'%(vid,target)
                    rows.append({'id':rid,'family':'six_general','vertex':vid,'target':target,'raw_coefficients':coeff,'coefficients_divided_by_25':[c/25 for c in coeff]})
                    catalog.append({'id':rid,'q0':q0,'vertex':vid,'parameters':x,'target':target,'source_IC_weight':a,'middle_caps':beta,'K_coefficient':S,'uses_C_equality':False})
                coeff=[]
                for bits in BITS:
                    total=sum(bits[:6]);share=F(bits[1],total) if total else F(0)
                    p,t,o=bits[0],bits[8],bits[7]
                    coeff.append(a*share-pure_min[(vid,p,t,o)]+sum(beta)*t)
                coeff.append(F(1));rid='six_C_only_'+vid
                rows.append({'id':rid,'family':'six_C_only','vertex':vid,'target':'C','raw_coefficients':coeff,'coefficients_divided_by_25':[c/25 for c in coeff]})
                catalog.append({'id':rid,'q0':q0,'vertex':vid,'parameters':x,'target':'C','source_IC_weight':a,'middle_caps':beta,'K_coefficient':F(1),'uses_C_equality':True,'free_C_equality_multiplier':sum(beta)})
            else:
                coeff=[]
                for bits in BITS:
                    total=sum(bits[:6]);share=F(bits[1],total) if total else F(0);p=bits[0]
                    G=(5*ordered_min[(vid,p,0,1)]+ordered_min[(vid,p,1,1)])/6
                    coeff.append(a*share-bits[7]*G)
                coeff.append(S);rid='ordered_'+vid
                rows.append({'id':rid,'family':'ordered_five','vertex':vid,'target':'outer_six_same_menu','raw_coefficients':coeff,'coefficients_divided_by_25':[c/25 for c in coeff]})
                catalog.append({'id':rid,'q0':q0,'vertex':vid,'parameters':x,'source_IC_weight':a,'middle_caps':beta,'K_coefficient':S,'uses_C_equality':False})
    # All actual six-query patterns, with independent forced target membership.
    pure_query_checks=[]
    for p,t,tail,menu in product((0,1),(0,1),TAILS,tuple(product((0,1),repeat=6))):
        r,z=tail[:3],tail[3];d=sum(menu);o=int(d>0)
        delta=affine(lambda x:actual_cost(F(1,6),x,p,t,F(d,6),r,z)-actual_cost(F(1,6),x,p,t,F(o,6),r,z))
        direct=affine(lambda x:F(d-o,6)*(F(1,p+t+sum(r)+1)+sum((x[i]/(p+t+sum(r[:i])+7-j) for i,j in enumerate(J)),F(0))))
        assert delta==direct and all(c>=0 for c in delta[:4]) and delta[4]==0
        pure_query_checks.append({'p':p,'t':t,'tail':tail,'menu':menu,'d':d,'o':o,'weakening_delta_coefficients':delta})
    byid={r['id']:r for r in rows};ceq=[]
    for v in domains['six_mean']['vertices']:
        vid=v['id'];B=sum(weights(F(1,6),v['point'])[1]);g=byid['six_general_%s_C'%vid];c=byid['six_C_only_'+vid]
        for col in range(513):
            ec=F(BITS[col][8]) if col<512 else F(-1)
            err=g['raw_coefficients'][col]-c['raw_coefficients'][col]+B*ec
            assert err==0
            ceq.append({'vertex':vid,'column':col,'E_C_coefficient':ec,'multiplier':B,'residual':err})
    cols=[{'column':col,'bits':bits,'type_string':''.join(map(str,bits))} for col,bits in enumerate(BITS)]+[{'column':512,'kind':'independent_K'}]
    write('coordinate_contract.json',{'variables':513,'bit_order':['a1','a2','a3','a4','a5','a6','x','o','c'],'columns':cols,'all_512_types_lexicographic':True,'K_is_independent':True,'raw_scale_terminal_BR_inner_average':F(1),'numeric_positive_divisor':F(25),'source_IC_weight':'lambda+tau3+tau4+tau5','query_vs_source_denominators':{'t1_anchor_source':'p+4=D-1','t1_anchor_all_queries':'p+5=D'},'row_groups':{'six_general':184,'six_C_only':23,'ordered_five':23},'C_equality':'sum_x c_x-K=0','C_row_relation':'R_six_general_C=R_six_C_only-(S-1)*E_C','no_row_or_column_pruning':True})
    write('parameter_domains.json',{'families':domains,'lambda_lower_is_research_window':True,'geometry_method':'all independent 4-facet intersections, Fraction arithmetic'})
    write('necessary_facet_witnesses.json',witnesses)
    write('analytic_state_checks.json',analytics)
    write('state_halfspaces.json',{k:v['state_halfspaces'] for k,v in analytics.items()})
    write('conditional_minimum_tables.json',tables)
    write('hidden_state_checks.json',hidden)
    write('outer_average_tables.json',outer)
    write('all_64_ordered_menu_checks.json',menus)
    write('all_64_pure_query_checks.json',pure_query_checks)
    write('C_equality_column_checks.json',ceq)
    write('exact_family.json',{'schema':'source2_lambda_strip_exact_v1','variables':513,'rows':rows,'row_count':len(rows),'numeric_positive_divisor':F(25),'no_pruning':True})
    write('row_catalog.json',catalog)
    assert len(rows)==230
    counts.update({'parameter_domains':2,'facets':22,'all_boundary_combinations':660,'vertices':46,'t1_query_zero_affine_states':64,'full_vertex_t1_query_zero_checks':1472,'t0_quadrant_affines':128,'t1_query_slope_affines':64,'free_beta_minimality_witnesses':6,'full_hidden_state_checks':len(hidden),'conditional_minimum_tables':len(tables),'all_weak_tie_attainers':sum(len(t['all_attaining_tails']) for t in tables),'max_weak_tie_size':max(len(t['all_attaining_tails']) for t in tables),'ordered_outer_average_rows':len(outer),'ordered_menu_contexts':len(menus),'ordered_actual_five_query_means':len(menus)*6,'pure_actual_six_query_contexts':len(pure_query_checks),'row_count':len(rows),'full_column_count':len(rows)*513,'C_equality_column_identities':len(ceq)})
    for rel,sha in PINS.items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==sha
    write('generator_output.json',{'status':'PASS','counts':counts,'source_pins_unchanged':True,'method':'pure Fraction local derivation; no optimization, LP points, or row pruning'})
    print(json.dumps(clean({'status':'PASS','counts':counts}),ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
