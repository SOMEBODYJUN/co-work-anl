"""Five-player global size-cap transfer into true off-history AP rows.

Discovery only. See global_size_cap_exchange.md for the exact necessary row.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import ap_binary_pricing as ap
base=ap.base
RPOS,TYPES,sc,q,PATHS=ap.RPOS,ap.TYPES,ap.sc,ap.q,ap.PATHS
LABELS=ap.LABELS
old_fast_rows=ap.fast_rows

def global_rows(bits,hist,oldrows,exact=True):
    Q=base.EX['q'] if exact else base.VE['q']
    bits=tuple(map(int,bits));b=dict(zip(LABELS,bits));out={}
    actual=PATHS['actual'];ld=sum(b[x] for x in actual)
    uj=[Q(b[x],ld) for x in actual]
    def sm(fn):return sum((n*fn(*map(int,t)) for n,t in zip(hist,TYPES)),F(0) if exact else 0)
    sh={i:sm(lambda *tt:Q(tt[i],sum(tt))) for i in (1,2,3)}
    for n,v in oldrows.items():
        if n.startswith('Root:APfixed:'):
            _,_,pn,ii,c,d=n.split(':');i=int(ii);k=5-i;path=PATHS[pn]
            un=Q(b[path[i]],sum(b[x] for x in path))
            for j in range(5):out[f'Root:Gfixed:{j}:{pn}:{i}:{c}:{d}']=v-k*k*un+5*k*uj[j]
        elif n.startswith(('Root:AProot:','Root:APown:')):
            _,tag,ii,c,d=n.split(':');i=int(ii);k=5-i
            gtag='Groot' if tag=='AProot' else 'Gown'
            for j in range(5):out[f'Root:{gtag}:{j}:{i}:{c}:{d}']=v-k*k*sh[i]+25*k*uj[j]
    return out

class Universe(ap.Universe):
    def __init__(self):
        super().__init__()
        template=self.atom_template()
        rr=global_rows(tuple(map(int,template['bits'])),template['root_hist'],self.atom_rows_base(template),True)
        self.gnames=list(rr);self.names+=self.gnames
        print(json.dumps({'global_cap_rows':len(rr),'total_rows':len(self.names)}),flush=True)
    @staticmethod
    def atom_template():
        h=[0]*32;h[31]=5
        return {'bits':'1111111111','AB_hist':[0,0,0,0,0,0,0,5],'AE_hist':[0,0,0,0,0,0,0,5],'second_hist':[0]*15+[5],'root_hist':h,'menus_lh':[(5,5)]*3}
    def atom_rows_base(self,a):return super().atom_rows(a)
    def atom_rows(self,a):
        rr=self.atom_rows_base(a)
        rr.update(global_rows(tuple(map(int,a['bits'])),a['root_hist'],rr,True));return rr
    def root_score(self,bits,weights,integer=False):
        own=[(n,v) for n,v in weights if n.startswith(('Root:Gfixed:','Root:Groot:','Root:Gown:'))]
        rest=[(n,v) for n,v in weights if not n.startswith(('Root:Gfixed:','Root:Groot:','Root:Gown:'))]
        _,const,co,E,H=super().root_score(bits,rest,integer)
        b=dict(zip(LABELS,map(int,bits)));actual=PATHS['actual'];ld=sum(b[x] for x in actual)
        uj=[q(b[x],ld) for x in actual];bi=self.apbits[tuple(map(int,bits))]
        for n,v in own:
            sp=n.split(':');tag=sp[1];j=int(sp[2])
            if tag=='Gfixed':
                pn,ii,c,d=sp[3:];i=int(ii);k=5-i;path=PATHS[pn]
                un=q(b[path[i]],sum(b[x] for x in path))
                old=f'Root:APfixed:{pn}:{i}:{c}:{d}'
                val=int(self.fixvalues[bi,self.fixidx[old]])+int(sc(-k*k*un+5*k*uj[j]))
                const+=v*val
            else:
                ii,c,d=sp[3:];i=int(ii);k=5-i
                const+=v*int(sc(25*k*uj[j]))
                if tag=='Gown':
                    co[f'Root:APown:{i}:{c}:{d}']+=v
                    co[f'APshare:{i}']-=v*k*k
                else:
                    aa=ap.alpha2(k);cv,dv=b[c],b[d]
                    co[f'APshare:{i}']+=v*(aa-k*k)
                    co[f'APworst:{i}']-=v*((aa-2)*cv+2*cv*dv)
                    co[f'APinstant:{i}']-=v*2*dv*(1-cv)
        key=tuple(sorted((n,v) for n,v in co.items() if v))
        return key,const,co,E,H

def fast_rows(a):
    rr=old_fast_rows(a)
    rr.update(global_rows(tuple(map(int,a['bits'])),a['root_hist'],rr,False));return rr

if __name__=='__main__':
    ap.Universe=Universe;ap.fast_rows=fast_rows
    ap.run(int(sys.argv[1]) if len(sys.argv)>1 else 80,'global_cap_discovery.json',HERE/'ap_binary_discovery.json')
