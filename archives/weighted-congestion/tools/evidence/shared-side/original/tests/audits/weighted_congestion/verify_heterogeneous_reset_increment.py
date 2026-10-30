"""异权排序势重置增量及坏局部最小点：作者路 Fraction 有限审计。"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import sys

SEED = 68421927
rng = random.Random(SEED)
counts = dict(nonuniform_resets=0, source_increment=0, marginal=0,
              games=0, hub_states=0, local_minima=0, real_deviations=0,
              source_reset_budgets=0, bad_minimum_formulas=0,
              strict_bad_minima=0, weak_product_endpoints=0,
              global_count_states=0, symbolic_polynomial_identities=0)


def cost(c, x):
    return sum((v * x**k for k, v in enumerate(c)), Q())


def kap(d, t):
    return min(d*t, 1+t)


def prefix(c, hubs, chosen, x):
    p = Q()
    ans = Q()
    for v in sorted(chosen, key=lambda i: (-hubs[i], i)):
        p += hubs[v]
        ans += cost(c, x+p)
    return ans


def ceilq(q):
    return -((-q.numerator)//q.denominator)


def ri_grid():
    for d in (2, 3, 5):
        for n in range(5):
            for t in range(60):
                A = Q(rng.randint(1, 9), rng.randint(1, 7))
                ws = [A+Q(rng.randint(0, 8), rng.randint(1, 7)) for _ in range(n)]
                p = []
                for b in ws:
                    p.append((p[-1] if p else Q())+b)
                U = sum(ws, Q())+Q(rng.randint(0, 7), rng.randint(1, 5))
                x = Q(rng.randint(0, 7), rng.randint(1, 5))
                w = Q(rng.randint(1, 30), rng.randint(1, 7))
                T = x+w+Q(rng.randint(0, 7), rng.randint(1, 5))
                # Force a constant, a zero and a large-w/minimal-T boundary.
                c = [Q(rng.randint(0, 4), rng.randint(1, 7)) for _ in range(d+1)]
                if t % 11 == 0:
                    c = [Q(3)] + [Q()] * d
                if t % 13 == 0:
                    c = [Q()] * (d+1)
                if t % 7 == 0:
                    x = Q(); w = 17*A; T = w; U = sum(ws, Q())
                Y = T+U
                left = sum((cost(c, x+w+z)-cost(c, x+z) for z in p), Q())
                right = kap(d, w/A)*(cost(c, Y)-cost(c, w))
                assert 0 <= left <= right, (d, n, A, p, x, w, T, U, c, left, right)
                counts['nonuniform_resets'] += 1


def scalar_grid():
    for d in (2, 3, 5):
        for trial in range(400):
            ts = [Q(rng.randint(1, 20), rng.randint(1, 20)) for _ in range(trial % 6)]
            if trial % 2:
                ts = [t/100 for t in ts]
            T = sum(ts, Q())
            a = Q(rng.randint(1, 12), rng.randint(1, 7))
            tau = (Q(1), Q(3, 2), Q(2), Q(11, 2))[trial % 4]
            c = [Q(rng.randint(0, 4), rng.randint(1, 5)) for _ in range(d+1)]
            left = sum((kap(d, t)*(cost(c, a*(1+t))-tau*cost(c, a*T)) for t in ts), Q())
            right = d*(cost(c, a*(1+T))-cost(c, a))
            assert left <= right, (d, ts, a, tau, c, left, right)
            counts['source_increment'] += 1


def whole_game(d, hubs, lights, sides, tau, alpha=None):
    """Literal original strategies; potential used only after costs are rebuilt."""
    n = len(hubs)
    W = [sum((w for o, w in lights if o == v), Q()) for v in range(n)]
    U = [sum((hubs[v] for v in H), Q()) for H, L, c in sides]
    T = [sum((lights[l][1] for l in L), Q()) for H, L, c in sides]
    A = [min((hubs[v] for v in H), default=None) for H, L, c in sides]
    R = max([Q(1)]+[hubs[v]/A[j] for j,(H,L,c) in enumerate(sides) for v in H])
    K = max([Q(1)]+[hubs[lights[l][0]]/A[j] for j,(H,L,c) in enumerate(sides) if H for l in L])
    alpha = max(Q(1), R, K*d/tau) if alpha is None else alpha
    assert alpha >= R and alpha*tau >= K*d
    if alpha*tau == K*d:
        counts['weak_product_endpoints'] += 1
    F = []
    for v,a in enumerate(hubs):
        c0 = Q(rng.randint(0, 2), 7)
        bound = Q()
        for l,(o,w) in enumerate(lights):
            if o != v:
                continue
            need = (tau-1)*c0 + sum((tau*cost(c, T[j]+U[j])-cost(c,w)
                    for j,(H,L,c) in enumerate(sides) if l in L), Q())
            den = (a+w)**d-tau*W[v]**d
            assert den > 0
            bound = max(bound, need/den)
        lam = Q(max(0,ceilq(bound))+1) if any(o == v for o,w in lights) else Q()
        F.append([c0]+[Q()]*(d-1)+[lam])
    for l,(v,w) in enumerate(lights):
        left = cost(F[v],hubs[v]+w)+sum((cost(c,w) for H,L,c in sides if l in L),Q())
        right = tau*(cost(F[v],W[v])+sum((cost(c,T[j]+U[j]) for j,(H,L,c) in enumerate(sides) if l in L),Q()))
        assert left >= right
    coeffs = {}
    strategies = []
    for v,c in enumerate(F):
        for b in (0,1):
            coeffs[('m',v,b)] = c
    for j,(H,L,c) in enumerate(sides):
        for b in (0,1):
            coeffs[('s',j,b)] = c
    for v in range(n):
        strategies.append([{('m',v,b)} | {('s',j,b) for j,(H,L,c) in enumerate(sides) if v in H} for b in (0,1)])
    for l,(o,w) in enumerate(lights):
        strategies.append([{('m',o,b)} | {('s',j,1-b) for j,(H,L,c) in enumerate(sides) if l in L} for b in (0,1)])
    weights = hubs+[w for o,w in lights]

    def real_costs(state):
        loads = {r:Q() for r in coeffs}
        for i,b in enumerate(state):
            for r in strategies[i][b]:
                loads[r] += weights[i]
        return [sum((cost(coeffs[r],loads[r]) for r in strategies[i][b]),Q()) for i,b in enumerate(state)]

    def E(h, source_bits=None):
        source_bits = h if source_bits is None else source_bits
        ans = Q()
        for H,L,c in sides:
            for b in (0,1):
                x = sum((lights[l][1] for l in L if source_bits[lights[l][0]] == b),Q())
                ans += prefix(c,hubs,{v for v in H if h[v] == b},x)
        return ans

    for h in product((0,1),repeat=n):
        counts['hub_states'] += 1
        for v in range(n):
            hv = h[:v]+(1-h[v],)+h[v+1:]
            actual_reset = E(hv)-E(hv, h)
            delta = cost(F[v],hubs[v]+W[v])-cost(F[v],hubs[v])
            B = Q()
            for l,(o,w) in enumerate(lights):
                if o != v:
                    continue
                B += sum((kap(d,w/A[j])*(cost(c,T[j]+U[j])-cost(c,w))
                         for j,(H,L,c) in enumerate(sides) if H and l in L), Q())
            assert actual_reset <= B <= K*d*delta/tau <= alpha*delta
            counts['source_reset_budgets'] += 1
        if any(E(h) > E(h[:v]+(1-h[v],)+h[v+1:]) for v in range(n)):
            continue
        counts['local_minima'] += 1
        state = h+tuple(1-h[o] for o,w in lights)
        old = real_costs(state)
        for i in range(len(weights)):
            dev = state[:i]+(1-state[i],)+state[i+1:]
            new = real_costs(dev)
            assert old[i] <= alpha*new[i], (d,hubs,lights,sides,tau,alpha,h,i,old[i],new[i])
            counts['real_deviations'] += 1
    counts['games'] += 1
    return dict(d=d, R=str(R), K=str(K), tau=str(tau), alpha=str(alpha),
                hubs=list(map(str,hubs)), lights=[(o,str(w)) for o,w in lights], sides=len(sides))


def marginal_grid():
    for d in (2,3,5):
        for trial in range(120):
            weights = [Q(rng.randint(1,12),rng.randint(1,6)) for _ in range(4)]
            A = min(weights)
            c = [Q(rng.randint(0,3),rng.randint(1,5)) for _ in range(d+1)]
            x = Q(rng.randint(0,7),rng.randint(1,5))
            for bits in product((0,1),repeat=4):
                S = {i for i,b in enumerate(bits) if b}
                for v in set(range(4))-S:
                    dp = prefix(c,weights,S|{v},x)-prefix(c,weights,S,x)
                    real = cost(c,x+weights[v]+sum((weights[i] for i in S),Q()))
                    assert real <= dp <= weights[v]*real/A
                    counts['marginal'] += 1


def bad_local_minima():
    examples = []
    for R in (Q(3,2),Q(2),Q(5),Q(13,3)):
        for alpha in (Q(1), (1+R)/2, R-Q(1,100)):
            n = max(1,ceilq(alpha*R/(R-alpha))+1)
            ratio = Q(n)*R/(R+n)
            assert ratio > alpha
            # Only two representative flips are needed: identities in each group are symmetric.
            for A in (Q(1),Q(2,7)):
                a=R*A
                Eold=a*n*(n+1)/2+A*n*(n+1)/2
                Eheavy=a*n*(n-1)/2+(n+1)*a+A*n*(n+1)/2
                Elight=a*n*(n+1)/2+n*a+A+A*n*(n-1)/2
                assert Eheavy-Eold == a > 0
                assert Elight-Eold == n*a-(n-1)*A > 0
                assert Q(n)*a > alpha*(a+n*A)
                counts['bad_minimum_formulas'] += 2
            # Enumerate actual identity flips for modest chosen members, without large-n state cube.
            if n <= 24:
                weights=[R]*n+[Q(1)]*n
                h=(0,)*n+(1,)*n
                def ep(h):
                    return sum((prefix([Q(),Q(1)],weights,{i for i,b in enumerate(h) if b==z},Q()) for z in (0,1)),Q())
                old=ep(h)
                for i in range(len(h)):
                    hv=h[:i]+(1-h[i],)+h[i+1:]
                    assert ep(hv)>old
                counts['strict_bad_minima'] += 1
            examples.append(dict(R=str(R),alpha=str(alpha),n=n,actual_ratio=str(ratio)))
    return examples


def global_minima_grid():
    for R in (Q(3,2),Q(2),Q(5),Q(13,3)):
        for n in range(1,20):
            a=R; A=Q(1)
            minima=[]
            for x in range(n+1):
                for y in range(n+1):
                    k=n-x; l=y
                    P=a*(x*(x+1)+(n-x)*(n-x+1))/2+a*(x*y+(n-x)*(n-y))+A*(y*(y+1)+(n-y)*(n-y+1))/2
                    base=(a+A)*n*(n+1)/2
                    rhs=a*(k-l)**2+(a-A)*l*(n-l)
                    assert P-base == rhs >= 0
                    if P == base:
                        minima.append((x,y))
                    counts['global_count_states']+=1
            assert minima==[(0,n),(n,0)]
    # Exact symbolic reverse check, not a floating-point substitution:
    # monomial exponents run in the order (n,k,l,a,A).
    from collections import defaultdict
    def C(q): return {(0,0,0,0,0):Q(q)}
    def V(i):
        e=[0]*5; e[i]=1
        return {tuple(e):Q(1)}
    def add(*ps):
        out=defaultdict(Q)
        for p in ps:
            for e,c in p.items(): out[e]+=c
        return {e:c for e,c in out.items() if c}
    def sc(p,q): return {e:c*q for e,c in p.items() if c*q}
    def mul(p,q):
        out=defaultdict(Q)
        for e,c in p.items():
            for f,d in q.items(): out[tuple(x+y for x,y in zip(e,f))]+=c*d
        return {e:c for e,c in out.items() if c}
    n,k,l,a,A=[V(i) for i in range(5)]; one=C(1)
    x=add(n,sc(k,-1)); y=l; nx=add(n,sc(x,-1)); ny=add(n,sc(y,-1))
    P=add(sc(mul(a,add(mul(x,add(x,one)),mul(nx,add(nx,one)))),Q(1,2)),mul(a,add(mul(x,y),mul(nx,ny))),sc(mul(A,add(mul(y,add(y,one)),mul(ny,add(ny,one)))),Q(1,2)))
    base=sc(mul(add(a,A),mul(n,add(n,one))),Q(1,2))
    difference=add(P,sc(base,-1))
    rhs=add(mul(a,mul(add(k,sc(l,-1)),add(k,sc(l,-1)))),mul(add(a,sc(A,-1)),mul(l,add(n,sc(l,-1)))))
    assert add(difference,sc(rhs,-1))=={}
    counts['symbolic_polynomial_identities']+=1


ri_grid()
scalar_grid()
marginal_grid()
fixtures=[]
# Both alpha=R and alpha*tau=Kd hold with equality, with genuine heterogeneous source feedback.
fixtures.append(whole_game(2,[Q(2),Q(1)],[(0,Q(1,100)),(1,Q(1,200))],
                          [({0,1},{0,1},[Q(),Q(),Q(1)])],Q(2),Q(2)))
for d in (2,3,5):
    for n in range(1,5):
        for trial in range(12):
            hubs=[Q(rng.randint(1,9),rng.randint(1,4)) for _ in range(n)]
            lights=[]
            for v,a in enumerate(hubs):
                for _ in range(rng.randint(0,2)):
                    lights.append((v,a*Q(rng.randint(1,3),100)))
            sides=[]
            for _ in range(rng.randint(0,5)):
                H={v for v in range(n) if rng.randrange(3)}
                L={l for l in range(len(lights)) if rng.randrange(2)}
                c=[Q(rng.randint(0,2),rng.randint(1,4)) for _ in range(d+1)]
                if trial%5==0:
                    c=[Q(2)]+[Q()]*d
                if trial%7==0:
                    c=[Q()]*(d+1)
                sides.append((H,L,c))
            tau=(Q(1),Q(3,2),Q(2),Q(4*d))[trial%4]
            f=whole_game(d,hubs,lights,sides,tau)
            if len(fixtures)<7:
                fixtures.append(f)
bad=bad_local_minima()
global_minima_grid()

print(json.dumps(dict(title='异权排序侧势重置增量及坏全局最小点的作者精确审计',
    seed=SEED,python=sys.version.split()[0],arithmetic='fractions.Fraction',
    counts=counts,fixtures=fixtures,bad_local_minimum_examples=bad,
    code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    reviewed_section_sha256='bf4478c57a426b5fd0817a07d06686951596f717cd888620ae663fb0a24afb76',
    scope='有限输入检查；一般正实参数结论仅由数学正文证明，不由本输出推断。'),ensure_ascii=False,indent=2))
