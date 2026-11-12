"""Decode saved original JSON fields only; never evaluate a game or an IC."""
from pathlib import Path
import argparse
import hashlib
import json


def decode(codec):
    vectors = codec['forced_vectors']
    groups = codec['forced_group_index']
    for depth in range(5):
        for ordinal in range(7 ** depth):
            digits = [0] * depth
            rest = ordinal
            for pos in range(depth - 1, -1, -1):
                digits[pos] = rest % 7
                rest //= 7
            key = ''.join(map(str, digits)) or 'e'
            group = ''.join(map(str, sorted(digits))) or 'e'
            chosen = codec['chosen_exceptions'].get(key, 0)
            tail = codec['tail_exceptions'].get(key, [0] * (5 - depth))
            vid = codec['forced_order_exceptions'].get(key, groups[group])
            forced = vectors[vid]
            payoff = forced[chosen]
            yield {
                'history': digits,
                'chosen': chosen,
                'actual_leaf': digits + tail,
                'payoff_scaled': payoff,
                'forced_payoffs_scaled': forced,
                'slacks_scaled': [payoff - value for value in forced],
            }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument('--codec', type=Path, default=Path(__file__).with_name('profiles-lossless-codec.json'))
    args = parser.parse_args()
    codec = json.loads(args.codec.read_text())
    source = (args.source_root / codec['source']['path']).read_bytes()
    records = list(decode(codec))
    original = [json.loads(line) for line in source.splitlines()]
    decoded = ''.join(json.dumps(record, ensure_ascii=False, separators=(',', ':')) + '\n' for record in records).encode()
    assert records == original
    assert decoded == source
    print(json.dumps({
        'purpose': 'lossless reading codec only; no payoff/IC/solver/audit calculation',
        'source_sha256': hashlib.sha256(source).hexdigest(),
        'decoded_sha256': hashlib.sha256(decoded).hexdigest(),
        'records_equal_in_order': records == original,
        'raw_bytes_equal': decoded == source,
    }, indent=2))


if __name__ == '__main__':
    main()
