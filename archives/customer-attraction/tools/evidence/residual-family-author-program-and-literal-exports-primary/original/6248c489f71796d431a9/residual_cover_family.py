"""Exact unit-customer family attacking OPT_m outside the SPE cover <= SPE welfare.

Independent checking below expands the customer types to unit customers and
checks every complete two-player history and every deviation.  It does not
call the repository's SPE solver or certificate verifier.
"""
from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def make_family(q:int):
    if not isinstance(q,int) or isinstance(q,bool) or q<2:
        raise ValueError('q must be an integer at least 2')
    labels=['A','B','D','E']+[f'T{j}' for j in range(1,q+1)]
    types=[({'A'},2*q),({'B'},2*q+1),({'A','D','E'},2),({'B','D','E'},2)]
    for j in range(1,q+1):
        t=f'T{j}'
        types += [({t},2*q-1),({t,'D'},2),({t,'E'},2)]
    instance={'players':2,'topics':labels,'customers':[{'topics':[labels.index(a) for a in sorted(s)],'multiplicity':r} for s,r in types]}
    response={a:('B' if a=='A' else 'E' if a=='D' else 'D') for a in labels}
    return instance,{'root':'A','reply':response}

def audit(q:int):
    instance,strategy=make_family(q);labels=instance['topics']
    # Each list element is a distinct unit customer, including repeated types.
    customers=[frozenset(labels[a] for a in typ['topics']) for typ in instance['customers'] for _ in range(typ['multiplicity'])]
    def pay(history):
        return tuple(sum((Fraction(1,sum(a in c for a in history)) for c in customers if who in c),Fraction(0)) for who in history)
    def covered(history):return {i for i,c in enumerate(customers) if any(a in c for a in history)}
    root_values={};matrix={}
    for a in labels:
        vals={b:pay((a,b))[1] for b in labels}
        b=strategy['reply'][a]
        assert vals[b]==max(vals.values()),(q,a,b,vals)
        root_values[a]=pay((a,b))[0]
        matrix[a]={b:str(v) for b,v in vals.items()}
    assert len(set(root_values.values()))==1
    assert root_values['A']==2*q+2
    assert root_values[strategy['root']]==max(root_values.values())
    actual=('A','B');C=covered(actual)
    opt=max(len(covered(h)) for h in combinations_with_replacement(labels,2))
    residual=max(len(covered(h)-C) for h in combinations_with_replacement(labels,2))
    assert len(customers)==2*q*q+7*q+5
    assert len(C)==4*q+5
    assert opt==residual==4*q+6
    assert covered(('T1','T2')).isdisjoint(C)
    return {'q':q,'players':2,'customer_count':len(customers),'actual':list(actual),'root_payoffs':{a:str(v) for a,v in root_values.items()},'reply_payoff_matrix':matrix,'welfare':len(C),'opt_2':opt,'residual_opt_2':residual,'spe':True,'main_half_inequality':2*len(C)>=opt}

def main():
    instance,strategy=make_family(2)
    (HERE/'residual_family_q2_instance.json').write_text(json.dumps(instance,indent=2)+'\n')
    (HERE/'residual_family_q2_strategy.json').write_text(json.dumps(strategy,indent=2)+'\n')
    report={'method':'Expanded unit customers; exact fractions; all root deviations and all one-action histories; no repository solver/verifier','cases':[audit(q) for q in range(2,13)]}
    (HERE/'residual_family_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'q_tested':list(range(2,13)),'q2':{k:v for k,v in report['cases'][0].items() if k!='reply_payoff_matrix'}},indent=2))
if __name__=='__main__':main()
