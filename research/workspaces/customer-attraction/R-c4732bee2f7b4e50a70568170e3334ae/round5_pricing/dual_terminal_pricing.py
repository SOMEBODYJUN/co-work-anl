"""737-row full pricing: AB and AE final-menu cross-family envelopes."""
from terminal_cross_pricing import *

class DualTerminalUniverse(TerminalUniverse):
    def __init__(self):
        super().__init__();self.single=[]
        for source in ('AB','AE'):
            for target in ('AB','AE','Sbranch'):
                if source==target:continue
                for pos in range(1,4 if target=='Sbranch' else 3):
                    for kind in ('D','O'):self.single.append((f'crossfinal:{source}:{target}:{pos}{kind}',source,target,pos,kind))
        self.names=self.names[:717]+[z[0] for z in self.single]
        print(json.dumps({'dual_source_terminal_rows':len(self.single),'total_rows':len(self.names)}),flush=True)
    def atom_rows(self,atom):
        rr=CrossUniverse.atom_rows(self,atom)
        for n,source,target,pos,kind in self.single:rr[n]=joint_row(atom,source,'second' if target=='Sbranch' else target,((pos,kind,F(1)),))
        return rr
    def price(self,lam,beta,batch=80,integer=False,objective_scale=1):
        dtype=object if integer=='object' else np.int64 if integer else float
        self.crossweights=[(*row,int(w) if integer else float(w)) for row,w in zip(self.cross,lam[557:717]) if abs(w)>1e-11];self.extra_cache={}
        sw=[(*row,int(w) if integer else float(w)) for row,w in zip(self.single,lam[717:]) if abs(w)>1e-11]
        weights=[(n,int(v) if integer else float(v)) for n,v in zip(self.names[:717],lam[:717]) if abs(v)>1e-11];fam={t:[] for t in ('AB','AE','Sbranch')}
        for n,v in weights:
            tag=n.split(':')[0]
            if tag in fam:fam[tag].append((n,v))
            elif ':sum-S' in n:fam['Sbranch'].append((n,v))
        ow=np.asarray(lam,dtype=dtype)[self.oldids];base=self.base@ow;EC=self.ec@ow;HC=self.hc@ow
        cache={};best=[];minimum=None;ownw={tag:sum(w*(1 if kind=='D' else 4) for _,source,target,pos,kind,w in sw if source==tag) for tag in ('AB','AE')}
        for bi,bits in enumerate(self.bits):
            vectors={};keys={};consts={};E=EC[bi].copy();H=HC[bi].copy();pp={'AB':bits[0]+bits[1],'AE':bits[0]+bits[4]}
            for tag in fam:
                key,const,vec,me,mh=self.family_score(bits,tag,fam[tag],integer=integer);k=key[0];keys[tag]=key;consts[tag]=const;E+=me.T;H+=mh.T
                if key not in cache:
                    score=np.zeros(len(self.hist[k]),dtype=dtype)
                    for v,a in vec:score+=v*(a.astype(object) if integer=='object' else a)
                    cache[key]=score
                vectors[tag]=cache[key]
                if tag in ownw:vectors[tag]=vectors[tag]+ownw[tag]*(self.M[3,pp[tag]]['zy'].astype(object) if integer=='object' else self.M[3,pp[tag]]['zy'])
            for d in range(6):
                states=[(h0,h1) for h0 in range(6-d) for h1 in range(d+1)]
                twoway={}
                for target,source in (('AB','AE'),('AE','AB')):
                    tables={}
                    for hs in states:
                        ck=('twoway',keys[target],target,pp[target],pp[source],d,hs)
                        if ck not in cache:
                            score=vectors[target].copy()
                            for _,ss,tt,pos,kind,w in sw:
                                if tt==target:
                                    a=self.qcost[3,pp[ss],d,*hs,pos,kind];score+=w*(a.astype(object) if integer=='object' else a)
                            vals={}
                            for ht in states:
                                ids=self.condids[d,*ht];arg=int(ids[np.argmax(score[ids])]);vals[ht]=(score[arg],arg)
                            cache[ck]=vals
                        tables[hs]=cache[ck]
                    twoway[target]=tables
                fbest=None;fidx=None
                for ha in states:
                    for he in states:
                        va,ia=twoway['AB'][he][ha];ve,ie=twoway['AE'][ha][he];ck=('second',keys['Sbranch'],pp['AB'],pp['AE'],d,ha,he)
                        if ck not in cache:
                            score=vectors['Sbranch'].copy()
                            for _,ss,tt,pos,kind,w in sw:
                                if tt=='Sbranch':
                                    hs=ha if ss=='AB' else he;a=self.qcost[4,pp[ss],d,*hs,pos,kind];score+=w*(a.astype(object) if integer=='object' else a)
                            ids=self.ids[4][d];arg=int(ids[np.argmax(score[ids])]);cache[ck]=(score[arg],arg)
                        vs,isec=cache[ck];value=va+ve+vs+sum(consts.values())
                        if fbest is None or value>fbest:fbest=value;fidx=[ia,ie,isec]
                menus=0;lhs=[]
                for f in range(3):
                    corners=[(0,0),(d,d),(5-d,0),(5,d)];lh=max(corners,key=lambda z:z[0]*E[d,f]+z[1]*H[d,f]);lhs.append(lh);menus+=lh[0]*E[d,f]+lh[1]*H[d,f]
                residual=120*(beta*int(any(bits[:5]))-objective_scale*int(d>0))-base[bi,d]-menus-fbest;minimum=residual if minimum is None else min(minimum,residual)
                if residual<(0 if integer else -1e-7):best.append((residual,{'bits':''.join(map(str,bits)),'AB_hist':list(self.hist[3][fidx[0]]),'AE_hist':list(self.hist[3][fidx[1]]),'second_hist':list(self.hist[4][fidx[2]]),'menus_lh':lhs}))
        best.sort(key=lambda z:z[0])
        for residual,atom in best[:batch]:
            rr=self.atom_rows(atom);rho=120*(beta*int(any(map(int,atom['bits'][:5])))-objective_scale*int(any(atom['AB_hist'][4:])))
            rho-=120*sum((int(v)*rr[n] if integer else float(v)*float(rr[n])) for n,v in zip(self.names,lam));assert abs(rho-residual)<F(1,10**6),(rho,residual)
        return minimum,best[:batch],len(cache)

def run(maxiter=100):
    U=DualTerminalUniverse();src=json.loads((HERE/'cg_terminal_cross_final.json').read_text());atoms=[];keys=set();cols=[];w=[];o=[]
    def add(a):
        key=atom_key(a)
        if key in keys:return False
        rr=U.atom_rows(a);cols.append([float(rr[n]) for n in U.names]);atoms.append(a);keys.add(key);w.append(int(any(map(int,a['bits'][:5]))));o.append(int(any(a['AB_hist'][4:])));return True
    checkpoint=HERE/'cg_dual_terminal.json'
    if checkpoint.exists():src=json.loads(checkpoint.read_text())
    for a in src['atoms']:add(a)
    history=[]
    for it in range(maxiter):
        t0=time.time();mat=np.asarray(cols).T;out=linprog(-np.asarray(o,dtype=float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[w],b_eq=[1.],bounds=(0,None),method='highs');assert out.success,out.message
        beta=-out.fun;lam=-out.ineqlin.marginals;minimum,new,contexts=U.price(lam,beta);count=sum(add(a) for _,a in new);rec={'iteration':it,'columns':len(atoms),'beta':beta,'pricing_minimum_scaled':float(minimum),'new_columns':count,'score_contexts':contexts,'seconds':time.time()-t0};history.append(rec);print(json.dumps(rec),flush=True)
        checkpoint.write_text(json.dumps({'scope':'737-row necessary-condition template; no SPE or true OPT claim','row_names':U.names,'atoms':atoms,'primal_float':out.x.tolist()+[0.]*count,'dual_beta_float':beta,'dual_multipliers_float':{n:float(v) for n,v in zip(U.names,lam) if v>1e-10},'history':history},indent=2)+'\n')
        if count==0:break
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 100)
