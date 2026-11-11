"""Independent fixed-hist parser for the enlarged old R/Z terminal network."""
from __future__ import annotations
from collections import Counter,defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
WORK=HERE.parent
ROOT=HERE.parents[3]
POINT=WORK/'zz_closure_lp/round2/augmented_lp_exact.json'
MATRIX=WORK/'zz_closure_lp/round2/exact_matrix.json.gz'
NODES=tuple(e for e in product(range(2),range(6),range(6)) if e[0] or e[1]!=e[2])
STATES=((0,0),(0,1),(1,0),(1,1))
DESC_SHA='afce2dcdff01e9393c04e317ee6bd52f5c0b378daedd92816647412243362460'

def sha(p):return sha256(Path(p).read_bytes()).hexdigest()

def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

def canon(xs):
    d={};return tuple(d.setdefault(x,len(d)) for x in xs)

def pairclass(e,f):return e[0],f[0],canon(e[1:]+f[1:])

def group(raw):return raw[0],raw[1],tuple(raw[2]),tuple(raw[3])

def words(h):return tuple(w for w,n in zip(product(range(2),repeat=3),h['hist']) for _ in range(n))

def ng(e,ws):return e[0],int(e[1]==e[2]),ws[e[1]],ws[e[2]]

def add(row,col,v):
    if v:
        row[col]=row.get(col,F())+v
        if not row[col]:del row[col]

def moment(row,ids,which,v):
    ss={'q':((1,0),(1,1)),'v':((0,1),(1,1)),'t':((1,1),)}[which]
    for s in ss:add(row,ids[s],v)

def dot(row,masses):return sum((v*masses[j] for j,v in row.items()),F())

def parse(path=POINT):
    point=json.loads(path.read_bytes());cols=point['columns'][:4849]
    desc=[{k:v for k,v in c.items() if k!='weight'} for c in cols]
    descsha=sha256(json.dumps(desc,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    assert descsha==DESC_SHA
    masses=tuple(F(c['weight']) for c in cols)
    hist={};groups=defaultdict(dict);ov=defaultdict(dict);families=defaultdict(list)
    hi=None
    for i,c in enumerate(cols):
        kind=c['kind']
        if kind=='hist':hi=i;hist[i]=c
        elif kind=='joint-reply':groups[hi].setdefault(group(c['group']),{})[tuple(c['state'])]=i
        elif kind=='overlap':ov[c['hist_column']][tuple(sorted(group(g) for g in c['groups']))]=i
        elif kind=='actual-B-family-state':families[c['hist_column'],f"B{c['source']}"].append(i)
        elif kind=='maximum-root-family-state':families[c['hist_column'],'M'].append(i)
    assert len(hist)==16 and sum(map(len,groups.values()))==194
    assert min(masses)>=0
    for h,gg in groups.items():
        ws=words(hist[h]);assert len(ws)==6
        assert sum(w[0] for w in ws)==hist[h]['d']
        assert set(gg)=={ng(e,ws) for e in NODES}
        for g,ids in gg.items():
            assert set(ids)==set(STATES[1:])
            assert sum(masses[j] for j in ids.values())<=masses[h]
        assert len(ov[h])==len(gg)*(len(gg)-1)//2
        for fam in ('B2','B3','B4','M'):
            assert sum((masses[j] for j in families[h,fam]),F())==masses[h]
    assert sum((masses[j]*cols[j].get('M',0) for j in range(4849) if cols[j]['kind']=='maximum-root-family-state'),F())==masses[0]
    return point,cols,masses,hist,groups,ov,families

def marg(hi,ids,masses):
    b,c,d=(masses[ids[s]] for s in STATES[1:]);return masses[hi]-b-c-d,b,c,d

def meta(path):return {'input_path':str(path),'input_sha256':sha(path),'original_columns_sha256':DESC_SHA,'parser_sha256':sha(Path(__file__))}
