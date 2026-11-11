#!/usr/bin/env python3
"""Freeze full-vector deduplicated union and supplement to the first 12 rows."""
from fractions import Fraction as F
import hashlib,json
from pathlib import Path
import sys
sys.dont_write_bytecode=True

HERE=Path(__file__).resolve().parent
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(row):
    return json.dumps([[int(i),str(F(v))] for i,v in sorted(row) if F(v)],separators=(',',':')).encode()

priority_path=HERE/'priority_named_discounted_M1_19556.json'
priority_raw=priority_path.read_bytes();priority=json.loads(priority_raw)
assert sha(priority_raw)=='7aefad539b2e01a1894cbbf744470624e1312dca39f41a041a5299064a8cca4b'
priority_keys={canonical(r['coefficients']):r['name'] for r in priority['selected_rows']}
assert len(priority_keys)==12
packs=[];seen={};rows=[];duplicates=[]
for name in ('selected_named_two_state_19556.json','selected_named_four_state_19556.json'):
    path=HERE/name;raw=path.read_bytes();data=json.loads(raw)
    assert data['source_sha256']==priority['source_sha256']
    assert data['matrix_sha256']==priority['matrix_sha256']
    packs.append({'path':str(path.resolve()),'sha256':sha(raw),'input_rows':len(data['selected_rows'])})
    for record in data['selected_rows']:
        assert F(record['slack'])<0 and record['independent_full_vector_equal']
        assert not record['baseline_matches']
        key=canonical(record['coefficients'])
        assert sha(key)==record['vector_sha256']
        if key in seen:
            duplicates.append({'name':record['name'],'same_as':seen[key]})
            continue
        seen[key]=record['name'];rows.append(record)
assert set(priority_keys)<=set(seen)
assert len(rows)==22 and len(duplicates)==3
common={k:priority[k] for k in ('source','source_sha256','input_W','matrix','matrix_sha256','baseline_rows','columns','original_columns')}
common.update(scope='Full-vector deduplicated union of independently audited named two/four-state same-source rows at ZZ19556; no SPE or half claim',
              origin_audited_packs=packs,priority_pack=str(priority_path.resolve()),priority_pack_sha256=sha(priority_raw),
              prior_priority_rows=12,all_prior_priority_vectors_recovered=True,
              all_nonzero_coordinates_below_4849=True,
              generator_sha256=sha(Path(__file__).read_bytes()))
out=dict(common,input_records=25,distinct_rows=22,selected_rows=rows,duplicates=duplicates)
allpath=HERE/'selected_all_named_19556.json';allpath.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
new=[r for r in rows if canonical(r['coefficients']) not in priority_keys]
assert len(new)==10
supp=dict(common,input_records=10,distinct_rows=10,selected_rows=new,duplicates=[],
          supplement_only=True,union_pack=str(allpath.resolve()),union_pack_sha256=sha(allpath.read_bytes()))
suppath=HERE/'supplemental_ten_named_19556.json';suppath.write_text(json.dumps(supp,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'union':str(allpath),'union_sha256':sha(allpath.read_bytes()),'distinct_rows':22,
                  'supplement':str(suppath),'supplement_sha256':sha(suppath.read_bytes()),'supplement_rows':10,
                  'duplicates':duplicates},ensure_ascii=False))

