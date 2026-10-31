from pathlib import Path
import json,hashlib,subprocess,sys
E=Path(__file__).parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=json.loads((E/"source-manifest.json").read_text()); assert len(m["sources"])==6 and len(m["related_dependencies"])==1
 for s in m["sources"]:
  p=E/"source"/Path(s["path"]).name; assert p.exists() and sha(p)==s["sha256"]
 for s in m["related_dependencies"]:
  p=E/"dependencies/cone_security_search.py"; assert sha(p)==s["sha256"]
 def check(name,n):
  d=json.loads((E/"source"/name).read_text()); assert len(d["cases"])==n and all(c["best_CCE_ratio"]<=1+1e-8 for c in d["cases"]); return d
 a=check("cone_cce_n3k4.json",10); b=check("cone_cce_n4k5.json",10); c=check("cone_cce_n5k7.json",8); d=json.loads((E/"source/cone_cce_named.json").read_text()); assert len(d["cases"])==4 and all(x["best_CCE_ratio"]<=1+1e-8 for x in d["cases"])
 sm=json.loads((E/"replay/cce_smoke.json").read_text()); assert len(sm["cases"])==1 and sm["cases"][0]["best_CCE_ratio"]<=1+1e-8 and not sm["cases"][0].get("witness")
 for p in [E/"source/cone_cce_named.py",E/"source/cone_cce_search.py",E/"dependencies/cone_security_search.py"]: subprocess.run([sys.executable,'-m','py_compile',str(p)],check=True)
 print(json.dumps({"passed":True,"source_count":6,"n3k4_cases":10,"n4k5_cases":10,"n5k7_cases":8,"named_cases":4,"smoke_cases":1,"max_ratio_overall":max([x["best_CCE_ratio"] for z in [a,b,c,d] for x in z["cases"]])},ensure_ascii=False))
if __name__=="__main__": main()
