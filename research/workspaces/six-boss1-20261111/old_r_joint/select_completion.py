"""Select a simple exact feasible mixture after all class values are audited."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse,json

def sha(p):return sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=Path,required=True)
    ap.add_argument('--audit',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--phase-b',default='0');args=ap.parse_args()
    w=json.loads(args.candidate.read_bytes());a=json.loads(args.audit.read_bytes())
    assert a['witness_sha256']==sha(args.candidate) and a['input_sha256']==w['input_sha256']
    lam=F(args.phase_b);assert 0<=lam<=1
    checks=[]
    for r in a['records']:
        v=(1-lam)*F(r['phase_A'])+lam*F(r['phase_B']);assert v>=0
        checks.append({'kind':r['kind'],'class':r['class'],'literal_queries':r['literal_queries'],
                       'orbit_sum':str(v),'individual_slack':str(v/r['literal_queries'])})
    w['candidate_source_sha256']=sha(args.candidate);w['selection_audit_sha256']=sha(args.audit)
    w['selection_source_sha256']=sha(Path(__file__))
    w['scope']='Exact selected common coverage completion for all old R/R, R/Z, Z/R, Z/Z terminal queries; not full SPE or cross-family completion'
    w['phase_A_weight']=str(1-lam);w['phase_B_weight']=str(lam)
    weights={'A':1-lam,'B':lam}
    w['expanded_positive_atoms']=720*sum(len(h['atoms']) for p in ('A','B') if weights[p] for h in w['phases'][p])
    w['selected_query_records']=checks
    args.output.write_text(json.dumps(w,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'output':str(args.output),'input_sha256':w['input_sha256'],
        'selected_weights':{p:str(v) for p,v in weights.items()},'all_168_classes_nonnegative':len(checks)==168,
        'expanded_positive_atoms':w['expanded_positive_atoms'],'witness_sha256':sha(args.output)},ensure_ascii=False))

if __name__=='__main__':main()
