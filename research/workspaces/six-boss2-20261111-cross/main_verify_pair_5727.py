"""Separate exact audit of the new shared-source PAIR cuts and strict witness."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from collections import defaultdict
import json,hashlib,time
B=Path(__file__).resolve().parent

def pay(a,b):return F(a,b) if a else F(0)

def terms(p,ell,t,q,b,c,j,v,s=0,ss=0,k=3):
    u={'t':F(t),'q':F(q),'b':F(b),'c':F(c),'j':F(j),'v':F(v)}
    z1=p+t+s+b+c;z2=p+c+ss+j+v
    e={'sourceT':pay(t,z1),'sourceC':pay(c,z2)}
    cost={'sourceT':(1,0,0),'sourceC':(1,0,0)}
    for label in 'bcjv':e['price:'+label]=u[label]/(ell+1);cost['price:'+label]=(0,1,0);e['cap:'+label]=u[label];cost['cap:'+label]=(0,0,1)
    for name,den,own,z,qs in [('last1',p+t+s+b+1,c,z1,'tqbjv'),('last2',p+c+ss+j+1,v,z2,'tqbcj'),('safeB',p+t+s+2,b,z1,'tqcjv'),('safeJ',p+c+ss+2,j,z2,'tqbcv')]:
        for a in qs:e[name+':'+a]=u[a]/den-pay(own,z);cost[name+':'+a]=(0,0,0)
    for a,count in [('s',s),('ss',ss)]:e['price:'+a]=F(count,ell+1);e['cap:'+a]=F(count);cost['price:'+a]=(0,k-3,0);cost['cap:'+a]=(0,0,k-3)
    labels=['t','q','b','c','j','v']
    for which,beta,first,last,z in [(1,p+t+s,b,c,z1),(2,p+c+ss,j,v,z2)]:
        for ai,aa in enumerate(labels):
            for bb in labels[ai:]:
                overlap=u[aa] if aa==bb else u[aa]*u[bb]
                key=f'pair{which}:{aa},{bb}'
                e[key]=(u[aa]+u[bb])/(beta+1)-(overlap+first)/((beta+1)*(beta+2))-pay(first+last,z)
                cost[key]=(0,0,0)
    return e,cost

def audit_strict():
    p=B/'joint_requery/actual_signature_witness.json';a=json.loads(p.read_text());tot=F(0);r=F(0);u6=F(0);sums=defaultdict(F)
    old={k:F(v) for k,v in a['slacks'].items()};theta={k:F(v) for k,v in a['theta_integer'].items()};K=F(a['K']);credit=F(0)
    for v in a['support']:
        aa=v['a'];t=v['t'];q=v['q'];h=v['hidden'];w=F(v['mass']);pfx=sum(aa[:3]);ell=sum(aa[:5]);tot+=w;r+=w*pay(aa[3],sum(aa));u6+=w*pay(aa[5],sum(aa));e,bud=terms(pfx,ell,t,q,*h)
        for name in old:
            if name.startswith('actualprice:'):
                label=name.split(':')[1];z=t if label=='t' else q if label=='q' else aa[int(label[1:])];sums[name]+=w*pay(z,ell+1)
            elif name.startswith('actualcap:'):
                label=name.split(':')[1];z=t if label=='t' else q if label=='q' else aa[int(label[1:])];sums[name]+=w*z
            else:sums[name]+=w*e[name]
        vv=[sum((v*terms(pfx,ell,t,q,*hidden)[0][n] for n,v in theta.items()),F(0)) for hidden in product((0,1),repeat=4)]
        mn=min(vv);expected=F(6052)*q/(pfx+1) if not t else F(925)+F(65146+6052*q,pfx+3)
        assert mn==expected;credit+=w*mn
    assert tot==1 and r==F(a['r_u4']) and u6==F(a['u6'])
    for name,value in sums.items():
        if name.startswith('actualprice:'):budget=u6
        elif name.startswith('actualcap:'):budget=K
        else:
            rr,uu,kk=bud[name];budget=rr*r+uu*u6+kk*K
        assert budget-value==old[name]>=0,(name,budget-value,old[name])
    gap=71198*r+925*K-credit
    assert gap==F(a['new_slack_integer_scale'])<0
    return {'atoms':len(a['support']),'old_rows_exact_nonnegative':len(old),'new_slack':str(gap),'actual_background_and_payoff_link':True}

def audit_cut(rec,cols):
    weights={key:F(v) for key,v in rec['weights'].items()};orb=tuple(rec['orb']);ct=6 if orb[1] else 30;source=rec['i'];k=rec['k']
    budget=[sum((w*terms(0,0,0,0,0,0,0,0,k=k)[1][n][j] for n,w in weights.items()),F(0)) for j in range(3)]
    assert budget[0]==1 and budget[1]==F(rec['u6_coefficient']) and budget[2]==F(rec['K_coefficient'])
    @lru_cache(None)
    def phi(p,ell,t,q):return min(sum((w*terms(p,ell,t,q,*h,s,ss,k)[0][n] for n,w in weights.items()),F(0)) for h in product((0,1),repeat=4) for s in range(k-2) for ss in range(k-2))
    row=[F(0)]*len(cols);row[0]=budget[2];cur=None
    for ci,col in enumerate(cols):
        if col['kind']=='hist':
            aa=tuple(map(int,col['actual_bits']));pfx=sum(aa[:source]);ell=sum(aa[:5]);words=tuple(w for w,n in zip(product((0,1),repeat=3),col['hist']) for _ in range(n));pairs=[(i,j) for i in range(6) for j in range(6) if (i==j)==bool(orb[1])]
            increments=defaultdict(F);base=F(0)
            for i,j in pairs:
                others=[l for l in range(6) if l not in {i,j}]
                qs=aa+words[i]+words[j]+(None,)+tuple(F(sum(words[l][q] for l in others),len(others)) for q in range(3))
                values=[]
                for t in (0,1):
                    q=t if rec['query']==12 else qs[rec['query']];values.append(phi(pfx,ell,t,F(q)))
                base+=values[0]/ct;increments[words[i],words[j]]+=(values[1]-values[0])/ct
            row[ci]=pay(aa[source],sum(aa))+budget[1]*pay(aa[5],sum(aa))-base
        elif col['kind']=='joint-reply':
            f,d,wi,wj=col['group']
            if (f,d)==orb and col['state'][rec['member']]:row[ci]=-increments[tuple(wi),tuple(wj)]
    target=[F(0)]*len(cols)
    for i,v in rec['sparse_row']:target[i]=F(v)
    assert target==row
    value=sum((w*F(c['weight']) for w,c in zip(row,cols)),F(0));assert value==F(rec['exact_slack'])<0
    return {'source':source+1,'k':k,'member':rec['member'],'orb':list(orb),'query':rec['query'],'slack':str(value),'full_coefficients_equal':True}
start=time.time();pointpath=B/'master_cuts/dynamic_5727_exact.json';packpath=B/'joint_requery/selected_cuts_5727.json';point=json.loads(pointpath.read_text());pack=json.loads(packpath.read_text())
assert pack['source_sha256']==hashlib.sha256(pointpath.read_bytes()).hexdigest()
report={'status':'PASS','scope':'Independent direct feature/PAIR/16-hidden-state/literal-index Fraction reconstruction, all k=3,4,5 middle counts; not SPE','cut_checks':[audit_cut(r,point['columns']) for r in pack['cuts']],'point_sha256':pack['source_sha256'],'pack_sha256':hashlib.sha256(packpath.read_bytes()).hexdigest(),'seconds':time.time()-start}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
