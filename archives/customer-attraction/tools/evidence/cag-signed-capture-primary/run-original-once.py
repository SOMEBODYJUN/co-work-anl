"""One exact original top-level run; passive trace records original joint guards/read_case returns."""
from pathlib import Path
import ast,contextlib,hashlib,json,os,platform,runpy,shutil,sys,time,traceback
E=Path(__file__).resolve().parent;rows=json.loads((E/'source-manifest.json').read_text());src=rows[0];deps=json.loads((E/'dependency-manifest.json').read_text());replay=E/'replay';replay.mkdir(exist_ok=False);root=replay/'source-root';root.mkdir();program=root/src['path'];program.parent.mkdir(parents=True);shutil.copyfile(E/'original'/src['path'],program)
for x in deps:
 p=root/x['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(E/x['copied_path'].split('/cag-signed-capture-primary/',1)[1],p)
# Dependency copied_path is stage-relative; confirm actual mirrors against recorded original SHA.
for x in deps:assert hashlib.sha256((root/x['path']).read_bytes()).hexdigest()==x['sha256']
expected_root=program.parent.parents[5];assert expected_root==root
text=program.read_text();tree=ast.parse(text);pay_line=next(n.lineno for n in ast.walk(tree)if isinstance(n,ast.Assert)and ast.unparse(n.test)=='Vnew >= lam * n * t + gamma');joint_line=next(n.lineno for n in ast.walk(tree)if isinstance(n,ast.AugAssign)and isinstance(n.target,ast.Name)and n.target.id=='joint_checks');cases=[];joint=[];pay_hits=[]
def tracer(frame,event,arg):
 if frame.f_code.co_filename!=str(program):return None
 if frame.f_code.co_name=='read_case':
  if event=='return':
   v=frame.f_locals;inst,customers,policy,_,_,checks=arg;cases.append({'name':v['name'],'m':inst['players'],'q':len(inst['topics']),'expanded_units':len(customers),'customer_likes':[sorted(c)for c in customers],'policy':[{'history':list(h),'action':a}for h,a in sorted(policy.items(),key=lambda x:(len(x[0]),x[0]))],'actual_original_IC_checks':checks})
  return tracer
 if frame.f_code.co_name=='<module>'and event=='line':
  v=frame.f_locals
  if frame.f_lineno==pay_line:pay_hits.append({'lambda':str(v['lam']),'history':list(v['h']),'action':v['a'],'n':v['n'],'d':str(v['rootold']),'V':str(v['V']),'t':str(v['t'])})
  if frame.f_lineno==joint_line:joint.append({'lambda':str(v['lam']),'depth':v['depth'],'history':list(v['h']),'action':v['a'],'n':v['n'],'root_old':str(v['rootold']),'root_new':str(v['rootnew']),'gamma':str(v['gamma']),'old_B':str(v['oldB']),'delta_B':str(v['dB']),'V':str(v['V']),'V_new':str(v['Vnew']),'eta':str(v['eta']),'factor':str(v['factor'])})
 return tracer if frame.f_code.co_name=='<module>'else None
prev=Path.cwd();oldargv=sys.argv[:];oldtrace=sys.gettrace();start=time.time();exit_code=0;namespace={};outputname='current-signed-capture-output.json';output=program.parent/outputname;assert not output.exists()
try:
 os.chdir(root);sys.argv=[str(program),'--output',outputname]
 with (replay/'original.stdout.txt').open('w')as out,(replay/'original.stderr.txt').open('w')as err:
  with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
   try:sys.settrace(tracer);namespace=runpy.run_path(str(program),run_name='__main__')
   except BaseException:exit_code=1;traceback.print_exc()
   finally:sys.settrace(oldtrace)
finally:os.chdir(prev);sys.argv=oldargv
snapshot={'scope':'passive trace of originally executed read_case returns and joint/PAY lines, plus returned original namespace; zero extra finish/pay/read_case/arrays/formal_phi calls','cases':cases,'joint_cases':joint,'conditional_PAY_assertion_hits':pay_hits,'conditional_PAY_assertion_hits_count':len(pay_hits)}
if namespace:snapshot.update({'threshold_t':str(namespace['t']),'source_checks':namespace['source_checks'],'matching_checks':namespace['matching_checks'],'joint_checks':namespace['joint_checks'],'edge_checks':namespace['edge_checks'],'path_checks':namespace['path_checks'],'actual':list(namespace['actual']),'optimal':list(namespace['optimal']),'incoming_positive':[{'position0':i,'action':a,'customer':x,'amount':str(v)}for(i,a,x),v in sorted(namespace['incoming'].items())if v],'absorption_by_customer':[{'customer':x,'amount':str(v)}for x,v in sorted(namespace['absorbed'].items())],'node_absorptions':[{'position0':i,'action':a,'amount':str(v)}for(i,a),v in sorted(namespace['A'].items())],'rows':list(map(str,namespace['rows'])),'paid_cost':str(namespace['cost']),'weighted_slack':str(namespace['weightedslack']),'original_output_object':namespace['out']})
(replay/'original-input-guards-and-flow.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
stdout=(replay/'original.stdout.txt').read_text();docs=[];pos=0;decoder=json.JSONDecoder()
try:
 while pos<len(stdout):
  while pos<len(stdout)and stdout[pos].isspace():pos+=1
  if pos==len(stdout):break
  obj,pos=decoder.raw_decode(stdout,pos);docs.append(obj)
except ValueError:pass
(replay/'stdout-documents.json').write_text(json.dumps(docs,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
state={'original_program_calls':1,'execution_count':1,'method':'runpy.run_path exact original top-level; passive source line/return tracing only, no extra source calls','argv':[str(program),'--output',outputname],'cwd':str(root),'program':src['path'],'program_bytes':program.stat().st_size,'program_sha256':sha(program),'resolved_original_ROOT':str(expected_root),'python':sys.version,'executable':sys.executable,'optimize':sys.flags.optimize,'platform':platform.platform(),'exit_code':exit_code,'duration_seconds':time.time()-start,'stdout_bytes':len(stdout.encode()),'stderr_bytes':(replay/'original.stderr.txt').stat().st_size,'external_file_inputs':[x['path']for x in deps],'local_program_imports':[],'third_party_libraries':[],'source_side_effect':'No main guard, all reads/audits before argparse; --output requires new file directly in HERE and x mode; stdout two separate JSON documents','path_difference':'source and four original JSON inputs at original repo-relative paths under independent source-root, not frozen physical root','report_created':output.exists(),'stdout_json_document_count':len(docs),'conditional_PAY_assertion_hits':len(pay_hits)}
if output.exists():
 report=json.loads(output.read_text());state.update({'report_bytes':output.stat().st_size,'report_sha256':sha(output),'matches_frozen_report_ids':[x['id']for x in rows if x['path'].endswith('.json')and output.read_bytes()==(E/'original'/x['path']).read_bytes()],'stdout_equals_report_bytes':stdout.encode()==output.read_bytes(),'stdout_documents_reconstruct_report':len(docs)==2 and {**docs[0],'capture_flow':docs[1]}==report})
(replay/'execution-state.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n');print(json.dumps(state,ensure_ascii=False));assert exit_code==0,'Original failure kept, no automatic retry'
