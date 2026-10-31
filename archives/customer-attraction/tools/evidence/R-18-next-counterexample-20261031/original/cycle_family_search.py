"""Scout the five-type clone-refutation incidence for larger player numbers."""
import json,sys,time
from pathlib import Path
import numpy as np
from search_terminal import Scout
m,steps=map(int,sys.argv[1:]);s=Scout(4,m);rng=np.random.default_rng(934+m);best=-1;start=time.time();save=np.array([1,1,1,1,3]);parent=Path(__file__).parent
for it in range(steps):
 if it%7==0:raw=rng.integers(1,100,5)
 elif it%7<6:
  raw=save.copy();j=rng.integers(5);raw[j]=max(0,raw[j]+rng.integers(-25,26))
 else:raw=rng.integers(0,9,5)
 w=np.zeros(15);w[np.array([1,2,6,9,12])-1]=raw
 b,half,u,W=s.run(w)
 if b[0]>best+1e-8:
  best=b[0];save=raw.copy();record={'m':m,'iteration':it,'C2_violation_ratio':best,'path':b[1],'five_weights':raw.tolist(),'weights':w.tolist(),'half_ratio':half}
  parent.joinpath(f'cycle_best_{m}.json').write_text(json.dumps(record,indent=2));print(record,flush=True)
 if it%1000==0:print('progress',it,'elapsed',time.time()-start,flush=True)
 if best>1.000001:break
