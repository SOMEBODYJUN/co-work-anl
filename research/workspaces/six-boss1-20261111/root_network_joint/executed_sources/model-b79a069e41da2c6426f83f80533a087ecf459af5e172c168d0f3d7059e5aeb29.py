"""Full positive-mu Cartesian domain over the fixed 100-atom R/Z/B4/D law.

The old named vector U is kept, with one simultaneous S6 action.  Equal
old words never identify their root events.  Each column has ALL SIX root
states and a whole old-network atom.  No min overlap is used as an event.
The 458 literal-orbit inequalities are 239+root-source, Main's 198, and
20 genuine D/root terminal or SAFE queries.  Finite coverage, not SPE.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import product, permutations
from math import prod, factorial
from pathlib import Path
import hashlib
import json
import sys
import time
import types

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
POINT = BASE/'union_augmented_lp/augmented_lp_exact.json'
MU = BASE/'root_marginal_closure/marginal_completion_exact.json'
NET = BASE/'fifth_reply_common/common_atoms_with_D.json'
PINS = {
    POINT: 'b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3',
    MU: '9866e82bbc40e661d15d4aee3a4472fd99137ade5a9fa7fd0872f6344ffe0966',
    NET: '91599404ee03184bbb072767d7d55761b95bcc89e1d55e748aebf2ee60f19c54',
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def serial(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [serial(v) for v in x]
    return x


def dump(name, obj):
    (HERE/name).write_text(json.dumps(serial(obj), ensure_ascii=False, indent=2)+'\n')


def load_module(name, p):
    mod = types.ModuleType(name)
    mod.__file__ = str(p)
    exec(compile(p.read_text(), str(p), 'exec'), mod.__dict__)
    return mod


def bits(w, n):
    return tuple((w >> (n-1-k)) & 1 for k in range(n))


def q(n, d):
    assert d or not n
    return F(n, d) if n else F()


def canon(seq):
    names = {}
    return tuple(names.setdefault(i, len(names)) for i in seq)


def row_key(name):
    return json.dumps(name, separators=(',', ':'))


class Model:
    def __init__(self):
        for path, expected in PINS.items():
            assert sha(path) == expected, path
        self.point, self.mu_cert, self.network = [json.loads(p.read_text()) for p in (POINT, MU, NET)]
        assert self.mu_cert['point_sha256'] == self.network['point_sha256'] == PINS[POINT]
        self.hist = {j: c for j, c in enumerate(self.point['columns']) if c['kind'] == 'hist'}
        self.H = {h: F(c['weight']) for h, c in self.hist.items()}
        self.blocks = {b['hist_column']: b for b in self.network['blocks']}
        self.mu = defaultdict(dict)
        for r in self.mu_cert['positive_states']:
            self.mu[r['hist'], r['old_word']][r['state']] = F(r['mass'])
        self.old = {h: tuple(w for w, count in enumerate(c['hist']) for _ in range(count))
                    for h, c in self.hist.items()}
        assert len(self.hist) == 16 and len(self.blocks) == 10 and sum(map(len, self.mu.values())) == 35
        assert self.network['base_atoms'] == sum(len(b['atoms']) for b in self.blocks.values()) == 100
        for h, c in self.hist.items():
            assert sum(c['hist']) == 6 and c['d'] == sum(c['hist'][4:]) == 1
            for w in set(self.old[h]):
                assert sum(self.mu[h, w].values(), F()) == self.H[h]
            if self.H[h]:
                assert self.blocks[h]['actual_bits'] == c['actual_bits']
                assert self.blocks[h]['hist'] == c['hist']
                assert sum((F(a['mass']) for a in self.blocks[h]['atoms']), F()) == self.H[h]
            else:
                assert h not in self.blocks
        self.rm = load_module('read_only_root239_model', BASE/'root_pair_joint_19662/model.py')
        self.rc = self.rm.root_contract()
        self.data = self.rm.load_inputs()
        self.root_names = self.rc.row_names(True)+self.rm.single_names()+self.rm.pair_names()+[('root-source',)]
        self.constant = self.rc.budgets(self.data, self.rc.row_names(True))+[F()]*76+[self.data['u'][0]]
        assert len(self.root_names) == len(self.constant) == 240
        self.nodes = tuple(tuple(e) for e in self.network['literal_node_order'])
        assert self.nodes == tuple(e for e in product(range(2), range(6), range(6)) if e[0] or e[1] != e[2])
        self.orbits = defaultdict(list)
        for i in range(6):
            for ei, (f, j, k) in enumerate(self.nodes):
                self.orbits[f, canon((i, j, k))].append((i, ei))
        self.net_names = []
        for kind in ('R-to-Y', 'Z-to-Y', 'Y-to-R', 'Y-to-Z'):
            self.net_names += [(kind, o, k) for o in self.orbits for k in range(5)]
        self.net_names += [(kind, k) for kind in ('F-to-Y', 'H1-safe-to-Y', 'Y-to-H1', 'Y-to-H2') for k in range(5)]
        self.net_names += [('B4-pair-to-Y', k, l) for k in range(5) for l in range(k, 5)]
        self.net_names += [('Y-pair-to-B4', key) for key in ('11', '12', '22')]
        self.d_names = [(kind, k, rel) for kind in ('D-to-Y', 'Y-to-D') for k in range(5) for rel in ('same', 'off')]
        assert len(self.net_names) == 198 and len(self.d_names) == 20
        self.new_names = self.net_names+self.d_names
        self.names = self.root_names+self.new_names
        self.constant += [F()]*(198+20)
        self.root_cache = {}
        self.local_cache = {}
        self.columns = []
        self.domain = []
        for h, c in self.hist.items():
            support = [tuple(sorted(self.mu[h, w])) for w in self.old[h]]
            count = prod(map(len, support))
            atoms = self.blocks.get(h, {}).get('atoms', [])
            self.domain.append(dict(hist=h, actual=c['actual_bits'], mass=self.H[h], old_words=self.old[h],
                old_word_multiplicities=c['hist'], positive_states={w: sorted(self.mu[h,w]) for w in sorted(set(self.old[h]))},
                named_slot_state_counts=list(map(len, support)), full_named_root_vectors=count,
                network_atoms=len(atoms), canonical_joint_columns=count*len(atoms),
                S6_copies=720*count*len(atoms), old_word_stabilizer=prod(factorial(n) for n in c['hist'])))
            for ai, atom in enumerate(atoms):
                for states in product(*support):
                    self.columns.append((h, ai, states))
        assert len(self.columns) == 3086 and sum(d['full_named_root_vectors'] for d in self.domain) == 1303

    def root_column(self, h, states):
        old = self.old[h]
        key = (h, tuple(sorted(zip(old, states))))
        if key not in self.root_cache:
            a = self.hist[h]['actual_bits']
            root, costs = self.rc.compressed_column(a, 1, [(w >> 2, s) for w, s in zip(old, states)],
                                                    self.rc.row_names(True), self.data['remainder'])
            inter = self.rm.interfaces(a, old, states)
            val = [-v for v in costs]+[inter[n] for n in self.rm.single_names()+self.rm.pair_names()]+[-root]
            self.root_cache[key] = val
        return self.root_cache[key]

    def local_column(self, h, ai, i, state):
        key = (h, ai, i, state)
        if key in self.local_cache:
            return self.local_cache[key]
        atom = self.blocks[h]['atoms'][ai]
        a = tuple(map(int, self.hist[h]['actual_bits']))
        old = [bits(w, 3) for w in self.old[h]]
        e, t = bits(state, 5), old[i][0]
        total, p3, P = t+sum(e), sum(a[:3]), sum(a[:4])
        val = defaultdict(F)
        for o, queries in self.orbits.items():
            for ii, ei in queries:
                if ii != i:
                    continue
                f, j, k = self.nodes[ei]
                r, z = divmod(atom['states'][ei], 2)
                rden = p3+old[j][0]+old[k][1+f]+1
                for l in range(5):
                    den = t+sum(e[:l])+5-l
                    truepay = q(e[l], total)
                    val['R-to-Y', o, l] += F(r-e[l], rden*len(queries))
                    val['Z-to-Y', o, l] += F(z-e[l], (P+r+1)*len(queries))
                    val['Y-to-R', o, l] += (truepay-F(r,den))/len(queries)
                    val['Y-to-Z', o, l] += (truepay-F(z,den))/len(queries)
        h1, h2, _ = atom['B4_state']
        base = p3+a[5]
        hpay, fpay = F(h1, base+1+h2), F(h2, base+1+h1)
        bpair = hpay+fpay+F(h1, (base+1)*(base+2))
        for l in range(5):
            den = t+sum(e[:l])+5-l
            truepay = q(e[l], total)
            val['F-to-Y', l] += F(h2-e[l], 6*(base+h1+1))
            val['H1-safe-to-Y', l] += (hpay-F(e[l],base+2))/6
            val['Y-to-H1', l] += (truepay-F(h1,den))/6
            val['Y-to-H2', l] += (truepay-F(h2,den))/6
            for k in range(l, 5):
                val['B4-pair-to-Y', l, k] += (bpair-F(e[l]+e[k],base+1)+F(e[l]*e[k],(base+1)*(base+2)))/6
        pref = t+sum(e[:3])
        ypair = F(e[3],pref+1+e[4])+F(e[4],pref+1+e[3])+F(e[3],(pref+1)*(pref+2))
        for label, b, c in (('11',h1,h1),('12',h1,h2),('22',h2,h2)):
            val['Y-pair-to-B4', label] += (ypair-F(b+c,pref+1)+F(b*c,(pref+1)*(pref+2)))/6
        for j in range(6):
            rel, norm = ('same',6) if i==j else ('off',30)
            d = atom['D_bits'][j]
            for l in range(5):
                den = t+sum(e[:l])+5-l
                val['D-to-Y',l,rel] += F(d-e[l],(P+old[j][0]+1)*norm)
                val['Y-to-D',l,rel] += (q(e[l],total)-F(d,den))/norm
        result = [val[n] for n in self.new_names]
        self.local_cache[key] = result
        return result

    def column(self, h, ai, states):
        pieces = [self.local_column(h,ai,i,s) for i,s in enumerate(states)]
        return self.root_column(h,states)+[sum(v,F()) for v in zip(*pieces)]

    def product_mass(self, h, ai, states):
        return F(self.blocks[h]['atoms'][ai]['mass'])*prod(self.mu[h,w][s]/self.H[h] for w,s in zip(self.old[h],states))

    def product_evaluate(self):
        # Exact finite-product expectations, avoiding materializing 2,221,920 copies.
        root_weights = defaultdict(F)
        for h,c in self.hist.items():
            if not self.H[h]:
                continue
            supports = [tuple(self.mu[h,w]) for w in self.old[h]]
            for states in product(*supports):
                mass = self.H[h]*prod(self.mu[h,w][s]/self.H[h] for w,s in zip(self.old[h],states))
                key = (h,tuple(sorted(zip(self.old[h],states))))
                root_weights[key] += mass
                self.root_column(h,states)
        sums = list(self.constant)
        for key,m in root_weights.items():
            for j,v in enumerate(self.root_cache[key]):
                sums[j] += m*v
        for h,b in self.blocks.items():
            for ai,atom in enumerate(b['atoms']):
                for i,w in enumerate(self.old[h]):
                    for s,m in self.mu[h,w].items():
                        mass = F(atom['mass'])*m/self.H[h]
                        for j,v in enumerate(self.local_column(h,ai,i,s)):
                            sums[240+j] += mass*v
        return sums

    def summary(self, slacks):
        result = {}
        for label,indices in [('root239_and_source',range(240)),('main198',range(240,438)),('D_root20',range(438,458)),('all458',range(458))]:
            vals = [slacks[j] for j in indices]
            result[label] = dict(rows=len(vals),negative=sum(v<0 for v in vals),zero=sum(v==0 for v in vals),
                                 positive=sum(v>0 for v in vals),minimum=min(vals),minimum_float=float(min(vals)))
        return result


def main():
    start = time.monotonic()
    m = Model()
    slacks = m.product_evaluate()
    # All 194 single-root dependent old rows must equal the supplied marginal certificate.
    frozen = {row_key(r['row']): F(r['slack']) for r in m.mu_cert['principal_slacks']}
    checks = 0
    for name,v in zip(m.names[:240],slacks[:240]):
        if name[0] not in ('cross-floor','cross-pair'):
            assert v == frozen[row_key(name)], (name,v,frozen.get(row_key(name)))
            checks += 1
    assert checks == 194
    rows = [dict(name=n,slack=v,approx=float(v)) for n,v in zip(m.names,slacks)]
    report = dict(status='EXACT_CONDITIONAL_PRODUCT_EVALUATED',scope=__doc__,
        point_sha256=PINS[POINT],mu_sha256=PINS[MU],network_sha256=PINS[NET],
        script_sha256=sha(Path(__file__)),summary=m.summary(slacks),domain=m.domain,
        named_root_vectors=1303,canonical_joint_columns=len(m.columns),S6_copies=720*len(m.columns),
        kernel='For canonical network atom a in hist h and all six named root states s_i, mass = m_a * product_i(mu[h,w_i,s_i]/H_h); then simultaneous pi in S6 with mass/720. H=0 gives the zero fiber.',
        mu_probabilities=[dict(hist=h,old_word=w,state=s,mass=mu,conditional_probability=mu/m.H[h])
                          for (h,w),states in sorted(m.mu.items()) for s,mu in sorted(states.items())],
        full_support_is_cartesian=True,equal_old_words_are_distinct_events=True,
        unchanged_single_root_row_checks=checks,rows=rows,negative_rows=[r for r in rows if r['slack']<0],
        no_SPE_claim=True,no_original_point_exclusion=True,elapsed_seconds=time.monotonic()-start)
    dump('conditional_product_exact.json',report)
    dump('inputs_exact.json',dict(inputs=[dict(path=str(p.relative_to(BASE)),sha256=v,bytes=p.stat().st_size) for p,v in PINS.items()],
        hist_records=[dict(column=h,**c) for h,c in m.hist.items()],positive_mu=m.mu_cert['positive_states'],
        network_schema='100 canonical atoms from pinned network input, each fixed in full; no marginal-only reconstruction.',
        coefficient_sources=[dict(path=str(p.relative_to(BASE)),sha256=sha(p)) for p in [BASE/'root_pair_joint_19662/model.py',BASE/'cross_root_pricing/contract.py',BASE/'root_pair_joint_19662/verify_completion.py',BASE/'main_glued_terminal_interfaces.py']],
        row_order=m.names,constants=m.constant))
    print(json.dumps(serial(dict(summary=report['summary'],negative_rows=report['negative_rows'],
                                root_cache=len(m.root_cache),local_cache=len(m.local_cache),elapsed_seconds=report['elapsed_seconds'])),ensure_ascii=False))


if __name__ == '__main__':
    main()
