from pathlib import Path
from fractions import Fraction
import argparse,hashlib,json,sys

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--point',type=Path,required=True);ap.add_argument('--reference',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    if a.out.exists(): raise RuntimeError('Unique output already exists; this once-only check must not overwrite or rerun.')
    pb=a.point.read_bytes();rb=a.reference.read_bytes();obj=json.loads(pb);ref=json.loads(rb)
    known={int(k):Fraction(v) for k,v in ref['published_verified_weights'].items()}
    reported_weights={z['mask']:Fraction(z['weight']) for z in obj['customer_weights']}
    assert len(obj['customer_weights'])==len(reported_weights)==len(known)==11
    assert reported_weights==known and all(v>0 for v in known.values())
    results=[]
    for i,z in enumerate(obj['y']):
        q=z['q'];label=z['a'];expected=sum((w/Fraction(sum(q[b] for b in range(6) if mask>>b&1)) for mask,w in known.items() if mask>>label&1),Fraction(0))
        value=Fraction(z['value']);results.append({'index':i,'q':q,'a':label,'reported_original':z['value'],'expected_from_published11weights':str(expected),'equal':value==expected,'difference':str(value-expected)})
    mismatch=[z for z in results if not z['equal']]
    report={'scope':'exact cross-field alignment of this new output y table with known published11weights; not an SPE, IC, dilution, LP, dual or optimum audit','point_sha256':hashlib.sha256(pb).hexdigest(),'reference_sha256':hashlib.sha256(rb).hexdigest(),'published_carrier_sha256':ref['published_carrier_sha256'],'weights_match_known_point':True,'entries':len(results),'all_exactly_equal':not mismatch,'mismatches':mismatch,'all126_entry_results':results,'original_program_import_or_entry_calls':0,'python':sys.version,'optimize':sys.flags.optimize}
    a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'entries':len(results),'weights_match':True,'all_exactly_equal':not mismatch,'mismatch_count':len(mismatch),'result_sha256':hashlib.sha256(a.out.read_bytes()).hexdigest()},ensure_ascii=False))
    if mismatch: raise SystemExit(1)
if __name__=='__main__': main()
