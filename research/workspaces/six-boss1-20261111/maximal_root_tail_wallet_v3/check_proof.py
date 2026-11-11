#!/usr/bin/env python3
"""Exact transcription audit for the published point, budget and two scales."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,re
H=Path(__file__).resolve().parent
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
    c=json.loads((H/'exact_certificate.json').read_text());i=json.loads((H/'exact_input.json').read_text());proof=(H/'proof.md').read_text()
    pointrows=re.findall(r'^\| (\d+) \| ([01]{7}) \| (\d+) \|$',proof,re.M)
    assert len(pointrows)==10
    for j,bits,n in pointrows:
        assert bits==''.join(map(str,i['atoms'][int(j)]['bits']))
        assert n==c['integer_primal'][j]
    assert c['primal_common_denominator'] in proof
    assert 'u='+c['integer_primal']['128']+'/E' in proof
    names={
       'ROOT_IC':'ROOT_IC','CAP_B2':'CAP_B2','CAP_B3':'CAP_B3','CAP_B4':'CAP_B4','CAP_B5':'CAP_B5','CAP_B6':'CAP_B6',
       'SAFE_j6(Omean)':'SAFE_j6|Omean','PAIR30(Omean,Omean)':'PAIR30|Omean|Omean',
       'C30原126000尺度':'OPT_SOURCE3_REQUERY_30_CUT','P25_i4(T=B6,Q=Omean)原25尺度':'PORTFOLIO25_i4|T=B6|Q=Omean'}
    parsed={}
    for label,n in re.findall(r'^\| (.+) \| (\d+) \|$',proof,re.M):
        if label in names:parsed[names[label]]=n
    assert parsed==c['dual']['integer_original_row_weights']
    line=c['universal_root_line']['integer_line'];budget=int(c['dual']['common_budget_denominator'])
    assert budget==4*int(line['u'])
    pi=list(map(int,c['dual']['integer_equality_multipliers']));cap=sum(int(v) for n,v in parsed.items() if n.startswith('CAP'))
    p25=F(parsed['PORTFOLIO25_i4|T=B6|Q=Omean']);p25_K=F(3,2)*p25
    assert pi[0]-cap-p25_K==4*int(line['K']) and pi[1]==4*int(line['O'])
    for n in [str(budget),str(pi[0]),str(pi[1]),str(cap),str(p25_K),str(4*int(line['K'])),str(4*int(line['O']))]:assert n in proof
    assert digest(H/'exact_input.json') in proof and digest(H/'exact_certificate.json') in proof
    zero=[j for j in range(128) if F(c['dual']['column_residuals'][str(j)])==0]
    assert '`'+', '.join(map(str,zero))+'`' in proof
    assert c['comparison_at_released_K']['root_gap_over_v6_u'].split('/')[0] in proof
    assert c['comparison_at_released_K']['root_gap_over_v6_u'].split('/')[1] in proof
    out={'status':'PASS_EXACT_PROOF_TABLES_AND_PARAMETER_BUDGET','proof_sha256':digest(H/'proof.md'),
         'input_sha256':digest(H/'exact_input.json'),'certificate_sha256':digest(H/'exact_certificate.json'),
         'primal_table_rows':10,'integer_budget_table_rows':10,'budget_scale_over_primitive_line':4,
         'five_CAP_integer_weight_sum':str(cap),'P25_independent_K_payment':str(p25_K),
         'free_equality_multipliers':list(map(str,pi)),'root_line_integer_coefficients':line,
         'zero_atom_residuals':zero,'optimizer_calls':0}
    (H/'proof_transcription_check.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
