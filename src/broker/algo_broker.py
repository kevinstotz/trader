import argparse
from src.algos.Algorithms import Algorithm


def main():
    parser = argparse.ArgumentParser(description="sample argument parser")
    parser.add_argument("algo", nargs='?', default=Algorithm.SMA.value)
    args = parser.parse_args()

    if args.algo == Algorithm.SMA.value:
        print("Hello SMA")
    else:
        print("Hello Unrecognized")


if __name__ == '__main__':
    main()
