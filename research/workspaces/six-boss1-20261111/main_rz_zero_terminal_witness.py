"""Main: a strict five-budget witness with both fresh terminal labels empty.

The already independently reconstructed sixteen-state costs are read as
exact tables. No optimizer or constructor is imported. All zero-mass
states remain. The witness diagnoses missing true terminal best responses;
it does not realize a strategy or reverse the full624 exclusion.
"""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

WS = Path(__file__).resolve().parent
BASE = WS/'rz_fresh_terminal5'
HIDDEN = tuple(product((0, 1), repeat=4))


def digest(p):
    return sha256(p.read_bytes()).hexdigest()


def serial(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [serial(v) for v in x]
    return x


def main():
    tables = json.loads((BASE/'local_tables_exact.json').read_bytes())
    saved = json.loads((BASE/'knapsack_exact.json').read_bytes())
    inputs = ['local_tables_exact.json', 'knapsack_exact.json',
              'independent_verification.json', 'final_manifest.json']
    expected = {r['path']: r['sha256'] for r in
                json.loads((BASE/'final_manifest.json').read_bytes())['files']}
    for name in inputs[:-1]:
        assert digest(BASE/name) == expected[str((BASE/name).relative_to(WS.parents[2]))]
    budget = {b: Q(saved['solutions'][b]['budget']) for b in ('A', 'B')}
    costs = {n: Q() for n in ('A', 'B', 'old_Z', 'R_to_vB', 'Z_to_vA',
              'cA_to_vB', 'vA_to_vB', 'cB_to_vA', 'vB_to_vA',
              'vA_to_Tmean', 'vB_to_Tmean')}
    atoms = []
    for s in tables['states']:
        mass = Q(s['mass'])
        assert mass >= 0
        selected = {}
        for branch in ('A', 'B'):
            values = list(map(Q, s[branch+'_costs']))
            index = min((k for k, hh in enumerate(HIDDEN) if hh[3] == 0),
                        key=lambda k: (values[k], k))
            assert index == s[branch+'_argmin_by_v'][0]
            assert values[index] == Q(s[branch+'_min_by_v'][0])
            selected[branch] = HIDDEN[index]
            costs[branch] += mass*values[index]
        r, z = s['old_state']
        p, P, q = s['p'], s['P'], Q(s['n'], 6)
        ba, ca, ja, va = selected['A']
        bb, cb, jb, vb = selected['B']
        assert va == vb == 0
        costs['old_Z'] += mass*(q-z)/Q(P+r+1)
        costs['R_to_vB'] += mass*Q(vb-r, s['denom_R'])
        costs['Z_to_vA'] += mass*Q(va-z, s['denom_Z'])
        costs['cA_to_vB'] += mass*Q(vb-ca, p+r+ba+1)
        costs['vA_to_vB'] += mass*Q(vb-va, p+ca+ja+1)
        costs['cB_to_vA'] += mass*Q(va-cb, p+z+bb+1)
        costs['vB_to_vA'] += mass*Q(va-vb, p+cb+jb+1)
        costs['vA_to_Tmean'] += mass*(q-va)/Q(p+ca+ja+1)
        costs['vB_to_Tmean'] += mass*(q-vb)/Q(p+cb+jb+1)
        atoms.append(dict(state_id=s['id'],hist_column=s['hist_column'],
                          old_state=s['old_state'],wi=s['wi'],wj=s['wj'],
                          mass=mass,A=selected['A'],B=selected['B']))
    assert len(atoms) == 312 and sum((a['mass'] for a in atoms), Q()) == 1
    slacks = {n: (budget[n] if n in budget else Q())-costs[n]
              for n in ('A','B','old_Z','R_to_vB','Z_to_vA')}
    for b in ('A','B'):
        assert costs[b] == Q(saved['solutions'][b]['baseline_v0_cost'])
    assert slacks['old_Z'] == Q(saved['old_Z_slack'])
    assert slacks['R_to_vB'] == Q(saved['solutions']['B']['query_capacity'])
    assert slacks['Z_to_vA'] == Q(saved['solutions']['A']['query_capacity'])
    eta = min(slacks.values())
    assert eta == slacks['old_Z'] > 0
    follow = ('cA_to_vB','vA_to_vB','cB_to_vA','vB_to_vA')
    assert all(costs[n] <= 0 for n in follow)
    assert costs['vA_to_Tmean'] > 0 and costs['vB_to_Tmean'] > 0
    report = dict(status='EXACT STRICT FIVE-BUDGET ZERO-TERMINAL WITNESS',
        inputs={n:digest(BASE/n) for n in inputs},script_sha256=digest(Path(__file__)),
        canonical_states=len(atoms),positive_states=sum(a['mass']>0 for a in atoms),
        total_mass=Q(1),atoms=atoms,slacks=slacks,
        slack_float={n:float(v) for n,v in slacks.items()},
        normalized_whole_five_cone_lower_bound=eta,
        normalized_lower_bound_float=float(eta),
        four_followup_costs={n:costs[n] for n in follow},
        missing_true_terminal_query_costs={n:costs[n] for n in ('vA_to_Tmean','vB_to_Tmean')},
        missing_query_costs_float={n:float(costs[n]) for n in ('vA_to_Tmean','vB_to_Tmean')},
        interpretation='The fixed five-budget cone has a single strictly feasible witness, and adding only the four mutual fresh-terminal queries still cannot separate. The witness fails each empty terminal versus the average of six legal T labels; it is not a SPE.')
    out=WS/'main_rz_zero_terminal_witness.json'
    assert not out.exists()
    out.write_text(json.dumps(serial(report),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(serial({k:v for k,v in report.items() if k!='atoms'}),ensure_ascii=False))


if __name__ == '__main__':
    main()
