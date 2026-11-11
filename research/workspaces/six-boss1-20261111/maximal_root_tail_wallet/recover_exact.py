#!/usr/bin/env python3
"""Exact support/basis reconstruction only; no optimization call."""
from pathlib import Path
from fractions import Fraction as F
from math import lcm,gcd
import json,hashlib

H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(H/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def solve_exact(A,b,n,free_hint=None):
    M=[[F(v) for v in row]+[F(rhs)] for row,rhs in zip(A,b)]
    piv=[];r=0
    for c in range(n):
        pivot=next((j for j in range(r,len(M)) if M[j][c]),None)
        if pivot is None:continue
        M[r],M[pivot]=M[pivot],M[r]
        scale=M[r][c];M[r]=[v/scale for v in M[r]]
        for j in range(len(M)):
            if j!=r and M[j][c]:
                t=M[j][c];M[j]=[v-t*w for v,w in zip(M[j],M[r])]
        piv.append(c);r+=1
        if r==len(M):break
    assert all(any(row[:n]) or row[n]==0 for row in M),'Inconsistent exact system'
    free=[c for c in range(n) if c not in piv]
    x=[F(0) for _ in range(n)]
    if free_hint is not None:
        for c in free:x[c]=F(str(free_hint[c])).limit_denominator(1000000)
    for row,c in zip(M,piv):x[c]=row[n]-sum(row[j]*x[j] for j in free)
    assert all(sum(F(v)*xx for v,xx in zip(row,x))==F(rhs) for row,rhs in zip(A,b))
    return x,{'rank':len(piv),'unknowns':n,'free_columns':free,'equations':len(M)}
def main():
    inp=json.loads((H/'exact_input.json').read_text());raw=json.loads((H/'discovery_output.json').read_text())
    assert raw['success'] and raw['optimizer_calls']==1 and raw['input_sha256']==sha(H/'exact_input.json')
    rows=inp['raw_rows'];eq=inp['equalities'];K=F(inp['fixed_K']);O=F(inp['fixed_O'])
    support=[j for j,x in enumerate(raw['x']) if x>1e-9]
    active=[r for r,res in enumerate(raw['ineqlin']['residual']) if abs(res)<1e-8]
    P_A=[[F(r['a'].get(str(j),'0')) for j in support] for r in eq]
    P_b=[F(r['rhs']) for r in eq]
    P_A += [[F(rows[r]['a'].get(str(j),'0')) for j in support] for r in active]
    P_b += [F(rows[r]['rhs']) for r in active]
    values,prank=solve_exact(P_A,P_b,len(support),[raw['x'][j] for j in support])
    primal={j:v for j,v in zip(support,values)};assert all(v>=0 for v in primal.values())
    full=[primal.get(j,F(0)) for j in range(129)]
    slacks={r['name']:sum(F(r['a'].get(str(j),'0'))*full[j] for j in range(129))-F(r['rhs']) for r in rows}
    assert all(v>=0 for v in slacks.values())
    for r in eq:assert sum(F(v)*full[int(k)] for k,v in r['a'].items())==F(r['rhs'])
    dsupport=[r for r,w in enumerate(raw['ineqlin']['marginals']) if -w>1e-9]
    dcols=[j for j,m in enumerate(raw['lower']['marginals']) if abs(m)<1e-8]
    D_A=[[F(rows[r]['a'].get(str(j),'0')) for r in dsupport]+[F(e['a'].get(str(j),'0')) for e in eq] for j in dcols]
    D_b=[F(int(j==128)) for j in dcols]
    dhint=[-raw['ineqlin']['marginals'][r] for r in dsupport]+raw['eqlin']['marginals']
    dual,drank=solve_exact(D_A,D_b,len(dsupport)+2,dhint)
    lam={rows[r]['name']:dual[k] for k,r in enumerate(dsupport)};pi=dual[-2:]
    assert all(w>=0 for w in lam.values())
    rowmap={r['name']:r for r in rows}
    residual={}
    for j in range(129):
        val=F(int(j==128))-sum(w*F(rowmap[n]['a'].get(str(j),'0')) for n,w in lam.items())-sum(p*F(e['a'].get(str(j),'0')) for p,e in zip(pi,eq))
        assert val>=0,(j,val);residual[str(j)]=str(val)
    a=pi[0]+sum(w*F(rowmap[n]['bK']) for n,w in lam.items())
    b=pi[1]+sum(w*F(rowmap[n]['bO']) for n,w in lam.items())
    dual_value=a*K+b*O;primal_value=full[128];assert primal_value==dual_value
    assert all(lam[n]*slacks[n]==0 for n in lam)
    assert all(F(residual[str(j)])*full[j]==0 for j in range(129))
    main_new=(1658*K+87*O)/10980;gap=primal_value-main_new
    d=lcm(a.denominator,b.denominator);a_int=int(a*d);b_int=int(b*d)
    divisor=gcd(gcd(d,abs(a_int)),abs(b_int));d//=divisor;a_int//=divisor;b_int//=divisor
    budgetden=lcm(*(w.denominator for w in list(lam.values())+pi))
    compare_slope=a-F(1658,10980);compare_intercept=b-F(87,10980)
    threshold=-compare_intercept/compare_slope if compare_slope else None
    data={'status':'EXACT_PRIMAL_DUAL_MATCH','claim':'Exact optimum at the specified K0 of this 128-type necessary root-C cone and a universal affine root bound; not a globally optimal root bound or complete SPE.',
          'input_sha256':sha(H/'exact_input.json'),'discovery_sha256':sha(H/'discovery_output.json'),
          'primal':{str(j):str(v) for j,v in primal.items() if v},'objective':str(primal_value),'objective_decimal':float(primal_value),
          'raw_row_slacks':{n:str(v) for n,v in slacks.items()},
          'dual':{'row_weights':{n:str(w) for n,w in lam.items() if w},'equality_C_size':str(pi[0]),'equality_OPT_union':str(pi[1]),
                  'column_residuals':residual,'common_budget_denominator':str(budgetden),
                  'integer_row_weights':{n:str(w*budgetden) for n,w in lam.items() if w},
                  'integer_equality_multipliers':[str(p*budgetden) for p in pi]},
          'universal_root_line':{'convention':'u >= a*K+b*O','a':str(a),'b':str(b),'integer_line':{'u':str(d),'K':str(a_int),'O':str(b_int)},
                                 'all_128_types_retained':True,'root_u_residual':residual['128']},
          'comparison_Main_NEW':{'value_at_K0':str(main_new),'value_at_K0_decimal':float(main_new),
                                 'improvement_at_K0':str(gap),'improvement_decimal':float(gap),
                                 'new_minus_Main_slope':str(compare_slope),'new_minus_Main_intercept':str(compare_intercept),
                                 'crossing_K_over_O':str(threshold) if threshold is not None else None},
          'recovery':{'primal_support':support,'active_raw_rows':[rows[r]['name'] for r in active],'primal_linear_system':prank,
                      'dual_positive_row_names':[rows[r]['name'] for r in dsupport],'dual_zero_reduced_cost_columns':dcols,'dual_linear_system':drank},
          'optimizer_calls':1,'exact_arithmetic_only_after_discovery':True}
    save('exact_certificate.json',data)
    text=['column\tbits_p_y2_y3_y4_y5_z_o\tprimal_mass\tdual_residual']
    for atom in inp['atoms']:
        j=atom['index'];text.append(f'{j}\t{"".join(map(str,atom["bits"]))}\t{full[j]}\t{residual[str(j)]}')
    text.append(f'128\tu\t{full[128]}\t{residual["128"]}')
    (H/'all_129_column_checks.tsv').write_text('\n'.join(text)+'\n')
    print(json.dumps({k:data[k] for k in ['status','objective','objective_decimal','universal_root_line','comparison_Main_NEW']},indent=2))
    print(json.dumps({'weights':data['dual']['row_weights'],'equalities':pi,'primal_system':prank,'dual_system':drank},default=str,indent=2))
if __name__=='__main__':main()
