"""Independent single-query Frechet ceilings for all 15 B4 queries."""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse,json

def sha(p):return sha256(Path(p).read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--point',type=Path,required=True)
    ap.add_argument('--verification',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();raw=json.loads(a.point.read_text());check=json.loads(a.verification.read_text())
    assert sha(a.point)==check['point_sha256']=='d70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f'
    hist={};own=defaultdict(dict);fam=defaultdict(dict)
    for i,c in enumerate(raw['columns'][:4849]):
        if c['kind']=='hist':h=i;hist[h]=c
        elif c['kind']=='joint-reply':
            f,b,u,v=c['group'];own[h].setdefault((f,b,tuple(u),tuple(v)),{})[tuple(c['state'])]=Q(c['weight'])
        elif c['kind']=='actual-B-family-state' and c['source']==4:
            fam[c['hist_column']][tuple(c['hidden'])+(c['ell']//6,)]=Q(c['weight'])
    nodes=[n for n in product(range(2),range(6),range(6)) if n[0] or n[1]!=n[2]]
    values=defaultdict(Q)
    for h,hc in hist.items():
        a6=tuple(map(int,hc['actual_bits']));P=sum(a6[:4]);D=(P+1)*(P+2);fd=sum(a6[:3])+a6[5]+1
        words=[w for w,n in zip(product(range(2),repeat=3),hc['hist']) for _ in range(n)]
        B=sum((m*Q(s[1],fd+s[0]) for s,m in fam[h].items()),Q())
        xi=[sum((m*s[k] for s,m in fam[h].items()),Q()) for k in range(3)]
        for f,i,j in nodes:
            orb=(f,int(i==j));size=6 if i==j else 30;m=own[h][f,int(i==j),words[i],words[j]]
            q=m[1,0]+m[1,1];v=m[0,1]+m[1,1];t=m[1,1]
            for kind,mu in (('R',q),('Z',v)):
                values['F-to-'+kind,orb]+=(B-mu/Q(fd)+min(mu,xi[0])/Q(fd*(fd+1)))/size
            for k in range(3):
                values['Z-to-X',orb,k]+=((v-xi[k])/Q(P+1)+(min(q,xi[k])-t)/Q(D))/size
    delta=Q(check['B4_minimum_slack']);rows=[];tight=[]
    for key,upper in sorted(values.items()):
        assert upper>0 and upper>=delta
        if upper==delta:tight.append(key)
        rows.append(dict(query=key,upper=str(upper),upper_float=float(upper)))
    out=dict(point_sha256=sha(a.point),independent_verification_sha256=sha(a.verification),
             source_sha256=sha(Path(__file__)),single_query_uppers=rows,
             zero_single_query_uppers=0,witness_common_margin=str(delta),tight_witness_margin_upper_queries=tight,
             exact_optimal_common_margin_on_zero_face_plus_B4=bool(tight),
             scope='Upper ceiling for any common completion; the saved common atoms attain this minimum B4 margin while satisfying the entire zero-cell face. Does not impose the remaining old IC.')
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='single_query_uppers'}))

if __name__=='__main__':main()
