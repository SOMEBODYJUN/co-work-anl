"""Exact attacks on a layout-selection barrier, not a full-game lower bound."""
from __future__ import annotations
import argparse
import json
import platform
from fractions import Fraction as F
from pathlib import Path
from definition_check import check_ne, from_pure
from run_reverse_audit import all_lexmax


def run():
    cases, deviations, maxima = [], 0, 0
    for k in (2, 3, 4, 7, 12):
        for h in (2, 7, 31, 1024):
            a, M = F(h+1, 2), F(3*(h+1), 4)
            beta = F(2*h, h+1)
            instance = dict(k=k, m=k, clients=[
                dict(weight=str(h), sites=[0,1]), dict(weight='1', sites=[0])
            ]+[dict(weight=str(M), sites=[j]) for j in range(2,k)])
            bad = (0,0)+tuple(range(2,k))
            p = [[F(1,2) if f<2 else F(0) for f in range(k)] for _ in range(2)]
            p += [[F(int(f==j)) for f in range(k)] for j in range(2,k)]
            badL = check_ne(instance, bad, p)
            assert badL == [a,a]+[M]*(k-2)
            if k <= 4 and h in (2,7):
                best, ties = all_lexmax(instance)
                assert best == tuple(sorted(badL))
                for s, _, _ in ties:
                    assert s.count(0)==2 and s.count(1)==0
                    assert all(s.count(j)==1 for j in range(2,k))
                maxima += 1
            good = (1,0)+tuple(range(2,k))
            goodL = check_ne(instance, good, from_pure(list(range(k)), k))
            witnesses = []
            for tag, layout, base, factor in [('lexmax',bad,badL,beta), ('exact',good,goodL,F(1))]:
                for f in range(k):
                    for r in range(k):
                        if r == layout[f]:
                            continue
                        target = list(layout)
                        target[f]=r
                        if tag == 'lexmax':
                            pure=list(range(k))
                            if f<2:
                                if r==1:
                                    pure[0],pure[1]=f,1-f
                                else:
                                    pure[0]=pure[1]=1-f
                            else:
                                pure[f]=-1
                        elif f==0 and r==0:
                            pure=list(range(k))
                            pure[0],pure[1]=1,0
                        else:
                            pure=[next((g for g,s in enumerate(target) if g!=f and s in c['sites']),-1)
                                  for c in instance['clients']]
                        L=check_ne(instance,target,from_pure(pure,k))
                        assert L[f]<=factor*base[f]
                        if tag=='lexmax' and f<2 and r==1:
                            assert L[f]/base[f]==beta
                        elif tag=='exact' and f==0 and r==0:
                            assert L[f]==1
                        else:
                            assert L[f]==0
                        deviations+=1
                        witnesses.append(dict(profile=tag,facility=f,target=r,
                                              pure_assignment=pure,deviator_load=str(L[f])))
            cases.append(dict(instance=instance,k=k,h=h,lexmax_occupancy=list(bad),
                              lexmax_layout_optimum=str(beta),full_instance_optimum='1',
                              exact_SPE_layout=list(good),witnesses=witnesses))
    return dict(claim='SC-K-LEXMAX-BARRIER',evidence_kind='Exact finite attacks, not the all-k/all-h proof',
                python=platform.python_version(),cases=len(cases),actual_deviations=deviations,
                independent_labeled_lexmax_enumerations=maxima,results=cases)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite frozen output')
    result=run()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2))
