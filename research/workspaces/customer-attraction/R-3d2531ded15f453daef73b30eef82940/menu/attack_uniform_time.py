"""Attack the exact general candidate sum_i min_A g_p(Z_i(A)) <= W.

A finite diagnostic over complete ordered-history policy cones. Customers vary
on every nonempty interest type. No discovery or negative output is a theorem.
"""
from pathlib import Path
import sys,json
from functools import lru_cache
from itertools import product
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance
from customer_attraction.certificate import StrategyCertificate,verify_certificate


def cone(m,k,actions):
    masks=np.arange(1,1<<k)
    inc=np.array([[(int(mask)>>a)&1 for a in range(k)] for mask in masks],float)
    @lru_cache(None)
    def terminal(h):
        return h if len(h)==m else terminal(h+(actions[h],))
    def utility(z,i):
        c=inc[:,z].sum(axis=1)
        return inc[:,z[i]]/np.where(c,c,1)
    gamma=[]
    for d in range(m):
        for h in product(range(k),repeat=d):
            act=terminal(h)
            for a in range(k):
                gamma.append(utility(act,d)-utility(terminal(h+(a,)),d))
    z=terminal(())
    W=(inc[:,z].sum(axis=1)>0).astype(float)
    K=np.array([[inc.T/(1+inc[:,terminal(z[:i]+(a,))].sum(axis=1))
                 for a in range(k)] for i in range(m)])
    return np.array(gamma),W,K,z


def weights_lp(gamma,W,K,p):
    m,k,_,n=K.shape
    rows=[np.r_[-g,np.zeros(m)] for g in gamma]
    vals=np.einsum('iaqn,q->ian',K,p)
    for i in range(m):
        for a in range(k):
            r=np.r_[-vals[i,a],np.zeros(m)];r[n+i]=1;rows.append(r)
    return linprog(np.r_[np.zeros(n),-np.ones(m)],A_ub=rows,b_ub=np.zeros(len(rows)),
                   A_eq=[np.r_[W,np.zeros(m)]],b_eq=[1],bounds=[(0,None)]*(n+m),method='highs')


def query_lp(K,w):
    m,k,_,n=K.shape
    vals=K@w
    rows=[]
    for i in range(m):
        for a in range(k):
            r=np.r_[-vals[i,a],np.zeros(m)];r[k+i]=1;rows.append(r)
    return linprog(np.r_[np.zeros(k),-np.ones(m)],A_ub=rows,b_ub=np.zeros(len(rows)),
                   A_eq=[np.r_[np.ones(k),np.zeros(m)]],b_eq=[1],bounds=[(0,None)]*(k+m),method='highs')


def main():
    rng=np.random.default_rng(31023)
    # Distinct policies, not more fixed-player theorem tasks. Every LP attacks
    # the same all-m/all-catalog candidate written in the module docstring.
    names=['individual_security_failure','local_security_increment',
           'eight_cce_welfare_gap','root_stationary_kernel','dynamic_iid_local',
           'fractional_actual_load_failure']
    report=[]
    for name in names:
        inst=Instance.from_dict(json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text()))
        raw=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
        cert=StrategyCertificate.from_dict(raw.get('strategy',raw.get('certificate',raw)))
        ck=verify_certificate(inst,cert)
        if not ck.valid: raise ValueError(name)
        gamma,W,K,z=cone(inst.players,inst.topic_count,cert.actions)
        m,k,_,n=K.shape
        best=None
        for start in range(25):
            p=np.ones(k)/k if start==0 else rng.dirichlet(np.ones(k)*rng.choice([.1,1,10]))
            prior=-np.inf
            for step in range(15):
                sol=weights_lp(gamma,W,K,p)
                if not sol.success: raise RuntimeError(sol.message)
                w=sol.x[:n]
                qsol=query_lp(K,w)
                if not qsol.success: raise RuntimeError(qsol.message)
                p=qsol.x[:k]
                val=-qsol.fun-1
                if best is None or val>best['gap']:
                    best={'gap':float(val),'query':p.tolist(),
                          'weights':{str(i+1):float(v) for i,v in enumerate(w) if v>1e-10},
                          'start':start,'step':step}
                if val>1e-7: break
                if val<prior+1e-10: break
                prior=val
            if best['gap']>1e-7: break
        item={'name':name,'m':m,'k':k,'actual':z,'best':best,
              'status':'numerical separation requiring exact audit' if best['gap']>1e-7 else 'no separation in this finite cone attack'}
        report.append(item)
        print(json.dumps(item),flush=True)
        Path(__file__).with_name('uniform_time_attack.json').write_text(json.dumps({'candidate':'sum_i min_A g_p(Z_i(A)) <= W for all p','scope':'finite complete policy-cone alternating LP diagnostic; no universal conclusion','results':report},indent=2)+'\n')
if __name__=='__main__':main()
