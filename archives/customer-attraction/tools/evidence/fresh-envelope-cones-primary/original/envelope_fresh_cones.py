"""Probe diverse full-history fresh-action cones, with no anonymous tie rule.

Uniform positive mass on every customer type makes every always-fresh policy
an SPE (M2 with signed perturbation zero). LPs subsequently vary all masses
while retaining that policy's complete original incentive matrix.
"""

import argparse
import itertools
import json
import random
import runpy
from pathlib import Path
from customer_attraction.model import Instance, CustomerType
from customer_attraction.certificate import StrategyCertificate, verify_certificate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--players', type=int, default=5)
    parser.add_argument('--topics', type=int, default=7)
    parser.add_argument('--trials', type=int, default=12)
    parser.add_argument('--seed', type=int, default=21062026)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.topics < args.players:
        raise ValueError('fresh policy requires topics >= players')
    optimize = runpy.run_path(str(Path(__file__).with_name('envelope_cone_probe.py')))['optimize']
    rng = random.Random(args.seed)
    p, m = args.topics, args.players
    instance = Instance(tuple(map(str, range(p))),
                        tuple(CustomerType(frozenset(a for a in range(p) if mask >> a & 1))
                              for mask in range(1, 1 << p)), m)
    records = []
    for trial in range(args.trials):
        actions = {h: rng.choice(tuple(a for a in range(p) if a not in h))
                   for depth in range(m) for h in itertools.product(range(p), repeat=depth)}
        h = ()
        while len(h) < m:
            h = h + (actions[h],)
        cert = StrategyCertificate(actions, instance.counts(h, terminal=True))
        if trial == 0:
            verify_certificate(instance, cert).assert_valid()
        result = optimize(instance, cert)
        result['trial'] = trial
        records.append(result)
        print(json.dumps({k:v for k,v in result.items() if k != 'numerical_weights'}), flush=True)
    with args.output.open('x') as f:
        json.dump({'status': 'floating_exploration_only',
                   'parameters': vars(args) | {'output': str(args.output)},
                   'policy_family': 'all ordered-history actions sampled independently among unused labels',
                   'records': records}, f, indent=2)
        f.write('\n')


if __name__ == '__main__':
    main()
