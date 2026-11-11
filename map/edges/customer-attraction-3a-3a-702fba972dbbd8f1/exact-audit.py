"""Definition-level finite checks for Boss5/702. No author import, LP, MILP or SPE solver."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,re,hashlib
D=Path(__file__).parent
ROOT=D.parents[2]

def full_policy(m,p,levels):
    out={}
    for depth,s in enumerate(levels):
        assert len(s)==p**depth
        out.update({h:int(a) for h,a in zip(product(range(p),repeat=depth),s)})
    return out

def finish(policy,h,m):
    while len(h)<m:h=h+(policy[h],)
    return h

def payoff(leaf,a,weights):
    return sum(F(w,sum(bool(mask>>b&1) for b in leaf)) for mask,w in weights.items() if mask>>a&1)

# Rebuild every coefficient of the existing 29x32 m2/p5 certificate.
p=ROOT/'archives/customer-attraction/tools/evidence/terminal-envelope-cone-program/exact/exact-small-cone.json'
c=json.loads(p.read_text());policy={tuple(a['history']):a['action'] for a in c['policy']['actions']}
rows=[]
for h in [()]+[(a,) for a in range(5)]:
    a=policy[h];z=finish(policy,h,2)
    for b in range(5):
        if a==b:continue
        zp=finish(policy,h+(b,),2)
        rows.append([payoff(zp,b,{mask:1})-payoff(z,a,{mask:1}) for mask in range(1,32)]+[F(0)])
for h in [(a,) for a in range(5)]:
    a=policy[h];row=[]
    for mask in range(1,32):
        W=bool(mask&6);load=bool(mask>>h[0]&1)
        E=F(2*bool(mask>>a&1)+load,1+load)
        row.append(2*F(W)-E)
    rows.append(row+[F(1)])
assert rows==[[F(x) for x in row] for row in c['matrix']]
x=[F(a) for a in c['primal']];lam=[F(a) for a in c['inequality_dual']];nu=F(c['normalization_dual'])
objective=[F(a) for a in c['objective']];normal=[F(a) for a in c['normalization']]
assert sum(a*b for a,b in zip(normal,x))==1
assert all(sum(a*b for a,b in zip(row,x))<=0 for row in rows)
reduced=[objective[j]-sum(lam[i]*rows[i][j] for i in range(29))-nu*normal[j] for j in range(32)]
assert reduced==[F(v) for v in c['dual_reduced_costs']]
assert all(z>=0 for z in reduced[:-1]) and reduced[-1]==0
assert sum(a*b for a,b in zip(objective,x))==nu==F(1,2)
assert all(l<=0 for l in lam)
# Directly check each customer-type identity, no floating certificate reliance.
assert [F(v) for v in c['pointwise_envelope_identity_residuals']]==[F(bool(mask&2 and not mask&4),2) for mask in range(1,32)]

# PB scalar comparisons use the published rational formulas; never execute the top-level author script.
r,Q,H,M,d=2475,2063,100000,10**9,20
f=lambda z:F(11)/(M+z)+F(1)/(M+z+1)
g=lambda z:F(1200000)/(H*M+z)
u=3*d*f(3);U=d*(9*f(3)+1648*f(1)+824*f(2)+4944*g(2472))
PB=[]
for mass in [r-1,r]:
    L=F(3*mass,Q);delta=d*(f(1+L)+2*g(1));hr=(F(11)/(M+1+L)**2+F(1)/(M+2+L)**2)/Q;hd=F(1200000)/(H*M+1)**2
    assert 3<L<4 and hr>hd and f(1+L)<g(1)
    assert delta>F(1,M+1) and 3*d*hr>max(F(1,Q)/(M+1+L)**2,F(1)/(H*M+1)**2)
    assert delta>u and U>r*delta
    levels=[]
    for j in range(4 if mass==r-1 else 2):
        future=mass-j;theta=3*(L-j)/future
        assert 0<=theta<=1 and j+future*theta/3==L and future*(3-theta)/(Q-3)==L
        levels.append({'j':j,'theta':str(theta)})
    PB.append(dict(mass=mass,L=str(L),delta_minus_u=str(delta-u),aggregate_balance=str(U-r*delta),levels=levels))
extra=json.loads((ROOT/'archives/customer-attraction/tools/evidence/round11-extra-fractional-plateau-primary/original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round11/aggregate/extra_fractional_plateau_check.json').read_text())
assert str(-F(PB[1]['delta_minus_u']))==extra['local_balance'] and PB[1]['aggregate_balance']==extra['aggregate_balance']

# Decode all nine complete action tables in the formal evidence page.
text=(ROOT/'archives/customer-attraction/state/计算/五份份额扫描与四个联合树保存点--计算.md').read_text()
parts=re.split(r'\n## ([^\n]+) / record (\d+)\n',text)[1:]
specs=[(3,5,{1:1,6:1,9:1,14:1,18:1,21:1,26:1,29:1}),
(3,7,{1:3400,6:1700,10:4939,13:4939,17:7625,18:7965,25:3579,30:3579,33:2240,34:3940,53:340,66:1360,73:4599,90:4599,101:8295,102:6935,110:4599,121:1360,125:3239}),
(4,6,{2:1025,5:6555,6:2187,9:555,10:3471,17:130,33:130,34:1280,38:240,41:890,49:3550,53:369,57:4783,62:3105}),
(5,7,{1:2,2:1}),(3,6,{1:1,2:1,5:1,6:1,57:1,58:1,61:1,62:1}),
(3,5,{6:1,25:1}),(3,5,{2:1,29:3}),(3,5,{1:1,30:3}),(3,5,{1:3,2:4,12:6,20:6,25:2,26:2})]
old=json.loads((ROOT/'archives/customer-attraction/tools/evidence/last-joint-share-primary/fixed-points-audit.json').read_text())
points=[];total=0
for k,(m,p,w) in enumerate(specs):
    name,rec,body=parts[3*k:3*k+3]
    levels=[v for depth,v in re.findall(r'\|([0-4])\|`([0-6]+)`\|',body)]
    if m==5:
        final=re.findall(r'\|`([0-6]{2})`\|`([0-6]{49})`\|',body)
        assert len(final)==49
        levels.append(''.join(v for _,v in final))
    pol=full_policy(m,p,levels);tests=0
    def check(weights):
        nonlocal_dummy=0
        for h,a in pol.items():
            z=finish(pol,h,m);v=payoff(z,a,weights)
            for b in range(p):
                if b==a:continue
                assert v>=payoff(finish(pol,h+(b,),m),b,weights),(name,h,a,b)
                nonlocal_dummy+=1
        return nonlocal_dummy
    tests+=check(w)
    actual=finish(pol,(),m);uvec=[payoff(actual,a,w) for a in actual];W=sum(w.values())
    assert list(map(str,uvec))==old['saved_points'][k]['payoffs']
    assert sum(uvec)==W==old['saved_points'][k]['welfare']
    if k<5:
        forced=finish(pol,(1,),m)
        assert actual==(0,)*(m-1)+(1,) and forced.count(0)==m-2 and forced.count(1)==2
        beta,mu,overlap=F(2,m+1),F(2*(m-1),m+1),F(m-1,m*(m+1))
        for mask in range(1,1<<p):
            aa,bb=bool(mask&1),bool(mask&2)
            ua=F(1,m-1) if aa and not bb else F(1,m) if aa else F(0)
            dev=F(1,2) if bb and not aa else F(1,m) if bb else F(0)
            ub=F(1) if bb and not aa else F(1,m) if bb else F(0)
            assert beta*F(aa or bb)-ub==mu*(ua-dev)+overlap*int(aa and bb)
        assert max(uvec)/W==uvec[-1]/W==beta
        tests+=check({1:m-1,2:2})
    points.append(dict(name=name+':'+rec,histories=len(pol),current_nonself_checks=tests,actual=list(actual),payoffs=list(map(str,uvec))))
    total+=tests
assert total==38060
out=dict(scope='Finite definition-level comparison check only. No universal result inferred from finite checks.',matrix_rows=29,matrix_columns=32,matrix_coefficients_checked=928,exact_fixed_cone_max_epsilon='-1/2',PB=PB,saved_point_checks=points,share_nonself_comparisons=total,author_imports=0,LP_runs=0,MILP_runs=0,SPE_solver_runs=0,passed=True)
(D/'exact-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':True,'matrix': [29,32],'PB_modes':len(PB),'saved_points':len(points),'share_nonself_comparisons':total}))
