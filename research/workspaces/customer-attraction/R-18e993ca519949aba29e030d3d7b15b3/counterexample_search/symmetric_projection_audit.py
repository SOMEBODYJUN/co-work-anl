"""Exact bottom-prefix audit of the fully symmetric 15-topic projection."""
import itertools,json,math,time
from fractions import Fraction as F
from cone_walk import ROOT,HERE
from customer_attraction import Instance,CustomerType,ExactSPESolver,verify_certificate

def main():
    started=time.monotonic()
    primal=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal']
    masses={}
    for atom in primal['atoms']:
        j=sum(atom['AB_hist'][4:])
        for selected in itertools.combinations(range(5),j):
            mask=sum(int(b)<<a for a,b in enumerate(atom['bits']))+sum(1<<(10+a) for a in selected)
            masses[mask]=masses.get(mask,0)+atom['mass_numerator']*(10//math.comb(5,j))
    common=math.gcd(*masses.values());masses={mask:n//common for mask,n in masses.items()}
    names=tuple('ABCDEUVWXY')+tuple('T'+str(i+1) for i in range(5))
    inst=Instance(names,tuple(CustomerType(frozenset(a for a in range(15) if mask&(1<<a)),n) for mask,n in sorted(masses.items())),5)
    solver=ExactSPESolver(inst);desired=(1,1,1,1,1)+(0,)*10
    rows=[]
    # Deepest obstruction implies no earlier policy could implement ABCDE.
    for depth in range(4,-1,-1):
        prefix=tuple(int(a<depth) for a in range(15))
        outcomes=solver.outcomes(prefix);floor=solver.threshold(prefix);actual=inst.topic_payoff(depth,desired)
        row={'prefix':names[:depth],'desired_continuation_SPE_feasible':desired in outcomes,'actual_chosen_payoff':str(actual),'threshold':str(floor),'margin_actual_minus_threshold':str(actual-floor),'outcome_count':len(outcomes)}
        if desired not in outcomes:
            branch=[]
            for a in range(15):
                child=tuple(v+int(j==a) for j,v in enumerate(prefix));R=solver.outcomes(child)
                mini=min(inst.topic_payoff(a,q) for q in R)
                if mini>actual:
                    q=min(q for q in R if inst.topic_payoff(a,q)==mini)
                    branch.append({'deviation':names[a],'minimum_gain_over_all_SPE_replies':str(mini-actual),'worst_reply_terminal':q})
            row['strictly_profitable_deviations_under_every_SPE_reply']=branch
        rows.append(row)
        print(json.dumps(row),flush=True)
        if desired not in outcomes:break
    result={'description':'Exact deepest-prefix obstruction for a symmetric actual 15-theme projection of the 437-row relaxed point. This does not exclude other realizations or the general conjecture.','instance':inst.to_dict(),'original_relaxation_beta':primal['comparison_cover'],'desired_root':desired,'records':rows,'elapsed':round(time.monotonic()-started,3),'method':'Canonical ExactSPESolver with Fraction, not float proposals.'}
    (HERE/'symmetric_projection_exact_obstruction.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
