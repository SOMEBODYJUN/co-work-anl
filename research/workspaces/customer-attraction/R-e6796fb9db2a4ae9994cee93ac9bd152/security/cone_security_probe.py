"""Exploratory true mixed security search inside one FULL strategy cone.

Not a SPE verifier or universal proof. The strategy is a compact automaton from
the prior 13-player example. Every node is used to form its real deviation row;
we then alternate two LPs (fixed query/weights) and retain numerical candidates.
"""
from pathlib import Path
from functools import lru_cache
import gzip,json,math,argparse
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
PACKET=ROOT/'research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz'

def compositions(n,k):
    if k==1:
        yield (n,);return
    for a in range(n+1):
        for r in compositions(n-a,k-1):yield (a,)+r

def load(mode='all'):
    packet=json.load(gzip.open(PACKET,'rt'))
    n=packet['instance']['players'];k=len(packet['instance']['topics'])
    masks=np.arange(1,1<<k);bits=np.array([[(t>>a)&1 for a in range(k)]for t in masks],float)
    nodes=packet['nodes'];out=[None]*len(nodes)
    for i in sorted(range(len(nodes)),key=lambda i:-sum(nodes[i]['counts'])):
        z=nodes[i]
        out[i]=np.array(z['counts']) if z.get('terminal') else out[z['children'][z['action']]]
    lcm=math.lcm(*range(1,n+1))
    def payoffrow(a,terminal):
        loads=bits@terminal
        return np.where(bits[:,a]>0,1/np.maximum(loads,1),0)
    rows=set()
    for i,z in enumerate(nodes):
        if z.get('terminal'):continue
        base=payoffrow(z['action'],out[i])
        for a,ch in enumerate(z['children']):
            row=np.rint(lcm*(base-payoffrow(a,out[ch]))).astype(int)
            if np.any(row):rows.add(tuple(row))
    gamma=np.array(sorted(rows),float)/lcm
    if mode=='all':bg=np.array(list(compositions(n-1,k)))
    elif mode=='root':
        bg=np.array([out[ch]-np.eye(k,dtype=int)[a]for a,ch in enumerate(nodes[packet['root']]['children'])])
    elif mode=='onpath':
        backgrounds=[];i=packet['root']
        while not nodes[i].get('terminal'):
            for a,ch in enumerate(nodes[i]['children']):backgrounds.append(tuple(out[ch]-np.eye(k,dtype=int)[a]))
            i=nodes[i]['children'][nodes[i]['action']]
        bg=np.array(sorted(set(backgrounds)))
    else:raise ValueError(mode)
    loads=bg@bits.T
    # (background,type,action) pure-query payoff coefficients per type
    coeff=bits[None,:,:]/(1+loads[:,:,None])
    rootcover=(bits@out[packet['root']]>0).astype(float)
    weights=np.zeros(len(masks))
    for cust in packet['instance']['customers']:
        mask=sum(1<<a for a in cust['topics']);weights[mask-1]+=cust.get('multiplicity',1)
    weights/=weights.sum()
    return n,k,masks,gamma,coeff,rootcover,weights

def query_lp(w,coeff):
    mat=np.einsum('bta,t->ba',coeff,w)
    obj=np.r_[np.zeros(mat.shape[1]),-1]
    res=linprog(obj,A_ub=np.c_[-mat,np.ones(len(mat))],b_ub=np.zeros(len(mat)),
      A_eq=[np.r_[np.ones(mat.shape[1]),0]],b_eq=[1],bounds=[(0,None)]*mat.shape[1]+[(None,None)],method='highs')
    assert res.success,res.message
    return res.x[:-1],res.x[-1]

def cone_lp(p,n,gamma,coeff,cover):
    beta=coeff@p
    obj=np.r_[cover,-n]
    res=linprog(obj,A_ub=np.r_[np.c_[-gamma,np.zeros(len(gamma))],np.c_[-beta,np.ones(len(beta))]],
      b_ub=np.zeros(len(gamma)+len(beta)),A_eq=[np.r_[np.ones(len(cover)),0]],b_eq=[1],
      bounds=[(0,None)]*len(cover)+[(None,None)],method='highs')
    assert res.success,res.message
    return res.x[:-1],res.x[-1],-res.fun

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=['all','root','onpath'],default='all')
    parser.add_argument('--weak',action='store_true');args=parser.parse_args()
    n,k,masks,gamma,coeff,cover,w0=load(args.mode)
    factor=n-.5 if args.weak else n
    print(json.dumps({'n':n,'k':k,'cone_rows':len(gamma),'backgrounds':len(coeff),'types':len(masks)}),flush=True)
    rng=np.random.default_rng(777)
    starts=[np.ones(k)/k,query_lp(w0,coeff)[0]]+[rng.dirichlet(np.ones(k))for _ in range(14)]
    trace=[];best=None
    for start,p in enumerate(starts):
        prev=None
        for iteration in range(12):
            w,lower,margin=cone_lp(p,factor,gamma,coeff,cover)
            p,value=query_lp(w,coeff)
            gap=factor*value-cover@w
            item={'start':start,'iteration':iteration,'true_gap':gap,'cone_margin':margin,'v':value,
              'W':float(cover@w),'p':p.tolist(),'weights':[(int(m),float(x))for m,x in zip(masks,w)if x>1e-9]}
            trace.append(item)
            if best is None or gap>best['true_gap']:
                best=item;print(json.dumps(item),flush=True)
            if prev is not None and abs(gap-prev)<1e-10:break
            prev=gap
    (HERE/f'cone_security_probe_{args.mode}_{factor}.json').write_text(json.dumps({'scope':'numerical alternating LP on one fixed full strategy cone; not independently certified','best':best,'trace':trace},indent=2))
if __name__=='__main__':main()
