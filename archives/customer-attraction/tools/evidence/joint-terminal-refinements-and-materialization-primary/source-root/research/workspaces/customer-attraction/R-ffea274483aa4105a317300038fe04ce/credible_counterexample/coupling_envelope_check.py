"""Necessary cross-menu diagonal/offdiagonal rows with shared optimal t_i.
Rearrangement relaxes cross-family joint coupling separately at each customer.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[5]
source=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())
atoms=source['primal']['atoms'];triples=list(product((0,1),repeat=3));quads=list(product((0,1),repeat=4))

def target_counts(z):
    out={f'L_{r}':(ell-h,h) for r,(ell,h) in zip(('actual','second','third'),z['menus_lh'])}
    for g in ('AB','AE'):
        hist=z[g+'_hist']
        for j,label in ((1,'R'),(2,'S')):
            out[g+'_'+label]=tuple(sum(n*bits[j] for n,bits in zip(hist,triples) if bits[0]==t) for t in (0,1))
    for j,label in ((1,'H'),(2,'I'),(3,'J')):
        out['second_'+label]=tuple(sum(n*bits[j] for n,bits in zip(z['second_hist'],quads) if bits[0]==t) for t in (0,1))
    return out

def source_terms(z,g):
    a,b,c,d,e,u,v,w,x,y=map(int,z['bits']);hist=z[g+'_hist'] if g!='second' else z['second_hist'];bitslist=triples if g!='second' else quads
    own=F(0);inv=[[],[]]
    for n,bits in zip(hist,bitslist):
        denom=(a+(b if g=='AB' else e)+bits[0]+bits[1]+1) if g!='second' else a+sum(bits[:3])+1
        own+=F(n*bits[-1],denom);inv[bits[0]] += [F(1,denom)]*n
    return own,inv

def rows(z):
    out={}
    for g in ('AB','AE','second'):
        own,inv=source_terms(z,g);total_inv=sum(inv[0]+inv[1],F(0))
        for target,counts in target_counts(z).items():
            if target.startswith(g+'_'):continue
            low=sum((sum(sorted(inv[t])[:counts[t]],F(0)) for t in (0,1)),F(0))
            high=sum((sum(sorted(inv[t],reverse=True)[:counts[t]],F(0)) for t in (0,1)),F(0))
            out[g+':'+target+':diag_min']=own-low
            out[g+':'+target+':offdiag_max']=4*own-sum(counts)*total_inv+high
    return out

def main():
    columns=[rows(z) for z in atoms]
    weights_original=[F(z['mass_numerator'],source['primal']['denominator']) for z in atoms]
    after=json.loads((ROOT/'research/workspaces/customer-attraction/R-d7f409d6a5914bdeb09875ab32618466/credible_counterexample/frozen_support_closure.json').read_text())
    weights_new=list(map(F,after['exact_reweighting']))
    report={}
    for label,weights in [('original',weights_original),('447_reweighted',weights_new)]:
        values={name:sum((w*c[name] for w,c in zip(weights,columns)),F(0)) for name in columns[0]}
        report[label]={'violations':{name:str(v) for name,v in values.items() if v<0},'minimum_slack':str(min(values.values())),'values':{name:str(v) for name,v in values.items()}}
    path=Path(__file__).with_suffix('.json');path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({label:{k:v for k,v in d.items() if k!='values'} for label,d in report.items()},indent=2))
if __name__=='__main__':main()
