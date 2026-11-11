"""Exact finite-domain dual for hist-specific four-threshold-phase failure."""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
from pathlib import Path
import json
from build_common import Data,HERE,POINT,LATENT,digest,save
from phase_mix import metrics,old_queries


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--point',type=Path,default=POINT)
    ap.add_argument('--witness',type=Path,default=LATENT)
    ap.add_argument('--attempt',type=Path,default=HERE/'hist_four_phase_attempt.json')
    ap.add_argument('--out-dir',type=Path,default=HERE)
    args=ap.parse_args();args.out_dir.mkdir(parents=True,exist_ok=True)
    data=Data(args.point,args.witness)
    saved=json.loads(args.attempt.read_bytes())
    assert saved['input_sha256']==digest(args.point)
    phases={ph:{b['hist_column']:[{**a,'mass':Q(a['mass']),
                                 'metrics':metrics(a['states'],sum(map(int,data.hist[b['hist_column']]['actual_bits'][:4])))}
                                for a in b['atoms']]for b in blocks}for ph,blocks in saved['phases'].items()}
    discover=saved['discovery']; specs=data.specs('B4')
    weights=[Q(str(max(0.,v))).limit_denominator(10**9)for v in discover['floating_IC_weights']]
    new_weights=weights[:len(specs)]
    old_weights={ (raw[0],(raw[1][0],raw[1][1],tuple(raw[1][2]))):w
                  for raw,w in zip(discover['old_queries_in_order'],weights[len(specs):])if w}
    positive_potentials={}
    for label,value in zip(discover['equality_rows_in_order'],discover['floating_equality_potentials']):
        if label[0]=='family-state':
            positive_potentials[label[1],label[2]]=Q(str(value)).limit_denominator(10**9)
    budget=sum((w*b for w,b in zip(new_weights,data.budgets('B4'))),Q())
    total_lower=Q(); blocks=[];cell_count=0;phase_count=0
    for h in data.hist:
        ss=data.family['B4'][h]
        # The last positive-state equality was omitted; its dual gauge is 0.
        # All zero-mass states are restored with a harmless low potential.
        beta={s['column']:positive_potentials.get((h,s['column']),Q())if s['mass']else Q(-100)for s in ss}
        old_by_phase={ph:old_queries(data,aa,[h])for ph,aa in phases.items()}
        alpha={}; minima={};phase_rhs={}
        for ph in phases:
            alpha[ph]={}
            for atom in phases[ph][h]:
                costs={s['column']:sum((w*data.cost(atom,s,sp)for w,sp in zip(new_weights,specs)if w),Q())for s in ss}
                value=min(costs[s['column']]-beta[s['column']]for s in ss)
                alpha[ph][atom['index']]=value
                for s in ss:
                    assert value+beta[s['column']]<=costs[s['column']]
                    cell_count+=1
            old_credit=sum((w*old_by_phase[ph][key]for key,w in old_weights.items()),Q())
            phase_rhs[ph]=sum((atom['mass']*alpha[ph][atom['index']]for atom in phases[ph][h]),Q())-old_credit
        gamma=min(phase_rhs.values())
        for ph,v in phase_rhs.items():
            assert gamma<=v
            phase_count+=1
        lower=gamma+sum((s['mass']*beta[s['column']]for s in ss),Q())
        total_lower+=lower
        blocks.append({'hist_column':h,'family_potentials':[{'column':j,'value':v}for j,v in beta.items()],
                       'atom_potentials':{ph:[{'atom':ai,'value':v}for ai,v in aa.items()]for ph,aa in alpha.items()},
                       'phase_potential':gamma,'phase_potential_upper_bounds':phase_rhs,'lower_cost':lower})
    slack=budget-total_lower
    assert slack<0
    report={'scope':'exact infeasibility of four threshold orientations with independent hist phase weights; not an original marginal-domain cut',
            'input_sha256':digest(args.point),'input_A_sha256':digest(args.witness),'attempt_sha256':digest(args.attempt),
            'source_sha256':digest(Path(__file__)),'family':'B4',
            'new_IC_weights':[{'query':sp,'weight':w}for sp,w in zip(specs,new_weights)if w],
            'old_IC_weights':[{'kind':key[0],'class':key[1],'weight':w}for key,w in old_weights.items()],
            'budget':budget,'exact_dual_lower_cost':total_lower,'exact_IC_combination_upper_bound':slack,
            'all_atom_state_dual_cells':cell_count,'all_phase_dual_inequalities':phase_count,'blocks':blocks,
            'hist_four_phase_impossible':True}
    save(args.out_dir/'hist_four_phase_obstruction.json',report)
    print({'hist_four_phase_impossible':True,'exact_negative_gap':float(slack),
           'all_atom_state_dual_cells':cell_count,'phase_inequalities':phase_count})


if __name__=='__main__':main()
