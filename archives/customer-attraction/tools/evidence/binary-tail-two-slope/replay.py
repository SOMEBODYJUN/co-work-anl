#!/usr/bin/env python3
"""Replay original two-slope certificates and independent raw-share audits.

Default uses only the standard library and frozen rational certificates.
--rediscover additionally runs the original NumPy/SciPy discovery and recovery.
The pinned Git reader is executed unchanged against its actual local Git object.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

BASE=Path(__file__).resolve().parent
REPO=next(p for p in BASE.parents if (p/'AGENTS.md').is_file())
PIN='a1d7184466e5ae115a86efd8c0da6da2aabfaa09'
CERT_PATH='research/workspaces/customer-attraction/R-febfdd131cde4128882ca0edd4d712ba/parent/binary_tail_exact_1999.json'

def run(command):
    result=subprocess.run(command,cwd=BASE/'replay',capture_output=True,text=True,check=True)
    assert not result.stderr,result.stderr
    return result.stdout

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rediscover',action='store_true')
    args=parser.parse_args()
    (BASE/'replay').mkdir(parents=True,exist_ok=True)
    pinned=subprocess.check_output(['git','show',PIN+':'+CERT_PATH],cwd=REPO)
    assert pinned==(BASE/'original/binary_tail_exact_1999.json').read_bytes()
    comparisons={}
    with tempfile.TemporaryDirectory(prefix='two-slope-replay-',dir=BASE) as tmp:
        tmp=Path(tmp);parent=tmp/'asset/parent';ind=tmp/'asset/independent';rawdir=tmp/'raw-audits'
        for p in (parent,ind,rawdir):p.mkdir(parents=True)
        for name,target in [('binary_tail_pareto.py',parent),('audit_binary_tail_certificate.py',ind),('oct25_binary_tail_raw_audit.py',rawdir)]:
            shutil.copyfile(BASE/'source'/name,target/name)
        if args.rediscover:
            stdout=run([sys.executable,str(parent/'binary_tail_pareto.py')])
            (BASE/'replay/discovery.stdout.txt').write_text(stdout)
            shutil.copyfile(parent/'binary_tail_pareto.json',BASE/'replay/binary_tail_pareto.json')
        for name,beta0 in [('binary_tail_exact','2'),('binary_tail_exact_1999','1999/1000')]:
            original=BASE/'original'/(name+'.json')
            if args.rediscover:
                stdout=run([sys.executable,str(parent/'binary_tail_pareto.py'),'--exact','--beta0',beta0,'--beta1','5/3','--output',name+'.json'])
                (BASE/'replay'/(name+'.author.stdout.txt')).write_text(stdout)
                recovered=json.loads((parent/(name+'.json')).read_text())
                reference=json.loads(original.read_text())
                assert recovered==reference,(name,'exact recovered certificate differs')
                comparisons[name]={'all_recovered_fields_equal':True,'recovered_sha256':hashlib.sha256((parent/(name+'.json')).read_bytes()).hexdigest()}
            else:
                shutil.copyfile(original,parent/(name+'.json'))
            shutil.copyfile(parent/(name+'.json'),BASE/'replay'/(name+'.json'))
            stdout=run([sys.executable,str(ind/'audit_binary_tail_certificate.py'),'--certificate',str(parent/(name+'.json'))])
            report=json.loads(stdout)
            reference=json.loads((BASE/'original'/('audit_'+name+'.json')).read_text())
            assert report==reference,name
            shutil.copyfile(ind/('audit_'+name+'.json'),BASE/'replay'/('audit_'+name+'.json'))
            comparisons.setdefault(name,{})['original_independent_report_all_fields_equal']=True
        initial=json.loads((BASE/'replay/audit_binary_tail_exact.json').read_text())
        old=json.loads((BASE/'original/binary_tail_audit.json').read_text())
        assert all(initial.get(k)==v for k,v in old.items())
        stdout=run([sys.executable,str(rawdir/'oct25_binary_tail_raw_audit.py')])
        (BASE/'replay/oct25_binary_tail_raw_audit.stdout.txt').write_text(stdout)
        report=json.loads((rawdir/'oct25_binary_tail_raw_audit.json').read_text())
        original=json.loads((BASE/'original/oct25_binary_tail_raw_audit.json').read_text())
        assert report==original
        shutil.copyfile(rawdir/'oct25_binary_tail_raw_audit.json',BASE/'replay/oct25_binary_tail_raw_audit.json')
    result={'scope':'original-implementation-replay-with-actual-pinned-git-read',
            'new_independent_reviewer_claimed':False,'rediscovery_run':args.rediscover,
            'pinned_certificate_bytes_equal_frozen_source':True,
            'pinned_ref':PIN,'certificate_sha256':hashlib.sha256(pinned).hexdigest(),
            'certificate_replays':comparisons,
            'old_initial_audit_all_fields_preserved_in_current_initial_report':True,
            'second_raw_share_audit_all_fields_equal':True,
            'raw_row_digest':report['raw_rows_sha256'],
            'retained_residual_states':len(report['retained_residuals_160']),
            'all_checks_passed':True}
    (BASE/'replay/reconciliation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
