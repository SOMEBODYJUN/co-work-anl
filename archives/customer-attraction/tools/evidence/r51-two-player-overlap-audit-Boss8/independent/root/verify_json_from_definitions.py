"""Independent JSON audit from client sets and the eight named payoff slacks.
Reads the frozen report; does not import or execute the author verifier.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
from collections import Counter
import hashlib,json
HERE=Path(__file__).resolve().parent
src=HERE/'audit_two_player_overlap.json'
J=json.loads(src.read_text())

def U(S,T):
    return sum((Q(1,2) if x in T else Q(1)) for x in S)

def audit_game(label,rec):
    S=[frozenset(row) for row in rec['topics']]
    p=len(S); replies=rec['replies']; a,b=rec['actual']
    assert len(replies)==p and replies[a]==b
    tail_table=[[U(T,B) for T in S] for B in S]
    tail_slacks=[]
    for i in range(p):
        chosen=tail_table[i][replies[i]]
        tail_slacks.extend(chosen-v for v in tail_table[i])
    root=[U(S[i],S[replies[i]]) for i in range(p)]
    root_slacks=[root[a]-v for v in root]
    assert min(tail_slacks)>=0 and min(root_slacks)>=0
    W=len(S[a]|S[b]); I=len(S[a]&S[b]); O=max(len(X|Y) for X in S for Y in S)
    assert (rec['W'],rec['I'],rec['OPT'])==(W,I,O)
    assert rec['comparisons']==p*p+p
    assert 10*W+2*I==8*O
    optimum_pairs=[[i,j] for i in range(p) for j in range(p) if len(S[i]|S[j])==O]
    return {'name':label,'topics':p,'clients':len(set().union(*S)), 'actual':[a,b],
        'W':W,'I':I,'OPT':O,'chosen_tail_payoffs':[str(tail_table[i][replies[i]]) for i in range(p)],
        'root_payoffs':[str(x) for x in root], 'tail_payoff_table':[[str(v) for v in row] for row in tail_table],
        'root_comparisons':p,'tail_comparisons':p*p,'minimum_root_slack':str(min(root_slacks)),
        'minimum_tail_slack':str(min(tail_slacks)),'optimal_ordered_pairs':optimum_pairs,'sharp_equality':10*W+2*I==8*O}

seen={}
for row in J['residuals']:
    key=tuple(row['bits'])
    assert key not in seen and len(key)==6 and set(key)<={0,1}
    c,d,t1,t2,r1,r2=key
    actual=Q(c,1+d); last=Q(d,1+c)
    F=[actual-Q(t1,1+r1),actual-Q(t2,1+r2)]
    P=[last-Q(t1,1+c),last-Q(t2,1+c)]
    Z=[last-Q(r1,1+c),last-Q(r2,1+c)]
    V=[Q(r1-t2,1+t1),Q(r2-t1,1+t2)]
    G=3*sum(F)+sum(P)+4*sum(Z)+4*sum(V)
    rho=10*int(c or d)+2*c*d-8*int(t1 or t2)-G
    assert rho==Q(row['residual']) and rho>=0
    t=t1+t2;r=r1+r2;h=t1*r1+t2*r2
    # Separate six-case table from the analytic proof.
    table=((Q(0),Q(h,2),4+Q(r,2)),(4-2*r,Q(7,2)+Q(h,2)-2*r,7-Q(3*r,2)))
    assert rho==table[c][t]
    seen[key]=rho
assert set(seen)==set(product((0,1),repeat=6))
assert J['binary_cases']==len(seen)==64
assert Q(J['minimum_residual'])==min(seen.values())==0
assert all(seen[c,0,t1,t2,r1,r2]==seen[c,1,t1,t2,r1,r2] for c,t1,t2,r1,r2 in product((0,1),repeat=5))
games=[audit_game('collision-free endpoint',J['endpoints'][0]),audit_game('full-overlap endpoint',J['endpoints'][1]),audit_game('Cartesian product',J['cartesian_product'])]
# Check literal product topic/reply construction in the report.
A=J['endpoints'][0];B=J['endpoints'][1];C=J['cartesian_product']
assert C['topics']==[sorted(set(x)|set(y)) for x in A['topics'] for y in B['topics']]
assert C['replies']==[2*A['replies'][a]+B['replies'][b] for a in range(4) for b in range(2)]
assert C['actual']==[2*A['actual'][0]+B['actual'][0],2*A['actual'][1]+B['actual'][1]]
assert all(C[k]==A[k]+B[k] for k in ['W','I','OPT'])
report={'source_id':'8790d2f2ec1c1e3501f0','source_size':len(src.read_bytes()),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
    'verification':'all assertions passed; author program not imported or executed',
    'binary_cases':len(seen),'residual_histogram':dict(sorted(Counter(str(x) for x in seen.values()).items(),key=lambda kv:Q(kv[0]))),
    'd_independent':True,'minimum_residual':str(min(seen.values())),'games':games,'complete_SPE_action_comparisons':sum(g['root_comparisons']+g['tail_comparisons'] for g in games)}
(HERE/'json-definition-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='games'},ensure_ascii=False,indent=2))
