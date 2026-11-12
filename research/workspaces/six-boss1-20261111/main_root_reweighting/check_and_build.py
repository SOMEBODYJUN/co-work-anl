"""Main: exact full-type reweighting of true root-history budgets.

No optimization call and no candidate point is used.  Reconstruct all C30
and P25 hidden costs, follow explicit algebraic directions, check every
root coordinate, then substitute the strongest checked row into gamma36.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from hashlib import sha256
from decimal import Decimal, getcontext
import json

H = Path(__file__).resolve().parent
W = H.parent
TYPES = list(product((0, 1), repeat=7))
DB = F(67510295447690880)
EPS = F(215, 3)
B = F(37482242363557, 1875285984658080)
ETA = F(1087978231314917, 84387869309613600)
A0 = F(883952004100291, 8438786930961360)
A1 = F(8839887370271285, 84387869309613600)
BASE_WEIGHTS = [F(v)/DB for v in [67510295447690880,
    622403086173831, 3736484626202371, 3694404008494650,
    3606523426712610, 3551800449688044, 1712829042623520,
    2292281651099340, 24602518440, 61096128288912]]
BASE_C = F(22376932866410102)/DB
NAMES = ['ROOT_IC', 'CAP_B2', 'CAP_B3', 'CAP_B4', 'CAP_B5',
         'CAP_B6', 'SAFE6_O', 'PAIR30_O', 'C30_R4_CAP', 'P25_B6']
KCOEFF = [F(0)]+[F(1)]*5+[F(0), F(0), EPS, F(3,2)]

def encode(value):
    if isinstance(value, F): return str(value)
    if isinstance(value, dict): return {str(k): encode(v) for k,v in value.items()}
    if isinstance(value, (list,tuple)): return [encode(v) for v in value]
    return value

def save(name, value):
    with (H/name).open('x') as out:
        out.write(json.dumps(encode(value), ensure_ascii=False, indent=2)+'\n')

def read(path): return json.loads(path.read_text())
def digest(path): return sha256(path.read_bytes()).hexdigest()
def dot(a,b): return sum((x*y for x,y in zip(a,b)), F(0))
def vector(a):
    return list(map(F,a)) if isinstance(a,list) else [F(a.get(str(j),'0')) for j in range(513)]

rows = []
true_states = []
for code,h in enumerate(TYPES):
    c,b2,b3,b4,b5,b6,o = h
    n = sum(h[:6]); v = [F(bit,n) if n else F(0) for bit in h[:6]]
    p = c+b2
    costs = []
    for q in (0,1):
        costs_q = []
        for r,y,z in product((0,1), repeat=3):
            D = 1+p+q+r
            value = F(126000*q,p+1+r+y+z)
            value += F(43*r+31218*y+34458*z,p+b3+3)
            value += F(1654*(r+y+z),p+b3+b4+b5+1)
            value += 5400*(F(o,6)-z)/(D+y)
            value += 7740*(F(o,3*D)-F(y,D+z)-F(z,D+y)-F(y,D*(D+1)))
            value += EPS*r
            costs_q.append(value)
        costs.append(costs_q)
    aq = [min(vs) for vs in costs]
    assert aq[1] > aq[0]
    m = aq[0]+F(o,6)*(aq[1]-aq[0])
    # Full moment interval is [o/6,o], including o=0; check both ends.
    assert m == min(aq[0]+F(o,6)*(aq[1]-aq[0]), aq[0]+o*(aq[1]-aq[0]))
    p25costs = []
    prefix = c+b2+b3
    for r,z in product((0,1), repeat=2):
        load = prefix+b6+r+z
        value = F(25*b6-z,load) if load else F(0)
        value += F(r,2)+z+F(o,6*(prefix+b6+r+1))
        p25costs.append(value)
    pm = min(p25costs)
    # Check the closed P25 envelope against all four actual hidden tails.
    assert pm == (F(3,2)+F(24,prefix+3))*b6+F(o,6*(prefix+1+2*b6))
    D = sum(h[:4])+1
    safe = v[5]-F(o,6*(sum(h[:5])+1))
    pair = v[4]+v[5]+F(b5,D*(D+1))-F(o,3*D)
    c30 = 126000*v[2]+65719*v[3]+4962*v[5]-m
    p25 = 25*v[3]-pm
    rows.append([-v[0]]+[-F(x) for x in h[1:6]]+[safe,pair,c30,p25])
    true_states.append({'code':code,'bits':h,'C30_costs':costs,'C30_minima':aq,
        'C30_weak_tails':[[list(t) for t,x in zip(product((0,1),repeat=3),cs) if x==min(cs)] for cs in costs],
        'C30_moment_minimum':m,'P25_costs':p25costs,
        'P25_weak_tails':[list(t) for t,x in zip(product((0,1),repeat=2),p25costs) if x==pm]})

def residuals(weights, nu):
    return [-ETA*h[0]*(1-h[6])-dot(weights,row)-nu*h[0]-B*h[6]
            for h,row in zip(TYPES,rows)]

def verify_state(label, weights, nu, a, expected_zero=None):
    rho = residuals(weights,nu)
    assert all(x>=0 for x in weights) and all(x>=0 for x in rho),label
    assert weights[0] == 1
    assert dot(weights,KCOEFF)-nu == -a
    for h,row,r in zip(TYPES,rows,rho):
        assert dot(weights,row)+nu*h[0]+B*h[6]+r == -ETA*h[0]*(1-h[6])
    zero = [i for i,r in enumerate(rho) if not r]
    if expected_zero is not None: assert zero==expected_zero,(label,zero)
    return {'label':label,'weights':weights,'C_multiplier':nu,'O_multiplier':B,
            'K_coefficient':a,'all128_residuals':rho,'zero_types':zero,
            'all131_coordinate_identities':'PASS','all_true_weights_strictly_positive':all(x>0 for x in weights)}

states = [verify_state('ROOT1_CAP4',BASE_WEIGHTS,BASE_C,A1,[0,3,5,9,17,102,123])]
old_main = read(W/'main_rootcap_gain/all128_root_payments.json')
assert states[0]['all128_residuals'] == [F(v['new_residual']) for v in old_main]

# Direction 1 is a convex mixture with an exact root/CAP algebraic identity.
trial = [F(1)]+[B]*5+[F(0)]*4
trial_c = F(1,5)+3*B
trial_a = F(1,5)-2*B
direction = residuals(trial,trial_c)
negative = [i for i,d in enumerate(direction) if d<0]
assert negative == [1,126,127]
limits = [(states[0]['all128_residuals'][i]/(-direction[i]),i) for i in negative]
t, limiting = min(limits)
assert (t,limiting) == (F(146931707350,112446727090671),1)
s = t/(1+t)
w2 = [(x+t*y)/(1+t) for x,y in zip(BASE_WEIGHTS,trial)]
c2 = (BASE_C+t*trial_c)/(1+t)
a2 = (A1+t*trial_a)/(1+t)
assert a2 == F(66400039579513467522586981249,633435930915908109658396979040)
states.append(verify_state('ROOT2_ROOT_CAP_MIX',w2,c2,a2,[0,1,3,5,9,17,123]))
directions = [{'label':'ROOT1_TO_ROOT2','t_star':t,'s_star':s,'negative_types':negative,
    'all_type_limits':limits,'trial_residuals':direction,'gain':a2-A1}]

def take_step(label, delta_weights, delta_c, expected_step=None, expected_zero=None):
    prior = states[-1]
    d = [-dot(delta_weights,row)-delta_c*h[0] for h,row in zip(TYPES,rows)]
    limits = [(r/(-di),'customer',i) for i,(r,di) in enumerate(zip(prior['all128_residuals'],d)) if di<0]
    limits += [(w/(-dw),'true_weight',i) for i,(w,dw) in enumerate(zip(prior['weights'],delta_weights)) if dw<0]
    step,kind,index = min(limits)
    assert step>0,(label,kind,index)
    if expected_step is not None: assert step==expected_step,(label,step)
    gain_rate = delta_c-dot(delta_weights,KCOEFF)
    assert gain_rate>0
    w = [x+step*y for x,y in zip(prior['weights'],delta_weights)]
    c = prior['C_multiplier']+step*delta_c
    a = prior['K_coefficient']+step*gain_rate
    state = verify_state(label,w,c,a,expected_zero)
    assert all(r+step*di==rr for r,di,rr in zip(prior['all128_residuals'],d,state['all128_residuals']))
    # Full affine identities, independent constant and slope, all 131 columns.
    assert dot(delta_weights,KCOEFF)-delta_c == -gain_rate
    assert delta_weights[0]==0
    for h,row,di in zip(TYPES,rows,d): assert dot(delta_weights,row)+delta_c*h[0]+di==0
    directions.append({'label':label,'step':step,'limiting_kind':kind,'limiting_index':index,
        'delta_weights':delta_weights,'delta_C':delta_c,'gain_rate':gain_rate,
        'all128_residual_directions':d,'all_parameter_upper_bounds':sorted(limits),
        'all131_affine_identities':'PASS','gain':step*gain_rate})
    states.append(state)

# Main's independently derived PAIR30 - 2 SAFE6 direction.
dw3 = [F(0)]*10
dw3[4],dw3[5],dw3[6],dw3[7] = -F(4,3),F(1),F(2),-F(1)
take_step('ROOT3_SAFE_PAIR',dw3,F(4,5),F(64038719369580574756325,56305416081414054191857509248),[0,1,3,5,9,17,123,125])
assert states[-1]['K_coefficient']==F(265603424292741718699660497571,2533743723663632438633587916160)

# Independently check the next explicit direction proposed by the agent.
dw4 = [F(0)]*10
dw4[3],dw4[4],dw4[5] = F(299,12),-F(17,12),-F(169,18)
dw4[6],dw4[7],dw4[9] = F(1),-F(1),F(1)
take_step('ROOT4_SAFE_PAIR_P25',dw4,F(721,45),F(214288412699877216115223075,102518086330234639169824559963296),[0,1,3,5,9,17,103,123])
assert states[-1]['K_coefficient']==F(644801865488859242734539976772381,6151085179814078350189473597797760)

# Main's next direction: balance the four singleton types, then h103.
# At the current CAP equalities, PAIR-2SAFE = A/18+17E/15.
dw5 = [F(0)]*10
dw5[6],dw5[7] = F(2),-F(1)
for code,cap_index in [(17,2),(9,3),(5,4),(3,5)]:
    dw5[cap_index] = dot(dw5,rows[code])
dc5 = -dot(dw5,rows[103])
assert dc5-dot(dw5,KCOEFF)==F(1,18)
take_step('ROOT5_PAIR_SAFE_A_BALANCE',dw5,dc5)

root_rows=[]
for state in states:
    a = state['K_coefficient']
    rr=[]
    for h in product((0,1),repeat=9):
        n=sum(h[:6]);rr.append((F(h[0],n) if n else F(0))-B*h[7]-ETA*h[8]*(1-h[7]))
    rr.append(-a);root_rows.append(rr)
assert root_rows[1]==vector(read(W/'root270_replycaps_iter2/ROOT270_REPLY_CAP_REWEIGHTED.json')['a'])

cp=W/'delta_uniform_audit/certificate_gamma36.json'
assert digest(cp)=='7c98da8d67c2deaa3b7541a761b3e9f6fa80a7deab00ac80e229d0cd57de15d9'
old=read(cp);inp=read(W/'visible_maximum_joint_v5/exact_input.json')
weights=list(map(F,old['all3056_payments_normalized']))
resids=list(map(F,old['all513_residuals_normalized']))
free=F(old['free_EC_weight_normalized']);alpha_old=F(old['alpha_new'])
positive=[i for i,v in enumerate(weights) if v]
caprow=[-F(atom['o']) for atom in inp['atom_columns']]+[F(6)]
overrides={int(k):vector(v['coefficients']) for k,v in old['row_coefficient_overrides'].items()}
assert overrides[868][512]==-A0
getcontext().prec=65
global_results=[]
for state,rootrow in zip(states,root_rows):
    gain=weights[868]*(state['K_coefficient']-A0)/6
    alpha=alpha_old+gain;overrides[868]=rootrow
    identities=[]
    for j in range(513):
        o=F(inp['equalities'][0]['a'].get(str(j),'0'))
        ec=F(inp['equalities'][1]['a'].get(str(j),'0'))
        obj=F(inp['objective'].get(str(j),'0'))
        rhs=resids[j]+free*ec+gain*caprow[j]
        for i in positive:
            rr=inp['raw_rows'][i]
            coef=overrides[i][j] if i in overrides else F(rr['a'].get(str(j),'0'))-F(rr['rhs'])*o
            rhs+=weights[i]*coef
        assert obj-alpha*o==rhs,j
        identities.append(F(0))
    global_results.append({'root_label':state['label'],'alpha':alpha,
        'alpha_decimal':str(Decimal(alpha.numerator)/Decimal(alpha.denominator)),
        'gain_over_gamma36':gain,'all513_identity_residuals':identities})

source_paths=['main_rootcap_gain/check_and_build.py','main_rootcap_gain/exact_certificate.json',
    'main_rootcap_gain/all128_root_payments.json','root270_replycaps_iter2/freeze_manifest.json',
    'root270_replycaps_iter2/ROOT270_REPLY_CAP_REWEIGHTED.json',
    'delta_uniform_audit/certificate_gamma36.json','visible_maximum_joint_v5/exact_input.json']
save('source_pins.json',{'files':[{'path':p,'sha256':digest(W/p),'bytes':(W/p).stat().st_size} for p in source_paths]})
save('all_true_costs.json',true_states)
save('all_root_payment_states.json',states)
save('all_reweighting_directions.json',directions)
save('all_root_visible_rows.json',[{'label':s['label'],'a':r,'rhs':'0','numerical_divisor':'1'} for s,r in zip(states,root_rows)])
save('all_global_identity_checks.json',global_results)
save('exact_certificate.json',{'status':'PASS_MAIN_TRUE_ROOT_REWEIGHTING_UNIVERSAL_BOUND',
    'strongest_root':states[-1]['label'],'alpha':global_results[-1]['alpha'],
    'alpha_decimal':global_results[-1]['alpha_decimal'],
    'all3056_original_position_weights':weights,'positive_original_indices':positive,
    'overrides':overrides,'additional_true_query_cap':{'a':caprow,'weight':global_results[-1]['gain_over_gamma36'],'rhs':'0'},
    'free_C_equality_multiplier':free,'all513_nonnegative_residuals':resids,
    'all513_identity_residuals':global_results[-1]['all513_identity_residuals'],
    'zero_residual_columns':[i for i,v in enumerate(resids) if not v],
    'half_status':'OPEN','optimizer_calls':0})
result={'status':'PASS_MAIN_ALL_TRUE_COSTS_ROOT131_AFFINE_DIRECTIONS_AND_GLOBAL513',
    'C30_true_costs':2048,'P25_true_costs':512,'root_states':len(states),
    'root_columns_each':131,'global_columns_each':513,'all_weak_tails_retained':True,
    'strongest_root_K_coefficient':states[-1]['K_coefficient'],
    'strongest_root_zero_types':states[-1]['zero_types'],
    'all_true_root_weights_strictly_positive':all(s['all_true_weights_strictly_positive'] for s in states),
    'alpha':global_results[-1]['alpha'],'alpha_decimal':global_results[-1]['alpha_decimal'],
    'optimizer_calls':0,'half_status':'OPEN'}
save('check_result.json',result)
print(json.dumps(encode({'result':result,'directions':[{k:d[k] for k in ['label','step','gain_rate','limiting_kind','limiting_index'] if k in d} for d in directions],
    'alphas':[{k:r[k] for k in ['root_label','alpha_decimal']} for r in global_results]}),ensure_ascii=False))
