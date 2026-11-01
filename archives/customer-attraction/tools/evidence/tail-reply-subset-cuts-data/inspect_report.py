"""Bind every empty-report field to the exact source point and static search domain.

No original module is imported, no original helper/main/discover is called,
and no LP or coefficient scan is performed. Existing point audits are reused.
"""
import argparse
import ast
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

def fingerprint(path):
    data=path.read_bytes()
    return {'path':str(path),'bytes':len(data),'sha256':sha256(data).hexdigest()}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--report',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();assert __debug__
    evidence=args.repo/'archives/customer-attraction/tools/evidence'
    codepath=evidence/'continuous-query-refinement-program/related/tail_reply_subset.py'
    pointpath=evidence/'continuous-query-refinement-program/related/continuous_refinement_exact.json'
    auditpath=evidence/'continuous-refinement-necessary-point/point-audit.json'
    eventpath=evidence/'continuous-query-refinement-program/rerun/execution.json'
    stdoutpath=evidence/'continuous-query-refinement-program/rerun/stdout.txt'
    report=json.loads(args.report.read_bytes());point=json.loads(pointpath.read_bytes())
    source=codepath.read_text();tree=ast.parse(source)
    assert fingerprint(args.report)['sha256']=='90d4421d8de0b5012cba1554e6469d19fb4d2a9c629134c7fb7d5c34951de4c3'
    assert fingerprint(codepath)['sha256']=='9f812b0381186aa8546a038416b6335424673cbf1f895e8da40f7b6f4baadfdc'
    assert set(report)=={'best_float','selected','scope','source','source_sha256','source_W'}
    assert report['best_float']==[0,None] and type(report['best_float'][0]) is int
    assert report['selected']==[]
    assert fingerprint(pointpath)['sha256']==report['source_sha256']=='abac45f78980d02f2bd056758a96653aa0bc0d8b87571820a5742397dc490246'
    assert F(report['source_W'])==F(point['W'])
    suffix='research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_3/continuous_refinement_exact.json'
    assert report['source'].endswith('/'+suffix)
    assignments={node.targets[0].id:node.value for node in tree.body if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name)}
    orbs=ast.literal_eval(assignments['ORBS']);queries=ast.literal_eval(assignments['QUERIES'])
    assert orbs==((0,0),(1,0),(1,1))
    assert queries==('opt_subset','opt_include_i','opt_exclude_i','opt_include_ij')
    beta={}
    for k,v in zip(assignments['BETA'].keys,assignments['BETA'].values):
        assert isinstance(v,ast.Call) and isinstance(v.func,ast.Name) and v.func.id=='F'
        beta[ast.literal_eval(k)]=str(F(*(ast.literal_eval(a) for a in v.args)))
    assert beta=={1:'1',2:'3/2',3:'5/3',4:'1499/750'}
    discover=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='discover')
    loop=next(n for n in discover.body if isinstance(n,ast.For))
    assert ast.unparse(loop.iter)=='product(range(1, 5), range(2), ORBS, QUERIES)'
    assert ast.unparse(loop.target)=='(i, member, orb, q)'
    domain=[{'source_i_zero_based':i,'actual_player_one_based':i+1,'remaining_true_tail_players':5-i,'beta':beta[5-i],
      'member':member,'reply_label':'R' if member==0 else 'Z','orb':list(orb),'ordered_edges':6 if orb[1] else 30,'query':q,
      'status':'static planned loop key; not a recorded successful LP, tested price, or cut'}
      for i,member,orb,q in product(range(1,5),range(2),orbs,queries)]
    assert len(domain)==96
    audit=json.loads(auditpath.read_bytes());event=json.loads(eventpath.read_bytes());stdout=ast.literal_eval(stdoutpath.read_text())
    assert audit['source_sha256']==report['source_sha256'] and audit['source_bytes']==pointpath.stat().st_size
    assert audit['top_level_metadata']=={k:v for k,v in point.items() if k!='columns'}
    assert audit['actual_W']==report['source_W']
    assert event['exit_code']==0 and event['stderr_bytes']==0 and event['frozen_bytes_unchanged']
    assert sha256(stdoutpath.read_bytes()).hexdigest()==event['stdout_sha256']
    columns=point['columns'];kinds=Counter(c['kind'] for c in columns)
    # Full record decoding and consumption map only. The existing 194-group,
    # overlap, floor and all-5075 checks are not recalculated.
    fieldsets={kind:[list(fields) for fields in sorted({tuple(c) for c in columns if c['kind']==kind})] for kind in kinds}
    weights=[F(c['weight']) for c in columns]
    assert len(columns)==1905 and kinds=={'K':1,'hist':16,'joint-reply':582,'overlap':1306}
    result={'scope':'full six-field interpretation, exact-byte source binding, complete input record decoding and static planned domain only; no historical entrypoint/helper/LP or repeated point-row audit',
      'report':report,'inputs':[fingerprint(p) for p in (args.report,codepath,pointpath,auditpath,eventpath,stdoutpath)],
      'six_field_meanings':{
        'best_float':'[0,null] is the unchanged initial incumbent; no parameter witness or solver-status list is preserved',
        'selected':'empty; no alpha/gamma/slack/coefficient row certificate exists in this file',
        'scope':'collection scope for exactly negative legal r<=4 necessary rows; does not turn an empty collection into an exact closure certificate',
        'source':'historical absolute provenance path; resolved by matching frozen suffix and SHA, not accessed as a current path',
        'source_sha256':'cryptographic binding to the saved 5075-row continuous-refinement input, not the same-W 5108 point',
        'source_W':'exact input objective metadata copied by main; not an optimum or SPE witness'},
      'static_domain_count':len(domain),'beta':beta,'planned_domain_file':'planned-domain.json',
      'point_metadata':{k:v for k,v in point.items() if k!='columns'},'point_column_counts':dict(kinds),'point_record_fieldsets':fieldsets,
      'all_1905_weight_strings_parsed':len(weights),'input_consumption':{'hist':'actual bits, d, histogram, mass; source and terminal profits','joint-reply':'group/state/weight aggregated into one selected R or Z marginal','K':'not consumed by states or nonzero row coefficients','overlap':'not consumed by states or nonzero row coefficients','hist_column_old':'not used; current sequential histogram block used'},
      'reused_point_audit':{'status':audit['status'],'scope':audit['scope'],'normalization_O':audit['normalization_O'],'actual_W':audit['actual_W'],'positive_counts':audit['positive_counts'],'all_record_nonnegative_and_194_implicit_states':'already checked in bound point-audit; not repeated here'},
      'reused_original_point_verify':{'event_scope':event['scope'],'stdout':stdout,'exit_code':event['exit_code'],'historical_tail_subset_discovery':False},
      'no_new_original_entrypoint_or_helper_calls':True,'new_LP_calls':0,'new_exact_cut_evaluations':0,
      'not_in_report':['number of successful or failed LPs','per-direction solver status','elapsed time and solver versions','alpha or gamma of any candidate','exact primal/dual certificate for non-separation','full SPE strategy','general half proof']}
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'data-interpretation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    (args.output/'planned-domain.json').write_text(json.dumps({'scope':'96 static loop keys, not historical outcomes','domain':domain},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PASS','report_fields':len(report),'saved_cuts':len(report['selected']),'static_planned_keys':len(domain),'input_columns_decoded':len(columns),'new_LP_calls':0,'new_helper_calls':0,'source_binding':report['source_sha256']},indent=2))

if __name__=='__main__':main()
