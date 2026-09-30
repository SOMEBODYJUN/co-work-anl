import argparse,json,time
from mitm_solver import lazy_ring_solve,serial
ap=argparse.ArgumentParser();ap.add_argument('input');args=ap.parse_args()
with open(args.input) as f:data=json.load(f)
start=time.perf_counter();result=lazy_ring_solve(data);result['elapsed_seconds']=time.perf_counter()-start
print(json.dumps(serial(result),indent=2))
