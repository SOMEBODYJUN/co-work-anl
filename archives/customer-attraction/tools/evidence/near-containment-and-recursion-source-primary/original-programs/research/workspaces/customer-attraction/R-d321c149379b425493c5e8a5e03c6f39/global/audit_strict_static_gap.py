"""Definition-level audit; imports no solver, discovery code, numpy, or scipy.

Every compressed customer is expanded into distinct unit customers.  The full
ordered strategy is specified below independently of the discovery JSON.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,json

BASE={1:3,3:3,4:1,5:1,10:1,12:1,14:2}
LAST=((2,2,1,0),(2,0,0,0),(1,0,0,0),(0,0,0,0))
SECOND=(3,0,0,0)

def run(weights):
    customers=[]
    for mask,n in weights.items():
        customers.extend([frozenset(a for a in range(4) if mask>>a&1)]*n)
    def utility(z,i):
        return sum((F(1,sum(a in c for a in z)) for c in customers if z[i] in c),F())
    def coverage(z):return sum(any(a in c for a in z) for c in customers)
    def action(h):return 3 if not h else SECOND[h[0]] if len(h)==1 else LAST[h[0]][h[1]]
    def finish(h):
        z=tuple(h)
        while len(z)<3:z+=(action(z),)
        return z
    comparisons=[];tables={}
    for depth in range(3):
        for h in product(range(4),repeat=depth):
            chosen=action(h);z=finish(h);values=[utility(finish(h+(a,)),depth) for a in range(4)]
            assert values[chosen]==utility(z,depth)
            for a,value in enumerate(values):
                if a!=chosen:
                    gap=values[chosen]-value
                    assert gap>0,(h,chosen,a,gap)
                    comparisons.append(gap)
            tables[''.join('ABCD'[a] for a in h) or 'root']=[str(v) for v in values]
    pne=[];notpne=[];static_strict=[]
    for z in product(range(4),repeat=3):
        gains=[]
        for i,a in enumerate(z):
            for b in range(4):
                if b==a:continue
                zz=z[:i]+(b,)+z[i+1:]
                gains.append((utility(zz,i)-utility(z,i),i,b))
        if max(g[0] for g in gains)<=0:
            assert all(g[0]<0 for g in gains)
            static_strict.extend(-g[0] for g in gains)
            pne.append({'terminal':z,'W':coverage(z),'utilities':[str(utility(z,i)) for i in range(3)]})
        else:
            best=max(gains)
            notpne.append(best[0])
    assert {tuple(x['terminal']) for x in pne}==set(product(range(4),repeat=3)).intersection({(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)})
    actual=finish(())
    assert actual==(3,0,0)
    assert min(x['W'] for x in pne)>coverage(actual)
    return {'customers':len(customers),'actual':actual,'utilities':[str(utility(actual,i)) for i in range(3)],'W':coverage(actual),'OPT3':max(coverage(z) for z in product(range(4),repeat=3)),'decision_histories':21,'comparisons_including_self':84,'minimum_nonself_SPE_margin':str(min(comparisons)),'minimum_static_PNE_strict_margin':str(min(static_strict)),'minimum_best_profitable_static_deviation_for_nonPNE':str(min(notpne)),'static_PNE':pne,'actual_node_payoff_tables':tables}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);a=ap.parse_args()
    base=run(BASE);full=run({b:100*BASE.get(b,0)+1 for b in range(1,16)})
    assert base['W']==11 and base['OPT3']==12 and base['utilities']==['4','7/2','7/2']
    assert base['minimum_nonself_SPE_margin']=='1/6'
    assert full['customers']==1215 and full['W']==1112 and full['OPT3']==1214
    out={'claim':'B2-STRICT-UNIQUE-SPE-STATIC-GAP-v1','status':'definition-level exact finite audit passed; not a half-coverage counterexample','base':base,'all_types_positive_M100':full}
    if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('base','all_types_positive_M100')},ensure_ascii=False))
    for label,r in [('base',base),('full_support',full)]:print(label,json.dumps({k:v for k,v in r.items() if k not in ('actual_node_payoff_tables','static_PNE')},ensure_ascii=False))
if __name__=='__main__':main()
