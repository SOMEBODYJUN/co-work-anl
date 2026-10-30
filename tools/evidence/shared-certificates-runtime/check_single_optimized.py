from copy import deepcopy
from fractions import Fraction as Q
import json,sys
from facility_spe.exact import single_overlap as mod
case={'weights':[2,3,5],'locations':[[0,1],[2],[0],[1]],'U1':[0,1],'U2':[2,3]}
out=mod.solve(case)
def forbidden(*a):raise RuntimeError('producer called')
mod.local=forbidden;mod.solve=forbidden
mod.verify(case,out)
bad=deepcopy(out);bad['deviations'].pop()
try:mod.verify(case,bad)
except ValueError:pass
else:raise RuntimeError('missing deviation accepted')
print(json.dumps({'optimization_flag':sys.flags.optimize,'producer_disabled_valid_certificate':'accepted','missing_deviation':'rejected','alpha':str(out['alpha'])}))
