#!/usr/bin/env python3

import sys

from typing import List


class SimHash:
    def __init__(self, fingerprint_size: int = 8):
        self._fsize = fingerprint_size

    def _words_to_vector(self, words: str) -> List[int]:
        mod = 1 << self._fsize
        return [sum([ord(c) for c in w]) % mod for w in words.split()]

    def _column_weights(self, words: List[int]) -> List[int]:
        weights = []

        for offset in range(self._fsize - 1, -1, -1):
            weight = 0
            for w in words:
                if w & (1 << offset):
                    weight += 1
                else:
                    weight -= 1

            weights.append(weight)

        return weights

    @staticmethod
    def _fingerprint_from_weights(weights: List[int]) -> int:
        fingerprint = 0

        for idx, w in enumerate(weights[::-1]):
            if w > 0:
                fingerprint |= (1 << idx)

        return fingerprint

    def hash(self, string: str) -> int:
        vec = self._words_to_vector(string)
        weights = self._column_weights(vec)
        return self._fingerprint_from_weights(weights)


def main():
    words = " ".join(sys.argv[1:])

    hasher = SimHash()
    fprint = hasher.hash(words)

    print(
        f"Fingerprint of \"{words}\" is: {fprint} ({format(fprint, '08b')})"
    )


if __name__ == "__main__":
    main()
