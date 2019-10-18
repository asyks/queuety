#!/usr/bin/env python
import argparse

from . import entry, log


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Run the asynchronous queue.",
    )
    parser.add_argument(
        "--simulate",
        help="Simulate pub/sub using a stream of fake messages.",
        action="store_true",
    )

    args = parser.parse_args()
    log.setup()

    if args.simulate:
        entry.run_simulation()
    else:
        entry.run()
