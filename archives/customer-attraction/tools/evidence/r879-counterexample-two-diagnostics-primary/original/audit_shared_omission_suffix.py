"""Exact unit-customer replay of two prescribed last-node comparisons, not SPE search."""
from fractions import Fraction as F
from collections import Counter
import json
from pathlib import Path


def replay(name, xi, xj, yi, yj, hi, hj, ri, rj, q):
    Xi={f'xi:{t}' for t in range(xi)}; Xj={f'xj:{t}' for t in range(xj)}
    Yi={f'y:{t}' for t in yi}; Yj={f'y:{t}' for t in yj}
    Hi={f'h:{t}' for t in hi}; Hj={f'h:{t}' for t in hj}
    q={f'h:{x}':n for x,n in q.items()}
    Ai=Xi|Yi; Aj=Xj|Yj; Bi=Ai|Hi; Bj=Aj|Hj
    def delta(A, otherX, B, otherB, r):
        load=Counter(q)
        load.update(A); load.update(otherX)
        for _ in range(r-1):load.update(B)
        def payoff(topic):return sum((F(1,1+load[x]) for x in topic),F(0))
        return payoff(B)-payoff(otherB), payoff(B), payoff(otherB)
    dij,ui,devj=delta(Ai,Xj,Bi,Bj,ri)
    dji,uj,devi=delta(Aj,Xi,Bj,Bi,rj)
    vi=sum((F(1,q.get(x,0)+1) for x in Hi),F(0))
    vj=sum((F(1,q.get(x,0)+1) for x in Hj),F(0))
    a=len(Yi-Yj);b=len(Yj-Yi);d=a+b
    def E(H1,H2,r):return sum((F(1,q.get(x,0)+1)-F(1,q.get(x,0)+r) for x in H1-H2),F(0))
    eij=E(Hi,Hj,ri);eji=E(Hj,Hi,rj)
    fi=F(xi-xj,2)+vi-vj+F(3*(len(Yi)-len(Yj)),4)-F(d,4)-F((ri-1)*(xi+a),2*(ri+1))-eij
    fj=F(xj-xi,2)+vj-vi+F(3*(len(Yj)-len(Yi)),4)-F(d,4)-F((rj-1)*(xj+b),2*(rj+1))-eji
    joint=-F(d,2)-F((ri-1)*(xi+a),2*(ri+1))-F((rj-1)*(xj+b),2*(rj+1))-eij-eji
    assert dij==fi and dji==fj and dij+dji==joint
    both=dij>=0 and dji>=0
    if both:
        assert Yi==Yj and ri==rj==1 and F(xi,2)+vi==F(xj,2)+vj
    return dict(name=name, x=[xi,xj], Y=[sorted(yi),sorted(yj)], H=[sorted(hi),sorted(hj)], r=[ri,rj], q=q,
                on=[str(ui),str(uj)], alternative=[str(devj),str(devi)], delta=[str(dij),str(dji)],
                joint=str(joint), bank_dilution=[str(eij),str(eji)], both_prescribed_actions_best_among_pair=both)

cases=[
 ('common_bank_equal_Y_one_punisher',2,2,{0,1},{0,1},{0,1},{0,1},1,1,{}),
 ('common_bank_disjoint_Y',2,2,{0},{1},{0},{0},1,1,{}),
 ('common_bank_overlapping_Y',4,4,{0,1,2},{1,2,3},{0,1},{0,1},1,1,{0:3,1:1}),
 ('common_bank_equal_Y_two_punishers',3,3,{0,1},{0,1},{0},{0},2,2,{}),
 ('signed_core_and_omission_differences',2,5,{0,1,2,3},{2,3},{0},{0},1,3,{}),
 ('different_banks_can_balance_core',2,4,{0,1},{0,1},{0},set(),1,1,{}),
 ('different_banks_nonuniform_baseline',3,5,{0,1,2},{1,2,3,4},{0,1,2},{1,3},2,3,{0:2,1:4,2:0,3:1}),
 ('empty_omission_different_banks',1,3,set(),set(),{0},{1},2,1,{0:0,1:4}),
]
report={'scope':'Exact two-terminal-node algebra replay; no SPE certificate or main-conjecture conclusion.',
        'cases':[replay(*case) for case in cases]}
out=Path(__file__).with_name('shared_omission_suffix_audit.json')
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'cases':len(cases),'all_identities_exact':True,'output':str(out)},ensure_ascii=False))
