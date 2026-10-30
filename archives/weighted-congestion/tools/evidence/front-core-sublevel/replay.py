#!/usr/bin/env python3
"""Four original audits in isolated copies, recording actual complete games."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent
BASE=Path('research/workspaces/shared/R-4018d5657f5d492ba41aa074bf9a5bbd/application_drafts')
CONFIG=[('quote_dp','algorithmic_core','quote_dp_audit.py','quote_dp_audit.json'),('front_quote','algorithmic_core','front_quote_audit.py',None),('source_sublevel','endpoint_applications','audit.py','audit.json'),('sparse_repair','repair_design','sparse_repair_audit.py',None)]
WRAPPER=r'''import json,runpy,sys
from fractions import Fraction
from pathlib import Path
records=[];seen=set()
def enc(v):
    if isinstance(v,Fraction):return str(v)
    if hasattr(v,'masks') and hasattr(v,'coefficients'):return {'masks':list(v.masks),'coefficients':enc(v.coefficients)}
    if isinstance(v,dict):return {str(k):enc(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [enc(x) for x in v]
    if isinstance(v,(set,frozenset)):return sorted(v)
    return v
def profile(f,event,arg):
    name=f.f_code.co_name
    if name not in ('solve','build','run_case','ratio_min','next_states'):return
    loc=f.f_locals;file=Path(f.f_code.co_filename).name
    if event=='call' and name=='solve' and file=='quote_dp_audit.py':
        records.append({'kind':'QDP solve','game':enc(loc['game']),'bags':enc(loc['bags']),'children':enc(loc['children']),'beta':enc(loc['beta']),'eps':enc(loc['eps'])})
    elif event=='return' and name=='build' and file=='front_quote_audit.py':
        records.append({'kind':'FQDP literal game','test':f.f_back.f_locals['test'],'game':enc(arg[0]),'classes':enc(arg[1]),'RD':enc(arg[2])})
    elif event=='call' and name=='solve' and file=='front_quote_audit.py':
        records.append({'kind':'FQDP solve parameters','domains':enc(loc['domains']),'bags':enc(loc['bags']),'children':enc(loc['children']),'beta':enc(loc['beta']),'eps':enc(loc['eps'])})
    elif event=='return' and name=='run_case' and file=='sparse_repair_audit.py':
        records.append({'kind':'sparse literal game','n':loc['n'],'alpha':enc(loc['alpha']),'p':loc['p'],'epsilon':enc(loc['epsilon']),'degree_override':loc['degree_override'],'degree':loc['D'],'weights':enc(loc['weights']),'allowed_actions':[[0,1] for _ in range(loc['n'])]+[[0]],'base':enc(loc['base']),'gates':enc(loc['gates'])})
    elif event=='call' and file=='audit.py' and f.f_back:
        p=f.f_back;pl=p.f_locals;parent=p.f_code.co_name
        if name=='ratio_min' and parent=='integral_audits':
            key=('integral',pl['_'])
            if key not in seen:
                seen.add(key);records.append({'kind':'integral source game','index':pl['_'],'weights':enc(pl['weights']),'menus':enc(pl['menus']),'polynomials':enc(pl['polynomials']),'seed':enc(pl['seed']),'cap':enc(pl['cap'])})
        elif name=='next_states' and parent=='transfer_audits':
            key=('tail',pl['_'])
            if key not in seen:
                seen.add(key);records.append({'kind':'high-degree tail game','index':pl['_'],'weights':enc(pl['weights']),'menus':enc(pl['menus']),'polynomials':enc(pl['orig']),'seed':enc(pl['seed']),'cap':enc(pl['cap']),'degree':pl['d'],'kappa':enc(pl['kappa']),'alpha':enc(pl['alpha'])})
sys.setprofile(profile)
try:runpy.run_path(sys.argv[1],run_name='__main__')
finally:
    sys.setprofile(None)
    Path('actual-game-inputs.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
'''
def run(config,output):
    name,group,code,frozen_name=config;work=output/name;work.mkdir(parents=True,exist_ok=True)
    source=ROOT/'original'/BASE/group/code;copy=work/code;shutil.copyfile(source,copy)
    report=work/(Path(code).stem+'.json' if name in ('front_quote','sparse_repair') else ('quote_dp_audit.json' if name=='quote_dp' else 'audit.json'))
    assert not report.exists(),('new output directory required',str(report))
    helper=None
    if name=='front_quote':
        helper=ROOT/'original'/BASE/group/'quote_dp_audit.py';shutil.copyfile(helper,work/helper.name)
    (work/'capture_inputs.py').write_text(WRAPPER)
    result=subprocess.run([sys.executable,'-B','capture_inputs.py',code],cwd=work,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (work/'stdout.txt').write_bytes(result.stdout);(work/'stderr.txt').write_bytes(result.stderr)
    assert result.returncode==0,(name,result.stderr.decode())
    actual=json.loads(report.read_bytes());inputs=json.load(open(work/'actual-game-inputs.json'))
    row={'name':name,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'copy_sha256':hashlib.sha256(copy.read_bytes()).hexdigest(),'exit_code':0,'actual_report':report.name,'actual_result':actual,'input_records':len(inputs),'input_kinds':{k:sum(x['kind']==k for x in inputs) for k in sorted({x['kind'] for x in inputs})}}
    if helper:row['helper_sha256']=hashlib.sha256(helper.read_bytes()).hexdigest()
    if frozen_name:
        frozen=ROOT/'original'/BASE/group/frozen_name;old=json.load(open(frozen));assert old==actual,(name,'frozen JSON mismatch');row.update(frozen_path=str(BASE/group/frozen_name),json_equal=True,report_byte_equal=frozen.read_bytes()==report.read_bytes())
    else:row.update(frozen_path=None,comparison_scope='new actual output; no frozen JSON in this claimed inventory closure, assertions passed only')
    return row
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path);args=parser.parse_args();output=args.output_dir.resolve() if args.output_dir else ROOT/'replay';output.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(lambda c:run(c,output),CONFIG))
    result={'runs':rows,'all_passed':True,'originals_never_run_in_place':True,'profiler_only_records_arguments_and_literal_games_no_function_replacement':True}
    (output/'comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps([{k:x.get(k) for k in ('name','exit_code','json_equal','report_byte_equal','input_records','input_kinds')} for x in rows]))
