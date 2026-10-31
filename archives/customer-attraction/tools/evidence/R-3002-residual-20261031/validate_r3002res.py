from pathlib import Path
import json,hashlib
E=Path(__file__).parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=json.loads((E/"source-manifest.json").read_text()); assert len(m["sources"])==16
 for s in m["sources"]:
  p=E/"source"/Path(s["path"]).name; assert p.exists(),p; assert sha(p)==s["sha256"],(p,sha(p),s["sha256"])
 names=["root_requery_baseline_o4.2_exact.json","root_requery_o4.2_exact.json","root_requery_third_L_o4.2_exact.json","root_requery_branch_D_o4.2_exact.json","root_requery_L_D_o4.34514_exact.json"]
 for n in names:
  d=json.loads((E/"source"/n).read_text()); assert d["verification"]["min_residual_numerator"]>=0 and d["verification"]["zero_types"]==1
  out=(E/"replay/verify"/(n+".stdout")).read_text(); assert '"min_residual_numerator": 0' in out
 rp=json.loads((E/"source/root_rows_joint_point.json").read_text()); assert rp["lp_success"] and rp["rows"]==3894 and rp["columns"]==1905 and rp["exact_verification"]["minimum_slack"]=="0"
 tau=json.loads((E/"source/tau6_endpoint_farkas.json").read_text()); assert tau["verification"]["status"].startswith("exact Farkas") and tau["verification"]["target_average"]=="-1051597/12277962"
 assert json.loads((E/"source/root_joint_audit.json").read_text())[0]["min_residual"]==0
 print(json.dumps({"passed":True,"source_count":16,"exact_requeries":5,"joint_rows":3894,"joint_columns":1905,"joint_min_slack":"0","tau6_target_average":"-1051597/12277962"},ensure_ascii=False))
if __name__=="__main__": main()
