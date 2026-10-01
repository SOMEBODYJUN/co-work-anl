"""Exact incidence audit for SPARSE-BAD-LONG; finite checks are not the proof.

Usage:
  python3 tests/audits/sparse_bad_long_cycles.py > evidence/runs/2026-10-01/sparse_bad_long_cycles.json
  python3 tests/audits/sparse_bad_long_cycles.py --instance 3
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
SIZES = [1, 2, 3, 10, 30, 100]
FACTOR = F(7, 4)


def serial(value):
    if isinstance(value, F):return str(value)
    if isinstance(value, list):return [serial(v) for v in value]
    if isinstance(value, dict):return {k:serial(v) for k,v in value.items()}
    return value


def instance(n):
    assert n >= 1
    h=F(1,100*(2*n+1));L=F(36,25)
    reaches=[L+(2*i-1)*h for i in range(1,n+1)]+[F(79,100)]
    reaches += [L+2*j*h for j in range(n)]+[F(9,5)]
    weights=[F(1),F(43,100)];sites=[set() for _ in range(2*(n+1))]
    for s in list(range(n))+list(range(n+1,2*n+2)):sites[s].add(0)
    for s in [n]+list(range(n+1,2*n+1)):sites[s].add(1)
    for s,reach in enumerate(reaches):
        private=reach-sum((weights[i] for i in sites[s]),F(0))
        assert private>0
        sites[s].add(len(weights));weights.append(private)
    return dict(weights=weights,locations=[sorted(s) for s in sites],
                U1=list(range(n+1)),U2=list(range(n+1,2*n+2)))


def audit(inst,n):
    w=list(map(F,inst['weights']));sets=list(map(set,inst['locations']))
    rows=inst['U1'];cols=inst['U2']
    assert len(rows)==len(cols)==n+1 and all(x>0 for x in w)
    reach=[sum((w[k] for k in c),F(0)) for c in sets]
    tab={}
    for s in rows:
        for t in cols:
            cc=sets[s]&sets[t];assert len(cc)<=1
            common=w[next(iter(cc))] if cc else F(0)
            assert not cc or reach[s]!=reach[t]
            tab[s,t]=(reach[s]-common,reach[t]) if reach[s]>reach[t] else (reach[s],reach[t]-common)
    D1={t:max(tab[s,t][0] for s in rows) for t in cols}
    D2={s:max(tab[s,t][1] for t in cols) for s in rows}
    br1={t:[s for s in rows if tab[s,t][0]==D1[t]] for t in cols}
    br2={s:[t for t in cols if tab[s,t][1]==D2[s]] for s in rows}
    c0=n+1;d=2*n+1;b=n
    assert br1[d]==[n-1] and br1[c0]==[b]
    for j in range(1,n):assert br1[c0+j]==[j-1]
    for i in range(n):assert br2[i]==[c0+i]
    assert br2[b]==[d]
    factors={f'{s},{t}':max(F(1),D1[t]/tab[s,t][0],D2[s]/tab[s,t][1])
             for s in rows for t in cols}
    best=min(factors.values());assert best>FACTOR
    # Follow actual full-catalog successors; every labeled action occurs once.
    path=[];v=d
    while v not in path:
        path.append(v)
        v=br1[v][0] if v in cols else br2[v][0]
    assert v==d and len(path)==2*(n+1)
    return dict(n=n,clients=len(w),layouts=len(tab),best_factor=str(best),
                cycle_length=len(path),cycle=path if n<=3 else None,
                minimum_reach=str(min(reach)),maximum_reach=str(max(reach)))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--instance',type=int)
    args=parser.parse_args()
    if args.instance:
        print(json.dumps(serial(instance(args.instance)),indent=2));return
    sample_path=ROOT/'examples/heterogeneous/sparse/bad_long_n3.json'
    stored=json.loads(sample_path.read_text())
    assert stored==serial(instance(3))
    results=[audit(instance(n),n) for n in SIZES]
    output={'schema_version':1,'recorded_on':'2026-10-01','name':'sparse_bad_long_cycles',
            'python_version':sys.version.split()[0],
            'base_commit':'b08c9e16e7c3214af6525e718cf56c024e34319d',
            'source_sha256':{'tests/audits/sparse_bad_long_cycles.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
            'input':'examples/heterogeneous/sparse/bad_long_n3.json',
            'input_sha256':hashlib.sha256(sample_path.read_bytes()).hexdigest(),
            'replay_commands':['python3 tests/audits/sparse_bad_long_cycles.py > evidence/runs/2026-10-01/sparse_bad_long_cycles.json',
                               'python3 tests/audits/sparse_bad_long_cycles.py --instance 3'],
            'observed':{'seed':'none, closed-form rational weights','r':'7/4','sizes':SIZES,'results':results},
            'limitations':'Finite exact checks support arithmetic only; the universal n and all-r<rho statements depend on the symbolic inequalities and rational-density proof.'}
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
