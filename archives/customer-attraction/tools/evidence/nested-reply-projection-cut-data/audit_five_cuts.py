"""Five frozen cuts: literal S/Z/V menu projection and direct indexed averaging.

Does not import the original raw/parse/row/discover functions or run LPs.
Input-layout validation is reused from the separately archived program audit.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
EV = HERE.parent
CUTS = HERE/'original/nested_reply_cuts.json'
POINT = EV/'nested-reply-projection-program/related/combined_branch_latest_exact.json'
RERUN = EV/'nested-reply-projection-program/replay/nested_reply_cuts.json'
INPUT_AUDIT = EV/'nested-reply-projection-program/input-interface-report.json'
PAT = tuple(product((0,1),repeat=3))
ACTIVE_NAMES = {'source','lastB','G','E','Pq','Pr','H2r','H3q','H3r'}
GS = ('source','middleB','lastB','lastY','innerQ','innerR','innerT','G','E','innerE',
      'Pq','Pr','Py','Cq','Cr','Cy','H2q','H2r','H2y','H3q','H3r','H3y','PAIRaa','PAIRab','PAIRbb')


def share(n,d):
    return F(n,d) if n else F()


def normalized_group(g):
    f,d,wi,wj = g
    return f,d,tuple(wi),tuple(wj)


def menu_rows(a,d,t,q,r,L,h):
    p = sum(a[:3])+t
    den, D = p+q+r,(p+1)*(p+2)
    uq,ur = share(q,den),share(r,den)
    total,ell = sum(a),sum(a[:5])
    u = [share(z,total) for z in a]
    S = 6*uq-F(d,p+1)+F(h,D)
    Z = 6*ur-F(L,p+q+1)
    V = F(d*L-6*h,D)
    G = S+Z/12+V/6
    expanded_G = 6*uq+ur/2-F(d,p+1)-F(L,12*(p+q+1))+F(d*L,6*D)
    assert G==expanded_G
    return {'source':u[3]-share(t,den),'lastB':ur-F(a[5],p+q+1),
            'G':G,'E':6*ur-F(d,p+q+1),
            'Pq':u[5]-F(q,ell+1),'Pr':u[5]-F(r,ell+1),
            'H2r':u[1]-F(r,5+a[0]),
            'H3q':u[2]-F(q,4+a[0]+a[1]),'H3r':u[2]-F(r,4+a[0]+a[1])}


def run():
    if sys.flags.optimize:
        raise RuntimeError('Assertions must be enabled')
    assert hashlib.sha256(CUTS.read_bytes()).hexdigest()=='933a18540d8ea69058cf5e23f999c17b5c69bda7624c817a9e0034fca2f97295'
    source = json.loads(CUTS.read_text())
    assert set(source)=={'scope','source','source_sha256','source_W','selected'}
    assert POINT.stat().st_size==823005
    assert hashlib.sha256(POINT.read_bytes()).hexdigest()==source['source_sha256']=='50d51fadd1bd5cc6f2eb2230f1c35ac7001e21a5a75d11e91f4e259c1bf69224'
    point = json.loads(POINT.read_text())
    assert point['W']==source['source_W']
    interface = json.loads(INPUT_AUDIT.read_text())
    # No original program is imported or called; this is source-data extraction.
    hs,hi = {},None
    for i,c in enumerate(point['columns']):
        if c['kind']=='hist':
            hi=i
            hs[hi]={'a':tuple(map(int,c['actual_bits'])),'d':c['d'],'hist':c['hist'],
                    'mass':F(c['weight']),'groups':{}}
        elif c['kind']=='joint-reply':
            hs[hi]['groups'].setdefault(normalized_group(c['group']),{})[tuple(c['state'])]=F(c['weight'])
    cuts = source['selected']
    assert len(cuts)==5
    assert [(c['member'],tuple(c['orb'])) for c in cuts]==[(0,(0,0)),(0,(1,0)),(1,(0,0)),(1,(1,0)),(1,(1,1))]
    weights = []
    for cut in cuts:
        assert set(cut)=={'member','orb','weights','slack'}
        assert set(cut['weights'])<=ACTIVE_NAMES
        w={k:F(v) for k,v in cut['weights'].items()}
        assert min(w.values())>0 and sum(w.values())==1
        assert F(cut['slack'])<0
        weights.append(w)
    raw_states=0
    @lru_cache(None)
    def coefficient(a,d,t,ci):
        nonlocal raw_states
        all_values,ends = [],[]
        for q,r,L in product(range(2),range(2),range(7)):
            fixed=[]
            for h in range(max(0,d+L-6),min(d,L)+1):
                rows=menu_rows(a,d,t,q,r,L,h)
                v=sum((w*rows[name] for name,w in weights[ci].items()),F())
                fixed.append(v);raw_states+=1
            assert fixed and min(fixed)==max(fixed)
            all_values+=fixed
            if L in (0,6):ends+=fixed
        assert max(all_values)==max(ends)
        return max(all_values)
    all_records=[]
    unique_visible=sorted({(h['a'],h['d']) for h in hs.values()})
    for ci,cut in enumerate(cuts):
        member=cut['member'];family,diag=cut['orb'];ct=6 if diag else 30
        contributions=[]
        for hc,h in hs.items():
            words=tuple(w for n,w in zip(h['hist'],PAT) for _ in range(n))
            edges=[(i,j) for i,j in product(range(6),repeat=2) if (i==j)==bool(diag)]
            assert len(edges)==ct
            one=F()
            for i,j in edges:
                states=h['groups'][family,diag,words[i],words[j]]
                one+=sum((v for state,v in states.items() if state[member]),F())/ct
            zero=h['mass']-one
            assert min(zero,one)>=0
            v0=coefficient(h['a'],h['d'],0,ci);v1=coefficient(h['a'],h['d'],1,ci)
            contribution=zero*v0+one*v1
            contributions.append({'hist_column':hc,'actual_bits':''.join(map(str,h['a'])),'d':h['d'],
                                  'hist_mass':str(h['mass']),'average_forced_zero_mass':str(zero),
                                  'average_forced_one_mass':str(one),'psi_t0':str(v0),'psi_t1':str(v1),
                                  'contribution':str(contribution)})
        val=sum((F(c['contribution']) for c in contributions),F())
        assert val==F(cut['slack'])
        all_records.append({'position':ci,'member':member,'orb':cut['orb'],'weights':cut['weights'],
                            'weights_sum':'1','K_coefficient':'0','depends_on_single_Y':False,
                            'indexed_terms_averaged':ct,'exact_slack':str(val),'histogram_contributions':contributions})
    replay=json.loads(RERUN.read_text())
    differing=[k for k in set(source)|set(replay) if source.get(k)!=replay.get(k)]
    assert differing==['source'] and source['selected']==replay['selected']
    base=EV/'combined-branch-master-program/dependencies/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5'
    local_comparisons=[]
    def template(c):
        return c['member'],tuple(c['orb']),tuple(F(c['weights'].get(n,'0')) for n in GS)
    for name in ('joint_local_cuts.json','joint_local_v2_cuts.json'):
        path=base/name
        if path.exists():
            nested=json.loads(path.read_text())['nested']
            local_comparisons.append({'file':name,'bytes':path.stat().st_size,
                                      'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                                      'nested_records':len(nested),
                                      'exact_ordered_templates_equal':list(map(template,nested))==list(map(template,cuts))})
    return {'status':'PASS_FIVE_FULL_CUTS_LITERAL_MENU_AND_INDEXED_AVERAGING',
            'scope':'All five source cuts; literal S/Z/V with feasible intersection h, full L and endpoint maxima; direct named-edge averaging. No LP or original program call.',
            'python_version':sys.version,'audit_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'inputs':{str(p.relative_to(EV)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (CUTS,POINT,RERUN,INPUT_AUDIT)},
            'source_fields':{k:v for k,v in source.items() if k!='selected'},
            'input_interface_reused':str(INPUT_AUDIT.relative_to(EV)),
            'histograms':len(hs),'positive_histograms':sum(h['mass']>0 for h in hs.values()),
            'all_current_visible_a_d':[(list(a),d) for a,d in unique_visible],
            'coefficients_reconstructed':coefficient.cache_info().currsize,
            'literal_hidden_intersection_states':raw_states,
            'full_L_0_to_6_max_equals_endpoint_max':True,'intersection_h_cancels_in_every_evaluated_state':True,
            'all_five_weight_sums_one':True,'all_five_K_coefficients_zero':True,
            'all_five_single_Y_coefficients_zero':True,'G_menu_used_by_cut_positions':[j for j,w in enumerate(weights) if w.get('G',0)],
            'original_entry_output_difference_fields':differing,'original_new_output_selected_byte_values_equal':True,
            'frozen_bytes':CUTS.stat().st_size,'new_output_bytes':RERUN.stat().st_size,
            'local_template_comparisons':local_comparisons,'all_five_cuts':all_records,
            'not_certified':['all continuous weights','unselected orbit cannot separate','exact LP optima','reoptimization after adding cuts','complete-history SPE','universal half']}


if __name__=='__main__':
    report=run()
    (HERE/'five-cut-definition-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
