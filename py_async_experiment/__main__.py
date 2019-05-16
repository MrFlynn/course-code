import argparse

from app import App


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--thread-timings', dest='timings', type=int, nargs='+')

    args = parser.parse_args()

    app = App(args.timings)
    app.run()
