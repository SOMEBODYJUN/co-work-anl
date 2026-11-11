"""Audit the frozen two-phase completion on the full old R/Z terminal network.

Candidate failure is not projected infeasibility.  Query payoffs are computed
directly, preserving the genuine old R prefix and every literal node.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
import argparse,json
from common import *

WITNESS=WORK/'multi_terminal_joint/common_completion_19556.json'
KINDS=('R-R','R-Z','Z-R','Z-Z')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--point',type=Path,default=POINT)
    ap.add_argument('--witness',type=Path,default=WITNESS)
    ap.add_argument('--interface',type=Path,default=HERE/'interface_audit_19556.json')
    ap.add_argument('--output',type=Path,default=HERE/'full_network_candidate_19556.json')
    args=ap.parse_args()
    point,cols,masses,hist,groups,ov,families=parse(args.point)
    w=json.loads(args.witness.read_bytes());assert w['input_sha256']==sha(args.point)
    assert tuple(map(tuple,w['literal_node_order']))==NODES
    pairs=[(i,j,pairclass(e,f)) for i,e in enumerate(NODES) for j,f in enumerate(NODES)]
    counts=Counter(cl for i,j,cl in pairs)
    phase_values={phase:defaultdict(F) for phase in ('A','B')}
    per_hist={phase:defaultdict(dict) for phase in ('A','B')}
    for phase in ('A','B'):
      for ent in w['phases'][phase]:
        hi=ent['hist_column'];h=hist[hi];ws=words(h)
        p=sum(map(int,h['actual_bits'][:3]));P=sum(map(int,h['actual_bits'][:4]))
        d=[p+ws[e[1]][0]+ws[e[2]][1+e[0]]+1 for e in NODES]
        local=defaultdict(F)
        own=[[F() for _ in range(4)] for e in NODES]
        for atom in ent['atoms']:
            m=F(atom['mass']);ss=atom['states'];rz=[divmod(s,2) for s in ss]
            coef=defaultdict(int)
            for i,s in enumerate(ss):own[i][s]+=m
            for i,j,cl in pairs:
                ri,zi=rz[i];rj,zj=rz[j]
                coef['R-R',cl,d[i]]+=ri-rj
                coef['R-Z',cl,d[i]]+=ri-zj
                coef['Z-R',cl,P+1+ri]+=zi-rj
                coef['Z-Z',cl,P+1+ri]+=zi-zj
            for (kind,cl,den),value in coef.items():local[kind,cl]+=m*F(value,den)
        for i,e in enumerate(NODES):assert tuple(own[i])==marg(hi,groups[hi][ng(e,ws)],masses)
        for kind in KINDS:
            for cl in counts:
                value=local[kind,cl]
                phase_values[phase][kind,cl]+=value;per_hist[phase][kind,cl][hi]=value
    intervals={};records=[]
    for kinds in (('Z-Z',),('Z-R',),KINDS):
        lower=F();upper=F(1);lo=None;up=None;constant_fail=[]
        for kind in kinds:
          for cl in counts:
            a=phase_values['A'][kind,cl];b=phase_values['B'][kind,cl];delta=b-a
            if delta>0 and -a/delta>lower:lower=-a/delta;lo=(kind,cl)
            elif delta<0 and a/(-delta)<upper:upper=a/(-delta);up=(kind,cl)
            elif delta==0 and a<0:constant_fail.append((kind,cl))
        intervals['+'.join(kinds)]={'lower':str(lower),'upper':str(upper),'lower_float':float(lower),'upper_float':float(upper),
            'lower_query':lo,'upper_query':up,'feasible':lower<=upper and not constant_fail,'constant_fail':constant_fail}
    known={}
    ia=args.interface
    if ia.exists():
        interf=json.loads(ia.read_bytes());assert interf['input_sha256']==sha(args.point)
        known={(r['kind'],tuple((r['class'][0],r['class'][1],tuple(r['class'][2])))):F(r['value']) for r in interf['records']}
    for kind in KINDS:
      for cl in sorted(counts):
        a=phase_values['A'][kind,cl];b=phase_values['B'][kind,cl]
        if kind in ('R-R','R-Z'):
            assert a==b
            if known:assert a==known[kind,cl]
        records.append({'kind':kind,'class':cl,'literal_queries':counts[cl],
            'phase_A':str(a),'phase_B':str(b),'half_mixture':str((a+b)/2),
            'phase_A_per_literal':str(a/counts[cl]),'phase_B_per_literal':str(b/counts[cl]),
            'half_per_literal':str((a+b)/(2*counts[cl])),
            'per_hist':[[hi,str(per_hist['A'][kind,cl][hi]),str(per_hist['B'][kind,cl][hi])] for hi in hist]})
    out=meta(args.point)|{'source_sha256':sha(Path(__file__)),'witness_path':str(args.witness),'witness_sha256':sha(args.witness),
        'scope':'Exact evaluation of a specified two-phase completion on the full old R/Z terminal query network; failure does not separate the marginal point',
        'query_types':KINDS,'classes_per_type':len(counts),'literal_queries_per_type':4356,
        'mixing_intervals':intervals,
        'summaries':{kind:{phase:sum(F(r[phase])<0 for r in records if r['kind']==kind)
                           for phase in ('phase_A','phase_B','half_mixture')} for kind in KINDS},
        'records':records}
    dump(args.output,out)
    print(json.dumps({k:v for k,v in out.items() if k!='records'},ensure_ascii=False))
    print('negative_half',[(r['kind'],r['class'],float(F(r['half_per_literal']))) for r in records if F(r['half_mixture'])<0])

if __name__=='__main__':main()
