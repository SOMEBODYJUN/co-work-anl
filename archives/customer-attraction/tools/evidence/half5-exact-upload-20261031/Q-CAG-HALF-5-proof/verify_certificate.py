"""Portable independent complete-domain arithmetic audit for the five-player proof.

No discovery program, row evaluator, pricing routine, or recovery program is
imported.  Indexed histograms are expanded into five literal branch types.
Off-diagonal and pair rows are reconstructed by their actual index tuples.
All coefficients are integers after the explicit common denominator and 120
share scaling.  Python integers (NumPy dtype=object) prevent overflow.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import ceil,floor
from pathlib import Path
import argparse,hashlib,json,time
import numpy as np

HERE=Path(__file__).resolve().parent
LABELS='ABCDEUVWXY'
PATHS={'actual':'ABCDE','second':'AEUVW','third':'ABEXY'}
FAMILIES=('AB','AE','Sbranch')
SCALE=10**6

def q(n,d):return F(n,d) if n else F(0)
def sc(v):
    r=120*F(v);assert r.denominator==1,r
    return r.numerator
def share(b,path,i):return q(b[path[i]],sum(b[c] for c in path))
def compositions(n,k):
    if k==1:
        yield (n,);return
    for v in range(n+1):
        for h in compositions(n-v,k-1):yield (v,)+h

def source_tables():
    """Reconstruct the documented row tables using only rational arithmetic.

    PC indices are explicit: the five priced-player-2 facets in their frozen
    file order, followed by the three priced-player-3 facets in file order.
    No floating discovery metadata or numerical sorting is used.
    """
    paths={
      'BG2':HERE/'components/background_player2.json',
      'BG3':HERE/'components/background_player3.json',
      'PC2':HERE/'components/priced_player2.json',
      'PC3':HERE/'components/priced_player3.json',
      'DEEP':HERE/'components/deep_root_query.json',
      'MAXROOT':HERE/'components/maxroot_four_copy.json'}
    raw={k:json.loads(p.read_text()) for k,p in paths.items()}
    bg=[]
    for idx in [0,1,3,5,11,12]:
        c=raw['BG2'][idx]
        bg.append((ceil(SCALE*F(c['Kcoef'])),[0]+[floor(SCALE*F(x)) for x in c['margin_coefs']],1))
    for c in raw['BG3'][:3]:
        bg.append((ceil(SCALE*F(c['beta_K'])),[floor(SCALE*F(x)) for x in c['gamma_ABTQ']],2))
    assert len(raw['PC2'])==5 and len(raw['PC3'])==3
    pcs=raw['PC2']+raw['PC3']
    pc=[]
    for c in pcs:
        g=[floor(SCALE*F(x)) for x in c.get('gamma',c.get('gamma_ABCDTQ',c.get('margin_coefs')))];g=([0]+g if len(g)==63 else g)
        u=[ceil(SCALE*F(x)) for x in c.get('u_coefs',c.get('u_coefficients'))]
        if 'u_coefs' in c:u[1]+=SCALE
        assert len(g)==64 and len(u)==5
        pc.append((ceil(SCALE*F(c['Kcoef'])),g,u))
    deep=[]
    for c in raw['DEEP']:
        a,k,g,z=[F(c[n]) for n in ('alpha','beta','gamma','zeta')]
        deep.append((ceil(SCALE*a),ceil(SCALE*k),ceil(SCALE*g),SCALE,ceil(SCALE*z)))
    root=raw['MAXROOT'][0]
    assert (ceil(SCALE*F(root['B'])),ceil(SCALE*F(root['C'])))==(46313177,-7412362)
    return bg,pc,deep,{k:{'path':str(p.relative_to(HERE)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for k,p in paths.items()}

class LiteralDomain:
    def __init__(self,bg,pc,deep):
        self.bg,self.pc,self.deep=bg,pc,deep
        self.hist={};self.expanded={};self.ids={};self.features={}
        for k in (3,4):
            ty=np.array(list(product((0,1),repeat=k)),dtype=np.int64)
            hist=list(compositions(5,2**k));self.hist[k]=hist
            # The order is only a representative of the histogram. Every row
            # used here sums over indices symmetrically and is invariant under
            # permutations of all five branches together.
            exp=np.array([[ty[j] for j,n in enumerate(h) for _ in range(n)] for h in hist],dtype=np.int64)
            self.expanded[k]=exp;ds=exp[:,:,0].sum(axis=1)
            self.ids[k]=[np.flatnonzero(ds==d) for d in range(6)]
            for p in range(3 if k==3 else 2):self.make_features(k,p)

    def make_features(self,k,p):
        e=self.expanded[k];n=len(e);feat={};loads=p+e.sum(axis=2)
        def frac_grid(num,den):
            out=np.zeros_like(den,dtype=np.int64)
            for d in range(1,6):out=np.where(den==d,(120//d)*num,out)
            assert not np.any((num!=0)&(den==0))
            return out
        branchshares=[frac_grid(e[:,:,i],loads) for i in range(k)]
        for i in range(k):
            feat[f'm{i}']=120*e[:,:,i].sum(axis=1)
            feat[f'sh{i}']=branchshares[i].sum(axis=1)
            for j in range(k):
                feat[f'e{i},{j}']=120*(e[:,:,i]*e[:,:,j]).sum(axis=1)
                feat[f'a{i},{j}']=120*e[:,:,i].sum(axis=1)*e[:,:,j].sum(axis=1)
        for pos in range(1,k):
            den=p+e[:,:,:pos].sum(axis=2)+k-pos
            floor_unit=frac_grid(np.ones_like(den),den)
            feat[f'den{pos}']=floor_unit.sum(axis=1)
            for query in range(k):
                # Every source branch compares all five legal query topics.
                val=np.zeros(n,dtype=np.int64)
                off=np.zeros(n,dtype=np.int64)
                own=np.zeros(n,dtype=np.int64)
                for i in range(5):
                    own+=branchshares[pos][:,i]-e[:,i,query]*floor_unit[:,i]
                    for j in range(5):
                        term=branchshares[pos][:,i]-e[:,j,query]*floor_unit[:,i]
                        val+=term
                        if i!=j:off+=term
                feat[f'floorall:{pos}:{query}']=val
                feat[f'floorown:{pos}:{query}']=own
                feat[f'flooroff:{pos}:{query}']=off
        pref=p+e[:,:,:k-2].sum(axis=2)
        A=frac_grid(np.ones_like(pref),pref+1)
        # Denominators here are 2,6,12,20; all divide 120.
        G=np.zeros_like(pref,dtype=np.int64)
        for b in range(4):G=np.where(pref==b,120//((b+1)*(b+2)),G)
        H=branchshares[-2]+branchshares[-1]+e[:,:,-2]*G
        feat['pair_H']=H.sum(axis=1)
        feat['pair_A']=A.sum(axis=1)
        feat['pair_G']=G.sum(axis=1)
        # Store primitive per-index arrays. Pair features are computed only
        # when a certificate actually uses the corresponding equality pattern.
        feat['_pair_primitives']=(A,G,H)
        self.features[k,p]=feat

    def pair_feature(self,k,p,u,v,pattern):
        feat=self.features[k,p];key=f'pair:{u}{v}:{pattern}'
        if key in feat:return feat[key]
        e=self.expanded[k];A,G,H=feat['_pair_primitives'];out=np.zeros(len(e),dtype=np.int64)
        for i,j,l in product(range(5),repeat=3):
            ok={'all_equal':i==j==l,
                'query_equal':j==l and i!=j,
                'first_branch':i==j and i!=l,
                'second_branch':i==l and i!=j,
                'all_distinct':len({i,j,l})==3}[pattern]
            if ok:out+=H[:,i]-(e[:,j,u]+e[:,l,v])*A[:,i]+e[:,j,u]*e[:,l,v]*G[:,i]
        feat[key]=out
        return out

    def bg_parts(self,b,e):
        kap,g,player=self.bg[e];h=b['A'] if player==1 else 2*b['A']+b['B'];g=g[4*h:4*h+4]
        return kap,SCALE*share(b,PATHS['actual'],player),g

    def pc_parts(self,b,e):
        kap,g,uc=self.pc[e];h=8*b['A']+4*b['B']+2*b['C']+b['D'];g=g[4*h:4*h+4]
        return kap,sum(uc[i]*share(b,PATHS['actual'],i) for i in range(5)),g

    def projected_fixed(self,kind,parts,b,d):
        e=int(parts[0]);kap,u,g=(self.bg_parts if kind=='BG' else self.pc_parts)(b,e)
        c0=g[0];ct=g[2]-g[0];cq=g[1]-g[0];both=g[3]-g[2]-g[1]+g[0]
        if parts[1].isdigit():
            t=b[LABELS[int(parts[1])]];v=b[LABELS[int(parts[2])]]
            return u-c0-ct*t-cq*v-both*t*v,kap
        if parts[1]=='fixed-opt':
            t=b[LABELS[int(parts[2])]];return 5*u-5*c0-5*ct*t-cq*d-both*t*d,5*kap
        if parts[1]=='opt-fixed':
            v=b[LABELS[int(parts[2])]];return 5*u-5*c0-ct*d-5*cq*v-both*d*v,5*kap
        if parts[1]=='opt-opt':return 25*u-25*c0-5*(ct+cq)*d-both*d*d,25*kap
        if parts[1]=='opt-offdiag':return 20*u-20*c0-4*(ct+cq)*d-both*d*(d-1),20*kap
        raise ValueError((kind,parts))

    def fixed_value(self,name,b,d,menus):
        z=name.split(':');kind=z[0]
        if kind in ('BG','PC'):return self.projected_fixed(kind,z[1:],b,d)
        if kind=='MAX':
            assert z[1]=='fixed';return -b[LABELS[int(z[2])]],1
        if name=='MAXROOT-NEW':return 46313177*share(b,PATHS['actual'],0)-SCALE*int(d>0),-7412362
        if name=='MAX-BACKGROUND-P2':return 29225304*share(b,PATHS['actual'],1)+2139529*b['A']-SCALE*int(d>0),-5220246
        if kind=='DEEP':
            a,kap,g,s,zeta=self.deep[int(z[1])];u=share(b,PATHS['actual'],0)
            if z[2].isdigit():
                t=b[LABELS[int(z[2])]];v=b[LABELS[int(z[3])]];return a*u+g*t-s*v+(s+zeta)*t*v,kap
            if z[2]=='fixed-opt':
                t=b[LABELS[int(z[3])]];return 5*a*u+5*g*t-s*d+(s+zeta)*t*d,5*kap
            if z[2]=='opt-fixed':
                v=b[LABELS[int(z[3])]];return 5*a*u+g*d-5*s*v+(s+zeta)*d*v,5*kap
            assert z[2]=='opt-opt';return 25*a*u+5*(g-s)*d+(s+zeta)*d*d,25*kap
        if kind=='F':
            i={'second':1,'third':2}[z[1]];return share(b,PATHS['actual'],i)-share(b,PATHS[z[1]],i),0
        path=PATHS[kind]
        if z[1]=='reply':
            p=sum(b[s] for s in path[:3]);den=(p+1)*(p+2);ell,h=menus[list(PATHS).index(kind)];tag=z[2]
            if tag=='S':v=5*share(b,path,3)-F(d,p+1)+F(h,den)
            elif tag=='V':v=F(d*ell-5*h,den)
            elif tag=='Z':v=5*share(b,path,4)-F(ell,p+b[path[3]]+1)
            elif tag=='P':v=5*share(b,path,4)-F(d,p+b[path[3]]+1)
            elif tag=='clone-opt':v=F(ell,p+1)-F(h,den)-F(d,p+2)
            elif tag=='all-opt':v=F(5*(ell-d),p+1)+F(d*d-5*h,den)
            elif tag.startswith('cross-L-'):
                other=menus[list(PATHS).index(tag.removeprefix('cross-L-'))][0];v=F(5*(ell-other),p+1)+F(d*other-5*h,den)
            elif tag.startswith('topic-'):
                x=b[tag.removeprefix('topic-')];v=F(ell-5*x,p+1)+F(d*x-h,den)
            else:raise ValueError(name)
            return v,0
        if z[1]=='r2':
            p=sum(b[s] for s in path[:3]);H=share(b,path,3)+share(b,path,4)+F(b[path[3]],(p+1)*(p+2))
            if z[2]=='O':return F(5,2)*H+F(p,p+1)-int(d>0),0
            assert z[2]=='exact-opt';return 10*H-F(d*(5-d),p+1)-F(d*(d-1),p+2),0
        i=int(z[1])-1;p=sum(b[s] for s in path[:i]);remain=5-i;u=share(b,path,i)
        if z[2]=='K':return u-F(b[z[3]],p+remain),0
        if z[2]=='O':return 5*remain*u+F(p,p+remain)-int(d>0),0
        if z[2]=='sum-opt':return 5*u-F(d,p+remain),0
        if z[2].startswith('sum-L-'):
            ell=menus[list(PATHS).index(z[2].removeprefix('sum-L-'))][0];return 5*u-F(ell,p+remain),0
        raise ValueError(name)

    def family_parts(self,tag,b,weights):
        """Return a constant and an exact linear combination of fixed features."""
        k=4 if tag=='Sbranch' else 3;p=b['A']+(b['B'] if tag=='AB' else b['E'] if tag=='AE' else 0)
        feat=self.features[k,p];co=defaultdict(int);const=0;kap=0
        for name,w in weights.items():
            z=name.split(':');z=z[1:] if z[0]==tag else z
            if z[0] in ('BG','PC'):
                e=int(z[1]);way=z[2];i=int(z[3]);j=int(z[4]);kk,u,g=(self.bg_parts if z[0]=='BG' else self.pc_parts)(b,e)
                c0=g[0];ct=g[2]-g[0];cq=g[1]-g[0];both=g[3]-g[2]-g[1]+g[0]
                if way=='MF':
                    v=b[LABELS[j]];const+=w*sc(5*u-5*c0-5*cq*v);co[f'm{i}']-=w*(ct+both*v);kap+=5*w*kk
                elif way=='FM':
                    t=b[LABELS[j]];const+=w*sc(5*u-5*c0-5*ct*t);co[f'm{i}']-=w*(cq+both*t);kap+=5*w*kk
                elif way=='eq':
                    const+=w*sc(5*u-5*c0);co[f'm{i}']-=w*ct;co[f'm{j}']-=w*cq;co[f'e{i},{j}']-=w*both;kap+=5*w*kk
                elif way=='all':
                    const+=w*sc(25*u-25*c0);co[f'm{i}']-=5*w*ct;co[f'm{j}']-=5*w*cq;co[f'a{i},{j}']-=w*both;kap+=25*w*kk
                else:raise ValueError(name)
            elif z[0] in ('F2','F3'):
                path=PATHS['second' if tag=='AE' else 'actual'];i=1 if k==4 else 2
                const+=w*sc(5*share(b,path,i));co['sh0']-=w
            elif z[0] in PATHS:
                path=PATHS[z[0]];i=int(z[1])-1;menu=z[2].removeprefix('sum-').removeprefix('S');pos=('TUVW' if k==4 else 'TXY').index(menu)
                assert z[2].startswith('sum-'),name
                const+=w*sc(5*share(b,path,i))
                # Feature m is scaled 120; coefficient 1/den may be rational.
                # Use a separate exact integer count feature to avoid that.
                rawkey=f'count{pos}'
                if rawkey not in feat:feat[rawkey]=self.expanded[k][:,:,pos].sum(axis=1)
                co[rawkey]-=w*sc(F(1,sum(b[s] for s in path[:i])+5-i))
            elif z[0]=='pair':
                u,v=map(int,z[1]);key=f'pair:{u}{v}:{z[2]}';self.pair_feature(k,p,u,v,z[2]);co[key]+=w
            elif z[0] in ('3','4','5'):
                seat=int(z[0]);pos=seat-(6-k)
                if z[1]=='K':co[f'sh{pos}']+=w;co[f'den{pos}']-=w*b[z[2]]
                elif z[1]=='offdiag':co[f'flooroff:{pos}:{int(z[2])}']+=w
                elif z[1].startswith('sum-'):
                    menu=z[1].removeprefix('sum-');query=0 if menu=='opt' else ('TUVW' if k==4 else 'TXY').index(menu)
                    co[f'floorall:{pos}:{query}']+=w
                elif z[1].startswith('own-'):
                    query=('TUVW' if k==4 else 'TXY').index(z[1].removeprefix('own-'));co[f'floorown:{pos}:{query}']+=w
                else:raise ValueError(name)
            else:raise ValueError(name)
        return (k,p,tuple(sorted((f,v) for f,v in co.items() if v))),const,kap

def load_certificate(path):
    data=path.read_bytes();src=json.loads(data);src['_loaded_sha256']=hashlib.sha256(data).hexdigest()
    weights={n:int(v) for n,v in src['integer_multipliers'].items() if int(v)}
    D=int(src['common_denominator']);B=int(src['beta_numerator'])
    assert weights and min(weights.values())>0 and 0<B<=2*D
    return src,weights,B,D,'exact supplied dual'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('certificate',type=Path,nargs='?',default=HERE/'certificate.json');ap.add_argument('--output',type=Path,default=HERE/'verification_report.json');ap.add_argument('--manifest',type=Path);args=ap.parse_args()
    start=time.monotonic();src,weights,B,D,mode=load_certificate(args.certificate)
    bg,pc,deep,sources=source_tables();manifest={'BG':bg,'PC':pc,'DEEP':deep,'sources':sources}
    if args.manifest:
        supplied=json.loads(args.manifest.read_text())
        for key in ('BG','PC','DEEP'):assert json.loads(json.dumps(manifest[key]))==supplied[key],key
        for key,record in supplied.get('sources',{}).items():assert record['sha256']==sources[key]['sha256'],key
    domain=LiteralDomain(bg,pc,deep)
    fixed={};family={tag:{} for tag in FAMILIES}
    for n,v in weights.items():
        tag=n.split(':')[0]
        if tag in family:family[tag][n]=v
        elif ':sum-S' in n:family['Sbranch'][n]=v
        else:fixed[n]=v
    menu_fixed={n:w for n,w in fixed.items() if ':reply:' in n or ':sum-L-' in n}
    cache={};minimum=None;zero=0;neg=[];byactual={};sample=[];kcoef=None
    for mask in product((0,1),repeat=10):
        b=dict(zip(LABELS,mask));maxima=[];currentkap=0
        for tag in FAMILIES:
            key,const,kap=domain.family_parts(tag,b,family[tag]);k,p,terms=key;currentkap+=kap
            if key not in cache:
                score=np.zeros(len(domain.hist[k]),dtype=object)
                for f,v in terms:score+=v*domain.features[k,p][f].astype(object)
                vals=[];choices=[]
                for ids in domain.ids[k]:
                    chosen=max(ids,key=lambda ix:score[ix]);vals.append(int(score[chosen]));choices.append(int(chosen))
                cache[key]=(vals,choices)
            maxima.append([x+const for x in cache[key][0]])
        # All remaining menu variables enter affinely. Their full feasibility
        # polygon is 0<=h<=d and 0<=ell-h<=5-d, with these four corners.
        for d in range(6):
            base=0;K=currentkap;menus0=[(0,0)]*3
            for n,w in fixed.items():
                value,kap=domain.fixed_value(n,b,d,menus0);base+=w*sc(value);K+=w*kap
            if kcoef is None:kcoef=K
            assert K==kcoef,('K coefficient must be a single scalar',mask,d,K,kcoef)
            extra=0
            for f in range(3):
                candidates=[]
                for ell,h in ((0,0),(d,d),(5-d,0),(5,d)):
                    menus=menus0.copy();menus[f]=(ell,h);value=0
                    for n,w in menu_fixed.items():
                        v,_=domain.fixed_value(n,b,d,menus);v0,_=domain.fixed_value(n,b,d,menus0);value+=w*sc(v-v0)
                    candidates.append(value)
                extra+=max(candidates)
            residual=120*(B*int(any(mask[:5]))-D*int(d>0))-base-extra-sum(a[d] for a in maxima)
            assert isinstance(residual,int)
            minimum=residual if minimum is None else min(minimum,residual);zero+=residual==0
            actual=''.join(map(str,mask[:5]));byactual[actual]=min(byactual.get(actual,residual),residual)
            if residual<0:neg.append({'bits':''.join(map(str,mask)),'d':d,'residual':str(residual)})
        if sum(mask)==0:print(json.dumps({'initialized':True,'seconds':time.monotonic()-start,'weights':len(weights)}),flush=True)
    report={'status':'passed' if not neg and kcoef<=0 else 'failed',
      'scope':'Independent exact complete-domain certificate check; no discovery or existing row-evaluation imports',
      'certificate_sha256':src['_loaded_sha256'],'mode':mode,
      'beta':str(F(B,D)),'positive_multipliers':len(weights),'common_denominator':str(D),
      'fixed_masks':1024,'shared_optimal_multiplicities':6,'conditional_cases':6144,
      'histograms_per_third_family':len(domain.hist[3]),'histograms_second_family':len(domain.hist[4]),
      'menu_corners_per_family':4,'cache_contexts':len(cache),
      'minimum_scaled_integer_residual':str(minimum),'zero_cases':zero,
      'K_column_residual':str(-kcoef),'minimum_by_actual_mask':{k:str(v) for k,v in byactual.items()},
      'negative_cases':neg,'source_lemmas':sources,'seconds':time.monotonic()-start}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    args.output.with_name(args.output.stem+'_row_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('negative_cases','minimum_by_actual_mask','source_lemmas')},indent=2))
    assert not neg and kcoef<=0,(len(neg),minimum,kcoef)

if __name__=='__main__':main()
