from itertools import product
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,StrategyCertificate,verify_certificate
from markov_probe import inc,count_states

def witness(inst,target):
 k=inst.topic_count;states=count_states(k,2)
 menus=[]
 for q in states:
  values=[inst.topic_payoff(a,inc(q,a)) for a in range(k)]
  menus.append(tuple(a for a,v in enumerate(values) if v==max(values)))
 for last in product(*menus):
  lp=dict(zip(states,last));children=[]
  for first in range(k):
   p=tuple(int(i==first) for i in range(k))
   terminals=[inc(inc(p,a),lp[inc(p,a)]) for a in range(k)]
   values=[inst.topic_payoff(a,q) for a,q in enumerate(terminals)]
   children.append(tuple((a,q) for a,q,v in zip(range(k),terminals,values) if v==max(values)))
  floor=max(min(inst.topic_payoff(a,q) for b,q in child) for a,child in enumerate(children))
  for first,child in enumerate(children):
   for second,q in child:
    if q!=target or inst.topic_payoff(first,target)<floor:continue
    sp={a:min(child,key=lambda bq:inst.topic_payoff(a,bq[1]))[0] for a,child in enumerate(children)}
    sp[first]=second
    actions={():first}
    for a in range(k):
     actions[(a,)]=sp[a]
     for b in range(k):actions[(a,b)]=lp[inst.counts((a,b))]
    cert=StrategyCertificate(actions,target);verify_certificate(inst,cert).assert_valid()
    return cert,lp
 raise ValueError('no witness')
if __name__=='__main__':
 data=json.loads((ROOT/'research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/boss/pne_bridge_certificate.json').read_text())
 inst=Instance.from_dict(data['instance']);target=tuple(data['certificate']['terminal_counts'])
 cert,lp=witness(inst,target)
 out={'instance':inst.to_dict(),'terminal_counts':target,'certificate':cert.to_dict(),'last_by_counts':[{ 'counts':q,'action':a} for q,a in lp.items()]}
 Path(__file__).with_name('boss_markov_alternative.json').write_text(json.dumps(out,indent=2))
 print(json.dumps(out,indent=2))
