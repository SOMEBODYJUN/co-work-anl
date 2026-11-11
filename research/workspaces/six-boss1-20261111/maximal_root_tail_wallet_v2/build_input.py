#!/usr/bin/env python3
"""Copy the original71 EXACT rows; append only the released all128 cut."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib

H=Path(__file__).resolve().parent;WS=H.parent;ROOT=WS.parents[2]
KNEW=F(1125421575458286230366665,6570307807568935468436467)
OLD_INPUT='3c1a824ed0a17562da812db1d0bb12485f0b1c7f743577af7bc2ecf316d3ab65'
CUT_CERT='209959db4dfce6ba4fe796eeb168b8ab71f186f795e0599f9148d08ceaa8b13e'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(H/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def main():
    olddir=WS/'maximal_root_tail_wallet';cutdir=WS/'maximal_root_opt_requery'
    assert sha(olddir/'exact_input.json')==OLD_INPUT and sha(cutdir/'exact_certificate.json')==CUT_CERT
    old=json.loads((olddir/'exact_input.json').read_text());cutcert=json.loads((cutdir/'exact_certificate.json').read_text())
    maincheck=json.loads((WS/'main_opt_requery_cut_check.json').read_text())
    assert maincheck['status']=='PASS_LITERAL_2048_STATES_128_ENVELOPES_AND_ACTUAL_HISTORY_MAP' and maincheck['certificate_sha256']==CUT_CERT
    cut=cutcert['universal_cut'];assert F(cut['cut_K'])==F(cut['cut_u'])==0 and len(cut['cut_z'])==128
    frozen={}
    for directory in (olddir,cutdir):
        for p in sorted(directory.rglob('*')):
            if p.is_file():frozen[str(p.relative_to(ROOT))]=sha(p)
    for rel in ['research/workspaces/six-boss1-20261111/maximal_root_tail_wallet.md','research/workspaces/six-boss1-20261111/maximal_root_opt_requery.md',
                'research/workspaces/six-boss1-20261111/main_opt_requery_cut_check.json','archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md']:
        frozen[rel]=sha(ROOT/rel)
    save('frozen_sources_before.json',frozen)
    rows=json.loads(json.dumps(old['raw_rows']))
    for row in rows:
        row['rhs']=str(F(row['bK'])*KNEW+F(row['bO']));row['numerical_divisor']='1'
    new={'name':'OPT_SOURCE3_REQUERY_CUT','family':'REQUERY_CUT','a':{j:v for j,v in cut['cut_z'].items() if F(v)},
         'bK':str(-F(cut['cut_K'])),'bO':'0','rhs':'0','numerical_divisor':'126000',
         'source_cut_u':cut['cut_u'],'source_cut_K':cut['cut_K'],'source_certificate_sha256':CUT_CERT}
    if F(cut['cut_u']):new['a']['128']=cut['cut_u']
    rows.append(new)
    eq=json.loads(json.dumps(old['equalities']));eq[0]['rhs']=str(KNEW);eq[1]['rhs']='1'
    result={'scope':'Original all128 root71 necessary system plus one universal optimal-menu requery cut; original unscaled rows retained.',
            'bit_order':old['bit_order'],'atoms':old['atoms'],'root_u_column':128,'nonnegative_columns':list(range(129)),
            'fixed_K':str(KNEW),'fixed_O':'1','objective':{'128':'1'},'convention':old['convention'],
            'raw_rows':rows,'equalities':eq,'old_input_sha256':OLD_INPUT,'cut_certificate_sha256':CUT_CERT,
            'source_review_sha256':sha(H/'source_review.md'),'source_manifest_sha256':sha(H/'frozen_sources_before.json'),
            'numeric_scaling':'Only solver divides each original GE row by its recorded positive numerical_divisor; exact input and checks remain unscaled.'}
    assert len(rows)==72
    save('exact_input.json',result)
    mapping={'root_columns_unchanged':True,'root_atom_columns':128,'root_u_column':128,
             'cut_K_coefficient':cut['cut_K'],'cut_u_coefficient':cut['cut_u'],
             'actual256_map_informational_only':[{'global_index':4*a+2*x+o,'root128_index':2*a+o} for a in range(64) for x in (0,1) for o in (0,1)],
             'actual_joint_rows_added_here':False}
    save('column_mapping.json',mapping)
    summary={'columns':129,'raw_rows':72,'equalities':2,'original_raw_rows_preserved':71,'new_cut_rows':1,
             'fixed_K':str(KNEW),'fixed_O':'1','appended_row_numerical_divisor':'126000',
             'input_sha256':sha(H/'exact_input.json'),'optimizer_calls':0,'old_sources_frozen':len(frozen)}
    save('build_summary.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
