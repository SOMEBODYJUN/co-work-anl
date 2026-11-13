"""Exact structured audit of both frozen 4849-column vectors; never runs an LP.

All fields in both large JSONs are parsed. Column descriptors are validated by
kind; every weight is converted to Fraction, and all 28 new rows are computed
twice (per state and by conditional first moments). No inherited 5664-row
reconstruction is claimed. Output lives only in the task's independent area.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[6]
E = ROOT / 'archives/customer-attraction/tools/evidence/b-family-menu-prices-boss3'
OUT = Path(__file__).with_name('exact-audit.json')
SCHEMA = {
    'K': {'kind', 'weight'},
    'hist': {'kind', 'actual_bits', 'd', 'hist', 'weight'},
    'joint-reply': {'kind', 'hist_column_old', 'group', 'state', 'weight'},
    'overlap': {'kind', 'hist_column', 'groups', 'weight'},
    'actual-B-family-state': {'kind', 'source', 'hist_column', 'hidden', 'ell', 'weight'},
    'maximum-root-family-state': {'kind', 'hist_column', 'M', 'hidden', 'ell', 'weight'},
}
KIND_COUNTS = {'K': 1, 'hist': 16, 'joint-reply': 582, 'overlap': 1306,
               'actual-B-family-state': 896, 'maximum-root-family-state': 2048}
TOP = {'scope', 'base_rows', 'first_raw_rows', 'additional_index_class_rows',
       'O', 'W', 'strict_half_gap', 'verified_rows', 'minimum_slack',
       'positive_columns', 'columns'}

def meta(c):
    return {k:v for k,v in c.items() if k != 'weight'}

def key(v):
    if isinstance(v,list): return tuple(key(x) for x in v)
    return v

def audit(filename, report_name, nrows, positive):
    p = E / 'original/research_2' / filename
    data = json.loads(p.read_text())
    saved = json.loads((E / 'replay' / report_name).read_text())
    assert set(data) == TOP
    assert isinstance(data['scope'], str) and 'not SPE' in data['scope']
    assert (data['base_rows'], data['first_raw_rows'], data['additional_index_class_rows']) == (702,37,100)
    assert data['verified_rows'] == nrows and F(data['minimum_slack']) == 0
    cols = data['columns']; ys = [F(c['weight']) for c in cols]
    assert len(cols)==4849 and min(ys)==0 and sum(y>0 for y in ys)==positive==data['positive_columns']
    assert Counter(c['kind'] for c in cols)==Counter(KIND_COUNTS)
    assert all(set(c)==SCHEMA[c['kind']] for c in cols)
    hist={i:c for i,c in enumerate(cols) if c['kind']=='hist'}
    pats=list(product((0,1),repeat=3))
    for c in hist.values():
        assert len(c['actual_bits'])==6 and set(c['actual_bits']) <= {'0','1'}
        assert len(c['hist'])==8 and all(type(x)==int and x>=0 for x in c['hist'])
        assert sum(c['hist'])==6 and c['d']==sum(n*p[0] for n,p in zip(c['hist'],pats))
    expected=[]
    for source in (2,3,4):
        for hj in hist:
            for h in product((0,1),repeat=6-source):
                for ell in (0,6):
                    expected.append(dict(kind='actual-B-family-state',source=source,hist_column=hj,hidden=list(h),ell=ell))
    for hj in hist:
        for m in (0,1):
            for h in product((0,1),repeat=5):
                for ell in (0,6):
                    expected.append(dict(kind='maximum-root-family-state',hist_column=hj,M=m,hidden=list(h),ell=ell))
    assert [meta(c) for c in cols[1905:]]==expected and len(expected)==2944
    # Recover old702 histogram numbering from the contiguous joint blocks.
    oldmap={}; joint=defaultdict(dict); current_hist=None
    for j,c in enumerate(cols[:1905]):
        if c['kind']=='hist': current_hist=j
        elif c['kind']=='joint-reply':
            old=c['hist_column_old']
            assert oldmap.setdefault(current_hist,old)==old
            g=key(c['group']); state=tuple(c['state'])
            assert len(g)==4 and g[0] in (0,1) and g[1] in (0,1)
            assert all(len(v)==3 and set(v)<={0,1} for v in g[2:])
            assert state in ((0,1),(1,0),(1,1)) and state not in joint[(current_hist,g)]
            joint[(current_hist,g)][state]=ys[j]
    assert len(joint)==194 and len(oldmap)==16
    assert {str(k):v for k,v in oldmap.items()}==saved.get('old_hist_column_id_map',{str(k):v for k,v in oldmap.items()})
    joint_bounds=[]
    for (hj,g),states in joint.items():
        assert set(states)=={(0,1),(1,0),(1,1)}
        bound=ys[hj]-sum(states.values(),F());assert bound>=0
        joint_bounds.append(bound)
    overlap_bounds=[]
    for j,c in enumerate(cols):
        if c['kind']!='overlap':continue
        hj=c['hist_column'];assert hj in hist and len(c['groups'])==2
        for gg in c['groups']:
            states=joint[(hj,key(gg))]
            r=states[(1,0)]+states[(1,1)]
            slack=r-ys[j];assert slack>=0;overlap_bounds.append(slack)
    assert len(overlap_bounds)==2612
    O=sum(ys[j]*int(c['d']>0) for j,c in hist.items())
    W=sum(ys[j]*int('1' in c['actual_bits']) for j,c in hist.items())
    assert O==F(data['O'])==1 and W==F(data['W'])
    assert O-2*W==F(data['strict_half_gap'])>0
    K=ys[0]
    families=defaultdict(list)
    for j,c in enumerate(cols):
        if c['kind']=='actual-B-family-state':families['actual-B-'+str(c['source'])].append(j)
        elif c['kind']=='maximum-root-family-state':families['maximum-M-root'].append(j)
    ua=[sum((ys[hj]*F(int(c['actual_bits'][a]),sum(map(int,c['actual_bits']))) for hj,c in hist.items() if c['actual_bits'][a]=='1'),F()) for a in range(6)]
    assert sum(ua,F())==W
    prices=[]; marginals=[]; moments=[]
    for name,js in families.items():
        z={}
        for hj in hist:
            mass=sum((ys[j] for j in js if cols[j]['hist_column']==hj),F())
            assert mass==ys[hj]
            z[hj]=sum((ys[j]*F(cols[j]['ell'],6) for j in js if cols[j]['hist_column']==hj),F())
            assert 0<=z[hj]<=mass
            marginals.append(dict(family=name,hist_column=hj,sum=str(mass),hist_mass=str(ys[hj]),difference='0'))
            moments.append(dict(family=name,hist_column=hj,mean_menu_mass=str(z[hj])))
        for a in range(6):
            q=sum((z[hj]/(6-a+sum(map(int,c['actual_bits'][:a]))) for hj,c in hist.items()),F())
            slack=ua[a]-q
            direct=F()
            for j in js:
                c=cols[j];bits=list(map(int,hist[c['hist_column']]['actual_bits']))
                share=F(bits[a],sum(bits)) if bits[a] else F()
                direct+=ys[j]*(share-F(c['ell'],6*(6-a+sum(bits[:a]))))
            assert direct==slack
            prices.append(dict(family=name,row='actual-menu-price:'+str(a+1),slack=str(slack)))
        prices.append(dict(family=name,row='menu-CAP',slack=str(K-sum(z.values(),F()))))
    assert prices==saved['new_menu_price_rows'] and marginals==saved['conditional_marginals']
    assert len(marginals)==64 and len(prices)==28
    rootmass=sum((ys[j]*cols[j]['M'] for j in families['maximum-M-root']),F())
    assert rootmass==K==F(saved['K'])==F(saved['maximum_root_M_mass'])
    caps=[]
    for a in range(6):
        sz=sum((ys[hj]*int(c['actual_bits'][a]) for hj,c in hist.items()),F())
        assert K>=sz
        caps.append(dict(actual_position=a+1,size=str(sz),K_minus_size=str(K-sz)))
    assert caps==saved['actual_theme_capacity_checks']
    assert [dict(column=i,weight=str(ys[i]),actual_bits=c['actual_bits'],d=c['d'],hist=c['hist']) for i,c in hist.items()]==saved['hist_masses']
    for fld in ('O','W'):
        assert F(saved[fld])==F(data[fld])
    assert F(saved['strict_half_gap_O_minus_2W'])==O-2*W
    assert saved['input_sha256']==sha256(p.read_bytes()).hexdigest()
    assert saved['column_count']==len(cols) and saved['kind_counts']==KIND_COUNTS
    assert saved['positive_kind_counts']==dict(Counter(c['kind'] for c,y in zip(cols,ys) if y>0))
    assert saved['positive_hist_support_count']==sum(ys[hj]>0 for hj in hist)==10
    assert saved['hist_support_count']==16 and saved['minimum_weight']=='0' and saved['positive_columns']==positive
    assert saved['header_only_until_separate_original_matrix_check']=={'verified_rows':nrows,'minimum_slack':'0'}
    assert saved['all_top_level_fields_consumed'] and saved['all_column_metadata_fields_consumed']
    assert saved['old1905_metadata_matched'] and saved['new2944_metadata_matched']
    if 'joint_reply_group_upper_bounds_checked' in saved:
        assert saved['joint_reply_group_upper_bounds_checked']==194
        assert F(saved['minimum_joint_group_bound_slack'])==min(joint_bounds)
        assert saved['overlap_upper_bounds_checked']==2612
        assert F(saved['minimum_overlap_bound_slack'])==min(overlap_bounds)
    neg=[x for x in prices if F(x['slack'])<0]
    zeros=[x for x in prices if not F(x['slack'])]
    if nrows==5692: assert not neg and len(zeros)==4
    else: assert len(neg)==1 and neg[0]['family']=='actual-B-2' and neg[0]['row']=='actual-menu-price:6'
    result=dict(input=dict(path=str(p.relative_to(ROOT)),sha256=sha256(p.read_bytes()).hexdigest()),
                all_fields_consumed=True,column_count=len(cols),kind_counts=KIND_COUNTS,
                positive_kind_counts=dict(Counter(c['kind'] for c,y in zip(cols,ys) if y>0)),
                positive_columns=positive,conditional_marginal_count=64,
                joint_upper_bound_count=194,overlap_upper_bound_count=2612,
                old_histogram_numbering={str(k):v for k,v in oldmap.items()},
                O=str(O),W=str(W),K=str(K),gap_O_minus_2W=str(O-2*W),
                actual_incomes=list(map(str,ua)),conditional_menu_first_moments=moments,
                new_menu_price_rows=prices,negative_rows=neg,zero_rows=zeros,
                saved_report_exactly_matched=True,
                inherited_matrix_evidence='saved same-implementation 5692 replay; old5664 header only; no fresh full-matrix execution')
    return data,cols,ys,result

def main():
    old,co,yo,ao=audit('maxroot_identity_exact.json','maxroot-structure-and-prices-audit.json',5664,252)
    new,cn,yn,an=audit('all_menu_prices_exact.json','structure-and-prices-audit.json',5692,261)
    assert [meta(c) for c in co]==[meta(c) for c in cn]
    old_layout_path=ROOT/'archives/customer-attraction/tools/evidence/full156-tail-parent-report/original/research_5/combined_branch_master_exact.json'
    old_layout=json.loads(old_layout_path.read_text())['columns']
    assert len(old_layout)==1905
    assert [meta(c) for c in cn[:1905]]==[meta(c) for c in old_layout]
    assert all(yo[i]==yn[i] for i,c in enumerate(cn) if c['kind'] in ('K','hist'))
    differences=[dict(column=j,kind=c['kind'],old_weight=str(yo[j]),new_weight=str(yn[j])) for j,c in enumerate(cn) if yo[j]!=yn[j]]
    comparison=json.loads((E/'replay/point-comparison.json').read_text())
    assert differences==comparison['changed_columns'] and len(differences)==214
    assert dict(Counter(c['kind'] for c in differences))==comparison['changed_weights_by_kind']
    assert comparison['old_root_new_price_violations']==ao['negative_rows']
    zero_corresponding=[x for x in an['new_menu_price_rows'] if (x['family'],x['row'])==('actual-B-2','actual-menu-price:6')][0]
    assert comparison['same_price_on_completed_point']==zero_corresponding
    assert comparison['metadata_identical_all_4849'] and comparison['W_identical'] and comparison['K_and_all_hist_weights_identical']
    assert comparison['changed_weight_count']==214 and comparison['old_root_new_price_negative_count']==1 and comparison['new_point_new_price_negative_count']==0
    assert comparison['old_author_reported_rows']==5664 and comparison['new_original_builder_verified_rows']==5692
    assert comparison['old_positive_columns']==252 and comparison['new_positive_columns']==261
    assert comparison['changed_top_level_noncolumn_fields']=={k:dict(old=old[k],new=new[k]) for k in TOP-{'columns'} if old[k]!=new[k]}
    endpoint_checks=0;safe_denominator_checks=0
    for bits in product((0,1),repeat=6):
        for a in range(6):
            den=6-a+sum(bits[:a]);assert den>=1
            for ell in range(7):
                at_ell=F(ell,6*den)
                assert at_ell==(1-F(ell,6))*F(0)+F(ell,6)*F(1,den)
                endpoint_checks+=1
            for later_coverage in range(6-a):
                assert F(1,sum(bits[:a])+1+later_coverage)>=F(1,den)
                safe_denominator_checks+=1
    result=dict(status='PASS',old=ao,new=an,
                inherited_1905_layout=dict(path=str(old_layout_path.relative_to(ROOT)),sha256=sha256(old_layout_path.read_bytes()).hexdigest(),
                                          complete_descriptor_match=True,weights_not_used_as_evidence_of_either_current_point=True),
                comparison=dict(metadata_identical_all_4849=True,K_and_histogram_masses_identical=True,
                                changed_weights=len(differences),changed_weights_by_kind=dict(Counter(c['kind'] for c in differences)),
                                all_214_saved_changes_exactly_matched=True),
                menu_formula_boundary_checks=dict(endpoint_affinity=endpoint_checks,safe_denominators=safe_denominator_checks,
                                                  covers_zero_actual_load_zero_menu_and_terminal_query=True),
                limitations='Exact finite arithmetic only: not an SPE construction, no optimality, no universal half conclusion, no fresh inherited-matrix replay.')
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',old_positive=252,new_positive=261,hidden_changes=214,new_price_negative=0,new_price_zero=4,old_price_negative=1)))

if __name__=='__main__':main()
