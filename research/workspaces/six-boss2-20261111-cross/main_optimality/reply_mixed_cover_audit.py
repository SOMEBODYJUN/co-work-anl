"""Exact six-slot cover tests with a named R_e/Z_e and five old slots.
All comparison-index relabelings are averaged simultaneously. R/Z remain
shared named topics; a joint-reply state is not split into independent bits.
No SPE claim is made about the audited mass vector.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement,product
from collections import defaultdict
import json,hashlib,argparse,time
from mixed_cover_audit import probability_miss

def word(bits):return 4*bits[0]+2*bits[1]+bits[2]

def decode(cols):
    blocks=[];cur=None
    for i,c in enumerate(cols):
        if c['kind']=='hist':
            cur={'index':i,'hist':tuple(c['hist']),'actual':sum((int(b)<<j) for j,b in enumerate(c['actual_bits'])),'d':c['d'],'mass':F(c['weight']),'groups':defaultdict(dict)};blocks.append(cur)
        elif c['kind']=='joint-reply':
            a,d,wi,wj=c['group'];cur['groups'][(a,d,word(wi),word(wj))][tuple(c['state'])]=(i,F(c['weight']))
    return blocks

def groups_for(block,orb,selected):
    hist=block['hist'];fam,diag=orb;ct=6 if diag else 30
    out=[]
    for (ff,dd,wi,wj),states in block['groups'].items():
        if (ff,dd)!=orb:continue
        count=hist[wi] if diag else hist[wi]*(hist[wj]-(wi==wj))
        rem=list(hist);rem[wi]-=1
        if not diag:rem[wj]-=1
        selected_states=[(i,w) for (r,z),(i,w) in states.items() if ((selected&1 and r) or (selected&2 and z))]
        missmass=block['mass']-sum((w for i,w in selected_states),F(0))
        assert missmass>=0
        out.append((wi,wj,tuple(rem),F(count,ct),missmass,selected_states))
    assert sum(g[3] for g in out)==1
    return out

def specs(diag,newcost):
    for anchors in product(range(8),repeat=1 if diag else 2):
        for remain in combinations_with_replacement(range(8),5 if diag else 4):
            cost=sum(m.bit_count() for m in anchors+remain)
            nactual=6-newcost-cost
            if 0<=nactual<=6:yield anchors,remain,nactual

def build_row(blocks,orb,selected,anchors,remain,actual):
    row={}
    for b in blocks:
        baseline=F(0)
        if not actual&b['actual']:
            for wi,wj,rem,prob,missmass,states in groups_for(b,orb,selected):
                if wi&anchors[0] or (not orb[1] and wj&anchors[1]):continue
                miss=prob*probability_miss(rem,remain)
                baseline+=miss
                for i,w in states:
                    if miss:row[i]=row.get(i,F(0))-miss
        co=F(b['d']>0)-1+baseline
        if co:row[b['index']]=row.get(b['index'],F(0))+co
    return {i:v for i,v in row.items() if v}

def audit(point_path,out_path):
    start=time.time();p=Path(point_path);point=json.loads(p.read_text());cols=point['columns'];blocks=decode(cols)
    constant=sum((F(b['d']>0)*b['mass']-b['mass'] for b in blocks),F(0))
    masks_by_count={c:[a for a in range(64) if a.bit_count()==c] for c in range(7)}
    checked=0;neg=[];best=None
    for orb in [(0,0),(1,0),(1,1)]:
        for selected in [1,2,3]:
            group_lists=[groups_for(b,orb,selected) for b in blocks]
            for anchors,remain,nactual in specs(orb[1],selected.bit_count()):
                uncovered=[]
                for b,gs in zip(blocks,group_lists):
                    v=F(0)
                    for wi,wj,rem,prob,missmass,states in gs:
                        if wi&anchors[0] or (not orb[1] and wj&anchors[1]):continue
                        v+=prob*probability_miss(rem,remain)*missmass
                    uncovered.append(v)
                for actual in masks_by_count[nactual]:
                    slack=constant+sum((v for b,v in zip(blocks,uncovered) if not actual&b['actual']),F(0))
                    checked+=1
                    rec={'orb':list(orb),'selected_reply_mask':selected,'anchor_masks':list(anchors),'remaining_index_masks':list(remain),'actual_mask':actual,'slack':str(slack),'float':float(slack)}
                    if best is None or slack<F(best['slack']):best=rec
                    if slack<0:neg.append(rec)
    # Build exact coefficient rows only where useful, independently re-evaluate.
    unique={};rows=[];x=[F(c['weight']) for c in cols]
    for rec in sorted(neg,key=lambda r:F(r['slack'])):
        row=build_row(blocks,tuple(rec['orb']),rec['selected_reply_mask'],tuple(rec['anchor_masks']),tuple(rec['remaining_index_masks']),rec['actual_mask'])
        assert sum((v*x[i] for i,v in row.items()),F(0))==F(rec['slack'])
        key=tuple((i,str(v)) for i,v in sorted(row.items()))
        if key in unique:continue
        unique[key]=1;rows.append({**rec,'coefficients':list(map(list,key))})
    result={'scope':'Static OPT6 six-slot inequalities with same-edge R/Z jointly retained; not SPE','input':str(p),'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'tested_menu_orbits':checked,'negative_menu_orbits':len(neg),'distinct_negative_rows':len(rows),'minimum_record':best,'negative_rows':rows,'elapsed_seconds':time.time()-start}
    Path(out_path).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='negative_rows'},ensure_ascii=False,indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--point',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();audit(a.point,a.output)
