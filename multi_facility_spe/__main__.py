"""Exact finite witness CLI. No polynomial-time guarantee."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .two_exists import Instance, construct


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('instance', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--method', choices=('lexmax', 'greedy-box'), default='lexmax',
                        help='finite constructor (default: legacy exhaustive lexmax)')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite an existing output; choose a new path')
    try:
        instance = Instance.from_json(json.loads(args.instance.read_text()))
        if args.method == 'greedy-box':
            from .greedy_box import construct as construct_greedy_box
            certificate = construct_greedy_box(instance)
        else:
            certificate = construct(instance)
    except (ValueError, KeyError, TypeError, ZeroDivisionError) as exc:
        parser.error(str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(certificate, indent=2)+'\n')
    print('Exact factor-two witness written. Construction is finite; no polynomial-time guarantee.')


if __name__ == '__main__':
    main()
