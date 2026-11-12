#!/usr/bin/env python3
"""Exact source-2 redistribution; no optimization and no project-code imports.

All files written by this script stay beside this script.  Affine lines use
the schema [intercept, delta_coefficient].  Each envelope is obtained from all
16 literal tail costs, with all tied tails retained.
"""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
END = F(5977, 6912)
T5 = F(43, 48)
STAR = F(61273, 6912)
EPS = F(1, 144)
TAILS = list(product((0, 1), repeat=4))
BITS = list(product((0, 1), repeat=9))
TARGETS = [('A'+str(j+1), j) for j in range(6)] + [('X', 6), ('C', 8)]


def write(name, obj):
    (HERE/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')


def add(x, y):
    return (x[0]+y[0], x[1]+y[1])


def sub(x, y):
    return (x[0]-y[0], x[1]-y[1])


def scale(x, q):
    return (x[0]*q, x[1]*q)


def val(x, d):
    return x[0]+x[1]*d


def enc(x):
    return [str(x[0]), str(x[1])]


def dec(x):
    return tuple(map(F, x))


def weights(q0, s, d):
    tau = {3:F(0), 4:END-d, 5:T5+d}
    beta = {j:q0/2+tau[j]+sum(q0*tau[k]/((7-k)*(8-k))
                             for k in range(j+1, 6)) for j in (3, 4, 5)}
    return tau, beta, 25+sum(tau.values())-s, 1+sum(beta.values())


def cost(q0, s, p, t, q, r, d):
    tau, beta, a, S = weights(q0, s, d)
    L = p+t+sum(r)
    num = a*t-r[3]-sum(tau[j]*r[j-3] for j in (3, 4, 5))
    assert L or num == 0
    out = num/L if L else F(0)
    out += sum(beta[j]*r[j-3] for j in (3, 4, 5))+r[3]
    out += q/(p+t+sum(r[:3])+1)
    out += sum(tau[j]*q/(p+t+sum(r[:j-3])+7-j) for j in (3, 4, 5))
    return out


def line(q0, s, context, r):
    args = [q0, s, context['p'], context['t'], F(context['q']), r]
    b = cost(*args, F(0))
    return (b, cost(*args, F(1))-b)


def minimizers(lines, d):
    values = {name:val(l, d) for name, l in lines.items()}
    lo = min(values.values())
    return lo, [name for name in lines if values[name] == lo]


def envelope(lines, left=F(0), right=END):
    candidates = {left, right}
    pairwise = []
    for (n1, x), (n2, y) in combinations(lines.items(), 2):
        if x[1] != y[1]:
            d = (y[0]-x[0])/(x[1]-y[1])
            if left <= d <= right:
                candidates.add(d)
                pairwise.append({'tails':[n1, n2], 'delta':str(d)})
    candidates = sorted(candidates)
    interior = [minimizers(lines, (u+v)/2)[1]
                for u, v in zip(candidates, candidates[1:])]
    kept = [candidates[0]]
    for k, d in enumerate(candidates[1:-1], 1):
        active = minimizers(lines, d)[1]
        if interior[k-1] != active or interior[k] != active:
            kept.append(d)
    kept.append(candidates[-1])
    points = []
    for d in kept:
        minimum, active = minimizers(lines, d)
        points.append({'delta':str(d), 'minimum':str(minimum), 'active_tails':active,
                       'all_16_costs':{n:str(val(l, d)) for n, l in lines.items()}})
    cells = []
    for u, v in zip(kept, kept[1:]):
        _, active = minimizers(lines, (u+v)/2)
        m = lines[active[0]]
        gaps = {n:[str(val(sub(l, m), u)), str(val(sub(l, m), v))]
                for n, l in lines.items()}
        assert all(F(z) >= 0 for zz in gaps.values() for z in zz)
        cells.append({'left':str(u), 'right':str(v), 'minimum_affine':enc(m),
                      'active_tails':active, 'all_16_endpoint_gaps':gaps})
    return {'breakpoints':list(map(str, kept)), 'points':points, 'open_cells':cells,
            'all_pair_intersections_in_domain':pairwise}


def pure_contexts():
    return {f'p{p}_t{t}_o{o}':{'p':p, 't':t, 'o':o, 'q':str(F(o, 6))}
            for p, t, o in product((0, 1), repeat=3)}


def ordered_contexts():
    result = {}
    for p in (0, 1):
        for d in range(7):
            for t in (0, 1):
                if (t == 0 and d < 6) or (t == 1 and d > 0):
                    result[f'p{p}_d{d}_t{t}'] = {'p':p, 'd':d, 't':t,
                                               'q':str(F(d-t, 5))}
    return result


def mline(case, cid, d):
    lines = {r:dec(x) for r, x in case['states'][cid].items()}
    _, active = minimizers(lines, d)
    return lines[active[0]]


def mvalue(case, cid, d):
    return min(val(dec(x), d) for x in case['states'][cid].values())


def fdline(case, p, d, probe):
    out = (F(0), F(0))
    if d < 6:
        out = add(out, scale(mline(case, f'p{p}_d{d}_t0', probe), F(6-d, 6)))
    if d > 0:
        out = add(out, scale(mline(case, f'p{p}_d{d}_t1', probe), F(d, 6)))
    return out


def fdvalue(case, p, d, delta):
    ans = F(0)
    if d < 6:
        ans += F(6-d, 6)*mvalue(case, f'p{p}_d{d}_t0', delta)
    if d > 0:
        ans += F(d, 6)*mvalue(case, f'p{p}_d{d}_t1', delta)
    return ans


def ordered_projection(case):
    coarse = sorted({F(x) for env in case['envelopes'].values() for x in env['breakpoints']})
    crossings = []
    allpoints = set(coarse)
    for left, right in zip(coarse, coarse[1:]):
        probe = (left+right)/2
        for p in (0, 1):
            f = {d:fdline(case, p, d, probe) for d in range(1, 7)}
            for d, e in combinations(range(1, 7), 2):
                diff = sub(f[d], f[e])
                if diff[1]:
                    x = -diff[0]/diff[1]
                    if left <= x <= right:
                        allpoints.add(x)
                        minimum = min(val(y, x) for y in f.values())
                        crossings.append({'p':p, 'd_pair':[d,e], 'delta':str(x),
                                          'coarse_cell':[str(left),str(right)],
                                          'on_G':val(f[d],x)==minimum})
                elif diff[0] == 0:
                    crossings.append({'p':p, 'd_pair':[d,e], 'coarse_cell':[str(left),str(right)],
                                      'identical_on_cell':True,
                                      'on_G':val(f[d],probe)==min(val(y,probe) for y in f.values())})
    allpoints = sorted(allpoints)
    points=[]; cells=[]
    for delta in allpoints:
        pdata=[]
        for p in (0,1):
            f={d:fdvalue(case,p,d,delta) for d in range(7)}
            g=min(f[d] for d in range(1,7))
            pdata.append({'p':p, 'f':{str(d):str(x) for d,x in f.items()},
                          'G':str(g), 'active_d':[d for d in range(1,7) if f[d]==g]})
        points.append({'delta':str(delta), 'prefix_tables':pdata})
    for left,right in zip(allpoints,allpoints[1:]):
        probe=(left+right)/2; pdata=[]
        for p in (0,1):
            f={d:fdline(case,p,d,probe) for d in range(7)}
            best=min(val(f[d],probe) for d in range(1,7))
            active=[d for d in range(1,7) if val(f[d],probe)==best]
            g=f[active[0]]
            gaps={str(d):[str(val(sub(f[d],g),left)),str(val(sub(f[d],g),right))]
                  for d in range(1,7)}
            assert all(F(x)>=0 for zz in gaps.values() for x in zz)
            pdata.append({'p':p, 'f_affine':{str(d):enc(f[d]) for d in range(7)},
                          'G_affine':enc(g), 'active_d':active,
                          'all_6_endpoint_gaps':gaps})
        cells.append({'left':str(left),'right':str(right),'prefix_tables':pdata})
    return {'conditional_breakpoints':list(map(str,coarse)),
            'all_f_pair_intersections':crossings, 'breakpoints':list(map(str,allpoints)),
            'points':points,'open_cells':cells}


def gline(case,p,probe):
    f={d:fdline(case,p,d,probe) for d in range(1,7)}
    return min(f.values(),key=lambda x:val(x,probe))


def gvalue(case,p,delta):
    return min(fdvalue(case,p,d,delta) for d in range(1,7))


def row_at(case,target,target_index,delta,c_only=False):
    q0=F(case['q0']); s=F(case['s'])
    tau,beta,a,S=weights(q0,s,delta)
    mu=S-s/5
    coefficients=[]
    if case['mode']=='pure':
        cached_minima={(p,t,o):mvalue(case,f'p{p}_t{t}_o{o}',delta)
                       for p,t,o in product((0,1),repeat=3)}
    else:
        cached_G={p:gvalue(case,p,delta) for p in (0,1)}
    for b in BITS:
        actual_load=sum(b[:6]); share=F(b[1],actual_load) if actual_load else F(0)
        if case['mode']=='pure':
            m=cached_minima[(b[0],b[target_index],b[7])]
        else:
            m=b[7]*cached_G[b[0]]
        value=a*share-m
        if c_only:
            value+=mu*b[8]
        coefficients.append(str(value))
    coefficients.append(str(S-mu if c_only else S))
    return {'id':f"{case['id']}__delta_{delta.numerator}_{delta.denominator}__{target}",
            'case':case['id'],'source':2,'mode':case['mode'],'target':target,'delta':str(delta),
            'sense':'>=','rhs':'0','numeric_divisor':'25','a':coefficients,
            'weights':{'tau':{str(j):str(x) for j,x in tau.items()},
                       'beta':{str(j):str(x) for j,x in beta.items()},
                       'source_IC':str(a),'K_before_C_equality':str(S),
                       'last_cap':'1','last_query_mean':'1'},
            'C_equality_multiplier':str(mu) if c_only else None}


def affine_row(case,target,target_index,left,right,c_only=False):
    probe=(left+right)/2
    r0=row_at(case,target,target_index,left,c_only)
    r1=row_at(case,target,target_index,right,c_only)
    A=[];B=[]
    for x,y in zip(r0['a'],r1['a']):
        v0,v1=F(x),F(y)
        slope=(v1-v0)/(right-left)
        A.append(str(v0-slope*left));B.append(str(slope))
    direct=row_at(case,target,target_index,probe,c_only)
    assert all(F(x)+F(y)*probe==F(z) for x,y,z in zip(A,B,direct['a']))
    return {'id':f"{case['id']}__cell_{left.numerator}_{left.denominator}__{right.numerator}_{right.denominator}__{target}",
            'case':case['id'],'source':2,'target':target,'left':str(left),'right':str(right),
            'intercept':A,'delta_coefficient':B,'numeric_divisor':'25'}


def main():
    cases=[]
    for mode,q0 in [('pure',F(1,6)),('ordered',F(1,5))]:
        for sname,s in [('s0',F(0)),('sstar',STAR),('s9',F(9))]:
            cid=f'{mode}_q{q0.denominator}_{sname}'
            contexts=pure_contexts() if mode=='pure' else ordered_contexts()
            case={'id':cid,'mode':mode,'q0':str(q0),'s':str(s),
                  'domain':['0',str(END)],'contexts':contexts,'states':{},'envelopes':{}}
            for name,context in contexts.items():
                lines={''.join(map(str,r)):line(q0,s,context,r) for r in TAILS}
                case['states'][name]={r:enc(l) for r,l in lines.items()}
                case['envelopes'][name]=envelope(lines)
            if mode=='ordered':
                case['projection']=ordered_projection(case)
                case['breakpoints']=case['projection']['breakpoints']
            else:
                case['breakpoints']=list(map(str,sorted({F(x) for e in case['envelopes'].values()
                                                         for x in e['breakpoints']})))
            cases.append(case)
            print(cid,'breakpoints',case['breakpoints'],flush=True)
    write('exact_envelopes.json',{'affine_schema':['intercept','delta_coefficient'],
                                'tail_order':['r3','r4','r5','r6'],'cases':cases})
    write('coordinate_contract.json',{'n_customer_columns':512,'K_column':512,'total_columns':513,
          'customer_bits':['a1','a2','a3','a4','a5','a6','x','o','c'],
          'customer_order':'lexicographic 0 before 1; c fastest; a1 slowest',
          'customer_columns':[{'index':i,'bits':list(b)} for i,b in enumerate(BITS)],
          'row_schema':'rows is a list; each row.a is a length-513 list of exact rational strings',
          'row_inequality':'sum_{k=0}^{512} row.a[k] * coordinate[k] >= 0',
          'raw_scale':'last cap and query mean weights 1; optional positive numeric divisor 25',
          'duplicates':'all provenance rows retained, including vectors identical across cases or cells',
          'C_equality':'E_C=|C|-K; R_C_only=R_general_C+(S-s/5)E_C'})
    raw=[]; checkpoints=[]; affine=[]; weak_tables=[]
    for case in cases:
        bp=list(map(F,case['breakpoints']))
        targets=TARGETS+[('C-only',8)] if case['mode']=='pure' else [('ordered-six-menu',None)]
        for d in bp:
            for target,ix in targets:
                raw.append(row_at(case,target,ix,d,target=='C-only'))
        if EPS not in bp:
            for target,ix in targets:
                checkpoints.append(row_at(case,target,ix,EPS,target=='C-only'))
        for left,right in zip(bp,bp[1:]):
            for target,ix in targets:
                affine.append(affine_row(case,target,ix,left,right,target=='C-only'))
        for delta in sorted(set(bp+[EPS]+[(x+y)/2 for x,y in zip(bp,bp[1:])])):
            kind='breakpoint' if delta in bp else ('epsilon' if delta==EPS else 'open_cell_probe')
            table=[]
            for name,ctx in case['contexts'].items():
                lines={r:dec(l) for r,l in case['states'][name].items()}
                minimum,active=minimizers(lines,delta)
                table.append({'context':name,'minimum':str(minimum),'all_active_tails':active})
            weak_tables.append({'case':case['id'],'delta':str(delta),'kind':kind,'tables':table})
    write('exact_family.json',{'schema':'length-513 list a; rational strings; raw >=0 rows',
                             'rows':raw,'row_count':len(raw)})
    write('epsilon_rows.json',{'delta':str(EPS),'rows':checkpoints,'row_count':len(checkpoints)})
    write('affine_family.json',{'schema':'row(delta)=intercept+delta*delta_coefficient; all 513 columns',
                              'closed_endpoint_consistency':True,'rows':affine,'row_count':len(affine)})
    write('all_weak_minimum_tables.json',{'tables':weak_tables})
    epsilon_checks=[]
    for case in cases:
        if case['mode']!='pure' or F(case['s'])==9:
            continue
        old=row_at(case,'C-only',8,F(0),True)
        new=row_at(case,'C-only',8,EPS,True)
        columns=[]
        for i,b in enumerate(BITS):
            p,c,o=b[0],b[8],b[7]
            n4=F(o,6*(p+2*c+3));n5=F(o,6*(p+3*c+2))
            m10=p*c*(1-o);m00=(1-p)*c*(1-o)
            expected=-EPS*(n5-n4)+F(1,180)*m10
            if F(case['s'])==STAR:
                expected+=F(101,27648)*m00
            actual=F(new['a'][i])-F(old['a'][i])
            assert actual==expected
            columns.append({'index':i,'actual_difference':str(actual),'claimed_difference':str(expected),
                            'residual':str(actual-expected)})
        assert F(new['a'][512])-F(old['a'][512])==0
        columns.append({'index':512,'actual_difference':'0','claimed_difference':'0','residual':'0'})
        epsilon_checks.append({'case':case['id'],'delta':str(EPS),'status':'PASS',
                               'checked_columns':columns})
    write('epsilon_identity_checks.json',{'status':'PASS','identities':epsilon_checks,
          'scope':'exact row equality, not a global objective or a claimed SPE realization'})
    summary={'agent_id':'/root/source2_conditional_redistribution','optimizer_calls':0,
             'global_candidate_reads':0,'case_count':len(cases),'raw_endpoint_rows':len(raw),
             'epsilon_extra_rows':len(checkpoints),'affine_segment_rows':len(affine),
             'raw_endpoint_columns':513*len(raw),'affine_state_count':sum(16*len(c['contexts']) for c in cases),
             'case_summary':[]}
    for c in cases:
        summary['case_summary'].append({'id':c['id'],'breakpoints':c['breakpoints'],
              'open_cells':len(c['breakpoints'])-1,'contexts':len(c['contexts']),
              'all_G_active_d':sorted({d for x in c.get('projection',{}).get('points',[])
                                         for pp in x['prefix_tables'] for d in pp['active_d']}),
              'all_f_pair_intersections':len(c.get('projection',{}).get('all_f_pair_intersections',[]))})
    hashes={}
    for r in raw:
        key=tuple(r['a']);hashes.setdefault(key,[]).append(r['id'])
    summary['duplicate_endpoint_groups']=[ids for ids in hashes.values() if len(ids)>1]
    summary['unique_endpoint_vectors']=len(hashes)
    write('derivation_summary.json',summary)
    lines=['# 全部真实包络断点','',
           '端点 0 与 5977/6912 均保留；每个区间上的 16 态比较及全部弱达到态见 exact_envelopes.json。',
           'ordered 的分片包含所有条件最小值变化及全部六重数仿射交点，不预设 d=1。','']
    for c in cases:
        lines += ['## '+c['id'],'','| 序号 | δ | 引发事件的条件 |','|---:|---:|---|']
        for i,d in enumerate(c['breakpoints']):
            causes=[name for name,e in c['envelopes'].items() if d in e['breakpoints']]
            lines.append('| '+str(i)+' | '+d+' | '+', '.join(causes)+' |')
        lines+=['']
    (HERE/'breakpoint_table.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ['duplicate_endpoint_groups']},ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
