"""Compile the exact d=1 relaxation point into a twelve-theme unit instance.

Set-valued backward induction retains every terminal count reachable by some
full ordered-history pure SPE. Count caching shares value sets only; choices
at different ordered histories remain independent. This is one candidate test.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import lcm
import json,time

HERE=Path(__file__).resolve().parent
M=6;P=12


def run():
    start=time.time()
    record=json.loads((HERE/'mixed_pair_results.json').read_text())['certificate']
    assert all(z['d']==1 for z in record['support'])
    den=lcm(*(F(z['weight']).denominator for z in record['support']))
    groups=[]
    # Each d=1 group is split equally among six distinct optimum themes.
    # Counts den*weight per optimal label implement 6*den scaled customer mass.
    for z in record['support']:
        a=tuple(map(int,z['actual_bits']));mass=F(z['weight'])*den;assert mass.denominator==1
        for j in range(6):groups.append((tuple(i for i,x in enumerate(a) if x)+(6+j,),int(mass)))
    ucache={};mincache={};ecache={};nodes=[0]*7

    def utilities(final):
        if final in ucache:return ucache[final]
        u=[0]*P
        for labels,n in groups:
            load=sum(final[j] for j in labels)
            if not load:continue
            assert 60%load==0
            for j in labels:
                if final[j]:u[j]+=n*(60//load)
        out=tuple(u);ucache[final]=out;return out

    def outcomes(prefix):
        if prefix in ecache:return ecache[prefix]
        depth=sum(prefix);nodes[depth]+=1
        if depth==M:return (prefix,)
        children=[];floor=[]
        for a in range(P):
            q=list(prefix);q[a]+=1;q=tuple(q)
            leaves=outcomes(q)
            children.append(leaves)
            floor.append(min(utilities(z)[a] for z in leaves))
        threshold=max(floor)
        keep={leaf for a,leaves in enumerate(children) for leaf in leaves if utilities(leaf)[a]>=threshold}
        assert keep
        result=tuple(sorted(keep));ecache[prefix]=result;mincache[prefix]=tuple(floor)
        if depth<=1:print('backward depth',depth,'outcomes',len(result),'nodes',sum(nodes),'seconds',time.time()-start,flush=True)
        return result

    goal=(1,)*6+(0,)*6
    goalu=utilities(goal)
    # Test the actual suffix from its end; no need to enumerate the root tree
    # if a later prescribed player already violates a genuine deviation floor.
    tests=[]
    for depth in range(5,-1,-1):
        prefix=(1,)*depth+(0,)*(P-depth)
        leaves=outcomes(prefix)
        floor=mincache[prefix];best=max(range(P),key=lambda a:floor[a])
        bad=floor[best]>goalu[depth]
        test={'position':depth+1,'own_scaled_integer':str(goalu[depth]),
              'max_deviation_minimum_scaled_integer':str(floor[best]),'deviation_label':best,
              'prescribed_final_in_subgame_SPE_set':goal in leaves,'strict_violation':bad,
              'all_action_floors_scaled_integer':list(map(str,floor))}
        tests.append(test)
        print('actual position',depth+1,'violation',bad,'best',best,'outcomes',len(leaves),flush=True)
        if bad:break
    result={'scope':'one exact compiled twelve-theme instance; set-valued pure SPE reachability, not half proof',
            'customer_scale':str(6*den),'utility_integer_scale':60,'themes':['A'+str(i+1) for i in range(6)]+['T'+str(i+1) for i in range(6)],
            'source_point_W_over_O':record['W'],'groups':[{'theme_indices':list(ls),'count':str(n)} for ls,n in groups],
            'actual_path_tests':tests,'visited_nodes_by_depth':nodes,'terminal_utility_vectors':len(ucache),
            'seconds':time.time()-start,'status':'prescribed path refuted' if any(t['strict_violation'] for t in tests) else 'all prescribed actual-prefix checks pass'}
    (HERE/'credible_catalog.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='groups'},indent=2),flush=True)


if __name__=='__main__':run()
