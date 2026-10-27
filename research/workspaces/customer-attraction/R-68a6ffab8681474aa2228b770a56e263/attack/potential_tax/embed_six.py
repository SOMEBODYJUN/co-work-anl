"""Construct, not verify, a full six-player SPE embedding of the ESM failure."""
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(Path(__file__).resolve().parents[6]))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver

d=json.loads((HERE/'esm_exact_obstruction.json').read_text())
inst=Instance(tuple(d['topics'])+('F',),tuple(CustomerType(frozenset(t['topics']),t['multiplicity'])
    for t in d['customers'])+(CustomerType(frozenset({5}),510),),6)
path=(5,5,5,0,1,2);solver=ExactSPESolver(inst);cert=solver.certificate(on_path=path)
packet={'claim':'Six-player actual-prefix ESM failure, auxiliary only',
        'scope':'full six-player ordered-history pure SPE; ESM fails at actual fourth node; not a half counterexample',
        'instance':inst.to_dict(),'strategy':cert.to_dict()['actions'],'actual_path':path,
        'examined_prefix':[5,5,5],'examined_action':0,'remaining':3,
        'original_three_player_packet':'esm_exact_obstruction.json'}
(HERE/'six_esm_embedding.json').write_text(json.dumps(packet,separators=(',',':'))+'\n')
print('constructed',len(cert.actions),'ordered decision histories')
