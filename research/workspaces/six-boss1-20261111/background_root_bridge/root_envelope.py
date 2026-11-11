"""Six real root deviations, charged five-tail certificates, common actual price.

Independent new output directory. Frozen background_five_bridge files are read
only. Small LP discovery optimizes the complete scalar envelope family at one
given necessary point; it does not solve any SPE-realizability problem.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,hashlib,argparse
import numpy as np
from scipy.optimize import linprog

OUT=Path(__file__).resolve().parent;RUN=OUT.parent;OLD=RUN/'background_five_bridge'
EPS=F(62212762317811658581,1250000000000000000000)
KAP=F(226487,10**21)
def q(n,d):return F(n,d) if n else F(0)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())

def input_data(filename,expected):
    path=RUN/filename;a=load(path);assert sha(path)==expected
    hist=[x for x in a['columns'] if x['kind']=='hist'];K=F(a['columns'][0]['weight'])
    rows={}
    for b in (0,1):
        r=load(OLD/f'fixed53_b{b}_profit.json')
        rows.update({(b,x['actual'],x['d']):F(x['min_rho']) for x in r['min_by_actual_and_d']})
    bycount={(b,c,d):min(v for (bb,e,dd),v in rows.items() if bb==b and sum(map(int,e))==c and dd==d)
             for b in (0,1) for c in range(6) for d in range(6)}
    u=[sum(F(x['weight'])*q(int(x['actual_bits'][i]),sum(map(int,x['actual_bits']))) for x in hist) for i in range(6)]
    assert sum(u)==F(a['W'])
    mass=defaultdict(F)
    zmiss=F(0);avgr=F(0);avgres=F(0);debt=F(0)
    for x in hist:
        w=F(x['weight']);bits=x['actual_bits'];b=int(bits[0]);e=bits[1:];d=x['d'];ell=sum(map(int,bits[:5]))
        mass[ell,d]+=w
        if bits=='100000':zmiss+=w
        avgR=(F(6-d,6)*q(d,b+d)+F(d,6)*q(d-1,b+d-1)) if d else F(0)
        avgm=(F(6-d,6)*rows[b,e,d] if d<6 else 0)+(F(d,6)*rows[b,e,d-1] if d else 0)
        avgr+=w*avgR;avgres+=w*avgm;debt+=w*(int(d>0)-avgR)
    diag={'input':filename,'input_sha256':sha(path),'not_an_SPE':True,'W':a['W'],'K':str(K),
          'u':[str(v) for v in u],'first_exclusive_mass':str(zmiss),'average_five_profit':str(avgr),
          'average_five_remainder':str(avgres),'six_omission_debt':str(debt),
          'charged_row_slack':str(2*sum(u[1:])+EPS*zmiss-avgr),
          'refined_row_slack':str(2*sum(u[1:])-avgr-avgres-KAP*K)}
    return a,hist,K,u,mass,rows,bycount,diag

def envelope_lp(K,u,mass,bycount,kind,capacity=True):
    # Scalar alpha (actual-last price), gamma (five-tail certificate), eta
    # (per-topic size cap). Source root-IC coefficient is exactly one.
    states=sorted({(ell,d,t) for ell,d in mass for t in (0,1) if (d if t else 6-d)>0})
    count=3+len(states);A=[];B=[];metadata=[]
    c=np.zeros(count);c[0]=5*float(u[5]);c[1]=-float(KAP*K) if kind=='refined' else 0;c[2]=5*float(K)
    for n,(ell,d,t) in enumerate(states):
        p=F(d if t else 6-d,6);weight=mass[ell,d]*p;c[3+n]=-float(weight)
        # The benchmark term gamma*(d-t)/d is placed outside the minimum.
        c[1]-=float(weight*q(d-t,d))
        for z in range(6):
            penalty=bycount[t,z,d-t] if kind=='refined' else -EPS*t*int(z==0)
            gamma_co=q(-2*z,t+z)+penalty
            alpha_co=F(z,ell+1);eta_co=F(z);source=q(t,t+z)
            row=np.zeros(count);row[0]=-float(alpha_co);row[1]=-float(gamma_co);row[2]=-float(eta_co);row[3+n]=1
            A.append(row);B.append(float(source));metadata.append({'state':[ell,d,t],'z':z,'alpha':str(alpha_co),'gamma':str(gamma_co),'eta':str(eta_co),'source':str(source)})
    bounds=[(0,None),(0,None),(0,None) if capacity else (0,0)]+[(None,None)]*len(states)
    res=linprog(c,A_ub=np.asarray(A),b_ub=np.asarray(B),bounds=bounds,method='highs')
    assert res.success,res.message
    pars=[F(float(v)).limit_denominator(10**9) for v in res.x[:3]]
    alpha,gamma,eta=pars;right=F(0);witness=[]
    for ell,d in mass:
        total=F(0)
        for t in (0,1):
            p=F(d if t else 6-d,6)
            if not p:continue
            vals=[]
            for z in range(6):
                penalty=bycount[t,z,d-t] if kind=='refined' else -EPS*t*int(z==0)
                vals.append(q(t,t+z)-2*gamma*q(z,t+z)+gamma*penalty+(alpha/F(ell+1)+eta)*z)
            v=min(vals);witness.append({'ell':ell,'d':d,'t':t,'min':str(v),'minimizing_z':[z for z,x in enumerate(vals) if x==v]})
            total+=p*(gamma*q(d-t,d)+v)
        right+=mass[ell,d]*total
    left=u[0]+5*alpha*u[5]+(5*eta-(gamma*KAP if kind=='refined' else 0))*K
    return {'kind':kind,'capacity_enabled':capacity,'variables':count,'inequalities':len(A),'scipy_status':res.message,
            'float_min_slack':float(res.fun+float(u[0])),'parameters':[str(v) for v in pars],
            'exact_chosen_row_slack':str(left-right),'chosen_row_rhs':str(right),'chosen_row_lhs':str(left),'minima':witness,
            'discovery_primal':res.x.tolist(),'discovery_dual':res.ineqlin.marginals.tolist(),
            'states':[list(s) for s in states],'row_metadata':metadata}

def main():
    a,h,K,u,mass,rows,bycount,diag=input_data('discounted_augmented_lp/augmented_lp_exact.json','a4e48a91f0e2c7b65725178d042b515c6bedf11562afdeeea2ae69b815e8f505')
    print(json.dumps(diag,indent=2),flush=True)
    results=[envelope_lp(K,u,mass,bycount,kind,cap) for kind in ('charged','refined') for cap in (False,True)]
    output={'diagnostic':diag,'envelopes':results,'min_remainder_by_tail_count':[{'b':b,'count':c,'d':d,'min':str(v)} for (b,c,d),v in bycount.items()]}
    (OUT/'root_envelope_discovery.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps([{k:r[k] for k in ('kind','capacity_enabled','float_min_slack','parameters','exact_chosen_row_slack')} for r in results],indent=2))

if __name__=='__main__':main()
