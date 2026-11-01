from fractions import Fraction
from pathlib import Path
import json, hashlib

ROOT=Path(__file__).resolve().parents[1]
files=[ROOT/'audit/individual_candidate_audit.json',ROOT/'audit/extra_candidate_audit.json',ROOT/'audit/cyclic_candidate_audit.json']
allrows=[]
for f in files:
    raw=f.read_bytes(); data=json.loads(raw)
    assert isinstance(data,list) and data
    allrows.extend(data)
    for row in data:
        assert row['full_history_SPE'] is True and row['violations']==[]
        assert row['minimum_slack']=='0'
        assert row['half_gap']==2*row['welfare']-row['optimum']
        assert row['decision_histories']==sum(row['topics']**d for d in range(row['players']))
        assert row['proper_deviation_comparisons']==row['decision_histories']*(row['topics']-1)
        assert Fraction(row['minimum_weak_individual_gap']) == (2*row['players']-1)*min(Fraction(x) for x in row['actual_payoffs'])-row['optimum']
        assert row['welfare']>=0 and row['optimum']>=row['welfare']
# expected named outcomes
by={Path(r['source']).name:r for r in allrows}
assert by['cyclic_m3p7_individual.json']['welfare']==11 and by['cyclic_m3p7_individual.json']['optimum']==13
assert by['cyclic_m5p7_half.json']['welfare']==7 and by['cyclic_m5p7_half.json']['optimum']==7
assert by['m4p5_11110_a0.json']['welfare']==19 and by['m4p5_11110_a0.json']['optimum']==19
assert max(r['optimum']-2*r['welfare'] for r in allrows) <= 0
out={'files':[{"path":str(f.relative_to(ROOT)),"sha256":hashlib.sha256(f.read_bytes()).hexdigest()} for f in files], 'rows':len(allrows), 'all_full_history_SPE':True, 'all_half_inequality_satisfied':True, 'max_OPT_minus_2W':max(r['optimum']-2*r['welfare'] for r in allrows), 'cyclic_m3p7_ratio':str(Fraction(by['cyclic_m3p7_individual.json']['optimum'],1)/Fraction(by['cyclic_m3p7_individual.json']['actual_payoffs'][0])), 'status':'pass'}
print(json.dumps(out,indent=2))
