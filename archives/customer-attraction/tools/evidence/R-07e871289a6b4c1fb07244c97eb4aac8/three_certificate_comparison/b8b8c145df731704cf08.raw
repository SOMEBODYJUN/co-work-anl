"""Add the proved same-source requery to the saved m=6 necessary-row system.
Rational primal/dual certificates are checked; the systems are relaxations.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys
from stress_nested_on_old_relaxation import phi,ROOT
WORK=ROOT/'research/workspaces/customer-attraction/R-07e871289a6b4c1fb07244c97eb4aac8/general_from_half5'
sys.path.insert(0,str(WORK))
from six_copy_refine import bridge_system,parametric_row,add_query_family,solve_exact_system,verify


def system():
    types,rows=bridge_system(6)
    old=json.loads((WORK/'six_copy_free_results.json').read_text())
    for c in old['cuts']:
        c={k:v for k,v in c.items() if k!='separation_slack'}
        rows.append(parametric_row(types,6,c))
    assert len(rows)==387
    def psi(a,t,q):return -F(2,7)*phi(sum(a[:3]),sum(a[:-1]),t,q)
    add_query_family(rows,types,6,'nested-same-source-requery',3,psi,F(1,42),((5,F(4,21)),))
    return types,rows

if __name__=='__main__':
    types,rows=system();target=Path(__file__).with_suffix('.json')
    if '--verify' in sys.argv:
        data=json.loads(target.read_text());verify(data,types,rows)
        print('EXACT VERIFIED',data['W'],len(types),'types',len(rows),'rows; relaxation only')
    else:
        data,_=solve_exact_system(6,types,rows)
        data['scope']='Exact necessary-row relaxation; not SPE or a six-provider half proof'
        data['source']='User-pasted 60-row proof local same-source requery; independently reconstructed for any m with three players remaining'
        target.write_text(json.dumps(data,indent=2)+'\n')
        print({k:data[k] for k in ['W','O','K','n_rows','dual_min_residual']})
