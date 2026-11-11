#!/usr/bin/env python3
"""Independent literal checker: no builder import, no optimizer, all raw rows/types."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product,combinations_with_replacement
from hashlib import sha256
from math import lcm,gcd
import json

H=Path(__file__).resolve().parent;WS=H.parent;ROOT=WS.parents[2];Z=Q(0)
def digest(p):return sha256(p.read_bytes()).hexdigest()
def save(n,o):(H/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def pay(bit,others):return Q(bit,others+bit) if bit else Z
def fraction(num,den):return Q(num,den) if den else Z
def bits7(j):return [(j>>k)&1 for k in range(6,-1,-1)]
def query_members(role,bits):return [bits[6],0,0,0,0,0] if role=='Omean' else [bits[0 if role=='C' else int(role[1:])-1]]
def query_safe(role,bits,others):
    members=query_members(role,bits)
    return sum((pay(q,others) for q in members),Z)/len(members)
def pair_cost(left,right,bits,others):
    ls=query_members(left,bits);rs=query_members(right,bits)
    return sum((pay(l,others)+pay(r,others+l) for l in ls for r in rs),Z)/(len(ls)*len(rs))
def tail_wallet(bits):
    bg=sum(bits[:4]);y,z=bits[4:6]
    return pay(y,bg+z)+pay(z,bg+y)+pay(y,bg)-pay(y,bg+y)
def literal_old(row,bits):
    l=bits[:6];total=sum(l);family=row['family']
    if family=='ROOT_IC':return -pay(l[0],total-l[0])
    if family=='CAP':return -Q(l[row['source']-1])
    if family=='UNION':return -Q(any(l))
    if family=='FLOOR':return Z
    if family=='SAFE':
        j=row['source'];return pay(l[j-1],total-l[j-1])-query_safe(row['queries'][0],bits,sum(l[:j-1])+6-j)
    assert family=='PAIR'
    return tail_wallet(bits)-pair_cost(*row['queries'],bits,sum(l[:4]))
def original_descriptors():
    out=[{'name':'ROOT_IC','family':'ROOT_IC'}]
    out += [{'name':f'CAP_B{j}','family':'CAP','source':j} for j in range(2,7)]
    out += [{'name':'BRANCH_UNION_OPT','family':'UNION'},{'name':'ROOT_K_FLOOR','family':'FLOOR'}]
    roles=['C','B2','B3','B4','B5','B6','Omean']
    out += [{'name':f'SAFE_j{i}|{q}','family':'SAFE','source':i,'queries':[q]} for i in range(2,7) for q in roles]
    out += [{'name':f'PAIR|{q}|{r}','family':'PAIR','queries':[q,r]} for q,r in combinations_with_replacement(roles,2)]
    return out
def requery_cost(bits,q,tail,inner):
    b=sum(bits[:2]);r,y,t=tail;bg=b+q+r;o=bits[6];menu=[o,0,0,0,0,0]
    source=126000*pay(q,b+r+y+t)
    old4=sum((weight*pay(bit,b+bits[2]+2) for weight,bit in zip((43,31218,34458),tail)),Z)
    old6=1654*sum((pay(bit,b+bits[2]+bits[3]+bits[4]) for bit in tail),Z)
    last=5400*(sum((pay(v,bg+y) for v in menu),Z)/6-pay(t,bg+y))
    wallet=pay(y,bg+t)+pay(t,bg+y)+pay(y,bg)-pay(y,bg+y)
    indices=[(a,c) for a in range(6) for c in range(6) if inner==36 or a!=c]
    query=sum((pay(menu[a],bg)+pay(menu[c],bg+menu[a]) for a,c in indices),Z)/inner
    return source+old4+old6+last+7740*(query-wallet)
def reconstruct_cuts():
    env30=json.loads((WS/'main_thirty_index_strengthening/requery30_envelopes.json').read_text())
    env36=json.loads((WS/'maximal_root_opt_requery/universal_moment_envelope.json').read_text())
    cuts={};state_records=[];envelope_records=[]
    for inner,source,field in [(36,env36,'minimum'),(30,env30,'m30')]:
        coeff={}
        for j in range(128):
            bits=bits7(j);o=bits[6]
            values={q:[(tail,requery_cost(bits,q,tail,inner)) for tail in product((0,1),repeat=3)] for q in (0,1)}
            a0=min(v for _,v in values[0]);a1=min(v for _,v in values[1])
            delta=max(a1-a0,Z);gamma=max(a0-a1,Z)
            m=a0 if not o else min((5*a0+a1)/6,a1)
            assert a0==Q(source[j]['a0']) and a1==Q(source[j]['a1']) and m==Q(source[j][field])
            assert m==a0+delta*Q(o,6)-gamma*o
            for q in (0,1):
                for tail,value in values[q]:
                    residual=value+(gamma-delta)*q-a0;assert residual>=0
                    if inner==30:state_records.append({'h':j,'q':q,'tail':list(tail),'cost':str(value),'residual':str(residual)})
            l=bits[:6];v=lambda i:pay(l[i-1],sum(l)-l[i-1])
            coeff[j]=126000*v(3)+65719*v(4)+4962*v(6)-m
            if inner==30:
                assert coeff[j]==Q(source[j]['cut'])
                envelope_records.append({'h':j,'bits':bits,'a0':str(a0),'a1':str(a1),'delta':str(delta),'gamma':str(gamma),'m30':str(m),'coefficient':str(coeff[j])})
        cuts[inner]=coeff
    save('literal_c30_states.json',state_records);save('literal_c30_envelopes.json',envelope_records)
    return cuts
def literal_p25_minimum(i,p,t,q):
    n=6-i;values=[]
    for tail in product((0,1),repeat=n):
        mid=sum(tail[:-1]);z=tail[-1]
        value=fraction(25*t-z,p+t+mid+z)+Q(mid,2)+z+pay(q,p+t+mid)
        values.append((tail,value))
    target=Q(n+1,2)*t+Q(24*t,p+n+1)+pay(q,p+n*t)
    assert min(v for _,v in values)==target
    return target,values
def p25_literal_checks():
    table={};state_records=[];menu_records=[];single_records=[]
    for i in range(2,6):
        n=6-i
        for p in range(i):
            for t,q in product((0,1),repeat=2):
                minimum,values=literal_p25_minimum(i,p,t,q);table[i,p,t,q]=minimum
                for tail,value in values:
                    state_records.append({'i':i,'p':p,'t':t,'q':q,'tail':list(tail),'cost':str(value),'minimum':str(minimum),'residual':str(value-minimum)})
            for member in product((0,1),repeat=6):
                o=int(any(member))
                double=sum((table[i,p,member[a],member[b]] for a in range(6) for b in range(6) if a!=b),Z)/30
                target=Q(o,6)*(table[i,p,1,0]+table[i,p,0,1]);assert double>=target
                menu_records.append({'i':i,'p':p,'menu':list(member),'exact30':str(double),'lower':str(target),'residual':str(double-target)})
                for pure in (0,1):
                    pure_mean=sum((table[i,p,pure,q] for q in member),Z)/6
                    pm=table[i,p,pure,0]+Q(o,6)*(table[i,p,pure,1]-table[i,p,pure,0]);assert pure_mean>=pm
                    mean_pure=sum((table[i,p,t,pure] for t in member),Z)/6
                    mp=table[i,p,0,pure]+Q(o,6)*(table[i,p,1,pure]-table[i,p,0,pure]);assert mean_pure>=mp
                    single_records.append({'i':i,'p':p,'menu':list(member),'pure':pure,'pure_mean_residual':str(pure_mean-pm),'mean_pure_residual':str(mean_pure-mp)})
    save('literal_p25_states.json',state_records);save('literal_p25_menus.json',{'double30':menu_records,'single':single_records})
    return table,{'states':len(state_records),'minima':len(table),'double_menu_states':len(menu_records),'single_menu_checks':2*len(single_records)}
def p25_coefficient(row,bits,table):
    i=row['source'];p=sum(bits[:i-1]);n=6-i
    T=row['T'];Qrole=row['Q'];o=bits[6]
    member=lambda role:bits[0 if role=='C' else int(role[1:])-1]
    if T!='Omean' and Qrole!='Omean':cost=table[i,p,member(T),member(Qrole)]
    elif T!='Omean':
        t=member(T);cost=table[i,p,t,0]+Q(o,6)*(table[i,p,t,1]-table[i,p,t,0])
    elif Qrole!='Omean':
        q=member(Qrole);cost=table[i,p,0,q]+Q(o,6)*(table[i,p,1,q]-table[i,p,0,q])
    else:cost=Q(o,6)*(table[i,p,1,0]+table[i,p,0,1])
    return 25*pay(bits[i-1],sum(bits[:6])-bits[i-1])-cost
def check_input():
    inp=json.loads((H/'exact_input.json').read_text());rows=inp['raw_rows'];K=Q(inp['fixed_K'])
    assert K==Q(87254934961879537539921985657780687995,449980920529477462633417363589807278334) and Q(inp['fixed_O'])==1
    assert len(rows)==270 and len(set(r['name'] for r in rows))==270
    assert inp['atoms']==[{'index':j,'bits':bits7(j)} for j in range(128)]
    assert inp['nonnegative_columns']==list(range(129)) and inp['root_u_column']==128 and inp['objective']=={'128':'1'}
    assert inp['convention']=='A*x >= bK*K+bO*O'
    assert inp['source_review_sha256']==digest(H/'source_review.md')
    for p,d in inp['source_bindings'].items():assert digest(WS/p)==d
    assert inp['source_bindings']['maximal_root_tail_wallet_v2/exact_input.json']=='86a235bf210862ef8f8bbbdea7ac324e71f691a8aa7af455a821e6379cfe117d'
    old=json.loads((WS/'maximal_root_tail_wallet_v2/exact_input.json').read_text())
    for row,prior in zip(rows[:72],old['raw_rows']):
        assert {k:v for k,v in row.items() if k!='rhs'}=={k:v for k,v in prior.items() if k!='rhs'}
        assert Q(row['rhs'])==Q(row['bK'])*K+Q(row['bO'])
    cuts=reconstruct_cuts();table,p25counts=p25_literal_checks();descs=original_descriptors();matrix=[]
    for row,desc in zip(rows[:71],descs):assert {k:row[k] for k in desc}==desc
    assert rows[71]['name']=='OPT_SOURCE3_REQUERY_CUT' and rows[71]['family']=='REQUERY_CUT'
    assert rows[72]['name']=='PAIR30|Omean|Omean' and rows[72]['family']=='PAIR30'
    assert rows[73]['name']=='OPT_SOURCE3_REQUERY_30_CUT' and rows[73]['family']=='REQUERY_30_CUT'
    roles=['C','B2','B3','B4','B5','B6','Omean']
    expected=[(i,t,q) for i in range(2,6) for t in roles for q in roles]
    assert [(r['source'],r['T'],r['Q']) for r in rows[74:]]==expected
    source25=json.loads((WS/'main_all_source25_family/exact_family.json').read_text())
    original25={r['name']:r for r in source25['rows']};crosschecks=0
    for ri,row in enumerate(rows):
        coefficients=[]
        for j in range(128):
            bits=bits7(j)
            if ri<71:value=literal_old(row,bits)
            elif ri==71:value=cuts[36][j]
            elif ri==72:
                menu=[bits[6],0,0,0,0,0];bg=sum(bits[:4])
                cost=sum((pay(menu[a],bg)+pay(menu[b],bg+menu[a]) for a in range(6) for b in range(6) if a!=b),Z)/30
                value=tail_wallet(bits)-cost
            elif ri==73:value=cuts[30][j]
            else:value=p25_coefficient(row,bits,table)
            coefficients.append(value);assert value==Q(row['a'].get(str(j),'0')),(ri,j,value,row['a'].get(str(j),'0'))
        u=Q(int(row['family'] in ('ROOT_IC','FLOOR')));coefficients.append(u)
        assert u==Q(row['a'].get('128','0')) and all(0<=int(j)<129 for j in row['a'])
        family=row['family'];bK=-Q(1) if family=='CAP' else (Q(1,6) if family=='FLOOR' else (-Q(7-row['source'],2) if ri>=74 else Z))
        bO=-Q(1) if family=='UNION' else Z
        assert Q(row['bK'])==bK and Q(row['bO'])==bO and Q(row['rhs'])==bK*K+bO
        scale=Q(126000) if ri in (71,73) else (Q(25) if ri>=74 else Q(1))
        assert Q(row['numerical_divisor'])==scale>0
        if ri>=74:
            ix=lambda role:roles.index(role)+1 if role!='Omean' else 8
            source=original25[f"PORTFOLIO25_i{row['source']}_T{ix(row['T'])}_Q{ix(row['Q'])}"]
            for a in range(64):
                for o in (0,1):
                    for x in (0,1):
                        assert coefficients[2*a+o]==Q(source['a'][str(4*a+2*x+o)]);crosschecks+=1
            assert -bK==Q(source['a']['256']);crosschecks+=1
        matrix.append(coefficients)
    expected_eq=[{'name':'C_size','a':{str(j):'1' for j in range(128) if bits7(j)[0]},'rhs':str(K),'parameter':'K'},
                 {'name':'OPT_union','a':{str(j):'1' for j in range(128) if bits7(j)[6]},'rhs':'1','parameter':'O'}]
    assert inp['equalities']==expected_eq
    pair30checks=0
    for D in range(1,6):
        for menu in product((0,1),repeat=6):
            value=sum((pay(menu[a],D-1)+pay(menu[b],D-1+menu[a]) for a in range(6) for b in range(6) if a!=b),Z)/30
            d=sum(menu);assert value==Q(d,3*D)-Q(d*(d-1),30*D*(D+1))>=Q(int(bool(d)),3*D);pair30checks+=1
    frozen=json.loads((H/'frozen_sources_before.json').read_text())
    assert inp['source_manifest_sha256']==digest(H/'frozen_sources_before.json')
    assert all(digest(ROOT/p)==d for p,d in frozen.items())
    out={'status':'PASS','input_sha256':digest(H/'exact_input.json'),'source_review_sha256':digest(H/'source_review.md'),
         'raw_rows':270,'columns':129,'equalities':2,'matrix_entries_rebuilt':270*129,'independent_parameter_entries_rebuilt':540,
         'old72_symbolic_rows_and_order_preserved':True,'old_fixed_rhs_reinstantiated':True,
         'new_pair30_full_menu_states':pair30checks,'c36_literal_states':2048,'c30_literal_states':2048,'c30_envelopes':128,
         'p25':p25counts,'p25_main_family_column_matches':crosschecks,
         'all128_types_including_o0_and_zero_retained':True,'source1_p25_rows':0,
         'frozen_source_files_unchanged':len(frozen),'positive_scaling_verified':True,'imports_builder':False,'optimizer_calls':0}
    save('literal_input_check.json',out);print(json.dumps(out,indent=2));return inp,matrix
def check_certificate(inp,matrix):
    path=H/'exact_certificate.json'
    if not path.exists():return
    cert=json.loads(path.read_text());assert cert['status']=='EXACT_PRIMAL_UNSCALED_DUAL_MATCH' and cert['optimizer_calls']==1
    assert cert['input_sha256']==digest(H/'exact_input.json') and cert['discovery_sha256']==digest(H/'discovery_output.json')
    rows=inp['raw_rows'];lookup={r['name']:i for i,r in enumerate(rows)}
    K=Q(inp['fixed_K']);O=Q(inp['fixed_O']);primal={int(j):Q(v) for j,v in cert['primal'].items()}
    assert all(0<=j<129 and v>=0 for j,v in primal.items())
    x=[primal.get(j,Z) for j in range(129)];assert sum(bits7(j)[0]*x[j] for j in range(128))==K
    assert sum(bits7(j)[6]*x[j] for j in range(128))==O
    slacks={row['name']:sum((a*v for a,v in zip(matrix[i],x)),Z)-Q(row['bK'])*K-Q(row['bO'])*O for i,row in enumerate(rows)}
    assert all(v>=0 for v in slacks.values()) and {n:str(v) for n,v in slacks.items()}==cert['raw_unscaled_row_slacks']
    weights={n:Q(v) for n,v in cert['dual']['original_unscaled_row_weights'].items()};assert set(weights)<=set(lookup) and all(v>0 for v in weights.values())
    piK=Q(cert['dual']['equality_C_size']);piO=Q(cert['dual']['equality_OPT_union'])
    scaled={n:Q(v) for n,v in cert['dual']['scaled_solver_form_weights'].items()}
    assert scaled=={n:v*Q(rows[lookup[n]]['numerical_divisor']) for n,v in weights.items()}
    residual={};homogeneous={}
    for j in range(129):
        paid=sum((v*matrix[lookup[n]][j] for n,v in weights.items()),Z)
        fromscaled=sum((scaled[n]*matrix[lookup[n]][j]/Q(rows[lookup[n]]['numerical_divisor']) for n in weights),Z)
        assert paid==fromscaled
        equality=piK*bits7(j)[0]+piO*bits7(j)[6] if j<128 else Z
        rho=Q(j==128)-paid-equality;assert rho>=0;residual[str(j)]=str(rho)
        homogeneous[str(j)]=str(Q(j==128)-paid-equality-Q(cert['dual']['column_residuals'][str(j)]))
        assert rho*x[j]==0
    assert residual==cert['dual']['column_residuals']
    a=piK+sum((v*Q(rows[lookup[n]]['bK']) for n,v in weights.items()),Z)
    b=piO+sum((v*Q(rows[lookup[n]]['bO']) for n,v in weights.items()),Z)
    line=cert['universal_root_line'];assert Q(line['a'])==a and Q(line['b'])==b
    assert -a==-piK-sum((v*Q(rows[lookup[n]]['bK']) for n,v in weights.items()),Z)
    assert -b==-piO-sum((v*Q(rows[lookup[n]]['bO']) for n,v in weights.items()),Z)
    homogeneous['K']=str(-a+piK+sum((v*Q(rows[lookup[n]]['bK']) for n,v in weights.items()),Z))
    homogeneous['O']=str(-b+piO+sum((v*Q(rows[lookup[n]]['bO']) for n,v in weights.items()),Z))
    assert homogeneous==cert['homogeneous_131_column_identity_residuals'] and all(Q(v)==0 for v in homogeneous.values())
    assert x[128]==Q(cert['objective'])==a*K+b*O
    assert all(v*slacks[n]==0 for n,v in weights.items())
    primitive=line['integer_line'];N=int(primitive['u']);A=int(primitive['K']);B=int(primitive['O'])
    assert N>0 and Q(A,N)==a and Q(B,N)==b and gcd(gcd(N,abs(A)),abs(B))==1
    budget=Q(cert['dual']['common_budget_denominator'])
    assert all((v*budget).denominator==1 for v in list(weights.values())+[piK,piO])
    assert cert['dual']['integer_original_row_weights']=={n:str(v*budget) for n,v in weights.items()}
    assert cert['dual']['integer_equality_multipliers']==[str(piK*budget),str(piO*budget)]
    union=weights.get('BRANCH_UNION_OPT',Z)
    assert line['requires_OPT6']==bool(union) and line['any_six_legal_query_union']==(union==0)
    previous=json.loads((WS/'universal_union_wallet_v6/exact_certificate.json').read_text())
    u6=Q(previous['derived']['u1_u6'][0]);gap=x[128]-u6;cmp=cert['comparison_at_released_K']
    assert Q(cmp['v6_actual_root_u'])==u6 and Q(cmp['root_gap_over_v6_u'])==gap
    assert gap>0
    out={'status':'PASS','input_sha256':digest(H/'exact_input.json'),'certificate_sha256':digest(path),
         'primal_raw_rows_checked':270,'primal_equalities_checked':2,'primal_nonnegative_columns_checked':129,
         'dual_nonnegative_row_weights_checked':270,'dual_nonnegative_residual_columns_checked':129,
         'free_parameter_columns_checked':2,'homogeneous_identity_columns':131,'scaled_unscaled_identities':129,
         'positive_primal_atoms':sum(x[j]>0 for j in range(128)),'positive_budget_weights':len(weights),
         'zero_atom_residuals':sum(Q(residual[str(j)])==0 for j in range(128)),
         'positive_atom_residuals':sum(Q(residual[str(j)])>0 for j in range(128)),
         'objective':str(x[128]),'universal_integer_line':primitive,'root_gap_over_v6_u':str(gap),
         'branch_union_OPT_weight':str(union),'any_six_legal_query_union':union==0,
         'imports_builder':False,'optimizer_calls':0,'not_claimed':['complete SPE','global root sharpness','half coverage']}
    save('literal_certificate_check.json',out);print(json.dumps(out,indent=2))
if __name__=='__main__':check_certificate(*check_input())
