import json, hashlib, pathlib, collections, sys
root=pathlib.Path(__file__).parent
p=root/'candidate_pool.json'; m=json.loads((root/'manifest.json').read_text()); d=json.loads(p.read_text())
assert hashlib.sha256(p.read_bytes()).hexdigest()==m['export_sha256']
assert hashlib.sha256(p.read_bytes()).hexdigest()==m['source_sha256']
assert len(d)==m['entry_count']==59
assert len({e['id'] for e in d})==m['unique_ids']==59
required={'id','title','origin','source_location','exact_question','minimal_target','known_overlap','fatal_risk','status','lane','provenance_note'}
assert all(required <= set(e) for e in d)
assert dict(collections.Counter(e['lane'] for e in d))==m['lane_counts']
assert dict(collections.Counter(e['status'] for e in d))==m['status_counts']
assert dict(collections.Counter(e['origin'] for e in d))==m['origin_counts']
print('candidate_pool validation OK:',len(d),'entries')
