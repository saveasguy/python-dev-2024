import argparse
import cowsay
import sys

parser = argparse.ArgumentParser("cow_say")
parser.add_argument("-e", type=str, dest="eye_string", default=cowsay.Option.eyes)
parser.add_argument("-l", action="store_true")
parser.add_argument("-f", type=str, dest="cowfile", default=None)
parser.add_argument("-n", action="store_true")
parser.add_argument("-T", type=str, dest="tongue_string", default=cowsay.Option.tongue)
parser.add_argument("-W", type=int, dest="column", default=40)
parser.add_argument("-b", action="store_true")
parser.add_argument("-d", action="store_true")
parser.add_argument("-g", action="store_true")
parser.add_argument("-p", action="store_true")
parser.add_argument("-s", action="store_true")
parser.add_argument("-t", action="store_true")
parser.add_argument("-w", action="store_true")
parser.add_argument("-y", action="store_true")
args = parser.parse_args()

if args.l:
    print(" ".join(cowsay.list_cows()))
    exit(0)
