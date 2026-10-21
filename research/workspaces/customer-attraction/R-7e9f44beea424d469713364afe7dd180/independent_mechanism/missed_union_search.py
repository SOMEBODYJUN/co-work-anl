"""Attack direct no-boycott candidate: max_m |union(T_j) minus actual union| <= W."""
from individual_gap_search import *
if __name__=='__main__':
 results=[];seen=set();paths=list((ROOT/'evidence/certificates/customer_attraction').glob('*.json'))+[ROOT/'evidence/runs/2026-10-09/cone_attack_credible_selected.json']
 for path in sorted(paths):
  try:obj=json.loads(path.read_text())
  except Exception:continue
  for aa in strategies(obj):
   if len(aa)>4000:continue
   acts={tuple(x['history']):x['action'] for x in aa};key=tuple(sorted(acts.items()))
   if key in seen:continue
   seen.add(key);p=1+max(max(h+(a,)) for h,a in acts.items());m=1+max(map(len,acts))
   if p>7:continue
   try:cone=StrategyCone(p,m,acts)
   except ValueError:continue
   for support in combinations(range(p),min(m,p)):
    objective=tuple(x*(1-y) for x,y in zip(coverage_row(p,support),cone.welfare));r=optimize(cone,objective)
    if r is None:continue
    vals,value=r;record={'source':str(path.relative_to(ROOT)),'m':m,'p':p,'root_counts':cone.root,'missed_over_W':value,'threshold':1,'portfolio':support}
    results.append(record);print(json.dumps(serializable(record)),flush=True)
    if value>1:
     clones=integer_clones(vals);assert independently_verify(cone,clones)
     inst=instance_from_clones(p,m,clones);record.update({'clones':clones,'actions':aa,'actual_optimum':inst.optimal_welfare(),'actual_welfare':inst.welfare(cone.root)})
     dest=Path(__file__).with_name('missed_union_counterexample.json');dest.write_text(json.dumps(serializable(record),indent=2)+'\n');print('VIOLATION_SAVED',dest,flush=True);sys.exit()
 Path(__file__).with_name('missed_union_scan.json').write_text(json.dumps(serializable(results),indent=2)+'\n')
