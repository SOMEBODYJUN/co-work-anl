"""Independent complete field reading of the frozen floor4963 point.

Every column descriptor and rational weight is checked. This does not import
the original graph, replay the old 9900 scan, or claim independent 4963 rows.
The Fréchet lower bound is a realization diagnostic, not an inherited row.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
from collections import Counter
import argparse
import hashlib
import json
import sys

REL = 'archives/customer-attraction/tools/evidence/all-reply-actual-floors-program/related/all_reply_floors_exact.json'
SHA = 'f6f4d5c28857e8e6350bdc8528daa6109122bce8a6fb00e8ac5c3150ffc42314'
PAT = tuple(product((0,1),repeat=3))
STATES = ((0,1),(1,0),(1,1))
GS = ((0,0),(1,0),(1,1))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def group(raw):
    assert isinstance(raw,list) and len(raw)==4
    f,d,w,v=raw
    assert (f,d) in GS and tuple(w) in PAT and tuple(v) in PAT
    if d: assert w==v
    return f,d,tuple(w),tuple(v)


def schema(obj,keys):
    assert set(obj)==set(keys)


def main():
    if not __debug__: raise RuntimeError('Assertions must be enabled')
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    here=Path(__file__).resolve().parent
    root=args.repo or next(p for p in here.parents if (p/'cleanup/OBJECTS.md').exists())
    output=args.output or here/'independent-point-audit.json'
    source=root/REL
    raw=source.read_bytes()
    assert len(raw)==815347 and digest(source)==SHA
    point=json.loads(raw)
    schema(point,('scope','base_rows','first_raw_rows','additional_index_class_rows','O','W','strict_half_gap','verified_rows','minimum_slack','positive_columns','columns','additional_new_reply_floors'))
    assert point['scope']=='exact necessary graph point with all 36 new R/Z actual-prefix floors; not SPE or game'
    assert (point['base_rows'],point['first_raw_rows'],point['additional_index_class_rows'],point['verified_rows'],point['minimum_slack'],point['additional_new_reply_floors'])==(702,37,100,4963,'0',36)
    cols=point['columns']
    assert len(cols)==1905
    weights=[F(c['weight']) for c in cols]
    assert all(str(w)==c['weight'] for w,c in zip(weights,cols))
    assert min(weights)>=0 and sum(w>0 for w in weights)==point['positive_columns']==168
    kinds=Counter(c['kind'] for c in cols)
    positive=Counter(c['kind'] for c,w in zip(cols,weights) if w>0)
    assert kinds=={'K':1,'hist':16,'joint-reply':582,'overlap':1306}
    assert positive=={'K':1,'hist':10,'joint-reply':83,'overlap':74}
    schema(cols[0],('kind','weight'))
    assert cols[0]['kind']=='K'
    K=weights[0]
    hist={}; current=None
    for index,c in enumerate(cols):
        if c['kind']=='hist':
            schema(c,('kind','actual_bits','d','hist','weight'))
            assert len(c['actual_bits'])==6 and set(c['actual_bits'])<={'0','1'}
            assert len(c['hist'])==8 and all(type(n) is int and n>=0 for n in c['hist']) and sum(c['hist'])==6
            assert c['d']==sum(n*w[0] for n,w in zip(c['hist'],PAT))==1
            current=index
            words=tuple(w for n,w in zip(c['hist'],PAT) for _ in range(n))
            expected=Counter((f,int(i==j),words[i],words[j]) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j)
            assert sum(expected.values())==66
            hist[index]={'column':c,'mass':weights[index],'a':tuple(map(int,c['actual_bits'])),'states':{},'old_ids':set(),'multiplicity':expected}
        elif c['kind']=='joint-reply':
            schema(c,('kind','hist_column_old','group','state','weight'))
            h=hist[current];g=group(c['group']);st=tuple(c['state'])
            assert g in h['multiplicity'] and st in STATES
            h['old_ids'].add(c['hist_column_old'])
            states=h['states'].setdefault(g,{})
            assert st not in states
            states[st]=(index,weights[index])
        elif c['kind']=='overlap':
            schema(c,('kind','hist_column','groups','weight'))
        else: assert index==0 and c['kind']=='K'
    group_records=[]; old_index=1
    for hi,h in hist.items():
        assert h['old_ids']=={old_index}
        h['old_id']=old_index
        old_index+=1+len(h['multiplicity'])
        assert set(h['states'])==set(h['multiplicity'])
        h['R']={};h['Z']={}
        for g,states in h['states'].items():
            assert set(states)==set(STATES)
            y={st:value for st,(index,value) in states.items()}
            zero=h['mass']-sum(y.values())
            assert zero>=0
            h['R'][g]=y[1,0]+y[1,1];h['Z'][g]=y[0,1]+y[1,1]
            group_records.append({'hist_column':hi,'hist_column_old':h['old_id'],'group':g,'ordered_edge_multiplicity':h['multiplicity'][g],
                                  'state_columns':{''.join(map(str,st)):states[st][0] for st in STATES},
                                  'state_masses':{''.join(map(str,st)):str(y[st]) for st in STATES},
                                  'implicit00':str(zero),'R':str(h['R'][g]),'Z':str(h['Z'][g])})
    assert len(group_records)==194
    overlaps={};overlap_records=[]; lower_bad=[]
    for index,c in enumerate(cols):
        if c['kind']!='overlap':continue
        assert c['hist_column'] in hist and len(c['groups'])==2
        h=hist[c['hist_column']];g1,g2=map(group,c['groups'])
        assert g1!=g2 and g1 in h['R'] and g2 in h['R']
        key=(c['hist_column'],frozenset((g1,g2)))
        assert key not in overlaps
        overlaps[key]=index
        v=weights[index];r1=h['R'][g1];r2=h['R'][g2]
        upper=(r1-v,r2-v);assert min(upper)>=0
        lower=v-r1-r2+h['mass']
        rec={'column':index,'hist_column':c['hist_column'],'groups':c['groups'],'overlap':str(v),'R_masses':[str(r1),str(r2)],
             'upper_slacks':list(map(str,upper)),'frechet_lower_slack':str(lower),'nested_maximum_gap':str(min(r1,r2)-v)}
        overlap_records.append(rec)
        if lower<0:lower_bad.append(rec)
    expected={(hi,frozenset((g1,g2))) for hi,h in hist.items() for g1,g2 in combinations(h['states'],2)}
    assert set(overlaps)==expected and len(overlaps)==1306
    O=sum(h['mass'] for h in hist.values())
    W=sum(h['mass'] for h in hist.values() if any(h['a']))
    u=[sum(h['mass']*F(h['a'][i],sum(h['a'])) for h in hist.values() if any(h['a'])) for i in range(6)]
    assert O==F(point['O'])==1 and W==F(point['W']) and sum(u)==W
    assert O-2*W==F(point['strict_half_gap'])>0
    actual_sizes=[sum(h['mass']*h['a'][i] for h in hist.values()) for i in range(6)]
    assert all(s<=K for s in actual_sizes)
    capacities=[]
    for f,d in GS:
        count=6 if d else 30
        for member in ('R','Z'):
            amount=sum(mult*h[member][g] for h in hist.values() for g,mult in h['multiplicity'].items() if g[:2]==(f,d))
            slack=count*K-amount;assert slack>=0
            capacities.append({'member':member,'family':f,'diag':d,'edges':count,'total_mass':str(amount),'slack':str(slack)})
    old_floors=[];old_capacities=[]
    for bit,name in ((1,'B'),(2,'C')):
        total=sum(h['mass']*sum(n*w[bit] for n,w in zip(h['column']['hist'],PAT)) for h in hist.values())
        assert 6*K-total>=0
        old_capacities.append({'theme':name,'total_mass':str(total),'slack':str(6*K-total)})
        for i in range(6):
            price=sum(h['mass']*F(sum(n*w[bit] for n,w in zip(h['column']['hist'],PAT)),sum(h['a'][:i])+6-i) for h in hist.values())
            slack=6*u[i]-price;assert slack>=0
            old_floors.append({'theme':name,'actual_player':i+1,'price':str(price),'slack':str(slack)})
    optimum=[]
    for query in (*range(6),'B','C'):
        value=F()
        for h in hist.values():
            d=h['column']['d']
            r=6*h['a'][query] if isinstance(query,int) else sum(n*w[1 if query=='B' else 2] for n,w in zip(h['column']['hist'],PAT))
            value+=h['mass']*(6*(d==1)-r*(d==1)-6*r*(d==0))
        assert value>=0
        optimum.append({'query':query,'slack':str(value)})
    comparisons=[]
    other_paths={
      'query4971':'archives/customer-attraction/tools/evidence/continuous-old-query-cuts-program/related/all_reply_query_cuts_exact.json',
      'combined5108':'archives/customer-attraction/tools/evidence/full156-tail-parent-report/original/research_5/combined_branch_master_exact.json'}
    desc=lambda c:{k:v for k,v in c.items() if k!='weight'}
    for label,rel in other_paths.items():
        other=root/rel;op=json.loads(other.read_text())
        assert len(op['columns'])==1905 and [desc(c) for c in cols]==[desc(c) for c in op['columns']]
        changed=[i for i,(a,b) in enumerate(zip(cols,op['columns'])) if a['weight']!=b['weight']]
        marginal_changes={'R':0,'Z':0}
        for record in group_records:
            sc=record['state_columns']
            new_R=F(op['columns'][sc['10']]['weight'])+F(op['columns'][sc['11']]['weight'])
            new_Z=F(op['columns'][sc['01']]['weight'])+F(op['columns'][sc['11']]['weight'])
            marginal_changes['R']+=new_R!=F(record['R'])
            marginal_changes['Z']+=new_Z!=F(record['Z'])
        comparisons.append({'point':label,'path':rel,'sha256':digest(other),'same_descriptors':True,'same_W':point['W']==op['W'],
                            'different_weight_columns':len(changed),'differences_by_kind':dict(Counter(cols[i]['kind'] for i in changed)),
                            'different_column_ids':changed,'reply_marginal_group_changes':marginal_changes})
    summary=[{'column':hi,'old_hist_column':h['old_id'],'actual_bits':h['column']['actual_bits'],'hist':h['column']['hist'],'d':h['column']['d'],
              'weight':str(h['mass']),'reply_groups':len(h['states']),'positive_joint_states':sum(value>0 for states in h['states'].values() for index,value in states.values())}
             for hi,h in hist.items()]
    report={'scope':'independent complete field/column audit, local capacities and old floors; no original graph import, grid scan, LP or complete strategy',
            'source':{'id':'daefb4354a8db9a4653d','path':REL,'bytes':len(raw),'sha256':SHA},'audit_sha256':digest(Path(__file__)),
            'metadata':{k:v for k,v in point.items() if k!='columns'},'all_top_fields':12,'all_column_records':len(cols),
            'column_kinds':dict(kinds),'positive_by_kind':dict(positive),'all_weights_nonnegative':True,'all_rational_strings_canonical':True,
            'K':str(K),'O':str(O),'W':str(W),'strict_half_gap':str(O-2*W),'actual_utilities':list(map(str,u)),
            'actual_sizes':list(map(str,actual_sizes)),'histograms':summary,'reply_groups':group_records,
            'implicit00_nonnegative_count':len(group_records),'overlap_records':overlap_records,'overlap_upper_bounds_passed':2612,
            'frechet_lower_violations':lower_bad,'frechet_lower_violation_count':len(lower_bad),
            'nested_maximum_equal_columns':sum(F(r['nested_maximum_gap'])==0 for r in overlap_records),
            'split_capacities':capacities,'old_BC_capacities':old_capacities,'actual_BC_floors':old_floors,'optimum_one_replace':optimum,
            'comparisons':comparisons,'all_expected_constraints_pass':True,
            'realization_boundary':'Fréchet lower diagnostics concern whether the saved overlap entries themselves are joint-set intersections. They are not inherited LP rows; replacing them by nested maxima requires the known nonnegative-coefficient argument and does not establish SPE.',
            'not_claimed':['independent complete 4963-row derivation','exact optimum','game realization preserving every auxiliary overlap','SPE','half counterexample']}
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('all_top_fields','all_column_records','positive_by_kind','implicit00_nonnegative_count','overlap_upper_bounds_passed','frechet_lower_violation_count','nested_maximum_equal_columns','all_expected_constraints_pass')},ensure_ascii=False,indent=2))


if __name__=='__main__': main()
