"""One thirteen-term application of the already-audited 448-cell projection.
No table construction, hidden maximization, coefficient audit or graph build.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib,time,sys
E=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);a=p.parse_args();repo=a.repo.resolve();stage=next((q for q in E.parents if q.name=='deliverables'),None) or repo
 t=time.perf_counter();started=time.time();manifest=json.loads((E/'source-manifest.json').read_text());ids={z['id']:z for z in manifest}
 def resolve(id):
  z=ids[id];q=stage/z['preserved_repo_path']
  if not q.exists():q=repo/z['preserved_repo_path']
  assert sha(q)==z['sha256'];return q
 pointfile=resolve('9e170d47648ca7d50779');point=json.loads(pointfile.read_text())['certificate'];assert len(point['support'])==13
 tablepath=repo/'archives/customer-attraction/tools/evidence/tail3-B-projection-program/related/tail3_B_projection_certificate.json';table=json.loads(tablepath.read_text());assert sha(tablepath)=='4d34cd746ce35dd48827c9014a85106c5defac30fc5f1159ae6085d4fd8fa1df'
 lookup={(z['actual_bits'],z['d']):F(z['psi']) for z in table['table']};assert len(lookup)==448
 terms=[]
 for z in point['support']:
  value=lookup[z['actual_bits'],z['d']];mass=F(z['weight']);terms.append({'actual_bits':z['actual_bits'],'d':z['d'],'mass':z['weight'],'psi':str(value),'contribution':str(mass*value)})
 total=sum((F(z['contribution']) for z in terms),F())
 def histread(id):
  return [{k:v for k,v in z.items()} for z in json.loads(resolve(id).read_text())['columns'] if z['kind']=='hist']
 h=histread('9e51f2c756ebb1a91fbf');assert table['old_point_sha256']==ids['9e51f2c756ebb1a91fbf']['sha256']
 assert h==histread('1b97bca5f91f635c1de6')==histread('dfc2594ca7e3f26b6d7f')
 result={'scope':'one exact application of an existing universally valid necessary projection to a different13-support point; no new 448-cell certificate','point_sha256':sha(pointfile),'point_W':point['W'],'projection_table_sha256':sha(tablepath),'projection_source_id':'ef49ddbe23cec45b1352','projection_original_path':'research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/tail3_B_projection_certificate.json','terms':terms,'exact_total':str(total),'total_float':float(total),'negative':total<0,'common_16_hist_identical_across_211_599_1905':True,'old_211_source_SHA_bound_to_projection_certificate':True,'mature_old_211_negative_value':table['old_point_value'],'new_scalar_terms':13,'new_table_rebuilds':0,'new_21504_audits':0,'new_graph_builds':0}
 out=E/'later-projection';out.mkdir(exist_ok=True);(out/'thirteen-term-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 event={'started_unix':started,'elapsed_seconds':time.perf_counter()-t,'python':sys.version,'exit_code':0,'script_sha256':sha(Path(__file__)),'projection_sha256':sha(tablepath),'point_sha256':sha(pointfile),'mathematical_run_attempt':1,'new_dot_products':1,'terms':13,'table_construction':0,'generic_audit':0,'original_CLI':0}
 (out/'execution.json').write_text(json.dumps(event,indent=2)+'\n');print(json.dumps({'exact_total':str(total),'negative':total<0,'common_16_hist_identical':True,'elapsed_seconds':event['elapsed_seconds']},indent=2))
if __name__=='__main__':main()
