"""New local-only boundary examples; frozen source is never changed."""
from pathlib import Path
import copy
import importlib.util
import json
import tempfile

E = Path(__file__).resolve().parent
S = E.parents[2]
rows = json.loads((E / 'source-manifest.json').read_text())
output = []
for row in rows[:2]:
    spec = importlib.util.spec_from_file_location('boundary_' + row['id'], S / row['saved_path'])
    b = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(b)
    b.git = lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError('No Git allowed in pure probes'))
    checks = []
    def record(name, condition, result):
        assert condition, name
        checks.append({'case': name, 'observed': result})
    def event(actor='R01', *, ident='a' * 32, seq=1, stamp=10, **body):
        return dict(b.make_intent(actor, 'message', dict(text='synthetic audit example', **body), ident),
                    schema=3, seq=seq, time=stamp)
    state = b.transition(b.empty_state(), event())
    backwards = b.transition(state, event(ident='b' * 32, seq=2, stamp=1))
    record('time is nonnegative, not monotonic', backwards['last_time'] == 1,
           {'times': [x['time'] for x in backwards['events']], 'last_time': backwards['last_time']})
    long_actor = 'A' * 101
    b.validate_intent(b.make_intent(long_actor, 'message', {'text': 'synthetic'}))
    rejected = False
    try:
        b.address(long_actor)
    except b.ValidationError:
        rejected = True
    record('actor validator and addressed view length differ', rejected,
           {'message_actor_length_accepted': 101, 'address_length_limit': 64})
    private = b.transition(b.empty_state(), event(to='R02', save='s'))
    record('private visibility is a projection of complete raw state',
           len(private['events']) == 1 and not b.visible(private['events'][0])
           and b.visible(private['events'][0], 'R02'),
           {'raw_events': 1, 'anonymous_render_hides': 'synthetic audit example' not in b.render(private),
            'participant_render_contains': 'synthetic audit example' in b.render(private, actor='R02')})
    for name, reply in [
        ('private reply cannot change participants', event('R02', ident='c' * 32, seq=2, to='R03', save='s', reply_to='a' * 32)),
        ('reply cannot cross saves', event('R02', ident='c' * 32, seq=2, to='R01', save='t', reply_to='a' * 32)),
    ]:
        rejected = False
        snapshot = copy.deepcopy(private)
        try:
            b.transition(private, reply)
        except b.ValidationError:
            rejected = True
        record(name, rejected and private == snapshot, 'ValidationError; input state unchanged')
    with tempfile.TemporaryDirectory(prefix='board-pure-', dir=S) as tmp:
        client = b.Board.__new__(b.Board)
        client.cache = Path(tmp)
        root = Path(tmp) / b.PREFIX
        root.mkdir(parents=True)
        (root / 'meta.json').write_text(b.encode({'schema': 3}))
        decoded = client.decode(tmp)
        record('missing events directory decodes as empty', decoded == b.empty_state(), decoded)
        client.read = lambda: private
        receipt = client.acknowledge('R02', 's', ['a' * 32])
        record('acknowledge is local read receipt only',
               client.seen('R02', 's') == {'a' * 32}
               and receipt['meaning'] == 'read receipt only; not mathematical adoption', receipt)
    descriptor = {'branch': 'non-main-fixture', 'commit': 'a' * 40, 'path': 'asset.md', 'sha256': 'b' * 64}
    b.asset_shape(descriptor)
    record('asset shape does not enforce main-only branch policy', True, descriptor)
    record('schema exact integer excludes bool', not b.current_metadata({'schema': True}),
           {'integer_3': b.current_metadata({'schema': 3}), 'bool_True': b.current_metadata({'schema': True})})
    output.append({'source_id': row['id'], 'sha256': row['sha256'], 'cases': checks,
                   'source_unmodified': True, 'git_network_calls': 0})
(E / 'runs/pure-boundaries.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'variants': len(output), 'local_examples_per_variant': len(output[0]['cases']),
                  'passed': True, 'new_evidence_scope': 'finite software boundary examples only'}))
