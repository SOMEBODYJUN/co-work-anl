"""Independent literal-index verifier of the compact 16-weight row.

No transfer/discovery/peer module is imported. The sixteen true-history costs
are written explicitly, every one of 30 ordered index pairs is enumerated,
and all four old R/Z states keep all sixteen B/C/J/V hidden states.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import hashlib,json,sys,time,platform,traceback

HERE=Path(__file__).resolve().parent
POINT=HERE.parent/'union_augmented_lp/augmented_lp_exact.json'
PACK=HERE/'compact_separating_row_exact.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def pay(n,d):
    assert d or not n
    return F(n,d) if n else F(0)
started=time.monotonic()
receipt={'argv':[sys.executable,*sys.argv],'cwd':str(Path.cwd()),'python':platform.python_version(),'script_sha256':sha(Path(__file__)),'point_sha256':sha(POINT),'certificate_sha256':sha(PACK),'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
try:
    assert sha(POINT)=='b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'
    point=json.loads(POINT.read_bytes());certificate=json.loads(PACK.read_bytes())
    columns=point['columns'];weights={n:F(v) for n,v in certificate['weights'].items()}
    assert set(weights)=={'sourceT','sourceC','price:b','price:c','price:j','price:v','cap:v','last2:b','last1:q6','pair2:q6,b','last1:q8','last1:q10','last2:q10','pair2:q14,b','oldpair1:6,10:product','priorZ:v'}
    assert all(w>=0 for w in weights.values())
    source=weights['sourceT']+weights['sourceC']
    lastprice=sum(weights['price:'+x] for x in 'bcjv')
    capacity=weights['cap:v']
    assert {'u4':str(source),'u6':str(lastprice),'K':str(capacity)}==certificate['wallet']
    vector=[F(0)]*15593;vector[0]=capacity
    blocks={}
    for ci,col in enumerate(columns[:4849]):
        if col['kind']=='hist':hist=ci;blocks[hist]={'column':col,'groups':{}}
        elif col['kind']=='joint-reply' and col['group'][:2]==[0,0]:
            key=tuple(col['group'][2]),tuple(col['group'][3])
            blocks[hist]['groups'].setdefault(key,{})[tuple(col['state'])]=ci
    literal_hidden_evaluations=0;literal_min_cancellations=0;tables=[]
    for hist,block in blocks.items():
        a=tuple(map(int,block['column']['actual_bits']))
        p,ell,p4=sum(a[:3]),sum(a[:5]),sum(a[:4])
        words=tuple(w for w,n in zip(product((0,1),repeat=3),block['column']['hist']) for _ in range(n))
        assert len(words)==6
        vector[hist]+=source*pay(a[3],sum(a))+lastprice*pay(a[5],sum(a))
        for li in range(6):
            for ri in range(6):
                if li==ri:continue
                wi,wj=words[li],words[ri]
                indices=block['groups'][wi,wj]
                ti,ci,bj=wi[0],wi[2],wj[1]
                mean_t=F(sum(words[k][0] for k in range(6) if k not in (li,ri)),4)
                psi={}
                for r,z in product((0,1),repeat=2):
                    candidates=[]
                    for b,c,j,v in product((0,1),repeat=4):
                        den1,den2=p+r+b+c,p+c+j+v
                        beta1,beta2=p+r,p+c
                        d1,d2=(beta1+1)*(beta1+2),(beta2+1)*(beta2+2)
                        terminal1,terminal2=pay(c,den1),pay(v,den2)
                        pair2=lambda x,y:F(x+y,beta2+1)-F(x*y+j,d2)-pay(j+v,den2)
                        e={'sourceT':pay(r,den1),'sourceC':pay(c,den2),
                           'price:b':F(b,ell+1),'price:c':F(c,ell+1),'price:j':F(j,ell+1),'price:v':F(v,ell+1),'cap:v':F(v),
                           'last2:b':F(b,p+c+j+1)-terminal2,
                           'last1:q6':F(ti,p+r+b+1)-terminal1,
                           'last1:q8':F(ci,p+r+b+1)-terminal1,
                           'last1:q10':F(bj,p+r+b+1)-terminal1,
                           'last2:q10':F(bj,p+c+j+1)-terminal2,
                           'pair2:q6,b':pair2(ti,b),'pair2:q14,b':pair2(mean_t,b),
                           'oldpair1:6,10:product':F(ti+bj,beta1+1)-F(ti*bj+b,d1)-pay(b+c,den1),
                           'priorZ:v':F(v,p4+r+1)-pay(z,p4+r+z)}
                        candidates.append(sum(weights[k]*e[k] for k in weights))
                        literal_hidden_evaluations+=1
                    psi[r,z]=min(candidates)
                    for cost in candidates:
                        residual=(cost-psi[r,z])/30
                        assert residual>=0
                        assert -cost/30+residual+psi[r,z]/30==0
                        literal_min_cancellations+=1
                vector[hist]-=psi[0,0]/30
                for state,index in indices.items():vector[index]-=(psi[state]-psi[0,0])/30
                tables.append({'hist_column':hist,'left':li,'right':ri,'psi_00_01_10_11':[str(psi[st]) for st in product((0,1),repeat=2)]})
    assert literal_hidden_evaluations==literal_min_cancellations==30720
    saved=list(map(F,certificate['original4849_vector']))+[F(0)]*10744
    assert vector==saved and all(v==0 for v in vector[4849:])
    x=[F(c['weight']) for c in columns]
    slack=sum(v*xv for v,xv in zip(vector,x))
    assert slack==F(certificate['exact_slack'])<0
    report={'status':'PASS','point_sha256':sha(POINT),'certificate_sha256':sha(PACK),'literal_hidden_evaluations':literal_hidden_evaluations,'literal_nonnegative_residual_and_cancellation_checks':literal_min_cancellations,'ordered_index_pairs_checked':480,'all_four_RZ_states_checked':True,'original_columns_exactly_equal':4849,'zero_auxiliary_columns_exactly_equal':10744,'full15593_coefficient_identity':True,'exact_slack':str(slack),'slack_float':float(slack),'wallet':certificate['wallet'],'minimum_feature_weight':str(min(weights.values())),'literal_tables':tables,'scope':'one actual4/R/family0-off exact Farkas projection; no SPE or half conclusion'}
    target=HERE/'literal_row_verification.json';assert not target.exists();target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='literal_tables'},ensure_ascii=False),flush=True)
    receipt['status']='SUCCESS'
except BaseException as e:
    receipt.update(status='FAILED',error=repr(e),traceback=traceback.format_exc());raise
finally:
    receipt['elapsed_seconds']=time.monotonic()-started
    target=HERE/'execution_literal_verify.json';assert not target.exists();target.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
