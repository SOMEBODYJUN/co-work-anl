"""Root saturation constraints plus the existing 557-row universe.

Numerical certificate discovery only. A floating value or a restricted-support
point is neither a universal proof nor a complete SPE counterexample.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import sys
import time
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'customer_attraction/__init__.py').exists())
SOURCE = ROOT / 'research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_pricing'
sys.path.insert(0, str(SOURCE))
import full_pricing as old


def extra_rows(bits, d):
    b = list(map(int, bits))
    k = sum(b[:5])
    u = F(b[0], k) if k else F()
    C = F(11, 2)
    L = 1 + 5 * C
    out = {}
    for i, t in enumerate(b):
        for j, q in enumerate(b):
            if i != j:
                out[f'RS:fixed:{i}:{j}'] = L * u - C * t - q + F(4, 5) * t * q
        out[f'RS:fixed-opt:{i}'] = 5 * L * u - 5 * C * t - d + F(4, 5) * t * d
        out[f'RS:opt-fixed:{i}'] = 5 * L * u - C * d - 5 * t + F(4, 5) * t * d
        out[f'CAP:k3:fixed:{i}'] = 33482 * u - 2897 * t - 1200 * int(d > 0)
        out[f'CAP:k4:fixed:{i}'] = 28735 * u - 4447 * t - 600 * int(d > 0)
    # Sum all 25 pairs, including diagonal, within the same optimal tuple.
    out['RS:opt-opt'] = 25 * L * u - 5 * (C + 1) * d + F(4, 5) * d * d
    out['CAP:k3:opt'] = 5 * 33482 * u - 2897 * d - 5 * 1200 * int(d > 0)
    out['CAP:k4:opt'] = 5 * 28735 * u - 4447 * d - 5 * 600 * int(d > 0)
    return out


class Universe(old.Universe):
    def __init__(self):
        super().__init__(1)
        names = list(extra_rows((0,) * 10, 0))
        arr = np.zeros((1024, 6, len(names)), dtype=np.int64)
        for bi, bits in enumerate(self.bits):
            for d in range(6):
                rr = extra_rows(bits, d)
                arr[bi, d] = old.sc([rr[n] for n in names])
        self.names += names
        self.oldnames += names
        self.oldids = [self.names.index(n) for n in self.oldnames]
        self.base = np.concatenate((self.base, arr), axis=-1)
        zero = np.zeros((1024, 6, 3, len(names)), dtype=np.int64)
        self.ec = np.concatenate((self.ec, zero), axis=-1)
        self.hc = np.concatenate((self.hc, zero), axis=-1)
        print(json.dumps({'root_saturation_rows': len(names), 'total_rows': len(self.names)}), flush=True)

    def atom_rows(self, atom):
        rr = super().atom_rows(atom)
        rr.update(extra_rows(atom['bits'], sum(atom['AB_hist'][4:])))
        return rr


def run(maxiter=30):
    U = Universe()
    source = json.loads((SOURCE / 'cg_overlap1_final.json').read_text())
    previous = HERE / 'root_saturation_cg.json'
    warm = json.loads(previous.read_text()) if previous.exists() else source
    atoms, keys, cols, ws, os = [], set(), [], [], []

    def add(a):
        key = old.atom_key(a)
        if key in keys:
            return False
        rows = U.atom_rows(a)
        atoms.append(a)
        keys.add(key)
        cols.append([float(rows[n]) for n in U.names])
        ws.append(int(any(map(int, a['bits'][:5]))))
        os.append(int(any(a['AB_hist'][4:])))
        return True

    for a in warm['atoms']:
        add(a)
    for d in (0, 5):
        h3, h4 = [0] * 8, [0] * 16
        h3[3 if d == 0 else 7] = 5
        h4[7 if d == 0 else 15] = 5
        add({'bits': '1111111111', 'AB_hist': h3, 'AE_hist': h3, 'second_hist': h4, 'menus_lh': [(5, d)] * 3})
    history = []
    for it in range(maxiter):
        start = time.monotonic()
        mat = np.array(cols).T
        out = linprog(-np.array(os, dtype=float), A_ub=-mat, b_ub=np.zeros(len(U.names)),
                      A_eq=[ws], b_eq=[1.], bounds=(0, None), method='highs')
        if not out.success:
            raise RuntimeError(out.message)
        beta, lam = float(-out.fun), -out.ineqlin.marginals
        minimum, new, contexts = U.price(lam, beta, batch=80)
        count = sum(add(a) for _, a in new)
        rec = {'iteration': it, 'columns': len(atoms), 'restricted_beta': beta,
               'full_pricing_min_scaled': minimum, 'new_columns': count,
               'contexts': contexts, 'seconds': time.monotonic() - start}
        history.append(rec)
        print(json.dumps(rec), flush=True)
        report = {'scope': 'Floating necessary-condition discovery; not a universal bound or SPE',
                  'row_names': U.names, 'atoms': atoms,
                  'primal_float': out.x.tolist() + [0.] * count,
                  'dual_beta_float': beta,
                  'dual_multipliers_float': {n: float(v) for n, v in zip(U.names, lam) if v > 1e-10},
                  'history': history}
        previous.write_text(json.dumps(report, indent=2) + '\n')
        if count == 0:
            break


if __name__ == '__main__':
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 30)
