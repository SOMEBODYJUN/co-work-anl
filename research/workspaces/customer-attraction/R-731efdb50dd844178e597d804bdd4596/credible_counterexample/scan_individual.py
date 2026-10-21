import json
from pathlib import Path
from customer_attraction import Instance,ExactSPESolver
for p in Path('examples/customer_attraction').glob('*.json'):
 try:i=Instance.from_dict(json.loads(p.read_text()))
 except (ValueError,KeyError,TypeError):continue
 if i.players>6 or i.topic_count>7:continue
 s=ExactSPESolver(i);o=i.optimal_welfare()
 for q in s.outcomes():
  u=min(i.topic_payoff(a,q) for a,n in enumerate(q) if n)
  if 2*i.players*u<o:print(p,q,u,o,flush=True)
