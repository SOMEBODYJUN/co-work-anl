"""Root optimal-topic continuation family added to the earlier 727-row model.
Numerical discovery only. Every additional row is a necessary SPE inequality.
"""
from pathlib import Path
import sys,json,time
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists())
BASE=ROOT/'research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_pricing'
sys.path.insert(0,str(BASE))
from full_pricing import Universe,PATHS,START,LABELS,EX,VE,sc,q,compositions,atom_key
RPOS='TXYZK'
TYPES=np.array(list(product((0,1),repeat=5)),dtype=np.int16)

def root_rows(bits,hist,lhs,exact=True):
    # T_i and four replies X_i,Y_i,Z_i,K_i are the true root-deviation path.
    # Works both with scalar hist and vectorized hist.T.
    b=dict(zip(LABELS,bits));Q=EX['q'] if exact else VE['q'];FF=F if exact else lambda x,y:x/y
    opt=lambda v:int(v>0) if exact else np.asarray(v>0,dtype=int)
    def sm(fn):return sum((n*fn(*map(int,ty)) for n,ty in zip(hist,TYPES)),F(0) if exact else 0)
    d=sm(lambda t,x,y,z,k:t);covered=opt(d)
    count={m:sm(lambda *tt:tt[i]) for i,m in enumerate(RPOS)}
    shares={m:sm(lambda *tt:Q(tt[i],sum(tt))) for i,m in enumerate(RPOS)}
    dens={i:sm(lambda *tt:Q(1,sum(tt[:i])+5-i)) for i in range(1,5)}
    def share(path,i):return Q(b[path[i]],sum(b[t] for t in path))
    out={'Root:F1':5*share(PATHS['actual'],0)-shares['T']}
    for i in range(1,5):
        sh=shares[RPOS[i]];de=dens[i]
        for m in LABELS:out[f'Root:{i+1}:K:{m}']=sh-b[m]*de
        out[f'Root:{i+1}:sum-opt']=5*sh-d*de
        for j,m in enumerate(RPOS):
            out[f'Root:{i+1}:own:{m}']=sh-sm(lambda *tt:Q(tt[j],sum(tt[:i])+5-i))
            out[f'Root:{i+1}:menu:{m}']=5*sh-count[m]*de
    # Four-remaining profit theorem, beta4=1499/750, multiplied by 750.
    def g4(p,j):return Q(j*(j-1),p+j-1)+Q((5-j)*j,p+j)
    tail=sum(shares[m] for m in RPOS[1:])
    for m in RPOS:
        cc=count[m]
        out['Root:r4:menu:'+m]=7495*tail-750*sm(lambda t,x,y,z,k:g4(t,cc))
    for pn,path in PATHS.items():
        cc=sum(b[v] for v in path)
        out['Root:r4:path:'+pn]=7495*tail-750*sm(lambda t,x,y,z,k:g4(t,cc))
    out['Root:actual4:opt']=7495*sum(share(PATHS['actual'],i) for i in range(1,5))-750*g4(b['A'],d)
    def g3(p,j):return Q(j*(5-j)*(4-j)//2,p+1)+Q(j*(j-1)*(5-j),p+2)+Q(j*(j-1)*(j-2)//2,p+3)
    tail3=sum(shares[m] for m in RPOS[2:])
    for m in RPOS:
        cc=count[m]
        out['Root:r3:menu:'+m]=100*tail3-6*sm(lambda t,x,y,z,k:g3(t+x,cc))
    for pn,path in PATHS.items():
        cc=sum(b[v] for v in path)
        out['Root:r3:path:'+pn]=100*tail3-6*sm(lambda t,x,y,z,k:g3(t+x,cc))
        pref=sum(b[v] for v in path[:2])
        out['Root:actual3:'+pn]=100*sum(share(path,i) for i in range(2,5))-6*g3(pref,d)
    H=shares['Z']+shares['K']+sm(lambda t,x,y,z,k:Q(z,(t+x+y+1)*(t+x+y+2)))
    D1=sm(lambda t,x,y,z,k:Q(1,t+x+y+1));D2=sm(lambda t,x,y,z,k:Q(1,t+x+y+2))
    out['Root:r2:O']=FF(5,2)*H+sm(lambda t,x,y,z,k:Q(t+x+y,t+x+y+1))-5*covered
    out['Root:r2:exact-opt']=10*H-d*(5-d)*D1-d*(d-1)*D2
    for a,c in combinations_with_replacement(RPOS,2):
        A=count[a];C=count[c]
        out[f'Root:r2:menu:{a}{c}']=25*H-(A*(5-C)+(5-A)*C)*D1-2*A*C*D2
    for f,(pn,path) in enumerate(PATHS.items()):
        p=sum(b[t] for t in path[:3]);DP=(p+1)*(p+2);ell,hh=lhs[f]
        for m in RPOS[1:]:
            c=count[m]
            for i in range(START[pn],5):
                pref=sum(b[t] for t in path[:i]);out[f'Root:{pn}:{i+1}:sum:{m}']=5*share(path,i)-Q(c,pref+5-i)
            out[f'Root:{pn}:reply:{m}']=Q(5*ell-5*c,p+1)+Q(d*c-5*hh,DP)
    return out

class RootUniverse(Universe):
    def __init__(self):
        super().__init__(1)
        self.oldn=len(self.names);t0=time.time()
        hs=np.array(list(compositions(5,32)),dtype=np.int16)
        self.rh=hs;self.rd=hs@TYPES[:,0];self.rids=[np.where(self.rd==d)[0] for d in range(6)]
        self.rc={m:hs@TYPES[:,i] for i,m in enumerate(RPOS)}
        rr=root_rows([0]*10,hs.T,[(0,0)]*3,False)
        self.rnames=list(rr);self.names+=self.rnames
        # Local root branch rows have fixed zero-background coefficients.
        self.local={n:sc(v) for n,v in rr.items() if n.split(':')[1] in ('F1','2','3','4','5','r2','r4','r3')}
        self.rden={}
        for i in range(1,5):self.rden[i]=hs@sc([q(1,int(sum(t[:i]))+5-i) for t in TYPES])
        tail=hs@sc([q(int(sum(t[1:])),int(sum(t))) for t in TYPES])
        self.local['tail']=tail
        for c in range(6):
            self.local['g4path:'+str(c)]=hs@sc([-750*(q(c*(c-1),int(t[0])+c-1)+q((5-c)*c,int(t[0])+c)) for t in TYPES])
        for a in (0,1):
            self.local['actual4:'+str(a)]=sc([-750*(q(int(d)*(int(d)-1),a+int(d)-1)+q((5-int(d))*int(d),a+int(d))) for d in self.rd])
        self.local['tail3']=hs@sc([q(int(sum(t[2:])),int(sum(t))) for t in TYPES])
        for c in range(6):
            self.local['g3path:'+str(c)]=hs@sc([-6*(q(c*(5-c)*(4-c)//2,int(t[0]+t[1])+1)+q(c*(c-1)*(5-c),int(t[0]+t[1])+2)+q(c*(c-1)*(c-2)//2,int(t[0]+t[1])+3)) for t in TYPES])
        for a in range(3):
            self.local['actual3:'+str(a)]=sc([-6*(q(int(d)*(5-int(d))*(4-int(d))//2,a+1)+q(int(d)*(int(d)-1)*(5-int(d)),a+2)+q(int(d)*(int(d)-1)*(int(d)-2)//2,a+3)) for d in self.rd])
        self.old_size=len(self.names)
        print(json.dumps({'root_init_seconds':time.time()-t0,'root_histograms':len(hs),'new_rows':len(self.rnames),'total_rows':len(self.names)}),flush=True)
    def atom_rows(self,a):
        rr=super().atom_rows(a)
        rr.update(root_rows(tuple(map(int,a['bits'])),a['root_hist'],a['menus_lh']))
        return rr
    def root_score(self,bits,weights,integer=False):
        b=dict(zip(LABELS,bits));co=defaultdict(int if integer else float);const=0
        E=np.zeros((3,6),dtype=np.int64 if integer else float);H=E.copy()
        def sh(path,i):return q(b[path[i]],sum(b[t] for t in path))
        for n,v in weights:
            sp=n.split(':')[1:]
            if sp[0]=='F1':const+=v*int(sc(5*sh(PATHS['actual'],0)));co[n]+=v
            elif sp[0] in ('2','3','4','5'):
                i=int(sp[0])-1
                if sp[1]=='K':co[f'Root:{i+1}:K:A']+=v;co['den:'+str(i)]-=v*b[sp[2]]
                else:co[n]+=v
            elif sp[0]=='r2':co[n]+=v
            elif sp[0]=='r4':
                if sp[1]=='menu':co[n]+=v
                else:
                    cc=sum(b[z] for z in PATHS[sp[2]])
                    co['Root:r4:menu:K']+=v
                    co['g4path:'+str(cc)]+=v
                    co['g4path:0']-=v
                    # Replace reference local K-menu with a pure tail term.
                    co['Root:r4:menu:K']-=v
                    co['tail']+=7495*v
            elif sp[0]=='r3':
                if sp[1]=='menu':co[n]+=v
                else:
                    cc=sum(b[z] for z in PATHS[sp[2]])
                    co['tail3']+=100*v
                    co['g3path:'+str(cc)]+=v
            elif sp[0]=='actual3':
                path=PATHS[sp[1]]
                const+=v*int(sc(100*sum(sh(path,i) for i in range(2,5))))
                co['actual3:'+str(sum(b[t] for t in path[:2]))]+=v
            elif sp[0]=='actual4':
                const+=v*int(sc(7495*sum(sh(PATHS['actual'],i) for i in range(1,5))))
                co['actual4:'+str(b['A'])]+=v
            else:
                pn=sp[0];path=PATHS[pn]
                if sp[1]=='reply':
                    m=sp[2];p=sum(b[t] for t in path[:3]);DP=(p+1)*(p+2);f=list(PATHS).index(pn)
                    E[f,:]+=v*int(sc(q(5,p+1)));H[f,:]-=v*int(sc(q(5,DP)))
                    co['count:'+m]-=v*int(sc(q(5,p+1)))
                    co['dcount:'+m]+=v*int(sc(q(1,DP)))
                else:
                    i=int(sp[1])-1;m=sp[3];pref=sum(b[t] for t in path[:i]);const+=v*int(sc(5*sh(path,i)))
                    co['count:'+m]-=v*int(sc(q(1,pref+5-i)))
        key=tuple(sorted((n,v) for n,v in co.items() if v))
        return key,const,co,E,H
    def root_price(self,co,integer=False):
        score=np.zeros(len(self.rh),dtype=np.int64 if integer else float)
        for n,v in co.items():
            if not v:continue
            if n.startswith('den:'):vec=self.rden[int(n[4:])]
            elif n.startswith('count:'):vec=self.rc[n[6:]]
            elif n.startswith('dcount:'):vec=self.rd*self.rc[n[7:]]
            else:vec=self.local[n]
            score+=v*vec
        vals=[];idx=[]
        for ids in self.rids:
            arg=ids[int(np.argmax(score[ids]))];vals.append(score[arg]);idx.append(int(arg))
        return np.array(vals),idx
    def price(self,lam,beta,batch=80,integer=False,objective_scale=1):
        weights=[(n,int(v) if integer else float(v)) for n,v in zip(self.names,lam) if abs(v)>1e-11]
        fam={t:[] for t in ('AB','AE','Sbranch')};rw=[]
        for n,v in weights:
            tag=n.split(':')[0]
            if tag=='Root':rw.append((n,v))
            elif tag in fam:fam[tag].append((n,v))
            elif ':sum-S' in n:fam['Sbranch'].append((n,v))
        ow=np.asarray(lam)[self.oldids];base=self.base@ow;EC=self.ec@ow;HC=self.hc@ow
        cache={};rcache={};best=[];minimum=1e100
        for bi,bits in enumerate(self.bits):
            fs=[];E=EC[bi].copy();H=HC[bi].copy();choices=[]
            for tag in fam:
                key,const,vec,me,mh=self.family_score(bits,tag,fam[tag],integer=integer);k=key[0]
                if key not in cache:
                    score=np.zeros(len(self.hist[k]),dtype=float)
                    for v,a in vec:score+=v*a
                    vals=[];idx=[]
                    for ids in self.ids[k]:
                        arg=ids[int(np.argmax(score[ids]))];vals.append(score[arg]);idx.append(int(arg))
                    cache[key]=(np.asarray(vals),idx)
                vals,idx=cache[key];fs.append(vals+const);choices.append(idx);E+=me.T;H+=mh.T
            rk,const,co,me,mh=self.root_score(bits,rw,integer)
            if rk not in rcache:rcache[rk]=self.root_price(co,integer)
            vals,ridx=rcache[rk];fs.append(vals+const);E+=me.T;H+=mh.T
            for d in range(6):
                corners=[(0,0),(d,d),(5-d,0),(5,d)];lhs=[];menus=0
                for f in range(3):
                    lh=max(corners,key=lambda lh:lh[0]*E[d,f]+lh[1]*H[d,f]);lhs.append(lh);menus+=lh[0]*E[d,f]+lh[1]*H[d,f]
                residual=120*(beta*int(any(bits[:5]))-objective_scale*int(d>0))-base[bi,d]-menus-sum(a[d] for a in fs)
                minimum=min(minimum,residual)
                if residual < -1e-7:
                    atom={'bits':''.join(map(str,bits)),'AB_hist':list(self.hist[3][choices[0][d]]),'AE_hist':list(self.hist[3][choices[1][d]]),'second_hist':list(self.hist[4][choices[2][d]]),'root_hist':self.rh[ridx[d]].tolist(),'menus_lh':lhs}
                    best.append((residual,atom))
        best.sort(key=lambda z:z[0])
        for residual,a in best[:batch]:
            direct=self.atom_rows(a);rho=120*(beta*int(any(map(int,a['bits'][:5])))-int(any(a['AB_hist'][4:])))
            rho-=120*sum(float(v)*float(direct[n]) for n,v in zip(self.names,lam))
            assert abs(rho-residual)<1e-6,(rho,residual)
        return minimum,best[:batch],len(cache)+len(rcache)

def rkey(a):return atom_key(a)+(tuple(a['root_hist']),)
def run(maxiter=100):
    U=RootUniverse();source=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal']
    atoms=[];keys=set();cols=[];ws=[];os=[]
    def add(a):
        k=rkey(a)
        if k in keys:return 0
        rr=U.atom_rows(a);cols.append([float(rr[n]) for n in U.names]);atoms.append(a);keys.add(k)
        ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])));return 1
    previous=HERE/'root_cg.json'
    if previous.exists():
        for a in json.loads(previous.read_text())['atoms']:add(a)
    # Start with each old atom paired to constant continuation histograms.
    for a in source['atoms']:
        d=sum(a['AB_hist'][4:])
        for r in (0,15):
            h=[0]*32;h[r]=5-d;h[16+r]=d;add({**a,'root_hist':h})
    for d in (0,5):
        h3=[0]*8;h3[3 if d==0 else 7]=5;h4=[0]*16;h4[7 if d==0 else 15]=5;h5=[0]*32;h5[15 if d==0 else 31]=5
        add({'bits':'1111111111','AB_hist':h3,'AE_hist':h3,'second_hist':h4,'root_hist':h5,'menus_lh':[(5,d)]*3})
    history=[]
    for it in range(maxiter):
        t0=time.time();mat=np.array(cols).T
        out=linprog(-np.array(os,dtype=float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs')
        if not out.success:raise RuntimeError(out.message)
        beta=-out.fun;lam=-out.ineqlin.marginals;minimum,new,ncache=U.price(lam,beta)
        count=sum(add(a) for _,a in new)
        rec={'iteration':it,'columns':len(atoms),'beta':beta,'pricing_minimum_scaled':minimum,'new_columns':count,'contexts':ncache,'seconds':time.time()-t0};history.append(rec);print(json.dumps(rec),flush=True)
        report={'scope':'Numerical discovery necessary-condition relaxation only','row_names':U.names,'atoms':atoms,'primal_float':out.x.tolist()+[0.]*count,'dual_beta_float':beta,'dual_multipliers_float':{n:float(v) for n,v in zip(U.names,lam) if v>1e-10},'history':history}
        (HERE/'root_cg.json').write_text(json.dumps(report,indent=2)+'\n')
        if count==0:break
    return U,out,atoms
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 100)
