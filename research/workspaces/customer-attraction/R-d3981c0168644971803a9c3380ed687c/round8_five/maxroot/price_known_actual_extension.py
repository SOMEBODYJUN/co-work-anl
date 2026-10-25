"""Sparse dual pricing of known old types times all eight actual-HQR states.

This is only the historical known pool. A lack of negative columns here
never certifies the complete allowed customer domain.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import json,hashlib,time,sys
import trueH_own_index_pricing as oi
fc=oi.fc;cm=oi.cm;th=oi.th;sl=fc.sl;HERE=Path(__file__).resolve().parent
import two_real_weighted_branches as ext
import cross_pair_pricing as cp
STATES=list(product((0,1),repeat=3));PREFIX='actual-extension:'

def fake_evaluator():
    U=object.__new__(oi.Universe);U.overlap=1;U.ty=cm.mp.TYPES;U.specs=cm.mp.menu_specs();U.cross=[]
    for source in ('AB','AE'):
        for target in ('AB','AE','Sbranch'):
            if source==target:continue
            k=4 if target=='Sbranch' else 3
            for u,v in combinations_with_replacement(range(k),2):
                for orb in cp.PARTITIONS:U.cross.append((f'crosspair:{source}:{target}:{u}{v}:{orb}',source,target,u,v,orb))
    return U

def sparse_old(a,names):
    base=object.__new__(cm.mp.BaseUniverse);base.overlap=1
    rr=cm.mp.BaseUniverse.atom_rows(base,a);bits=tuple(map(int,a['bits']));b=dict(zip(cm.mp.LABELS,bits));mb=tuple(map(int,a['max_bits']));d=sum(a['AB_hist'][4:]);maxrows=None;out={}
    full=None
    for n in names:
        if n in rr:out[n]=rr[n]
        elif n.startswith('max:'):
            if maxrows is None:maxrows=cm.mj.new_rows(a,mb)
            out[n]=maxrows[n]
        elif n.startswith('APfixed:'):
            _,pn,pos,c,e=n.split(':');p,k,u=cm.mp.source(bits,(pn,int(pos)));cv,nc=(d,5) if c=='opt' else (b[c],1);dv,nd=(d,5) if e=='opt' else (b[e],1);out[n]=cm.mp.ap_value(u,p,k,cv,dv,nc,nd)
        elif n in cm.SPEC:
            spec=cm.SPEC[n];out[n]=cm.one_row(spec,b,d,mb,cm.counts(a,spec[1]))
        elif n in sl.SPEC:
            _,tag,node,dc=sl.SPEC[n];out[n]=sl.row_value(a,tag,node,dc)
        elif n in fc.SPEC:
            node,label=fc.SPEC[n]
            if node=='max':p=sum(mb[:2]);u=cm.lm.q(mb[2],sum(mb))
            else:p,k,u=cm.mp.source(bits,(node,2))
            out[n]=17040*u+1085*mb[0]-F(13395*fc.query(bits,mb,label),p+3)-th.FT[p][d]
        elif n in fc.ISPEC:
            label=fc.ISPEC[n];q=fc.query(bits,mb,label);bg=b['A']
            out[n]=sum((v*(17040*cm.lm.q(t[1],bg+sum(t))+1085*mb[0]-F(13395*q,bg+t[0]+3)-th.FT[bg+t[0]][d]) for v,t in zip(a['second_hist'],cm.mp.TYPES[4])),F(0))
        else:
            if full is None:full=oi.Universe.atom_rows(fake_evaluator(),a)
            out[n]=full[n]
    return out

def extension_row(name,a,state):
    bits=dict(zip(cm.mp.LABELS,map(int,a['bits'])));mb=tuple(map(int,a['max_bits']));p=bits['A']+bits['B'];h,q,r=state;s=p+h+q+r;K=F(h,p+3);vh,vq,vr=(cm.lm.q(t,s) for t in state);tax=vq+vr+F(q,(p+h+1)*(p+h+2));d=sum(a['AB_hist'][4:])
    def query(t):
        if t=='opt':return d,5
        if t.startswith('z'):return mb[int(t[1:])],1
        if t.startswith('f'):return state[int(t[1:])],1
        return bits[t],1
    def cost(c,t,nc,nt):return nc*nt*tax-F(nt*c+nc*t-2*c*t,p+h+1)-F(2*c*t,p+h+2)
    ss=name.split(':')
    if ss[0]=='trueH':
        kind=ss[1]
        if kind=='source-IC':return cm.lm.q(bits['C'],sum(bits[t] for t in 'ABCDE'))-vh
        if kind=='weighted-cap':x,n=query(ss[2]);return n*K-F(x,p+3)
        if kind in ('Q','R'):
            assert ss[2]=='K';x,n=query(ss[3]);return n*(vq if kind=='Q' else vr)-F(x,p+h+2 if kind=='Q' else p+h+q+1)
        if kind=='global-size':return F(mb[0]-state[int(ss[2])])
        if kind=='tax':x,nx=query(ss[2]);y,ny=query(ss[3]);return cost(x,y,nx,ny)
        if kind=='oldK':
            pn,i,j=ss[2],int(ss[3]),int(ss[4]);path=cm.mp.PATHS[pn];u=cm.lm.q(bits[path[i]],sum(bits[t] for t in path));pref=sum(bits[t] for t in path[:i]);return u-F(state[j],pref+5-i)
        if kind=='maxK':
            i,j=int(ss[2]),int(ss[3]);return cm.lm.q(mb[i],sum(mb))-F(state[j],sum(mb[:i])+5-i)
    tag=ss[0];cc=cm.counts(a,tag)
    def mq(t):return (cc[t],5) if t in cc else query(t)
    kind=ss[2]
    if kind=='weighted-cap':return 5*K-F(cc[ss[3]],p+3)
    if kind in ('Q','R') and ss[3]=='K':return 5*(vq if kind=='Q' else vr)-F(cc[ss[4]],p+h+2 if kind=='Q' else p+h+q+1)
    if kind=='Q' and ss[3]=='AP':x,nx=mq(ss[4]);y,ny=mq(ss[5]);return cm.mp.ap_value(vq,p+h,2,x,y,nx,ny)
    if kind=='tax':x,nx=mq(ss[3]);y,ny=mq(ss[4]);return cost(x,y,nx,ny)
    raise ValueError(name)

def run(source=None):
    explicit_source=source is not None
    source=Path(source) if explicit_source else HERE.parent/'certificate/full_actual_extension_discovery.json';known=HERE/'trueH_own_index_discovery.json';src=json.loads(source.read_text());pool=json.loads(known.read_text())['atoms'];weights=src['dual_multipliers_float'];oldw={n:v for n,v in weights.items() if not n.startswith(PREFIX)};neww={n[len(PREFIX):]:v for n,v in weights.items() if n.startswith(PREFIX)};beta=src['dual_beta_float'];oldcache={};scores=[];begin=time.time()
    for index,a in enumerate(pool):
        rr=sparse_old(a,oldw);oldcache[index]=rr;oldscore=sum(w*float(rr[n]) for n,w in oldw.items());base=beta*int(any(map(int,a['bits'][:5])))-int(any(a['AB_hist'][4:]))-oldscore
        for state in STATES:
            residual=base-sum(w*float(extension_row(n,a,state)) for n,w in neww.items());scores.append((residual,index,state))
    scores.sort();negative=[x for x in scores if x[0]<-1e-7]
    # Cross-check selected sparse arithmetic against every original full row.
    U=fake_evaluator();checks=0
    for residual,index,state in negative[:12]:
        a=pool[index];full=oi.Universe.atom_rows(U,a);raw=ext.rows(a,state,'actual');assert all(full[n]==oldcache[index][n] for n in oldw);assert all(raw[n]==extension_row(n,a,state) for n in neww);checks+=len(oldw)+len(neww)
    oldkeys={cm.mp.atom_key(a)+(a['max_bits'],a['actual_HQR_bits']) for a in src['atoms']};cols=[]
    for residual,index,state in negative:
        a=dict(pool[index],actual_HQR_bits=''.join(map(str,state)));key=cm.mp.atom_key(a)+(a['max_bits'],a['actual_HQR_bits'])
        if key in oldkeys:continue
        cols.append({'residual_float':residual,'atom':a})
        if len(cols)==200:break
    out={'scope':__doc__,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'known_pool_sha256':hashlib.sha256(known.read_bytes()).hexdigest(),'known_old_types':len(pool),'priced_columns':len(scores),'active_old_rows':len(oldw),'active_extension_rows':len(neww),'minimum_residual_float':scores[0][0],'negative_columns':len(negative),'sparse_full_coefficient_checks':checks,'new_columns':cols,'seconds':time.time()-begin}
    target=HERE/(f'known_actual_extension_pricing_{source.stem}.json' if explicit_source else 'known_actual_extension_pricing.json')
    target.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'output':str(target),**{k:v for k,v in out.items() if k!='new_columns'}},indent=2))
if __name__=='__main__':run(sys.argv[1] if len(sys.argv)>1 else None)
