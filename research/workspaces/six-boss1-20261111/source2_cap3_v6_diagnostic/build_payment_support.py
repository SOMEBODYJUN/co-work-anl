#!/usr/bin/env python3
"""Expand only literal positive v6 payments supported by this own source proof."""
from pathlib import Path
from fractions import Fraction as F
import json

P=Path(__file__).resolve().parent
records=json.loads((P/"point_slacks_all585.json").read_text())["rows"]
out=[]
for rec in records:
    row=rec["metadata"]
    for match in rec["literal_input_row_matches"]:
        y=F(match["actual_raw_dual_weight"])
        if not y: continue
        assert y>0 and F(rec["slack"])==0
        budget=row["real_budget"]
        tau={j:F(w) for j,w in budget["internal_SAFE"].items()}
        caps={j:F(w) for j,w in budget["intermediate_CAP"].items()}
        out.append(dict(row_id=row["id"],source_vertex=row["vertex_key"],delta=row["delta"],h=row["h"],s=row["s"],
            raw_index=match["raw_index"],raw_name=match["name"],actual_raw_dual_weight=str(y),
            source_IC_weight=str(y*F(budget["source_IC"])),
            intermediate_CAP_weights={j:str(y*w) for j,w in caps.items()},
            terminal_CAP_weight=str(y*F(budget["terminal_CAP"])),
            terminal_BR_average_weight=str(y*F(budget["terminal_BR"])),
            terminal_BR_per_query_index_weight=str(y*F(budget["terminal_BR"])/6),
            internal_SAFE_average_weights={j:str(y*w) for j,w in tau.items()},
            internal_SAFE_per_query_index_weights={j:str(y*w/6) for j,w in tau.items()},
            signed_free_EC_weight=str(y*F(row["free_EC"])),
            final_independent_K_weight=str(y*F(row["K"])),
            zero_weight_SAFE_indices=[j for j,w in tau.items() if not w],
            numerical_divisor_applied=False,
            scope="These are true original-scale payments for this source; free EC is signed and no zero-weight term acquires an equality obligation."))
assert [r["raw_index"] for r in out]==[4012,4067,4107]
(P/"positive_true_payment_support.json").write_text(json.dumps(dict(count=3,records=out),ensure_ascii=False,indent=2)+"\n")
print("PASS: expanded original-scale true payments for raw 4012, 4067, 4107")
