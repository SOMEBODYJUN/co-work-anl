"""Independent replay of the pre-existing precise terminal-price-tax failure."""
import json
from fractions import Fraction as F
from pathlib import Path
root=Path(__file__).resolve().parents[6]
source=root/'research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/terminal_balance/refined_failure.json'
d=json.loads(source.read_text());m=d['m'];customers=d['instance']['customers']
strategy={tuple(z['history']):z['action'] for z in d['certificate']['actions']}
def rollout(h):
    while len(h)<m:h=h+(strategy[h],)
    return h
def payoff(path,action):
    return sum((F(z['multiplicity'],sum(j in z['topics'] for j in path))
                for z in customers if action in z['topics']),F())
checks=0
for history,action in strategy.items():
    actual=payoff(rollout(history),action)
    for alternative in range(d['p']):
        assert actual>=payoff(rollout(history+(alternative,)),alternative)
        checks+=1
path=rollout(())
W=sum(z['multiplicity'] for z in customers if any(a in z['topics'] for a in path))
u=payoff(path,path[-1])
P=sum((F(z['multiplicity'],sum(a in z['topics'] for a in path[:-1])+1)
       for z in customers if any(a in z['topics'] for a in path)),F())
assert m*u-W-P==F(3,5)
print(json.dumps({'source':str(source),'m':m,'path':path,'histories':len(strategy),
                 'IC_checks':checks,'W':W,'u_last':str(u),'P':str(P),
                 'm_u_last_minus_W_minus_P':str(m*u-W-P)},indent=2))
