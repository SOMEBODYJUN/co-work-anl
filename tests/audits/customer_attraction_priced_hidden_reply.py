"""Independent review checks for the arbitrary-horizon priced projection.

Build full ordered-history pure SPEs in small m=6 games. Check the projection
at every true source node, every forced T and query Q, together with its exact
nonnegative-slack identity. This is a finite semantic test, not a proof of all
instances. Sorting identity is also checked against literal binary minima.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import importlib.util

ROOT=Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0,str(ROOT))
from customer_attraction import priced_hidden_reply as mech


def share(n,d):
    return F(n,d) if n else F(0)


def parameters(k,scheme):
    n=k-1
    if scheme==0:
        return (F(1,8),)*(n-1)+(F(1,5),),(F(0),)*(n-1)+(F(1,20),),F(1,4)
    if scheme==1:
        return tuple(F(j+1,j+3) for j in range(n)),tuple(F((3*j+1)%5,j+11) for j in range(n)),F(2,3)
    return (F(0),)*n,(F(0),)*n,F(0)


@lru_cache(None)
def literal_projection(p,ell,t,q,alpha,beta,mu):
    candidates=[]
    for hidden in product((0,1),repeat=len(alpha)):
        z=p+t+sum(hidden)
        value=(share(t,z)+sum(beta[j]*hidden[j] for j in range(len(alpha)))
               +sum(alpha[j]*hidden[j] for j in range(len(alpha)))/(ell+1)
               -mu*share(hidden[-1],z)+mu*F(q,p+t+sum(hidden[:-1])+1))
        candidates.append(value)
    expected=min(candidates)
    # Import only to compare with the proposed implementation.
    assert expected==mech.projected_by_count(p,ell,t,q,alpha,beta,mu)
    return expected


def solve_game(catalog,nclients,seed,m=6):
    memo={}
    @lru_cache(None)
    def terminal_payoffs(counts):
        loads=[sum(counts[a]*((catalog[a]>>x)&1) for a in range(len(catalog))) for x in range(nclients)]
        # Only played actions have a player payoff in this terminal outcome.
        return tuple(sum(share((topic>>x)&1,loads[x]) for x in range(nclients)) if counts[a] else F(0) for a,topic in enumerate(catalog))
    def solve(history):
        if len(history)==m:
            counts=tuple(history.count(a) for a in range(len(catalog)))
            outcome=history
            return outcome,terminal_payoffs(counts)
        candidates=[]
        for action in range(len(catalog)):
            outcome,payoffs=solve(history+(action,))
            candidates.append((payoffs[action],action,outcome,payoffs))
        best=max(c[0] for c in candidates)
        ties=[c for c in candidates if c[0]==best]
        # Full ordered history, not only its anonymous counts, chooses a tie.
        tie=int.from_bytes(hashlib.sha256(repr((seed,history)).encode()).digest()[:8],'big')%len(ties)
        _,action,outcome,payoffs=ties[tie]
        memo[history]=(action,outcome,payoffs)
        return outcome,payoffs
    outcome,payoffs=solve(())
    return memo,outcome,payoffs


def check_game(catalog,nclients,seed):
    memo,actual,actual_payoffs=solve_game(catalog,nclients,seed)
    K=max(topic.bit_count() for topic in catalog)
    actual_ell=[sum((catalog[a]>>x)&1 for a in actual[:-1]) for x in range(nclients)]
    um=actual_payoffs[actual[-1]]
    nodes=inequalities=0
    min_gap=None
    for history,(_,outcome,payoffs) in memo.items():
        if len(history)>4:
            continue
        nodes+=1;k=6-len(history)
        r=payoffs[outcome[len(history)]]
        p=[sum((catalog[a]>>x)&1 for a in history) for x in range(nclients)]
        for T in range(len(catalog)):
            branch,branch_payoffs=memo[history+(T,)][1:]
            followers=branch[len(history)+1:]
            vT=branch_payoffs[T]
            vLast=branch_payoffs[branch[-1]]
            prices=[sum(F((catalog[a]>>x)&1,actual_ell[x]+1) for x in range(nclients)) for a in followers]
            assert r>=vT
            assert all(um>=price for price in prices)
            for Q in range(len(catalog)):
                prefix=[sum((catalog[a]>>x)&1 for a in branch[:-1]) for x in range(nclients)]
                query=sum(F((catalog[Q]>>x)&1,prefix[x]+1) for x in range(nclients))
                assert vLast>=query
                for scheme in range(3):
                    alpha,beta,mu=parameters(k,scheme)
                    lhs=r+sum(alpha)*um+sum(beta)*K
                    rhs=F(0);projection_slack=F(0)
                    for x in range(nclients):
                        t=(catalog[T]>>x)&1;q=(catalog[Q]>>x)&1
                        f=tuple((catalog[a]>>x)&1 for a in followers)
                        psi=literal_projection(p[x],actual_ell[x],t,q,alpha,beta,mu)
                        rhs+=psi
                        z=p[x]+t+sum(f)
                        local=(share(t,z)+sum(beta[j]*f[j] for j in range(len(f)))
                               +sum(alpha[j]*f[j] for j in range(len(f)))/(actual_ell[x]+1)
                               -mu*share(f[-1],z)+mu*F(q,p[x]+t+sum(f[:-1])+1))
                        assert local>=psi
                        projection_slack+=local-psi
                    gap=lhs-rhs
                    decomposition=(r-vT+sum(alpha[j]*(um-prices[j]) for j in range(len(followers)))
                                   +sum(beta[j]*(K-catalog[a].bit_count()) for j,a in enumerate(followers))
                                   +mu*(vLast-query)+projection_slack)
                    assert gap==decomposition and gap>=0,(catalog,history,T,Q,scheme,gap,decomposition)
                    min_gap=gap if min_gap is None else min(min_gap,gap)
                    inequalities+=1
    return {'catalog_bitmasks':catalog,'clients':nclients,'tie_seed':seed,'complete_strategy_nodes':len(memo),'true_source_nodes_checked':nodes,'projected_inequalities':inequalities,'minimum_gap':str(min_gap),'actual_history':actual}


def main():
    sorting_checks=0
    # More horizons, including k=2 (no sortable early follower). Nonnegativity
    # is needed for legal use of capacity/price inequalities in the theorem.
    for k in range(2,11):
        for scheme in range(3):
            alpha,beta,mu=parameters(k,scheme)
            for p,ell,t,q in product(range(4),range(7),(0,1),(0,1)):
                literal_projection(p,ell,t,q,alpha,beta,mu)
                sorting_checks+=1
    rng=random.Random(6172026)
    catalogs=[(0,),(1,),(0,1),(1,2),(0,3),(1,2,4),(0,1,2),(0,3,5),(1,2,4,8),(0,3,5,10)]
    catalogs += [tuple(sorted(rng.sample(range(16),size))) for size in (2,3,4,4,4,4)]
    games=[]
    for seed,catalog in enumerate(catalogs):
        games.append(check_game(catalog,4,seed))
    report={'status':'passed','scope':'Finite m=6 full ordered-history SPE semantic audit plus exact sorting-vs-enumeration checks','sorting_cases':sorting_checks,'horizons':list(range(2,11)),'complete_m6_games':len(games),'true_nodes_checked':sum(g['true_source_nodes_checked'] for g in games),'projected_inequalities_checked':sum(g['projected_inequalities'] for g in games),'games':games}
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
