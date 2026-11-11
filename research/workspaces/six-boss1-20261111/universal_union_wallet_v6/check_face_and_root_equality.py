#!/usr/bin/env python3
"""Exact whole optimum face and same-root equality obstruction, zero optimizer."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
N=257
read=lambda p:json.loads(p.read_text())
vec=lambda d:[F(d.get(str(j),'0')) for j in range(N)]
dot=lambda a,b:sum((x*y for x,y in zip(a,b)),F(0))
sha=lambda p:sha256(p.read_bytes()).hexdigest()

def save(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def main():
    inp=read(HERE/'exact_input.json');cert=read(HERE/'exact_certificate.json')
    assert sha(HERE/'exact_input.json')=='49532be5fae2913f2ab56ae641452510d7b0f8f14ff7049de0dd62fa7b9a8936'
    assert sha(HERE/'exact_certificate.json')=='98fa318efae0c6fef36e87b1861d559ede340ab4aaf7ed390c426854e5711f1d'
    z=vec(cert['primal']);atoms=inp['atom_columns']
    residual=vec(cert['dual']['nonnegative_column_residual'])
    zero=[j for j,v in enumerate(residual) if not v]
    expected=[0,1,7,9,11,25,37,133,165,229,233,241,249,256]
    assert zero==expected and all(v>=0 for v in residual)
    names=list(cert['dual']['row_weights'])
    assert len(names)==12 and all(F(v)>0 for v in cert['dual']['row_weights'].values())
    byname={r['name']:r for r in inp['unique_rows']}
    full_rows=[vec(inp['equality']['a'])]+[vec(byname[n]['a']) for n in names]
    rhs=[F(1)]+[F(byname[n]['rhs']) for n in names]
    assert rhs==[F(1)]+[F(0)]*12
    m=len(full_rows)
    M=[[row[j] for j in zero]+[b] for row,b in zip(full_rows,rhs)]
    T=[[F(int(i==j)) for j in range(m)] for i in range(m)]
    rank=0;pivots=[]
    for col in range(len(zero)):
        candidates=[r for r in range(rank,m) if M[r][col]]
        if not candidates:continue
        pivot=candidates[0]
        M[rank],M[pivot]=M[pivot],M[rank];T[rank],T[pivot]=T[pivot],T[rank]
        divisor=M[rank][col]
        M[rank]=[v/divisor for v in M[rank]];T[rank]=[v/divisor for v in T[rank]]
        for r in range(m):
            if r!=rank and M[r][col]:
                ratio=M[r][col]
                M[r]=[a-ratio*b for a,b in zip(M[r],M[rank])]
                T[r]=[a-ratio*b for a,b in zip(T[r],T[rank])]
        pivots.append(col);rank+=1
    assert rank==13 and len(zero)==14
    free=[j for j in range(len(zero)) if j not in pivots]
    assert free==[zero.index(0)]
    for r,col in enumerate(pivots):
        assert M[r][free[0]]==0 and M[r][-1]==z[zero[col]]
        for k,j in enumerate(zero):
            assert sum(T[r][i]*full_rows[i][j] for i in range(m))==M[r][k]
    assert z[0]==0 and all(z[j]==0 for j in range(N) if j not in zero)
    assert all(F(row['a'].get('0','0'))==0 for row in inp['raw_rows'])
    assert F(inp['objective'].get('0','0'))==F(inp['equality']['a'].get('0','0'))==0
    assert all(v>=0 for v in z) and dot(vec(inp['equality']['a']),z)==1
    assert all(dot(vec(row['a']),z)>=F(row['rhs']) for row in inp['raw_rows'])
    face={'status':'PASS','optimizer_calls':0,'zero_columns':zero,'positive_row_names':names,
        'equation_rank':rank,'variable_count':14,'exact_feasible_face':'z = certificate_primal + s e_0, s >= 0',
        'all867_rows_annihilate_e0':True,'full_domain_retained':True,'scope':'Exact face of necessary system; no SPE realization claim.'}
    save('optimum_face_diagnostic.json',face)
    quantities={'K':[F(0)]*256+[F(1)],
        'u1':[F(a['a'][0],sum(a['a'])) if sum(a['a']) else F(0) for a in atoms]+[F(0)],
        'O_minus_K':[F(a['o']) for a in atoms]+[F(-1)]}
    for name in ['SAFE_6_7','MX_8','RC_7_8','ROOT30_B2_CAPACITY_FEEDBACK']:
        raw=next(r for r in inp['raw_rows'] if r['name']==name)
        assert F(raw['rhs'])==0;quantities[name]=vec(raw['a'])
    identities={}
    for name,g in quantities.items():
        payment=[F(0)]*m
        for r,col in enumerate(pivots):
            payment=[a+g[zero[col]]*b for a,b in zip(payment,T[r])]
        remain=[g[j]-sum(payment[i]*full_rows[i][j] for i in range(m)) for j in range(N)]
        assert all(remain[j]==0 for j in zero)
        value=dot(payment,rhs);assert value==dot(g,z)
        identities[name]={'constant_on_normalized_face':str(value),
            'formula':'g dot (z,K) - constant O = sum signed_weight R_positive + sum signed_residual_j variable_j',
            'normalization_coefficient':str(payment[0]),
            'signed_row_weights':{n:str(w) for n,w in zip(names,payment[1:]) if w},
            'all257_signed_residuals':[str(v) for v in remain],
            'all_residuals_zero_on_dual_zero_domain':True}
    save('face_signed_identities.json',identities)

    root=read(HERE/'root_feedback_check.json')
    assert root['status']=='PASS' and root['old_and_new_free_column_checks']==131
    rho={int(j):F(v) for j,v in root['all129_new_residuals'].items()}
    assert all(v>=0 for v in rho.values())
    rootzero=[h for h in range(128) if not rho[h]]
    assert rootzero==[0,2,9,125]
    assert F(root['new_weights']['CAP_B2'])>0 and F(root['new_weights']['CAP_B4'])>0
    assert F(cert['dual']['row_weights']['ROOT30_B2_CAPACITY_FEEDBACK'])>0
    assert F(identities['ROOT30_B2_CAPACITY_FEEDBACK']['constant_on_normalized_face'])==0
    all_signed={};zero_table=[]
    for h in range(128):
        p,y2,y3,y4,y5,last,o=map(int,format(h,'07b'))
        e=o-p-y4+y2
        all_signed[str(h)]=str(e)
        if h in rootzero:
            assert e==0
            zero_table.append({'h':h,'bits':[p,y2,y3,y4,y5,last,o],'o_minus_p':o-p,'y4_minus_y2':y4-y2})
    gap=F(identities['O_minus_K']['constant_on_normalized_face'])
    assert gap==1-F(cert['K'])>0
    result={'status':'PASS','optimizer_calls':0,'input_sha256':sha(HERE/'exact_input.json'),
        'certificate_sha256':sha(HERE/'exact_certificate.json'),'root_zero_state_table':zero_table,
        'exact_root_identity':'O-K = CAP_B2-CAP_B4 + sum_h (o-p-y4+y2)w_h + E_p-E_o',
        'all128_signed_root_coefficients':all_signed,
        'positive_cap_weights':{n:root['new_weights'][n] for n in ['CAP_B2','CAP_B4']},
        'necessary_equality':'ROOT30_B2_CAPACITY_FEEDBACK=0 in a real SPE forces root support in{0,2,9,125} and CAP_B2=CAP_B4=0, hence O=K.',
        'whole_v6_face_O_minus_K':str(gap),'whole_v6_face_O_minus_K_decimal':float(gap),
        'whole_v6_optimum_face_excluded_from_SPE':True,'new_matrix_rows':0,'new_optimizer_calls':0,
        'scope':'Exact equality obstruction, not a quantified improvement or half proof; no cross-branch splicing.'}
    save('root_equality_diagnostic.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='all128_signed_root_coefficients'},indent=2))

if __name__=='__main__':main()
