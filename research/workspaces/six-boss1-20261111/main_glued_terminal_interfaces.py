"""Main: glue the two exact customer laws over their full labelled old vector.

This constructs the conditional-product law only as a test witness.  It is
not an independence assumption on SPE.  New cross-block query failures only
reject this law, not every possible coupling or the original fixed point.
All coefficients below use original true-node or SAFE payoff denominators.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import json

WS = Path(__file__).resolve().parent
POINT = WS/'union_augmented_lp/augmented_lp_exact.json'
NET = WS/'common_network_19662/common_atoms.json'
ROOT = WS/'root_pair_joint_19662/joint_completion_exact.json'
PIN = 'b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'


def sha(p):
    return sha256(p.read_bytes()).hexdigest()


def bitword(w, width):
    return tuple((w >> (width-1-k)) & 1 for k in range(width))


def canon(seq):
    names = {}
    return tuple(names.setdefault(i, len(names)) for i in seq)


def ratio(n, d):
    assert d or not n
    return Q(n, d) if n else Q()


def serial(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serial(v) for v in x]
    return x


def main():
    assert sha(POINT) == PIN
    point, net, roots = [json.loads(p.read_bytes()) for p in (POINT, NET, ROOT)]
    assert net['point_sha256'] == roots['point_sha256'] == PIN
    cols = point['columns'][:4849]
    hist, own, b4 = {}, defaultdict(dict), defaultdict(dict)
    for j, c in enumerate(cols):
        if c['kind'] == 'hist':
            hi = j
            hist[hi] = c
        elif c['kind'] == 'joint-reply':
            f, diag, wi, wj = c['group']
            own[hi].setdefault((f, diag, tuple(wi), tuple(wj)), {})[tuple(c['state'])] = Q(c['weight'])
        elif c['kind'] == 'actual-B-family-state' and c['source'] == 4:
            b4[c['hist_column']][tuple(c['hidden'])+(c['ell']//6,)] = Q(c['weight'])
    for hi, c in hist.items():
        H = Q(c['weight'])
        for ss in own[hi].values():
            ss[0, 0] = H-sum(ss.values(), Q())
            assert min(ss.values()) >= 0
        assert sum(b4[hi].values(), Q()) == H
    nodes = [e for e in product(range(2), range(6), range(6)) if e[0] or e[1] != e[2]]
    orbits = defaultdict(list)
    for i in range(6):
        for ei, (f, j, k) in enumerate(nodes):
            orbits[f, canon((i, j, k))].append((i, ei))
    assert len(orbits) == 8 and sum(map(len, orbits.values())) == 396
    # S6 acts simultaneously on root index and both old node indices.
    perms = list(permutations(range(6)))
    frequency_checks = 0
    for o, pairs in orbits.items():
        target = {(i, nodes[ei][1], nodes[ei][2]) for i, ei in pairs}
        i, ei = pairs[0]
        _, j, k = nodes[ei]
        counts = Counter((p[i], p[j], p[k]) for p in perms)
        assert set(counts) == target
        assert set(counts.values()) == {720//len(pairs)}
        frequency_checks += 720
    net_hist = {b['hist_column']: sum((Q(a['mass']) for a in b['atoms']), Q()) for b in net['blocks']}
    root_hist = defaultdict(Q)
    for atom in roots['atoms']:
        root_hist[atom['hist']] += Q(atom['mass'])
    assert all(net_hist.get(h, Q()) == root_hist[h] == Q(c['weight']) for h, c in hist.items())
    # An explicit finite kernel: for each network atom and root atom in h,
    # pair every permutation p sending root old_words to canonical old_words,
    # with canonical weight m_net*m_root/(H*number_of_alignments), followed
    # by all 720 simultaneous permutations.  Its two marginals are exact.
    kernel = []
    blocks = {b['hist_column']: b for b in net['blocks']}
    for hi, b in blocks.items():
        canonical = tuple(w for w, n in enumerate(b['hist']) for _ in range(n))
        H = Q(hist[hi]['weight'])
        for ri, a in enumerate(roots['atoms']):
            if a['hist'] != hi:
                continue
            aligns = [p for p in perms if all(canonical[p[i]] == a['old_words'][i] for i in range(6))]
            assert len(aligns) > 0
            counts = Counter(tuple(a['new_words'][p.index(i)] for i in range(6)) for p in aligns)
            assert sum(counts.values()) == len(aligns)
            kernel.append(dict(hist=hi,root_atom=ri,root_mass=a['mass'],hist_mass=str(H),
                               number_of_alignments=len(aligns),
                               aligned_root_vectors=[dict(new_words=v,multiplicity=n) for v,n in sorted(counts.items())],
                               network_atom_count=len(b['atoms'])))
    slacks = defaultdict(Q)
    for atom in roots['atoms']:
        hi, mass = atom['hist'], Q(atom['mass'])
        H = Q(hist[hi]['weight'])
        actual = tuple(map(int, atom['actual']))
        old = list(map(lambda w: bitword(w, 3), atom['old_words']))
        new = list(map(lambda w: bitword(w, 5), atom['new_words']))
        assert [atom['old_words'].count(w) for w in range(8)] == hist[hi]['hist']
        p3, P = sum(actual[:3]), sum(actual[:4])
        raw = []
        for f, j, k in nodes:
            ss = own[hi][f, int(j == k), old[j], old[k]]
            r, z, rz = ss[1,0]+ss[1,1], ss[0,1]+ss[1,1], ss[1,1]
            den = p3+old[j][0]+old[k][1+f]+1
            zpay = (z-rz)/Q(P+1)+rz/Q(P+2)
            zquery_price = (H-r)/Q(P+1)+r/Q(P+2)
            raw.append((r,z,r/Q(den),zpay,zquery_price,den))
        for o, pairs in orbits.items():
            for i, ei in pairs:
                e, t = new[i], old[i][0]
                total = t+sum(e)
                r,z,rpay,zpay,zprice,den = raw[ei]
                factor = mass/(H*len(pairs))
                for k in range(5):
                    slacks['R-to-Y',o,k] += factor*(rpay-Q(e[k]*H,den))
                    slacks['Z-to-Y',o,k] += factor*(zpay-e[k]*zprice)
                    safe_den = t+sum(e[:k])+5-k
                    ypay = H*ratio(e[k],total)
                    slacks['Y-to-R',o,k] += factor*(ypay-r/Q(safe_den))
                    slacks['Y-to-Z',o,k] += factor*(ypay-z/Q(safe_den))
        base = p3+actual[5]
        B = b4[hi]
        h1 = sum((v*s[0] for s,v in B.items()),Q())
        h2 = sum((v*s[1] for s,v in B.items()),Q())
        h12 = sum((v*s[0]*s[1] for s,v in B.items()),Q())
        fpay = sum((v*Q(s[1],base+s[0]+1) for s,v in B.items()),Q())
        hpay = sum((v*Q(s[0],base+s[1]+1) for s,v in B.items()),Q())
        fprice = sum((v/Q(base+s[0]+1) for s,v in B.items()),Q())
        bpair = fpay+hpay+h1/Q((base+1)*(base+2))
        for i in range(6):
            e,t = new[i],old[i][0]
            total = t+sum(e)
            factor = mass/(6*H)
            for k in range(5):
                den = t+sum(e[:k])+5-k
                slacks['F-to-Y',k] += factor*(fpay-e[k]*fprice)
                slacks['H1-safe-to-Y',k] += factor*(hpay-H*Q(e[k],base+2))
                slacks['Y-to-H1',k] += factor*(H*ratio(e[k],total)-h1/Q(den))
                slacks['Y-to-H2',k] += factor*(H*ratio(e[k],total)-h2/Q(den))
            for k in range(5):
                for l in range(k,5):
                    cost=H*(Q(e[k]+e[l],base+1)-Q(e[k]*e[l],(base+1)*(base+2)))
                    slacks['B4-pair-to-Y',k,l] += factor*(bpair-cost)
            pref=t+sum(e[:3])
            ypair=H*(Q(e[3],pref+1+e[4])+Q(e[4],pref+1+e[3])+Q(e[3],(pref+1)*(pref+2)))
            for key, m1,m2,inter in [('11',h1,h1,h1),('12',h1,h2,h12),('22',h2,h2,h2)]:
                cost=(m1+m2)/Q(pref+1)-inter/Q((pref+1)*(pref+2))
                slacks['Y-pair-to-B4',key] += factor*(ypair-cost)
    assert len(slacks) == 198
    rows=[dict(query=k,slack=v,slack_float=float(v)) for k,v in sorted(slacks.items(),key=lambda kv:str(kv[0]))]
    report=dict(scope='Conditional-product gluing of old R/Z+B4 and root239 over the full labelled old vector; exactly 198 new terminal/SAFE/PAIR interface orbit tests. A failed row rejects only this chosen gluing.',
        point_sha256=PIN,network_sha256=sha(NET),root_sha256=sha(ROOT),script_sha256=sha(Path(__file__)),
        original_blocks_preserved=['17424 old R/Z literal queries','15 B4 orbit queries','239 nonroot and one root-source budgets'],
        old_word_joint_law='Uniform S6 orbit separately within each original hist, with exact hist mass',
        conditional_kernel=kernel,synchronous_triple_orbits=len(orbits),synchronous_frequency_checks=frequency_checks,
        new_rows=len(rows),negative=sum(r['slack']<0 for r in rows),zero=sum(r['slack']==0 for r in rows),
        positive=sum(r['slack']>0 for r in rows),minimum=min(slacks.values()),rows=rows,
        no_full_SPE_claim=True,no_general_infeasibility_claim=True)
    out=WS/'main_glued_terminal_interfaces.json'
    assert not out.exists()
    out.write_text(json.dumps(serial(report),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(serial({k:v for k,v in report.items() if k not in ('rows','conditional_kernel')}),ensure_ascii=False))


if __name__=='__main__':
    main()
