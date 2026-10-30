#!/usr/bin/env python3
"""Execute the two unchanged canonical programs in isolated fixture trees.

This is a new curation harness. TeX binaries and template assets are explicit
non-production fixtures; no real PDF is compiled or author class certified.
The conversion uses the actually preserved current structural TeX and Bib.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cache', type=Path, required=True)
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--work', type=Path, required=True)
parser.add_argument('--evidence', type=Path, required=True)
args = parser.parse_args()
args.work.mkdir(parents=True, exist_ok=False)
args.evidence.mkdir(parents=True, exist_ok=True)
assignment = args.cache / 'next8-assignment.json'
if assignment.exists():
    sources = json.loads(assignment.read_text())['cohort_pair_next']
else:
    # The preserved original/ tree plus the adjacent source manifest forms a
    # self-contained replay input; the transient orchestration cache is optional.
    sources = json.loads((Path(__file__).resolve().parent / 'source-manifest.json').read_text())['sources']
for item in sources:
    data = (args.cache / item['path']).read_bytes()
    assert len(data) == item['size'] and sha256(data).hexdigest() == item['sha256']

BUILD = args.cache / 'research/manuscripts/build.py'
CONVERT = args.cache / 'research/manuscripts/prepare_mor.py'
CURRENT = args.repo / 'archives/weighted-congestion/papers/structural-methods-current'
TEX = (CURRENT / 'structural_methods_article.tex').read_bytes()
BIB = (CURRENT / 'structural_methods_article.bib').read_bytes()
old_pdf = b'FIXTURE OLD OUTPUT; NOT A PDF\n'


def digest(b):
    return sha256(b).hexdigest()


def make_repo(name):
    root = args.work / name / 'repository'
    scripts = root / 'research/manuscripts'
    scripts.mkdir(parents=True)
    shutil.copy2(BUILD, scripts / 'build.py')
    shutil.copy2(CONVERT, scripts / 'prepare_mor.py')
    paths = [scripts / 'shared_catalog/main.tex', scripts / 'multiple_facilities/main.tex',
             root / 'research/current/weighted_congestion/structural_reconstruction/structural_methods_article.tex']
    for i, p in enumerate(paths):
        p.parent.mkdir(parents=True)
        p.write_bytes(TEX if i == 2 else b'% explicit non-mathematical build fixture\n')
        p.with_suffix('.pdf').write_bytes(old_pdf)
    paths[2].with_suffix('.bib').write_bytes(BIB)
    return root, scripts, paths


shim = args.work / 'command-fixtures'
shim.mkdir()
stub = r'''#!/usr/bin/env python3
import os
from pathlib import Path
import sys
name = Path(sys.argv[0]).name
mode = os.environ.get('MB_FIXTURE_MODE', 'clean')
if name == 'kpsewhich':
    if mode != 'format': print('/explicit-fixture/pdflatex.fmt')
elif name == 'pdftex':
    out = Path(next(a.split('=', 1)[1] for a in sys.argv if a.startswith('-output-directory=')))
    (out / 'pdflatex.fmt').write_text('EXPLICIT NON-PRODUCTION FORMAT FIXTURE\n')
    print('fixture format generated')
elif name == 'latexmk':
    if mode == 'compile_fail' or (mode == 'partial_fail' and Path.cwd().name == 'multiple_facilities'):
        print('fixture compiler failure; no real TeX was invoked')
        raise SystemExit(23)
    out = Path(next(a.split('=', 1)[1] for a in sys.argv if a.startswith('-outdir=')))
    stem = Path(sys.argv[-1]).stem
    message = {'warning': 'LaTeX Warning: explicit fixture warning',
               'overfull': 'Overfull \\hbox (1pt too wide)',
               'undefined': 'Undefined fixture diagnostic',
               'underfull': 'Underfull \\vbox (badness 10000)'}
    if mode != 'missing_log': (out / (stem + '.log')).write_text(message.get(mode, 'clean fixture log') + '\n')
    (out / (stem + '.pdf')).write_bytes(b'FIXTURE COMPILED OUTPUT; NOT A PDF\n')
    print('fixture latexmk completed; no real PDF compiled')
'''
for name in ('kpsewhich', 'pdftex', 'latexmk'):
    p = shim / name
    p.write_text(stub)
    p.chmod(0o755)


def execute(command, cwd, mode='clean'):
    env = os.environ.copy()
    env['PATH'] = str(shim) + os.pathsep + env.get('PATH', '')
    env['MB_FIXTURE_MODE'] = mode
    run = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True)
    return {'returncode': run.returncode, 'stdout': run.stdout, 'stderr': run.stderr}


build_runs = []
cases = [('explicit_all', 'clean', ['shared', 'multiple', 'congestion']),
         ('default_no_args', 'clean', []), ('help', 'clean', ['--help']),
         ('invalid_key', 'clean', ['not-a-paper']), ('format_branch', 'format', ['congestion']),
         ('warning_gate', 'warning', ['congestion']), ('overfull_gate', 'overfull', ['congestion']),
         ('undefined_gate', 'undefined', ['congestion']), ('underfull_allowed', 'underfull', ['congestion']),
         ('compiler_failure', 'compile_fail', ['congestion']), ('missing_log', 'missing_log', ['congestion']),
         ('partial_batch', 'partial_fail', ['shared', 'multiple', 'congestion'])]
for name, mode, keys in cases:
    root, scripts, paths = make_repo('build-' + name)
    source_before = [digest(p.read_bytes()) for p in paths]
    result = execute([sys.executable, str(scripts / 'build.py'), *keys], root, mode)
    result.update({'case': name, 'mode': mode, 'keys': keys,
                   'pdf_copied': [p.with_suffix('.pdf').read_bytes() != old_pdf for p in paths],
                   'source_unchanged': source_before == [digest(p.read_bytes()) for p in paths],
                   'format_log_created': (paths[2].parent / '.build/format-build.txt').exists()})
    assert result['source_unchanged']
    build_runs.append(result)

by_name = {x['case']: x for x in build_runs}
assert by_name['explicit_all']['returncode'] == 0 and by_name['explicit_all']['pdf_copied'] == [True]*3
assert by_name['help']['returncode'] == 0
assert by_name['invalid_key']['returncode'] == 2
assert by_name['format_branch']['returncode'] == 0
assert by_name['underfull_allowed']['returncode'] == 0
for name in ('warning_gate', 'overfull_gate', 'undefined_gate', 'compiler_failure', 'missing_log'):
    assert by_name[name]['returncode'] != 0 and by_name[name]['pdf_copied'] == [False]*3
assert by_name['partial_batch']['returncode'] != 0 and by_name['partial_batch']['pdf_copied'] == [True, False, False]


def template_fixtures(parent, omit=None):
    p = parent / 'template-fixture'
    p.mkdir()
    for name in ('informs4.cls', 'eqndefns-left.sty', 'informs2014.bst', 'informs_Logo.pdf'):
        if name != omit:
            (p / name).write_bytes(('EXPLICIT NON-OFFICIAL COPY FIXTURE: ' + name + '\n').encode())
    return p


conversion_runs = []
for name in ('success', 'inside_root', 'root_itself', 'missing_template', 'missing_appendix'):
    root, scripts, paths = make_repo('convert-' + name)
    template = template_fixtures(root.parent, 'eqndefns-left.sty' if name == 'missing_template' else None)
    if name == 'missing_appendix':
        paths[2].write_bytes(TEX.replace(b'\\appendix\n', b'% fixture removed expected appendix marker\n'))
    out = root.parent / 'output'
    if name == 'inside_root': out = root / 'private-output'
    if name == 'root_itself': out = root
    result = execute([sys.executable, str(scripts / 'prepare_mor.py'), str(template), str(out)], root)
    result.update({'case': name, 'output_created': out.exists(),
                   'files_in_output': sorted(p.name for p in out.iterdir() if p.is_file()) if out.exists() else []})
    if name == 'success':
        converted = (out / 'main.tex').read_bytes()
        result['main_tex_sha256'] = digest(converted)
        result['matches_historically_reported_private_TeX_hash'] = digest(converted) == '0729d63bd9fb0e7f5d47c02f0a41461b5c983da37f2e0a7493941aba5ec2e422'
        result['bib_unchanged'] = (out / 'main.bib').read_bytes() == BIB
        result['template_fixture_copies_unchanged'] = all((out/p.name).read_bytes() == p.read_bytes() for p in template.iterdir())
        # Keep the generated MOR source in the external work tree. Only its
        # hashes and comparisons enter the curation evidence directory.
        result['generated_source_kept_in_external_work_tree'] = str(out / 'main.tex')
        text, before = converted.decode(), TEX.decode()
        def formal(s):
            return re.findall(r'\\begin\{(lemma|theorem|corollary|proposition)\}(.*?)\\end\{\1\}', s, re.S)
        def proofs(s):
            return [re.sub(r'\s+', '', x.replace(r'\Halmos', '')) for x in
                    re.findall(r'\\begin\{proof\}[^\n]*\n(.*?)\\end\{proof\}', s, re.S)]
        result['formal_statements_count'] = len(formal(before))
        result['formal_statements_byte_equal'] = formal(before) == formal(text)
        result['proof_count'] = len(proofs(before))
        result['proof_arguments_equal_after_heading_and_Halmos_normalization'] = proofs(before) == proofs(text)
        result['labels_preserved_order'] = re.findall(r'\\label\{([^}]+)\}', before) == re.findall(r'\\label\{([^}]+)\}', text)
        def displays(s):
            return [(m.group(1), m.group(2)) for m in re.finditer(r'\\begin\{(equation|align)\}(.*?)\\end\{\1\}', s, re.S)] + [('bracket', m.group(1)) for m in re.finditer(r'(?<!\\)\\\[(.*?)\\\]', s, re.S)]
        def normalized_math(s):
            s = re.sub(r'\\(?:begin|end)\{aligned\}', '', s)
            s = s.replace('&', '').replace('\\\\', '')
            s = re.sub(r'\\(?:qquad|quad|,|;|!)', '', s)
            return re.sub(r'\s+', '', s)
        old, new = displays(before), displays(text)
        result['display_count'] = [len(old), len(new)]
        result['display_raw_differences'] = [i for i, (x,y) in enumerate(zip(old,new)) if x != y]
        result['display_math_equal_after_documented_alignment_normalization'] = len(old) == len(new) and all(x[0] == y[0] and normalized_math(x[1]) == normalized_math(y[1]) for x,y in zip(old,new))
        result['proof_headings_for_INFORMS'] = {'optional_proof_headings_remaining': len(re.findall(r'\\begin\{proof\}\[', text)),
                                                'Halmos_count': text.count(r'\Halmos'),
                                                'APPENDICES_begin': text.count(r'\begin{APPENDICES}'),
                                                'APPENDICES_end': text.count(r'\end{APPENDICES}')}
        result['intro_disclosure_removed'] = r'\subsection{Research process and AI assistance}' not in text
        result['relocated_disclosure_present'] = r'\subsection*{Use of generative AI in the research process}' in text
        assert result['returncode'] == 0 and result['bib_unchanged'] and result['template_fixture_copies_unchanged']
        assert result['formal_statements_count'] == result['proof_count'] == 24
        assert result['formal_statements_byte_equal'] and result['proof_arguments_equal_after_heading_and_Halmos_normalization']
        assert result['labels_preserved_order'] and result['display_math_equal_after_documented_alignment_normalization']
        assert result['display_count'] == [119,119]
    elif name in ('inside_root', 'root_itself'):
        assert result['returncode'] == 2
    elif name == 'missing_template':
        assert result['returncode'] != 0 and result['files_in_output'] == ['informs4.cls']
    elif name == 'missing_appendix':
        text = (out / 'main.tex').read_text()
        result['APPENDICES_begin'] = text.count(r'\begin{APPENDICES}')
        result['APPENDICES_end'] = text.count(r'\end{APPENDICES}')
        assert result['returncode'] == 0 and result['APPENDICES_begin'] == 0 and result['APPENDICES_end'] == 1
    conversion_runs.append(result)

report = {'scope': 'Actual unchanged canonical program execution with explicitly non-production command/template fixtures; no TeX compilation or external/private PDF inspection.',
          'canonical_sources_verified': len(sources),
          'python': sys.version.split()[0],
          'texlive_tree_exists': Path('/usr/share/texlive/texmf-dist').is_dir(),
          'build_runs': build_runs, 'conversion_runs': conversion_runs,
          'current_real_source_unchanged': digest((CURRENT / 'structural_methods_article.tex').read_bytes()) == digest(TEX),
          'current_real_bib_unchanged': digest((CURRENT / 'structural_methods_article.bib').read_bytes()) == digest(BIB)}
(args.evidence / 'interface-replay.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'build_cases': len(build_runs), 'default_no_args': by_name['default_no_args'],
                  'conversion_cases': len(conversion_runs), 'successful_conversion': conversion_runs[0]}, ensure_ascii=False, indent=2))
