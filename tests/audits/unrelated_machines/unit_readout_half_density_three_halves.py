#!/usr/bin/env python3
"""全变量私有双树的半密度半槽匹配：实际三半界。

Input keys: k,h,variables,clause_capacities. Each variable is
 {"id":"x", "positive":[{"path":[0,1],"clause":0},...],
             "negative":[...]}.
Every depth-h leaf path is explicit. Prefixes must form a full k-ary tree;
this prevents hidden expansion of a binary-encoded unary-chain height.
Clause c has A_c distinct original unit machines; every leaf of c may use
any of them. Require total leaf arity d_c<=2*A_c. Large A_c is not expanded:
we explicitly retain q_c=min(A_c,d_c) units and all their port edges.
The matching uses the first ceil(d_c/2); every remaining original unit is
explicitly zero or represented by an omitted-zero range.

This is a direct uniform-half-mass ST slot-matching specialization, not a
new general approximation algorithm. All variables/jobs are mandatory.
The constructor uses no SAT, OPT, LP oracle or search for a YES schedule.
--input returns actual sigma with exact all-machine loads (unused unit
ranges explicitly zero); --output exclusively creates a new JSON file.
"""
from fractions import Fraction as F
from collections import deque,Counter
from pathlib import Path
import re

SOURCE_CLAIMS=("UM-UNIT-READOUT-HALF-DENSITY-THREE-HALVES-v1",)


def positive_integer(x):
    if type(x) is int:y=x
    elif type(x) is str and re.fullmatch(r"\+?\d+",x):y=int(x)
    else:raise ValueError('positive exact integer required')
    if y<1:raise ValueError('positive integer required')
    return y


def capacity_integer(x):
    if type(x) is int:y=x
    elif type(x) is str and re.fullmatch(r"\+?\d+",x):y=int(x)
    else:raise ValueError('nonnegative exact capacity integer required')
    if y<0:raise ValueError('nonnegative capacity integer required')
    return y


def validate(data):
    if type(data) is not dict or set(data)!={'k','h','variables','clause_capacities'}:raise ValueError('exact input keys required')
    k,h=positive_integer(data['k']),positive_integer(data['h'])
    if type(data['clause_capacities']) not in (list,tuple) or type(data['variables']) not in (list,tuple):raise ValueError('explicit lists required')
    A=[capacity_integer(x) for x in data['clause_capacities']]
    trees=[];labels=[];arity=[0]*len(A)
    for variable in data['variables']:
        if type(variable) is not dict or set(variable)!={'id','positive','negative'}:raise ValueError('variable id and two explicit trees required')
        label=variable['id']
        if type(label) not in (int,str) or label in labels:raise ValueError('distinct exact variable labels required')
        labels.append(label);pair=[]
        for sign in ('positive','negative'):
            leaves=variable[sign]
            if type(leaves) not in (list,tuple) or not leaves:raise ValueError('nonempty full-tree leaf list required')
            wiring={};children={}
            for leaf in leaves:
                if type(leaf) is not dict or set(leaf)!={'path','clause'}:raise ValueError('explicit leaf path/clause required')
                path=leaf['path'];c=leaf['clause']
                if type(path) not in (list,tuple) or len(path)!=h or any(type(x) is not int or not 0<=x<k for x in path):raise ValueError('invalid explicit depth-h path')
                path=tuple(path)
                if path in wiring or type(c) is not int or not 0<=c<len(A):raise ValueError('duplicate path or unknown clause')
                wiring[path]=c;arity[c]+=1
                for d in range(h):children.setdefault(path[:d],set()).add(path[d])
            if any(len(ch)!=k for ch in children.values()):raise ValueError('prefix children do not form a full k-ary tree')
            pair.append({'wiring':wiring,'children':children})
        trees.append(pair)
    if any(d>2*a for d,a in zip(arity,A)):raise ValueError('half-density d_c<=2*A_c required')
    return k,h,labels,A,arity,trees


def covering_matching(adj,slots):
    # Both sides have degree at most2; Hall follows by counting2 edges/job.
    left=[None]*len(adj);right=[None]*len(slots)
    for start in range(len(adj)):
        queue=deque([start]);prev={start:None};seen=set();finish=None
        while queue and finish is None:
            u=queue.popleft()
            for s in adj[u]:
                if s in seen:continue
                seen.add(s)
                if right[s] is None:finish=(u,s);break
                v=right[s]
                if v not in prev:prev[v]=(u,s);queue.append(v)
        if finish is None:raise RuntimeError('degree-two Hall matching failed')
        u,s=finish
        while True:
            left[u]=s;right[s]=u
            if u==start:break
            u,s=prev[u]
    assert len(set(left))==len(adj)
    return left


def processing_time(job,machine):
    for v,p in job['edges']:
        if machine==v:return p
    if job['kind']=='port':
        e=job['external']
        if e['start']<=machine<e['start']+e['count']:return F(1)
    raise ValueError('unavailable original edge')


def actual_loads(jobs,sigma):
    if len(jobs)!=len(sigma):raise ValueError('one destination per original job required')
    load={}
    for job,v in zip(jobs,sigma):
        if type(v) is not int or v<0:raise ValueError('invalid machine ID')
        load[v]=load.get(v,F(0))+processing_time(job,v)
    return load


def extract_forest(result):
    k=result['k'];r=(k+1)//2;chosen=[];slots=set();clause_count=[0]*len(result['clause_ranges'])
    for v,roots in enumerate(result['roots']):
        root=result['sigma'][v]
        if root not in roots:raise RuntimeError('selector did not choose a private root')
        stack=[root];nodes=[];edges=[];ports=[]
        while stack:
            u=stack.pop();nodes.append(u)
            away=[j for j in result['outgoing_jobs'][u] if result['sigma'][j]!=u]
            if len(away)<r:raise RuntimeError('actual schedule lost required active children')
            for j in away[:r]:
                job=result['jobs'][j];edges.append(j)
                if job['kind']=='edge':
                    assert result['sigma'][j]==job['child'];stack.append(job['child'])
                else:
                    assert job['kind']=='port';s=result['sigma'][j]
                    if s in slots:raise RuntimeError('selected leaf injection repeated a unit')
                    slots.add(s);ports.append(j);clause_count[job['clause']]+=1
        chosen.append({'variable':v,'root':root,'active_internal':nodes,'selected_child_jobs':edges,'selected_ports':ports})
    assert all(count<=row['count'] for count,row in zip(clause_count,result['clause_ranges']))
    return {'r':r,'variables':chosen,'selected_leaf_counts':clause_count,'selected_unit_machines':sorted(slots)}


def construct_half_density(data):
    k,h,labels,A,arity,trees=validate(data)
    machines=[];node_id={};roots=[];outgoing={};incoming={}
    for v,pair in enumerate(trees):
        root=[]
        for sign,tree in enumerate(pair):
            for path in sorted(tree['children'],key=lambda p:(len(p),p)):
                u=len(machines);node_id[v,sign,path]=u;outgoing[u]=[]
                machines.append({'machine':u,'kind':'internal','variable':labels[v],'sign':sign,'path':list(path)})
            root.append(node_id[v,sign,()])
        roots.append(root)
    internal_count=len(machines);ranges=[];base=internal_count
    for c,(a,d) in enumerate(zip(A,arity)):
        ranges.append({'clause':c,'start':base,'count':a,'arity':d,'listed_units':min(a,d),'matching_units':(d+1)//2});base+=a
    full_m=base
    jobs=[];clause_ports=[[] for c in A]
    for v,root in enumerate(roots):
        j=len(jobs);jobs.append({'job':j,'kind':'selector','variable':v,'edges':[[root[0],F(1)],[root[1],F(1)]]})
        for u in root:incoming[u]=j
    for v,pair in enumerate(trees):
        for sign,tree in enumerate(pair):
            for path in sorted(tree['children'],key=lambda p:(len(p),p)):
                parent=node_id[v,sign,path]
                for child_index in sorted(tree['children'][path]):
                    child_path=path+(child_index,);j=len(jobs)
                    if len(child_path)==h:
                        c=tree['wiring'][child_path]
                        job={'job':j,'kind':'port','variable':v,'sign':sign,'path':list(child_path),
                             'parent':parent,'clause':c,'edges':[[parent,F(1,k)]]+[[ranges[c]['start']+t,F(1)] for t in range(ranges[c]['listed_units'])],
                             'external':{'start':ranges[c]['start'],'count':A[c],'time':F(1)}}
                        clause_ports[c].append(j)
                    else:
                        child=node_id[v,sign,child_path]
                        job={'job':j,'kind':'edge','variable':v,'sign':sign,'parent':parent,'child':child,
                             'edges':[[parent,F(1,k)],[child,F(1)]]};incoming[child]=j
                    jobs.append(job);outgoing[parent].append(j)
    slots=[];adj=[[] for j in jobs]
    def add_slot(machine,js):
        s=len(slots);slots.append({'slot':s,'machine':machine,'jobs':js})
        for j in js:adj[j].append(s)
    for u in range(internal_count):
        ordered=[incoming[u]]+outgoing[u]
        assert len(outgoing[u])==k
        for t in range(0,len(ordered),2):add_slot(u,ordered[t:t+2])
    for c,ports in enumerate(clause_ports):
        assert (len(ports)+1)//2<=A[c]
        for t in range(0,len(ports),2):
            machine=ranges[c]['start']+t//2;add_slot(machine,ports[t:t+2])
        for t in range(ranges[c]['listed_units']):
            machines.append({'machine':ranges[c]['start']+t,'kind':'clause_unit','clause':c,'unit':t})
    assert all(len(neighbors)==2 and len(set(neighbors))==2 for neighbors in adj)
    assert all(1<=len(slot['jobs'])<=2 for slot in slots)
    matched=covering_matching(adj,slots)
    sigma=[slots[s]['machine'] for s in matched]
    load=actual_loads(jobs,sigma)
    bound=F(1)+F(k//2,k)
    assert max(load.values(),default=F(0))<=bound<=F(3,2)
    assert all(load.get(u,F(0))<=1 for u in load if u>=internal_count)
    dummy=False
    if full_m==0:
        full_m=1;dummy=True;machines=[{'machine':0,'kind':'dummy'}]
    listed_loads=[{'machine':row['machine'],'load':load.get(row['machine'],F(0))} for row in machines]
    result={'k':k,'h':h,'variable_labels':labels,'roots':roots,'jobs':jobs,'sigma':sigma,
            'listed_machines':machines,'listed_loads':listed_loads,'clause_ranges':ranges,
            'full_machine_count':full_m,'dummy_used':dummy,'internal_machine_count':internal_count,
            'omitted_unit_machine_count':sum(A)-sum(row['listed_units'] for row in ranges),
            'omitted_unit_machine_load':F(0),'matching_unit_machine_count':sum(row['matching_units'] for row in ranges),'explicit_clipped_unit_machine_count':sum(row['listed_units'] for row in ranges),'outgoing_jobs':outgoing,
            'slots':slots,'job_slots':adj,'matching':matched,
            'makespan':max(load.values(),default=F(0)),'bound':bound,'universal_bound':F(3,2)}
    result['forest']=extract_forest(result)
    return result


def jsonable(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):jsonable(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [jsonable(y) for y in x]
    return x


def audit():
    from itertools import product
    from random import Random
    import hashlib,platform,time
    started=time.perf_counter();rng=Random(110803);counts=Counter();hist=Counter()
    def encode(V,k,h,wiring,A):
        paths=list(product(range(k),repeat=h));variables=[];position=0
        for v in range(V):
            row={'id':v}
            for name in ('positive','negative'):
                row[name]=[{'path':list(p),'clause':wiring[position+j]} for j,p in enumerate(paths)];position+=len(paths)
            variables.append(row)
        assert position==len(wiring)
        return {'k':k,'h':h,'variables':variables,'clause_capacities':A}
    def check(result):
        load=actual_loads(result['jobs'],result['sigma'])
        assert max(load.values(),default=F(0))==result['makespan']<=result['bound']
        assert len(result['forest']['variables'])==len(result['roots'])
        assert all(record['load']==load.get(record['machine'],F(0)) for record in result['listed_loads'])
        assert result['omitted_unit_machine_load']==0
        for job in result['jobs']:
            if job['kind']=='port':assert len(job['edges'])==1+result['clause_ranges'][job['clause']]['listed_units']
        assert len(result['matching'])==len(set(result['matching']))==len(result['jobs'])
        if result['roots'] and result['k']==1:assert result['makespan']==1
    for V,k,h,C in ((1,1,1,2),(1,1,3,3),(2,1,2,3),(1,2,1,3),(1,2,2,2),(1,3,1,3)):
        n=2*V*k**h
        for wiring in product(range(C),repeat=n):
            d=[wiring.count(c) for c in range(C)];A=[max(1,(x+1)//2) for x in d]
            result=construct_half_density(encode(V,k,h,wiring,A));check(result)
            counts['exhaustive_wiring_actual_schedules']+=1;hist[str(result['makespan'])]+=1
    for unused in range(300):
        V=rng.randrange(5);k=rng.randrange(1,5);h=rng.randrange(1,4);n=2*V*k**h
        C=rng.randrange(1,13);wiring=[rng.randrange(C) for j in range(n)]
        d=[wiring.count(c) for c in range(C)]
        A=[max(1,(x+1)//2)+rng.randrange(4) for x in d]
        if unused%17==0:A[rng.randrange(C)]+=10**120+151
        result=construct_half_density(encode(V,k,h,wiring,A));check(result)
        counts['random_k_h_wiring_actual_schedules']+=1
    for V,k,h in ((2,1,128),(1,2,8),(1,3,4)):
        wiring=[0]*(2*V*k**h);A=[10**120+151]
        result=construct_half_density(encode(V,k,h,wiring,A));check(result)
        assert len(result['listed_machines'])<=result['internal_machine_count']+len(wiring)
        counts['deep_unary_large_A_boundaries']+=1
    for data in ({'k':1,'h':10**120,'variables':[],'clause_capacities':[]},
                 {'k':2,'h':1,'variables':[],'clause_capacities':[10**120+151]},
                 {'k':1,'h':1,'variables':[],'clause_capacities':[0]}):
        result=construct_half_density(data);check(result);assert result['makespan']==0;counts['empty_boundaries']+=1
    result=construct_half_density(encode(1,1,2,[1,1],[0,1]));check(result)
    counts['nonempty_tree_zero_capacity_empty_clause']+=1
    # Existing split-capacity sharp instance embedded at h=1,k=2.
    # Its actual lower certificate is reused, not re-enumerated in this audit.
    sharp=encode(3,2,1,[0,0,1,1,0,1,2,3,2,2,3,3],[2,2,2,2])
    result=construct_half_density(sharp);check(result)
    assert result['full_machine_count']==14 and len(result['jobs'])==15 and result['makespan']==F(3,2)
    counts['prior_split_sharp_actual_upper_reused']+=1
    sharp_record={'input':sharp,'sigma':result['sigma'],'listed_loads':result['listed_loads'],
                  'actual_upper':result['makespan'],'exact_optimum_by_prior_certificate':F(3,2),
                  'lower_certificate_reference':{'source':'UM-SPLIT-CAPACITY-DUAL-RAIL-THREE-HALVES-v1 sharp four-clause instance',
                    'audit_code_sha256':'5611227e746a02a7e71e93db097dfb58b070fde3a2a841e97115f04d7f66d306',
                    'lower_proof':'At C<=1 all selector-sign ports are external. The first two clauses force the y selector negative; the last two then force both choices of z, contradiction. Half-grid loads imply OPT>=3/2.',
                    'physical_or_mode_enumerations_here':0}}
    invalid=[{'k':0,'h':1,'variables':[],'clause_capacities':[]},
             {'k':1,'h':0,'variables':[],'clause_capacities':[]},
             {'k':1,'h':1,'variables':[],'clause_capacities':[-1]},
             encode(1,2,1,[0,0,0,0],[1])]
    broken=encode(1,2,2,[0]*8,[4]);broken['variables'][0]['positive'][0]['path']=[0];invalid.append(broken)
    broken=encode(1,2,1,[0]*4,[2]);broken['variables'][0]['negative'].pop();invalid.append(broken)
    for data in invalid:
        try:construct_half_density(data)
        except ValueError:counts['invalid_domains_rejected']+=1
        else:raise AssertionError('invalid half-density input accepted')
    return {'status':'passed','source_claims':SOURCE_CLAIMS,'python':platform.python_version(),'seed':110803,
            'precision':'exact half-incidence matching and Fraction actual loads','counts':dict(counts),
            'exhaustive_makespan_histogram':dict(hist),'sharp_reference':sharp_record,
            'code_sha256':__import__('hashlib').sha256(Path(__file__).read_bytes()).hexdigest(),
            'runtime_seconds':round(time.perf_counter()-started,3),
            'limits':'ST uniform-half-mass specialization. Upper theorem covers every given half-density wiring; finite tests are implementation checks. Sharpness lower bound is explicitly reused from the split-capacity certificate, not re-enumerated here. No general UM hardness claim.'}


def main():
    import argparse,json
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--input');parser.add_argument('--output')
    args=parser.parse_args()
    if args.input:
        with Path(args.input).open() as handle:data=json.load(handle)
        payload={'source_claims':SOURCE_CLAIMS,'result':construct_half_density(data)}
    else:payload=audit()
    text=json.dumps(jsonable(payload),ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if args.output:
        with Path(args.output).open('x') as handle:handle.write(text)
    else:print(text,end='')


if __name__=='__main__':main()
