"""Independent literal Fraction checks of rooted incidence-tree privatization.

This is a finite diagnostic, not a proof. No repository imports or network calls.
The resource cost/deviation evaluator does not use the computed tariffs.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from random import Random
import json
import hashlib
from pathlib import Path
import sys


@dataclass
class Game:
    weights: dict
    strategies: dict
    coeffs: dict

    def val(self, e, x):
        return sum((a*x**k for k, a in enumerate(self.coeffs[e])), F(0))

    def incident(self, i):
        return set().union(*self.strategies[i])

    def users(self, e):
        return {i for i in self.weights if e in self.incident(i)}

    def cost(self, i, state):
        # Literal load recomputation, with no tariff/DP calls.
        return sum((self.val(e, sum((self.weights[j] for j in self.weights
                                    if e in state.get(j,())), F(0)))
                    for e in state[i]), F(0))

    def deviations(self, state, alpha=F(1)):
        bad=[]
        for i in self.weights:
            current=self.cost(i,state)
            for t in self.strategies[i]:
                other=dict(state)
                other[i]=t
                if current>alpha*self.cost(i,other):
                    bad.append((i,t,current,self.cost(i,other)))
        return bad


class PlayerPlan:
    def __init__(self, game, i, parent_e=None):
        self.g=game
        self.i=i
        self.parent=parent_e
        self.children={e:ResourcePlan(game,e,i)
                       for e in sorted(game.incident(i)-{parent_e})}
        self.options={}
        for b in (0,1):
            candidates=[]
            for s in game.strategies[i]:
                if parent_e is not None and int(parent_e in s)!=b:
                    continue
                v=sum((self.children[e].q for e in s if e!=parent_e),F(0))
                candidates.append((v,tuple(sorted(s)),s))
            self.options[b]=min(candidates,key=lambda v:v[:2]) if candidates else None

    def realize(self,b):
        option=self.options[b]
        assert option is not None
        state={self.i:option[2]}
        for e,plan in self.children.items():
            state.update(plan.realize(int(e in option[2])))
        return state


class ResourcePlan:
    def __init__(self, game, e, parent_i):
        self.g=game
        self.e=e
        self.parent=parent_i
        self.children={i:PlayerPlan(game,i,e)
                       for i in sorted(game.users(e)-{parent_i})}
        self.q=game.val(e,game.weights[parent_i]+self.load(game.weights[parent_i]))

    def choices(self,x):
        chosen={}
        load=F(0)
        optional=[]
        for i,p in self.children.items():
            if p.options[0] is None:
                chosen[i]=1
                load+=self.g.weights[i]
            elif p.options[1] is None:
                chosen[i]=0
            else:
                chosen[i]=0
                optional.append((p.options[0][0]-p.options[1][0],i))
        optional.sort(key=lambda z:(-z[0],z[1]))
        for delta,i in optional:
            if self.g.val(self.e,x+load+self.g.weights[i])<=delta:
                chosen[i]=1
                load+=self.g.weights[i]
        return chosen,load

    def load(self,x):
        return self.choices(x)[1]

    def realize(self,b):
        chosen,_=self.choices(self.g.weights[self.parent]*b)
        state={}
        for i,p in self.children.items():
            state.update(p.realize(chosen[i]))
        return state

    def verify_recursive(self):
        # Actual descendant costs and deviations while parent inclusion is fixed.
        for b in (0,1):
            desc=self.realize(b)
            state=dict(desc)
            state[self.parent]=frozenset({self.e}) if b else frozenset()
            for i in desc:
                current=self.g.cost(i,state)
                for t in self.g.strategies[i]:
                    deviated=dict(state)
                    deviated[i]=t
                    assert current<=self.g.cost(i,deviated)
        absent=self.realize(0)
        present=self.realize(1)
        absent[self.parent]=frozenset({self.e})
        present[self.parent]=frozenset({self.e})
        # Cost on root resource only; parent's other branches are outside this test.
        cost_abs=self.g.val(self.e,sum((self.g.weights[j] for j in absent
                                      if self.e in absent[j]),F(0)))
        cost_pre=self.g.val(self.e,sum((self.g.weights[j] for j in present
                                      if self.e in present[j]),F(0)))
        assert cost_pre==self.q<=cost_abs
        xs=[F(k,3) for k in range(49)]
        loads=[self.load(x) for x in xs]
        assert all(a>=b for a,b in zip(loads,loads[1:]))
        count=1
        for p in self.children.values():
            for r in p.children.values():
                count+=r.verify_recursive()
        return count


def random_tree(rng,n):
    # Grow an actual bipartite tree, maintaining all intended incidence edges.
    adjp={0:set()}
    adje={}
    nextp,nexte=1,0
    while nextp<n or not adje:
        if nextp==n or (not adje) or rng.randrange(2):
            i=rng.choice(list(adjp))
            adjp[i].add(nexte)
            adje[nexte]={i}
            nexte+=1
        else:
            e=rng.choice(list(adje))
            adje[e].add(nextp)
            adjp[nextp]={e}
            nextp+=1
        if nexte>n+2:
            e=rng.choice(list(adje))
            adje[e].add(nextp)
            adjp[nextp]={e}
            nextp+=1
    strategies={}
    for i,es in adjp.items():
        es=sorted(es)
        allsets=[frozenset(e for e,b in zip(es,bits) if b)
                 for bits in product((0,1),repeat=len(es))]
        rng.shuffle(allsets)
        ss=allsets[:min(len(allsets),rng.randrange(1,6))]
        # A full set guarantees every grown edge occurs in a legal strategy.
        ss.append(frozenset(es))
        strategies[i]=tuple(dict.fromkeys(ss))
    coeffs={e:tuple(F(rng.randrange(4),rng.randrange(1,4))
                    for _ in range(rng.randrange(1,5))) for e in adje}
    weights={i:F(rng.randrange(1,9),rng.randrange(1,5)) for i in adjp}
    return Game(weights,strategies,coeffs)


def verify_forest(rng,cases):
    nodes=0
    for trial in range(cases):
        game=random_tree(rng,1+rng.randrange(5))
        root=PlayerPlan(game,0)
        state=root.realize(0)
        assert not game.deviations(state)
        for plan in root.children.values():
            nodes+=plan.verify_recursive()
    return nodes


def core_game(rng):
    # A four-cycle in the incidence graph, with one complex pendant tree per core.
    weights={0:F(2),1:F(3,2)}
    strategies={0:(frozenset(),frozenset({0}),frozenset({1})),
                1:(frozenset({0}),frozenset({1}),frozenset({0,1}))}
    coeffs={0:(F(1),F(0),F(1)),1:(F(0),F(2))}
    roots=[]
    nexti,nexte=2,2
    for parent in (0,1):
        tree=random_tree(rng,4)
        imap={0:parent}
        for i in tree.weights:
            if i:
                imap[i]=nexti
                weights[nexti]=tree.weights[i]
                nexti+=1
        emap={e:nexte+k for k,e in enumerate(tree.coeffs)}
        nexte+=len(emap)
        # Couple original core choices arbitrarily with pendant resource subsets.
        new=[]
        allroot=list(tree.strategies[0])
        for k,s in enumerate(strategies[parent]):
            a=allroot[k%len(allroot)]
            new.append(s|frozenset(emap[e] for e in a))
        new.append(frozenset(emap[e] for e in tree.incident(0)))
        strategies[parent]=tuple(dict.fromkeys(new))
        for i in tree.weights:
            if i:
                strategies[imap[i]]=tuple(frozenset(emap[e] for e in s)
                                          for s in tree.strategies[i])
        for e,cs in tree.coeffs.items():
            coeffs[emap[e]]=cs
        roots.extend((parent,emap[e]) for e in tree.incident(0))
    return Game(weights,strategies,coeffs),roots


def verify_core(rng,cases):
    profiles=0
    stable=0
    for trial in range(cases):
        game,roots=core_game(rng)
        plans={(p,e):ResourcePlan(game,e,p) for p,e in roots}
        reduced=Game({i:game.weights[i] for i in (0,1)},
                     {i:game.strategies[i] for i in (0,1)},
                     {0:game.coeffs[0],1:game.coeffs[1],
                      **{e:(plan.q,) for (p,e),plan in plans.items()}})
        for s0,s1 in product(*(reduced.strategies[i] for i in (0,1))):
            rs={0:s0,1:s1}
            full=dict(rs)
            for (p,e),plan in plans.items():
                full.update(plan.realize(int(e in rs[p])))
            profiles+=1
            for i in (0,1):
                assert game.cost(i,full)==reduced.cost(i,rs)
                for t in game.strategies[i]:
                    fd=dict(full)
                    fd[i]=t
                    rd=dict(rs)
                    rd[i]=t
                    assert game.cost(i,fd)>=reduced.cost(i,rd)
            for i in set(game.weights)-{0,1}:
                cur=game.cost(i,full)
                for t in game.strategies[i]:
                    fd=dict(full)
                    fd[i]=t
                    assert cur<=game.cost(i,fd)
            for alpha in (F(1),F(3,2),F(3),F(10)):
                if not reduced.deviations(rs,alpha):
                    stable+=1
                    assert not game.deviations(full,alpha)
    return profiles,stable


def verify_discontinuous_stars():
    """Exhaustive two-child stars for monotone discontinuous/table latencies.

    Offsets are represented by deltas; both offsets can be nonnegative using
    A0=max(delta,0), A1=max(-delta,0). Forced cases ignore the delta.
    """
    costs=(lambda x:F(0),lambda x:F(1),
           lambda x:F(int(x>=F(3,2))),
           lambda x:F(0) if x<F(1) else (F(1) if x<=F(2) else F(7)))
    checked=0
    for weights in product((F(1,2),F(1),F(2)),repeat=2):
        for deltas in product((F(-1),F(0),F(1),F(2),F(7)),repeat=2):
            for modes in product(('optional','forced-in','forced-out'),repeat=2):
                for c in costs:
                    records=[]
                    for x in (F(0),F(1,2),F(1),F(3,2),F(2),F(5)):
                        joined={i for i in range(2) if modes[i]=='forced-in'}
                        load=sum((weights[i] for i in joined),F(0))
                        ordered=sorted((i for i in range(2) if modes[i]=='optional'),
                                       key=lambda i:(-deltas[i],i))
                        for i in ordered:
                            if c(x+load+weights[i])<=deltas[i]:
                                joined.add(i)
                                load+=weights[i]
                        for i in ordered:
                            if i in joined:
                                assert c(x+load)<=deltas[i]
                            else:
                                assert c(x+load+weights[i])>=deltas[i]
                        records.append(load)
                        checked+=1
                    assert all(a>=b for a,b in zip(records,records[1:]))
    return checked


def verify_unicycle():
    # Original input only, evaluated by the same literal resource-load oracle.
    game=Game({0:F(1),1:F(2)},
              {0:(frozenset(('e','p')),frozenset(('f',))),
               1:(frozenset(('e','f')),frozenset(('q',)))},
              {'e':(F(0),F(0),F(1)), 'f':(F(0),F(9,2)),
               'p':(F(4),), 'q':(F(71,4),)})
    endpoint=F(72,71)
    rows=[]
    maxima=[]
    endpoint_states=[]
    checked=0
    for bits in product((0,1),repeat=2):
        state={i:game.strategies[i][bits[i]] for i in (0,1)}
        current=[game.cost(i,state) for i in (0,1)]
        gains=[]
        deviated_costs=[]
        for i in (0,1):
            deviated=dict(state)
            deviated[i]=game.strategies[i][1-bits[i]]
            val=game.cost(i,deviated)
            assert val>0
            gain=current[i]/val
            # Reversal check uses exact multiplication, not a float display.
            assert gain*val==current[i]
            gains.append(gain)
            deviated_costs.append(val)
            checked+=1
        maximum=max(F(1),*gains)
        assert maximum>=endpoint>1
        assert any(a>b for a,b in zip(current,deviated_costs))
        maxima.append(maximum)
        if not game.deviations(state,endpoint):
            endpoint_states.append(''.join(map(str,bits)))
        rows.append({'state':''.join(map(str,bits)),
                     'current_costs':list(map(str,current)),
                     'deviation_costs':list(map(str,deviated_costs)),
                     'all_nontrivial_gains':list(map(str,gains)),
                     'maximum_gain':str(maximum)})
    assert min(maxima)==endpoint
    assert endpoint_states==['00']
    # All four prescribed improving inequalities are strict exactly below endpoint.
    for row in rows:
        assert F(row['maximum_gain'])>=endpoint
    vertices={('p',i) for i in game.weights}|{('e',e) for e in game.coeffs}
    edges={frozenset((('p',i),('e',e))) for i in game.weights
           for e in game.incident(i)}
    reached={next(iter(vertices))}
    while True:
        expanded=reached|{v for edge in edges if edge&reached for v in edge}
        if expanded==reached:
            break
        reached=expanded
    assert reached==vertices
    assert len(edges)-len(vertices)+1==1
    assert game.users('e')==game.users('f')=={0,1}
    assert game.users('p')=={0} and game.users('q')=={1}
    return {'claim':'WC-INCIDENCE-UNICYCLE-COUNTEREXAMPLE-v1',
            'vertices':len(vertices),'edges':len(edges),'components':1,
            'cycle_rank':1,'distinct_unilateral_deviations':checked,
            'best_factor':str(endpoint),'endpoint_states':endpoint_states,
            'rows':rows}


if __name__=='__main__':
    seed=2718281828
    rng=Random(seed)
    nodes=verify_forest(rng,350)
    profiles,stable=verify_core(rng,100)
    discontinuous=verify_discontinuous_stars()
    unicycle=verify_unicycle()
    print(json.dumps({'status':'passed','seed':seed,'forest_cases':350,
                      'recursive_resource_tests':nodes,
                      'cyclic_core_games':100,'core_profiles':profiles,
                      'lifted_alpha_equilibrium_cases':stable,
                      'exhaustive_discontinuous_star_states':discontinuous,
                      'unicycle':unicycle,
                      'python_version':sys.version,
                      'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      'generator_parameters':{
                          'forest_player_count':'1+randrange(5)',
                          'weights':'Fraction(randrange(1,9),randrange(1,5))',
                          'polynomial_coefficients':'Fraction(randrange(4),randrange(1,4))',
                          'coefficient_count':'randrange(1,5)',
                          'strategy_generation':'random subset of all incident-resource subsets plus full set',
                          'background_grid':'Fraction(k,3) for k in range(49)',
                          'tested_alpha_values':['1','3/2','3','10'],
                          'core_generation':'two-player four-cycle, each with independent random four-player pendant tree',
                          'full_generation_code':Path(__file__).name},
                      'arithmetic':'fractions.Fraction',
                      'scope':'finite checks only'},sort_keys=True))
