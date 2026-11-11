"""Exact single-row coupling upper bounds with the fixed NEW mu marginals.

Every pair transport is only an upper bound on a row of a common law.
Their separate optimizers are never asserted jointly realizable.  Negative
bounds would exclude this fixed-mu lift, not the original necessary point.
No optimizer or floating point is used for these transportation problems.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import json,time
from model import Model, bits, q, dump, serial, sha, MU, NET, POINT, PINS


def transport_max(left, right, coefficient):
    """Rational min-cost flow, with an independently checkable exact dual."""
    lx,ry=list(left),list(right)
    H=sum(left.values(),F())
    assert H==sum(right.values(),F()) and H>0
    nl,nr=len(lx),len(ry)
    start,end=nl+nr,nl+nr+1
    nv=end+1
    edges=[];adj=[[] for _ in range(nv)]
    def edge(a,b,cap,cost):
        idx=len(edges)
        edges.append([a,b,cap,cost,F()]);edges.append([b,a,F(),-cost,F()])
        adj[a].append(idx);adj[b].append(idx+1)
        return idx
    for i,s in enumerate(lx):edge(start,i,left[s],F())
    arc={}
    for i,s in enumerate(lx):
        for j,t in enumerate(ry):arc[i,j]=edge(i,nl+j,2*H,-coefficient(s,t))
    for j,t in enumerate(ry):edge(nl+j,end,right[t],F())
    sent=F();augmentations=0
    while sent<H:
        dist=[None]*nv;previous=[None]*nv;dist[start]=F()
        for _ in range(nv-1):
            changed=False
            for ei,(a,b,cap,cost,flow) in enumerate(edges):
                if cap-flow>0 and dist[a] is not None:
                    new=dist[a]+cost
                    if dist[b] is None or new<dist[b]:
                        dist[b]=new;previous[b]=ei;changed=True
            if not changed:break
        assert dist[end] is not None
        path=[];node=end
        while node!=start:
            ei=previous[node];assert ei is not None
            path.append(ei);node=edges[ei][0]
            assert len(path)<=nv
        amount=min([H-sent]+[edges[ei][2]-edges[ei][4] for ei in path])
        assert amount>0
        for ei in path:
            edges[ei][4]+=amount;edges[ei^1][4]-=amount
        sent+=amount;augmentations+=1
    # Super-source zero distances give feasible residual potentials.
    dist=[F()]*nv
    for iteration in range(nv):
        changed=False
        for a,b,cap,cost,flow in edges:
            if cap-flow>0 and dist[b]>dist[a]+cost:
                dist[b]=dist[a]+cost;changed=True
        if not changed:break
        assert iteration<nv-1,'negative residual cycle'
    alpha={s:dist[i] for i,s in enumerate(lx)}
    beta={t:-dist[nl+j] for j,t in enumerate(ry)}
    primal=F();coupling=[]
    for i,s in enumerate(lx):
        for j,t in enumerate(ry):
            c=coefficient(s,t);flow=edges[arc[i,j]][4]
            assert alpha[s]+beta[t]>=c
            if flow:
                assert alpha[s]+beta[t]==c
                coupling.append(dict(left=s,right=t,mass=flow))
                primal+=flow*c
    assert all(sum((r['mass'] for r in coupling if r['left']==s),F())==left[s] for s in lx)
    assert all(sum((r['mass'] for r in coupling if r['right']==t),F())==right[t] for t in ry)
    dual=sum((left[s]*alpha[s] for s in lx),F())+sum((right[t]*beta[t] for t in ry),F())
    assert primal==dual
    return dict(upper=dual,left=[dict(state=s,mass=left[s],dual=alpha[s]) for s in lx],
        right=[dict(state=t,mass=right[t],dual=beta[t]) for t in ry],
        coefficients=[[coefficient(s,t) for t in ry] for s in lx],
        optimal_pair_coupling=coupling,augmentations=augmentations)


def root_coefficient(name,v,w,s,t):
    own,donor=bits(s,5),bits(t,5)
    st,dt=v>>2,w>>2
    if name[0]=='cross-floor':
        k,l=name[1:]
        return q(own[k],st+sum(own))-F(donor[l],st+sum(own[:k])+5-k)
    assert name[0]=='cross-pair'
    x,y=name[1:]
    pref=st+sum(own[:3])
    wallet=F(own[3],pref+1+own[4])+F(own[4],pref+1+own[3])+F(own[3],(pref+1)*(pref+2))
    target=(dt,)+donor
    return wallet-F(target[x]+target[y],pref+1)+F(target[x]*target[y],(pref+1)*(pref+2))


def main():
    started=time.monotonic();m=Model()
    product_report=json.loads((Path(__file__).parent/'conditional_product_exact.json').read_text())
    rows=[]
    own={};cur=None
    for cidx,c in enumerate(m.point['columns'][:4849]):
        if c['kind']=='hist':cur=cidx
        elif c['kind']=='joint-reply':
            f,diag,v,w=c['group'];key=(cur,f,diag,tuple(v),tuple(w))
            own.setdefault(key,{})[tuple(c['state'])]=F(c['weight'])
    for key,ss in own.items():
        ss[0,0]=m.H[key[0]]-sum(ss.values(),F())
    transports=0
    for negative in product_report['negative_rows']:
        name=negative['name'];pieces=[];bound=F()
        if name[0] in ('cross-floor','cross-pair'):
            norm=6 if name[0]=='cross-floor' else 30
            for h,hc in m.hist.items():
                if not m.H[h]:continue
                for v,nv in enumerate(hc['hist']):
                    for w,nw in enumerate(hc['hist']):
                        count=nv*(nw-int(v==w))
                        if not count:continue
                        cert=transport_max(m.mu[h,v],m.mu[h,w],lambda s,t:root_coefficient(name,v,w,s,t))
                        factor=F(count,norm);bound+=factor*cert['upper'];transports+=1
                        pieces.append(dict(hist=h,source_old_word=v,donor_old_word=w,named_pair_count=count,
                                           factor=factor,**cert))
        else:
            assert name[0]=='Y-to-R' and name[1]==[1,[0,0,0]] and name[2]==4
            for h,hc in m.hist.items():
                if not m.H[h]:continue
                for w,count in enumerate(hc['hist']):
                    if not count:continue
                    ss=own[h,1,1,bits(w,3),bits(w,3)]
                    qr=ss[1,0]+ss[1,1]
                    right={b:mass for b,mass in [(0,m.H[h]-qr),(1,qr)] if mass}
                    def coefficient(s,r):
                        e=bits(s,5);t=w>>2
                        return q(e[4],t+sum(e))-F(r,t+sum(e[:4])+1)
                    cert=transport_max(m.mu[h,w],right,coefficient)
                    factor=F(count,6);bound+=factor*cert['upper'];transports+=1
                    pieces.append(dict(hist=h,root_old_word=w,named_count=count,factor=factor,**cert))
        rows.append(dict(name=name,conditional_product_slack=negative['slack'],conditional_product_approx=negative['approx'],
            upper=bound,upper_approx=float(bound),negative=bound<0,pieces=pieces))
    report=dict(status='EXACT_PAIR_TRANSPORT_UPPER_BOUNDS',point_sha256=PINS[POINT],mu_sha256=PINS[MU],
        network_input_sha256=PINS[NET],script_sha256=sha(Path(__file__)),
        scope='Bounds only use the fixed new mu and, for the reverse R query, the original own R marginal. They apply to every common coupling, without fixing the 100-atom network. Pair optimizers are not a joint certificate.',
        tested_product_failures=len(rows),negative_upper_bounds=sum(r['negative'] for r in rows),
        exact_transport_problems=transports,rows=rows,elapsed_seconds=time.monotonic()-started)
    dump('fixed_mu_upper_bounds_exact.json',report)
    print(json.dumps(serial(dict(tested=len(rows),negative=report['negative_upper_bounds'],transports=transports,
        bounds=[{k:r[k] for k in ('name','conditional_product_approx','upper','upper_approx','negative')} for r in rows],
        elapsed_seconds=report['elapsed_seconds'])),ensure_ascii=False))


if __name__=='__main__':main()
