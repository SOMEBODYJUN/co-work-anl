"""Exact odd-subset upper potentials for every literal three-node ZZ cycle.

All 66 nodes remain literal. Each directed cycle is counted once, and then
all comparison-index relabelings are aggregated by a rotation-canonical
family/equality pattern. No separate-hist weighting of true IC is used.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import time

from audit_cycles import add, canonical, parse, row_value

HERE = Path(__file__).resolve().parent
ODD = tuple(mask for mask in range(64) if mask.bit_count() % 2)
STATES = ((0,1), (1,0), (1,1))


def plus_moment(row, ids, moment, weight):
    states = {'q': ((1,0),(1,1)),
              'v': ((0,1),(1,1)),
              't': ((1,1),),
              'd': ((0,1),(1,0))}[moment]
    for state in states:
        add(row, ids[state], weight)


def cycle_catalog():
    nodes = [(f,i,j) for f,i,j in product(range(2),range(6),range(6)) if f or i != j]
    assert len(nodes) == 66
    classes = {}
    cycles = []
    for i, e in enumerate(nodes):
        for j in range(i+1,len(nodes)):
            for k in range(i+1,len(nodes)):
                if j == k:
                    continue
                entries = ((i,e),(j,nodes[j]),(k,nodes[k]))
                variants = []
                for shift in range(3):
                    rotated = entries[shift:] + entries[:shift]
                    name = (tuple(x[1][0] for x in rotated),
                            canonical(tuple(t for _,n in rotated for t in n[1:])))
                    variants.append((name,tuple(x[0] for x in rotated)))
                name, literal = min(variants)
                if name not in classes:
                    classes[name] = len(classes)
                cycles.append((classes[name],*literal))
    names = [None]*len(classes)
    for name,index in classes.items():
        names[index] = name
    assert len(cycles) == 66*65*64//3
    return nodes,names,cycles


def local_envelope(hi, ids, masses):
    moments = []
    for ix in ids:
        b,c,d = (masses[ix[st]] for st in STATES)
        moments.append((c+d,b+d,d,b+c))
    q,v,t,dis = map(list,zip(*moments))
    next_v = v[1:]+v[:1]
    lower = [abs(q[i]-next_v[i]) for i in range(3)]
    free_value = sum((min(q[i],next_v[i])-t[i] for i in range(3)),F())
    best = free_value
    selected = -1
    for mask in ODD:
        value = (sum((dis[i] for i in range(3) if not (mask>>i&1)),F())
                 - sum((lower[i] for i in range(3) if mask>>(3+i)&1),F())
                 + ((mask.bit_count()-1)//2)*masses[hi])
        if value < best:
            best = value
            selected = mask
    row = {}
    if selected == -1:
        for i in range(3):
            plus_moment(row,ids[i],'t',F(-1))
            if q[i] <= next_v[i]:
                plus_moment(row,ids[i],'q',F(1))
            else:
                plus_moment(row,ids[(i+1)%3],'v',F(1))
    else:
        add(row,hi,F((selected.bit_count()-1)//2))
        for i in range(3):
            if not (selected>>i&1):
                plus_moment(row,ids[i],'d',F(1))
            if selected>>(3+i)&1:
                sign = 1 if q[i] >= next_v[i] else -1
                plus_moment(row,ids[i],'q',F(-sign))
                plus_moment(row,ids[(i+1)%3],'v',F(sign))
    assert row_value(row,masses) == best
    return best,free_value,row,selected


def audit(path):
    started = time.monotonic()
    raw,point,cols,masses,hist,groups = parse(path)
    nodes,names,cycles = cycle_catalog()
    rows = [dict() for _ in names]
    totals = [F() for _ in names]
    free = [F() for _ in names]
    per_hist = [dict() for _ in names]
    selections = [Counter() for _ in names]
    counts = Counter(c[0] for c in cycles)
    cache_sizes = []
    for hi,h in hist.items():
        words = [word for word,n in zip(product(range(2),repeat=3),h['hist']) for _ in range(n)]
        assert len(words) == 6
        group_names = sorted(groups[hi])
        group_index = {g:i for i,g in enumerate(group_names)}
        node_groups = [group_index[e[0],int(e[1]==e[2]),words[e[1]],words[e[2]]] for e in nodes]
        compressed = Counter()
        for name,a,b,c in cycles:
            triple = (node_groups[a],node_groups[b],node_groups[c])
            triple = min(triple,triple[1:]+triple[:1],triple[2:]+triple[:2])
            compressed[(name,*triple)] += 1
        local = {}
        p = sum(map(int,h['actual_bits'][:4]))
        denominator = (p+1)*(p+2)
        for (name,a,b,c),count in compressed.items():
            triple = (a,b,c)
            if triple not in local:
                ids = [groups[hi][group_names[g]] for g in triple]
                local[triple] = local_envelope(hi,ids,masses)
            value,loose,row,selected = local[triple]
            scale = F(count,denominator)
            totals[name] += scale*value
            free[name] += scale*loose
            per_hist[name][hi] = per_hist[name].get(hi,F())+scale*value
            selections[name][selected] += count
            for col,coef in row.items():
                add(rows[name],col,scale*coef)
        cache_sizes.append({'hist':hi,'compressed_terms':len(compressed),'local_triples':len(local)})
        print(json.dumps({'hist_done':hi,'seconds':round(time.monotonic()-started,3),
                          'local_triples':len(local)},ensure_ascii=False),flush=True)
    records = []
    for index,name in sorted(enumerate(names),key=lambda pair:pair[1]):
        assert row_value(rows[index],masses) == totals[index]
        improvement = free[index]-totals[index]
        assert improvement >= 0
        rec = {
            'class': name,
            'directed_literal_cycles_per_hist': counts[index],
            'value': str(totals[index]),
            'free_sum_value': str(free[index]),
            'improvement': str(improvement),
            'per_hist': [[h,str(per_hist[index].get(h,F()))] for h in hist],
            'selected_potentials_minus1_means_free': sorted(selections[index].items()),
        }
        if improvement > 0:
            rec['row'] = [[j,str(v)] for j,v in sorted(rows[index].items())]
        records.append(rec)
    original_columns_sha = sha256(json.dumps(
        [{k:v for k,v in c.items() if k!='weight'} for c in cols],
        sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    return {
        'scope': 'Three-node odd-subset necessary upper potentials; no multi-node sufficiency or SPE claim',
        'input_path': str(path.resolve()),'input_sha256':sha256(raw).hexdigest(),
        'point_W':point['W'],'point_exact_verified':point.get('exact_verified'),
        'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'parser_sha256':sha256((HERE/'audit_cycles.py').read_bytes()).hexdigest(),
        'original_columns_sha256':original_columns_sha,
        'directed_literal_cycles_per_hist':len(cycles),
        'rotation_canonical_classes':len(names),
        'odd_subsets':len(ODD),
        'negative_count':sum(F(r['value'])<0 for r in records),
        'negative_with_strict_improvement':sum(F(r['value'])<0 and F(r['improvement'])>0 for r in records),
        'negative_with_nonnegative_own_free_sum':sum(F(r['value'])<0<=F(r['free_sum_value']) for r in records),
        'improved_count':sum(F(r['improvement'])>0 for r in records),
        'minimum':min((r['value'] for r in records),key=F),
        'elapsed_seconds':time.monotonic()-started,
        'hist_compression':cache_sizes,
        'direction':'dot(row,x) >= 0',
        'records':records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('point',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    out = audit(args.point)
    args.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('records','hist_compression')},ensure_ascii=False))
    print('strictly_improved_negative',[(r['class'],r['value'],r['free_sum_value'])
                                       for r in out['records']
                                       if F(r['value'])<0 and F(r['improvement'])>0])


if __name__=='__main__':
    main()
