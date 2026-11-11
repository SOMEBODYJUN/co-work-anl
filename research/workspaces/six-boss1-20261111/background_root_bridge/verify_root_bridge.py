"""Standard-library independent audit of the saved root-envelope witness.

No solver or construction module imports. Reconstructs all 71 scalar budgets
from real-history formulas, verifies the shared marginal identities, checks
the displayed closed-form necessary row, and computes a genuine six-player
cycle's unpaid Theta using the previously proved two-group SPE construction.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from itertools import combinations
import hashlib,json

OUT=Path(__file__).resolve().parent;RUN=OUT.parent;OLD=RUN/'background_five_bridge'
EPS=F(62212762317811658581,1250000000000000000000);KAP=F(226487,10**21)
def q(n,d):return F(n,d) if n else F(0)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    pointpath=RUN/'discounted_augmented_lp/augmented_lp_exact.json'
    assert sha(pointpath)=='a4e48a91f0e2c7b65725178d042b515c6bedf11562afdeeea2ae69b815e8f505'
    point=load(pointpath);hist=[x for x in point['columns'] if x['kind']=='hist']
    K=F(point['columns'][0]['weight']);u=[sum(F(x['weight'])*q(int(x['actual_bits'][i]),sum(map(int,x['actual_bits']))) for x in hist) for i in range(6)]
    rem={}
    for b in (0,1):
        a=load(OLD/f'fixed53_b{b}_profit.json')
        for x in a['min_by_actual_and_d']:rem[b,x['actual'],x['d']]=F(x['min_rho'])
    witness=load(OUT/'ordered_root_exact_nonseparation.json')
    context=defaultdict(F);primitive=defaultdict(F);source_total=F(0)
    root_compare=F(0)
    for x in hist:
        w=F(x['weight']);d=x['d']
        for t in (0,1):
            p=F(d if t else 6-d,6)
            context[x['actual_bits'],d,t]+=w*p
            root_compare+=w*p*q(d-t,d)
    assert root_compare==F(5,6)
    contexts_seen=defaultdict(F)
    for row in witness['support']:
        a=tuple(map(int,row['actual']));d=row['d'];t=row['root_membership'];e=tuple(map(int,row['tail']))
        w=F(row['mass']);assert w>=0
        contexts_seen[row['actual'],d,t]+=w
        z=sum(e);ell=sum(a[:5]);v=[q(x,t+z) for x in e]
        source_total+=w*q(t,t+z)
        primitive[('gamma',)]+=w*(-2*q(z,t+z)+rem[t,row['tail'],d-t])
        for i in range(5):
            primitive['price',i]+=w*q(e[i],ell+1);primitive['capacity',i]+=w*e[i]
            den=t+sum(e[:i])+5-i
            for j in range(6):primitive['floor-actual',i,j]+=w*(q(a[j],den)-v[i])
            primitive['floor-other-opt',i]+=w*(q(d-t,den)-5*v[i])
            primitive['floor-root-topic',i]+=w*(q(t,den)-v[i])
            for j in range(5):
                if i!=j:primitive['floor-own-tail',i,j]+=w*(q(e[j],den)-v[i])
    for c,m in context.items():assert contexts_seen[c]==m,(c,contexts_seen[c],m)
    assert len(primitive)==71
    slacks={}
    for p,x in primitive.items():
        budget=(-KAP*K-root_compare if p[0]=='gamma' else u[5] if p[0]=='price' else K if p[0]=='capacity' else F(0))
        slacks[p]=budget-x;assert slacks[p]>=0,(p,slacks[p])
    saved={tuple(x['parameter']):F(x['slack']) for x in witness['column_slacks']}
    assert slacks==saved
    lower=u[0]-source_total
    assert lower==F(witness['strict_lower_bound_for_every_row_slack'])>0
    # Closed row from alpha=2/59,gamma=1/118,eta=0. All background costs
    # remain in the derivation, although z=0 is not active for t=1 here.
    alpha=F(2,59);gamma=F(1,118);cases=0
    for ell in range(6):
        for t in (0,1):
            values=[q(t,t+z)-2*gamma*q(z,t+z)-gamma*EPS*t*int(z==0)+alpha*q(z,ell+1) for z in range(6)]
            expected=gamma*min(F(0),-2+F(4,ell+1)) if t==0 else (F(9)+F(10,ell+1))/59
            assert min(values)==expected,(ell,t,min(values),expected)
            cases+=6
    def closed_coefficient(a,d):
        ell=sum(map(int,a[:5]))
        return 5*int(d>0)+2*d*(F(9)+F(10,ell+1))+(6-d)*min(F(0),-2+F(4,ell+1))
    row_rhs=sum(F(x['weight'])*closed_coefficient(x['actual_bits'],x['d']) for x in hist)
    closed_slack=708*u[0]+120*u[5]-row_rhs
    assert closed_slack>0
    # Recompute both earlier actual-path rows at this new point independently.
    R0=F(0);M0=F(0);E0point=F(0)
    for x in hist:
        w=F(x['weight']);a=x['actual_bits'];b=int(a[0]);e=a[1:];d=x['d']
        E0point+=w*b*int('1' not in e)
        for t in (0,1):
            p=F(d if t else 6-d,6)
            if p:
                R0+=w*p*q(d-t,b+d-t)
                M0+=w*p*rem[b,e,d-t]
    old_rows={'first_exclusive_mass':E0point,'average_five_profit':R0,
        'average_five_remainder':M0,'six_omission_debt':F(1)-R0,
        'charged_row_slack':2*sum(u[1:])-R0+EPS*E0point,
        'refined_row_slack':2*sum(u[1:])-R0-KAP*K-M0}
    discovery=load(OUT/'root_envelope_discovery.json')['diagnostic']
    for name,value in old_rows.items():assert value==F(discovery[name]),name
    # Per-customer joint-ledger algebra. Root tails may differ by root index.
    # Constancy within each t-class is enough here by linearity; no pointwise
    # IC sign is assumed. These identities include all impossible-endpoint
    # conventions, all background bits, all actual loads, and every d=0..6.
    joint_cases=0
    for b in (0,1):
      for c in range(6):
       for d in range(7):
        for z0 in range(6):
         for z1 in range(6):
            o=F(int(d>0));v0=q(c,b+c);r0=q(b,b+c);w0=v0+r0;ex0=b*int(c==0)
            p0=F(6-d,6);p1=F(d,6)
            Ract=p0*q(d,b+d)+(p1*q(d-1,b+d-1) if d else 0)
            Rroot=F(5,6)*o;delta=o-Ract
            vr=p0*q(z0,z0)+p1*q(z1,1+z1);rr=p1*q(1,1+z1);er=p1*int(z1==0)
            dw=vr+rr-w0;s=r0-rr
            cact=2*v0-Ract+EPS*ex0;croot=2*vr-Rroot+EPS*er
            assert vr-v0==dw+s
            assert croot-cact==2*(dw+s)+o/6-delta+EPS*(er-ex0)
            for lam in (F(0),F(1,3),F(1)):
                assert 2*w0-o==(1-lam)*cact+lam*croot+2*r0-(1-lam)*delta-lam*o/6-EPS*((1-lam)*ex0+lam*er)-2*lam*(dw+s)
            joint_cases+=1
    # Existing analytical q=5,a=1,b=2 complete-SPE family, made explicit.
    topics={f'{g}{i}':[] for g in ('X','Y') for i in range(5)};customers=[]
    for A,B in combinations(topics,2):
        for _ in range(1 if A[0]==B[0] else 2):
            cid=len(customers);customers.append((A,B));topics[A].append(cid);topics[B].append(cid)
    def root_path(T):
        other='Y' if T[0]=='X' else 'X'
        return [T]+[f'{other}{i}' for i in range(5)]
    def pay(path):
        load=[sum(x in topics[s] for s in path) for x in range(len(customers))]
        return [sum(q(int(x in topics[s]),load[x]) for x in range(len(customers))) for s in path]
    cycle=['X4','Y4'];cycle_data=[]
    for T in cycle:
        path=root_path(T);pays=pay(path)
        assert path[-1]==cycle[(cycle.index(T)+1)%2]
        exclusive=set(topics[T])-set(x for Q in path[1:] for x in topics[Q])
        cycle_data.append({'root':T,'path':path,'payoffs':[str(x) for x in pays],'exclusive_customers':len(exclusive)})
        assert pays==[F(9)]+[F(11)]*5 and len(exclusive)==4
    theta=sum(F(x['payoffs'][-1])-F(x['payoffs'][0]) for x in cycle_data)/2
    fee=EPS*4
    assert theta==2 and theta>fee and theta>F(9,20)
    # Same six optimal comparison labels: all X and Y4. Actual is X0,Y0..Y4.
    comparison=[f'X{i}' for i in range(5)]+['Y4'];actual=root_path('X0')
    union=set(x for s in comparison for x in topics[s]);actual_union=set(x for s in actual for x in topics[s])
    assert len(union)==len(actual_union)==64
    O=F(len(union));W=F(len(actual_union));u0=pay(actual)[0];V0=W-u0
    delta=F(0);R0avg=F(0);root_Ravg=F(0);Vavg=F(0);ravg=F(0);Eavg=F(0)
    for T in comparison:
        path=root_path(T);py=pay(path);ravg+=py[0]/6;Vavg+=sum(py[1:])/6
        Eavg+=F(len(set(topics[T])-set(x for Q in path[1:] for x in topics[Q])),6)
    E0=F(len(set(topics[actual[0]])-set(x for Q in actual[1:] for x in topics[Q])))
    for x in range(len(customers)):
        d=sum(x in topics[T] for T in comparison);b=int(x in topics[actual[0]])
        R0avg+=(F(6-d,6)*q(d,b+d)+F(d,6)*q(d-1,b+d-1)) if d else 0
        root_Ravg+=F(5,6)*int(d>0)
    delta=O-R0avg
    C0=2*V0-R0avg+EPS*E0;Cr=2*Vavg-root_Ravg+EPS*Eavg
    DW=(Vavg+ravg)-W;root_gap=u0-ravg
    assert Cr-C0==2*(DW+root_gap)+O/6-delta+EPS*(Eavg-E0)
    result={'status':'INDEPENDENT STANDARD-LIBRARY ROOT BRIDGE AUDIT PASSED',
        'point_sha256':sha(pointpath),'marginal_support_atoms':len(witness['support']),'exact_common_budgets_verified':71,
        'strict_nonseparation_lower_bound':str(lower),'strict_nonseparation_lower_bound_float':float(lower),
        'closed_row_hidden_types_checked':cases,'closed_row_new_point_slack':str(closed_slack),
        'old_two_rows_new_point':{name:str(value) for name,value in old_rows.items()},
        'joint_ledger_customer_types_checked':joint_cases,
        'theta_counterexample':{'source':'degree-two-shared-customers-complete-spe-negative-stationary-flux-family; q5/a1/b2',
           'customers':70,'topics':topics,'cycle':cycle_data,'theta':str(theta),'root_ic_gap':'0',
           'average_exclusive_fee':str(fee),'first_payoff_twentieth':'9/20','W':64,'OPT6':64,
           'six_comparison':comparison,'actual_path':actual,'actual_five_profit':str(V0),
           'root_average_tail_profit':str(Vavg),'actual_six_drop_profit':str(R0avg),
           'root_six_drop_profit':str(root_Ravg),'actual_omission_debt':str(delta),
           'actual_charged_slack':str(C0),'root_average_charged_slack':str(Cr),
           'coverage_change':str(DW),'root_ic_average_gap':str(root_gap),'joint_ledger_verified':True},
        'source_sha256':{str(p.relative_to(RUN)):sha(p) for p in (OLD/'fixed53_b0_profit.json',OLD/'fixed53_b1_profit.json',OUT/'ordered_root_exact_nonseparation.json')}}
    (OUT/'root_bridge_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('theta_counterexample','source_sha256')},indent=2))
    print(json.dumps({k:v for k,v in result['theta_counterexample'].items() if k not in ('topics','cycle')},indent=2))
if __name__=='__main__':main()
