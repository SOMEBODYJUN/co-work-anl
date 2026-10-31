#!/usr/bin/env python3
"""Replay exact frozen fractional-load evidence without modifying originals.

Requires only Python standard library. The output directory must not exist.
Original auditors run from a temporary mirror; reports are copied out only after
all auditors succeed. Universal mathematical claims remain in the Markdown.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from fractions import Fraction
import argparse, hashlib, importlib.util, json, shutil, subprocess, sys

HERE=Path(__file__).resolve().parent
C13=Path('research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security')
A13=Path('research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round10/security')

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,required=True);args=p.parse_args()
 if args.output_dir.exists():p.error('output directory already exists')
 for row in json.loads((HERE/'source-manifest.json').read_text()):
  raw=(HERE/'original'/row['path']).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
 with TemporaryDirectory(prefix='fractional-load-replay-') as td:
  tmp=Path(td);root=tmp/'original';shutil.copytree(HERE/'original',root)
  out=tmp/'reports';out.mkdir()
  commands=[
   [sys.executable,str(root/'tests/audits/customer_attraction_fractional_actual_load.py'),'--output',str(out/'replay-actual-load.json')],
   [sys.executable,str(root/'tests/audits/customer_attraction_fractional_cover.py'),'--output',str(out/'replay-cover.json')],
   [sys.executable,str(root/'tests/audits/customer_attraction_waterfill.py'),'--output',str(out/'replay-waterfill.json')],
   [sys.executable,str(root/C13/'audit_refined_tax_packet.py')],
   [sys.executable,str(root/A13/'old13_alpha_one_tax_arithmetic.py')]]
  for command in commands:
   result=subprocess.run(command,cwd=root,text=True,capture_output=True)
   if result.returncode:
    sys.stderr.write(result.stdout+result.stderr);raise RuntimeError(command[-1])
  shutil.copy2(root/C13/'refined_tax_k10_audit.json',out/'replay-refined-tax.json')
  shutil.copy2(root/A13/'old13_alpha_one_tax_arithmetic.json',out/'replay-alpha-one.json')
  spec=importlib.util.spec_from_file_location('fractional_actual_audit',root/'tests/audits/customer_attraction_fractional_actual_load.py')
  module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  certificate=json.loads((root/'evidence/certificates/customer_attraction/fractional_actual_load_failure.json').read_text())
  _,generated=module.construct(4)
  original={tuple(row['history']):row['action']for row in certificate['actions']}
  canonical={tuple(row['history']):row['action']for row in generated['actions']}
  diff=[{'history':list(h),'original':original[h],'canonical_beta':canonical[h]}for h in original if original[h]!=canonical[h]]
  assert len(diff)==13
  comparison={'topic_order':['A','B','Q','D'],'different_off_path_nodes':len(diff),'differences':diff,'scope':'Both tables independently audited; original table is preserved rather than replaced by canonical beta tie choices.'}
  (out/'certificate-comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
  a=json.loads((out/'replay-actual-load.json').read_text());c=json.loads((out/'replay-cover.json').read_text());w=json.loads((out/'replay-waterfill.json').read_text());r=json.loads((out/'replay-refined-tax.json').read_text());one=json.loads((out/'replay-alpha-one.json').read_text())
  assert a['concrete_full_history_audit']['weak_bridge_gap']=='11/26'
  assert r['aggregate_refined_tax_violation']=='29481/123025'
  assert one['m_max_g_minus_W_minus_J']=='37/66'
  summary={'status':'passed','original_source_hashes_verified':True,'original_certificate_nodes':a['concrete_full_history_audit']['ordered_decision_nodes'],'original_proper_comparisons':a['concrete_full_history_audit']['proper_action_comparisons'],'family_players':[x['players'] for x in a['family_full_history_audits']],'cover_regression':c['finite_spe'],'waterfill_rational_cases':len(w['rational_cases']),'waterfill_all_subset_queries':sum(x['queries_checked']for x in w['rational_cases']),'refined_tax_automaton_nodes':r['automaton_nodes'],'refined_tax_comparisons':r['decision_comparisons'],'refined_tax_violation':r['aggregate_refined_tax_violation'],'alpha_one_violation':one['m_max_g_minus_W_minus_J'],'scope':'Finite complete certificates and boundary regressions; universal family/product/waterfill conclusions are analytic proofs, not finite search extrapolations.'}
  (out/'replay-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
  shutil.copytree(out,args.output_dir)
  print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
