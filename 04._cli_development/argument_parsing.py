"""Minimal demo of the stdlib argparse module.

Try:
    python argument_parsing.py --help
    python argument_parsing.py Alice
    python argument_parsing.py Alice --count 3 -v
    python argument_parsing.py Alice --count three    # argparse rejects this
"""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(prog="greet", description="Greet someone from the command line.")
    parser.add_argument("name", help="who to greet")                                        # positional argument
    parser.add_argument("-n", "--count", type=int, default=1, help="how many times to greet")  # option with a value
    parser.add_argument("-v", "--verbose", action="store_true", help="print extra output")    # flag (True/False)

    args = parser.parse_args()  # reads sys.argv[1:]

    if args.verbose:
        print(f"Parsed arguments: {args}")
    for _ in range(args.count):
        print(f"Hello, {args.name}!")


if __name__ == "__main__":
    main()
