"""Project the already certified one-prefix five-tail tables; no optimization."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent


def part(n, d):
    return F(n, d) if n else F(0)


def main():
    pins = ['0e5ab5156e98eda9e967e8227e760c7181e77d4db78540aee8b367b1769861ed',
            'ece4ff20dfd3fc6f7a33c2efd6a7b4af4f21fb2089523a13517246746aabfa64']
    tables, source = {}, []
    for b in (0, 1):
        p = WS/'background_five_bridge'/f'fixed53_b{b}_profit.json'
        assert sha256(p.read_bytes()).hexdigest() == pins[b]
        d = json.loads(p.read_text())
        assert len(d['all_6144_conditional_residuals']) == 6144
        groups = {}
        for state in d['all_6144_conditional_residuals']:
            key = (state['bits'][:5], state['d'])
            groups.setdefault(key, []).append(F(state['rho']))
        for record in d['min_by_actual_and_d']:
            key = (record['actual'], record['d'])
            assert min(groups[key]) == F(record['min_rho'])
            assert len(groups[key]) == 32
            tables[(b,)+key] = F(record['min_rho'])
        source.append({'path': str(p.relative_to(WS)), 'sha256': pins[b]})
        assert F(d['K_residual']) == F(226487, 10**21)
    coefficients, records = {}, []
    for j, bits in enumerate(product((0, 1), repeat=8)):
        a, x, o = bits[:6], bits[6], bits[7]
        b, tail = a[0], ''.join(map(str,a[1:]))
        choices = []
        for six_d in (range(1,7) if o else (0,)):
            h = F(0)
            if six_d < 6:
                h += F(6-six_d,6)*(part(six_d,b+six_d)+tables[(b,tail,six_d)])
            if six_d:
                h += F(six_d,6)*(part(six_d-1,b+six_d-1)+tables[(b,tail,six_d-1)])
            choices.append((six_d,h))
        m = min(value for _,value in choices)
        coefficient = 2*part(sum(a[1:]),sum(a))-m
        coefficients[str(j)] = str(coefficient)
        records.append({'index':j,'bits':list(bits),'minimum':str(m),
                        'attaining_d':[k for k,v in choices if v==m],
                        'all_allowed_d':{str(k):str(v) for k,v in choices}})
    coefficients['256'] = str(-F(226487,10**21))
    evaluations = {}
    for name in ['universal_union_wallet_lp','universal_union_wallet_v2','universal_union_wallet_v3','universal_union_wallet_v4']:
        p=WS/name/'exact_certificate.json'
        if not p.exists(): continue
        point=json.loads(p.read_text())['primal']
        value=sum((F(c)*F(point.get(j,0)) for j,c in coefficients.items()),F(0))
        evaluations[name]={'value':str(value),'decimal':float(value),'certificate_sha256':sha256(p.read_bytes()).hexdigest()}
    result={'status':'PASS_EXACT_PROJECTION_OF_FROZEN_TABLES','optimizer_calls':0,
            'scope':'Inherited full-domain 53-weight one-prefix profit certificate; six legal comparison labels averaged over deletions, actual history only.',
            'new_original_oracle_execution':False,'source_pins':source,'conditional_table_entries_checked':12288,
            'all256_d_minima':records,'all257_coefficients':coefficients,'point_evaluations':evaluations,
            'warning':'The domain proof and original 53-budget payment are inherited from the registered parent; no claim of newly recomputing its large oracle.'}
    (HERE/'exact_projection.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'evaluations':evaluations},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
