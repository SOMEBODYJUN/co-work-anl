"""Exact comparison examples; does not read or verify any new 44/60 package.

Writes only into compare_new/.  The old 53-row package is read unchanged.
Optional --certificate-recheck reruns its verifier on the K-balanced variant.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=Path(__file__).resolve().parents[5]
OLD=ROOT/'customer_attraction/proofs/half5_exact_v1'


def sh(n,d):
    return F(n,d) if n else F(0)


@lru_cache(None)
def new_credit(p,ell,t,q):
    values=[]
    for b,c,j,v in product((0,1),repeat=4):
        # Negative of the constant part in the seven weighted slacks.
        # Source IC weights 2,3/2; V-vs-B IC 1/2; J,V prices 1/4,5/12;
        # V capacity 1/12; first C-vs-Q IC 1.
        z1=p+t+b+c;z2=p+c+j+v
        val=(2*sh(t,z1)+F(3,2)*sh(c,z2)
             -F(1,2)*(sh(v,z2)-F(b,p+c+j+1))
             +F(j,4*(ell+1))+F(5*v,12*(ell+1))+F(v,12)
             -sh(c,z1)+F(q,p+t+b+1))
        values.append(val)
    return min(values)


def credit_table_crossing():
    out={'new_normalized_credit_larger':[],'new_normalized_credit_smaller':[],'equal':0}
    for p in range(4):
        for ell in range(p,p+3):
            for t,q in product((0,1),repeat=2):
                old=min(sh(t,p+t+b+c)+F(c,20)+(F(b,8)+F(c,5))/(ell+1)
                        -F(1,4)*(sh(c,p+t+b+c)-F(q,p+t+b+1))
                        for b,c in product((0,1),repeat=2))
                new=F(2,7)*new_credit(p,ell,t,q)
                key='new_normalized_credit_larger' if new>old else 'new_normalized_credit_smaller'
                if new==old:out['equal']+=1
                else:out[key].append({'p':p,'ell':ell,'t':t,'q':q,'old_credit':str(old),'new_normalized_credit':str(new)})
    return out


def same_row_arbitrary_support():
    # Target x-y equals the weighted sum of n copies of x-y>=0.
    out={}
    for n in (1,44,53,60):
        weights=[F(1,n)]*n
        assert sum(weights)==1 and all(v>0 for v in weights)
        out[str(n)]={'positive_multipliers':n,'aggregate_x_coefficient':'1','aggregate_y_coefficient':'-1'}
    return out


def joint_projection():
    # A real m=2 singleton-client singleton-catalogue SPE chooses T twice:
    # source payoff r=1/2, K=1, hidden last membership g=1.
    # Row A is source IC. Row B is the same IC plus K-|G|>=0.
    A={g:F(1,1+g) for g in (0,1)}
    B={g:F(1,1+g)+g for g in (0,1)}
    separate=min(A.values())+min(B.values())
    together=min(A[g]+B[g] for g in (0,1))
    assert separate==F(3,2) and together==2
    r,K=F(1,2),F(1)
    assert 2*r+K==together
    return {'A_g0_g1':[str(A[g]) for g in (0,1)],'B_g0_g1':[str(B[g]) for g in (0,1)],'sum_of_separate_minima':str(separate),'minimum_of_sum':str(together),'strict_gain':str(together-separate),'real_SPE_budget_2r_plus_K':str(2*r+K)}


def make_Kzero_variant():
    old=json.loads((OLD/'certificate.json').read_text())
    columns=json.loads((OLD/'active_k_columns.json').read_text())['row_K_coefficients']
    weighted=sum(int(v)*int(columns[n]) for n,v in old['integer_multipliers'].items())
    assert weighted==-2264870 and int(columns['MAX:fixed:2'])==1
    new=json.loads(json.dumps(old))
    new['integer_multipliers']['MAX:fixed:2']+=-weighted
    new['claim']='2 W >= OPT_5; review-only exact K-balanced representation'
    assert sum(int(v)*int(columns[n]) for n,v in new['integer_multipliers'].items())==0
    assert len([v for v in new['integer_multipliers'].values() if int(v)>0])==53
    target=HERE/'certificate53_Kzero.json'
    target.write_text(json.dumps(new,indent=2)+'\n')
    return {'old_K_residual_numerator':str(-weighted),'capacity_row_multiplier_increment':str(-weighted),'new_K_residual_numerator':'0','positive_multipliers':53,'customer_residual_change':'adds 2264870*1_C/10^22','variant_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}


def negative_old_point_check():
    # Rebuild and verify the exact old 387-row relaxation plus its saved
    # single-final-reply closure witnesses. No numerical optimization runs.
    sys.path.insert(0,str(ROOT/'research/workspaces/customer-attraction/R-07e871289a6b4c1fb07244c97eb4aac8/general_from_half5'))
    import six_copy_refine as oldgen
    source=(ROOT/'research/workspaces/customer-attraction/'
            'R-07e871289a6b4c1fb07244c97eb4aac8/general_from_half5/six_copy_free_results.json')
    data=json.loads(source.read_text()); point=data['final'];m=point['m']
    types,rows=oldgen.bridge_system(m)
    for cut in data['cuts']:
        rows.append(oldgen.parametric_row(types,m,{k:v for k,v in cut.items() if k!='separation_slack'}))
    assert len(rows)==point['n_rows']==387
    oldgen.verify(point,types,rows)
    oldgen.verify_reply_closure(point,types,data['reply_closure_witnesses'])
    support=[(tuple(map(int,s['actual_bits'])),s['d'],F(s['weight'])) for s in point['support']]
    src=m-3
    us=sum(mass*sh(a[src],sum(a)) for a,d,mass in support)
    um=sum(mass*sh(a[-1],sum(a)) for a,d,mass in support)
    K=F(point['K']);budget=F(7,2)*us+F(2,3)*um+K/12
    # Form the off-diagonal average by literal comparison indices, not by
    # using the closed d(d-1) probability formula in the other stress script.
    credit=F(0)
    for a,d,mass in support:
        memberships=[1]*d+[0]*(m-d)
        credit+=mass*sum(new_credit(sum(a[:src]),sum(a[:-1]),memberships[i],memberships[j])
                         for i in range(m) for j in range(m) if i!=j)/F(m*(m-1))
    slack=budget-credit
    assert slack==F(-4111629751,260320095276)
    return {'old_rows_exactly_verified':len(rows),'old_single_reply_closure_exactly_verified':True,'point_W_over_O':point['W'],'m':m,'source_player':src+1,'u_source':str(us),'u_last':str(um),'K':str(K),'new_offdiag_slack':str(slack),'conclusion':'The new row is not implied by this specific old relaxation and saved single-reply closure; the point is not a SPE.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--certificate-recheck',action='store_true');args=parser.parse_args()
    report={'status':'passed','new_44_or_60_package_verified':False,'same_row_support_sizes':same_row_arbitrary_support(),'shared_variable_projection':joint_projection(),'old_53_K_balance':make_Kzero_variant(),'nested_row_separation':negative_old_point_check(),'normalized_budgets':{'old_r':'1','old_u_last':'13/40','old_K':'1/20','new_r':'1','new_u_last':str(F(2,3)/F(7,2)),'new_K':str(F(1,12)/F(7,2))},'credit_table_crossing':credit_table_crossing()}
    if args.certificate_recheck:
        subprocess.run([sys.executable,str(OLD/'verify_certificate.py'),str(HERE/'certificate53_Kzero.json'),'--manifest',str(OLD/'row_manifest.json'),'--output',str(HERE/'certificate53_Kzero_recheck.json')],check=True)
        report['old_53_K_balance']['full_domain_rechecked']=True
    (HERE/'comparison_microchecks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
