"""Independent exact reconstruction of the old packet and new extra-one tests.

No previous author's audit or cached desired outcome is read.  Scipy is used
only to discover LP supports; every claimed LP value has Fraction primal and
dual certificates checked against every enumerated background column.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import gzip
import hashlib
import json
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
SOURCE = ROOT/'research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/continuation/prices/packet13_source.json.gz'


def rref_solve(A, b):
    """Return particular solution, free column indices, homogeneous bases."""
    a = [[F(x) for x in row] + [F(y)] for row,y in zip(A,b)]
    n = len(A[0]); row=0; pivots=[]
    for col in range(n):
        pivot=next((j for j in range(row,len(a)) if a[j][col]),None)
        if pivot is None:continue
        a[row],a[pivot]=a[pivot],a[row]
        q=a[row][col];a[row]=[x/q for x in a[row]]
        for j in range(len(a)):
            if j!=row and a[j][col]:
                q=a[j][col];a[j]=[x-q*y for x,y in zip(a[j],a[row])]
        pivots.append(col);row+=1
    if any(not any(z[:n]) and z[n] for z in a):return None
    free=[j for j in range(n) if j not in pivots]
    particular=[F() for j in range(n)]
    for i,p in enumerate(pivots):particular[p]=a[i][n]
    basis=[]
    for f in free:
        z=[F() for j in range(n)];z[f]=F(1)
        for i,p in enumerate(pivots):z[p]=-a[i][f]
        basis.append(z)
    return particular,free,basis


def certified_minimax(M):
    """M rows are queries, columns are independently mixed backgrounds."""
    k,n=len(M),len(M[0]);mat=np.array([[float(x) for x in r] for r in M])
    # Query maximizes the worst background column.
    opt=linprog([0.]*k+[-1.],A_ub=np.column_stack((-mat.T,np.ones(n))),
                b_ub=np.zeros(n),A_eq=[[1.]*k+[0.]],b_eq=[1.],
                bounds=[(0,None)]*k+[(None,None)],method='highs')
    assert opt.success
    I=[i for i in range(k) if opt.x[i]>1e-8]
    J=[j for j in range(n) if -opt.ineqlin.marginals[j]>1e-8]
    # Recover exact query and value using every primal-supported column.
    A=[[M[i][j] for i in I]+[-1] for j in J]+[[1]*len(I)+[0]]
    sol=rref_solve(A,[0]*len(J)+[1]);assert sol and not sol[1]
    pv=sol[0];v=pv[-1];p=[F() for _ in range(k)]
    for i,z in zip(I,pv):p[i]=z
    assert sum(p)==1 and min(p)>=0
    colvalues=[sum((p[i]*M[i][j] for i in range(k)),F()) for j in range(n)]
    assert min(colvalues)>=v
    # Discover a rational mixed-background candidate, then verify it exactly.
    # This also handles degeneracy (e.g. a singleton optimal query).
    q=[F(float(-opt.ineqlin.marginals[j])).limit_denominator(10**9) for j in J]
    assert sum(q)==1 and min(q)>=0
    rowvalues=[sum((q[t]*M[i][j] for t,j in enumerate(J)),F()) for i in range(k)]
    assert max(rowvalues)<=v
    return dict(value=str(v),query=list(map(str,p)),
                background_indices=J,background_weights=list(map(str,q)),
                query_values=list(map(str,rowvalues)),
                minimum_dual_column=str(min(colvalues)),
                columns=n,query_support=I)


def counts_of(n,k):
    if k==1:yield (n,);return
    for a in range(n+1):
        for tail in counts_of(n-a,k-1):yield (a,)+tail


def main():
    data=json.loads(gzip.decompress(SOURCE.read_bytes()))
    nodes=data['nodes'];root=data['root'];k=len(data['instance']['topics'])
    m=data['instance']['players']
    customers=[]
    for c in data['instance']['customers']:
        customers.extend([frozenset(c['topics'])]*c['multiplicity'])
    targets=[None]*len(nodes)
    for j in sorted(range(len(nodes)),key=lambda j:-sum(nodes[j]['counts'])):
        node=nodes[j]
        if 'action' not in node:
            assert sum(node['counts'])==m
            targets[j]=tuple(node['counts'])
        else:
            for a,child in enumerate(node['children']):
                q=node['counts'].copy();q[a]+=1
                assert q==nodes[child]['counts']
            targets[j]=targets[node['children'][node['action']]]
    def own(a,z):
        return sum((F(1,sum(z[b] for b in C)) for C in customers if a in C),F())
    def extra(a,z):
        return sum((F(1,1+sum(z[b] for b in C)) for C in customers if a in C),F())
    comparisons=0
    for j,node in enumerate(nodes):
        if 'action' not in node:continue
        current=own(node['action'],targets[j])
        for a,child in enumerate(node['children']):
            assert current>=own(a,targets[child]);comparisons+=1
    Z=[targets[c] for c in nodes[root]['children']]
    u=own(nodes[root]['action'],targets[root])
    root_values=[own(a,Z[a]) for a in range(k)]
    assert root_values==[F(5,2)]*k
    M=[[extra(a,z) for z in Z] for a in range(k)]
    H=[[(M[a][b]+M[b][a])/2 for b in range(k)] for a in range(k)]
    # Every maximum of a quadratic on the simplex is stationary on its
    # smallest support.  Solve all 63 face stationarity systems exactly.
    faces=[];best=F(-1);best_p=None
    singular=[]
    for size in range(1,k+1):
        for I in combinations(range(k),size):
            A=[[H[a][b] for b in I]+[-1] for a in I]+[[1]*size+[0]]
            sol=rref_solve(A,[0]*size+[1])
            if sol is None:continue
            z,free,basis=sol
            assert all(v[-1]==0 for v in basis)
            value=z[-1]
            if free:
                singular.append(dict(support=I,stationary_value=str(value)))
                continue
            if min(z[:-1])<0:continue
            faces.append(dict(support=I,query=list(map(str,z[:-1])),value=str(value)))
            if value>best:
                best=value;best_p=[F() for _ in range(k)]
                for a,p in zip(I,z):best_p[a]=p
    assert all(F(z['stationary_value'])<=best for z in singular)
    assert best_p is not None
    assert sum((best_p[a]*best_p[b]*M[a][b] for a in range(k) for b in range(k)),F())==best
    half=[F() for _ in range(k)];half[2]=half[5]=F(1,2)
    halfvalue=sum((half[a]*half[b]*M[a][b] for a in range(k) for b in range(k)),F())
    menu=certified_minimax(M)
    free_counts=list(counts_of(m,k))
    freeM=[[extra(a,z) for z in free_counts] for a in range(k)]
    free=certified_minimax(freeM)
    free['backgrounds']=[free_counts[j] for j in free['background_indices']]
    menu['backgrounds']=[Z[j] for j in menu['background_indices']]
    result=dict(status='Exact finite auxiliary candidate discrimination; no general theorem',
                source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                topics=data['instance']['topics'],customers=len(customers),players=m,
                nodes=len(nodes),SPE_comparisons=comparisons,root_action=nodes[root]['action'],
                root_target=targets[root],root_utility=str(u),root_deviation_utilities=list(map(str,root_values)),root_menu=Z,
                extra_one_matrix=[[str(x) for x in row] for row in M],
                pair_TP=dict(value=str((M[2][5]+M[5][2])/2),excess=str((M[2][5]+M[5][2])/2-u),
                             forward=str(M[2][5]),backward=str(M[5][2])),
                WP_half_TP=str(halfvalue),WP_maximum=str(best),WP_maximizer=list(map(str,best_p)),
                WP_margin=str(u-best),stationary_faces=faces,singular_faces=singular,
                menu_minimax=menu,free_extra_one=free)
    (HERE/'packet_extra_one_report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('stationary_faces','singular_faces','extra_one_matrix')},indent=2))


if __name__=='__main__':main()
