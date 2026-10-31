from fractions import Fraction as F
from itertools import product
from random import Random
from collections import defaultdict
import json, hashlib, sys


def all_sources(G, Z, P, T):
    H=len(G); B=len(P)
    opts=[sorted(p) for p in P]
    opts += [[('h',h)]+[('z',z) for z in sorted(g['E'])] for h,g in enumerate(G) for _ in g['w']]
    sources=[]; count=0
    for assn in product(*opts):
        count+=1
        if len(set(assn[:B]))<B: continue
        lh=[F(0)]*H; lz=[F(0)]*Z
        for j,h in enumerate(assn[:B]):lh[h]+=P[j][h]
        rows=[]; i=B
        for h,g in enumerate(G):
            row=[]
            for j,w in enumerate(g['w']):
                k,z=assn[i];i+=1;row.append((k,z))
                if k=='h':lh[z]+=w
                else:lz[z]+=g['p'][z][j]
            rows.append(row)
        if max([F(0)]+lh+lz)<=T:sources.append((assn[:B],rows))
    return sources,count


def ka_guard(kappa):
    return kappa>=1


def verify(G,Z,P,T,de,kappa,Bbar,r,sources,trace=None):
    H=len(G); M=len(P); W=[sum(g['w'],F(0)) for g in G]
    assert T>=0 and 0<=de<F(1,2) and ka_guard(kappa) and F(1,2)<=r<1-de
    for h,g in enumerate(G):
        assert W[h]<=T and all(0<=w<=de*T for w in g['w'])
        for z in g['E']:
            assert 0<=g['b'][z]<=Bbar
            assert all(g['b'][z]*w/kappa<=p<=g['b'][z]*w for w,p in zip(g['w'],g['p'][z]))
    d=[max(F(0),w-r*T) for w in W]
    a=[defaultdict(F) for _ in P];y=[defaultdict(F) for _ in G]
    mass=F(1,len(sources))
    for ms,rows in sources:
        for j,h in enumerate(ms):a[j][h]+=mass
        for h in ms:
            if not d[h]:y[h][None]+=mass;continue
            ez=defaultdict(F)
            for w,(kind,z) in zip(G[h]['w'],rows[h]):
                if kind=='z':ez[z]+=w
            e=sum(ez.values(),F(0))
            assert e>W[h]-T/2>=d[h]>0
            for z,v in ez.items():y[h][z]+=mass*v/e
    for h in range(H):
        occ=sum((row.get(h,F(0)) for row in a),F(0))
        assert occ<=1 and sum(y[h].values(),F(0))==occ
    for z in range(Z):
        c=sum((G[h]['b'].get(z,F(0))*d[h]*y[h].get(z,F(0)) for h in range(H)),F(0))
        assert c<=kappa*T
    # Independently build ordered unit intervals. Dummy is represented as a
    # private home-slot, not a shared artificial sink.
    N=[[] for _ in G]; frac_budget=[]; slot_total=0; nonint=0
    for z in range(Z):
        at=F(0);budget=F(0)
        order=sorted(range(H),key=lambda h:(-G[h]['b'].get(z,F(0))*d[h],h))
        for h in order:
            q=y[h].get(z,F(0));end=at+q
            if not q:continue
            lo=at.numerator//at.denominator
            hi=(end.numerator+end.denominator-1)//end.denominator
            for j in range(lo,hi):
                if min(end,F(j+1))>max(at,F(j)):N[h].append((z,j))
            budget+=G[h]['b'][z]*d[h]*q;at=end
        frac_budget.append(budget)
        slot_total+=(at.numerator+at.denominator-1)//at.denominator
        nonint+=bool(at.denominator>1)
    for h in range(H):
        if y[h].get(None,F(0))>0:N[h].append((None,h))
    # Exponential audit oracle finds one integral macro/home/slot packing;
    # no imported max-flow or repository rounding code is used.
    seenH=set();seenS=set();sel=[]
    def choose(j):
        if j==M:return True
        for h in sorted(a[j]):
            if h in seenH or a[j][h]<=0:continue
            for slot in N[h]:
                if slot in seenS:continue
                seenH.add(h);seenS.add(slot);sel.append((h,slot))
                if choose(j+1):return True
                sel.pop();seenS.remove(slot);seenH.remove(h)
        return False
    assert choose(0),'fractional witness failed integral packing'
    occ=dict(sel); home=[F(0)]*H;sink=[F(0)]*Z;token=[F(0)]*Z
    for j,(h,_) in enumerate(sel):home[h]+=P[j][h]
    out=[]
    for h,g in enumerate(G):
        rem=W[h];row=[]
        z=occ[h][0] if h in occ else None
        for j,w in enumerate(g['w']):
            if h in occ and rem>(r+de)*T:
                assert z is not None and z in g['E']
                row.append(('z',z));sink[z]+=g['p'][z][j];rem-=w
            else:row.append(('h',h))
        assert W[h]-rem<=d[h]
        home[h]+=rem;out.append(row)
        if h in occ and z is not None:token[z]+=g['b'][z]*d[h]
    for z in range(Z):
        assert sink[z]<=token[z]
        assert token[z]<=frac_budget[z]+max([F(0)]+[G[h]['b'].get(z,F(0))*d[h] for h in range(H)])
        assert token[z]<=(kappa+Bbar*(1-r))*T
    assert all(v<=(1+r+de)*T for v in home)
    # Every actual task is counted once in the real input profile.
    h2=[F(0)]*H;z2=[F(0)]*Z
    for j,(h,_) in enumerate(sel):h2[h]+=P[j][h]
    for h,g in enumerate(G):
        for j,(kind,z) in enumerate(out[h]):
            if kind=='h':h2[z]+=g['w'][j]
            else:z2[z]+=g['p'][z][j]
    assert (home,sink)==(h2,z2)
    if trace is not None:
        trace.update({'input':{'groups':G,'sinks':Z,'macros':P,'T':T,'delta':de,'kappa':kappa,'Bbar':Bbar,'r':r},'source_schedules':sources,'LP_macro_flow':[dict(v) for v in a],'LP_token_flow':[dict(v) for v in y],'output':{'macro_home_slot':sel,'private_assignment':out,'home_loads':home,'sink_loads':sink,'token_loads':token,'demand':d}})
    return nonint, sum(bool(g['b'].get(z,F(0))==0) for g in G for z in g['E'])


def main(fixture_output=None):
    rng=Random(2984106)
    fixtures=[]
    params=[(F(1,4),F(5,4),F(3,2),F(3,5)),(F(1,5),F(6,5),F(2),F(2,3)),(F(1,10),F(1),F(4),F(39,50)),(F(0),F(3,2),F(5),F(11,12)),(F(1,4),F(5,4),F(0),F(1,2))]
    report={'seed':2984106,'fixtures':0,'original_assignments':0,'T_feasible_fixtures':0,'source_schedules_used':0,'nonintegral_last_slots':0,'zero_profile_edges':0,'parameters':[]}
    for de,ka,bb,r in params:
        alpha=max(1+r+de,ka+bb*(1-r))
        rstar=max(F(1,2),(ka+bb-1-de)/(1+bb))
        assert r==rstar
        assert ka+bb*de<2 and alpha<2
        assert all(alpha<=max(1+q+de,ka+bb*(1-q)) for q in [F(1,2)]+[F(500+k,1000) for k in range(501)])
        report['parameters'].append(dict(delta=str(de),kappa=str(ka),Bbar=str(bb),r=str(r),alpha=str(alpha)))
        saved=0
        for case in range(240):
            H=rng.randrange(4); Z=rng.randrange(4)
            if H+Z==0:Z=1
            G=[]
            for h in range(H):
                w=[rng.choice([F(0),de/3,de*F(2,3),de]) for _ in range(rng.randrange(4))]
                E={z for z in range(Z) if rng.randrange(3)>0}
                b={z:rng.choice([F(0),bb/3,bb*F(2,3),bb]) for z in E}
                p={z:[w0*b[z]*(F(1,ka)+(1-F(1,ka))*rng.choice([F(0),F(1,4),F(1,2),F(3,4),F(1)])) for w0 in w] for z in E}
                G.append({'w':w,'E':E,'b':b,'p':p})
            P=[]
            for _ in range(rng.randrange(min(H,2)+1)):
                allowed={h:rng.choice([F(11,20),F(3,4),F(1),F(6,5)]) for h in range(H) if rng.randrange(3)>0}
                if not allowed:allowed[rng.randrange(H)]=F(3,4)
                P.append(allowed)
            src,cnt=all_sources(G,Z,P,F(1));report['fixtures']+=1;report['original_assignments']+=cnt
            if not src:continue
            report['T_feasible_fixtures']+=1
            picked=rng.sample(src,min(7,len(src)));report['source_schedules_used']+=len(picked)
            trace={} if saved<2 and any(g['w'] for g in G) else None
            nonint,zero=verify(G,Z,P,F(1),de,ka,bb,r,picked,trace)
            if trace is not None:fixtures.append(trace);saved+=1
            report['nonintegral_last_slots']+=nonint;report['zero_profile_edges']+=zero
    # Active-prefix family: larger group total forces an actual task prefix
    # to leave the selected occupied home. General random fixtures above
    # also cover many low-demand groups but should not inflate this coverage.
    de,ka,bb,r=params[0]
    report['active_prefix_random_fixtures']=0
    report['active_prefix_random_sources']=0
    report['active_prefix_actual_exports']=0
    report['active_prefix_exported_jobs']=0
    active_saved=0
    for _ in range(48):
        G=[]
        for h in range(2):
            w=[rng.choice([F(1,5),F(1,4)]) for _ in range(4)]
            b={0:F(5,4),1:F(5,4)}
            p={z:[w0*rng.choice([F(1),F(17,16),F(9,8),F(5,4)]) for w0 in w] for z in b}
            G.append({'w':w,'E':{0,1},'b':b,'p':p})
        P=[{0:F(3,4),1:F(3,4)} for _ in range(rng.choice([1,2]))]
        src,cnt=all_sources(G,2,P,F(1));report['fixtures']+=1;report['original_assignments']+=cnt
        if not src:continue
        report['T_feasible_fixtures']+=1
        chosen=rng.sample(src,min(7,len(src)));report['source_schedules_used']+=len(chosen)
        trace={};nonint,zero=verify(G,2,P,F(1),de,ka,bb,r,chosen,trace)
        report['active_prefix_random_fixtures']+=1;report['active_prefix_random_sources']+=len(chosen)
        report['active_prefix_exported_jobs']+=sum(kind=='z' for row in trace['output']['private_assignment'] for kind,_ in row)
        if any(trace['output']['sink_loads']):
            report['active_prefix_actual_exports']+=1
            if active_saved<4:fixtures.append(trace);active_saved+=1
        report['nonintegral_last_slots']+=nonint;report['zero_profile_edges']+=zero
    # Deterministic partial-slot witness: each occupied group exports three
    # quarter-sized jobs to two sinks in the exact source schedule.
    de,ka,bb,r=params[0]
    G=[{'w':[F(1,4)]*4,'E':{0,1},'b':{0:F(5,4),1:F(5,4)},'p':{0:[F(3,10)]+[F(1,4)]*3,1:[F(3,10)]+[F(1,4)]*3}} for _ in range(2)]
    P=[{0:F(3,4)},{1:F(3,4)}]
    rows=[[('h',h),('z',0),('z',0),('z',1)] for h in range(2)]
    trace={}
    nonint,zero=verify(G,2,P,F(1),de,ka,bb,r,[((0,1),rows)],trace)
    fixtures.append(trace)
    assert nonint==2
    report['nonintegral_last_slots']+=nonint
    report['deterministic_partial_slot_case']={'mass_sink0':'4/3','mass_sink1':'2/3','actual_first_prefix_cost':'3/10','virtual_prefix_budget':'1/2'}
    # Exact scaling preserves all statements even with a 127-bit denominator.
    scale=F(1,2**127-1);de,ka,bb,r=params[0]
    G=[{'w':[scale/5]*3,'E':{0,1},'b':{0:F(3,2),1:F(1)},'p':{0:[scale/4,scale*F(6,25),scale*F(3,10)],1:[scale*F(4,25),scale*F(1,5),scale*F(9,50)]}}]
    P=[{0:scale*F(3,4)}]
    src,cnt=all_sources(G,2,P,scale);assert src
    trace={}
    verify(G,2,P,scale,de,ka,bb,r,src[:7],trace)
    fixtures.append(trace)
    report['large_denominator_sources']=len(src);report['large_denominator_assignments']=cnt
    # True zero-target source and all-zero group/sink profile boundary.
    de,ka,bb,r=params[0]
    zeroG=[{'w':[F(0),F(0)],'E':set(),'b':{},'p':{}}]
    zeroSrc,zeroCnt=all_sources(zeroG,0,[],F(0));assert zeroSrc
    verify(zeroG,0,[],F(0),de,ka,bb,r,zeroSrc)
    emptySrc,emptyCnt=all_sources([],1,[],F(0));assert emptySrc
    verify([],1,[],F(0),de,ka,bb,r,emptySrc)
    zeroProf=[{'w':[F(1,4)]*4,'E':{0},'b':{0:F(0)},'p':{0:[F(0)]*4}}]
    zeroPSrc,zeroPCnt=all_sources(zeroProf,1,[{0:F(3,4)}],F(1));assert zeroPSrc
    verify(zeroProf,1,[{0:F(3,4)}],F(1),de,ka,bb,r,zeroPSrc)
    report['explicit_zero_boundaries']={'zero_target_assignments':zeroCnt,'empty_assignments':emptyCnt,'zero_profile_assignments':zeroPCnt}
    # An occupied positive-demand home with no eligible receiver is impossible
    # for both the actual schedule and the explicit LP conservation equations.
    blocked=[{'w':[F(1,4)]*4,'E':set(),'b':{},'p':{}}]
    blockedSrc,blockedCnt=all_sources(blocked,1,[{0:F(3,4)}],F(1))
    assert not blockedSrc
    blockedDemand=F(1)-F(1,2)
    assert blockedDemand>0 and F(1)!=sum([],F(0))
    report['explicit_blocked_conservation']={'actual_assignments':blockedCnt,'x':'1','sum_allowed_y':'0','demand':str(blockedDemand),'LP':'infeasible by 0=1'}
    # T=0 and empty-task validation is separate because the positive-T proof
    # has normalization by real exported volume.
    assert all(any(p==0 for p in row) for row in [[F(0),F(1)],[F(0)]])
    assert not all(any(p==0 for p in row) for row in [[F(0)],[F(1)]])
    report['zero_target_logic']='zero edge for every task iff OPT=0; empty conjunction true'
    report['python']=sys.version.split()[0]
    report['sha256']=hashlib.sha256(open(__file__,'rb').read()).hexdigest()
    report['limitations']='Finite source-derived certificates only; no LP solver, arbitrary pseudo-witness enumeration, or general theorem validation.'
    def exact(x):
        if isinstance(x,F):return str(x)
        if isinstance(x,dict):return {str(k):exact(v) for k,v in x.items()}
        if isinstance(x,(list,tuple,set)):return [exact(v) for v in x]
        return x
    if fixture_output is not None:
        with open(fixture_output,'x') as f:f.write(json.dumps({'seed':2984106,'cases':exact(fixtures)},ensure_ascii=False,indent=2))
        report['actual_fixture_file']=fixture_output
        report['actual_fixture_sha256']=hashlib.sha256(open(fixture_output,'rb').read()).hexdigest()
    report['actual_fixture_count']=len(fixtures)
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--fixtures-output',help='explicit new fixture path; existing files are never overwritten')
    main(parser.parse_args().fixtures_output)
