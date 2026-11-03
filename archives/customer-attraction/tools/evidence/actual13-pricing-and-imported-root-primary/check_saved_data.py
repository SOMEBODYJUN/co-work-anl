"""Read all saved records and compare identities; do not execute old mathematics.

No original imports, row reconstruction, LP, oracle, SPE or coefficient-domain
scan. Fraction arithmetic below only consumes saved coordinates and row values.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter, defaultdict
import argparse, ast, gzip, hashlib, json, math, re

HERE = Path(__file__).resolve().parent
PREFIX = 'research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round8_five/'

def digest(b): return hashlib.sha256(b).hexdigest()
def consume(v):
    if isinstance(v, dict): return 1 + sum(consume(k)+consume(x) for k,x in v.items())
    if isinstance(v, list): return 1 + sum(map(consume,v))
    if isinstance(v, float): assert math.isfinite(v)
    assert isinstance(v,(str,int,float,bool,type(None)))
    return 1

def atom(a):
    assert len(a['bits'])==10 and set(a['bits']) <= {'0','1'}
    assert len(a['max_bits'])==5 and set(a['max_bits']) <= {'0','1'}
    ds=[]
    for name,k in [('AB_hist',3),('AE_hist',3),('second_hist',4)]:
        h=a[name];assert len(h)==2**k and all(type(v) is int and v>=0 for v in h) and sum(h)==5
        ds.append(sum(h[2**(k-1):]))
    assert len(set(ds))==1
    for l,h in a['menus_lh']: assert 0<=h<=ds[0] and 0<=l-h<=5-ds[0]
    if 'exact_mass' in a: assert F(a['exact_mass'])>=0
    if 'actual_HQR_bits' in a: assert len(a['actual_HQR_bits'])==3 and set(a['actual_HQR_bits'])<={'0','1'}
    return ds[0]

def coord(a): return json.dumps({k:v for k,v in a.items() if k not in ('exact_mass','actual_HQR_bits')},sort_keys=True,separators=(',',':'))
def totals(atoms):
    return { 'W':str(sum((F(a['exact_mass'])*int('1' in a['bits'][:5]) for a in atoms),F(0))),
             'O':str(sum((F(a['exact_mass'])*int(any(a['AB_hist'][4:])) for a in atoms),F(0))),
             'K':str(sum((F(a['exact_mass'])*int(a['max_bits'][0]) for a in atoms),F(0))) }

def run(repo):
    manifest=json.loads((HERE/'source-manifest.json').read_text());primary={};texts={};syntax=0;nodes={}
    tree=HERE.parents[4]
    for r in manifest:
        b=(tree/r['preserved_path']).read_bytes()
        assert len(b)==r['size'] and digest(b)==r['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob']
        sh=json.loads((HERE/r['read_after_receipt']).read_text())['source']
        assert (sh['id'],sh['sha256'],sh['blob'],sh['size'])==(r['id'],r['sha256'],r['blob'],r['size'])
        name=Path(r['path']).name
        if name.endswith('.json'):
            primary[name]=json.loads(b);nodes[name]=consume(primary[name])
        elif name.endswith('.py'): ast.parse(b);syntax+=1
        elif name.endswith('.md'):texts[name]=b.decode()
    deps=json.loads((HERE/'reused-dependencies.json').read_text());related={}
    for r in deps:
        b=(repo/r['path']).read_bytes();assert len(b)==r['size'] and digest(b)==r['sha256']
        if r['path'].endswith('.gz'):
            b=gzip.decompress(b);assert len(b)==r['uncompressed_size'] and digest(b)==r['uncompressed_sha256']
        if r['path'].endswith(('.json','.json.gz')):
            related[Path(r['path']).name.removesuffix('.gz')]=json.loads(b)
            consume(related[Path(r['path']).name.removesuffix('.gz')])
        elif r['path'].endswith('.py'):ast.parse(b)
    discovery=primary['actual13_payment_discovery.json'];old=related['trueH_own_index_discovery.json']
    assert discovery['atoms']==old['atoms'] and discovery['row_names']==old['row_names']+['Actual13TrueHQRProjection']
    assert len(discovery['atoms'])==len(discovery['primal_float'])==849 and len(set(discovery['row_names']))==6751
    assert set(discovery['dual_multipliers_float'])<=set(discovery['row_names'])
    assert all(v>=0 for v in discovery['dual_multipliers_float'].values())
    assert discovery['code_sha256']==next(r['sha256'] for r in manifest if r['path'].endswith('/actual13_payment_pricing.py'))
    for a in discovery['atoms']:atom(a)
    positive=[i for i,v in enumerate(discovery['primal_float']) if v>1e-8];assert len(positive)==63
    assert sum(v==0 for v in discovery['primal_float'])==786
    exact=related['exact_current_source_actual13_v1.json']
    assert exact['source_sha256']==next(r['sha256'] for r in manifest if r['path'].endswith('/actual13_payment_discovery.json'))
    for a in exact['atoms']:atom(a)
    assert Counter(coord(a) for a in exact['atoms'])==Counter(coord(discovery['atoms'][i]) for i in positive)
    float_W=sum(w*int('1' in a['bits'][:5]) for a,w in zip(discovery['atoms'],discovery['primal_float']))
    float_O=sum(w*int(any(a['AB_hist'][4:])) for a,w in zip(discovery['atoms'],discovery['primal_float']))
    binary=primary['new_binary_four_tail_payment_check.json'];cert=related['binary_four_tail_uncorrected_certificate.json']
    floors=related['reconciliation.json']['residual_floors']
    assert binary['source_sha256']==next(r['sha256'] for r in deps if r['path'].endswith('/exact_current_source_actual13_v1.json'))
    assert binary['binary_certificate_sha256']==next(r['sha256'] for r in deps if r['path'].endswith('/binary_four_tail_uncorrected_certificate.json'))
    assert F(binary['beta'])==F(cert['beta'])
    for r in floors:
        for p in (0,1):assert F(binary['own_new_RHOMIN'][f"{p}:{r['actual_bits']}"])==F(r[f'uncorrected_p{p}'])
    assert len(binary['own_new_RHOMIN'])==32 and binary['checked_rows']==17546 and binary['negative_count']==0 and binary['negative_rows']==[]
    for r in binary['cases']:
        assert r['checked_rows']==8773 and F(r['minimum_row']['exact_slack_with_NEW_RHOMIN'])>0
        assert F(r['minimum_row']['exact_uncorrected_slack_without_rho'])>0 and F(r['new_rho_payment'])>=0
    local=primary['imported_maxroot_independent_recheck.json'];mc=related['maxroot_four_copy.json']
    assert local['source_sha256']==next(r['sha256'] for r in deps if r['path'].endswith('/components/maxroot_four_copy.json'))
    text=(repo/'archives/customer-attraction/state/引理/五人最大主题根界--引理.md').read_text()
    tables={m.group(1):(m.group(2),m.group(3)) for m in re.finditer(r'\| `([01]{5})` \| (\d+) \| (\d+) \|',text)}
    assert len(tables)==32
    mature=[r for r in related['local.json']['checks'] if r['family']=='MAXROOT']
    for i,(a,b,m) in enumerate(zip(local['certificates'],mc,mature)):
        assert F(a['B'])==F(b['B']) and F(a['signed_C'])==F(b['C'])
        assert len(b['multipliers'])==22 and all(F(v)>0 for v in b['multipliers'].values())
        assert a['membership_states']==m['types']==1024 and a['coverage_bit_states_checked']==2048
        assert a['zero_membership_states']==m['zero_residuals']==56 and a['minimum_residual']=='0'
        assert a['scaled_prefix_minima']=={p:v[i] for p,v in tables.items()}
    sep=primary['old_point_imported_row_separation.json'];point=related['exact_full_actual_extension_known_v1.json']
    assert sep['source_sha256']==next(r['uncompressed_sha256'] for r in deps if r['path'].endswith('/exact_full_actual_extension_known_v1.json.gz'))
    assert sep['proof_certificate_sha256']==next(r['sha256'] for r in deps if r['path'].endswith('/half5-exact/certificate.json'))
    assert len(point['atoms'])==64 and len(point['actual_HQR_lift'])==85 and len(point['row_slacks'])==7497
    for a in point['atoms']+point['actual_HQR_lift']:atom(a)
    assert all(F(v)>=0 for v in point['row_slacks'].values())
    projected=defaultdict(F)
    for a in point['actual_HQR_lift']: projected[coord(a)]+=F(a['exact_mass'])
    assert dict(projected)=={coord(a):F(a['exact_mass']) for a in point['atoms']}
    tt=totals(point['atoms']);assert tt=={k:sep[k] for k in ('W','O','K')}
    assert set(sep['all_53_slacks'])==set(related['certificate.json']['integer_multipliers'])
    negatives={n:v for n,v in sep['all_53_slacks'].items() if F(v)<0};assert negatives==sep['negative_rows'] and len(negatives)==13
    assert primary['actual13_decomposition_audit.json']['checks']==65664
    wallet={}
    for m in re.finditer(r'\| ([01]{4}) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|',texts['actual_payment.md']):
        for i,(a1,c) in enumerate([(0,0),(0,1),(1,0),(1,1)]):wallet[(str(a1)+m.group(1),c)]=F(m.group(i+2).strip())
    mature_wallet=(repo/'archives/customer-attraction/state/引理/五人实际并集钱包的真实前缀付款--引理.md').read_text()
    wallet2={}
    for m in re.finditer(r'\|([01]{5})\|([^|]+)\|([^|]+)\|',mature_wallet):
        for c in (0,1):wallet2[(m.group(1),c)]=F(m.group(c+2))
    assert len(wallet)==len(wallet2)==64 and wallet==wallet2
    out={'status':'passed','scope':'saved bytes, full fields, data arithmetic and report identity only; no reconstructed old row or mathematical domain scan',
        'primary_sources':len(manifest),'primary_bytes':sum(r['size'] for r in manifest),'primary_python_AST':syntax,'json_nodes_consumed':nodes,'reused_dependencies':len(deps),'saved_wallet_64_entries_equal_formal_proof':True,
        'discovery':{'rows':6751,'columns':849,'row_family_counts':dict(Counter(n.split(':')[0] for n in discovery['row_names'])),'dual_support':len(discovery['dual_multipliers_float']),
            'current_primal_positive':63,'atoms_byte_fields_equal_previous_849_pool':True,'exact_mass_is_inherited_not_current_primal':True,
            'float_W':float_W,'float_O':float_O,'restricted_beta':discovery['dual_beta_float'],'minimum_slack_float':discovery['minimum_slack_float'],
            'positive_indices':positive,'exact_successor_same_coordinates':True,'exact_successor_totals':totals(exact['atoms'])},
        'binary_payment':{'saved_rows':17546,'cases':binary['cases'],'own_32_floors_equal_mature_uncorrected_table':True,'newly_evaluated_payment_rows':0},
        'maxroot':{'input_SHA_matches':True,'two_32_prefix_tables_equal_formal_lemma':True,'two_1024_56_records_equal_mature_local':True,'newly_evaluated_coefficient_states':0},
        'old_point':{'projected_atoms':64,'extended_atoms':85,'stored_old_row_slacks_consumed':7497,'stored_slack_minimum':str(min(map(F,point['row_slacks'].values()))),'totals':tt,
            'active_rows':53,'negative_rows':negatives,'negative_count':13,'active_sign_counts':dict(Counter('negative' if F(v)<0 else 'zero' if F(v)==0 else 'positive' for v in sep['all_53_slacks'].values())),
            'newly_evaluated_active_rows':0},
        'executions':{'original_programs':0,'new_mathematical_row_checks':0,'LP_oracle_SPE':0,'saved_data_check':1}}
    (HERE/'saved-data-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('json_nodes_consumed','discovery','binary_payment','old_point')},ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=HERE.parents[4]);args=p.parse_args();run(args.repo)
