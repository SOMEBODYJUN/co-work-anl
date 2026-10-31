"""New exact checks of EI displayed math; no original audit entry is executed."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

types=[(2,7),(16,1),(20,6),(26,4),(29,1),(31,1),(33,5),
       (35,5),(39,6),(45,5),(47,7),(55,1),(58,4),(62,1)]
clients=[{a for a in range(6) if mask>>a&1} for mask,n in types for _ in range(n)]
assert len(clients)==54
def utility(z,i):
    return sum((F(1,sum(a in M for a in z)) for M in clients if z[i] in M),F())
reply=[1,5,5,5,5,2];last_rows=[]
for a in range(6):
    vals=[utility((1,a,b),2) for b in range(6)]
    assert [b for b in range(6) if vals[b]==max(vals)]==[reply[a]]
    last_rows.append({'first_tail':a,'reply':reply[a],'values':list(map(str,vals))})
first_values=[utility((1,a,reply[a]),1) for a in range(6)]
assert first_values==[F(53,3),14,15,10,F(25,2),17]
assert [a for a in range(6) if first_values[a]==max(first_values)]==[0]
assert [utility((1,0,1),i) for i in range(3)]==[F(44,3),F(53,3),F(44,3)]
pne=[];configs=[]
for a,b in product(range(6),repeat=2):
    z=(1,a,b);u=[utility(z,i) for i in range(3)];witnesses=[];all_deviations=[]
    for i in [1,2]:
        for t in range(6):
            zz=z[:i]+(t,)+z[i+1:];gain=utility(zz,i)-u[i]
            all_deviations.append({'tail_position':i,'topic':t,'gain':str(gain)})
            if gain>0:witnesses.append(all_deviations[-1])
    if not witnesses:pne.append({'tail':(a,b),'observer':str(u[0])})
    configs.append({'tail':(a,b),'payoffs':list(map(str,u)),
        'all_12_deviation_gains_including_stay':all_deviations,
        'is_tail_PNE':not witnesses,'one_profitable_move':witnesses[0] if witnesses else None})
assert pne==[{'tail':(2,5),'observer':'21'},{'tail':(5,2),'observer':'21'}]
assert F(21)-F(44,3)==F(19,3)

ring=[]
for k in [9,10,11,12]:
    topics=[{(i-1)%k,i,(i+1)%k} for i in range(k)]
    def share(z,i):return sum((F(1,sum(x in topics[a] for a in z)) for x in topics[z[i]]),F())
    optimum=max(len(set().union(*(topics[a] for a in z))) for z in product(range(k),repeat=3))
    assert optimum==9 and len(topics[1]|topics[4]|topics[7])==9
    roots=[]
    for i in range(k):
        leaf=(i,(i-1)%k,(i+1)%k)
        pay=[share(leaf,j) for j in range(3)];assert pay==[F(4,3),F(11,6),F(11,6)]
        last_values=[share((i,(i-1)%k,a),2) for a in range(k)]
        assert last_values[(i+3)%k]==max(last_values)==3
        assert not(topics[(i+3)%k] & (topics[i]|topics[(i-1)%k]))
        roots.append({'root':i,'abstract_leaf':leaf,'shares':list(map(str,pay)),
            'last_best_value':'3','explicit_deviation':(i+3)%k,'last_all_action_values':list(map(str,last_values)),
            'last_improvement':'7/6'})
    ring.append({'k':k,'OPT3':optimum,'threshold':'3/2','all_roots':roots,
                 'is_SPE_certificate':False})

deletion=[]
for b in [0,1,2,1000]:
    for s in range(1,13):
        for c in range(s+1):
            original=F(1,b+1+c)
            expected=(F(c,s)*F(1,b+c)+F(s-c,s)*original) if c else original
            assert s*expected<=(s+1)*original
            if b==0:assert s*expected==(s+1)*original-int(c==0)
            deletion.append({'b':b,'labelled_competitor_slots':s,'covering_slots':c,
                'original':str(original),'after_uniform_deletion_expected':str(expected),
                'scaled_inequality_slack':str((s+1)*original-s*expected)})

bank=[]
for m in range(2,13):
    u=F(m,m-1);W=2*m;OPT=3*m-2;floor=F(OPT,2*m)
    extra=F(3,2)-F(1,2*m-1)
    assert (floor>u)==(m>=5) and (extra>u)==(m>=4)
    bank.append({'m':m,'root':str(u),'W':W,'OPT':OPT,'direct_threshold':str(floor),
        'threshold_minus_root':str(floor-u),'extra_fractional_value':str(extra),
        'extra_minus_root':str(extra-u),'integer_v_m_upper_bound':'2',
        'W_minus_m_times_v_upper_bound':0,'half_slack':2*W-OPT,
        'provenance':'numeric substitution in alreadyproved bank theorem; no bankcontroller re-audit'})
assert bank[3]['threshold_minus_root']=='1/20'
report={'status':'PASS','original_program_entries':0,
    '54_client_fixed_background_tail':{'literal_unit_clients':54,'fixed_old_topic':1,
        'tail_nodes':7,'tail_action_values_including_stay':42,'tail_genuine_alternatives':35,
        'last_rows':last_rows,'first_tail_values':list(map(str,first_values)),
        'actual_full_tuple':[1,0,1],'payoffs':['44/3','53/3','44/3'],
        'all_static_tail_configs':configs,'tail_PNE':pne,'observer_difference':'19/3',
        'original_root_IC_verified':False,'old_player_is_frozen_in_static_tail_game':True},
    'three_window_abstract_menus':ring,'random_slot_deletion_scalar_checks':deletion,
    'bank_theorem_numeric_substitutions':bank,
    'not_executed':['originalauthorobserveraudit','originalblindtailaudit','originalringaudit','LPprobes','bankcontrolleroriginalaudit'],
    'universal_quantifiers':'written finitepolicycertificate, generalringargument andstaticdeletionproof; finite samples do not prove generalhalf'}
Path('report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','tail_nodes':7,'tail_queries_including_stay':42,
    'static_tail_configs':36,'tail_PNE_count':len(pne),'ring_roots':sum(len(r['all_roots']) for r in ring),
    'deletion_scalar_cases':len(deletion),'bank_substitutions':len(bank)}))
