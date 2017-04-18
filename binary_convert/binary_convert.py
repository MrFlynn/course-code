#!/usr/bin/env python3

import math

def main():
    input_number = input("Number to convert to binary: ")
    working_value = int(input_number)
    binary_array = []

    while (working_value != 0):
        binary_array.append(working_value % 2)
        working_value = math.floor(working_value / 2)

    final_binary_list = list(reversed(binary_array))
    print("".join([str(x) for x in final_binary_list]))

if __name__ == '__main__':
    main()