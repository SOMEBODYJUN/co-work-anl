from itertools import product
from functools import lru_cache
import json, hashlib

def perfect(q,edges):
    adj=[[] for _ in range(q)]
    for x,y,z in edges: adj[x].append((y,z))
    @lru_cache(None)
    def visit(x,ys,zs):
        if x==q: return True
        return any(not(ys>>y&1) and not(zs>>z&1) and visit(x+1,ys|1<<y,zs|1<<z) for y,z in adj[x])
    return visit(0,0,0)

def denominator_matching(q,edges,r):
    for counts in product(range(r+1),repeat=len(edges)):
        totals=[[0]*q for _ in range(3)]
        for edge,n in zip(edges,counts):
            for j,v in enumerate(edge): totals[j][v]+=n
        if all(x==r for row in totals for x in row): return True
    return False

def pool(q,edges,r):
    return [(x*r+i,y*r+j,z*r+k) for x,y,z in edges for i,j,k in product(range(r),repeat=3)]

def tensor(q,edges):
    return [(q*a[0]+b[0],q*a[1]+b[1],q*a[2]+b[2]) for a in edges for b in edges]

def run():
    universe=list(product(range(2),repeat=3)); count=0
    for mask in range(256):
        edges=[e for i,e in enumerate(universe) if mask>>i&1]
        for r in (1,2,3):
            assert perfect(2*r,pool(2,edges,r))==denominator_matching(2,edges,r),(edges,r)
            count+=1
    parity=[(0,0,0),(0,1,1),(1,0,1),(1,1,0)]
    witness=[(2*a+b,2*b+(a^b),2*(a^b)+a) for a,b in product(range(2),repeat=2)]
    assert not perfect(2,parity)
    assert perfect(4,pool(2,parity,2)) and perfect(4,tensor(2,parity))
    assert all(e in tensor(2,parity) for e in witness)
    assert all(len({e[j] for e in witness})==4 for j in range(3))
    print(json.dumps({'pool_cases':count,'scope':'all 256 q=2 3DM supports, r=1,2,3',
      'parity_tensor_square_witness':witness,'pool_edges':len(pool(2,parity,2)),
      'tensor_square_edges':len(tensor(2,parity)),'all_passed':True,
      'script_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest()},indent=2))

if __name__=='__main__': run()
