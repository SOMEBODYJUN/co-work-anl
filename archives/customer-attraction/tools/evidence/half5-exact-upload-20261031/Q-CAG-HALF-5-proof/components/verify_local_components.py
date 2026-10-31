#!/usr/bin/env python3
"""Portable exact verification of local lemmas for the five-provider proof.
Standard library only. Reads the seven JSON files beside this script.
Reconstructs literal payoffs and legal-history coefficient rows; imports no
solver, discovery implementation, repository module, or global certificate.
All arithmetic that decides a claim uses fractions.Fraction.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
REPORT = []
SOURCES = {}

def load(name):
    path = HERE / name
    data = path.read_bytes()
    SOURCES[name] = hashlib.sha256(data).hexdigest()
    return json.loads(data)

def sh(n, d):
    """A literal share; the zero numerator convention avoids any 0/0."""
    return F(n, d) if n else F(0)

def states(names):
    for bits in product((0, 1), repeat=len(names)):
        yield dict(zip(names, bits))

def binary(b, names):
    ans = 0
    for name in names:
        ans = 2 * ans + b[name]
    return ans

def check_multipliers(lam):
    assert lam and all(v >= 0 for v in lam.values())

def add_report(family, index, count, zeros, **extra):
    REPORT.append(dict(family=family, index=index, types=count,
                       zero_residuals=zeros, verified=True, **extra))


def verify_deep():
    """Root forced T, then true Q deviations at players 2,3,4."""
    cuts = load('deep_root_query.json')
    names = 'TABCDEFGQHIJ'
    paths = ('TABCD', 'TAQEF', 'TABQG', 'TQHIJ')
    first_optimizing_index = {'TABCD': 1, 'TAQEF': 3,
                              'TABQG': 4, 'TQHIJ': 2}
    def value(b, path, i):
        return sh(b[path[i]], sum(b[s] for s in path))
    def raw(b, key):
        z = key.split(':')
        if z[0] == 'CAP':
            return F(b[z[1]])
        if key == 'ROOT':
            return value(b, 'TABCD', 0)
        if z[0] == 'IC':
            prefix, own, query = z[1:]
            path = next(p for p in paths if p.startswith(prefix + own))
            i = len(prefix)
            assert i >= first_optimizing_index[path]
            return sh(b[query], sum(b[s] for s in prefix) + 5-i) - value(b, path, i)
        if key == 'TRUE2':
            return value(b, 'TQHIJ', 1) - value(b, 'TABCD', 1)
        if key == 'TRUE3':
            return value(b, 'TAQEF', 2) - value(b, 'TABCD', 2)
        if key == 'TRUE4':
            return value(b, 'TABQG', 3) - value(b, 'TABCD', 3)
        if z[0] == 'TAX':
            pref, query = z[1:]
            path = next(p for p in paths if p.startswith(pref))
            assert len(pref) == 3 and path != 'TABQG'
            p = sum(b[s] for s in pref)
            n = sum(b[s] for s in query)
            H = value(b, path, 3) + value(b, path, 4) + sh(b[path[3]], (p+1)*(p+2))
            return sh(n, p+n) - H
        raise AssertionError(key)
    for i, c in enumerate(cuts):
        assert c['query_deviations'] is True
        lam = {k: F(v) for k, v in c['multipliers'].items()}
        check_multipliers(lam)
        assert lam['ROOT'] == F(c['alpha']) > 0
        assert sum(v for k, v in lam.items() if k.startswith('CAP:')) == F(c['beta'])
        gamma, zeta = F(c['gamma']), F(c['zeta'])
        zeros = 0
        for b in states(names):
            inter = b['T'] * b['Q']
            rho = sum(v*raw(b, k) for k, v in lam.items()) + gamma*b['T'] + zeta*inter - (b['Q']-inter)
            assert rho >= 0, ('DEEP', i, b, rho)
            zeros += rho == 0
        assert zeros == c['zero_types']
        add_report('DEEP', i, 4096, zeros)


def verify_background2():
    """Actual prefix A; forced T and true Q deviations at players 3,4."""
    cuts = load('background_player2.json')
    names = 'ATQBCDEFG'
    paths = ('TBCD', 'TQEF', 'TBQG')
    def value(b, path, i):
        return sh(b[path[i]], b['A'] + sum(b[s] for s in path))
    def raw(b, key):
        z = key.split(':')
        if z[0] == 'CAP':
            return F(b[z[1]])
        if key == 'TRUE3':
            return value(b, 'TQEF', 1) - value(b, 'TBCD', 1)
        if key == 'TRUE4':
            return value(b, 'TBQG', 2) - value(b, 'TBCD', 2)
        if z[0] == 'IC':
            prefix, own, query = z[1:]
            path = next(p for p in paths if p.startswith(prefix + own))
            i = len(prefix)
            assert i >= {'TBCD': 1, 'TQEF': 2, 'TBQG': 3}[path]
            return sh(b[query], b['A'] + sum(b[s] for s in prefix) + 4-i) - value(b, path, i)
        raise AssertionError(key)
    for i, c in enumerate(cuts):
        lam = {k: F(v) for k, v in c['multipliers'].items()}
        check_multipliers(lam)
        assert sum(v for k, v in lam.items() if k.startswith('CAP:')) == F(c['Kcoef'])
        gamma = [F(0)] + [F(v) for v in c['margin_coefs']]
        zeros = 0
        for b in states(names):
            rho = value(b, 'TBCD', 0) + sum(v*raw(b, k) for k, v in lam.items()) - gamma[binary(b, 'ATQ')]
            assert rho >= 0, ('BG2', i, b, rho)
            zeros += rho == 0
        assert zeros == c['zero_types']
        add_report('BG2', i, 512, zeros)


def verify_background3():
    """Ordered AB; forced T and true fourth-player queries/copy."""
    cuts = load('background_player3.json')
    names = 'ABTQCDEF'
    paths = {'TC': 'TCD', 'TQ': 'TQE', 'TD': 'TDF', 'T': 'TCD'}
    def value(b, path, i):
        return sh(b[path[i]], b['A']+b['B'] + sum(b[s] for s in path))
    def raw(b, key):
        z = key.split(':')
        p = b['A']+b['B']
        if z[0] == 'CAP':
            return F(b[z[1]])
        if z[0] == 'IC':
            pref, own, query = z[1:]
            path = paths[pref]
            i = len(pref)
            assert path[i] == own and i >= 1
            if path != 'TCD':
                assert i == 2
            return sh(b[query], p+sum(b[s] for s in pref)+3-i)-value(b, path, i)
        if key == 'TRUE4-Q':
            return value(b, 'TQE', 1)-value(b, 'TCD', 1)
        if key == 'TRUE4-D':
            return value(b, 'TDF', 1)-value(b, 'TCD', 1)
        if z[0] == 'TAX':
            n = sum(b[s] for s in z[1])
            pref = p+b['T']
            H = value(b, 'TCD', 1)+value(b, 'TCD', 2)+sh(b['C'], (pref+1)*(pref+2))
            return sh(n, pref+n)-H
        raise AssertionError(key)
    for i, c in enumerate(cuts):
        lam = {k: F(v) for k, v in c['weights'].items()}
        check_multipliers(lam)
        assert sum(v for k, v in lam.items() if k.startswith('CAP:')) == F(c['beta_K'])
        gamma = [F(v) for v in c['gamma_ABTQ']]
        zeros = 0
        for b in states(names):
            rho = value(b, 'TCD', 0)+sum(v*raw(b, k) for k, v in lam.items())-gamma[binary(b, 'ABTQ')]
            assert rho >= 0, ('BG3', i, b, rho)
            zeros += rho == 0
        add_report('BG3', i, 256, zeros)


def verify_priced2():
    """Actual ABCD prices and the true second-player forced-T subtree."""
    cuts = load('priced_player2.json')
    names = 'ABCDTQEFGHIJ'
    paths = {'init': 'TEFG', 'third': 'TQHI', 'fourth': 'TEQJ'}
    def value(b, tag, i):
        path = paths[tag]
        return sh(b[path[i]], b['A']+sum(b[s] for s in path))
    def raw(b, key):
        z = key.split(':')
        if z[0] == 'CAP':
            return F(b[z[1]])
        if z[0] == 'ACTUAL':
            i = int(z[1])-1
            return sh(b[z[2]], sum(b[s] for s in 'ABCD'[:i])+5-i)
        if z[0] == 'IC':
            tag, i, query = z[1], int(z[2]), z[3]
            assert i >= {'init': 1, 'third': 2, 'fourth': 3}[tag]
            pref = b['A']+sum(b[s] for s in paths[tag][:i])
            return sh(b[query], pref+4-i)-value(b, tag, i)
        if key == 'TRUE3':
            return value(b, 'third', 1)-value(b, 'init', 1)
        if key == 'TRUE4':
            return value(b, 'fourth', 2)-value(b, 'init', 2)
        if z[0] == 'TAX':
            tag, query = z[1:]
            path = paths[tag]
            pref = b['A']+b[path[0]]+b[path[1]]
            n = sum(b[s] for s in query)
            H = value(b, tag, 2)+value(b, tag, 3)+sh(b[path[2]], (pref+1)*(pref+2))
            return sh(n, pref+n)-H
        raise AssertionError(key)
    for i, c in enumerate(cuts):
        lam = {k: F(v) for k, v in c['multipliers'].items()}
        check_multipliers(lam)
        assert sum(v for k, v in lam.items() if k.startswith('CAP:')) == F(c['Kcoef'])
        for player in range(5):
            assert sum((v for k, v in lam.items() if k.startswith('ACTUAL:'+str(player+1)+':')), F(0)) == F(c['u_coefs'][player])
        gamma = [F(v) for v in c['gamma']]
        zeros = 0
        for b in states(names):
            rho = value(b, 'init', 0)+sum(v*raw(b, k) for k, v in lam.items())-gamma[binary(b, 'ABCDTQ')]
            assert rho >= 0, ('PC2', i, b, rho)
            zeros += rho == 0
        assert zeros == c['zero_types']
        add_report('PC2', i, 4096, zeros)


def verify_priced3():
    """Actual ABCD prices and the true third-player forced-T subtree."""
    cuts = load('priced_player3.json')
    names = 'ABCDTQEFGH'
    paths = {'init': 'TEF', 'query': 'TQG', 'copy': 'TFH'}
    def value(b, tag, i):
        path = paths[tag]
        return sh(b[path[i]], b['A']+b['B']+sum(b[s] for s in path))
    def raw(b, key):
        z = key.split(':')
        if z[0] == 'CAP':
            return F(b[z[1]])
        if z[0] == 'ACTUAL':
            i = int(z[1])-1
            return sh(b[z[2]], sum(b[s] for s in 'ABCD'[:i])+5-i)
        if z[0] == 'IC':
            tag, i, query = z[1], int(z[2]), z[3]
            assert i >= {'init': 1, 'query': 2, 'copy': 2}[tag]
            pref = b['A']+b['B']+sum(b[s] for s in paths[tag][:i])
            return sh(b[query], pref+3-i)-value(b, tag, i)
        if key == 'TRUE4-F':
            return value(b, 'copy', 1)-value(b, 'init', 1)
        if key == 'TRUE4-Q':
            return value(b, 'query', 1)-value(b, 'init', 1)
        raise AssertionError(key)
    for i, c in enumerate(cuts):
        lam = {k: F(v) for k, v in c['weights'].items()}
        check_multipliers(lam)
        assert sum(v for k, v in lam.items() if k.startswith('CAP:')) == F(c['Kcoef'])
        for player in range(5):
            assert F(player == 2)+sum((v for k, v in lam.items() if k.startswith('ACTUAL:'+str(player+1)+':')), F(0)) == F(c['u_coefficients'][player])
        gamma = [F(v) for v in c['gamma_ABCDTQ']]
        zeros = 0
        for b in states(names):
            rho = value(b, 'init', 0)+sum(v*raw(b, k) for k, v in lam.items())-gamma[binary(b, 'ABCDTQ')]
            assert rho >= 0, ('PC3', i, b, rho)
            zeros += rho == 0
        add_report('PC3', i, 1024, zeros)


def verify_maxroot():
    """Maximum root T, true two nested copy-D branches, OPT bit cancels."""
    cuts = load('maxroot_four_copy.json')
    names = 'TABCDQRSXY'
    paths = {'actual': 'ABCD', 'root': 'DQRS', 'second': 'ADXY'}
    def value(b, tag, i):
        path = paths[tag]
        return sh(b[path[i]], b['T']+sum(b[s] for s in path))
    def nonnegative_row(b, o, key):
        z = key.split(':')
        if z[0] == 'CAP':
            return F(b['T']-b[z[1]])
        if z[0] == 'copy':
            i = {'root': 0, 'second': 1}[z[1]]
            return value(b, 'actual', i)-value(b, z[1], i)
        tag, path = z[0], paths[z[0]]
        if z[1].isdigit():
            i = int(z[1])
            assert i >= {'actual': 0, 'root': 1, 'second': 2}[tag]
            return value(b, tag, i)-sh(b[z[3]], b['T']+sum(b[s] for s in path[:i])+4-i)
        if z[1] == 'pairO':
            p = b['T']+b[path[0]]+b[path[1]]
            H = value(b, tag, 2)+value(b, tag, 3)+sh(b[path[2]], (p+1)*(p+2))
            return F(5,2)*H+sh(p,p+1)-o
        if z[1] == 'lastO':
            p = b['T']+sum(b[s] for s in path[:3])
            return 5*value(b, tag, 3)+sh(p,p+1)-o
        raise AssertionError(key)
    for i, c in enumerate(cuts):
        B, C = F(c['B']), F(c['C'])
        lam = {k: F(v) for k, v in c['multipliers'].items()}
        check_multipliers(lam)
        assert B > 0
        assert sum(v for k, v in lam.items() if k.endswith(':pairO') or k.endswith(':lastO')) == 1
        zeros = 0
        for b in states(names):
            vT = sh(b['T'], sum(b[s] for s in 'TABCD'))
            rho = B*vT+C*b['T']-sum(v*nonnegative_row(b,0,k) for k,v in lam.items())
            assert rho >= 0, ('MAXROOT', i, b, rho)
            assert (rho*245803508760).denominator == 1
            rho1 = B*vT+C*b['T']-1-sum(v*nonnegative_row(b,1,k) for k,v in lam.items())
            assert rho1 == rho
            zeros += rho == 0
        add_report('MAXROOT', i, 1024, zeros, comparison_bit_cancels=True)


def verify_max_background():
    """Optional maximum-source player-2 envelope; unused fourth reply removed."""
    c = load('max_background_player2.json')
    names = 'ATBCDEF'
    paths = {'init': 'TBCD', 'third': 'TDEF'}
    lam = {k:F(v) for k,v in c['multipliers'].items()}
    check_multipliers(lam)
    B,C,Ac,gT,gA = (F(c[k]) for k in ('B','C','Acoef','gammaT','gammaA'))
    assert B == lam['FORCED'] and Ac == gA
    assert C == gT+sum(v for k,v in lam.items() if k.startswith('CAP:'))
    def value(b,tag,i):
        path=paths[tag]
        return sh(b[path[i]],b['A']+sum(b[s] for s in path))
    def raw(b,d,key):
        z=key.split(':')
        if z[0]=='CAP':return F(b[z[1]])
        if key=='FORCED':return value(b,'init',0)
        if key=='TRUE3':return value(b,'third',1)-value(b,'init',1)
        if z[0] in ('IC','OPT'):
            tag,i=z[1],int(z[2])
            assert i>= {'init':1,'third':2}[tag]
            den=b['A']+sum(b[s] for s in paths[tag][:i])+4-i
            return (sh(b[z[3]],den)-value(b,tag,i)) if z[0]=='IC' else (sh(d,den)-5*value(b,tag,i))
        if z[:2]==['PAIR','OPT']:
            tag=z[2];path=paths[tag];p=b['A']+b[path[0]]+b[path[1]]
            H=value(b,tag,2)+value(b,tag,3)+sh(b[path[2]],(p+1)*(p+2))
            return sh(d*(5-d),p+1)+sh(d*(d-1),p+2)-10*H
        raise AssertionError(key)
    zeros=0
    for b in states(names):
        for d in range(6):
            rho=sum(v*raw(b,d,k) for k,v in lam.items())+gT*b['T']+gA*b['A']-(d>0)
            assert rho>=0,('MAX-BG2',b,d,rho)
            zeros+=rho==0
    assert 2*zeros==c['zero_types']
    add_report('MAX-BG2',0,768,zeros,unused_reply_removed=True)


def main():
    start=time.perf_counter()
    verify_deep()
    verify_background2()
    verify_background3()
    verify_priced2()
    verify_priced3()
    verify_maxroot()
    verify_max_background()
    print(json.dumps(dict(status='ALL LOCAL COMPONENTS VERIFIED EXACTLY',
                         arithmetic='Python standard-library fractions.Fraction',
                         component_count=len(REPORT),
                         coefficient_states=sum(v['types'] for v in REPORT),
                         input_sha256=SOURCES,
                         checks=REPORT,
                         elapsed_seconds=round(time.perf_counter()-start,3)),
                     ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
