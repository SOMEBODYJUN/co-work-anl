#!/usr/bin/env python3
"""Replay the preserved complete ordered-history m=5 payment audit.

No symbolic links, game solver, LP, discovery generator or external data are
used. The original audit writes only beside its temporary unmodified copy.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

BASE=Path(__file__).resolve().parent

def main():
    source=BASE/'source/audit_joint_payment.py'
    original=BASE/'original/joint_payment_audit.json'
    source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix='joint-payment-replay-',dir=BASE) as tmp:
        tmp=Path(tmp);copy=tmp/source.name
        shutil.copyfile(source,copy)
        assert hashlib.sha256(copy.read_bytes()).hexdigest()==source_hash
        result=subprocess.run([sys.executable,str(copy)],cwd=tmp,check=True,capture_output=True,text=True)
        assert not result.stderr
        report=json.loads((tmp/'joint_payment_audit.json').read_text())
        assert report==json.loads(original.read_text())
        (BASE/'replay').mkdir(parents=True,exist_ok=True)
        shutil.copyfile(tmp/'joint_payment_audit.json',BASE/'replay/joint_payment_audit.json')
        (BASE/'replay/audit_joint_payment.stdout.txt').write_text(result.stdout)
    assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
    # Explicitly expand the fixed labels into the thirteen different unit clients.
    labels=[(a,b) for a in range(5) for b in range(4)]
    coverage={str(label):[label[0],5+2*label[1],6+2*label[1]] for label in labels}
    assert len({tuple(c) for c in coverage.values()})==20
    assert set().union(*(set(c) for c in coverage.values()))==set(range(13))
    summary={'scope':'original-full-ordered-history-payment-audit-replay',
             'new_independent_reviewer_claimed':False,'source_sha256':source_hash,
             'original_report_all_fields_equal':True,
             'original_report_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),
             'replayed_report_sha256':hashlib.sha256((BASE/'replay/joint_payment_audit.json').read_bytes()).hexdigest(),
             'unit_clients':13,'action_labels':20,'distinct_coverage_sets_in_this_example':20,
             'coverage_map':coverage,'histories':report['histories'],
             'nonprescribed_action_comparisons':report['comparisons'],
             'strict':report['strict'],'tied':report['tied'],
             'symlinks_used':False,'all_checks_passed':True}
    (BASE/'replay/reconciliation.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='coverage_map'},indent=2))

if __name__=='__main__':main()
