"""Exact independent reconstruction of old R terminal rows and RR envelopes."""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
import argparse,ast,gzip,json
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
from common import *

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--point',type=Path,default=POINT)
    ap.add_argument('--matrix',type=Path,default=MATRIX);ap.add_argument('--output',type=Path,default=HERE/'interface_audit_19556.json')
    args=ap.parse_args();point,cols,masses,hist,groups,ov,families=parse(args.point)
    matrix=json.load(gzip.open(args.matrix,'rt'))
    assert matrix['columns'][:4849]==[{k:v for k,v in c.items() if k!='weight'} for c in cols]
    matrix_rows={n:(i,{j:F(v) for j,v in rr}) for i,(n,rr) in enumerate(zip(matrix['row_names'],matrix['rows']))}
    counts=Counter(pairclass(e,f) for e in NODES for f in NODES)
    rows=defaultdict(dict);hist_values=defaultdict(dict)
    for hi,h in hist.items():
        ws=words(h);p=sum(map(int,h['actual_bits'][:3]));P=sum(map(int,h['actual_bits'][:4]));D=(P+1)*(P+2)
        local=defaultdict(dict)
        for e in NODES:
            ge=ng(e,ws);ie=groups[hi][ge]
            de=p+ws[e[1]][0]+ws[e[2]][1+e[0]]+1
            assert 1<=de<=6
            for f in NODES:
                gf=ng(f,ws);jf=groups[hi][gf];cl=pairclass(e,f)
                rr=local['R-R',cl];moment(rr,ie,'q',F(1,de));moment(rr,jf,'q',F(-1,de))
                rz=local['R-Z',cl];moment(rz,ie,'q',F(1,de));moment(rz,jf,'v',F(-1,de))
                zr=local['Z-R-envelope',cl]
                moment(zr,ie,'v',F(1,P+1));moment(zr,jf,'q',F(-1,P+1));moment(zr,ie,'t',F(-1,D))
                if ge==gf:moment(zr,ie,'q',F(1,D))
                else:add(zr,ov[hi][tuple(sorted((ge,gf)))],F(1,D))
        for key,row in local.items():
            rows[key]
            hist_values[key][hi]=dot(row,masses)
            for j,v in row.items():add(rows[key],j,v)
    records=[]
    for (kind,cl),row in sorted(rows.items()):
        oldkind={'R-R':'new-new','R-Z':'R-Z','Z-R-envelope':'Z-R'}[kind]
        expected_name=str((oldkind,*cl));index,saved=matrix_rows[expected_name]
        assert row==saved,(kind,cl,index)
        value=dot(row,masses);assert value>=0
        records.append({'kind':kind,'class':cl,'literal_queries':counts[cl],
            'value':str(value),'per_literal_symmetrized':str(value/counts[cl]),
            'matrix_row':index,'matrix_name':expected_name,'exact_existing_row_match':True,
            'per_hist':[[h,str(hist_values[kind,cl][h])] for h in hist],
            'row':[[j,str(v)] for j,v in sorted(row.items())]})
    overlap_cols={j for j,c in enumerate(cols) if c['kind']=='overlap'}
    bad=[]
    for i,(name,row) in enumerate(zip(matrix['row_names'],matrix['rows'])):
        for j,v in row:
            if j in overlap_cols and F(v)<0 and not name.startswith('overlap-upper:'):
                bad.append([i,name,j,v])
    assert not bad
    hist_records=[]
    for hi,h in hist.items():
        hist_records.append({'column':hi,'actual_bits':h['actual_bits'],'d':h['d'],'hist':h['hist'],
            'mass':str(masses[hi]),'groups':len(groups[hi]),'overlap_upper_auxiliaries':len(ov[hi]),
            'family_state_counts':{fam:len(families[hi,fam]) for fam in ('B2','B3','B4','M')}})
    out=meta(args.point)|{'source_sha256':sha(Path(__file__)),'matrix_sha256':sha(args.matrix),
        'scope':'Existing exact marginal-only R-R/R-Z rows and surrogate Z-R rows; no new joint cut',
        'column_kind_counts':dict(Counter(c['kind'] for c in cols)),
        'family_marginals_exact':True,'maximum_root_K_identity_exact':True,
        'overlap_sign_exceptions':bad,'classes_per_query_type':len(counts),'exact_matched_rows':len(records),
        'negative_marginal_rows':sum(F(r['value'])<0 for r in records if r['kind']!='Z-R-envelope'),
        'histograms':hist_records,'records':records}
    dump(args.output,out)
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','histograms')},ensure_ascii=False))
    for kind in ('R-R','R-Z','Z-R-envelope'):
        kk=[r for r in records if r['kind']==kind]
        print(kind,'zero',sum(F(r['value'])==0 for r in kk),'minimum',min(float(F(r['per_literal_symmetrized'])) for r in kk))

if __name__=='__main__':main()
