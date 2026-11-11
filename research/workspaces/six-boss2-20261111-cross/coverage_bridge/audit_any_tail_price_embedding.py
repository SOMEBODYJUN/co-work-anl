#!/usr/bin/env python3
"""General-price implementation checks: k2 embedding and genuinely k3 edges."""
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path

import any_tail_price_projection as new
import balanced_price_projection as old

HERE=Path(__file__).resolve().parent


def main():
    qs=(F(0),)*17
    beta=[F(0)]*new.DP;beta[3]=F(1,2);beta[4]=F(1)
    edges={(t,c):min(new.dot(new.price_features(0,0,t,c,s,qs),beta) for s in (0,1))
           for t,c in itertools.product((0,1),repeat=2)}
    assert edges=={(0,0):0,(0,1):F(-1,2),(1,0):F(1,2),(1,1):F(1,2)}
    assert edges[0,0]+edges[1,1]!=edges[0,1]+edges[1,0]
    first=new.price_values(qs,3,F(1,2),[beta])[0]
    assert first==(F(-1,6),F(1,6))
    beta[2]=F(1)
    second=new.price_values(qs,3,F(1,2),[beta])[0]
    assert second==(F(0),F(1,2))
    # Changing a middle capacity price changes w for k3. This guards against
    # accidentally applying the special balanced k2 formula in the new path.
    assert first[1]-first[0]!=second[1]-second[0]
    report=json.loads((HERE/'new5752_balanced_prices_sources1to3.json').read_text())
    r=next(r for r in report['results'] if r['source']==3 and r['member']==1 and r['orbit']==[0,0])
    data,cols,hs,K,u=new.data_api.read_input(report['input'])
    assert hashlib.sha256(Path(report['input']).read_bytes()).hexdigest()==report['input_sha256']
    alpha=[F(r['alpha'].get(n,'0')) for n in new.prefix.NAMES]
    before=[];after=[]
    for label in new.LABELS:
        d=r['prices'].get(label,{})
        before.append([F(d.get(n,'0')) for n in old.PRICE_NAMES])
        after.append([F(d.get(n,'0')) for n in new.PRICE_NAMES])
    row_old,nold=old.exact_row(cols,hs,2,1,(0,0),F(3,4),alpha,before)
    row_new,nnew=new.exact_row(cols,hs,2,4,1,(0,0),F(3,4),alpha,after)
    assert row_new==row_old
    assert new.budgets(4,2,alpha,after)==old.budgets(4,alpha,before)
    value=sum((x*F(c['weight']) for x,c in zip(row_new,cols)),F(0))
    assert value==F(r['exact_slack'])
    out={'scope':'implementation checks only; general positivity is proved separately',
         'k3_edges':{f'{t}{c}':str(x) for (t,c),x in edges.items()},
         'k3_psi_without_middle_price':list(map(str,first)),
         'k3_psi_with_middle_price_one':list(map(str,second)),
         'k3_is_not_using_k2_balanced_formula':True,
         'k2_embedded_full_columns':len(cols),'projected_contexts':[nold,nnew],
         'embedding_input_sha256':report['input_sha256'],'embedding_exact_slack':str(value),
         'embedding_exact_slack_float':float(value)}
    (HERE/'any_tail_price_embedding_audit.json').write_text(json.dumps(out,indent=2)+'\n')
    print({k:v for k,v in out.items() if k!='embedding_exact_slack'})


if __name__=='__main__':main()
