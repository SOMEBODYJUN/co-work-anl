"""逐资源精确核验类内三元时钟编译障碍；不导入仓库其他实现。

默认在仓库根运行。显式 --input 可用于固定候选；stdout 是新运行结果，
本程序从不原位重写输入或冻结证据。有限断言不替代正文的一般局部证明。
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from hashlib import sha256
import argparse
import json
import platform
import sys

DEFAULT_INPUT='examples/weighted_congestion/class_internal_clock_compiler_obstruction.json'

def front_bits(nc,phase):
    phase%=2*nc
    return [int(j<phase) if phase<nc else int(j>=phase-nc) for j in range(nc)]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',default=DEFAULT_INPUT)
    args=parser.parse_args()
    input_path=Path(args.input)
    raw=input_path.read_bytes();fixture=json.loads(raw)
    assert fixture['schema_version']==1
    assert fixture['claim_id']=='WC-CLASS-INTERNAL-CLOCK-COMPILER-OBSTRUCTION-v1'
    exponent=int(fixture['degree']);alpha=F(fixture['alpha'])
    class_weights=tuple(map(F,fixture['class_weights']))
    nc=int(fixture['clones_per_class']);m=len(class_weights)
    assert exponent==8 and alpha==F(21,20)
    assert (nc,class_weights)==(4,(F(1),F(1,4),F(1,16)))
    players=tuple((j,a) for j in range(nc) for a in range(m))
    weights=tuple(class_weights[a] for j,a in players)
    strategies=[[set(),set()] for u in players]
    resources=[]
    for test_index,test in enumerate(fixture['tests']):
        a,b,K,o=(int(test[k]) for k in ['a','b','window','orientation'])
        coefficient=F(test['resource_coefficient'])
        assert a!=b and 0<=a<m and 0<=b<m and 1<=K<=nc and o in [-1,1]
        assert coefficient>0
        for j in range(nc):
            h=j*m+a;literal={h:0}
            for k in range(K):
                u=((j+int(a>b)+k)%nc)*m+b
                literal[u]=int(u>h)^int(o<0)
            for side in [0,1]:
                resource_id=len(resources)
                resources.append((literal,side,coefficient))
                for u,offset in literal.items():
                    strategies[u][side^offset].add(resource_id)
    assert all(s0 and s1 and not(s0&s1) for s0,s1 in strategies)
    assert len(players)==12 and len(resources)==64

    def cost(state,player):
        total=F()
        for rid in strategies[player][state[player]]:
            literal,side,coefficient=resources[rid]
            load=sum((weights[u] for u,offset in literal.items() if state[u]^offset==side),F())
            assert load>=weights[player]
            total+=coefficient*load**exponent
        return total

    def old_post(state,player):
        old=cost(state,player)
        post=state.copy();post[player]^=1
        return old,cost(post,player)

    state=[0]*len(players);sweep=[]
    for half in range(2):
        for player in range(len(players)):
            old,new=old_post(state,player);margin=old-alpha*new
            assert margin>F(3,4)
            sweep.append({'half':half,'player':player,'old':str(old),'post':str(new),'alpha_margin':str(margin)})
            state[player]^=1
    assert not any(state)
    for row in sweep:
        a=row['player']%m
        assert (row['old'],row['post'])==(sweep[a]['old'],sweep[a]['post'])
    phases=fixture['front_phases']
    assert phases==[0,0,1]
    front=[front_bits(nc,phases[a])[j] for j,a in players]
    front_rows=[]
    front_upper_bounds=tuple(map(F,['-1/2','-3','-3/4','-6/5','-6/5','-19/10','-4/5','-8','-2','-4','-6','-7/5']))
    for player in range(len(players)):
        old,new=old_post(front,player)
        assert old-new<front_upper_bounds[player]
        assert old-new<-F(1,2)
        front_rows.append({'player':player,'clone':player//m,'class':player%m,
                           'old':str(old),'post':str(new),'exact_margin':str(old-new),
                           'alpha_margin':str(old-alpha*new),'proof_upper_bound':str(front_upper_bounds[player])})
    geometry_checks=0
    for width in range(3,10):
        for phase in range(2*width):
            bits=front_bits(width,phase)
            for j0,j1,j2 in combinations(range(width),3):
                literal={j0:0,j1:1,j2:0}
                loads=[0,0]
                for u,offset in literal.items():loads[bits[u]^offset]+=1
                assert max(loads)<=2
                for u,offset in literal.items():
                    side=bits[u]^offset
                    old_load=loads[side];post_load=loads[1-side]+1
                    assert (old_load,post_load) in [(2,2),(1,3)]
                    geometry_checks+=1
    out={'status':'all exact assertions passed','claim_id':fixture['claim_id'],
         'scope':'Fixed strict 24-edge alpha-cycle and strict exact-PNE product front; arbitrary-degree class-internal ordered monotone same-fee 010/101 clocks preserve that front. Finite geometry checks do not replace the general proof. Cross-class clocks, asymmetric pair fees and the universal target are not covered.',
         'degree':exponent,'alpha':str(alpha),'players':len(players),'resources':len(resources),
         'clones_per_class':nc,'class_weights':list(map(str,class_weights)),
         'literal_sweep_edges':len(sweep),'cycle_margin_lower_bound':'3/4',
         'minimum_cycle_margin':str(min(F(row['alpha_margin']) for row in sweep)),
         'class_cycle_margins':[sweep[a]['alpha_margin'] for a in range(m)],
         'sweep':sweep,'front_phases':phases,'front_bits':front,'front_costs':front_rows,
         'exact_front_margin_upper_bound':'-1/2',
         'maximum_exact_front_margin':str(max(F(row['exact_margin']) for row in front_rows)),
         'clock_geometry_checks':geometry_checks,'clock_geometry_widths':list(range(3,10)),
         'input_path':str(input_path),'input_sha256':sha256(raw).hexdigest(),
         'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
         'command':[sys.executable,*sys.argv],'python':platform.python_version(),
         'precision':'exact fractions; no tolerance, random seed or numerical optimization'}
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
