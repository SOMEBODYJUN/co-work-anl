"""Exact input-schema checks only; does not import the projected-row generator."""
from pathlib import Path
from itertools import product
from collections import Counter
from fractions import Fraction as F
import json,hashlib
HERE=Path(__file__).resolve().parent
path=HERE/'related/combined_branch_latest_exact.json'
p=json.loads(path.read_text());cols=p['columns'];PAT=tuple(product(range(2),repeat=3))
assert cols[0]['kind']=='K'
assert len(cols)==1905
weights=[F(c['weight']) for c in cols]
assert all(w>=0 for w in weights)
blocks=[];current=None
for index,c in enumerate(cols):
    if c['kind']=='hist':
        assert len(c['actual_bits'])==6 and set(c['actual_bits'])<=set('01')
        assert len(c['hist'])==8 and all(isinstance(n,int) and n>=0 for n in c['hist'])
        assert sum(c['hist'])==6
        assert c['d']==sum(word[0]*n for word,n in zip(PAT,c['hist']))
        current={'index':index,'hist':c,'groups':{}}
        blocks.append(current)
    elif c['kind']=='joint-reply':
        assert current is not None
        fam,diag,wi,wj=c['group'];g=(fam,diag,tuple(wi),tuple(wj));state=tuple(c['state'])
        assert fam in (0,1) and diag in (0,1) and not (fam==0 and diag==1)
        assert tuple(wi) in PAT and tuple(wj) in PAT and state in ((0,1),(1,0),(1,1))
        assert state not in current['groups'].setdefault(g,{})
        current['groups'][g][state]=F(c['weight'])
assert len(blocks)==16
checks=[];group_count=0;implicit_zero=0
states={(member,orb):{} for member in (0,1) for orb in ((0,0),(1,0),(1,1))}
for block in blocks:
    h=block['hist'];hm=F(h['weight']);hc=dict(zip(PAT,h['hist']));expected=set()
    for fam,diag in ((0,0),(1,0),(1,1)):
        for wi in PAT:
            for wj in PAT:
                number=hc[wi] if diag and wi==wj else 0 if diag else hc[wi]*hc[wj]-(hc[wi] if wi==wj else 0)
                if number:expected.add((fam,diag,wi,wj))
    assert set(block['groups'])==expected
    for g,vals in block['groups'].items():
        assert set(vals)=={(0,1),(1,0),(1,1)}
        z=hm-sum(vals.values());assert z>=0
        implicit_zero+=int(z>0);group_count+=1
    counts={}
    for orb in ((0,0),(1,0),(1,1)):
        ct=6 if orb[1] else 30
        pairs=[]
        words=[word for word,n in hc.items() for _ in range(n)]
        for i in range(6):
            for j in range(6):
                if (i==j)!=bool(orb[1]):continue
                pairs.append((orb[0],orb[1],words[i],words[j]))
        assert len(pairs)==ct
        counts[str(orb)]=len(pairs)
        for member in (0,1):
            st=states[member,orb]
            for g in pairs:
                vals=block['groups'][g]
                one=sum(v for state,v in vals.items() if state[member])
                assert 0<=one<=hm
                for t,mass in ((0,hm-one),(1,one)):
                    key=(h['actual_bits'],h['d'],t)
                    st[key]=st.get(key,F())+mass/ct
    checks.append({'column':block['index'],'actual_bits':h['actual_bits'],'d':h['d'],'groups':len(block['groups']),'weight':h['weight'],'orbit_edge_counts':counts})
assert group_count==194
hist_by_index={b['index']:b for b in blocks}
for index,c in enumerate(cols):
    if c['kind']=='overlap':
        block=hist_by_index[c['hist_column']]
        marg=[]
        for group in c['groups']:
            g=(group[0],group[1],tuple(group[2]),tuple(group[3]))
            vals=block['groups'][g]
            marg.append(sum(v for st,v in vals.items() if st[0]))
        assert F(c['weight'])<=min(marg)
O=sum(F(b['hist']['weight']) for b in blocks if b['hist']['d']>0)
W=sum(F(b['hist']['weight']) for b in blocks if '1' in b['hist']['actual_bits'])
assert O==F(p['O'])==1 and W==F(p['W'])
report={'scope':'input schema, orbit normalization, marginal bounds, O/W only; no reconstruction of historical 5180 rows or SPE',
'source_id':'10ef4a8ec398c9fa7aac','bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
'columns':len(cols),'kinds':dict(Counter(c['kind'] for c in cols)),'positive_kinds':dict(Counter(c['kind'] for c in cols if F(c['weight'])>0)),
'nonnegative_columns':len(cols),'complete_joint_groups':group_count,'positive_implicit_00_groups':implicit_zero,'overlap_bounds_checked':1306,
'hist_blocks':checks,'O':str(O),'W':str(W),
'visible_state_counts':[{'member':member,'orb':list(orb),'positive_states':sum(v>0 for v in st.values()),'total_mass':str(sum(st.values()))} for (member,orb),st in states.items()],
'original_module_imports':0,'solver_calls':0,'cut_evaluations':0}
(HERE/'input-interface-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='hist_blocks'},ensure_ascii=False,indent=2))
