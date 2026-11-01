from pathlib import Path
import runpy,json
from fractions import Fraction
g=runpy.run_path(str(Path(__file__).with_name('original-point-snippet.py')))
a,h,mass=g['a'],g['h'],g['mass']
out=dict(original_assertions_passed=True,histograms=len(h),d_values=sorted({v['d']for v in h}),RZ_atoms=len(a['RZ_atoms']),mass=str(sum(mass.values())),positive_hist_indices=[i for i in range(len(h))if mass[i]>0],d0_mass=str(sum(w for i,w in mass.items()if h[i]['d']==0)),promotion_states=len(a['promotion_states']),promotion_referenced_d_values=sorted({h[v['hist_index']]['d']for v in a['promotion_states']}),RZ_all_weights_nonnegative=all(Fraction(v['weight'])>=0 for v in a['RZ_atoms']),promotion_all_weights_nonnegative=all(Fraction(v['weight'])>=0 for v in a['promotion_states']),source_declared_rows=a['rows'],source_declared_O=a['O'],source_declared_W=a['W'],source_declared_K=a['K'],source_declared_minimum_slack=a['minimum_slack'],all_1269_rows_recomputed=False,full_SPE_strategy_checked=False)
print(json.dumps(out,ensure_ascii=False,indent=2))
