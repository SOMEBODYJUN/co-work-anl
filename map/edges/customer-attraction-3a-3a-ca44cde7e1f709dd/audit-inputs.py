"""Read-only input hashes and provenance metadata; never runs mathematics."""
import argparse
import hashlib
import json
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(repo):
    task_path = 'research/operations/map-v2/tasks/customer-attraction-3a-3a-ca44cde7e1f709dd.json'
    task = json.loads((repo / task_path).read_text())['definition']
    refs = task['context_plan']['reading_refs']
    rows = []
    for index, ref in enumerate(refs):
        actual = sha(repo / ref['path'])
        rows.append({'index': index, **ref, 'actual_sha256': actual,
                     'matches': actual == ref['sha256']})
    body = 'archives/customer-attraction/state/计算/实际末主题单枝与三枝条件联合的精确点--计算.md'
    driver = 'archives/customer-attraction/tools/evidence/coupled-b-fixed-points-boss3/verify_fixed_point.py'
    failed = 'archives/customer-attraction/tools/evidence/coupled-b-fixed-points-boss3/replay/failed-type-comparison/verifier.py'
    registry = json.loads((repo / 'research/registry.json').read_text())['objects']
    if isinstance(registry, dict):
        registry = list(registry.values())
    affected = []
    for obj in registry:
        hits = []
        for slot, ref in [('body', obj['body'])] + [('evidence', ref) for ref in obj.get('evidence', [])]:
            if ref['path'] in (body, driver):
                hits.append({'slot': slot, **ref})
        if hits:
            affected.append({'object_id': obj['object_id'], 'version': obj['version'], 'hits': hits})
    affected_ids = {obj['object_id'] for obj in affected}
    edge_uses = []
    for path in sorted((repo / 'map/edges').rglob('*.json')):
        try:
            data = json.loads(path.read_text())
        except (ValueError, UnicodeDecodeError):
            continue
        if isinstance(data, list):
            edges = data
        elif isinstance(data, dict) and 'edge_id' in data:
            edges = [data]
        elif isinstance(data, dict) and isinstance(data.get('edges'), list):
            edges = data['edges']
        else:
            continue
        for edge in edges:
            if not isinstance(edge, dict):
                continue
            endpoints = affected_ids.intersection(edge.get('source_ids', []) + edge.get('target_ids', []))
            evidence = [ref for ref in edge.get('evidence', [])
                        if isinstance(ref, dict) and ref.get('path') in (body, driver)]
            if endpoints or evidence:
                edge_uses.append({'path': str(path.relative_to(repo)), 'edge_id': edge.get('edge_id'),
                                  'status': edge.get('status'), 'endpoints': sorted(endpoints), 'evidence': evidence})
    return {
        'scope': 'Read-only hashes and metadata; no driver, builder, LP, SPE, BI or mathematical audit invoked.',
        'task': {'path': task_path, 'sha256': sha(repo / task_path)},
        'registry_sha256': sha(repo / 'research/registry.json'),
        'reading_refs': rows,
        'all_reading_ref_hashes_match': all(row['matches'] for row in rows),
        'distinct_reading_paths': len({ref['path'] for ref in refs}),
        'driver_provenance': {'current_driver': {'path': driver, 'sha256': sha(repo / driver)},
                              'preserved_failed_driver': {'path': failed, 'sha256': sha(repo / failed)},
                              'byte_identical': (repo / driver).read_bytes() == (repo / failed).read_bytes(),
                              'current_driver_invocations': 0, 'historical_success_driver_identity_recovered': False},
        'affected_registry_objects': affected,
        'existing_edge_uses': edge_uses,
        'mathematical_program_invocations': 0,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = audit(args.repo.resolve())
    with args.output.open('x') as output:
        json.dump(report, output, ensure_ascii=False, indent=2)
        output.write('\n')
    print(json.dumps({'all_reading_ref_hashes_match': report['all_reading_ref_hashes_match'],
                      'references': len(report['reading_refs']),
                      'affected_objects': len(report['affected_registry_objects']),
                      'existing_edge_uses': len(report['existing_edge_uses']),
                      'mathematical_program_invocations': 0}, ensure_ascii=False))
