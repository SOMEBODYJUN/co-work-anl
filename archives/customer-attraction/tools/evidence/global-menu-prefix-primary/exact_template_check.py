"""Independent standard-library Fraction check; no original solver/main imports."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,math
HERE=Path(__file__).resolve().parent
def row(m,bits,d,l):
    k=m-2;es=bits[:k];a,b=bits[-2:];p=sum(es);c=sum(bits);w=int(c>0)
    u=[F(e,c)if e else F(0)for e in bits]
    prefix=[];t=0
    for e in bits:prefix.append(t);t+=e
    g=m*u[-2]+u[-1]/2-F(d,p+1)-F(l,2*m*(p+a+1))+F(d*l,m*(p+1)*(p+2))
    r=[u[j]-F(a,prefix[j]+m-j)for j in range(k)]
    last=[u[-1]-F(es[j],p+a+1)for j in range(k)]
    h=[m*u[j]-F(d,prefix[j]+m-j)for j in range(m)]
    return [g]+r+last+h,F(2*w-int(d>0))
def main():
    folder=HERE/'original/research/workspaces/customer-attraction/R-e6796fb9db2a4ae9994cee93ac9bd152/global'
    v2=json.loads((folder/'menu_prefix_lp_v2.json').read_text());positive=[];total=0
    for source in v2:
        if not source['success']:continue
        m=source['m'];coeff=list(map(F,source['coeff']));assert len(coeff)==3*m-3 and min(coeff)>=0
        bybits=[];globalmin=None
        for bits in product([0,1],repeat=m):
            values=[]
            for d,l in product(range(m+1),repeat=2):
                a,q=row(m,bits,d,l);values.append((q-sum(x*y for x,y in zip(a,coeff)),d,l));total+=1
            worst=min(values);assert worst[0]>=0
            if globalmin is None or worst[0]<globalmin:globalmin=worst[0]
            bybits.append(dict(bits=list(bits),exact_minimum=str(worst[0]),at=[worst[1],worst[2]]))
        assert globalmin==F(source['worst'])==0
        positive.append(dict(m=m,coeff=source['coeff'],integer_grid_rows=2**m*(m+1)**2,corner_rows=6*2**m,exact_minimum=str(globalmin),by_actual_membership=bybits))
    assert total==528 and [r['m']for r in positive]==[3,4]
    # Three saved m3 minimax active rows recover an exact separating combination.
    v1=json.loads((folder/'menu_prefix_lp.json').read_text());active=v1[0]['active'];ys=[F(1,9),F(2,3),F(2,9)];combined=[F(0),F(0)];qsum=F(0)
    for rec,y in zip(active,ys):
        bits,d,l=rec['type'];a,q=row(3,bits,d,l);g=a[0];r=a[1:3]
        # Fixed-G template uses R/L only and q_fixed=q-G.
        for i,x in enumerate(r):combined[i]+=y*x
        qsum+=y*(q-g)
    assert sum(ys)==1 and combined==[0,0]and qsum==F(-1,3)
    corrections=[];family=[];weak=[]
    for m in range(3,14):
        for l in [0,1,m]:
            a,q=row(m,(0,)*(m-2)+(1,0),1,l)
            assert a[0]==m-1+F(l,4*m)
            corrections.append(dict(m=m,ell=l,actual_A_only_G=str(a[0]),formula='m-1+ell/(4m)'))
        assert F(m)-F(3,2)*sum((F(1,r)for r in range(1,m+1)),F(0))>0
        if m>=4:
            gap=F(3*m-2,2*m-1)-F(m,m-1);assert gap==F(m*m-4*m+2,(2*m-1)*(m-1))>0;weak.append(dict(m=m,bank_weak_individual_gap=str(gap)))
        if m>=6:
            L=math.lcm(*range(3,m+1));W=L*(sum((F(1,r)for r in range(1,m+1)),F(0))+F(1,2));O=m*L
            assert W.denominator==1 and O>2*W
            family.append(dict(m=m,L=L,W=int(W),O=O,half_gap=int(O-2*W),scope='specified relaxed path only, not SPE'))
    out=dict(status='pass',original_main_executions=0,scipy_calls=0,positive_scaled_template_certificates=positive,integer_grid_rows_checked=total,fixed_G_m3_exact_separator=dict(weights=list(map(str,ys)),combined_R_L=list(map(str,combined)),combined_right_side=str(qsum),proves='fixed-G m3 coefficient template infeasible, not a game counterexample'),comparison_source_local_correction=corrections,relaxed_non_SPE_family_finite_checks=family,bank_later_correction_finite_checks=weak,scope='Exact checks of saved coefficients and finite arithmetic; all-m impossibility, rectangular corner reduction and non-SPE explanation are proved in the formal bodies. No floating infeasibility or HALF counterexample is certified.')
    (HERE/'exact-template-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in ['positive_scaled_template_certificates','comparison_source_local_correction','relaxed_non_SPE_family_finite_checks','bank_later_correction_finite_checks']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
