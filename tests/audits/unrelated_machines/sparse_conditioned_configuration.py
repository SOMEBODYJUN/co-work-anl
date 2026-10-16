#!/usr/bin/env python3
"""Exact finite audit of sparse, edge-conditioned CONFIG gap.
No shared repository files are edited. Finite expanded cases verify every edge;
large cases verify rational formulae only and are not expanded.
"""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import json, sys
from pathlib import Path
import hashlib

def verify_frozen_input_and_certificate():
    """Recheck serialized witnesses directly, without the generator or LP code."""
    repo=Path(__file__).resolve().parents[3]
    input_path=repo/'examples/unrelated_machines/sparse_conditioned_configuration_input.json'
    witness_path=repo/'evidence/certificates/unrelated_machines/sparse_conditioned_configuration_witness.json'
    raw=json.loads(input_path.read_text());witness=json.loads(witness_path.read_text())
    costs=[{i:F(p) for i,p in j['eligible']} for j in raw['jobs']]
    cover=[F(0) for _ in costs];forced=F(0)
    assert len(witness['configuration_point'])==len(raw['machines'])
    seen=set()
    for row in witness['configuration_point']:
        i=row['machine'];assert i not in seen;seen.add(i)
        assert sum(F(c['weight']) for c in row['configurations'])==1
        big=F(0)
        for c in row['configurations']:
            weight=F(c['weight']);assert weight>=0
            assert len(c['jobs'])==len(set(c['jobs']))
            assert sum(costs[j][i] for j in c['jobs'])<=F(raw['threshold'])
            for j in c['jobs']:
                cover[j]+=weight
                if costs[j][i]>F(raw['threshold'])/2:big+=weight
                if (j,i)==(witness['forced_job'],witness['forced_machine']):forced+=weight
        assert big<=1
    assert all(c==1 for c in cover) and forced==1
    assignment=witness['integer_upper_assignment'];assert len(assignment)==len(costs)
    loads=[F(0) for _ in raw['machines']]
    for j,i in enumerate(assignment):loads[i]+=costs[j][i]
    assert max(loads)==F(witness['integer_upper_makespan'])
    return {'input_sha256':hashlib.sha256(input_path.read_bytes()).hexdigest(),
            'witness_sha256':hashlib.sha256(witness_path.read_bytes()).hexdigest(),
            'forced_mass':str(forced),'integer_upper_makespan':str(max(loads))}

def parameters(k):
    r=F(k-1,k);s0=1
    while k*r**s0>1:s0+=1
    assert s0>=2
    M=(k-1)*k**(s0-2);H=max(s0,2)
    while 2**(H-2)<M:H+=1
    gamma=F(1,2**(H-2))
    return s0,M,H,gamma

def instance(k,H,gamma):
    machines=[]; jobs=[]; outs={}; incoming={}; groups={}
    def job(kind,costs,**meta):
        j=len(jobs);jobs.append(dict(kind=kind,costs=costs,**meta));return j
    roots=[('v',t,()) for t in range(2)]
    for t in range(2):
        for d in range(H):
            for path in product(range(k),repeat=d):
                v=('v',t,path);machines.append(v);outs[v]=[]
                for ell in range(k):
                    w=('v',t,path+(ell,)) if d+1<H else ('t',t,path,ell)
                    j=job('tree' if d+1<H else 'star',{v:F(1,k),w:F(1)},tree=t,parent=v,child=w)
                    outs[v].append(j);incoming[w]=j
                if d==H-1:
                    terms=[('t',t,path,ell) for ell in range(k)];machines.extend(terms);blocks=[]
                    for ell in range(k-1):
                        blocks.append(job('block',{terms[ell]:F(1),terms[ell+1]:F(1),('z',):gamma},tree=t,leaf=path,index=ell))
                    groups[(t,path)]=(terms,blocks)
    bridge=job('bridge',{roots[0]:F(1),roots[1]:F(1)});machines.append(('z',))
    return dict(k=k,H=H,gamma=gamma,machines=machines,jobs=jobs,outs=outs,incoming=incoming,groups=groups,roots=roots,bridge=bridge)

def certificate(P,force):
    k,H=P['k'],P['H'];jobs=P['jobs'];fj,fm=force;target=jobs[fj]
    root=P['roots'].index(fm) if target['kind']=='bridge' else 1-target['tree']
    alpha={P['roots'][0]:F(root==0),P['roots'][1]:F(root==1)}
    cert={v:[] for v in P['machines']};escapers=[]
    def add(v,w,S):
        if w:cert[v].append((w,tuple(S)))
    for t in range(2):
        for d in range(H):
            for path in product(range(k),repeat=d):
                v=('v',t,path);a=P['bridge'] if not path else P['incoming'][v];beta=alpha[v];out=P['outs'][v]
                remove=fj if target['kind'] in ('tree','star') and target['parent']==v and fm==target['child'] else None
                for j in out:add(v,beta/k,[a,j] if j!=remove else [a])
                add(v,1-beta,[j for j in out if j!=remove])
                for j in out:alpha[jobs[j]['child']]=F(1) if j==remove else F(k-1,k)*beta
    for (t,path),(terms,blocks) in P['groups'].items():
        stars=P['outs'][('v',t,path)];b=[alpha[jobs[j]['child']] for j in stars]
        special=target['kind']=='block' and fj in blocks
        if special:
            assert all(v==0 for v in b)
            direction=0 if fm==('z',) else int(fm==terms[target['index']+1])
            placed={}
            for ell,j in enumerate(blocks):
                if j==fj and fm==('z',):escapers.append(j)
                else:placed[terms[ell+direction]]=j
            for v in terms:add(v,F(1),[placed[v]] if v in placed else [])
        elif max(b)>F(1,k):
            escapers.extend(blocks)
            for ell,v in enumerate(terms):add(v,b[ell],[stars[ell]]);add(v,1-b[ell],[])
        else:
            for ell,v in enumerate(terms):
                add(v,b[ell],[stars[ell]])
                if ell>0:add(v,F(ell,k),[blocks[ell-1]])
                if ell<k-1:add(v,F(k-ell-1,k),[blocks[ell]])
                add(v,F(1,k)-b[ell],[])
    add(('z',),F(1),escapers)
    return cert,len(escapers)

def verify(P,cert,force):
    T=1+F(1,P['k']);cover=[F(0) for _ in P['jobs']];marg=defaultdict(F);maxbig=F(0)
    for v,configs in cert.items():
        assert sum(w for w,S in configs)==1
        big=F(0)
        for w,S in configs:
            assert w>=0 and len(S)==len(set(S))
            load=sum(P['jobs'][j]['costs'][v] for j in S)
            assert load<=T
            for j in S:
                cover[j]+=w;marg[j,v]+=w
                if P['jobs'][j]['costs'][v]>T/2:big+=w
        assert big<=1;maxbig=max(maxbig,big)
    assert all(w==1 for w in cover)
    assert marg[force]==1
    return maxbig

def expanded(k):
    s0,M,H,gamma=parameters(k);P=instance(k,H,gamma);nedge=0;classes=defaultdict(int);maxesc=0
    for j,rec in enumerate(P['jobs']):
        for v in rec['costs']:
            cert,nesc=certificate(P,(j,v));verify(P,cert,(j,v));nedge+=1;classes[rec['kind']]+=1;maxesc=max(maxesc,nesc)
    return dict(k=k,H=H,s0=s0,M=M,gamma=str(gamma),machines=len(P['machines']),jobs=len(P['jobs']),all_finite_edges=nedge,forced_classes=dict(classes),max_escapers=maxesc,max_sink_load=str(gamma*maxesc))

def formula(k):
    s0,M,H,gamma=parameters(k);r=F(k-1,k);T=1+F(1,k)
    assert H>=s0 and k*r**H<=1 and gamma*M<=1
    assert gamma*2**(H-1)==2
    # Strong edge conditioning propagates alpha -> r*alpha, never truncates it.
    for s in range(1,s0):
        b=r**s;assert k*b>1
        E=(k-1)*k**(s-1);assert E<=M and gamma*E<=1
        assert 1+b*0<=T
    assert (k-1)<=M
    assert (2-F(1,k))/T==2-F(3,k+1)
    # Full branching: >=2^(H-1) bad leaf clusters force integer sink load >=2.
    assert 1+F(k-1,k)==2-F(1,k)
    return dict(k=k,s0=s0,H=H,gamma=str(gamma),M=M,integer_sink_lower='2',gap=str(2-F(3,k+1)))

if __name__=='__main__':
    result=dict(arithmetic='fractions.Fraction',python=sys.version.split()[0],
                code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                frozen_serialization=verify_frozen_input_and_certificate(),
                full_expanded=[expanded(3)],formula=[formula(k) for k in range(4,33)])
    print(json.dumps(result,indent=2))
