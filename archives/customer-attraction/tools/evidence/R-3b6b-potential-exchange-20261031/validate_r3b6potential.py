from pathlib import Path
import json,hashlib,subprocess,sys
E=Path(__file__).parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=json.loads((E/"source-manifest.json").read_text()); assert len(m["sources"])==7
 names={"429ed2e586e03d6f3349":"audit_last_average_selection.py","3ca2d866816d6f114ec4":"last_average_selection_certificate.json","cacc185d00575ac093c4":"last_average_selection_independent_audit.json","3d30826d714909e683cc":"last_average_selection_small_certificate.json","ec4335c6f2c374154ab1":"min_payoff_k5_m3_discovery.json","6ab3c753a22bf3a21193":"min_payoff_lp_discovery.json","d2155e7c5d622d1b17e2":"min_payoff_lp_search.py"}
 for s in m["sources"]:
  p=E/"source"/names[s["id"]]; assert p.exists(),p; assert sha(p)==s["sha256"],(p,sha(p),s["sha256"])
 small=json.loads((E/"source/last_average_selection_small_certificate.json").read_text()); large=json.loads((E/"source/last_average_selection_certificate.json").read_text()); audit=json.loads((E/"source/last_average_selection_independent_audit.json").read_text()); replay=json.loads((E/"replay/audit_last_average_selection.json").read_text()); vp=json.loads((E/"replay/verify_potential.stdout").read_text())
 assert audit==replay and audit["status"]=="passed" and audit["all_ordered_histories"]==21 and audit["strict_nonself_comparisons"]==63 and audit["minimum_strict_margin"]=="1/6" and audit["unique_spe_path"]==[1,2,1] and audit["welfare"]==16 and audit["opt"]==16 and audit["last_minus_mean"]=="1/6"
 assert vp["passed"] and len(vp["certificates"])==2
 assert vp["certificates"][0]["welfare"]==45 and vp["certificates"][0]["optimum"]==49 and vp["certificates"][0]["checked_histories"]==21 and vp["certificates"][0]["checked_deviations"]==63
 assert vp["certificates"][1]["welfare"]==16 and vp["certificates"][1]["optimum"]==16
 assert large["min_welfare"]==45 and large["opt"]==49 and large["all_spe_terminal_counts"]==[[0,2,1,0]] and small["min_welfare"]==16 and small["opt"]==16
 for p in [E/"source/audit_last_average_selection.py",E/"source/min_payoff_lp_search.py",E/"replay/verify_potential.py"]: subprocess.run([sys.executable,'-m','py_compile',str(p)],check=True)
 for fn,pol,gap in [("min_payoff_lp_discovery.json",425,8.326672684688674e-17),("min_payoff_k5_m3_discovery.json",813,1.3322676295501878e-15)]:
  d=json.loads((E/"source"/fn).read_text()); assert d["result"]=="no counterexample found" and d["policies"]==pol and abs(d["best_gap_normalized"]-gap)<1e-20
 sm=json.loads((E/"replay/min_payoff_smoke.json").read_text()); assert sm["result"]=="no counterexample found" and sm["trials"]==20 and sm["policies"]==19
 print(json.dumps({"passed":True,"source_count":7,"average_selection_histories":21,"average_selection_deviations":63,"strict_margin":"1/6","certificates_verified":2,"min_payoff_source_searches":2,"min_payoff_smoke_trials":20},ensure_ascii=False))
if __name__=="__main__": main()
