"""Exact complete-332 lift at a point separated by a new old-query PAIR.

Mass equations are eliminated symbolically before QR selects the candidate
active square system. All returned masses, budgets, and row evaluations are
then checked with Fraction. No numerical optimality claim is required.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import sys,json,hashlib,time
import numpy as np
from scipy.linalg import qr
import portfolio_master as old
import cross_query_pairs_v1 as new
from separate_master import blocks_from_columns,div

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'portfolio_comparison'))
from recover_single_lifts import square_solve


def recover(visible,res,r_actual,u,K,k):
    hc=old.hidden_configs(k);count=len(hc);n=len(visible);bud=old.budget(k)
    @lru_cache(None)
    def fs(vi,hi):
        p,ell,t,qs,mass=visible[vi]
        ins,alpha,off=old.hidden_arrays(p,ell,t,k)
        return ins[hi]+tuple(a*q+b for q in qs for a,b in zip(alpha[hi],off[hi]))
    bases=[];extras=[]
    for vi in range(n):
        weights=res.x[vi*count:(vi+1)*count]
        base=int(np.argmax(weights));assert weights[base]>0
        bases.append(base)
        extras.extend((vi,hi) for hi,x in enumerate(weights) if hi!=base and x>1e-11)
    variables=extras+[None]  # The last variable is the optimized source payment.
    base_sums=[sum(mass*fs(vi,bases[vi])[ni] for vi,(*state,mass) in enumerate(visible)) for ni in range(len(old.NAMES))]
    eq=[];rhs=[];labels=[]
    for ni,name in enumerate(old.NAMES):
        if res.ineqlin.residual[ni]>1e-8:continue
        eq.append([fs(vi,hi)[ni]-fs(vi,bases[vi])[ni] for vi,hi in extras]+[-F(bud[ni][0])])
        rhs.append(bud[ni][1]*u+bud[ni][2]*K-base_sums[ni]);labels.append(name)
    _,R,piv=qr(np.asarray(eq,dtype=float).T,pivoting=True,mode='economic')
    rank=sum(abs(R[i,i])>1e-10 for i in range(min(R.shape)));assert rank==len(variables),(rank,len(variables))
    selected=list(map(int,piv[:len(variables)]))
    exact=square_solve([eq[i] for i in selected],[rhs[i] for i in selected])
    assert min(exact)>=0
    r_recovered=exact[-1];assert r_recovered<=r_actual,(float(r_recovered-r_actual),r_recovered-r_actual)
    basemass=[v[-1] for v in visible];records=[]
    for (vi,hi),weight in zip(extras,exact[:-1]):
        if weight:
            basemass[vi]-=weight
            records.append({'visible':vi,'hidden':list(hc[hi]),'mass':str(weight)})
    assert min(basemass)>=0
    records.extend({'visible':vi,'hidden':list(hc[hi]),'mass':str(weight)} for vi,(hi,weight) in enumerate(zip(bases,basemass)) if weight)
    records.sort(key=lambda item:(item['visible'],item['hidden']))
    masses=[F(0)]*n;sums=[F(0)]*len(old.NAMES);hindex={h:i for i,h in enumerate(hc)}
    for item in records:
        vi=item['visible'];weight=F(item['mass']);hi=hindex[tuple(item['hidden'])];masses[vi]+=weight
        for ni,value in enumerate(fs(vi,hi)):sums[ni]+=weight*value
    assert masses==[v[-1] for v in visible]
    slack_actual=[b[0]*r_actual+b[1]*u+b[2]*K-s for b,s in zip(bud,sums)]
    slack_recovered=[b[0]*r_recovered+b[1]*u+b[2]*K-s for b,s in zip(bud,sums)]
    assert min(slack_actual)>=0 and min(slack_recovered)>=0
    return {'r_recovered_feasible':str(r_recovered),'r_actual_minus_recovered':str(r_actual-r_recovered),'support':records,'eliminated_mass_equations':n,'reduced_system_size':len(variables),'selected_row_equations':[labels[i] for i in selected],'all_332_slacks_at_actual':{name:str(slack) for name,slack in zip(old.NAMES,slack_actual)},'minimum_slack_at_actual':str(min(slack_actual)),'minimum_slack_at_recovered':str(min(slack_recovered)),'mass_equalities_exact':True,'nonnegative_masses_exact':True}


def main():
    start=time.monotonic();source=HERE.parent/'master_cuts/dynamic_5775_exact.json';raw=source.read_bytes();data=json.loads(raw)
    expected='81983304076358d591cbdac2e6bf7a4b697fc2854aad40918e8cf8cf2d99dd02';assert hashlib.sha256(raw).hexdigest()==expected
    columns=data['columns'];blocks=blocks_from_columns(columns);actual=[sum(F(b['column']['weight'])*div(b['a'][i],sum(b['a'])) for b in blocks) for i in range(6)]
    i=3;member=0;orb=(0,0);k=6-i;K=F(columns[0]['weight']);u=actual[5];r=actual[i]
    visible=old.visible_distribution(blocks,member,orb,i);res=old.solve(visible,u,K,k);assert res.success
    lift=recover(visible,res,r,u,K,k)
    # Use the small integer direction seen in the exact 616 separation, but
    # independently rebuild its entire finite minimum and 4849-coordinate row.
    integers={'sourceT':267,'sourceC':146,'price:b':49,'price:c':45,'price:j':28,'price:v':42,'cap:v':14,'last2:b':56,'last1:q6':34,'last1:q8':32,'last1:q10':32,'oldpair1:6,10:product':48}
    theta={name:F(weight,413) for name,weight in integers.items()}
    row,au,aK,psi=new.make_row(columns,blocks,member,orb,i,theta);negative=sum(F(c['weight'])*value for c,value in zip(columns,row));assert negative<0
    fullvis=new.visible_distribution(blocks,member,orb,i)
    assert negative==r+au*u+aK*K-sum(w*psi(p,ell,t,qs,mu) for p,ell,t,qs,mu,w in fullvis)
    out={'status':'PASS','scope':'A full 332-feature shared-17-query hidden lift is feasible at one fixed actual-linked source/orbit distribution, while a 12-integer-weight 616 cross-query PAIR cut is negative. No SPE construction is asserted.','source_path':str(source),'source_sha256':expected,'i':i,'k':k,'member':member,'orb':orb,'actual_utilities':list(map(str,actual)),'K':str(K),'query_menu':new.QUERY_MENU,'old_feature_count':len(old.NAMES),'old_visible':[{'state':[p,ell,t,list(map(str,qs))],'mass':str(w)} for p,ell,t,qs,w in visible],'old_lift':lift,'cross_cut':{'integer_weights':integers,'source_denominator':413,'normalized_weights':{n:str(w) for n,w in theta.items()},'u6_coefficient':str(au),'K_coefficient':str(aK),'exact_slack':str(negative),'slack_float':float(negative),'sparse_row':[[j,str(v)] for j,v in enumerate(row) if v],'row_sha256':hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest(),'visible_minima':[{'state':[p,ell,t,list(map(str,qs)),list(map(str,mu))],'mass':str(w),'minimum':str(psi(p,ell,t,qs,mu))} for p,ell,t,qs,mu,w in fullvis]},'elapsed_seconds':time.monotonic()-start}
    target=HERE/'exact_332_lift_cross_strictness_5775_v1.json';target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'visible_states':len(visible),'hidden_support':len(lift['support']),'reduced_system_size':lift['reduced_system_size'],'old_minimum_slack':lift['minimum_slack_at_actual'],'old_source_margin_float':float(F(lift['r_actual_minus_recovered'])),'cross_slack':float(negative),'target':str(target),'elapsed_seconds':out['elapsed_seconds']},ensure_ascii=False))


if __name__=='__main__':main()
