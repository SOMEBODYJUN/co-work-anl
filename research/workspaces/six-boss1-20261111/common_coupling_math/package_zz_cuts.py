"""Package independently audited fixed ZZ rows; do not optimize any LP."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
AUDITS=(HERE/'round2-boolean-audit.json',HERE/'sorting13853-boolean-audit.json')


def main():
    audits=[json.loads(p.read_text()) for p in AUDITS]
    assert len({a['original_columns_sha256'] for a in audits})==1
    points=[]
    for a in audits:
        p=Path(a['input_path']);raw=p.read_bytes()
        assert sha256(raw).hexdigest()==a['input_sha256']
        points.append([F(c['weight']) for c in json.loads(raw)['columns'][:4849]])
    unique={};records=[];cuts=[]
    for ai,a in enumerate(audits):
        for r in a['known_ZZ_frechet_bounds_at_this_point']:
            row=r['row']
            assert all(0<=j<4849 for j,v in row)
            value=sum((F(v)*points[ai][j] for j,v in row),F())
            assert value==F(r['value'])==F(r['direct_frechet_value'])
            fp=sha256(json.dumps(row,separators=(',',':')).encode()).hexdigest()
            index=None
            if row:
                if fp not in unique:
                    unique[fp]=len(cuts)
                    values=[sum((F(v)*point[j] for j,v in row),F()) for point in points]
                    cuts.append({'name':'ZZ-Frechet:'+str(len(cuts)),
                                 'row':row,'sparse_sha256':fp,'source_records':[],
                                 'values_at_inputs':list(map(str,values))})
                index=unique[fp]
                assert cuts[index]['row']==row
                cuts[index]['source_records'].append([ai,r['name']])
            records.append({'audit':ai,'class':r['name'],'unique_cut':index,
                            'input_value':str(value),'sparse_sha256':fp})
    out={'scope':'Valid fixed-16hist ZZ necessary cuts; neither an SPE nor a universal welfare theorem',
         'direction':'dot(row,x) >= 0','columns':4849,
         'original_columns_sha256':audits[0]['original_columns_sha256'],
         'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
         'audits':[{'path':str(p),'sha256':sha256(p.read_bytes()).hexdigest(),
                    'input_path':a['input_path'],'input_sha256':a['input_sha256'],
                    'generator_sha256':a['source_sha256'],'W':a['point_W'],
                    'nonempty_classes':a['ZZ_nonempty_literal_classes'],
                    'negative_own_selected_rows':a['ZZ_negative_count']}
                   for p,a in zip(AUDITS,audits)],
         'record_count':len(records),'zero_self_records':sum(r['unique_cut'] is None for r in records),
         'distinct_nonzero_cut_count':len(cuts),
         'negative_unique_cuts_at_inputs':[sum(F(c['values_at_inputs'][i])<0 for c in cuts) for i in range(len(audits))],
         'records':records,'cuts':cuts}
    dest=HERE/'zz-cuts-two-points.json'
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','cuts')},ensure_ascii=False))

if __name__=='__main__':main()
