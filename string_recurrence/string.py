#!/usr/bin/env python3
# Nick Pleatsikas
# CS111 Homework #3, Problem #1.
#
# Given a set of strings and a string size, create combinations of strings of 
# the desired size.
import itertools
from typing import Callable

def generate_tuples_of_size(strings: list, size: int, func: Callable) -> list:
    list_of_tuples = []

    for i in range(size + 1):
        items = list(func(strings, r=i))
        sized_items = filter(lambda x: sum(map(len, x)) == size, items)

        list_of_tuples.extend(list(sized_items))

    return list_of_tuples

def build_strings_of_size(strings: list, size: int) -> list:
    all_strings = []

    all_strings.extend(generate_tuples_of_size(strings, size, itertools.combinations_with_replacement))
    all_strings.extend(generate_tuples_of_size(strings, size, itertools.permutations))

    return list(set([''.join(i) for i in all_strings]))

def main():
    size = int(input('Strings of size='))
    base_strings = ['A', 'BB', 'BC', 'CB', 'CC', 'EEF', 'FEE']

    strings = build_strings_of_size(base_strings, size)
    print(f'Number of strings: {len(strings)}')
    print(strings)

if __name__ == '__main__':
    main()
