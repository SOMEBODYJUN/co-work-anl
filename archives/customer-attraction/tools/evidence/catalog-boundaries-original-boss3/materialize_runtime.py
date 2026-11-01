"""Copy SHA-checked frozen originals and four dependencies; run no audit."""
from pathlib import Path
import argparse,hashlib,json,shutil

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runtime",type=Path)
    target=parser.parse_args().runtime.resolve()
    evidence=Path(__file__).resolve().parent
    repository=evidence.parents[4]
    if target.is_relative_to(repository):
        raise ValueError("Choose a runtime outside this repository")
    if target.exists() and any(target.iterdir()):
        raise ValueError("Use a new empty runtime")
    target.mkdir(parents=True,exist_ok=True)
    rows=json.loads((evidence/"source-manifest.json").read_text())+json.loads((evidence/"dependency-manifest.json").read_text())
    for item in rows:
        source=evidence/item["preserved_as"]
        raw=source.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=item["sha256"]:
            raise ValueError("Frozen source SHA mismatch: "+item["path"])
        out=target/item["path"];out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
    print(json.dumps({"files":len(rows),"runtime":str(target),"mathematical_entries_run":0}))

if __name__=="__main__":main()
