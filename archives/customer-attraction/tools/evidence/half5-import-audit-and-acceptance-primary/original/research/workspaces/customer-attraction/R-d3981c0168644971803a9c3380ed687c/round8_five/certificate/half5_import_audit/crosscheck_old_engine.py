"""Cross-check the imported 53-row proof with the preexisting 557 engine.

Does not import the new portable verifier. Existing legacy features and its
full histogram oracle are reused, so this is an independent-parser cross-
check, not a second self-contained proof implementation.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
from math import ceil,floor
import json,sys,hashlib,time
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists())
PKG=ROOT/'customer_attraction/proofs/half5_exact_v1'
OLD=ROOT/'research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_pricing'
sys.path.insert(0,str(OLD));import full_pricing as old

def sc(v):
    v=120*F(v);assert v.denominator==1;return int(v)
def share(b,i):
    total=sum(b[t] for t in 'ABCDE');return F(b['ABCDE'[i]],total) if b['ABCDE'[i]] else F(0)


def tables():
    read=lambda n:json.loads((PKG/'components'/n).read_text())
    b2,b3=read('background_player2.json'),read('background_player3.json')
    bg=[]
    for i in (0,1,3,5,11,12):
        c=b2[i];bg.append([ceil(10**6*F(c['Kcoef'])),[0]+[floor(10**6*F(v)) for v in c['margin_coefs']],1])
    for c in b3[:3]:bg.append([ceil(10**6*F(c['beta_K'])),[floor(10**6*F(v)) for v in c['gamma_ABTQ']],2])
    pc=[]
    for c in read('priced_player2.json'):
        uc=[ceil(10**6*F(v)) for v in c['u_coefs']];uc[1]+=10**6
        pc.append([ceil(10**6*F(c['Kcoef'])),[floor(10**6*F(v)) for v in c['gamma']],uc])
    for c in read('priced_player3.json'):
        pc.append([ceil(10**6*F(c['Kcoef'])),[floor(10**6*F(v)) for v in c['gamma_ABCDTQ']],
                   [ceil(10**6*F(v)) for v in c['u_coefficients']]])
    dp=[]
    for c in read('deep_root_query.json'):
        dp.append([ceil(10**6*F(c[n])) for n in ('alpha','beta','gamma')]+[10**6,ceil(10**6*F(c['zeta']))])
    manifest=json.loads((PKG/'row_manifest.json').read_text())
    assert bg==manifest['BG'] and pc==manifest['PC'] and dp==manifest['DEEP']
    return bg,pc,dp


class CrossCheck(old.Universe):
    def __init__(self,weights,bg,pc,deep):
        super().__init__(overlap=1);self.bg,self.pc,self.deep=bg,pc,deep
        self.added=[n for n in weights if n not in self.names]
        assert len(self.added)==18,self.added
        self.familynew={n for n in self.added if n.split(':')[0] in ('AB','AE','Sbranch')}
        fixednew=[n for n in self.added if n not in self.familynew]
        start=len(self.names);self.names+=self.added
        extra=np.zeros((1024,6,len(fixednew)),dtype=np.int64)
        for bi,bits in enumerate(self.bits):
            b=dict(zip(old.LABELS,bits))
            for d in range(6):
                for j,n in enumerate(fixednew):extra[bi,d,j]=sc(self.fixed(n,b,d))
        self.base=np.concatenate([self.base,extra],axis=2)
        zz=np.zeros((1024,6,3,len(fixednew)),dtype=np.int64)
        self.ec=np.concatenate([self.ec,zz],axis=3);self.hc=np.concatenate([self.hc,zz],axis=3)
        self.oldids += [self.names.index(n) for n in fixednew]
    def parts(self,kind,i,b):
        if kind=='BG':
            kap,g,seat=self.bg[i];offset=4*(b['A'] if seat==1 else 2*b['A']+b['B'])
            return kap,10**6*share(b,seat),g[offset:offset+4]
        kap,g,uc=self.pc[i];offset=4*(8*b['A']+4*b['B']+2*b['C']+b['D'])
        return kap,sum(uc[j]*share(b,j) for j in range(5)),g[offset:offset+4]
    def fixed(self,name,b,d):
        if name=='MAXROOT-NEW':return 46313177*share(b,0)-10**6*int(d>0)
        z=name.split(':')
        if z[0]=='MAX':return -F(b[old.LABELS[int(z[2])]])
        if z[0]=='DEEP':
            alpha,kap,gamma,scale,zeta=self.deep[int(z[1])];t=b[old.LABELS[int(z[2])]];q=b[old.LABELS[int(z[3])]]
            return alpha*share(b,0)+gamma*t-scale*q+(scale+zeta)*t*q
        kap,u,g=self.parts(z[0],int(z[1]),b)
        return u-g[2*b[old.LABELS[int(z[2])]]+b[old.LABELS[int(z[3])]]]
    def family_score(self,bits,tag,weights,integer=False):
        own=[(n,w) for n,w in weights if n in self.familynew];rest=[(n,w) for n,w in weights if n not in self.familynew]
        key,const,vec,me,mh=super().family_score(bits,tag,rest,integer=integer)
        b=dict(zip(old.LABELS,bits));co=defaultdict(int)
        for n,w in own:
            _,kind,idx,way,ii,jj=n.split(':');assert way=='eq';i,j=int(ii),int(jj)
            kap,u,g=self.parts(kind,int(idx),b)
            const+=w*sc(5*u-5*g[0])
            co[('count',i)]+=-120*w*(g[2]-g[0]);co[('count',j)]+=-120*w*(g[1]-g[0])
            co[('overlap',i,j)]+=-120*w*(g[3]-g[2]-g[1]+g[0])
        for feature,v in co.items():
            if not v:continue
            k=key[0];ty=self.ty[k]
            bitsv=ty[:,feature[1]] if feature[0]=='count' else ty[:,feature[1]]*ty[:,feature[2]]
            arr=self.H[k]@bitsv;vec.append((v,arr))
        return (key[0],key,tuple(sorted(co.items()))),const,vec,me,mh
    def atom_rows(self,a):
        out=super().atom_rows(a);b=dict(zip(old.LABELS,map(int,a['bits'])));d=sum(a['AB_hist'][4:])
        for n in self.added:
            if n not in self.familynew:out[n]=self.fixed(n,b,d);continue
            tag,kind,idx,way,ii,jj=n.split(':');i,j=int(ii),int(jj);kap,u,g=self.parts(kind,int(idx),b)
            k=4 if tag=='Sbranch' else 3;field={'AB':'AB_hist','AE':'AE_hist','Sbranch':'second_hist'}[tag]
            out[n]=5*u-sum(count*g[2*int(t[i])+int(t[j])] for count,t in zip(a[field],self.ty[k]))
        return out


def run():
    start=time.time();manifest=json.loads((PKG/'MANIFEST.json').read_text());checks=[]
    for name,record in manifest['files'].items():
        raw=(PKG/name).read_bytes();assert len(raw)==record['bytes'] and hashlib.sha256(raw).hexdigest()==record['sha256'];checks.append(name)
    cert=json.loads((PKG/'certificate.json').read_text());weights={n:int(v) for n,v in cert['integer_multipliers'].items()}
    D=int(cert['common_denominator']);B=int(cert['beta_numerator']);assert len(weights)==53 and min(weights.values())>0 and B==2*D
    kcols=json.loads((PKG/'active_k_columns.json').read_text())['row_K_coefficients'];assert set(weights)==set(kcols)
    ksum=sum(weights[n]*int(kcols[n]) for n in weights);assert ksum==-2264870
    bg,pc,deep=tables();U=CrossCheck(weights,bg,pc,deep);lam=[weights.get(n,0) for n in U.names]
    minimum,bad,contexts=U.price(lam,B,integer='object',objective_scale=D,batch=20)
    assert minimum>=0 and not bad
    report={'status':'passed','scope':__doc__,'manifest_files_checked':len(checks),'positive_integer_multipliers':len(weights),
            'common_denominator':str(D),'target_beta':'2','conditional_domain':'1024 fixed bit masks x6 common optimal counts; complete old histogram/corner oracle',
            'minimum_scaled_integer_residual':str(minimum),'negative_types':len(bad),'score_contexts':contexts,'K_weighted_sum':str(ksum),
            'certificate_sha256':hashlib.sha256((PKG/'certificate.json').read_bytes()).hexdigest(),
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seconds':time.time()-start}
    (HERE/'old_engine_crosscheck.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':run()
