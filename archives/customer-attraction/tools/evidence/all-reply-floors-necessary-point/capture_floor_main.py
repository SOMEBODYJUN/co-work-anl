"""Execute the unchanged floor main once, observing its returned local values.

This is the original generator and its exact verification, not an independent
4963-row implementation. No discovery or LP branch is entered.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib
import json
import runpy
import sys


def main():
    runtime, output = map(Path, sys.argv[1:3])
    source = runtime / 'research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_3/all_reply_actual_floors.py'
    point = json.loads((source.parent/'all_reply_floors_exact.json').read_text())
    sys.argv = [str(source), '--priced', '--optimum', '--verify']
    sys.path.insert(0, str(source.parent))
    seen = []

    def observe(frame, event, arg):
        if event != 'return' or frame.f_code.co_filename != str(source) or frame.f_code.co_name != 'main':
            return
        local = frame.f_locals
        assert 'slacks' in local and 'w' in local
        names, rows, cols = local['names'], local['m'], local['cols']
        values = local['slacks']
        assert len(rows) == len(names) == len(values) == 4963
        # The author's verify branch checks weights by position; bind all
        # generated descriptors to the frozen point as an extra observation.
        frozen = [{k:v for k,v in c.items() if k != 'weight'} for c in point['columns']]
        normalized = json.loads(json.dumps(cols))
        assert normalized == frozen and len(cols) == 1905
        assert min(values) == Fraction(point['minimum_slack']) == 0
        assert local['w'] == Fraction(point['W'])
        text = json.dumps([[name,str(value)] for name,value in zip(names,values)], ensure_ascii=False, separators=(',',':'))
        report = {
            'scope': 'unchanged original floor main executed once via runpy; returned locals observed; no independent full-row derivation or optimization',
            'required_flags': ['--priced','--optimum','--verify'],
            'original_main_invocations_observed': 1,
            'generated_descriptors_equal_frozen_all_columns': True,
            'rows': len(rows), 'columns': len(cols),
            'slack_signs': dict(Counter('positive' if s>0 else 'zero' if s==0 else 'negative' for s in values)),
            'minimum_slack': str(min(values)), 'W': str(local['w']),
            'ordered_name_slack_sha256': hashlib.sha256(text.encode()).hexdigest(),
            'ordered_rows': [{'index':i,'name':name,'slack':str(value)} for i,(name,value) in enumerate(zip(names,values))]
        }
        (output/'original-row-slacks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        seen.append(True)

    sys.setprofile(observe)
    try:
        runpy.run_path(str(source),run_name='__main__')
    finally:
        sys.setprofile(None)
    assert seen == [True]


if __name__ == '__main__':
    main()
