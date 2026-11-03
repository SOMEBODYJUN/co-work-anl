"""Freeze explicit stage-2 outputs and compose independently written ID batches."""
import json
import subprocess
import uuid

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
    baseline = {'schema': 1, 'scope': source['scope'], 'coverage_note': source['coverage_note'],
                'commit': head.stdout.strip() if head.returncode == 0 else None,
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
    objects, materials, batch_ids = {}, {}, set()
    duplicates = []
    for batch in manifest['batches']:
        batch_id = runtime.identity(batch['batch_id'])
        if batch_id in batch_ids: raise ValueError('Duplicate batch assignment')
        batch_ids.add(batch_id)
        runtime.ref_bytes(root, batch['record'])
        record = json.loads(_safe_path(root, batch['record']['path']).read_text())
        if record.get('schema') != 2 or record.get('edge_files'):
            raise ValueError('Registration batches use schema 2 and do not build stage-3 relations')
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
