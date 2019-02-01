#!/usr/bin/python3

import argparse
import time
import sys
import random

def apply_rule(rule, a, b, c):
    if rule > 255 or rule < 0:
        raise IOError("Rule value must be between 0 and 255")

    index = 4*a + 2*b + c
    rule_values = str(bin(rule+256))[3::] # Add 256 to ensure string is 8 bits long
    return int(rule_values[7-index])


def next_row(row, rule, wrap=False):
    old_row = row.copy()
    for i in range(len(row)):
        if i == 0:
            if wrap:
                a = old_row[len(row)-1]
            else:
                a = 0
        else:
            a = old_row[i-1]
        b = old_row[i]
        if i == len(row)-1:
            if wrap:
                c = old_row[0]
            else:
                c = 0
        else:
            c = old_row[i+1]
        row[i] = apply_rule(rule, a, b, c)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rule", type=int, help="Wolfram rule to apply. Supply in base 10 (0-255).")
    parser.add_argument("-w", "--width", type=int, help="Width of the space.", default=80)
    parser.add_argument("-x", "--random", action="store_true", help="Popuate generation 0 randomly")
    parser.add_argument("-c", action="store_true", help="Turns grid into a continuous surface which wraps-around the edges")
    parser.add_argument("-t", "--time_delay", type=float, help="Delay between sucessive generations in seconds", default=0.1)

    args = parser.parse_args()

    if args.rule == None:
        print("Error: A wolfram rule must be set (with -r)")
        sys.exit(1)

    row = [0]*args.width

    if args.random:
        for i in range(len(row)):
            row[i] = random.randint(0,1)
    else:
        row[args.width//2] = 1

    rule = args.rule

    while 1:
        for r in row:
            if r == 1:
                print("*", end = "")
            else:
                print(" ", end = "")
        print()
        next_row(row, args.rule, wrap=args.c)
        time.sleep(args.time_delay)
