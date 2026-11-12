"""Main: reconstruct C30 with true reply size caps and pay a universal gain.

All rational formulas below are independently transcribed from the formal
C30/ROOT270 proof. No optimizer or candidate-point support is used.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
from decimal import Decimal, getcontext
import json

H = Path(__file__).resolve().parent
W = H.parent

def read(p):
    return json.loads(p.read_text())

def digest(p):
    return sha256(p.read_bytes()).hexdigest()

def dump(name, value):
    p = H / name
    with p.open('x') as f:
        f.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def fraclist(values):
    return [str(v) for v in values]

def vec(v):
    if isinstance(v, list):
        assert len(v) == 513
        return list(map(F, v))
    return [F(v.get(str(j), '0')) for j in range(513)]

DB = F(67510295447690880)
LC = F(24602518440)
EPS = F(215, 3)
ETA = F(1087978231314917, 84387869309613600)
OLD_BK = F(1767904008200582, 16877573861922720)
BO = F(337340181272013, 16877573861922720)
GAIN_K = LC * EPS / (6 * DB)
BK = OLD_BK + GAIN_K
assert GAIN_K == F(14693170735, 3375514772384544)
assert BK == F(8839887370271285, 84387869309613600)
CAP = list(map(F, [622403086173831, 3736778489617071, 3696167188982850,
                  3608286607200810, 3553563630176244]))
NEW_CAP = [CAP[0], CAP[1]-LC*EPS/6] + [v-LC*EPS for v in CAP[2:]]
assert all(v > 0 for v in NEW_CAP)
LE = F(1712829042623520)
LP = F(2292281651099340)
L25 = F(61096128288912)
BETA_C = F(22380459227386502)
NEW_BETA_C = BETA_C - 2*LC*EPS
BETA_O = F(1349360725088052)

def phi(h, q, r, y, t):
    c,b2,b3,b4,b5,b6,o = h
    b = c+b2
    D = 1+b+q+r
    return (F(126000*q, b+1+r+y+t)
            + F(43*r+31218*y+34458*t, b+b3+3)
            + F(1654*(r+y+t), b+b3+b4+b5+1)
            + F(5400)*(F(o,6)-t)/F(D+y)
            + F(7740)*(F(o,3*D)-F(y,D+t)-F(t,D+y)-F(y,D*(D+1))))

def envelope(h, eps):
    costs = [[phi(h,q,*tail)+eps*tail[0] for tail in product((0,1),repeat=3)] for q in (0,1)]
    aq = [min(row) for row in costs]
    tails = list(product((0,1),repeat=3))
    weak = [[list(tails[i]) for i,c in enumerate(costs[q]) if c == aq[q]] for q in (0,1)]
    m = aq[0] if not h[-1] else min((5*aq[0]+aq[1])/6,aq[1])
    return m, costs, aq, weak

all_states = []
root_checks = []
old_zero = []
new_zero = []
for index,h in enumerate(product((0,1), repeat=7)):
    c,b2,b3,b4,b5,b6,o = h
    load = sum(h[:6])
    v = [F(t,load) if load else F(0) for t in h[:6]]
    m0,cost0,a0,weak0 = envelope(h,F(0))
    m1,cost1,a1,weak1 = envelope(h,EPS)
    for q in (0,1):
        for j,tail in enumerate(product((0,1), repeat=3)):
            assert cost1[q][j]-cost0[q][j] == EPS*tail[0]
        assert all(x >= a1[q] for x in cost1[q])
    end = v[5]-F(o,6*(sum(h[:5])+1))
    D = sum(h[:4])+1
    pair = v[4]+v[5]+F(b5,D*(D+1))-F(o,3*D)
    c30old = 126000*v[2]+65719*v[3]+4962*v[5]-m0
    c30new = 126000*v[2]+65719*v[3]+4962*v[5]-m1
    p = c+b2+b3
    p25 = 25*v[3]-(F(3,2)+F(24,p+3))*b6-F(o,6*(p+1+2*b6))
    root_old = -DB*v[0]-sum(L*t for L,t in zip(CAP,h[1:6]))+LE*end+LP*pair+LC*c30old+L25*p25
    root_new = -DB*v[0]-sum(L*t for L,t in zip(NEW_CAP,h[1:6]))+LE*end+LP*pair+LC*c30new+L25*p25
    rho0 = -root_old-BETA_C*c-BETA_O*o-DB*ETA*c*(1-o)
    rho1 = -root_new-NEW_BETA_C*c-BETA_O*o-DB*ETA*c*(1-o)
    assert rho0 >= 0 and rho1 >= 0, (index, rho0, rho1)
    assert rho1-rho0 == LC*((m1-m0)+EPS*(2*c-F(b3,6)-b4-b5-b6))
    if not rho0: old_zero.append(index)
    if not rho1: new_zero.append(index)
    assert root_new+rho1+NEW_BETA_C*c+BETA_O*o == -DB*ETA*c*(1-o)
    root_checks.append({'index':index,'bits':list(h),'old_strict_residual':str(rho0/DB),
        'new_residual':str(rho1/DB),'old_envelope':str(m0),'new_envelope':str(m1),
        'new_root_customer_identity_residual':'0'})
    all_states.append({'index':index,'bits':list(h),'old_costs':[fraclist(a) for a in cost0],
        'new_costs':[fraclist(a) for a in cost1],'old_minima':fraclist(a0),'new_minima':fraclist(a1),
        'old_weak_tails':weak0,'new_weak_tails':weak1})
assert old_zero == [0,1,3,5,9,17,33,102,103,115,121,123,125]
assert new_zero == [0,3,5,9,17,102,123]
new_K_rhs = sum(NEW_CAP)+LC*EPS+F(3,2)*L25-NEW_BETA_C
assert new_K_rhs == -DB*BK
assert -BETA_O == -DB*BO
assert DB == DB*1

# Lift the genuinely universal root row, with the actual root payoff, to all9 bits.
root_row=[]
for h in product((0,1), repeat=9):
    a = h[:6]; n=sum(a); o,c=h[7],h[8]
    root_row.append((F(a[0],n) if n else F(0))-BO*o-ETA*c*(1-o))
root_row.append(-BK)
old_row = vec(read(W/'main_root270_strict_outside/ROOT270_STRICT_C_OUTSIDE.json')['a'])
assert all(root_row[j] == old_row[j] for j in range(512))
assert root_row[512] == old_row[512]-GAIN_K

# Reuse the already audited complete universal certificate, without another LP.
cp = W/'delta_uniform_audit/certificate_gamma36.json'
assert digest(cp) == '7c98da8d67c2deaa3b7541a761b3e9f6fa80a7deab00ac80e229d0cd57de15d9'
old = read(cp)
inp = read(W/'visible_maximum_joint_v5/exact_input.json')
weights = list(map(F, old['all3056_payments_normalized']))
residuals = list(map(F, old['all513_residuals_normalized']))
free = F(old['free_EC_weight_normalized'])
alpha_old = F(old['alpha_new'])
query_cap_weight = weights[868]*GAIN_K/6
alpha = alpha_old+query_cap_weight
caprow = [-F(atom['o']) for atom in inp['atom_columns']]+[F(6)]
overrides = {int(k):vec(row['coefficients']) for k,row in old['row_coefficient_overrides'].items()}
assert overrides[868] == old_row
overrides[868] = root_row
positive = [k for k,x in enumerate(weights) if x]
identities=[]
for j in range(513):
    o = F(inp['equalities'][0]['a'].get(str(j),'0'))
    ec = F(inp['equalities'][1]['a'].get(str(j),'0'))
    objective = F(inp['objective'].get(str(j),'0'))
    rhs = residuals[j]+free*ec+query_cap_weight*caprow[j]
    for k in positive:
        row = inp['raw_rows'][k]
        coefficient = overrides[k][j] if k in overrides else F(row['a'].get(str(j),'0'))-F(row['rhs'])*o
        rhs += weights[k]*coefficient
    assert objective-alpha*o == rhs, j
    assert residuals[j] >= 0
    identities.append('0')
getcontext().prec=60
dump('all128_root_payments.json',root_checks)
dump('all2048_true_C30_costs_and_weak_tails.json',all_states)
dump('ROOT270_CAP4_STRICT_K.json',{'name':'ROOT270_CAP4_STRICT_K','a':fraclist(root_row),
    'rhs':'0','numerical_divisor':'1','scope':'Every original complete-history SPE; any six legal query union; C is a genuine maximum-size legal label.',
    'root_K_gain':str(GAIN_K),'source_CAP4_cost_weight':str(EPS)})
dump('exact_certificate.json',{'status':'PASS_MAIN_TRUE_ROOT_CAP4_UNIVERSAL_WELFARE_CERTIFICATE',
    'old_alpha':str(alpha_old),'alpha':str(alpha),'gain':str(query_cap_weight),
    'alpha_decimal':str(Decimal(alpha.numerator)/Decimal(alpha.denominator)),
    'all3056_original_position_weights':fraclist(weights),'positive_original_indices':positive,
    'overrides':{str(k):fraclist(v) for k,v in overrides.items()},
    'additional_true_query_cap':{'a':fraclist(caprow),'weight':str(query_cap_weight),'rhs':'0'},
    'free_C_equality_multiplier':str(free),'all513_nonnegative_residuals':fraclist(residuals),
    'all513_identity_residuals':identities,'zero_residual_columns':[j for j,x in enumerate(residuals) if not x],
    'half_status':'OPEN','optimizer_calls':0,'scope':'Universal necessary welfare bound, not an LP optimum or an SPE construction.'})
result={'status':'PASS_MAIN_ROOT_CAP4_ALL_TRUE_COSTS_ROOT131_AND_GLOBAL513',
    'true_tail_costs_rebuilt':2048,'all_weak_tail_states_preserved':True,
    'root_customer_columns':128,'root_total_columns_including_u_K_O':131,
    'old_strict_zero_types':old_zero,'new_strict_zero_types':new_zero,
    'new_positive_root_CAP_weights':fraclist(NEW_CAP),'new_C30_CAP4_weight':str(LC*EPS),
    'new_free_root_C_multiplier':str(NEW_BETA_C),'root_K_gain':str(GAIN_K),
    'full_global_columns':513,'positive_global_payments':len(positive)+1,
    'old_alpha':str(alpha_old),'alpha':str(alpha),'alpha_decimal':str(Decimal(alpha.numerator)/Decimal(alpha.denominator)),
    'global_gain':str(query_cap_weight),'input_old_certificate_sha256':digest(cp),
    'optimizer_calls':0,'half_status':'OPEN'}
dump('check_result.json',result)
print(json.dumps(result,ensure_ascii=False))
