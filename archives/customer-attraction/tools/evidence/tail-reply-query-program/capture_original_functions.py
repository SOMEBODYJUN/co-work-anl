"""Call only the unchanged original exact row/state functions on four frozen cuts.

No original main/discover/linprog call. This is an original-function replay,
not a second independent mathematical implementation or historical CLI event.
"""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import json
import sys
import time


def main():
    ap = ArgumentParser()
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--point', type=Path, required=True)
    ap.add_argument('--cuts', type=Path, required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    args = ap.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    raw = args.source.read_bytes()
    assert sha256(raw).hexdigest() == '5c474c910391fed3e3eecf801146aeb25c0f4dd1a2f88bd99ef313c8612b004c'
    point_raw, cuts_raw = args.point.read_bytes(), args.cuts.read_bytes()
    point, cuts = json.loads(point_raw), json.loads(cuts_raw)
    assert cuts['source_sha256'] == sha256(point_raw).hexdigest()
    assert cuts['source_W'] == point['W']
    cols = point['columns']; weights = [F(c['weight']) for c in cols]
    assert len(cols) == 1905 and min(weights) >= 0 and len(cuts['selected']) == 4
    spec = spec_from_file_location('frozen_tail_reply_cuts', args.source.resolve())
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    calls = Counter()
    source_path = str(args.source.resolve())
    def profile(frame, event, arg):
        if event == 'call':
            code = frame.f_code
            if code.co_filename == source_path:
                calls[code.co_name] += 1
            elif code.co_name == 'linprog':
                calls['external_linprog'] += 1
    before = {str(p): sha256(p.read_bytes()).hexdigest() for p in [args.source,args.point,args.cuts]}
    start = time.monotonic(); records = []
    sys.setprofile(profile)
    try:
        for cut in cuts['selected']:
            assert F(cut['alpha']) >= 0 and F(cut['gamma']) >= 0
            states, ui, u6 = module.states(point, cut)
            row = module.coefficient_rows(cols, cut)
            assert len(row) == len(cols)
            value = sum(c*w for c,w in zip(row,weights))
            r = 5-cut['i']
            direct = ui+r*F(cut['alpha'])*u6-sum(w*module.psi(*state,r,F(cut['alpha']),F(cut['gamma'])) for state,w in states.items())
            assert value == direct == F(cut['slack']) < 0
            assert all(row[j] == 0 for j,c in enumerate(cols) if c['kind'] in ['K','overlap'])
            records.append({'cut':cut,'u_source':str(ui),'u6':str(u6),
                            'state_count':len(states),'state_mass':str(sum(states.values())),
                            'states':[{'b':k[0],'ell':k[1],'t':k[2],'q_count':k[3],'mass':str(w)} for k,w in sorted(states.items())],
                            'coefficients':[str(x) for x in row],
                            'nonzero_coefficients':sum(x != 0 for x in row),
                            'row_value':str(value),'direct_state_value':str(direct)})
    finally:
        sys.setprofile(None)
    elapsed = time.monotonic()-start
    assert calls['states']==4 and calls['coefficient_rows']==4
    assert calls['main']==calls['discover']==calls['external_linprog']==0
    assert before == {str(p): sha256(p.read_bytes()).hexdigest() for p in [args.source,args.point,args.cuts]}
    result = {'scope':'Unchanged original functions, four frozen selected cuts only; no discovery or whole-5287-graph check.','records':records}
    out = args.output_dir/'original-function-rows.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    import numpy, scipy
    report = {'status':'PASS_FOUR_FROZEN_ROWS_IN_ORIGINAL_EXACT_FUNCTIONS','python':sys.version,
              'numpy':numpy.__version__,'scipy':scipy.__version__,
              'argv':sys.argv,'assertions_enabled':__debug__,
              'source_sha256':sha256(raw).hexdigest(),'point_sha256':sha256(point_raw).hexdigest(),
              'cuts_sha256':sha256(cuts_raw).hexdigest(),'wrapper_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
              'elapsed_seconds':elapsed,'primary_function_calls':dict(calls),
              'original_main_calls':0,'original_discover_calls':0,'LP_calls':0,
              'frozen_files_unchanged':True,'rows':4,'columns_per_row':1905,
              'all_row_values_equal_frozen_negative_slacks':True,
              'row_report_sha256':sha256(out.read_bytes()).hexdigest()}
    (args.output_dir/'function-execution.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
