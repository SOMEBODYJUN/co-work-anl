"""Acquire observed vendor series with exact installed AKShare functions; no vintage claim."""
from pathlib import Path
import akshare as ak
import hashlib,json,datetime,inspect
from concurrent.futures import ThreadPoolExecutor,as_completed
ROOT=Path(__file__).resolve().parents[4]
BASE=Path(__file__).resolve().parents[2]/"data"
BASE.mkdir(exist_ok=True)
NAMES=["macro_china_pmi","macro_china_industrial_value_added","macro_china_consumer_goods_retail","macro_china_urban_unemployment"]
def task(name):
 f=getattr(ak,name)
 r={"function":name,"retrieved_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source_code_sha256":hashlib.sha256(inspect.getsource(f).encode()).hexdigest(),"input_kind":"observed_vendor_series","information_mode":"retrospective_revised_latest_vintage","original_publisher":"NBS; retrieved through AKShare/Eastmoney; validate current anchors against original release"}
 try:
  df=f();p=BASE/(name+".csv");df.to_csv(p,index=False);r.update(status="retrieved",rows=len(df),columns=list(df.columns),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),file=p.name,head=json.loads(df.head(2).to_json(orient="records",force_ascii=False,date_format="iso")),tail=json.loads(df.tail(2).to_json(orient="records",force_ascii=False,date_format="iso")))
 except Exception as e:r.update(status="failed",error=type(e).__name__+": "+str(e))
 (BASE/(name+"-receipt.json")).write_text(json.dumps(r,ensure_ascii=False,indent=2)+"\n")
 return r
if __name__=="__main__":
 with ThreadPoolExecutor(max_workers=4) as pool:
  for fut in as_completed([pool.submit(task,n) for n in NAMES]):print(json.dumps(fut.result(),ensure_ascii=False),flush=True)
