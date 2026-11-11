#!/usr/bin/env python3
"""Exact phase-I dual basis and all-type moment-envelope Farkas cut."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import lcm,gcd
from functools import reduce
import json,hashlib
from build_input import coefficient,base

H=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):(H/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def linear_solve(A,b,n,hint):
    M=[[F(x) for x in row]+[F(y)] for row,y in zip(A,b)];piv=[];r=0
    for c in range(n):
        at=next((j for j in range(r,len(M)) if M[j][c]),None)
        if at is None:continue
        M[r],M[at]=M[at],M[r];d=M[r][c];M[r]=[v/d for v in M[r]]
        for j in range(len(M)):
            if j!=r and M[j][c]:
                t=M[j][c];M[j]=[v-t*w for v,w in zip(M[j],M[r])]
        piv.append(c);r+=1
    assert all(any(row[:n]) or not row[-1] for row in M)
    free=[c for c in range(n) if c not in piv];x=[F(0)]*n
    for c in free:x[c]=F(str(hint[c])).limit_denominator(1000000)
    for row,c in zip(M,piv):x[c]=row[-1]-sum(row[j]*x[j] for j in free)
    assert all(sum(F(a)*v for a,v in zip(row,x))==F(y) for row,y in zip(A,b))
    return x,{'rank':len(piv),'unknowns':n,'free_columns':free,'equations':len(A)}
def main():
    inp=json.loads((H/'exact_input.json').read_text());raw=json.loads((H/'discovery_output.json').read_text())
    assert raw['success'] and raw['fun']>0 and raw['optimizer_calls']==1 and raw['input_sha256']==sha(H/'exact_input.json')
    rows=inp['raw_rows'];eq=inp['equalities'];atoms=inp['all_old_atoms']
    support=[i for i,w in enumerate(raw['ineqlin']['marginals']) if -w>1e-10]
    cols=[j for j in range(160) if abs(raw['lower']['marginals'][j])<1e-8]
    A=[[F(rows[i]['a'].get(str(j),'0')) for i in support]+[-F(e['a'].get(str(j),'0')) for e in eq] for j in cols]
    b=[F(0)]*len(cols);A.append([F(1)]*len(support)+[F(0)]*len(eq));b.append(F(1))
    hint=[-raw['ineqlin']['marginals'][i] for i in support]+raw['eqlin']['marginals']
    dual,rank=linear_solve(A,b,len(support)+len(eq),hint)
    phase_weights={rows[i]['name']:dual[k] for k,i in enumerate(support)};betas=dual[len(support):]
    assert all(w>=0 for w in phase_weights.values()) and sum(phase_weights.values())==1
    rowmap={r['name']:r for r in rows};phase_res={}
    for j in range(160):
        v=sum(w*F(rowmap[n]['a'].get(str(j),'0')) for n,w in phase_weights.items())-sum(beta*F(e['a'].get(str(j),'0')) for beta,e in zip(betas,eq))
        assert v>=0,(j,v);phase_res[str(j)]=str(v)
    phase_bound=sum(beta*F(e['rhs']) for beta,e in zip(betas,eq))-sum(w*F(rowmap[n]['rhs']) for n,w in phase_weights.items())
    assert phase_bound>0
    genuine={n:w for n,w in phase_weights.items() if rowmap[n]['family'] not in ('Q_LOWER','Q_UPPER') and w>0}
    denom=lcm(*(w.denominator for w in genuine.values()));integers={n:int(w*denom) for n,w in genuine.items()}
    g=reduce(gcd,integers.values());weights={n:v//g for n,v in integers.items()}
    chosen=[rowmap[n] for n in weights]
    envelope=[];env={};residuals=[];cut={};state_lines=['atom\tq\ttail\tweighted_A\taq_minimum\tlower_weight\tupper_weight\tresidual']
    wallet={f'v{i}':0 for i in range(1,7)};wallet.update(K=0,u=0)
    for n,w in weights.items():
        r=rowmap[n]
        if r['family']=='SOURCE_IC':wallet['v3']+=w
        elif r['family']=='OLD_SAFE':wallet[f'v{r["source"]}']+=w
        wallet['K']+=w*F(r['base_K']);wallet['u']+=w*F(r['base_u'])
    for atom in atoms:
        byq={}
        for q in (0,1):
            byq[q]=[(tuple(s),sum((weights[r['name']]*coefficient(r,atom,q,s) for r in chosen),F(0))) for s in product((0,1),repeat=3)]
        a0=min(v for s,v in byq[0]);a1=min(v for s,v in byq[1]);delta=max(a1-a0,F(0));gamma=max(a0-a1,F(0));o=atom['bits'][6]
        m=a0+delta*F(o,6)-gamma*o
        assert m==(a0 if not o else min((5*a0+a1)/6,a1))
        rec={'atom':atom['index'],'a0':str(a0),'a1':str(a1),'lower_weight':str(delta),'upper_weight':str(gamma),'minimum':str(m),
             'argmin_q0':[k for k,(s,v) in enumerate(byq[0]) if v==a0],'argmin_q1':[k for k,(s,v) in enumerate(byq[1]) if v==a1]}
        envelope.append(rec);env[atom['index']]=rec
        for q in (0,1):
            aq=a0 if not q else a1
            for s,v in byq[q]:
                residual=v+(gamma-delta)*q-a0;assert residual==v-aq and residual>=0
                residuals.append(residual)
                state_lines.append(f'{atom["index"]}\t{q}\t{"".join(map(str,s))}\t{v}\t{aq}\t{delta}\t{gamma}\t{residual}')
        basevalue=sum((weights[r['name']]*base(r,atom) for r in chosen),F(0))
        cut[str(atom['index'])]=str(basevalue-m)
    save('universal_moment_envelope.json',envelope)
    (H/'all_2048_state_residuals.tsv').write_text('\n'.join(state_lines)+'\n')
    table=['atom\tp_y2_y3_y4_y5_z_o\ta0\ta1\tminimum\tcut_coefficient']
    for atom in atoms:
        e=env[atom['index']];table.append(f'{atom["index"]}\t{"".join(map(str,atom["bits"]))}\t{e["a0"]}\t{e["a1"]}\t{e["minimum"]}\t{cut[str(atom["index"])]}')
    (H/'universal_cut_128.tsv').write_text('\n'.join(table)+'\n')
    mass={int(h):F(m) for h,m in inp['fixed_mass'].items()};K=F(inp['fixed_K']);u=F(inp['fixed_u'])
    B=sum((weights[r['name']]*F(r['rhs']) for r in chosen),F(0))
    M=sum((F(env[h]['minimum'])*w for h,w in mass.items()),F(0));value=B-M
    assert value<0
    assert value==sum((F(cut[str(h)])*w for h,w in mass.items()),F(0))+F(wallet['K'])*K+F(wallet['u'])*u
    fixed_res={}
    for col in inp['columns']:
        e=env[col['atom']];v=sum((weights[r['name']]*F(r['a'].get(str(col['index']),'0')) for r in chosen),F(0))
        rr=v+(F(e['upper_weight'])-F(e['lower_weight']))*col['q']-F(e['a0']);assert rr>=0;fixed_res[str(col['index'])]=str(rr)
    normalization=F(sum(weights.values()))+sum(F(env[h]['lower_weight'])+F(env[h]['upper_weight']) for h in mass)
    normalized_bound=-value/normalization;assert normalized_bound>0
    result={'status':'EXACT_INFEASIBLE','claim':'The released maximal-root-tail point has no completion of this six-optimal-label source3 requery layer; the moment-envelope cut is valid on all128 old types. Not a complete-SPE or sharp-root-line claim.',
            'input_sha256':sha(H/'exact_input.json'),'discovery_sha256':sha(H/'discovery_output.json'),
            'genuine_row_weights':weights,'wallet_coefficients':{k:str(v) for k,v in wallet.items()},
            'fixed_weighted_budget_rhs':str(B),'fixed_weighted_moment_minimum':str(M),'fixed_cut_value':str(value),'fixed_cut_value_decimal':float(value),
            'fixed_extended_q_weights':{str(h):{'lower':env[h]['lower_weight'],'upper':env[h]['upper_weight']} for h in mass},
            'fixed_mass_multipliers':{str(h):env[h]['a0'] for h in mass},'fixed_column_residuals':fixed_res,
            'extended_certificate_weight_sum':str(normalization),'extended_phase_I_lower_bound':str(normalized_bound),'extended_phase_I_lower_bound_decimal':float(normalized_bound),
            'universal_cut':{'convention':'sum cut_z[h]*w_h + cut_K*K + cut_u*u >= 0','cut_z':cut,'cut_K':str(wallet['K']),'cut_u':str(wallet['u']),
                             'all_old_types':128,'all_q_tail_states':2048,'q_interval':'[o/6,o]','envelope_sha256':sha(H/'universal_moment_envelope.json'),
                             'state_residuals_sha256':sha(H/'all_2048_state_residuals.tsv')},
            'recovered_phase_dual':{'row_weights':{n:str(w) for n,w in phase_weights.items()},'mass_multipliers':{e['name']:str(beta) for e,beta in zip(eq,betas)},
                                    'column_residuals':phase_res,'epsilon_residual':'0','lower_bound':str(phase_bound),'linear_system':rank},
            'optimizer_calls':1,'exact_arithmetic_only_after_discovery':True}
    save('exact_certificate.json',result)
    print(json.dumps({k:result[k] for k in ['status','genuine_row_weights','wallet_coefficients','fixed_cut_value','fixed_cut_value_decimal','extended_phase_I_lower_bound','extended_phase_I_lower_bound_decimal']},indent=2))
    print(json.dumps({'phase_dual_recovery':rank,'phase_dual_exact_lower_bound':str(phase_bound),'state_residuals_zero':sum(v==0 for v in residuals),'state_residuals_positive':sum(v>0 for v in residuals)},indent=2))
if __name__=='__main__':main()
