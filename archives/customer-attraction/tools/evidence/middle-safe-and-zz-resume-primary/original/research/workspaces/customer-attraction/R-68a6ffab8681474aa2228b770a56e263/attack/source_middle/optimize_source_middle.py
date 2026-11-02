"""Optimize a valid local source projection on one frozen necessary point.

This is a cut diagnostic. The input has no full SPE realization.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import json, argparse
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
POINT=ROOT/'research/workspaces/customer-attraction/R-a241704002304c95bca9ef95d516b61f/solo_six/source_requery_exact.json'
PAT=tuple(product((0,1),repeat=3))
QUERY=['Ti','Bi','Ci','Yj','R']+['A'+str(i+1) for i in range(6)]

def share(n,d): return F(n,d) if n else F()

def configs(data,family):
    configs=defaultdict(F);u=[F() for _ in range(6)]
    for atom in data['atoms']:
        hi=atom['hist_index'];h=data['histograms'][hi]
        a=tuple(map(int,h['actual_bits']));weight=F(atom['weight'])
        for i in range(6):u[i]+=weight*share(a[i],sum(a))
        words=[w for w,n in zip(PAT,h['hist']) for _ in range(n)]
        groups={(g[0],g[1],tuple(g[2]),tuple(g[3])):k for k,g in enumerate(data['groups'][hi])}
        for i,j in product(range(6),repeat=2):
            fam=int(family.startswith('C'))
            if family.endswith('off') and i==j:continue
            if family.endswith('diag') and i!=j:continue
            r=atom['R'][groups[fam,int(i==j),words[i],words[j]]]
            q=(*words[i],words[j][1+fam],r,*a)
            configs[a,r,q]+=weight
    return configs,u

def make_g(a,r,q,source,y,names):
    b=sum(a[:source-1]);k=7-source;s=sum(y);den=b+r+s
    vals=[]
    for kind,l,x in names:
        if kind=='capacity':v=F(y[l])
        elif kind=='price':v=share(y[l],sum(a[:x])+6-x)
        else:
            d=b+r+sum(y[:l])+k-l-1
            v=-share(y[l],den)+share(q[x],d)
        vals.append(v)
    return share(r,den),vals

def optimize(data,source,family,middle=True):
    cs,u=configs(data,family);k=7-source;nidx=6 if family.endswith('diag') else 30
    names=[]
    for l in range(k-1):
        names += [('capacity',l,-1)]+[('price',l,i) for i in range(6)]
        if middle or l==k-2:names += [('safe',l,x) for x in range(len(QUERY))]
    names=tuple(names);nv=len(names);cost=[]
    for kind,l,x in names:cost.append(nidx*(F(data['K']) if kind=='capacity' else u[x] if kind=='price' else F()))
    rr=[];cc=[];vv=[];rhs=[]
    for h,(cfg,mass) in enumerate(cs.items()):
        a,r,q=cfg
        for y in product((0,1),repeat=k-1):
            base,vals=make_g(a,r,q,source,y,names);row=len(rhs);rhs.append(float(base))
            rr.append(row);cc.append(nv+h);vv.append(1.)
            for j,v in enumerate(vals):
                if v:rr.append(row);cc.append(j);vv.append(-float(v))
    A=coo_matrix((vv,(rr,cc)),shape=(len(rhs),nv+len(cs))).tocsr()
    obj=[float(x) for x in cost]+[-float(x) for x in cs.values()]
    sol=linprog(obj,A_ub=A,b_ub=rhs,bounds=[(0,32)]*nv+[(None,None)]*len(cs),method='highs')
    if not sol.success: return {'status':sol.message}
    weights=[F(float(x)).limit_denominator(100000) for x in sol.x[:nv]]
    lhs=nidx*u[source-1]+sum(c*w for c,w in zip(cost,weights))
    rhs=F()
    for (a,r,q),mass in cs.items():
        vals=[]
        for y in product((0,1),repeat=k-1):
            base,row=make_g(a,r,q,source,y,names);vals.append(base+sum(v*w for v,w in zip(row,weights)))
        rhs+=mass*min(vals)
    return {'source':source,'family':family,'include_middle_safe':middle,'configurations':len(cs),
            'scope':'exact projected cut evaluation at frozen necessary point, not SPE or half certificate',
            'lambda_source':'1','parameter_bound':32,'lhs':str(lhs),'rhs':str(rhs),'slack':str(lhs-rhs),'slack_float':float(lhs-rhs),
            'parameters':[{'kind':n[0],'tail_position':n[1]+1,'query':QUERY[n[2]] if n[0]=='safe' else n[2]+1 if n[0]=='price' else None,'weight':str(w)} for n,w in zip(names,weights) if w]}

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=int,default=4);p.add_argument('--family',default='B-off');args=p.parse_args()
    data=json.loads(POINT.read_text());out={'with_middle':optimize(data,args.source,args.family,True),'terminal_only':optimize(data,args.source,args.family,False)}
    target=HERE/f'cut_source{args.source}_{args.family}.json';target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
