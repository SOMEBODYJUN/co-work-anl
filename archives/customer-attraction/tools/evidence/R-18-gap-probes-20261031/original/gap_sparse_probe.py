from static_comparison_probe import *

def score(m,p,r):
    scale=lcm(*range(1,m+1))
    types=[(tuple(a for a in range(p) if mask>>a&1),v) for mask,v in enumerate(r,1) if v]
    @lru_cache(None)
    def u(q):
        out=[0]*p
        for bs,v in types:
            c=sum(q[b] for b in bs)
            if c:
                for b in bs:
                    if q[b]:out[b]+=v*(scale//c)
        return tuple(out)
    def welfare(q):return sum(v for bs,v in types if any(q[b] for b in bs))
    @lru_cache(None)
    def spe(q):
        if sum(q)==m:return frozenset([q])
        children=[spe(q[:a]+(q[a]+1,)+q[a+1:]) for a in range(p)]
        floor=max(min(u(t)[a] for t in child) for a,child in enumerate(children))
        return frozenset(t for a,child in enumerate(children) for t in child if u(t)[a]>=floor)
    opt=max(map(welfare,comps(m,p)));best=F(-1);bestq=None
    for q in spe((0,)*p):
        pay=u(q);umin=min(pay[a] for a in range(p) if q[a]);gap=opt-welfare(q)
        rat=F(gap*scale,umin) if umin else F(0)
        if rat>best:best,bestq=rat,q
    return best, {'m':m,'p':p,'types':r,'q':bestq,'opt':opt,'w':welfare(bestq),'factor':str(best)}

if __name__=='__main__':
    rng=Random(811377)
    bests=[]
    for m,p,rounds in [(3,4,5000),(4,5,5000),(5,7,5000)]:
        best=F(-1);champ=None
        for i in range(rounds):
            if i%1000==0:
                r=[0]*(2**p-1);r[0]=m*3
                for a in range(1,min(m,p)):r[(1<<a)-1]=3
                # Extra labels perturb only a small random selection of types.
            elif i%20==0:
                r=[0]*(2**p-1)
                for a in range(p):r[(1<<a)-1]=rng.randrange(0,m*3+1)
                for _ in range(rng.randrange(0,p+1)):
                    mask=rng.randrange(1,2**p);r[mask-1]=rng.randrange(1,5)
            else:
                r=champ['types'].copy()
                for _ in range(rng.randrange(1,4)):
                    k=rng.randrange(2**p-1)
                    r[k]=max(0,r[k]+rng.choice([-2,-1,1,2]))
            val,item=score(m,p,r)
            if val>best:
                best,champ=val,item
                print('best',m,p,i,str(best),item['w'],item['opt'],sum(r),flush=True)
                Path(__file__).with_name(f'gap_sparse_best_m{m}p{p}.json').write_text(json.dumps(item,indent=2))
            if val>m:
                print('FAIL',json.dumps(item));sys.exit(0)
        bests.append(champ)
    Path(__file__).with_name('gap_sparse_results.json').write_text(json.dumps(bests,indent=2))
