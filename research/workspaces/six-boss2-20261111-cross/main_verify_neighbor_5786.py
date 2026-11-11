"""Independent derivation of the early-capacity and cross-ZZ bridge rows.

Uses count compression for the four newly generated successors and literal
ordered edge pairs for ZZ. It imports no other research code or row builder.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter,defaultdict
from functools import lru_cache
import hashlib,json,time
B=Path(__file__).resolve().parent
pp=B/'master_cuts/dynamic_5786_exact.json'
cp=B/'master_cuts/neighbor_5786_selected_13_v1.json'
point,pack=json.loads(pp.read_text()),json.loads(cp.read_text())
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
assert pack['source_sha256']==sha(pp)
submitted_report_path=B.parents[2]/pack['reconstruction_report']
assert sha(submitted_report_path)==pack['reconstruction_report_sha256']
submitted_report=json.loads(submitted_report_path.read_text())
assert submitted_report['point_sha256']==sha(pp)
cols=point['columns'];x=[F(c['weight']) for c in cols]
assert pack['cut_count']==len(pack['cuts'])==13 and len(cols)==pack['columns']==4849
desc=[{k:v for k,v in c.items() if k!='weight'} for c in cols]
assert hashlib.sha256(json.dumps(desc,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==pack['descriptor_sha256']
start=time.time()
def pay(num,den):return F(num)/den if num else F(0)
def rowhash(row):return hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest()

@lru_cache(None)
def phi(p,t,q):
    # Every count 0..3 is realized by a binary triple, and all three middle
    # capacity coefficients agree. Thus 8 count states cover all 16 literals.
    candidates=[]
    for count in range(4):
        for g in (0,1):
            z=p+t+count+g
            candidates.append(pay(t,z)-pay(g,z)/16+F(3*count+4*g,64)+F(q,16*(p+t+count+1)))
    ans=min(candidates)
    closed=F(25,64)*t+F(1,16)*q-F(1,20)*t*q if p==0 else F(109,320)*t+F(1,32)*q-F(1,48)*t*q
    assert ans==closed
    return ans
for p,t,q in product((0,1),repeat=3):phi(p,t,q)

cap=[F(0)]*len(cols);cap[0]=F(13,64)
hist_columns={j:c for j,c in enumerate(cols) if c['kind']=='hist'}
family_masses=defaultdict(F)
for j,c in enumerate(cols):
    if c['kind']=='hist':
        a=tuple(map(int,c['actual_bits']))
        cap[j]=pay(a[1],sum(a))
    elif c['kind']=='maximum-root-family-state':
        hi=c['hist_column'];a=tuple(map(int,cols[hi]['actual_bits']))
        assert hi in hist_columns and len(c['hidden'])==5
        assert c['M'] in (0,1) and all(v in (0,1) for v in c['hidden'])
        # hidden[0] is the first true successor of root-forced M, not M itself.
        cap[j]=-phi(a[0],c['hidden'][0],a[5])
        family_masses[hi]+=x[j]
assert dict(family_masses)=={j:x[j] for j in hist_columns}

blocks=[]
for j,c in enumerate(cols):
    if c['kind']=='hist':blocks.append([j,c,{}])
    elif c['kind']=='joint-reply':
        f,d,wi,wj=c['group']
        group=(f,d,tuple(wi),tuple(wj))
        blocks[-1][2].setdefault(group,{})[tuple(c['state'])]=j
edges=tuple((f,i,j) for f in (0,1) for i in range(6) for j in range(6) if f==1 or i!=j)
assert len(edges)==66
def equality_pattern(items):
    labels=[]
    return tuple(labels.index(v) if v in labels else (labels.append(v) or len(labels)-1) for v in items)

degree_checks=0
endpoint_choices=Counter()
def zzrow(rec):
    global degree_checks
    fs,ft,pat=rec['class']
    pairs=tuple((e,f) for e in edges for f in edges if e!=f and e[0]==fs and f[0]==ft and equality_pattern(e[1:]+f[1:])==tuple(pat))
    assert len(pairs)==rec['literal_pairs']>0
    row=[F(0)]*len(cols)
    for hi,h,groups in blocks:
        words=tuple(w for w,n in zip(product((0,1),repeat=3),h['hist']) for _ in range(n))
        a=tuple(map(int,h['actual_bits']));P=sum(a[:4]);den=(P+1)*(P+2)
        def group(e):return (e[0],int(e[1]==e[2]),words[e[1]],words[e[2]])
        all_in_group=defaultdict(list)
        for e in edges:all_in_group[group(e)].append(e)
        joint_pairs=defaultdict(list)
        for e,f in pairs:joint_pairs[group(e),group(f)].append((e,f))
        for (g,k),subset in joint_pairs.items():
            left,right=Counter(e for e,f in subset),Counter(f for e,f in subset)
            assert len(subset)%len(all_in_group[g])==0 and len(subset)%len(all_in_group[k])==0
            assert all(left[e]==F(len(subset),len(all_in_group[g])) for e in all_in_group[g])
            assert all(right[f]==F(len(subset),len(all_in_group[k])) for f in all_in_group[k])
            degree_checks+=2
        # Reconstruct coefficients one literal pair at a time, independently
        # of the discovering program's grouped multiplicity expansion.
        for e,f in pairs:
            sg,tg=groups[group(e)],groups[group(f)]
            assert set(sg)==set(tg)=={(0,1),(1,0),(1,1)}
            for st in ((0,1),(1,1)):
                row[sg[st]]+=F(1,P+1)
                row[tg[st]]-=F(1,P+1)
            row[sg[1,1]]-=F(1,den)
            q=x[sg[1,0]]+x[sg[1,1]]
            v=x[tg[0,1]]+x[tg[1,1]]
            assert q>=0 and v>=0
            if q<=v:
                endpoint_choices['source_R']+=1
                row[sg[1,0]]+=F(1,den);row[sg[1,1]]+=F(1,den)
            else:
                endpoint_choices['target_Z']+=1
                row[tg[0,1]]+=F(1,den);row[tg[1,1]]+=F(1,den)
    return row

rows=[]
for index,rec in enumerate(pack['cuts']):
    if rec['family']=='early-capacity-H0':
        assert index==0 and rec['budget']=='u2 + 13 K / 64'
        raw=cap
        scale=F(1)
        for q in submitted_report['capacity_bridge']['table']:assert phi(q['p'],q['t'],q['q'])==F(q['phi'])
    else:
        assert rec['family']=='ZZ-Frechet'
        raw=zzrow(rec)
        scale=F(1,rec['literal_pairs'])
    assert scale==F(rec['normalization_scale'])>0
    assert rowhash(raw)==rec['original_row_sha256']
    raw_slack=sum((a*b for a,b in zip(raw,x)),F(0))
    assert raw_slack==F(rec['original_exact_slack'])<0
    row=[v*scale for v in raw]
    saved=[F(0)]*len(cols)
    sparse=rec.get('row_nonzero',rec.get('sparse_row'))
    assert len({i for i,v in sparse})==len(sparse)
    for i,v in sparse:saved[i]=F(v)
    assert row==saved and rowhash(row)==rec['row_sha256']
    slack=sum((a*b for a,b in zip(row,x)),F(0))
    assert slack==F(rec['exact_slack'])==scale*raw_slack<0
    rows.append({'index':index,'family':rec['family'],'class':rec.get('class'),
                 'all_4849_coefficients_equal':True,'exact_slack':str(slack),
                 'row_sha256':rec['row_sha256'],'scale':str(scale)})
assert len({r['row_sha256'] for r in rows})==13
verified=json.loads((B/'main_verify_dynamic_5786.json').read_text())
assert verified['status']=='PASS' and verified['point_sha256']==sha(pp)
out={'status':'PASS','scope':'Independent 13-row reconstruction from source IC plus four capacities/one true last query, and literal ZZ IC plus valid Frechet majorants; all rows bound to current 5786, no complete SPE assertion',
     'point_sha256':sha(pp),'pack_sha256':sha(cp),'columns':len(cols),'rows':rows,
     'capacity_visible_types':8,'capacity_count_candidates_checked':64,'capacity_family_marginals_exact':True,
     'ZZ_regular_degree_checks':degree_checks,'ZZ_literal_endpoint_choices':dict(endpoint_choices),'seconds':time.time()-start}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
