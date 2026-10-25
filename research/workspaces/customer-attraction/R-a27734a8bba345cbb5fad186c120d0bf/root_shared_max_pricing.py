"""Root saturation and root capacity with ONE shared maximum topic size.

K is one scalar auxiliary variable for the full catalogue maximum, not a
per-customer load, free bank, or independently chosen per-row parameter.
Floating discovery; no SPE or rigorous welfare bound is claimed by output.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import time
import numpy as np
from scipy.optimize import linprog
import root_saturation_pricing as source

HERE = Path(__file__).resolve().parent
KCO = {}


def shared_rows(bits, d):
    b = list(map(int, bits))
    k = sum(b[:5])
    u = F(b[0], k) if k else F()
    o, w = int(d > 0), int(k > 0)
    rows = {}
    # Use the genuine copy-reply root certificate, with independent review separate.
    # Scale by 30 so every coefficient fits the legacy 120-grid.
    A, B, C = F(44, 3), F(13, 5), F(16, 3)
    scale = 30
    for i, t in enumerate(b):
        for j, q in enumerate(b):
            if i != j:
                name = f'KRS:fixed:{i}:{j}'
                rows[name] = scale * (A * u - C * t - q + F(4, 5) * t * q)
                KCO[name] = scale * B
        name = f'KRS:fixed-opt:{i}'
        rows[name] = scale * (5 * A * u - 5 * C * t - d + F(4, 5) * t * d)
        KCO[name] = 5 * scale * B
        name = f'KRS:opt-fixed:{i}'
        rows[name] = scale * (5 * A * u - C * d - 5 * t + F(4, 5) * t * d)
        KCO[name] = 5 * scale * B
        rows[f'MAX:fixed:{i}'] = -t
        KCO[f'MAX:fixed:{i}'] = 1
    rows['KRS:opt-opt'] = scale * (25 * A * u - 5 * (C + 1) * d + F(4, 5) * d * d)
    KCO['KRS:opt-opt'] = 25 * scale * B
    rows['KRS:maxsource-opt'] = 1100 * u - 15 * o
    KCO['KRS:maxsource-opt'] = -193
    for ell in (2, 3, 4):
        rows[f'KCAP:{ell}'] = (29985 * ell * (ell + 1) - 25000) * u - 12000 * o
        KCO[f'KCAP:{ell}'] = 31000 + 29985 * (4 - 2 * ell)
    rows.update({'MAX:opt-sizes': -d, 'MAX:root': 5 * u,
                 'MAX:all-payoffs': w, 'MAX:opt-cover': -o})
    KCO.update({'MAX:opt-sizes': 5, 'MAX:root': -1,
                'MAX:all-payoffs': -1, 'MAX:opt-cover': 5})
    return rows


source.extra_rows = shared_rows


def run(maxiter=30):
    U = source.Universe()
    kcol = np.array([float(KCO.get(n, 0)) for n in U.names])
    previous = HERE / 'root_shared_max_copy_cg.json'
    warmfile = previous if previous.exists() else source.SOURCE / 'cg_overlap1_final.json'
    warm = json.loads(warmfile.read_text())
    atoms, keys, cols, ws, os = [], set(), [], [], []

    def add(a):
        key = source.old.atom_key(a)
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
    history = []
    for it in range(maxiter):
        start = time.monotonic()
        mat = np.column_stack((np.array(cols).T, kcol))
        out = linprog(-np.array(os + [0.], dtype=float), A_ub=-mat,
                      b_ub=np.zeros(len(U.names)), A_eq=[ws + [0.]], b_eq=[1.],
                      bounds=(0, None), method='highs')
        if not out.success:
            raise RuntimeError(out.message)
        beta, lam = float(-out.fun), -out.ineqlin.marginals
        minimum, new, contexts = U.price(lam, beta, batch=80)
        count = sum(add(a) for _, a in new)
        rec = {'iteration': it, 'columns': len(atoms), 'restricted_beta': beta,
               'shared_K': float(out.x[-1]), 'full_pricing_min_scaled': minimum,
               'K_dual_residual': float(-kcol @ lam),
               'new_columns': count, 'contexts': contexts, 'seconds': time.monotonic() - start}
        history.append(rec)
        print(json.dumps(rec), flush=True)
        report = {'scope': 'Floating shared-K necessary-condition discovery; no universal bound or SPE',
                  'row_names': U.names, 'atoms': atoms,
                  'primal_float': out.x[:-1].tolist() + [0.] * count,
                  'shared_K_float': float(out.x[-1]), 'K_column': kcol.tolist(),
                  'dual_beta_float': beta,
                  'dual_multipliers_float': {n: float(v) for n, v in zip(U.names, lam) if v > 1e-12},
                  'history': history}
        previous.write_text(json.dumps(report, indent=2) + '\n')
        if count == 0:
            break


if __name__ == '__main__':
    run()
