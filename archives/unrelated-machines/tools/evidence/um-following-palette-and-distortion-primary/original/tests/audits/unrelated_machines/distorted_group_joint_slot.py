"""组内异端畸变的共同槽流：给定精确LP见证后的验证与实际舍入。

This module does not implement a general rational LP backend. Standard integer
flow and exact-rational parsing are reused from weighted_group_joint_slot.py.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util

_primitive = Path(__file__).with_name('weighted_group_joint_slot.py')
if not _primitive.exists():
    _primitive = Path.cwd() / 'tests/audits/unrelated_machines/weighted_group_joint_slot.py'
_spec = importlib.util.spec_from_file_location('_weighted_group_joint_slot', _primitive)
_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_base)
Flow, rational = _base.Flow, _base.rational


def _index(i, n):
    return isinstance(i,int) and not isinstance(i,bool) and 0 <= i < n


def round_distorted_certificate(groups, sink_count, macros, T, delta, kappa,
                               Bbar, r, macro_flow, receiver_flow):
    """groups=[{'w':[exact,...], 'E':[sink,...], 'b':{sink:upper},
                'p':{sink:[actual processing times,...]}}].

    macros and macro_flow are lists of {home:exact}; receiver_flow[h] maps a
    sink or None (zero-demand bypass) to exact mass. Each job has its own
    actual sink time. Group and sink lists are explicit.

    Success bounds do not require the macro lower bound p>T/2. That lower
    bound is used only by the theorem proving a witness exists when OPT<=T.
    """
    T,delta,kappa,Bbar,r = map(rational,(T,delta,kappa,Bbar,r))
    if T<0 or not 0<=delta<F(1,2) or kappa<1 or Bbar<0 or not F(1,2)<=r<1-delta:
        raise ValueError('invalid target or distortion/cut parameters')
    if isinstance(sink_count,bool) or not isinstance(sink_count,int) or sink_count<0:
        raise ValueError('explicit nonnegative sink count required')
    H,M=len(groups),len(macros)
    if H+sink_count<1:
        raise ValueError('at least one machine required')
    G=[];W=[]
    for g in groups:
        w=list(map(rational,g['w'])); E=set(g['E'])
        if any(not _index(z,sink_count) for z in E):
            raise ValueError('invalid eligible sink')
        b={z:rational(v) for z,v in g['b'].items()}
        p={z:list(map(rational,v)) for z,v in g['p'].items()}
        if set(b)!=E or set(p)!=E or any(not _index(z,sink_count) for z in list(b)+list(p)):
            raise ValueError('every eligible profile must be explicit')
        if any(v<0 or v>delta*T for v in w) or sum(w,F(0))>T:
            raise ValueError('private size or total bound violated')
        for z in E:
            if not 0<=b[z]<=Bbar or len(p[z])!=len(w):
                raise ValueError('invalid profile dimensions or upper multiplier')
            if any(v<0 or b[z]*u>kappa*v or v>b[z]*u for u,v in zip(w,p[z])):
                raise ValueError('actual processing profile exceeds envelope')
        G.append({'w':w,'E':E,'b':b,'p':p});W.append(sum(w,F(0)))
    P=[]
    for row in macros:
        q={h:rational(v) for h,v in row.items()}
        if not q or any(not _index(h,H) or v<0 for h,v in q.items()):
            raise ValueError('invalid macro endpoints')
        P.append(q)
    if len(macro_flow)!=M or len(receiver_flow)!=H:
        raise ValueError('flow dimensions')
    A=[]
    for j,row in enumerate(macro_flow):
        a={h:rational(v) for h,v in row.items()}
        if sum(a.values(),F(0))!=1 or any(not _index(h,H) or h not in P[j] or v<0 or (v>0 and P[j][h]>T) for h,v in a.items()):
            raise ValueError('invalid macro flow')
        A.append(a)
    d=[max(F(0),v-r*T) for v in W]
    x=[sum((a.get(h,F(0)) for a in A),F(0)) for h in range(H)]
    Y=[]
    for h,row in enumerate(receiver_flow):
        y={z:rational(v) for z,v in row.items()}
        if x[h]>1 or sum(y.values(),F(0))!=x[h]:
            raise ValueError('home capacity or same-flow conservation')
        for z,v in y.items():
            if v<0 or (z is None and d[h]>0) or (z is not None and (not _index(z,sink_count) or z not in G[h]['E'])):
                raise ValueError('invalid token endpoint or bypass')
        Y.append(y)
    budget=[]
    for z in range(sink_count):
        value=sum((G[h]['b'].get(z,F(0))*d[h]*Y[h].get(z,F(0)) for h in range(H)),F(0))
        if value>kappa*T:
            raise ValueError('distorted receiver budget exceeded')
        budget.append(value)
    net=Flow();s=('source',);t=('target',)
    for j,a in enumerate(A):
        net.add(s,('macro',j),1)
        for h in sorted(a):
            if a[h]>0:net.add(('macro',j),('hi',h),1)
    for h in range(H):net.add(('hi',h),('ho',h),1)
    neighbor=[[] for _ in G];slots=set()
    for z in range(sink_count):
        at=F(0)
        order=sorted(range(H),key=lambda h:(-G[h]['b'].get(z,F(0))*d[h],h))
        for h in order:
            mass=Y[h].get(z,F(0))
            if not mass:continue
            end=at+mass
            lo=at.numerator//at.denominator
            hi=(end.numerator+end.denominator-1)//end.denominator
            for j in range(lo,hi):
                if min(end,F(j+1))<=max(at,F(j)):continue
                slot=('slot',z,j)
                neighbor[h].append((z,j))
                net.add(('ho',h),slot,1)
                if slot not in slots:
                    slots.add(slot);net.add(slot,t,1)
            at=end
    for h in range(H):
        if Y[h].get(None,F(0))>0:
            neighbor[h].append((None,h));net.add(('ho',h),t,1)
    assert net.maxflow(s,t)==M,'validated fractional witness must lift to integer flow'
    chosen=[];occupied={}
    for j,a in enumerate(A):
        homes=[h for h in sorted(a) if a[h]>0 and net.used(('macro',j),('hi',h))==1]
        assert len(homes)==1
        h=homes[0];assert h not in occupied
        dest=[]
        for z,k in neighbor[h]:
            node=t if z is None else ('slot',z,k)
            if net.used(('ho',h),node)==1:dest.append((z,k))
        assert len(dest)==1
        occupied[h]=dest[0];chosen.append(h)
    home=[F(0)]*H;sink=[F(0)]*sink_count;token=[F(0)]*sink_count
    for j,h in enumerate(chosen):home[h]+=P[j][h]
    assignment=[]
    for h,g in enumerate(G):
        row=[('h',h)]*len(g['w']);rem=W[h]
        if h in occupied:
            z,_=occupied[h]
            if z is not None:token[z]+=g['b'][z]*d[h]
            for j,w in enumerate(g['w']):
                if rem<=(r+delta)*T:break
                assert z is not None and z in g['E']
                row[j]=('z',z);sink[z]+=g['p'][z][j];rem-=w
            assert W[h]-rem<=d[h]
        home[h]+=rem;assignment.append(row)
    for z in range(sink_count):
        assert sink[z]<=token[z]
        assert token[z]<=budget[z]+max([F(0)]+[g['b'].get(z,F(0))*d[h] for h,g in enumerate(G)])
        assert token[z]<=(kappa+Bbar*(1-r))*T
    assert all(v<=(1+r+delta)*T for v in home)
    return {'macro_assignment':chosen,'private_assignment':assignment,
            'home_loads':home,'sink_loads':sink,'token_loads':token,
            'demand':d,'fractional_sink_costs':budget,'selected_slots':occupied,
            'makespan':max([F(0)]+home+sink),'slot_count':len(slots)}


def actual_loads(G,Z,P,macro_assignment,private_assignment):
    """Independently recalculate all actual loads from complete task output."""
    H=len(G)
    if len(macro_assignment)!=len(P) or len(private_assignment)!=H:
        raise ValueError('incomplete output')
    home=[F(0)]*H;sink=[F(0)]*Z
    for j,h in enumerate(macro_assignment):
        if h not in P[j]:raise ValueError('illegal actual macro endpoint')
        home[h]+=rational(P[j][h])
    for h,(g,row) in enumerate(zip(G,private_assignment)):
        if len(row)!=len(g['w']):raise ValueError('incomplete private output')
        for j,(kind,z) in enumerate(row):
            if kind=='h' and z==h:home[h]+=rational(g['w'][j])
            elif kind=='z' and z in g['E']:sink[z]+=rational(g['p'][z][j])
            else:raise ValueError('illegal actual private endpoint')
    return home,sink


def audit_fixtures(path):
    import json,sys,hashlib
    raw=Path(path).read_bytes();data=json.loads(raw)
    reports=[]
    for case in data['cases']:
        a=case['input'];G=a['groups']
        for g in G:
            g['b']={int(z):v for z,v in g['b'].items()}
            g['p']={int(z):v for z,v in g['p'].items()}
        P=[{int(h):v for h,v in row.items()} for row in a['macros']]
        mf=[{int(h):v for h,v in row.items()} for row in case['LP_macro_flow']]
        yf=[{None if z=='None' else int(z):v for z,v in row.items()} for row in case['LP_token_flow']]
        ans=round_distorted_certificate(G,a['sinks'],P,a['T'],a['delta'],a['kappa'],a['Bbar'],a['r'],mf,yf)
        recalculated=actual_loads(G,a['sinks'],P,ans['macro_assignment'],ans['private_assignment'])
        assert recalculated==(ans['home_loads'],ans['sink_loads'])
        old=case['output'];oldmacros=[h for h,_ in old['macro_home_slot']]
        oldhome,oldsink=actual_loads(G,a['sinks'],P,oldmacros,old['private_assignment'])
        assert oldhome==list(map(F,old['home_loads'])) and oldsink==list(map(F,old['sink_loads']))
        T,de,ka,bb,r=map(F,(a['T'],a['delta'],a['kappa'],a['Bbar'],a['r']))
        assert all(v<=(1+r+de)*T for v in oldhome)
        assert all(v<=(ka+bb*(1-r))*T for v in oldsink)
        reports.append({'home_loads':list(map(str,ans['home_loads'])),'sink_loads':list(map(str,ans['sink_loads'])),'same_assignment_as_independent':ans['macro_assignment']==oldmacros and [list(map(list,row)) for row in ans['private_assignment']]==old['private_assignment']})
    boundary_reports=[]
    direct=[
        ('zero_target',[{'w':['0','0'],'E':[],'b':{},'p':{}}],0,[],'0','1/4','5/4','3/2','3/5',[],[{}]),
        ('empty_tasks',[],1,[],'0','1/4','5/4','3/2','3/5',[],[]),
        ('single_machine',[{'w':[],'E':[],'b':{},'p':{}}],0,[{0:'3/4'}],'1','1/4','5/4','3/2','3/5',[{0:'1'}],[{None:'1'}]),
        ('zero_profile_active_prefix',[{'w':['1/4']*4,'E':[0],'b':{0:'0'},'p':{0:['0']*4}}],1,[{0:'3/4'}],'1','1/4','5/4','0','1/2',[{0:'1'}],[{0:'1'}]),
        ('delta_zero',[{'w':['0'],'E':[0],'b':{0:'1'},'p':{0:['0']}}],1,[{0:'3/4'}],'1','0','3/2','5','11/12',[{0:'1'}],[{None:'1'}]),
    ]
    for label,G,Z,P,T,de,ka,bb,r,mf,yf in direct:
        out=round_distorted_certificate(G,Z,P,T,de,ka,bb,r,mf,yf)
        assert actual_loads(G,Z,P,out['macro_assignment'],out['private_assignment'])==(out['home_loads'],out['sink_loads'])
        boundary_reports.append({'case':label,'home_loads':list(map(str,out['home_loads'])),'sink_loads':list(map(str,out['sink_loads'])),'exported_jobs':sum(kind=='z' for row in out['private_assignment'] for kind,_ in row)})
    return {'fixture_count':len(reports),'fixtures_sha256':hashlib.sha256(raw).hexdigest(),'implementation_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':sys.version.split()[0],'replays':reports,'direct_boundaries':boundary_reports,'scope':'exact supplied-LP witness rounding and both complete outputs recalculated; no LP backend'}

if __name__=='__main__':
    import argparse,json
    ap=argparse.ArgumentParser();ap.add_argument('fixtures')
    print(json.dumps(audit_fixtures(ap.parse_args().fixtures),ensure_ascii=False,indent=2))
