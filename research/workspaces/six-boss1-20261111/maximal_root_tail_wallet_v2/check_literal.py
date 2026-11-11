#!/usr/bin/env python3
"""Independent original71 shares + all2048 literal requery-cut reconstruction."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product,combinations_with_replacement
import json,hashlib
H=Path(__file__).resolve().parent;WS=H.parent;ROOT=WS.parents[2];ZERO=Q(0)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(H/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def pay(bit,others):return Q(1,others+1) if bit else ZERO
def members(label,bits):
    if label=='Omean':return [bits[6],0,0,0,0,0]
    return [bits[0 if label=='C' else int(label[1:])-1]]
def query_mean(label,bits,others):
    ls=members(label,bits);return sum((pay(q,others) for q in ls),ZERO)/len(ls)
def pair_mean(left,right,bits,others):
    ls=members(left,bits);rs=members(right,bits)
    return sum((pay(l,others)+pay(r,others+l) for l in ls for r in rs),ZERO)/(len(ls)*len(rs))
def old_literal(row,bits):
    l=bits[:6];count=sum(l);family=row['family']
    if family=='ROOT_IC':return -pay(l[0],count-l[0])
    if family=='CAP':return -Q(l[row['source']-1])
    if family=='UNION':return -Q(any(l))
    if family=='FLOOR':return ZERO
    if family=='SAFE':
        j=row['source'];return pay(l[j-1],count-l[j-1])-query_mean(row['queries'][0],bits,sum(l[:j-1])+6-j)
    bg=sum(l[:4]);y,z=l[4:]
    wallet=pay(y,bg+z)+pay(z,bg+y)+pay(y,bg)-pay(y,bg+y)
    return wallet-pair_mean(*row['queries'],bits,bg)
def old_descriptors():
    rows=[{'name':'ROOT_IC','family':'ROOT_IC'}]
    rows += [{'name':f'CAP_B{j}','family':'CAP','source':j} for j in range(2,7)]
    rows += [{'name':'BRANCH_UNION_OPT','family':'UNION'},{'name':'ROOT_K_FLOOR','family':'FLOOR'}]
    queries=['C','B2','B3','B4','B5','B6','Omean']
    rows += [{'name':f'SAFE_j{j}|{q}','family':'SAFE','source':j,'queries':[q]} for j in range(2,7) for q in queries]
    rows += [{'name':f'PAIR|{q}|{r}','family':'PAIR','queries':[q,r]} for q,r in combinations_with_replacement(queries,2)]
    return rows
def requery_literal(bits,q,tail):
    p,y2,y3,y4,y5,z,o=bits;r,y,t=tail;b=p+y2;bg=b+q+r
    mean=[o,0,0,0,0,0]
    source=126000*pay(q,b+sum(tail))
    old4=sum(w*pay(s,b+y3+2) for w,s in zip((43,31218,34458),tail))
    old6=1654*sum(pay(s,b+y3+y4+y5) for s in tail)
    terminal=5400*(sum(pay(v,bg+y) for v in mean)/6-pay(t,bg+y))
    wallet=pay(y,bg+t)+pay(t,bg+y)+pay(y,bg)-pay(y,bg+y)
    query=sum(pay(l,bg)+pay(rr,bg+l) for l in mean for rr in mean)/36
    return source+old4+old6+terminal+7740*(query-wallet)
def rebuild_cut(atoms):
    source=json.loads((WS/'maximal_root_opt_requery/exact_certificate.json').read_text())
    env=json.loads((WS/'maximal_root_opt_requery/universal_moment_envelope.json').read_text())
    cut={};states=0
    for atom in atoms:
        bits=atom['bits'];allvals=[[requery_literal(bits,q,s) for s in product((0,1),repeat=3)] for q in (0,1)]
        states+=16;a0=min(allvals[0]);a1=min(allvals[1]);o=bits[6]
        m=a0 if not o else min((5*a0+a1)/6,a1)
        e=env[atom['index']];assert a0==Q(e['a0']) and a1==Q(e['a1']) and m==Q(e['minimum'])
        assert all(v-min(allvals[q])>=0 for q in (0,1) for v in allvals[q])
        l=bits[:6];count=sum(l)
        v=lambda j:pay(l[j-1],count-l[j-1])
        cut[str(atom['index'])]=str(126000*v(3)+65719*v(4)+4962*v(6)-m)
    assert cut==source['universal_cut']['cut_z'] and Q(source['universal_cut']['cut_K'])==Q(source['universal_cut']['cut_u'])==0
    return cut,states
def check_input():
    inp=json.loads((H/'exact_input.json').read_text());oldpath=WS/'maximal_root_tail_wallet/exact_input.json'
    cutpath=WS/'maximal_root_opt_requery/exact_certificate.json'
    assert sha(oldpath)==inp['old_input_sha256']=='3c1a824ed0a17562da812db1d0bb12485f0b1c7f743577af7bc2ecf316d3ab65'
    assert sha(cutpath)==inp['cut_certificate_sha256']=='209959db4dfce6ba4fe796eeb168b8ab71f186f795e0599f9148d08ceaa8b13e'
    old=json.loads(oldpath.read_text());atoms=[{'index':i,'bits':list(bits)} for i,bits in enumerate(product((0,1),repeat=7))]
    assert inp['atoms']==old['atoms']==atoms and inp['nonnegative_columns']==list(range(129)) and inp['root_u_column']==128
    assert inp['objective']=={'128':'1'} and inp['convention']=='A*x >= bK*K+bO*O'
    K=Q(1125421575458286230366665,6570307807568935468436467);assert Q(inp['fixed_K'])==K and Q(inp['fixed_O'])==1
    rows=inp['raw_rows'];descs=old_descriptors();assert len(rows)==72 and len(descs)==71
    checked=0
    for row,desc,oldrow in zip(rows[:71],descs,old['raw_rows']):
        assert {k:row[k] for k in desc}==desc
        a={str(h['index']):str(old_literal(row,h['bits'])) for h in atoms if old_literal(row,h['bits'])}
        if row['family'] in ('ROOT_IC','FLOOR'):a['128']='1'
        assert a==row['a']==oldrow['a']
        bK=-Q(1) if row['family']=='CAP' else (Q(1,6) if row['family']=='FLOOR' else ZERO)
        bO=-Q(1) if row['family']=='UNION' else ZERO
        assert Q(row['bK'])==Q(oldrow['bK'])==bK and Q(row['bO'])==Q(oldrow['bO'])==bO
        assert Q(row['rhs'])==bK*K+bO and row['numerical_divisor']=='1';checked+=129
    cut,states=rebuild_cut(atoms);new=rows[-1]
    assert new['name']=='OPT_SOURCE3_REQUERY_CUT' and new['family']=='REQUERY_CUT'
    assert new['a']=={h:v for h,v in cut.items() if Q(v)}
    assert Q(new['source_cut_u'])==Q(new['source_cut_K'])==Q(new['bK'])==Q(new['bO'])==Q(new['rhs'])==0
    assert new['numerical_divisor']=='126000' and Q(new['numerical_divisor'])>0
    checked+=129
    expected_eq=[{'name':'C_size','a':{str(h['index']):'1' for h in atoms if h['bits'][0]},'rhs':str(K),'parameter':'K'},
                 {'name':'OPT_union','a':{str(h['index']):'1' for h in atoms if h['bits'][6]},'rhs':'1','parameter':'O'}]
    assert inp['equalities']==expected_eq
    mapping=json.loads((H/'column_mapping.json').read_text())
    assert mapping['actual256_map_informational_only']==[{'global_index':4*a+2*x+o,'root128_index':2*a+o} for a in range(64) for x in (0,1) for o in (0,1)]
    assert not mapping['actual_joint_rows_added_here']
    frozen=json.loads((H/'frozen_sources_before.json').read_text());assert all(sha(ROOT/p)==h for p,h in frozen.items())
    out={'status':'PASS','input_sha256':sha(H/'exact_input.json'),'columns':129,'raw_rows':72,'equalities':2,
         'unscaled_matrix_entries_compared':checked,'unchanged_original_raw_rows':71,'new_cut_rows':1,
         'all128_cut_envelopes_rebuilt':128,'all2048_requery_states_rebuilt':states,
         'new_cut_numerical_divisor':'126000','exact_rows_remain_unscaled':True,'fixed_K':str(K),
         'frozen_old_source_files_unchanged':len(frozen),'uses_optimizer':False,'imports_builder':False}
    save('literal_input_check.json',out);print(json.dumps(out,indent=2));return inp,cut
def check_certificate(inp,cut):
    path=H/'exact_certificate.json'
    if not path.exists():return
    cert=json.loads(path.read_text());assert cert['status']=='EXACT_PRIMAL_UNSCALED_DUAL_MATCH' and cert['optimizer_calls']==1
    assert cert['input_sha256']==sha(H/'exact_input.json') and cert['discovery_sha256']==sha(H/'discovery_output.json')
    atoms=inp['atoms'];rows={r['name']:r for r in inp['raw_rows']};K=Q(inp['fixed_K']);O=Q(inp['fixed_O'])
    def coefficient(row,j):
        if j==128:return Q(int(row['family'] in ('ROOT_IC','FLOOR')))
        if row['family']=='REQUERY_CUT':return Q(cut[str(j)])
        return old_literal(row,atoms[j]['bits'])
    point={int(k):Q(v) for k,v in cert['primal'].items()};assert all(0<=j<129 and v>=0 for j,v in point.items())
    u=point.get(128,ZERO)
    assert sum((a['bits'][0]*point.get(a['index'],ZERO) for a in atoms),ZERO)==K
    assert sum((a['bits'][6]*point.get(a['index'],ZERO) for a in atoms),ZERO)==O
    slacks={}
    for n,row in rows.items():
        value=sum((coefficient(row,j)*point.get(j,ZERO) for j in range(129)),ZERO)-Q(row['bK'])*K-Q(row['bO'])*O
        assert value>=0,(n,value);slacks[n]=str(value)
    assert slacks==cert['raw_unscaled_row_slacks']
    weights={n:Q(v) for n,v in cert['dual']['original_unscaled_row_weights'].items()};assert set(weights)<=set(rows) and all(v>=0 for v in weights.values())
    scaled={n:Q(v) for n,v in cert['dual']['scaled_solver_form_weights'].items()}
    assert scaled=={n:v*Q(rows[n]['numerical_divisor']) for n,v in weights.items()}
    piK=Q(cert['dual']['equality_C_size']);piO=Q(cert['dual']['equality_OPT_union'])
    residual={}
    for j in range(129):
        paid=sum((w*coefficient(rows[n],j) for n,w in weights.items()),ZERO)
        scaled_paid=sum((scaled[n]*coefficient(rows[n],j)/Q(rows[n]['numerical_divisor']) for n in scaled),ZERO)
        assert paid==scaled_paid
        equality=piK*atoms[j]['bits'][0]+piO*atoms[j]['bits'][6] if j<128 else ZERO
        h=Q(int(j==128))-paid-equality;assert h>=0,(j,h);residual[str(j)]=str(h)
    assert residual==cert['dual']['column_residuals']
    a=piK+sum((w*Q(rows[n]['bK']) for n,w in weights.items()),ZERO)
    b=piO+sum((w*Q(rows[n]['bO']) for n,w in weights.items()),ZERO)
    line=cert['universal_root_line'];assert a==Q(line['a']) and b==Q(line['b'])
    integer=line['integer_line'];N=Q(integer['u']);A=Q(integer['K']);B=Q(integer['O'])
    assert N>0 and N*a==A and N*b==B
    assert -a==-piK-sum((w*Q(rows[n]['bK']) for n,w in weights.items()),ZERO)
    assert -b==-piO-sum((w*Q(rows[n]['bO']) for n,w in weights.items()),ZERO)
    assert u==a*K+b*O==Q(cert['objective'])
    for n,w in weights.items():assert w*Q(slacks[n])==0
    for j in range(129):assert point.get(j,ZERO)*Q(residual[str(j)])==0
    D=Q(cert['dual']['common_budget_denominator']);assert D==2*N
    assert cert['dual']['integer_original_row_weights']=={n:str(w*D) for n,w in weights.items()}
    assert cert['dual']['integer_equality_multipliers']==[str(piK*D),str(piO*D)]
    assert line['all128_types_retained'] and Q(line['root_u_residual'])==0
    priora=Q(11595684007,112944305160);priorb=Q(2178783435,112944305160)
    cmp=cert['comparison_previous_root_line'];prior=priora*K+priorb*O;gap=u-prior
    assert prior==Q(cmp['previous_value_at_same_K']) and gap==Q(cmp['improvement_at_same_K'])>0
    ds=a-priora;di=b-priorb
    assert ds==Q(cmp['difference_slope'])<0 and di==Q(cmp['difference_intercept'])>0
    assert -di/ds==Q(cmp['crossing_K_over_O'])>1 and ds+di==Q(cmp['difference_at_K_equals_O'])>0
    assert weights.get('BRANCH_UNION_OPT',ZERO)==weights.get('ROOT_K_FLOOR',ZERO)==0
    assert weights['OPT_SOURCE3_REQUERY_CUT']==Q(2312374,6366254820863)
    frozen=json.loads((H/'frozen_sources_before.json').read_text());assert all(sha(ROOT/p)==h for p,h in frozen.items())
    out={'status':'PASS','claim':'Exact root72 primal/unscaled-dual match at the specified K and universal affine root line; not complete SPE or global root sharpness.',
         'input_sha256':sha(H/'exact_input.json'),'certificate_sha256':sha(path),'primal_raw_rows_checked':72,'dual_columns_checked':129,
         'parameter_columns_checked':2,'all128_types_retained':True,'positive_primal_atoms':sum(j<128 and v>0 for j,v in point.items()),
         'positive_unscaled_budget_weights':sum(w>0 for w in weights.values()),
         'zero_atom_residuals':sum(Q(residual[str(j)])==0 for j in range(128)),
         'positive_atom_residuals':sum(Q(residual[str(j)])>0 for j in range(128)),
         'root_u_residual':residual['128'],'scaled_vs_unscaled_dual_column_identities':129,
         'appended_cut_positive_divisor':'126000','appended_cut_original_weight':str(weights['OPT_SOURCE3_REQUERY_CUT']),
         'integer_budget_scale_over_primitive_line':'2','objective':str(u),'universal_integer_line':integer,
         'improvement_at_same_K':str(gap),'strictly_dominates_prior_root_line_on_0_le_K_le_O':True,
         'union_cap_weight':'0','floor_weight':'0','frozen_old_source_files_unchanged':len(frozen),'uses_optimizer':False,'imports_builder':False}
    save('literal_certificate_check.json',out);print(json.dumps(out,indent=2))
if __name__=='__main__':check_certificate(*check_input())
