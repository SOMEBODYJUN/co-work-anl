"""Exercise registration -> joint hyperedge -> two packets -> feedback -> resume."""
import argparse
import json
from pathlib import Path

import research_runtime as runtime


def create(destination):
    if destination.exists(): raise ValueError('Demo destination must be new; existing work is preserved')
    destination.mkdir(parents=True)
    body = 'archives/demo/subarchives/sum/state/sum.md'
    files = {body: '# Domain\nLet x and y be positive real numbers.\n\n# A\nx>0.\n\n# B\ny>0.\n\n# C\nx+y>0, because adding y>0 to x>0 preserves strict positivity.\n',
             'research/target.md': '# Exact problem\nProve x+y>0 for every pair of positive real numbers x,y.\n',
             'research/definitions.md': '# Definitions\nPositive means strictly greater than zero in the ordered field of real numbers.\n',
             'research/obstacles.md': '# Boundary\nPositivity of x alone is insufficient if y is an arbitrary real number: x=1,y=-2.\n'}
    for name, text in files.items():
        path = destination / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text)
    def ref(name, section=None):
        row = {'path': name, 'sha256': runtime.digest((destination / name).read_bytes())}
        if section: row['section'] = section
        return row
    objects = []
    for oid, statement in [('A', 'x>0'), ('B', 'y>0'), ('C', 'x+y>0')]:
        objects.append({'object_id': oid, 'version': 1, 'title': statement, 'kind': 'lemma', 'truth_status': 'proved',
                        'model': 'ordered field of real numbers, x,y strictly positive', 'statement': statement,
                        'quantifiers': 'for every positive real x and every positive real y', 'assumptions': ['x>0', 'y>0'],
                        'scope': 'elementary software integration example', 'objections': 'No known objection under the stated assumptions',
                        'body': ref(body, oid), 'evidence': [], 'sources': [], 'keywords': ['positive', 'sum']})
    edge = {'edge_id': 'AB-C', 'kind': 'implies', 'status': 'accepted', 'source_ids': ['A', 'B'], 'target_ids': ['C'],
            'premises_mode': 'all', 'relation_mode': 'unconditional', 'conditions': 'same positive real x,y',
            'explanation': 'Two joint positivity premises imply positivity of the sum in an ordered field',
            'scope': 'the stated domain only', 'roles': {'A': 'positivity of x', 'B': 'positivity of y', 'C': 'positivity of sum'},
            'evidence': [ref(body, 'C')], 'reviewed_by': 'Elementary demo author', 'review_note': 'Direct addition of strict inequalities, not a research claim'}
    bindings = runtime.edge_bindings(destination, edge, {o['object_id']: o for o in objects})
    edge.update({k: v for k, v in bindings.items() if k != 'note'})
    runtime._write_json(destination / 'map/edges/AB-C.json', edge)
    registry = {'schema': 2, 'objects': objects, 'materials': [dict(ref(body), disposition='objects', object_ids=['A', 'B', 'C'], reason='Three independently addressable statements in one unchanged Markdown page')], 'edge_files': ['map/edges/AB-C.json']}
    runtime._write_json(destination / 'research/registration/baseline.json', {'schema': 1, 'scope': 'repository', 'coverage_note': 'Complete elementary demo input', 'materials': [ref(body)]})
    registry['baseline'] = ref('research/registration/baseline.json')
    runtime._write_json(destination / runtime.REGISTRY, registry)
    runtime._write_json(destination / 'map/coverage.json', {o['object_id']: {'state': 'linked', 'edge_ids': ['AB-C'], 'reason': 'The sum relation', 'comparison_scope': 'A B C', 'object_pin': runtime.pin(o)} for o in objects})
    review = {'comparison_scope': 'The complete elementary positive-sum family', 'outcome': 'One joint relation, no additional archive transfer claimed', 'unresolved': []}
    runtime._write_json(destination / 'map/integration.json', {'reviewed_by': 'Elementary demo author', 'review_note': 'All demo comparisons explicitly checked',
        'registry_pin': runtime.pin(registry), 'edge_pins': {'AB-C': runtime.pin(edge)},
        'archive_reviews': {scope: review for scope in runtime.object_scopes({o['object_id']: o for o in objects})}, 'cross_archive_review': review})
    spec = {'problem_id': 'positive-sum', 'problem': ref('research/target.md'), 'definitions': [ref('research/definitions.md')], 'obstacles': [ref('research/obstacles.md')], 'seed_ids': ['C'], 'hops': 2}
    runtime._write_json(destination / 'research/spec.json', spec)
    graph = runtime.build(destination, final=True)
    start = runtime.init_run(destination, 'demo-run', 'research/spec.json')
    note = 'research/workspaces/demo/solver1.md'
    path = destination / note; path.parent.mkdir(parents=True, exist_ok=True); path.write_text('# Partial result\nUse positivity of both variables.\n')
    first = runtime.update_run(destination, 'demo-run', 'solver1', 'full', note, 'Check strictness at zero', 'candidate')
    second = runtime.update_run(destination, 'demo-run', 'solver1', 'full', note, 'Explain the zero boundary', 'needs-feedback', feedback='The original domain is strictly positive. Explain what changes at zero.')
    resumed = runtime.resume(destination, 'demo-run')
    report = {'status': 'passed', 'graph': graph, 'run': start, 'events': [first, second],
              'resumed_solver': resumed['run']['solvers']['solver1'],
              'scope': 'Elementary integration fixture. No mathematical research agents launched; no Q-CAG-HALF-6 conclusion.'}
    runtime._write_json(destination / 'report.json', report)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument('--out', type=Path, required=True); args = parser.parse_args()
    try: result = create(args.out.resolve())
    except (ValueError, OSError, KeyError) as exc: raise SystemExit(str(exc))
    print(json.dumps({'status': result['status'], 'report': str(args.out / 'report.json')}, indent=2))
