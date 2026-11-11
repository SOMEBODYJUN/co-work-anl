#!/usr/bin/env python3
"""Deterministically package an independently rebuilt neighbor-bridge report.

Existing packs are only compared byte-for-byte, never overwritten. The raw
capacity/ZZ reconstruction and its source-point binding remain authoritative.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,json,sys
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def full_sha(row,n):
    values=['0']*n
    for j,v in row:values[j]=str(F(v))
    return hashlib.sha256(json.dumps(values,separators=(',',':')).encode()).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('audit');ap.add_argument('output');ap.add_argument('verification')
    args=ap.parse_args()
    audit=Path(args.audit).resolve();output=Path(args.output).resolve();verification=Path(args.verification).resolve()
    assert all(p.is_relative_to(HERE) for p in (audit,output,verification))
    report=json.loads(audit.read_text());assert report['status']=='PASS'
    point_path=REPO/report['point_path'];assert sha(point_path)==report['point_sha256']
    point=json.loads(point_path.read_text());x=[F(c['weight']) for c in point['columns']]
    assert len(x)==4849
    cap=report['capacity_bridge']
    first={k:v for k,v in cap.items() if k not in ('table','slack_display')}
    first.update({'family':'early-capacity-H0','normalization_scale':'1',
                  'original_row_sha256':cap['row_sha256'],
                  'original_exact_slack':cap['exact_slack'],
                  'literal_case_table_source':audit.name+':capacity_bridge.table'})
    cuts=[first]
    for old in report['zz_classes']:
        if F(old['exact_slack'])>=0:continue
        count=old['literal_pairs'];assert count>0
        scale=F(1,count)
        row=[[j,str(F(v)*scale)] for j,v in old['sparse_row']]
        value=F(old['exact_slack'])*scale
        cuts.append({'family':'ZZ-Frechet','class':old['class'],
                     'literal_pairs':count,'normalization_scale':str(scale),
                     'original_row_sha256':old['row_sha256'],
                     'original_exact_slack':old['exact_slack'],
                     'sparse_row':row,'row_sha256':full_sha(row,len(x)),
                     'exact_slack':str(value),'slack_display':float(value)})
    assert len(set(c['row_sha256'] for c in cuts))==len(cuts)
    for cut in cuts:
        row=cut.get('sparse_row',cut.get('row_nonzero'))
        assert full_sha(row,len(x))==cut['row_sha256']
        assert sum(F(v)*x[j] for j,v in row)==F(cut['exact_slack'])<0
    raw_generator=HERE/'neighbor_bridge_audit_v1.py'
    # Keep the original schema/ordering to reproduce the reviewed 13-row pack.
    pack={
        'scope':'Thirteen necessary bridge candidates: one independently rebuilt early capacity row at source two using maximum-root hidden[0], plus twelve exact ZZ Frechet rows with current-point fixed endpoints. Pending Main independent full-coefficient review before integration; not an SPE or universal half certificate.',
        'source_path':str(point_path.relative_to(REPO)),
        'source_sha256':sha(point_path),'columns':4849,
        'descriptor_sha256':report['descriptor_sha256'],
        'reconstruction_report':str(audit.relative_to(REPO)),
        'reconstruction_report_sha256':sha(audit),
        'generator_path':str(raw_generator.relative_to(REPO)),
        'generator_sha256':sha(raw_generator),
        'normalization':'CAP source weight one retained; each ZZ row divided by its positive number of literal edge pairs; original vector SHA, scale and exact source slack retained per cut.',
        'cut_count':len(cuts),'cuts':cuts
    }
    assert len(cuts)==13,'This frozen pack schema is specifically the reviewed 5786 thirteen-row batch.'
    serialized=(json.dumps(pack,ensure_ascii=False,indent=2)+'\n').encode()
    if output.exists():assert output.read_bytes()==serialized,'Existing pack differs; refusing overwrite.'
    else:output.write_bytes(serialized)
    evidence={'status':'PASS','role':'Exact deterministic serialization and rescaling replay; no new mathematical row theorem.',
              'command':[sys.executable,'-B',str(Path(__file__).resolve()),str(audit),str(output),str(verification)],
              'script_sha256':sha(Path(__file__)),'audit_sha256':sha(audit),
              'point_sha256':sha(point_path),'pack_sha256':sha(output),
              'rows':len(cuts),'columns':len(x),'all_exact_slacks_strictly_negative':True,
              'existing_bytes_preserved':True}
    if verification.exists():assert json.loads(verification.read_text())==evidence
    else:verification.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(evidence,ensure_ascii=False))

if __name__=='__main__':main()
