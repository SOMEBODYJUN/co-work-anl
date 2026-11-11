"""Exact certificate recovery and retained positive-row transfer pack.

Floating arrays only select supports. Every accepted lift or separator is
recomputed over Fraction and contains the complete original-coordinate row.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import sys, time, platform, traceback, json
import transfer as T

HERE=T.HERE

def projected(weights, fixed, name):
    weights={k:F(v) for k,v in weights.items() if F(v)}
    assert set(weights)<=T.feature_names() and min(weights.values(),default=F(0))>=0
    names=list(weights)
    a=sum(v*T.budget_coefficients(k)[0] for k,v in weights.items())
    u=sum(v*T.budget_coefficients(k)[1] for k,v in weights.items())
    cap=sum(v*T.budget_coefficients(k)[2] for k,v in weights.items())
    x=list(map(F,fixed['original4849_coordinates']))
    row=defaultdict(F);row[0]=cap
    hist_actual={c['hist_column']:c['actual'] for c in fixed['cells']}
    for col,bits in hist_actual.items():
        row[col]+=a*T.pay(bits[3],sum(bits))+u*T.pay(bits[5],sum(bits))
    tables=[];variable_residuals=[];eq_multipliers=[]
    for c in fixed['cells']:
        omega=F(c['omega']);samples=tuple(tuple(s) for s in c['samples'])
        costs=[sum((weights[n]*v for n,v in zip(names,T.values(names,tuple(c['actual']),samples,h))),F(0)) for h in T.HIDDEN]
        psi=min(costs)
        for col,v in c['old_marginal_affine']:row[col]-=omega*psi*F(v)
        residues=[omega*(v-psi) for v in costs]
        assert min(residues)>=0
        variable_residuals.extend(residues)
        mult=omega*psi
        eq_multipliers.append({'cell':c['cell'],'peer_matrix_row':11418+2*c['cell']+(mult<0),'weight':str(abs(mult))})
        tables.append({'cell':c['cell'],'costs_all16':list(map(str,costs)),'minimum':str(psi),'minimizer_hidden_indices':[i for i,v in enumerate(costs) if v==psi]})
        for cost,residue in zip(costs,residues): assert -omega*cost+residue+mult==0
    full=[row[i] for i in range(4849)]+[F(0)]*10744
    slack=sum(v*w for v,w in zip(full[:4849],x))
    exact_other=a*F(fixed['actual_utilities'][3])+u*F(fixed['actual_utilities'][5])+cap*F(fixed['K'])-sum(F(c['omega'])*F(c['mass'])*F(tb['minimum']) for c,tb in zip(fixed['cells'],tables))
    assert exact_other==slack
    return {'name':name,'point_sha256':T.sha(T.POINT),'scope':'actual4/R/family0-off, original16 hist and all312 four-state cells','weights':{k:str(v) for k,v in weights.items()},'wallet':{'u4':str(a),'u6':str(u),'K':str(cap)},'source_zero_face':a==0,'exact_slack':str(slack),'slack_float':float(slack),'sign':('negative' if slack<0 else 'positive' if slack>0 else 'zero'),'sparse_original4849_row':T.sparse(row),'original4849_vector':list(map(str,full[:4849])),'zero_auxiliary_columns':{'first':4849,'count':10744,'last':15592},'dense15593_sha256':T.canon(list(map(str,full))),'literal_hidden_evaluations':4992,'tables':tables,'nonnegative_hidden_column_residuals':list(map(str,variable_residuals)),'nonnegative_margin_direction_multipliers':eq_multipliers,'certificate_identity':'Pi=sum(lambda*raw_budget)+sum(omega*(F-Psi)*X)+sum(omega*Psi*margin_plus); negative Psi uses margin_minus','all_hidden_columns_cancel_exactly':True}

def known():
    fixed=T.read(HERE/'fixed_problem.json')
    records=[]
    specifications=[
        ('single76_5716','joint_requery/selected_cuts_5716.json','cuts'),
        ('common332_5744','joint_requery/portfolio_selected_5744.json','cuts'),
        ('common332_5752','joint_requery/portfolio_selected_5752.json','cuts'),
        ('common616_5775','joint_requery/cross_pairs_selected_5775_v1.json','cuts'),
        ('reverse624_5799','joint_requery/reverse_terminal_5799_one_v1.json','cuts'),
        ('common616_5799','joint_requery/reverse_terminal_5799_one_v1.json','old616_cut'),
    ]
    for label,rel,key in specifications:
        path=T.PEER/rel;pack=T.read(path)
        candidates=pack[key] if isinstance(pack[key],list) else [pack[key]]
        for index,c in enumerate(candidates):
            if c.get('i',3)!=3 or c['member']!=0 or c['orb']!=[0,0]:continue
            w=c['weights']
            if 'query' in c:
                qi=c['query'];w={name.replace(':q',':q'+str(qi)).replace(',q',',q'+str(qi)):val for name,val in w.items()}
            proof=projected(w,fixed,label+'_'+str(index))
            if 'sparse_row' in c:
                assert proof['sparse_original4849_row']==c['sparse_row'],label
            proof['source']={'path':str(path.relative_to(T.REPO)),'sha256':T.sha(path),'record_key':key,'record_index':index,'old_point_slack_not_reused':True}
            records.append(proof)
    path=T.PEER/'master_cuts/complete624_actual4_R00_opt_v2_dual.json'
    d=T.read(path)
    w={v['row_name'].split('macro624:budget:',1)[1]:v['weight'] for v in d['row_multipliers'] if v['row_index']>=12042}
    proof=projected(w,fixed,'complete624_opt_v2_budget_wallet')
    proof['source']={'path':str(path.relative_to(T.REPO)),'sha256':T.sha(path),'interpretation':'nonnegative 624-budget portion only; exact full-peer optimum not transported'}
    records.append(proof)
    report={'point_sha256':T.sha(T.POINT),'status':'PASS','records':records,'positive_count':sum(r['sign']=='positive' for r in records),'zero_count':sum(r['sign']=='zero' for r in records),'negative_count':sum(r['sign']=='negative' for r in records),'all_nonnegative_rows_retained':True}
    T.write('known_rows_transfer_pack.json',report)
    print(json.dumps({'status':'PASS','rows':[{k:r[k] for k in ('name','sign','slack_float')} for r in records]},ensure_ascii=False),flush=True)

def separate():
    import numpy as np
    fixed=T.read(HERE/'fixed_problem.json');raw=np.load(HERE/'phase1_raw_arrays.npz')
    result=T.read(HERE/'phase1_result.json')
    assert result['success'] and result['phase1_objective']>1e-9
    attempts=[]
    for grid in (10**6,10**7,10**8,10**9,10**10):
        w={n:F(round(max(0,-float(v))*grid),grid) for n,v in zip(fixed['names'],raw['ineq_dual'])}
        w={n:v for n,v in w.items() if v}
        proof=projected(w,fixed,'phase1_exact_separator')
        attempts.append({'grid':grid,'exact_slack':proof['exact_slack'],'slack_float':proof['slack_float'],'weights':proof['weights']})
        if F(proof['exact_slack'])<0:
            proof['discovery']={'phase1_raw_sha256':T.sha(HERE/'phase1_raw_arrays.npz'),'rounding_grid':grid,'attempts':attempts,'floating_status_not_used_as_proof':True}
            T.write('separating_row_exact.json',proof)
            print(json.dumps({k:proof[k] for k in ('name','wallet','exact_slack','slack_float')},ensure_ascii=False),flush=True)
            return
    T.write('separation_failures.json',attempts)
    raise AssertionError('No exact separator recovered from the phase-I multipliers')

def recover():
    import numpy as np
    from scipy.linalg import qr
    import sympy as sp
    fixed=T.read(HERE/'fixed_problem.json');raw=np.load(HERE/'phase1_raw_arrays.npz')
    result=T.read(HERE/'phase1_result.json')
    assert result['success'] and abs(result['phase1_objective'])<1e-9
    mat=T.read(T.MATRIX)
    coeff=[{col-7639:-F(v) for col,v in row['nonzero'] if col>=7639} for row in mat['rows'][12042:]]
    budgets=list(map(F,fixed['budgets']));m=[F(c['mass']) for c in fixed['cells']]
    xf=raw['x'][:4992]
    attempts=[]
    for threshold in (1e-11,1e-13,1e-9):
        rec={'support_threshold':threshold}
        try:
            support=[i for i,v in enumerate(xf) if v>threshold]
            groups=defaultdict(list)
            for i in support:groups[i//16].append(i)
            assert set(groups)=={i for i,v in enumerate(m) if v>0}
            bases={cell:max(indices,key=lambda j:xf[j]) for cell,indices in groups.items()}
            extra=[i for i in support if i!=bases[i//16]]
            n=len(extra)
            C=[];rhs=[]
            for k in range(624):
                constant=sum(coeff[k].get(base,F(0))*m[cell] for cell,base in bases.items())
                C.append([coeff[k].get(j,F(0))-coeff[k].get(bases[j//16],F(0)) for j in extra])
                rhs.append(budgets[k]-constant)
            active=[i for i,v in enumerate(raw['ineq_residual']) if abs(v)<1e-8]
            if n:
                floating=np.array([[float(c) for c in C[i]] for i in active])
                _,R,piv=qr(floating.T,pivoting=True,mode='economic')
                assert len(piv)>=n and abs(R[n-1,n-1])>1e-10
                chosen=[active[int(i)] for i in piv[:n]]
                A=sp.Matrix([[sp.Rational(v.numerator,v.denominator) for v in C[i]] for i in chosen])
                b=sp.Matrix([sp.Rational(rhs[i].numerator,rhs[i].denominator) for i in chosen])
                solution=A.inv(method='DM')*b
                y=[F(int(v.p),int(v.q)) for v in solution]
            else:chosen=[];y=[]
            full=[F(0)]*4992
            for cell,base in bases.items():full[base]=m[cell]
            for j,v in zip(extra,y):
                full[j]=v;full[bases[j//16]]-=v
            slacks=[budgets[k]-sum(v*full[j] for j,v in coeff[k].items() if full[j]) for k in range(624)]
            rec.update(support=support,bases=bases,core_variables=extra,chosen_active_rows=chosen,minimum_mass=str(min(full)),minimum_budget_slack=str(min(slacks)),exact_negative_budget_rows=[i for i,v in enumerate(slacks) if v<0],exact_negative_variables=[i for i,v in enumerate(full) if v<0])
            assert min(full)>=0 and min(slacks)>=0
            assert all(sum(full[16*i:16*i+16])==mass for i,mass in enumerate(m))
            report={'status':'EXACT_FEASIBLE','point_sha256':T.sha(T.POINT),'matrix_sha256':T.sha(T.MATRIX),'fixed_problem_sha256':T.sha(HERE/'fixed_problem.json'),'all4992_hidden_weights':list(map(str,full)),'nonzero_hidden_weights':[[i+7639,str(v)] for i,v in enumerate(full) if v],'nonzero_count':sum(v>0 for v in full),'all312_marginal_equalities_exact':True,'all624_budgets':[{'feature_index':i,'name':name,'budget':str(budgets[i]),'cost':str(budgets[i]-slacks[i]),'slack':str(slacks[i])} for i,name in enumerate(fixed['names'])],'minimum_mass':str(min(full)),'minimum_budget_slack':str(min(slacks)),'original4849_values_unchanged':True,'our10744_auxiliaries_unchanged':True,'augmented_dimensions':{'rows':20910,'columns':20585},'reconstruction':rec,'prior_reconstruction_failures':attempts,'scope':'one joint actual4/R/family0-off full624 lift; hence all nonnegative624 projected weights including zero source; no all24 closure, no SPE realization'}
            T.write('lift_exact.json',report)
            print(json.dumps({k:report[k] for k in ('status','nonzero_count','minimum_mass','minimum_budget_slack','all312_marginal_equalities_exact','augmented_dimensions')},ensure_ascii=False),flush=True)
            return
        except Exception as e:
            rec['error']=repr(e);rec['traceback']=traceback.format_exc();attempts.append(rec)
    T.write('lift_recovery_failures.json',attempts)
    raise AssertionError('All exact lift candidates failed; no feasible claim')

if __name__=='__main__':
    stage=sys.argv[1]
    receipt={'argv':[sys.executable,*sys.argv],'cwd':str(Path.cwd()),'python':platform.python_version(),'script_sha256':T.sha(Path(__file__)),'transfer_script_sha256':T.sha(HERE/'transfer.py'),'stage':stage,'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
    started=time.monotonic()
    try:
        globals()[stage]();receipt['status']='SUCCESS'
    except BaseException as e:
        receipt.update(status='FAILED',error=repr(e),traceback=traceback.format_exc());raise
    finally:
        receipt['elapsed_seconds']=time.monotonic()-started
        T.write('execution_'+stage+'.json',receipt)
