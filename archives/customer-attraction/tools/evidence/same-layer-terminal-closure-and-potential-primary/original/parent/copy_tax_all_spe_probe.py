"""Exact finite attack of the new six-provider potential candidate.

E(prefix)[terminal] is minimum remaining copy tax over every SPE path ending
there. The threshold max_a min_{SPE child leaves} u_a allows independent
off-path tie choices. Count caching shares outcome sets, not strategy choices.
All utility/potential/tax arithmetic uses integers scaled by 60.
"""
from pathlib import Path
from functools import lru_cache
import hashlib,json
import numpy as np
import copy_tax_potential_probe as m

HERE=Path(__file__).resolve().parent


def run():
    rng=np.random.default_rng(61247);records=[];inputs=hashlib.sha256()
    for trial in range(300):
        weights=np.zeros(len(m.TYPES),dtype=np.int64)
        for j in range(int(rng.integers(3,14))):
            weights[int(rng.integers(len(weights)))]+=int(rng.integers(1,5))
        inputs.update(weights.astype('<i8').tobytes())
        utilities=m.U@weights;potential=m.POT@weights
        @lru_cache(None)
        def all_spe(prefix):
            if sum(prefix)==m.M:return {m.FI[prefix]:0}
            remaining=m.M-sum(prefix);past=m.TYPES@np.array(prefix)
            children=[]
            for a in range(m.P):
                child=list(prefix);child[a]+=1
                children.append(all_spe(tuple(child)))
            threshold=max(min(int(utilities[leaf,a]) for leaf in outcomes)
                          for a,outcomes in enumerate(children))
            kept={}
            for a,outcomes in enumerate(children):
                tax=int((m.TYPES[:,a]*((60//(past+1))-(60//(past+remaining))))@weights)
                for leaf,tail_tax in outcomes.items():
                    if utilities[leaf,a]>=threshold:
                        kept[leaf]=min(kept.get(leaf,10**30),tail_tax+tax)
            assert kept
            return kept
        roots=all_spe((0,)*m.P);best_potential=int(max(potential))
        gaps={leaf:best_potential-60*int((m.LOAD[leaf]>0).astype(np.int64)@weights)-tax
              for leaf,tax in roots.items()}
        worst=max(gaps,key=gaps.get)
        rec={'trial':trial,'unit_customers':int(weights.sum()),'root_SPE_terminal_counts':len(roots),
             'largest_auxiliary_gap_scaled60':int(gaps[worst]),'prefix_count_states':all_spe.cache_info().currsize}
        records.append(rec)
        if gaps[worst]>0:
            rec['instance']=[{'members':list(map(int,t)),'count':int(w)} for t,w in zip(m.TYPES,weights) if w]
            break
    report={'scope':'complete SPE outcome/tie sets for the listed finite instances, not arbitrary catalogs or a general proof',
            'm':m.M,'catalog_size':m.P,'seed':61247,'requested_trials':300,'numpy_version':np.__version__,
            'input_weights_sha256':inputs.hexdigest(),'refutation_found':any(r['largest_auxiliary_gap_scaled60']>0 for r in records),
            'arithmetic':'integer utility, tax and harmonic potential scale 60','records':records}
    (HERE/'copy_tax_all_spe_probe.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='records'},indent=2))
    print('largest observed gap60',max(r['largest_auxiliary_gap_scaled60'] for r in records))


if __name__=='__main__':run()
