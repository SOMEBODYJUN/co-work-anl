"""Independent standard-library all-row/all-column rational verification.

No assembly, numerical solver, recovery, or feature-discovery module is
imported.  The exact full block is compared to its pinned symbolic transfer,
the312 marginal maps and all624 original-coordinate budgets are rebuilt,
and all20910 primal rows and20585 dual residuals are evaluated as Fractions.
"""
from collections import defaultdict,Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import gzip,json,sys,time

HERE=Path(__file__).resolve().parent
RUN=HERE.parent
arguments=sys.argv[1:]
STRUCTURE_ONLY='--structure-only' in arguments
arguments=[s for s in arguments if s!='--structure-only']
assert len(arguments)<=1
OUT=Path(arguments[0]).resolve() if arguments else HERE
BASE=RUN/'union_augmented_lp';TRANSFER=RUN/'complete624_transfer'
M,N,Q,ADDM,ADDN=19662,15593,4849,1248,4992
PINS={
    BASE/'exact_matrix.json.gz':'99253e05bfe4c5705619777a5989ec9fab5c38dc7e56f934bbe8d9c071040ded',
    BASE/'augmented_lp_exact.json':'b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3',
    BASE/'exact_dual_certificate.json':'78a7cb206f9e807d0228d20ca7eaeafaf088fc551c719ba44dad4ed10f70f5ef',
    TRANSFER/'full_lift_bundle.json.gz':'3031a0710bd3b99fe421889ccb891e671d11f019f7d9cc9b3165818adc759d03',
}
def sha(path):return sha256(path.read_bytes()).hexdigest()
def read(path):
    if str(path).endswith('.gz'):
        with gzip.open(path,'rt',encoding='utf-8') as f:return json.load(f)
    return json.loads(path.read_text())
@lru_cache(maxsize=None)
def rational(text):return Fraction(text)
def dot(row,x):return sum((rational(v)*x[j] for j,v in row if x[j]),Fraction())
def decode(row,n):
    out={}
    for j,v in row:
        assert type(j) is int and 0<=j<n and j not in out
        w=rational(v);assert w
        out[j]=w
    return out
def emit(name,data):
    p=OUT/name;assert not p.exists(),str(p)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def verify_dual(certificate,matrix,slacks,values):
    lower=Fraction(certificate['normalization_multiplier'])
    obj=list(map(Fraction,matrix['objective']));norm=list(map(Fraction,matrix['normalization']))
    residuals=[c-lower*a for c,a in zip(obj,norm)];seen=set();complement=Fraction()
    for i,v in certificate['row_multipliers']:
        assert type(i) is int and 0<=i<len(matrix['rows']) and i not in seen
        seen.add(i);lam=Fraction(v);assert lam>0
        for j,a in matrix['rows'][i]:residuals[j]-=lam*rational(a)
        if slacks is not None:complement+=lam*slacks[i]
    assert min(residuals)>=0
    assert residuals==list(map(Fraction,certificate['residuals']))
    if values is not None:
        assert complement==0
        assert sum((a*b for a,b in zip(residuals,values)),Fraction())==0
    return lower,len(seen),residuals


def main():
    started=time.monotonic()
    for p,expected in PINS.items():assert sha(p)==expected,str(p)
    inputs=read(HERE/'inputs_manifest.json')
    for relative,expected in inputs['sha256'].items():assert sha(RUN/relative)==expected,relative
    matrix=read(OUT/'exact_matrix.json.gz');old=read(BASE/'exact_matrix.json.gz')
    bundle=read(TRANSFER/'full_lift_bundle.json.gz')
    assert len(matrix['rows'])==len(matrix['row_names'])==M+ADDM
    assert len(matrix['columns'])==len(matrix['objective'])==len(matrix['normalization'])==N+ADDN
    assert matrix['rows'][:M]==old['rows'] and matrix['row_names'][:M]==old['row_names']
    assert matrix['columns'][:N]==old['columns']
    assert matrix['objective'][:N]==old['objective'] and matrix['normalization'][:N]==old['normalization']
    assert matrix['rows'][M:]==bundle['rows'] and matrix['row_names'][M:]==bundle['row_names']
    assert matrix['columns'][N:]==bundle['new_columns']
    assert matrix['objective'][N:]==matrix['normalization'][N:]==['0']*ADDN
    assert not any(map(Fraction,matrix['objective'][Q:]+matrix['normalization'][Q:]))
    assert sum(map(len,matrix['rows']))==3208797
    assert sum(map(len,matrix['rows'][M:]))==2254128
    # Validate the sparse domain of every row, including old rows.
    for row in matrix['rows']:decode(row,N+ADDN)
    assert all(j<Q or j>=N for row in matrix['rows'][M:] for j,v in row)
    blocks={};current=None
    for j,c in enumerate(old['columns'][:Q]):
        if c['kind']=='hist':current=j;blocks[j]={'descriptor':c,'groups':defaultdict(dict)}
        elif c['kind']=='joint-reply' and c['group'][:2]==[0,0]:
            key=(tuple(c['group'][2]),tuple(c['group'][3]))
            blocks[current]['groups'][key][tuple(c['state'])]=j
    assert len(blocks)==16
    expected_groups=[]
    for h,b in blocks.items():
        words=[tuple(map(int,format(i,'03b'))) for i,n in enumerate(b['descriptor']['hist']) for k in range(n)]
        assert len(words)==6
        pairs=defaultdict(list)
        for i in range(6):
            for j in range(6):
                if i!=j:pairs[(words[i],words[j])].append([i,j])
        assert sum(map(len,pairs.values()))==30
        for key,states in b['groups'].items():
            assert key in pairs and set(states)=={(0,1),(1,0),(1,1)}
            expected_groups.append((h,key,states,pairs[key]))
    assert len(expected_groups)==78
    assert len(bundle['mapping']['groups'])==78
    for gi,((hist,key,states,pairs),g) in enumerate(zip(expected_groups,bundle['mapping']['groups'])):
        assert g['group_index']==gi and g['hist_column']==hist
        assert tuple(map(tuple,g['group'][2:]))==key
        assert g['literal_index_pairs']==pairs
        assert g['multiplicity']==len(pairs) and Fraction(g['orbit_weight'])==Fraction(len(pairs),30)
        assert g['hist']==blocks[hist]['descriptor']['hist']
        assert g['actual_bits']==blocks[hist]['descriptor']['actual_bits']
        assert len(g['states'])==4
        for si,s in enumerate(g['states']):
            state=(si//2,si%2);assert s['state']==list(state)
            marginal={hist:Fraction(1),**{j:Fraction(-1) for j in states.values()}} if state==(0,0) else {states[state]:Fraction(1)}
            assert decode(s['old_marginal_affine'],Q)==marginal
            hidden=list(range(N+64*gi+16*si,N+64*gi+16*si+16))
            assert s['hidden_columns']==hidden
            plus={j:Fraction(1) for j in hidden}
            for j,v in marginal.items():plus[j]=-v
            index=M+2*(4*gi+si)
            assert (s['equality_plus_row'],s['equality_minus_row'])==(index,index+1)
            assert decode(matrix['rows'][index],N+ADDN)==plus
            assert decode(matrix['rows'][index+1],N+ADDN)=={j:-v for j,v in plus.items()}
            for offset,j in enumerate(hidden):
                c=matrix['columns'][j]
                assert c['kind']=='actual4-R-shared624-conditional-mass'
                assert c['hist_column']==hist and c['group']==g['group'] and c['state']==list(state)
                assert c['macro_hidden']==[(offset>>k)&1 for k in (3,2,1,0)]
    # Independently reconstruct all original-coordinate budget coefficients.
    zero_budgets=[]
    for alpha,b in enumerate(bundle['mapping']['budgets']):
        i=M+624+alpha;assert b['feature_index']==alpha and b['row_index']==i
        costs=b['external_coefficients'];a4,a6,K=[Fraction(costs[k]) for k in ('u4','u6','K')]
        name=b['feature_name']
        if name in ('sourceT','sourceC'):expected_costs=(Fraction(1),Fraction(),Fraction())
        elif name.startswith('price:'):expected_costs=(Fraction(),Fraction(1),Fraction())
        elif name.startswith('cap:'):expected_costs=(Fraction(),Fraction(),Fraction(1))
        else:expected_costs=(Fraction(),Fraction(),Fraction())
        # The four middle price/cap rows are identically zero and carry no external wallet.
        if b['identically_zero_row']:expected_costs=(Fraction(),Fraction(),Fraction())
        assert (a4,a6,K)==expected_costs,(alpha,name,costs)
        expected={0:K} if K else {}
        for h,block in blocks.items():
            bits=list(map(int,block['descriptor']['actual_bits']));load=sum(bits)
            coefficient=(a4*bits[3]+a6*bits[5])/load if load else Fraction()
            if coefficient:expected[h]=coefficient
        assert {j:rational(v) for j,v in matrix['rows'][i] if j<Q}==expected
        if b['identically_zero_row']:
            assert not matrix['rows'][i];zero_budgets.append(i)
    if STRUCTURE_ONLY:
        inherited=read(OUT/'inherited_dual_lower_bound.json')
        old_dual=read(BASE/'exact_dual_certificate.json')
        assert inherited['row_multipliers']==old_dual['row_multipliers']
        assert inherited['source_sha256']==PINS[BASE/'exact_dual_certificate.json']
        assert inherited['matrix_sha256']==sha(OUT/'exact_matrix.json.gz')
        lower,count,residuals=verify_dual(inherited,matrix,None,None)
        oldpoint=read(BASE/'augmented_lp_exact.json')
        oldvalues=[Fraction(c['weight']) for c in oldpoint['columns']]
        assert [{k:v for k,v in c.items() if k!='weight'} for c in oldpoint['columns']]==old['columns']
        assert min(oldvalues)>=0
        oldslacks=[dot(row,oldvalues) for row in old['rows']]
        assert min(oldslacks)>=0
        assert sum((Fraction(c)*x for c,x in zip(old['normalization'],oldvalues)),Fraction())==1
        assert sum((Fraction(c)*x for c,x in zip(old['objective'],oldvalues)),Fraction())==lower
        oldlower,_,_=verify_dual(old_dual,old,oldslacks,oldvalues)
        assert oldlower==lower==Fraction(oldpoint['W'])
        assert residuals[N:]==[Fraction()]*ADDN
        report={'status':'PASS','scope':'Independent full symbolic retention and inherited lower-bound check. No augmented primal or optimum is certified.',
            'rows':M+ADDM,'columns':N+ADDN,'nonzeros':3208797,
            'old_rows_unchanged':M,'old_column_descriptors_unchanged':N,'old_auxiliaries_preserved':10744,
            'appended_rows_exactly_equal_pinned_bundle':ADDM,'appended_columns_exactly_equal_pinned_bundle':ADDN,
            'independently_rebuilt_symbolic_marginals':312,'independently_rebuilt_original_budget_vectors':624,
            'all16_histogram_descriptors_retained':True,'all4992_hidden_columns_retained':True,
            'fixed_point_rhs_substitutions':0,'zero_budget_rows_retained':zero_budgets,
            'baseline_exact_primal_rows_reverified':M,'baseline_exact_primal_columns_reverified':N,
            'inherited_dual_columns_checked':N+ADDN,'inherited_positive_dual_rows':count,
            'lower_bound':str(lower),'lower_bound_float':float(lower),'minimum_dual_residual':str(min(residuals)),
            'new_dual_row_weights_and_column_residuals_zero':True,
            'augmented_primal_verified':False,'new_optimum_comparison':'UNRESOLVED',
            'matrix_sha256':sha(OUT/'exact_matrix.json.gz'),'verifier_sha256':sha(Path(__file__)),
            'seconds':time.monotonic()-started}
        emit('structure_and_lower_verification.json',report)
        print(json.dumps(report,ensure_ascii=False,indent=2))
        return
    point=read(OUT/'augmented_lp_exact.json')
    assert [{k:v for k,v in c.items() if k!='weight'} for c in point['columns']]==matrix['columns']
    values=[Fraction(c['weight']) for c in point['columns']]
    assert len(values)==N+ADDN and min(values)>=0
    assert point['positive_columns']==sum(v>0 for v in values)
    epi=read(OUT/'epigraph_structure.json');zz=read(OUT/'zz_envelope_structure.json')
    assert sha(OUT/'epigraph_structure.json')==sha(BASE/'epigraph_structure.json')
    assert sha(OUT/'zz_envelope_structure.json')==sha(BASE/'zz_envelope_structure.json')
    assert len(epi['thresholds'])==7954 and len(zz['auxiliaries'])==2790
    for j,i in epi['thresholds']:
        assert values[j]==max(Fraction(),-dot([[k,v] for k,v in matrix['rows'][i] if k<Q],values))
    for r in zz['auxiliaries']:
        assert values[r['column']]==min(dot([[k,v] for k,v in matrix['rows'][i] if k<Q],values)
            for i in (r['q_upper_row'],r['v_upper_row']))
    W=sum((Fraction(c)*x for c,x in zip(matrix['objective'],values)),Fraction())
    O=sum((Fraction(c)*x for c,x in zip(matrix['normalization'],values)),Fraction())
    assert O==Fraction(point['O'])==1 and W==Fraction(point['W'])
    assert Fraction(point['strict_half_gap'])==1-2*W
    slacks=[dot(row,values) for row in matrix['rows']]
    assert min(slacks)>=0 and point['minimum_slack']==str(min(slacks))
    assert point['verified_rows']==M+ADDM
    primal_audit=read(OUT/'primal_exact_audit.json')
    assert slacks==list(map(Fraction,primal_audit['row_slacks']))
    recovery=primal_audit['recovery'];support=recovery['support']
    assert len(support)==len(set(support))==recovery['variables']
    assert recovery['rank']+len(recovery['free_variables'])==len(support)
    assert {j for j,v in enumerate(values) if v and (j<Q or j>=N)}<=set(support)
    for k,v in recovery['free_values']:assert values[support[k]]==Fraction(v)
    selected=read(OUT/('primal_'+recovery['attempt']+'_recovery_inputs.json'))
    for name,expected in selected['input_sha256'].items():assert sha(OUT/name)==expected,name
    for eq in selected['selected_equations']:
        lhs=Fraction();rhs=Fraction()
        for k,v in eq:
            if k==len(support):rhs=Fraction(v)
            else:lhs+=Fraction(v)*values[support[k]]
        assert lhs==rhs
    dual=read(OUT/'exact_dual_certificate.json')
    assert dual['matrix_sha256']==sha(OUT/'exact_matrix.json.gz')
    lower,positive_dual,residuals=verify_dual(dual,matrix,slacks,values)
    assert lower==W
    inherited=read(OUT/'inherited_dual_lower_bound.json')
    old_dual=read(BASE/'exact_dual_certificate.json')
    assert inherited['row_multipliers']==old_dual['row_multipliers']
    assert inherited['source_sha256']==PINS[BASE/'exact_dual_certificate.json']
    oldW,_,oldresiduals=verify_dual(inherited,matrix,None,None)
    assert oldW==Fraction(read(BASE/'augmented_lp_exact.json')['W'])
    assert oldresiduals[N:]==[Fraction()]*ADDN and oldW<=W
    new_support={i:Fraction(w) for i,w in dual['row_multipliers'] if i>=M}
    new_results=[{'row':i,'name':matrix['row_names'][i],'slack':str(slacks[i]),
        'dual_weight':str(new_support.get(i,Fraction()))} for i in range(M,M+ADDM)]
    emit('new_row_results.json',new_results)
    executed=[]
    for receipt in OUT.glob('execution_*.json'):
        r=read(receipt);snapshot=OUT/r['source_snapshot']
        assert sha(snapshot)==r['source_sha256']
        stage=receipt.stem[len('execution_'):]
        assert sha(OUT/(stage+'_stdout.txt'))==r['stdout_sha256']
        assert sha(OUT/(stage+'_stderr.txt'))==r['stderr_sha256']
        executed.append({'receipt':receipt.name,'status':r['status'],'exit_code':r['exit_code']})
    report={'status':'PASS','scope':'Complete symbolic actual4/R/family0-off on original16 hist; finite necessary LP only. General pureSPE half remains OPEN.',
        'rows':M+ADDM,'columns':N+ADDN,'nonzeros':3208797,'O':str(O),'W':str(W),'W_float':float(W),
        'old_W':str(oldW),'exact_increase':str(W-oldW),'increase_float':float(W-oldW),'same_optimum':W==oldW,
        'strictly_higher_optimum':W>oldW,'below_half':W<Fraction(1,2),'strict_half_gap':str(1-2*W),
        'all_old_rows_unchanged':M,'all_old_columns_unchanged':N,'old_auxiliaries_retained':10744,
        'full_new_symbolic_block_equal_to_pinned_bundle':True,'fixed_point_rhs_substitutions':0,
        'all_symbolic_marginals_independently_rebuilt':312,'all_original_budget_vectors_independently_rebuilt':624,
        'all16_histogram_descriptors_retained':True,'all4992_nonnegative_hidden_columns_retained':True,
        'zero_budget_rows_retained':zero_budgets,'canonical_max_checked':7954,'canonical_min_checked':2790,
        'primal_rows_checked':M+ADDM,'nonnegative_primal_columns_checked':N+ADDN,
        'minimum_primal_slack':str(min(slacks)),'dual_columns_checked':N+ADDN,
        'minimum_dual_residual':str(min(residuals)),'positive_dual_rows':positive_dual,
        'new_positive_dual_rows':len(new_support),'inherited_exact_dual_reverified':True,
        'primal_recovery_rank':recovery['rank'],'primal_free_variables':len(recovery['free_variables']),
        'positive_original_columns':sum(v>0 for v in values[:Q]),
        'positive_old_auxiliaries':sum(v>0 for v in values[Q:N]),
        'positive_new_hidden_columns':sum(v>0 for v in values[N:]),
        'zero_histograms_at_new_point':sum(values[h]==0 for h in blocks),
        'new_row_slack_signs':dict(Counter('zero' if s==0 else 'positive' for s in slacks[M:])),
        'source_and_execution_receipts_checked':executed,
        'matrix_sha256':sha(OUT/'exact_matrix.json.gz'),'point_sha256':sha(OUT/'augmented_lp_exact.json'),
        'dual_sha256':sha(OUT/'exact_dual_certificate.json'),'verifier_sha256':sha(Path(__file__)),
        'seconds':time.monotonic()-started}
    emit('certificate_verification.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
