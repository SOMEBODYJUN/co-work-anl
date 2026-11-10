#!/usr/bin/env python3
"""Exact retuned-v2 audit: m1/2/3, Boolean table and two tail constants.
No author modules or reports are imported; no m4..19 computation occurs.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import itertools
import json
import sys

sys.set_int_max_str_digits(0)
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_name('verification.json')
CERT = ROOT / 'archives/weighted-congestion/tools/evidence/crossover/original/evidence/certificates/weighted_congestion/crossover/limit_evidence/retuned_m3_certificate.json'
MASKS = ('0101','0112','1022','1100','1120','1122','1211')
T = tuple(Q(x) for x in ('49/100','11/10','49/100','3/5','1/50','3/100','1'))
STATES = tuple(''.join(x) for x in itertools.product('01',repeat=4))
WITNESS = dict(zip(STATES[:8], (2,2,3,0,3,2,3,1)))
WITNESS.update({''.join(str(1-int(b)) for b in s):i for s,i in list(WITNESS.items())})


def resources(m):
    w = (Q(1),Q(1,10*m),Q(1,20*m),Q(1,50*m))
    out = []
    for j,mask in enumerate(MASKS):
        support = [i for i,x in enumerate(mask) if x!='0']
        total = sum((w[i] for i in support),Q(0))
        for side in (0,1):
            required = {i:(int(mask[i])-1)^side for i in support}
            out.append((j,support,required,total,w))
    return out


def table(m=None):
    data = {}
    for s in STATES:
        costs = [Q(0)]*4
        for j,support,required,total,w in resources(1 if m is None else m):
            users = [i for i in support if int(s[i])==required[i]]
            if m is None:
                active = (len(users)==len(support)) if j<6 else (0 in users)
                fee = T[j] if active else Q(0)
            else:
                load = sum((w[i] for i in users),Q(0))
                fee = T[j]*(load/total)**(32*m*m if j<6 else 2)
            for i in users:costs[i]+=fee
        data[s]=tuple(costs)
    return data


def flips(data,s):
    return tuple(data[s[:i]+str(1-int(s[i]))+s[i+1:]][i] for i in range(4))


def analyze(data):
    maxima = {s:max(Q(1),*(data[s][i]/flips(data,s)[i] for i in range(4))) for s in STATES}
    best = min(maxima.values())
    return best,[s for s in STATES if maxima[s]==best],maxima


def main():
    raw=CERT.read_bytes(); cert=json.loads(raw)
    assert cert['m']==3 and cert['degree']==288
    assert tuple(map(Q,cert['coefficients_exact']))==T
    assert Q(cert['comparison_alpha_exact'])==2
    records=cert['records']; assert len(records)==16
    by_state={r['state']:r for r in records};assert set(by_state)==set(STATES)
    data=table(3);best,minimum,maxima=analyze(data)
    margins=[]; decimal_equal=True
    for s in STATES:
        r=by_state[s];old=data[s];new=flips(data,s);who=WITNESS[s]
        ratios=tuple(old[i]/new[i] for i in range(4));margin=old[who]-2*new[who]
        assert all(x>0 for x in old+new)
        assert tuple(map(Q,r['costs_exact']))==old
        assert tuple(map(Q,r['deviation_costs_exact']))==new
        assert tuple(map(Q,r['flip_ratios_exact']))==ratios
        assert r['template_witness_player_zero_based']==who
        assert Q(r['template_witness_alpha_margin_exact'])==margin
        assert r['template_witness_strict_alpha_margin_positive'] is (margin>0)
        assert margin>0
        decimal_equal &= r['max_flip_ratio_decimal_informational']==float(maxima[s])
        margins.append(margin)
    assert Q(cert['best_equilibrium_factor_exact'])==best
    assert cert['minimizing_states']==minimum==['0101','1010']
    assert Q(cert['minimum_template_witness_margin_exact'])==min(margins)
    assert cert['strict_alpha_obstruction_all_states'] is all(x>2 for x in maxima.values())
    assert cert['template_witnesses_strict_all_states'] is all(x>0 for x in margins)
    assert cert['all_current_and_deviation_costs_positive'] is True
    decimal_equal &= cert['best_equilibrium_factor_decimal_informational']==float(best)
    assert decimal_equal
    finite=[]
    for m in (1,2):
        dat=table(m);b,mins,mx=analyze(dat)
        assert b<2 and mins==['0100','1011']
        assert all(dat[s][i]<=2*flips(dat,s)[i] for s in ('0100','1011') for i in range(4))
        finite.append({'m':m,'degree':32*m*m,'states':16,'flips':64,
                       'B_decimal_informational':float(b),'minimizers':mins,
                       'B_lt_two_exact':True,'states_0100_1011_are_two_PNE_exact':True,
                       'all_four_0100_flip_ratios_exact':[str(dat['0100'][i]/flips(dat,'0100')[i]) for i in range(4)]})
    lim=table();b,mins,mx=analyze(lim)
    assert b==Q(100,49) and mins==['0100','0101','1010','1011']
    limit_margins=[lim[s][WITNESS[s]]-2*flips(lim,s)[WITNESS[s]] for s in STATES[:8]]
    assert limit_margins==list(map(Q,('24/25','51/50','9/20','7/50','1/50','1/50','7/50','19/100')))
    a,b0,c,d,e,f,g=T;h=d+e+f
    stated=[(d+g,a+d,g,a+g),(d+g,b0+d,b0+g,b0),
            (d+e+g,a+d+e,e,a+g),(c+h+g,h,c+e+f,c+f),
            (g,g,g,g),(g,a+g,g,a),(g,b0+g,b0,b0+g),(c+g,a+g,c,a+c)]
    assert [lim[s] for s in STATES[:8]]==stated
    assert all(lim[s]==lim[''.join(str(1-int(x)) for x in s)] for s in STATES)
    accessible=[sum((T[j] for j,mask in enumerate(MASKS[:6]) if mask[i]!='0'),Q(0)) for i in range(4)]
    assert accessible==list(map(Q,('57/50','56/25','41/25','211/100')))
    for s in STATES:
        i=WITNESS[s]
        assert (int(s[i])^(int(MASKS[6][i])-1))==(int(s[0])^(int(MASKS[6][0])-1))
    old=Q(1,50)-3*(Q(273,100)*Q(3,8)**28+Q(17,2600))
    new=Q(1,50)-Q(17,1000)-Q(289,2000000)-Q(112,25)*Q(3,8)**10
    assert old==Q(9671406313347824129679641,25145657047984286833888460800)>0
    assert new==Q(2735869393,1048576000000)>0
    assert Q(64*52,117)>28 and Q(64*20,117)>10
    report={'schema':1,'method':'resource-by-resource exact Fraction reconstruction; no author-code or report imports',
      'certificate':{'path':str(CERT.relative_to(ROOT)),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),
        'structurally_parsed':True,'manual_read_scope':'schema and field meanings; individual huge integer digits were not read as prose',
        'checked_exact_fields':{'current_costs':64,'deviation_costs':64,'flip_ratios':64,'template_margins':16,'best_factor':1,'minimum_margin':1,'amplitudes':7,'alpha':1},
        'checked_other_fields':'m, degree, states/coverage, 16 witness players, all strict/positivity booleans, minimizers, informational decimal displays',
        'all_checks_pass':True},
      'm3':{'resources':14,'states':16,'real_unilateral_flips':64,'B_decimal_informational':float(best),'B_gt_two_exact':True,'minimizers':minimum,
            'all_template_margins_positive_exact':True,'minimum_template_margin_decimal_informational':float(min(margins))},
      'm1_m2':finite,
      'limit':{'B_exact':str(b),'minimizers':mins,'all_16_states_64_flips_reconstructed':True,'eight_margin_exact':list(map(str,limit_margins)),
               'eight_cost_rows_exact':[list(map(str,lim[s])) for s in STATES[:8]],'eight_maximum_ratios_exact':[str(mx[s]) for s in STATES[:8]],'complement_symmetry_checked':True},
      'tails':{'accessible_first_six_amplitudes_exact':list(map(str,accessible)),
               'all_selected_current_seventh_resources_include_heavy_player':True,
               'v1_m52_absolute_margin_exact':str(old),'v2_m20_directed_margin_exact':str(new),
               'verified_exponent_rational_comparisons':{'64*52/117>28':True,'64*20/117>10':True},
               'infinite_scope_source':'monotonic analytic inequalities in reading-and-proof.md; finite computation alone does not prove tails'},
      'scope':'Core v2 only: m3 exact certificate; m1/2 two-PNE; M20 directed tail and separate M52 absolute tail constants; no m4..19 computation, endpoint claim, external review or full-ledger audit.'}
    OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'output':str(OUT.relative_to(ROOT)),'certificate_bytes':len(raw),'m3_all_exact_checks':True,
                      'm3_B_decimal':float(best),'m1_m2_two_PNE':True,'B_limit':str(b),'M52_margin':str(old),'M20_margin':str(new)},ensure_ascii=False))

if __name__=='__main__':main()
