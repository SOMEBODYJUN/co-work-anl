"""Exact frozen-template and row audit, with no discovery or graph entrypoint.

Nested coefficient values are inherited from the archived independent literal
menu audit. Requery and portfolio minima are rebuilt from labelled hidden bits;
all row aggregation uses six named comparison indices, not histogram products.
Original row functions are AST-selected as comparison targets only. Nested's
coeff target is supplied the verified inherited cache to avoid recomputing its
already completed hidden-menu calculation.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
from types import SimpleNamespace
import ast
import hashlib
import json
import sys

PAT = tuple(product((0, 1), repeat=3))
GS = ((0, 0), (1, 0), (1, 1))


def share(n, d):
    return F(n, d) if n else F()


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def selected_functions(path, names, extra=None):
    tree = ast.parse(path.read_text())
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes} == set(names)
    namespace = dict(F=F, product=product, lru_cache=lru_cache, PAT=PAT, GS=GS)
    namespace.update(extra or {})
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), namespace)
    return namespace


def norm(c, family, names=()):
    head = (c.get('i'), c['member'], tuple(c['orb']))
    if family == 'nested':
        return head + (tuple(F(c['weights'].get(n, '0')) for n in names),)
    if family == 'requery':
        return head + (c['query'], tuple(map(F, c['parameters'])))
    mus = tuple(map(F, c['mu']))
    return head + tuple(F(c.get(k, '0')) for k in ('alpha_middle', 'alpha_last', 'beta_middle', 'beta_last')) + (mus + (F(),) * (16-len(mus)),)


def run(repo, report_path, source_path, original_requery_report):
    if sys.flags.optimize:
        raise RuntimeError('Assertions must remain enabled')
    if report_path.exists():
        raise RuntimeError('Do not silently repeat an already saved audit')
    ev = repo / 'archives/customer-attraction/tools/evidence'
    dep = ev / 'combined-branch-master-program/dependencies/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1'
    paths = {
        'joint': source_path,
        'joint_shared': dep / 'research_5/joint_local_v2_cuts.json',
        'base': dep / 'research_5/joint_local_cuts.json',
        'nested_original_cuts': ev / 'nested-reply-projection-cut-data/original/nested_reply_cuts.json',
        'nested_audit': ev / 'nested-reply-projection-cut-data/five-cut-definition-audit.json',
        'input_interface': ev / 'nested-reply-projection-program/input-interface-report.json',
        'point': ev / 'nested-reply-projection-program/related/combined_branch_latest_exact.json',
        'nested_code': ev / 'nested-reply-projection-program/original/nested_reply_projection.py',
        'requery_code': dep / 'research_3/early_reply_requery_cuts.py',
        'portfolio_code': dep / 'research_3/terminal_portfolio_cuts.py',
        'groups_code': ev / 'old-query-grid-separation-program/original/old_query_reply_cuts.py',
        'old_capacity': dep / 'research_3/terminal_capacity_refinement_cuts.json',
        'old_portfolio': dep / 'research_3/terminal_portfolio_refinement_cuts.json',
        'original_requery_report': original_requery_report,
    }
    before = {k: {'path': str(p), 'bytes': p.stat().st_size, 'sha256': sha(p)} for k,p in paths.items()}
    assert before['joint']['sha256'] == before['joint_shared']['sha256'] == '49aaf81f49aac3b544cf38ed97efdb6fa1849e1c810ff1705b7dd313052017a1'
    assert before['point']['sha256'] == '50d51fadd1bd5cc6f2eb2230f1c35ac7001e21a5a75d11e91f4e259c1bf69224'
    data = json.loads(paths['joint'].read_text())
    base = json.loads(paths['base'].read_text())
    nested_audit = json.loads(paths['nested_audit'].read_text())
    nested_original = json.loads(paths['nested_original_cuts'].read_text())
    original_rq = json.loads(paths['original_requery_report'].read_text())
    interface = json.loads(paths['input_interface'].read_text())
    assert nested_audit['inputs']['nested-reply-projection-program/related/combined_branch_latest_exact.json']['sha256'] == before['point']['sha256']
    assert nested_audit['coefficients_reconstructed'] == 120
    assert nested_audit['literal_hidden_intersection_states'] == 5760
    assert nested_audit['full_L_0_to_6_max_equals_endpoint_max']
    assert set(data) == {'scope', 'nested', 'requery', 'portfolio'}
    assert [len(data[k]) for k in ('nested', 'requery', 'portfolio')] == [5,5,8]
    tree = ast.parse(paths['nested_code'].read_text())
    names = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'NAMES' for t in n.targets))
    for c in data['nested']:
        assert set(c) == {'member','orb','weights','slack'}
        assert set(c['weights']) <= set(names)
        assert all(F(v)>0 for v in c['weights'].values())
        assert sum(map(F, c['weights'].values())) == 1
        assert F(c['slack'])<0
    for c in data['requery']:
        assert set(c) == {'i','member','orb','query','parameters'}
        assert c['i']==3 and c['query']==5 and len(c['parameters'])==6
        a,*rest=map(F,c['parameters'])
        assert 0<=a<=1 and min(rest)>=0
    for c in data['portfolio']:
        assert set(c)=={'i','member','orb','alpha_middle','alpha_last','beta_middle','beta_last','mu'}
        assert c['i'] in (1,2,3) and len(c['mu'])==13
        assert F(c['beta_middle'])==0 and F(c['beta_last'])>0
        assert min(map(F,c['mu']))>=0 and sum(bool(F(v)) for v in c['mu'])==1
    for family in ('nested','requery','portfolio'):
        for c in data[family]:
            assert c['member'] in (0,1) and tuple(c['orb']) in GS
    assert data['nested'] == base['nested'] == nested_original['selected']
    assert data['requery'][:4] == base['requery']
    comparison = {}
    for family in ('nested','requery','portfolio'):
        bkeys=[norm(c,family,names) for c in base.get(family,[])]
        vkeys=[norm(c,family,names) for c in data[family]]
        assert not (Counter(bkeys)-Counter(vkeys))
        comparison[family]={'base_records':len(bkeys),'v2_records':len(vkeys),'base_to_v2_positions':[vkeys.index(k) for k in bkeys], 'base_multiset_contained':True,'new_v2_positions':[j for j,k in enumerate(vkeys) if k not in bkeys], 'v2_distinct_templates':len(set(vkeys))}
    old_comparison = {}
    for key in ('old_capacity','old_portfolio'):
        old = json.loads(paths[key].read_text())['cuts']
        keys = [norm(c,'portfolio') for c in old]
        old_comparison[key] = {'records':len(old),'exact_matches':[[i,j] for i,c in enumerate(data['portfolio']) for j,k in enumerate(keys) if norm(c,'portfolio')==k]}

    oq = SimpleNamespace(**selected_functions(paths['groups_code'], {'groups'}))
    pc = selected_functions(paths['portfolio_code'], {'share','qvec','psi','row'}, {'oq':oq})
    rq = selected_functions(paths['requery_code'], {'share','candidates','psi','row'}, {'oq':oq,'pc':SimpleNamespace(**pc)})
    cache={}
    for ci, rec in enumerate(nested_audit['all_five_cuts']):
        assert rec['weights']==data['nested'][ci]['weights']
        w=tuple(F(rec['weights'].get(n,'0')) for n in names)
        for h in rec['histogram_contributions']:
            for t in (0,1):
                k=(tuple(map(int,h['actual_bits'])),h['d'],t,w)
                v=F(h['psi_t'+str(t)])
                assert k not in cache or cache[k]==v
                cache[k]=v
    def inherited_coeff(a,d,t,w):
        return cache[a,d,t,tuple(w)]
    nr = selected_functions(paths['nested_code'], {'row'}, {'NAMES':names,'NI':{n:i for i,n in enumerate(names)},'coeff':inherited_coeff})

    requery_hidden=0
    @lru_cache(None)
    def literal_requery(a,t,pars):
        nonlocal requery_hidden
        p=sum(a[:3]);ell=sum(a[:5]);q=a[5]
        lam,c,d,e,cap,mu=pars
        values=[]
        # k=3 has no intermediate followers; use two named last-two pairs.
        for B,C,J,V in product((0,1),repeat=4):
            first_den=p+t+B+C
            second_den=p+C+J+V
            value=(lam*share(t,first_den)+(1-lam)*share(C,second_den)
                   +c*(F(B,p+C+J+1)-share(V,second_den))
                   +F(d*J+e*V,ell+1)+cap*V
                   +mu*(F(q,p+t+B+1)-share(C,first_den)))
            values.append(value);requery_hidden+=1
        return min(values)

    portfolio_hidden=0
    @lru_cache(None)
    def literal_portfolio(i,a,t,q,params,mu):
        nonlocal portfolio_hidden
        p=sum(a[:i]);ell=sum(a[:5]);n=5-i
        am,al,bm,bl=params
        values=[]
        for hidden in product((0,1),repeat=n):
            den=p+t+sum(hidden)
            total=share(t,den)
            for j,f in enumerate(hidden):
                price,cap=(al,bl) if j==n-1 else (am,bm)
                total+=F(price*f,ell+1)+cap*f
            total+=mu*(F(q,p+t+sum(hidden[:-1])+1)-share(hidden[-1],den))
            values.append(total);portfolio_hidden+=1
        return min(values)

    literal_domain_comparisons=0
    for cut in data['portfolio']:
        qi=next(j for j,v in enumerate(cut['mu']) if F(v))
        mu=F(cut['mu'][qi]);params=tuple(F(cut[k]) for k in ('alpha_middle','alpha_last','beta_middle','beta_last'))
        mus=tuple(map(F,cut['mu']))
        for a in product((0,1),repeat=6):
            for t in (0,1):
                for q in ((a[5],) if qi==5 else (0,1)):
                    qs=[F()]*16;qs[qi]=q
                    lhs=literal_portfolio(cut['i'],a,t,q,params,mu)
                    rhs=pc['psi'](cut['i'],sum(a[:cut['i']]),sum(a[:5]),t,tuple(qs),*params,mus)
                    assert lhs==rhs
                    # The stored 13-query template and zero-padded 16 menu agree.
                    assert rhs==pc['psi'](cut['i'],sum(a[:cut['i']]),sum(a[:5]),t,tuple(qs),*params,mus+(F(),)*3)
                    literal_domain_comparisons+=1

    point=json.loads(paths['point'].read_text());cols=point['columns'];ys=[F(c['weight']) for c in cols]
    assert len(cols)==1905 and cols[0]['kind']=='K'
    blocks=[];block=None
    for j,c in enumerate(cols):
        if c['kind']=='hist':
            block={'index':j,'column':c,'joint':[]};blocks.append(block)
        elif c['kind']=='joint-reply':block['joint'].append((j,c))
    assert len(blocks)==16
    all_rows=[];records=[];hist_records=[]
    for family in ('nested','requery','portfolio'):
        for ci,cut in enumerate(data[family]):
            member=cut['member'];f,diag=cut['orb'];ct=6 if diag else 30
            row=[F()]*len(cols)
            if family=='requery':
                pars=tuple(map(F,cut['parameters']));row[0]=pars[4];lastprice=pars[2]+pars[3]
            elif family=='portfolio':
                params=tuple(F(cut[k]) for k in ('alpha_middle','alpha_last','beta_middle','beta_last'))
                am,al,bm,bl=params;n=5-cut['i'];row[0]=(n-1)*bm+bl;lastprice=(n-1)*am+al
                qi=next(j for j,v in enumerate(cut['mu']) if F(v));mu=F(cut['mu'][qi])
            contrib=[]
            for block in blocks:
                c=block['column'];a=tuple(map(int,c['actual_bits']));whole=sum(a)
                words=tuple(w for h,w in zip(c['hist'],PAT) for _ in range(h));assert len(words)==6
                edges=[(j,l) for j,l in product(range(6),repeat=2) if (j==l)==bool(diag)]
                assert len(edges)==ct
                histvalue=F() if family=='nested' else share(a[cut['i']],whole)+lastprice*share(a[5],whole)
                group_differences=Counter()
                for j,l in edges:
                    if family=='nested':
                        w=tuple(F(cut['weights'].get(n,'0')) for n in names)
                        v0=inherited_coeff(a,c['d'],0,w);v1=inherited_coeff(a,c['d'],1,w);sign=1
                    elif family=='requery':
                        v0=literal_requery(a,0,pars);v1=literal_requery(a,1,pars);sign=-1
                    else:
                        q=a[5] if qi==5 else (words[j]+words[l])[qi-6]
                        v0=literal_portfolio(cut['i'],a,0,q,params,mu)
                        v1=literal_portfolio(cut['i'],a,1,q,params,mu);sign=-1
                    histvalue+=sign*v0/ct
                    group_differences[f,diag,words[j],words[l]]+=sign*(v1-v0)/ct
                row[block['index']]=histvalue
                val=histvalue*ys[block['index']]
                for j,jc in block['joint']:
                    ff,dd,wi,wj=jc['group']
                    row[j]=group_differences[ff,dd,tuple(wi),tuple(wj)]*jc['state'][member]
                    val+=row[j]*ys[j]
                contrib.append({'hist_column':block['index'],'contribution':str(val)})
            original_row={'nested':nr['row'],'requery':rq['row'],'portfolio':pc['row']}[family](cols,cut)
            assert row==original_row,(family,ci)
            slack=sum((v*y for v,y in zip(row,ys)),F())
            assert slack==row[0]*ys[0]+sum(F(x['contribution']) for x in contrib)
            if family=='nested':assert slack==F(cut['slack'])
            if family=='requery':
                matches=[x for x in original_rq['selected'] if norm(x['cut'],'requery')==norm(cut,'requery')]
                assert len(matches)==1 and F(matches[0]['slack'])==slack
            raw='\n'.join(map(str,row)).encode()+b'\n'
            records.append({'family':family,'position':ci,'global_position':len(records),'cut':cut,'K_coefficient':str(row[0]),'row_sha256':hashlib.sha256(raw).hexdigest(),'nonzero_coefficients':sum(bool(x) for x in row),'exact_slack_on_frozen_5180_point':str(slack),'slack_origin':'inherited frozen nested value confirmed on assembled row' if family=='nested' else 'new exact diagnostic, not a value stored in the joint table','histogram_contributions':contrib})
            all_rows.append(tuple(row))
    assert len(all_rows)==18
    assert all(sha(p)==before[k]['sha256'] for k,p in paths.items())
    result={
        'status':'PASS',
        'scope':'18 stored templates and all 34290 row coefficients on the archived 1905-column layout; no original CLI, LP, or graph build. Nested hidden minima reused from the prior independent audit.',
        'audit_sha256':sha(Path(__file__)),
        'inputs':before,
        'source_fields':{'scope':data['scope'],'families':{k:len(data[k]) for k in ('nested','requery','portfolio')},'only_nested_records_have_historical_slack':True,'joint_table_has_no_source_point_or_W':True},
        'base_comparison':comparison,
        'old_portfolio_template_comparison':old_comparison,
        'point_identity':{'W':point['W'],'columns':len(cols),'histograms':len(blocks),'source_reported_rows':point.get('verified_rows'),'full_row_feasibility_reverified':False,'input_interface_inherited':str(paths['input_interface'])},
        'nested_inherited_independent_coefficients':120,
        'nested_inherited_hidden_states':5760,
        'nested_original_row_used_inherited_coefficient_cache':True,
        'portfolio_full_actual_binary_cases':literal_domain_comparisons,
        'portfolio_literal_hidden_evaluations':portfolio_hidden,
        'portfolio_13_vs_16_zero_padding_equal':True,
        'requery_unique_local_minima':literal_requery.cache_info().currsize,
        'requery_literal_hidden_evaluations':requery_hidden,
        'row_coefficient_comparisons':18*len(cols),
        'row_vector_distinct_count':len(set(all_rows)),
        'all_inputs_sha_unchanged':True,
        'new_original_entry_runs':0,
        'all_rows':records,
        'not_certified':['all 5180 necessary rows','5198 graph or reoptimization','complete-history SPE','six-player half','linear independence of 18 rows','original discovery provenance for missing portfolio metadata'],
    }
    report_path.parent.mkdir(parents=True,exist_ok=True)
    report_path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return {k:result[k] for k in ('status','portfolio_full_actual_binary_cases','portfolio_literal_hidden_evaluations','requery_unique_local_minima','requery_literal_hidden_evaluations','row_coefficient_comparisons','row_vector_distinct_count','new_original_entry_runs')}


if __name__=='__main__':
    if len(sys.argv)!=5:
        raise SystemExit('repo-root report-path joint-source-path original-requery-report')
    print(json.dumps(run(*(Path(x).resolve() for x in sys.argv[1:])),ensure_ascii=False))
