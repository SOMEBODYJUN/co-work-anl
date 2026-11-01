"""Test one explicit general coupling candidate on frozen full SPE certificates.
No game search; exact Fraction arithmetic and full histories are retained.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import json

CANDIDATE='For every legal prefix h and every p, E_A u_current(finish(h,A)) >= E_A,T K_h(T,A), where K_h(T,A)=sum_{x in T}1/(1+c_x(finish(h,A))) and A,T iid p.'
NAMES=['portfolio_matching_failure','root_tax_failure','individual_security_failure','eight_cce_welfare_gap','coverage_opportunity_failure','prefix_balance_failure']

def run(name):
    data=json.loads(Path(f'examples/customer_attraction/{name}.json').read_text())
    cert=json.loads(Path(f'evidence/certificates/customer_attraction/{name}.json').read_text())
    m,k=data['players'],len(data['topics'])
    clients=[set(c['topics']) for c in data['customers'] for _ in range(c.get('multiplicity',1))]
    topics=[{x for x,t in enumerate(clients) if a in t} for a in range(k)]
    sigma={tuple(t['history']):t['action'] for t in cert.get('strategy',cert)['actions']}
    histories=[h for i in range(m) for h in product(range(k),repeat=i)]
    assert set(histories)==set(sigma)
    def finish(h):
        h=tuple(h)
        while len(h)<m:h+=(sigma[h],)
        return h
    def loads(z):return [sum(a in t for a in z) for t in clients]
    def pay(z,i):
        c=loads(z)
        return sum((F(1,c[x]) for x in topics[z[i]]),F())
    checked=0; tested=0; worst=None; negative_pairs=0
    for h in histories:
        i=len(h); prescribed=finish(h);v=pay(prescribed,i)
        leaves=[finish(h+(a,)) for a in range(k)]
        d=[pay(z,i) for z in leaves]
        for a in range(k):assert v>=d[a];checked+=1
        K=[[sum((F(1,1+loads(z)[x]) for x in topics[t]),F()) for z in leaves] for t in range(k)]
        H=[[F(d[a]+d[b]-K[a][b]-K[b][a],2) for b in range(k)] for a in range(k)]
        negative_pairs+=sum(H[a][b]<0 for a in range(k) for b in range(a+1,k))
        distributions=[]
        for mask in range(1,1<<k):
            supp=[a for a in range(k) if mask>>a&1]
            distributions.append([F(1,len(supp)) if a in supp else F() for a in range(k)])
        for a,b in combinations(range(k),2):
            # p=a weight t, b weight 1-t. Test exact interior minimizer.
            aa,bb,ab=H[a][a],H[b][b],H[a][b]
            den=aa+bb-2*ab
            if den>0:
                t=(bb-ab)/den
                if 0<t<1:
                    p=[F() for _ in range(k)];p[a]=t;p[b]=1-t;distributions.append(p)
        for p in distributions:
            gap=sum((p[a]*p[b]*H[a][b] for a in range(k) for b in range(k)),F())
            tested+=1
            if worst is None or gap<worst[0]:worst=(gap,h,p,d,K,leaves)
    gap,h,p,d,K,leaves=worst
    return dict(name=name,players=m,topics=k,complete_ic_checks=checked,exact_distributions_tested=tested,negative_cross_coefficients=negative_pairs,min_gap=str(gap),witness=dict(history=h,p=list(map(str,p)),diagonal=list(map(str,d)),full_query_matrix=[[str(x) for x in row] for row in K],forced_leaves=leaves))

if __name__=='__main__':
    ans=dict(candidate=CANDIDATE,scope='Frozen full strategies only; no absence of counterexample proves the universal candidate.',arithmetic='Fraction',cases=[run(n) for n in NAMES])
    print(json.dumps(ans,indent=2))
