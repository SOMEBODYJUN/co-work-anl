"""New unit-customer, Fraction checks; no original audit program is executed."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,hashlib

def expand(groups):
    return [set(M) for M,n in groups for _ in range(n)]
def utility(clients,z,i):
    return sum((F(1,sum(a in M for a in z)) for M in clients if z[i] in M),F())
def cover(clients,z):return sum(any(a in M for a in z) for M in clients)
def rental(clients,s,z):
    return sum((F(1,1+sum(a in M for a in z)) for M in clients if s in M),F())
def finish(policy,h,m):
    h=list(h)
    while len(h)<m:h.append(policy[tuple(h)])
    return tuple(h)
def certify(clients,policy,p,m):
    rows=[];nontrivial=0
    for depth in range(m):
        for h in product(range(p),repeat=depth):
            assert h in policy
            prescribed=finish(policy,h,m)
            vals=[utility(clients,finish(policy,h+(a,),m),depth) for a in range(p)]
            assert vals[policy[h]]==max(vals),(h,vals,policy[h])
            nontrivial+=p-1
            rows.append({'history':h,'choice':policy[h],'action_values':list(map(str,vals))})
    return {'nodes':len(rows),'queries_including_stay':p*len(rows),'genuine_alternatives':nontrivial,'all_node_tables':rows}

seven=expand([({0},1),({0,1},1),({1,2},3),({0,1,2},2)])
seven_policy={():2,**{(a,):[1,1,2][a] for a in range(3)},
              **{(a,b):(0 if a==b==2 else 1) for a,b in product(range(3),repeat=2)}}
cycle=certify(seven,seven_policy,3,3)
seven_z=finish(seven_policy,(),3)
tails=[finish(seven_policy,(s,),3)[1:] for s in range(3)]
matrix=[[rental(seven,q,tails[s]) for s in range(3)] for q in range(3)]
assert seven_z==(2,2,0) and cover(seven,seven_z)==7
assert matrix==[[2,2,F(5,3)],[2,2,F(8,3)],[F(5,3),F(5,3),F(13,6)]]
diag=matrix[1][1]+matrix[2][2];cross=matrix[1][2]+matrix[2][1]
assert diag==F(25,6) and cross==F(26,6) and (diag-cross)/4==-F(1,24)
assert max(matrix[q][1] for q in range(3))==2<F(13,6)
cycle.update({'actual_path':seven_z,'actual_payoffs':list(map(str,[utility(seven,seven_z,i) for i in range(3)])),
    'welfare':7,'opt':max(cover(seven,z) for z in product(range(3),repeat=3)),
    'tail_columns':tails,'rental_matrix':[[str(v) for v in row] for row in matrix],
    'diagonal_sum':str(diag),'cross_sum':str(cross),'half_half_decorrelation_gap':str((diag-cross)/4),'pure_BB_cap':'2'})

source=Path(__file__).parent/'comparison-original/f218c3c894b4635ecca2.json'
raw=json.loads(source.read_text());instance=raw['instance'];m=instance['players'];p=len(instance['topics'])
clients=expand([(set(r['topics']),r['multiplicity']) for r in instance['customers']]);assert len(clients)==34 and m==3 and p==7
policy={tuple(r['history']):r['action'] for r in raw['certificate']['actions']};assert len(policy)==57
audit=certify(clients,policy,p,m);assert audit['nodes']==57 and audit['genuine_alternatives']==342
z=finish(policy,(),m);u=[utility(clients,z,i) for i in range(m)]
assert z==(0,3,4) and u==[F(29,3),F(67,6),F(67,6)] and sum(u)==32
assert [z.count(a) for a in range(p)]==raw['certificate']['terminal_counts']
root_paths=[finish(policy,(a,),m) for a in range(p)]
assert [list(z) for z in root_paths]==raw['forced_root_paths']
assert [str(utility(clients,z,0)) for z in root_paths]==raw['forced_root_payoffs']
assert raw['verification']=={'valid':True,'histories':57,'deviations':342}
endpoints=[]
for i in range(m):
    for t in range(p):
        zz=finish(policy,z[:i]+(t,),m)
        endpoints.append({'i_zero_based':i,'forced_topic':t,'terminal':zz,
            'current_payoff':str(utility(clients,zz,i)),
            'query_values':list(map(str,[rental(clients,s,zz) for s in range(p)]))})
actual_column=[rental(clients,s,z) for s in range(p)]
assert actual_column==[F(27,4),8,F(33,4),F(29,4),F(29,4),F(17,2),0]
assert max(actual_column)==F(17,2)<F(32,3)
empty_root=root_paths[6]
dominance=[(sum(a in M for a in z),sum(a in M for a in empty_root)) for M in clients]
assert all(a>=b for a,b in dominance)
F_X2=min(F(row['query_values'][2]) for row in endpoints)
assert F_X2==F(13,2)
q=[F(int(s==2)) for s in range(p)]
def free_value(probs):
    return min(sum((probs[s]*F(row['query_values'][s]) for s in range(p)),F()) for row in endpoints)
homogeneity=[]
queries=[[F(int(s==a)) for s in range(p)] for a in range(p)]
queries.append([F(1,6) if s<6 else F() for s in range(p)])
for n,query in enumerate(queries):
    for eps in [F(),F(1,24),F(1,10),F(1)]:
        probs=[eps*v+(1-eps)*F(int(s==6)) for s,v in enumerate(query)]
        v=free_value(probs);assert v==eps*free_value(query)
        homogeneity.append({'query_case':n,'epsilon':str(eps),'free_value':str(v)})
by={(row['i_zero_based'],row['forced_topic']):row for row in endpoints}
Dq=sum((F(by[i,2]['current_payoff']) for i in range(m)),F())
HE=sum((F(by[i,6]['query_values'][2]) for i in range(m)),F())
Gq=sum((F(by[i,2]['query_values'][2]) for i in range(m)),F())
assert (Dq,HE,Gq)==(F(63,2),F(65,2),F(41,2))
eps=F(1,24);D=eps*Dq;G=eps*eps*Gq+eps*(1-eps)*HE
assert D-G==12*eps*eps-eps==-F(1,48) and free_value([eps*x+(1-eps)*F(int(s==6)) for s,x in enumerate(q)])==F(13,48)
# The input JSON records root-local D/C at epsilon=1/10, not the aggregate above.
probs=list(map(F,raw['query_probability']));rootD=sum((probs[a]*utility(clients,root_paths[a],0) for a in range(p)),F())
rootC=sum((probs[s]*probs[a]*rental(clients,s,root_paths[a]) for s,a in product(range(p),repeat=2)),F())
assert str(rootD)==raw['D'] and str(rootC)==raw['C'] and str(rootD-rootC)==raw['D_minus_C'] and str(u[0]-rootC)==raw['u_minus_C']
assert str(rental(clients,2,empty_root))==raw['entry_X2_after_empty'] and str(rental(clients,2,root_paths[2]))==raw['entry_X2_after_X2']
audit.update({'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'literal_unit_clients':34,
    'topics':instance['topics'],'actual_path':z,'actual_payoffs':list(map(str,u)),'welfare':32,
    'opt':max(cover(clients,zz) for zz in product(range(p),repeat=m)),
    'all_21_endpoints':endpoints,'actual_complete_column_values':list(map(str,actual_column)),
    'actual_column_cap':'17/2','budget_W_over_m':'32/3','empty_root_path':empty_root,
    'per_unit_client_actual_vs_empty_root_loads':dominance,'F_dirac_X2':'13/2','F_epsilon_1_over24':'13/48',
    'homogeneity_checks':homogeneity,
    'aggregate_three_positions':{'D_q':str(Dq),'H_empty_q':str(HE),'G_q':str(Gq),'epsilon':'1/24','D_epsilon':str(D),'G_epsilon':str(G),'difference':str(D-G),'formula':'12epsilon^2-epsilon'},
    'input_JSON_root_local':{'epsilon':'1/10','D':str(rootD),'C':str(rootC),'difference':str(rootD-rootC),'u_minus_C':str(u[0]-rootC)},
    'JSON_metadata':'kind/source_instance kept descriptive only; all numeric arrays/probabilities/certificate/verification fields independently checked'})
report={'status':'PASS','role':'new literal unit-customer checker; no original audit entry run',
    'seven_client_cycle':cycle,'34_client_empty_extension':audit,
    'original_program_entries':0,'homogeneity_scope':'finite32checks validate code; arbitraryq/epsilon theorem isanalytic',
    'not_proved':['generalFM','generalhalf','menu failure for seven-clientexample','minimality','externalreview/newness']}
Path('report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','nodes':[13,57],'queries_including_stay':[39,399],
    'genuine_alternatives':[26,342],'complete_i_t_endpoints':21,'homogeneity_cases':len(homogeneity),
    'root_local_gap':str(rootD-rootC),'aggregate_gap':str(D-G)}))
