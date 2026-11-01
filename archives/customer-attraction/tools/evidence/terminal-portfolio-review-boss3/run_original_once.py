"""Replay the unchanged standalone historical audit in a new external folder.

Usage: python3 run_original_once.py /absolute/new-empty-runtime
Only the audit source is an execution input; the old JSON is a comparison.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
CODE=HERE/'original/47bc029a1cfc7f55f5d5/review_terminal_portfolio.py'
REPORT=HERE/'original/f98a6bd9fd91fe44896e/review_terminal_portfolio.json'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    runtime=Path(sys.argv[1]).resolve();runtime.mkdir(parents=True,exist_ok=False)
    code=runtime/'review_terminal_portfolio.py';shutil.copyfile(CODE,code)
    before={str(p):sha(p) for p in (CODE,REPORT,code)}
    argv=[sys.executable,'-I','-B',str(code)]
    started=datetime.now(timezone.utc).isoformat();start=time.monotonic()
    result=subprocess.run(argv,cwd=runtime,input=b'',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    elapsed=time.monotonic()-start
    runs=HERE/'runs';runs.mkdir(exist_ok=True)
    (runs/'original.stdout').write_bytes(result.stdout);(runs/'original.stderr').write_bytes(result.stderr)
    generated=runtime/'review_terminal_portfolio.json'
    assert result.returncode==0 and not result.stderr
    shutil.copyfile(generated,runs/'generated-review.json')
    assert generated.read_bytes()==REPORT.read_bytes()==result.stdout
    after={str(p):sha(p) for p in (CODE,REPORT,code)};assert before==after
    record=dict(start_utc=started,argv=argv,cwd=str(runtime),elapsed_seconds=elapsed,
        exit_code=result.returncode,stdout_bytes=len(result.stdout),stderr_bytes=len(result.stderr),
        execution_inputs=[dict(role='standalone audit source',path=str(code),sha256=sha(code),size=code.stat().st_size)],
        comparison_input=dict(path=str(REPORT),sha256=sha(REPORT),size=REPORT.stat().st_size),
        source_and_comparison_inputs_before=before,source_and_comparison_inputs_after=after,
        generated_report_bytes=generated.stat().st_size,generated_report_sha256=sha(generated),
        generated_report_and_stdout_byte_equal_to_frozen=True,
        original_audit_executions=1,new_independent_mathematical_implementations=0,
        author_program_or_row_executions=0,LP_or_full_graph_executions=0,
        scope='same historical 13-query local arithmetic audit replayed once; not a new independent review of current author file')
    (runs/'execution.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in {'source_and_comparison_inputs_before','source_and_comparison_inputs_after'}},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
