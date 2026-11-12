#!/usr/bin/env python3
"""Independent JSON-only local checker: no generator/project code imports.

Reconstructs true shares and per-index legal queries, then computes minima.
Independent geometry uses exact edge clipping and triangular slice corners.
Only the five pinned original model/proof/contracts and this package are read.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product, combinations
import hashlib
import json

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[3]
NAMES = ('tau3','tau4','tau5','lambda')


def read(name):
    return json.loads((OUT/name).read_text())


def encode(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [encode(v) for v in x]
    return x


def save(name,obj):
    (OUT/name).write_text(json.dumps(encode(obj),ensure_ascii=False,indent=2)+'\n')


def scalar(a,b):
    value=Q(0)
    for x,y in zip(a,b):value+=x*y
    return value


def matrix_rank(vectors):
    work=[list(v) for v in vectors]
    if not work:return 0
    used=0
    for c in range(len(work[0])):
        found=None
        for r in range(used,len(work)):
            if work[r][c]!=0:found=r;break
        if found is None:continue
        work[used],work[found]=work[found],work[used]
        denominator=work[used][c]
        for h in range(c,len(work[used])):work[used][h]/=denominator
        for r in range(used+1,len(work)):
            factor=work[r][c]
            for h in range(c,len(work[r])):work[r][h]-=factor*work[used][h]
        used+=1
        if used==len(work):break
    return used


def variables(k):
    return tuple(Q(int(i==k)) for i in range(4))


def extract_affine(f):
    base=f((Q(0),)*4)
    return (base,)+tuple(f(variables(k))-base for k in range(4))


def wallet(q0,x):
    h3,h4,h5,lam=x
    b3=q0/2+h3+q0*h4/12+q0*h5/6
    b4=q0/2+h4+q0*h5/6
    b5=q0/2+h5
    return lam+h3+h4+h5,(b3,b4,b5),1+b3+b4+b5


def literal(q0,x,p,t,q,tail):
    a,beta,S=wallet(q0,x)
    members=(t,)+tuple(tail)
    final_load=p+sum(members)
    shares=[Q(bit,final_load) if final_load else Q(0) for bit in members]
    # The sign is reconstructed from source IC, caps, last BR, and internal SAFE.
    result=a*shares[0]
    for j in range(3):result+=beta[j]*tail[j]-x[j]*shares[j+1]
    result+=tail[3]-shares[4]
    preceding=p+t
    for j in range(3):
        result+=x[j]*q/(preceding+4-j)
        preceding+=tail[j]
    result+=q/(preceding+1)
    return result


def literal_menu(q0,x,p,t,tail,menu,excluded=None):
    # Sum each legal label query separately, including repeated covered labels.
    base=literal(q0,x,p,t,Q(0),tail)
    inds=[l for l in range(6) if l!=excluded]
    divider=len(inds)
    for l in inds:
        member=menu[l]
        previous=p+t
        for j in range(3):
            base+=x[j]*Q(member,divider*(previous+4-j))
            previous+=tail[j]
        base+=Q(member,divider*(previous+1))
    return base


def W(q0,x,p):
    return sum(wallet(q0,x)[1])+x[3]/(p+4)


def Z(q0,x,p):
    return q0*(Q(1,p+1)+x[0]/(p+4)+x[1]/(p+3)+x[2]/(p+2))


def cost_zero_query_gap(q0,x,p,missing,z):
    tail=tuple(0 if j in missing else 1 for j in (3,4,5))+(z,)
    return literal(q0,x,p,1,Q(0),tail)-W(q0,x,p)


def original_halfspaces(q0):
    facets=[]
    for k in range(3):
        v=[Q(0)]*4;v[k]=-1
        facets.append(('tau%d_nonnegative'%(k+3),tuple(v),Q(0)))
    facets.append(('lambda_lower',(Q(0),Q(0),Q(0),Q(-1)),Q(-9)))
    v=extract_affine(lambda x:20*cost_zero_query_gap(q0,x,0,(),1))
    facets.append(('lambda_upper',tuple(-y for y in v[1:]),v[0]))
    for group,p,z in (('A',1,0),('B',0,1)):
        for j in (3,4,5):
            v=extract_affine(lambda x:cost_zero_query_gap(q0,x,p,(j,),z))
            facets.append((group+str(j),tuple(-y for y in v[1:]),v[0]))
    return facets


def room(face,x):return face[2]-scalar(face[1],x)


def clipped_vertices(necessary):
    bounds=[]
    for j in range(3):
        v=[Q(0)]*4;v[j]=-1;bounds.append(('box_low_'+str(j),tuple(v),Q(0)))
        v=[Q(0)]*4;v[j]=1;bounds.append(('box_high_'+str(j),tuple(v),Q(1)))
    bounds+=necessary[3:5]
    vertices=set(tuple(Q(y) for y in z) for z in product((0,1),(0,1),(0,1),(9,16)))
    stages=[]
    for face in necessary[5:]:
        old=list(vertices)
        kept={x for x in old if room(face,x)>=0}
        new_edges=0
        for u,v in combinations(old,2):
            ru,rv=room(face,u),room(face,v)
            if ru*rv>=0:continue
            common=[f[1] for f in bounds if room(f,u)==room(f,v)==0]
            if matrix_rank(common)!=3:continue
            # Only a genuine old edge is cut; never arbitrary vertex chords.
            theta=ru/(ru-rv)
            w=tuple(u[k]+theta*(v[k]-u[k]) for k in range(4))
            assert room(face,w)==0
            kept.add(w);new_edges+=1
        bounds.append(face);vertices=kept
        assert all(room(f,x)>=0 for x in vertices for f in bounds)
        stages.append({'cut':face[0],'vertices_before':len(old),'crossing_true_edges':new_edges,'vertices_after':len(vertices)})
    return vertices,stages


def corner_vertices(q0):
    found=set()
    for lam in (9,15,16):
        alpha=min(Q(lam,20),Q(3,4))-q0/2
        for e3,e4,e5 in product((0,1),repeat=3):
            if lam==15 and (e3,e4,e5)==(0,0,0):continue
            h5=e5*4*alpha/3
            h4=e4*Q(4,3)*(alpha-q0*h5/6)
            h3=e3*Q(4,3)*(alpha-q0*h4/12-q0*h5/6)
            assert alpha-q0*h5/6>0 and alpha-q0*h4/12-q0*h5/6>0
            found.add((h3,h4,h5,Q(lam)))
    return found


def decoded_bits(col,n):return tuple((col>>j)&1 for j in range(n-1,-1,-1))


def main():
    pins=read('source_pins.json')
    for src in pins['sources']:
        raw=(REPO/src['repository_relative_path']).read_bytes()
        assert len(raw)==src['bytes'] and hashlib.sha256(raw).hexdigest()==src['sha256']
    datasets=read('parameter_domains.json')['families']
    analytics=read('analytic_state_checks.json')
    assert read('state_halfspaces.json')=={g:a['state_halfspaces'] for g,a in analytics.items()}
    witnesses=read('necessary_facet_witnesses.json')
    tails=tuple(decoded_bits(k,4) for k in range(16))
    vertices={};gcheck={};acheck={};count={'optimizers':0,'global_LP_inputs_or_points_read':0}
    full_rho=0
    for group,q0 in (('six_mean',Q(1,6)),('ordered_five',Q(1,5))):
        dom=datasets[group]
        assert dom['dimension']==4 and dom['variable_order']==list(NAMES)
        hs=original_halfspaces(q0)
        assert len(hs)==11
        for saved,derived in zip(dom['facets'],hs):
            assert saved['id']==derived[0]
            assert tuple(map(Q,saved['normal']))==derived[1] and Q(saved['rhs'])==derived[2]
        clipped,stages=clipped_vertices(hs);corners=corner_vertices(q0)
        supplied={tuple(map(Q,v['point'])) for v in dom['vertices']}
        assert clipped==corners==supplied and len(clipped)==23
        vertices[group]={v['id']:tuple(map(Q,v['point'])) for v in dom['vertices']}
        face_checks=[]
        for face in hs:
            on=[x for x in clipped if room(face,x)==0]
            ar=matrix_rank([[u-v for u,v in zip(x,on[0])] for x in on[1:]])
            assert ar==3
            saved=next(f for f in dom['facets'] if f['id']==face[0])
            assert saved['affine_rank']==ar and len(saved['vertex_ids'])==len(on)
            assert {vertices[group][vid] for vid in saved['vertex_ids']}==set(on)
            face_checks.append({'facet':face[0],'vertices_on_facet':len(on),'affine_rank':ar})
        for v in dom['vertices']:
            x=vertices[group][v['id']]
            active=[f[0] for f in hs if room(f,x)==0]
            assert active==v['active_facets']
            normals=[f[1] for f in hs if f[0] in v['independent_active_basis']]
            assert len(normals)==matrix_rank(normals)==4
            a,beta,S=wallet(q0,x)
            assert a>=9 and all(b>=q0/2 for b in beta)
            for p in (0,1):
                for tail in tails:
                    assert literal(q0,x,p,1,Q(0),tail)>=W(q0,x,p)
                    full_rho+=1
        for wit in witnesses[group]:
            pt=tuple(map(Q,wit['point_violating_only_this_facet']))
            for face in hs:
                s=room(face,pt)
                assert s==Q(wit['all_facet_slacks'][face[0]])
                assert (s<0)==(face[0]==wit['facet'])
            assert wallet(q0,pt)[0]==Q(wit['source_IC_weight'])>0
            if 'corresponding_true_rho' in wit:
                facet=next(f for f in dom['facets'] if f['id']==wit['facet'])
                st=facet['state']
                rr=cost_zero_query_gap(q0,pt,st['p'],tuple(st['missing']),st['z'])
                assert rr==Q(wit['corresponding_true_rho'])<0
        # Reconstruct every retained affine expression and all free-cap necessities.
        for item in analytics[group]['state_halfspaces']:
            actual=extract_affine(lambda x:cost_zero_query_gap(q0,x,item['p'],item['missing'],item['tail'][3]))
            assert actual==tuple(map(Q,item['affine_coefficients']))
        for item in analytics[group]['t0_nonnegative_coefficients']:
            p,q,tail=item['p'],Q(item['q']),tuple(item['tail'])
            actual=extract_affine(lambda x:literal(q0,x,p,0,q,tail)-(Z(q0,x,p) if q else 0))
            assert actual==tuple(map(Q,item['coefficients']))
            assert all(k>=0 for k in actual[:4]) and actual[4]==0
        for item in analytics[group]['t1_query_slope_nonnegative_coefficients']:
            p,tail=item['p'],tuple(item['tail'])
            actual=extract_affine(lambda x:literal(q0,x,p,1,Q(1),tail)-literal(q0,x,p,1,Q(0),tail)-(1+sum(x[:3]))/(p+5))
            assert actual==tuple(map(Q,item['coefficients']))
            assert all(k>=0 for k in actual[:4]) and actual[4]==0
        for item in analytics[group]['independent_beta_necessity']:
            j=item['j']-3
            def free_delta(y):
                tau=y[:3];beta=y[3:];r=[0,0,0];r[j]=1
                value=beta[j]-tau[j]+q0/2
                before=0
                for h in range(3):
                    value+=tau[h]*q0/(before+4-h)
                    before+=r[h]
                zero=q0+sum((tau[h]*q0/(4-h) for h in range(3)),Q(0))
                return value-zero
            origin=(Q(0),)*6;base=free_delta(origin)
            actual=(base,)+tuple(free_delta(tuple(Q(int(k==h)) for k in range(6)))-base for h in range(6))
            assert actual==tuple(map(Q,item['coefficients']))
        gcheck[group]={'exact_edge_clipping_stages':stages,'vertices':sorted(clipped,key=lambda x:(x[3],x[:3])),'matches_triangular_corners_and_generator':True,'facet_checks':face_checks}
        acheck[group]={'true_query_zero_state_count':len(analytics[group]['state_halfspaces']),'t0_quadrant_affines':len(analytics[group]['t0_nonnegative_coefficients']),'query_slope_affines':len(analytics[group]['t1_query_slope_nonnegative_coefficients']),'free_cap_necessary_states':len(analytics[group]['independent_beta_necessity'])}
    # Recompute all physical contexts and retain every weak-tie attaining tail.
    supplied_tables=read('conditional_minimum_tables.json')
    table_index={}
    for v in supplied_tables:
        key=(v['family'],v['vertex'],v['p'],v['t'],Q(v['q']))
        assert key not in table_index;table_index[key]=v
    mins={};all_costs={};attainers={};table_count=0;hidden_count=0;tie_count=0
    for group,q0 in (('six_mean',Q(1,6)),('ordered_five',Q(1,5))):
        for vid,x in vertices[group].items():
            for p in (0,1):
                contexts=[(t,Q(o,6)) for t in (0,1) for o in (0,1)] if group=='six_mean' else [(t,Q(d-t,5)) for d in range(7) for t in (0,1) if t<=d and d<=5+t]
                assert len(contexts)==(4 if group=='six_mean' else 12)
                for t,q in contexts:
                    key=(group,vid,p,t,q)
                    vals={tail:literal(q0,x,p,t,q,tail) for tail in tails}
                    m=min(vals.values());ties=[tail for tail in tails if vals[tail]==m]
                    saved=table_index[key]
                    assert m==Q(saved['minimum'])
                    assert ties==[tuple(tail) for tail in saved['all_attaining_tails']]
                    if t==1:assert m==W(q0,x,p)+q*(1+sum(x[:3]))/(p+5)
                    elif q==0:assert m==0
                    elif q==q0:assert m==Z(q0,x,p)
                    mins[key]=m;all_costs[key]=vals;attainers[key]=ties
                    table_count+=1;hidden_count+=len(vals);tie_count+=len(ties)
    assert table_count==len(table_index)==736 and hidden_count==11776
    hidden_records=read('hidden_state_checks.json');assert len(hidden_records)==hidden_count
    seen=set()
    for rec in hidden_records:
        key=(rec['family'],rec['vertex'],rec['p'],rec['t'],Q(rec['q']));tail=tuple(rec['tail'])
        assert (key,tail) not in seen;seen.add((key,tail))
        assert Q(rec['cost'])==all_costs[key][tail] and Q(rec['minimum'])==mins[key]
        assert Q(rec['slack'])==all_costs[key][tail]-mins[key]>=0
    # Continuous-domain strict W-Z comparison, including exact attaining endpoint.
    wz=[]
    for p in (0,1):
        coeff=extract_affine(lambda x:W(Q(1,5),x,p)-Z(Q(1,5),x,p))
        gap=extract_affine(lambda x:W(Q(1,5),x,p)-Z(Q(1,5),x,p)-2-Q(19,20)*sum(x[:3]))
        shifted=(gap[0]+9*gap[4],)+gap[1:]
        assert all(c>=0 for c in shifted)
        wz.append({'p':p,'W_minus_Z_coefficients':coeff,'minus_uniform_bound_coefficients_in_lambda_minus_9':shifted})
    assert W(Q(1,5),(Q(0),Q(0),Q(0),Q(9)),1)-Z(Q(1,5),(Q(0),Q(0),Q(0),Q(9)),1)==2
    projections={};outer_records=read('outer_average_tables.json');outer_by={}
    for rec in outer_records:outer_by[(rec['vertex'],rec['p'],rec['d'])]=rec
    assert len(outer_by)==len(outer_records)==322
    for vid,x in vertices['ordered_five'].items():
        for p in (0,1):
            vals=[]
            for d in range(7):
                value=Q(0)
                if d<6:value+=(6-d)*mins[('ordered_five',vid,p,0,Q(d,5))]
                if d>0:value+=d*mins[('ordered_five',vid,p,1,Q(d-1,5))]
                value/=6;vals.append(value)
                rec=outer_by[(vid,p,d)]
                assert Q(rec['f'])==value
            G=min(vals[1:]);assert vals[0]==0 and [d for d in range(1,7) if vals[d]==G]==[1]
            assert G==(5*Z(Q(1,5),x,p)+W(Q(1,5),x,p))/6
            for d in range(1,7):
                bound=(d-1)*(W(Q(1,5),x,p)-Z(Q(1,5),x,p))/6
                assert vals[d]-G>=bound
                rec=outer_by[(vid,p,d)]
                assert Q(rec['G'])==G and Q(rec['projection_slack'])==vals[d]-G
                assert Q(rec['strict_gap_bound'])==bound
            projections[(vid,p)]=(G,vals)
    menu_records=read('all_64_ordered_menu_checks.json');assert len(menu_records)==2944
    menu_seen=set();menu_branch_count=0;literal_attaining_checks=0
    for rec in menu_records:
        vid,p=rec['vertex'],rec['p'];menu=tuple(rec['six_membership_bits']);x=vertices['ordered_five'][vid]
        assert (vid,p,menu) not in menu_seen;menu_seen.add((vid,p,menu))
        d=sum(menu);total=Q(0)
        for k in range(6):
            q=sum((Q(menu[l],5) for l in range(6) if l!=k),Q(0))
            assert q==Q(d-menu[k],5)
            key=('ordered_five',vid,p,menu[k],q);m=mins[key]
            saved=rec['branches'][k]
            assert saved['outer_index']==k+1 and saved['t']==menu[k] and Q(saved['inner_q'])==q and Q(saved['minimum'])==m
            for tail in attainers[key]:
                assert literal_menu(Q(1,5),x,p,menu[k],tail,menu,k)==m
                literal_attaining_checks+=1
            total+=m;menu_branch_count+=1
        total/=6;G,fd=projections[(vid,p)]
        assert total==fd[d]==Q(rec['average'])
        assert Q(rec['union_bound'])==(G if d else 0) and Q(rec['slack'])==total-(G if d else 0)>=0
    # Five-query identity is checked by summing actual indexed members for every denominator.
    indexed_query_checks=0
    for mask in range(64):
        menu=decoded_bits(mask,6)
        for k in range(6):
            for denominator in range(1,7):
                actual=sum((Q(menu[l],5*denominator) for l in range(6) if l!=k),Q(0))
                assert actual==Q(sum(menu)-menu[k],5*denominator)
                indexed_query_checks+=1
    # Pure six-query union weakening is checked for all 4096 membership contexts.
    pure_query=read('all_64_pure_query_checks.json');assert len(pure_query)==4096
    pure_seen=set()
    for item in pure_query:
        p,t,tail,menu=item['p'],item['t'],tuple(item['tail']),tuple(item['menu'])
        assert (p,t,tail,menu) not in pure_seen;pure_seen.add((p,t,tail,menu))
        d=sum(menu);o=int(d>0)
        coeff=extract_affine(lambda x:literal_menu(Q(1,6),x,p,t,tail,menu)-literal(Q(1,6),x,p,t,Q(o,6),tail))
        assert coeff==tuple(map(Q,item['weakening_delta_coefficients']))
        assert all(c>=0 for c in coeff[:4]) and coeff[4]==0
    # Full 513-column contract; no support reduction, target deletion, or row pruning.
    contract=read('coordinate_contract.json');assert contract['variables']==513 and len(contract['columns'])==513
    assert contract['bit_order']==['a1','a2','a3','a4','a5','a6','x','o','c']
    for col in range(512):assert decoded_bits(col,9)==tuple(contract['columns'][col]['bits'])
    assert contract['columns'][512]=={'column':512,'kind':'independent_K'}
    family=read('exact_family.json');rows=family['rows'];assert family['row_count']==len(rows)==230
    rowids={r['id'] for r in rows};assert len(rowids)==230
    expected=set()
    for vid in vertices['six_mean']:
        expected|={'six_general_'+vid+'_'+t for t in ('A1','A2','A3','A4','A5','A6','X','C')}
        expected.add('six_C_only_'+vid)
    expected|={'ordered_'+vid for vid in vertices['ordered_five']}
    assert rowids==expected
    catalog=read('row_catalog.json')
    by_catalog={r['id']:r for r in catalog}
    assert len(catalog)==len(by_catalog)==230 and set(by_catalog)==rowids
    derived={};column_count=0
    with (OUT/'full_column_checks.tsv').open('w') as stream:
        stream.write('row_id\tcolumn\tsupplied_raw\tliteral_raw\traw_residual\tdivided_by_25_residual\n')
        for row in rows:
            vid=row['vertex'];group='ordered_five' if row['family']=='ordered_five' else 'six_mean'
            q0=Q(1,5) if group=='ordered_five' else Q(1,6)
            x=vertices[group][vid];a,beta,S=wallet(q0,x);raw=[]
            metadata=by_catalog[row['id']]
            assert Q(metadata['q0'])==q0 and tuple(map(Q,metadata['parameters']))==x
            assert Q(metadata['source_IC_weight'])==a and tuple(map(Q,metadata['middle_caps']))==beta
            assert Q(metadata['K_coefficient'])==(1 if row['family']=='six_C_only' else S)
            assert metadata['uses_C_equality']==(row['family']=='six_C_only')
            if row['family']=='six_C_only':assert Q(metadata['free_C_equality_multiplier'])==sum(beta)
            if group=='six_mean':assert metadata['target']==row['target']
            for col in range(512):
                bits=decoded_bits(col,9);load=sum(bits[:6]);share=Q(bits[1],load) if load else Q(0)
                p,o=bits[0],bits[7]
                if group=='ordered_five':
                    projected=projections[(vid,p)][0]
                    value=a*share-o*projected
                    closed=(sum(beta)+x[3]/(p+4)+Q(1,p+1)+x[0]/(p+4)+x[1]/(p+3)+x[2]/(p+2))/6
                    assert projected==closed
                else:
                    target=row['target']
                    index=int(target[1:])-1 if target.startswith('A') else (6 if target=='X' else 8)
                    t=bits[index]
                    value=a*share-mins[(group,vid,p,t,Q(o,6))]
                    closed=t*(sum(beta)+x[3]/(p+4))+Q(o,6*(p+1+4*t))
                    for j in range(3):closed+=x[j]*Q(o,6*(p+(j+1)*t+4-j))
                    assert closed==mins[(group,vid,p,t,Q(o,6))]
                    if row['family']=='six_C_only':value+=sum(beta)*bits[8]
                raw.append(value)
            raw.append(Q(1) if row['family']=='six_C_only' else S)
            assert len(row['raw_coefficients'])==len(row['coefficients_divided_by_25'])==513
            for col,value in enumerate(raw):
                supplied=Q(row['raw_coefficients'][col]);normalized=Q(row['coefficients_divided_by_25'][col])
                error=supplied-value;scaled_error=normalized-value/25
                assert error==scaled_error==0
                stream.write('%s\t%d\t%s\t%s\t%s\t%s\n'%(row['id'],col,supplied,value,error,scaled_error))
                column_count+=1
            derived[row['id']]=raw
    eq_records=read('C_equality_column_checks.json');assert len(eq_records)==23*513
    for rec in eq_records:
        vid,col=rec['vertex'],rec['column'];x=vertices['six_mean'][vid];B=sum(wallet(Q(1,6),x)[1])
        ec=Q(decoded_bits(col,9)[8]) if col<512 else Q(-1)
        assert Q(rec['multiplier'])==B and Q(rec['E_C_coefficient'])==ec
        error=derived['six_general_'+vid+'_C'][col]-derived['six_C_only_'+vid][col]+B*ec
        assert error==Q(rec['residual'])==0
    for src in pins['sources']:
        assert hashlib.sha256((REPO/src['repository_relative_path']).read_bytes()).hexdigest()==src['sha256']
    count.update({'domains':2,'independent_exact_clipped_vertices':46,'irreducible_facets':22,'full_vertex_true_query_zero_rho_checks':full_rho,'affine_true_query_zero_states':64,'affine_t0_quadrant_checks':128,'affine_t1_query_slope_checks':64,'free_cap_minimality_checks':6,'physical_conditional_minimum_tables':table_count,'full_hidden_state_checks':hidden_count,'all_weak_tie_attainers':tie_count,'ordered_outer_average_rows':len(outer_records),'all_64_ordered_menu_contexts':len(menu_records),'actual_inner_five_means':menu_branch_count,'actual_menu_attaining_tail_cost_checks':literal_attaining_checks,'indexed_five_query_denominator_identities':indexed_query_checks,'all_64_pure_six_query_contexts':len(pure_query),'rows':len(rows),'full_columns':column_count,'free_C_equality_column_identities':len(eq_records)})
    assert count['full_columns']==117990
    save('literal_geometry_checks.json',gcheck)
    save('literal_analytic_checks.json',{'checks':acheck,'W_minus_Z':wz})
    save('literal_checker_output.json',{'status':'PASS','counts':count,'five_source_pins_unchanged':True,'independent_of_generator_code':True,'reads_global_LP_or_candidates':False,'no_row_pruning':True,'methods':['direct individual final shares','per-index legal queries','all physical tails with all weak ties','exact true-edge clipping','triangular slice corners','full 513-column reconstruction']})
    print(json.dumps(encode({'status':'PASS','counts':count}),ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
