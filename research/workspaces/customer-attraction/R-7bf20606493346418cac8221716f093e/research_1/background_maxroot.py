"""Discover and exactly audit a five-tail / one-background maximum-topic row.

The schema uses true SPE rows only.  No frozen five-player projected row is
treated as valid in the new background.  Clients have literal membership bits
in Z,T,A,B,C,D,Q,R,S,X,Y.  Z is the fixed earlier legal topic; T is a maximum
catalog topic forced at the current (five remaining) node.  Comparators number
M=6, and their union bit cancels by sum of six union-row multipliers = 1.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,json
import numpy as np
from scipy.optimize import linprog

LABELS='ZTABCDQRSXY'
PATHS={'actual':'ABCD','root':'DQRS','second':'ADXY'}
BASE=Path(__file__).resolve().parent

def sh(n,d): return F(n,d) if n else F(0)

def value(b,tag,i):
    path=PATHS[tag]
    return sh(b[path[i]],b['Z']+b['T']+sum(b[s] for s in path))

def raw(b,o,name,M=6):
    z=name.split(':')
    if z[0]=='CAP': return F(b['T']-b[z[1]])
    if z[0]=='copy':
        i={'root':0,'second':1}[z[1]]
        return value(b,'actual',i)-value(b,z[1],i)
    if name=='union-cap': return M*b['T']-o
    tag,path=z[0],PATHS[z[0]]
    if z[1].isdigit():
        i=int(z[1]);assert i>={'actual':0,'root':1,'second':2}[tag]
        return value(b,tag,i)-sh(b[z[3]],b['Z']+b['T']+sum(b[s] for s in path[:i])+4-i)
    if z[1]=='pairO':
        p=b['Z']+b['T']+b[path[0]]+b[path[1]]
        H=value(b,tag,2)+value(b,tag,3)+sh(b[path[2]],(p+1)*(p+2))
        return F(M,2)*H+sh(p,p+1)-o
    if z[1]=='lastO':
        p=b['Z']+b['T']+sum(b[s] for s in path[:3])
        return M*value(b,tag,3)+sh(p,p+1)-o
    raise ValueError(name)

def rows():
    names=['CAP:'+s for s in 'ZABCDQRSXY']
    names+=['copy:root','copy:second']
    # All safe-floor queries against these visible legal topics are valid.
    for tag in PATHS:
        for i in range({'actual':0,'root':1,'second':2}[tag],4):
            for query in LABELS:
                names.append(f'{tag}:{i}:floor:{query}')
        names.extend([tag+':pairO',tag+':lastO'])
    names.append('union-cap')
    return names

def table():
    names=rows();states=[];mat=[];v=[];t=[];o=[]
    # Zero-union and one-union rows kept explicit: no assumption that the
    # union-row multipliers cancel is needed by the exact verifier.
    for bits in product((0,1),repeat=len(LABELS)):
        b=dict(zip(LABELS,bits));vT=sh(b['T'],b['Z']+sum(b[s] for s in 'TABCD'))
        for ox in (0,1):
            states.append((bits,ox));mat.append([raw(b,ox,n) for n in names])
            v.append(vT);t.append(F(b['T']));o.append(F(ox))
    return names,states,mat,v,t,o

def discover(C,output):
    names,states,mat,v,t,o=table()
    A=np.asarray(mat,dtype=float)
    # B*v + C*t - o - A lambda >=0, lambda>=0, B>=0.
    Aub=np.column_stack([A,-np.asarray(v,dtype=float)])
    rhs=float(C)*np.asarray(t,dtype=float)-np.asarray(o,dtype=float)
    c=np.zeros(len(names)+1);c[-1]=1
    ans=linprog(c,A_ub=Aub,b_ub=rhs,bounds=[(0,None)]*len(c),method='highs')
    assert ans.success,ans.message
    active=[i for i,x in enumerate(ans.x[:-1]) if x>1e-8]
    # Recover an exact basic solution from numerically active dual rows.
    slack=rhs-Aub@ans.x
    tight=np.flatnonzero(np.abs(slack)<1e-7)
    vars_=active+[len(names)]
    pivots={};nv=len(vars_)
    for j in tight:
        row=[mat[j][i] for i in active]+[-v[j],C*t[j]-o[j]]
        for p,old in sorted(pivots.items()):
            if row[p]:
                ratio=row[p];row=[x-ratio*y for x,y in zip(row,old)]
        p=next((i for i in range(nv) if row[i]),None)
        if p is None:
            assert not row[-1],('inconsistent exact tight rows',j,row[-1])
            continue
        ratio=row[p];row=[x/ratio for x in row]
        for q,old in list(pivots.items()):
            if old[p]:
                ratio=old[p];pivots[q]=[x-ratio*y for x,y in zip(old,row)]
        pivots[p]=row
    assert len(pivots)==nv,('nonunique active solution',len(pivots),nv)
    sol=[pivots[i][-1] for i in range(nv)]
    lam={names[i]:x for i,x in zip(active,sol[:-1])}
    B=sol[-1]
    assert B>0 and min(lam.values())>=0
    residual=[]
    for bits,ox in states:
        b=dict(zip(LABELS,bits));vt=sh(b['T'],b['Z']+sum(b[s] for s in 'TABCD'))
        residual.append(B*vt+C*b['T']-ox-sum(w*raw(b,ox,n) for n,w in lam.items()))
    assert min(residual)>=0,min(residual)
    result={'B':str(B),'C':str(C),'M':6,'scope':'Any legal fixed prefix topic Z; five remaining providers; original complete SPE at every ordered history; union of six arbitrary legal comparison topics.',
      'multipliers':{n:str(x) for n,x in lam.items()},'minimum_residual':str(min(residual)),
      'states':len(states),'positive_multipliers':len(lam),'comparison_bit_coefficient':str(sum(w for n,w in lam.items() if n.endswith('O') or n=='union-cap'))}
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--C',default='-7');ap.add_argument('--output',type=Path,default=BASE/'background_maxroot_certificate.json');args=ap.parse_args()
    discover(F(args.C),args.output)
