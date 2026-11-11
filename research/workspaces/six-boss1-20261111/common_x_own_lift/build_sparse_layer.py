"""Build only the 1260-row common-X own layer; never assemble or optimize an LP.

Mapping is reconstructed from the frozen full matrix's coordinate descriptors.
No primal point is opened.  Existing own_blocks is a cross-check, not a source
for the mapping or coefficients.  All writes stay in this owned directory.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import gzip
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
MATRIX = BASE / 'maxb_augmented_lp/full_lift/exact_matrix.json.gz'
MATRIX_SHA = 'c054aadf745ea4540233a3da693917498527d19d4ccecb0fdd34ad884e461e4b'
INPUTS = [MATRIX, BASE/'terminal_response_cycles/max_b_symbolic_lift.json',
          BASE/'maxb_augmented_lp/full_lift/maxb_envelope_structure.json',
          BASE/'root_x_joint_contract/own_blocks.json',
          BASE/'root_x_joint_contract/verify_kernel.py',
          BASE/'root_x_joint_contract.md', BASE/'main_common_X_pair_facets.md',
          BASE/'terminal_response_cycles.md']
FACETS = [
    ('O1', 'yQ+yR-x+m00', {'yQ':1,'yR':1,'x':-1,'00':1}, [0,3]),
    ('O2', 'm10-yQ+yR', {'10':1,'yQ':-1,'yR':1}, [1,2]),
    ('O3', 'm01+yQ-yR', {'01':1,'yQ':1,'yR':-1}, [2,1]),
    ('O4', 'm00+m10-x+yR', {'00':1,'10':1,'x':-1,'yR':1}, [1,3]),
    ('O5', 'm00+m01-x+yQ', {'00':1,'01':1,'x':-1,'yQ':1}, [2,3]),
    ('O6', 'x+m11-yQ-yR', {'x':1,'11':1,'yQ':-1,'yR':-1}, [3,0]),
]


def frozen(x):
    return tuple(map(frozen,x)) if isinstance(x,list) else x


def canonical(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def add(*terms):
    result=defaultdict(Fraction)
    for scale,row in terms:
        for j,v in row:
            result[j] += scale*Fraction(v)
    return [[j,str(v)] for j,v in sorted(result.items()) if v]


def main():
    assert digest(MATRIX)==MATRIX_SHA
    with gzip.open(MATRIX,'rt',encoding='utf-8') as f:
        matrix=json.load(f)
    columns=matrix['columns']
    assert len(columns)==21021 and len(matrix['rows'])==22297
    assert matrix['all_columns_nonnegative']
    hist={}; rz=defaultdict(dict); b4=defaultdict(dict); xmap={}; ymap={}; legacy_hist={}
    for j,c in enumerate(columns):
        if c['kind']=='hist':
            h=j; hist[h]=c
        elif c['kind']=='joint-reply':
            assert j<4849
            # hist_column_old is a legacy coordinate, not the current H index.
            legacy=c['hist_column_old']
            assert legacy_hist.setdefault(legacy,h)==h
            rz[h,frozen(c['group'])][tuple(c['state'])]=j
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            assert c['ell'] in (0,6)
            b4[c['hist_column']][tuple(c['hidden'])+(c['ell']//6,)]=j
        elif c['kind']=='common-X-mass':
            xmap[c['hist_column']]=j
        elif c['kind']=='X-query-overlap-upper':
            ymap[c['hist_column'],frozen(c['query_token'])]=j
    assert len(hist)==16 and len(rz)==194 and len(b4)==16
    assert list(xmap.values())==list(range(20585,20601))
    assert sorted(ymap.values())==list(range(20601,21021))
    small_rows=defaultdict(list)
    for i,row in enumerate(matrix['rows']):
        if len(row)<=9:
            small_rows[frozen(row)].append(i)

    def old_row(row):
        ids=small_rows[frozen(row)]
        assert len(ids)==1,(row,ids)
        i=ids[0]
        return dict(row_index=i,name=matrix['row_names'][i],row=matrix['rows'][i])

    blocks=[]; rows=[]
    for (h,tq),yq in sorted(ymap.items(),key=lambda kv:kv[1]):
        if tq[0]=='R':
            group=tq[1]; d=rz[h,group]
            assert set(d)=={(0,1),(1,0),(1,1)}
            mass={'00':add((1,[[h,'1']]),(-1,[[j,'1'] for j in d.values()])),
                  '10':[[d[1,0],'1']],'01':[[d[0,1],'1']],'11':[[d[1,1],'1']]}
            tr=('Z',group); key=['own-RZ',h,group]; labels=['R','Z']
            nonneg={s:dict(nonnegative_columns=[d[tuple(map(int,s))]]) for s in ('10','01','11')}
            nonneg['00']=dict(inherited_inequality=old_row(mass['00']))
            mass_identity=dict(kind='coefficient-identity',sum_atoms_minus_H=[])
        elif tq==('H',0):
            d=b4[h]
            assert set(d)=={tuple(map(int,f'{k:03b}')) for k in range(8)}
            mass={s:[[j,'1'] for t,j in sorted(d.items()) if t[:2]==tuple(map(int,s))]
                  for s in ('00','10','01','11')}
            tr=('H',1); key=['B4-H1H2',h]; labels=['H1','H2']
            nonneg={s:dict(nonnegative_columns=[j for j,_ in row]) for s,row in mass.items()}
            residual=add(*[(1,r) for r in mass.values()],(-1,[[h,'1']]))
            mass_identity=dict(kind='inherited-two-sided-equality',sum_atoms_minus_H=residual,
                               positive=old_row(residual),negative=old_row(add((-1,residual))))
        else:
            continue
        yr=ymap[h,tr]; x=xmap[h]
        q=add((1,mass['10']),(1,mass['11']))
        r=add((1,mass['01']),(1,mass['11']))
        assert q==columns[yq]['query_marginal'] and r==columns[yr]['query_marginal']
        upper=[old_row([[x,'1'],[yq,'-1']]),old_row(add((1,q),(-1,[[yq,'1']]))),
               old_row([[x,'1'],[yr,'-1']]),old_row(add((1,r),(-1,[[yr,'1']])))]
        block=dict(block=len(blocks),key=key,labels=labels,H_column=h,X_column=x,
                   yQ_column=yq,yR_column=yr,query_tokens=[tq,tr],mass_by_QR=mass,
                   query_marginals=[q,r],old_upper_rows=[a['row_index'] for a in upper],
                   base_contract=dict(X_at_most_H=old_row([[h,'1'],[x,'-1']]),
                                      overlap_upper_bounds=upper,atom_nonnegativity=nonneg,
                                      mass_identity=mass_identity,
                                      nonnegative_core_columns=[h,x,yq,yr]))
        symbols={**mass,'x':[[x,'1']],'yQ':[[yq,'1']],'yR':[[yr,'1']]}
        for facet,formula,template,pair in FACETS:
            row=add(*[(v,symbols[s]) for s,v in template.items()])
            i=len(rows)
            rows.append(dict(local_row=i,append_index_if_used=22297+i,
                             name=f'common-X-own:{len(blocks)}:{facet}',
                             block=len(blocks),key=key,facet=facet,formula=formula,
                             beta_comparison=dict(lower_index=pair[0],upper_index=pair[1]),
                             inequality='>=0',constant='0',row=row,
                             base_contract_block=len(blocks),
                             mass_equality_rows=([mass_identity['positive']['row_index'],
                                                  mass_identity['negative']['row_index']]
                                                 if mass_identity['kind']=='inherited-two-sided-equality' else [])))
        blocks.append(block)
    assert len(blocks)==210 and len(rows)==1260
    used=sorted({j for record in rows for j,_ in record['row']} |
                {b['H_column'] for b in blocks})
    assert len(used)==1162
    lift=json.loads((BASE/'terminal_response_cycles/max_b_symbolic_lift.json').read_text())
    zero_hist=lift['zero_histograms']
    assert zero_hist==[1,59,366,449,524,574]
    prior=json.loads((BASE/'root_x_joint_contract/own_blocks.json').read_text())
    for own,old in zip(blocks,prior['blocks']):
        for k in ('block','key','labels','H_column','X_column','yQ_column','yR_column','mass_by_QR','old_upper_rows'):
            assert frozen(own[k])==frozen(old[k]),(own['block'],k)
    output=dict(schema='common-X-own-sparse-layer-v1',
                status='FROZEN_SYMBOLIC_LAYER_NO_POINT_USED',
                run='six-boss1-20261111',base_rows=22297,coordinate_count=21021,
                row_count=len(rows),new_columns=0,nonzeros=sum(len(r['row']) for r in rows),
                hypothetical_appended_shape=[23557,21021],larger_matrix_assembled=False,
                block_count=210,own_RZ_blocks=194,B4_H1H2_blocks=16,
                inputs=[dict(path=str(p.relative_to(BASE)),sha256=digest(p)) for p in INPUTS],
                builder_sha256=digest(Path(__file__)),
                coordinate_descriptors_sha256=sha256(canonical(columns)).hexdigest(),
                relevant_columns=used,
                relevant_descriptors_sha256=sha256(canonical([[j,columns[j]] for j in used])).hexdigest(),
                hist_records=[[h,c] for h,c in hist.items()],all_16_histograms_retained=True,
                legacy_hist_column_old_to_full=sorted(legacy_hist.items()),
                historically_zero_histograms=zero_hist,histogram_values_not_read=True,
                facet_order=[a[0] for a in FACETS],
                beta_lower_order=['0','yQ-m10','yR-m01','yQ+yR-x'],
                beta_upper_order=['m11','yQ','yR','m00-x+yQ+yR'],
                semantics=dict(X='One fixed full-catalog f_P-maximizing label, shared by all hist/query groups.',
                               promoted_real_core_columns=list(range(20601,21021)),
                               canonical_min_for_promoted_columns=False,
                               old_canonical_max_count=7954,old_canonical_min_count=2790,
                               old_10744_auxiliary_semantics_unchanged=True,
                               beta='Eliminated explanation variable; never an added coordinate.',
                               conclusion_scope='Exact local own-pair completion, not full shared hidden law or SPE.'),
                blocks=blocks,rows=rows,
                counts_by_hist=[dict(H_column=h,X_column=xmap[h],
                                    RZ_blocks=sum(b['H_column']==h and b['key'][0]=='own-RZ' for b in blocks),
                                    B4_blocks=1,rows=6*sum(b['H_column']==h for b in blocks)) for h in hist])
    (HERE/'own_facets.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ('status','row_count','coordinate_count','new_columns','nonzeros')}))
    print('own_facets_sha256='+digest(HERE/'own_facets.json'))


if __name__=='__main__':
    main()
