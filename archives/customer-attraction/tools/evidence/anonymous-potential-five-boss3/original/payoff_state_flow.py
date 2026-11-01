"""Exploratory full-depth payoff-state transport. Floating LP only unless checked.

An incentive row is an arc from (deviation terminal counts, chosen theme)
to (prescribed terminal counts, prescribed theme). Ordered histories are
retained until these payoff-identical endpoints are formed.
"""
from itertools import product, combinations_with_replacement
from fractions import Fraction
from pathlib import Path
import json
import random
import argparse
from math import lcm
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


def counts(history, topics):
    return tuple(history.count(a) for a in range(topics))


def recover_basic(matrix,rhs,floating,denominator_bound):
    """Exact elimination on the positive support of a floating basic solution.

Matrix entries are integer linear combinations of query coordinates, so their
denominators divide the known query denominator. This is not blind rational
reconstruction of unknown data.
"""
    support=[j for j,x in enumerate(floating) if x>1e-8]
    dense=matrix[:,support].toarray()
    basis={}
    for values,right in zip(dense,rhs):
        row=[Fraction(float(x)).limit_denominator(denominator_bound) for x in values]+[Fraction(right)]
        for pivot,old in sorted(basis.items()):
            coefficient=row[pivot]
            if coefficient:row=[x-coefficient*y for x,y in zip(row,old)]
        pivot=next((j for j,x in enumerate(row[:-1]) if x),None)
        if pivot is None:
            if row[-1]:return None
        else:
            coefficient=row[pivot]
            basis[pivot]=[x/coefficient for x in row]
    if len(basis)!=len(support):return None
    solution=[Fraction(0)]*len(support)
    for pivot,row in sorted(basis.items(),reverse=True):
        solution[pivot]=row[-1]-sum(row[j]*solution[j] for j in range(pivot+1,len(support)))
    exact=[Fraction(0)]*len(floating)
    for j,x in zip(support,solution):exact[j]=x
    return exact if all(x>=0 for x in exact) else None


class PayoffGraph:
    def __init__(self, topics, players, actions, monotone=False):
        self.p, self.n = topics, players
        self.actions = actions
        self.terminals = {}
        for depth in range(players, -1, -1):
            for h in product(range(topics), repeat=depth):
                self.terminals[h] = (counts(h, topics) if depth == players else
                                     self.terminals[h + (actions[h],)])
        self.root = self.terminals[()]
        self.vertices = [(q, a) for q in map(lambda h: counts(h, topics),
                             combinations_with_replacement(range(topics), players))
                         for a in range(topics) if q[a]]
        self.index = {v: i for i, v in enumerate(self.vertices)}
        self.edges = {}
        for h, b in actions.items():
            head = (self.terminals[h], b)
            for a in range(topics):
                tail = (self.terminals[h + (a,)], a)
                if tail != head:
                    self.edges.setdefault((tail, head), (h, a, 'incentive'))
        if monotone:
            for q, a in self.vertices:
                for r, b in self.vertices:
                    if a == b and q != r and q[a] >= r[a] and all(
                            q[c] <= r[c] for c in range(topics) if c != a):
                        self.edges.setdefault(((q, a), (r, a)), ((), a, 'monotone'))
        self.backgrounds = [counts(h, topics) for h in
                            combinations_with_replacement(range(topics), players - 1)]

    def solve(self, query, potential=False):
        """Solve root-demand minus independent-query supply = arc divergence."""
        edges = list(self.edges)
        nv, ne, nb = len(self.vertices), len(edges), len(self.backgrounds)
        rr, cc, vv = [], [], []
        for j, (tail, head) in enumerate(edges):
            rr += [self.index[head], self.index[tail]]
            cc += [j, j]
            vv += [1, -1]
        for j, b in enumerate(self.backgrounds):
            for a, mass in enumerate(query):
                q = list(b); q[a] += 1
                rr.append(self.index[(tuple(q), a)])
                cc.append(ne + j)
                vv.append(self.n * float(mass))
            rr.append(nv); cc.append(ne + j); vv.append(1)
        rhs = [self.root[a] if q == self.root else 0 for q, a in self.vertices] + [1]
        matrix = coo_matrix((vv, (rr, cc)), shape=(nv + 1, ne + nb)).tocsr()
        if potential:
            phis=list(dict.fromkeys([q for q,a in self.vertices]+self.backgrounds))
            phi_index={q:i for i,q in enumerate(phis)}
            tr,tc,tv=[],[],[]
            for j,(q,a) in enumerate(self.vertices):
                b=list(q);b[a]-=1
                tr.extend([phi_index[q],phi_index[tuple(b)]])
                tc.extend([j,j]);tv.extend([1,-1])
            tr.append(len(phis));tc.append(nv);tv.append(1)
            projection=coo_matrix((tv,(tr,tc)),shape=(len(phis)+1,nv+1)).tocsr()
            matrix=projection@matrix
            rhs=list(projection@np.array(rhs))
        result = linprog([1] * ne + [0] * nb,
                         A_eq=matrix, b_eq=rhs, bounds=(0, None), method='highs')
        if result.success:
            exact=recover_basic(matrix,rhs,result.x,lcm(*(x.denominator for x in query)))
            if exact is None:
                exact = [Fraction(float(x)).limit_denominator(10**8) for x in result.x]
            residual = [Fraction(0) for _ in range(nv + 1)]
            for x, (tail, head) in zip(exact[:ne], edges):
                residual[self.index[head]] += x
                residual[self.index[tail]] -= x
            for x, b in zip(exact[ne:], self.backgrounds):
                for a, mass in enumerate(query):
                    q = list(b); q[a] += 1
                    residual[self.index[(tuple(q), a)]] += self.n * mass * x
                residual[nv] += x
            if potential:
                projected=[Fraction(0) for _ in phis]+[residual[-1]]
                for v,(q,a) in zip(residual[:-1],self.vertices):
                    b=list(q);b[a]-=1
                    projected[phi_index[q]]+=v;projected[phi_index[tuple(b)]]-=v
                residual=projected
            exact_ok = all(x >= 0 for x in exact) and residual == list(map(Fraction, rhs))
            return {'success': True, 'exact_ok': exact_ok,
                    'arc_support': sum(bool(x) for x in exact[:ne]),
                    'backgrounds': [(list(b), str(x)) for b, x in zip(self.backgrounds, exact[ne:]) if x],
                    'flow': [(list(t[0]),t[1],list(h[0]),h[1],str(x),self.edges[(t,h)])
                             for (t,h), x in zip(edges,exact[:ne]) if x]}
        return {'success': False, 'status': result.message}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--certificate')
    parser.add_argument('--topics',type=int,default=3)
    parser.add_argument('--players',type=int,default=3)
    parser.add_argument('--samples',type=int,default=100)
    parser.add_argument('--monotone',action='store_true')
    parser.add_argument('--random-query',action='store_true')
    parser.add_argument('--potential',action='store_true')
    args=parser.parse_args()
    if args.certificate:
        cert=json.loads(Path(args.certificate).read_text())
        actions={tuple(x['history']):x['action'] for x in cert['actions']}
        p=max(max(h,default=-1) for h in actions)+1
        n=max(map(len,actions))+1
        graph=PayoffGraph(p,n,actions,args.monotone)
        print(json.dumps(graph.solve([Fraction(1,p)]*p,args.potential),indent=2))
        return
    rng=random.Random(20261021)
    passed=0
    for iteration in range(args.samples):
        actions={h:rng.randrange(args.topics) for d in range(args.players)
                 for h in product(range(args.topics),repeat=d)}
        graph=PayoffGraph(args.topics,args.players,actions,args.monotone)
        query=[rng.randrange(1,100) for _ in range(args.topics)] if args.random_query else [1]*args.topics
        query=[Fraction(x,sum(query)) for x in query]
        result=graph.solve(query,args.potential)
        if not result['success'] or not result['exact_ok']:
            print(json.dumps({'iteration':iteration,'query':list(map(str,query)),'result':result,'actions':
                              [{'history':h,'action':a} for h,a in actions.items()]},indent=2))
            break
        passed+=1
    print(json.dumps({'passed':passed,'monotone':args.monotone}))


if __name__=='__main__':main()
