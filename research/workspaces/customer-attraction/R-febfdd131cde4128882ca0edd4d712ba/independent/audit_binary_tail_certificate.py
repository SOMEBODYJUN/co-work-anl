"""Independent exact audit from raw utilities of binary-background four-tail lemma.

Reads only submitted rational multipliers, not author's coefficient implementation.
"""
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import json,argparse

BASE=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--certificate',type=Path,default=BASE/'parent/binary_tail_exact.json')
args=parser.parse_args()
cert=json.loads(args.certificate.read_text())
weights={name:F(value) for name,value in cert['multipliers'].items()}
assert weights and all(value>=0 for value in weights.values())
beta0,beta1=F(cert['beta0']),F(cert['beta1'])
assert beta0>=0 and beta1>=0

def safe(n,d):
    return F(n,d) if n else F(0)

def raw_rows(background,bits,optbits):
    # The first path is the genuine four-player continuation after an arbitrary
    # fixed binary-load history. The second forces its root to copy last theme D.
    aa,bb,cc,dd,qq,rr,ss=bits
    actual=(aa,bb,cc,dd)
    branch=(dd,qq,rr,ss)
    e=sum(optbits)
    labels=dict(zip('abcdqrs',bits))
    def utility(path,index):
        return safe(path[index],background+sum(path))
    def safety(path,index,label):
        prefix=background+sum(path[:index])
        return utility(path,index)-safe(labels[label],prefix+4-index)
    def last_opt(path):
        return sum((utility(path,3)-safe(t,background+sum(path[:3])+1)
                    for t in optbits),F(0))
    def pair_opt(path):
        prefix=background+sum(path[:2])
        H=utility(path,2)+utility(path,3)+safe(path[2],(prefix+1)*(prefix+2))
        # For every one of six index pairs, the two-player tax bound says its
        # residual profit is at most H. Reconstruct every pair individually.
        return sum((H-safe(optbits[i]+optbits[j],prefix+optbits[i]+optbits[j])
                    for i,j in combinations(range(4),2)),F(0))
    rows={}
    for i in range(4):
        for label in labels:rows[f'actual:{i}:K:'+label]=safety(actual,i,label)
    for i in range(1,4):
        for label in labels:rows[f'off:{i}:K:'+label]=safety(branch,i,label)
    rows['actual:3:sum-opt']=last_opt(actual)
    rows['actual:pair-opt']=pair_opt(actual)
    rows['off:1:K:c']=safety(branch,1,'c')
    rows['off:3:K:c']=safety(branch,3,'c')
    rows['off:3:sum-opt']=last_opt(branch)
    rows['off:pair-opt']=pair_opt(branch)
    rows['root-copy-d']=utility(actual,0)-utility(branch,0)
    assert set(weights)<=set(rows)
    target=safe(e,background+e)
    V=safe(sum(actual),background+sum(actual))
    return rows,(beta0 if background==0 else beta1)*V-target

# Full 16 comparator bit patterns independently reconstruct the six pairs;
# their aggregated coefficient must depend only on count e.
residuals=[]
by_count={}
for p,eta,opt in product((0,1),product((0,1),repeat=7),product((0,1),repeat=4)):
    rows,lhs=raw_rows(p,eta,opt)
    R=lhs-sum((weight*rows[name] for name,weight in weights.items()),F(0))
    assert R>=0,(p,eta,opt,R)
    key=(p,eta,sum(opt))
    if key in by_count:assert by_count[key]==R
    else:by_count[key]=R
    residuals.append(R)
assert len(by_count)==1280
assert min(residuals)==0
zeros=sum(r==0 for r in by_count.values())
assert zeros==cert['zero_residuals']
out={
 'status':'PASS',
 'reconstruction':'raw terminal shares; six comparator index pairs individually; no author code imports',
 'full_states_checked':len(residuals),'compressed_count_states':len(by_count),
 'nonnegative_multipliers':len(weights),'min_residual':str(min(residuals)),
 'zero_count_states':zeros,
 'beta0':str(beta0),'beta1':str(beta1),
 'theorem':f'R_binary_background(Q1,Q2,Q3,Q4) <={beta0} V_outside+({beta1})V_inside',
 'aligned_root_consequence':f'4OPT+({beta0-beta1})sum|Ti| <={beta0}sum V_i+({beta0-beta1})sum z_i',
}
(BASE/'independent'/('audit_'+args.certificate.stem+'.json')).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
