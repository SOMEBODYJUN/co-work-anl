"""One new arithmetic check of the saved restricted-support certificates.

Reuse the previously verified old64 terminal/pair coefficient tables rather
than repeating their literal-index checks. Reuse canonical old437 definitions
on the new weak masses/dual, and the parent's independent selected-old-row
definitions for the strong Farkas combination. No optimizer or original CLI.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from math import lcm
import ast, hashlib, json

E = Path(__file__).resolve().parent
OUT = E / 'restricted-certificate-check.json'
if OUT.exists():
    raise SystemExit('Successful check already exists; do not repeat it')
REPO = next(p for p in E.parents if (p / 'cleanup/OBJECTS.md').exists())
canonpath = REPO / 'archives/customer-attraction/tools/evidence/five-player-indexed/evidence/certificates/customer_attraction/five_player_indexed_bound.json'
oldpath = REPO / 'archives/customer-attraction/tools/evidence/five-player-indexed/tests/audits/customer_attraction_five_indexed.py'
maturepath = REPO / 'archives/customer-attraction/tools/evidence/index-equality-closure-and-hybrid-primary/new-index-pattern-and-hybrid-check.json'
certpath = E / 'original/frozen_pair_reoptimization.json'
parentpath = E / 'original/audit_pair_credibility.py'
assert hashlib.sha256(canonpath.read_bytes()).hexdigest() == '18e074ba51357dfa03090fe9b97b8ff868b9c83b2687c7da7ff6f7b39489abe1'
assert hashlib.sha256(certpath.read_bytes()).hexdigest() == '6d8c11b52fa32a3d301f1bf9a4094b824f049e5d28ab0279f69d9f8d388acffc'
canon = json.loads(canonpath.read_text())['primal']
cert = json.loads(certpath.read_text())
mature = json.loads(maturepath.read_text())
assert mature['input64_sha256'] == hashlib.sha256(canonpath.read_bytes()).hexdigest()
atoms = canon['atoms']
assert len(atoms) == 64
nodes = []
for node in ast.parse(oldpath.read_text()).body:
    if isinstance(node, ast.ImportFrom) and node.module == 'pathlib':
        break
    nodes.append(node)
ns = {}
exec(compile(ast.Module(body=nodes, type_ignores=[]), str(oldpath), 'exec'), ns)
oldcols = [ns['evaluate'](tuple(map(int,a['bits'])), [a['AB_hist'],a['AE_hist'],a['second_hist']],a['menus_lh'],True) for a in atoms]
assert all(len(c) == 437 and set(c) == set(canon['rows']) for c in oldcols)
terminal = {f"{r['family']}:5:offdiag:{r['query_position']}":list(map(F,r['atom_coefficients'])) for r in mature['terminal_rows']}
pair = {}
pattern_names = {'all_equal':'all_equal', 'query_equal_not_branch':'query_equal',
                 'first_query_equals_branch':'first_branch',
                 'second_query_equals_branch':'second_branch', 'all_distinct':'all_distinct'}
for r in mature['pair_rows']:
    n = f"{r['family']}:pair:{r['M_position']}{r['N_position']}:{pattern_names[r['index_pattern']]}"
    pair[r['overlap_coefficient'], n] = list(map(F,r['atom_coefficients']))
assert len(terminal) == 10 and len(pair) == 220 and all(len(v) == 64 for v in terminal.values())
weakcols = [dict(c) for c in oldcols]
for name, coeff in terminal.items():
    for c, v in zip(weakcols, coeff):
        c[name] = v
for (omega, name), coeff in pair.items():
    if omega == 2:
        for c, v in zip(weakcols, coeff):
            c[name] = v
assert all(len(c) == 557 for c in weakcols)

def key(a):
    return json.dumps({k:a[k] for k in ('bits','AB_hist','AE_hist','second_hist','menus_lh')}, sort_keys=True)

index = {key(a):i for i,a in enumerate(atoms)}
assert len(index) == 64
weak = cert['weak_pair_tax']
mass = [F(0)] * 64
mapping = []
for a in weak['atoms']:
    i = index[key(a)]
    assert mass[i] == 0 and a['mass_numerator'] is None
    mass[i] = F(a['exact_mass'])
    assert mass[i] > 0
    mapping.append(i)
assert len(mapping) == weak['positive_masses'] == 29
w = [int(any(map(int,a['bits'][:5]))) for a in atoms]
o = [int(any(a['AB_hist'][4:])) for a in atoms]
W = sum((v*ww for v,ww in zip(mass,w)), F(0))
O = sum((v*oo for v,oo in zip(mass,o)), F(0))
assert W == F(weak['welfare']) == 1
assert O == F(weak['comparison_cover']) == F(weak['dual_beta']) < 2
assert O-2 == F(weak['gap_above_two'])
totals = {n:sum((m*c[n] for m,c in zip(mass,weakcols)),F(0)) for n in weak['slacks']}
assert len(totals) == 557 and set(totals) == set(weakcols[0])
assert min(totals.values()) == F(weak['minimum_primal_slack']) == 0
assert all(v == F(weak['slacks'][n]) for n,v in totals.items())
lam = {n:F(v) for n,v in weak['dual_multipliers'].items()}
assert len(lam) == weak['positive_dual_multipliers'] == 28 and min(lam.values()) > 0
beta = F(weak['dual_beta'])
dualres = [beta*ww-oo-sum((v*c[n] for n,v in lam.items()),F(0)) for c,ww,oo in zip(weakcols,w,o)]
assert dualres == list(map(F,weak['dual_residuals'])) and min(dualres) == F(weak['minimum_dual_residual']) == 0
assert all(totals[n] == 0 for n in lam)
assert all(dualres[i] == 0 for i in mapping)

# Read and execute just the original parent's independent fifteen-row function.
fn = next(n for n in ast.parse(parentpath.read_text()).body if isinstance(n,ast.FunctionDef) and n.name == 'selected_old_rows')
pns = {'F':F,'product':product,'combinations_with_replacement':combinations_with_replacement}
exec(compile(ast.Module(body=[fn], type_ignores=[]),str(parentpath),'exec'),pns)
strong = cert['retained_overlap_pair_tax']
flam = {n:F(v) for n,v in strong['farkas_multipliers'].items()}
assert len(flam) == strong['positive_farkas_multipliers'] == 19 and min(flam.values()) > 0
oldnames = [n for n in flam if ':pair:' not in n]
pairnames = [n for n in flam if ':pair:' in n]
assert len(oldnames) == 15 and len(pairnames) == 4 and not any('offdiag' in n for n in flam)
strongres = []
independent_old_rows = []
for i,a in enumerate(atoms):
    rr = pns['selected_old_rows'](a)
    assert set(rr) == set(oldnames) and all(v == oldcols[i][n] for n,v in rr.items())
    independent_old_rows.append({n:str(v) for n,v in rr.items()})
    rr.update({n:pair[1,n][i] for n in pairnames})
    strongres.append(-F(w[i])-sum((v*rr[n] for n,v in flam.items()),F(0)))
assert strongres == list(map(F,strong['certificate_residuals']))
assert min(strongres) == F(strong['minimum_certificate_residual']) == 0
FD = lcm(*(v.denominator for v in flam.values()))
report = {
    'scope':'Two saved557-row certificates on exactly the original64 allowed types; no unrestricted-type or SPE theorem',
    'successful_new_entry_invocations':1,'original_cli_invocations':0,'optimizer_invocations':0,
    'old64_pair_literal_checks_repeated':0,'degenerate6648_checks_repeated':0,'42point_matrix_repeated':0,
    'mature_to_original_pattern_name_mapping':pattern_names,
    'input_bindings':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (canonpath,oldpath,maturepath,certpath,parentpath)},
    'weak':{'row_count':557,'allowed_types':64,'positive_masses':29,'source_old_indices_in_saved_mass_order':mapping,
            'full64_mass_vector':list(map(str,mass)),'welfare':str(W),'comparison_cover':str(O),'gap_above_two':str(O-2),
            'saved557_slacks_all_equal':True,'slacks':{n:str(v) for n,v in totals.items()},'zero_slacks':[n for n,v in totals.items() if not v],
            'dual_multipliers':{n:str(v) for n,v in lam.items()},'dual_residuals':list(map(str,dualres)),
            'dual_residuals_saved64_all_equal':True,'zero_dual_residual_old_indices':[i for i,v in enumerate(dualres) if not v],
            'both_complementary_slackness_checks_passed':True,'exact_restricted_primal_dual_values_equal':True},
    'strong':{'allowed_types':64,'positive_multipliers':19,'independently_rebuilt_old_rows':15,'reused_mature_pair_rows':4,'used_offdiagonal_rows':0,
              'independent15_old_coefficients_all_equal_canonical':True,'all64_saved_residuals_equal':True,
              'minimum_residual':str(min(strongres)),'residuals':list(map(str,strongres)),
              'zero_residual_old_indices':[i for i,v in enumerate(strongres) if not v],
              'integer_common_denominator':str(FD),'integer_multipliers':{n:str(v*FD) for n,v in flam.items()},
              'independent_old15_coefficients_by_old_atom':independent_old_rows}}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'scope':report['scope'],'weak':{k:v for k,v in report['weak'].items() if k not in ('full64_mass_vector','slacks','dual_multipliers','dual_residuals','zero_slacks')},'strong':{k:v for k,v in report['strong'].items() if k not in ('integer_multipliers','independent_old15_coefficients_by_old_atom','residuals')}},ensure_ascii=False,indent=2))
