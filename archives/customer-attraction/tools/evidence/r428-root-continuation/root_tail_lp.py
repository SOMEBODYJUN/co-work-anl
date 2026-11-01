"""Discovery only: five-player true root/middle branches and tail-profit rows.

No feasible point here is claimed to be a game or an SPE.  The independent
variable O is bounded by valid aggregate comparisons, not identified with a
particular realizable optimal menu.  A dual would require exact recovery.
"""
from pathlib import Path
import json
import time
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
LABELS = 'ABCDEFGHIUVWXY'
PATHS = {'actual': 'ABCDE', 'root': 'EFGHI',
         'second': 'AEUVW', 'third': 'ABEXY'}
START = {'actual': 0, 'root': 1, 'second': 2, 'third': 3}


def solve():
    began = time.time()
    integer = np.arange(1 << len(LABELS), dtype=np.int64)
    bits = ((integer[:, None] >> np.arange(len(LABELS))) & 1).T
    b = dict(zip(LABELS, bits))
    size = len(integer)
    rows, names = [], []

    def ratio(numerator, denominator):
        return np.divide(numerator, denominator,
                         out=np.zeros(size), where=denominator != 0)

    def add(name, atom, opt=0):
        rows.append(np.r_[atom, opt])
        names.append(name)

    shares = {}
    for tag, path in PATHS.items():
        load = sum(b[t] for t in path)
        sh = [ratio(b[t], load) for t in path]
        shares[tag] = sh
        for i in range(START[tag], 5):
            prefix = sum((b[t] for t in path[:i]), np.zeros(size))
            remain = 5 - i
            for topic in LABELS:
                add(f'{tag}:{i+1}:floor:{topic}',
                    sh[i] - ratio(b[topic], prefix + remain))
            add(f'{tag}:{i+1}:aggregate',
                5 * remain * sh[i] + ratio(prefix, prefix + remain), -1)
        for k, beta in [(3, 5 / 3), (4, 1499 / 750)]:
            i = 5-k
            if i < START[tag]:
                continue
            prefix = sum((b[t] for t in path[:i]), np.zeros(size))
            add(f'{tag}:tail{k}:profit',
                (5 * beta / k) * sum(sh[i:]) + ratio(prefix, prefix + 1), -1)
        prefix = sum(b[t] for t in path[:3])
        tax = ratio(b[path[3]], (prefix+1)*(prefix+2))
        add(f'{tag}:tail2:tax',
            2.5 * (sh[3]+sh[4]+tax) + ratio(prefix, prefix+1), -1)
    add('IC:root:E', shares['actual'][0]-shares['root'][0])
    add('IC:second:E', shares['actual'][1]-shares['second'][1])
    add('IC:third:E', shares['actual'][2]-shares['third'][2])

    matrix = np.asarray(rows)
    welfare = (sum(b[t] for t in PATHS['actual']) > 0).astype(float)
    objective = np.r_[np.zeros(size), -1]
    result = linprog(objective, A_ub=-matrix, b_ub=np.zeros(len(rows)),
                     A_eq=np.r_[welfare, 0][None, :], b_eq=[1],
                     bounds=(0, None), method='highs',
                     options={'time_limit': 240})
    report = {'status': int(result.status), 'message': result.message,
              'labels': LABELS, 'paths': PATHS, 'starts': START,
              'rows': names, 'atoms': size,
              'elapsed_seconds': time.time()-began,
              'claim': 'discovery relaxation only, never an SPE certificate'}
    if result.success:
        report['optimum_float'] = float(-result.fun)
        report['support'] = [{'bits': ''.join(map(str, bits[:, j])),
                              'weight_float': float(x)}
                             for j, x in enumerate(result.x[:-1]) if x > 1e-9]
        report['multipliers_float'] = {
            name: float(-v) for name, v in zip(names, result.ineqlin.marginals)
            if abs(v) > 1e-10}
        report['minimum_slack_float'] = float((matrix@result.x).min())
    (HERE/'root_tail_lp_result.json').write_text(
        json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()
                      if k not in {'support','multipliers_float','rows'}}, indent=2), flush=True)


if __name__ == '__main__':
    solve()
