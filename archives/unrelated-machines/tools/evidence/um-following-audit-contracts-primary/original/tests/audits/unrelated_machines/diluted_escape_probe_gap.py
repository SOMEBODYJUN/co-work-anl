#!/usr/bin/env python3
"""稀释终端加共享逃逸：配置、全部LST边探针与GHMR证书。

This extension dynamically imports frozen baseline builders/verifiers without
editing them. Fraction throughout. It writes JSON only to stdout.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,importlib.util,json,platform,time

DEFAULT_REPO=Path(__file__).resolve().parents[3]


def import_file(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def extend_instance(base,k):
    d=base.instance(k)
    z=len(d['configs'])
    d['configs'].append([(F(1),())])
    blockers=set()
    for g in d['gadgets']:
        for b in g['blockers']:
            assert b not in blockers
            blockers.add(b)
            d['edges'][b][z]=F(1,2)
    d['escape']=z
    d['blockers']=blockers
    return d


def escape_probe_certificate(base,d,jfix,ifix):
    if ifix!=d['escape']:
        # All original edge certificates remain valid: the extra machine is
        # unused and no old processing time changed.
        return base.probe_certificate(d,jfix,ifix)
    assert jfix in d['blockers']
    normal=dict(d['down'])
    x={j:{i:F(1)} for j,i in normal.items()}
    x[jfix]={ifix:F(1)}
    for g in d['gadgets']:
        used={t:F(0) for t in g['terminals']}
        for j in g['ordinary']:
            i=normal[j]
            if i in used:
                used[i]+=d['edges'][j][i]
        residual={t:d['T']-used[t] for t in used}
        assert all(c>=0 for c in residual.values())
        remaining=[b for b in g['blockers'] if b!=jfix]
        total=sum(residual.values())
        assert total>=len(remaining)
        for b in remaining:
            x[b]={t:c/total for t,c in residual.items() if c}
    return x


def ghmr_certificate(d,raw,small,big,mandatory,unique,jfix=None,ifix=None):
    """Independent certificate covers required jobs and ALL optional U_i.

    This proves the actual GHMR maximum W equals F_i, without assuming an
    optimizer's answer. No greedy matching routine is imported here.
    """
    bridge=d['bridge']
    assert mandatory=={bridge}
    match={}
    if jfix is not None:
        assert ifix in big[jfix]
        match[jfix]=ifix
        for s in unique[ifix]:
            assert s!=jfix
            assert d['roles'][s][0] in ('ordinary','tree')
            match[s]=d['down'][s]
    if bridge not in match:
        occupied=set(match.values())
        root=next(r for r in d['roots'] if r not in occupied)
        match[bridge]=root
    assert mandatory<=match.keys()
    assert len(set(match.values()))==len(match)
    assert all(i in big[j] for j,i in match.items())
    if jfix is not None:
        assert match[jfix]==ifix
        assert unique[ifix]<=match.keys()
        full=sum((raw[ifix][s] for s in unique[ifix]),F(0))
        W=sum((raw[ifix][s] for s in unique[ifix] if s in match),F(0))
        assert W==full
        assert raw[ifix][jfix]+full-W<=d['T']
    return len(match)


def audit(repo,run_peer=True,all_star=True):
    basepath=repo/'tests/audits/unrelated_machines/diluted_sink_probe_gap.py'
    peerpath=repo/'tests/audits/unrelated_machines/heavy_matching_residual.py'
    base=import_file(basepath,'frozen_diluted_sink_baseline')
    peer=import_file(peerpath,'actual_peer_ghmr') if run_peer else None
    d=extend_instance(base,4)
    started=time.monotonic()
    configcols=base.check_config(d)
    sigma,value=base.optimal_schedule(d)
    assert d['escape'] not in sigma.values()
    n=len(d['edges']);m=len(d['configs'])
    oldedges=newedges=0
    maxload=F(0)
    for j,e in enumerate(d['edges']):
        for i in e:
            point=escape_probe_certificate(base,d,j,i)
            load=base.check_lst(d,point,j,i)
            maxload=max(maxload,load)
            if i==d['escape']:
                newedges+=1
            else:
                oldedges+=1
    lst_seconds=time.monotonic()-started
    raw=[[edge.get(i) for edge in d['edges']] for i in range(m)]
    domains=[set(edge) for edge in d['edges']]
    small=[{i for i in domains[j] if raw[i][j]<=d['T']/2} for j in range(n)]
    big={j:{i for i in domains[j] if raw[i][j]>d['T']/2} for j in range(n)}
    mandatory={j for j in range(n) if not small[j]}
    unique=[{j for j in range(n) if small[j]=={i}} for i in range(m)]
    ghmr_certificate(d,raw,small,big,mandatory,unique)
    bigprobes=0
    for j,neighbors in big.items():
        for i in neighbors:
            ghmr_certificate(d,raw,small,big,mandatory,unique,j,i)
            bigprobes+=1
    # Although GHMR has no big query at z, it too has a complete matching for
    # all uniquelysmall blockers; this prevents a misleading 'ignored zero'
    # interpretation of its failure mechanism.
    zmatches={}
    for g in d['gadgets']:
        for b,t in zip(g['blockers'],g['terminals']):
            zmatches[b]=t
    assert unique[d['escape']]==set(zmatches)
    assert len(set(zmatches.values()))==len(zmatches)
    assert all(t in big[b] for b,t in zmatches.items())
    stars=0
    if all_star:
        for j,e in enumerate(d['edges']):
            for i in e:
                base.star_matching_certificate(d,i,j)
                stars+=1
    actual=None
    if peer is not None:
        peerstarted=time.monotonic()
        outcome=peer.filter_domains(raw,d['T'])
        assert outcome['feasible'] and not outcome['trace']
        assert all(outcome['domains'][j]==domains[j] for j in range(n))
        actual={'accepted':outcome['feasible'],'rounds':outcome['rounds'],
                'deleted_edges':len(outcome['trace']),
                'elapsed_seconds':round(time.monotonic()-peerstarted,3)}
    formulas=[]
    for k in range(4,65):
        h,a=base.height(k)
        assert h>=3
        optimum=2-F(1,k);T=1+F(1,k)
        assert (optimum/T)*T==optimum
        assert optimum/T==2-F(3,k+1)
        assert 2**(h-1)*F(1,2)>=2>optimum
        # Ordinary LST mass after all k normal jobs are sent down.
        N=k*(k-1)
        assert N*T-k==N-1
        assert N*T-k>=N-2
        formulas.append({'k':k,'h':h,'active_bottom_lower_bound':str(2**(h-1)),
                         'escape_load_lower_bound':str(2**(h-1)*F(1,2)),
                         'optimum':str(optimum),'T':str(T),'ratio':str(optimum/T)})
    return {'title':'稀释终端与共享逃逸的全部边探针及GHMR有限审计',
            'python':platform.python_version(),'arithmetic':'fractions.Fraction; exact',
            'seed':None,'extension_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'base_path':str(basepath.relative_to(repo)),
            'base_sha256':hashlib.sha256(basepath.read_bytes()).hexdigest(),
            'peer_path':str(peerpath.relative_to(repo)),
            'peer_sha256':hashlib.sha256(peerpath.read_bytes()).hexdigest(),
            'expanded':{'k':4,'height':d['h'],'N':d['N'],'machines':m,'jobs':n,
                        'eligible_edges':oldedges+newedges,'configuration_columns':configcols,
                        'all_original_edge_LST_probes_checked':oldedges,
                        'all_added_escape_edge_LST_probes_checked':newedges,
                        'max_probe_load':str(maxload),'T':str(d['T']),
                        'independent_GHMR_big_edge_certificates':bigprobes,
                        'all_star_matching_certificates':stars,
                        'only_mandatory_job':d['bridge'],
                        'constructed_schedule_value':str(value),
                        'actual_peer_GHMR':actual,'LST_elapsed_seconds':round(lst_seconds,3)},
            'compressed_formula_checks':formulas,
            'limits':['Only k=4 expanded; k=4..64 are formula checks, not scheduling enumeration.',
                      'General OPT lower bound is proved separately; no full expanded assignment oracle.',
                      'All edge LST probes are separate certificates, not one joint distribution.',
                      'No guarantee for probes that couple heavy-cardinality or configuration constraints.',
                      'No universal approximation algorithm, hardness theorem, or novelty claim.']}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,default=DEFAULT_REPO)
    parser.add_argument('--skip-peer',action='store_true')
    parser.add_argument('--skip-star',action='store_true')
    args=parser.parse_args()
    print(json.dumps(audit(args.repo,not args.skip_peer,not args.skip_star),ensure_ascii=False,indent=2))
