#!/usr/bin/env python3
"""Check the unfilled entry gate without loading or inventing a gamepoint."""
from hashlib import sha256
from pathlib import Path
import ast
import gzip
import json
import runpy

HERE = Path(__file__).resolve().parent


def main():
    for name in ('build_layer.py', 'fill_fixed_point_template.py', 'project_visible_prefix_rows.py'):
        ast.parse((HERE / name).read_text(), filename=name)
    template_path = HERE / 'fixed_point_feasibility_template.json.gz'
    release_path = HERE / 'main_point_release_template.json'
    before = {p.name: sha256(p.read_bytes()).hexdigest() for p in (template_path, release_path)}
    with gzip.open(template_path, 'rt') as f:
        template = json.load(f)
    release = json.loads(release_path.read_text())
    assert template['point_binding']['old_vector'] is None
    assert release['old_vector'] is None and release['main_release_reference'] is None
    assert template['objective'] is None and template['optimizer_authorization'] is False
    functions = runpy.run_path(str(HERE / 'fill_fixed_point_template.py'))
    rejected = False
    reason = ''
    try:
        functions['bind'](template, release)
    except AssertionError as error:
        rejected, reason = True, str(error)
    assert rejected and reason == 'Main release reference is required'
    assert before == {p.name: sha256(p.read_bytes()).hexdigest() for p in (template_path, release_path)}
    report = {'status': 'PASS', 'syntax_checked_python_entries': 3,
              'unfilled_main_release_rejected': True, 'rejection_reason': reason,
              'point_vector_remains_null': True, 'template_and_release_bytes_unchanged': True,
              'no_synthetic_or_old_gamepoint_used': True, 'no_prepared_fixed_point_file_created': True,
              'optimizer_calls': 0, 'input_sha256': before}
    out = HERE / 'template_entry_verification.json'
    assert not out.exists(), ('refuse_overwrite', str(out))
    out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
