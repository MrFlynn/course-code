## twos_complement

Converts two's complement binary numbers to decimal and vise versa. You will need
need [Rust](https://rust-lang.org) installed in order to build the utility.

Build the Script:
```bash
$ cd CS-Utilities/twos_complement/
$ cargo build
```

Example Usage:
```bash
$ ./target/debug/convert
Converts two's complement binary to decimal and vise-versa.
Usage:
    ./convert [OPTION] [VALUE]

Options:
    -c  converts from two's complement
    -d  converts from decimal

$ ./target/debug/convert -c 111
-1
```