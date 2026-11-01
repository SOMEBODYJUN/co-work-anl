"""Call the unmodified original Probe once on the saved input; no random main."""
import argparse,hashlib,importlib.util,json,platform,sys,time
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
import scipy

def fingerprint(p):
    raw=p.read_bytes();return {'path':str(p.resolve()),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def main():
    assert __debug__
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--input',type=Path,required=True)
    ap.add_argument('--out-dir',type=Path,required=True)
    a=ap.parse_args();source=a.source.resolve();inp=a.input.resolve();out=a.out_dir.resolve()
    sf=fingerprint(source);inf=fingerprint(inp)
    assert sf['sha256']=='4db23c4998abc729dafb08bf6535ec825231a7ba21a37690ca52e374b33cb842'
    assert inf['sha256']=='19ad9937d6c7149dfef7ccfc4e33f914f6360c8f90619f2a0db9652befb15913'
    data=json.loads(inp.read_bytes());assert (data['n'],data['k'])==(5,7)
    w=np.array(data['weights'],dtype=np.int64)
    assert w.shape==(127,) and np.all(w>=0) and int(w.sum())==34
    out.mkdir(parents=True,exist_ok=False)
    started=datetime.now(timezone.utc).isoformat();clock=time.perf_counter()
    spec=importlib.util.spec_from_file_location('frozen_static_security_search',source)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    init_start=time.perf_counter();p=mod.Probe(data['n'],data['k']);init_seconds=time.perf_counter()-init_start
    solve_start=time.perf_counter()
    ratio,target,v,query,results,pay=p.solve(w)
    solve_seconds=time.perf_counter()-solve_start
    root=results[(0,)*p.k]
    returned={'n':p.n,'k':p.k,'weights':w.tolist(),'ratio_W_over_nv':ratio,'v_screen':v,'query_screen':query.tolist(),'target':list(p.term[target]),'target_index':target,'target_welfare':int(p.cov[target]@w),'root_outcome_indices':list(map(int,root)),'root_outcome_counts':[list(p.term[int(i)]) for i in root],'root_outcomes':len(root),'state_count':len(results),'state_outcome_sizes':sorted({len(x) for x in results.values()}),'scale':p.scale,'terminal_count':len(p.term),'background_count':len(p.backgrounds),'dtype':{'q':str(p.q.dtype),'inc':str(p.inc.dtype),'loads':str(p.loads.dtype),'pay_coefficients':str(p.pay.dtype),'weights':str(w.dtype),'weighted_pay':str(pay.dtype),'security':str(p.security.dtype),'outcome_indices':str(root.dtype)},'ranges':{'q_min':int(p.q.min()),'q_max':int(p.q.max()),'coefficient_min':int(p.pay.min()),'coefficient_max':int(p.pay.max()),'weighted_pay_min':int(pay.min()),'weighted_pay_max':int(pay.max()),'integer_dot_product_upper_bound':p.scale*int(w.sum())},'matches_saved_fields':{key:(returned_value==data[key]) for key,returned_value in [('ratio_W_over_nv',ratio),('v_screen',v),('query_screen',query.tolist()),('target',list(p.term[target]))]},'scope':'original unmodified Probe.solve return; numerical LP values are not independently certified here'}
    (out/'original-return.json').write_text(json.dumps(returned,indent=2)+'\n')
    states=[{'prefix_counts':list(q),'terminal_indices':list(map(int,results[q])),'terminal_counts':[list(p.term[int(i)]) for i in results[q]]} for q in sorted(results,key=lambda q:(sum(q),q))]
    (out/'outcome-sets.json').write_text(json.dumps({'scope':'all original count-state outcome sets; not a complete ordered-history action table','states':states},indent=2)+'\n')
    (out/'terminal-payments.json').write_text(json.dumps({'scope':'original returned scaled pay matrix, one row per terminal count, unoccupied actions zero','scale':p.scale,'terminal_counts':[list(q) for q in p.term],'scaled_pay':pay.tolist()},indent=2)+'\n')
    event={'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'duration_seconds':time.perf_counter()-clock,'init_seconds':init_seconds,'solve_seconds':solve_seconds,'invocation':'import unchanged frozen source under a non-main module name; Probe(5,7); solve(saved int64 weights) exactly once','original_main_runs':0,'original_Probe_initializations':1,'original_solve_calls':1,'original_integer_BI_calls':1,'original_security_LP_calls':1,'random_candidates_regenerated':0,'versions':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},'inputs_before':[sf,inf],'inputs_after':[fingerprint(source),fingerprint(inp)],'files':{path.name:fingerprint(path) for path in sorted(out.iterdir()) if path.is_file()},'LP_success_flag':'not returned or checked by original source; successful return observed','full_ordered_policy_certificate_generated':False,'independent_fraction_audit_run_here':False}
    assert event['inputs_before']==event['inputs_after']
    assert returned['target_welfare']==29 and len(root)==1 and len(results)==792
    assert all(len(x)==1 for x in results.values()) and list(p.term[target])==[0,0,0,0,0,5,0]
    (out/'execution.json').write_text(json.dumps(event,indent=2)+'\n')
    print(json.dumps({'original_calls':{'init':1,'solve':1,'BI':1,'LP':1,'main':0},'init_seconds':init_seconds,'solve_seconds':solve_seconds,'returned':returned},indent=2))
if __name__=='__main__':main()
