#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
base=Path(__file__).resolve().parent
m=json.loads((base/"source-manifest.json").read_text())
for s in m["sources"]:
    name={"1adf040842bbb51868e1":"independent_row_v3.md","1c5ff76cfa939112e428":"read_after_pcsp_v3.md","3b1b06c474aefb6a2360":"read_after_row_v3.md"}[s["id"]]
    p=base/name; b=p.read_bytes(); assert len(b)==s["size"]; assert hashlib.sha256(b).hexdigest()==s["sha256"]
print("PASS",len(m["sources"]))
