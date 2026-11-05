"""Freeze explicit stage-2 outputs and compose independently written ID batches."""
import json
import re
import subprocess
import uuid
from pathlib import PurePosixPath

from curation import _safe_path, formal_paths
import research_runtime as runtime


def freeze(root, inputs_file, output):
    source = json.loads(_safe_path(root, inputs_file).read_text())
    runtime.nonempty(source, ['coverage_note'])
    if source.get('scope') not in {'repository', 'partial'} or not isinstance(source.get('materials'), list) or not source['materials']:
        raise ValueError('Declare repository/partial scope and a nonempty list of actual stage-2 output versions')
    rows = []
    seen = set()
    for row in source['materials']:
        ref = {k: row[k] for k in ('path', 'sha256')}
        runtime.ref_bytes(root, ref)
        if row['path'] in seen: raise ValueError('Duplicate frozen material')
        seen.add(row['path'])
        rows.append(dict(ref, **({'catalogue_id': row['catalogue_id']} if 'catalogue_id' in row else {})))
    if source['scope'] == 'repository':
        missing = {p.relative_to(root).as_posix() for p in formal_paths(root)} - seen
        if missing: raise ValueError('Repository freeze omits %d current formal materials' % len(missing))
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True)
    if head.returncode:
        raise ValueError('Cannot freeze inputs without a committed repository HEAD')
    commit = head.stdout.strip()
    for row in rows:
        path = row['path']
        exists = subprocess.run(['git', 'cat-file', '-e', f'{commit}:{path}'], cwd=root, capture_output=True)
        if exists.returncode:
            raise ValueError('Frozen material is not present in committed HEAD: ' + path)
        blob = subprocess.run(['git', 'show', f'{commit}:{path}'], cwd=root, capture_output=True)
        if blob.returncode or runtime.digest(blob.stdout) != row['sha256']:
            raise ValueError('Frozen material differs from committed HEAD: ' + path)
    baseline = {'schema': 1, 'scope': source['scope'], 'coverage_note': source['coverage_note'],
                'commit': commit,
                'materials': sorted(rows, key=lambda row: row['path'])}
    destination = _safe_path(root, output)
    if destination.exists():
        previous = json.loads(destination.read_text())
        if any(previous.get(k) != baseline[k] for k in ('schema', 'scope', 'coverage_note', 'materials')):
            raise ValueError('Frozen baseline exists; publish a new explicit version instead of overwriting it')
        return {'status': 'already-frozen', 'path': output, 'materials': len(rows)}
    runtime._write_json(destination, baseline)
    return {'status': 'frozen-local-not-pushed', 'path': output, 'materials': len(rows), 'scope': baseline['scope']}


def compose(root, manifest_file, output):
    manifest = json.loads(_safe_path(root, manifest_file).read_text())
    baseline_ref = manifest['baseline']
    runtime.ref_bytes(root, baseline_ref)
    baseline = json.loads(_safe_path(root, baseline_ref['path']).read_text())
    if baseline.get('schema') != 1: raise ValueError('Explicit frozen registration baseline required')
    if not isinstance(manifest.get('batches'), list) or not manifest['batches']: raise ValueError('Explicit published batch references required')
    assignment_ref = manifest.get('assignments')
    if not isinstance(assignment_ref, dict): raise ValueError('Compose manifest must pin the published assignments file')
    runtime.ref_bytes(root, assignment_ref)
    assignments = json.loads(_safe_path(root, assignment_ref['path']).read_text())
    check_assignments(root, assignment_ref['path'])
    assignment_rows = {row['batch_id']: row for row in assignments['assignments']}
    objects, materials, batch_ids = {}, {}, set()
    duplicates = []
    for batch in manifest['batches']:
        batch_id = runtime.identity(batch['batch_id'])
        if batch_id in batch_ids: raise ValueError('Duplicate batch assignment')
        batch_ids.add(batch_id)
        assigned = assignment_rows.get(batch_id)
        if not assigned: raise ValueError('Manifest batch is not in published assignments: ' + batch_id)
        if batch['record']['path'] != assigned['write_path']:
            raise ValueError('Batch record path does not match its assignment: ' + batch_id)
        runtime.ref_bytes(root, batch['record'])
        record = json.loads(_safe_path(root, batch['record']['path']).read_text())
        if record.get('schema') != 2 or record.get('edge_files'):
            raise ValueError('Registration batches use schema 2 and do not build stage-3 relations')
        record_paths = {row['path'] for row in record.get('materials', [])}
        if record_paths != set(assigned['material_paths']):
            raise ValueError('Batch materials do not match its published assignment: ' + batch_id)
        for label, rows, table, key in [('object', record['objects'], objects, 'object_id'), ('material', record['materials'], materials, 'path')]:
            for row in rows:
                identity = row[key]
                if identity in table:
                    if row != table[identity]: raise ValueError('Conflicting ' + label + ' across batches: ' + identity)
                    duplicates.append({'kind': label, 'id': identity})
                table[identity] = row
    proposed = {'schema': 2, 'baseline': baseline_ref, 'objects': [objects[k] for k in sorted(objects)],
                'materials': [materials[k] for k in sorted(materials)], 'edge_files': [],
                'registration_batches': manifest['batches'], 'retired_objects': manifest.get('retired_objects', {})}
    runtime.load(root, provided=proposed)
    destination = _safe_path(root, output)
    if destination == _safe_path(root, runtime.REGISTRY):
        raise ValueError('Compose a candidate; only the integration Boss registers the canonical table')
    runtime._write_json(destination, proposed)
    return {'status': 'composed-local-not-pushed', 'path': output, 'objects': len(objects), 'materials': len(materials), 'identical_duplicates': duplicates}


def check(root, registry=runtime.REGISTRY, final=False):
    data, objects = runtime.load(root, registry)
    rows = {row['path']: row for row in data['materials']}
    pending = [row['path'] for row in rows.values() if row['disposition'] == 'needs-decision']
    baseline_ref = data.get('baseline')
    missing, added = [], []
    scope = 'unfrozen'
    if baseline_ref:
        baseline = json.loads(runtime.ref_bytes(root, baseline_ref))
        if baseline.get('schema') != 1: raise ValueError('Invalid registration baseline')
        scope = baseline['scope']
        frozen = {row['path']: row for row in baseline['materials']}
        for name, row in frozen.items():
            runtime.ref_bytes(root, {k: row[k] for k in ('path', 'sha256')})
            if name not in rows: missing.append(name)
            elif rows[name]['sha256'] != row['sha256']: raise ValueError('Registration changed a frozen material version: ' + name)
        if scope == 'repository': added = sorted({p.relative_to(root).as_posix() for p in formal_paths(root)} - frozen.keys())
    if final and (not baseline_ref or scope != 'repository' or missing or added or pending):
        raise ValueError('Registration coverage incomplete: frozen repository scope required; %d missing, %d new formal paths, %d pending' % (len(missing), len(added), len(pending)))
    return {'status': 'registration-complete-declared-not-a-truth-verdict' if final else 'registration-partial',
            'objects': len(objects), 'materials': len(rows), 'scope': scope,
            'missing_materials': missing, 'new_formal_paths': added, 'pending_materials': pending,
            'graph_required': False}


def new_ids(count):
    if not 1 <= count <= 1000: raise ValueError('Request 1..1000 explicitly identified mathematical objects')
    return {'object_ids': ['M-' + uuid.uuid4().hex for _ in range(count)],
            'instruction': 'Assign once in your batch and checkpoint. Preserve existing object IDs; do not allocate an ID per file or per log.'}


def check_assignments(root, assignment_file):
    """Validate a pre-split 2.5.3 batch table before any Boss starts."""
    data = json.loads(_safe_path(root, assignment_file).read_text())
    if data.get('schema') != 1 or not isinstance(data.get('assignments'), list) or not data['assignments']:
        raise ValueError('Assignments need schema 1 and a nonempty assignments list')
    runtime.ref_bytes(root, data['baseline'])
    baseline = json.loads(runtime.ref_bytes(root, data['baseline']))
    frozen = {row['path'] for row in baseline.get('materials', [])}
    batches, owners, materials, writes = set(), set(), set(), set()
    for row in data['assignments']:
        if set(row) != {'batch_id', 'owner', 'material_paths', 'write_path'}:
            raise ValueError('Each assignment needs batch_id, owner, material_paths and write_path')
        batch_id = runtime.identity(row['batch_id'])
        if batch_id in batches: raise ValueError('Duplicate batch assignment: ' + batch_id)
        batches.add(batch_id)
        if not isinstance(row['owner'], str) or not re.fullmatch(r'Boss[1-9][0-9]*', row['owner']):
            raise ValueError('Assignment owner must be an explicit Boss number')
        owners.add(row['owner'])
        paths = row['material_paths']
        runtime.strings(paths, 'material_paths', True)
        if materials.intersection(paths): raise ValueError('Material path assigned twice')
        if any(path not in frozen for path in paths): raise ValueError('Assignment material is outside the frozen baseline')
        materials.update(paths)
        write_path = row['write_path']
        if write_path in writes or not write_path.startswith('research/registration/batches/') or not write_path.endswith('.json'):
            raise ValueError('Batch write paths must be unique under research/registration/batches')
        writes.add(write_path)
    if materials != frozen:
        raise ValueError('Assignments must cover every frozen material exactly once')
    return {'status': 'assignments-valid-not-a-mathematical-verdict', 'batches': len(batches),
            'owners': sorted(owners), 'materials': len(materials)}


def draft_assignments(root, baseline_file, owners, output, batch_size=80):
    """Create a deterministic scheduling draft; a Boss must review it before publishing."""
    baseline_path = _safe_path(root, baseline_file)
    baseline = json.loads(baseline_path.read_text())
    if baseline.get('schema') != 1 or not isinstance(baseline.get('materials'), list) or not baseline['materials']:
        raise ValueError('Draft assignments need a frozen baseline')
    if not isinstance(owners, list) or not owners:
        raise ValueError('At least one explicit Boss owner is required')
    for owner in owners:
        if not isinstance(owner, str) or not re.fullmatch(r'Boss[1-9][0-9]*', owner):
            raise ValueError('Assignment owner must be an explicit Boss number')
    if not isinstance(batch_size, int) or batch_size < 1:
        raise ValueError('Batch size must be positive')
    destination = _safe_path(root, output)
    if destination.exists(): raise ValueError('Refuse to overwrite an assignment draft')
    groups = {}
    for row in baseline['materials']:
        parts = PurePosixPath(row['path']).parts
        group = '/'.join(parts[:2]) if len(parts) >= 2 and parts[0] == 'archives' else parts[0]
        groups.setdefault(group, []).append(row['path'])
    chunks = []
    for group in sorted(groups):
        paths = sorted(groups[group])
        for offset in range(0, len(paths), batch_size): chunks.append(paths[offset:offset + batch_size])
    assignments = [{'batch_id': f'batch-{i:04d}', 'owner': owners[(i - 1) % len(owners)],
                   'material_paths': paths, 'write_path': f'research/registration/batches/batch-{i:04d}.json'}
                   for i, paths in enumerate(chunks, 1)]
    result = {'schema': 1, 'draft': True,
              'baseline': {'path': baseline_file, 'sha256': runtime.digest(baseline_path.read_bytes())},
              'grouping': 'archive-then-batch', 'batch_size': batch_size, 'assignments': assignments}
    runtime._write_json(destination, result)
    return {'status': 'assignments-draft-local-not-pushed', 'path': output, 'batches': len(assignments),
            'materials': sum(len(row['material_paths']) for row in assignments), 'owners': owners,
            'review_required': True}
