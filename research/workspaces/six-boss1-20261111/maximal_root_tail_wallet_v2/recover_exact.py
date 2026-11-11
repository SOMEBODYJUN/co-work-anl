#!/usr/bin/env python3
"""Exact primal/unscaled-dual recovery; no further optimization."""
from pathlib import Path
from fractions import Fraction as F
from math import lcm,gcd
import json,hashlib
H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(H/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def exact_solve(A,b,n,hint):
    M=[[F(v) for v in row]+[F(rhs)] for row,rhs in zip(A,b)];piv=[];rank=0
    for col in range(n):
        r=next((r for r in range(rank,len(M)) if M[r][col]),None)
        if r is None:continue
        M[rank],M[r]=M[r],M[rank];d=M[rank][col];M[rank]=[x/d for x in M[rank]]
        for k in range(len(M)):
            if k!=rank and M[k][col]:
                d=M[k][col];M[k]=[x-d*y for x,y in zip(M[k],M[rank])]
        piv.append(col);rank+=1
    assert all(any(r[:n]) or r[-1]==0 for r in M)
    free=[c for c in range(n) if c not in piv];x=[F(0)]*n
    for c in free:x[c]=F(str(hint[c])).limit_denominator(1000000)
    for row,c in zip(M,piv):x[c]=row[-1]-sum(row[f]*x[f] for f in free)
    assert all(sum(F(v)*y for v,y in zip(row,x))==F(rhs) for row,rhs in zip(A,b))
    return x,{'rank':rank,'unknowns':n,'free_columns':free,'equations':len(A)}
def main():
    inp=json.loads((H/'exact_input.json').read_text());raw=json.loads((H/'discovery_output.json').read_text())
    assert raw['success'] and raw['optimizer_calls']==1 and raw['input_sha256']==sha(H/'exact_input.json')
    rows=inp['raw_rows'];eq=inp['equalities'];K=F(inp['fixed_K']);O=F(inp['fixed_O'])
    scales=[F(r['numerical_divisor']) for r in rows]
    assert raw['row_numerical_divisors']==[str(v) for v in scales] and all(v>0 for v in scales)
    support=[j for j,x in enumerate(raw['x']) if x>1e-9]
    active=[i for i,slack in enumerate(raw['ineqlin']['residual']) if abs(slack)<1e-8]
    A=[[F(r['a'].get(str(j),'0')) for j in support] for r in eq]+[[F(rows[i]['a'].get(str(j),'0')) for j in support] for i in active]
    b=[F(r['rhs']) for r in eq]+[F(rows[i]['rhs']) for i in active]
    primal,prank=exact_solve(A,b,len(support),[raw['x'][j] for j in support])
    vector={j:v for j,v in zip(support,primal)};assert all(v>=0 for v in vector.values())
    full=[vector.get(j,F(0)) for j in range(129)]
    slacks={r['name']:sum(F(v)*full[int(j)] for j,v in r['a'].items())-F(r['rhs']) for r in rows}
    assert all(v>=0 for v in slacks.values())
    for r in eq:assert sum(F(v)*full[int(j)] for j,v in r['a'].items())==F(r['rhs'])
    dsupport=[i for i,v in enumerate(raw['ineqlin']['marginals']) if -v>1e-9]
    zerocols=[j for j,v in enumerate(raw['lower']['marginals']) if abs(v)<1e-8]
    DA=[[F(rows[i]['a'].get(str(j),'0')) for i in dsupport]+[F(e['a'].get(str(j),'0')) for e in eq] for j in zerocols]
    Db=[F(int(j==128)) for j in zerocols]
    hints=[-raw['ineqlin']['marginals'][i]/float(scales[i]) for i in dsupport]+raw['eqlin']['marginals']
    dual,drank=exact_solve(DA,Db,len(dsupport)+2,hints)
    weights={rows[i]['name']:dual[k] for k,i in enumerate(dsupport)};pi=dual[-2:]
    assert all(w>=0 for w in weights.values())
    byname={r['name']:r for r in rows};residual={}
    for j in range(129):
        v=F(int(j==128))-sum(w*F(byname[n]['a'].get(str(j),'0')) for n,w in weights.items())-sum(p*F(e['a'].get(str(j),'0')) for p,e in zip(pi,eq))
        assert v>=0,(j,v);residual[str(j)]=str(v)
    a=pi[0]+sum(w*F(byname[n]['bK']) for n,w in weights.items())
    b=pi[1]+sum(w*F(byname[n]['bO']) for n,w in weights.items())
    objective=full[128];assert objective==a*K+b*O
    assert all(w*slacks[n]==0 for n,w in weights.items())
    assert all(F(residual[str(j)])*full[j]==0 for j in range(129))
    d=lcm(a.denominator,b.denominator);ai=int(a*d);bi=int(b*d);gg=gcd(gcd(d,abs(ai)),abs(bi));d//=gg;ai//=gg;bi//=gg
    budgetD=lcm(*(v.denominator for v in list(weights.values())+pi))
    previous_a=F(11595684007,112944305160);previous_b=F(2178783435,112944305160)
    previous_value=previous_a*K+previous_b*O;gap=objective-previous_value
    ds=a-previous_a;di=b-previous_b;cross=-di/ds if ds else None
    result={'status':'EXACT_PRIMAL_UNSCALED_DUAL_MATCH','claim':'Universal root line and exact optimum of the specified root72 cone at the released K; not global root sharpness, half or complete SPE.',
            'input_sha256':sha(H/'exact_input.json'),'discovery_sha256':sha(H/'discovery_output.json'),
            'primal':{str(j):str(v) for j,v in vector.items() if v},'objective':str(objective),'objective_decimal':float(objective),
            'raw_unscaled_row_slacks':{n:str(v) for n,v in slacks.items()},
            'dual':{'original_unscaled_row_weights':{n:str(v) for n,v in weights.items() if v},
                    'scaled_solver_form_weights':{n:str(v*F(byname[n]['numerical_divisor'])) for n,v in weights.items() if v},
                    'equality_C_size':str(pi[0]),'equality_OPT_union':str(pi[1]),'column_residuals':residual,
                    'common_budget_denominator':str(budgetD),'integer_original_row_weights':{n:str(v*budgetD) for n,v in weights.items() if v},
                    'integer_equality_multipliers':[str(p*budgetD) for p in pi]},
            'universal_root_line':{'convention':'u >= a*K+b*O','a':str(a),'b':str(b),'integer_line':{'u':str(d),'K':str(ai),'O':str(bi)},
                                   'all128_types_retained':True,'root_u_residual':residual['128']},
            'comparison_previous_root_line':{'previous_value_at_same_K':str(previous_value),'previous_value_decimal':float(previous_value),
                                            'improvement_at_same_K':str(gap),'improvement_decimal':float(gap),
                                            'difference_slope':str(ds),'difference_intercept':str(di),'crossing_K_over_O':str(cross) if cross is not None else None,
                                            'difference_at_K_equals_O':str(ds+di)},
            'recovery':{'primal_support':support,'active_raw_rows':[rows[i]['name'] for i in active],'primal_linear_system':prank,
                        'dual_positive_row_names':[rows[i]['name'] for i in dsupport],'dual_zero_reduced_cost_columns':zerocols,'dual_linear_system':drank,
                        'scaling_unwound_before_exact_solve':True},
            'optimizer_calls':1,'exact_arithmetic_only_after_discovery':True}
    save('exact_certificate.json',result)
    out=['column\tbits_p_y2_y3_y4_y5_z_o\tprimal\tunscaled_dual_residual']
    for atom in inp['atoms']:
        j=atom['index'];out.append(f'{j}\t{"".join(map(str,atom["bits"]))}\t{full[j]}\t{residual[str(j)]}')
    out.append(f'128\tu\t{objective}\t{residual["128"]}')
    (H/'all_129_column_checks.tsv').write_text('\n'.join(out)+'\n')
    print(json.dumps({k:result[k] for k in ['status','objective','objective_decimal','universal_root_line','comparison_previous_root_line']},indent=2))
    print(json.dumps({'weights':result['dual']['original_unscaled_row_weights'],'equalities':[str(p) for p in pi],'primal_rank':prank,'dual_rank':drank},indent=2))
if __name__=='__main__':main()
