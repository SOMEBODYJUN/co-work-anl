"""Independent standard-library reconstruction of the binary four-tail proof.

Only certificate scalars are read. No discovery generator, optimizer, prior audit,
or imported residual table is used to establish the claim. All formulas below
are transcribed from four_remaining_profit_bound.md equations (3)--(13).
"""
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import json,hashlib

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'root'/'binary_four_tail_certificate.json'
raw=json.loads(SOURCE.read_text())
NAMES=('K_C','K_D','K_Q','K_R','K_S','E','P','current_IC',
       'Q_query_S','R_query_C','R_query_S','S_query_B')
assert set(raw['weights'])==set(NAMES)
weights={name:F(raw['weights'][name]) for name in NAMES}
beta=F(raw['beta'])
assert beta==F(22869393,11445824)
assert all(x>=0 for x in weights.values())
assert weights['E']+weights['P']==1
assert beta<F(1499,750)<2

def share(numerator,denominator):
    return F(numerator,denominator) if numerator else F(0)

def denominator(p):return (p+1)*(p+2)*(p+3)*(p+4)

def correction_pair(p,v):
    return F(1,p+1)-F(1,p+v+1)+(F(2*p*p,3*denominator(p)) if v==2 else F(0))

def correction_last(p,v):
    return F(1,p+1)-F(1,p+v+1)+(F(p*p+p,denominator(p)) if v==3 else F(0))

# Reconstruct the twelve original rows first using the common-denominator
# numerators in the OLD mathematical text, rather than the discovery function.
def polynomial_rows(p,eta):
    a,b,c,d,q,r,s=eta
    load_actual=a+b+c+d;load_dev=d+q+r+s;D=denominator(p)
    P={0:F(0)}
    for j in range(1,5):P[j]=F(D,p+j)
    Q={j:F(D,(p+j)*(p+j+1)) for j in range(1,4)}
    nums={}
    for label,membership in zip(('C','D','Q','R','S'),(c,d,q,r,s)):
        nums['K_'+label]=b*P[load_actual]-membership*P[a+3]
    H=(c+d)*P[load_actual]+c*Q[a+b+1]
    nums['P']=2*H+P[1]-P[a+b+1]+(F(2*p*p,3) if a+b==2 else F(0))
    nums['E']=4*d*P[load_actual]+P[1]-P[a+b+c+1]+(p*p+p if a+b+c==3 else 0)
    nums['current_IC']=a*P[load_actual]-d*P[load_dev]
    nums['Q_query_S']=q*P[load_dev]-s*P[d+3]
    nums['R_query_C']=r*P[load_dev]-c*P[d+q+2]
    nums['R_query_S']=r*P[load_dev]-s*P[d+q+2]
    nums['S_query_B']=s*P[load_dev]-b*P[d+q+r+1]
    return {name:nums[name]/D for name in NAMES}

# An independent second transcription directly from terminal payoffs and the
# two aggregated slacks. This checks all polynomial numerator conventions.
def payoff_rows(p,eta):
    a,b,c,d,q,r,s=eta
    ka=a+b+c+d;kd=d+q+r+s
    ua,ub,uc,ud=(share(x,p+ka) for x in (a,b,c,d))
    zd,zq,zr,zs=(share(x,p+kd) for x in (d,q,r,s))
    result={}
    for label,membership in zip(('C','D','Q','R','S'),(c,d,q,r,s)):
        result['K_'+label]=ub-F(membership,p+a+3)
    H=uc+ud+F(c,(p+a+b+1)*(p+a+b+2))
    result['P']=2*H+correction_pair(p,a+b)
    result['E']=4*ud+correction_last(p,a+b+c)
    result['current_IC']=ua-zd
    result['Q_query_S']=zq-F(s,p+d+3)
    result['R_query_C']=zr-F(c,p+d+q+2)
    result['R_query_S']=zr-F(s,p+d+q+2)
    result['S_query_B']=zs-F(b,p+d+q+r+1)
    return result

# Rebuild aggregation from all 16 memberships in four comparison labels,
# explicitly summing SIX pairs, not just trusting a compressed e formula.
aggregate_counts={'pair':0,'last':0}
minimum_aggregate={'pair':None,'last':None}
for p in (0,1):
    for t in product((0,1),repeat=4):
        e=sum(t);O=share(e,p+e)
        for v in range(3):
            pair_sum=sum((share(t[i]+t[j],p+v+t[i]+t[j])
                          for i,j in combinations(range(4),2)),F(0))
            residual=pair_sum/3+correction_pair(p,v)-O
            assert residual>=0,(p,v,t,'P',residual)
            key='pair';aggregate_counts[key]+=1
            minimum_aggregate[key]=(residual if minimum_aggregate[key] is None else min(residual,minimum_aggregate[key]))
        for v in range(4):
            query_sum=sum((F(x,p+v+1) for x in t),F(0))
            residual=query_sum+correction_last(p,v)-O
            assert residual>=0,(p,v,t,'E',residual)
            key='last';aggregate_counts[key]+=1
            minimum_aggregate[key]=(residual if minimum_aggregate[key] is None else min(residual,minimum_aggregate[key]))

# The exported residues are only a consistency comparison AFTER rebuilding.
exported={}
for item in raw['residues']:
    key=(item['p'],tuple(item['bits']))
    assert key not in exported
    exported[key]=F(item['rho'])
new_residuals={};row_equalities=0
for p in (0,1):
    for eta in product((0,1),repeat=7):
        polynomial=polynomial_rows(p,eta)
        direct=payoff_rows(p,eta)
        assert polynomial==direct,(p,eta)
        row_equalities+=len(NAMES)
        V=share(sum(eta[:4]),p+sum(eta[:4]))
        rho=beta*V-sum((weights[name]*polynomial[name] for name in NAMES),F(0))
        assert rho>=0,(p,eta,rho)
        new_residuals[(p,eta)]=rho
        assert exported[(p,eta)]==rho
assert set(exported)==set(new_residuals) and len(new_residuals)==256
assert sum(r==0 for r in new_residuals.values())==17==raw['zero_residues']

# On binary backgrounds the two positive arbitrary-p corrections are optional.
# Recheck uncorrected aggregation independently, including all e,v states.
uncorrected_aggregate=0
for p in (0,1):
    for v in range(3):
        for e in range(5):
            pair=F(e*(4-e),3*(p+v+1))+F(e*(e-1),3*(p+v+2))
            tau=F(1,p+1)-F(1,p+v+1)
            assert pair+tau-share(e,p+e)>=0
            uncorrected_aggregate+=1
    for v in range(4):
        for e in range(5):
            tau=F(1,p+1)-F(1,p+v+1)
            assert F(e,p+v+1)+tau-share(e,p+e)>=0
            uncorrected_aggregate+=1
UNCSOURCE=SOURCE.with_name('binary_four_tail_uncorrected_certificate.json')
uncraw=json.loads(UNCSOURCE.read_text())
assert F(uncraw['beta'])==beta
assert {n:F(v) for n,v in uncraw['weights'].items()}==weights
uncexported={(r['p'],tuple(r['bits'])):F(r['rho']) for r in uncraw['residues']}
assert set(uncexported)==set(new_residuals)
uncorrected_states=0
for (p,eta),rho in new_residuals.items():
    a,b,c,d,q,r,s=eta;D=denominator(p)
    extraP=F(2*p*p,3*D) if a+b==2 else F(0)
    extraE=F(p*p+p,D) if a+b+c==3 else F(0)
    expected=rho+weights['P']*extraP+weights['E']*extraE
    assert expected>=rho>=0
    assert uncexported[(p,eta)]==expected
    uncorrected_states+=1

out={
 'status':'PASS_independent_exact_binary_four_tail_certificate',
 'scope':'Original five-provider model, any ordered one-provider prefix, four genuine SPE successors; p_x in {0,1}.',
 'conclusion':'F4(p)<=beta*V4 only; not full coverage, not HALF(5), no arbitrary-background or old-RHOMIN assertion.',
 'beta':str(beta),'gap_below_two':str(2-beta),'improvement_over_old':str(F(1499,750)-beta),
 'nonnegative_weights':True,'E_plus_P':str(weights['E']+weights['P']),
 'aggregate_states':aggregate_counts,'aggregate_minima':{k:str(v) for k,v in minimum_aggregate.items()},
 'coefficient_states':len(new_residuals),'row_transcription_equalities':row_equalities,
 'zero_residuals':sum(v==0 for v in new_residuals.values()),
 'new_minimum_by_p':{str(p):str(min(v for (q,b),v in new_residuals.items() if q==p)) for p in (0,1)},
 'new_positive_minimum_by_p':{str(p):str(min(v for (q,b),v in new_residuals.items() if q==p and v>0)) for p in (0,1)},
 'uncorrected_binary_aggregation_states':uncorrected_aggregate,
 'uncorrected_coefficient_states':uncorrected_states,
 'uncorrected_certificate_sha256':hashlib.sha256(UNCSOURCE.read_bytes()).hexdigest(),
 'certificate_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
 'imports':'Python standard library only; no generator, optimizer, existing audit, or RHOMIN import.'
}
OUT=HERE/'audit_binary_four_tail_independent.json';OUT.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
