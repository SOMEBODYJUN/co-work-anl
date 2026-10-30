"""Exact original-point root-saturation and directed-difference evidence."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
ROOT=Path(__file__).resolve().parents[5]
source=ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
p=json.loads(source.read_text())['primal'];D=p['denominator'];atoms=p['atoms'];rs=[F(a['mass_numerator'],D) for a in atoms];bs=[list(map(int,a['bits'])) for a in atoms]
size=lambda j:sum((r*b[j] for b,r in zip(bs,rs)),F(0))
diff=lambda j,k:sum((r*b[j]*(1-b[k]) for b,r in zip(bs,rs)),F(0))
r=sum((mass*F(b[0],sum(b[:5])) for b,mass in zip(bs,rs) if b[0]),F(0))
assert size(2)==size(3)==5*r
assert diff(2,3)==diff(3,2)>0
report={'scope':'exact non-completability obstruction of the published 437-row primal under any catalog extension preserving its original theme memberships and multiplicities','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'root_actual_payoff':str(r),'C_size':str(size(2)),'D_size':str(size(3)),'C_minus_D':str(diff(2,3)),'D_minus_C':str(diff(3,2)),'C_intersect_D':str(size(2)-diff(2,3)),'C_D_equal_size':True,'C_size_equals_5_root_payoff':True,'minimum_gap_root_payoff_for_C_D_to_coexist_if_they_are_global_maxima':str(diff(3,2)/20),'new_arbitrary_pair_C_D_row_violation':str(-8*diff(3,2))}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
