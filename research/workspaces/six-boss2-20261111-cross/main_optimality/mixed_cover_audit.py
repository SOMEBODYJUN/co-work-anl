"""Exact OPT6 inequalities on permutation-averaged six-label menus.

The three bits use (T_i,B_i,C_i), with T=4,B=2,C=1.
Every selected labeled menu has at most six entries. Average its valid
coverage <= OPT6 inequality over the SAME permutation of comparison indices.
This averages inequalities; it does not assume a symmetric strategy.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations_with_replacement
import json, hashlib, argparse

@lru_cache(None)
def probability_miss(hist, masks):
    if not masks: return F(1)
    n=sum(hist)
    ans=F(0)
    for word,count in enumerate(hist):
        if count and not(word & masks[0]):
            tail=list(hist);tail[word]-=1
            ans+=F(count,n)*probability_miss(tuple(tail),masks[1:])
    return ans

def generate_rows(columns):
    hcols=[(i,c) for i,c in enumerate(columns) if c['kind']=='hist']
    patterns=[]
    for masks in combinations_with_replacement(range(8),6):
        cost=sum(x.bit_count() for x in masks)
        if cost<=6:patterns.append((masks,cost))
    rows=[]
    for masks,cost in patterns:
        for actual in range(64):
            if actual.bit_count()+cost!=6:continue
            coeffs={}
            for i,c in hcols:
                union_actual=any(bit=='1' and (actual & (1<<j)) for j,bit in enumerate(c['actual_bits']))
                coverage=F(1) if union_actual else 1-probability_miss(tuple(c['hist']),masks)
                co=F(c['d']>0)-coverage
                if co: coeffs[i]=co
            rows.append((actual,masks,coeffs))
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--point',required=True);ap.add_argument('--output',required=True);args=ap.parse_args()
    p=Path(args.point);point=json.loads(p.read_text());cols=point['columns'];x=[F(c['weight']) for c in cols]
    rows=generate_rows(cols);unique={}
    records=[]
    for actual,masks,co in rows:
        key=tuple((i,str(v)) for i,v in sorted(co.items()))
        if key in unique:continue
        unique[key]=len(records)
        slack=sum((v*x[i] for i,v in co.items()),F(0))
        records.append({'actual_mask':actual,'index_masks':list(masks),'slack':str(slack),'float':float(slack),'coefficients':[[i,str(v)] for i,v in co.items()]})
    negatives=[r for r in records if F(r['slack'])<0]
    records.sort(key=lambda r:F(r['slack']))
    result={'scope':'Necessary static optimal-six-tuple inequalities; no SPE certificate','input':str(p),'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'indexed_menu_orbits':len(rows),'distinct_rows_on_current_hist':len(records),'negative_rows':len(negatives),'minimum_slack':records[0]['slack'],'minimum_record':records[0],'rows':records}
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
