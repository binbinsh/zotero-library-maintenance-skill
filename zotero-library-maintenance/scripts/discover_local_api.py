#!/usr/bin/env python3
import argparse
import json

from zotero_discovery import discover_local_api


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-base", action="append", default=[])
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()
    print(json.dumps(discover_local_api(args.candidate_base, timeout=args.timeout), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
