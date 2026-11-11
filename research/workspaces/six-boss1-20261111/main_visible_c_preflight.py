"""Main's independent full-column transcription check; no optimizer."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json

W = Path(__file__).resolve().parent
P = W / 'visible_maximum_joint'


def load(p):
    return json.loads(p.read_text())


def main():
    out = W / 'main_visible_c_preflight.json'
    assert not out.exists()
    raw = (P / 'exact_input.json').read_bytes()
    assert sha256(raw).hexdigest() == 'b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33'
    inp = json.loads(raw)
    manifest = load(P / 'freeze_manifest.json')
    for path, pin in manifest['artifacts'].items():
        assert sha256((P / path).read_bytes()).hexdigest() == pin['sha256'], path
    old = load(W / 'universal_union_wallet_v6/exact_input.json')
    rows, previous = inp['raw_rows'], old['raw_rows']
    assert len(rows) == 1002 and len(previous) == 867 and inp['variables'] == 513
    for r, s in zip(rows, previous):
        assert {k:v for k,v in r.items() if k != 'a'} == {k:v for k,v in s.items() if k != 'a'}
        expected = {}
        for key, value in s['a'].items():
            j = int(key)
            if j == 256:
                expected['512'] = value
            else:
                expected[str(2*j)] = value
                expected[str(2*j+1)] = value
        assert expected == r['a'], r['name']
    for col in range(513):
        if col < 512:
            bits = tuple((col >> k) & 1 for k in range(8, -1, -1))
            a, x, o, c = bits[:6], bits[6], bits[7], bits[8]
            total, p4 = sum(a), sum(a[:4])
            u = [F(v, total) if total else F(0) for v in a]
            D = p4 + 1
            val = {'A'+str(i+1):F(v) for i,v in enumerate(a)}
            val.update(X=F(x), C=F(c), Omean=F(o, 6))
        for idx, r in enumerate(rows[867:], 867):
            f = r['family']
            if col == 512:
                if idx == 867:
                    v = -F(117135582158121, 1145925867755340)
                elif idx == 868:
                    v = -F(1767904008200582, 16877573861922720)
                elif f == 'VISIBLE_C_PORTFOLIO25':
                    v = F(7-r['source'], 2)
                elif idx == 1001:
                    v = F(1)
                else:
                    v = F(0)
            elif idx in (867, 868):
                beta = F(23074097917720, 1145925867755340) if idx == 867 else F(337340181272013, 16877573861922720)
                v = u[0] - beta*o
            elif f == 'VISIBLE_C_SAFE':
                i = r['source']-1
                v = u[i]-F(c, sum(a[:i])+6-i)
            elif f == 'VISIBLE_C_FMAX':
                v = F(x-c, D)
            elif f == 'VISIBLE_C_MX':
                v = u[4]-F(c, D+x)
            elif f in ('VISIBLE_C_RC', 'VISIBLE_C_PAIR'):
                q = val[r['right']]
                cost = F(c, D)+q/D-c*q/(D*(D+1))
                wallet = u[4]+F(x,D) if f == 'VISIBLE_C_RC' else u[4]+u[5]+F(a[4],D*(D+1))
                v = wallet-cost
            elif f == 'VISIBLE_C_PORTFOLIO25':
                i = r['source']-1
                n, p = 5-i, sum(a[:i])
                A, B = F(n+1,2)+F(24,p+n+1), F(1,p+1)
                E = F(n,(p+1)*(p+n+1))
                t, q = val[r['T']], val[r['Q']]
                assert not (r['T'] == r['Q'] == 'Omean')
                v = 25*u[i]-(A*t+B*q-E*t*q)
            elif f == 'VISIBLE_C_OPT6':
                v = -F(any(val[q] for q in r['labels']))
            elif idx == 1001:
                v = -F(o,6)
            else:
                raise AssertionError((idx,f))
            assert F(r['a'].get(str(col),'0')) == v, (r['name'],col)
        expected_obj = int(any(a)) if col < 512 else 0
        assert F(inp['objective'].get(str(col),'0')) == expected_obj
        for j, eq in enumerate(inp['equalities']):
            v = (o if j == 0 else c) if col < 512 else (0 if j == 0 else -1)
            assert F(eq['a'].get(str(col),'0')) == v
    assert [e['rhs'] for e in inp['equalities']] == ['1','0']
    scales = load(P / 'numerical_scaling.json')['raw_scales']
    assert all(F(scales[r['name']]) > 0 for r in rows)
    result = dict(status='PASS_MAIN_FULL_1002_INPUT_REPLAY', input_sha256=sha256(raw).hexdigest(),
                  old_raw_rows_literal=867, new_independent_column_entries=135*513,
                  all_columns=513, equalities=2, frozen_artifacts_unchanged=True, optimizer_calls=0,
                  sources_read='Complete source_review and real-payment formulas read by Main; roots separately checked in root270 bridge and CAP4 certificates.')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))


if __name__ == '__main__':
    main()
