"""Eight original-terminal queries added to the frozen shared 616-row cone.

Original R and Z nodes query the new macro's B,C,J,V, with their own exact
backgrounds. No new query slots, third moments, or external payoff budgets.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from collections import defaultdict
import json,hashlib,time,sys
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
import cross_query_pairs_v1 as base
from separate_master import blocks_from_columns,div

HERE=Path(__file__).resolve().parent
REVERSE_NAMES=tuple(f'prior{node}:{theme}' for node in ('R','Z') for theme in ('b','c','j','v'))
NAMES=base.NAMES+REVERSE_NAMES
assert len(NAMES)==624


@lru_cache(None)
def reverse_prices(queries,orb):
    assert all(q in (0,1) for q in queries[:14])
    p3=sum(queries[:3]);p4=sum(queries[:4]);r,z=queries[12:14]
    second=queries[10] if orb[0]==0 else queries[11]
    betaR=p3+queries[6]+second;betaZ=p4+r
    return (div(1,betaR+1),div(r,betaR+r),div(1,betaZ+1),div(z,betaZ+z))


@lru_cache(None)
def hidden_bits(k):return tuple(tuple(map(F,h[:4])) for h in base.hidden_configs(k))


def budget(k):return base.budget(k)+((0,0,0),)*8


def feature_vector(p,ell,t,queries,moments,hi,k,orb):
    internal,alpha,offset=base.old.hidden_arrays(p,ell,t,k)
    single=tuple(a*q+b for q in queries for a,b in zip(alpha[hi],offset[hi]))
    pairs=base.pair_values(queries,moments,5 if orb[1] else 4)
    coefficients=base.hidden_pair_coefficients(p,t,k)[hi]
    pairfeatures=tuple(coefficients[3*branch]*sm+coefficients[3*branch+1]*rho+coefficients[3*branch+2] for branch in range(2) for sm,rho in pairs)
    aR,payR,aZ,payZ=reverse_prices(queries,orb)
    reverse=tuple(a*bit-pay for a,pay in ((aR,payR),(aZ,payZ)) for bit in hidden_bits(k)[hi])
    return internal[hi]+single+pairfeatures+reverse


def solve(visible,u,K,k,orb):
    count=len(base.hidden_configs(k));d=5 if orb[1] else 4;mats=[];bud=budget(k);bits=np.asarray(hidden_bits(k),dtype=float)
    for p,ell,t,queries,moments,mass in visible:
        ins,alpha,off=base.old.float_hidden_arrays(p,ell,t,k);q=np.asarray(queries,dtype=float)
        single=(alpha[:,None,:]*q[None,:,None]+off[:,None,:]).reshape(count,17*16)
        pairs=np.asarray(base.pair_values(queries,moments,d),dtype=float)
        coefficients=np.asarray(base.hidden_pair_coefficients(p,t,k),dtype=float).reshape(count,2,3)
        extra=[coefficients[:,br,0,None]*pairs[None,:,0]+coefficients[:,br,1,None]*pairs[None,:,1]+coefficients[:,br,2,None] for br in range(2)]
        aR,payR,aZ,payZ=map(float,reverse_prices(queries,orb))
        reverse=np.concatenate((aR*bits-payR,aZ*bits-payZ),axis=1)
        mats.append(np.concatenate((ins,single,*extra,reverse),axis=1).T)
    A=np.concatenate(mats,axis=1);A=np.column_stack((A,[-b[0] for b in bud]))
    objective=np.zeros(A.shape[1]);objective[-1]=1
    erow=np.repeat(np.arange(len(visible)),count);ecol=np.arange(count*len(visible))
    eq=coo_matrix((np.ones(len(ecol)),(erow,ecol)),shape=(len(visible),A.shape[1])).tocsr()
    return linprog(objective,A_ub=A,b_ub=[float(b[1]*u+b[2]*K) for b in bud],A_eq=eq,b_eq=[float(v[-1]) for v in visible],bounds=(0,None),method='highs')


def make_row(columns,blocks,member,orb,source_index,theta):
    k=6-source_index;d=5 if orb[1] else 4;bud=budget(k);weights=tuple(theta.get(name,F(0)) for name in NAMES)
    assert sum(w*b[0] for w,b in zip(weights,bud))==1
    au=sum(w*b[1] for w,b in zip(weights,bud));aK=sum(w*b[2] for w,b in zip(weights,bud))
    wi=weights[:60];wq=tuple(weights[60+i*16:60+(i+1)*16] for i in range(17));wqs=tuple(sum(wq[i][kind] for i in range(17)) for kind in range(16))
    wp=(weights[332:474],weights[474:616]);wps=tuple(sum(v) for v in wp);wr=weights[616:620];wz=weights[620:624]
    @lru_cache(None)
    def psi(p,ell,t,queries,moments):
        ins,alpha,offset=base.old.hidden_arrays(p,ell,t,k)
        weighted_q=tuple(sum(wq[i][kind]*queries[i] for i in range(17)) for kind in range(16))
        pairs=base.pair_values(queries,moments,d)
        sums=tuple(sum(w*pairs[i][0] for i,w in enumerate(wb)) for wb in wp)
        overlaps=tuple(sum(w*pairs[i][1] for i,w in enumerate(wb)) for wb in wp)
        aR,payR,aZ,payZ=reverse_prices(queries,orb)
        values=[]
        for iv,av,bv,pv,bits in zip(ins,alpha,offset,base.hidden_pair_coefficients(p,t,k),hidden_bits(k)):
            value=sum((w*x for w,x in zip(wi,iv)),F(0))+sum((a*q+b*w for a,b,q,w in zip(av,bv,weighted_q,wqs)),F(0))
            value+=sum(pv[3*br]*sums[br]+pv[3*br+1]*overlaps[br]+pv[3*br+2]*wps[br] for br in range(2))
            value+=aR*sum(w*x for w,x in zip(wr,bits))-payR*sum(wr)+aZ*sum(w*x for w,x in zip(wz,bits))-payZ*sum(wz)
            values.append(value)
        return min(values)
    row=[F(0)]*len(columns);row[0]=aK;family,diag=orb;ct=6 if diag else 30
    for block in blocks:
        a,words=block['a'],block['words'];p,ell=sum(a[:source_index]),sum(a[:5]);baseline=F(0);delta=defaultdict(F)
        for left in range(6):
            for right in range(6):
                if (left==right)!=bool(diag):continue
                values={}
                for state in product((0,1),repeat=2):
                    queries,moments=base.queries_and_moments(a,words,left,right,*state)
                    values[state]=psi(p,ell,state[member],queries,moments)
                baseline+=values[0,0]/ct
                for state in ((0,1),(1,0),(1,1)):delta[family,diag,words[left],words[right],state]+=(values[state]-values[0,0])/ct
        row[block['ci']]=div(a[source_index],sum(a))+au*div(a[5],sum(a))-baseline
        for ci,column in block['joint']:
            ff,dd,wl,wr0=column['group']
            if (ff,dd)==orb:row[ci]=-delta[ff,dd,tuple(wl),tuple(wr0),tuple(column['state'])]
    return row,au,aK,psi


def rational_weights(res,grid):
    integers={name:round(max(0.,-float(value))*grid) for name,value in zip(NAMES,res.ineqlin.marginals)}
    source=integers['sourceT']+integers['sourceC'];assert source>0
    return {name:F(value,source) for name,value in integers.items() if value},source


def main():
    start=time.monotonic();source=Path(sys.argv[1]) if len(sys.argv)>1 else HERE.parent/'master_cuts/dynamic_5786_exact.json'
    raw=source.read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha=='6927af3bda45a12a36885d949b7690fbd4f24c5938618e1e6a81cb4a7d71ed27'
    data=json.loads(raw);columns=data['columns'];blocks=blocks_from_columns(columns)
    actual=[sum(F(b['column']['weight'])*div(b['a'][i],sum(b['a'])) for b in blocks) for i in range(6)];u=actual[5];K=F(columns[0]['weight']);i=3;member=0;orb=(0,0);k=3
    visible=base.visible_distribution(blocks,member,orb,i);oldres=base.solve(visible,u,K,k,4);res=solve(visible,u,K,k,orb)
    out={'scope':'One actual4/R/orb00 structure, eight original-terminal R/Z queries of macro B/C/J/V added to the existing616. No new query slot or third moment.','source_path':str(source),'source_sha256':sha,'columns':len(columns),'i':i,'k':k,'member':member,'orb':orb,'query_menu':base.QUERY_MENU,'feature_count':len(NAMES),'feature_names':NAMES,'actual_utilities':list(map(str,actual)),'K':str(K),'old616':{'success':bool(oldres.success),'message':oldres.message},'new624':{'success':bool(res.success),'message':res.message},'cuts':[]}
    if oldres.success:out['old616'].update({'minimum_r_float':oldres.fun,'gap_float':oldres.fun-float(actual[i])})
    if res.success:out['new624'].update({'minimum_r_float':res.fun,'gap_float':res.fun-float(actual[i])})
    if res.success and res.fun>float(actual[i])+1e-9:
        for grid in (10**5,10**6,10**7,10**8,10**9):
            theta,den=rational_weights(res,grid);row,au,aK,psi=make_row(columns,blocks,member,orb,i,theta)
            slack=sum(F(c['weight'])*value for c,value in zip(columns,row))
            if slack>=0 or -float(slack)<0.99*out['new624']['gap_float']:continue
            assert slack==actual[i]+au*u+aK*K-sum(mass*psi(p,ell,t,qs,mu) for p,ell,t,qs,mu,mass in visible)
            cut={'i':i,'k':k,'member':member,'orb':orb,'weights':{name:str(w) for name,w in theta.items()},'new_reverse_weights':{name:str(theta[name]) for name in REVERSE_NAMES if name in theta},'source_weight_sum':'1','u6_coefficient':str(au),'K_coefficient':str(aK),'common_denominator':den,'rounding_grid':grid,'exact_slack':str(slack),'slack_float':float(slack),'sparse_row':[[ci,str(value)] for ci,value in enumerate(row) if value],'row_sha256':hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest(),'visible':[{'state':[p,ell,t,list(map(str,qs)),list(map(str,mu))],'mass':str(mass),'minimum':str(psi(p,ell,t,qs,mu))} for p,ell,t,qs,mu,mass in visible]}
            out['cuts'].append(cut);break
    out['elapsed_seconds']=time.monotonic()-start;target=HERE/'reverse_terminal_5786_one_v1.json';target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'old616':out['old616'],'new624':out['new624'],'cuts':len(out['cuts']),'new_reverse_weights':out['cuts'][0]['new_reverse_weights'] if out['cuts'] else {},'exact_slack':out['cuts'][0]['slack_float'] if out['cuts'] else None,'elapsed_seconds':out['elapsed_seconds']},ensure_ascii=False))


if __name__=='__main__':main()
