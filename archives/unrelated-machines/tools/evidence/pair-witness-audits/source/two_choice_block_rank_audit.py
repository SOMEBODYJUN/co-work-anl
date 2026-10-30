"""Independent finite audit of actual schedules and exact rational-grid search."""
from fractions import Fraction as F
from itertools import product
import importlib.util
import json
from pathlib import Path
import platform
import random
from two_choice_block_rank_exact import BlockRankSolver, solve_matrix


def brute(jobs):
    best=None
    for choices in product(*(range(len(opts)) for opts in jobs)):
        loads={}
        for opts,c in zip(jobs,choices):
            v,p=opts[c];loads[v]=loads.get(v,F(0))+p
        z=max(loads.values(),default=F(0))
        if best is None or z<best:best=z
    return best


def witness(jobs,schedule,T):
    assert len(schedule)==len(jobs)
    load={}
    for opts,v in zip(jobs,schedule):
        p=dict(opts)[v]
        load[v]=load.get(v,F(0))+p
    assert max(load.values(),default=F(0))<=T


def main():
    result={'scope':'finite exact oracle/witness evidence, not a general proof',
            'python':platform.python_version(),'seed':20261017}
    rng=random.Random(result['seed']); comparisons=0
    for trial in range(1000):
        m=rng.randrange(1,7);n=rng.randrange(11);jobs=[]
        for j in range(n):
            arity=1 if m==1 else rng.choice((1,2,2,2))
            opts=[(v,F(rng.randrange(13),rng.choice((1,2,3,5))))
                  for v in rng.sample(range(m),arity)]
            jobs.append(opts)
        s=BlockRankSolver(jobs,machine_count=m);opt=brute(jobs)
        got,schedule=s.solve()
        assert got==opt;witness(jobs,schedule,opt)
        for T in (F(0),max(F(0),opt-F(1,30)),opt,opt+F(1,30),F(rng.randrange(21),3)):
            schedule=s.feasible(T)
            assert (schedule is not None)==(opt<=T)
            if schedule is not None:witness(jobs,schedule,T)
            comparisons+=1
    result['random']={'instances':1000,'exact_optimum_searches':1000,
                      'threshold_comparisons':comparisons,'all_witnesses_checked':True}
    shape=[(0,1),(1,2),(2,0),(0,3),(3,4),(4,0)]
    comparisons=0
    for weight in product((0,1),repeat=12):
        jobs=[[(u,F(weight[2*i])),(v,F(weight[2*i+1]))]
              for i,(u,v) in enumerate(shape)]
        s=BlockRankSolver(jobs,machine_count=5);opt=brute(jobs)
        assert s.b==1
        for T in (F(0),F(1),F(2),F(3)):
            schedule=s.feasible(T)
            assert (schedule is not None)==(opt<=T)
            if schedule is not None:witness(jobs,schedule,T)
            comparisons+=1
    result['two_triangle_cut_vertex']={'instances':2**12,'threshold_comparisons':comparisons,
                                      'all_witnesses_checked':True}
    assert solve_matrix([[]])==(F(0),[])
    assert solve_matrix([[0,None],[None,F(1,3)]])==(F(1,3),[0,1])
    # No allocation by numeric machine_count or by processing-time magnitudes.
    huge=2**1000
    s=BlockRankSolver([[(0,F(0)),(huge-1,F(0))]],machine_count=huge)
    assert s.solve()[0]==0
    tiny=F(1,2**521-1);hugetime=F(2**601+7,2**127-1)
    jobs=[[(0,tiny)],[(0,F(0)),(1,hugetime)],[(1,F(0))]]
    s=BlockRankSolver(jobs);opt,schedule=s.solve()
    assert opt==tiny;witness(jobs,schedule,opt)
    # Iterative graph and tree traversals handle deep chains without recursion.
    jobs=[[(v,F(0)),(v+1,F(1,3))] for v in range(4000)]
    s=BlockRankSolver(jobs);assert s.b==0
    opt,schedule=s.solve();assert opt==0;witness(jobs,schedule,opt)
    # Multiple labelled parallel edges must form one block of rank E-1.
    jobs=[[(0,F(j,7)),(1,F(7-j,11))] for j in range(7)]
    s=BlockRankSolver(jobs);assert s.b==6
    opt,schedule=s.solve();assert opt==brute(jobs);witness(jobs,schedule,opt)
    result['boundaries']=['empty jobs','all zero','single finite machines','explicit matrix infinity',
        'binary huge sparse labels','521-bit denominator and 602-bit numerator',
        '4000-edge deep tree with iterative traversal','7 labelled parallel jobs; b=6']
    spec=importlib.util.spec_from_file_location('cactus_gap',Path(__file__).with_name('cactus_high_girth_configuration_gap.py'))
    gap=importlib.util.module_from_spec(spec);spec.loader.exec_module(gap)
    cactus=[]
    for k,g in ((2,3),(3,3),(2,4),(2,7),(4,3),(4,7)):
        data=gap.build(k,g);gap.check(data)
        jobs=[list(opts) for label,opts in data['jobs']]
        s=BlockRankSolver(jobs,machine_count=len(data['machines']));assert s.b==1
        checks=[]
        for T in (F(0),F(1),data['T'],data['theta']-F(1,100*k),data['theta']):
            schedule=s.feasible(T)
            assert (schedule is not None)==(data['theta']<=T)
            if schedule is not None:witness(jobs,schedule,T)
            checks.append({'T':str(T),'feasible':schedule is not None})
        opt,schedule=s.solve();assert opt==data['theta'];witness(jobs,schedule,opt)
        cactus.append({'k':k,'girth':g,'machines':len(data['machines']),'jobs':len(jobs),'b':s.b,
                       'exact_optimum':str(opt),'threshold_checks':checks,
                       'all_witnesses_checked':True})
    result['independent_cactus_crosscheck']=cactus
    invalid = [lambda: BlockRankSolver([[(0,True)]]),
               lambda: BlockRankSolver([[(0,1.0)]]),
               lambda: BlockRankSolver([[(False,1)]]),
               lambda: BlockRankSolver([],machine_count=True),
               lambda: BlockRankSolver([[]]),
               lambda: BlockRankSolver([[(0,1),(0,2)]]),
               lambda: BlockRankSolver([[(0,-1)]]),
               lambda: BlockRankSolver([[(0,1)]],machine_count=0),
               lambda: solve_matrix([[None]]),
               lambda: gap.build(2,False), lambda: gap.build(2.0,3)]
    for bad in invalid:
        try: bad()
        except ValueError: pass
        else: raise AssertionError('invalid input accepted')
    result['invalid_cases_rejected'] = len(invalid)
    result['status']='all checks passed'
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
