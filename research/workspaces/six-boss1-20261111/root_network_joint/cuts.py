"""Extend two exact dual upper bounds to ALL 32 states in every hist/word.

These are valid necessary rows for the full single-root marginal lift,
with original point coordinates retained symbolically.  They separate the
current 35-positive-mu certificate, never the old point after eliminating mu.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import json,time
from model import Model,bits,q,dump,sha,PINS,POINT,MU,NET,serial
from bounds import root_coefficient


def extend(left, right, coefficient, all_left, all_right):
    alpha=dict(left);beta=dict(right)
    if not beta:
        beta={t:F() for t in all_right}
    for s in all_left:
        if s not in alpha:
            alpha[s]=max(coefficient(s,t)-v for t,v in beta.items())
    for t in all_right:
        if t not in beta:
            beta[t]=max(coefficient(s,t)-v for s,v in alpha.items())
    gaps=[alpha[s]+beta[t]-coefficient(s,t) for s in all_left for t in all_right]
    assert min(gaps)>=0
    return alpha,beta,min(gaps),len(gaps)


def main():
    started=time.monotonic();m=Model();here=Path(__file__).parent
    bounds=json.loads((here/'fixed_mu_upper_bounds_exact.json').read_text())
    selected=[r for r in bounds['rows'] if r['negative']]
    assert len(selected)==2
    mus=[dict(hist=h,old_word=w,state=s) for h,hc in m.hist.items() for w,n in enumerate(hc['hist']) if n for s in range(32)]
    mi={(v['hist'],v['old_word'],v['state']):j for j,v in enumerate(mus)}
    assert len(mus)==1216
    oldcols=m.point['columns'];own={};cur=None
    for j,c in enumerate(oldcols[:4849]):
        if c['kind']=='hist':cur=j
        elif c['kind']=='joint-reply':
            f,d,v,w=c['group'];own.setdefault((cur,f,d,tuple(v),tuple(w)),{})[tuple(c['state'])]=j
    rows=[]
    for frozen in selected:
        name=frozen['name'];a=defaultdict(F);b=defaultdict(F);pieces=[];cells=0
        if name[0]=='cross-pair':
            old={(z['hist'],z['source_old_word'],z['donor_old_word']):z for z in frozen['pieces']}
            for h,hc in m.hist.items():
                for v,nv in enumerate(hc['hist']):
                    for w,nw in enumerate(hc['hist']):
                        count=nv*(nw-int(v==w))
                        if not count:continue
                        p=old.get((h,v,w),{})
                        left={r['state']:F(r['dual']) for r in p.get('left',[])}
                        right={r['state']:F(r['dual']) for r in p.get('right',[])}
                        coef=lambda s,t:root_coefficient(name,v,w,s,t)
                        alpha,beta,gap,checked=extend(left,right,coef,range(32),range(32))
                        factor=F(count,30);cells+=checked
                        for s,x in alpha.items():a[mi[h,v,s]]+=factor*x
                        for t,x in beta.items():a[mi[h,w,t]]+=factor*x
                        pieces.append(dict(hist=h,source_old_word=v,donor_old_word=w,factor=factor,
                            alpha=[alpha[s] for s in range(32)],beta=[beta[t] for t in range(32)],
                            coefficient_cells=checked,minimum_dominance_gap=gap))
        else:
            assert name==['Y-to-R',[1,[0,0,0]],4]
            old={(z['hist'],z['root_old_word']):z for z in frozen['pieces']}
            for h,hc in m.hist.items():
                for w,n in enumerate(hc['hist']):
                    if not n:continue
                    p=old.get((h,w),{})
                    left={r['state']:F(r['dual']) for r in p.get('left',[])}
                    right={r['state']:F(r['dual']) for r in p.get('right',[])}
                    def coef(s,r):
                        e=bits(s,5);t=w>>2
                        return q(e[4],t+sum(e))-F(r,t+sum(e[:4])+1)
                    alpha,beta,gap,checked=extend(left,right,coef,range(32),range(2))
                    factor=F(n,6);cells+=checked
                    for s,x in alpha.items():a[mi[h,w,s]]+=factor*x
                    b[h]+=factor*beta[0]
                    ss=own[h,1,1,bits(w,3),bits(w,3)]
                    for j in (ss[1,0],ss[1,1]):b[j]+=factor*(beta[1]-beta[0])
                    pieces.append(dict(hist=h,root_old_word=w,factor=factor,
                        alpha=[alpha[s] for s in range(32)],beta=[beta[r] for r in range(2)],
                        R_old_columns=[ss[1,0],ss[1,1]],coefficient_cells=checked,minimum_dominance_gap=gap))
        a={j:v for j,v in a.items() if v};b={j:v for j,v in b.items() if v}
        value=sum((x*F(m.mu_cert['mu'][j]) for j,x in a.items()),F())+sum((x*F(oldcols[j]['weight']) for j,x in b.items()),F())
        assert value==F(frozen['upper'])<0
        rows.append(dict(name=['full32-upper',name],source_query=name,positive_slack_inequality='old dot x + mu dot mu >= 0',
            old=[[j,v] for j,v in sorted(b.items())],mu=[[j,v] for j,v in sorted(a.items())],
            old_nonzero_coefficients=len(b),mu_nonzero_coefficients=len(a),
            current_mu_value=value,current_mu_approx=float(value),full_domain_dominance_cells=cells,pieces=pieces))
    report=dict(status='TWO_FULL_32_STATE_NECESSARY_ROWS_EXACT',point_sha256=PINS[POINT],mu_sha256=PINS[MU],
        source_bounds_sha256=sha(here/'fixed_mu_upper_bounds_exact.json'),script_sha256=sha(Path(__file__)),
        old_columns=len(oldcols),mu_columns=mus,rows=rows,
        total_full_domain_dominance_cells=sum(r['full_domain_dominance_cells'] for r in rows),
        mathematical_scope='For the fixed 16 hist identities but arbitrary nonnegative old masses and all 32-state root marginals having the correct group mass. Every genuine common law satisfying the source query obeys the displayed linear upper row. No claim of sufficiency or elimination of mu.',
        construction='Keep dual potentials on current positive supports; extend missing left states by max over retained right potentials, then missing right states by max over all left. Zero-mass hist fibers are also filled and checked on the complete domain.',
        no_original_point_exclusion=True,elapsed_seconds=time.monotonic()-started)
    dump('full32_obstruction_rows_exact.json',report)
    print(json.dumps(serial(dict(rows=[{k:r[k] for k in ('source_query','current_mu_value','current_mu_approx','old_nonzero_coefficients','mu_nonzero_coefficients','full_domain_dominance_cells')} for r in rows],
        total_cells=report['total_full_domain_dominance_cells'],elapsed_seconds=report['elapsed_seconds'])),ensure_ascii=False))


if __name__=='__main__':main()
