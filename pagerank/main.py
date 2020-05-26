#!/usr/bin/env python3

from __future__ import annotations
from typing import Dict, Iterable, List


class Node:
    def __init__(self, name: int):
        self.name = name
        self.score = 1.0

        self._temp_score = 1.0
        self._parents: List[Node] = []
        self._children: List[Node] = []

    def update(self, new_score: float, epsilon: float) -> bool:
        self._temp_score = new_score
        return abs(new_score - self.score) < epsilon

    def release(self):
        self.score = self._temp_score

    def connect(self, other: Node) -> None:
        if other not in self._children:
            self._children.append(other)

        other.add_parent(self)

    def add_parent(self, parent: Node) -> None:
        if parent not in self._parents:
            self._parents.append(parent)

    def parents(self) -> Iterable[Node]:
        return self._parents

    @property
    def outgoing(self) -> int:
        return len(self._children)


class PageRank:
    def __init__(self, damping: int = 0.7, epsilon: float = 0.001):
        self.epsilon = epsilon
        self.damping = damping

        self._jump_factor = damping
        self._converged: Dict[Node, bool] = {}

    def add(self, new_node: Node) -> None:
        self._converged[new_node] = False
        self._jump_factor = (1-self.damping)/len(self._converged)

    def print_scores(self):
        print("Scores:")
        for node in self._converged.keys():
            print(f"{node.name}: score:{node.score:.2f}")

    def run(self, max_iterations: int = 100):
        count = 0
        while(count < max_iterations and not all(self._converged.values())):
            for node in self._converged.keys():
                if self._converged[node]:
                    continue

                new_score = (
                    self._jump_factor
                    + self.damping
                    * sum([n.score / n.outgoing for n in node.parents()])
                )

                stop = node.update(new_score, self.epsilon)
                self._converged[node] = stop

            for node in self._converged.keys():
                node.release()

            count += 1

        self.print_scores()
        print(f"\nIterations:{count}")


def main():
    a = Node(1)
    b = Node(2)
    c = Node(3)
    d = Node(4)
    e = Node(5)

    a.connect(b)
    b.connect(c); b.connect(e)
    c.connect(a)
    d.connect(e)
    e.connect(e)

    ranker = PageRank()
    ranker.add(a); ranker.add(b); ranker.add(c); ranker.add(d); ranker.add(e)

    ranker.run()


if __name__ == "__main__":
    main()
