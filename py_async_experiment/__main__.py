#!/usr/bin/env python

"""This is an example application meant to test the fundamental design of an
application I am writing for my job.

It served as a testbed for what design would best accomplish the overall goal
of this application.
"""

import argparse
import sys

from app import App


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=sys.modules[__name__].__doc__
    )
    parser.add_argument('--thread-timings', dest='timings', type=int, nargs='+')

    args = parser.parse_args()

    app = App(args.timings)
    app.run()
