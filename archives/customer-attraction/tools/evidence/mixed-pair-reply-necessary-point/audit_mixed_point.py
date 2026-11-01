"""Full point readback and new-weight audits, reusing certified row mathematics.

All 1905 records and weights are traversed. No old CLI, LP, or SPE solver runs.
The old coefficient identity audit is not repeated on an identical layout.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import runpy
import sys

PAT=tuple(product((0,1),repeat=3))
GROUPS=((0,0),(1,0),(1,1))
SOURCE_SHA='83b469f45e6017c024d1f87c614c5b1e968be94bb171ed27bb913c7119843613'

def sha(p):
    b=p.read_bytes();return {'name':p.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def group(g):
    f,d,wi,wj=g
    assert (f,d) in GROUPS and tuple(wi) in PAT and tuple(wj) in PAT
    assert not d or wi==wj
    return f,d,tuple(wi),tuple(wj)

def summary(values):
    return {'rows':len(values),'negative':sum(v<0 for v in values),'zero':sum(v==0 for v in values),
            'positive':sum(v>0 for v in values),'minimum':str(min(values)),'maximum':str(max(values))}

def descriptors(cols):return [{k:v for k,v in c.items() if k!='weight'} for c in cols]

def structure(point):
    cols=point['columns'];weights=[F(c['weight']) for c in cols]
    assert len(cols)==1905 and min(weights)>=0 and sum(v>0 for v in weights)==point['positive_columns']==184
    assert set(cols[0])=={'kind','weight'} and cols[0]['kind']=='K'
    hs={};hi=None
    for j,c in enumerate(cols):
        kind=c['kind'];w=weights[j]
        if kind=='hist':
            assert set(c)=={'kind','actual_bits','d','hist','weight'}
            assert len(c['actual_bits'])==6 and set(c['actual_bits'])<={'0','1'}
            assert len(c['hist'])==8 and all(type(n) is int and n>=0 for n in c['hist']) and sum(c['hist'])==6
            assert c['d']==sum(n*t[0] for n,t in zip(c['hist'],PAT))==1
            hi=j;hs[j]={'a':tuple(map(int,c['actual_bits'])),'hist':c['hist'],'mass':w,'states':{},'old_id':None}
        elif kind=='joint-reply':
            assert set(c)=={'kind','hist_column_old','group','state','weight'} and hi is not None
            h=hs[hi]
            if h['old_id'] is None:h['old_id']=c['hist_column_old']
            assert type(c['hist_column_old']) is int and c['hist_column_old']==h['old_id']
            g=group(c['group']);st=tuple(c['state']);assert st in {(0,1),(1,0),(1,1)}
            states=h['states'].setdefault(g,{});assert st not in states;states[st]=w
        elif kind=='K':assert j==0
        else:assert kind=='overlap'
    assert Counter(c['kind'] for c in cols)=={'K':1,'hist':16,'joint-reply':582,'overlap':1306}
    implicit=[]
    for hc,h in hs.items():
        words=[word for n,word in zip(h['hist'],PAT) for _ in range(n)]
        edges=[(f,int(i==j),words[i],words[j]) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j]
        h['multiplicities']=Counter(edges)
        assert len(edges)==66 and set(h['states'])==set(edges)
        assert Counter(g[:2] for g in edges)=={(0,0):30,(1,0):30,(1,1):6}
        h['R']={};h['Z']={}
        for g,states in h['states'].items():
            assert set(states)=={(0,1),(1,0),(1,1)}
            implicit.append(h['mass']-sum(states.values()));assert implicit[-1]>=0
            h['R'][g]=states[1,0]+states[1,1];h['Z'][g]=states[0,1]+states[1,1]
    assert len(hs)==16 and len(implicit)==194
    seen=set();upper=[];lower=[];lower_failures=[];saturated=0
    for j,c in enumerate(cols):
        if c['kind']!='overlap':continue
        assert set(c)=={'kind','hist_column','groups','weight'} and c['hist_column'] in hs and len(c['groups'])==2
        hc=c['hist_column'];h=hs[hc];g1,g2=map(group,c['groups']);assert g1!=g2 and g1 in h['R'] and g2 in h['R']
        key=(hc,frozenset((g1,g2)));assert key not in seen;seen.add(key)
        r,s=h['R'][g1],h['R'][g2];v=weights[j]
        upper.extend((r-v,s-v));assert min(r-v,s-v)>=0
        lo=max(F(),r+s-h['mass']);lower.append(v-lo);saturated+=v==min(r,s)
        if v<lo:lower_failures.append({'column':j,'hist_column':hc,'stored_auxiliary':str(v),'Frechet_lower_bound':str(lo),'shortfall':str(lo-v)})
    assert seen=={(hc,frozenset(gs)) for hc,h in hs.items() for gs in combinations(h['states'],2)} and len(upper)==2612
    O=sum((h['mass'] for h in hs.values()),F());W=sum((h['mass'] for h in hs.values() if any(h['a'])),F())
    assert O==F(point['O'])==1 and W==F(point['W']) and 1-2*W==F(point['strict_half_gap'])>0
    u=[sum((h['mass']*F(h['a'][j],sum(h['a'])) for h in hs.values() if h['a'][j]),F()) for j in range(6)]
    assert sum(u)==W
    capacities=[];floors=[]
    for member,name in enumerate(('R','Z')):
        for f,d in GROUPS:
            count=6 if d else 30
            amount=sum((h['multiplicities'][g]*v for h in hs.values() for g,v in h[name].items() if g[:2]==(f,d)),F())
            slack=count*weights[0]-amount;assert slack>=0
            capacities.append({'member':member,'family':f,'diagonal':d,'slack':str(slack)})
            for i in range(6):
                price=sum((h['multiplicities'][g]*v/F(sum(h['a'][:i])+6-i) for h in hs.values() for g,v in h[name].items() if g[:2]==(f,d)),F())
                v=count*u[i]-price;assert v>=0
                floors.append({'key':[i,member,f,d],'slack':str(v)})
    return hs,{'column_counts':dict(Counter(c['kind'] for c in cols)),
        'positive_counts':dict(Counter(c['kind'] for c in cols if F(c['weight'])>0)),
        'histograms':[{'column':hc,'old_id':h['old_id'],'actual_bits':''.join(map(str,h['a'])),'hist':h['hist'],'mass':str(h['mass']),'groups':len(h['states'])} for hc,h in hs.items()],
        'implicit_00':summary(implicit),'overlap_upper_bounds':summary(upper),
        'overlap_literal_Frechet_diagnostic':{**summary(lower),'at_maximal_intersection':saturated,'all_violations':lower_failures,
            'scope':'Diagnostic only: stored auxiliary lower bounds are not asserted by original graph. A negative value prevents reading that auxiliary literally as an intersection.'},
        'O':str(O),'W':str(W),'strict_half_gap':str(1-2*W),'K':str(weights[0]),'six_actual_payoffs':list(map(str,u)),
        'split_capacity_slacks':capacities,'actual_prefix_floor_slacks':floors,'actual_prefix_floor_summary':summary([F(x['slack']) for x in floors])}

def main():
    p=argparse.ArgumentParser()
    for name in ('repo','point','out'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();assert not sys.flags.optimize
    assert sha(a.point)=={'name':a.point.name,'bytes':816556,'sha256':SOURCE_SHA}
    point=json.loads(a.point.read_text());ev=a.repo/'archives/customer-attraction/tools/evidence'
    assert set(point)=={'scope','base_rows','first_raw_rows','additional_index_class_rows','O','W','strict_half_gap','verified_rows','minimum_slack','positive_columns','additional_new_reply_floors','columns'}
    assert (point['base_rows'],point['first_raw_rows'],point['additional_index_class_rows'],point['verified_rows'],point['minimum_slack'],point['additional_new_reply_floors'])==(702,37,100,5043,'0',36)
    hs,readback=structure(point);cols=point['columns'];comparisons=[]
    paths=[('floor_4963',ev/'all-reply-actual-floors-program/related/all_reply_floors_exact.json'),
           ('query_4971',ev/'continuous-old-query-cuts-program/related/all_reply_query_cuts_exact.json'),
           ('refinement_5075',ev/'continuous-query-refinement-program/related/continuous_refinement_exact.json'),
           ('master_5108',ev/'full156-tail-parent-report/original/research_5/combined_branch_master_exact.json')]
    for name,path in paths:
        other=json.loads(path.read_text());oc=other['columns'];assert descriptors(cols)==descriptors(oc)
        changed=[j for j,(x,y) in enumerate(zip(cols,oc)) if F(x['weight'])!=F(y['weight'])]
        comparisons.append({'name':name,'source':sha(path),'metadata':{k:v for k,v in other.items() if k!='columns'},
            'identical_all_1905_descriptors':True,'same_W':F(point['W'])==F(other['W']),
            'changed_counts_by_kind':dict(Counter(cols[j]['kind'] for j in changed)),'changed_positions':changed})
    helper=ev/'mixed-pair-reply-rows-program/audit_mixed_rows.py'
    assert sha(helper)['sha256']=='0f28ac7578d79ccfc50e0828e01be5323c6d8bcbf8dde831c7707096715ae561'
    oldaudit=json.loads((ev/'mixed-pair-reply-rows-program/exact-audit.json').read_text());assert oldaudit['pass'] and all(z['coefficient_equalities']==137160 for z in oldaudit['points'])
    defs=runpy.run_path(str(helper),run_name='shared_mixed_mathematical_definitions')
    keys=tuple((m,f,d,q) for m in range(2) for f,d in GROUPS for q in range(12))
    rows=defs['direct_rows'](cols,keys);ys=[F(c['weight']) for c in cols]
    mixed=[sum((v*w for v,w in zip(row,ys)),F()) for row in rows];assert min(mixed)>=0
    oldcuts=json.loads((ev/'all-reply-actual-floors-program/related/old_query_cuts.json').read_text())['selected']
    mapped=[]
    for item in oldcuts:
        i,m,f,d,q,mode,aa,mu=item['cut'];assert i==4 and F(aa)==F(mu)==1
        k=(m,f,d,q+6);mapped.append({'cut':item['cut'],'mixed_key':k,'slack':str(mixed[keys.index(k)])})
    integrator=ev/'continuous-old-query-cut-data/audit_cuts.py';prior=json.loads((ev/'continuous-old-query-cut-data/three-stage-cut-audit.json').read_text())
    assert sha(integrator)['sha256']==prior['audit_sha256']
    definitions=runpy.run_path(str(integrator),run_name='shared_continuous_mathematical_definitions');ih=definitions['read_point'](point)
    cutreports=[]
    for name,path,field in [('old64',ev/'continuous-old-query-cut-data/original/continuous_old_query_cuts.json','selected'),('refinement32',ev/'continuous-old-query-cut-data/related/continuous_refinement_cuts.json','cuts')]:
        data=json.loads(path.read_text());cuts=[x['cut'] for x in data[field]] if field=='selected' else data[field]
        values=[definitions['evaluate'](ih,c) for c in cuts]
        cutreports.append({'name':name,'source':sha(path),'summary':summary(values),'all_slacks':[{'position':j,'cut':c,'slack':str(v)} for j,(c,v) in enumerate(zip(cuts,values))]})
    report={'status':'PASS_POINT_STRUCTURE_AND_72_NECESSARY_ROWS; SUCCESSOR_CUTS_DIAGNOSTIC',
        'scope':'New point arithmetic and full data readback only; prior identical-layout coefficient proof reused. Separate original verifier event checks all 5043 rows.',
        'python':sys.version,'audit_sha256':sha(Path(__file__))['sha256'],'source':sha(a.point),
        'top_level_metadata':{k:v for k,v in point.items() if k!='columns'},'point_structure':readback,'comparison_points':comparisons,
        'reused_coefficient_audit':{'file':'../mixed-pair-reply-rows-program/exact-audit.json','helper':sha(helper),'repeated_coefficient_comparisons':0,'basis':'all 1905 descriptors equal both previously audited points'},
        'mixed_rows':{'summary':summary(mixed),'all_slacks':[{'key':k,'slack':str(v)} for k,v in zip(keys,mixed)]},'eight_old_cuts':mapped,
        'successor_integrator':sha(integrator),'saved_successor_cut_evaluations':cutreports,
        'not_certified':['exact optimum or historical discovery iterations','general graph closure','complete-history SPE or six-half counterexample']}
    a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'point':{k:readback[k] for k in ('O','W','K','positive_counts')},'mixed':summary(mixed),'Frechet_diagnostic':summary([F(z['stored_auxiliary'])-F(z['Frechet_lower_bound']) for z in readback['overlap_literal_Frechet_diagnostic']['all_violations']]) if readback['overlap_literal_Frechet_diagnostic']['all_violations'] else 'no violations','successor_cuts':{r['name']:r['summary'] for r in cutreports}},indent=2))

if __name__=='__main__':main()
