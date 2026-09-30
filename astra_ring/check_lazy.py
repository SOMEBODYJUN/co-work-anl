"""Independent lazy/full regression; no optional packages."""
import random,json
from mitm_solver import game_solve,lazy_ring_solve
rng=random.Random(33221); total_pruned=0
for _ in range(30):
    data={'weights':[rng.randrange(1,25) for i in range(8)],'locations':[[i for i in range(8) if rng.random()<.6] for j in range(6)]}
    full=game_solve(data);lazy=lazy_ring_solve(data)
    assert all(val==full['d'][int(j)] for j,val in lazy['d_on_visited'].items())
    assert full['alpha']<=lazy['alpha']
    total_pruned+=lazy['stats']['pruned_responses']
print(json.dumps({'lazy_full_checks':30,'pruned_responses':total_pruned,'status':'passed'},indent=2))
