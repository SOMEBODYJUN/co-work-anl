"""共同资格私有组的加权槽联合整数流；输入精确有理 LP 证书，未实现通用 LP 求解。"""
from fractions import Fraction as F
from collections import deque


def rational(x):
    if isinstance(x, bool) or isinstance(x, float):
        raise ValueError('exact rational required')
    return F(x)


class Flow:
    def __init__(self):
        self.adj = {}
        self.cap = {}
        self.initial = {}
    def add(self, u, v, c):
        if (u,v) in self.initial:
            raise ValueError('duplicate edge')
        self.adj.setdefault(u, []).append(v)
        self.adj.setdefault(v, []).append(u)
        self.cap[u,v] = c
        self.cap[v,u] = 0
        self.initial[u,v] = c
    def maxflow(self, s, t):
        value = 0
        while True:
            previous = {s: None}
            queue = deque([s])
            while queue and t not in previous:
                u = queue.popleft()
                for v in self.adj.get(u, []):
                    if v not in previous and self.cap[u,v] > 0:
                        previous[v] = u
                        queue.append(v)
            if t not in previous:
                return value
            v = t
            while v != s:
                u = previous[v]
                self.cap[u,v] -= 1
                self.cap[v,u] += 1
                v = u
            value += 1
    def used(self, u, v):
        return self.initial.get((u,v), 0) - self.cap.get((u,v), 0)


def round_certificate(groups, sink_count, macros, T, delta, macro_flow, receiver_flow):
    """groups=[{'weights':[exact,...], 'eligible':[0,...]}].
    macros=[{home: exact processing_time,...}]. macro_flow mirrors macros.
    receiver_flow[h]={z:exact unit mass,...}, z=None denotes zero-demand dummy.
    Private jobs are available at their home and all listed eligible sinks,
    with the same weight on each. Successful rounding only needs finite macro
    times >=0; the theorem uses large macro times to supply LP feasibility.
    Output private_assignment[h][j] is ('h',h)
    or ('z',z); macro_assignment[b] is the actual chosen home.
    """
    T, delta = rational(T), rational(delta)
    if T < 0 or delta < 0 or delta >= F(1,2):
        raise ValueError('require T>=0 and 0<=delta<1/2')
    if isinstance(sink_count,bool) or not isinstance(sink_count,int) or sink_count < 0:
        raise ValueError('explicit nonnegative sink count required')
    H, B = len(groups), len(macros)
    if H+sink_count<1:
        raise ValueError('at least one explicit machine required')
    weights=[]; E=[]; W=[]
    for g in groups:
        w=[rational(v) for v in g['weights']]
        e=set(g['eligible'])
        if any(isinstance(z,bool) or not isinstance(z,int) or z<0 or z>=sink_count for z in e):
            raise ValueError('illegal receiver')
        if any(v<0 or v>delta*T for v in w) or sum(w,F(0))>T:
            raise ValueError('private size or group upper bound violated')
        weights.append(w); E.append(e); W.append(sum(w,F(0)))
    p=[]
    for row in macros:
        row2={h:rational(t) for h,t in row.items()}
        if not row2 or any(isinstance(h,bool) or not isinstance(h,int) or h<0 or h>=H or t<0 for h,t in row2.items()):
            raise ValueError('macro domain violated')
        p.append(row2)
    if len(macro_flow)!=B or len(receiver_flow)!=H:
        raise ValueError('certificate dimensions')
    f=[]; x=[]
    for b,row in enumerate(macro_flow):
        row2={h:rational(v) for h,v in row.items()}
        if any(isinstance(h,bool) or not isinstance(h,int) or h not in p[b] or v<0 or (v>0 and p[b][h]>T) for h,v in row2.items()) or sum(row2.values(),F(0))!=1:
            raise ValueError('illegal macro flow')
        f.append(row2)
    occupancy=[sum((row.get(h,F(0)) for row in f),F(0)) for h in range(H)]
    d=[max(F(0),w-T/2) for w in W]
    for h,row in enumerate(receiver_flow):
        row2={z:rational(v) for z,v in row.items()}
        if occupancy[h]>1 or any(v<0 or (z is None and d[h]!=0) or (z is not None and (isinstance(z,bool) or not isinstance(z,int) or z not in E[h])) for z,v in row2.items()):
            raise ValueError('illegal receiver flow')
        if sum(row2.values(),F(0))!=occupancy[h]:
            raise ValueError('home conservation')
        x.append(row2)
    for z in range(sink_count):
        if sum((d[h]*x[h].get(z,F(0)) for h in range(H)),F(0))>T:
            raise ValueError('weighted receiver budget')
    network=Flow(); s=('source',); t=('target',)
    for b in range(B):
        network.add(s,('b',b),1)
        for h in sorted(f[b]):
            if f[b][h]>0:
                network.add(('b',b),('hi',h),1)
    for h in range(H):
        network.add(('hi',h),('ho',h),1)
    slots=[]; neighbors={h:[] for h in range(H)}
    for z in [None]+list(range(sink_count)):
        at=F(0)
        for h in sorted(range(H),key=lambda h:(-d[h],h)):
            mass=x[h].get(z,F(0))
            if not mass:
                continue
            right=at+mass
            lo=at.numerator//at.denominator
            hi=-((-right.numerator)//right.denominator)
            for k in range(lo,hi):
                overlap=min(right,F(k+1))-max(at,F(k))
                if overlap>0:
                    slot=('slot',z,k)
                    neighbors[h].append((z,k))
                    network.add(('ho',h),slot,1)
                    if slot not in slots:
                        slots.append(slot)
                        network.add(slot,t,1)
            at=right
    assert network.maxflow(s,t)==B, 'valid fractional witness must lift to integral flow'
    macro_assignment=[]
    occupied={}
    for b in range(B):
        hs=[h for h in sorted(f[b]) if f[b][h]>0 and network.used(('b',b),('hi',h))==1]
        assert len(hs)==1
        h=hs[0]; macro_assignment.append(h)
        choices=[(z,k) for z,k in neighbors[h] if network.used(('ho',h),('slot',z,k))==1]
        assert len(choices)==1 and h not in occupied
        occupied[h]=choices[0]
    home_loads=[F(0)]*H
    sink_loads=[F(0)]*sink_count
    slot_loads=[F(0)]*sink_count
    private_assignment=[]
    tau=F(1,2)+delta
    for b,h in enumerate(macro_assignment):
        home_loads[h]+=p[b][h]
    for h in range(H):
        row=[('h',h)]*len(weights[h])
        rem=W[h]
        if h in occupied:
            z,_=occupied[h]
            if z is not None:
                slot_loads[z]+=d[h]
            for j,w in enumerate(weights[h]):
                if rem<=tau*T:
                    break
                assert z is not None and z in E[h]
                row[j]=('z',z)
                sink_loads[z]+=w
                rem-=w
            assert W[h]-rem<=d[h]
        home_loads[h]+=rem
        private_assignment.append(row)
    assert all(v<=F(3,2)*T for v in slot_loads)
    assert all(v<=F(3,2)*T for v in sink_loads)
    assert all(v<=(F(3,2)+delta)*T for v in home_loads)
    return {'macro_assignment':macro_assignment,'private_assignment':private_assignment,
            'home_loads':home_loads,'sink_loads':sink_loads,
            'slot_demand_loads':slot_loads,'demand':d,
            'slot_count':len(slots),
            'makespan':max([F(0)]+home_loads+sink_loads)}


def original_schedules(groups,Z,macros,T):
    from itertools import product
    H=len(groups)
    options=[list(row) for row in macros]
    options += [[('h',h)]+[('z',z) for z in g['eligible']] for h,g in enumerate(groups) for _ in g['weights']]
    good=[]; checked=0
    for a in product(*options):
        checked+=1
        home=[F(0)]*H; sink=[F(0)]*Z
        macropos=a[:len(macros)]
        if len(set(macropos))<len(macropos):
            continue
        for b,h in enumerate(macropos): home[h]+=macros[b][h]
        choices=[]; at=len(macros)
        for h,g in enumerate(groups):
            row=[]
            for w in g['weights']:
                kind,i=a[at]; at+=1; row.append((kind,i))
                if kind=='h': home[i]+=w
                else: sink[i]+=w
            choices.append(row)
        if max([F(0)]+home+sink)<=T: good.append((macropos,choices))
    return good,checked


def certificate(groups,Z,macros,T,schedules):
    H=len(groups); f=[{} for _ in macros]; x=[{} for _ in groups]
    mass=F(1,len(schedules))
    for macropos,choices in schedules:
        for b,h in enumerate(macropos):
            f[b][h]=f[b].get(h,F(0))+mass
        for h in macropos:
            W=sum(groups[h]['weights'],F(0)); d=max(F(0),W-T/2)
            if d==0:
                x[h][None]=x[h].get(None,F(0))+mass
                continue
            export={}
            for w,(kind,z) in zip(groups[h]['weights'],choices[h]):
                if kind=='z': export[z]=export.get(z,F(0))+w
            e=sum(export.values(),F(0))
            assert e>=d>0
            for z,w in export.items(): x[h][z]=x[h].get(z,F(0))+mass*w/e
    return f,x


def audit_fixtures(path):
    """Replay actual exact inputs/certificates; this does not implement LP solving."""
    import hashlib, json, sys
    from pathlib import Path
    fixtures=json.loads(Path(path).read_text())
    reports=[]
    for case in fixtures['cases']:
        args=case['input']
        groups=args['groups']
        macros=[dict(row) for row in args['macros']]
        f=[dict(row) for row in args['macro_flow']]
        x=[dict(row) for row in args['receiver_flow']]
        out=round_certificate(groups,args['sink_count'],macros,args['T'],args['delta'],f,x)
        # Recompute every actual task against input availability and sizes.
        home=[F(0)]*len(groups); sink=[F(0)]*args['sink_count']
        assert len(out['macro_assignment'])==len(macros)
        for b,h in enumerate(out['macro_assignment']):
            home[h]+=rational(macros[b][h])
        for h,(g,row) in enumerate(zip(groups,out['private_assignment'])):
            assert len(row)==len(g['weights'])
            for w,(kind,i) in zip(g['weights'],row):
                if kind=='h':
                    assert i==h
                    home[h]+=rational(w)
                else:
                    assert i in g['eligible']
                    sink[i]+=rational(w)
        assert home==out['home_loads'] and sink==out['sink_loads']
        source_scope=case.get('source_enumeration')
        if source_scope is not None:
            exact_groups=[{'weights':[rational(w) for w in g['weights']],
                           'eligible':g['eligible']} for g in groups]
            exact_macros=[{h:rational(v) for h,v in row.items()} for row in macros]
            sources, checked=original_schedules(exact_groups,args['sink_count'],exact_macros,rational(args['T']))
            assert checked==source_scope['all_assignments']
            assert len(sources)==source_scope['feasible_source_schedules']
            source_f,source_x=certificate(exact_groups,args['sink_count'],exact_macros,rational(args['T']),sources)
            assert source_f==[{h:rational(v) for h,v in row.items()} for row in f]
            assert source_x==[{z:rational(v) for z,v in row.items()} for row in x]
        expected=case['expected']
        assert [str(v) for v in home]==expected['home_loads']
        assert [str(v) for v in sink]==expected['sink_loads']
        assert str(out['makespan'])==expected['makespan']
        reports.append({'case':case['name'],'output':out,
                        'independent_source_scope':case.get('source_enumeration')})
    return {'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'fixtures_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            'python':sys.version,'reports':reports,
            'scope':'finite exact input-certificate replay; generic rational LP backend not implemented'}


if __name__=='__main__':
    import argparse, json
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixtures', required=True)
    args=parser.parse_args()
    print(json.dumps(audit_fixtures(args.fixtures),default=str,indent=2))
