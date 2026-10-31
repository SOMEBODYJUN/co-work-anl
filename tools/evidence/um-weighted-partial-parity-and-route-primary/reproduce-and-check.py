#!/usr/bin/env python3
"""One original-entry rerun plus explicit compressed-P certificates; no CONFIG solver."""
from fractions import Fraction as F
from itertools import product
from math import factorial
from pathlib import Path
import hashlib
import json
import subprocess
import sys


def h(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def actual_certificate(d, s):
    q = 2*s
    X = [(g, a) for g in range(s) for a in (0, 1)]
    labels = [(g, a, b) for g, a in X for b in product((0, 1), repeat=d) if (a+sum(b)) % 2 == 1]
    R = ('root',)
    xm = {x: ('X', *x) for x in X}
    lm = {l: ('L', l[0], l[1], ''.join(map(str, l[2]))) for l in labels}
    zm = {(g, j, bit): ('Z', g, j, bit) for g in range(s) for j in range(d) for bit in (0, 1)}
    # Every token is an original distinct job. A label token has all label-child ends.
    jobs = {('root-unit',): {R: F(1)}}
    assignment = {('root-unit',): R}
    for r, x in enumerate(X):
        jobs[('root-token', r)] = {R: F(1, q), **{xm[y]: F(1) for y in X}}
        assignment[('root-token', r)] = xm[x]
    chosen = {}
    for g, a in X:
        b = ((1,)+(0,)*(d-1)) if a == 0 else ((1,)*d if d % 2 == 0 else (0,)+(1,)*(d-1))
        chosen[g, a] = (g, a, b)
        assert (g, a, b) in lm
        jobs[('X-token', g, a)] = {xm[g, a]: F(1), **{lm[l]: F(1) for l in labels if l[:2] == (g, a)}}
        assignment[('X-token', g, a)] = lm[g, a, b]
    for l in labels:
        g, a, b = l
        resources = [zm[g, j, b[j]] for j in range(d)]
        for r in range(d):
            job = ('label-token', lm[l], r)
            jobs[job] = {lm[l]: F(1, d), **{u: F(1) for u in resources}}
            if l == chosen[g, a] and (d % 2 or r > 0):
                assignment[job] = resources[r]
            else:
                assignment[job] = lm[l]
    assert set(jobs) == set(assignment)
    all_machines = {R, *xm.values(), *lm.values(), *zm.values()}
    loads = {m: F(0) for m in all_machines}
    for j, i in assignment.items():
        assert i in jobs[j]
        loads[i] += jobs[j][i]
    target = 1+F(1, d) if d % 2 == 0 else F(1)
    assert max(loads.values()) == target
    S = s*2**d
    finite = sum(map(len, jobs.values()))
    assert len(all_machines) == 1+2*s+S+2*d*s
    assert len(jobs) == 1+4*s+d*S
    assert finite == 1+q*(1+q)+q*(1+2**(d-1))+d*S*(1+d)
    assert all(loads[xm[x]] == 1 for x in X) and loads[R] == 1
    return {"d": d, "s": s, "parity": "even" if d % 2 == 0 else "odd",
            "machines": len(all_machines), "jobs": len(jobs), "finite_entries": finite,
            "peak_of_complete_assignment": str(target), "all_jobs_once_original_legal_end": True,
            "one_X_token_per_choice_vertex": True, "no_unit_job_per_X_label_arc": True,
            "selected_label_count": len(chosen), "resource_peak": str(max(loads[z] for z in zm.values())),
            "proves_OPT_by_enumeration": False,
            "scope": "complete compressed-P actual certificate only; lower bound from quota/tree proof"}


def main():
    out = Path(sys.argv[1]);out.mkdir(parents=True, exist_ok=False)
    (out/'original-entry-cwd').mkdir()
    root = Path(__file__).resolve().parent
    program = root/'support/parity_block_check.py'
    assert h(program) == '70be5e590ff81e65d4cda932c8b5a562a258d92dfa9f5bc55925baa599e786e5'
    result = subprocess.run([sys.executable, str(program)], cwd=out/'original-entry-cwd',
                            text=True, capture_output=True, check=False)
    (out/'stdout.txt').write_text(result.stdout)
    (out/'stderr.txt').write_text(result.stderr)
    assert result.returncode == 0 and result.stderr == ''
    expected = []
    for d in (2, 4, 6):
        for s in (1, 2):
            vals = [2*s]*(d-1)+[s]
            expected.append(f'd={d},s={s}: nu={vals}, b={F(d-1,d)}, OPT={1+F(1,d)}')
    assert result.stdout.splitlines() == expected
    eta, a, c = F(1, 100000), F(79, 125), F(283, 1000)
    bound = a*(1-eta)+(1-a*(1-eta))*c*(F(1, 3)-eta)
    assert bound == F(2500154630232929,3750000000000000)
    assert bound-F(2, 3) == F(154630232929,3750000000000000) > 0
    # Positive Taylor partial sums certify the two proof constants without floating exp.
    e_lower = sum((F(1, factorial(k)) for k in range(7)), F(0))
    e_third_lower = sum((F(1, 3**k*factorial(k)) for k in range(5)), F(0))
    assert e_lower > 1/(1-a) and e_third_lower > 1/(1-c)
    certificates = [actual_certificate(d, s) for d in (2, 4, 6) for s in (1, 2)]
    certificates += [actual_certificate(d, 1) for d in (3, 5)]
    report = {"status": "original finite stdout reproduced; exact constants and eight complete compressed-P certificates passed",
              "wrapper_runs": 1, "archived_entry_runs": 1, "archived_entry_sha256": h(program),
              "wrapper_sha256": h(Path(__file__)), "python": sys.version, "arithmetic": "standard-library Fraction/integer sets",
              "original_dependencies": ["itertools.product", "itertools.combinations", "fractions.Fraction"],
              "original_entry_imports_no_project_modules": True, "original_entry_code_lines_actually_read": 39,
              "original_returncode": result.returncode, "original_stdout_matches_six_source_note_lines": True,
              "original_finite_scope": "resource-subset nu_t DFS for d2,4,6 and s1,2; not full scheduling enumeration",
              "constants": {"eta": str(eta), "a": str(a), "c": str(c), "coverage_bound": str(bound),
                            "margin_over_two_thirds": str(bound-F(2, 3)),
                            "e_lower_sum_0_to_6": str(e_lower), "e_one_third_lower_sum_0_to_4": str(e_third_lower)},
              "complete_ordinary_UM_certificates": certificates,
              "limits": ["No CONFIG solver or weak-separation/primal recovery implemented",
                         "No all-schedule enumeration or general theorem established by these eight certificates",
                         "No source hardness, hard-image membership, outside novelty or independent full-proof maturation claim"]}
    (out/'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    (out/'command.json').write_text(json.dumps({"wrapper_argv": sys.argv, "original_argv": [sys.executable, str(program)],
               "fresh_output_directory": str(out.resolve()), "original_cwd": str((out/'original-entry-cwd').resolve()),
               "output_dependencies": "no files consumed or produced by original besides captured stdout; all inputs fixed in source"},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({"status": report['status'], "original_returncode": result.returncode,
                      "archived_entry_runs": 1, "ordinary_UM_certificates": len(certificates), "output": str(out.resolve())},ensure_ascii=False))


if __name__ == '__main__':
    main()
