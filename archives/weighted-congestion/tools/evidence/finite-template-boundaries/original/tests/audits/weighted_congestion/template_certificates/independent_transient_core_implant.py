from fractions import Fraction as F
from itertools import product
from hashlib import sha256
from pathlib import Path
import json
import argparse, sys, platform

w = (F(1), F(2), F(3, 2), F(7, 3), F(5, 4))
d, alpha = 2, F(52, 51)
m, nprime, flag = d + 2, 4, 4
states = list(product((0,1), repeat=len(w)))
Q0 = [(0,0), (1,0), (1,1), (0,1)]
Q = [y + (0,0,1) for y in Q0]
q=Q[0][:-1]
nextQ = dict(zip(Q, Q[1:]+Q[:1]))

def select(s):
    if s[flag]==0:
        i = 0 if sum(s[:m])%2==0 else flag
    elif s in nextQ:
        t=nextQ[s]
        i=next(j for j in range(len(w)) if s[j]!=t[j])
    else:
        i=next(j for j in range(nprime) if s[j]!=q[j])
    t=list(s); t[i]=1-t[i]
    return i, tuple(t)

S = [s for s in states if s[flag]==0 and sum(s[:m])%2==0]

def resourcecost(s,i,sig,k):
    if sig[i]!=s[i]: return F(0)
    load=sum((wj for j,wj in enumerate(w) if sig[j]==s[j]), F(0))
    return load**k

def columnvalue(s,sig,k,beta):
    i,t=select(s)
    return resourcecost(s,i,sig,k)-beta*resourcecost(t,i,sig,k)

sigs=[sig for sig in product((-1,0,1),repeat=len(w)) if any(x!=-1 for x in sig)]
colcount=0
beta_set=(F(1),alpha,F(2))
for sig in sigs:
    for k in range(d+1):
        avgs=[]
        for beta in beta_set:
            avg=sum((columnvalue(s,sig,k,beta) for s in S),F(0))/len(S)
            assert avg<=0
            avgs.append(avg)
        assert avgs[0]==0
        colcount+=1

# Every path has the one prescribed recurrent cycle and every edge flips one bit.
for s in states:
    i,t=select(s)
    assert sum(x!=y for x,y in zip(s,t))==1
    seen={}; trajectory=[]; u=s
    while u not in seen:
        seen[u]=len(trajectory); trajectory.append(u); u=select(u)[1]
    recurrence=trajectory[seen[u]:]
    assert len(recurrence)==len(Q) and set(recurrence)==set(Q)
    for beta in beta_set:
        sig=tuple(s[j] if j==i else -1 for j in range(len(w)))
        assert columnvalue(s,sig,0,beta)==1

# Recompute original game actual resource loads, without matrix aggregation.
resources=[((1,1,-1,-1,-1),1,F(13)),
           ((1,0,-1,-1,-1),2,F(3)),
           ((0,1,-1,-1,-1),2,F(3)),
           ((0,0,-1,-1,-1),1,F(13))]

def gamecost(s,i):
    return sum((a*resourcecost(s,i,sig,k) for sig,k,a in resources),F(0))
b={}
for s in states:
    i,t=select(s)
    b[s]=gamecost(s,i)-alpha*gamecost(t,i)
assert all(b[s]>0 for s in Q)
eta=min(b[s] for s in Q)
M=max([F(0)]+[-b[s] for s in states if s not in Q])
bound=eta/(eta+M)
assert 0<bound<=1
assert sum(b[s] for s in S)/len(S)<=0

# Detect loss of cancellation immediately one degree beyond the claimed range.
frontier_sig=(1,1,1,1,-1)
frontier_val=sum((columnvalue(s,frontier_sig,d+1,F(1)) for s in S),F(0))/len(S)
assert frontier_val!=0

result={
 'statement_sha256':'c55819d7419000c36ff7d5a0257cc46af509f7e2d4d3fbd6c953410d7615e694',
 'proof_sha256':'c2cde533f35fbc9d8bcaa0bc0894aad2d015af7528835b71f9e98515d041f5c7',
 'scope':'finite exact fixture; general proof independently checked separately',
 'arithmetic':'fractions.Fraction; no solver, tolerance or randomness',
 'd':d,'alpha':str(alpha),'weights':[str(x) for x in w],
 'states':len(states),'parity_support':len(S),'fullproper_signatures':len(sigs),
 'checked_columns':colcount,'checked_beta':[str(x) for x in beta_set],
 'recurrent_cost_margins':[str(b[s]) for s in Q],
 'eta':str(eta),'M':str(M),'mass_lower_bound':str(bound),
 'one_degree_beyond_parity_value':str(frontier_val),
 'result':'all stated finite checks passed'
}
parser=argparse.ArgumentParser(description='Independent literal full-proper transient necessity fixture audit')
parser.add_argument('--output',type=Path)
args=parser.parse_args()
result.update(source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
              command=' '.join(sys.argv),python=platform.python_version(),seed=None)
output=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
if args.output:
    with args.output.open('x') as stream:stream.write(output)
    print(json.dumps({'output':str(args.output),'status':'PASS'}))
else:print(output,end='')
