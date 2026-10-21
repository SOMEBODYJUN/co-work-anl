"""Finite attack on the safe-action sufficient lemma for fractional floors."""
from fractional_floor_probe import *
from itertools import combinations_with_replacement


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--players', type=int, default=3)
    ap.add_argument('--topics', type=int, default=6)
    ap.add_argument('--trials', type=int, default=2000)
    ap.add_argument('--seed', type=int, default=887719)
    ap.add_argument('--seconds', type=float, default=45)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    start = time.monotonic()
    completed = 0
    result = None
    best_count = 0
    for trial in range(args.trials):
        if time.monotonic()-start >= args.seconds:
            break
        types = tuple(CustomerType(frozenset(a for a in range(args.topics) if mask >> a & 1),
                                   rng.randint(1, 10))
                      for mask in range(1, 1 << args.topics) if rng.random() < .3)
        if not types:
            continue
        instance = Instance(tuple(map(str, range(args.topics))), types, args.players)
        opt, _ = fractional_floor(instance)
        completed += 1
        if not opt.success:
            continue
        tau = opt.fun
        witness = {}
        for a in range(args.topics):
            for bs in combinations_with_replacement(range(args.topics), args.players-1):
                counts = instance.counts((a,)+bs)
                pay = instance.topic_payoffs(counts)
                if float(pay[a]) < tau-1e-7 and min(float(pay[b]) for b in bs) >= tau+1e-7:
                    witness[a] = {'others': bs, 'root_pay': str(pay[a]),
                                  'other_pays': [str(pay[b]) for b in bs]}
                    break
        best_count = max(best_count, len(witness))
        if len(witness) == args.topics:
            result = {'candidate_only': True, 'instance': instance.to_dict(),
                      'fractional_numerical': float(tau), 'q': opt.x[:-1].tolist(),
                      'witness': witness}
            break
    out = {'scope': 'finite random safe-action sufficient-lemma attack; no SPE asserted',
           'universal_claim_proved': False, 'completed': completed, 'best_bad_action_count': best_count,
           'elapsed': time.monotonic()-start, 'candidate': result}
    args.output.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
