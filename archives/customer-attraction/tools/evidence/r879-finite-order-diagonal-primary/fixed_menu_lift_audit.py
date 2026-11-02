"""Independent exact audit of ONE saved seven-label menu and its tail-permutation lift.
No optimization, random search, game-tree generation, or SPE certification.
Private customers distinguish all labels. All customers have unit value.
"""
from fractions import Fraction as F
from itertools import permutations, combinations
from collections import Counter
import json

BITS=(0,0,0,1,1,1,0)
ROWS=((3,0,0),(3,0,1),(3,1,1),(4,2,2),(4,2,6),(4,6,6),(5,5,5))

def customers(v,bits):
    return {('private',v)} | ({('shared','x')} if bits[v] else set())

def utility(v,profile,bits,private=True,shared=True):
    total=F(0)
    for x in customers(v,bits):
        if x[0]=='private' and not private: continue
        if x[0]=='shared' and not shared: continue
        total += F(1,sum(x in customers(w,bits) for w in profile))
    return total

def averages(bits,rows):
    n=len(bits); profiles={v:(v,)+tuple(rows[v]) for v in bits}
    result={}
    for name,private,shared in [('shared',False,True),('private',True,False),('all',True,True)]:
        root=sum((utility(v,p,bits,private,shared) for v,p in profiles.items()),F(0))/n
        tail=sum((sum((utility(w,p,bits,private,shared) for w in p[1:]),F(0))/3 for p in profiles.values()),F(0))/n
        result[name]={'root':root,'tail':tail,'root_minus_tail':root-tail}
    return result

def joint_probabilities(bits,rows):
    ps=[(v,)+tuple(rows[v]) for v in bits]; n=len(ps)
    result=[]
    for j in range(1,4):
        hs=[sum(all(bits[p[k]] for k in (0,)+sub) for p in ps)*F(1,n) for sub in combinations(range(1,4),j-1)]
        gs=[sum(all(bits[p[k]] for k in sub) for p in ps)*F(1,n) for sub in combinations(range(1,4),j)]
        result.append({'degree':j,'literal_h':hs,'literal_g':gs,'mean_h':sum(hs,F(0))/len(hs),'mean_g':sum(gs,F(0))/len(gs)})
    return result

def encode(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [encode(v) for v in x]
    return x

def main():
    bits=dict(enumerate(BITS)); rows=dict(enumerate(ROWS))
    incoming=Counter(w for row in rows.values() for w in row)
    assert all(incoming[v]==3 for v in bits)
    base=averages(bits,rows); moments=joint_probabilities(bits,rows)
    assert base['shared']=={'root':F(3,14),'tail':F(11,42),'root_minus_tail':F(-1,21)}
    assert base['private']=={'root':F(16,21),'tail':F(41,63),'root_minus_tail':F(1,9)}
    assert base['all']=={'root':F(41,42),'tail':F(115,126),'root_minus_tail':F(4,63)}
    assert moments[0]['literal_g']==[F(1),F(1,7),F(1,7)]
    assert [(r['mean_h'],r['mean_g']) for r in moments]==[(F(3,7),F(3,7)),(F(1,7),F(1,7)),(F(0),F(1,7))]
    before=(0,3,0,0); after=(0,3,0,4)
    old=utility(0,before,bits); new=utility(4,after,bits)
    assert (old,new,new-old)==(F(1,3),F(3,2),F(7,6))
    perms=tuple(permutations(range(3)))
    lifted_bits={(v,pi):BITS[v] for v in range(7) for pi in perms}
    lifted_rows={(v,pi):tuple((ROWS[v][pi[j]],pi) for j in range(3)) for v,pi in lifted_bits}
    incoming_lift=Counter(w for row in lifted_rows.values() for w in row)
    assert len(lifted_bits)==42 and all(incoming_lift[v]==3 for v in lifted_bits)
    lift_av=averages(lifted_bits,lifted_rows); lift_mom=joint_probabilities(lifted_bits,lifted_rows)
    assert lift_av==base
    for r in lift_mom:
        assert len(set(r['literal_h']))==len(set(r['literal_g']))==1
        if r['degree']<=2: assert r['literal_h'][0]==r['literal_g'][0]
    return {'scope':'fixed seven-label menu and its 42-label deterministic lift only; no SPE certification',
        'base':{'labels':7,'unit_customers':8,'tails':ROWS,'indegree':[incoming[v] for v in bits],
                'moments':moments,'profits':base},
        'base_last_player_violation':{'prefix':[0,3,0],'prescribed':0,'deviation':4,'prescribed_utility':old,'deviation_utility':new,'gain':new-old},
        'lift':{'labels':42,'unit_customers':43,'permutations':perms,'all_indegrees':3,'moments':lift_mom,'profits':lift_av}}

if __name__=='__main__':
    print(json.dumps(encode(main()),ensure_ascii=False,indent=2))
