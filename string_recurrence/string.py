#!/usr/bin/env python3
# Nick Pleatsikas
# CS111 Homework #3, Problem #1.
#
# Given a set of strings and a string size, create combinations of strings of 
# the desired size.


def reverse_string_build(prev: str, size: int, base_strs: list) -> list:
    """Recursively generates a list of all strings of `size` containing all
    valid combiantions (i.e. the combination fits within the specific size) of
    `base_strs` prepended to the input string `prev`.

    :param prev: previous strings to prepend valid combinations too.
    :param size: remainaing size of string.
    :param base_strs: list of all strings that may be prepended to `prev`.
    :return: list of valid combinations of `prev` and `base_strs`.
    """

    # Filter `base_strs` to just those of length `size`.
    prepenable_strings = list(filter(lambda x: len(x) <= size, base_strs))
    full_branch = []

    if size > 0:
        for s in prepenable_strings:
            full_branch.append(s + prev)

            # Recursive call to this function, but with size limited and 
            # `prev` modified.
            sub_branch = reverse_string_build(s + prev, 
                            size - len(s), 
                            base_strs)
            full_branch.extend(sub_branch)

    return full_branch


def main():
    # Get the size and declare the base list of strs to create other strings.
    size = int(input('Strings of size = '))
    base_strings = ['A', 'BB', 'BC', 'CB', 'CC', 'EEF', 'FEE']
    
    # Get output from recursive function call of `reverse_string_build`.
    filtered_output = list(
        filter(lambda x: len(x) == size, 
        reverse_string_build('', size, base_strings)))

    # Print the size and the list.
    print(f'Number of elements: {len(filtered_output)}')
    print(filtered_output)


if __name__ == '__main__':
    main()
