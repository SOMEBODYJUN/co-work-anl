"""Definition-level independent audit of the density ledger on existing SPEs.

Does not import the author's code or the canonical solver.  It replays the
stored full history policies, checks every original IC with Fraction, chooses
one lexicographic optimal tuple, and injects unit residuals on its omitted
clients.  This is a regression of identities, not evidence for a welfare bound.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement, product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'customer_attraction' / 'model.py').exists())

def audit(name):
    raw = json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text())
    packet = json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
    packet = packet.get('strategy', packet)
    sigma = {tuple(r['history']): r['action'] for r in packet['actions']}
    m, k = raw['players'], len(raw['topics'])
    clients = [frozenset(r['topics']) for r in raw['customers'] for _ in range(r['multiplicity'])]
    assert set(sigma) == {h for d in range(m) for h in product(range(k), repeat=d)}
    @lru_cache(None)
    def finish(h):
        return h if len(h) == m else finish(h + (sigma[h],))
    @lru_cache(None)
    def loads(z):
        return tuple(sum(a in likes for a in z) for likes in clients)
    def pay(z, i):
        c = loads(z)
        return sum((F(1, c[x]) for x, likes in enumerate(clients) if z[i] in likes), F())
    ic = []
    for h in sigma:
        i, z = len(h), finish(h)
        for a in range(k):
            gap = pay(z, i) - pay(finish(h+(a,)), i)
            assert gap >= 0
            ic.append(gap)
    Z = finish(())
    u = [pay(Z, i) for i in range(m)]
    def coverage(t):
        return frozenset(x for x, likes in enumerate(clients) if any(a in likes for a in t))
    candidates = [(len(coverage(t)), t) for t in combinations_with_replacement(range(k), m)]
    opt = max(v for v, t in candidates)
    Topt = min(t for v, t in candidates if v == opt)
    R = sorted(coverage(Topt) - coverage(Z))
    owner = {x: next(i for i,a in enumerate(Topt) if a in clients[x]) for x in R}
    src, f = defaultdict(lambda: defaultdict(F)), defaultdict(lambda: defaultdict(F))
    for x in R:
        q = (owner[x], Topt[owner[x]])
        src[q][x] += 1
        f[q][x] += 1
    M = F(len(R))
    H = absorb = Ksrc = Kin = Jsum = Tsum = Csum = Lsum = F()
    contexts = nonzero_cov = positive_cov_charge = negative_cov_charge = positive_return = negative_return = positive_slack = 0
    states = 0
    for i in range(m):
        for q in sorted(q for q in f if q[0] == i):
            density = dict(f[q]); a = q[1]
            B = finish(Z[:i]+(a,)); cB = loads(B); Dq = pay(B, i)
            Aabs = sum((v / cB[x] for x,v in density.items()), F())
            assert Aabs > 0 and Dq > 0 and Dq <= u[i]
            states += 1
            absorb += Aabs
            H += sum((v / (cB[x]**2) for x,v in density.items()), F())
            Ksrc += u[i] * sum((v/cB[x] for x,v in src[q].items()),F()) / Dq
            for j in range(i+1,m):
                b = B[j]
                incoming = {x: v/cB[x] for x,v in density.items() if b in clients[x]}
                if not incoming:
                    continue
                contexts += 1
                child = (j,b)
                for x,v in incoming.items():
                    assert cB[x] >= 2
                    f[child][x] += v
                h = B[:j]
                assert sigma[h] == b and finish(h) == B
                A = finish(Z[:j]+(b,)); W = finish(h+(Z[j],))
                cA, cW = loads(A), loads(W)
                D, vB, vW = pay(A,j), pay(B,j), pay(W,j)
                ell = vB-vW
                assert ell >= 0 and D > 0 and D <= u[j]
                theta = sum((v/cA[x] for x,v in incoming.items()),F())/D
                J = sum((v/cB[x] for x,v in incoming.items()),F())
                full_action = [x for x,likes in enumerate(clients) if b in likes]
                assert sum((F(1,cA[x])/D for x in full_action),F()) == 1
                ef = sum((F(1,cA[x])/D*incoming.get(x,F()) for x in full_action),F())
                er = sum((F(1,cA[x])/D*F(cA[x],cB[x]) for x in full_action),F())
                efr = sum((F(1,cA[x])/D*incoming.get(x,F())*F(cA[x],cB[x]) for x in full_action),F())
                covcharge = -D*(efr-ef*er)
                directcharge = sum(((theta-incoming.get(x,F()))/cB[x] for x in full_action),F())
                assert ef == theta and covcharge == directcharge == theta*vB-J
                ret, loss, cost = theta*(u[j]-vW), theta*ell, theta*u[j]
                assert cost == J+ret+covcharge-loss
                assert J <= sum(incoming.values(),F())/2
                nonzero_cov += bool(covcharge)
                positive_cov_charge += covcharge > 0
                negative_cov_charge += covcharge < 0
                positive_return += ret > 0
                negative_return += ret < 0
                positive_slack += loss > 0
                Kin += cost; Jsum += J; Tsum += ret; Csum += covcharge; Lsum += loss
    assert absorb == M
    assert Jsum == M-H
    assert Kin == M-H+Tsum+Csum-Lsum
    assert Ksrc+Kin-M == Ksrc-H+Tsum+Csum-Lsum
    assert H >= 0 and Lsum >= 0
    return dict(case=name, customers=len(clients), players=m, topics=k,
                original_IC_comparisons=len(ic), original_minimum_IC=str(min(ic)),
                actual=list(Z), optimal_tuple=list(Topt), OPT=opt,
                actual_payoffs=list(map(str,u)), residual_rule='all omitted clients have rho=1',
                M=str(M), states=states, natural_parent_contexts=contexts,
                K_source=str(Ksrc), K_incoming=str(Kin), H=str(H), diagonal_total=str(Jsum),
                actual_return_T=str(Tsum), covariance_COV=str(Csum), offhistory_slack_L=str(Lsum),
                nonzero_covariance_contexts=nonzero_cov,
                positive_covariance_charge_contexts=positive_cov_charge,
                negative_covariance_charge_contexts=negative_cov_charge,
                positive_actual_return_contexts=positive_return,
                negative_actual_return_contexts=negative_return,
                positive_offhistory_slack_contexts=positive_slack,
                local_and_global_identities_exact=True)

out = dict(status='passed',
           scope='independent definition-level replay of three existing complete policies; no new instances or general cost bound',
           reports=[audit(n) for n in ('root_tax_failure','individual_security_failure','portfolio_matching_failure')],
           proves_half=False, proves_general_budget=False)
path = HERE/'density_ledger_independent_audit.json'
with path.open('x',encoding='utf-8') as f:
    json.dump(out,f,ensure_ascii=False,indent=2); f.write('\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
