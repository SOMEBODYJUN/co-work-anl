#!/usr/bin/env python3
"""Reuse complete exact vectors after verifying the full original-column prefix.

The 4906 stored vectors are mathematical rows, independent of the discovery
point.  This command revalues every vector on a fresh rational point and
repeats exact full-vector baseline deduplication.  It never carries old signs.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
from audit_existing import summaries


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(row):
    return json.dumps([[int(i),str(F(v))] for i,v in sorted(row) if F(v)],separators=(',',':')).encode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--origin-audit',type=Path,default=HERE/'existing_at_13931.json')
    ap.add_argument('--point',type=Path,required=True)
    ap.add_argument('--matrix',type=Path,required=True)
    ap.add_argument('--label',required=True)
    ap.add_argument('--output-dir',type=Path,default=HERE)
    args = ap.parse_args()
    origin = json.loads(args.origin_audit.read_text())
    origin_raw = Path(origin['source']).read_bytes()
    assert sha(origin_raw) == origin['source_sha256']
    old = json.loads(origin_raw)
    vector_path = Path(origin['complete_vectors'])
    assert sha(vector_path.read_bytes()) == origin['complete_vectors_sha256']
    raw = args.point.read_bytes();matrix_raw = args.matrix.read_bytes()
    point = json.loads(raw);matrix = json.loads(gzip.decompress(matrix_raw))
    desc = lambda c:{k:v for k,v in c.items() if k!='weight'}
    assert [desc(c) for c in point['columns']] == matrix['columns']
    assert [desc(c) for c in point['columns'][:4849]] == [desc(c) for c in old['columns'][:4849]]
    weights = [F(c['weight']) for c in point['columns']]
    old_weights = [F(c['weight']) for c in old['columns']]
    assert min(weights) >= 0
    baseline = defaultdict(list)
    for index,row in enumerate(matrix['rows']):
        baseline[canonical(row)].append({'index':index,'name':matrix['row_names'][index]})
    records = []; selected = []; seen = {};duplicates = []
    with gzip.open(vector_path,'rt',encoding='utf-8') as stream:
        for index,line in enumerate(stream):
            record = json.loads(line)
            coeffs = record.pop('coefficients')
            assert not coeffs or max(i for i,_ in coeffs)<4849
            # Origin vectors were normalized to canonical Fraction strings.
            # Verify their stored complete-vector hash before using the fast key.
            encoded = json.dumps(coeffs,separators=(',',':')).encode()
            assert sha(encoded) == record['vector_sha256']
            old_value = sum((F(v)*old_weights[i] for i,v in coeffs if old_weights[i]),F())
            assert old_value == F(record['slack'])
            value = sum((F(v)*weights[i] for i,v in coeffs if weights[i]),F())
            record.update(origin_slack=record['slack'],slack=str(value),slack_float=float(value),
                          full_column_count=len(weights),baseline_matches=baseline.get(encoded,[]),
                          duplicate_of=seen.get(encoded))
            records.append(record)
            if encoded in seen:
                duplicates.append({'name':record['name'],'same_as':seen[encoded]})
            else:
                seen[encoded] = record['name']
                if value<0:
                    assert not record['baseline_matches']
                    selected.append(dict(record,coefficients=coeffs))
            if (index+1)%1000 == 0:
                print(json.dumps({'revalued':index+1}),flush=True)
    assert len(records) == origin['records']
    out = {'scope':'Fresh exact revaluation of all specified full early vectors on a new necessary-LP point; no SPE or half claim',
           'source':str(args.point.resolve()),'source_sha256':sha(raw),
           'matrix':str(args.matrix.resolve()),'matrix_sha256':sha(matrix_raw),
           'input_W':point['W'],'columns':len(weights),'original_columns':4849,
           'baseline_rows':len(matrix['rows']),'records':len(records),'distinct_vectors':len(seen),
           'negative_records':sum(F(r['slack'])<0 for r in records),'distinct_negative_vectors':len(selected),
           'original_column_descriptors_equal':True,'every_origin_value_rechecked':True,
           'per_mechanism':summaries(records),'rows':records,'selected_rows':selected,'duplicates':duplicates,
           'origin_audit':str(args.origin_audit.resolve()),'origin_audit_sha256':sha(args.origin_audit.read_bytes()),
           'complete_vectors':str(vector_path.resolve()),'complete_vectors_sha256':origin['complete_vectors_sha256']}
    args.output_dir.mkdir(parents=True,exist_ok=True)
    target = args.output_dir/f'existing_at_{args.label}.json'
    target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    pack = {k:out[k] for k in ('scope','source','source_sha256','matrix','matrix_sha256','columns','original_columns','baseline_rows','selected_rows')}
    pack.update(input_records=len(selected),distinct_rows=len(selected),duplicates=[])
    cuts = args.output_dir/f'existing_negative_cuts_{args.label}.json'
    cuts.write_text(json.dumps(pack,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('rows','selected_rows','duplicates')},ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
