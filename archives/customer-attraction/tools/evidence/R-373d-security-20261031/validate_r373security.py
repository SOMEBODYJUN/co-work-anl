from pathlib import Path
import json,hashlib,subprocess,sys,math
E=Path(__file__).parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 m=json.loads((E/"source-manifest.json").read_text()); assert len(m["sources"])==4
 for s in m["sources"]:
  p=E/"source"/(Path(s["path"]).name); assert p.exists(),p; assert sha(p)==s["sha256"],(p,sha(p),s["sha256"])
 b=json.load(open(E/"source/background_security_probe.json")); br=json.load(open(E/"replay/background_security_probe.json")); assert b==br
 assert len(b["trace"])==460 and b["best"]["gap"]<0 and max(x["gap"] for x in b["trace"])<0
 f=json.load(open(E/"source/fractional_background_probe.json")); fr=json.load(open(E/"replay/fractional_background_probe.json")); assert len(f["trace"])==len(fr["trace"])==105
 assert f["best"]["prefix"]==fr["best"]["prefix"] and abs(f["best"]["gap"]-fr["best"]["gap"])<1e-12
 assert max(x["gap"] for x in f["trace"])<0 and max(x["gap"] for x in fr["trace"])<0
 assert "no proof" in f["scope"] and "counterexample certificate" in f["scope"]
 for p in [E/"source/background_security_probe.py",E/"source/fractional_background_probe.py",E/"validate_r373security.py"]: subprocess.run([sys.executable,'-m','py_compile',str(p)],check=True)
 print(json.dumps({"passed":True,"source_count":4,"background_starts":460,"background_best_gap":b["best"]["gap"],"fractional_starts":105,"fractional_best_gap":f["best"]["gap"],"fractional_replay_best_gap":fr["best"]["gap"],"no_positive_gap":True},ensure_ascii=False))
if __name__=="__main__": main()
