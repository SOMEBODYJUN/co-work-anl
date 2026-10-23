"""One explicit three-response tail diagnostic; not a main SPE counterexample."""
from fractions import Fraction
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver

def make(k=2):
    sets={}
    X=[{f'x{j}_{i}' for i in range(2)} for j in range(k)]
    P=[{f'p{j}_{i}' for i in range(3)} for j in range(k)]
    Y={f'y{i}' for i in range(4)}; Z={f'z{i}' for i in range(4)}
    E=[{f'e{j}_{i}' for i in range(n)} for j,n in enumerate((18,12,12))]
    for j in range(k):
        sets[f'C{j}']=X[j];sets[f'A{j}']=X[j]|P[j]
        sets[f'T1_{j}']=E[0]|E[1]|X[j]|P[j]
        sets[f'T2_{j}']=E[0]|E[2]|X[j]|P[j]
    sets['CB']=Y;sets['AB']=Y|Z;sets['T3']=E[1]|E[2]|Y|Z;sets['D']=set.union(*E)
    names=tuple(sets); idx={s:i for i,s in enumerate(names)}
    ins=Instance.from_topic_sets(sets.values(),k+4,names)
    return ins,idx

if __name__=='__main__':
    ins,idx=make(); solver=ExactSPESolver(ins)
    pref=['C0','C1','CB']; outcomes={}
    for label,actual in [('small_A',['A0','C1','CB']),('large_A',['C0','C1','AB'])]:
        counts=ins.counts(tuple(idx[s] for s in actual)); outs=solver.outcomes(counts)
        leader=idx['A0' if label=='small_A' else 'AB']
        target=counts
        for s in ['T1_0','T2_0','T3']:
            j=idx[s];target=target[:j]+(target[j]+1,)+target[j+1:]
        out={'outcome_count':len(outs),'leader_min':str(min(ins.topic_payoff(leader,z) for z in outs)),'leader_max':str(max(ins.topic_payoff(leader,z) for z in outs)),'target_terminal_in_outcomes':target in outs}
        if target in outs:
            seq=tuple(idx[s] for s in actual+['T1_0','T2_0','T3'])
            q=counts
            checks=[]
            for action in seq[len(actual):]:
                checks.append({'prescribed':ins.topics[action],'payoff':str(ins.topic_payoff(action,target)),'threshold':str(solver.threshold(q))})
                q=q[:action]+(q[action]+1,)+q[action+1:]
            out['ordered_tail_admissible']=all(Fraction(c['payoff'])>=Fraction(c['threshold']) for c in checks)
            out['ordered_checks']=checks
        outcomes[label]=out
    outcomes['stats']=solver.stats.__dict__
    print(json.dumps(outcomes,indent=2))

# Export one full ordered-history three-responder certificate. Prefix players
# stay fixed and are not asserted optimal at their earlier decision nodes.
def export_certificate(path):
    ins,idx=make(); solver=ExactSPESolver(ins)
    pref=tuple(idx[s] for s in ['A0','C1','CB'])
    actual=tuple(idx[s] for s in ['T1_0','T2_0','T3'])
    target=ins.counts(pref+actual,terminal=True); initial=ins.counts(pref)
    assert target in solver.outcomes(initial)
    actions={}
    def increment(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
    def expand(h,q,z):
        if len(h)==3:
            assert q==z
            return
        threshold=solver.threshold(q)
        admissible=[a for a in range(ins.topic_count) if z in solver.outcomes(increment(q,a)) and ins.topic_payoff(a,z)>=threshold]
        a=actual[len(h)] if h==actual[:len(h)] else min(admissible)
        assert a in admissible
        actions[h]=a
        for b in range(ins.topic_count):
            child=increment(q,b)
            want=z if a==b else min(solver.outcomes(child),key=lambda t:(ins.topic_payoff(b,t),t))
            expand(h+(b,),child,want)
    expand((),initial,target)
    def outcome(h):
        while len(h)<3:h=h+(actions[h],)
        return ins.counts(pref+h,terminal=True)
    comparisons=0;strict=0
    for h,a in actions.items():
        value=ins.topic_payoff(a,outcome(h+(a,)))
        for b in range(ins.topic_count):
            other=ins.topic_payoff(b,outcome(h+(b,)))
            assert value>=other,(h,a,b,value,other)
            comparisons+=1;strict+=value>other
    obj={'scope':'full three-responder SPE after fixed prefix; prefix-player optimality is not asserted','instance':ins.to_dict(),'fixed_prefix':list(pref),'on_path_suffix':list(actual),'terminal':list(target),'actions':[{'history':list(h),'action':a} for h,a in sorted(actions.items())],'audit':{'ordered_nodes':len(actions),'comparisons_including_self':comparisons,'strict_comparisons':strict,'leader_payoff':str(ins.topic_payoff(idx['A0'],target)),'responder_payoffs':[str(ins.topic_payoff(a,target)) for a in actual]}}
    Path(path).write_text(json.dumps(obj,indent=2))
    return obj['audit']
