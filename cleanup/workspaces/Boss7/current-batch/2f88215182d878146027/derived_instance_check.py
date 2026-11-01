from fractions import Fraction
from itertools import product
import json
p=5
types=[{1},{0,2},{3},{4}]
rho=(1,2,1,2,0)
actual=(4,0)
def payoff(path,player):
    a=path[player]
    val=Fraction(0)
    for B in types:
        if a in B:
            den=sum(int(t in B) for t in path)
            val += Fraction(1,den)
    return val
root_payoff=payoff(actual,0)
root_rows=[]
for a in range(p):
    path=(a,rho[a])
    root_rows.append({'first':a,'path':path,'root_payoff':str(payoff(path,0)),'difference':str(root_payoff-payoff(path,0))})
reply_rows=[]
for a in range(p):
    prescribed=(a,rho[a])
    prescribed_payoff=payoff(prescribed,1)
    for b in range(p):
        reply_rows.append({'first':a,'deviation':b,'difference':str(prescribed_payoff-payoff((a,b),1))})
def covered(pair,B):return bool(set(pair)&B)
values=[]
for pair in product(range(p),repeat=2):
    values.append((sum(covered(pair,B) for B in types),pair))
opt=max(v for v,_ in values)
result={'customers':[sorted(B) for B in types],'actual_path':list(actual),'actual_player_payoffs':[str(payoff(actual,i)) for i in range(2)],'W':str(sum(1 for B in types if set(actual)&B)),'root_rows':root_rows,'reply_rows':reply_rows,'minimum_root_slack':str(min(Fraction(x['difference']) for x in root_rows)),'minimum_reply_slack':str(min(Fraction(x['difference']) for x in reply_rows)),'OPT_over_ordered_pairs':opt,'optimal_pairs':[list(pair) for v,pair in values if v==opt],'ratio_W_over_OPT':str(Fraction(2,opt))}
open('cleanup/workspaces/Boss7/current-batch/2f88215182d878146027/derived_instance_check.json','w').write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
