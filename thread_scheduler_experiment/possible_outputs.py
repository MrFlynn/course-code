#!/usr/bin/env python

import sys

from itertools import permutations

func_matrix = [
    lambda x: x * x,
    lambda x: x - 1,
]

def shared_idx():
    count = 0
    i_idx = [0] * 2
    possible_outputs = set()
    for r in permutations(range(4)):
        for idx in r:
            if i_idx[0] >= 2 or i_idx[1] >= 2:
                break

            count = func_matrix[idx % 2](count)
            i_idx[idx % 2] = i_idx[idx % 2] + 1

        possible_outputs.add(count)
        i_idx = [0] * 2
        count = 0

    print(possible_outputs)

def shared_count():
    count = 0
    possible_outputs = set()
    for r in permutations(range(4)):
        for idx in r:
            count = func_matrix[idx % 2](count)

        possible_outputs.add(count)
        count = 0

    print(possible_outputs)

if __name__ =='__main__':
    try:
        if sys.argv[1] == "0":
            shared_count()
        else:
            shared_idx()
    except IndexError:
        print("Please select 0 or 1!")
