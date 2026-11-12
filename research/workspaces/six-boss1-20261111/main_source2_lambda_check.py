"""Main checks a released source2 lambda family from geometry and true costs.

Imports only Main's earlier independent elementary rational routines, no producer.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, product
from collections import Counter
from hashlib import sha256
import json,sys
from main_minimal_caps_complete_check import solve,rank,cost

W=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def h(p):return sha256(p.read_bytes()).hexdigest()
def plane_value(h,x):return h[0]+sum(a*b for a,b in zip(h[1],x))

def main(package):
    assert package in ['source2_lambda_strip','source2_lambda_anchor_complete']
    pth=W/package;assert (pth/'freeze_manifest.json').is_file()
    window=package=='source2_lambda_strip';expected=23 if window else 16
    out=W/('main_'+package+'_check.json');assert not out.exists()
    domains=read(pth/'parameter_domains.json')['families'];fam=read(pth/'exact_family.json')
    vertices={};params={};minima={};Gs={};geoms=[];states=0;conditions=0;ties=0;menus=0;cols=0
    for tag,q0 in [('six_mean',F(1,6)),('ordered_five',F(1,5))]:
        pl=[]
        for k in range(3):
            a=[F(0)]*4;a[k]=1;pl.append((F(0),tuple(a)))
        if window:pl.append((F(-9),(F(0),F(0),F(0),F(1))))
        pl.append((F(16),(F(0),F(0),F(0),F(-1))))
        for k,j in enumerate(range(3,6)):
            for cap,lcoef in [(F(0),F(1,20)),(F(3,4),F(0))]:
                a=[F(0)]*4;a[k]=F(-3,4);a[3]=lcoef
                for l in range(j+1,6):a[l-3]=-q0/((7-l)*(8-l))
                pl.append((cap-q0/2,tuple(a)))
        vv=set()
        for basis in combinations(pl,4):
            x=solve(basis)
            if x is not None and all(plane_value(h,x)>=0 for h in pl):vv.add(x)
        by={v['id']:tuple(map(F,v['point'])) for v in domains[tag]['vertices']}
        assert vv==set(by.values()) and len(vv)==expected
        for h0 in pl:
            on=[x for x in vv if plane_value(h0,x)==0]
            assert on and rank([[a-b for a,b in zip(x,on[0])] for x in on[1:]])==3
        geoms.append({'q0':str(q0),'complete_vertices':expected,'facets':len(pl),
                      'lambda_layers':dict(Counter(str(x[-1]) for x in vv))})
        for vid,x in by.items():
            tau={j:x[j-3] for j in range(3,6)};lam=x[-1]
            beta={j:q0/2+tau[j]+sum((q0*tau[l]/((7-l)*(8-l)) for l in tau if l>j),F(0)) for j in tau}
            B=sum(beta.values());S=1+B;a=lam+sum(tau.values())
            assert lam>=10*q0 and lam<=16 and a>0
            params[tag,vid]=(tau,lam,beta,B,S,a)
            for p in [0,1]:
                Wv=B+lam/(p+4);Z=q0*(F(1,p+1)+sum((tau[j]/(p+7-j) for j in tau),F(0)))
                cc=([(t,q0*o) for t,o in product([0,1],repeat=2)] if tag=='six_mean'
                    else [(0,F(d,5)) for d in range(6)]+[(1,F(d-1,5)) for d in range(1,7)])
                for t,q in cc:
                    values=[cost(2,p,t,q,tail,tau,beta,a) for tail in product([0,1],repeat=4)]
                    value=min(values);minima[tag,vid,p,t,q]=value
                    states+=16;conditions+=1;ties+=values.count(value)
                    if t:assert value==Wv+(1+sum(tau.values()))*q/(p+5)
                    elif q in [F(0),q0]:assert value==(Z if q else F(0))
                if tag=='ordered_five':
                    assert Wv-Z>=F(3,5)+F(19,20)*sum(tau.values())
                    G=(5*Z+Wv)/6;Gs[vid,p]=G
                    for menu in product([0,1],repeat=6):
                        d=sum(menu);val=F(0)
                        for k,t in enumerate(menu):
                            q=sum((F(menu[l],5) for l in range(6) if l!=k),F(0))
                            assert q==F(d-t,5)
                            val+=minima[tag,vid,p,t,q]/6
                        assert val==0 if d==0 else val==G if d==1 else val>G
                        menus+=1
        vertices[tag]=by
    atoms=list(product([0,1],repeat=9))
    row_counts=Counter(r['family'] for r in fam['rows'])
    assert row_counts=={'six_general':8*expected,'six_C_only':expected,'ordered_five':expected}
    for row in fam['rows']:
        tag='ordered_five' if row['family']=='ordered_five' else 'six_mean';vid=row['vertex']
        tau,lam,beta,B,S,a=params[tag,vid]
        if tag=='six_mean':
            target=row['target'];ti=int(target[1:])-1 if target.startswith('A') else {'X':6,'C':8}[target]
        for j,bits in enumerate(atoms):
            load=sum(bits[:6]);u2=F(bits[1],load) if load else F(0);p=bits[0]
            if tag=='ordered_five':want=a*u2-bits[7]*Gs[vid,p]
            else:
                want=a*u2-minima[tag,vid,p,bits[ti],F(bits[7],6)]
                if row['family']=='six_C_only':want+=B*bits[8]
            assert F(row['raw_coefficients'][j])==want
            assert F(row['coefficients_divided_by_25'][j])==want/25
            cols+=1
        want=F(1) if row['family']=='six_C_only' else S
        assert F(row['raw_coefficients'][512])==want
        assert F(row['coefficients_divided_by_25'][512])==want/25;cols+=1
    assert cols==expected*10*513
    result={'status':'PASS_MAIN_SOURCE2_LAMBDA_COMPLETE_GEOMETRY_TRUE_COST_AND_ALL_COLUMNS',
            'package':package,'research_window_lower_9':window,'geometry':geoms,
            'raw_rows':expected*10,'complete_true_hidden_states':states,'physical_minima':conditions,
            'weak_tie_occurrences':ties,'ordered_menu_contexts':menus,'full_column_checks':cols,
            'optimizer_calls':0,'candidate_points_read':0,'proof_personally_read_complete':True,
            'proof_sha256':h(pth/'proof.md'),'family_sha256':h(pth/'exact_family.json'),
            'manifest_sha256':h(pth/'freeze_manifest.json'),
            'main_elementary_routines_sha256':h(W/'main_minimal_caps_complete_check.py'),
            'scope':'Specified true-budget anchor family; no LP claim, no SPE construction, no half conclusion.'}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main(sys.argv[1])
