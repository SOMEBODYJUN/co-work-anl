#!/usr/bin/env python3
"""Replay original retained-residual and aligned-credit calculations.

Uses the preserved 69-atom input only for the stated extra-row calculation;
does not reconstruct or certify the input's 727-row relaxation.
"""
from contextlib import redirect_stdout
from fractions import Fraction as F
from io import StringIO
from itertools import product
from pathlib import Path
import hashlib
import json
import runpy
import shutil
import subprocess
import sys
import tempfile

BASE=Path(__file__).resolve().parent
REPO=next(p for p in BASE.parents if (p/'work.py').is_file())
INPUT=BASE/'inputs/exact_optimum_primal_terminal_cross.json'
CANONICAL=BASE.parent/'tail-profit/source/customer_attraction_four_remaining_profit.py'

def decode_records(text):
    decoder=json.JSONDecoder();records=[]
    while text.strip():
        record,n=decoder.raw_decode(text.lstrip());records.append(record);text=text.lstrip()[n:]
    return records

def main():
    inp=json.loads(INPUT.read_text())
    # Inspect every input record without accepting its stored slacks as proofs.
    assert len(inp['atoms'])==69 and len(inp['slacks'])==727
    for atom in inp['atoms']:
        assert len(atom['bits'])==10 and set(atom['bits'])<={'0','1'}
        assert all(isinstance(n,int) and n>=0 for k in ('AB_hist','AE_hist','second_hist') for n in atom[k])
        assert all(sum(atom[k])==5 for k in ('AB_hist','AE_hist','second_hist'))
        assert F(atom['exact_mass'])>=0
    stored_slacks=[F(x) for x in inp['slacks'].values()]
    with tempfile.TemporaryDirectory(prefix='credit-replay-',dir=BASE) as tmp:
        tmp=Path(tmp)
        # Preserve original path depth: one audit computes ROOT by parents[5].
        sources={
          'four_background_residual.py':tmp/'research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/direct/four_background_residual.py',
          'audit_aligned_credit.py':tmp/'research/workspaces/customer-attraction/R-febfdd131cde4128882ca0edd4d712ba/root_tail/audit_aligned_credit.py',
          'audit_four_profit_root_gain.py':tmp/'research/workspaces/customer-attraction/R-febfdd131cde4128882ca0edd4d712ba/independent/audit_four_profit_root_gain.py'}
        for name,path in sources.items():
            path.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(BASE/'source'/name,path)
        (tmp/'work.py').symlink_to(REPO/'work.py')
        target=tmp/'research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round5_pricing/exact_optimum_primal_terminal_cross.json'
        target.parent.mkdir(parents=True);shutil.copyfile(INPUT,target)
        target=tmp/'tests/audits/customer_attraction_four_remaining_profit.py'
        target.parent.mkdir(parents=True);shutil.copyfile(CANONICAL,target)
        outputs={}
        for name,path in sources.items():
            completed=subprocess.run([sys.executable,str(path)],cwd=BASE/'replay',check=True,capture_output=True,text=True)
            assert not completed.stderr
            outputs[name]=completed.stdout
        captured=StringIO()
        with redirect_stdout(captured):
            residual=runpy.run_path(str(sources['four_background_residual.py']))
        assert not captured.getvalue()
        exact=residual['audit_primal'](INPUT)
        canonical=runpy.run_path(str(target))
        for p in (0,1):
            for actual in product((0,1),repeat=4):
                for aux in product((0,1),repeat=3):
                    assert residual['rho'](p,actual,aux)==canonical['direct_rho']((*actual,*aux),F(p))
        table={''.join(map(str,b)):[str(residual['mins'][p,b]) for p in (0,1)] for b in product((0,1),repeat=4)}
    old=json.loads((BASE/'original/four_background_residual_replay.json').read_text())
    lines=outputs['four_background_residual.py'].splitlines()
    assert len(lines)==17 and lines[-1]==old['last_line']
    assert hashlib.sha256((BASE/'source/four_background_residual.py').read_bytes()).hexdigest()==old['source_sha256']
    aligned=decode_records(outputs['audit_aligned_credit.py'])
    independent=decode_records(outputs['audit_four_profit_root_gain.py'])
    assert len(aligned)==1 and aligned[0]['table']==table
    assert len(independent)==2 and independent[0]['exact_best_c']=='251/1500'
    assert independent[1]['minimum_pattern_tables']=='PASS'
    for name,out in outputs.items():
        (BASE/'replay'/(Path(name).stem+'.stdout.txt')).write_text(out)
    (BASE/'replay/aligned_credit.json').write_text(json.dumps(aligned[0],indent=2)+'\n')
    (BASE/'replay/independent_root_gain.json').write_text(json.dumps({'records':independent},indent=2)+'\n')
    result={
      'scope':'original-implementation-replay-and-extra-row-evaluation-only',
      'new_independent_review_claimed':False,'canonical_raw_residual_equalities':256,
      'table':table,'original_replay_last_line_equal':True,'import_stdout_empty':True,
      'different_cwd_execution_succeeded':True,
      'finite_input':{'source_id':'91a2873f83444dd805ff','sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),
                      'atom_count':69,'stored_slack_count':len(stored_slacks),
                      'stored_slack_minimum':str(min(stored_slacks)),
                      'stored_slacks_reconstructed':False,
                      'full_relaxation_feasibility_or_optimality_certified':False,
                      'source_semantic_disposition_claimed':False},
      'extra_row_evaluation':{k:{'exact':str(v),'float_for_original_report_comparison':float(v)} for k,v in exact.items()},
      'all_checks_passed':True}
    (BASE/'replay/reconciliation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
