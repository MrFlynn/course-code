from typing import Mapping, Tuple

Store = Mapping[str, Tuple[int, str]]


def stringToStore(s: str) -> Store:
    m: Store = {}

    for line in s.splitlines():
        if len(fields := line.split(",")) > 2:
            m[fields[0].strip()] = (int(fields[1]), fields[2])

    return m


def storeToString(s: Store) -> str:
    return "\n".join([f"{k},{v[0]},{v[1]}" for k, v in s.items()])


def combineStores(x: Store, y: Store) -> Store:
    m: Store = {}

    def iterStore(s: Store) -> None:
        for k, v in s.items():
            if k in m:
                m[k] = (m[k][0] + v[0], v[1])
            else:
                m[k] = (v[0], v[1])

    iterStore(x)
    iterStore(y)

    return m


def sortStore(m: Store) -> Store:
    return {k: v for k, v in sorted(m.items(), key=lambda item: item[1][0])}


def main() -> None:
    s1 = """hello,2,hi
	Blah,4,bleh
	Foo,6,bar"""

    s2 = """hello,4,hi
	Blah,6,bleh
	Baz,7,fizz"""

    x = stringToStore(s1)
    y = stringToStore(s2)

    m = sortStore(combineStores(x, y))

    print(storeToString(m))


if __name__ == "__main__":
    main()
