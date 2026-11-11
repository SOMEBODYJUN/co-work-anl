"""Joint old-menu portfolio over the same shared-C macro, all actual sources.

The 17 old queries receive independent nonnegative weights within ONE joint
hidden minimization. Pure diagonal q,q is affine in q; no mean-squared overlap.
This contains each single-Q 76-row cone. It does not yet add Q_l,Q_m with l!=m.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from collections import defaultdict
from pathlib import Path
import hashlib,json,sys,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix,hstack as sparse_hstack
from explore_projection import features,ALL_NAMES,hidden_configs,div
from separate_master import blocks_from_columns,ORBITS,WORDS

HERE=Path(__file__).resolve().parent
NQ=17
INTERNAL=('t','b','c','j','v')
INTERNAL_NAMES=tuple(n for n in ALL_NAMES if not (n.split(':',1)[-1]=='q' or (n.startswith('pair') and 'q' in n.split(':',1)[1].split(','))))
QUERY_KINDS=('last1','last2','safeB','safeJ')+tuple(f'pair{br}:{e}' for br in (1,2) for e in INTERNAL)+('pair1:diag','pair2:diag')


def query_name(qi,kind):
    if kind.startswith('pair'):
        prefix,e=kind.split(':')
        return f'{prefix}:q{qi},'+(f'q{qi}' if e=='diag' else e)
    return f'{kind}:q{qi}'


NAMES=INTERNAL_NAMES+tuple(query_name(qi,kind) for qi in range(NQ) for kind in QUERY_KINDS)
assert len(INTERNAL_NAMES)==60 and len(QUERY_KINDS)==16 and len(NAMES)==332


def qvec(a,words,left,right,r,z):
    others=[i for i in range(6) if i not in {left,right}]
    return tuple(map(F,a+words[left]+words[right]+(r,z)))+tuple(F(sum(words[i][j] for i in others),len(others)) for j in range(3))


def visible_distribution(blocks,member,orb,source_index):
    masses=defaultdict(F);_,diag=orb;ct=6 if diag else 30
    for block in blocks:
        mass=F(block['column']['weight']);a=block['a'];words=block['words'];joint=defaultdict(lambda: defaultdict(F))
        for ci,c in block['joint']:
            ff,dd,wi,wj=c['group']
            if (ff,dd)==orb:joint[tuple(wi),tuple(wj)][tuple(c['state'])]+=F(c['weight'])
        for left in range(6):
            for right in range(6):
                if (left==right)!=bool(diag):continue
                state_masses=dict(joint[words[left],words[right]])
                state_masses[0,0]=mass-sum(state_masses.values())
                assert min(state_masses.values())>=0
                for state,w in state_masses.items():
                    if w:
                        visible=(sum(a[:source_index]),sum(a[:5]),state[member],qvec(a,words,left,right,*state))
                        masses[visible]+=w/ct
    return [(*state,w) for state,w in sorted(masses.items()) if w]


@lru_cache(None)
def hidden_arrays(p,ell,t,k):
    internals=[];alphas=[];betas=[]
    for b,c,j,v,s,ss in hidden_configs(k):
        fs,bud=features(p,ell,t,F(0),b,c,j,v,s,ss,k)
        z1,z2=p+t+s+b+c,p+c+ss+j+v
        beta1,beta2=p+t+s,p+c+ss
        bits=dict(zip(INTERNAL,(t,b,c,j,v)))
        alpha=[div(1,beta1+b+1),div(1,beta2+j+1),div(1,beta1+2),div(1,beta2+2)]
        offset=[-div(c,z1),-div(v,z2),-div(b,z1),-div(j,z2)]
        for br,bg,fst,lst,z in ((1,beta1,b,c,z1),(2,beta2,j,v,z2)):
            D=(bg+1)*(bg+2)
            for e in INTERNAL:
                val=bits[e]
                alpha.append(div(1,bg+1)-div(val,D))
                offset.append(div(val,bg+1)-div(fst,D)-div(fst+lst,z))
        for bg,fst,lst,z in ((beta1,b,c,z1),(beta2,j,v,z2)):
            D=(bg+1)*(bg+2)
            alpha.append(div(2,bg+1)-div(1,D))
            offset.append(-div(fst,D)-div(fst+lst,z))
        internals.append(tuple(fs[n] for n in INTERNAL_NAMES));alphas.append(tuple(alpha));betas.append(tuple(offset))
    return tuple(internals),tuple(alphas),tuple(betas)


def budget(k):
    _,bud=features(0,0,0,F(0),0,0,0,0,0,0,k)
    return tuple(bud[n] for n in INTERNAL_NAMES)+((0,0,0),)*(NQ*16)


@lru_cache(None)
def float_hidden_arrays(p,ell,t,k):
    return tuple(np.asarray(x,dtype=float) for x in hidden_arrays(p,ell,t,k))


def solve(visible,u,K,k):
    mats=[];count=len(hidden_configs(k));bud=budget(k)
    for p,ell,t,queries,mass in visible:
        ins,alpha,off=float_hidden_arrays(p,ell,t,k)
        queries=np.asarray(queries,dtype=float)
        qe=(alpha[:,None,:]*queries[None,:,None]+off[:,None,:]).reshape(count,NQ*16)
        mats.append(np.concatenate((ins,qe),axis=1).T)
    A=np.concatenate(mats,axis=1)
    A=np.column_stack((A,[-x[0] for x in bud]))
    rhs=[float(x[1]*u+x[2]*K) for x in bud]
    objective=np.zeros(A.shape[1]);objective[-1]=1
    eqrow=np.repeat(np.arange(len(visible)),count);eqcol=np.arange(count*len(visible))
    eq=coo_matrix((np.ones(len(eqcol)),(eqrow,eqcol)),shape=(len(visible),A.shape[1])).tocsr()
    return linprog(objective,A_ub=A,b_ub=rhs,A_eq=eq,b_eq=[float(v[-1]) for v in visible],bounds=(0,None),method='highs')


def weights_from_dual(res,maxden):
    theta={n:F(float(-x)).limit_denominator(maxden) for n,x in zip(NAMES,res.ineqlin.marginals) if x<-1e-8}
    source=theta.get('sourceT',F(0))+theta.get('sourceC',F(0))
    return {n:w/source for n,w in theta.items() if w} if source else None


def make_row(columns,blocks,member,orb,source_index,theta):
    k=6-source_index;bud=budget(k);weights=tuple(theta.get(n,F(0)) for n in NAMES)
    assert sum(weights[i]*bud[i][0] for i in range(len(NAMES)))==1
    au=sum(weights[i]*bud[i][1] for i in range(len(NAMES)))
    aK=sum(weights[i]*bud[i][2] for i in range(len(NAMES)))
    w_internal=weights[:60];w_query=tuple(weights[60+i*16:60+(i+1)*16] for i in range(NQ))
    sum_weights=tuple(sum(w_query[i][kind] for i in range(NQ)) for kind in range(16))
    @lru_cache(None)
    def psi(p,ell,t,queries):
        ins,alphas,betas=hidden_arrays(p,ell,t,k)
        weighted_queries=tuple(sum(w_query[i][kind]*queries[i] for i in range(NQ)) for kind in range(16))
        return min(sum((w*x for w,x in zip(w_internal,iv)),F(0))+
                   sum((a*q+b*w for a,b,q,w in zip(av,bv,weighted_queries,sum_weights)),F(0))
                   for iv,av,bv in zip(ins,alphas,betas))
    row=[F(0)]*len(columns);row[0]=aK;family,diag=orb;ct=6 if diag else 30
    for block in blocks:
        a,words=block['a'],block['words'];p,ell=sum(a[:source_index]),sum(a[:5]);baseline=F(0);delta=defaultdict(F)
        for left in range(6):
            for right in range(6):
                if (left==right)!=bool(diag):continue
                vals={state:psi(p,ell,state[member],qvec(a,words,left,right,*state)) for state in product((0,1),repeat=2)}
                baseline+=vals[0,0]/ct
                for state in ((0,1),(1,0),(1,1)):
                    delta[family,diag,words[left],words[right],state]+=(vals[state]-vals[0,0])/ct
        row[block['ci']]=div(a[source_index],sum(a))+au*div(a[5],sum(a))-baseline
        for ci,col in block['joint']:
            ff,dd,wi,wj=col['group']
            if (ff,dd)==orb:row[ci]=-delta[ff,dd,tuple(wi),tuple(wj),tuple(col['state'])]
    return row,au,aK,psi


def main():
    started=time.monotonic();source=Path(sys.argv[1]);sources=tuple(map(int,sys.argv[2].split(','))) if len(sys.argv)>2 else (3,2,1,0)
    raw=source.read_bytes();data=json.loads(raw);columns=data['columns'];blocks=blocks_from_columns(columns)
    actual=[sum(F(b['column']['weight'])*div(b['a'][i],sum(b['a'])) for b in blocks) for i in range(6)]
    K=F(columns[0]['weight']);u=actual[5]
    out={'scope':'Joint nonnegative weights for the 17 old queries on one shared-C macro, preserving the joint R/Z four-state mass; no SPE or half certificate.','query_menu':['A1','A2','A3','A4','A5','A6','Ti','Bi','Ci','Tj','Bj','Cj','R','Z','other_T_mean','other_B_mean','other_C_mean'],'source_path':str(source),'source_sha256':hashlib.sha256(raw).hexdigest(),'columns':len(columns),'actual_utilities':list(map(str,actual)),'K':str(K),'feature_count':len(NAMES),'feature_names':NAMES,'cuts':[],'scans':[]}
    target=HERE/f"portfolio_{data.get('verified_rows','point')}_separation.json"
    for source_index in sources:
        k=6-source_index;r=actual[source_index]
        for member in (0,1):
            for orb in ORBITS:
                visible=visible_distribution(blocks,member,orb,source_index)
                res=solve(visible,u,K,k)
                scan={'i':source_index,'k':k,'member':member,'orb':orb,'visible_states':len(visible),'hidden_per_state':len(hidden_configs(k)),'success':bool(res.success),'message':res.message}
                if res.success:scan.update({'minimum_r_float':res.fun,'gap_float':res.fun-float(r)})
                out['scans'].append(scan)
                if res.success and res.fun>float(r)+1e-9:
                    for maxden in (1000,10000,100000,1000000,10000000):
                        theta=weights_from_dual(res,maxden)
                        if theta is None:continue
                        row,au,aK,psi=make_row(columns,blocks,member,orb,source_index,theta)
                        slack=sum(F(c['weight'])*v for c,v in zip(columns,row))
                        if slack<0:
                            direct=r+au*u+aK*K-sum(w*psi(p,ell,t,queries) for p,ell,t,queries,w in visible)
                            assert direct==slack
                            cut={'i':source_index,'k':k,'member':member,'orb':orb,'weights':{n:str(w) for n,w in theta.items()},'source_weight_sum':'1','u6_coefficient':str(au),'K_coefficient':str(aK),'exact_slack':str(slack),'slack_float':float(slack),'denominator_limit':maxden,'sparse_row':[[i,str(v)] for i,v in enumerate(row) if v],'row_sha256':hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest(),'visible':[{'state':[p,ell,t,list(map(str,queries))],'mass':str(w),'minimum':str(psi(p,ell,t,queries))} for p,ell,t,queries,w in visible]}
                            out['cuts'].append(cut)
                            print(json.dumps({'i':source_index,'k':k,'member':member,'orb':orb,'slack':float(slack),'nonzero_weights':len(theta)},ensure_ascii=False),flush=True)
                            break
                out['elapsed_seconds']=time.monotonic()-started;target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
        hidden_arrays.cache_clear();float_hidden_arrays.cache_clear();features.cache_clear()
    out['elapsed_seconds']=time.monotonic()-started;target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'done':True,'scans':len(out['scans']),'cuts':len(out['cuts']),'elapsed':out['elapsed_seconds']}))


if __name__=='__main__':main()
