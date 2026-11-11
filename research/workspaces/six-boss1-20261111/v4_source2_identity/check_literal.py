#!/usr/bin/env python3
"""Independent literal old225 face check; JSON-only, Fraction/Bareiss, no LP."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import lcm, prod
from pathlib import Path
import csv
import json

HERE=Path(__file__).resolve().parent
WS=HERE.parent
ROOT=HERE.parents[3]
def load(path):return json.loads(path.read_text())
def digest(path):return sha256(path.read_bytes()).hexdigest()
def vector(sparse):return [F(sparse.get(str(i),'0')) for i in range(257)]
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))

def integer_determinant(source):
    """Independent fraction-free determinant, not builder's Gaussian solve."""
    M=[row[:] for row in source];n=len(M);previous=1;sign=1
    for k in range(n-1):
        pivot_row=next((j for j in range(k,n) if M[j][k]),None)
        if pivot_row is None:return 0
        if pivot_row!=k:M[k],M[pivot_row]=M[pivot_row],M[k];sign=-sign
        pivot=M[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator=M[i][j]*pivot-M[i][k]*M[k][j]
                assert numerator%previous==0
                M[i][j]=numerator//previous
            M[i][k]=0
        previous=pivot
    return sign*M[-1][-1]

def main():
    input_path=WS/'universal_union_wallet_v4/exact_input.json'
    oldcert_path=WS/'universal_union_wallet_v4/exact_certificate.json'
    data=load(input_path);oldcert=load(oldcert_path)
    face=load(HERE/'exact_face_certificate.json')
    assert digest(input_path)==face['input_sha256']=='b520abb0565c6df7ae4192971bf90d712ddf92a4304f3ce51710cd9b2617b8f5'
    assert digest(oldcert_path)==face['parent_certificate_sha256']=='290f90feba9bf7ec8232e16e59f02b7f4e05dc41413f14510592c3d16ef28819'
    assert face['optimizer_calls']==0
    assert len(data['raw_rows'])==225 and data['nonnegative_columns']==list(range(257))
    R={r['name']:vector(r['a']) for r in data['raw_rows']}
    b={r['name']:F(r['rhs']) for r in data['raw_rows']}
    assert len(R)==225
    assert {n:str(v) for n,v in b.items() if v}==face['nonzero_raw_rhs']
    assert len(face['nonzero_raw_rhs'])==9
    eq=vector(data['equality']['a']);obj=vector(data['objective'])
    assert F(data['equality']['rhs'])==1
    p=[F(v) for v in face['constant_all257']]
    h=[F(v) for v in face['t_direction_all257']]
    zero=[F(v) for v in face['zero_type_direction_all257']]
    assert p==vector(oldcert['primal'])
    assert {j:v for j,v in enumerate(h) if v}=={1:F(-1),3:F(1),9:F(1),11:F(-1)}
    assert zero==[F(int(j==0)) for j in range(257)]
    assert dot(eq,p)==1 and dot(eq,h)==dot(eq,zero)==0
    optimum=F(face['welfare_optimum'])
    assert dot(obj,p)==optimum==F(oldcert['objective'])
    assert dot(obj,h)==dot(obj,zero)==0
    weights={n:F(v) for n,v in face['positive_dual_weights'].items()}
    assert weights=={n:F(v) for n,v in oldcert['dual']['row_weights'].items()}
    assert len(weights)==11 and all(v>0 for v in weights.values())
    assert all(b[n]==0 for n in weights)
    residual=[obj[j]-optimum*eq[j]-sum(w*R[n][j] for n,w in weights.items()) for j in range(257)]
    assert residual==[F(v) for v in face['all257_dual_residual']]
    assert residual==vector(oldcert['dual']['nonnegative_column_residual'])
    assert min(residual)>=0 and all(not residual[j]*p[j] for j in range(257))
    positive=[j for j,v in enumerate(residual) if v>0]
    zeros=[j for j,v in enumerate(residual) if not v]
    assert positive==face['positive_residual_columns'] and len(positive)==243
    assert zeros==face['zero_residual_columns']==[0,1,3,7,9,11,25,37,153,165,229,241,249,256]
    assert face['non_primal_zero_residual_columns']==[j for j in zeros if not p[j]]==[0,3]
    assert all(R[n][0]==0 for n in R) and eq[0]==obj[0]==0
    for n,row in R.items():
        slack=dot(row,p)-b[n]
        assert slack==F(oldcert['raw_row_slacks'][n])>=0
        if n in weights:assert slack==dot(row,h)==dot(row,zero)==0

    minor=face['rank_minor'];basis=minor['column_indices']
    assert len(basis)==12 and sorted(set(basis)|{0,3})==zeros
    row_names=minor['row_names']
    assert row_names==['NORMALIZATION_O']+list(weights)
    full_rows=[eq]+[R[n] for n in row_names[1:]]
    rational=[[row[j] for j in basis] for row in full_rows]
    scalars=[lcm(*(v.denominator for v in row)) for row in rational]
    integers=[[int(v*s) for v in row] for row,s in zip(rational,scalars)]
    assert integers==minor['integer_matrix']
    assert [str(s) for s in scalars]==minor['row_denominator_multipliers']
    determinant=integer_determinant(integers)
    assert determinant==int(minor['integer_determinant'])!=0
    assert F(determinant,prod(scalars))==F(minor['rational_determinant'])
    assert face['equality_rank']==12 and face['affine_dimension']==2
    # 243 zero coordinates + this rank12 yields total affine codimension255.

    lo=F(face['parameter_domain']['t_min']);hi=F(face['parameter_domain']['t_max'])
    assert lo==0<hi
    assert hi==F('130432152540345931391239458166315/179845952006454638284338650603236947')
    assert face['parameter_domain']['lower_endpoint_rows']==['NONNEGATIVE_3']
    assert face['parameter_domain']['upper_endpoint_rows']==['SAFE_6_7']
    assert p[3]==0 and h[3]==1
    upper_base=dot(R['SAFE_6_7'],p)-b['SAFE_6_7']
    upper_slope=dot(R['SAFE_6_7'],h)
    assert upper_slope==F(-1,2) and upper_base+hi*upper_slope==0
    endpoint_checks=0;nonnegative_endpoint_checks=0
    for label,t in [('lower',lo),('upper',hi)]:
        point=[x+t*y for x,y in zip(p,h)]
        assert point==[F(v) for v in face['endpoints_all257'][label]]
        assert dot(eq,point)==1 and dot(obj,point)==optimum
        assert min(point)>=0;nonnegative_endpoint_checks+=len(point)
        for n,row in R.items():
            slack=dot(row,point)-b[n]
            assert slack==F(face['endpoint_raw225_slacks'][label][n])>=0
            endpoint_checks+=1

    # Literal all256 shares and the three exact whole-face tight budgets.
    actual_u2=[F(0)]*257
    literal={n:[F(0)]*257 for n in ('SAFE_2_5','K_ge_size_5','K_ge_size_6')}
    literal['K_ge_size_5'][256]=literal['K_ge_size_6'][256]=F(1)
    target={q:[F(0)]*257 for q in ('A6','X')}
    for j in range(256):
        bits=[int(v) for v in format(j,'08b')];a=bits[:6];x,o=bits[6:]
        atom=data['atom_columns'][j]
        assert atom=={'index':j,'a':a,'x':x,'o':o}
        actual_u2[j]=F(a[1],sum(a)) if sum(a) else F(0)
        assert obj[j]==int(any(a)) and eq[j]==o
        literal['SAFE_2_5'][j]=actual_u2[j]-F(a[4],a[0]+5)
        literal['K_ge_size_5'][j]=-a[4]
        literal['K_ge_size_6'][j]=-a[5]
        target['A6'][j]=F(a[5],a[0]+4*a[4]+1)-actual_u2[j]
        target['X'][j]=F(x,a[0]+4*a[4]+1)-actual_u2[j]
    assert obj[256]==eq[256]==0
    assert all(R[n]==row and n in weights for n,row in literal.items())
    assert dot(actual_u2,h)==dot(actual_u2,zero)==0
    assert str(dot(actual_u2,p))==face['u2_constant']
    assert str(p[256])==face['K_constant'] and h[256]==0

    identity_checks=0;gap_summary={}
    for query,claimed in face['terminal_gaps'].items():
        assert [F(v) for v in claimed['target_all257']]==target[query]
        theta={n:F(v) for n,v in claimed['positive_budget_coefficients'].items()}
        assert set(theta)==set(weights)
        eta={int(j):F(v) for j,v in claimed['zero_on_face_column_coefficients'].items()}
        assert set(eta)<=set(positive)
        normal=F(claimed['normalization']);slope=F(claimed['z3_coefficient'])
        for j in range(257):
            paid=normal*eq[j]+slope*int(j==3)+sum(v*R[n][j] for n,v in theta.items())+eta.get(j,F(0))
            assert paid==target[query][j]
            identity_checks+=1
        assert normal==dot(target[query],p)>0
        assert slope==dot(target[query],h)==(F(0) if query=='A6' else F(4,5))
        assert dot(target[query],zero)==0
        assert min(normal+slope*lo,normal+slope*hi)==F(claimed['minimum_on_entire_face'])>0
        assert str(normal+slope*lo)==claimed['lower_endpoint_gap']
        assert str(normal+slope*hi)==claimed['upper_endpoint_gap']
        gap_summary[query]={'constant':str(normal),'t_coefficient':str(slope),
            'positive_lower_bound':claimed['minimum_on_entire_face'],
            'query_value_at_base':str(normal+dot(actual_u2,p))}
    assert gap_summary['A6']['constant']=='104997578333106831070437069794935859/899229760032273191421693253016184735'
    assert gap_summary['X']['constant']=='367236037058350577615317768596918154/4496148800161365957108466265080923675'
    rigidity_checks=0;strict_rigidity_checks=0
    for a1 in (0,1):
        for tail in product((0,1),repeat=4):
            s=sum(tail)
            excess=F(1,a1+1+s)-F(1,a1+5)
            assert excess==F(4-s,(a1+1+s)*(a1+5))>=0
            assert (excess==0)==(tail==(1,1,1,1))
            rigidity_checks+=1;strict_rigidity_checks+=excess>0

    with (HERE/'all_257_face_columns.tsv').open() as handle:
        table=list(csv.DictReader(handle,delimiter='\t'))
    assert len(table)==257
    for j,line in enumerate(table):
        assert int(line['column'])==j
        assert tuple(F(line[k]) for k in ['primal','dual_residual','constant','t_direction','sigma_direction'])==(p[j],residual[j],p[j],h[j],zero[j])
    with (HERE/'all_225_endpoint_rows.tsv').open() as handle:
        table=list(csv.DictReader(handle,delimiter='\t'))
    assert len(table)==225
    for line in table:
        n=line['row']
        assert line['lower_endpoint_slack']==face['endpoint_raw225_slacks']['lower'][n]
        assert line['upper_endpoint_slack']==face['endpoint_raw225_slacks']['upper'][n]
    frozen=load(HERE/'source_hashes.json')['file_sha256']
    changed=[path for path,hsh in frozen.items() if digest(ROOT/path)!=hsh]
    assert not changed,changed
    result={
        'status':'PASS_ALL257_DUAL_RANK12_FULL225_FACE_AND_TWO_TRUE_TERMINAL_GAPS',
        'optimizer_calls':0,'all257_dual_columns_checked':257,
        'strictly_positive_dual_rows':11,'strictly_positive_column_residuals':243,
        'zero_residual_columns':zeros,'non_primal_zero_columns_retained':[0,3],
        'rank':12,'bareiss_integer_determinant':str(determinant),
        'full_face_affine_dimension':2,'raw225_endpoint_row_checks':endpoint_checks,
        'nonnegative_endpoint_column_checks':nonnegative_endpoint_checks,
        'nonzero_rhs_preserved':9,'literal_key_row_coefficients':3*257,
        'literal_terminal_gap_coefficients':2*257,
        'signed_identity_column_checks':identity_checks,
        'source2_rigidity_cases':rigidity_checks,'strict_non_allfour_cases':strict_rigidity_checks,
        'terminal_gap_values':gap_summary,'t_max':str(hi),
        'read_only_source_files_checked':len(frozen),'changed_old_files':changed,
        'uses_new320_family':False,'uses_243_phase_I':False,
        'claim':'Entire old225 optimal face cannot be induced by a genuine SPE; no new quantitative universal welfare bound claimed.',
        'file_sha256':{name:digest(HERE/name) for name in ['derivation.md','derive_face.py',
            'exact_face_certificate.json','all_257_face_columns.tsv','all_225_endpoint_rows.tsv','source_hashes.json']}}
    (HERE/'literal_check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='file_sha256'},indent=2))

if __name__=='__main__':main()
