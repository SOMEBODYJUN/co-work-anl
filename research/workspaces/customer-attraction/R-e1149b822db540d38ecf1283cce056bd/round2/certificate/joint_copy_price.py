"""All-type floating separation for sparse cross-copy support.
Full domain, but floating discovery only: no rational certificate is claimed.
"""
from pathlib import Path
from itertools import product
import sys,json,time
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import joint_copy_restricted as j
c=j.c;old=c.old

def Q(n,d):
    n,d=np.broadcast_arrays(n,d)
    return np.divide(n,d,out=np.zeros(n.shape,dtype=float),where=n!=0)

def unary(bits,src,weights,L,H):
    b=dict(zip(c.LABELS,bits));pre,forced=c.SPECS[src]
    cb=[np.asarray(c.STATES[src])[None,None,:,k] for k in range(c.TAILS[src])]
    path=[*(b[x] for x in pre),b[forced],*cb];total=sum(path);us=[Q(x,total) for x in path]
    out=np.zeros((6,64,len(c.STATES[src])));ds=np.arange(6)[:,None,None]
    labels={**b,**dict(zip('fghi',cb))};st=c.FIRST[src]
    for n,v in weights:
        z=n.split(':')
        if z[0]=='forced-IC':
            act=c.PATHS['actual'];k=st-1;val=Q(b[act[k]],sum(b[x] for x in act))-us[k]
        elif z[0]=='old':
            pn,ii,lab=z[1:];i=int(ii);act=c.PATHS[pn]
            val=Q(b[act[i]],sum(b[x] for x in act))-Q(labels[lab],sum(b[x] for x in act[:i])+5-i)
        elif z[0].isdigit():
            i=int(z[0]);assert z[1]=='K';val=us[i]-Q(labels[z[2]],sum(path[:i])+5-i)
        elif z[0]=='r2':
            p=sum(path[:3]);hh=us[3]+us[4]+Q(path[3],(p+1)*(p+2))
            if z[1]=='O':val=2.5*hh+Q(p,p+1)-(ds>0)
            elif z[1]=='pair':
                x,y=(labels[q] for q in z[2:]);val=hh-Q(x+y-2*x*y,p+1)-Q(2*x*y,p+2)
            else:raise ValueError(n)
        elif z[0]=='queryL':
            i=int(z[1]);fi=list(c.PATHS).index(z[2]);val=5*us[i]-Q(L[:,:,fi,None],sum(path[:i])+5-i)
        elif z[0]=='lastmenu':
            pn,lab=z[1:];fi=list(c.PATHS).index(pn);p=sum(b[x] for x in c.PATHS[pn][:3]);x=labels[lab]
            val=Q(L[:,:,fi,None]-5*x,p+1)+Q(ds*x-H[:,:,fi,None],(p+1)*(p+2))
        else:raise ValueError(n)
        out+=120*v*val
    return out,path,us

ORDER=tuple(c.ROOTS)
ELIM=('D2','D3','D','B','C','E')

def maxjoint(unaries,pairs):
    factors=[((s,),v) for s,v in unaries.items()]+[(ss,v[None,None,:,:]) for ss,v in pairs.items()]
    records=[]
    for x in ELIM:
        group=[f for f in factors if x in f[0]];factors=[f for f in factors if x not in f[0]]
        scope=tuple(s for s in ORDER if any(s in ss for ss,a in group))
        shape=(6,64)+tuple(len(c.STATES[s]) for s in scope)
        val=np.zeros(shape)
        for ss,a in group:
            reshape=a.shape[:2]+tuple(len(c.STATES[s]) if s in ss else 1 for s in scope)
            val+=a.reshape(reshape)
        axis=2+scope.index(x);arg=np.argmax(val,axis=axis);newscope=tuple(s for s in scope if s!=x)
        factors.append((newscope,np.max(val,axis=axis)));records.append((x,newscope,arg))
    assert all(ss==() for ss,a in factors)
    return sum(a for ss,a in factors),records

def recover(records,d,m):
    states={}
    for x,ss,arg in records[::-1]:states[x]=int(arg[(d,m)+tuple(states[s] for s in ss)])
    return {s:list(c.STATES[s][states[s]]) for s in ORDER}

def run():
    t0=time.time();data=json.loads((HERE/'joint_copy_restricted_all.json').read_text());weights=data['dual_multipliers_float'];beta=data['restricted_beta_float']
    old.VE['q']=Q;c.fixed_rows.__globals__['base'].VE['q']=Q
    U=old.Universe(1)
    ow=np.array([weights.get(n,0) for n in U.oldnames]);fixed=U.base@ow;EC=U.ec@ow;HC=U.hc@ow
    ap=[(n,v) for n,v in weights.items() if n.startswith('Root:')]
    for bi,bits in enumerate(U.bits):
        b=dict(zip(c.LABELS,bits));r=old.q(b['A'],sum(b[x] for x in 'ABCDE'))
        for n,v in ap:
            _,_,pn,ii,cc,dd=n.split(':');i=int(ii);k=5-i;aa=8*(k-1)+k*k;p=sum(b[x] for x in c.PATHS[pn][:i]);x,y=b[cc],b[dd]
            val=aa*old.q(b[c.PATHS[pn][i]],sum(b[x] for x in c.PATHS[pn]))-old.q((aa-2)*x+2*x*y,p+k)-old.q(2*y*(1-x),p+1)
            fixed[bi]+=120*v*float(val)
    fam={t:[] for t in ('AB','AE','Sbranch')}
    for n,v in weights.items():
        tag=n.split(':')[0]
        if tag in fam:fam[tag].append((n,v))
        elif ':sum-S' in n:fam['Sbranch'].append((n,v))
    cp={s:[(n.split(':',1)[1],v) for n,v in weights.items() if n.startswith('Copy'+s+':')] for s in ORDER}
    joint=[(n.split(':')[1:],v) for n,v in weights.items() if n.startswith('Joint:')]
    ML=[];MH=[]
    for d in range(6):
        menus=list(product([(0,0),(d,d),(5-d,0),(5,d)],repeat=3))
        ML.append([[z[0] for z in mm] for mm in menus]);MH.append([[z[1] for z in mm] for mm in menus])
    ML=np.array(ML);MH=np.array(MH)
    cache={};best=[];minimum=1e100
    for bi,bits in enumerate(U.bits):
        b=dict(zip(c.LABELS,bits));fs=[];E=EC[bi].copy();H=HC[bi].copy();choices=[]
        for tag in fam:
            key,con,vec,me,mh=U.family_score(bits,tag,fam[tag]);k=key[0]
            if key not in cache:
                score=np.zeros(len(U.hist[k]))
                for v,a in vec:score+=v*a
                vals=[];ids=[]
                for ii in U.ids[k]:
                    arg=ii[int(np.argmax(score[ii]))];vals.append(score[arg]);ids.append(int(arg))
                cache[key]=(np.asarray(vals),ids)
            val,ids=cache[key];fs.append(val+con);choices.append(ids);E+=me.T;H+=mh.T
        un={};paths={};us={}
        for s in ORDER:un[s],paths[s],us[s]=unary(bits,s,cp[s],ML,MH)
        pairs={}
        for (s,ii,t,jj),v in joint:
            i=int(ii);jj=int(jj);un[s]+=120*v*us[s][i]
            scope=tuple(x for x in ORDER if x in (s,t));raw=-120*v*np.broadcast_to(Q(1,sum(paths[s][:i])+5-i),(1,1,len(c.STATES[s]))).reshape(-1,1)*np.asarray(c.STATES[t])[:,jj].reshape(1,-1)
            if scope!=(s,t):raw=raw.T
            pairs[scope]=pairs.get(scope,0)+raw
        score,records=maxjoint(un,pairs)
        score+=np.einsum('dmf,df->dm',ML,E)+np.einsum('dmf,df->dm',MH,H)
        for d in range(6):
            mi=int(np.argmax(score[d]));rho=120*(beta*int(any(bits[:5]))-int(d>0))-fixed[bi,d]-sum(v[d] for v in fs)-score[d,mi]
            minimum=min(minimum,float(rho))
            if rho<-1e-7:
                a={'bits':''.join(map(str,bits)),'AB_hist':list(U.hist[3][choices[0][d]]),'AE_hist':list(U.hist[3][choices[1][d]]),'second_hist':list(U.hist[4][choices[2][d]]),'menus_lh':list(zip(ML[d,mi].tolist(),MH[d,mi].tolist())),'copies':recover(records,d,mi)}
                best.append((float(rho),a))
        if bi%128==0:print(json.dumps({'priced_masks':bi,'minimum_scaled_residual_float':minimum,'seconds':time.time()-t0}),flush=True)
    best.sort(key=lambda z:z[0]);test=object.__new__(c.Universe)
    for rho,a in best[:10]:
        rr=test.atom_rows(a,False);rr.update(j.cross_rows(a));direct=120*(beta*int(any(map(int,a['bits'][:5])))-int(any(a['AB_hist'][4:]))) -120*sum(v*float(rr[n]) for n,v in weights.items())
        assert abs(direct-rho)<1e-6,(direct,rho)
    out={'scope':__doc__,'beta_float':beta,'minimum_scaled_residual_float':minimum,'negative_columns':len(best),'new_atoms':[{'scaled_residual_float':v,'atom':a} for v,a in best[:100]],'seconds':time.time()-t0,'coefficient_domain':{'fixed_masks':1024,'optimal_multiplicities':6,'shared_menu_vertices':64,'branch_domains':[len(c.STATES[s]) for s in ORDER]},'exact_certificate':False}
    (HERE/'joint_copy_pricing.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='new_atoms'}),flush=True)
if __name__=='__main__':run()
