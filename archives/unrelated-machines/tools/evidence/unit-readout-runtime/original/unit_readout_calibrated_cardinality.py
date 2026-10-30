#!/usr/bin/env python3
"""单位读出双树：给定强行见证的有理槽舍入、校准见证、bounded-D算法。

The explicit leaf schema follows the reviewed half-density constructor, copied
and adapted here (not claimed to be an independent implementation). A_c>=0.
No production entry point calls an OPT oracle or an LP solver. Original unit
ranges are retained; only min(A_c,d_c) units are explicitly listed, and every
omitted original unit has exact zero load. Empty variables return before
computing k**h or walking a binary-encoded enormous empty-tree height.
"""
from fractions import Fraction as F
from collections import deque, Counter
from itertools import product
from pathlib import Path
import re
import sys

# Binary input guarantees must not be capped by Python decimal-text defaults.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

SOURCE_CLAIMS=('UM-UNIT-READOUT-CALIBRATED-SLOT-v1','UM-UNIT-READOUT-BOUNDED-DENSITY-SUBTWO-v1')


def integer(x, minimum=0):
    if type(x) is int: y=x
    elif type(x) is str and re.fullmatch(r'\+?\d+',x): y=int(x)
    else: raise ValueError('exact nonnegative integer required')
    if y<minimum: raise ValueError('integer outside domain')
    return y


def rational(x):
    if isinstance(x,F): return x
    if type(x) not in (int,str): raise ValueError('exact rational string/int required')
    return F(x)


def validate(data):
    if type(data) is not dict or set(data)!={'k','h','variables','clause_capacities'}: raise ValueError('exact input keys required')
    k,h=integer(data['k'],1),integer(data['h'],1)
    if type(data['variables']) not in (list,tuple) or type(data['clause_capacities']) not in (list,tuple): raise ValueError('explicit lists required')
    A=[integer(x) for x in data['clause_capacities']]; labels=[]; trees=[]; arity=[0]*len(A)
    for variable in data['variables']:
        if type(variable) is not dict or set(variable)!={'id','positive','negative'}: raise ValueError('exact variable keys required')
        label=variable['id']
        if type(label) not in (int,str) or label in labels: raise ValueError('distinct exact variable labels required')
        labels.append(label); pair=[]
        for sign in ('positive','negative'):
            leaves=variable[sign]
            if type(leaves) not in (list,tuple) or not leaves: raise ValueError('nonempty explicit full-tree leaves required')
            wiring={}; children={}
            for leaf in leaves:
                if type(leaf) is not dict or set(leaf)!={'path','clause'}: raise ValueError('exact leaf path/clause required')
                path,c=leaf['path'],leaf['clause']
                if type(path) not in (list,tuple) or len(path)!=h or any(type(z) is not int or not 0<=z<k for z in path): raise ValueError('invalid explicit leaf path')
                path=tuple(path)
                if path in wiring or type(c) is not int or not 0<=c<len(A): raise ValueError('duplicate path or unknown clause')
                wiring[path]=c; arity[c]+=1
                for depth in range(h): children.setdefault(path[:depth],set()).add(path[depth])
            if any(len(ch)!=k for ch in children.values()): raise ValueError('prefixes are not a full k-ary tree')
            pair.append({'wiring':wiring,'children':children})
        trees.append(pair)
    return k,h,labels,A,arity,trees


def build_instance(data):
    k,h,labels,A,arity,trees=validate(data)
    machines=[]; node_id={}; roots=[]; incoming={}; outgoing={}; path_jobs={}
    for v,pair in enumerate(trees):
        root=[]
        for sign,tree in enumerate(pair):
            for path in sorted(tree['children'],key=lambda p:(len(p),p)):
                u=len(machines); node_id[v,sign,path]=u; outgoing[u]=[]
                machines.append({'machine':u,'kind':'internal','variable':labels[v],'sign':sign,'path':list(path)})
            root.append(node_id[v,sign,()])
        roots.append(root)
    internal_count=len(machines); base=internal_count; ranges=[]
    for c,(a,d) in enumerate(zip(A,arity)):
        ranges.append({'clause':c,'start':base,'count':a,'arity':d,'listed_units':min(a,d)}); base+=a
    jobs=[]; clause_ports=[[] for c in A]
    for v,root in enumerate(roots):
        j=len(jobs); jobs.append({'job':j,'kind':'selector','variable':v,'edges':[[root[0],F(1)],[root[1],F(1)]]})
        for u in root: incoming[u]=j
    for v,pair in enumerate(trees):
        for sign,tree in enumerate(pair):
            for path in sorted(tree['children'],key=lambda p:(len(p),p)):
                parent=node_id[v,sign,path]
                for digit in sorted(tree['children'][path]):
                    cp=path+(digit,); j=len(jobs)
                    common={'job':j,'variable':v,'sign':sign,'path':list(cp),'parent':parent}
                    if len(cp)==h:
                        c=tree['wiring'][cp]; row=ranges[c]
                        job=dict(common,kind='port',clause=c,edges=[[parent,F(1,k)]]+[[row['start']+s,F(1)] for s in range(row['listed_units'])],external={'start':row['start'],'count':A[c],'time':F(1)})
                        clause_ports[c].append(j)
                    else:
                        child=node_id[v,sign,cp]; job=dict(common,kind='edge',child=child,edges=[[parent,F(1,k)],[child,F(1)]]); incoming[child]=j
                    jobs.append(job); outgoing[parent].append(j); path_jobs[v,sign,cp]=j
    for row in ranges:
        for s in range(row['listed_units']): machines.append({'machine':row['start']+s,'kind':'clause_unit','clause':row['clause'],'unit':s})
    dummy=base==0
    if dummy: base=1; machines=[{'machine':0,'kind':'dummy'}]
    return {'k':k,'h':h,'labels':labels,'A':A,'arity':arity,'trees':trees,'roots':roots,'incoming':incoming,'outgoing':outgoing,'jobs':jobs,'clause_ports':clause_ports,'ranges':ranges,'machines':machines,'internal_count':internal_count,'full_m':base,'dummy':dummy,'path_jobs':path_jobs}


def processing_time(job,machine):
    for u,p in job['edges']:
        if u==machine: return p
    if job['kind']=='port':
        row=job['external']
        if row['start']<=machine<row['start']+row['count']: return F(1)
    raise ValueError('unavailable original edge')


def actual_loads(I,sigma):
    if len(sigma)!=len(I['jobs']): raise ValueError('all original jobs required')
    load={}
    for j,u in enumerate(sigma):
        if type(u) is not int or not 0<=u<I['full_m']: raise ValueError('invalid machine')
        load[u]=load.get(u,F(0))+processing_time(I['jobs'][j],u)
    return load


def finish(I,sigma,bound,**extra):
    load=actual_loads(I,sigma); C=max(load.values(),default=F(0))
    if C>bound: raise RuntimeError('actual schedule exceeded proved bound')
    listed=[{'machine':row['machine'],'load':load.get(row['machine'],F(0))} for row in I['machines']]
    listed_ids={row['machine'] for row in I['machines']}
    if any(u not in listed_ids and value for u,value in load.items()): raise RuntimeError('omitted unit used')
    result={'source_claims':SOURCE_CLAIMS,'k':I['k'],'h':I['h'],'variable_labels':I['labels'],'roots':I['roots'],'jobs':I['jobs'],'sigma':sigma,'listed_machines':I['machines'],'listed_loads':listed,'clause_ranges':I['ranges'],'full_machine_count':I['full_m'],'dummy_used':I['dummy'],'internal_machine_count':I['internal_count'],'omitted_unit_machine_count':sum(I['A'])-sum(row['listed_units'] for row in I['ranges']),'omitted_unit_machine_load':F(0),'makespan':C,'bound':bound}
    result.update(extra); return result


def covering_matching(adj,slot_count):
    """Generic exact covering matching; Hall is certified by input fractions."""
    left=[None]*len(adj); right=[None]*slot_count
    for start in range(len(adj)):
        queue=deque([start]); previous={start:None}; seen_slots=set(); found=None
        while queue and found is None:
            u=queue.popleft()
            for s in adj[u]:
                if s in seen_slots: continue
                seen_slots.add(s)
                if right[s] is None: found=(u,s); break
                v=right[s]
                if v not in previous: previous[v]=(u,s); queue.append(v)
        if found is None: raise RuntimeError('fractional Hall certificate failed')
        u,s=found
        while True:
            left[u]=s; right[s]=u
            if u==start: break
            u,s=previous[u]
    if len(set(left))!=len(left): raise RuntimeError('matching duplicated a slot')
    return left


def given_witness(data,r,t):
    I=build_instance(data); k=I['k']; r=integer(r,1)
    if r>k: raise ValueError('r<=k required')
    if type(t) not in (list,tuple) or len(t)!=len(I['jobs']): raise ValueError('one exact t per original job required')
    t=[rational(z) for z in t]
    if any(z<0 or z>1 for z in t): raise ValueError('fractions must lie in [0,1]')
    jobs=I['jobs']; rows={}; allocations=[[] for j in jobs]
    def put(j,u,mass):
        if mass:
            rows.setdefault(u,{})[j]=rows.setdefault(u,{}).get(j,F(0))+mass
            allocations[j].append([u,mass])
    for j,job in enumerate(jobs):
        if job['kind']=='selector':
            put(j,job['edges'][0][0],t[j]); put(j,job['edges'][1][0],1-t[j])
        else:
            put(j,job['parent'],1-t[j])
            if job['kind']=='edge': put(j,job['child'],t[j])
    clause_mass=[]
    for c,ports in enumerate(I['clause_ports']):
        total=sum((t[j] for j in ports),F(0)); clause_mass.append(total)
        if total>I['A'][c]: raise ValueError('clause fractional mass exceeds original capacity')
        unit=0; filled=F(0)
        for j in ports:
            mass=t[j]
            while mass:
                if unit>=I['ranges'][c]['listed_units']: raise RuntimeError('clipped unit range insufficient')
                take=min(mass,1-filled); put(j,I['ranges'][c]['start']+unit,take); mass-=take; filled+=take
                if filled==1: unit+=1; filled=F(0)
    B=k-r+1; row_mass=[]
    for u in range(I['internal_count']):
        mass=sum(rows.get(u,{}).values(),F(0)); row_mass.append(mass)
        if mass>B: raise ValueError('strong row-cardinality witness violated')
    for alloc in allocations:
        if sum((mass for u,mass in alloc),F(0))!=1: raise RuntimeError('fractional job column not exactly one')
    slots=[]; adj=[[] for j in jobs]
    def add_row(u,ordered):
        local=[]; position=F(0)
        for j in ordered:
            mass=rows.get(u,{}).get(j,F(0))
            while mass:
                index=position.numerator//position.denominator
                if index==len(local):
                    s=len(slots); local.append(s); slots.append({'slot':s,'machine':u,'fractions':[]})
                s=local[index]; take=min(mass,F(index+1)-position)
                slots[s]['fractions'].append([j,take])
                if s not in adj[j]: adj[j].append(s)
                position+=take; mass-=take
        return local
    for u in range(I['internal_count']):
        local=add_row(u,[I['incoming'][u]]+I['outgoing'][u])
        if len(local)>B: raise RuntimeError('too many internal slots')
    for u,row in sorted(rows.items()):
        if u>=I['internal_count']:
            if sum(row.values(),F(0))>1: raise RuntimeError('unit fractional overload')
            if len(add_row(u,sorted(row)))>1: raise RuntimeError('too many unit slots')
    for slot in slots:
        if not 0<sum((mass for j,mass in slot['fractions']),F(0))<=1: raise RuntimeError('invalid slot mass')
    for j in range(len(jobs)):
        if sum((mass for slot in slots for jj,mass in slot['fractions'] if jj==j),F(0))!=1: raise RuntimeError('slot column not one')
    matched=covering_matching(adj,len(slots)); sigma=[slots[s]['machine'] for s in matched]
    bound=F(2)-F(r,k) if jobs else F(0)
    return finish(I,sigma,bound,mode='given-strong-witness',r=r,t=t,internal_row_cardinality=row_mass,clause_fractional_mass=clause_mass,slots=slots,job_slots=adj,matching=matched)


def calibrated(data,r):
    I=build_instance(data); k=I['k']; r=integer(r,1)
    if r>k: raise ValueError('r<=k required')
    if not I['roots']:
        return finish(I,[],F(0),mode='calibrated-empty',r=r,x_h=None,t=[])
    x=[F(1,2)]
    for depth in range(I['h']): x.append((r-1+x[-1])/k)
    if any(d*x[-1]>a for d,a in zip(I['arity'],I['A'])): raise ValueError('calibrated clause inequality violated')
    t=[F(1,2) if job['kind']=='selector' else x[len(job['path'])] for job in I['jobs']]
    result=given_witness(data,r,t); result.update(mode='calibrated',x_by_depth=x,x_h=x[-1]); return result


def variable_clause_matching(I):
    neighbors=[]
    for pair in I['trees']: neighbors.append(sorted(set(c for tree in pair for c in tree['wiring'].values())))
    owners=[[] for c in I['A']]; assigned=[None]*len(neighbors)
    for start in range(len(neighbors)):
        queue=deque([start]); previous={start:None}; seen=set(); found=None
        while queue and found is None:
            u=queue.popleft()
            for c in neighbors[u]:
                if c in seen: continue
                seen.add(c)
                if len(owners[c])<min(I['A'][c],I['arity'][c]): found=(u,c); break
                for v in owners[c]:
                    if v not in previous: previous[v]=(u,c); queue.append(v)
        if found is None:
            reached=sorted(previous); clauses=sorted(set(c for v in reached for c in neighbors[v]))
            if sum(I['A'][c] for c in clauses)>=len(reached): raise RuntimeError('matching failure lacks Hall cut')
            return None,{'variables':reached,'clauses':clauses,'capacity':sum(I['A'][c] for c in clauses),'variable_count':len(reached)}
        u,c=found
        while True:
            old=assigned[u]
            if old is not None: owners[old].remove(u)
            owners[c].append(u); assigned[u]=c
            if u==start: break
            u,c=previous[u]
    return assigned,None


def bounded_density(data,D):
    I=build_instance(data); D=rational(D)
    if D<2: raise ValueError('D>=2 required')
    if any(d>D*a for d,a in zip(I['arity'],I['A'])): raise ValueError('bounded density d<=D*A required')
    ratio=F(2)-1/(4*D)
    if not I['roots']: return finish(I,[],F(0),mode='bounded-density-empty',D=D,approximation_ratio=ratio,exact_optimum=F(0))
    k=I['k']
    if k>=D:
        r=1+((k-1)*D.denominator)//(2*D.numerator)
        result=calibrated(data,r); result.update(mode='bounded-density-calibrated',D=D,approximation_ratio=ratio)
        if result['bound']>ratio: raise RuntimeError('calibrated bound misses approximation constant')
        return result
    assignment,cut=variable_clause_matching(I)
    sigma=[job['edges'][0][0] if job['kind']=='selector' else job['parent'] for job in I['jobs']]
    if assignment is None:
        return finish(I,sigma,F(2),mode='bounded-density-optimum-two',D=D,approximation_ratio=ratio,exact_optimum=F(2),matching_hall_cut=cut)
    next_unit=[0]*len(I['A']); paths=[]
    for v,c in enumerate(assignment):
        found=None
        for sign,tree in enumerate(I['trees'][v]):
            for path,clause in sorted(tree['wiring'].items()):
                if clause==c: found=(sign,path); break
            if found is not None: break
        if found is None: raise RuntimeError('matched clause unreachable')
        sign,path=found; sigma[v]=I['roots'][v][sign]
        for depth in range(1,I['h']+1):
            j=I['path_jobs'][v,sign,path[:depth]]; job=I['jobs'][j]
            if depth<I['h']: sigma[j]=job['child']
            else:
                sigma[j]=I['ranges'][c]['start']+next_unit[c]; next_unit[c]+=1
        paths.append({'variable':v,'sign':sign,'path':list(path),'clause':c})
    return finish(I,sigma,F(2)-F(1,k),mode='bounded-density-path-matching',D=D,approximation_ratio=ratio,variable_clause_matching=assignment,selected_paths=paths)


def encode(V,k,h,wiring,A):
    paths=list(product(range(k),repeat=h)); variables=[]; pos=0
    for v in range(V):
        row={'id':v}
        for name in ('positive','negative'):
            row[name]=[{'path':list(path),'clause':wiring[pos+j]} for j,path in enumerate(paths)]; pos+=len(paths)
        variables.append(row)
    if pos!=len(wiring): raise ValueError('wrong wiring count')
    return {'k':k,'h':h,'variables':variables,'clause_capacities':A}


def small_actual_optimum(data):
    """Audit only: enumerate all original legal sigma, independently of slots."""
    I=build_instance(data)
    choices=[]
    for job in I['jobs']:
        eligible={u for u,p in job['edges']}
        if job['kind']=='port': eligible.update(range(job['external']['start'],job['external']['start']+job['external']['count']))
        choices.append(sorted(eligible))
    best=None; witness=None; count=0
    for sigma in product(*choices):
        load=actual_loads(I,sigma); C=max(load.values(),default=F(0)); count+=1
        if best is None or C<best: best=C; witness=list(sigma)
    return best,witness,count


def jsonable(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):jsonable(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [jsonable(y) for y in x]
    return x


def audit():
    from random import Random
    import hashlib,platform,time
    started=time.perf_counter(); rng=Random(110841); counts=Counter(); hist=Counter(); cases=[]
    def check(data,result):
        I=build_instance(data); load=actual_loads(I,result['sigma']); C=max(load.values(),default=F(0))
        assert C==result['makespan']<=result['bound']
        assert all(row['load']==load.get(row['machine'],F(0)) for row in result['listed_loads'])
        assert len(result['jobs'])==len(result['sigma'])
        assert all(u<I['internal_count'] or p<=1 for u,p in load.items())
        assert result['omitted_unit_machine_load']==0
        for row in result['clause_ranges']: assert row['listed_units']==min(row['count'],row['arity'])
        if 'matching' in result:
            assert len(result['matching'])==len(set(result['matching']))==len(I['jobs'])
            for j,s in enumerate(result['matching']): assert s in result['job_slots'][j]
        counts['actual_schedules']+=1; counts['actual_jobs']+=len(I['jobs']); hist[str(C)]+=1
    # Exhaustive small wirings; every quota r gets the minimal calibrated caps.
    for V,k,h,C in ((1,1,1,3),(1,1,3,2),(2,1,2,2),(1,2,1,3),(1,2,2,2),(1,3,1,2)):
        n=2*V*k**h
        for wiring in product(range(C),repeat=n):
            d=[wiring.count(c) for c in range(C)]
            for r in range(1,k+1):
                x=F(1,2)
                for depth in range(h): x=(r-1+x)/k
                A=[(z*x.numerator+x.denominator-1)//x.denominator for z in d]
                data=encode(V,k,h,wiring,A); result=calibrated(data,r); check(data,result); counts['exhaustive_calibrated_wirings_r']+=1
    for trial in range(240):
        V=rng.randrange(1,4); k=rng.randrange(1,5); h=rng.randrange(1,4); C=rng.randrange(1,10); r=rng.randrange(1,k+1)
        wiring=[rng.randrange(C) for j in range(2*V*k**h)]; data=encode(V,k,h,wiring,[0]*C); I=build_instance(data)
        t=[F(0) for j in I['jobs']]
        for v in range(V): t[v]=F(rng.randrange(25),24)
        for u in range(I['internal_count']):
            incoming=I['incoming'][u]; job=I['jobs'][incoming]
            y=t[incoming] if job['kind']!='selector' or job['edges'][0][0]==u else 1-t[incoming]
            children=I['outgoing'][u]; values={j:F(1) for j in children}; excess=F(k-r+1)-y
            order=list(children); rng.shuffle(order)
            for j in order:
                take=min(excess,F(rng.randrange(25),24)); values[j]-=take; excess-=take
            for j in order:
                take=min(excess,values[j]); values[j]-=take; excess-=take
            assert excess==0
            for j in children: t[j]=values[j]
        A=[]
        for ports in I['clause_ports']:
            mass=sum((t[j] for j in ports),F(0)); A.append((mass.numerator+mass.denominator-1)//mass.denominator)
        data['clause_capacities']=A; result=given_witness(data,r,t); check(data,result); counts['random_general_given_witnesses']+=1
    Ds=[F(2),F(5,2),F(3),F(9,2),F(8)]
    for trial in range(320):
        V=rng.randrange(1,5); k=rng.randrange(1,7); h=rng.randrange(1,4); C=rng.randrange(1,13); D=Ds[trial%len(Ds)]
        wiring=[rng.randrange(C) for j in range(2*V*k**h)]; d=[wiring.count(c) for c in range(C)]
        A=[(z*D.denominator+D.numerator-1)//D.numerator for z in d]
        if trial%29==0: A[rng.randrange(C)]+=10**100+151
        data=encode(V,k,h,wiring,A); result=bounded_density(data,D); check(data,result); counts['random_bounded_density']+=1; counts[result['mode']]+=1
    # Actual original-matrix OPT examples, including smallest strong-LP cut.
    nonnecessary=encode(1,2,1,[0,0,0,0],[2]); best,sigma,n=small_actual_optimum(nonnecessary)
    assert best==1; result=finish(build_instance(nonnecessary),sigma,F(1)); check(nonnecessary,result)
    try: calibrated(nonnecessary,2)
    except ValueError: pass
    else: raise AssertionError('impossible strong witness accepted')
    assert 2*(2-1)+1>2
    cases.append({'name':'strong-LP-not-necessary-four-machines-five-jobs','input':nonnecessary,'optimum':best,'assignments_enumerated':n,'certificate':result,'strong_LP_total_outflow_lower_bound':3,'clause_capacity':2})
    weak=encode(1,4,1,[0]*4+[1]*4,[1,1]); best,sigma,n=small_actual_optimum(weak)
    assert best==F(7,4); result=finish(build_instance(weak),sigma,F(7,4)); check(weak,result)
    weak_t=[F(1,2)]+[F(1,4)]*8
    assert 4*F(1,4)==2*F(1,2) and 4*F(1,4)<=1
    try: given_witness(weak,2,weak_t)
    except ValueError: pass
    else: raise AssertionError('weak-only witness accepted as strong')
    cases.append({'name':'weak-LP-not-sufficient-four-machines-nine-jobs','input':weak,'optimum':best,'assignments_enumerated':n,'weak_t':weak_t,'certificate':result})
    failure=encode(2,2,1,[0]*8,[1]); result=bounded_density(failure,F(8)); check(failure,result)
    best,sigma,n=small_actual_optimum(failure); assert best==2==result['exact_optimum']; assert result['mode']=='bounded-density-optimum-two'
    cases.append({'name':'small-k-failed-matching-optimum-two','input':failure,'optimum':best,'assignments_enumerated':n,'certificate':result})
    counts['small_original_OPT_instances']=len(cases); counts['all_legal_assignments_enumerated']=sum(case['assignments_enumerated'] for case in cases)
    for k,h,D,A in ((1,10**100,F(2),[]),(10**100,10**100,F(5,2),[10**100+151])):
        data={'k':k,'h':h,'variables':[],'clause_capacities':A}; result=bounded_density(data,D); check(data,result); assert result['makespan']==0; counts['empty_huge_binary_boundaries']+=1
    for data in (encode(1,1,80,[0,0],[1]),encode(1,2,7,[0]*256,[10**100+151])):
        result=bounded_density(data,F(2)); check(data,result); counts['deep_explicit_large_capacity_boundaries']+=1
    huge_denominator=10**5000+151
    data=encode(1,1,1,[0,0],[str(huge_denominator)])
    result=bounded_density(data,'2');check(data,result)
    assert result['makespan']==1
    data=encode(1,1,1,[0,0],[1])
    z=F(1,huge_denominator)
    result=given_witness(data,1,['1/'+str(huge_denominator),'1/'+str(huge_denominator),str(huge_denominator-1)+'/'+str(huge_denominator)])
    check(data,result);assert result['makespan']==1
    counts['decimal_text_over_4300_digits_exact_cases']=2
    invalids=[({'k':2,'h':1,'variables':[{'id':0,'positive':[{'path':[0],'clause':0}],'negative':[{'path':[0],'clause':0}]}],'clause_capacities':[1]},'missing-full-branch'),(encode(1,2,1,[0]*4,[0]),'no-clause-capacity')]
    for data,name in invalids:
        try: bounded_density(data,F(2))
        except ValueError: counts['invalid_inputs_rejected']+=1
        else: raise AssertionError(name)
    for D in ('1.99',0,-2):
        try: bounded_density({'k':1,'h':1,'variables':[],'clause_capacities':[]},D)
        except ValueError: counts['invalid_D_rejected']+=1
        else: raise AssertionError('invalid D')
    return {'status':'passed','source_claims':SOURCE_CLAIMS,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seed':110841,'python':platform.python_version(),'counts':dict(counts),'actual_makespan_histogram':dict(sorted(hist.items())),'actual_original_matrix_boundary_certificates':cases,'scope':'Finite exact checks of production schedules and three small original-P optimum examples; not a general proof or novelty certification. Given-witness is a sufficient contract only; no LP solver; production never calls OPT oracle.','elapsed_seconds':time.perf_counter()-started}


if __name__=='__main__':
    import argparse,json,sys
    parser=argparse.ArgumentParser(); parser.add_argument('--input'); parser.add_argument('--output'); parser.add_argument('--mode',choices=['bounded','calibrated','witness'],default='bounded'); parser.add_argument('--D',default='2'); parser.add_argument('--r',default='1'); parser.add_argument('--t-file'); args=parser.parse_args()
    if args.input:
        data=json.loads(Path(args.input).read_text())
        if args.mode=='bounded': result=bounded_density(data,args.D)
        elif args.mode=='calibrated': result=calibrated(data,args.r)
        else:
            if not args.t_file: parser.error('--t-file required for witness')
            result=given_witness(data,args.r,json.loads(Path(args.t_file).read_text()))
    else: result=audit()
    output=json.dumps(jsonable(result),ensure_ascii=False,indent=2)+'\n'
    if args.output:
        with Path(args.output).open('x') as handle: handle.write(output)
    else: sys.stdout.write(output)
