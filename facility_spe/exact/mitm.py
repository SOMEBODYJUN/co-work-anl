#!/usr/bin/env python3
"""Exact rational two-location Nash load optimization by threshold/MITM.
No third-party packages. See ring_solver_notes.md for bounds and proof.
"""
from fractions import Fraction as Q
from bisect import bisect_left, bisect_right
import argparse, json, random, time


def frac(x):
    return x if isinstance(x, Q) else Q(str(x))


def verify(a, b, weights, probs):
    a, b = frac(a), frac(b)
    weights, probs = list(map(frac, weights)), list(map(frac, probs))
    assert len(weights) == len(probs)
    l = a + sum((w*x for w,x in zip(weights, probs)), Q(0))
    r = b + sum((w*(1-x) for w,x in zip(weights, probs)), Q(0))
    for w,x in zip(weights, probs):
        assert 0 <= x <= 1
        diff = l-r+w*(1-2*x)
        assert (x == 0 and diff >= 0) or (x == 1 and diff <= 0) or (0<x<1 and diff == 0)
    return l,r


def table(ws, stats):
    # Identical (mixed count, signed pure weight) states have identical futures.
    d={(0,Q(0)): ()}
    for w in ws:
        out={}
        for (k,z), word in d.items():
            out.setdefault((k,z+w),word+(1,))
            out.setdefault((k,z-w),word+(0,))
            out.setdefault((k+1,z),word+(2,))
        d=out
    stats['half_states'] += len(d)
    groups={}
    for (k,z),word in d.items():
        groups.setdefault(k,{})[z]=word
    return {k:(sorted(v),v) for k,v in groups.items()}


def optimize_pair(a,b,weights,target=None,score=None):
    """Find a Nash equilibrium minimizing score(gap).
    score must decrease on (-infinity,target] and increase on [target,infinity).
    Defaults to min first facility load (score=gap,target=-total).
    """
    a,b=frac(a),frac(b)
    ws=list(map(frac,weights)); n=len(ws)
    assert min([a,b]+ws)>=0 and all(w>0 for w in ws)
    order=sorted(range(n),key=lambda i:ws[i],reverse=True)
    w=[ws[i] for i in order]; total=a+b+sum(w,Q(0))
    if target is None: target=-total
    target=frac(target)
    if score is None: score=lambda gap:gap
    stats={'half_states':0,'queries':0,'candidates':0}
    best=None; best_score=None
    prefix=[Q(0)]
    for v in w: prefix.append(prefix[-1]+v)
    for h in range(n+1):
        upper=w[h-1] if h else total
        lower=w[h] if h<n else Q(0)
        if lower>upper: continue
        cut=h//2
        left=table(w[:cut],stats);right=table(w[cut:h],stats)
        light=prefix[n]-prefix[h]
        for sign in [-1,1]:
            lo,hi=(-upper,-lower) if sign<0 else (lower,upper)
            offset=a-b-sign*light
            for kl,(zl,wl) in left.items():
                for kr,(zr,wr) in right.items():
                    k=kl+kr; factor=1-k
                    for lv in zl:
                        stats['queries']+=1
                        if factor==0:
                            rv=-offset-lv;ix=bisect_left(zr,rv)
                            if ix==len(zr) or zr[ix]!=rv: continue
                            candidates=[(rv,min(hi,max(lo,target)))]
                        else:
                            v1=factor*lo-offset-lv;v2=factor*hi-offset-lv
                            start=bisect_left(zr,min(v1,v2));end=bisect_right(zr,max(v1,v2))
                            if start==end: continue
                            goal=factor*target-offset-lv
                            ix=bisect_left(zr,goal,start,end)
                            inds={min(end-1,max(start,ix)),min(end-1,max(start,ix-1))}
                            candidates=[(zr[j],(offset+lv+zr[j])/factor) for j in inds]
                        for rv,gap in candidates:
                            stats['candidates']+=1
                            value=score(gap)
                            if best is not None and value>=best_score:continue
                            word=wl[lv]+wr[rv]+((1 if sign<0 else 0),)*(n-h)
                            p_sorted=[Q(t) if t!=2 else (1+gap/wi)/2 for t,wi in zip(word,w)]
                            probs=[Q(0)]*n
                            for ix,p in zip(order,p_sorted):probs[ix]=p
                            loads=verify(a,b,ws,probs)
                            assert loads[0]-loads[1]==gap
                            best={'gap':gap,'loads':loads,'prob_first':probs}
                            best_score=value
    assert best is not None
    best['score']=best_score;best['stats']=stats
    return best


def brute_pair(a,b,weights,target=None,score=None):
    # Independent support enumeration for small regression checks only.
    from itertools import product
    a,b=frac(a),frac(b);w=list(map(frac,weights));total=a+b+sum(w,Q(0))
    if target is None:target=-total
    target=frac(target)
    if score is None:score=lambda d:d
    best=None
    for word in product([0,1,2],repeat=len(w)):
        k=word.count(2)
        z=a-b+sum((v if t==1 else -v if t==0 else Q(0) for v,t in zip(w,word)),Q(0))
        lo=-total;hi=total
        for v,t in zip(w,word):
            if t==0:lo=max(lo,-v)
            if t==1:hi=min(hi,v)
            if t==2:lo=max(lo,-v);hi=min(hi,v)
        if lo>hi:continue
        if k==1:
            if z!=0:continue
            gap=min(hi,max(lo,target))
        else:
            gap=z/(1-k)
            if not lo<=gap<=hi:continue
        val=score(gap)
        if best is None or val<best[0]:best=(val,gap)
    return best


def game_solve(data):
    w=list(map(frac,data['weights'])); sites=[set(x) for x in data['locations']];N=len(sites)
    assert N and all(0<=i<len(w) for s in sites for i in s)
    m=[[Q(0)]*N for _ in range(N)]; punish={}; pair_data={}
    counts={'pair_oracle_calls':0,'half_states':0,'queries':0}
    def solve(a,b,c,**kw):
        ans=optimize_pair(a,b,c,**kw);counts['pair_oracle_calls']+=1
        for k in ('half_states','queries'):counts[k]+=ans['stats'][k]
        return ans
    for s in range(N):
        for t in range(s,N):
            common=sorted(sites[s]&sites[t]); a=sum((w[i] for i in sites[s]-sites[t]),Q(0));b=sum((w[i] for i in sites[t]-sites[s]),Q(0));c=[w[i] for i in common]
            pair_data[s,t]=(a,b,c,common)
            mn=solve(a,b,c);mx=solve(a,b,c,target=a+b+sum(c,Q(0)),score=lambda gap:-gap)
            m[s][t]=mn['loads'][0];m[t][s]=mx['loads'][1]
            punish[s,t]={'common':common,**mn}
            punish[t,s]={'common':common,'prob_first':[1-x for x in mx['prob_first']],'loads':mx['loads'][::-1]}
    d=[max(m[s][t] for s in range(N)) for t in range(N)]
    response=[max(range(N),key=lambda s:m[s][t]) for t in range(N)]
    seen={};path=[];v=0
    while v not in seen:seen[v]=len(path);path.append(v);v=response[v]
    ring=path[seen[v]:]
    def ratio(num,den):
        if not num:return Q(0)
        return num/den if den else float('inf')
    best=None
    for (s,t),(a,b,c,common) in pair_data.items():
        f=a+b+sum(c,Q(0));den=d[t]+d[s]
        target=f*(d[t]-d[s])/den if den else Q(0)
        score=lambda gap:max(Q(1),ratio(d[t],(f+gap)/2),ratio(d[s],(f-gap)/2))
        ans=solve(a,b,c,target=target,score=score)
        if best is None or ans['score']<best['alpha']:
            best={'layout':[s,t],'alpha':ans['score'],'on_path':{'common':common,**ans}}
    s,t=best['layout'];certificate=[]
    for deviator,opponent,current in [(0,t,s),(1,s,t)]:
        for destination in range(N):
            if destination==current:continue
            p=punish[destination,opponent]
            verify(*pair_private(data,destination,opponent),p['prob_first'])
            assert p['loads'][0]<=best['alpha']*best['on_path']['loads'][deviator]
            certificate.append({'deviator':deviator,'destination':destination,'opponent':opponent,**p})
    return {'status':'exact','m':m,'d':d,'response':response,'ring':ring,**best,'deviation_certificate':certificate,'counts':counts}


def pair_private(data,s,t):
    w=list(map(frac,data['weights']));ss=set(data['locations'][s]);tt=set(data['locations'][t])
    return sum((w[i] for i in ss-tt),Q(0)),sum((w[i] for i in tt-ss),Q(0)),[w[i] for i in sorted(ss&tt)]


def selftest():
    rng=random.Random(604030);cases=0
    # Includes continuum with one mixer, zero overlaps, ties, private domination.
    seeds=[(0,0,[1]),(0,0,[3,3,3,3]),(20,0,[1,2]),(0,8,[]),(0,0,[])]
    seeds += [(rng.randrange(10),rng.randrange(10),[Q(rng.randrange(1,10),rng.randrange(1,5)) for _ in range(rng.randrange(8))]) for _ in range(140)]
    for a,b,w in seeds:
        total=frac(a)+frac(b)+sum(w,Q(0))
        for target,score in [(-total,lambda z:z),(total,lambda z:-z),(Q(1,3),lambda z:abs(z-Q(1,3)))]:
            ans=optimize_pair(a,b,w,target,score);ref=brute_pair(a,b,w,target,score)
            assert ans['score']==ref[0],(a,b,w,target,ans,ref)
            cases+=1
    for _ in range(12):
        data={'weights':[rng.randrange(1,10) for _ in range(7)],'locations':[[i for i in range(7) if rng.random()<.6] for _ in range(4)]}
        ans=game_solve(data)
        assert ans['alpha']**2-ans['alpha']-1<=0,ans
    return {'pair_regression_checks':cases,'global_games':12,'status':'passed'}


def serial(obj):
    if isinstance(obj,Q):return str(obj)
    if isinstance(obj,dict):return {str(k):serial(v) for k,v in obj.items()}
    if isinstance(obj,(tuple,list)):return [serial(v) for v in obj]
    return obj





def greedy_pair(a,b,weights):
    """Descending-weight list scheduling with fixed private baselines is a pure NE."""
    a,b=frac(a),frac(b);w=list(map(frac,weights));p=[Q(0)]*len(w);l,r=a,b
    for i in sorted(range(len(w)),key=lambda i:w[i],reverse=True):
        if l<=r:p[i]=Q(1);l+=w[i]
        else:r+=w[i]
    assert verify(a,b,w,p)==(l,r)
    return {'prob_first':p,'loads':(l,r),'gap':l-r}


def lazy_ring_solve(data):
    """Exact lazy maximin ring; finds the best ratio on that ring.
    Does not claim this ratio is the optimum over all locations.
    """
    N=len(data['locations']);ds={};br={};punish={};path=[];seen={};v=0
    stats={'exact_pair_calls':0,'pruned_responses':0,'visited_locations':0}
    while v not in seen:
        seen[v]=len(path);path.append(v)
        uppers=[]
        for s in range(N):
            a,b,w=pair_private(data,s,v);g=greedy_pair(a,b,w)
            common=sorted(set(data['locations'][s])&set(data['locations'][v]))
            punish[s,v]={'common':common,**g}
            uppers.append((g['loads'][0],s,a,b,w))
        best=Q(-1);winner=None
        for upper,s,a,b,w in sorted(uppers,reverse=True):
            if upper<=best:
                stats['pruned_responses']+=1;continue
            exact=optimize_pair(a,b,w);stats['exact_pair_calls']+=1
            punish[s,v]={'common':punish[s,v]['common'],**exact}
            value=exact['loads'][0]
            if value>best:best=value;winner=s
        ds[v]=best;br[v]=winner;v=winner
    ring=path[seen[v]:];stats['visited_locations']=len(path)
    best=None
    def div(n,d):return n/d if d else (Q(0) if n==0 else float('inf'))
    for si,s in enumerate(ring):
        for t in ring[si:]:
            a,b,w=pair_private(data,s,t);f=a+b+sum(w,Q(0));den=ds[s]+ds[t]
            target=f*(ds[t]-ds[s])/den if den else Q(0)
            objective=lambda gap:max(Q(1),div(2*ds[t],f+gap),div(2*ds[s],f-gap))
            ans=optimize_pair(a,b,w,target,objective);stats['exact_pair_calls']+=1
            if best is None or ans['score']<best['alpha']:
                best={'layout':[s,t],'alpha':ans['score'],'on_path':{'common':sorted(set(data['locations'][s])&set(data['locations'][t])),**ans}}
    s,t=best['layout'];certificate=[]
    for deviator,opponent,current in [(0,t,s),(1,s,t)]:
        for dest in range(N):
            if dest==current:continue
            p=punish[dest,opponent]
            assert p['loads'][0]<=best['alpha']*best['on_path']['loads'][deviator]
            certificate.append({'deviator':deviator,'destination':dest,'opponent':opponent,**p})
    assert best['alpha']**2-best['alpha']-1<=0,'Counterexample to ring theorem or implementation error'
    return {'status':'exact_ring_restricted','ring':ring,'visited_path':path,'d_on_visited':ds,'response_on_visited':br,**best,'deviation_certificate':certificate,'stats':stats}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('input',nargs='?');ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
    start=time.perf_counter()
    if args.self_test:out=selftest()
    else:
        with open(args.input) as f:dat=json.load(f,parse_float=str)
        out=game_solve(dat) if 'locations' in dat else optimize_pair(dat.get('A',0),dat.get('B',0),dat['weights'])
    out['elapsed_seconds']=time.perf_counter()-start
    print(json.dumps(serial(out),indent=2))
