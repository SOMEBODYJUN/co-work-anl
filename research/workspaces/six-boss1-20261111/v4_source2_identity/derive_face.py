#!/usr/bin/env python3
"""All-column old225 face reconstruction by Fraction algebra; no optimizer."""
from fractions import Fraction as F
from hashlib import sha256
from math import lcm
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
WS=HERE.parent
ROOT=HERE.parents[3]
INPUT=WS/'universal_union_wallet_v4/exact_input.json'
CERT=WS/'universal_union_wallet_v4/exact_certificate.json'
EXPECTED_INPUT='b520abb0565c6df7ae4192971bf90d712ddf92a4304f3ce51710cd9b2617b8f5'
EXPECTED_CERT='290f90feba9bf7ec8232e16e59f02b7f4e05dc41413f14510592c3d16ef28819'
def digest(path):return sha256(path.read_bytes()).hexdigest()
def load(path):return json.loads(path.read_text())
def dense(a):return [F(a.get(str(j),'0')) for j in range(257)]
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def strings(a):return [str(x) for x in a]
def save(name,data):(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def solve_square(A,b):
    n=len(A);M=[list(row)+[rhs] for row,rhs in zip(A,b)]
    det=F(1);pivots=[]
    assert all(len(row)==n for row in A)
    for j in range(n):
        k=next(k for k in range(j,n) if M[k][j])
        if k!=j:M[k],M[j]=M[j],M[k];det=-det
        p=M[j][j];det*=p;pivots.append(p)
        M[j]=[v/p for v in M[j]]
        for i in range(n):
            if i!=j and M[i][j]:
                q=M[i][j];M[i]=[x-q*y for x,y in zip(M[i],M[j])]
    assert all(M[i][j]==int(i==j) for i in range(n) for j in range(n))
    return [row[-1] for row in M],det,pivots

def main():
    assert digest(INPUT)==EXPECTED_INPUT and digest(CERT)==EXPECTED_CERT
    data=load(INPUT);certificate=load(CERT)
    assert data['variables']==257 and len(data['raw_rows'])==225
    assert data['nonnegative_columns']==list(range(257))
    assert F(data['equality']['rhs'])==1
    rows={r['name']:dense(r['a']) for r in data['raw_rows']}
    row_rhs={r['name']:F(r['rhs']) for r in data['raw_rows']}
    objective=dense(data['objective']);norm=dense(data['equality']['a'])
    primal=dense(certificate['primal'])
    assert min(primal)>=0 and dot(norm,primal)==1
    weights={n:F(v) for n,v in certificate['dual']['row_weights'].items()}
    assert len(weights)==11 and all(v>0 for v in weights.values())
    assert all(row_rhs[n]==0 for n in weights)
    beta=F(certificate['dual']['normalization_multiplier'])
    assert beta==F(certificate['objective'])==dot(objective,primal)
    residual=[objective[j]-beta*norm[j]-sum(w*rows[n][j] for n,w in weights.items()) for j in range(257)]
    assert min(residual)>=0
    assert residual==dense(certificate['dual']['nonnegative_column_residual'])
    raw_slacks={n:dot(row,primal)-row_rhs[n] for n,row in rows.items()}
    assert min(raw_slacks.values())>=0
    assert all(not raw_slacks[n] for n in weights)
    assert all(not residual[j]*primal[j] for j in range(257))
    zeros=[j for j,r in enumerate(residual) if not r]
    positive=[j for j,r in enumerate(residual) if r>0]
    assert zeros==[0,1,3,7,9,11,25,37,153,165,229,241,249,256]
    assert len(positive)==243
    labels=['NORMALIZATION_O']+list(weights)
    matrix=[norm]+[rows[n] for n in weights]
    rhs=[F(1)]+[F(0)]*11
    basis=[j for j in zeros if j not in (0,3)]
    minor=[[row[j] for j in basis] for row in matrix]
    reconstructed,det,pivots=solve_square(minor,rhs)
    assert det and reconstructed==[primal[j] for j in basis]
    direction_values,_,_=solve_square(minor,[-row[3] for row in matrix])
    direction=[F(0)]*257;direction[3]=F(1)
    for j,v in zip(basis,direction_values):direction[j]=v
    assert {j:str(v) for j,v in enumerate(direction) if v}=={1:'-1',3:'1',9:'1',11:'-1'}
    sigma=[F(int(j==0)) for j in range(257)]
    assert all(not dot(row,direction) and not dot(row,sigma) for row in matrix)
    assert not dot(objective,direction) and not dot(objective,sigma)
    assert all(row[0]==0 for row in rows.values())
    lcms=[lcm(*(v.denominator for v in row)) for row in minor]
    integer_minor=[[int(v*s) for v in row] for row,s in zip(minor,lcms)]
    determinant_integer=det
    for s in lcms:determinant_integer*=s
    assert determinant_integer.denominator==1

    # Necessary and sufficient exact interval from all225 rows and all257 columns.
    restrictions=[]
    for j in range(257):restrictions.append((f'NONNEGATIVE_{j}',primal[j],direction[j]))
    for name,row in rows.items():restrictions.append((name,dot(row,primal)-row_rhs[name],dot(row,direction)))
    lower=[];upper=[]
    for name,c,d in restrictions:
        if d>0:lower.append((-c/d,name))
        elif d<0:upper.append((-c/d,name))
        else:assert c>=0
    tmin=max(v for v,_ in lower);tmax=min(v for v,_ in upper)
    assert tmin==0 and tmax==F('130432152540345931391239458166315/179845952006454638284338650603236947')
    lower_owners=[n for v,n in lower if v==tmin]
    upper_owners=[n for v,n in upper if v==tmax]
    assert 'NONNEGATIVE_3' in lower_owners and 'SAFE_6_7' in upper_owners
    endpoints={label:[x+t*h for x,h in zip(primal,direction)] for label,t in [('lower',tmin),('upper',tmax)]}
    endpoint_slacks={}
    for label,point in endpoints.items():
        assert min(point)>=0 and dot(norm,point)==1 and dot(objective,point)==beta
        slacks={n:dot(row,point)-row_rhs[n] for n,row in rows.items()}
        assert min(slacks.values())>=0
        endpoint_slacks[label]=slacks

    # Literal actual shares / key budgets / true terminal costs on all256 types.
    gaps={q:[F(0)]*257 for q in ('A6','X')}
    literal_key_rows={n:[F(0)]*257 for n in ('SAFE_2_5','K_ge_size_5','K_ge_size_6')}
    literal_key_rows['K_ge_size_5'][256]=literal_key_rows['K_ge_size_6'][256]=F(1)
    payoff2=[F(0)]*257;size5=[F(0)]*257;size6=[F(0)]*257
    for atom in data['atom_columns']:
        j=atom['index'];a=atom['a'];total=sum(a)
        assert tuple(a+[atom['x'],atom['o']])==tuple(map(int,format(j,'08b')))
        assert objective[j]==int(total>0) and norm[j]==atom['o']
        u2=F(a[1],total) if total else F(0);payoff2[j]=u2
        size5[j]=F(a[4]);size6[j]=F(a[5])
        literal_key_rows['SAFE_2_5'][j]=u2-F(a[4],a[0]+5)
        literal_key_rows['K_ge_size_5'][j]=-F(a[4])
        literal_key_rows['K_ge_size_6'][j]=-F(a[5])
        gaps['A6'][j]=F(a[5],a[0]+1+4*a[4])-u2
        gaps['X'][j]=F(atom['x'],a[0]+1+4*a[4])-u2
    assert all(rows[n]==vector for n,vector in literal_key_rows.items())
    assert all(n in weights for n in literal_key_rows)
    assert primal[256]==dot(size5,primal)==dot(size6,primal)

    # Signed identities are face identities, never nonnegative universal duals.
    signed={}
    transpose=[list(col) for col in zip(*minor)]
    for query,target in gaps.items():
        linear_coeffs,_,_=solve_square(transpose,[target[j] for j in basis])
        constant=linear_coeffs[0]
        slope=dot(target,direction)
        assert constant==dot(target,primal)>0
        assert slope==(F(0) if query=='A6' else F(4,5))
        eta=[target[j]-sum(c*row[j] for c,row in zip(linear_coeffs,matrix))-slope*int(j==3) for j in range(257)]
        assert all(eta[j]==0 for j in zeros)
        minimum=min(constant+slope*tmin,constant+slope*tmax)
        assert minimum>0
        signed[query]={
            'target_all257':strings(target),'normalization':str(constant),
            'z3_coefficient':str(slope),
            'positive_budget_coefficients':{n:str(c) for n,c in zip(labels[1:],linear_coeffs[1:])},
            'zero_on_face_column_coefficients':{str(j):str(eta[j]) for j in positive if eta[j]},
            'minimum_on_entire_face':str(minimum),
            'lower_endpoint_gap':str(constant+slope*tmin),
            'upper_endpoint_gap':str(constant+slope*tmax),
            'claim':'Signed identity on the exposed old225 face, not a universal nonnegative certificate'}

    source_paths=[INPUT,CERT,WS/'universal_union_wallet_v4/source_review.md',
        ROOT/'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
        WS/'main_thirty_index_strengthening/proof.md',
        WS/'actual_source2_opt_requery/freeze_manifest.json',
        WS/'actual_source2_opt_requery/SHA256SUMS']
    symbolic=load(WS/'actual_source2_opt_requery/freeze_manifest.json')
    for name,expected in symbolic['file_sha256'].items():
        path=(WS/'actual_source2_opt_requery'/name).resolve()
        assert digest(path)==expected
        source_paths.append(path)
    for name,expected in load(WS/'actual_source2_opt_requery/frozen_sources_before.json')['file_sha256'].items():
        path=ROOT/name
        assert digest(path)==expected
        source_paths.append(path)
    v4_manifest=WS/'universal_union_wallet_v4/manifest.json'
    source_paths.append(v4_manifest)
    for name,entry in load(v4_manifest)['files'].items():
        path=(v4_manifest.parent/name).resolve()
        assert digest(path)==entry['sha256']
        source_paths.append(path)
    source_paths=sorted(set(p.resolve() for p in source_paths),key=str)
    source_hashes={str(p.relative_to(ROOT)):digest(p) for p in source_paths}
    save('source_hashes.json',{'read_only_files':len(source_hashes),'file_sha256':source_hashes})
    result={
        'status':'EXACT_WHOLE_225_OPTIMAL_FACE_RECONSTRUCTED',
        'optimizer_calls':0,'input_sha256':EXPECTED_INPUT,'parent_certificate_sha256':EXPECTED_CERT,
        'raw_rows':225,'all_columns':257,'normalization':'O=1','welfare_optimum':str(beta),
        'nonzero_raw_rhs':{n:str(v) for n,v in row_rhs.items() if v},
        'positive_dual_weights':{n:str(w) for n,w in weights.items()},
        'all257_dual_residual':strings(residual),
        'positive_residual_columns':positive,'zero_residual_columns':zeros,
        'non_primal_zero_residual_columns':[0,3],
        'positive_budget_rows':list(weights),'equality_rank':12,
        'rank_minor':{'row_names':labels,'column_indices':basis,
            'rational_determinant':str(det),'fraction_pivots':strings(pivots),
            'row_denominator_multipliers':[str(s) for s in lcms],
            'integer_matrix':integer_minor,'integer_determinant':str(determinant_integer)},
        'constant_all257':strings(primal),'t_direction_all257':strings(direction),
        'zero_type_direction_all257':strings(sigma),
        'parameter_domain':{'t_min':str(tmin),'t_max':str(tmax),
            'lower_endpoint_rows':lower_owners,'upper_endpoint_rows':upper_owners,
            'zero_type_mass':'sigma>=0, no upper bound'},
        'endpoints_all257':{n:strings(v) for n,v in endpoints.items()},
        'endpoint_raw225_slacks':{n:{r:str(v) for r,v in values.items()} for n,values in endpoint_slacks.items()},
        'terminal_gaps':signed,
        'u2_constant':str(dot(payoff2,primal)),'K_constant':str(primal[256]),
        'affine_dimension':2,'dimensions':'one bounded X-overlap exchange plus retained all-zero-client ray',
        'claimed_exclusion':'No point on this normalized old225 optimal face is induced by a genuine complete-history pure SPE with K the catalog maximum.',
        'not_claimed':['new LP optimum','strict global welfare improvement','half coverage','complete SPE counterexample','320-row-family result']}
    save('exact_face_certificate.json',result)
    table=['column\tbits_or_K\tprimal\tdual_residual\tconstant\tt_direction\tsigma_direction']
    for j in range(257):
        table.append('\t'.join([str(j),format(j,'08b') if j<256 else 'K',
            str(primal[j]),str(residual[j]),str(primal[j]),str(direction[j]),str(sigma[j])]))
    (HERE/'all_257_face_columns.tsv').write_text('\n'.join(table)+'\n')
    table=['row\tlower_endpoint_slack\tupper_endpoint_slack']
    for n in rows:table.append('\t'.join([n,str(endpoint_slacks['lower'][n]),str(endpoint_slacks['upper'][n])]))
    (HERE/'all_225_endpoint_rows.tsv').write_text('\n'.join(table)+'\n')
    print(json.dumps({'status':result['status'],'optimizer_calls':0,
        'zero_residual_columns':zeros,'positive_residual_columns':len(positive),
        'rank':12,'affine_dimension':2,'t_max':str(tmax),
        'gap_A6':signed['A6']['minimum_on_entire_face'],
        'gap_X_min':signed['X']['minimum_on_entire_face'],
        'certificate_sha256':digest(HERE/'exact_face_certificate.json')},indent=2))

if __name__=='__main__':main()
