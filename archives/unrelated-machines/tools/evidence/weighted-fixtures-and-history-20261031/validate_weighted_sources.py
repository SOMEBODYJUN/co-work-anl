#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).parent

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

# Weighted fanout star profile: exact row sums and explicit profile fields.
d=json.loads((ROOT/'weighted_fanout_profile_star.json').read_text())
assert len(d['p'])==6 and all(len(r)==4 for r in d['p'])
assert d['S1']==[0,0,0,0] and d['S2']==[1,2,3,4] and d['T']=='7/3' and d['a']==0
assert d['outputs']==[1,2,3,4,5] and d['missing_subset']==[1,2,3,4]
T=F(d['T']); row_sums=[]
for r in d['p']:
    vals=[]
    for x in r:
        if x is not None:
            assert isinstance(x,str); vals.append(F(x)); assert F(x)>=0
    row_sums.append(sum(vals,F(0)))
assert row_sums[:5]==[T]*5 and row_sums[5]==0
betas=[F(x) for x in d['beta']]; assert betas==[F(1,10),F(1,5),F(3,10),F(2,5)]
fanout_check={'rows':6,'columns':4,'nonzero_rows':5,'T':'7/3','row_sums':[str(x) for x in row_sums],'betas':[str(x) for x in betas],'bounds':[str((F(2)-b)*T) for b in betas]}

# Weighted menu fixtures: preserve state identity and validate exact nonnegative incidences.
d=json.loads((ROOT/'weighted_menu_joint_fixtures.json').read_text())
assert list(d)==['joint_bad_heavy_yes','near_two_single_state_no','zero_work_empty_and_duplicate_states','rational_unequal_menus_and_bonuses','aux_opt_zero_fallback']
menu_counts={}; state_sums={}
for case,c in d.items():
    assert len(c['resources'])==len(set(c['resources']))
    gids=[g['id'] for g in c['groups']]; assert len(gids)==len(set(gids))
    for g in c['groups']:
        sids=[s['id'] for s in g['states']]; assert len(sids)==len(set(sids))
        for s in g['states']:
            rs=[i['resource'] for i in s['incidences']]; assert len(rs)==len(set(rs))
            total=F(0)
            for inc in s['incidences']:
                assert inc['resource'] in c['resources']
                q=F(inc['p']); assert q>=0; total+=q
            state_sums[f'{case}:{g["id"]}:{s["id"]}']=str(total)
    menu_counts[case]={'resources':len(c['resources']),'groups':len(c['groups']),'states':sum(len(g['states']) for g in c['groups'])}
assert state_sums['joint_bad_heavy_yes:g0:heavy']=='1'
assert state_sums['joint_bad_heavy_yes:g0:diffuse']=='1'
assert state_sums['zero_work_empty_and_duplicate_states:g0:empty']=='0'
assert state_sums['zero_work_empty_and_duplicate_states:g0:zero']=='0'
menu_check={'cases':menu_counts,'state_sums':state_sums,'finite_audit_reference':'existing degree-two-menu-joint source independently enumerates 832 original assignments; this script validates the raw fixture structure only'}

# History README is an operations/resource document, not a mathematical claim.
h=(ROOT/'history_README.md').read_text()
required=['历史与可追溯来源','source/manuscripts','source/notes','source/audits','proofs','searches','现行研究','迁移表','不充当现行定理的唯一入口']
for x in required: assert x in h, x
history_check={'bytes':len(h.encode()),'required_markers':required,'classification':'historical operations/resource index; no mathematical theorem inferred'}

manifest={
 'batch':'weighted-fixtures-and-history-20261031',
 'source_commits':['68fad804ec5946cb296f77dc5b336308a66abf12','aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c'],
 'source_ids':{'weighted_fanout_profile_star':'0c3bf6d24f1ba76ead00','weighted_menu_joint_fixtures':'b88c0af63e1cab4774d1','history_README':'56adacf9717c2c0b7539'},
 'source_sha256':{p.name:sha(p) for p in ROOT.glob('*') if p.name not in {'validation.json','validate_weighted_sources.py'}},
 'checks':{'weighted_fanout_profile_star':fanout_check,'weighted_menu_joint_fixtures':menu_check,'history_README':history_check},
 'scope':'exact source preservation and structural/Fraction checks; finite fixture and historical index only'
}
(ROOT/'validation.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
