#!/usr/bin/env python3
"""Zero-optimizer source2 equality and complete v5 optimum-face diagnostic.

This does not add any row to the released 546-row input.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
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
    assert sha(HERE/'exact_input.json')=='3b2065e702c5590d50ebc8acd5ea30337e82db2a84585f87040acd36e91db553'
    assert sha(HERE/'exact_certificate.json')=='5e5a2377ed780f4a9c9f58ca8703fc5a473d41ea1945a654aa0ee6c0efa0deda'
    z=vec(cert['primal']);atoms=inp['atom_columns']
    table=[];state_rows=[];count=0
    for p,t,q in product((0,1),repeat=3):
        m=4*t+F(30*t,p+5)+F(q,p+1+4*t)
        equality=[]
        for tails in product((0,1),repeat=4):
            s,last=sum(tails[:3]),tails[3]
            den=p+t+s+last
            phi=(F(31*t-last,den) if den else F(0))+s+last+F(q,p+t+s+1)
            rho=phi-m
            assert rho>=0
            state_rows.append({'p':p,'t':t,'q':q,'tails':list(tails),'phi':str(phi),'minimum':str(m),'residual':str(rho)})
            if not rho:
                equality.append(''.join(map(str,tails)))
                assert t or not any(tails[:3])
            count+=1
        table.append({'p':p,'t':t,'q':q,'zero_residual_tails':equality})
    assert count==128
    # Exactly the eight complete equality sets, including every weak tie.
    expected=[['0000','0001'],['0000','0001'],['1111'],['1111'],
              ['0000'],['0000'],['0111','1011','1101','1111'],['1111']]
    assert [r['zero_residual_tails'] for r in table]==expected
    save('source2_equality_states.json',state_rows)

    # All optimum points are confined by the certified positive residuals.
    residual=vec(cert['dual']['nonnegative_column_residual'])
    zero=[j for j in range(N) if residual[j]==0]
    assert all(v>=0 for v in residual)
    rows_by_name={r['name']:r for r in inp['unique_rows']}
    positive_names=list(cert['dual']['row_weights'])
    assert len(positive_names)==11
    assert all(F(v)>0 for v in cert['dual']['row_weights'].values())
    full_rows=[vec(inp['equality']['a'])]+[vec(rows_by_name[n]['a']) for n in positive_names]
    rhs=[F(1)]+[F(rows_by_name[n]['rhs']) for n in positive_names]
    assert rhs==[F(1)]+[F(0)]*11
    M=[[r[j] for j in zero]+[b] for r,b in zip(full_rows,rhs)]
    transform=[[F(int(i==j)) for j in range(12)] for i in range(12)]
    pivot_columns=[];rank=0
    for col in range(len(zero)):
        candidates=[r for r in range(rank,len(M)) if M[r][col]]
        if not candidates:continue
        pivot=candidates[0]
        M[rank],M[pivot]=M[pivot],M[rank]
        transform[rank],transform[pivot]=transform[pivot],transform[rank]
        divisor=M[rank][col]
        M[rank]=[v/divisor for v in M[rank]]
        transform[rank]=[v/divisor for v in transform[rank]]
        for r in range(len(M)):
            if r!=rank and M[r][col]:
                ratio=M[r][col]
                M[r]=[a-ratio*b for a,b in zip(M[r],M[rank])]
                transform[r]=[a-ratio*b for a,b in zip(transform[r],transform[rank])]
        pivot_columns.append(col);rank+=1
    assert rank==12 and len(zero)==13
    free=[j for j in range(len(zero)) if j not in pivot_columns]
    assert free==[zero.index(0)]
    assert all(M[r][free[0]]==0 for r in range(rank))
    for r,col in enumerate(pivot_columns):
        assert M[r][-1]==z[zero[col]]
        assert all(sum(transform[r][i]*full_rows[i][j] for i in range(12))==M[r][zero.index(j)] for j in zero)
    # Feasibility of the whole ray, not just an affine solution space.
    assert z[0]==0 and all(z[j]==0 for j in range(N) if j not in zero)
    assert all(F(r['a'].get('0','0'))==0 for r in inp['raw_rows'])
    assert F(inp['equality']['a'].get('0','0'))==F(inp['objective'].get('0','0'))==0
    assert all(dot(vec(r['a']),z)>=F(r['rhs']) for r in inp['raw_rows'])
    faces={'status':'PASS','optimizer_calls':0,'zero_columns':zero,'positive_row_names':positive_names,
        'restricted_equation_rank':rank,'restricted_variable_count':len(zero),
        'exact_feasible_face':'z = certificate_primal + s e_0, s >= 0',
        'free_column':0,'all546_rows_annihilate_free_direction':True,
        'scope':'Exact full optimum face of the released necessary system, not an SPE realization statement.'}
    save('optimum_face_diagnostic.json',faces)

    # Full257 signed identities for fixed face quantities; off-face signs are not asserted.
    quantities={'K':[F(0)]*256+[F(1)],
                'u1':[F(a['a'][0],sum(a['a'])) if sum(a['a']) else F(0) for a in atoms]+[F(0)]}
    for T in (4,5,6):
        quantities[f'K_minus_size_A{T}']=[-F(a['a'][T-1]) for a in atoms]+[F(1)]
    identities={}
    for name,g in quantities.items():
        payment=[F(0)]*12
        for r,col in enumerate(pivot_columns):
            payment=[v+g[zero[col]]*u for v,u in zip(payment,transform[r])]
        remainder=[g[j]-sum(payment[i]*full_rows[i][j] for i in range(12)) for j in range(N)]
        assert all(remainder[j]==0 for j in zero)
        constant=dot(payment,rhs)
        assert constant==dot(g,z)
        identities[name]={'constant_on_normalized_face':str(constant),
            'formula':'g dot (z,K) - constant O = sum signed_weight R_positive + sum signed_residual_j variable_j',
            'normalization_coefficient':str(payment[0]),
            'signed_row_weights':{n:str(w) for n,w in zip(positive_names,payment[1:]) if w},
            'all257_signed_residuals':[str(v) for v in remainder],
            'residuals_vanish_on_entire_zero_domain':True}
    save('face_signed_identities.json',identities)
    gaps={str(T):F(identities[f'K_minus_size_A{T}']['constant_on_normalized_face']) for T in (4,5,6)}
    for T,Q in [(4,7),(5,6),(6,5)]:
        name=f'PORTFOLIO31_i2_T{T}_Q{Q}'
        assert F(cert['dual']['row_weights'][name])>0
        assert dot(vec(rows_by_name[name]['a']),z)==0 and gaps[str(T)]>0
    result={'status':'PASS','optimizer_calls':0,'input_sha256':sha(HERE/'exact_input.json'),
        'certificate_sha256':sha(HERE/'exact_certificate.json'),'literal_source2_states':128,'zero_state_table':table,
        'necessary_equality':'If a pure source2 PORTFOLIO31(T,Q) row is tight in a real SPE, all four real tail size caps are tight and each of the first three tails is contained in T; hence K=|T|.',
        'all_optimum_face_gaps_K_minus_T':{k:str(v) for k,v in gaps.items()},
        'all_optimum_face_excluded_from_SPE':True,
        'projection_scope':'This does not change the matching lower bound or refute half; it excludes equality at this necessary-system optimum.',
        'new_matrix_rows':0,'new_optimizer_calls':0}
    save('equality_diagnostic.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='zero_state_table'},indent=2))

if __name__=='__main__':main()
