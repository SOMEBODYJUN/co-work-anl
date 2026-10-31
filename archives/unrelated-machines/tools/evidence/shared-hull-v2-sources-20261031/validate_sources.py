#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
r=Path(__file__).resolve().parent;m=json.loads((r/"manifest.json").read_text());out=[]
for s in m["sources"]:
 p=r/s["evidence_file"];h=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
 out.append({"id":s["id"],"exists":p.exists(),"size":p.stat().st_size if p.exists() else None,"sha256":h,"matches":h==s["source_sha256"]})
ok=all(x["exists"] and x["matches"] for x in out);print(json.dumps({"status":"pass" if ok else "fail","checks":out},ensure_ascii=False,indent=2));raise SystemExit(0 if ok else 1)
