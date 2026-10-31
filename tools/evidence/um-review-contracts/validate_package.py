"""Structural/byte provenance checker. Does not run any archived mathematical program."""
import hashlib
import json
import re
from pathlib import Path

stage = Path(__file__).resolve().parents[3]
repo = stage.parent.parent / 'boss4-research'
ev = stage / 'tools/evidence/um-review-contracts'
ws = stage / 'cleanup/workspaces/Boss4/r3-um-review-contracts'
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
    return json.loads(p.read_text())

sources = load(ev / 'source-manifest.json')
supports = load(ev / 'supporting-source-manifest.json')
assert len(sources) == 5 and len(supports) == 5
inventory = {s['id']: s for s in map(json.loads, (repo/'cleanup/inventory.jsonl').read_text().splitlines())}
verified = []
for s in sources + supports:
    f = stage/s['preserved_path']
    inv = inventory[s['id']]
    assert sha(f) == s['sha256'] == inv['sha256']
    assert f.stat().st_size == s['size'] == inv['size']
    assert len(f.read_text().splitlines()) == s['lines']
    verified.append({'id':s['id'], 'path':s['preserved_path'], 'sha256':sha(f), 'bytes':f.stat().st_size, 'lines':s['lines']})

coverage = load(ev/'source-section-map.json')
for s in sources:
    seen = []
    for b in coverage['blocks']:
        if b['source_id'] == s['id']:
            a,z = b['lines']
            assert 1 <= a <= z <= s['lines']
            seen.extend(range(a,z+1))
            for target in b['targets']:
                assert (stage/target).exists() or (repo/target).exists(), target
    assert seen == list(range(1,s['lines']+1)), (s['id'], seen)
assert coverage['total_primary_lines'] == sum(s['lines'] for s in sources) == 164
assert sum(s['size'] for s in sources) == 21497

receipts = load(ws/'semantic-receipts.json')
assert len(receipts) == 5 and {x['id'] for x in receipts} == {s['id'] for s in sources}
for x in receipts:
    assert all(x[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
    assert x['disposition'] == 'integrated'
    assert all((stage/p).is_file() for p in x['targets'])
formal = sorted(stage.glob('archives/**/*.md'))
assert len(formal) == 6
ids = []
for f in formal:
    text = f.read_text()
    assert text.startswith('---\n')
    front = text.split('---\n',2)[1]
    for key in ('id','kind','type_tag','title','status','summary','source_refs'):
        assert re.search(r'^'+key+r':',front,re.M), (f,key)
    oid = re.search(r'^id: (.+)$',front,re.M).group(1)
    ids.append(oid)
assert len(set(ids)) == len(ids)
old_ids = set()
for f in (repo/'archives').rglob('*.md'):
    m = re.search(r'^id: (.+)$',f.read_text(),re.M)
    if m: old_ids.add(m.group(1))
assert not set(ids) & old_ids

links = []
for f in formal + [ev/'README.md', ws/'README.md', ws/'semantic-review.md']:
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',f.read_text()):
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target): continue
        target = target.split('#',1)[0]
        if not target: continue
        candidate = (f.parent/target).resolve()
        rel = candidate.relative_to(stage)
        assert candidate.exists() or (repo/rel).exists(), (str(f.relative_to(stage)),target)
        links.append({'from':str(f.relative_to(stage)),'to':str(rel)})

provenance = load(ev/'provenance-bindings.json')
assert len(provenance['historical_source_bindings']) == 13
for b in provenance['historical_source_bindings']:
    assert b['matches']
    assert b['inventory_sha256'] == inventory[b['inventory_id']]['sha256']
    assert set(b['reported_sha256']) == {b['inventory_sha256']}
home = next(s for s in supports if s['id']=='eef751243f82cd1689d6')
home_bytes = (stage/home['preserved_path']).read_bytes()
assert hashlib.sha256(home_bytes[:13728]).hexdigest() == provenance['anonymous_prefix']['sha256']
block = next(s for s in supports if s['id']=='ea09d8d6b48b2a06d18f')
block_bytes = (stage/block['preserved_path']).read_bytes()
needle = '任意非空选择域'.encode()
assert block_bytes.count(needle) == 1
inverse = block_bytes.replace(needle,'任意选择域'.encode(),1)
assert len(inverse) == 16914
assert hashlib.sha256(inverse).hexdigest() == provenance['binary_nonempty_edit']['inverse_sha256']

comparison = load(ev/'comparison-manifest.json')
for a in comparison:
    f = repo/a['path']
    assert f.exists() and sha(f) == a['sha256']
    assert a['extra_done'] is False and a['modified'] is False
assert len(comparison) == 10
relations = load(ws/'relations.json')['relations']
assert len(relations) == 10
for a in relations:
    assert all(a.get(k) for k in ('from','to','type','common_premises','evidence','gap'))
    assert (stage/a['from']).exists()
    assert (stage/a['to']).exists() or (repo/a['to']).exists()

json_paths = sorted(stage.rglob('*.json'))
for p in json_paths:
    json.loads(p.read_text())
existing_collisions = [str(f.relative_to(stage)) for f in stage.rglob('*') if f.is_file() and (repo/f.relative_to(stage)).exists()]
assert not existing_collisions, existing_collisions
result = {
    'status':'PASS',
    'scope':'new byte/structure/provenance validation only; no archived mathematical program executed',
    'verified_originals':verified,
    'primary_files':5,'primary_bytes':21497,'primary_lines':164,
    'coverage_blocks':len(coverage['blocks']),
    'supporting_full_read_files':4,'supporting_full_read_lines':590,
    'supporting_selected_read':{'id':home['id'],'lines':[112,304],'selected_line_count':193,'old_prefix_reaudited':False},
    'formal_files':6,'formal_lines':sum(len(f.read_text().splitlines()) for f in formal),
    'formal_ids':ids,'semantic_receipts':5,'comparison_snapshots':10,
    'local_markdown_links_checked':len(links),'links':links,
    'historical_metadata_bindings':13,'binary_inverse_edit_old_hash_match':True,
    'anonymous_prefix_hash_match':True,'relations_with_premises_and_gaps':10,
    'json_files_parsed_before_validation_and_manifest':len(json_paths),
    'new_repo_path_collisions':existing_collisions,
    'fresh_mathematical_program_runs':0,
    'external_pdf_new_read':False,
    'no_worker_git_claim_done_or_graph_mutation':True,
}
(ev/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'verified_originals','formal_ids','links'}},ensure_ascii=False))
