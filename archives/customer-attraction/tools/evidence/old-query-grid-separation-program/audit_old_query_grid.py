"""Independent exact grid aggregation and literal hidden-bit oracle.

This does not call discover(), build(), or any LP. Original psi is only
the comparison target for the finite local grid.
"""
import argparse
import hashlib
import importlib.util
import itertools
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

PAT=tuple(itertools.product((0,1),repeat=3))
GS=((0,0),(1,0),(1,1))
AA=(F(),F(1,8),F(1,4),F(1,2),F(1),F(2))
MU=(F(),F(1,2),F(1),F(2),F(4))


@lru_cache(None)
def literal(i,p,ell,t,q,mode,aa,mu):
    values=[]
    for bits in itertools.product((0,1),repeat=5-i):
        total=sum(bits);g=bits[-1];denom=p+t+total
        price=aa*(total if mode=='all' else g)/(ell+1)
        values.append((F(t,denom) if t else F())+price
                      -(mu*g/denom if g else F())
                      +mu*F(q,p+t+total-g+1))
    return min(values)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--point',type=Path,required=True)
    ap.add_argument('--cuts',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    spec=importlib.util.spec_from_file_location('original_old_query',args.source)
    original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
    point=json.loads(args.point.read_text());saved=json.loads(args.cuts.read_text())
    cols=point['columns'];weights=[F(c['weight']) for c in cols]
    assert len(cols)==1905 and min(weights)>=0
    hs=[];current=None;groups=defaultdict(list)
    for index,c in enumerate(cols):
        if c['kind']=='hist':
            a=tuple(map(int,c['actual_bits']))
            words=tuple(w for w,n in zip(PAT,c['hist']) for _ in range(n))
            assert len(a)==6 and set(a)<={0,1} and len(words)==6
            assert all(type(x) is int and x>=0 for x in c['hist'])
            assert sum(w[0] for w in words)==c['d']
            current={'index':index,'a':a,'words':words,'mass':weights[index],'joint':defaultdict(lambda:[F(),F()])}
            hs.append(current)
        elif c['kind']=='joint-reply':
            assert current is not None
            f,d,wi,wj=c['group'];key=(f,d,tuple(wi),tuple(wj))
            assert (f,d) in GS and tuple(wi) in PAT and tuple(wj) in PAT
            assert tuple(c['state']) in ((0,1),(1,0),(1,1))
            groups[current['index'],key].append(index)
            for m in range(2):current['joint'][key][m]+=weights[index]*c['state'][m]
    for (idx,key),indices in groups.items():
        assert len(indices)==3 and {tuple(cols[j]['state']) for j in indices}=={(0,1),(1,0),(1,1)}
        assert sum(weights[j] for j in indices)<=weights[idx]
    us=[sum(h['mass']*F(h['a'][i],sum(h['a'])) for h in hs if h['a'][i]) for i in range(6)]
    O=sum(h['mass'] for h in hs if sum(w[0] for w in h['words']))
    W=sum(h['mass'] for h in hs if sum(h['a']))
    assert O==F(point['O'])==1 and W==F(point['W']) and F(point['strict_half_gap'])==O-2*W
    assert len(hs)==16 and sum(w>0 for w in weights)==point['positive_columns']
    source_groups_checks=0
    for h in hs:
        for f,d in GS:
            direct=Counter((h['words'][a],h['words'][b]) for a in range(6) for b in range(6) if (a==b)==bool(d))
            target={(wi,wj):n for (ff,dd,wi,wj),n in original.groups(cols[h['index']]['hist']).items() if (ff,dd)==(f,d)}
            assert direct==target
            source_groups_checks+=1
    grids=[(mode,aa,mu) for mode,aa,mu in itertools.product(('all','last'),AA,MU)
           if not (mode=='last' and aa==0)]
    projections=0
    for i in range(5):
        for p,rest,t,q,(mode,aa,mu) in itertools.product(range(i+1),range(6-i),(0,1),(0,1),grids):
            ell=p+rest
            assert literal(i,p,ell,t,q,mode,aa,mu)==original.psi(i,p,ell,t,q,mode,aa,mu)
            projections+=1
    stats={}
    for i,member,(f,d),qi in itertools.product(range(5),range(2),GS,range(6)):
        mass=defaultdict(F)
        for h in hs:
            p=sum(h['a'][:i]);ell=sum(h['a'][:5])
            for a,b in itertools.product(range(6),repeat=2):
                if (a==b)!=bool(d):continue
                wi,wj=h['words'][a],h['words'][b];q=(wi+wj)[qi]
                m1=h['joint'].get((f,d,wi,wj),(F(),F()))[member]
                assert 0<=m1<=h['mass']
                mass[p,ell,0,q]+=h['mass']-m1
                mass[p,ell,1,q]+=m1
        stats[i,member,f,d,qi]={s:w for s,w in mass.items() if w}
    all_records=[];negative=[];classes=defaultdict(list);signs=Counter();counts_by_i=defaultdict(Counter)
    for i,member,(f,d),qi in itertools.product(range(5),range(2),GS,range(6)):
        for mode,aa,mu in grids:
            coefficient=(5-i)*aa if mode=='all' else aa
            value=(6 if d else 30)*(us[i]+coefficient*us[5])
            value-=sum(w*literal(i,*state,mode,aa,mu) for state,w in stats[i,member,f,d,qi].items())
            cut=(i,member,f,d,qi,mode,str(aa),str(mu))
            all_records.append([list(cut),str(value)])
            classes[cut[:6]].append((value,cut))
            sign='negative' if value<0 else 'zero' if value==0 else 'positive'
            signs[sign]+=1;counts_by_i[str(i)][sign]+=1
            if value<0:negative.append((value,cut))
    negative.sort();seen=set();selected=[]
    for value,cut in negative:
        if cut[:6] in seen:continue
        seen.add(cut[:6]);selected.append({'cut':list(cut),'slack':str(value)})
        if len(selected)==64:break
    assert len(all_records)==9900==saved['candidates_checked']
    assert len(negative)==saved['negative_candidates']==8
    assert selected==saved['selected']
    minima=[]
    for key,values in sorted(classes.items()):
        values.sort()
        minima.append({'structure_including_mode':list(key),'candidate_count':len(values),
                       'minimum_slack':str(values[0][0]),'minimizing_parameter_pairs':[[c[6],c[7]] for v,c in values if v==values[0][0]],
                       'negative_count':sum(v<0 for v,c in values)})
    report={'status':'PASS','scope':'exact finite 9900-grid evaluation at one necessary point; no continuous-price closure or whole-graph proof',
            'source_sha256':sha(args.source),'point_sha256':sha(args.point),'cuts_sha256':sha(args.cuts),
            'column_count':len(cols),'column_kind_counts':dict(Counter(c['kind'] for c in cols)),
            'positive_columns':sum(w>0 for w in weights),'O':str(O),'W':str(W),'actual_utilities':list(map(str,us)),
            'groups_compared':source_groups_checks,'joint_mass_groups_checked':len(groups),
            'literal_projection_comparisons':projections,'structures_without_mode':len(stats),
            'structures_with_mode':len(classes),'grid_price_pairs_all_mode':30,'grid_price_pairs_last_mode':25,
            'raw_loop_slots':10800,'zero_last_mode_skipped':900,'candidates_checked':len(all_records),
            'sign_counts':dict(signs),'sign_counts_by_source_i':{k:dict(v) for k,v in counts_by_i.items()},
            'all_grid_values_sha256':hashlib.sha256((json.dumps(all_records,separators=(',',':'))+'\n').encode()).hexdigest(),
            'negative_candidates':len(negative),'selected':selected,'selected_exact_equal_frozen':True,
            'original_discover_called':False,'original_row_8_vector_audit_delegated_to_data_object':True,
            'whole_4963_or_4971_or_5108_graph_run':False,'finite_structure_minima':minima}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('finite_structure_minima','selected')},indent=2))


if __name__=='__main__':main()
