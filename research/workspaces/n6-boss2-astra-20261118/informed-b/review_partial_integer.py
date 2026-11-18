"""Non-author integer replay of the continuous-target certificate and its two examples."""
from fractions import Fraction as Q
from itertools import product
from math import lcm
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[4]
PACK=ROOT/'tools/evidence/six-partial-fractional-cover'
PIN='bac98ca7fd6ef1c7eafc1d82fbdadc9555fbd37cd08ba427452b08cc4a2910ac'
FREEZE=ROOT/f'research/runs/n6-boss2-astra-20261118/studio/freezes/SIX-PARTIAL-FRACTIONAL-COVER-R1/{PIN}.json'
frozen=json.loads(FREEZE.read_bytes());refs=frozen['content_refs']
for ref in refs:
    data=(ROOT/ref['path']).read_bytes()
    assert hashlib.sha256(data).hexdigest()==ref['sha256']
cert=json.loads((PACK/'certificate.json').read_bytes());tau=Q(cert['tau']);alpha=Q(cert['coverage_coefficient'])
assert tau==Q(4977,1000) and 2*alpha>1 and 1/alpha==Q(cert['opt_over_welfare_bound'])
rows={g:{k:Q(v) for k,v in w.items()} for g,w in cert['weights'].items()}
D=lcm(alpha.denominator,*(v.denominator for w in rows.values() for v in w.values()));L={g:{k:int(v*D) for k,v in w.items()} for g,w in rows.items()}
assert all(v>0 for w in L.values() for v in w.values())
branches=[(0,6),(1,6),(2,6),(2,4),(3,5)]; assert set(L)=={'actual'}|{f'{i}:{j}' for i,j in branches}
scale=60000

def divided(n,d):
    q,r=divmod(n,d);assert not r
    return q

def payoff(bits,i):return divided(scale,sum(bits)) if bits[i] else 0

def branch_value(group,source,bits,common,o,tail):
    total=0
    for name,weight in L[group].items():
        if name.startswith('F'):
            i=int(name[1:]);assert i>source
            term=divided(4977*payoff(bits,i),1000)-divided(scale*o,6-i+sum(bits[:i]))
        elif name.startswith('H'):
            i,k=map(int,name[1:].split('-'));assert i>source and k==6+len(tail)
            term=payoff(bits,i)-divided(scale*bits[-1],6-i+sum(bits[:i]))
        elif name=='R1/2':
            assert source<4
            p=sum(bits[:4]);term=divided(4977*payoff(bits,4),1000)+divided(payoff(bits,5),2)-divided(scale*o,p+1)
            if p==0 and bits[4]:term+=divided(scale*o,4)
        elif name=='IC-own':
            assert source>=0
            term=payoff(common[:6],source)-payoff(bits,source)
        else:
            assert name.startswith('CAP')
            j=int(name[3:]);term=scale*(common[6]-(tail[j] if source>=0 else common[j]))
        total+=weight*term
    return total

gaps=[];count=0
for a in product(range(2),repeat=7):
    for o in (0,1):
        e=a[:6];v=branch_value('actual',-1,e,a,o,())
        for i,j in branches:
            local=[]
            for t in product(range(2),repeat=5-i):
                local.append(branch_value(f'{i}:{j}',i,e[:i]+(a[j],)+t,a,o,t));count+=1
            v+=max(local)
        gaps.append(scale*(D*int(any(e))-int(alpha*D)*o)-v)
assert min(gaps)==0 and gaps.count(0)==17 and len(gaps)==256 and count==17408
saved=json.loads((PACK/'replay.json').read_bytes());fresh=json.loads(subprocess.check_output([sys.executable,'-B',str(PACK/'verify.py')]))
assert fresh==saved and Q(saved['half_cover_full_fractional_cutoff'])==2*tau*alpha
cycle_sets=[{(i+k)%99 for k in range(20)} for i in range(99)]
assert len(set.union(*(cycle_sets[i] for i in (0,20,40,60,80,98))))==99
assert all(sum(x in B for B in cycle_sets)==20 for x in range(99))
assert Q(49,10)<Q(99,20)<2*tau*alpha
excess=2*alpha*(40000+Q(977,1000))-40002
assert excess>0
print(json.dumps({'freeze_sha256':hashlib.sha256(FREEZE.read_bytes()).hexdigest(),'reviewed_refs':len(refs),'rows':sum(map(len,L.values())),'common_endpoints':len(gaps),'branch_patterns':count,'zero_endpoints':gaps.count(0),'minimum':str(Q(min(gaps),D*scale)),'least_positive':str(Q(min(v for v in gaps if v>0),D*scale)),'author_replay_equal':fresh==saved,'full_cover_threshold':str(2*tau*alpha),'cycle_coverage':99,'second_example_surplus':str(excess)},indent=2))
