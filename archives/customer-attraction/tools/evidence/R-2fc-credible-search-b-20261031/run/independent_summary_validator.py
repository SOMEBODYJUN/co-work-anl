#!/usr/bin/env python3
"""Independent arithmetic checks over the browser-read credible-search summaries.
No optimizer or customer-attraction implementation is imported.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'browser-read/summaries.json').read_text())
rows=[]
for x in data:
    m=x['milp']['players']; p=x['milp']['topics']
    # full ordered histories for depth m: sum_{d=0}^{m-1} p**d
    histories=sum(p**d for d in range(m))
    comparisons=histories*(p-1)
    e=x['exact_candidate']
    assert e['nodes']==histories,(x['file'],e['nodes'],histories)
    assert e['deviation_checks']==comparisons,(x['file'],e['deviation_checks'],comparisons)
    w=Fraction(e['welfare']); opt=Fraction(e['optimal_welfare']); u=Fraction(e['individual_payoff'])
    ratio=opt/u
    assert str(ratio)==e['actual_OPT_ratio'],(x['file'],ratio,e['actual_OPT_ratio'])
    half_gap=2*w-opt
    assert half_gap>=0,(x['file'],half_gap)
    weak_gap=(2*m-1)*u-opt
    assert str(weak_gap)==e['weak_individual_gap'],(x['file'],weak_gap,e['weak_individual_gap'])
    rows.append({'file':x['file'],'players':m,'topics':p,'histories':histories,'deviation_checks':comparisons,'welfare':str(w),'optimal_welfare':str(opt),'individual_payoff':str(u),'actual_OPT_ratio':str(ratio),'half_gap_2W_minus_OPT':str(half_gap),'weak_individual_gap':str(weak_gap),'milp_status':x['milp']['status'],'classification':x['classification']})
print(json.dumps({'passed':True,'count':len(rows),'rows':rows},ensure_ascii=False,indent=2))
