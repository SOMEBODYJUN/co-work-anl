#!/usr/bin/env python3
"""Build one explicit four-player SPE; verification is a separate script.

This uses the repository's exact outcome oracle only to produce a complete
ordered strategy. The final assertion is not delegated to this constructor.
"""
from pathlib import Path
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType,ExactSPESolver

base=Instance.from_dict(json.loads((ROOT/"examples/customer_attraction/individual_security_failure.json").read_text()))
ins=Instance(base.topics+("P",),base.customers+(CustomerType(frozenset({6}),19),),4)
sol=ExactSPESolver(ins)
cert=sol.certificate(on_path=(6,0,3,4))
(HERE/"endogenous_53_instance.json").write_text(json.dumps(ins.to_dict(),indent=2)+"\n")
(HERE/"endogenous_53_strategy.json").write_text(json.dumps(cert.to_dict(),indent=2)+"\n")
print(json.dumps({"players":4,"topics":7,"customers":ins.customer_count,
                  "ordered_decision_histories":len(cert.actions),"path":[6,0,3,4],
                  "construction_scope":"exact oracle constructs a full strategy; see independent audit for proof"},indent=2))
