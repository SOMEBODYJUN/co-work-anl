"""One exact B4 zero-face diagnostic on the newly recovered E certificate.

No optimization, no modification of Main's files, and no new global cut.
The EB2 bound is evaluated only where the old H2-to-Z envelope is exactly 0.
"""
from collections import Counter,defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip
import json

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
POINT=WORK/'full624_augmented_lp/recovery/augmented_lp_exact.json'

def sha(p):return sha256(p.read_bytes()).hexdigest()
def group(g):return g[0],g[1],tuple(g[2]),tuple(g[3])
def serial(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x

def main():
    assert sha(POINT)=='cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932'
    point=json.loads(POINT.read_bytes());cert=json.loads((HERE/'exact_certificate.json').read_bytes())
    verified=json.loads((HERE/'independent_certificate_audit.json').read_bytes())
    assert cert['kind']=='primal' and verified['passed']
    assert verified['certificate_sha256']==sha(HERE/'exact_certificate.json')
    lift=json.loads(gzip.decompress((HERE/'symbolic_lift.json.gz').read_bytes()))
    hist={};old=defaultdict(dict);b4=defaultdict(dict);E=defaultdict(dict)
    for j,c in enumerate(point['columns'][:4849]):
        if c['kind']=='hist':h=j;hist[h]=c
        elif c['kind']=='joint-reply':old[h,group(c['group'])][tuple(c['state'])]=Q(c['weight'])
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            b4[c['hist_column']][tuple(c['hidden'])+(c['ell']//6,)]=Q(c['weight'])
    for c,v in zip(lift['new_columns'][:776],cert['E_values']):
        E[c['hist_column'],group(c['group'])][tuple(c['old_state'])]=Q(v)
    assert set(old)==set(E) and len(hist)==16
    for (h,g),states in old.items():
        states[0,0]=Q(hist[h]['weight'])-sum(states.values(),Q())
        assert all(Q()<=E[h,g][s]<=v for s,v in states.items())
    nodes=[(f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j]
    orbits=defaultdict(list)
    for e in nodes:orbits[e[0],int(e[1]==e[2])].append(e)
    trueincome=Q()
    for h,c in hist.items():
        a=list(map(int,c['actual_bits']));d=sum(a[:3])+a[5]+1
        assert sum(b4[h].values(),Q())==Q(c['weight'])
        trueincome+=sum((mass*Q(s[1],d+s[0]) for s,mass in b4[h].items()),Q())
    previous={tuple(r['name']):Q(r['value']) for r in json.loads((HERE/'new_envelopes_exact.json').read_bytes())['rows']}
    output=[]
    for orbit,items in sorted(orbits.items()):
        oldupper=trueincome;plain=trueincome;blocks=[]
        for h,c in hist.items():
            a=list(map(int,c['actual_bits']));d=sum(a[:3])+a[5]+1
            words=[w for w,n in zip(product((0,1),repeat=3),c['hist']) for _ in range(n)]
            high=sum((mass*s[0] for s,mass in b4[h].items()),Q());H=Q(c['weight'])
            for f,i,j in items:
                key=(h,(f,int(i==j),words[i],words[j]));ss=old[key];xx=E[key]
                z=ss[0,1]+ss[1,1];e=sum(xx.values(),Q());ez=xx[0,1]+xx[1,1]
                cmax=min(z,high);plainoverlap=min(e,high);fac=Q(1,len(items));tax=Q(1,d*(d+1))
                oldupper-=fac*(z/d-cmax*tax);plain-=fac*(e/d-plainoverlap*tax)
                blocks.append(dict(hist=h,node=(f,i,j),group=key[1],H=H,Z=z,H1=high,E=e,EZ=ez,
                                   d=d,plain_overlap=plainoverlap,candidate_ZH1=cmax))
        assert plain==previous['H2-to-E',*orbit]
        saturated=oldupper==0
        if saturated:
            nested=trueincome
            for b in blocks:
                H,z,h,e,k,c=b['H'],b['Z'],b['H1'],b['E'],b['EZ'],b['candidate_ZH1']
                t1=min(k,c);t0=min(e-k,h-c)
                layer1=[z-k-c+t1,c-t1,k-t1,t1]
                layer0=[H-z-e+k-h+c+t0,h-c-t0,e-k-t0,t0]
                assert min(layer1+layer0)>=0 and sum(layer1+layer0,Q())==H
                sharper=t1+t0
                assert sharper==min(e,h,k+max(h-z,Q())) and sharper<=b['plain_overlap']
                b.update(forced_ZH1=c,layer1=layer1,layer0=layer0,nested_overlap=sharper,
                         strict_improvement=sharper<b['plain_overlap'])
                nested-=Q(1,len(items))*(e/b['d']-sharper/Q(b['d']*(b['d']+1)))
            improvement=plain-nested;assert improvement>=0
        else:
            nested=None;improvement=None
            for b in blocks:b.update(forced_ZH1=None,nested_overlap=None,strict_improvement=None)
        output.append(dict(orbit=orbit,nodes=len(items),old_H2_to_Z_upper=oldupper,
                           saturation_certified=saturated,plain_H2_to_E_upper=plain,
                           conditional_H2_to_E_upper=nested,improvement=improvement,
                           strict_blocks=sum(b['strict_improvement'] is True for b in blocks),blocks=blocks))
    assert [r['saturation_certified'] for r in output]==[True,True,False]
    result={'scope':'One conditional B4 diagnostic of the new exact E marginal on the cb45 old zero faces; no new original-point exclusion or common realization.',
            'point_sha256':sha(POINT),'E_certificate_sha256':sha(HERE/'exact_certificate.json'),
            'independent_E_audit_sha256':sha(HERE/'independent_certificate_audit.json'),
            'source_sha256':sha(Path(__file__)),
            'Main_contract_sha256':sha(WORK/'main_E_B4_conditional_bound.md'),
            'histograms':len(hist),'zero_histograms':[h for h,c in hist.items() if Q(c['weight'])==0],
            'true_H2_income':trueincome,'rows':output,'optimization_calls':0,
            'negative_conditional_rows':sum(r['conditional_H2_to_E_upper'] is not None and r['conditional_H2_to_E_upper']<0 for r in output),
            'joint_blocks_checked':sum(len(r['blocks']) for r in output if r['saturation_certified']),
            'larger_optimization_requested':False}
    (HERE/'conditional_B4_diagnostic.json').write_text(json.dumps(serial(result),ensure_ascii=False,indent=2)+'\n')
    summary={k:v for k,v in result.items() if k!='rows'}
    summary['rows']=[{k:v for k,v in r.items() if k!='blocks'} for r in output]
    (HERE/'conditional_B4_summary.json').write_text(json.dumps(serial(summary),ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(serial(summary),ensure_ascii=False))

if __name__=='__main__':main()
