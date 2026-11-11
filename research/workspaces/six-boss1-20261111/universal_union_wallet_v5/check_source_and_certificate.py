#!/usr/bin/env python3
"""Independent Fraction replay of released sources and optional v5 certificate.

No optimizer; no builder imports; writes only this package's check reports.
The original fixed53 enlarged-domain oracle is inherited, not rerun here.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
from math import lcm
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
N = 257

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return sha256(path.read_bytes()).hexdigest()

def save(name, value):
    (HERE/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def vec(row):
    return [F(row.get(str(j), '0')) for j in range(N)]

def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))

def share(numerator, denominator):
    assert denominator or not numerator
    return F(numerator, denominator) if denominator else F(0)

def minimum(p, n, t, q):
    return n*t + F(30*t, p+n+1) + F(q, p+1+n*t)

def phi(p, n, t, q, tails):
    s, z = sum(tails[:-1]), tails[-1]
    return share(31*t-z, p+t+s+z) + s+z + F(q, p+t+s+1)

def mean_cost(p, n, t, q, o):
    """None denotes menu averaging, never a legal synthetic action."""
    D = p+n+1
    if t is not None and q is not None:
        return minimum(p, n, t, q)
    if t is not None:
        return n*t + F(30*t, D) + F(o, 6*(p+1+n*t))
    if q is not None:
        return F(q, p+1) + F(o, 6)*(n+F(30, D)-F(n*q, (p+1)*D))
    return o*(F(n, 6)+F(5, D)+F(1, 6*(p+1)))

def main():
    inp = read(HERE/'exact_input.json')
    release = read(HERE/'main_release.json')
    assert release['authorized_by'] == '/root'
    assert release['status'] == 'MAIN_EXPLICIT_546_ROW_RELEASE'
    assert release['optimizer_calls_authorized'] == 1
    assert inp['v5_main_release_sha256'] == sha(HERE/'main_release.json')
    assert inp['v5_source_sha256'] == release['source_sha256']
    for name, digest in release['source_sha256'].items():
        assert sha(WS/name) == digest, name
    oldpins = read(HERE/'prior_frozen_hashes.json')
    for name, digest in oldpins.items():
        assert sha(WS/name) == digest, name
    owner = read(HERE/'background_owner_pin.json')
    assert sha(REPO/owner['path']) == owner['sha256']
    baseline = read(WS/'universal_union_wallet_v4/exact_input.json')
    oldcert = read(WS/'universal_union_wallet_v4/exact_certificate.json')
    assert oldcert['input_sha256'] == sha(WS/'universal_union_wallet_v4/exact_input.json')
    assert inp['raw_rows'][:225] == baseline['raw_rows']
    assert len(inp['raw_rows']) == inp['raw_inequality_count'] == 546
    assert inp['variables'] == 257 and inp['K_column'] == 256
    assert inp['nonnegative_columns'] == list(range(257))
    for field in ['objective','equality','atom_columns','inequality_convention']:
        assert inp[field] == baseline[field], field
    atoms = inp['atom_columns']
    for j, bits in enumerate(product((0, 1), repeat=8)):
        assert atoms[j] == {'index':j, 'a':list(bits[:6]), 'x':bits[6], 'o':bits[7]}
    assert len(atoms) == 256
    objective, eq = vec(inp['objective']), vec(inp['equality']['a'])
    assert objective == [F(bool(sum(r['a']))) for r in atoms]+[F(0)]
    assert eq == [F(r['o']) for r in atoms]+[F(0)]
    assert F(inp['equality']['rhs']) == 1

    # Literal same-branch IC31 + n size caps + true-terminal BR.
    family = read(WS/'main_all_source31_family/exact_family.json')
    states = minima = menu_count = mixed_count = 0
    literal_minima = []
    for i in range(1, 6):
        n = 6-i
        for p in range(i):
            for t, q in product((0,1), repeat=2):
                values = [phi(p,n,t,q,tails) for tails in product((0,1), repeat=n)]
                states += len(values)
                target = minimum(p,n,t,q)
                assert min(values) == target
                assert all(v >= target for v in values)
                minima += 1
                literal_minima.append({'i':i,'p':p,'t':t,'q':q,'minimum':str(target)})
            for menu in product((0,1), repeat=6):
                d, o = sum(menu), int(any(menu))
                exact = sum((minimum(p,n,menu[k],menu[l]) for k in range(6) for l in range(6) if k != l), F(0))/30
                h = F(d,6)*(n+F(30,p+n+1)+F(1,p+1))-F(n*d*(d-1),30*(p+1)*(p+n+1))
                assert exact == h and exact >= mean_cost(p,n,None,None,o)
                menu_count += 1
                for bit in (0,1):
                    pure_t = sum((minimum(p,n,bit,q) for q in menu), F(0))/6
                    pure_q = sum((minimum(p,n,t,bit) for t in menu), F(0))/6
                    assert pure_t >= mean_cost(p,n,bit,None,o)
                    assert pure_q >= mean_cost(p,n,None,bit,o)
                    mixed_count += 2
    assert (states,minima,menu_count,mixed_count) == (456,60,960,3840)
    assert literal_minima == family['all_minima']
    assert len(family['rows']) == 320
    assert inp['raw_rows'][225:545] == family['rows']
    for offset, (i,T,Q) in enumerate(product(range(1,6), range(1,9), range(1,9))):
        row = inp['raw_rows'][225+offset]
        assert (row['source'],row['T'],row['Q']) == (i,T,Q)
        assert row['name'] == f'PORTFOLIO31_i{i}_T{T}_Q{Q}'
        assert F(row['rhs']) == 0 and F(row['numerical_divisor']) == 31
        expect = []
        for r in atoms:
            a = r['a']; roles = a+[r['x']]
            p, n = sum(a[:i-1]), 6-i
            t = roles[T-1] if T < 8 else None
            q = roles[Q-1] if Q < 8 else None
            expect.append(31*share(a[i-1],sum(a))-mean_cost(p,n,t,q,r['o']))
        expect.append(F(6-i))
        assert vec(row['a']) == expect, row['name']

    # Replay all saved conditional residuals. This is not the large original oracle.
    kappa = F(226487,10**21)
    table_minima = {}
    conditional_count = 0
    for b in (0,1):
        table = read(WS/f'background_five_bridge/fixed53_b{b}_profit.json')
        assert F(table['K_residual']) == kappa
        entries = table['all_6144_conditional_residuals']
        assert len(entries) == 6144
        grouped = {}
        seen = set()
        for e in entries:
            bits, d, rho = e['bits'], e['d'], F(e['rho'])
            assert len(bits) == 10 and set(bits) <= {'0','1'} and 0 <= d <= 5
            assert (bits,d) not in seen
            seen.add((bits,d))
            grouped.setdefault((bits[:5],d), []).append(rho)
            conditional_count += 1
        expected_keys = {(''.join(map(str,a)),d) for a in product((0,1),repeat=5) for d in range(6)}
        assert set(grouped) == expected_keys and all(len(v)==32 for v in grouped.values())
        saved = {(e['actual'],e['d']):F(e['min_rho']) for e in table['min_by_actual_and_d']}
        assert set(saved) == expected_keys and len(table['min_by_actual_and_d']) == 192
        for key, values in grouped.items():
            assert min(values) == saved[key]
            table_minima[(b,)+key] = min(values)
    assert conditional_count == 12288
    projection = read(WS/'main_background_projection/exact_projection.json')
    bgvec = []
    details = []
    for r in atoms:
        a, o = r['a'], r['o']
        b, tail = a[0], ''.join(map(str,a[1:]))
        choices = {}
        for d in (range(1,7) if o else (0,)):
            g = F(0)
            if d < 6:
                g += F(6-d,6)*(share(d,b+d)+table_minima[(b,tail,d)])
            if d > 0:
                g += F(d,6)*(share(d-1,b+d-1)+table_minima[(b,tail,d-1)])
            choices[d] = g
        lower = min(choices.values())
        bgvec.append(2*share(sum(a[1:]),sum(a))-lower)
        details.append({'index':r['index'],'bits':a+[r['x'],r['o']], 'minimum':str(lower),
                        'attaining_d':[d for d,v in choices.items() if v==lower],
                        'all_allowed_d':{str(d):str(v) for d,v in choices.items()}})
    bgvec.append(-kappa)
    assert details == projection['all256_d_minima']
    assert vec(projection['all257_coefficients']) == bgvec
    bgrow = inp['raw_rows'][545]
    assert bgrow['name'] == 'BG5_ACTUAL_SIX_DELETION_PROJECTION'
    assert F(bgrow['rhs']) == 0 and F(bgrow['numerical_divisor']) == 1
    assert vec(bgrow['a']) == bgvec and bgvec[256] < 0

    # Zero/exact-duplicate removal only, with an explicit raw-to-unique map.
    seen = {}; unique = []; mapping = []; zero = []; duplicate = []
    for k,row in enumerate(inp['raw_rows']):
        key = (tuple(vec(row['a'])),F(row['rhs']))
        if not any(key[0]) and key[1] == 0:
            zero.append(row['name'])
            mapping.append({'raw_index':k,'name':row['name'],'status':'zero','unique_index':None})
        elif key in seen:
            prev,uid = seen[key]
            duplicate.append({'name':row['name'],'identical_to':inp['raw_rows'][prev]['name']})
            mapping.append({'raw_index':k,'name':row['name'],'status':'duplicate','first_raw_index':prev,'unique_index':uid})
        else:
            uid = len(unique); seen[key] = (k,uid); unique.append(row)
            mapping.append({'raw_index':k,'name':row['name'],'status':'kept','unique_index':uid})
    assert unique == inp['unique_rows'] and len(unique) == inp['unique_inequality_count'] == 533
    assert zero == inp['removed_zero_rows'] and duplicate == inp['removed_exact_duplicate_rows']
    assert mapping == read(HERE/'duplicate_mapping.json')
    scales = read(HERE/'numerical_scaling.json')['scales']
    assert set(scales) == {r['name'] for r in unique}
    for row in unique:
        expected = F(row['numerical_divisor']) if 'numerical_divisor' in row else max([F(1),abs(F(row['rhs']))]+[abs(v) for v in vec(row['a'])])
        assert F(scales[row['name']]) == expected and expected > 0

    # Old feasible dual extends by zero weights to all new rows.
    oldz = vec(oldcert['primal'])
    assert all(v >= 0 for v in oldz) and dot(eq,oldz) == 1
    for row in baseline['raw_rows']:
        assert dot(vec(row['a']),oldz)-F(row['rhs']) >= 0
    row_by_name = {row['name']:row for row in unique}
    weights = {name:F(v) for name,v in oldcert['dual']['row_weights'].items()}
    nu = F(oldcert['dual']['normalization_multiplier'])
    assert all(v >= 0 for v in weights.values())
    residual = [objective[j]-nu*eq[j]-sum(w*F(row_by_name[name]['a'].get(str(j),'0')) for name,w in weights.items()) for j in range(N)]
    assert all(v >= 0 for v in residual)
    assert residual == vec(oldcert['dual']['nonnegative_column_residual'])
    oldbound = nu+sum(w*F(row_by_name[name]['rhs']) for name,w in weights.items())
    assert oldbound == F(oldcert['objective']) == dot(objective,oldz)
    save('baseline_dual_extension.json', {'status':'PASS','objective':str(oldbound),'all257_columns_pass':257,
         'old_positive_weights':{n:str(w) for n,w in weights.items()},'new_row_weights':'all zero',
         'normalization_multiplier':str(nu),'all257_residuals':[str(v) for v in residual]})
    old_family_values = {r['name']:dot(vec(r['a']),oldz)-F(r['rhs']) for r in inp['raw_rows'][225:545]}
    old_bg = dot(bgvec,oldz)
    source_result = {'status':'PASS','optimizer_calls_by_checker':0,'input_sha256':sha(HERE/'exact_input.json'),
        'raw_rows':546,'unique_rows':533,'columns':257,'unchanged_old_raw_rows':225,'unchanged_frozen_files':len(oldpins),
        'source31_literal_states':states,'source31_minima':minima,'ordered_unequal_menu_cases':menu_count,
        'mixed_mean_cases':mixed_count,'family_coefficients_independently_rebuilt':320*257,
        'saved_background_conditional_entries':conditional_count,'background_columns_rebuilt':257,
        'background_K_coefficient':str(bgvec[256]),'background_original_oracle_rerun':False,
        'zero_rows':len(zero),'exact_duplicate_rows':len(duplicate),'all_positive_numerical_scalings':True,
        'old_bound_extended':str(oldbound),'negative_new_family_rows_at_old_point':sum(v<0 for v in old_family_values.values()),
        'background_value_at_old_point':str(old_bg),'source_sha256':release['source_sha256']}
    save('source_check.json',source_result)
    if not (HERE/'exact_certificate.json').exists():
        print(json.dumps(source_result,indent=2)); return

    cert = read(HERE/'exact_certificate.json')
    assert cert['input_sha256'] == sha(HERE/'exact_input.json') and cert['optimizer_calls'] == 1
    z = vec(cert['primal'])
    assert all(v>=0 for v in z) and dot(eq,z)==1
    rawslack = [dot(vec(row['a']),z)-F(row['rhs']) for row in inp['raw_rows']]
    assert all(v>=0 for v in rawslack)
    assert {row['name']:str(s) for row,s in zip(inp['raw_rows'],rawslack)} == cert['raw_row_slacks']
    W = dot(objective,z)
    assert W == F(cert['objective']) and W >= oldbound and F(cert['K']) == z[256]
    weights = {name:F(v) for name,v in cert['dual']['row_weights'].items()}
    assert all(v>0 for v in weights.values()) and set(weights) <= set(row_by_name)
    nu = F(cert['dual']['normalization_multiplier'])
    residual = [objective[j]-nu*eq[j]-sum(w*F(row_by_name[name]['a'].get(str(j),'0')) for name,w in weights.items()) for j in range(N)]
    assert all(v>=0 for v in residual) and residual == vec(cert['dual']['nonnegative_column_residual'])
    bound = nu+sum(w*F(row_by_name[name]['rhs']) for name,w in weights.items())
    assert bound == W == F(cert['dual']['objective'])
    assert all(residual[j]*z[j]==0 for j in range(N))
    for name,w in weights.items():
        row = row_by_name[name]
        assert w*(dot(vec(row['a']),z)-F(row['rhs'])) == 0
    positive_atom = [j for j in range(256) if z[j]>0]
    positive_residual = [j for j in range(N) if residual[j]>0]
    zero_residual = [j for j in range(N) if not residual[j]]
    tight = [i for i,s in enumerate(rawslack) if not s]
    indices = {'positive_atom_columns':positive_atom,'positive_primal_columns':[j for j in range(N) if z[j]>0],
        'positive_dual_raw_rows':[i for i,row in enumerate(inp['raw_rows']) if row['name'] in weights],
        'tight_raw_row_indices':tight,'tight_raw_row_names':[inp['raw_rows'][i]['name'] for i in tight],
        'zero_column_residual_indices':zero_residual,'positive_column_residual_indices':positive_residual,
        'positive_dual_unique_indices':[i for i,row in enumerate(unique) if row['name'] in weights]}
    save('residual_index.json',indices)
    scale = lcm(W.denominator,nu.denominator,*(w.denominator for w in weights.values()))
    paid = {name:str(scale*w) for name,w in weights.items()}
    scaled_res = [scale*v for v in residual]
    identity = {'scope':'All257 unscaled rational columns; global homogeneous identity uses each rhs times O.',
        'formula':'E W - N O = sum p_i (a_i dot (z,K) - rhs_i O) + sum r_j (z,K)_j',
        'E':str(scale),'N':str(scale*W),'positive_integer_row_payments':paid,
        'normalization_multiplier_scaled':str(scale*nu),
        'all257_scaled_residuals':[str(v) for v in scaled_res],
        'K_residual':str(scaled_res[256]),'all_residuals_nonnegative':True}
    assert all(F(v).denominator==1 for v in paid.values()) and F(identity['N']).denominator==1
    save('global_identity.json',identity)
    with (HERE/'all257_column_checks.tsv').open('w') as f:
        f.write('column\ta1_a6\tx\to\tprimal_mass\texact_dual_residual\tcomplementarity\n')
        for j in range(N):
            r=atoms[j] if j<256 else None
            f.write(f"{j}\t{''.join(map(str,r['a'])) if r else 'K'}\t{r['x'] if r else ''}\t{r['o'] if r else ''}\t{z[j]}\t{residual[j]}\t{z[j]*residual[j]}\n")
    result={'status':'PASS','optimizer_calls_by_checker':0,'input_sha256':sha(HERE/'exact_input.json'),
        'certificate_sha256':sha(HERE/'exact_certificate.json'),'all_raw_rows_checked':546,'all_columns_checked':257,
        'objective':str(W),'objective_decimal':float(W),'half_gap':str(F(1,2)-W),
        'positive_atoms':len(positive_atom),'positive_dual_rows':len(weights),'positive_column_residuals':len(positive_residual),
        'zero_column_residuals':len(zero_residual),'complementarity':True,'exact_duality_gap':'0',
        'K':str(z[256]),'K_residual':str(residual[256]),'source_preflight':'PASS','unchanged_frozen_files':len(oldpins)}
    save('checker_output.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
