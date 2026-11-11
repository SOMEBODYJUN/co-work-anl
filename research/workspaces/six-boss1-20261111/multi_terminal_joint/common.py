"""Standalone parsing and literal-index bookkeeping for the terminal joint audit."""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
WORK = HERE.parent
POINT = WORK / 'zz_closure_lp/round2/augmented_lp_exact.json'
EXPECTED_POINT_SHA = 'bf47390017e37f49f47a8f89126eb8e812982e16bd535adb555f042c178a2ca3'
EXPECTED_COLUMNS_SHA = 'afce2dcdff01e9393c04e317ee6bd52f5c0b378daedd92816647412243362460'
NODES = tuple((f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i != j)
STATES = ((0,0),(0,1),(1,0),(1,1))


def sha(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def canonical(xs):
    seen = {}
    return tuple(seen.setdefault(x,len(seen)) for x in xs)


def pair_class(e,f):
    return (e[0],f[0],canonical(e[1:]+f[1:]))


def parse(path=POINT):
    raw = path.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED_POINT_SHA
    point = json.loads(raw)
    cols = point['columns'][:4849]
    desc_sha = sha256(json.dumps([{k:v for k,v in c.items() if k!='weight'} for c in cols],
                                 sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    assert desc_sha == EXPECTED_COLUMNS_SHA
    masses = tuple(F(c['weight']) for c in cols)
    assert len(cols)==4849 and min(masses)>=0
    hist = {}
    groups = defaultdict(dict)
    current = None
    for j,c in enumerate(cols):
        if c['kind']=='hist':
            current = j
            hist[j] = c
        elif c['kind']=='joint-reply':
            rawg = c['group']
            g = (rawg[0],rawg[1],tuple(rawg[2]),tuple(rawg[3]))
            state = tuple(c['state'])
            assert state not in groups[current].setdefault(g,{})
            groups[current][g][state] = j
    assert len(hist)==16 and sum(map(len,groups.values()))==194
    for hi,gs in groups.items():
        for g,ids in gs.items():
            assert set(ids)==set(STATES[1:])
            assert sum(masses[j] for j in ids.values())<=masses[hi]
    return point,cols,masses,hist,groups


def words(h):
    out = tuple(w for w,n in zip(product(range(2),repeat=3),h['hist']) for _ in range(n))
    assert len(out)==6
    return out


def node_group(e,ws):
    return e[0],int(e[1]==e[2]),ws[e[1]],ws[e[2]]


def marginal(hi,ids,masses):
    b,c,d = (masses[ids[s]] for s in STATES[1:])
    return (masses[hi]-b-c-d,b,c,d)


def add(row,j,value):
    if value:
        row[j]=row.get(j,F())+value
        if not row[j]:
            del row[j]


def row_value(row,masses):
    return sum((v*masses[j] for j,v in row.items()),F())


def potential_row(hi,ids,pot):
    row={hi:sum((p[0] for p in pot),F())}
    for ix,pp in zip(ids,pot):
        for s,p in zip(STATES[1:],pp[1:]):
            add(row,ix[s],p-pp[0])
    return {j:v for j,v in row.items() if v}


def metadata():
    return {'input_path':str(POINT),'input_sha256':sha(POINT),
            'original_columns_sha256':EXPECTED_COLUMNS_SHA,
            'parser_path':str(Path(__file__)),'parser_sha256':sha(Path(__file__))}


def dump(path,obj):
    Path(path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
