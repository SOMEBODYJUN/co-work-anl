"""Independent original-payoff audit of the imported MAXROOT local lemma.

Does not import either portable verifier or old discovery implementations.
Only the frozen public rational multiplier data are read.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
SOURCE=ROOT/'customer_attraction/proofs/half5_exact_v1/components/maxroot_four_copy.json'
LABELS='TABCDQRSXY'
PATHS={'actual':'TABCD','root':'TDQRS','second':'TADXY'}
def sh(n,d):return F(n,d) if n else F(0)
def rows(bits,o):
    b=dict(zip(LABELS,bits));pays={name:[sh(b[t],sum(b[x] for x in path)) for t in path] for name,path in PATHS.items()}
    out={f'CAP:{t}':F(b['T']-b[t]) for t in LABELS[1:]}
    for t in 'RSXY':out[f'actual:3:floor:{t}']=pays['actual'][4]-F(b[t],sum(b[x] for x in 'TABC')+1)
    out['root:1:floor:S']=pays['root'][2]-F(b['S'],b['T']+b['D']+3)
    out['copy:root']=pays['actual'][1]-pays['root'][1]
    out['copy:second']=pays['actual'][2]-pays['second'][2]
    for name,path in PATHS.items():
        p=sum(b[x] for x in path[:3]);p4=p+b[path[3]]
        H=pays[name][3]+pays[name][4]+F(b[path[3]],(p+1)*(p+2))
        out[f'{name}:pairO']=F(5,2)*H+F(p,p+1)-o
        out[f'{name}:lastO']=5*pays[name][4]+F(p4,p4+1)-o
    return out,pays['actual'][0]
def run():
    records=[]
    for rec in json.loads(SOURCE.read_text()):
        B,C=F(rec['B']),F(rec['C']);w={n:F(v) for n,v in rec['multipliers'].items()};assert B>0 and all(v>=0 for v in w.values());assert sum(v for n,v in w.items() if n.endswith(':pairO') or n.endswith(':lastO'))==1
        residues=[];by_prefix={}
        for bits in product((0,1),repeat=10):
            both=[]
            for o in (0,1):
                rr,v=rows(bits,o);assert set(rr)==set(w)
                residue=B*v+C*bits[0]-o-sum(w[n]*rr[n] for n in w);assert residue>=0;both.append(residue)
            assert both[0]==both[1];residues.append(both[0]);prefix=''.join(map(str,bits[:5]));by_prefix[prefix]=min(by_prefix.get(prefix,both[0]),both[0])
        scale=F(245803508760);assert all((scale*x).denominator==1 for x in residues)
        records.append({'B':str(B),'signed_C':str(C),'membership_states':1024,'coverage_bit_states_checked':2048,'minimum_residual':str(min(residues)),'zero_membership_states':sum(r==0 for r in residues),'scaled_prefix_minima':{p:str(scale*v) for p,v in by_prefix.items()}})
    out={'status':'passed','scope':__doc__,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'certificates':records}
    HERE.joinpath('imported_maxroot_independent_recheck.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({**out,'certificates':[{k:v for k,v in r.items() if k!='scaled_prefix_minima'} for r in records]},indent=2))
if __name__=='__main__':run()
