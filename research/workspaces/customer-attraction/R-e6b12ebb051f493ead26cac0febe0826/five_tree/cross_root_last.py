"""Root-query terminal nodes query the second-query terminal menu.

The only new row is an exact sum of 25 last-mover SPE comparisons.
The conditional pricer exhausts all second-J counts 0,...,5; it preserves
the parent template's complete customer coefficient universe. Discovery
uses floating LPs and is not a proof until rational/global verification.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib, json, sys, time
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'customer_attraction/__init__.py').exists())
PEER = ROOT / 'research/workspaces/customer-attraction/R-bfbfe64dd5f94fa09d36b75198633f2b/five_only'
sys.path.insert(0, str(PEER))
import combined_root_penultimate as parent

NAME = 'CrossRootLast:second-J'
RTYPES = tuple(product((0, 1), repeat=5))
STYPES = tuple(product((0, 1), repeat=4))


def row(atom, exact=True):
    """Per-customer coefficient, including all five indexed root nodes."""
    Q = (lambda a, b: F(int(a), int(b)) if a else F()) if exact else (lambda a, b: a / b if a else 0.)
    den = sum(n * Q(1, sum(t[:-1]) + 1) for n, t in zip(atom['root_hist'], RTYPES))
    share = sum(n * Q(t[-1], sum(t)) for n, t in zip(atom['root_hist'], RTYPES))
    count = sum(n * t[-1] for n, t in zip(atom['second_hist'], STYPES))
    return 5 * share - count * den


def diagnose():
    src = PEER / 'ap_binary_discovery.json'
    data = json.loads(src.read_text())
    support = [(a, w) for a, w in zip(data['atoms'], data['primal_float']) if w > 1e-9]
    slack = sum(w * float(row(a)) for a, w in support)
    report = {'scope': 'Floating separation of an older necessary-condition point only; not a SPE instance or welfare theorem',
              'source': str(src.relative_to(ROOT)), 'source_sha256': hashlib.sha256(src.read_bytes()).hexdigest(),
              'source_beta_float': data['dual_beta_float'], 'positive_atoms': len(support),
              'new_row': NAME, 'new_row_slack_float': slack}
    (HERE / 'separation.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report), flush=True)


class Universe(parent.Universe):
    def __init__(self):
        super().__init__()
        self.cross_id = len(self.names)
        self.names.append(NAME)
        self.second_count = self.count[4]['W']

    def atom_rows(self, atom, exact=True):
        rr = super().atom_rows(atom, exact)
        rr[NAME] = row(atom, exact)
        return rr

    def price(self, lam, beta, batch=80):
        """Exact domain split, floating arithmetic inherited from parent.

        With second-J count c fixed, the new weighted coefficient is
        5*lambda*share_K - lambda*c*den_4, a root-local linear function.
        The second family is restricted to its complete (d,c) fiber;
        all other complete families and shared old menus are unchanged.
        """
        lam = np.asarray(lam)
        weight = float(lam[self.cross_id])
        if abs(weight) < 1e-13:
            return super().price(lam, beta, batch)
        original_ids = self.ids[4]
        original_price = self.root_engine.root_price
        minima, output, total_contexts = [], [], 0
        try:
            for count in range(6):
                self.ids[4] = [ids[self.second_count[ids] == count] for ids in original_ids]
                assert all(len(ids) for ids in self.ids[4])
                def conditional_root_price(co, integer=False, count=count):
                    adjusted = dict(co)
                    adjusted['Root:5:K:A'] = adjusted.get('Root:5:K:A', 0.) + 5 * weight
                    adjusted['den:4'] = adjusted.get('den:4', 0.) - count * weight
                    return original_price(adjusted, integer)
                self.root_engine.root_price = conditional_root_price
                minimum, atoms, contexts = super().price(lam, beta, batch)
                minima.append(minimum)
                output.extend(atoms)
                total_contexts += contexts
                print(json.dumps({'conditional_second_J_count': count, 'minimum_scaled_residual': minimum,
                                  'negative_columns_returned': len(atoms)}), flush=True)
        finally:
            self.ids[4] = original_ids
            self.root_engine.root_price = original_price
        output.sort(key=lambda pair: pair[0])
        return min(minima), output[:batch], total_contexts


def run(maxiter=10):
    universe = Universe()
    target = HERE / 'cross_root_last_search.json'
    source = target if target.exists() else PEER / 'combined_root_saturation_search.json'
    warm = json.loads(source.read_text())
    atoms, columns, keys, ws, os = [], [], set(), [], []
    def add(atom):
        key = parent.key(atom)
        if key in keys:
            return 0
        rr = universe.atom_rows(atom, False)
        columns.append([float(rr[name]) for name in universe.names])
        atoms.append(atom); keys.add(key)
        ws.append(int(any(map(int, atom['bits'][:5])))); os.append(int(any(atom['AB_hist'][4:])))
        return 1
    keep = list(range(0, len(warm['atoms']), max(1, len(warm['atoms']) // 160)))
    keep += list(range(max(0, len(warm['atoms']) - 180), len(warm['atoms'])))
    for i in sorted(set(keep)):
        add(warm['atoms'][i])
    for atom in atoms[::max(1, len(atoms)//6)]:
        exact = universe.atom_rows(atom)
        fast = universe.atom_rows(atom, False)
        assert max(abs(float(exact[n])-float(fast[n])) for n in universe.names) < 1e-8
    print(json.dumps({'initial_columns': len(atoms), 'rows': len(universe.names), 'exact_fast_crosschecks': 'passed'}), flush=True)
    test_weights=np.zeros(len(universe.names));test_weights[-1]=1.
    test_minimum,test_atoms,test_contexts=universe.price(test_weights,2.,batch=6)
    assert abs(test_minimum+3000.)<1e-8,(test_minimum,'new-row-only global extremum')
    for residual,atom in test_atoms:
        expected=120*(2*int(any(map(int,atom['bits'][:5])))-int(any(atom['AB_hist'][4:]))-float(row(atom)))
        assert abs(residual-expected)<1e-8
    print(json.dumps({'six_fiber_nonzero_multiplier_selfcheck':'passed','new_row_only_global_minimum_scaled':test_minimum}),flush=True)
    provenance = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in (Path(__file__), Path(parent.__file__), source)}
    history = []
    for iteration in range(maxiter):
        tick = time.time()
        matrix = np.asarray(columns).T
        scale = np.maximum(1., np.max(np.abs(matrix), axis=1))
        out = linprog(np.ones(len(universe.names)), A_ub=(matrix/scale[:, None]).T,
                      b_ub=2*np.asarray(ws)-np.asarray(os), bounds=(0, None), method='highs')
        if not out.success:
            report = {'scope': 'Restricted necessary-row certificate search only, not a SPE or game theorem',
                      'status': 'restricted-certificate-infeasible', 'message': out.message,
                      'sources': provenance, 'atoms': atoms, 'history': history}
            target.write_text(json.dumps(report, indent=2)+'\n')
            print(json.dumps({k:v for k,v in report.items() if k not in ('atoms','history')}), flush=True)
            return
        lam = out.x/scale
        minimum, new, contexts = universe.price(lam, 2., batch=160)
        added = sum(add(a) for _, a in new)
        record = {'iteration': iteration, 'columns': len(atoms), 'minimum_scaled_residual': minimum,
                  'new_columns': added, 'contexts': contexts, 'cross_multiplier_float': float(lam[-1]),
                  'seconds': time.time()-tick}
        history.append(record); print(json.dumps(record), flush=True)
        report = {'scope': 'Floating complete-domain coefficient discovery only; not a welfare bound or SPE instance',
                  'status': 'fixed-beta-two-search', 'sources': provenance, 'atoms': atoms, 'history': history,
                  'dual_multipliers_float': {n:float(v) for n,v in zip(universe.names,lam) if v>1e-10}}
        target.write_text(json.dumps(report, indent=2)+'\n')
        if added == 0:
            return


if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1]=='diagnose':
        diagnose()
    else:
        run(int(sys.argv[1]) if len(sys.argv)>1 else 10)
