"""Definition-level exact failure of state transport without potential cycles.

This is an abstract anonymous game, not a customer attraction instance.
"""
from fractions import Fraction
import json
from payoff_state_flow import PayoffGraph


def audit(p=5):
    def utility(a,b):
        return Fraction(b!=a and b!=(a+1)%p)
    sigma={():0}|{(a,):(a+1)%p for a in range(p)}
    for a in range(p):
        b=sigma[a,]
        assert utility(b,a)==max(utility(c,a) for c in range(p))
        assert utility(a,b)==0
        for c in range(p):
            assert utility(a,a)<=utility(a,c)
    security=Fraction(p-2,p)
    assert all(sum(utility(a,b) for a in range(p))/p==security for b in range(p))
    welfare=utility(0,1)+utility(1,0)
    circulation=sum(utility(a,(a+1)%p)-utility((a+1)%p,a) for a in range(p))
    assert circulation==-p
    graph=PayoffGraph(p,2,sigma,True)
    assert not graph.solve([Fraction(1,p)]*p)['success']
    assert graph.solve([Fraction(1,p)]*p,potential=True)['success']
    return {'status':'NOT_A_CUSTOMER_ATTRACTION_INSTANCE','players':2,'topics':p,
            'full_SPE_welfare':str(welfare),'exact_security':str(security),
            'welfare_minus_n_security':str(welfare-2*security),
            'nonzero_exact_potential_circulation':str(circulation),
            'graph_transport_infeasible':True,
            'potential_projected_transport_feasible':True}


if __name__=='__main__':print(json.dumps(audit(),indent=2))
