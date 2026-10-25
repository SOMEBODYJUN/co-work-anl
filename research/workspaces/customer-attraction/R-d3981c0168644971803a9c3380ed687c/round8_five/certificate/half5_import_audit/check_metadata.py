"""Standalone manifest, exact 53-weight and K-column reconstruction.

No portable verifier, local verifier, or old feature engine is imported.
"""
from pathlib import Path
from fractions import Fraction as F
from math import ceil
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists())
PKG=ROOT/'customer_attraction/proofs/half5_exact_v1'


def run():
    manifest=json.loads((PKG/'MANIFEST.json').read_text());files=[]
    for n,entry in manifest['files'].items():
        raw=(PKG/n).read_bytes();assert len(raw)==entry['bytes'] and hashlib.sha256(raw).hexdigest()==entry['sha256'];files.append(n)
    certbytes=(PKG/'certificate.json').read_bytes();cert=json.loads(certbytes)
    assert hashlib.sha256(certbytes).hexdigest()==manifest['certificate_sha256']
    w={n:int(v) for n,v in cert['integer_multipliers'].items()};D=int(cert['common_denominator'])
    assert len(w)==53 and min(w.values())>0 and int(cert['beta_numerator'])==2*D and D==10**22
    read=lambda n:json.loads((PKG/'components'/n).read_text())
    b2,b3,p2,p3=map(read,('background_player2.json','background_player3.json','priced_player2.json','priced_player3.json'))
    bg=[F(b2[i]['Kcoef']) for i in (0,1,3,5,11,12)]+[F(c['beta_K']) for c in b3[:3]]
    pc=[F(c['Kcoef']) for c in p2]+[F(c['Kcoef']) for c in p3]
    deep=[F(c['beta']) for c in read('deep_root_query.json')]
    signed_root=F(read('maxroot_four_copy.json')[0]['C'])
    k={}
    for name in w:
        z=name.split(':');family=z[0] in ('AB','AE','Sbranch');parts=z[1:] if family else z
        if name=='MAXROOT-NEW':v=ceil(10**6*signed_root)
        elif parts[0]=='MAX':v=1
        elif parts[0]=='DEEP':v=ceil(10**6*deep[int(parts[1])])
        elif parts[0]=='BG':v=(5 if family else 1)*ceil(10**6*bg[int(parts[1])])
        elif parts[0]=='PC':v=(5 if family else 1)*ceil(10**6*pc[int(parts[1])])
        else:v=0
        k[name]=v
    provided={n:int(v) for n,v in json.loads((PKG/'active_k_columns.json').read_text())['row_K_coefficients'].items()}
    assert k==provided
    weighted=sum(w[n]*k[n] for n in w);assert weighted==-2264870
    report={'status':'passed','scope':__doc__,'files_checked':len(files),'positive_integer_multipliers':len(w),
            'common_denominator':str(D),'target':'2','reconstructed_K_coefficients':k,
            'weighted_K_column':str(weighted),'integer_identity_K_credit':str(-120*weighted),
            'certificate_sha256':hashlib.sha256(certbytes).hexdigest(),
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'metadata_and_K_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key!='reconstructed_K_coefficients'},indent=2))


if __name__=='__main__':run()
