"""Validate explicit research increments and merge unchanged material owners."""
import json

from path_utils import _safe_path
import research_runtime as runtime


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

    Callers may supply exact existing peer owners as read-only validation
    context, without adding objects or material assignments to this increment.
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
