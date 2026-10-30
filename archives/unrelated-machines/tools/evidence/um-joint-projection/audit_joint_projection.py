#!/usr/bin/env python3
"""New exact finite witnesses for two interface sources, not their general proof.

No LP, CSP optimizer, original checker, network call or Git command is invoked.
The all-R decoder and the scheduling transfer retain their written proof/scope.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,itertools,json,platform


def heavy_fixture():
    matrix={'A':(F(19,20),F(19,20)),'B':(F(17,20),F(17,20)),
            'l1':(F(1,10),None),'l2':(None,F(1,10))}
    schedules=[]
    for a,b in itertools.product(range(2),repeat=2):
        assignment={'A':a,'B':b,'l1':0,'l2':1}
        loads=[sum((p[assignment[j]] for j,p in matrix.items()if assignment[j]==i),F())for i in range(2)]
        schedules.append({'assignment':assignment,'loads':loads,'makespan':max(loads)})
    optimum=min(x['makespan']for x in schedules);assert optimum==F(21,20)
    placements=[x for x in schedules if x['assignment']['A']!=x['assignment']['B']]
    assert [x['loads']for x in placements]==[[F(21,20),F(19,20)],[F(19,20),F(21,20)]]
    # Two affine price functions: enumerate their breakpoints exactly.
    lines=[(x['loads'][1],x['loads'][0]-x['loads'][1])for x in placements]
    cross=(lines[1][0]-lines[0][0])/(lines[0][1]-lines[1][1]);assert cross==F(1,2)
    points=[F(),cross,F(1)]
    price_value=max(min(a+b*t for a,b in lines)for t in points)
    common=min(max(x['loads'])for x in placements)
    assert price_value==1 and common==F(21,20)
    prices=[]
    for a in [F(),F(1,4),F(1,2),F(3,4),F(1)]:
        values=[a*x['loads'][0]+(1-a)*x['loads'][1]-1 for x in placements]
        assert min(values)==-abs(2*a-1)/20
        prices.append({'lambda':[a,1-a],'G_by_placement':values})
    classification=[]
    for delta in [F(1,20),F(3,20),F(1,4),F(49,100)]:
        heavy={j:[i for i,p in enumerate(times)if p is not None and p>1-delta]for j,times in matrix.items()}
        classification.append({'delta':delta,'heavy_threshold':1-delta,'heavy_edges':heavy})
    return {'T':F(1),'delta_used_for_two_heavy_example':F(1,4),'matrix':matrix,
            'all_four_actual_schedules':schedules,'original_OPT':optimum,
            'admissible_two_heavy_placements':placements,'normalized_price_lines':lines,
            'exact_price_breakpoints':points,'price_convexified_value':price_value,
            'common_integer_heavy_fractional_light_value':common,'sample_prices':prices,
            'strict_heavy_classification_boundaries':classification,
            'scope':'This original numeric input has OPT>T, so it is not a YES-promise algorithm counterexample. The all-price formula is proved analytically in the formal text.'}


def validate_and_decode(left,right,mu,edges,couplings):
    assert all(sum(mu[v],F())==1 and min(mu[v])>=0 for v in left+right)
    supports={v:[b for b,x in enumerate(mu[v])if x>0]for v in right}
    L=max(len(s)for s in supports.values());assert L>=1
    assert sum((e['weight']for e in edges),F())==1
    taus=[];refined=F();quadratic=F();initial=F();original_mu_expectation=F()
    for edge,xi in zip(edges,couplings):
        u,v,pi,w=edge['u'],edge['v'],edge['pi'],edge['weight'];assert w>=0
        assert len(pi)==len(mu[u])and all(0<=b<len(mu[v])for b in pi)
        l=[F()for _ in mu[u]];r=[F()for _ in mu[v]]
        for a,b,q in xi:
            assert q>=0 and b==pi[a];l[a]+=q;r[b]+=q
        assert all(a<=b for a,b in zip(l,mu[u]))and all(a<=b for a,b in zip(r,mu[v]))
        tau=sum(l,F());assert tau==sum(r,F())and 0<=tau<=1
        alpha=sum((q for a,q in enumerate(mu[u])if pi[a]in supports[v]),F());assert alpha>=tau
        taus.append(tau);refined+=w*tau/len(supports[v]);quadratic+=w*tau*tau/L
        initial+=w*alpha/len(supports[v])
        original_mu_expectation+=w*sum((mu[u][a]*mu[v][pi[a]]for a in range(len(pi))),F())
    beta=sum((e['weight']*tau for e,tau in zip(edges,taus)),F())
    assert initial>=refined>=beta/L
    labels={}
    for u in left:
        scores=[sum((e['weight']/len(supports[e['v']])for e in edges if e['u']==u and e['pi'][a]in supports[e['v']]),F())for a in range(len(mu[u]))]
        labels[u]=max(range(len(scores)),key=lambda a:(scores[a],-a))
    after_left=sum((e['weight']/len(supports[e['v']])for e in edges if e['pi'][labels[e['u']]]in supports[e['v']]),F())
    assert after_left>=initial
    for v in right:
        labels[v]=max(supports[v],key=lambda b:(sum((e['weight']for e in edges if e['v']==v and e['pi'][labels[e['u']]]==b),F()),-b))
    achieved=sum((e['weight']for e in edges if e['pi'][labels[e['u']]]==labels[e['v']]),F());assert achieved>=after_left
    assert quadratic>=beta*beta/L
    return {'L':L,'tau_by_edge':taus,'beta':beta,'refined_linear_guarantee':refined,
            'uniform_L_guarantee':beta/L,'q1_edge_quadratic_guarantee':quadratic,
            'q1_beta_squared_guarantee':beta*beta/L,'original_mu_independent_expectation':original_mu_expectation,
            'right_uniform_initial_expectation':initial,'after_left_choice_expectation':after_left,
            'labels':labels,'satisfied_weight':achieved}


def shift_fixture(R,L):
    left=['u'];right=['v'];S=list(range(L));mu={'u':[F(1,R)]*R,'v':[F(1,L)if b in S else F()for b in range(R)]}
    edges=[{'u':'u','v':'v','pi':[(a+s)%R for a in range(R)],'weight':F(1,R)}for s in range(R)]
    xi=[[(a,(a+s)%R,F(1,R))for a in range(R)if(a+s)%R in S]for s in range(R)]
    decoded=validate_and_decode(left,right,mu,edges,xi)
    all_pairs=[]
    for a,b in itertools.product(range(R),repeat=2):
        value=sum((e['weight']for e in edges if e['pi'][a]==b),F());assert value==F(1,R)
        all_pairs.append({'a':a,'b':b,'satisfied_weight':value})
    assert decoded['beta']==F(L,R)and decoded['uniform_L_guarantee']==decoded['satisfied_weight']==F(1,R)
    return {'R':R,'L':L,'right_support':S,'left_vertices':left,'right_vertices':right,
            'mu':mu,'edges':edges,'partial_couplings':xi,'decoder':decoded,
            'all_single_label_pairs':all_pairs,'exact_game_value':F(1,R)}


def nonuniform_fixture():
    mu={'u0':[F(1,2),F(1,3),F(1,6)],'u1':[F(1,4),F(1,4),F(1,2)],
        'v0':[F(2,3),F(1,3),F()],'v1':[F(),F(1,4),F(3,4)]}
    edges=[{'u':'u0','v':'v0','pi':[0,1,2],'weight':F(1,4)},
           {'u':'u0','v':'v1','pi':[1,2,0],'weight':F(1,4)},
           {'u':'u1','v':'v0','pi':[0,0,0],'weight':F(1,4)},
           {'u':'u1','v':'v1','pi':[2,1,2],'weight':F(1,4)}]
    xi=[[(0,0,F(1,3)),(1,1,F(1,6))],[(0,1,F(1,8)),(1,2,F(1,4))],
        [(0,0,F(1,4)),(1,0,F(1,4)),(2,0,F(1,6))],
        [(0,2,F(1,4)),(1,1,F(1,8)),(2,2,F(1,4))]]
    decoded=validate_and_decode(['u0','u1'],['v0','v1'],mu,edges,xi)
    assert decoded['beta']==F(13,24)and decoded['uniform_L_guarantee']==F(13,48)
    assert decoded['right_uniform_initial_expectation']==F(11,24)and decoded['after_left_choice_expectation']==F(1,2)and decoded['satisfied_weight']==F(3,4)
    return {'mu':mu,'edges':edges,'partial_couplings':xi,'decoder':decoded,
            'scope':'Uniformizing the right support gives a stronger certified lower bound; its actual initial expectation need not exceed sampling the original right mu.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    if args.output.exists():parser.error('refusing to overwrite evidence')
    shifts=[shift_fixture(R,L)for R in range(1,9)for L in range(1,R+1)]
    out={'arithmetic':'fractions.Fraction/integer only; no floating tolerance','python':platform.python_version(),
         'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'heavy_numeric_fixture':heavy_fixture(),'shift_family_cases':shifts,
         'nonuniform_decoder_fixture':nonuniform_fixture(),
         'counts':{'actual_heavy_schedules':4,'admissible_heavy_placements':2,'shift_parameter_cases':len(shifts),'shift_single_label_pair_checks':sum(len(x['all_single_label_pairs'])for x in shifts),'extra_nonuniform_decoder_cases':1},
         'scope':'New finite exact audit of literal fixtures and decoder implementation. Not an all-parameter proof, no scheduling-to-projection reduction, and no source hardness certification.'}
    assert out['counts']['shift_parameter_cases']==36 and out['counts']['shift_single_label_pair_checks']==1296
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x')as f:json.dump(out,f,ensure_ascii=False,indent=2,default=str);f.write('\n')
    print(json.dumps({'status':'PASS','counts':out['counts'],'output':str(args.output)},ensure_ascii=False))


if __name__=='__main__':main()
