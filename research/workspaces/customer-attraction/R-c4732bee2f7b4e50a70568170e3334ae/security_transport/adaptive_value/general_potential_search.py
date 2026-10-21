"""Does aggregate security follow from symmetric exact potential alone?

Auxiliary model: u_i(z)=F(count(z))-C(count(z minus i)).  This is a
symmetric exact-potential game, but generally not a customer-attraction game.
"""
from itertools import product, combinations_with_replacement
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog


def run(iterations=1000, topics=3, players=3, seed=31):
    rng = np.random.default_rng(seed)
    terminals = list(combinations_with_replacement(range(topics), players))
    backgrounds = list(combinations_with_replacement(range(topics), players-1))
    tid = {z:i for i,z in enumerate(terminals)}
    bid = {z:i+len(terminals) for i,z in enumerate(backgrounds)}
    dim = len(terminals)+len(backgrounds)

    def row(a, z):
        z = sorted(z)
        z.remove(a)
        result = np.zeros(dim)
        result[tid[tuple(sorted(z+[a]))]] = 1
        result[bid[tuple(z)]] = -1
        return result

    all_utilities = np.array([row(a,z) for z in terminals for a in set(z)])
    beta = np.array([[row(a,B+(a,)) for a in range(topics)] for B in backgrounds])
    histories = [h for d in range(players) for h in product(range(topics), repeat=d)]
    best = 0.
    for iteration in range(iterations):
        sigma = {h:int(rng.integers(topics)) for h in histories}
        p = rng.dirichlet(np.ones(topics))
        def terminal(h):
            while len(h)<players:
                h += (sigma[h],)
            return h
        gamma = np.array([row(sigma[h],terminal(h))-row(a,terminal(h+(a,)))
                          for h in histories for a in range(topics)])
        z = terminal(())
        total = sum(row(a,z) for a in z)
        for repeat in range(5):
            bp = np.einsum('bad,a->bd', beta,p)
            result = linprog(np.r_[total,-players],
                A_ub=np.r_[np.c_[-gamma,np.zeros(len(gamma))],
                          np.c_[-all_utilities,np.zeros(len(all_utilities))],
                          np.c_[all_utilities,np.zeros(len(all_utilities))],
                          np.c_[-bp,np.ones(len(backgrounds))]],
                b_ub=np.r_[np.zeros(len(gamma)+len(all_utilities)),
                           np.ones(len(all_utilities)),np.zeros(len(backgrounds))],
                bounds=[(None,None)]*(dim+1),method='highs')
            if not result.success:
                raise RuntimeError(result.message)
            gap=-result.fun
            if gap>best+1e-8:
                best=gap
                print('best',gap,'iteration',iteration,flush=True)
                data={'topics':topics,'players':players,'terminals':terminals,'backgrounds':backgrounds,
                      'F':result.x[:len(terminals)].tolist(),'C':result.x[len(terminals):dim].tolist(),
                      'sigma':[dict(history=h,action=a) for h,a in sigma.items()],
                      'query':p.tolist(),'gap':gap,'value':result.x[-1],
                      'total':float(total@result.x[:-1])}
                Path(__file__).with_name('general_potential_best.json').write_text(json.dumps(data,indent=2))
            if gap>1e-7:
                return
            mat=np.einsum('bad,d->ba',beta,result.x[:-1])
            primal=linprog(np.r_[np.zeros(topics),-1],A_ub=np.c_[-mat,np.ones(len(backgrounds))],
                b_ub=np.zeros(len(backgrounds)),A_eq=np.array([[1.]*topics+[0]]),b_eq=[1],
                bounds=[(0,None)]*topics+[(None,None)],method='highs')
            p=primal.x[:-1]
    print('finished best',best,flush=True)

if __name__=='__main__':
    run()
