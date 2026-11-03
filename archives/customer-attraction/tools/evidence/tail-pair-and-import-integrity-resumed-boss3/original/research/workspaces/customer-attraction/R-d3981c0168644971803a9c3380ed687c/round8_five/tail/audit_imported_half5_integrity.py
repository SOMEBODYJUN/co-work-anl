"""Independent source/metadata/K-column audit; optional unmodified copy replay.
Does not import either proof verifier. Never writes in the frozen package.
"""
from pathlib import Path
from fractions import Fraction
import argparse,hashlib,json,re,shutil,subprocess,sys,tempfile,zipfile

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/proofs/half5_exact_v1').is_dir())
PACKAGE=ROOT/'customer_attraction/proofs/half5_exact_v1'
ARCHIVE=ROOT/'history/source/notes/customer_attraction/half5_exact_upload.zip'
EXPECTED_ZIP='290133028779a9c1d1d7a2f09b3300049c2b796d8ea65115eb0107808e6c6b64'
EXPECTED_CERT='395e056b218d237abe8b85db894f0b1c37d2e14d55c74b1dca723abeceb6a44e'
sha=lambda b:hashlib.sha256(b).hexdigest()
def exact_int(v):
    assert isinstance(v,int) and not isinstance(v,bool) or isinstance(v,str) and re.fullmatch(r'-?\d+',v)
    return int(v)
def exact_fraction(v):
    assert isinstance(v,(str,int)) and not isinstance(v,bool)
    return Fraction(v)
def fingerprint():return {str(p.relative_to(PACKAGE)):sha(p.read_bytes()) for p in PACKAGE.rglob('*') if p.is_file()}
def run(replay=False):
    before=fingerprint();manifest=json.loads((PACKAGE/'MANIFEST.json').read_bytes())
    details=[]
    for rel,rec in manifest['files'].items():
        b=(PACKAGE/rel).read_bytes()
        assert len(b)==rec['bytes'] and sha(b)==rec['sha256'],rel
        details.append({'path':rel,'bytes':len(b),'sha256':sha(b)})
    assert sha(ARCHIVE.read_bytes())==EXPECTED_ZIP
    with zipfile.ZipFile(ARCHIVE) as z:
        prefix='Q-CAG-HALF-5-proof/'
        archived={n.removeprefix(prefix):z.read(n) for n in z.namelist() if not n.endswith('/')}
        assert set(archived)==set(manifest['files'])|{'MANIFEST.json'}
        assert all(data==(PACKAGE/rel).read_bytes() for rel,data in archived.items())
    cert_b=(PACKAGE/'certificate.json').read_bytes();assert sha(cert_b)==EXPECTED_CERT
    cert=json.loads(cert_b);D=exact_int(cert['common_denominator']);B=exact_int(cert['beta_numerator'])
    weights={k:exact_int(v) for k,v in cert['integer_multipliers'].items()}
    assert D==10**22 and B==2*D and len(weights)==53 and min(weights.values())>0
    cols=json.loads((PACKAGE/'active_k_columns.json').read_bytes())
    assert cols['certificate_sha256']==EXPECTED_CERT
    k={a:exact_int(v) for a,v in cols['row_K_coefficients'].items()}
    assert set(k)==set(weights)
    terms={a:weights[a]*k[a] for a in weights}
    total=sum(terms.values())
    assert total==-2264870 and total==exact_int(cols['weighted_sum']) and -total==exact_int(cols['K_residual'])
    local=[];total_local_weights=0
    for path in sorted((PACKAGE/'components').glob('*.json')):
        if path.name=='local_check_report.json':continue
        source=json.loads(path.read_bytes());entries=source if isinstance(source,list) else [source]
        for i,c in enumerate(entries):
            field='multipliers' if 'multipliers' in c else 'weights'
            assert isinstance(c[field],dict) and c[field]
            vals=[exact_fraction(v) for v in c[field].values()]
            assert min(vals)>=0,(path.name,i)
            local.append({'file':path.name,'index':i,'field':field,'count':len(vals),'minimum':str(min(vals))})
            total_local_weights+=len(vals)
    proof=(PACKAGE/'PROOF_ZH.md').read_text()
    appendix=dict(re.findall(r'\| `([^`]+)` \| (\d+) \|',proof))
    assert all(int(appendix[a])==v for a,v in weights.items())
    out={'scope':'Source-byte integrity, exact multiplier signs and independent scalar K arithmetic; not a second main-domain implementation',
         'status':'passed','archive_sha256':EXPECTED_ZIP,'archive_members_exactly_equal_package':len(archived),
         'manifest_sha256':sha((PACKAGE/'MANIFEST.json').read_bytes()),'manifest_entries_passed':len(details),
         'certificate_sha256':EXPECTED_CERT,'main_positive_multipliers':len(weights),'main_denominator':str(D),
         'exact_beta':str(Fraction(B,D)),'appendix_53_weights_match':True,
         'local_component_records':len(local),'local_nonnegative_multiplier_values':total_local_weights,
         'K_weighted_sum':str(total),'K_residual':str(-total),'K_residual_times_120':str(-120*total),
         'nonzero_K_products':{a:str(v) for a,v in terms.items() if v},'local_multiplier_checks':local,
         'file_integrity':details}
    if replay:
        # Copy to fresh scratch; neither script nor data is altered.
        scratch=Path(tempfile.mkdtemp(prefix='half5_tail_scope_',dir='/workspace/scratch/4df200643a53'))
        copy=scratch/'proof';shutil.copytree(PACKAGE,copy)
        assert all((copy/rel).read_bytes()==(PACKAGE/rel).read_bytes() for rel in archived)
        local_run=subprocess.run([sys.executable,str(copy/'components/verify_local_components.py')],cwd=copy,capture_output=True,text=True,check=True)
        loc=json.loads(local_run.stdout);assert loc['component_count']==36 and loc['coefficient_states']==47872
        (HERE/'imported_half5_local_replay.json').write_text(json.dumps(loc,indent=2,ensure_ascii=False)+'\n')
        main_out=HERE/'imported_half5_main_replay.json'
        main_run=subprocess.run([sys.executable,str(copy/'verify_certificate.py'),'--manifest',str(copy/'row_manifest.json'),'--output',str(main_out)],cwd=copy,capture_output=True,text=True,check=True)
        main=json.loads(main_out.read_text())
        assert main['status']=='passed' and main['conditional_cases']==6144 and main['minimum_scaled_integer_residual']=='0' and main['K_column_residual']=='2264870' and main['negative_cases']==[]
        assert main['certificate_sha256']==EXPECTED_CERT
        out['unmodified_copy_replay']={'copy_root':str(copy),'python':sys.version.split()[0],
          'local_components':loc['component_count'],'local_coefficient_states':loc['coefficient_states'],
          'main_conditional_cases':main['conditional_cases'],'minimum_customer_residual':main['minimum_scaled_integer_residual'],
          'K_residual':main['K_column_residual'],'negative_cases':len(main['negative_cases']),
          'scope':'Both delivered scripts rerun; one delivered main-domain implementation, not two independent main implementations'}
    assert fingerprint()==before
    out['frozen_package_unchanged_after_audit']=True
    target=HERE/'imported_half5_integrity_audit.json'
    target.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({a:v for a,v in out.items() if a not in ('file_integrity','local_multiplier_checks','nonzero_K_products')},indent=2,ensure_ascii=False))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--replay-copy',action='store_true');args=parser.parse_args();run(args.replay_copy)
