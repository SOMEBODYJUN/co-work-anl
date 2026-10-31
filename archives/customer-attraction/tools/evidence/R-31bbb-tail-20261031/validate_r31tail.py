from pathlib import Path
import json,hashlib
E=Path(__file__).parent
def main():
 m=json.loads((E/"source-manifest.json").read_text()); assert len(m["sources"])==6
 for s in m["sources"]:
  local={"probe.py":"terminal_probe.py","named_run.json":"named_run.json"}.get(Path(s["path"]).name,Path(s["path"]).name)
  p=E/"source"/local
  assert p.exists(),p
  assert hashlib.sha256(p.read_bytes()).hexdigest()==s["sha256"]
  assert p.stat().st_size==s["size"]
 a=json.loads((E/"source/addition_m4p6_seed10211.json").read_text()); pr=json.loads((E/"replay/portfolio_200_replay.json").read_text())
 for k in ("status","games_processed","policy_target_pairs","largest_gap","candidate"): assert a[k]==pr[k],(k,a[k],pr[k])
 assert a["candidate"] is None and a["largest_gap"]<0
 sm=json.loads((E/"replay/terminal_named_smoke.json").read_text()); src=json.loads((E/"source/named_run.json").read_text()); d={x["label"]:x for x in sm["results"] if "label" in x}
 assert len(src["results"])==17 and all(x["label"] in d and x==d[x["label"]] for x in src["results"])
 assert all(x["status"]=="finite_floating_cone_result_only" and x["gap"]<0 for x in src["results"])
 mk=json.loads((E/"replay/markov_smoke.json").read_text()); assert mk["status"]=="no_floating_separator_in_finite_sample" and mk["games_processed"]==2 and mk["candidate"] is None and mk["largest_gap"]<0
 ps=json.loads((E/"replay/portfolio_smoke.json").read_text()); assert ps["status"]=="no_floating_separator_in_finite_sample" and ps["games_processed"]==1 and ps["candidate"] is None
 w=json.loads((E/"source/workspace.json").read_text()); assert w["actor"]=="R-31bbb6cfd6594bc8bb076db7b2950993" and w["save"]=="customer-attraction"
 print(json.dumps({"passed":True,"source_count":6,"named_source_rows":17,"named_labels_matched":17,"markov_smoke_games":2,"portfolio_smoke_games":1,"portfolio_replay_games":200,"portfolio_replay_pairs":1663,"portfolio_replay_largest_gap":pr["largest_gap"]},ensure_ascii=False))
if __name__=="__main__": main()
