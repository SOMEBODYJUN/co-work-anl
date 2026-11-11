#!/usr/bin/env python3
"""Independent literal shares and full Cartesian query averages; stdlib only."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product,combinations_with_replacement
import json,hashlib

H=Path(__file__).resolve().parent;ROOT=H.parent.parents[2];Z=Q(0)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(H/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def pay(member,others):return Q(1,others+1) if member else Z
def bitlist(label,bits):
    if label=='Omean':return [bits[-1],0,0,0,0,0]
    if label=='C':return [bits[0]]
    return [bits[int(label[1:])-1]]
def query_pay(label,bits,others):
    qs=bitlist(label,bits)
    return sum((pay(q,others) for q in qs),Z)/len(qs)
def pair_pay(q,r,bits,others):
    left=bitlist(q,bits);right=bitlist(r,bits)
    # All 36 ordered pairs are explicitly summed when both labels are Omean.
    return sum((pay(l,others)+pay(rr,others+l) for l in left for rr in right),Z)/(len(left)*len(right))
def literal(row,bits):
    l=bits[:6];cnt=sum(l);fam=row['family']
    if fam=='ROOT_IC':return -pay(l[0],cnt-l[0])
    if fam=='CAP':return -Q(l[row['source']-1])
    if fam=='UNION':return -Q(any(l))
    if fam=='FLOOR':return Z
    if fam=='SAFE':
        j=row['source'];return pay(l[j-1],cnt-l[j-1])-query_pay(row['queries'][0],bits,sum(l[:j-1])+6-j)
    background=sum(l[:4]);y,z=l[4:]
    wallet=pay(y,background+z)+pay(z,background+y)+pay(y,background)-pay(y,background+y)
    return wallet-pair_pay(*row['queries'],bits,background)
def expected_rows():
    out=[{'name':'ROOT_IC','family':'ROOT_IC'}]
    for j in range(2,7):out.append({'name':f'CAP_B{j}','family':'CAP','source':j})
    out += [{'name':'BRANCH_UNION_OPT','family':'UNION'},{'name':'ROOT_K_FLOOR','family':'FLOOR'}]
    qs=['C','B2','B3','B4','B5','B6','Omean']
    for j in range(2,7):
        for q in qs:out.append({'name':f'SAFE_j{j}|{q}','family':'SAFE','source':j,'queries':[q]})
    for q,r in combinations_with_replacement(qs,2):out.append({'name':f'PAIR|{q}|{r}','family':'PAIR','queries':[q,r]})
    return out
def payments():
    n_pair=n_safe=n_mean=0
    for b in range(5):
        U=lambda l,r:pay(l,b+r)
        f=lambda l:pay(l,b)
        g=lambda l,r:f(l)-U(l,r)
        for y,z,l,r,j in product((0,1),repeat=5):
            s=U(y,z);w=U(z,y)
            lhs=s+w+g(y,y)-f(l)-f(r)+g(l,r)
            rhs=(s-U(l,j))+(U(j,l)-U(r,l))+(w-U(j,y))+(g(y,y)-g(y,j))
            assert lhs==rhs and g(y,y)-g(y,j)>=0;n_pair+=1
    for j in range(2,7):
        for b in range(j):
            for q in (0,1):
                for tail in product((0,1),repeat=6-j):
                    assert pay(q,b+sum(tail))>=pay(q,b+6-j);n_safe+=1
    for b in range(6):
        for d in range(7):
            members=[int(i<d) for i in range(6)];weak=[int(d>0),0,0,0,0,0]
            assert sum(pay(q,b) for q in members)>=sum(pay(q,b) for q in weak);n_mean+=1
            for l in (0,1):
                assert sum(pay(l,b)+pay(r,b+l) for r in members)>=sum(pay(l,b)+pay(r,b+l) for r in weak);n_mean+=1
            strong=sum(pay(l,b)+pay(r,b+l) for l in members for r in members)/36
            low=sum(pay(l,b)+pay(r,b+l) for l in weak for r in weak)/36
            assert strong>=low
            o=int(d>0);assert low==Q(o,3*(b+1))-Q(o,36*(b+1)*(b+2));n_mean+=1
    return {'PAIR_three_IC':n_pair,'SAFE_actual_future_patterns':n_safe,'union_mean_weakening':n_mean}
def check_input():
    inp=json.loads((H/'exact_input.json').read_text())
    atoms=[{'index':i,'bits':list(bits)} for i,bits in enumerate(product((0,1),repeat=7))]
    assert inp['atoms']==atoms and inp['root_u_column']==128 and inp['nonnegative_columns']==list(range(129))
    assert inp['objective']=={'128':'1'} and inp['convention']=='A*x >= bK*K+bO*O'
    K=Q(24376964954228547006,142891298915142483961);assert Q(inp['fixed_K'])==K and Q(inp['fixed_O'])==1
    expected=expected_rows();rows=inp['raw_rows'];assert len(rows)==len(expected)==71
    entries=0;zero_rows=[];keys=[]
    for row,desc in zip(rows,expected):
        assert {k:row[k] for k in desc}==desc
        coeffs={}
        for atom in atoms:
            val=literal(row,atom['bits']);entries+=1
            if val:coeffs[str(atom['index'])]=str(val)
        ucoef=int(row['family'] in ('ROOT_IC','FLOOR'));entries+=1
        if ucoef:coeffs['128']=str(ucoef)
        assert row['a']==coeffs,row['name']
        bK=-Q(1) if row['family']=='CAP' else (Q(1,6) if row['family']=='FLOOR' else Z)
        bO=-Q(1) if row['family']=='UNION' else Z
        assert Q(row['bK'])==bK and Q(row['bO'])==bO and Q(row['rhs'])==bK*K+bO
        if not coeffs and bK==bO==0:zero_rows.append(row['name'])
        keys.append((tuple(sorted(coeffs.items())),str(bK),str(bO)))
    assert inp['equalities']==[
        {'name':'C_size','a':{str(a['index']):'1' for a in atoms if a['bits'][0]},'rhs':str(K),'parameter':'K'},
        {'name':'OPT_union','a':{str(a['index']):'1' for a in atoms if a['bits'][6]},'rhs':'1','parameter':'O'}]
    before=json.loads((H/'frozen_sources_before.json').read_text())
    assert all(sha(ROOT/p)==h for p,h in before.items())
    out={'status':'PASS','input_sha256':sha(H/'exact_input.json'),'columns':129,'all_boolean_types':128,'raw_rows':71,
         'all_matrix_entries_compared':entries,'equalities':2,'zero_rows_retained':zero_rows,
         'affine_duplicate_rows_retained':len(keys)-len(set(keys)),'proof_checks':payments(),
         'frozen_source_files_unchanged':len(before),'imports_builder':False,'uses_optimizer':False}
    save('literal_input_check.json',out);print(json.dumps(out,indent=2));return inp
def check_certificate(inp):
    p=H/'exact_certificate.json'
    if not p.exists():return
    cert=json.loads(p.read_text());assert cert['input_sha256']==sha(H/'exact_input.json')
    assert cert['discovery_sha256']==sha(H/'discovery_output.json')
    assert cert['status']=='EXACT_PRIMAL_DUAL_MATCH' and cert['optimizer_calls']==1
    point={int(k):Q(v) for k,v in cert['primal'].items()}
    assert all(0<=j<129 and v>=0 for j,v in point.items())
    atoms=inp['atoms'];K=Q(inp['fixed_K']);O=Q(inp['fixed_O']);u=point.get(128,Z)
    assert sum((Q(a['bits'][0])*point.get(a['index'],Z) for a in atoms),Z)==K
    assert sum((Q(a['bits'][6])*point.get(a['index'],Z) for a in atoms),Z)==O
    rows={r['name']:r for r in inp['raw_rows']}
    slacks={}
    for name,row in rows.items():
        lhs=sum((literal(row,a['bits'])*point.get(a['index'],Z) for a in atoms),Z)
        if row['family'] in ('ROOT_IC','FLOOR'):lhs+=u
        slack=lhs-Q(row['bK'])*K-Q(row['bO'])*O
        assert slack>=0,(name,slack);slacks[name]=str(slack)
    assert slacks==cert['raw_row_slacks']
    weights={name:Q(v) for name,v in cert['dual']['row_weights'].items()}
    assert set(weights)<=set(rows) and all(v>=0 for v in weights.values())
    piK=Q(cert['dual']['equality_C_size']);piO=Q(cert['dual']['equality_OPT_union'])
    residuals={}
    for atom in atoms:
        coeff=-sum((weight*literal(rows[name],atom['bits']) for name,weight in weights.items()),Z)
        coeff-=piK*atom['bits'][0]+piO*atom['bits'][6]
        assert coeff>=0,(atom,coeff);residuals[str(atom['index'])]=str(coeff)
    ures=1-sum(weight for name,weight in weights.items() if rows[name]['family'] in ('ROOT_IC','FLOOR'))
    assert ures>=0;residuals['128']=str(ures)
    assert residuals==cert['dual']['column_residuals']
    a=piK+sum((weight*Q(rows[name]['bK']) for name,weight in weights.items()),Z)
    b=piO+sum((weight*Q(rows[name]['bO']) for name,weight in weights.items()),Z)
    line=cert['universal_root_line'];assert a==Q(line['a']) and b==Q(line['b'])
    integer=line['integer_line'];D=Q(integer['u']);A=Q(integer['K']);B=Q(integer['O'])
    assert D>0 and A==D*a and B==D*b
    # Check the two parameter columns of the homogeneous identity as well.
    assert -a==-sum((weight*Q(rows[name]['bK']) for name,weight in weights.items()),Z)-piK
    assert -b==-sum((weight*Q(rows[name]['bO']) for name,weight in weights.items()),Z)-piO
    assert u==a*K+b*O==Q(cert['objective'])
    for name,weight in weights.items():assert weight*Q(slacks[name])==0
    for j in range(129):assert point.get(j,Z)*Q(residuals[str(j)])==0
    assert line['all_128_types_retained'] and Q(line['root_u_residual'])==ures
    budgetD=Q(cert['dual']['common_budget_denominator']);assert budgetD>0
    assert cert['dual']['integer_row_weights']=={name:str(weight*budgetD) for name,weight in weights.items()}
    assert cert['dual']['integer_equality_multipliers']==[str(piK*budgetD),str(piO*budgetD)]
    other=(1658*K+87*O)/10980;diff=u-other;comparison=cert['comparison_Main_NEW']
    assert other==Q(comparison['value_at_K0']) and diff==Q(comparison['improvement_at_K0']) and diff>0
    slope=a-Q(1658,10980);intercept=b-Q(87,10980)
    assert slope==Q(comparison['new_minus_Main_slope']) and intercept==Q(comparison['new_minus_Main_intercept'])
    assert slope<0<intercept and -intercept/slope==Q(comparison['crossing_K_over_O'])
    # All 128 types, including o=0 and the all-zero atom, remain in the residual table.
    assert set(residuals)==set(map(str,range(129)))
    assert weights.get('BRANCH_UNION_OPT',Z)==0 and weights.get('ROOT_K_FLOOR',Z)==0
    frozen=json.loads((H/'frozen_sources_before.json').read_text())
    assert all(sha(ROOT/path)==h for path,h in frozen.items())
    out={'status':'PASS','claim':'Exact matching primal and universal dual of the specified necessary root-C cone at K0; not a complete SPE or a globally optimal root bound.',
         'input_sha256':sha(H/'exact_input.json'),'certificate_sha256':sha(p),'columns_checked':129,'parameter_columns_checked':2,
         'all_128_boolean_types_retained':True,'primal_positive_atoms':sum(j<128 for j,v in point.items() if v>0),
         'raw_primal_rows_checked':71,'positive_dual_rows':sum(v>0 for v in weights.values()),
         'dual_zero_atom_residuals':sum(Q(residuals[str(j)])==0 for j in range(128)),
         'dual_positive_atom_residuals':sum(Q(residuals[str(j)])>0 for j in range(128)),
         'root_u_residual':str(ures),'free_equality_multipliers':[str(piK),str(piO)],
         'objective':str(u),'universal_root_line':integer,'improvement_over_Main_NEW':str(diff),
         'union_cap_weight':'0','floor_weight':'0','frozen_source_files_unchanged':len(frozen),
         'uses_optimizer':False,'imports_builder':False}
    save('literal_certificate_check.json',out);print(json.dumps(out,indent=2))

if __name__=='__main__':check_certificate(check_input())
