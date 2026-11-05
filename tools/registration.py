"""Freeze explicit stage-2 outputs and compose independently written ID batches."""
import json
from pathlib import Path
import subprocess
import uuid

from curation import _safe_path, formal_paths, is_formal_path
import research_runtime as runtime


def repository_material_names(root):
    """Include sparse-checkout omissions in the formal-material denominator."""
    root = Path(root).resolve()
    visible = {p.relative_to(root).as_posix() for p in formal_paths(root)}
    top = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=root, capture_output=True, text=True)
    if top.returncode or Path(top.stdout.strip()).resolve() != root:
        # Standalone exported workspaces and the self-contained demonstration
        # have no Git snapshot or sparse index to omit their visible files.
        return visible, 'filesystem-without-own-git-snapshot'
    names = set(visible)
    for args in [('ls-tree', '-r', '--name-only', '-z', 'HEAD'), ('ls-files', '-z')]:
        result = subprocess.run(['git', *args], cwd=root, capture_output=True)
        if result.returncode:
            raise ValueError('Cannot enumerate the actual Git formal-material snapshot')
        names.update(n for n in result.stdout.decode('utf-8').split('\0') if is_formal_path(n))
    return names, 'git-head-and-index'


def require_materialized(root, names):
    missing = [name for name in sorted(names) if not _safe_path(root, name).is_file()]
    if missing:
        raise ValueError('Repository scope has %d unmaterialized formal files; restore the archive files before freezing/checking. Examples: %s' % (len(missing), ', '.join(missing[:5])))


def prepare_inputs(root, output='research/registration/inputs.json', scope='repository', coverage_note=None, paths_file=None):
    """Write the real path/SHA inventory; never infer mathematical objects."""
    if scope not in {'repository', 'partial'}:
        raise ValueError('Explicit repository or partial input scope required')
    supplied = []
    if paths_file:
        supplied = json.loads(_safe_path(root, paths_file).read_text())
        if isinstance(supplied, dict): supplied = supplied.get('materials')
        if not isinstance(supplied, list) or not supplied:
            raise ValueError('paths_file must contain actual selected paths or material references')
    if scope == 'partial' and not supplied:
        raise ValueError('Partial preparation requires an explicit paths_file')
    names, denominator = repository_material_names(root) if scope == 'repository' else (set(), 'explicit-selected-paths')
    extra = {}
    for item in supplied:
        row = {'path': item} if isinstance(item, str) else item
        if not isinstance(row, dict) or not isinstance(row.get('path'), str):
            raise ValueError('Selected materials require a repository-relative path')
        _safe_path(root, row['path'])
        names.add(row['path']); extra[row['path']] = row
    if not names: raise ValueError('No actual formal material was selected')
    require_materialized(root, names)
    rows = []
    for name in sorted(names):
        sha = runtime.digest(_safe_path(root, name).read_bytes())
        if extra.get(name, {}).get('sha256', sha) != sha:
            raise ValueError('Selected material changed: ' + name)
        rows.append({'path': name, 'sha256': sha, **({'catalogue_id': extra[name]['catalogue_id']} if 'catalogue_id' in extra.get(name, {}) else {})})
    data = {'scope': scope, 'coverage_note': coverage_note or 'Actual current formal material bytes; identity and mathematical status are assigned by the registration workers.',
            'inventory_source': denominator, 'materials': rows}
    runtime._write_json(_safe_path(root, output), data)
    return {'status': 'inputs-prepared-local-not-frozen', 'path': output, 'scope': scope, 'materials': len(rows), 'inventory_source': denominator}


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
        actual, denominator = repository_material_names(root)
        require_materialized(root, actual)
        missing = actual - seen
        if missing: raise ValueError('Repository freeze omits %d current formal materials' % len(missing))
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root, capture_output=True, text=True)
    baseline = {'schema': 1, 'scope': source['scope'], 'coverage_note': source['coverage_note'],
                'commit': head.stdout.strip() if head.returncode == 0 else None,
                'materials': sorted(rows, key=lambda row: row['path'])}
    if source['scope'] == 'repository': baseline['inventory_source'] = denominator
    destination = _safe_path(root, output)
    if destination.exists():
        previous = json.loads(destination.read_text())
        if any(previous.get(k) != baseline[k] for k in ('schema', 'scope', 'coverage_note', 'materials')):
            raise ValueError('Frozen baseline exists; publish a new explicit version instead of overwriting it')
        return {'status': 'already-frozen', 'path': output, 'materials': len(rows)}
    runtime._write_json(destination, baseline)
    return {'status': 'frozen-local-not-pushed', 'path': output, 'materials': len(rows), 'scope': baseline['scope']}


def published_batches(root, workflow_run, baseline_ref):
    # Import at use time: the shared queue validates registration receipts via
    # this module.  Its collector is the single authority for done replacements.
    import map_tasks
    run = runtime.identity(workflow_run)
    ctx = {'phase': 'registration', 'run': run,
           'home': 'research/operations/' + run, 'config': {}, 'local': True}
    collected = map_tasks.collect(root, 'registration', ctx=ctx, baseline_ref=baseline_ref)
    return collected['batches']


def merge_material(previous, incoming):
    """Merge read-only support of independent Claims on unchanged material."""
    if previous.get('sha256') != incoming.get('sha256') or not {previous.get('disposition'), incoming.get('disposition')} <= {'objects', 'attachment'}:
        raise ValueError('Conflicting material version or disposition: ' + incoming['path'])
    row = dict(previous)
    row.update(incoming)
    row['disposition'] = 'objects' if 'objects' in {previous['disposition'], incoming['disposition']} else 'attachment'
    row['object_ids'] = list(dict.fromkeys(previous.get('object_ids', []) + incoming.get('object_ids', [])))
    row['reason'] = '\n'.join(dict.fromkeys([previous['reason'], incoming['reason']]))
    return row


def validate_batch(root, record, expected_materials=None, baseline_ref=None):
    """Validate this batch and only the existing owners it explicitly reuses."""
    if record.get('schema') != 2 or record.get('edge_files'):
        raise ValueError('Registration batches use schema 2 and no edge_files')
    if not isinstance(record.get('objects'), list) or not isinstance(record.get('materials'), list):
        raise ValueError('A registration batch needs objects and materials')
    own = {runtime.object_identity(o.get('object_id')): o for o in record['objects']}
    if len(own) != len(record['objects']): raise ValueError('Duplicate mathematical object in one batch')
    if expected_materials is not None:
        expected = {r['path']: r['sha256'] for r in expected_materials}
        actual = {r['path']: r['sha256'] for r in record['materials']}
        if expected != actual or len(actual) != len(record['materials']):
            raise ValueError('Batch must dispose exactly its assigned material versions')
    if baseline_ref is not None:
        baseline = json.loads(runtime.ref_bytes(root, baseline_ref))
        if record.get('baseline', baseline_ref) != baseline_ref:
            raise ValueError('Batch uses another frozen baseline')
        frozen = {r['path']: r['sha256'] for r in baseline['materials']}
        if any(frozen.get(r['path']) != r['sha256'] for r in record['materials']):
            raise ValueError('Batch material is outside its declared frozen input versions')
    referenced = {oid for r in record['materials'] for oid in r.get('object_ids', [])}
    external = referenced - own.keys()
    materials = [dict(r) for r in record['materials']]
    if external:
        canonical = _safe_path(root, runtime.REGISTRY)
        existing = json.loads(canonical.read_text()) if canonical.exists() else {}
        known = {o['object_id']: o for o in existing.get('objects', [])}
        if external - known.keys(): raise ValueError('Unknown existing mathematical owner: ' + ', '.join(sorted(external - known.keys())))
        paths = {r['path']: r for r in materials}
        for oid in sorted(external):
            owner = known[oid]; own[oid] = owner
            body = owner['body']
            if body['path'] not in paths:
                row = {'path': body['path'], 'sha256': body['sha256'], 'disposition': 'objects', 'object_ids': [oid],
                       'reason': 'Read-only existing mathematical owner; not a new batch material'}
                materials.append(row); paths[body['path']] = row
    runtime.load(root, provided={'schema': 2, 'objects': list(own.values()), 'materials': materials, 'edge_files': []})
    return {'objects': len(record['objects']), 'materials': len(record['materials']), 'reused_existing_owners': sorted(external)}


def compose(root, manifest_file, output):
    manifest = json.loads(_safe_path(root, manifest_file).read_text())
    baseline_ref = manifest['baseline']
    runtime.ref_bytes(root, baseline_ref)
    baseline = json.loads(_safe_path(root, baseline_ref['path']).read_text())
    if baseline.get('schema') != 1: raise ValueError('Explicit frozen registration baseline required')
    batches = manifest.get('batches')
    if manifest.get('workflow_run'):
        if batches: raise ValueError('Choose explicit batches or one completed workflow, not both')
        batches = published_batches(root, manifest['workflow_run'], baseline_ref)
    if not isinstance(batches, list) or not batches: raise ValueError('Explicit published batch references required')
    mode = manifest.get('mode', 'full')
    if mode not in {'full', 'incremental'}: raise ValueError('Composition mode is full or incremental')
    existing = {}
    canonical = _safe_path(root, runtime.REGISTRY)
    if canonical.exists(): existing = json.loads(canonical.read_text())
    if mode == 'incremental':
        base = manifest.get('base_registry')
        if not isinstance(base, dict): raise ValueError('Incremental registration binds its exact base_registry reference')
        existing = json.loads(runtime.ref_bytes(root, base))
        if existing.get('schema') != 2: raise ValueError('Incremental registration requires a current v2 registry')
        incorporated = {b['batch_id']: b['record'] for b in existing.get('registration_batches', [])}
        batches = [b for b in batches if incorporated.get(b['batch_id']) != b['record']]
        if not batches: raise ValueError('No new published registration batch after the bound base registry')
    objects = {o['object_id']: o for o in existing.get('objects', [])} if mode == 'incremental' else {}
    materials = {r['path']: r for r in existing.get('materials', [])} if mode == 'incremental' else {}
    batch_ids, seen_objects, seen_materials = set(), set(), set()
    duplicates = []
    for batch in batches:
        batch_id = runtime.identity(batch['batch_id'])
        if batch_id in batch_ids: raise ValueError('Duplicate batch assignment')
        batch_ids.add(batch_id)
        runtime.ref_bytes(root, batch['record'])
        record = json.loads(_safe_path(root, batch['record']['path']).read_text())
        if record.get('schema') != 2 or record.get('edge_files'):
            raise ValueError('Registration batches use schema 2 and do not build stage-3 relations')
        for label, rows, table, key, seen in [('object', record['objects'], objects, 'object_id', seen_objects), ('material', record['materials'], materials, 'path', seen_materials)]:
            for row in rows:
                identity = row[key]
                if identity in table:
                    previous = table[identity]
                    if row == previous:
                        duplicates.append({'kind': label, 'id': identity})
                    elif label == 'material':
                        row = merge_material(previous, row)
                    elif identity in seen or mode != 'incremental':
                        raise ValueError('Conflicting ' + label + ' across batches: ' + identity)
                    elif label == 'object' and row.get('version', 0) <= previous.get('version', 0):
                        raise ValueError('An incrementally changed object needs a new version: ' + identity)
                table[identity] = row
                seen.add(identity)
    retired = dict(existing.get('retired_objects', {})); retired.update(manifest.get('retired_objects', {}))
    if mode == 'incremental':
        for oid in manifest.get('retired_objects', {}): objects.pop(oid, None)
        for row in materials.values():
            if row.get('object_ids'): row['object_ids'] = [oid for oid in row['object_ids'] if oid in objects]
    prior_batches = existing.get('registration_batches', []) if mode == 'incremental' else []
    all_batches = {b['batch_id']: b for b in prior_batches}
    all_batches.update({b['batch_id']: b for b in batches})
    proposed = dict(existing if mode == 'incremental' else {}, schema=2, baseline=baseline_ref,
                objects=[objects[k] for k in sorted(objects)], materials=[materials[k] for k in sorted(materials)],
                edge_files=existing.get('edge_files', []), registration_batches=list(all_batches.values()), retired_objects=retired)
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
        if scope == 'repository':
            current, _ = repository_material_names(root)
            if final: require_materialized(root, current)
            added = sorted(current - frozen.keys())
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
