from pathlib import Path
import json,hashlib
E=Path(__file__).parent
def main():
 s=json.loads((E/"source/three_price_template_report.json").read_text()); r=json.loads((E/"replay/three_price_template_replay.json").read_text())
 assert len(s)==len(r)==8
 assert s==[{k:v for k,v in x.items() if k!="enriched"} for x in r]
 assert [x["n"] for x in s]==[1,2,3,4,5,10,20,100]
 assert [x["status"] for x in s]==[0,0,2,2,2,2,2,2]
 assert s[0]["minimum_slack"]==0.0 and abs(s[1]["minimum_slack"])<2e-15
 print(json.dumps({"passed":True,"source_id":"6dbdbebce8e0f3aa71ee","rows":8,"feasible_n":[1,2],"infeasible_n":[3,4,5,10,20,100],"replay_shared_fields_equal":True},ensure_ascii=False))
if __name__=="__main__": main()
