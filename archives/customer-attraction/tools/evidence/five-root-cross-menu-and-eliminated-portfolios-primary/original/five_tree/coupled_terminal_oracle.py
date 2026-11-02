"""Exact diagonal/offdiagonal root-second matching support oracle.

No welfare claim: this handles only the missing common-index correlation.
"""
from itertools import product
from fractions import Fraction as F
from pathlib import Path
import json, hashlib

TYPES=tuple(product((0,1),repeat=5))
SECOND=tuple(product((0,1),repeat=4))

def target_counts(second_hist):
    return tuple(sum(n*t[-1] for n,t in zip(second_hist,SECOND) if t[0]==group) for group in (0,1))

def greedy(root_hist, counts, maximize):
    """Optimize sum_i j_i/(1+p_i) with shared t_i and two J counts."""
    assigned=[0]*32;value=F()
    for group,count in enumerate(counts):
        ids=[i for i,t in enumerate(TYPES) if t[0]==group]
        ids.sort(key=lambda i:F(1,1+sum(TYPES[i][:-1])),reverse=maximize)
        remaining=count
        for i in ids:
            use=min(remaining,root_hist[i]);assigned[i]=use
            value+=use*F(1,1+sum(TYPES[i][:-1]));remaining-=use
        assert remaining==0
    return value,assigned

def support(root_hist, second_hist, diagonal_weight, offdiagonal_weight):
    """Maximize the weighted two-row coefficient over every joint matching."""
    assert sum(root_hist)==sum(second_hist)==5
    droot=sum(n*t[0] for n,t in zip(root_hist,TYPES))
    dsecond=sum(n*t[0] for n,t in zip(second_hist,SECOND))
    assert droot==dsecond
    counts=target_counts(second_hist);totalcount=sum(counts)
    den=sum(n*F(1,1+sum(t[:-1])) for n,t in zip(root_hist,TYPES))
    share=sum(n*F(t[-1],sum(t)) for n,t in zip(root_hist,TYPES) if t[-1])
    slope=offdiagonal_weight-diagonal_weight
    match,assigned=greedy(root_hist,counts,maximize=slope>=0)
    diagonal=share-match
    offdiagonal=4*share-totalcount*den+match
    return diagonal_weight*diagonal+offdiagonal_weight*offdiagonal,assigned

def compositions(n,k):
    if k==1:
        yield (n,);return
    for first in range(n+1):
        for tail in compositions(n-first,k-1):yield (first,)+tail

def audit():
    # Every possible (t,p) cost class is represented; K and the identities
    # of X/Y/Z do not affect the matching objective.
    classes=((0,0),(0,1),(0,2),(0,3),(1,1),(1,2),(1,3),(1,4))
    histograms=0;assignments=0;conditional_checks=0
    for hist in compositions(5,8):
        records=[tp for n,tp in zip(hist,classes) for _ in range(n)]
        groups={}
        for js in product((0,1),repeat=5):
            key=tuple(sum(j for j,(t,p) in zip(js,records) if t==group) for group in (0,1))
            value=sum((F(j,p+1) for j,(t,p) in zip(js,records)),F())
            groups.setdefault(key,[]).append(value);assignments+=1
        for counts,values in groups.items():
            costs=[]
            for maximize in (False,True):
                ans=F()
                for group,count in enumerate(counts):
                    weights=sorted((F(1,p+1) for t,p in records if t==group),reverse=maximize)
                    ans+=sum(weights[:count],F())
                costs.append(ans)
            assert costs==[min(values),max(values)]
            conditional_checks+=1
        histograms+=1
    # This local two-histogram state passes the summed 25-row inequality
    # and fails every common-index diagonal completion.
    rh=[0]*32;rh[16]=1;rh[13]=1;rh[14]=3
    sh=[0]*16;sh[9]=1;sh[0]=4
    diagonal,_=support(rh,sh,F(1),F(0))
    offdiagonal,_=support(rh,sh,F(0),F(1))
    assert diagonal==F(-1,6) and offdiagonal==F(1,4)
    assert diagonal+offdiagonal==F(1,12)>0
    report={'scope':'Exact matching-support algebra only; the local information example is not a game/SPE or a full-template feasible point',
            'status':'passed','cost_histograms':histograms,'joint_assignments':assignments,
            'conditional_extremum_checks':conditional_checks,
            'strict_local_information_example':{'root_hist':rh,'second_hist':sh,
                 'all25_slack':str(diagonal+offdiagonal),'maximum_diagonal_slack':str(diagonal),
                 'maximum_offdiagonal_slack':str(offdiagonal)},
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':audit()
