#!/usr/bin/env python3
"""Check a shared-catalog phi certificate without rebuilding witness menus."""
import argparse
import json

from common_phi_algorithm import verify


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="exact-rational incidence JSON")
    parser.add_argument("certificate", help="output of common_phi_algorithm.py")
    args = parser.parse_args()
    with open(args.input, encoding="utf-8") as stream:
        instance = json.load(stream, parse_float=str)
    with open(args.certificate, encoding="utf-8") as stream:
        certificate = json.load(stream, parse_float=str)
    verify(instance, certificate)
    print("Valid exact-customer-NE facility-deviation certificate")


if __name__ == "__main__":
    main()
