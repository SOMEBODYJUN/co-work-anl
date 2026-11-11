"""Fixed-53 multiplier coefficient audit with one genuine prefix customer bit.

This is an explicitly documented adaptation of the frozen portable verifier,
not an independent second implementation.  It changes physical denominators,
recomputes local gamma tables with fixed source weights, and charges the fixed
MAXROOT residual.  It does not change any of the 53 outside multipliers.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json, hashlib, argparse, time
import numpy as np
from shift_local import ROOT, OUT, SRC, M

def q(n,d):return F(n,d) if n else F(0)

def build(b,mode):
    source=(SRC/'verify_certificate.py').read_text()
    replacements=[
       ('def share(b,path,i):return q(b[path[i]],sum(b[c] for c in path))',
        'def share(b,path,i):return q(b[path[i]],BACKGROUND+sum(b[c] for c in path))'),
       ('loads=p+e.sum(axis=2)','loads=BACKGROUND+p+e.sum(axis=2)'),
       ('for d in range(1,6):out=', 'for d in range(1,7):out='),
       ('den=p+e[:,:,:pos].sum(axis=2)+k-pos','den=BACKGROUND+p+e[:,:,:pos].sum(axis=2)+k-pos'),
       ('pref=p+e[:,:,:k-2].sum(axis=2)','pref=BACKGROUND+p+e[:,:,:k-2].sum(axis=2)'),
       ('for b in range(4):G=', 'for b in range(5):G='),
       ('p=sum(b[s] for s in path[:3]);','p=BACKGROUND+sum(b[s] for s in path[:3]);'),
       ('i=int(z[1])-1;p=sum(b[s] for s in path[:i]);','i=int(z[1])-1;p=BACKGROUND+sum(b[s] for s in path[:i]);'),
       ('sc(F(1,sum(b[s] for s in path[:i])+5-i))','sc(F(1,BACKGROUND+sum(b[s] for s in path[:i])+5-i))')]
    for old,new in replacements:
        assert old in source,old
        source=source.replace(old,new)
    ns={'__file__':str(SRC/'verify_certificate.py'),'__name__':'adapted_five_certificate','BACKGROUND':b}
    exec(compile(source,str(OUT/'adapted_frozen_verifier.py'),'exec'),ns)
    bg,pc,deep,sources=ns['source_tables']()
    shifted=json.loads((OUT/'shifted_local_tables.json').read_text())
    tabs={(r['family'],r['source_index']):r for r in shifted['components']}
    if b:
        for idx,srcidx in ((0,0),(2,3),(4,11)):
            k,g,player=bg[idx];bg[idx]=(k,tabs['BG2',srcidx]['gamma_b1_floor_million'],player)
        for idx in (0,1,2,3,5,6,7):
            k,g,u=pc[idx];family='PC2' if idx<5 else 'PC3';srcidx=idx if idx<5 else idx-5
            pc[idx]=(k,tabs[family,srcidx]['gamma_b1_floor_million'],u)
    base=ns['LiteralDomain'];paths=ns['PATHS'];labels=ns['LABELS'];share=ns['share']
    def target(d):return q(d,b+d) if mode=='profit' else F(d>0)
    class ShiftedDomain(base):
        def fixed_value(self,name,bits,d,menus):
            z=name.split(':');kind=z[0]
            if name=='MAXROOT-NEW':
                correction=shifted['maxroot'][mode]['charge_floor_million'] if b else 0
                return 46313177*share(bits,paths['actual'],0)-M*target(d)-correction,-7412362
            if kind=='DEEP' and b:
                assert z[2].isdigit()
                a,k,g,s,zeta=self.deep[int(z[1])]
                t=bits[labels[int(z[2])]];v=bits[labels[int(z[3])]]
                gamma=tabs['DEEP',0]['gamma_b1_floor_million'][2*t+v]
                return a*share(bits,paths['actual'],0)-gamma,k
            if kind in paths and z[1].isdigit() and z[2]=='O':
                path=paths[kind];i=int(z[1])-1;p=sum(bits[s] for s in path[:i]);remain=5-i
                tax_num=p+(b if mode=='coverage' else 0)
                return 5*remain*share(bits,path,i)+q(tax_num,b+p+remain)-target(d),0
            return super().fixed_value(name,bits,d,menus)
    return ns,ShiftedDomain(bg,pc,deep),target

def run(b,mode):
    start=time.time();ns,domain,target=build(b,mode)
    src,weights,B,D,_=ns['load_certificate'](SRC/'certificate.json')
    fixed={};family={tag:{} for tag in ns['FAMILIES']}
    for n,v in weights.items():
        tag=n.split(':')[0]
        if tag in family:family[tag][n]=v
        elif ':sum-S' in n:family['Sbranch'][n]=v
        else:fixed[n]=v
    menu_fixed={n:w for n,w in fixed.items() if ':reply:' in n or ':sum-L-' in n}
    cache={};conditional=[];best_by_actual={};worst=None;kcoef=None
    for imask,mask in enumerate(product((0,1),repeat=10)):
        bits=dict(zip(ns['LABELS'],mask));maxima=[];choices=[];currentkap=0
        for tag in ns['FAMILIES']:
            key,const,kap=domain.family_parts(tag,bits,family[tag]);k,p,terms=key;currentkap+=kap
            if key not in cache:
                score=np.zeros(len(domain.hist[k]),dtype=object)
                for f,v in terms:score+=v*domain.features[k,p][f].astype(object)
                vals=[];choice=[]
                for ids in domain.ids[k]:
                    chosen=max(ids,key=lambda ix:score[ix]);vals.append(int(score[chosen]));choice.append(int(chosen))
                cache[key]=(vals,choice)
            maxima.append([x+const for x in cache[key][0]]);choices.append((k,cache[key][1]))
        for d in range(6):
            base=0;K=currentkap;menus0=[(0,0)]*3
            for n,w in fixed.items():
                value,kap=domain.fixed_value(n,bits,d,menus0);base+=w*ns['sc'](value);K+=w*kap
            if kcoef is None:kcoef=K
            assert K==kcoef
            extra=0;chosen_menus=[]
            for f in range(3):
                candidates=[]
                for ell,h in ((0,0),(d,d),(5-d,0),(5,d)):
                    menus=menus0.copy();menus[f]=(ell,h);value=0
                    for n,w in menu_fixed.items():
                        v,_=domain.fixed_value(n,bits,d,menus);v0,_=domain.fixed_value(n,bits,d,menus0)
                        value+=w*ns['sc'](v-v0)
                    candidates.append((value,ell,h))
                v,ell,h=max(candidates);extra+=v;chosen_menus.append((ell,h))
            c=sum(mask[:5]);actual=q(c,b+c) if mode=='profit' else F(bool(b+c))
            # Main target is 2V-R_b in profit mode, full 2W-O_5 in coverage.
            scaled=120*D*(2*actual-target(d))-base-extra-sum(a[d] for a in maxima)
            assert F(scaled).denominator==1;scaled=int(scaled)
            value=F(scaled,120*D)
            rec={'bits':''.join(map(str,mask)),'d':d,'rho':str(value),'scaled_integer':str(scaled)}
            conditional.append(rec)
            actual_bits=''.join(map(str,mask[:5]));ak=(actual_bits,d)
            if ak not in best_by_actual or value<best_by_actual[ak]['value']:
                best_by_actual[ak]={'value':value,'witness':dict(rec,menus=chosen_menus,
                    histograms={tag:list(domain.hist[k][ch[d]]) for tag,(k,ch) in zip(ns['FAMILIES'],choices)})}
            if worst is None or value<worst['value']:worst=best_by_actual[ak]
        if imask%128==0:print(json.dumps({'background':b,'mode':mode,'mask':imask,'seconds':round(time.time()-start,2)}),flush=True)
    assert kcoef==-2264870
    if b==0:assert min(F(x['rho']) for x in conditional)>=0
    table=[];root_factor=F(0)
    for (bits,d),v in sorted(best_by_actual.items()):
        charge=max(F(0),-v['value']);factor=charge*(1+sum(map(int,bits)))
        root_factor=max(root_factor,factor)
        table.append({'actual':bits,'d':d,'min_rho':str(v['value']),'needed_nonnegative_charge':str(charge),
            'first_player_share_factor':str(factor),'witness':v['witness']})
    result={'background':b,'mode':mode,'certificate_sha256':src['_loaded_sha256'],
        'frozen_verifier_sha256':hashlib.sha256((SRC/'verify_certificate.py').read_bytes()).hexdigest(),
        'shifted_local_sha256':hashlib.sha256((OUT/'shifted_local_tables.json').read_bytes()).hexdigest(),
        'positive_outer_multipliers':len(weights),'outside_common_denominator':str(D),
        'residual_scale':str(120*D),'K_residual':str(F(-kcoef,D)),
        'min_rho':str(worst['value']),'global_worst_witness':worst['witness'],
        'negative_conditional_cases':sum(F(r['rho'])<0 for r in conditional),
        'first_player_sufficient_factor':str(root_factor),
        'min_by_actual_and_d':table,'all_6144_conditional_residuals':conditional,
        'seconds':time.time()-start}
    file=OUT/f'fixed53_b{b}_{mode}.json';file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('min_by_actual_and_d','all_6144_conditional_residuals','global_worst_witness')},indent=2),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--background',type=int,choices=(0,1),required=True);ap.add_argument('--mode',choices=('profit','coverage'),required=True)
    a=ap.parse_args();run(a.background,a.mode)
