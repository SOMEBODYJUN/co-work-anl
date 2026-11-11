#!/usr/bin/env python3
"""Exact rational linear algebra only after the one authorized discovery call."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from math import lcm,gcd
import json
H=Path(__file__).resolve().parent;WS=H.parent;Z=F(0)
def digest(p):return sha256(p.read_bytes()).hexdigest()
def save(n,o):(H/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def solve_unique(A,b,n):
    matrix=[[F(v) for v in r]+[F(v)] for r,v in zip(A,b)];rank=0;piv=[]
    for col in range(n):
        pivot=next((r for r in range(rank,len(matrix)) if matrix[r][col]),None)
        if pivot is None:continue
        matrix[rank],matrix[pivot]=matrix[pivot],matrix[rank]
        d=matrix[rank][col];matrix[rank]=[v/d for v in matrix[rank]]
        for r in range(len(matrix)):
            if r!=rank and matrix[r][col]:
                d=matrix[r][col];matrix[r]=[v-d*w for v,w in zip(matrix[r],matrix[rank])]
        piv.append(col);rank+=1
    assert all(any(r[:n]) or r[-1]==0 for r in matrix),'Inconsistent exact support equations.'
    assert rank==n,('Exact support not uniquely determined; no optimizer retry.',rank,n)
    x=[Z]*n
    for r,col in zip(matrix,piv):x[col]=r[-1]
    assert all(sum((F(v)*w for v,w in zip(r,x)),Z)==F(rhs) for r,rhs in zip(A,b))
    return x,{'rank':rank,'unknowns':n,'equations':len(A),'free_columns':[]}
def main():
    inp=json.loads((H/'exact_input.json').read_text());raw=json.loads((H/'discovery_output.json').read_text())
    assert raw['success'] and raw['optimizer_calls']==1 and raw['input_sha256']==digest(H/'exact_input.json')
    rows=inp['raw_rows'];eq=inp['equalities'];K=F(inp['fixed_K']);O=F(inp['fixed_O']);scales=[F(r['numerical_divisor']) for r in rows]
    assert raw['row_numerical_divisors']==[str(s) for s in scales] and all(s>0 for s in scales)
    support=[j for j,v in enumerate(raw['x']) if v>1e-9]
    active=[i for i,v in enumerate(raw['ineqlin']['residual']) if abs(v)<1e-8]
    M=[[F(e['a'].get(str(j),'0')) for j in support] for e in eq]
    rhs=[F(e['rhs']) for e in eq]
    M += [[F(rows[i]['a'].get(str(j),'0')) for j in support] for i in active]
    rhs += [F(rows[i]['rhs']) for i in active]
    pv,prank=solve_unique(M,rhs,len(support));x=[Z]*129
    for j,v in zip(support,pv):x[j]=v
    assert all(v>=0 for v in x)
    slacks={r['name']:sum((F(v)*x[int(j)] for j,v in r['a'].items()),Z)-F(r['rhs']) for r in rows}
    assert all(v>=0 for v in slacks.values())
    for e in eq:assert sum((F(v)*x[int(j)] for j,v in e['a'].items()),Z)==F(e['rhs'])
    dsupport=[i for i,v in enumerate(raw['ineqlin']['marginals']) if -v>1e-9]
    zerocols=[j for j,v in enumerate(raw['lower']['marginals']) if abs(v)<1e-8]
    # Form equations with the ORIGINAL rows: numerical scaled weights are not used as original weights.
    D=[[F(rows[i]['a'].get(str(j),'0')) for i in dsupport]+[F(e['a'].get(str(j),'0')) for e in eq] for j in zerocols]
    drhs=[F(j==128) for j in zerocols]
    dv,drank=solve_unique(D,drhs,len(dsupport)+2)
    weights={rows[i]['name']:dv[k] for k,i in enumerate(dsupport) if dv[k]};pi=dv[-2:]
    assert all(v>0 for v in weights.values());lookup={r['name']:r for r in rows};residual={}
    for j in range(129):
        rho=F(j==128)-sum((w*F(lookup[n]['a'].get(str(j),'0')) for n,w in weights.items()),Z)-sum((p*F(e['a'].get(str(j),'0')) for p,e in zip(pi,eq)),Z)
        assert rho>=0,(j,rho);residual[str(j)]=str(rho);assert rho*x[j]==0
    a=pi[0]+sum((w*F(lookup[n]['bK']) for n,w in weights.items()),Z)
    b=pi[1]+sum((w*F(lookup[n]['bO']) for n,w in weights.items()),Z)
    assert x[128]==a*K+b*O and all(w*slacks[n]==0 for n,w in weights.items())
    denominator=lcm(a.denominator,b.denominator);ai=int(a*denominator);bi=int(b*denominator)
    g=gcd(gcd(denominator,abs(ai)),abs(bi));denominator//=g;ai//=g;bi//=g
    budget=lcm(*(v.denominator for v in list(weights.values())+pi));pointden=lcm(*(v.denominator for v in x))
    union=weights.get('BRANCH_UNION_OPT',Z);floor=weights.get('ROOT_K_FLOOR',Z)
    v6path=WS/'universal_union_wallet_v6/exact_certificate.json';v6=json.loads(v6path.read_text());u6=F(v6['derived']['u1_u6'][0]);gap=x[128]-u6
    assert F(v6['K'])==K and gap>0
    old=json.loads((WS/'maximal_root_tail_wallet_v2/exact_certificate.json').read_text())
    old_a=F(old['universal_root_line']['a']);old_b=F(old['universal_root_line']['b'])
    m30=json.loads((WS/'main_thirty_index_strengthening/exact_certificate.json').read_text())
    r30a=F(m30['root_old_a']);r30b=F(m30['root_new_b'])
    globalinp=json.loads((WS/'universal_union_wallet_v6/exact_input.json').read_text())
    feedback=next(r for r in globalinp['raw_rows'] if r['name']=='ROOT30_B2_CAPACITY_FEEDBACK')
    b2a=-F(feedback['a']['256']);b2b=-F(feedback['a']['1']);assert u6==b2a*K+b2b*O
    homog={str(j):'0' for j in range(129)}
    homog['K']=str(-a+pi[0]+sum((w*F(lookup[n]['bK']) for n,w in weights.items()),Z))
    homog['O']=str(-b+pi[1]+sum((w*F(lookup[n]['bO']) for n,w in weights.items()),Z))
    assert all(F(v)==0 for v in homog.values())
    result={'status':'EXACT_PRIMAL_UNSCALED_DUAL_MATCH',
            'claim':'Universal affine root lower bound and exact optimum only of this specified 270-row necessary cone at the released K. No complete SPE, global root sharpness or half claim.',
            'input_sha256':digest(H/'exact_input.json'),'discovery_sha256':digest(H/'discovery_output.json'),
            'primal':{str(j):str(v) for j,v in enumerate(x) if v},'objective':str(x[128]),'objective_decimal':float(x[128]),
            'primal_common_denominator':str(pointden),'integer_primal':{str(j):str(v*pointden) for j,v in enumerate(x) if v},
            'raw_unscaled_row_slacks':{n:str(v) for n,v in slacks.items()},
            'dual':{'original_unscaled_row_weights':{n:str(v) for n,v in weights.items()},
                    'scaled_solver_form_weights':{n:str(v*F(lookup[n]['numerical_divisor'])) for n,v in weights.items()},
                    'equality_C_size':str(pi[0]),'equality_OPT_union':str(pi[1]),'column_residuals':residual,
                    'common_budget_denominator':str(budget),'integer_original_row_weights':{n:str(v*budget) for n,v in weights.items()},
                    'integer_equality_multipliers':[str(p*budget) for p in pi],
                    'K_parameter_contributions':{n:str(v*F(lookup[n]['bK'])) for n,v in weights.items() if F(lookup[n]['bK'])},
                    'O_parameter_contributions':{n:str(v*F(lookup[n]['bO'])) for n,v in weights.items() if F(lookup[n]['bO'])}},
            'universal_root_line':{'convention':'u >= a*K+b*O','a':str(a),'b':str(b),
                                   'integer_line':{'u':str(denominator),'K':str(ai),'O':str(bi)},
                                   'all128_types_retained':True,'root_u_residual':residual['128'],
                                   'requires_OPT6':bool(union),'any_six_legal_query_union':union==0},
            'homogeneous_131_column_identity_residuals':homog,
            'comparison_at_released_K':{'v6_certificate_sha256':digest(v6path),'fixed_K':str(K),'fixed_O':str(O),
                                       'v6_actual_root_u':str(u6),'v6_actual_root_u_decimal':float(u6),
                                       'root_gap_over_v6_u':str(gap),'root_gap_over_v6_u_decimal':float(gap),
                                       'ROOT30_B2_a':str(b2a),'ROOT30_B2_b':str(b2b),'v6_u_attains_ROOT30_B2':True,
                                       'prior_v2_line_value':str(old_a*K+old_b*O),'ROOT30_value':str(r30a*K+r30b*O),
                                       'new_minus_ROOT30_B2_slope':str(a-b2a),'new_minus_ROOT30_B2_intercept':str(b-b2b)},
            'recovery':{'primal_support':support,'active_raw_rows':[rows[i]['name'] for i in active],'primal_linear_system':prank,
                        'dual_positive_row_names':[rows[i]['name'] for i in dsupport],'dual_zero_reduced_cost_columns':zerocols,
                        'dual_linear_system':drank,'original_unscaled_rows_used':True,'parameter_coefficients_recovered_separately':True},
            'branch_union_OPT_weight':str(union),'root_K_floor_weight':str(floor),
            'optimizer_calls':1,'exact_arithmetic_only_after_discovery':True}
    save('exact_certificate.json',result)
    lines=['column\tbits_C_B2_B3_B4_B5_B6_o\tprimal\tunscaled_dual_residual']
    for atom in inp['atoms']:
        j=atom['index'];lines.append(f'{j}\t{"".join(map(str,atom["bits"]))}\t{x[j]}\t{residual[str(j)]}')
    lines.append(f'128\tu\t{x[128]}\t{residual["128"]}');(H/'all_129_column_checks.tsv').write_text('\n'.join(lines)+'\n')
    print(json.dumps({k:result[k] for k in ['status','objective','objective_decimal','universal_root_line','comparison_at_released_K']},indent=2))
    print(json.dumps({'weights':result['dual']['original_unscaled_row_weights'],'pi':[str(p) for p in pi],
                      'primal_rank':prank,'dual_rank':drank,'certificate_sha256':digest(H/'exact_certificate.json')},indent=2))
if __name__=='__main__':main()
