"""Definition-level unit-customer replay. No canonical solver/verifier import."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,json

ROOT=Path(__file__).resolve().parents[5]

def game(k):
    xs=[{f'x{i}-{j}' for j in range(6)} for i in range(k)]
    hs=[{f'h{i}-{j}' for j in range(4)} for i in range(k)]
    blocks={z:{f'{z}-{j}' for j in range(n)} for z,n in [('p',6),('q',4),('r',4),('u',3),('v',2)]}
    p,q,r,u,v=(blocks[z] for z in ['p','q','r','u','v'])
    sets=[]
    for x,h in zip(xs,hs):sets.extend([x,x|h,x|p|q,x|p|r])
    return sets+[p|u,q|r|v]

def utility(sets,h,i):
    return sum((F(1,sum(x in sets[a] for a in h)) for x in sets[h[i]]),F(0))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args()
    old=ROOT/'research/workspaces/customer-attraction/R-5c4f6385eec046eb9a20052facacba11/credible/anchor_a_two_thirds_base.json'
    actions={tuple(d['history']):d['action'] for d in json.loads(old.read_text())['certificate']['actions']}
    sets=game(1);checks=0
    def terminal(h):
        while len(h)<3:h=h+(actions[h],)
        return h
    for depth in range(3):
        for h in product(range(6),repeat=depth):
            actual=utility(sets,terminal(h),depth)
            for a in range(6):
                assert actual>=utility(sets,terminal(h+(a,)),depth),(h,a)
                checks+=1
    assert terminal(())==(0,4,5)
    reports=[]
    for k in range(2,9):
        sets=game(k);prefix=tuple(4*i for i in range(k-1));h=prefix+(1,);br={};floor=F(0)
        for b in range(len(sets)):
            values=[utility(sets,h+(b,c),len(h)+1) for c in range(len(sets))]
            maximum=max(values);br[b]=[c for c,v in enumerate(values) if v==maximum]
            floor=max(floor,min(utility(sets,h+(b,c),len(h)) for c in br[b]))
        outcomes=[h+(b,c) for b,cs in br.items() for c in cs if utility(sets,h+(b,c),len(h))>=floor]
        rewards={utility(sets,q,len(prefix)) for q in outcomes}
        assert floor==10 and rewards=={F(7)},(k,floor,rewards)
        assert all(q[-2]//4!=0 and q[-1]//4!=0 for q in outcomes)
        # Check the complete class table with one representative other-old
        # group when present; t=0, fresh=k-1.
        f=4*(k-1);j=4 if k>=3 else None
        categories=[0,1,2,3,f,f+1,f+2,f+3]+([] if j is None else [j,j+1,j+2,j+3])+[4*k,4*k+1]
        left=[F(3,2),F(7,2),F(13,2),F(17,2),6,10,11,13]+([] if j is None else [3,7,8,10])+[6,8]
        right=[2,4,7,9,3,7,8,10]+([] if j is None else [3,7,8,10])+[6,8]
        for a,v,z in zip(categories,left,right):
            assert utility(sets,h+(2,a),len(h)+1)==v
            assert utility(sets,h+(f+2,a),len(h)+1)==z
        reports.append({'k':k,'two_tail_threshold':str(floor),'SPE_ordered_tail_outcomes':len(outcomes),'deviator_rewards':[str(x) for x in sorted(rewards)]})
    report={'k1_histories':len(actions),'k1_comparisons_including_self':checks,'k1_terminal':terminal(()),
            'replication_checks':reports,'status':'definition-level finite replay; arbitrary k conclusion rests on the class proof'}
    if args.output:
        if args.output.exists():raise FileExistsError(args.output)
        args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':main()
