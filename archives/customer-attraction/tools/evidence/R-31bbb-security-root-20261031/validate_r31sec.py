from pathlib import Path
import json,hashlib
E=Path(__file__).parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=json.loads((E/"source-manifest.json").read_text()); assert len(m["sources"])==7
 for s in m["sources"]:
  p=E/("dependencies/ssr/research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/security_aggregate/pair_theory/all_optimal_query_failure_41.json" if s["id"]=="e83dd064c0f6a8588794" else "source/"+Path(s["path"]).name)
  assert p.exists(),p
  assert sha(p)==s["sha256"],(p,sha(p),s["sha256"])
 c=json.loads((E/"source/common_policy_Q_numerical.json").read_text())["cases"]
 assert len(c)==85 and all(x["status"]==0 for x in c)
 assert all(abs(sum(x["Q"])-1)<3e-12 for x in c)
 assert all(min(x["Q"])>=-1e-10 for x in c)
 assert json.loads((E/"common_smoke.json").read_text())["cases"]==c[:7]
 n=json.loads((E/"source/background_pair_numerical.json").read_text()); l=json.loads((E/"source/background_pair_large_numerical.json").read_text())
 assert n["status"]==l["status"]=="numerical_only" and n["candidate"] is None and l["candidate"] is None and n["max_ratio"]==l["max_ratio"]==1.0
 s=json.loads((E/"source/ssr_41_isolation_numerical.json").read_text()); assert s["status"]=="numerical_only" and s["completed"]==1500 and s["max_min_optimal_regret"]==0.0 and s["counterexample_candidate"] is None
 sm=json.loads((E/"ssr_smoke.json").read_text()); assert sm["status"]=="numerical_only" and sm["completed"]==2 and sm["counterexample_candidate"] is None
 print(json.dumps({"passed":True,"source_count":7,"common_cases":85,"common_smoke_prefix":True,"normal_trials":260,"large_trials":120,"ssr_trials":1500,"ssr_smoke_trials":2},ensure_ascii=False))
if __name__=="__main__": main()
