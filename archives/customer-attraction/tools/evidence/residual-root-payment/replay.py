#!/usr/bin/env python3
"""Replay the unchanged residual-payment counterexample audit.

Restores its documented read-only certificate path in a temporary fixture using
ordinary copies only. No symlinks, solver, network or Git mutation is used.
"""
from pathlib import Path
import hashlib
import json
from itertools import product
import runpy
import shutil
import subprocess
import sys
import tempfile

BASE=Path(__file__).resolve().parent
REPO=next(p for p in BASE.parents if (p/'AGENTS.md').is_file())
CERT_REL='research/workspaces/customer-attraction/R-febfdd131cde4128882ca0edd4d712ba/parent/binary_tail_exact_1999.json'
CERT_SHA='dc50440f598bad7c511e01bccd8cb14a0c8f84d61396df354cdff8631e292511'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    source=BASE/'source/audit_residual_payment.py'
    certificate=BASE/'inputs/binary_tail_exact_1999.json'
    original=BASE/'original/residual_payment_audit.json'
    assert sha(certificate)==CERT_SHA
    cert=json.loads(certificate.read_text())
    assert cert['beta0']=='1999/1000' and cert['beta1']=='5/3' and len(cert['multipliers'])==13
    source_hash=sha(source)
    with tempfile.TemporaryDirectory(prefix='residual-payment-replay-',dir=BASE) as tmp:
        tmp=Path(tmp);fixture=tmp/'fixture';fixture.mkdir()
        # The original script reads only is_file() for this real marker copy.
        shutil.copyfile(REPO/'AGENTS.md',fixture/'AGENTS.md')
        target=fixture/CERT_REL;target.parent.mkdir(parents=True);shutil.copyfile(certificate,target)
        work=fixture/'five_background';work.mkdir();copy=work/source.name;shutil.copyfile(source,copy)
        assert sha(copy)==source_hash and sha(target)==CERT_SHA
        process=subprocess.run([sys.executable,str(copy)],cwd=work,check=True,capture_output=True,text=True)
        assert not process.stderr
        result=work/'residual_payment_audit.json'
        report=json.loads(result.read_text())
        assert report==json.loads(original.read_text())
        (BASE/'replay').mkdir(parents=True,exist_ok=True)
        shutil.copyfile(result,BASE/'replay/residual_payment_audit.json')
        (BASE/'replay/audit_residual_payment.stdout.txt').write_text(process.stdout)
        functions=runpy.run_path(str(copy))
        positive=[]
        for aux in product((0,1),repeat=3):
            positive.append({'qrs':''.join(map(str,aux)),
                             'root_B':str(functions['rho'](1,(1,1,1,1),aux,0)),
                             'root_private':str(functions['rho'](0,(1,1,1,1),aux,1))})
        table={'scope':'displayed-two-positive-type-minimizations-from-preserved-certificate',
               'new_independent_review_claimed':False,'rows':positive}
        previous=BASE/'replay/positive_type_eight_cases.json'
        if previous.exists():assert json.loads(previous.read_text())==table
        previous.write_text(json.dumps(table,indent=2)+'\n')
    assert sha(source)==source_hash
    out={'scope':'unchanged-original-residual-payment-audit-replay',
         'new_independent_reviewer_claimed':False,'symlinks_used':False,
         'source_sha256':source_hash,'certificate_sha256':CERT_SHA,
         'original_report_all_fields_equal':True,
         'original_report_sha256':sha(original),
         'replayed_report_sha256':sha(BASE/'replay/residual_payment_audit.json'),
         'history_nodes':report['histories'],'nonprescribed_IC':report['IC_comparisons'],
         'strict':report['strict'],'tied':report['tied'],
         'root_branches':len(report['branch_detail']),
         'unit_client_branch_cases':5*9,'auxiliary_cases_per_minimum':8,
         'residual_payment_defect':report['residual_payment_defect'],
         'defect_after_actual_matched_G':report['defect_after_also_subtracting_actual_matched_G'],
         'all_checks_passed':True}
    (BASE/'replay/reconciliation.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
