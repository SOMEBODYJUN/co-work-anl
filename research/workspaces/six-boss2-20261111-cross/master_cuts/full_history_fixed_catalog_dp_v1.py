#!/usr/bin/env python3
"""One approved 12-label input, all full-history SPE terminal menus.

All mathematical comparisons use unbounded Python integers at utility scale60.
The count cache stores complete menus; strategy witnesses also carry a desired
terminal, so different ordered histories are not forced to share one action.
"""
from __future__ import annotations
from collections import deque
from fractions import Fraction as F
from pathlib import Path
import datetime, gzip, hashlib, json, platform, resource, sys, time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
INPUT=HERE/'full_history_probe_12label_v1.json'
INPUT_SHA='59e86b2961662aba4c9a9c9128fa03f2ee68b0b7c5bd7577896bc897838508f7'
REVIEW=HERE.parent/'main_verify_twelve_label_input_v1.json'
STEM='full_history_probe_12label_v1'


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def log(stage,**kw):print(json.dumps({'stage':stage,**kw},ensure_ascii=False),flush=True)
def compositions(n,k):
    if k==1:yield (n,);return
    for first in range(n+1):
        for tail in compositions(n-first,k-1):yield (first,)+tail
def save(kind,obj,compressed=False):
    p=HERE/(STEM+'_'+kind+'.json'+('.gz' if compressed else ''))
    encoded=(json.dumps(obj,ensure_ascii=False,separators=(',',':'))+'\n').encode()
    if compressed:
        with p.open('xb') as raw:
            with gzip.GzipFile(filename='',fileobj=raw,mode='wb',mtime=0) as stream:stream.write(encoded)
    else:
        with p.open('xb') as stream:stream.write(encoded)
    return p


def run():
    start=time.time()
    assert sha(INPUT)==INPUT_SHA and json.loads(REVIEW.read_text())['status']=='PASS'
    assert INPUT_SHA in REVIEW.read_text()
    assert not (HERE/(STEM+'_menus.json.gz')).exists()
    inp=json.loads(INPUT.read_text());assert inp['players']==6 and len(inp['labels'])==12
    labels=inp['labels'];N=int(inp['unit_customers']);types=[]
    for entry in inp['nonzero_customer_types']:
        mask=entry['mask'];count=int(entry['integer_clones']);assert type(mask) is int and count>0
        members=tuple(a for a in range(12) if mask&(1<<a));assert sum(a>=6 for a in members)==1
        types.append((members,count))
    assert sum(count for _,count in types)==N
    layers=[list(compositions(d,12)) for d in range(7)]
    states=[c for layer in layers for c in layer];sid={c:i for i,c in enumerate(states)}
    leaves=layers[6];fid={f:i for i,f in enumerate(leaves)}
    assert len(states)==18564 and len(leaves)==12376
    utilities=[];welfare=[]
    for f in leaves:
        pay=[0]*12;W=0
        for members,count in types:
            load=sum(f[a] for a in members)
            if not load:continue
            assert 60%load==0;W+=count;share=count*(60//load)
            for a in members:
                if f[a]:pay[a]+=share
        assert sum(f[a]*pay[a] for a in range(12))==60*W
        utilities.append(tuple(pay));welfare.append(W)
    assert max(welfare)==N
    menus=[None]*len(states);thresholds=[None]*len(states)
    min_leaves=[None]*len(states);minimum_values=[None]*len(states);children=[None]*len(states)
    for f in leaves:menus[sid[f]]=(fid[f],)
    log('leaf-payoffs-ready',leaves=len(leaves),types=len(types),population_bits=N.bit_length(),seconds=time.time()-start)
    for depth in range(5,-1,-1):
        for c in layers[depth]:
            j=sid[c];child=[]
            for a in range(12):
                q=list(c);q[a]+=1;child.append(sid[tuple(q)])
            mins=[min(menus[child[a]],key=lambda k:(utilities[k][a],k)) for a in range(12)]
            values=[utilities[mins[a]][a] for a in range(12)];tau=max(values)
            kept=set()
            for a in range(12):
                for leaf in menus[child[a]]:
                    assert leaves[leaf][a]>0
                    if utilities[leaf][a]>=tau:kept.add(leaf)
            assert kept
            menus[j]=tuple(sorted(kept));thresholds[j]=tau
            min_leaves[j]=tuple(mins);minimum_values[j]=tuple(values);children[j]=tuple(child)
        log('menu-layer',depth=depth,states=len(layers[depth]),retained=sum(len(menus[sid[c]]) for c in layers[depth]),seconds=time.time()-start)
    assert sum(len(m) for m in menus)<=475020
    root=sid[(0,)*12];rootmenu=menus[root]
    target=fid[tuple(inp['target_terminal_counts'])]
    worst=min(rootmenu,key=lambda k:(welfare[k],k));worst_ids=[k for k in rootmenu if welfare[k]==welfare[worst]]
    target_rejection=None;order_checks=[]
    for depth in range(5,-1,-1):
        c=tuple([1]*depth+[0]*(12-depth));j=sid[c];a=depth;child=children[j][a]
        member=target in menus[child];pay=utilities[target][a];tau=thresholds[j]
        record={'prefix':labels[:depth],'state_id':j,'action':labels[a],
                'target_in_specified_child':member,'target_payoff_scaled60':str(pay),
                'threshold_scaled60':str(tau),'specified_action_admissible':member and pay>=tau}
        order_checks.append(record)
        if not record['specified_action_admissible'] and target_rejection is None:
            # This is the first failure encountered from the leaf upward.
            assert member and tau>pay
            b=next(b for b in range(12) if minimum_values[j][b]==tau)
            leaf=min_leaves[j][b]
            target_rejection={**record,'deviation_label':labels[b],
                'deviation_child_state_id':children[j][b],
                'deviation_child_menu_size':len(menus[children[j][b]]),
                'deviation_minimizing_terminal_id':leaf,'deviation_minimizing_terminal':list(leaves[leaf]),
                'deviation_minimum_payoff_scaled60':str(tau),
                'strict_gap_scaled60':str(tau-pay),'strict_gap_unit_customer':str(F(tau-pay,60)),
                'strict_gap_normalized':str(F(tau-pay,60*N)),
                'all_child_minimizers':list(min_leaves[j]),
                'all_child_minima_scaled60':list(map(str,minimum_values[j]))}
    def witness(root_leaf):
        pending=deque([(root,root_leaf)]);seen=set();nodes=[];minimum_margin=None
        while pending:
            j,leaf=pending.popleft()
            if (j,leaf) in seen:continue
            seen.add((j,leaf));c=states[j]
            assert leaf in menus[j]
            if sum(c)==6:
                assert leaves[leaf]==c
                nodes.append({'state_id':j,'target_terminal_id':leaf,'terminal':True});continue
            a=next(a for a in range(12) if leaf in menus[children[j][a]] and utilities[leaf][a]>=thresholds[j])
            targets=list(min_leaves[j]);targets[a]=leaf
            payoff=utilities[leaf][a]
            margins=[payoff-utilities[targets[b]][b] for b in range(12)]
            assert min(margins)>=0
            minimum_margin=min(margins) if minimum_margin is None else min(minimum_margin,min(margins))
            nodes.append({'state_id':j,'target_terminal_id':leaf,'chosen_action':a,
                'child_target_terminal_ids':targets,'minimum_IC_margin_scaled60':str(min(margins))})
            for b in range(12):pending.append((children[j][b],targets[b]))
        return {'root_state_id':root,'root_target_terminal_id':root_leaf,
            'meaning':'At an ordered history carry its desired terminal. Chosen child retains it; every other child gets the stored credible target. Count/target pairs may share this certificate without forcing count-uniform actions.',
            'nodes':nodes,'node_count':len(nodes),'minimum_IC_margin_scaled60':str(minimum_margin),
            'covers_all_ordered_histories_by_recursive_unfolding':True}
    witnesses={'worst':witness(worst)}
    if target in rootmenu:witnesses['target']=witness(target)
    else:assert target_rejection is not None
    common={'input_path':str(INPUT.relative_to(ROOT)),'input_sha256':INPUT_SHA,
        'script_sha256':sha(__file__),'arithmetic':'Python arbitrary-precision integer utilities scaled by60; weak comparisons >=.',
        'players':6,'labels':labels,'unit_customers':str(N)}
    menu_path=save('menus',{**common,'leaf_terminal_counts':[list(f) for f in leaves],
        'states':[{'state_id':j,'past_counts':list(c),'menu_terminal_ids':list(menus[j]),
             'threshold_scaled60':None if thresholds[j] is None else str(thresholds[j]),
             'child_state_ids':None if children[j] is None else list(children[j]),
             'child_minimizing_terminal_ids':None if min_leaves[j] is None else list(min_leaves[j]),
             'child_minimum_payoffs_scaled60':None if minimum_values[j] is None else list(map(str,minimum_values[j]))}
             for j,c in enumerate(states)]},True)
    witness_path=save('witnesses',{**common,**witnesses},True)
    result={**common,'status':'EXACT_FIXED_CATALOG_COMPLETED','OPT6':str(N),
        'root_menu_size':len(rootmenu),'root_terminal_records':[
            {'terminal_id':k,'counts':list(leaves[k]),'W':str(welfare[k]),'W_over_OPT6':str(F(welfare[k],N))} for k in rootmenu],
        'target_terminal_id':target,'target_in_root_menu':target in rootmenu,
        'target_W':str(welfare[target]),'target_W_over_OPT6':str(F(welfare[target],N)),
        'specified_actual_order_realizable':target_rejection is None,
        'specified_order_checks_leaf_to_root':order_checks,'first_target_rejection_leaf_to_root':target_rejection,
        'minimum_root_W':str(welfare[worst]),'minimum_root_W_over_OPT6':str(F(welfare[worst],N)),
        'minimum_root_2W_minus_OPT6':str(2*welfare[worst]-N),
        'worst_terminal_ids':worst_ids,'selected_worst_terminal_id':worst,
        'states':len(states),'terminals':len(leaves),'all_retained_state_terminal_pairs':sum(len(m) for m in menus),
        'menus_path':str(menu_path.relative_to(ROOT)),'menus_sha256':sha(menu_path),
        'witnesses_path':str(witness_path.relative_to(ROOT)),'witnesses_sha256':sha(witness_path),
        'worst_witness_nodes':witnesses['worst']['node_count'],
        'minimum_worst_witness_IC_scaled60':witnesses['worst']['minimum_IC_margin_scaled60'],
        'scope':'Exactly this fixed12-label catalog and all its full-history pure SPE terminal counts. Failure does not exclude added labels or other customer weights. This does not realize all columns of the source necessary LP.',
        'seconds':time.time()-start,'optimizer_calls':0,'random_inputs':0,'input_catalogs':1,
        'mathematical_float_operations':0,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    result_path=save('result',result)
    log('fixed-catalog-complete',result_sha256=sha(result_path),root_menu_size=len(rootmenu),
        target_in_root_menu=target in rootmenu,minimum_ratio=result['minimum_root_W_over_OPT6'],
        first_rejection=target_rejection,seconds=time.time()-start,peak_rss_kib=result['peak_rss_kib'])


def main():
    started=time.time();stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();success=False
    try:run();success=True
    finally:save('execution',{'command':[sys.executable,'-B',str(Path(__file__).resolve())],
        'cwd':str(ROOT),'input_sha256':INPUT_SHA,'script_sha256':sha(__file__),
        'main_input_review_sha256':sha(REVIEW),'python':platform.python_version(),
        'started_utc':stamp,'elapsed_seconds':time.time()-started,'success':success,
        'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})


if __name__=='__main__':main()
