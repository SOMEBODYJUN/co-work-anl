"""New bounded exact checks of DS formulas; no original program entry is executed."""
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import json

prior=json.loads((Path(__file__).parent/'prior-check-input/dn-definition-report.json').read_text())
c=prior['certificate_checks'][1]
policy={tuple(r['h']):r['chosen'] for r in c['all_node_tables']}
groups=[({0},1),({2},2),({1,2},2),({0,1,3},2)]
def follow(h):
    h=list(h)
    while len(h)<3:h.append(policy[tuple(h)])
    return tuple(h)
def utility(z,i):
    return sum((F(n,sum(a in M for a in z)) for M,n in groups if z[i] in M),F())
def coverage(z):return sum(n for M,n in groups if any(a in M for a in z))
z=follow(());u=[utility(z,i) for i in range(3)];W=sum(u,F());assert z==(0,1,2) and W==7
V=sum((F(n,sum(a in M for a in z)+1) for M,n in groups if any(a in M for a in z)),F())
debt_rows=[];signs=set()
for T in product(range(4),repeat=3):
    O=coverage(T);sum_f=sum_delta=sum_debt=sum_IC=F()
    players=[]
    for i,a in enumerate(T):
        f=sum((F(n,sum(b in M for b in z)+1) for M,n in groups if a in M),F())
        delta=sum((F(n,sum(b in M for b in z)*(sum(b in M for b in z)+1))
                   for M,n in groups if a in M and z[i] in M),F())
        frozen=z[:i]+(a,)+z[i+1:]
        q=utility(frozen,i);assert q==f+delta
        d=utility(follow(z[:i]+(a,)),i)
        R=q-d;slack=u[i]-d;assert slack>=0
        signs.add((R>0)-(R<0))
        sum_f+=f;sum_delta+=delta;sum_debt+=R;sum_IC+=slack
        players.append({'i':i,'T_i':a,'f':str(f),'delta':str(delta),'frozen':str(q),'true':str(d),'signed_R':str(R),'IC_slack':str(slack)})
    cov_slack=W-V+sum_f-O;assert cov_slack>=0
    rhs=V+sum_delta-sum_debt+cov_slack+sum_IC
    assert rhs==2*W-O
    assert O<=2*W-V-sum_delta+sum_debt
    debt_rows.append({'T':T,'O':O,'is_optimal':O==7,'players':players,
        'V':str(V),'sum_delta':str(sum_delta),'sum_R':str(sum_debt),
        'coverage_slack':str(cov_slack),'sum_IC_slack':str(sum_IC),'2W_minus_O':str(rhs)})
assert signs=={-1,0}
# A separate known two-player full-policy example supplies a positiveR witness.
# Themes A=ab,B=abc,C=cd; root A; last replies C,B,B after A,B,C.
other_themes=[set('ab'),set('abc'),set('cd')]
other_reply=[2,1,1]
def root_value(a,b):
    return sum((F(1,1+int(x in other_themes[b])) for x in other_themes[a]),F())
assert [root_value(a,other_reply[a]) for a in range(3)]==[2,F(3,2),F(3,2)]
assert all(root_value(other_reply[a],a)==max(root_value(b,a) for b in range(3)) for a in range(3))
signed_witness={str(a):{'frozen':str(root_value(a,2)), 'true':str(root_value(a,other_reply[a])),
                         'R':str(root_value(a,2)-root_value(a,other_reply[a]))} for a in range(3)}
assert signed_witness['1']['R']=='1' and signed_witness['2']['R']=='-1/2'

prefix_rows=[]
for m in range(2,101):
    D=F(1);pay=[]
    for i in range(m):
        r=m-i;v=D/(m*r);pay.append(v);D-=v
    P=F()
    for i,v in enumerate(pay):
        assert P+m*(m-i)*v==1;P+=v
    prod=F(1)
    for r in range(1,m+1):prod*=1-F(1,m*r)
    assert P==1-prod
    if m>=4:assert P<F(1,2)
    prefix_rows.append({'m':m,'value':str(P),'tight_vector':list(map(str,pay))})
assert prefix_rows[2]['value']=='893/2048'

n=[[0,0,0,1],[0,0,1,0],[0,0,0,1],[2,2,1,0]]
pi=list(map(F,[F(2,9),F(1,9),F(2,9),F(4,9)]));J={1,2}
assert all(sum(n[j][i] for j in range(4))==2 and n[i][i]==0 for i in range(4))
assert [sum((F(n[j][i],2)*pi[i] for i in range(4)),F()) for j in range(4)]==pi
K=[sum(n[j][i] for j in J) for i in range(4)]
delta=[F(2-K[i],2*(1+K[i])) if i in J else -F(1,2) if K[i]>0 else F() for i in range(4)]
assert K==[0,0,1,1] and delta==[0,1,F(1,4),-F(1,2)]
weighted=sum((pi[i]*delta[i] for i in range(4)),F());assert weighted==-F(1,18)

incidence_rows=[]
for s in range(2,8):
    edges=list(combinations(range(s),2));O=len(edges)
    for r in range(1,7):
        beta=[F(r,2)]*s;B=F(s*r,2)
        past=[[0]*s,[1]*s]+[[int(j==a) for j in range(s)] for a in range(s)]
        for p in past:
            f=[sum((F(1,sum(p[a] for a in I)+r) for I in edges if j in I),F()) for j in range(s)]
            raw=sum(((p[j]+beta[j])*f[j] for j in range(s)),F())
            assert raw==O and O<=(sum(p)+B)*max(f)
        incidence_rows.append({'s':s,'r':r,'all_pair_B':str(B),'past_vectors':len(past)})

# Exact fixed-prefix minimum-SPE value example, no original solver imported.
A,B=set(range(3)),set(range(3,5))
single_policy=[]
for root,a,b in product(range(2),repeat=3):
    themes=[A,B];last=[a,b]
    def uu(x,y):return sum((F(1,1+int(c in themes[y])) for c in themes[x]),F())
    if any(uu(last[h],h)<max(uu(k,h) for k in range(2)) for h in range(2)):continue
    values=[uu(h,last[h]) for h in range(2)]
    if values[root]!=max(values):continue
    single_policy.append(values[root])
assert single_policy and min(single_policy)==3
fixed=max(F(len(A),2),F(len(B)))
assert fixed==2

report={'status':'PASS','original_program_entries':0,'prior_policy_reuse':'DN four-topic authorpolicy report; no rerun of old full-node certification',
    'debt_checks':debt_rows,'reused_policy_R_signs':sorted(signs),'separate_two_player_signed_R_witness':signed_witness,
    'prefix_LP_checks':prefix_rows,'prefix_LP_domain':'abstract nonnegative vectors, not asserted SPE realizable',
    'stationary_flow':{'labels':'zero based 0,1,2,3','n':n,'pi':list(map(str,pi)),'J':sorted(J),'K':K,'delta':list(map(str,delta)),'weighted':str(weighted),'is_SPE_certificate':False},
    'incidence_A_checks':incidence_rows,'all_pair_LP_optimality':'analytic summed pair constraints lower bound sr/2; uniform beta=r/2 attains',
    'fixed_prefix_minimum_SPE':{'themes_disjoint_sizes':[3,2],'M2_root':'3','M1_after_A':str(fixed),'SPE_count':len(single_policy)},
    'not_executed':['23875 historical scan','2000 historical floating security probes','original scripts','bank controller original audit','LP/MILP solver'],
    'universal_proofs':'written derivations; bounded checks do not establish general half'}
Path('report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','debt_tuples':len(debt_rows),'prefix_vectors':len(prefix_rows),'incidence_cases':len(incidence_rows),'stationary_weighted':str(weighted)}))
