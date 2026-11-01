from pathlib import Path
import sys,json,random,subprocess
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance,CustomerType,ExactSPESolver,verify_certificate
ROOT=Path(__file__).parent
rng=random.Random(7102026);results=[]
for case in range(22):
 if case<2:ins=Instance.from_dict(json.loads((ROOT/['search_best.json','restart_best.json'][case]).read_text()))
 else:
  w={}
  for j in range(rng.randrange(3,25)):
   mask=rng.randrange(1,128);w[mask]=w.get(mask,0)+rng.randrange(1,12)
  ins=Instance(tuple('ABCDEFG'),tuple(CustomerType(frozenset(a for a in range(7) if mask>>a&1),n) for mask,n in w.items()),5)
 weights=[0]*128
 for c in ins.customers:weights[sum(1<<a for a in c.topics)]+=c.multiplicity
 output=subprocess.check_output([str(ROOT/'exact_integer_search'),'--evaluate'],input=' '.join(map(str,weights[1:])).encode()).decode().splitlines()
 opt,mn,num=map(int,output[0].split());cpp={tuple(map(int,row.split())) for row in output[1:]}
 s=ExactSPESolver(ins);canonical=s.outcomes()
 assert cpp==canonical,(case,cpp^canonical)
 assert opt==ins.optimal_welfare() and mn==s.minimum_welfare()
 result={'case':case,'types':len(ins.customers),'customers':ins.customer_count,'outcomes':num,'opt':opt,'minimum':mn,'full_outcome_identity':True}
 if case<2:
  cert=s.worst_certificate();report=verify_certificate(ins,cert);report.assert_valid()
  result['all_history_certificate_valid']=True;result['histories']=len(cert.actions)
  (ROOT/f'search_certificate_{case}.json').write_text(json.dumps({'instance':ins.to_dict(),'certificate':cert.to_dict()},indent=2))
 results.append(result)
(ROOT/'search_audit.json').write_text(json.dumps({'integer_scale':60,'cases':results},indent=2));print(json.dumps(results,indent=2))
