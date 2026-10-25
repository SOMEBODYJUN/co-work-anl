"""Named-instance attack of the general ROW/SUM payment candidates.

Unlike fixed-policy replay this optimizes all complete SPE via QueryEnvelope.
No negative value is an assurance only about these named finite inputs.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
from query_envelope import QueryEnvelope
from customer_attraction import Instance,CustomerType,big_theme_lower_bound,verify_certificate


def instance(p,m,types):
    return Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(a for a in range(p)if mask>>a&1),n)for mask,n in types),m)


def main():
    cases=[('existing-individual-security-34',instance(6,3,[(4,1),(27,4),(29,3),(30,3),(31,2),(32,1),(43,3),(45,3),(46,3),(51,3),(53,3),(54,3),(59,2)])),
           ('existing-actual-prefix-52',instance(6,4,[(1,10),(2,12),(4,5),(8,5),(20,2),(24,2),(36,2),(40,2),(49,6),(50,6)])),
           ('existing-all-big-five',big_theme_lower_bound(5))]
    outputs=[]
    for name,inst in cases:
        p,m=inst.topic_count,inst.players;optimum=inst.optimal_welfare();best_row=best_sum=best_sharp=None;count=0;attainable=None
        for J in combinations(range(p),min(m,p)):
            cover=sum(c.multiplicity for c in inst.customers if c.topics.intersection(J))
            if cover!=optimum:continue
            weights=tuple(int(a in J)for a in range(p));envelope=QueryEnvelope(inst,weights);count+=1
            for terminal,(total,row)in envelope.values().items():
                w=inst.welfare(terminal);r=(row+w-optimum,tuple(J),terminal);s=(total+m*(w-optimum),tuple(J),terminal);sh=(total+(m-1)*w-m*optimum,tuple(J),terminal)
                if best_row is None or r<best_row:best_row=r
                if best_sum is None or s<best_sum:
                    best_sum=s;attainable=(envelope,terminal,total)
                if best_sharp is None or sh<best_sharp:best_sharp=sh
        e,t,target=attainable;cert=e.sum_certificate(t);report=verify_certificate(inst,cert);report.assert_valid()
        root_seed=e.root_repair_bad_gap()
        output={'name':name,'input':inst.to_dict(),'topics':p,'players':m,'customer_count':inst.customer_count,'OPT':optimum,'optimal_distinct_comparison_sets':count,'all_SPE_minimum_ROW_margin':str(best_row[0]),'all_SPE_minimum_SUM_half_margin':str(best_sum[0]),'all_SPE_minimum_SUM_sharp_margin':str(best_sharp[0]),'attaining_SUM_terminal':list(t),'attaining_SUM_query_total':str(target),'credible_child_root_repair_max_bad_gap':str(root_seed[0]),'definition_level_certificate_valid':report.valid}
        outputs.append(output);print(json.dumps(output,ensure_ascii=False),flush=True)
    Path(__file__).with_name('named_instance_results.json').write_text(json.dumps({'status':'finite-only','records':outputs,'limits':'No all-input payment theorem or target counterexample follows from nonnegative named-instance margins. All-big five has five distinct topics, so no padding duplicates are needed.'},ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
