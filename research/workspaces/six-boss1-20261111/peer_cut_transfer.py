"""Main revalues reviewed Boss2 332/616/shared-terminal rows on our 19578 point.

Full descriptors, source point fingerprints and original exact slacks are
checked before transferring a vector.  A negative result separates this
necessary point only.  Mathematical contracts were read separately by Main.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import gzip
import json

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
PEER=REPO/'research/workspaces/six-boss2-20261111-cross'
OUT=HERE/'peer_cut_transfer'
PACKS=[
    ('common332-5744','joint_requery/portfolio_selected_5744.json'),
    ('common332-5752','joint_requery/portfolio_selected_5752.json'),
    ('shared-terminal-5752','coverage_bridge/selected_prefix_tail_5752.json'),
    ('cross616-5775','joint_requery/cross_pairs_selected_5775_v1.json'),
    ('cross616-5783','joint_requery/cross_pairs_selected_5783_three_compact_v1.json'),
]


def digest(p):return sha256(p.read_bytes()).hexdigest()
def desc(c):return {k:v for k,v in c.items() if k!='weight'}
def canonical(row):
    seen={}
    for i,v in row:
        i=int(i);assert i not in seen
        if F(v):seen[i]=str(F(v))
    return [[i,seen[i]] for i in sorted(seen)]
def encoded(row):return json.dumps(row,separators=(',',':')).encode()


def main():
    pp=HERE/'discounted_augmented_lp/augmented_lp_exact.json'
    mp=HERE/'discounted_augmented_lp/exact_matrix.json.gz'
    assert digest(pp)=='a4e48a91f0e2c7b65725178d042b515c6bedf11562afdeeea2ae69b815e8f505'
    assert digest(mp)=='a95bd72e0fdc2b0b93af79b1a0e8b324b6bd1fc8f62abe8a3ce642be4bcc3936'
    point=json.loads(pp.read_bytes());matrix=json.loads(gzip.decompress(mp.read_bytes()))
    columns=point['columns'];weights=[F(c['weight']) for c in columns]
    assert list(map(desc,columns))==matrix['columns']
    baseline={encoded(canonical(row)) for row in matrix['rows']}
    records=[];selected=[];seen={};sources=[]
    for mechanism,name in PACKS:
        path=PEER/name;pack=json.loads(path.read_bytes())
        source_name=pack.get('source_path',pack.get('input'))
        source_path=Path(source_name)
        if not source_path.is_absolute():
            source_path=REPO/source_path
        elif not source_path.exists():
            # A frozen packet may name its producer's former clone.  Route
            # only the explicit same-RUN repository suffix, then verify SHA.
            marker='research/workspaces/six-boss2-20261111-cross/'
            assert marker in source_name
            source_path=REPO/(marker+source_name.split(marker,1)[1])
        source_hash=pack.get('source_sha256',pack.get('input_sha256'))
        assert digest(source_path)==source_hash,(name,'source SHA')
        old=json.loads(source_path.read_bytes())
        assert len(old['columns'])==4849
        assert list(map(desc,old['columns']))==list(map(desc,columns[:4849]))
        ow=[F(c['weight']) for c in old['columns']]
        per=[]
        for i,cut in enumerate(pack['cuts']):
            row=canonical(cut.get('sparse_row',cut.get('row_nonzero')))
            assert all(0<=j<4849 for j,_ in row)
            old_value=sum((F(v)*ow[j] for j,v in row),F())
            assert old_value==F(cut['exact_slack']),(name,i,'old slack')
            new_value=sum((F(v)*weights[j] for j,v in row),F())
            key=encoded(row)
            rec={'name':mechanism+':'+str(i),'mechanism':mechanism,
                 'source_package':str(path.relative_to(REPO)),'source_package_sha256':digest(path),
                 'source_cut_index':i,'original_exact_slack':str(old_value),
                 'slack':str(new_value),'slack_float':float(new_value),
                 'vector_sha256':sha256(key).hexdigest(),
                 'baseline_match':key in baseline,'duplicate_of':seen.get(key),
                 'coefficients':row}
            records.append(rec);per.append(new_value)
            if key not in seen:
                seen[key]=rec['name']
                if new_value<0:
                    assert key not in baseline
                    selected.append(rec)
        sources.append({'package':str(path.relative_to(REPO)),'sha256':digest(path),
            'original_point_reference':source_name,
            'source_point':str(source_path.relative_to(REPO)),'source_point_sha256':source_hash,
            'rows':len(per),'negative':sum(v<0 for v in per),
            'minimum':str(min(per)),'minimum_float':float(min(per))})
    OUT.mkdir(exist_ok=True)
    report={'scope':'Reviewed existing Boss2 mathematical rows revalued on one new Boss1 necessary point; no new mechanism or SPE claim.',
            'point':str(pp.relative_to(REPO)),'point_sha256':digest(pp),
            'matrix':str(mp.relative_to(REPO)),'matrix_sha256':digest(mp),
            'full_column_count':len(columns),'original_columns':4849,
            'all_descriptors_exactly_equal':True,'all_original_slacks_exactly_reproduced':True,
            'records':len(records),'distinct_vectors':len(seen),'distinct_negative_rows':len(selected),
            'sources':sources,'all_rows':records,'selected_rows':selected,
            'source_sha256':digest(Path(__file__))}
    (OUT/'audit_19578.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    out={k:report[k] for k in ('scope','point','point_sha256','matrix','matrix_sha256','original_columns','selected_rows')}
    out.update(columns=len(columns),baseline_rows=len(matrix['rows']),input_records=len(selected),distinct_rows=len(selected))
    (OUT/'negative_cuts_19578.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('all_rows','selected_rows')},ensure_ascii=False))


if __name__=='__main__':main()
