"""Independent ordered SPE / Floyd-Warshall SCC check for lattice circulation."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json


def run():
    # Independently transcribed complete strategy, labels A=0 B=1 C=2.
    actions={():0,(0,):2,(1,):0,(2,):0}
    for first,row in enumerate(((2,0,0),(0,0,0),(1,0,0))):
        for second,a in enumerate(row):actions[first,second]=a
    customers=[]
    for membership,count in (({0},3),({1},2),({0,1},3),({2},2),
                             ({0,2},3),({1,2},1),({0,1,2},1)):
        customers += [frozenset(membership)]*count
    histories=[h for n in range(3) for h in product(range(3),repeat=n)]
    assert set(histories)==set(actions)

    def follow(history):
        while len(history)<3:history=history+(actions[history],)
        return history

    def utility(path,player):
        return sum((F(1,sum(a in client for a in path))
                    for client in customers if path[player] in client),F(0))

    def endpoint(history,action):
        path=follow(history+(action,))
        return tuple(path.count(a) for a in range(3)),action

    def type_row(endpoint):
        q,a=endpoint
        return tuple(F(1,sum(q[j] for j in range(3) if B>>j&1))
                     if B>>a&1 else F(0) for B in range(1,8))

    edges=[];rows={};slacks=[]
    for history in histories:
        actual=follow(history)
        target=endpoint(history,actions[history])
        for a in range(3):
            deviation=follow(history+(a,))
            slack=utility(actual,len(history))-utility(deviation,len(history))
            assert slack>=0
            slacks.append(slack)
            source=endpoint(history,a)
            rows[history,a]=tuple(x-y for x,y in zip(type_row(target),type_row(source)))
            edges.append((source,target))
    vertices=sorted({v for e in edges for v in e})
    index={v:i for i,v in enumerate(vertices)}
    N=len(vertices)
    reach=[[i==j for j in range(N)] for i in range(N)]
    for a,b in edges:reach[index[a]][index[b]]=True
    # Transitive closure differs from the discovery audit's per-node DFS.
    for k in range(N):
        for i in range(N):
            if reach[i][k]:
                for j in range(N):reach[i][j]=reach[i][j] or reach[k][j]
    used=set();components=[]
    for i in range(N):
        if i in used:continue
        C={j for j in range(N) if reach[i][j] and reach[j][i]}
        used|=C;components.append(sorted(vertices[j] for j in C))
    nontrivial=[C for C in components if len(C)>1]
    assert nontrivial==[[((1,1,1),1),((2,0,1),0)]]
    selected=[rows[(),1],rows[(0,),0],rows[(1,),2],rows[(2,0),0]]
    assert [sum(v) for v in zip(*selected)]==[F(0)]*7
    root=selected[0]
    scc_difference=tuple(x-y for x,y in zip(type_row(nontrivial[0][0]),type_row(nontrivial[0][1])))
    assert any(scc_difference)
    assert scc_difference[2]==0 and root[2]==F(1,6)
    assert [utility(follow(()),i) for i in range(3)]==[F(13,3)]*3
    welfare=sum(any(a in client for a in follow(())) for client in customers)
    optimum=max(sum(any(a in client for a in path) for client in customers)
                for path in product(range(3),repeat=3))
    assert welfare==13 and optimum==15
    return {'status':'independently verified; no fatal objection',
            'unit_customers':len(customers),'ordered_histories':len(histories),
            'all_action_comparisons':len(slacks),'minimum_slack':str(min(slacks)),
            'only_nontrivial_payoff_SCC':nontrivial,
            'zero_combination_rows':[[str(v) for v in row] for row in selected],
            'root_row_outside_SCC_space':'AB coordinate root=1/6, SCC generator=0',
            'welfare':welfare,'OPT':optimum,'general_half':'OPEN'}


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    result=run()
    if args.output:
        with args.output.open('x') as stream:
            json.dump(result,stream,ensure_ascii=False,indent=2)
            stream.write('\n')
    print(json.dumps(result,ensure_ascii=False))
