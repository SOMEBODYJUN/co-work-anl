"""Standard-library exact replay of the missing B-menu price family.

Input is one necessary-condition point, never interpreted as a full SPE.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent

def audit(path):
 raw=path.read_bytes();d=json.loads(raw);cols=d['columns'];us=[F(0)]*6;prices=[F(0)]*6;size=F(0);K=F(0)
 for c in cols:
  weight=F(c['weight'])
  if c['kind']=='K':K+=weight
  elif c['kind']=='hist':
   ac=tuple(map(int,c['actual_bits']));load=sum(ac)
   for i,bit in enumerate(ac):
    if bit:us[i]+=weight*F(bit,load)
  elif c['kind']=='actual-B-branch-state':
   ac=tuple(map(int,cols[c['hist_column']]['actual_bits']));ell=c['ell'];size+=weight*F(ell,6)
   for i in range(6):prices[i]+=weight*F(ell,6*(sum(ac[:i])+6-i))
 slacks=[u-v for u,v in zip(us,prices)]
 return {'scope':'exact price rows of one necessary point, not SPE','source_sha256':hashlib.sha256(raw).hexdigest(),'actual_utilities':[str(v) for v in us],'reply_family_prices':[str(v) for v in prices],'price_slacks':[str(v) for v in slacks],'capacity_slack':str(K-size)}

def main():
 p=argparse.ArgumentParser();p.add_argument('--point',type=Path,default=HERE.parent/'research_2/coupled_B_master_exact.json');a=p.parse_args();out=audit(a.point)
 if out['source_sha256']=='6269be5cbcd61d397c33e19ce2ac31ace3f73aeec22c978426d8f3b30b0fada7':
  assert F(out['price_slacks'][5])==-F(1974049873898062469246100717814969218795193,183894086250618414573513470611398608470558592)
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
