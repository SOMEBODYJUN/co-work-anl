#!/usr/bin/env python3
"""Only the three frozen ranges: preserve source layout and compare finite records.

The reports contain floating optima, not exact dual certificates. Numerical
comparison below does not upgrade their evidence level.
"""
from pathlib import Path
import hashlib
import json
import math
import os
import platform
import shutil
import subprocess
import sys
import time

P = Path(__file__).resolve().parent
RUNTIME = Path('/workspace/scratch/9559bf893d22/boss3_security_probes_runtime')
REL = Path('research/workspaces/customer-attraction/R-5d61c5324e744dc0a66133207fcbd010/security')


def compare(expected, actual, path='root'):
    if type(expected) is float:
        assert isinstance(actual, (float, int)), (path, expected, actual)
        assert math.isfinite(actual) and abs(expected-actual) <= 1e-7, (path, expected, actual)
        return [abs(expected-actual)]
    assert type(expected) is type(actual), (path, type(expected), type(actual))
    if isinstance(expected, dict):
        assert list(expected) == list(actual), (path, list(expected), list(actual))
        return [v for k in expected for v in compare(expected[k], actual[k], path+'.'+k)]
    if isinstance(expected, list):
        assert len(expected) == len(actual), path
        return [v for i, (x, y) in enumerate(zip(expected, actual))
                for v in compare(x, y, path+f'[{i}]')]
    assert expected == actual, (path, expected, actual)
    return []


def main():
    import numpy
    import scipy
    specs = [
        ('direct-n4', 'direct_floor_probe.py', 7, 4, 16, 231026,
         'direct_floor_probe_n4_k7_seed231026.json'),
        ('direct-n5', 'direct_floor_probe.py', 7, 5, 4, 231027,
         'direct_floor_probe_n5_k7_seed231027.json'),
        ('padding-n3', 'safe_padding_probe.py', 6, 3, 8, 231028,
         'safe_padding_probe_n3_k6_seed231028.json'),
    ]
    manifest = json.loads((P/'dependency-manifest.json').read_text())
    events = []
    for label, entry, k, m, cases, seed, report in specs:
        root = RUNTIME/label
        assert not root.exists(), ('fresh runtime required', str(root))
        source = root/REL
        source.mkdir(parents=True)
        inputs = []
        for name in ('direct_floor_probe.py', 'safe_padding_probe.py'):
            data = (P/'original'/name).read_bytes()
            (source/name).write_bytes(data)
            inputs.append({'path':str(REL/name),'sha256':hashlib.sha256(data).hexdigest()})
        for x in manifest:
            src=P/'dependencies'/x['path']; data=src.read_bytes()
            assert hashlib.sha256(data).hexdigest() == x['sha256']
            target=root/x['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
            inputs.append({'path':x['path'],'sha256':x['sha256']})
        command=[sys.executable,str(source/entry),'--topics',str(k),'--players',str(m),
                 '--cases',str(cases),'--seed',str(seed)]
        start=time.perf_counter()
        result=subprocess.run(command,cwd=root,capture_output=True,
                              env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        elapsed=time.perf_counter()-start
        (P/(label+'.stdout')).write_bytes(result.stdout)
        (P/(label+'.stderr')).write_bytes(result.stderr)
        assert result.returncode==0,(label,result.returncode,result.stderr.decode())
        data=(source/report).read_bytes()
        (P/('replayed_'+report)).write_bytes(data)
        expected_data=(P/'original'/report).read_bytes()
        expected=json.loads(expected_data);actual=json.loads(data)
        diffs=compare(expected,actual)
        assert len(actual['records']) == cases
        assert not (source/'direct_floor_candidate.json').exists()
        assert not (source/'safe_padding_candidate.json').exists()
        event={'label':label,'command':command,'cwd':str(root),'input_files':inputs,
               'returncode':result.returncode,'wall_seconds':elapsed,'records':cases,
               'exact_structure_and_nonfloat_fields_match':True,
               'float_values_compared':len(diffs),'absolute_tolerance':1e-7,
               'max_absolute_float_difference':max(diffs,default=0),
               'byte_exact':data==expected_data,'candidate_file_created':False,
               'replayed_report_sha256':hashlib.sha256(data).hexdigest()}
        events.append(event)
        (P/'replay-events.json').write_text(json.dumps({'scope':'finite float replay; no exact cone upper certificates',
             'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,
             'runs':events},indent=2)+'\n')
        print(json.dumps({k:v for k,v in event.items() if k not in ('input_files','command')}),flush=True)


if __name__ == '__main__':
    main()
