"""Freeze explicit stage-2 outputs and compose independently written ID batches."""
import json
import math
import re
from pathlib import Path, PurePosixPath
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


def prepare_inputs(root, output='research/registration/inputs.json', scope='repository', coverage_note=None, paths_file=None, paths=None):
    """Write the real path/SHA inventory; never infer mathematical objects."""
    if scope not in {'repository', 'partial'}:
        raise ValueError('Explicit repository or partial input scope required')
    supplied = list(paths or [])
    if paths_file:
        loaded = json.loads(_safe_path(root, paths_file).read_text())
        if isinstance(loaded, dict): loaded = loaded.get('materials')
        if not isinstance(loaded, list) or not loaded:
            raise ValueError('paths_file must contain actual selected paths or material references')
        supplied.extend(loaded)
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
    destination = _safe_path(root, output)
    if destination.exists():
        previous = json.loads(destination.read_text())
        if previous != data:
            raise ValueError('Inputs manifest exists with different bytes; create an explicit new filename')
        return {'status': 'already-prepared', 'path': output, 'scope': scope, 'materials': len(rows), 'inventory_source': denominator}
    runtime._write_json(destination, data)
    return {'status': 'inputs-prepared-local-not-frozen', 'path': output, 'scope': scope, 'materials': len(rows), 'inventory_source': denominator}


def committed_materials(root, rows):
    """Bind a real repository HEAD and verify its exact material blobs in one batch."""
    root = Path(root).resolve()
    head = subprocess.run(['git', 'rev-parse', '--show-toplevel', 'HEAD'], cwd=root, capture_output=True, text=True)
    lines = head.stdout.splitlines()
    if head.returncode or len(lines) != 2 or Path(lines[0]).resolve() != root:
        raise ValueError("Cannot freeze inputs without this repository's committed HEAD")
    commit = lines[1]
    tree = subprocess.run(['git', 'ls-tree', '-r', '-z', commit], cwd=root, capture_output=True)
    if tree.returncode: raise ValueError('Cannot read committed material paths')
    blobs = {}
    for entry in tree.stdout.split(b'\0'):
        if not entry: continue
        metadata, name = entry.split(b'\t', 1)
        _, kind, oid = metadata.split()
        if kind == b'blob': blobs[name.decode('utf-8')] = oid.decode('ascii')
    for row in rows:
        if row['path'] not in blobs:
            raise ValueError('Frozen material is not present in committed HEAD: ' + row['path'])
    requested = ''.join(blobs[row['path']] + '\n' for row in rows).encode('ascii')
    result = subprocess.run(['git', 'cat-file', '--batch'], cwd=root, input=requested, capture_output=True)
    if result.returncode: raise ValueError('Cannot read committed material bytes')
    offset = 0
    for row in rows:
        end = result.stdout.find(b'\n', offset)
        header = result.stdout[offset:end].split()
        if end < 0 or len(header) != 3 or header[1] != b'blob':
            raise ValueError('Cannot read committed material: ' + row['path'])
        size = int(header[2]); content = result.stdout[end + 1:end + 1 + size]
        if runtime.digest(content) != row['sha256']:
            raise ValueError('Frozen material differs from committed HEAD: ' + row['path'])
        offset = end + 2 + size
    if offset != len(result.stdout): raise ValueError('Invalid committed material response')
    return commit


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
    commit = committed_materials(root, rows)
    baseline = {'schema': 1, 'scope': source['scope'], 'coverage_note': source['coverage_note'],
                'commit': commit,
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


def validate_batch(root, record, expected_materials=None, baseline_ref=None, peer_objects=None):
    """Validate one batch and the exact published owners it explicitly reuses.

    The queue may supply owners from the other already-pushed records in one
    atomic delivery. They are read-only validation context, not extra objects
    or material assignments in this batch.
    """
    if record.get('schema') != 2 or record.get('edge_files'):
        raise ValueError('Registration batches use schema 2 and no edge_files')
    if not isinstance(record.get('objects'), list) or not isinstance(record.get('materials'), list):
        raise ValueError('A registration batch needs objects and materials')
    own = {runtime.object_identity(o.get('object_id')): o for o in record['objects']}
    if len(own) != len(record['objects']): raise ValueError('Duplicate mathematical object in one batch')
    peers = {} if peer_objects is None else peer_objects
    if not isinstance(peers, dict): raise ValueError('Published peer owners must be an object-ID mapping')
    for oid, owner in peers.items():
        if runtime.object_identity(oid) != owner.get('object_id'):
            raise ValueError('Published peer owner identity differs from its key')
        if oid in own and own[oid] != owner:
            raise ValueError('Conflicting mathematical owner across completion batches: ' + oid)
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
        known = dict(peers)
        if external - known.keys():
            canonical = _safe_path(root, runtime.REGISTRY)
            existing = json.loads(canonical.read_text()) if canonical.exists() else {}
            known.update({o['object_id']: o for o in existing.get('objects', []) if o['object_id'] not in known})
        if external - known.keys(): raise ValueError('Unknown existing mathematical owner: ' + ', '.join(sorted(external - known.keys())))
        paths = {r['path']: r for r in materials}
        for oid in sorted(external):
            owner = known[oid]; own[oid] = owner
            body = owner['body']
            if body['path'] not in paths:
                row = {'path': body['path'], 'sha256': body['sha256'], 'disposition': 'objects', 'object_ids': [oid],
                       'reason': 'Read-only existing mathematical owner; not a new batch material'}
                materials.append(row); paths[body['path']] = row
            else:
                row = paths[body['path']]
                if row['sha256'] != body['sha256'] or row.get('disposition') != 'objects':
                    raise ValueError('A reused mathematical owner needs its exact body declared as mathematics: ' + oid)
                row['object_ids'] = list(dict.fromkeys(row.get('object_ids', []) + [oid]))
    runtime.load(root, provided={'schema': 2, 'objects': list(own.values()), 'materials': materials, 'edge_files': []})
    return {'objects': len(record['objects']), 'materials': len(record['materials']),
            'reused_existing_owners': sorted(external - peers.keys()),
            'reused_published_group_owners': sorted(external & peers.keys())}


def compose(root, manifest_file, output):
    manifest = json.loads(_safe_path(root, manifest_file).read_text())
    baseline_ref = manifest['baseline']
    runtime.ref_bytes(root, baseline_ref)
    baseline = json.loads(_safe_path(root, baseline_ref['path']).read_text())
    if baseline.get('schema') != 1: raise ValueError('Explicit frozen registration baseline required')
    frozen = {row['path']: row['sha256'] for row in baseline['materials']}
    batches = manifest.get('batches')
    if manifest.get('workflow_run'):
        if batches: raise ValueError('Choose explicit batches or one completed workflow, not both')
        batches = published_batches(root, manifest['workflow_run'], baseline_ref)
    if not isinstance(batches, list) or not batches: raise ValueError('Explicit published batch references required')
    assignment_rows = None
    if 'assignments' in manifest:
        assignment_ref = manifest['assignments']
        if not isinstance(assignment_ref, dict):
            raise ValueError('An explicitly selected assignments table needs a path/SHA reference')
        assignments = json.loads(runtime.ref_bytes(root, assignment_ref))
        check_assignments(root, assignment_ref['path'])
        if assignments['baseline'] != baseline_ref:
            raise ValueError('Assignments and composition must bind the same frozen baseline')
        assignment_rows = {row['batch_id']: row for row in assignments['assignments']}
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
        assigned = assignment_rows.get(batch_id) if assignment_rows is not None else None
        if assignment_rows is not None:
            if not assigned: raise ValueError('Manifest batch is not in selected assignments: ' + batch_id)
            if batch['record']['path'] != assigned['write_path']:
                raise ValueError('Batch record path does not match its assignment: ' + batch_id)
        runtime.ref_bytes(root, batch['record'])
        record = json.loads(_safe_path(root, batch['record']['path']).read_text())
        if record.get('schema') != 2 or record.get('edge_files'):
            raise ValueError('Registration batches use schema 2 and do not build stage-3 relations')
        if assigned is not None and {row['path'] for row in record['materials']} != set(assigned['material_paths']):
            raise ValueError('Batch materials do not match selected assignments: ' + batch_id)
        if any(frozen.get(row['path']) != row['sha256'] for row in record['materials']):
            raise ValueError('Batch material differs from the bound frozen baseline: ' + batch_id)
        for label, rows, table, key, seen in [('object', record['objects'], objects, 'object_id', seen_objects), ('material', record['materials'], materials, 'path', seen_materials)]:
            for row in rows:
                identity = row[key]
                if identity in table:
                    previous = table[identity]
                    if row == previous:
                        duplicates.append({'kind': label, 'id': identity})
                    elif label == 'material':
                        if previous.get('sha256') == row.get('sha256') and {previous.get('disposition'), row.get('disposition')} <= {'objects', 'attachment'}:
                            row = merge_material(previous, row)
                        elif mode != 'incremental' or identity in seen:
                            raise ValueError('Conflicting material version or disposition across batches: ' + identity)
                        # The first explicit update in an incremental batch may
                        # replace old material bytes or resolve its disposition.
                        # The baseline and incoming objects bind the new bytes;
                        # load below rejects any unchanged owner left stale.
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


def _registration_scope(name):
    """Keep closely related archive material together without assigning Claims."""
    parts = PurePosixPath(name).parts
    if len(parts) >= 2 and parts[0] == 'archives':
        stop = 2
        while len(parts) > stop + 1 and parts[stop] == 'subarchives':
            stop += 2
        return '/'.join(parts[:stop])
    return '/'.join(parts[:-1]) or '.'


def _registration_links(name, text, known):
    """Local Markdown links are scheduling clues, never inferred relations."""
    import posixpath
    from urllib.parse import unquote
    result = set()
    for value in re.findall(r'\[[^\]]*\]\(([^\n]*?)\)', text):
        value = value.strip()
        if value.startswith('<') and '>' in value:
            value = value[1:value.index('>')]
        elif re.search(r'\s+["\']', value):
            value = re.split(r'\s+["\']', value, maxsplit=1)[0]
        value = unquote(value.split('#', 1)[0])
        if not value or re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:', value):
            continue
        target = posixpath.normpath(value.lstrip('/') if value.startswith('/') else
                                    posixpath.join(str(PurePosixPath(name).parent), value))
        if target in known and target != name:
            result.add(target)
    return result


def _registration_order(names, links):
    """Follow direct local families, keeping common definition hubs shared."""
    names = set(names)
    degree = {name: 0 for name in names}
    for name in names:
        for target in links[name] & names:
            degree[target] += 1
    hub_limit = max(8, (len(names) + 19) // 20)
    hubs = {name for name, count in degree.items() if count >= hub_limit}
    adjacent = {name: set() for name in names}
    for name in names:
        for target in links[name] & names:
            if target not in hubs and name not in hubs:
                adjacent[name].add(target)
                adjacent[target].add(name)
    result, left = [], set(names)
    while left:
        first = min(left)
        pending = [first]
        while pending:
            name = pending.pop()
            if name not in left:
                continue
            left.remove(name)
            result.append(name)
            pending.extend(sorted(adjacent[name] & left, reverse=True))
    return result, hubs


def _published_registration_materials(root, include_completed=True):
    """Read only a synced published queue, never a local unpublished task JSON."""
    import coordination
    note = {'source': 'not-a-published-queue-snapshot', 'skipped_materials': 0}
    top = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=root, capture_output=True, text=True)
    if top.returncode or Path(top.stdout.strip()).resolve() != root:
        return set(), dict(note, registry_source='local-unpublished-workspace'), None
    run = coordination.config(root, 'wcg.workflowRun') or 'p25-register-v2'
    config = _safe_path(root, 'research/operations/' + runtime.identity(run) + '/run.json')
    states = {'available', 'claimed', 'blocked', 'handoff'} | ({'done'} if include_completed else set())
    if (coordination.config(root, 'wcg.workflowRun') and config.is_file()
            and json.loads(config.read_text()).get('phase') == 'registration'):
        import map_tasks
        with map_tasks.latest(root, 'registration') as (directory, ctx):
            records = map_tasks.listing(directory, ctx=ctx)
            tip = map_tasks.board.git(directory, 'rev-parse', 'HEAD').stdout.decode().strip()
            already = {(ref['path'], ref['sha256']) for row in records
                       if row.get('state') in states and row.get('definition', {}).get('stage') == 'registration'
                       for ref in row['definition'].get('materials', [])}
            if runtime.REGISTRY in map_tasks._tree(directory):
                map_tasks._ensure(directory, runtime.REGISTRY)
                data, _ = runtime.load(directory, verify=False)
                published_materials = {row['path']: row for row in data['materials']}
            else:
                published_materials = {}
        return already, {'source': 'latest-published-workflow-snapshot', 'tip': tip, 'workflow_run': run,
                         'registry_source': 'latest-published-workflow-snapshot',
                         'skipped_materials': 0,
                         'note': 'Same-version work already in the published queue is resumed/integrated; withdrawn tasks can be reassigned.'}, published_materials
    if not config.is_file() or json.loads(config.read_text()).get('phase') != 'registration':
        run = 'p25-register-v2'
    branch = coordination.config(root, 'wcg.branch') or subprocess.run(
        ['git', 'branch', '--show-current'], cwd=root, capture_output=True, text=True).stdout.strip()
    tracking = 'refs/remotes/origin/' + branch
    tip = subprocess.run(['git', 'rev-parse', '--verify', tracking], cwd=root, capture_output=True, text=True)
    if tip.returncode:
        return set(), dict(note, source='unavailable-remote-tracking-snapshot', tracking=tracking,
                           registry_source='local-unpublished-workspace'), None
    commit = tip.stdout.strip()
    prefix = 'research/operations/' + run + '/tasks/'
    tree = subprocess.run(['git', 'ls-tree', '-r', '-z', commit, '--', prefix], cwd=root, capture_output=True)
    if tree.returncode:
        raise ValueError('Cannot read the published registration task snapshot; sync before drafting')
    entries = []
    for entry in tree.stdout.split(b'\0'):
        if not entry:
            continue
        meta, name = entry.split(b'\t', 1)
        _, kind, oid = meta.split()
        if kind == b'blob' and name.endswith(b'.json'):
            entries.append((name.decode('utf-8'), oid.decode('ascii')))
    raw = subprocess.run(['git', 'cat-file', '--batch'], cwd=root, capture_output=True,
                         input=''.join(oid + '\n' for _, oid in entries).encode('ascii'))
    if raw.returncode:
        raise ValueError('Cannot read published registration task bytes; sync before drafting')
    already, offset = set(), 0
    for name, _ in entries:
        end = raw.stdout.find(b'\n', offset)
        header = raw.stdout[offset:end].split()
        if end < 0 or len(header) != 3 or header[1] != b'blob':
            raise ValueError('Cannot read published registration task: ' + name)
        size = int(header[2])
        record = json.loads(raw.stdout[end + 1:end + 1 + size])
        offset = end + 2 + size
        definition = record.get('definition', {})
        if record.get('state') in states and definition.get('stage') == 'registration':
            already.update((ref['path'], ref['sha256']) for ref in definition.get('materials', []))
    if offset != len(raw.stdout):
        raise ValueError('Invalid published registration task response')
    registry_tree = subprocess.run(['git', 'ls-tree', '--name-only', commit, '--', runtime.REGISTRY],
                                   cwd=root, capture_output=True)
    if registry_tree.returncode:
        raise ValueError('Cannot inspect the published registration table; sync before drafting')
    if registry_tree.stdout.strip():
        canonical = subprocess.run(['git', 'show', commit + ':' + runtime.REGISTRY], cwd=root, capture_output=True)
        if canonical.returncode:
            raise ValueError('Cannot read the published registration table; sync before drafting')
        data, _ = runtime.load(root, provided=json.loads(canonical.stdout), verify=False)
        published_materials = {row['path']: row for row in data['materials']}
    else:
        published_materials = {}
    return already, {'source': tracking, 'tip': commit, 'workflow_run': run,
                     'registry_source': tracking,
                     'skipped_materials': 0,
                     'note': 'Same-version materials already in published unfinished or completed tasks are resumed/integrated instead of scheduled again; withdrawn tasks may be reassigned.'}, published_materials


_CONTEXT_ENCODINGS = {}


def _context_text(path, raw):
    binary_suffixes = {'.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.tif', '.tiff', '.zip', '.gz', '.parquet', '.pkl', '.npy', '.npz', '.sqlite', '.db'}
    if path.suffix.lower() in binary_suffixes or b'\0' in raw or raw.startswith((b'%PDF-', b'PK\x03\x04')):
        return None
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        return None


def text_cost(text, model='gpt-6.1-sol'):
    """Count characters/bytes separately and label text-token measurement honestly."""
    if not isinstance(text, str):
        raise ValueError('Text measurement requires decoded text')
    if model not in _CONTEXT_ENCODINGS:
        try:
            import tiktoken
            encoding = tiktoken.encoding_for_model(model)
        except Exception:
            encoding = None
        _CONTEXT_ENCODINGS[model] = encoding
    encoding = _CONTEXT_ENCODINGS[model]
    if encoding is not None:
        tokens = len(encoding.encode(text, disallowed_special=()))
        estimator = 'tiktoken-model-mapping:' + encoding.name
        estimated = False
    else:
        # Standard-library fallback for Chinese mathematical Markdown. It is a
        # deliberately padded planning estimate, never characters == tokens.
        tokens = 0
        for run in re.findall(r'[A-Za-z0-9_]+|[ \t]+|\r\n|\n|.', text, re.DOTALL):
            if run.isascii() and re.fullmatch(r'[A-Za-z0-9_]+', run):
                tokens += math.ceil(len(run) / 3)
            elif run.isspace() and '\n' not in run and '\r' not in run:
                tokens += math.ceil(len(run) / 8)
            elif run in {'\n', '\r\n'}:
                tokens += 1
            elif len(run) == 1 and (0x3400 <= ord(run) <= 0x9fff or 0x20000 <= ord(run) <= 0x3134f):
                tokens += 2
            else:
                tokens += len(run.encode('utf-8'))
        tokens = math.ceil(tokens * 1.15)
        estimator = 'conservative-math-text-estimate-v1; not a tokenizer count'
        estimated = True
    return {'chars': len(text), 'utf8_bytes': len(text.encode('utf-8')),
            'estimated_tokens': tokens, 'token_count_is_estimate': estimated,
            'estimator': estimator, 'model': model}


def context_budget(context_tokens=500000, window_source='official-default', used_tokens=None,
                   reserve_tokens=None, inherited=False, output_tokens=None, model='gpt-6.1-sol'):
    """A tunable reading plan; unknown runtime usage is not invented as telemetry."""
    if not isinstance(model, str) or not model.strip():
        raise ValueError('Declare the worker model for a reading plan')
    if window_source == 'official-default' and (model != 'gpt-6.1-sol' or context_tokens != 500000):
        raise ValueError('The 500K official default here is for gpt-6.1-sol; provide a reported or user-specified window for another model')
    if type(context_tokens) is not int or context_tokens < 1:
        raise ValueError('context_tokens must be a positive integer')
    if window_source not in {'official-default', 'platform-reported', 'user-specified'}:
        raise ValueError('State whether the context window is official-default, platform-reported or user-specified')
    if used_tokens is not None and (type(used_tokens) is not int or used_tokens < 0):
        raise ValueError('used_tokens is a platform reading, or omitted when unknown')
    if reserve_tokens is None:
        reserve_tokens = max(1, context_tokens * 2 // 5)
    if type(reserve_tokens) is not int or not 0 < reserve_tokens < context_tokens:
        raise ValueError('Reserve explicit room for instructions, reasoning, tools and writing')
    if output_tokens is None:
        output_tokens = min(100000, max(1, reserve_tokens // 2))
    if type(output_tokens) is not int or not 0 < output_tokens <= reserve_tokens:
        raise ValueError('Output allowance must fit within the reserved context')
    available = context_tokens - reserve_tokens - (used_tokens if used_tokens is not None else 0)
    if available < 1:
        raise ValueError('The declared usage and reserves leave no reading budget; use a fresh worker or correct the budget')
    assumptions = ['Window source is declared, not discovered from this conversation.',
                   'Reading budget includes source text and object/task metadata.',
                   'Reserved context includes expected generated records and later reasoning/tool growth.']
    if inherited and used_tokens is None:
        # A long inherited conversation is not a fresh 500K window. Keep the
        # result usable as a small-window draft but never claim it fits exactly.
        available = min(available, max(1, context_tokens // 5))
        assumptions.append('Inherited context usage is unknown: limited planning window only; prefer a fresh worker or supply reported used_tokens.')
    elif used_tokens is None:
        assumptions.append('Fresh worker assumed; actual system/prefix usage is unknown and covered only by the engineering reserve.')
    return {'context_tokens': context_tokens, 'window_source': window_source, 'model': model,
            'used_tokens': used_tokens, 'history_mode': 'inherited' if inherited else 'fresh-worker',
            'reserve_tokens': reserve_tokens, 'reading_tokens': available,
            'output_tokens': output_tokens, 'runtime_remaining_tokens': None,
            'declared_remaining_before_reserve_tokens': None if used_tokens is None else context_tokens-used_tokens,
            'assumptions': assumptions, 'budget_is_runtime_measurement': False}


def _merged_intervals(intervals):
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    return merged


def reading_cost(root, refs, metadata=None, cache=None, model='gpt-6.1-sol'):
    """Measure complete requested reading spans once per path/SHA, not per Claim."""
    cache = {} if cache is None else cache
    sources = {}
    for ref in refs:
        path = runtime.reference(root, ref)
        key = (ref['path'], ref['sha256'])
        if key not in cache:
            raw = path.read_bytes()
            if runtime.digest(raw) != ref['sha256']:
                raise ValueError('Stale content binding: ' + ref['path'])
            text = _context_text(path, raw)
            cache[key] = {'text': text, 'bytes': len(raw)}
        text = cache[key]['text']
        row = sources.setdefault(key, {'ref': {'path': key[0], 'sha256': key[1]}, 'spans': []})
        if text is None:
            row['unmeasured'] = True
            continue
        if 'section' not in ref:
            row['spans'].append((0, len(text)))
        else:
            selected = runtime.section(text, ref['section'])
            positions = [start for title, _, start in runtime.heading_sections(text) if title == ref['section']]
            if len(positions) != 1:
                raise ValueError('Section title missing or ambiguous: ' + ref['section'])
            row['spans'].append((positions[0], positions[0] + len(selected)))
    totals = {'chars': 0, 'utf8_bytes': 0, 'source_tokens': 0, 'metadata_tokens': 0,
              'estimated_tokens': 0, 'metadata_chars': 0, 'metadata_utf8_bytes': 0, 'distinct_files': len(sources), 'reading_segments': 0,
              'token_count_is_estimate': False, 'estimators': [], 'unmeasured_refs': []}
    for key, row in sources.items():
        if row.get('unmeasured'):
            totals['unmeasured_refs'].append(dict(row['ref'], bytes=cache[key]['bytes'],
                reason='Non-text evidence: export/read with the appropriate tool, then size its actual extracted context'))
            continue
        text = cache[key]['text']
        spans = _merged_intervals(row['spans'])
        signature = (model, tuple(spans))
        measured = cache[key].setdefault('span_costs', {})
        if signature not in measured:
            measured[signature] = text_cost('\n'.join(text[start:end] for start, end in spans), model)
        cost = measured[signature]
        totals['chars'] += cost['chars']; totals['utf8_bytes'] += cost['utf8_bytes']
        totals['source_tokens'] += cost['estimated_tokens']; totals['reading_segments'] += len(spans)
        totals['token_count_is_estimate'] |= cost['token_count_is_estimate']
        if cost['estimator'] not in totals['estimators']: totals['estimators'].append(cost['estimator'])
    if metadata is not None:
        text = metadata if isinstance(metadata, str) else json.dumps(metadata, ensure_ascii=False, sort_keys=True)
        cost = text_cost(text, model)
        totals['metadata_tokens'] = cost['estimated_tokens']
        totals['metadata_chars'] = cost['chars']; totals['metadata_utf8_bytes'] = cost['utf8_bytes']
        totals['token_count_is_estimate'] |= cost['token_count_is_estimate']
        if cost['estimator'] not in totals['estimators']: totals['estimators'].append(cost['estimator'])
    totals['estimated_tokens'] = totals['source_tokens'] + totals['metadata_tokens']
    totals['measurement_scope'] = 'Requested complete text spans plus supplied metadata; binary evidence is not token-counted from raw bytes.'
    return totals


def pack_units(root, units, budget, max_items=200, cache=None):
    """Pack caller-ordered mathematical units; never truncate an oversized object."""
    if type(max_items) is not int or max_items < 1:
        raise ValueError('max_items must be positive')
    if not isinstance(units, list): raise ValueError('A concrete ordered list of reading units is required')
    cache = {} if cache is None else cache
    seen = set()
    for unit in units:
        key = unit.get('key')
        if not isinstance(key, str) or not key or key in seen:
            raise ValueError('Reading units require distinct nonempty keys')
        seen.add(key)
        if not isinstance(unit.get('refs'), list): raise ValueError('Reading unit refs must be an explicit list')
        output = unit.get('estimated_output_tokens', 0)
        if type(output) is not int or output < 0: raise ValueError('Output estimates must be nonnegative integers')
    metadata_costs = {}
    for item in units:
        metadata = item.get('metadata', {'key': item['key']})
        value = metadata if isinstance(metadata, str) else json.dumps(metadata, ensure_ascii=False, sort_keys=True)
        metadata_costs[item['key']] = text_cost(value, budget.get('model', 'gpt-6.1-sol'))
    def measure(items):
        refs = [ref for item in items for ref in item['refs']]
        cost = reading_cost(root, refs, None, cache, budget.get('model', 'gpt-6.1-sol'))
        cost['metadata_tokens'] = sum(metadata_costs[item['key']]['estimated_tokens'] for item in items)
        cost['metadata_chars'] = sum(metadata_costs[item['key']]['chars'] for item in items)
        cost['metadata_utf8_bytes'] = sum(metadata_costs[item['key']]['utf8_bytes'] for item in items)
        cost['estimated_tokens'] += cost['metadata_tokens']
        cost['token_count_is_estimate'] |= any(metadata_costs[item['key']]['token_count_is_estimate'] for item in items)
        for item in items:
            estimator = metadata_costs[item['key']]['estimator']
            if estimator not in cost['estimators']: cost['estimators'].append(estimator)
        cost['task_overhead_tokens'] = 32 * len(items)
        cost['estimated_tokens'] += cost['task_overhead_tokens']
        return cost
    def entry(items, cost):
        output = sum(item.get('estimated_output_tokens', 0) for item in items)
        oversized = cost['estimated_tokens'] > budget['reading_tokens'] or output > budget['output_tokens']
        unknown = bool(cost['unmeasured_refs'])
        return {'units': list(items), 'reading': cost, 'estimated_output_tokens': output,
                'oversized': oversized, 'requires_export': unknown,
                'budget_status': 'requires-evidence-export' if unknown else 'requires-connected-reading-passes' if oversized else 'within-declared-planning-budget',
                'context_budget': budget}
    packs, current, current_cost = [], [], None
    for unit in units:
        alone = measure([unit])
        output = unit.get('estimated_output_tokens', 0)
        exceptional = bool(alone['unmeasured_refs']) or alone['estimated_tokens'] > budget['reading_tokens'] or output > budget['output_tokens']
        if exceptional:
            if current: packs.append(entry(current, current_cost)); current, current_cost = [], None
            packs.append(entry([unit], alone))
            continue
        candidate = [*current, unit]
        cost = measure(candidate)
        candidate_output = sum(item.get('estimated_output_tokens', 0) for item in candidate)
        if current and (len(candidate) > max_items or cost['estimated_tokens'] > budget['reading_tokens'] or candidate_output > budget['output_tokens']):
            packs.append(entry(current, current_cost)); current, current_cost = [unit], alone
        else:
            current, current_cost = candidate, cost
    if current: packs.append(entry(current, current_cost))
    return {'packs': packs, 'units': len(units), 'unassigned_units': [],
            'oversized_units': [item['key'] for pack in packs if pack['oversized'] for item in pack['units']],
            'requires_export_units': [item['key'] for pack in packs if pack['requires_export'] for item in pack['units']]}


def draft_registration_tasks(root, baseline_file='research/registration/baseline.json',
                             output='research/registration/tasks.json', max_materials=200,
                             task_prefix='register', context_options=None,
                             include_registered=False):
    """Pack many frozen materials into each existing registration queue task.

    The program schedules reading and ownership only. It never allocates a
    mathematical object per page or fills mathematical records automatically.
    """
    root = Path(root).resolve()
    runtime.identity(task_prefix)
    if type(max_materials) is not int or max_materials < 1:
        raise ValueError('max_materials must be a positive batch ceiling')
    baseline_path = _safe_path(root, baseline_file)
    baseline_bytes = baseline_path.read_bytes()
    baseline = json.loads(baseline_bytes)
    if baseline.get('schema') != 1 or not isinstance(baseline.get('materials'), list) or not baseline['materials']:
        raise ValueError('Registration planning needs an actual frozen input baseline')
    budget = context_budget(**(context_options or {}))
    scheduled, queue_snapshot, published_materials = _published_registration_materials(root, include_completed=not include_registered)
    known = {}
    if not include_registered:
        if published_materials is not None:
            known = published_materials
        elif _safe_path(root, runtime.REGISTRY).is_file():
            registered, _ = runtime.load(root, verify=False)
            known = {row['path']: row for row in registered['materials']}
    rows, texts, links, scopes, file_bytes = {}, {}, {}, {}, {}
    already_registered, already_scheduled = 0, 0
    for original in baseline['materials']:
        row = {key: original[key] for key in ('path', 'sha256')}
        name = row['path']
        if name in rows:
            raise ValueError('Duplicate frozen material: ' + name)
        runtime.reference(root, row)
        rows[name] = row
        previous = known.get(name, {})
        if previous.get('sha256') == row['sha256'] and previous.get('disposition') in {'objects', 'attachment', 'excluded'}:
            already_registered += 1
            continue
        if (name, row['sha256']) in scheduled:
            already_scheduled += 1
            continue
        raw = runtime.ref_bytes(root, row)
        file_bytes[name] = len(raw)
        texts[name] = _context_text(_safe_path(root, name), raw)
        scopes.setdefault(_registration_scope(name), []).append(name)
    for name in texts:
        links[name] = _registration_links(name, texts[name] or '', rows)
    definitions = {name for name in rows if any(part.casefold() in {'定义', '模型', 'definition', 'definitions', 'model', 'models'}
                   for part in PurePosixPath(name).parts) or PurePosixPath(name).stem.endswith(('--定义', '--模型'))}
    units, cost_cache = [], {}
    for scope, names in sorted(scopes.items()):
        ordered, _ = _registration_order(names, links)
        for name in ordered:
            shared = sorted(links[name] & definitions)
            cost = text_cost(texts[name], budget['model']) if texts[name] is not None else {'estimated_tokens': 0}
            cached = {'text': texts[name], 'bytes': file_bytes[name]}
            if texts[name] is not None:
                cached['span_costs'] = {(budget['model'], ((0, len(texts[name])),)): cost}
            cost_cache[(name, rows[name]['sha256'])] = cached
            estimated_output = 400 + min(1600, (int(cost['estimated_tokens']) * 8 + 99) // 100)
            units.append({'key': name, 'material': rows[name], 'scope': scope,
                          'refs': [rows[name], *(rows[target] for target in shared)],
                          'metadata': {'material': name, 'scope': scope},
                          'estimated_output_tokens': estimated_output,
                          'requires_export': texts[name] is None})
    packed = pack_units(root, units, budget, max_items=max_materials, cache=cost_cache)
    packs = packed['packs']
    baseline_ref = {'path': baseline_file, 'sha256': runtime.digest(baseline_bytes)}
    plan_id = runtime.pin({'baseline': baseline_ref, 'budget': budget, 'max_materials': max_materials,
                           'include_registered': bool(include_registered),
                           'groups': [[unit['key'] for unit in pack['units']] for pack in packs]})[:10]
    tasks = []
    for number, pack in enumerate(packs, 1):
        members = pack['units']
        task_id = runtime.identity(task_prefix + '-' + plan_id + '-' + str(number).zfill(4))
        primary = [unit['material'] for unit in members]
        primary_paths = {ref['path'] for ref in primary}
        shared = {ref['path']: ref for unit in members for ref in unit['refs'] if ref['path'] not in primary_paths}
        unknown = sorted({unit['key'] for unit in members if unit.get('requires_export')} |
                         {ref['path'] for ref in pack['reading'].get('unmeasured_refs', [])})
        mode = 'export-before-reading' if unknown else 'sectioned-reading' if pack.get('oversized') else 'planned-window'
        task = {'task_id': task_id, 'stage': 'registration', 'baseline': baseline_ref,
                'materials': primary,
                'goal': '批量登记本批已整理数学材料；实读精确对象、稳定身份、正文与必要证据。保留各自模型和量词，不逐源重新清洗，不在本步建超边。',
                'write_paths': ['research/registration/batches/' + task_id + '.json',
                                'research/registration/receipts/' + task_id + '.json'],
                'context_plan': {'budget': budget, 'reading': pack['reading'],
                                 'estimated_output_tokens': pack['estimated_output_tokens'],
                                 'output_estimate': 'Scheduling estimate from source length, not an inferred Claim count; adjust if actual independent objects need more space.',
                                 'material_count': len(primary), 'scopes': sorted({unit['scope'] for unit in members}),
                                 'shared_read_refs': [shared[name] for name in sorted(shared)],
                                 'reading_mode': mode, 'oversized': bool(pack.get('oversized')),
                                 'unmeasured_materials': unknown,
                                 'instruction': 'Read the assigned materials in useful batches. Shared definitions are read-only and counted once. If a unit exceeds the window, continue it in sections with saved mathematical notes; do not truncate it or mark it read from a summary.'}}
        tasks.append(task)
    destination = _safe_path(root, output)
    if destination == baseline_path or output == runtime.REGISTRY or output in rows:
        raise ValueError('Write the task draft separately from frozen inputs and mathematical content')
    try:
        previous_plan = json.loads(destination.read_text()) if destination.is_file() else None
    except ValueError:
        previous_plan = None
    if previous_plan != tasks:
        runtime._write_json(destination, tasks)
    return {'status': 'registration-current-no-new-materials' if not tasks else
                      'registration-tasks-already-drafted' if previous_plan == tasks else
                      'registration-tasks-drafted-local-not-published', 'path': output,
            'tasks': len(tasks), 'materials': len(texts), 'baseline_materials': len(rows),
            'already_registered_materials': already_registered,
            'already_scheduled_materials': already_scheduled,
            'queue_snapshot': dict(queue_snapshot, skipped_materials=already_scheduled),
            'materials_per_task': [len(task['materials']) for task in tasks],
            'max_materials': max_materials, 'context_budget': budget,
            'oversized_tasks': [task['task_id'] for task in tasks if task['context_plan']['oversized']],
            'unmeasured_materials': sorted(name for name in texts if texts[name] is None),
            'next': ('Publish this task array once with registration-task plan --record-file ' + output + '; each claim/done operates on a complete many-material task.') if tasks else
                    'No new material batches were created. Resume existing run tasks and integration; do not pass an empty draft to plan.'}
