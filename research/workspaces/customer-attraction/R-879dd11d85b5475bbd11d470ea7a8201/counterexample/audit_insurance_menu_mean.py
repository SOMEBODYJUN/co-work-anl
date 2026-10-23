"""Direct unit-customer/Fraction replay of one specified insurance-family menu diagnostic."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def audit(n,b,s,d):
    assert n>=2 and 0<d<=b and n*d<=2*s
    sizes={'A':2*b-d,'B':b,'C':b*n,'X':s,'Y':s*(n+1),'Z':s}
    clients={a:{f'{a}:{i}' for i in range(v)} for a,v in sizes.items()}
    actions=[p+q for p,q in product('ABC','XYZ')]
    themes={pq:clients[pq[0]]|clients[pq[1]] for pq in actions}
    def load(q1,q2):
        counter=Counter()
        for a,count in zip('ABCXYZ',q1+q2):
            for _ in range(count):counter.update(clients[a])
        return counter
    endpoint_A=load((2,0,n),(1,n,1))
    result=[]
    for topic in actions:
        P,Q=topic
        counts1=(2,0,n) if P=='A' else (1,1,n)
        counts2=(1,n,1) if P=='A' else ((0,n+1,1) if Q=='Z' else (1,n+1,0))
        endpoint=load(counts1,counts2)
        root=sum((F(1,endpoint[x]) for x in themes[topic]),F(0))
        query=sum((F(1,1+endpoint_A[x]) for x in themes[topic]),F(0))
        root_formula=(F(2*b-d,2)+s+(F(s,n) if Q=='Y' else 0)) if P=='A' else F(b+s)
        query_formula={'A':F(2*b-d,3),'B':F(b),'C':F(b*n,n+1)}[P]+(F(s) if Q=='Y' else F(s,2))
        gap_formula=({'A':F(2*b-d,6)+(F(s,n) if Q=='Y' else F(s,2)),
                      'B':F(0) if Q=='Y' else F(s,2),
                      'C':F(b,n+1)+(F(0) if Q=='Y' else F(s,2))})[P]
        assert root==root_formula and query==query_formula and root-query==gap_formula>=0
        result.append({'topic':topic,'root_endpoint':[counts1,counts2],'root_payoff':str(root),
                       'query_on_common_endpoint':str(query),'gap':str(root-query)})
    return {'parameters':{'n':n,'b':b,'s':s,'d':d},'unit_customers':sum(sizes.values()),
            'common_endpoint_counts':[[2,0,n],[1,n,1]],'all_rowwise_comparisons_exact':True,'rows':result}

report={'scope':'One specified insurance architecture; no general menu-mean theorem or main-conjecture conclusion.',
        'reports':[audit(*params) for params in [(2,1,1,1),(3,9,6,3),(5,100,5,2)]]}
out=Path(__file__).with_name('insurance_menu_mean_audit.json')
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'parameter_sets':3,'rows_checked':27,'all_exact':True,'output':str(out)}))
