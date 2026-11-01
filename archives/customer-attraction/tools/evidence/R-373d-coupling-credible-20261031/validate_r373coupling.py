from pathlib import Path
import json,hashlib,subprocess,sys
E=Path(__file__).parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=json.loads((E/"source-manifest.json").read_text()); assert len(m["sources"])==8
 for s in m["sources"]:
  p=E/"source"/(Path(s["path"]).name)
  assert p.exists(),p
  assert sha(p)==s["sha256"],(p,sha(p),s["sha256"])
 a=json.loads((E/"source/signed_graph_menu_audit.json").read_text()); b=json.loads((E/"replay/signed_graph_menu_audit.json").read_text()); assert a==b and a["status"]=="passed" and a["random_definition_cases"]==1200 and a["half_density_sharp_cases"]==150 and a["clique_sharp_cases"]==135 and a["K5"]=={"joint_deficit":"2","best_scalar_odd_cycle_packing":"5/3"}
 bridge=json.loads((E/"source/pair_interest_static_bridge_failure.json").read_text()); assert bridge["status"].startswith("exact finite bridge") and bridge["full_history_checks"]==780 and bridge["static_move"]=={"from":0,"to":1,"before":"10","after":"21/2"}
 cand=json.loads((E/"replay/candidates_verify.stdout").read_text()); assert cand["passed"] and len(cand["candidates"])==3
 expected={"7b8aa422a024fb55c995.out":("4","6",156),"996cdb7259e85f9c6208.out":("1","1",341),"c5a462aba83d26ea38af.out":("5","6",341)}
 for x in cand["candidates"]: assert (x["welfare"],x["optimum"],x["verified_histories"])==expected[x["file"]]
 f2=json.load(open(E/"replay/fixed_bridge/research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/credible/fixed_bridge_mult2.json")); f3=json.load(open(E/"replay/fixed_bridge/research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/credible/fixed_bridge_mult3.json")); assert f2["objective"]=="-6/23" and f2["welfare"]==138 and f2["optimum"]==198 and f3["objective"]=="-123/206" and f3["welfare"]==103 and f3["optimum"]==145
 for p in [E/"source/audit_signed_graph_menus.py",E/"source/count_milp.py",E/"source/fixed_bridge_attack.py",E/"replay/verify_candidates.py"]: subprocess.run([sys.executable,'-m','py_compile',str(p)],check=True)
 print(json.dumps({"passed":True,"source_count":8,"formula_random_cases":1200,"half_sharp_cases":150,"clique_cases":135,"bridge_history_checks":780,"candidate_certificates":3,"fixed_bridge_runs":2},ensure_ascii=False))
if __name__=="__main__": main()
