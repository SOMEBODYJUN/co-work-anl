"""Read all saved coordinates and audit the new hybrid point's 56 local rows.

No historical graph builder, optimizer or entrypoint is imported or called.
The previously audited utility definition literal() is reused only on this point;
its full-domain coefficient audit main() is deliberately never called.
"""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from itertools import product
from collections import Counter
import argparse
import importlib.util
import json

def digest(path):
    data=path.read_bytes()
    return {'path':str(path),'bytes':len(data),'sha256':sha256(data).hexdigest()}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--threshold',type=Path,required=True)
    ap.add_argument('--author-report',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    assert __debug__
    e=args.repo/'archives/customer-attraction/tools/evidence'
    oldpath=e/'combined-branch-master-program/dependencies/research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra/attractive_nested_exact.json'
    utilitypath=e/'split-basic-graph-program/verify_split_rows.py'
    old=json.loads(oldpath.read_bytes());new=json.loads(args.threshold.read_bytes())
    assert sha256(oldpath.read_bytes()).hexdigest()==new['source_sha256']=='cc48d8fdf557be7370ce964ee1d891ea99c8c830011c41cff76293b3819356b1'
    assert sha256(args.threshold.read_bytes()).hexdigest()=='72b0d89a7c36f304aead4ae0be9fffa7279316870cd6c3070497f19317367bd0'
    spec=importlib.util.spec_from_file_location('previous_local_utility_definition',utilitypath)
    definition=importlib.util.module_from_spec(spec);spec.loader.exec_module(definition)
    columns=old['columns'];byhist={};hi=None
    def key(g):return g[0],g[1],tuple(g[2]),tuple(g[3])
    assert len(columns)==1905 and columns[0]['kind']=='K'
    for j,c in enumerate(columns):
        assert F(c['weight'])>=0
        if c['kind']=='hist':
            hi=j;assert len(c['actual_bits'])==6 and set(c['actual_bits'])<={'0','1'}
            assert len(c['hist'])==8 and all(type(n) is int and n>=0 for n in c['hist']) and sum(c['hist'])==6
            words=tuple(w for w,n in zip(definition.PAT,c['hist']) for _ in range(n))
            assert c['d']==sum(w[0] for w in words)
            byhist[hi]={'c':c,'words':words,'groups':{}}
        elif c['kind']=='joint-reply':
            st=byhist[hi]['groups'].setdefault(key(c['group']),{})
            assert tuple(c['state']) not in st
            st[tuple(c['state'])]=F(c['weight'])
        else:assert c['kind'] in ('K','overlap')
    for c in columns:
        if c['kind']=='overlap':
            gs=byhist[c['hist_column']]['groups']
            assert len(c['groups'])==2 and all(key(g) in gs for g in c['groups'])
    expected=[];moments={};slab_count=0
    for hi,dd in byhist.items():
        h=F(dd['c']['weight']);words=dd['words'];gs=dd['groups']
        edges={(f,int(i==j),words[i],words[j]) for f,i,j in product(range(2),range(6),range(6)) if f or i!=j}
        assert set(gs)==edges
        for g,s in gs.items():
            assert set(s)=={(0,1),(1,0),(1,1)} and sum(s.values())<=h
            moments[hi,g]={'h':h,'r':s[1,0]+s[1,1],'z':F(),'rz':F(),'old_z':s[0,1]+s[1,1],'old_rz':s[1,1]}
        if not h:continue
        cuts=sorted({F(),h,*(moments[hi,g]['r'] for g in gs)})
        assert cuts[0]==0 and cuts[-1]==h
        for left,right in zip(cuts,cuts[1:]):
            assert left<right;slab_count+=1
            for g in gs:
                expected.append({'hist_column':hi,'left':str(left),'right':str(right),'group':[g[0],g[1],list(g[2]),list(g[3])],'r':int(right<=moments[hi,g]['r'])})
    assert len(expected)==len(new['variables'])==new['variables_count']==321
    positions=Counter();family=Counter();histvars=Counter()
    for expected_v,v in zip(expected,new['variables']):
        assert set(v)==set(expected_v)|{'weight'}
        assert {k:x for k,x in v.items() if k!='weight'}==expected_v
        weight=F(v['weight']);bound=F(v['right'])-F(v['left'])
        assert 0<=weight<=bound
        positions['zero' if not weight else 'upper' if weight==bound else 'interior']+=1
        family[str(v['group'][0])]+=1;histvars[v['hist_column']]+=1
        m=moments[v['hist_column'],key(v['group'])]
        m['z']+=weight;m['rz']+=v['r']*weight
    assert positions['upper']+positions['interior']==new['positive_variables']==134
    assert positions['interior']==new['free_vertex_variables']==17
    slacks={k:F() for k in definition.SPLIT};edge_count=Counter();state_evals=0;ledger=[]
    for (hi,g),m in moments.items():
        h,r,z,rz=(m[k] for k in ('h','r','z','rz'))
        states={(0,0):h-r-z+rz,(0,1):z-rz,(1,0):r-rz,(1,1):rz}
        assert min(states.values())>=0 and sum(states.values())==h
        ledger.append({'hist_column':hi,'group':[g[0],g[1],list(g[2]),list(g[3])],**{k:str(v) for k,v in m.items()},'state_masses':{str(s):str(v) for s,v in states.items()}})
    for hi,dd in byhist.items():
        h=F(dd['c']['weight'])
        if not h:continue
        a=tuple(map(int,dd['c']['actual_bits']));words=dd['words']
        for i,j in product(range(6),repeat=2):
            dg=int(i==j);m=moments[hi,(1,dg,words[i],words[j])]
            r,z,rz=(m[k] for k in ('r','z','rz'))
            states={(0,0):h-r-z+rz,(0,1):z-rz,(1,0):r-rz,(1,1):rz}
            edge_count[dg]+=1
            for state,mass in states.items():
                values=definition.literal(a,words,i,j,*state);state_evals+=1
                for index,coefficient in values.items():slacks[definition.SPLIT[index]]+=mass*coefficient
    for stage in ('R','Z'):
        for dg,count in ((0,30),(1,6)):slacks[stage,dg,'capacity']+=count*F(columns[0]['weight'])
    report=json.loads(args.author_report.read_bytes())
    negative=[{'row':str(k),'slack':str(v)} for k,v in slacks.items() if v<0]
    assert len(slacks)==report['rows']==56 and negative==report['negative_rows']
    assert str(min(slacks.values()))==report['minimum_slack']
    merged=[{'stage':stage,'name':name,'value':str(slacks[stage,0,name]+slacks[stage,1,name])} for stage,names in (('R',definition.RN),('Z',definition.ZN)) for name in names]
    assert all(F(c['value'])>=0 for c in merged)
    O=sum(F(dd['c']['weight']) for dd in byhist.values() if dd['c']['d']>0)
    W=sum(F(dd['c']['weight']) for dd in byhist.values() if '1' in dd['c']['actual_bits'])
    assert O==F(old['O'])==F(new['O'])==1 and W==F(old['W'])==F(new['W'])<F(1,2)
    result={'scope':'full saved-coordinate decode and current hybrid-point local evaluation only; no historical graph construction, optimizer or complete coefficient audit',
      'inputs':[digest(p) for p in (oldpath,args.threshold,args.author_report,utilitypath)],
      'old_metadata':{k:v for k,v in old.items() if k!='columns'},'threshold_metadata':{k:v for k,v in new.items() if k!='variables'},
      'column_kinds':dict(Counter(c['kind'] for c in columns)),'histograms':len(byhist),'positive_histograms':sum(F(dd['c']['weight'])>0 for dd in byhist.values()),
      'all_reply_groups':len(moments),'slabs':slab_count,'variables':len(expected),'variable_positions':dict(positions),'variables_by_family':dict(family),'variables_by_histogram':dict(histvars),
      'complete_descriptor_order_and_r_bits_match_threshold_construction':True,'all_variable_bounds_and_all_four_state_masses_nonnegative':True,
      'groups_with_changed_z':sum(m['z']!=m['old_z'] for m in moments.values()),'groups_with_changed_rz':sum(m['rz']!=m['old_rz'] for m in moments.values()),
      'edges_by_diagonal':dict(edge_count),'four_state_evaluations':state_evals,'literal_utility_coefficients_evaluated':state_evals*28,
      'O':str(O),'W':str(W),'split_slacks':[{'stage':s,'diagonal':d,'name':n,'value':str(v)} for (s,d,n),v in slacks.items()],
      'negative_rows_match_author':True,'negative_count':len(negative),'zero_split_slacks':sum(v==0 for v in slacks.values()),'minimum_split_slack':str(min(slacks.values())),
      'all_28_merged_basic_slacks_nonnegative':True,'merged_basic_slacks':merged,
      'limitations':'The 3949 row feasibility and general common-cube strategy claims are not verified by this script. 1306 old overlap coordinates are parsed/bound to groups but unused. Saved metadata is distinguished from local facts.'}
    args.output.mkdir(exist_ok=True,parents=True)
    (args.output/'input-and-local-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    (args.output/'hybrid-moment-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('inputs','old_metadata','threshold_metadata','split_slacks','merged_basic_slacks','limitations')},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
