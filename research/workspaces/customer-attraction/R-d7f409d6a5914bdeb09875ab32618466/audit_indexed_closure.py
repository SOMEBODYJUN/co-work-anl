"""Independent exact acceptance of the 447-row template witness.

No optimization or recovery code is imported. The established 437-row account
is reused verbatim; the ten newly required common-catalog rows are reconstructed
from ordered pairs of distinct indices, independently of the search routine.
This proves a finite relaxation obstruction, never existence of a real SPE.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
SOURCE=ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
WITNESS=HERE/'credible_counterexample/frozen_support_closure.json'


def main():
    row_code=(ROOT/'tests/audits/customer_attraction_five_indexed.py').read_text()
    established={}
    exec(row_code.split('\nfrom pathlib import Path\nfrom collections')[0],established)
    atoms=json.loads(SOURCE.read_text())['primal']['atoms']
    record=json.loads(WITNESS.read_text())
    masses=list(map(F,record['exact_reweighting']))
    assert len(atoms)==len(masses)==64 and min(masses)>=0
    totals={};W=F(0);O=F(0);new_names=set()
    for atom,mass in zip(atoms,masses):
        bits=tuple(map(int,atom['bits']));b=dict(zip('ABCDEUVWXY',bits))
        rows=established['evaluate'](bits,[atom[f] for f in ('AB_hist','AE_hist','second_hist')],atom['menus_lh'],include_second_correlations=True)
        assert len(rows)==437
        for family,field,dim,prefix in [('AB','AB_hist',3,b['A']+b['B']),('AE','AE_hist',3,b['A']+b['E']),('Sbranch','second_hist',4,b['A'])]:
            cells=[ty for ty,n in zip(product((0,1),repeat=dim),atom[field]) for _ in range(n)]
            assert len(cells)==5
            for pos in range(dim):
                name=f'{family}:5:offdiag:{pos}'
                assert name not in rows
                new_names.add(name)
                # At branch i, final mover compares its own reply against menu
                # coordinate pos of every other branch j. The denominator is
                # unchanged because the final mover is replaced by the query.
                rows[name]=sum((F(cells[i][-1]-cells[j][pos],prefix+sum(cells[i][:-1])+1)
                                for i in range(5) for j in range(5) if i!=j),F(0))
        assert len(rows)==447
        for name,v in rows.items():totals[name]=totals.get(name,F(0))+mass*v
        W+=mass*int(any(bits[:5]))
        O+=mass*int(any(ty[0] and n for ty,n in zip(product((0,1),repeat=3),atom['AB_hist'])))
    assert len(new_names)==10 and len(totals)==447
    assert W==1 and O==F(record['exact_primal_value']) and O>2
    assert min(totals.values())>=0
    # Reverse checks of both the stated ratio and its strict excess.
    excess=O-2*W
    assert O==2*W+excess and excess>0
    report={'claim':'B9-INDEXED-447-ROWS-NOT-HALF-v1','status':'exact finite relaxation obstruction; no real SPE asserted',
            'atoms':len(atoms),'nonzero_masses':sum(x>0 for x in masses),'old_rows':437,'new_rows':len(new_names),'all_rows':len(totals),
            'W':str(W),'O':str(O),'O_minus_2W':str(excess),'minimum_slack':str(min(totals.values())),
            'new_row_totals':{n:str(totals[n]) for n in sorted(new_names)},
            'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'witness_sha256':hashlib.sha256(WITNESS.read_bytes()).hexdigest(),
            'optimality_claimed':False}
    target=HERE/'audit_indexed_closure.json'
    if target.exists():raise FileExistsError(target)
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
