"""One deterministic actual-signature atom repairs the old616 source budget.

Recover a rational616 lift with source payment r'>u4, then add mass6(r'-u4)
of an explicit actual A4/A6 atom. This preserves the actual utility linkage and
all616 budgets while the new624 direction remains negative. This is a local
projection witness, not a completion of all5799 rows or a complete SPE.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import json,hashlib,time,sys
import numpy as np
from scipy.linalg import qr
import reverse_terminal_624_v1 as cone
from separate_master import blocks_from_columns,div

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'portfolio_comparison'))
from recover_single_lifts import square_solve


def main():
    start=time.monotonic();package_raw=(HERE/'reverse_terminal_5799_one_v1.json').read_bytes();package=json.loads(package_raw)
    raw=Path(package['source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==package['source_sha256']
    data=json.loads(raw);columns=data['columns'];blocks=blocks_from_columns(columns);actual=list(map(F,package['actual_utilities']));r,u=actual[3],actual[5];K=F(package['K']);orb=(0,0)
    visible=cone.base.visible_distribution(blocks,0,orb,3);res=cone.base.solve(visible,u,K,3,4);assert res.success
    names=cone.base.NAMES;bud=cone.base.budget(3);hc=cone.base.hidden_configs(3);count=len(hc);n=len(visible)
    @lru_cache(None)
    def fs(vi,hi):
        p,ell,t,qs,mu,mass=visible[vi]
        return cone.feature_vector(p,ell,t,qs,mu,hi,3,orb)[:616]
    bases=[];extras=[]
    for vi in range(n):
        weights=res.x[vi*count:(vi+1)*count];base=int(np.argmax(weights));assert weights[base]>0;bases.append(base)
        extras.extend((vi,hi) for hi,x in enumerate(weights) if hi!=base and x>1e-11)
    fixed=[sum(state[-1]*fs(vi,bases[vi])[ni] for vi,state in enumerate(visible)) for ni in range(616)]
    equations=[];rhs=[];labels=[]
    for ni,name in enumerate(names):
        if res.ineqlin.residual[ni]>1e-8:continue
        equations.append([fs(vi,hi)[ni]-fs(vi,bases[vi])[ni] for vi,hi in extras]+[-F(bud[ni][0])])
        rhs.append(bud[ni][1]*u+bud[ni][2]*K-fixed[ni]);labels.append(name)
    _,R,piv=qr(np.asarray(equations,dtype=float).T,pivoting=True,mode='economic');size=len(extras)+1
    assert sum(abs(R[i,i])>1e-10 for i in range(min(R.shape)))==size
    selected=list(map(int,piv[:size]));sol=square_solve([equations[j] for j in selected],[rhs[j] for j in selected]);assert min(sol)>=0
    recovered=sol[-1];delta=recovered-r;assert delta>0
    basemasses=[v[-1] for v in visible];records=[]
    for (vi,hi),weight in zip(extras,sol[:-1]):
        if weight:basemasses[vi]-=weight;records.append({'visible':vi,'hidden':list(hc[hi]),'mass':str(weight)})
    assert min(basemasses)>=0
    records.extend({'visible':vi,'hidden':list(hc[hi]),'mass':str(weight)} for vi,(hi,weight) in enumerate(zip(bases,basemasses)) if weight)
    hindex={h:i for i,h in enumerate(hc)};sums=[F(0)]*616;masses=[F(0)]*n
    for record in records:
        vi=record['visible'];hi=hindex[tuple(record['hidden'])];weight=F(record['mass']);masses[vi]+=weight
        for j,value in enumerate(fs(vi,hi)):sums[j]+=weight*value
    assert masses==[v[-1] for v in visible]
    oldslacks=[b[0]*recovered+b[1]*u+b[2]*K-value for b,value in zip(bud,sums)];assert min(oldslacks)>=0
    # The explicit new type uses the existing17 labels; its old six words are
    # all111 and the originalR/Z membership is1 for every selected index pair.
    padding_actual=(0,0,0,1,0,1);padding_words=((1,1,1),)*6
    qs,mu=cone.base.queries_and_moments(padding_actual,padding_words,0,1,1,1);padding_mass=6*delta
    padding_state=(0,1,1,qs,mu,padding_mass);padding_hidden=(1,1,1,1,0,0);padding_hi=hindex[padding_hidden]
    padvector=cone.feature_vector(*padding_state[:-1],padding_hi,3,orb)[:616]
    newactual=[value+padding_mass*F(padding_actual[i],2) for i,value in enumerate(actual)];newK=K+padding_mass
    combined=visible+[padding_state]
    linked=[sum(mass*div(q[i],sum(q[:6])) for p,ell,t,q,mom,mass in combined) for i in range(6)];assert linked==newactual
    newslacks=[b[0]*newactual[3]+b[1]*newactual[5]+b[2]*newK-value-padding_mass*pad for b,value,pad in zip(bud,sums,padvector)];assert min(newslacks)>=0
    records.append({'visible':n,'hidden':list(padding_hidden),'mass':str(padding_mass)});records.sort(key=lambda record:(record['visible'],record['hidden']))
    cut=package['cuts'][0];theta={name:F(w) for name,w in cut['weights'].items()};row,au,aK,psi=cone.make_row(columns,blocks,0,orb,3,theta)
    pad_min=psi(*padding_state[:-1]);pad_slack=F(1,2)+au/2+aK-pad_min;assert pad_slack==F(1,6)
    negative=newactual[3]+au*newactual[5]+aK*newK-sum(mass*psi(p,ell,t,q,mom) for p,ell,t,q,mom,mass in combined)
    assert negative==F(cut['exact_slack'])+delta and negative<0
    # Additional visible-menu last prices and capacities are retained as well;
    # these checks are not a claim about all early-position master constraints.
    menu_caps=[newK-sum(mass*q[qi] for p,ell,t,q,mom,mass in combined) for qi in range(17)]
    menu_prices=[newactual[5]-sum(mass*q[qi]/(ell+1) for p,ell,t,q,mom,mass in combined) for qi in range(17)]
    assert min(menu_caps)>=0 and min(menu_prices)>=0
    out={'status':'PASS','scope':'General actual-fourth-source/R/orb00/17-menu local projection domain with one additional111 histogram. A complete616 hidden lift is feasible at actual-linked newu4/u6/K but a624 true row is negative. No claim of full5799-master feasibility or completeSPE.','base_source_path':package['source_path'],'base_source_sha256':package['source_sha256'],'separator_package_sha256':hashlib.sha256(package_raw).hexdigest(),'query_menu':package['query_menu'],'original_actual_utilities':list(map(str,actual)),'original_K':str(K),'recovered_old616_feasible_source':str(recovered),'source_gap_delta':str(delta),'source_gap_delta_float':float(delta),'reduced_system_size':size,'selected_equation_labels':[labels[j] for j in selected],'original_lift_minimum_slack_at_recovered_source':str(min(oldslacks)),'padding':{'actual_bits':padding_actual,'six_old_words':padding_words,'R':1,'Z':1,'macro_hidden':padding_hidden,'mass':str(padding_mass),'source_slack_per_unit':'1/6','new_cut_slack_per_unit':str(pad_slack)},'actual_utilities':list(map(str,newactual)),'K':str(newK),'visible':[{'state':[p,ell,t,list(map(str,q)),list(map(str,mom))],'mass':str(mass)} for p,ell,t,q,mom,mass in combined],'hidden_lift':records,'all616_slacks_at_actual':{name:str(value) for name,value in zip(names,newslacks)},'minimum_old616_slack':str(min(newslacks)),'all17_menu_caps':list(map(str,menu_caps)),'all17_actual_terminal_prices':list(map(str,menu_prices)),'new624_weights':cut['weights'],'new624_reverse_weights':cut['new_reverse_weights'],'new624_exact_slack':str(negative),'new624_slack_float':float(negative),'new624_visible_minima':list(map(str,(psi(p,ell,t,q,mom) for p,ell,t,q,mom,mass in combined))),'elapsed_seconds':time.monotonic()-start}
    target=HERE/'actual_padding_616_vs_624_strictness_5799_v1.json';target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS','visible_types':len(combined),'hidden_atoms':len(records),'reduced_system_size':size,'source_gap_delta':float(delta),'padding_mass':float(padding_mass),'minimum616_slack':str(min(newslacks)),'new624_slack':float(negative),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'elapsed':out['elapsed_seconds']},ensure_ascii=False))


if __name__=='__main__':main()
