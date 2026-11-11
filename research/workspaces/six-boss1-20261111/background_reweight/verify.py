"""Replay exact upper and/or lower outputs without a numerical LP solver."""
import argparse
import json
from pathlib import Path
from cone import Oracle, check_inputs, verify_lower, verify_upper


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('directory', type=Path)
    ap.add_argument('--lower-only', action='store_true')
    args = ap.parse_args()
    check_inputs()
    report = {}
    lower = args.directory/'exact_lower_certificate.json'
    if lower.exists():
        report['lower'] = verify_lower(json.loads(lower.read_text()))
    upper = args.directory/'exact_upper_certificate.json'
    if upper.exists() and not args.lower_only:
        report['upper'] = verify_upper(json.loads(upper.read_text()), Oracle(), progress=lambda x: print(json.dumps(x), flush=True))
        assert report['upper']['status'] == 'UNIVERSAL-CONE-CERTIFICATE'
    assert report, 'No applicable exact certificate was supplied.'
    (args.directory/'replay_audit.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
