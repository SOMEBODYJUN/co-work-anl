"""616-row shared-C cone with exact distinct-old-query PAIR couplings.

The three remaining-family means retain their TB/TC/BC same-index moments.
Both same and off couplings are explicit; independent draws are their mixture.
Existing frozen generators are imported read-only.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from collections import defaultdict
import hashlib,json,sys,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
import portfolio_master as old
from explore_projection import features,hidden_configs,div
from separate_master import blocks_from_columns,ORBITS

HERE=Path(__file__).resolve().parent
PAIR_CONFIGS=tuple((i,j,mode) for i in range(17) for j in range(i+1,17)
                   for mode in (('same','off') if i>=14 else ('product',)))+tuple((i,i,'off') for i in range(14,17))
assert len(PAIR_CONFIGS)==142
EXTRA_NAMES=tuple(f'oldpair{br}:{i},{j}:{mode}' for br in (1,2) for i,j,mode in PAIR_CONFIGS)
NAMES=old.NAMES+EXTRA_NAMES
assert len(NAMES)==616
QUERY_MENU=['A1','A2','A3','A4','A5','A6','Ti','Bi','Ci','Tj','Bj','Cj','R','Z','other_T_mean','other_B_mean','other_C_mean']
MOMENT_PAIRS=((0,1),(0,2),(1,2))


def queries_and_moments(a,words,left,right,r,z):
    rest=[i for i in range(6) if i not in {left,right}];d=len(rest)
    queries=old.qvec(a,words,left,right,r,z)
    moments=tuple(F(sum(words[i][f]*words[i][g] for i in rest),d) for f,g in MOMENT_PAIRS)
    return queries,moments


@lru_cache(None)
def pair_values(queries,moments,d):
    assert d in (4,5) and all(q in (0,1) for q in queries[:14])
    moments_map=dict(zip(MOMENT_PAIRS,moments));out=[]
    for left,right,mode in PAIR_CONFIGS:
        ql,qr=queries[left],queries[right]
        if mode=='product':
            assert left<14
            rho=ql*qr
        else:
            assert left>=14
            f,g=left-14,right-14
            same=ql if f==g else moments_map[f,g]
            rho=same if mode=='same' else (d*ql*qr-same)/(d-1)
        assert rho>=0 and rho<=min(ql,qr)
        out.append((ql+qr,rho))
    return tuple(out)


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
                sm=dict(joint[words[left],words[right]]);sm[0,0]=mass-sum(sm.values());assert min(sm.values())>=0
                for state,w in sm.items():
                    if not w:continue
                    queries,moments=queries_and_moments(a,words,left,right,*state)
                    key=(sum(a[:source_index]),sum(a[:5]),state[member],queries,moments)
                    masses[key]+=w/ct
    return [(*key,w) for key,w in sorted(masses.items()) if w]


@lru_cache(None)
def hidden_pair_coefficients(p,t,k):
    out=[]
    for b,c,j,v,s,ss in hidden_configs(k):
        row=[]
        for bg,d,e in ((p+t+s,b,c),(p+c+ss,j,v)):
            denominator=(bg+1)*(bg+2)
            row.extend((div(1,bg+1),-div(1,denominator),-div(d,denominator)-div(d+e,bg+d+e)))
        out.append(tuple(row))
    return tuple(out)


def budget(k):return old.budget(k)+((0,0,0),)*284


def solve(visible,u,K,k,d):
    count=len(hidden_configs(k));mats=[];bud=budget(k)
    for p,ell,t,queries,moments,mass in visible:
        ins,alpha,off=old.float_hidden_arrays(p,ell,t,k);q=np.asarray(queries,dtype=float)
        single=(alpha[:,None,:]*q[None,:,None]+off[:,None,:]).reshape(count,17*16)
        pairs=np.asarray(pair_values(queries,moments,d),dtype=float)
        coeff=np.asarray(hidden_pair_coefficients(p,t,k),dtype=float).reshape(count,2,3)
        extra=[]
        for br in range(2):
            extra.append(coeff[:,br,0,None]*pairs[None,:,0]+coeff[:,br,1,None]*pairs[None,:,1]+coeff[:,br,2,None])
        mats.append(np.concatenate((ins,single,*extra),axis=1).T)
    A=np.concatenate(mats,axis=1);A=np.column_stack((A,[-x[0] for x in bud]))
    objective=np.zeros(A.shape[1]);objective[-1]=1
    eqrow=np.repeat(np.arange(len(visible)),count);eqcol=np.arange(count*len(visible))
    eq=coo_matrix((np.ones(len(eqcol)),(eqrow,eqcol)),shape=(len(visible),A.shape[1])).tocsr()
    return linprog(objective,A_ub=A,b_ub=[float(x[1]*u+x[2]*K) for x in bud],A_eq=eq,b_eq=[float(v[-1]) for v in visible],bounds=(0,None),method='highs')


def weights_from_dual(res,maxden):
    theta={n:F(float(-x)).limit_denominator(maxden) for n,x in zip(NAMES,res.ineqlin.marginals) if x<-1e-8}
    source=theta.get('sourceT',F(0))+theta.get('sourceC',F(0))
    return {n:w/source for n,w in theta.items() if w} if source else None


def make_row(columns,blocks,member,orb,source_index,theta):
    k=6-source_index;d=5 if orb[1] else 4;bud=budget(k);weights=tuple(theta.get(n,F(0)) for n in NAMES)
    assert sum(weights[i]*bud[i][0] for i in range(len(NAMES)))==1
    au=sum(weights[i]*bud[i][1] for i in range(len(NAMES)));aK=sum(weights[i]*bud[i][2] for i in range(len(NAMES)))
    wi=weights[:60];wq=tuple(weights[60+i*16:60+(i+1)*16] for i in range(17));wqs=tuple(sum(wq[i][kind] for i in range(17)) for kind in range(16))
    we=(weights[332:474],weights[474:616]);wes=tuple(sum(v) for v in we)
    @lru_cache(None)
    def psi(p,ell,t,queries,moments):
        ins,alphas,betas=old.hidden_arrays(p,ell,t,k)
        weighted_q=tuple(sum(wq[i][kind]*queries[i] for i in range(17)) for kind in range(16))
        pairvals=pair_values(queries,moments,d)
        xsum=tuple(sum(w*pairvals[i][0] for i,w in enumerate(wb)) for wb in we)
        rsum=tuple(sum(w*pairvals[i][1] for i,w in enumerate(wb)) for wb in we)
        vals=[]
        for iv,av,bv,pv in zip(ins,alphas,betas,hidden_pair_coefficients(p,t,k)):
            val=sum((w*x for w,x in zip(wi,iv)),F(0))+sum((a*q+b*w for a,b,q,w in zip(av,bv,weighted_q,wqs)),F(0))
            val+=sum(pv[3*br]*xsum[br]+pv[3*br+1]*rsum[br]+pv[3*br+2]*wes[br] for br in range(2))
            vals.append(val)
        return min(vals)
    row=[F(0)]*len(columns);row[0]=aK;family,diag=orb;ct=6 if diag else 30
    for block in blocks:
        a,words=block['a'],block['words'];p,ell=sum(a[:source_index]),sum(a[:5]);baseline=F(0);delta=defaultdict(F)
        for left in range(6):
            for right in range(6):
                if (left==right)!=bool(diag):continue
                vals={}
                for state in product((0,1),repeat=2):
                    queries,moments=queries_and_moments(a,words,left,right,*state)
                    vals[state]=psi(p,ell,state[member],queries,moments)
                baseline+=vals[0,0]/ct
                for state in ((0,1),(1,0),(1,1)):
                    delta[family,diag,words[left],words[right],state]+=(vals[state]-vals[0,0])/ct
        row[block['ci']]=div(a[source_index],sum(a))+au*div(a[5],sum(a))-baseline
        for ci,col in block['joint']:
            ff,dd,wl,wr=col['group']
            if (ff,dd)==orb:row[ci]=-delta[ff,dd,tuple(wl),tuple(wr),tuple(col['state'])]
    return row,au,aK,psi


def main():
    start=time.monotonic();source=Path(sys.argv[1]);sources=tuple(map(int,sys.argv[2].split(','))) if len(sys.argv)>2 else (3,2,1,0)
    raw=source.read_bytes();data=json.loads(raw);columns=data['columns'];blocks=blocks_from_columns(columns)
    actual=[sum(F(b['column']['weight'])*div(b['a'][i],sum(b['a'])) for b in blocks) for i in range(6)];K=F(columns[0]['weight']);u=actual[5]
    out={'scope':'616 nonnegative true-row features, with exact same/off old-query couplings and shared C. Fixed necessary-point separation only.','source_path':str(source),'source_sha256':hashlib.sha256(raw).hexdigest(),'columns':len(columns),'query_menu':QUERY_MENU,'feature_count':616,'feature_names':NAMES,'extra_pair_configurations':[{'left':i,'right':j,'coupling':m} for i,j,m in PAIR_CONFIGS],'actual_utilities':list(map(str,actual)),'K':str(K),'scans':[],'cuts':[]}
    target=HERE/f"cross_pairs_{data.get('verified_rows','point')}_v1_separation.json"
    for source_index in sources:
        k=6-source_index;r=actual[source_index]
        for member in (0,1):
            for orb in ORBITS:
                d=5 if orb[1] else 4;visible=visible_distribution(blocks,member,orb,source_index);res=solve(visible,u,K,k,d)
                scan={'i':source_index,'k':k,'member':member,'orb':orb,'visible_states':len(visible),'hidden_per_state':len(hidden_configs(k)),'success':bool(res.success),'message':res.message}
                if res.success:scan.update({'minimum_r_float':res.fun,'gap_float':res.fun-float(r)})
                out['scans'].append(scan)
                if res.success and res.fun>float(r)+1e-9:
                    for maxden in (1000,10000,100000,1000000,10000000):
                        theta=weights_from_dual(res,maxden)
                        if theta is None:continue
                        row,au,aK,psi=make_row(columns,blocks,member,orb,source_index,theta);slack=sum(F(c['weight'])*v for c,v in zip(columns,row))
                        if slack<0:
                            direct=r+au*u+aK*K-sum(w*psi(p,ell,t,qs,mom) for p,ell,t,qs,mom,w in visible);assert direct==slack
                            cut={'i':source_index,'k':k,'member':member,'orb':orb,'weights':{n:str(w) for n,w in theta.items()},'source_weight_sum':'1','u6_coefficient':str(au),'K_coefficient':str(aK),'exact_slack':str(slack),'slack_float':float(slack),'uses_new_cross_pair':any(n.startswith('oldpair') for n in theta),'denominator_limit':maxden,'sparse_row':[[i,str(v)] for i,v in enumerate(row) if v],'row_sha256':hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest(),'visible':[{'state':[p,ell,t,list(map(str,qs)),list(map(str,mom))],'mass':str(w),'minimum':str(psi(p,ell,t,qs,mom))} for p,ell,t,qs,mom,w in visible]}
                            out['cuts'].append(cut);print(json.dumps({'i':source_index,'k':k,'member':member,'orb':orb,'slack':float(slack),'uses_new_cross_pair':cut['uses_new_cross_pair'],'weights':len(theta)}),flush=True);break
                out['elapsed_seconds']=time.monotonic()-start;target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
        old.hidden_arrays.cache_clear();old.float_hidden_arrays.cache_clear();features.cache_clear();hidden_pair_coefficients.cache_clear();pair_values.cache_clear()
    out['elapsed_seconds']=time.monotonic()-start;target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'done':True,'scans':len(out['scans']),'cuts':len(out['cuts']),'elapsed':out['elapsed_seconds']}))


if __name__=='__main__':main()
