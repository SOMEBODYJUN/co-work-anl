"""Worst-case exponential exact ring solver with sound lazy pruning."""
import argparse
import json
import time

from facility_spe.exact.mitm import lazy_ring_solve, serial


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()
    with open(args.input, encoding="utf-8") as stream:
        data = json.load(stream, parse_float=str)
    start = time.perf_counter()
    result = lazy_ring_solve(data)
    result["elapsed_seconds"] = time.perf_counter() - start
    print(json.dumps(serial(result), indent=2))


if __name__ == "__main__":
    main()
