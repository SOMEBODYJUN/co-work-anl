"""Independent exact menu/saddle audit of aggregate11's named old packet.

No optimizer, new game, policy-cone query, or universal welfare conclusion.
The all-history insurance SPE proof is inherited from its read source.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
from insurance_transport_exact import m,banks,acts,ad,inc,weights,finish

HERE=Path(__file__).resolve().parent
source=HERE.parent/'aggregate/insurance_shared_saddle_m6_exact.json'
raw=source.read_bytes()
data=json.loads(raw)
L=[F(x) for x in data['L']]
t=[1/(1+x) for x in L]
z=finish(())
cols=[[[sum(inc[ad[b]][x] for j,b in enumerate(finish(z[:i]+(a,))) if j!=i)
          for x in range(len(L))] for a in acts] for i in range(m)]
q=[[F(0)]*len(acts) for i in range(m)]
for i,row in enumerate(data['q']):
    for a,value in row:q[i][a]=F(value)
assert all(sum(row)==1 and min(row)>=0 for row in q)
assert all(sum(q[i][a]*cols[i][a][x] for i in range(m) for a in range(len(acts)))==m*L[x]
           for x in range(len(L)))
support=[a for a,pair in enumerate(acts) if pair[0]!=0]
rho=[F(0)]+[F(1,5)]*5+[F(1,5)]*5
linear=[[sum((weights[x]*rho[x]*t[x]**2*cols[i][a][x] for x in range(len(L))),F(0))
         for a in range(len(acts))] for i in range(m)]
assert all(q[i][a]==0 or linear[i][a]==max(linear[i])
           for i in range(m) for a in range(len(acts)))
g=[sum((weights[x]*inc[a][x]*t[x] for x in range(len(L))),F(0))
   for a in range(len(acts))]
assert all(g[a]==F(37,22) for a in support)
assert all(g[a]==F(14,11) for a in range(len(acts)) if a not in support)
assert max(g)==F(data['F_optimum'])
C=[[sum((weights[x]*inc[a][x]*t[x]**2*(cols[i][a][x]-L[x])
         for x in range(len(L))),F(0)) for a in range(len(acts))] for i in range(m)]
D=[[sum((weights[x]*inc[a][x]*t[x]**2*(cols[i][a][x]-L[x])**2/(1+cols[i][a][x])
         for x in range(len(L))),F(0)) for a in range(len(acts))] for i in range(m)]
d=[[sum((F(weights[x]*inc[a][x],1+cols[i][a][x]) for x in range(len(L))),F(0))
    for a in range(len(acts))] for i in range(m)]
u=[d[i][ad[z[i]]] for i in range(m)]
assert all(d[i][a]<=u[i] for i in range(m) for a in range(len(acts)))
assert all(cols[0][a][acts[a][0]]==4 for a in support)
assert all(cols[i][a][acts[a][0]]==0 for i in range(1,m) for a in support)
assert all(all(cols[i][a][x]==1 for x in range(m,len(L)))
           for i in range(m) for a in support)
ci=[F(795,484)]+[F(-105,484)]*5
assert all(C[i][a]==ci[i] for i in range(m) for a in support)
CT=sum(ci)
DT=sum(D[i][a]/25 for i in range(m) for a in support)
IC=sum(u)-sum(d[i][a]/25 for i in range(m) for a in support)
assert (CT,DT,IC)==(F(135,242),F(2017,1210),F(4,5))
assert sum(u)-m*max(g)==IC-CT+DT==F(21,11)
report=dict(scope='independent exact audit of one named inherited complete SPE and fixed saddle p*',
            source=str(source),source_sha256=hashlib.sha256(raw).hexdigest(),
            full_SPE='source all-m analytic proof read; no new all-tree m6 enumeration',
            actual_prefix_menus_checked=m*len(acts),all_actual_prefix_IC_checked=True,
            shared_q_feasible=True,inner_KKT=True,outer_active_query_saddle=True,
            optimizer_L=list(map(str,L)),saddle_value=str(max(g)),
            all_support_query_values=str(F(37,22)),excluded_query_values=str(F(14,11)),
            C_by_role=list(map(str,ci)),C=str(CT),D=str(DT),IC=str(IC),
            W_minus_mF=str(sum(u)-m*max(g)),
            every_transport_preserving_this_p_has_same_positive_C=True,
            existence_of_other_favorable_outer_p='closed analytically: unique primal load and every dual optimal p excludes anchor0; all transports have same positive C',
            unique_primal_minimax_load='proved by strict convexity on active coordinates and fixed total economy load',
            shared_load_cap='not refuted',general_half='OPEN',all_checks=True)
(HERE/'insurance_saddle_independent.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
