from customer_attraction import Instance, ExactSPESolver, CustomerType
from fractions import Fraction
import random, time, json

def Ls(inst, solver, hist):
    vals = []
    for i in range(inst.players):
        cnt = inst.counts(hist[:i]); row = []
        for a in range(inst.topic_count):
            child = tuple(cnt[j] + (j == a) for j in range(inst.topic_count))
            row.append(min(inst.topic_payoff(a, t) for t in solver._solve(child)))
        vals.append(row)
    return vals

def best_opt_dp(inst, ls):
    p, m, O = inst.topic_count, inst.players, inst.optimal_welfare()
    welfare = [inst.welfare(tuple(int(j in mask) for j in range(p))) for mask in range(1 << p)]
    best = None
    for support in range(1 << p):
        if welfare[support] != O: continue
        dp = {0: (Fraction(0), ())}
        for i in range(m):
            nd = {}
            for mask, (value, tup) in dp.items():
                for a in range(p):
                    nm = mask | (1 << a)
                    if nm & ~support: continue
                    nv = value + ls[i][a]
                    if nm not in nd or nv < nd[nm][0]: nd[nm] = (nv, tup + (a,))
            dp = nd
        if support in dp and (best is None or dp[support][0] < best[0]):
            best = (dp[support][0], dp[support][1], support)
    return best

def run(inst):
    solver = ExactSPESolver(inst); O = inst.optimal_welfare()
    for z in solver.worst_outcomes():
        W = inst.welfare(z); h = next(solver.ordered_outcomes(z))
        best = best_opt_dp(inst, Ls(inst, solver, h))
        if best and best[0] < O - W:
            return {'bad': True, 'O': O, 'W': W, 'sumL': best[0], 'gap': O-W,
                    'h': h, 'z': z, 'T': best[1], 'mask': best[2], 'inst': inst.to_dict()}
    return None

random.seed(20261024); start = time.time()
for it in range(20000):
    p, m = 3, random.randint(6, 10)
    mult = [0] + [random.randint(0, 20) for _ in range(7)]
    customers = tuple(CustomerType(frozenset(j for j in range(p) if mask >> j & 1), mult[mask])
                      for mask in range(1, 8) if mult[mask])
    inst = Instance(tuple(f'T{j}' for j in range(p)), customers, m)
    try: result = run(inst)
    except Exception: continue
    if result:
        print(json.dumps({k: str(v) for k, v in result.items()}, indent=2)); break
    if it % 100 == 0: print('it', it, 'sec', time.time()-start, flush=True)
else: print('none')
