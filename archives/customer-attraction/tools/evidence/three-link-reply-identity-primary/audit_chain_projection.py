"""Definition-level audit; does not import the author's implementation."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def share(bit, load):
    if bit == 0:
        return Q(0)
    assert load > 0
    return Q(1, load)


def coefficients(past, last_past, bits):
    t = bits[:3]
    b = bits[3:6]
    y = bits[6:]
    pay_source = [share(t[q], past+t[q]+b[q]+y[q]) for q in range(3)]
    pay_last = [share(y[q], past+t[q]+b[q]+y[q]) for q in range(3)]
    queries = [share(b[q], past+t[q+1]+b[q+1]+b[q]) for q in range(2)]
    # These are the customer coefficients in the eleven nonnegative rows:
    # 3 source ICs, 2 last-response ICs, 3 actual-last ICs, 3 capacities.
    rows = [-v for v in pay_source]
    rows += [pay_last[q+1]-queries[q] for q in range(2)]
    rows += [-share(y[q], last_past+1) for q in range(3)]
    rows += [-Q(y[q]) for q in range(3)]
    weights = (1,3,2,4,1,1,1,1,1,1,1)
    residual = -sum((a*z for a,z in zip(weights,rows)), Q(0))
    explicit = sum((Q(w)*pay_source[q] for q,w in enumerate((1,3,2))),Q(0))
    explicit += sum((share(y[q],last_past+1)+y[q] for q in range(3)),Q(0))
    explicit += 4*(queries[0]-pay_last[1])+(queries[1]-pay_last[2])
    assert explicit == residual
    return residual


def main():
    report = json.loads((ROOT/'original'/'chain_L3_exact.json').read_text())
    assert report['L'] == 3
    assert report['lambda'] == ['1','3','2']
    assert report['eta'] == ['4','1']
    assert report['alpha'] == report['beta'] == ['1','1','1']
    rows = []
    evals = 0
    for old in report['rows']:
        p, ell = old['p'], old['ell']
        linked, free = [], []
        for bits in product((0,1), repeat=9):
            value = coefficients(p,ell,bits)
            evals += 1
            free.append((value,bits))
            if bits[1] == bits[6] and bits[2] == bits[7]:
                linked.append((value,bits))
        lval, larg = min(linked,key=lambda z:z[0])
        fval, farg = min(free,key=lambda z:z[0])
        as_arg = lambda bits: [list(bits[:3]),list(bits[3:6]),list(bits[6:])]
        assert len(linked)==old['linked_states']==128
        assert len(free)==old['free_states']==512
        assert str(lval)==old['linked_min'] and str(fval)==old['free_min']
        assert as_arg(larg)==old['linked_arg'] and as_arg(farg)==old['free_arg']
        assert str(lval-fval)==old['identity_gain']
        reachable = 0 <= ell-p <= 2
        rows.append(dict(p=p,ell=ell,linked_min=str(lval),free_min=str(fval),
                         identity_gain=str(lval-fval),
                         reference_path_reachable=reachable))
    assert len(rows)==18
    real = [r for r in rows if r['reference_path_reachable']]
    assert len(real)==12
    result = dict(scope='local necessary projection; no game or SPE construction',
                  original_rows=18, original_linked_states_per_row=128,
                  original_free_states_per_row=512,
                  independently_checked_row_decompositions=evals,
                  reference_path_rows=len(real),
                  strict_identity_rows=sum(Q(r['identity_gain'])>0 for r in rows),
                  reference_path_strict_identity_rows=sum(Q(r['identity_gain'])>0 for r in real),
                  reference_path_negative_linked_min_rows=sum(Q(r['linked_min'])<0 for r in real),
                  rows=rows)
    (ROOT/'audit-output.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))


if __name__ == '__main__':
    main()
