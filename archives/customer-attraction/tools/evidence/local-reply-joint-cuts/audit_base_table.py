"""Base 5+4 table, with a new 48-state literal same-source requery oracle.

No original module imports or LPs. Previously certified nested coefficients and
the larger joint-table audit are reused, rather than recomputing their scans.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
EV = HERE.parent
BASE = HERE/'original/joint_local_cuts.json'
V2 = EV/'combined-branch-master-program/dependencies/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/joint_local_v2_cuts.json'
NESTED = EV/'nested-reply-projection-cut-data/original/nested_reply_cuts.json'
NESTED_AUDIT = EV/'nested-reply-projection-cut-data/five-cut-definition-audit.json'
JOINT_AUDIT = EV/'local-reply-portfolio-joint-cuts/exact-audit.json'
POINT = EV/'nested-reply-projection-program/related/combined_branch_latest_exact.json'
NEW_CLI = EV/'early-reply-requery-program/replay/report.json'
PAT = tuple(product((0,1),repeat=3))
PARS = tuple(map(F,('4/7','1/7','1/14','3/28','1/28','2/7')))


def share(bit,load):
    return F(bit,load) if bit else F()


def literal_rhs(p,ell,t,q,b,c,j,v):
    alpha,gamma,delta_j,delta_v,kappa,mu = PARS
    first_load,second_load = p+t+b+c,p+c+j+v
    # First path T,B,C; second path C,J,V: the SAME c belongs to both paths.
    source_t = share(t,first_load)
    source_c = share(c,second_load)
    first_last_c = share(c,first_load)
    second_last_v = share(v,second_load)
    probe_b = F(b,p+c+j+1)
    probe_q = F(q,p+t+b+1)
    return (alpha*source_t+(1-alpha)*source_c
            +gamma*(probe_b-second_last_v)
            +delta_j*F(j,ell+1)+delta_v*F(v,ell+1)+kappa*v
            +mu*(probe_q-first_last_c))


def template(cut):
    return cut['i'],cut['member'],tuple(cut['orb']),cut['query'],tuple(map(F,cut['parameters']))


def group(g):
    f,d,wi,wj=g
    return f,d,tuple(wi),tuple(wj)


def run():
    if sys.flags.optimize:
        raise RuntimeError('Assertions must be enabled')
    expected = {BASE:'891561660fda75c722b970082f4f16fd7a65e2dc8fb368f35ec5e54b047183da',
                V2:'49aaf81f49aac3b544cf38ed97efdb6fa1849e1c810ff1705b7dd313052017a1',
                NESTED:'933a18540d8ea69058cf5e23f999c17b5c69bda7624c817a9e0034fca2f97295',
                POINT:'50d51fadd1bd5cc6f2eb2230f1c35ac7001e21a5a75d11e91f4e259c1bf69224',
                JOINT_AUDIT:'63f801c55d6f4be32bf939e22d01b519e577c6c258a80e987cda269cce458c6f'}
    for path,sha in expected.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest()==sha
    base,v2,nested,point,joint,prior,newcli = [json.loads(p.read_text()) for p in (BASE,V2,NESTED,POINT,JOINT_AUDIT,NESTED_AUDIT,NEW_CLI)]
    assert set(base)=={'scope','nested','requery'}
    assert len(base['nested'])==5 and len(base['requery'])==4
    assert base['nested']==nested['selected']==v2['nested']
    assert base['requery']==v2['requery'][:4] and len(v2['requery'])==5 and len(v2['portfolio'])==8
    for cut in base['requery']:
        assert set(cut)=={'i','member','orb','query','parameters'}
        assert cut['i']==3 and cut['query']==5 and tuple(map(F,cut['parameters']))==PARS
    assert 0<=PARS[0]<=1 and min(PARS[1:])>=0
    psi={};table=[];candidate_states=0
    for p in range(4):
        for ell,t,q in product(range(p,p+3),range(2),range(2)):
            values=[]
            for hidden in product(range(2),repeat=4):
                values.append((literal_rhs(p,ell,t,q,*hidden),hidden));candidate_states+=1
            value=min(x[0] for x in values)
            psi[p,ell,t,q]=value
            table.append({'p':p,'ell':ell,'t':t,'q':q,'minimum':str(value),
                          'all_minimizers_B_C_J_V':[h for v,h in values if v==value]})
    assert len(psi)==48 and candidate_states==768
    hs={};hi=None
    for i,c in enumerate(point['columns']):
        if c['kind']=='hist':
            hi=i;hs[hi]={'a':tuple(map(int,c['actual_bits'])),'hist':c['hist'],
                         'mass':F(c['weight']),'groups':{}}
        elif c['kind']=='joint-reply':
            hs[hi]['groups'].setdefault(group(c['group']),{})[tuple(c['state'])]=F(c['weight'])
    cli_map={template(r['cut']):F(r['slack']) for r in newcli['selected']}
    inherited_map={template(r['cut']):r for r in joint['all_rows'] if r['family']=='requery'}
    K=F(point['columns'][0]['weight']);records=[]
    for cut in base['requery']:
        member=cut['member'];family,diag=cut['orb'];ct=6 if diag else 30
        contributions=[]
        for hc,h in hs.items():
            a,mass=h['a'],h['mass'];p,ell,q=sum(a[:3]),sum(a[:5]),a[5]
            words=tuple(w for n,w in zip(h['hist'],PAT) for _ in range(n))
            edges=[(i,j) for i,j in product(range(6),repeat=2) if (i==j)==bool(diag)]
            assert len(edges)==ct
            one=sum((sum((w for state,w in h['groups'][family,diag,words[i],words[j]].items()
                          if state[member]),F()) for i,j in edges),F())/ct
            zero=mass-one;assert min(zero,one)>=0
            actual=mass*(share(a[3],sum(a))+(PARS[2]+PARS[3])*share(a[5],sum(a)))
            contribution=actual-zero*psi[p,ell,0,q]-one*psi[p,ell,1,q]
            contributions.append({'hist_column':hc,'actual_bits':''.join(map(str,a)),
                                  'hist_mass':str(mass),'average_t0':str(zero),'average_t1':str(one),
                                  'psi0':str(psi[p,ell,0,q]),'psi1':str(psi[p,ell,1,q]),
                                  'row_contribution':str(contribution)})
        val=PARS[4]*K+sum((F(r['row_contribution']) for r in contributions),F())
        old=inherited_map[template(cut)]
        assert val==cli_map[template(cut)]==F(old['exact_slack_on_frozen_5180_point'])<0
        records.append({'cut':cut,'K_coefficient':str(PARS[4]),'actual_last_profit_coefficient':str(PARS[2]+PARS[3]),
                        'source_profit_coefficient':'1','current_5180_slack':str(val),
                        'nested_histogram_point_identity':'not an origin recorded in base JSON',
                        'matches_original_24LP_new_report':True,'matches_larger_table_audit':True,
                        'row_sha256_from_larger_audit':old['row_sha256'],'histograms':contributions})
    nested_records=[]
    for c,r in zip(base['nested'],prior['all_five_cuts']):
        assert c['slack']==r['exact_slack']
        nested_records.append({'member':c['member'],'orb':c['orb'],'stored_historical_slack':c['slack'],
                               'current_5180_slack_reused':r['exact_slack'],'new_nested_coefficient_runs':0})
    paths=[BASE,V2,NESTED,NESTED_AUDIT,JOINT_AUDIT,POINT,NEW_CLI]
    return {'status':'PASS_BASE_5_PLUS_4_AND_LITERAL_48_STATE_REQUERY_TABLE',
            'scope':'Complete three-field base table; nested audit reused. New full legal i=3 coarse-load domain (48 minima/768 hidden states) and four exact indexed-average diagnostics, no source imports or LP.',
            'python_version':sys.version,'audit_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'inputs':{str(p.relative_to(EV)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths},
            'all_source_metadata':{'scope':base['scope'],'nested_count':5,'requery_count':4},
            'base_exactly_equals_v2_nested_and_first_four_requeries':True,
            'v2_extra_requery':v2['requery'][4],'v2_extra_portfolios':len(v2['portfolio']),
            'templates_not_rank_or_spe_inclusion':True,
            'parameters':list(map(str,PARS)),'parameter_sum_is_not_simplex_normalization':str(sum(PARS)),
            'first_source_IC_multiplier':str(PARS[0]),'second_source_IC_multiplier':str(1-PARS[0]),
            'new_local_minima':48,'new_literal_hidden_states':candidate_states,'all_48_minima':table,
            'nested_five_inherited':nested_records,'requery_four_current_diagnostics':records,
            'original_entries':0,'LPs':0,'nested_coefficient_reruns':0,'larger_matrix_reruns':0,
            'not_certified':['historical origin of base four requery templates','all price/query closure',
                             'combined local exact point or optimum','complete-history SPE','general half']}


if __name__=='__main__':
    report=run()
    (HERE/'base-table-definition-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
