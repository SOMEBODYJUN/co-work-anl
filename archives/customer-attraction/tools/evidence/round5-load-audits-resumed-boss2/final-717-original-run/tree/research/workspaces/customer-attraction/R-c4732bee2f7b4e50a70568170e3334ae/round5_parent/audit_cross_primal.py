"""Independent literal reconstruction of all717 necessary-condition rows.

Only earlier reviewed437/120 row auditors are reused. No discovery pricing
module or compact cross-cost calculator is imported. Cross rows are summed
over the actual three index positions, using any common-t preserving lift.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ACTOR = HERE.parent
path = ACTOR/'round4_parent/audit_full_primal.py'
spec = importlib.util.spec_from_file_location('earlier_parent_audit', path)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)


def states(atom, family):
    field, arity = {'AB':('AB_hist',3), 'AE':('AE_hist',3),
                    'Sbranch':('second_hist',4)}[family]
    return [s for s,n in zip(product((0,1),repeat=arity),atom[field]) for _ in range(n)]


def literal_cross(atom):
    bits = dict(zip('ABCDEUVWXY', map(int, atom['bits'])))
    rows = {}
    for source in ('AB','AE'):
        src = states(atom, source)
        base = bits['A']+bits['B' if source=='AB' else 'E']
        for target in ('AB','AE','Sbranch'):
            if source==target:
                continue
            tgt = states(atom, target)
            assert [s[0] for s in src]==[s[0] for s in tgt]
            k = len(tgt[0])
            for u in range(k):
                for v in range(u,k):
                    totals = dict.fromkeys(('all_equal','query_equal','first_branch',
                                           'second_branch','all_distinct'),F(0))
                    for i,s in enumerate(src):
                        p = base+s[0]
                        a,b = s[-2:]
                        H = (F(a+b,p+a+b) if a+b else F(0))+F(a,(p+1)*(p+2))
                        for j,t in enumerate(tgt):
                            for l,z in enumerate(tgt):
                                if i==j==l:
                                    orbit = 'all_equal'
                                elif j==l:
                                    orbit = 'query_equal'
                                elif i==j:
                                    orbit = 'first_branch'
                                elif i==l:
                                    orbit = 'second_branch'
                                else:
                                    orbit = 'all_distinct'
                                cost = F(t[u]+z[v],p+1)-F(t[u]*z[v],(p+1)*(p+2))
                                totals[orbit] += H-cost
                    for orbit,value in totals.items():
                        rows[f'crosspair:{source}:{target}:{u}{v}:{orbit}'] = value
    assert len(rows)==160
    return rows


def audit():
    source = ACTOR/'round5_pricing/exact_optimum_primal_cross_pair.json'
    cert = json.loads(source.read_text())
    evaluate = prior.old_evaluator()
    totals = dict.fromkeys(cert['slacks'],F(0))
    W=O=F(0)
    for atom in cert['atoms']:
        bits = tuple(map(int,atom['bits']))
        hs = [atom[k] for k in ('AB_hist','AE_hist','second_hist')]
        assert all(sum(h)==5 and all(type(x)is int and x>=0 for x in h) for h in hs)
        d = sum(hs[0][4:])
        assert d==sum(hs[1][4:])==sum(hs[2][8:])
        mass = F(atom['exact_mass'])
        assert mass>0
        rows = evaluate(bits,hs,atom['menus_lh'],True)
        rows.update(prior.literal_added(atom))
        rows.update(literal_cross(atom))
        assert len(rows)==717 and set(rows)==set(totals)
        for name,value in rows.items():
            totals[name] += mass*value
        W += mass*any(bits[:5])
        O += mass*(d>0)
    assert W==F(cert['welfare'])==1
    assert O==F(cert['comparison_cover'])>2
    assert all(totals[n]==F(cert['slacks'][n])>=0 for n in totals)
    return {'scope':'717-row exact primal feasibility only; no SPE completion/actualOPT or full-universe dual acceptance',
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'positive_atoms':len(cert['atoms']),'rows':717,
            'cross_rows_rebuilt_by_literal_triple_sums':160,
            'comparison_cover':str(O),'welfare':str(W),'ratio_float':float(O),
            'all_slacks_match':True,'minimum_slack':str(min(totals.values())),
            'zero_slacks':sum(v==0 for v in totals.values())}


if __name__=='__main__':
    report = audit()
    (HERE/'audit_cross_primal.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
