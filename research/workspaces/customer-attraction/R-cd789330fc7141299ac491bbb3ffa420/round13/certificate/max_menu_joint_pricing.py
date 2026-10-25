"""Join the real maximum-theme four-tail with full menu AP pricing.

Given the old ten bits and optimal multiplicity, the five maximum-branch
bits are a separate complete 32-state block. Old-menu caps split into a
linear old-menu count and one shared maximum bit. Tail queries of the old
reply menus are omitted: they would couple the two blocks. Float discovery.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import comb
import json,sys,time,hashlib
import numpy as np
from scipy.optimize import linprog
import menu_ap_pricing as mp
import lift_maximum_branch as lm
HERE=Path(__file__).resolve().parent
STATES=lm.STATES

def rho4(p,abcd,qrs):
    a,b,c,d=abcd;q,r,s=qrs;k=sum(abcd);t=d+q+r+s
    pay=[lm.q(h,p+k) for h in abcd];z=[lm.q(h,p+t) for h in (d,q,r,s)]
    den=(p+1)*(p+2)*(p+3)*(p+4)
    dt2=F(1,p+1)-F(1,p+a+b+1)+(F(2*p*p,3*den) if a+b==2 else 0)
    dt3=F(1,p+1)-F(1,p+a+b+c+1)+(F(p*p+p,den) if a+b+c==3 else 0)
    pp=2*(pay[2]+pay[3]+F(c,(p+a+b+1)*(p+a+b+2)))+dt2;ee=4*pay[3]+dt3
    ff=pay[0]-z[0];kk=[pay[1]-F(x,p+a+3) for x in (c,d,q,r,s)]
    ll=[z[1]-F(s,p+d+3),z[2]-F(c,p+d+q+2),z[2]-F(s,p+d+q+2),z[3]-F(b,p+d+q+r+1)]
    gg=(sum(w*x for w,x in zip((341,302,306,302,355),kk))+354*ee+646*pp+1267*ff+sum(w*x for w,x in zip((24,8,17,108),ll)))/1000
    return F(1499,750)*lm.q(k,p+k)-gg
RHOMIN={(p,b):min(rho4(p,b,q) for q in product((0,1),repeat=3)) for p in (0,1) for b in product((0,1),repeat=4)}
def mapping(n):
    for tag,menus in mp.MENUS.items():
        for i,m in enumerate(menus,1):
            if n==f'max:cap:{"second" if tag=="Sbranch" else tag}:menu{i}':return f'{tag}:MaxCap:{m}'
    return n
def new_rows(a,mb):
    rr={mapping(n):v for n,v in lm.rows(a,mb).items() if ':tailmenu:' not in n}
    d=sum(a['AB_hist'][4:]);total=sum(mb)
    for rem,beta in ((3,F(5,3)),(4,F(1499,750))):
        p=sum(mb[:5-rem]);v=lm.q(sum(mb[5-rem:]),total)
        target=sum((comb(d,j)*comb(5-d,rem-j)*F(j,p+j) for j in range(1,rem+1) if j<=d and 0<=rem-j<=5-d),F(0))
        rr[f'max:profit{rem}:opt-subsets']=comb(5,rem)*beta*v-target
        if rem==4:rr['max:profit4:opt-residual']=5*beta*v-target-5*RHOMIN[mb[0],tuple(mb[1:])]
    return rr

class Universe(mp.Universe):
    def __init__(self):
        super().__init__();self.before_max=len(self.names)
        dummy={'bits':'0'*10,'AB_hist':[5]+[0]*7,'AE_hist':[5]+[0]*7,'second_hist':[5]+[0]*15,'menus_lh':[(0,0)]*3}
        self.maxnames=list(new_rows(dummy,STATES[0]));self.names+=self.maxnames
        self.B=np.asarray(self.bits,dtype=float);self.SMB=np.asarray(STATES,dtype=float);self.dd=np.arange(6)[None,:,None]
        self.m=self.SMB[:,0][None,None,:];self.bt=self.B[:,None,:];self._maxchoices=None
        print(json.dumps({'maximum_branch_rows':len(self.maxnames),'total_rows':len(self.names)}),flush=True)
    def atom_rows(self,a):
        if 'max_bits' not in a:
            assert self._maxchoices is not None
            bi=int(a['bits'],2);d=sum(a['AB_hist'][4:]);a['max_bits']=''.join(map(str,STATES[int(self._maxchoices[bi,d])]))
        rr=super().atom_rows(a);rr.update(new_rows(a,tuple(map(int,a['max_bits']))));return rr
    def family_score(self,bits,tag,weights,integer=False):
        caps=[(n,v) for n,v in weights if ':MaxCap:' in n];rest=[(n,v) for n,v in weights if ':MaxCap:' not in n]
        key,const,vec,me,mh=super().family_score(bits,tag,rest,integer=integer)
        cc=[]
        for n,v in caps:
            menu=n.split(':')[-1];vec.append((-120*v,self.countarr[tag][menu]));cc.append((menu,v))
        return (key[0],key,tuple(cc)),const,vec,me,mh
    def block_coeff(self,name):
        # Arrays broadcast to old_bits x optimal_multiplicity x max_branch.
        b=self.B;m=self.m;mb=self.SMB;d=self.dd
        def bit(t):return b[:,mp.LABELS.index(t)][:,None,None]
        def mt(i):return mb[:,i][None,None,:]
        total=mb.sum(1);pre=[mb[:,:i].sum(1) for i in range(5)]
        def share(i):return np.divide(mb[:,i],total,out=np.zeros(32),where=total>0)[None,None,:]
        def old(pn,i):
            path=mp.PATHS[pn];load=b[:,[mp.LABELS.index(t) for t in path]].sum(1);u=np.divide(b[:,mp.LABELS.index(path[i])],load,out=np.zeros(1024),where=load>0);p=b[:,[mp.LABELS.index(t) for t in path[:i]]].sum(1)
            return u[:,None,None],p[:,None,None],5-i
        sp=name.split(':');u1=old('actual',0)[0]
        if ':MaxCap:' in name:return 5*m
        if sp[1]=='root':return u1-share(0)
        if sp[1]=='cap':
            if sp[2] in mp.LABELS and len(sp[2])==1:return m-bit(sp[2])
            if sp[2].startswith('reply'):return m-mt(int(sp[2][5:]))
            if sp[2]=='optimal-sum':return 5*m-d
            if sp[2].startswith('oldmenu'):return 5*m
            raise ValueError(name)
        if sp[1]=='BNS':
            if sp[2]=='optimal-sum':return 400*u1-75*m-(5-4*m)*d
            return 80*u1-15*m-(5-4*m)*bit(sp[2])
        if sp[1]=='oldK':
            u,p,k=old(sp[2],int(sp[3]));return u-mt(int(sp[4]))/(p+k)
        if sp[1] in ('tailK','tailownK','tailopt','tailAP'):
            i=int(sp[2]);p=pre[i][None,None,:];k=5-i;u=share(i)
            if sp[1]=='tailK':return u-bit(sp[3])/(p+k)
            if sp[1]=='tailownK':return u-mt(int(sp[3]))/(p+k)
            if sp[1]=='tailopt':return 5*u-d/(p+k)
            c=bit(sp[3]);e=bit(sp[4]);a=mp.aa(k);return a*u-((a-2)*c+2*c*e)/(p+k)-2*e*(1-c)/(p+1)
        if sp[1]=='tax':
            p=pre[3][None,None,:];h=share(3)+share(4)+mt(3)/((p+1)*(p+2))
            if sp[2]=='opt-union':return 2.5*h+p/(p+1)-(d>0)
            if sp[2]=='opt-pairs':return 10*h-d*(5-d)/(p+1)-d*(d-1)/(p+2)
            c=bit(sp[2]);e=bit(sp[3]);return h-(c+e-2*c*e)/(p+1)-2*c*e/(p+2)
        if sp[1].startswith('profit'):
            rem=int(sp[1][6:]);beta=F(5,3) if rem==3 else F(1499,750);ans=np.zeros((1,6,32))
            for di in range(6):
                for mi,st in enumerate(STATES):
                    p=sum(st[:5-rem]);v=lm.q(sum(st[5-rem:]),sum(st));tar=sum((comb(di,j)*comb(5-di,rem-j)*F(j,p+j) for j in range(1,rem+1) if j<=di and 0<=rem-j<=5-di),F(0));val=comb(5,rem)*beta*v-tar
                    if sp[2]=='opt-residual':val-=5*RHOMIN[st[0],tuple(st[1:])]
                    ans[0,di,mi]=float(val)
            return ans
        raise ValueError(name)
    def maximum_scores(self,lam):
        maxlam=lam[self.before_max:];score=np.zeros((1024,6,32))
        for name,v in zip(self.maxnames,maxlam):
            if abs(v)>1e-11:score+=120*v*self.block_coeff(name)
        return score
    def price(self,lam,beta,**kw):
        assert not kw.get('integer',False),'Exact recovery must compute the actual coefficient LCM; current 511-row block uses 36000.'
        maxlam=lam[self.before_max:];score=self.maximum_scores(lam)
        self._maxchoices=np.argmax(score,axis=2);support=np.max(score,axis=2)
        nonzero=np.where(abs(maxlam)>1e-11)[0]
        if not len(nonzero):return super().price(lam,beta,**kw)
        chosen=self.before_max+int(nonzero[0]);div=lam[chosen]
        base,ec,hc,ids=self.base,self.ec,self.hc,self.oldids
        pieces=[support[:,:,None]/div];ep=[np.zeros((1024,6,3,1))];extraids=[chosen]
        for f in range(3):
            name=f'max:cap:oldmenu{f}';j=self.names.index(name)
            pieces.append(np.zeros((1024,6,1)));ee=np.zeros((1024,6,3,1));ee[:,:,f,0]=-120;ep.append(ee);extraids.append(j)
        self.base=np.concatenate([base]+pieces,axis=2);self.ec=np.concatenate([ec]+ep,axis=3);self.hc=np.concatenate([hc]+[np.zeros_like(a) for a in ep],axis=3);self.oldids=ids+extraids
        try:return super().price(lam,beta,**kw)
        finally:self.base,self.ec,self.hc,self.oldids=base,ec,hc,ids

def run(maxiter=8,universe_class=Universe,target_name='max_menu_joint_discovery.json',source_name='menu_ap_discovery.json'):
    U=universe_class();target=HERE/target_name;source=target if target.exists() else HERE/source_name;src=json.loads(source.read_text());atoms=[];cols=[];keys=set();ws=[];os=[]
    def add(a,oldrr=None):
        key=mp.atom_key(a)+(a['max_bits'],)
        if key in keys:return 0
        rr=U.atom_rows(a) if oldrr is None else {**oldrr,**new_rows(a,tuple(map(int,a['max_bits'])))}
        cols.append([float(rr[n]) for n in U.names]);atoms.append(a);keys.add(key);ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])));return 1
    keep=[i for i,v in enumerate(src['primal_float']) if v>1e-8]
    for i in keep:
        a=src['atoms'][i]
        if 'max_bits' in a:add(a)
        else:
            rr=mp.Universe.atom_rows(U,a)
            for st in STATES:add(dict(a,max_bits=''.join(map(str,st))),rr)
    for d in (0,5):
        h3=[0]*8;h3[3 if d==0 else 7]=5;h4=[0]*16;h4[7 if d==0 else 15]=5
        add({'bits':'1111111111','AB_hist':h3,'AE_hist':h3,'second_hist':h4,'menus_lh':[(5,d)]*3,'max_bits':'11111'})
    history=[]
    for it in range(maxiter):
        start=time.time();mat=np.asarray(cols).T;lp=linprog(-np.array(os,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs');assert lp.success,lp.message
        beta=-lp.fun;lam=-lp.ineqlin.marginals
        # Any restricted primal above two already rules out this row system.
        if beta>2+1e-7:minimum=None;new=[];contexts=None
        else:minimum,new,contexts=U.price(lam,beta,batch=80)
        count=sum(add(a) for _,a in new);rec={'iteration':it,'columns':len(atoms),'restricted_beta':beta,'minimum_scaled_residual':minimum,'new_columns':count,'pricing_contexts':contexts,'seconds':time.time()-start};history.append(rec);print(json.dumps(rec),flush=True)
        report={'scope':'Floating joint maximum-branch/menu-AP necessary-condition discovery. Not a universal certificate or game.','row_names':U.names,'atoms':atoms,'primal_float':lp.x.tolist()+[0.]*count,'dual_beta_float':beta,'history':history,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};target.write_text(json.dumps(report,indent=2)+'\n')
        if beta>2+1e-7 or count==0:break
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 8)
