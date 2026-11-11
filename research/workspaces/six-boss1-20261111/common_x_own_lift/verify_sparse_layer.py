"""Independent exact audit of the standalone 1260 common-X own rows.

No imports from a builder, evaluator, recovery or optimizer.  Reconstruction
starts from original column descriptors, derives all 16 comparisons from the
eight nonnegative cells, and proves that precisely ten are inherited.
This program never reads any primal point.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip
import json

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
SOURCE=BASE/'maxb_augmented_lp/full_lift/exact_matrix.json.gz'
SOURCE_SHA='c054aadf745ea4540233a3da693917498527d19d4ccecb0fdd34ad884e461e4b'


def sha(path): return sha256(path.read_bytes()).hexdigest()


def json_hash(value):
    return sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def key(value):
    if isinstance(value,list): return tuple(key(t) for t in value)
    return value


def combine(*terms):
    out={}
    for scale,row in terms:
        for j,a in row.items(): out[j]=out.get(j,F())+scale*a
    return {j:a for j,a in out.items() if a}


def decode(row):
    assert len(row)==len({j for j,_ in row})
    return {j:F(v) for j,v in row}


def substitution(vector,forms):
    return combine(*[(a,forms[s]) for s,a in vector.items()])


def main():
    counts=Counter()
    layer=json.loads((HERE/'own_facets.json').read_text())
    assert sha(SOURCE)==SOURCE_SHA
    for src in layer['inputs']:
        assert sha(BASE/src['path'])==src['sha256']
    assert sha(HERE/'build_sparse_layer.py')==layer['builder_sha256']
    with gzip.open(SOURCE,'rt',encoding='utf-8') as f: source=json.load(f)
    columns=source['columns']
    assert len(columns)==21021 and len(source['rows'])==22297
    assert json_hash(columns)==layer['coordinate_descriptors_sha256']
    assert layer['row_count']==len(layer['rows'])==1260 and layer['new_columns']==0
    assert layer['coordinate_count']==21021 and not layer['larger_matrix_assembled']
    assert layer['semantics']['canonical_min_for_promoted_columns'] is False
    assert layer['semantics']['old_10744_auxiliary_semantics_unchanged'] is True
    assert layer['semantics']['promoted_real_core_columns']==list(range(20601,21021))
    old_hist={j:c for j,c in enumerate(columns[:4849]) if c['kind']=='hist'}
    old_atoms=defaultdict(dict); b4_atoms=defaultdict(list)
    # Recover ownership from the original H-sum(three atoms)>=0 row.  This is
    # independent of the generator's nearest-hist column scan.  The descriptor
    # field hist_column_old belongs to an earlier coordinate numbering.
    atom_to_hist={}; legacy_hist={}
    for i,name in enumerate(source['row_names']):
        if not name.startswith('joint-state-upper:'): continue
        row=decode(source['rows'][i])
        positive=[j for j,a in row.items() if a==1]
        negative=[j for j,a in row.items() if a==-1]
        assert len(row)==4 and len(positive)==1 and len(negative)==3
        h=positive[0]; assert h in old_hist
        for j in negative:
            assert columns[j]['kind']=='joint-reply' and j not in atom_to_hist
            atom_to_hist[j]=h
    assert len(atom_to_hist)==582
    for j,c in enumerate(columns[:4849]):
        if c['kind']=='joint-reply':
            h=atom_to_hist[j]
            assert legacy_hist.setdefault(c['hist_column_old'],h)==h
            old_atoms[h,key(c['group'])][tuple(c['state'])]=j
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            assert c['ell'] in (0,6)
            b4_atoms[c['hist_column']].append((j,tuple(c['hidden']),c['ell']))
    assert layer['legacy_hist_column_old_to_full']==[[a,b] for a,b in sorted(legacy_hist.items())]
    assert len(legacy_hist)==16
    new_x={}; new_y={}
    # Independent of the generator's scan: derive all new identities from the
    # compressed source lift, then compare the full matrix's final 436 columns.
    lift=json.loads((BASE/'terminal_response_cycles/max_b_symbolic_lift.json').read_text())
    assert columns[20585:]==lift['new_columns']
    for j,c in enumerate(lift['new_columns'],20585):
        if c['kind']=='common-X-mass': new_x[c['hist_column']]=j
        else:
            assert c['kind']=='X-query-overlap-upper'
            new_y[c['hist_column'],key(c['query_token'])]=j
    env=json.loads((BASE/'maxb_augmented_lp/full_lift/maxb_envelope_structure.json').read_text())
    assert dict(env['hist_to_x'])==new_x
    assert len(old_atoms)==194 and len(b4_atoms)==16 and len(new_y)==420
    own_reference=json.loads((BASE/'root_x_joint_contract/own_blocks.json').read_text())

    # Eight cell expressions in (m00,m10,m01,m11,x,yQ,yR,beta).
    # Split on beta's coefficient to eliminate beta by Fourier--Motzkin.
    cells=[
        ('psi00',{'x':1,'yQ':-1,'yR':-1,'beta':1}),
        ('psi10',{'yQ':1,'beta':-1}),
        ('psi01',{'yR':1,'beta':-1}),
        ('psi11',{'beta':1}),
        ('rest00',{'00':1,'x':-1,'yQ':1,'yR':1,'beta':-1}),
        ('rest10',{'10':1,'yQ':-1,'beta':1}),
        ('rest01',{'01':1,'yR':-1,'beta':1}),
        ('rest11',{'11':1,'beta':-1}),
    ]
    lower_by_cell={}; upper_by_cell={}
    for name,cell in cells:
        b=cell['beta']; rest={s:F(v) for s,v in cell.items() if s!='beta'}
        if b==1: lower_by_cell[name]={s:-v for s,v in rest.items()}
        else:
            assert b==-1
            upper_by_cell[name]=rest
    lower=[lower_by_cell[s] for s in ('psi11','rest10','rest01','psi00')]
    upper=[upper_by_cell[s] for s in ('rest11','psi10','psi01','rest00')]
    comparisons={(i,j):combine((1,upper[j]),(-1,lower[i])) for i in range(4) for j in range(4)}
    new_positions=[(0,3),(1,2),(2,1),(1,3),(2,3),(3,0)]
    inherited={(0,0):'m11',(0,1):'yQ',(0,2):'yR',(1,0):'q-yQ',
               (1,1):'m10',(2,0):'r-yR',(2,2):'m01',(3,1):'x-yR',
               (3,2):'x-yQ',(3,3):'m00'}
    assert set(comparisons)==set(new_positions)|set(inherited)
    assert not set(new_positions)&set(inherited)
    table=[dict(lower_index=i,upper_index=j,classification=(f'O{new_positions.index((i,j))+1}'
              if (i,j) in new_positions else inherited[i,j]),
              coefficients={s:str(v) for s,v in comparisons[i,j].items()})
           for i in range(4) for j in range(4)]
    touched=set(); touched_y=set(); signed_y=defaultdict(Counter); hist_counts=Counter()
    independent_blocks=[]
    for h in sorted(old_hist):
        entries=[]
        for (hh,g),atom in old_atoms.items():
            if hh!=h: continue
            assert set(atom)=={(0,1),(1,0),(1,1)}
            forms={'00':{h:F(1),**{j:F(-1) for j in atom.values()}},
                   '10':{atom[1,0]:F(1)},'01':{atom[0,1]:F(1)},'11':{atom[1,1]:F(1)}}
            entries.append((new_y[h,('R',g)],['own-RZ',h,g],forms,('R',g),('Z',g)))
        ba=b4_atoms[h]
        assert len(ba)==8 and {(s,e) for _,s,e in ba}==set(product(product((0,1),repeat=2),(0,6)))
        forms={f'{a}{b}':{j:F(1) for j,s,e in ba if s==(a,b)} for a,b in product((0,1),repeat=2)}
        entries.append((new_y[h,('H',0)],['B4-H1H2',h],forms,('H',0),('H',1)))
        independent_blocks.extend(sorted(entries,key=lambda z:z[0]))
    assert len(independent_blocks)==210
    for bid,(yq,bkey,forms,tq,tr) in enumerate(independent_blocks):
        b=layer['blocks'][bid]; prior=own_reference['blocks'][bid]; h=bkey[1]
        x=new_x[h]; yr=new_y[h,tr]
        assert b['block']==bid and key(b['key'])==key(bkey)
        assert [b[k] for k in ('H_column','X_column','yQ_column','yR_column')]==[h,x,yq,yr]
        assert key(b['query_tokens'])==(tq,tr)
        assert b['labels']==(['R','Z'] if bkey[0]=='own-RZ' else ['H1','H2'])
        for state,row in forms.items():
            assert decode(b['mass_by_QR'][state])==row
            assert decode(prior['mass_by_QR'][state])==row
        assert all(b[k]==prior[k] for k in ('block','labels','H_column','X_column','yQ_column','yR_column','old_upper_rows'))
        assert key(prior['key'])==key(bkey)
        q=combine((1,forms['10']),(1,forms['11']))
        r=combine((1,forms['01']),(1,forms['11']))
        assert decode(columns[yq]['query_marginal'])==q and decode(columns[yr]['query_marginal'])==r
        assert [decode(a) for a in b['query_marginals']]==[q,r]
        base=b['base_contract']
        def check_witness(record,expected):
            i=record['row_index']
            assert 0<=i<22297 and record['name']==source['row_names'][i]
            assert record['row']==source['rows'][i]
            assert decode(source['rows'][i])==expected
            counts['inherited_row_witness_checks']+=1
        check_witness(base['X_at_most_H'],{h:F(1),x:F(-1)})
        bounds=[{x:F(1),yq:F(-1)},combine((1,q),(-1,{yq:F(1)})),
                {x:F(1),yr:F(-1)},combine((1,r),(-1,{yr:F(1)}))]
        for rec,expected in zip(base['overlap_upper_bounds'],bounds): check_witness(rec,expected)
        assert b['old_upper_rows']==[rec['row_index'] for rec in base['overlap_upper_bounds']]
        for state,expected in forms.items():
            proof=base['atom_nonnegativity'][state]
            if 'inherited_inequality' in proof:
                assert state=='00' and bkey[0]=='own-RZ'
                check_witness(proof['inherited_inequality'],expected)
            else:
                assert expected=={j:F(1) for j in proof['nonnegative_columns']}
                assert source['all_columns_nonnegative']
            counts['atom_nonnegativity_checks']+=1
        residual=combine(*[(1,v) for v in forms.values()],(-1,{h:F(1)}))
        mass_id=base['mass_identity']
        assert decode(mass_id['sum_atoms_minus_H'])==residual
        if bkey[0]=='own-RZ':
            assert not residual and mass_id['kind']=='coefficient-identity'
        else:
            assert len(residual)==9 and mass_id['kind']=='inherited-two-sided-equality'
            check_witness(mass_id['positive'],residual)
            check_witness(mass_id['negative'],combine((-1,residual)))
            counts['B4_old_mass_equalities_checked']+=1
        forms.update(x={x:F(1)},yQ={yq:F(1)},yR={yr:F(1)})
        old_forms={'m00':forms['00'],'m10':forms['10'],'m01':forms['01'],'m11':forms['11'],
                   'yQ':forms['yQ'],'yR':forms['yR'],'q-yQ':bounds[1],'r-yR':bounds[3],
                   'x-yR':bounds[2],'x-yQ':bounds[0]}
        for p,name in inherited.items():
            assert substitution(comparisons[p],forms)==old_forms[name]
            counts['ten_inherited_comparisons']+=1
        for k,p in enumerate(new_positions):
            record=layer['rows'][6*bid+k]
            expected=substitution(comparisons[p],forms)
            assert decode(record['row'])==expected
            assert record['row']==[[j,str(v)] for j,v in sorted(expected.items())]
            assert record['local_row']==6*bid+k and record['append_index_if_used']==22297+6*bid+k
            assert record['block']==record['base_contract_block']==bid
            assert record['facet']==f'O{k+1}' and record['name']==f'common-X-own:{bid}:O{k+1}'
            assert key(record['key'])==key(bkey)
            assert record['beta_comparison']==dict(lower_index=p[0],upper_index=p[1])
            assert record['inequality']=='>=0' and record['constant']=='0'
            assert record['mass_equality_rows']==([mass_id['positive']['row_index'],mass_id['negative']['row_index']]
                                                   if residual else [])
            for j,v in expected.items():
                assert 0<=j<21021 and not (4849<=j<20585)
                touched.add(j)
                if j>=20601: signed_y[j]['positive' if v>0 else 'negative']+=1
            counts['sparse_rows_independently_reconstructed']+=1
            counts['sparse_coefficients_independently_reconstructed']+=len(expected)
        touched.add(h); touched_y.update((yq,yr)); hist_counts[h]+=1
        counts['independently_reconstructed_blocks']+=1
    assert touched_y==set(range(20601,21021))
    assert all(c['negative'] and c['positive'] for c in signed_y.values())
    assert sorted(touched)==layer['relevant_columns'] and len(touched)==1162
    assert json_hash([[j,columns[j]] for j in sorted(touched)])==layer['relevant_descriptors_sha256']
    assert dict(hist_counts)=={h:sum(b['H_column']==h for b in layer['blocks']) for h in old_hist}
    assert set(hist_counts)==set(old_hist)==set(new_x)
    assert layer['historically_zero_histograms']==lift['zero_histograms']==[1,59,366,449,524,574]
    assert layer['nonzeros']==counts['sparse_coefficients_independently_reconstructed']

    # Exhaustive small integer populations are a supplementary check, not the
    # universal proof.  They include zero fibres, repeated labels and x=0,H.
    irredundancy={}
    for H in range(6):
        for masses in product(range(H+1),repeat=4):
            if sum(masses)!=H: continue
            m00,m10,m01,m11=masses
            for X in range(H+1):
                for yq in range(min(X,m10+m11)+1):
                    for yr in range(min(X,m01+m11)+1):
                        vals=dict(zip(('00','10','01','11','x','yQ','yR'),masses+(X,yq,yr)))
                        ev=lambda form: sum((a*vals[s] for s,a in form.items()),F())
                        low=list(map(ev,lower)); high=list(map(ev,upper))
                        slacks=[ev(comparisons[p]) for p in new_positions]
                        witnesses=[]
                        for beta in range(H+1):
                            vals['beta']=beta
                            if all(ev(row)>=0 for _,row in cells): witnesses.append(beta)
                        assert bool(witnesses)==(max(low)<=min(high))==(min(slacks)>=0)
                        if witnesses:
                            assert min(witnesses)==max(low) and max(witnesses)==min(high)
                        negative=[k for k,v in enumerate(slacks) if v<0]
                        if len(negative)==1 and negative[0] not in irredundancy:
                            irredundancy[negative[0]]=dict(H=H,masses=list(masses),x=X,yQ=yq,yR=yr,
                                                          slacks=list(map(str,slacks)))
                        counts['integer_population_interval_eight_cell_cases']+=1
                        if H==0: counts['zero_population_cases']+=1
                        if X in (0,H): counts['X_endpoint_cases']+=1
                        if m10==m01==0: counts['equal_coverage_QR_cases']+=1
    assert set(irredundancy)==set(range(6))
    # Exact rational counterexample: fixed canonical y fails; same x, new y works.
    counter=[]
    for q in (F(1,2),F(1,4)):
        vals={'00':F(),'10':F(1,2),'01':F(1,2),'11':F(),'x':F(1,2),'yQ':q,'yR':q}
        ev=lambda row:sum((a*vals[s] for s,a in row.items()),F())
        lo=max(map(ev,lower)); hi=min(map(ev,upper))
        counter.append(dict(yQ=str(q),yR=str(q),L=str(lo),U=str(hi),complete=lo<=hi))
    assert not counter[0]['complete'] and counter[1]['complete']
    report=dict(status='INDEPENDENT_COMMON_X_OWN_SPARSE_LAYER_PASS',checks=dict(counts),
                row_count=1260,coordinate_count=21021,new_columns=0,
                all_16_histograms_retained=True,all_6_historically_zero_histograms_retained=True,
                promoted_y_columns_with_both_coefficient_signs=len(signed_y),
                sixteen_comparison_partition=table,
                six_generic_facets_individually_needed=[dict(facet=f'O{k+1}',**irredundancy[k]) for k in range(6)],
                fixed_canonical_failure_does_not_exclude_reselected_y=counter,
                LP_calls=0,primal_point_reads=0,larger_matrix_assembled=False,
                original_10744_auxiliary_columns_touched_by_new_rows=0,
                row_package_sha256=sha(HERE/'own_facets.json'),
                verifier_sha256=sha(Path(__file__)),
                input_matrix_sha256=SOURCE_SHA,
                scope='Exact local own-pair projection only. No full hidden law, cross-group identity, or SPE claim.')
    (HERE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','row_count','coordinate_count','new_columns','checks')},ensure_ascii=False))


if __name__=='__main__': main()
