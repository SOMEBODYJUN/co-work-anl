"""Prepare the complete one-structure624 hidden lift; do not optimize.

Retain the full11418x7639 certified ZZ extension. On each of the16 histograms,
every valid family0 off-diagonal word-pair group receives all4 R/Z states and
all16 shared macro hidden states, regardless of any current zero mass.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict,Counter
import json,gzip,io,hashlib,time,sys
import reverse_terminal_624_v1 as cone
from separate_master import blocks_from_columns,div

HERE=Path(__file__).resolve().parent
MASTER=HERE.parent/'master_cuts'
STEM='complete624_actual4_R00_v1'
BASE=MASTER/'complete_zz_5799_v1_matrix.json.gz'
POINT=MASTER/'complete_zz_5799_v1_exact.json'
SEMANTIC_POINT=MASTER/'complete_zz_5799_v1_original4849_exact.json'
BASE_SHA='8b076497ef826b60c797edcb8dc719f2f7ad678a01a34ecf66d2e757af525a20'
POINT_SHA='e5cd48369fc08f652490b09ecddc80dbacc09dd45d06e5fe97dc64de3f247075'
SEMANTIC_SHA='1af6fd35f9cf1a51220072e627df042b450a52a7c6ecac388a98247ecac043d2'
RZ_STATES=tuple(product((0,1),repeat=2))
HIDDEN=tuple(product((0,1),repeat=4))


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def canonical(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def save(suffix,data):
    path=HERE/f'{STEM}_{suffix}.json';assert not path.exists(),path
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');return path
def add_row(rows,name,entries,kind,**metadata):
    entries=sorted(([int(i),str(F(v))] for i,v in entries if F(v)),key=lambda item:item[0])
    assert len(entries)==len({i for i,v in entries})
    row={'index':len(rows),'name':name,'sparse_sha256':canonical(entries),'nonzero':entries,'new_row_kind':kind,**metadata}
    rows.append(row);return row['index']


def main():
    started=time.monotonic();assert sha(BASE)==BASE_SHA and sha(POINT)==POINT_SHA and sha(SEMANTIC_POINT)==SEMANTIC_SHA
    output=HERE/f'{STEM}_matrix.json.gz';assert not output.exists()
    with gzip.open(BASE,'rt',encoding='utf-8') as f:base=json.load(f)
    point=json.loads(POINT.read_text());semantic=json.loads(SEMANTIC_POINT.read_text())
    assert base['row_count']==11418 and base['column_count']==7639
    assert [{k:v for k,v in c.items() if k!='weight'} for c in point['columns']]==base['columns']
    assert point['columns'][:4849]==semantic['columns']
    blocks=blocks_from_columns(base['columns'][:4849]);assert len(blocks)==16
    assert tuple(h[:4] for h in cone.base.hidden_configs(3))==HIDDEN
    # The entire combinatorial domain is obtained from descriptors. Current
    # point weights are not consulted until after all rows/columns are built.
    geometry=[]
    for block in blocks:
        groups=defaultdict(dict)
        for ci,column in block['joint']:
            family,diag,wi,wj=column['group']
            if (family,diag)==(0,0):groups[tuple(wi),tuple(wj)][tuple(column['state'])]=ci
        pairs=defaultdict(list)
        for left in range(6):
            for right in range(6):
                if left!=right:pairs[block['words'][left],block['words'][right]].append((left,right))
        assert set(groups)==set(pairs) and sum(map(len,pairs.values()))==30
        for group in sorted(groups):
            assert set(groups[group])=={(0,1),(1,0),(1,1)}
            wi,wj=group;counts=Counter(block['words']);multiplicity=counts[wi]*(counts[wj]-int(wi==wj))
            assert multiplicity==len(pairs[group])>0
            geometry.append((block,group,groups[group],pairs[group],multiplicity))
    assert len(geometry)==78
    nbase=7639;mbase=11418;new_count=len(geometry)*4*16;columns=list(base['columns']);rows=list(base['rows']);bud=cone.budget(3)
    budget_entries=[]
    for br,bu,bK in bud:
        entries=[]
        if bK:entries.append([0,str(F(bK))])
        for block in blocks:
            a=block['a'];coefficient=br*div(a[3],sum(a))+bu*div(a[5],sum(a))
            if coefficient:entries.append([block['ci'],str(coefficient)])
        budget_entries.append(entries)
    maps=[];literal_query_checks=0;zero_domain_states=[]
    for group_index,(block,group,state_columns,pairs,multiplicity) in enumerate(geometry):
        hist=block['ci'];a,words=block['a'],block['words'];p,ell=sum(a[:3]),sum(a[:5]);wi,wj=group;weight=F(multiplicity,30)
        left,right=pairs[0];state_records=[]
        for state_index,state in enumerate(RZ_STATES):
            qs,mu=cone.base.queries_and_moments(a,words,left,right,*state)
            for li,rj in pairs:
                assert cone.base.queries_and_moments(a,words,li,rj,*state)==(qs,mu);literal_query_checks+=1
            if state==(0,0):marginal=[[hist,'1']]+[[state_columns[s],'-1'] for s in ((0,1),(1,0),(1,1))]
            else:marginal=[[state_columns[state],'1']]
            hidden_columns=[]
            for hi,hidden in enumerate(HIDDEN):
                ci=len(columns);assert ci==nbase+64*group_index+16*state_index+hi
                columns.append({'kind':'actual4-R-shared624-conditional-mass','hist_column':hist,'group':[0,0,list(wi),list(wj)],'state':list(state),'macro_hidden':list(hidden),'meaning':'per-selected-word-pair joint mass; orbit multiplicity is applied in budget rows'})
                hidden_columns.append(ci)
                vector=cone.feature_vector(p,ell,state[0],qs,mu,hi,3,(0,0));assert len(vector)==624
                for ni,value in enumerate(vector):
                    if value:budget_entries[ni].append([ci,str(-weight*value)])
            equality=[[ci,'1'] for ci in hidden_columns]+[[ci,str(-F(value))] for ci,value in marginal]
            plus=add_row(rows,f'macro624:margin:g{group_index}:rz{state[0]}{state[1]}:+',equality,'shared-macro-marginal-equality-plus',group_index=group_index,state=list(state))
            minus=add_row(rows,f'macro624:margin:g{group_index}:rz{state[0]}{state[1]}:-',[[ci,str(-F(value))] for ci,value in equality],'shared-macro-marginal-equality-minus',group_index=group_index,state=list(state))
            assert plus==mbase+2*(4*group_index+state_index) and minus==plus+1
            state_records.append({'state':list(state),'old_marginal_affine':sorted(marginal),'hidden_columns':hidden_columns,'equality_plus_row':plus,'equality_minus_row':minus,'visible':{'p':p,'ell':ell,'t':state[0],'queries':list(map(str,qs)),'moments':list(map(str,mu))}})
        maps.append({'group_index':group_index,'hist_column':hist,'actual_bits':''.join(map(str,a)),'hist':block['column']['hist'],'six_words':[list(w) for w in words],'group':[0,0,list(wi),list(wj)],'literal_index_pairs':[list(pair) for pair in pairs],'multiplicity':multiplicity,'orbit_weight':str(weight),'states':state_records})
    budget_start=len(rows);assert budget_start==12042
    budget_map=[]
    for ni,(name,entries,coefficients) in enumerate(zip(cone.NAMES,budget_entries,bud)):
        ri=add_row(rows,'macro624:budget:'+name,entries,'complete-shared-macro624-budget',feature_index=ni,feature_name=name)
        budget_map.append({'feature_index':ni,'feature_name':name,'row_index':ri,'external_coefficients':{'u4':str(F(coefficients[0])),'u6':str(F(coefficients[1])),'K':str(F(coefficients[2]))},'identically_zero_row':not rows[ri]['nonzero']})
    assert len(columns)==12631 and len(rows)==12666 and new_count==4992
    assert rows[:mbase]==base['rows'] and columns[:nbase]==base['columns']
    assert all(not (4849<=ci<nbase) for row in rows[mbase:] for ci,value in row['nonzero'])
    assert all(ci<nbase for row in rows[:mbase] for ci,value in row['nonzero'])
    for item in maps:
        for state in item['states']:
            first=rows[state['equality_plus_row']]['nonzero'];second=rows[state['equality_minus_row']]['nonzero']
            assert first==[[ci,str(-F(value))] for ci,value in second]
    # Exact algebraic elimination identity for the new624 separator: weighted
    # raw budgets + pointwise nonnegative min residual + signed mass equalities
    # equals the old-coordinate projected row, zero on every auxiliary column.
    separator_path=HERE/'reverse_terminal_5799_one_v1.json';separator_raw=separator_path.read_bytes();separator=json.loads(separator_raw)['cuts'][0]
    theta={name:F(value) for name,value in separator['weights'].items()}
    expected,au,aK,psi=cone.make_row(base['columns'],blocks,0,(0,0),3,theta);expected+=([F(0)]*new_count)
    saved=[F(0)]*4849
    for ci,value in separator['sparse_row']:saved[ci]=F(value)
    assert expected[:4849]==saved and all(value==0 for value in expected[4849:])
    combined=defaultdict(F)
    for name,multiplier in theta.items():
        feature=cone.NAMES.index(name)
        for ci,value in rows[budget_map[feature]['row_index']]['nonzero']:combined[ci]+=multiplier*F(value)
    residual_count=0
    for item in maps:
        weight=F(item['orbit_weight'])
        for state in item['states']:
            v=state['visible'];minimum=psi(v['p'],v['ell'],v['t'],tuple(map(F,v['queries'])),tuple(map(F,v['moments'])))
            for ci in state['hidden_columns']:
                cost=-combined[ci]/weight;residual=weight*(cost-minimum);assert residual>=0
                residual_count+=bool(residual);combined[ci]+=residual
            for ci,value in rows[state['equality_plus_row']]['nonzero']:combined[ci]+=weight*minimum*F(value)
    assert all(combined[ci]==value for ci,value in enumerate(expected))
    # A margin-only completion at the new exact ZZ point: use h=0000 for each
    # positive old state. This checks all links, and makes NO budget feasibility
    # or optimality claim about the candidate extension.
    old_values=[F(c['weight']) for c in point['columns']];fill=old_values+[F(0)]*new_count
    zero_hist_count=sum(old_values[b['ci']]==0 for b in blocks);zero_marginal_count=0
    for item in maps:
        for state in item['states']:
            mass=sum(old_values[ci]*F(value) for ci,value in state['old_marginal_affine']);assert mass>=0
            zero_marginal_count+=mass==0;fill[state['hidden_columns'][0]]=mass
    for row in rows[mbase:budget_start]:assert sum(F(value)*fill[ci] for ci,value in row['nonzero'] if fill[ci])==0
    fill_budget=[sum(F(value)*fill[ci] for ci,value in row['nonzero'] if fill[ci]) for row in rows[budget_start:]]
    objective=base['objective']+['0']*new_count;normalization=base['normalization']+['0']*new_count
    assert sum(F(value)*x for value,x in zip(normalization,fill) if value!='0' and x)==1
    assert sum(F(value)*x for value,x in zip(objective,fill) if value!='0' and x)==F(point['W'])
    extended=dict(base);extended.update({'scope':'Prepared complete624 hidden lift for exactly actual4/R/family0-off on the fixed16 histograms, retaining every certified39-class ZZ auxiliary and every old row. No optimization, no SPE completion claim.','base_row_count':mbase,'base_column_count':nbase,'added_row_count':len(rows)-mbase,'added_column_count':new_count,'row_count':len(rows),'column_count':len(columns),'rows':rows,'columns':columns,'objective':objective,'normalization':normalization,'nonnegative_columns':'all','complete_macro624_structure':{'source_index':3,'member':0,'orbit':[0,0],'histograms':16,'word_pair_groups':78,'RZ_states_per_group':4,'hidden_states_per_RZ_state':16,'semantic_old_column_prefix':4849,'preserved_ZZ_auxiliary_columns':2790}})
    with output.open('wb') as file:
        with gzip.GzipFile(fileobj=file,mode='wb',filename='',mtime=0,compresslevel=6) as zipped:
            with io.TextIOWrapper(zipped,encoding='utf-8') as text:json.dump(extended,text,ensure_ascii=False,separators=(',',':'))
    mapping_path=save('mapping',{'scope':'All structural columns and raw budgets, built solely from the fixed descriptors, including zero-mass types/states.','base_matrix_path':str(BASE),'base_matrix_sha256':BASE_SHA,'base_point_sha256':POINT_SHA,'semantic_point_sha256':SEMANTIC_SHA,'base_column_prefix':nbase,'semantic_old_column_prefix':4849,'base_row_prefix':mbase,'new_column_range':[nbase,len(columns)],'link_row_range':[mbase,budget_start],'budget_row_range':[budget_start,len(rows)],'hidden_state_order':[list(h) for h in HIDDEN],'RZ_state_order':[list(s) for s in RZ_STATES],'groups':maps,'budgets':budget_map,'new_column_index_formula':'7639+64*group_index+16*(2*r+z)+(8*b+4*c+2*j+v)','equality_plus_formula':'sum hidden masses - old marginal = 0; a separate negative row is retained'})
    fill_path=save('margin_fill',{'scope':'Only a canonical margin completion at the new ZZ point; NOT asserted624-budget-feasible.','base_point_sha256':POINT_SHA,'new_nonzero_columns':[[ci,str(value)] for ci,value in enumerate(fill) if ci>=nbase and value],'all312_margin_equalities_exact':True,'minimum624_budget_slack':str(min(fill_budget)),'negative624_budget_rows':sum(value<0 for value in fill_budget),'all624_budget_slacks':list(map(str,fill_budget))})
    identity=save('identity',{'status':'PREPARED_EXACT_NOT_OPTIMIZED','base_matrix_sha256':BASE_SHA,'base_point_sha256':POINT_SHA,'semantic_point_sha256':SEMANTIC_SHA,'base_rows':mbase,'base_columns':nbase,'rows':len(rows),'columns':len(columns),'word_pair_groups':78,'new_hidden_columns':new_count,'marginal_equalities':312,'encoded_margin_rows':624,'raw_budget_rows':624,'identically_zero_raw_budget_rows':[item['feature_name'] for item in budget_map if item['identically_zero_row']],'new_nonzeros':sum(len(row['nonzero']) for row in rows[mbase:]),'all_nonzeros':sum(len(row['nonzero']) for row in rows),'old_rows_exactly_unchanged':True,'old_columns_exactly_unchanged':True,'objective_and_normalization_zero_extended':True,'no_new_read_of_ZZ_auxiliaries':True,'literal_query_equivalence_checks':literal_query_checks,'current_zero_histograms_still_retained':zero_hist_count,'current_zero_RZ_marginals_still_retained':zero_marginal_count,'all_16_hidden_columns_for_each_RZ_state':True,'projected_separator_sha256':hashlib.sha256(separator_raw).hexdigest(),'projected_separator_exact_lift_identity':True,'nonnegative_min_residual_count':residual_count,'projected_separator_value_at_new_ZZ_point':str(sum(expected[ci]*old_values[ci] for ci in range(nbase))),'matrix_sha256':sha(output),'mapping_sha256':sha(mapping_path),'margin_fill_sha256':sha(fill_path),'old_row_vector_list_sha256':canonical([row['sparse_sha256'] for row in rows[:mbase]]),'all_row_vector_list_sha256':canonical([row['sparse_sha256'] for row in rows]),'old_column_descriptor_sha256':canonical(columns[:nbase]),'all_column_descriptor_sha256':canonical(columns),'optimizer_calls':0,'mathematical_float_operations':0,'script_sha256':sha(Path(__file__)),'elapsed_seconds':time.monotonic()-started})
    report=json.loads(identity.read_text());print(json.dumps({k:report[k] for k in ('status','rows','columns','new_hidden_columns','marginal_equalities','raw_budget_rows','new_nonzeros','matrix_sha256','mapping_sha256','current_zero_histograms_still_retained','current_zero_RZ_marginals_still_retained','optimizer_calls','elapsed_seconds')},ensure_ascii=False),flush=True)


if __name__=='__main__':main()
