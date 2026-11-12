#!/usr/bin/env python3
"""Exact source-1 lambda closure; fixed local sources, no optimizer or LP input.

This package intentionally does not materialize 900 duplicate rows.  It records
the complete domains, all raw states, all vertex correspondences, and exact
513-column identities with the already-frozen local source families.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product, combinations
from functools import reduce
from math import gcd, lcm
import hashlib
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
J = (2, 3, 4, 5)
TAILS = list(product((0, 1), repeat=5))
TYPES = list(product((0, 1), repeat=9))
ORDER = ['constant', 'tau2', 'tau3', 'tau4', 'tau5', 'lambda']
SOURCES = [
    WS/'all_source_minimal_cap_safe/proof.md',
    WS/'ordered_minimal_cap/proof.md',
    WS/'source2_lambda_anchor_complete/proof.md',
    WS/'later_sources_lambda_cells/proof.md',
    REPO/'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
    WS/'all_source_minimal_cap_safe/parameter_domains.json',
    WS/'all_source_minimal_cap_safe/parameter_families.json',
    WS/'all_source_minimal_cap_safe/exact_family.json',
    WS/'all_source_minimal_cap_safe/row_catalogue.json',
    WS/'ordered_minimal_cap/parameter_domains.json',
    WS/'ordered_minimal_cap/exact_family.json',
    WS/'ordered_minimal_cap/row_catalog.json',
]

def dump(name, data):
    (HERE/name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def vec(c=0):
    return (F(c), F(0), F(0), F(0), F(0), F(0))

def variable(k):
    x = list(vec()); x[k] = F(1); return tuple(x)

def add(*xs):
    return tuple(sum(v) for v in zip(*xs)) if xs else vec()

def scale(x, f):
    return tuple(v*f for v in x)

def sub(x, y):
    return add(x, scale(y, -1))

def ev(x, p):
    return x[0]+sum(a*b for a, b in zip(x[1:], p))

def ss(x):
    return [str(v) for v in x]

def primitive(x):
    den = lcm(*(v.denominator for v in x))
    a = [int(v*den) for v in x]
    g = reduce(gcd, (abs(v) for v in a), 0)
    return tuple(v//g for v in a) if g else tuple(a)

def rank(rows):
    a = [list(r) for r in rows]
    if not a: return 0
    k = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(k, len(a)) if a[i][c]), None)
        if pivot is None: continue
        a[k], a[pivot] = a[pivot], a[k]
        w = a[k][c]; a[k] = [v/w for v in a[k]]
        for i in range(k+1, len(a)):
            if a[i][c]:
                w = a[i][c]; a[i] = [v-w*z for v, z in zip(a[i], a[k])]
        k += 1
        if k == len(a): break
    return k

TAU = {j: variable(j-1) for j in J}
LAM = variable(5)
THETA = add(*(TAU[j] for j in J))
A = add(LAM, THETA)

def weights(q0):
    beta = {j: add(vec(q0/2), TAU[j], *(
        scale(TAU[l], q0/F((7-l)*(8-l))) for l in J if l>j)) for j in J}
    B = add(*beta.values())
    return beta, B, add(vec(1), B)

def literal(q0, t, q, tail):
    beta, _, _ = weights(q0)
    r = dict(zip(J, tail[:4])); z = tail[4]
    L = t+sum(r.values())+z
    num = add(scale(A, t), vec(-z), *(scale(TAU[j], -r[j]) for j in J))
    out = scale(num, F(1,L)) if L else vec()
    out = add(out, vec(z), *(scale(beta[j], r[j]) for j in J))
    out = add(out, vec(q/F(t+sum(r.values())+1)), *(
        scale(TAU[j], q/F(t+sum(r[h] for h in J if h<j)+7-j)) for j in J))
    return out

def build_facets(q0):
    beta, _, _ = weights(q0)
    out = [{'id': f'tau{j}_nonnegative', 'affine': ss(TAU[j]),
            'origin': {'kind': 'true_SAFE_weight', 'j': j}} for j in J]
    out.append({'id': 'lambda_le_25', 'affine': ss(sub(vec(25), LAM)),
                'origin': {'tail': [1,1,1,1,1], 'rho_multiplier': '30'}})
    for j in J:
        for kind, expr, z in [
            ('H', sub(add(vec(F(4,5)), scale(TAU[j], F(1,5))), beta[j]), 1),
            ('A', sub(add(scale(LAM, F(1,20)), scale(TAU[j], F(1,4))), beta[j]), 0)]:
            out.append({'id': f'{kind}{j}', 'affine': ss(expr),
                        'origin': {'tail': [int(h!=j) for h in J]+[z], 'rho_multiplier': '1'}})
    for j,k in combinations(J, 2):
        expr = sub(add(vec(F(3,4)), scale(LAM,F(1,20)),
                       scale(add(TAU[j],TAU[k]),F(1,4))), add(beta[j],beta[k]))
        out.append({'id': f'P{j}{k}', 'affine': ss(expr),
                    'origin': {'tail': [int(h not in (j,k)) for h in J]+[1], 'rho_multiplier': '1'}})
    return out

def transformed_old(q0):
    if q0 == F(1,6):
        old = next(x for x in json.loads(SOURCES[5].read_text())['sources'] if x['source']==1)
        raw = [(x['name'], list(map(F,[x['constant']]+x['coefficients'])))
               for x in old['complete_domain_halfspaces']]
    else:
        old = next(x for x in json.loads(SOURCES[9].read_text())['domains'] if x['source']==1)
        raw = [(x['id'], [F(x['rhs'])]+[-F(v) for v in x['normal']]) for x in old['facets']]
    facets=[]
    for name, v in raw:
        v[0]+=25*v[5]; v[5]=-v[5]
        facets.append({'old_id':name, 'lambda_affine':ss(v)})
    return old, facets

def main():
    pins = [{'path':str(p.relative_to(REPO)), 'sha256':sha(p)} for p in SOURCES]
    dump('source_pins.json', {'sources':pins,'only_fixed_local_mathematical_sources':True,
         'global_LP_files_read':False,'optimizer_calls':0})
    domains=[]; states=[]; analytic=[]; witnesses=[]
    vertex_md=['# 第一源完整 λ 域的全部顶点对应', '',
               '坐标顺序：`(τ₂,τ₃,τ₄,τ₅,λ)`；旧参数只作 `s=25−λ`。两套各90顶点全部保留。','']
    for q0 in (F(1,6),F(1,5)):
        label = 'q6' if q0==F(1,6) else 'q5'
        beta,B,S=weights(q0); W=add(B,scale(LAM,F(1,5)))
        Z=scale(add(vec(1),*(scale(TAU[j],F(1,7-j)) for j in J)),q0)
        facets=build_facets(q0); fa={x['id']:tuple(map(F,x['affine'])) for x in facets}
        old, oldfacets=transformed_old(q0)
        assert {primitive(x) for x in fa.values()} == {primitive(tuple(map(F,x['lambda_affine']))) for x in oldfacets}
        for f in facets:
            f['old_facet_id']=next(x['old_id'] for x in oldfacets
                if primitive(tuple(map(F,x['lambda_affine'])))==primitive(tuple(map(F,f['affine']))))
        vv=[]
        vertex_md += [f'## {label}：q₀={q0}', '', '| λ顶点 | 旧顶点 | τ₂ | τ₃ | τ₄ | τ₅ | λ | 旧s |', '|---|---|---:|---:|---:|---:|---:|---:|']
        for k,v in enumerate(old['vertices']):
            op=list(map(F,v['parameters'])); p=tuple(op[:4]+[25-op[4]])
            assert all(ev(h,p)>=0 for h in fa.values())
            active=[i for i,h in fa.items() if ev(h,p)==0]
            assert rank([fa[i][1:] for i in active])==5
            row={'id':f'{label}_V{k:03d}','old_vertex_id':v['id'],'parameters':ss(p),
                 'old_parameters':ss(op),'active_facets':active,
                 'source_IC_weight':str(ev(A,p)), 'S':str(ev(S,p)),
                 'anchor_tails':[[1,1,1,1,0]]+([[1,1,1,1,1]] if p[4]==25 else [])}
            vv.append(row)
            vertex_md.append('| '+' | '.join([row['id'],v['id']]+ss(p)+[str(op[4])])+' |')
        assert len(vv)==90 and len({tuple(v['parameters']) for v in vv})==90
        pv=[tuple(map(F,v['parameters'])) for v in vv]
        for f in facets:
            h=tuple(map(F,f['affine']))
            face=[v for v in pv if ev(h,v)==0]
            assert rank([[x-y for x,y in zip(v,face[0])] for v in face[1:]])==4
            center=tuple(sum(v[k] for v in face)/len(face) for k in range(5))
            n=h[1:]; bounds=[F(1,100)]
            for oid,oh in fa.items():
                if oid==f['id']: continue
                s=ev(oh,center); assert s>0
                d=sum(x*y for x,y in zip(oh[1:],n))
                if d>0: bounds.append(s/(2*d))
            d=sum(x*y for x,y in zip(A[1:],n))
            if d>0: bounds.append(ev(A,center)/(2*d))
            eps=min(bounds); point=tuple(v-eps*w for v,w in zip(center,n))
            slacks={i:ev(v,point) for i,v in fa.items()}
            assert slacks[f['id']]<0 and all(v>=0 for i,v in slacks.items() if i!=f['id'])
            assert ev(A,point)>0
            f['supporting_vertices']=[v['id'] for v in vv if ev(h,tuple(map(F,v['parameters'])))==0]
            f['supporting_affine_rank']=4
            witness={'q0':str(q0),'facet':f['id'],'point':ss(point),
                     'facet_slacks':{i:str(x) for i,x in slacks.items()},
                     'source_IC_weight':str(ev(A,point)), 'local_state_not_SPE_realization':True}
            if 'tail' in f['origin']:
                witness['tail']=f['origin']['tail']
                witness['true_rho']=str(ev(sub(literal(q0,1,F(0),f['origin']['tail']),W),point))
                assert F(witness['true_rho'])<0
            witnesses.append(witness)
        interior=(F(1,100),)*4+(F(10),)
        assert all(ev(h,interior)>0 for h in fa.values())
        domain={'id':label,'q0':str(q0),'dimension':5,'parameter_order':ORDER[1:],
                'facets':facets,'old_transformed_facets':oldfacets,'vertices':vv,
                'strict_interior':ss(interior),'lambda_minimum':str(10*q0),
                'lambda_maximum':'25','tau_individual_upper_bound':str(1-F(5,8)*q0),
                'old_domain_relation':'exact equality under s=25-lambda',
                'genuinely_new_inequality_rows':0}
        domains.append(domain)
        for tail in TAILS:
            M=[j for j,r in zip(J,tail[:4]) if not r]; k=len(M); z=tail[4]
            U=add(*(TAU[j] for j in M)); BM=add(*(beta[j] for j in M))
            rho=sub(literal(q0,1,F(0),tail),W)
            formula=add(scale(add(LAM,U,vec(-z)),F(1,5-k+z)),vec(z),scale(BM,-1),scale(LAM,F(-1,5)))
            assert rho==formula
            terms={}; rem=vec()
            if k==0 and z==1: terms={'lambda_le_25':'1/30'}
            elif k==1: terms={f'{"H" if z else "A"}{M[0]}':'1'}
            elif k==2 and z==1: terms={f'P{M[0]}{M[1]}':'1'}
            elif k>=2 and z==0:
                terms={f'A{j}':'1' for j in M}
                rem=scale(add(scale(LAM,F(k,5)),U),F(k-1,4*(5-k)))
            elif k==3 and z==1:
                terms={f'A{j}':'1' for j in M}
                rem=add(vec(F(2,3)),scale(LAM,F(-1,60)),scale(U,F(1,12)))
            elif k==4 and z==1:
                terms={f'A{j}':'1' for j in M}
                rem=add(vec(F(1,2)),scale(LAM,F(1,10)),scale(U,F(1,4)))
            decomp=add(rem,*(scale(fa[i],F(c)) for i,c in terms.items()))
            assert decomp==rho
            oldrho=add(scale(add(vec(25),U,vec(-z)),F(1,5-k+z)),
                       scale(variable(5),F(-1,5-k+z)),vec(z-5),scale(BM,-1),scale(variable(5),F(1,5)))
            tr=list(oldrho); tr[0]+=25*tr[5]; tr[5]=-tr[5]
            assert tuple(tr)==rho
            states.append({'q0':str(q0),'tail':list(tail),'missing':M,'k':k,'z':z,
                'rho_affine':ss(rho),'literal_cost_affine':ss(literal(q0,1,F(0),tail)),
                'anchor_affine':ss(W),'facet_terms':terms,'remainder_affine':ss(rem),
                'old_s_rho_affine':ss(oldrho),'old_after_substitution_residual':ss(sub(tuple(tr),rho)),
                'all_90_vertex_values':[str(ev(rho,p)) for p in pv]})
            assert all(ev(rho,p)>=0 for p in pv)
        for t,q in [(0,F(0)),(0,q0)]:
            anchor=vec() if q==0 else Z
            for tail in TAILS:
                residual=sub(literal(q0,t,q,tail),anchor)
                assert all(x>=0 for x in residual) and residual[-1]==0
                analytic.append({'q0':str(q0),'kind':'t0_all_nonnegative_tau',
                                 'q':str(q),'tail':list(tail),'residual':ss(residual)})
        for tail in TAILS:
            slope=sub(literal(q0,1,F(1),tail),literal(q0,1,F(0),tail))
            residual=sub(slope,scale(add(vec(1),THETA),F(1,6)))
            assert all(x>=0 for x in residual)
            analytic.append({'q0':str(q0),'kind':'t1_all_q_slope','tail':list(tail),'residual':ss(residual)})
        for j in J:
            tail=tuple(int(k==j) for k in J)+(0,)
            assert literal(q0,0,q0,tail)==Z
            analytic.append({'q0':str(q0),'kind':'coordinate_minimal_cap_necessary',
                'j':j,'tail':list(tail),'free_cap_formula':
                f'beta{j}-q0/2-tau{j}-sum(l>{j})q0*tau_l/((7-l)*(8-l))',
                'equality_after_minimal_cap_substitution':True})
        if q0==F(1,5):
            diff=sub(W,Z)
            # lambda>=2; every tau coefficient is strictly positive.
            lower=sub(diff,add(vec(F(3,5)),scale(THETA,F(9,10))))
            assert lower[0]+2*lower[5]==0 and all(v>=0 for v in lower[1:])
            analytic.append({'q0':str(q0),'kind':'ordered_continuous_W_minus_Z',
                'exact_affine':ss(diff),'lower_bound':'3/5+(9/10)*Theta',
                'residual_affine':ss(lower),'lambda_lower_bound':'2',
                'all_positive_multiplicities':'d=1 uniquely minimizes f(d); no extra cell cuts'})
        vertex_md.append('')
    dump('parameter_domains.json',{'affine_order':ORDER,'domains':domains,
        'status':'EXACTLY_OLD_ROOT_DOMAINS_UNDER_PARAMETER_BIJECTION','optimizer_calls':0})
    dump('all_32_tail_identities.json',{'affine_order':ORDER,'state_count_per_q0':32,'states':states})
    dump('analytic_checks.json',{'affine_order':ORDER,'checks':analytic})
    dump('necessary_facet_witnesses.json',{'witnesses':witnesses,'count':len(witnesses)})
    (HERE/'endpoint_table.md').write_text('\n'.join(vertex_md)+'\n')

    # Explicit preserved counterexample to omitting the six double-missing faces.
    p=(F(0),F(0),F(5977,6912),F(43,48),25-F(68185,6912))
    beta,B,S=weights(F(1,6)); W=add(B,scale(LAM,F(1,5)))
    fs=build_facets(F(1,6)); slacks={f['id']:ev(tuple(map(F,f['affine'])),p) for f in fs}
    assert all(v>=0 for i,v in slacks.items() if not i.startswith('P'))
    rho=ev(sub(literal(F(1,6),1,F(0),(1,1,0,0,1)),W),p)
    assert rho==F(-1,192)
    dump('double_missing_counterexample.json',{'q0':'1/6','parameters':ss(p),
        'old_s':'68185/6912','tail':[1,1,0,0,1],'rho':str(rho),
        'source_IC_weight':str(ev(A,p)), 'facet_slacks':{i:str(v) for i,v in slacks.items()},
        'not_a_full_SPE_counterexample':True})

    # Complete symbolic 513-column identities, without copying duplicate rows.
    targets={**{f'A{i}':i-1 for i in range(1,7)},'X':6,'C':8}
    coltext=['mode\tcolumn\tlambda_affine\told_after_substitution_affine\tdifference']
    for mode in list(targets)+['C-only','ordered']:
        q0=F(1,5) if mode=='ordered' else F(1,6)
        beta,B,S=weights(q0); W=add(B,scale(LAM,F(1,5)))
        oldW=add(S,vec(4),scale(sub(vec(25),LAM),F(-1,5)))
        assert W==oldW
        for k,bits in enumerate(TYPES):
            load=sum(bits[:6]); u=F(bits[0],load) if load else F(0)
            o=bits[7]
            if mode=='ordered':
                query=add(vec(1),*(scale(TAU[j],F(1,7-j)) for j in J))
                new=sub(scale(A,u),scale(add(W,query),F(o,6)))
                old=sub(scale(A,u),scale(add(oldW,query),F(o,6)))
            else:
                t=bits[targets['C' if mode=='C-only' else mode]]
                query=add(vec(F(o,6*(1+5*t))),*(scale(TAU[j],F(o,6*((j-1)*t+7-j))) for j in J))
                new=sub(scale(A,u),add(scale(W,t),query))
                old=sub(scale(A,u),add(scale(oldW,t),query))
                if mode=='C-only':
                    # E_C has customer coefficient c, K coefficient -1.
                    old=add(old,scale(B,t))
                    new=sub(scale(A,u),add(scale(LAM,F(t,5)),query))
            assert new==old
            coltext.append('\t'.join([mode,str(k),','.join(ss(new)),','.join(ss(old)),','.join(ss(sub(new,old)))]))
        new=vec(1) if mode=='C-only' else S
        old=sub(S,B) if mode=='C-only' else S
        assert new==old
        coltext.append('\t'.join([mode,'512',','.join(ss(new)),','.join(ss(old)),','.join(ss(sub(new,old)))]))
    (HERE/'all_513_affine_column_identities.tsv').write_text('\n'.join(coltext)+'\n')

    oldrows6=json.loads(SOURCES[7].read_text())['rows']
    oldrows5=json.loads(SOURCES[10].read_text())['rows']
    correspondence=[]; column_count=0; equality_count=0
    for domain in domains:
        q0=F(domain['q0']); beta,B,S=weights(q0); W=add(B,scale(LAM,F(1,5)))
        rows=oldrows6 if q0==F(1,6) else oldrows5
        index={(r['vertex_id'],r.get('forced_target','ordered')):(i,r)
               for i,r in enumerate(rows) if r['source']==1}
        for v in domain['vertices']:
            p=tuple(map(F,v['parameters']))
            for target in (list(targets) if q0==F(1,6) else ['ordered']):
                raw,r=index[(v['old_vertex_id'],target)]
                expected=[]
                for bits in TYPES:
                    load=sum(bits[:6]); u=F(bits[0],load) if load else F(0); o=bits[7]
                    if target=='ordered':
                        G=ev(add(W,vec(1),*(scale(TAU[j],F(1,7-j)) for j in J)),p)/6
                        x=ev(A,p)*u-o*G
                    else:
                        t=bits[targets[target]]
                        m=ev(W,p)*t+F(o,6*(1+5*t))+sum(p[j-2]*F(o,6*((j-1)*t+7-j)) for j in J)
                        x=ev(A,p)*u-m
                    expected.append(x)
                expected.append(ev(S,p))
                assert all(expected[k]==F(r['a'][str(k)]) for k in range(513))
                column_count+=513
                rowhash=hashlib.sha256((','.join(ss(expected))).encode()).hexdigest()
                correspondence.append({'q0':str(q0),'vertex_id':v['id'],'target':target,
                    'old_vertex_id':v['old_vertex_id'],'old_raw_index':raw,'old_name':r['name'],
                    'all_513_columns_equal':True,'canonical_coefficient_sha256':rowhash})
                if target=='C':
                    b=ev(B,p); conly=[x+b*bits[8] for x,bits in zip(expected[:512],TYPES)]+[F(1)]
                    assert all(conly[k]-expected[k]==b*TYPES[k][8] for k in range(512))
                    assert conly[512]-expected[512]==-b
                    equality_count+=513
                    correspondence.append({'q0':str(q0),'vertex_id':v['id'],'target':'C-only',
                        'old_vertex_id':v['old_vertex_id'],'old_raw_index':raw,
                        'free_equality':'E_C=|C|-K','free_equality_multiplier':str(b),
                        'all_513_equality_columns_checked':True,
                        'canonical_coefficient_sha256':hashlib.sha256((','.join(ss(conly))).encode()).hexdigest()})
    dump('old_row_correspondence.json',{'entries':correspondence,
        'existing_exact_row_identities':810,'existing_row_columns_checked':column_count,
        'C_only_equality_representations':90,'C_only_columns_checked':equality_count,
        'new_inequality_information_modulo_E_C':0,'duplicate_raw_matrix_materialized':False})
    assert column_count==810*513 and equality_count==90*513
    for p,pin in zip(SOURCES,pins): assert sha(p)==pin['sha256']
    dump('closure_summary.json',{'status':'PASS_EXACT_REPARAMETRIZATION_NO_NEW_ROWS',
        'actual_agent_id':'/root/source1_lambda_complete','q0_values':['1/6','1/5'],
        'facets':[19,19],'vertices':[90,90],'raw_tail_forms':64,
        't0_affine_checks':128,'query_slope_checks':64,'cap_necessity_checks':8,
        'ordered_continuous_multiplicity_proof':True,'facet_necessity_witnesses':38,
        'symbolic_column_identities':10*513,'old_row_column_identities':column_count,
        'C_only_column_identities':equality_count,'new_rows':0,'optimizer_calls':0,
        'all_direct_sources_unchanged':True})
    print(json.dumps({'status':'PASS','facets':[19,19],'vertices':[90,90],
                      'full_old_columns_checked':column_count,'C_only_columns':equality_count,
                      'new_rows':0},ensure_ascii=False))

if __name__=='__main__': main()
