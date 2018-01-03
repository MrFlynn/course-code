// Use getopts crate.
extern crate getopts;
use getopts::Options;

// Enable ENV parsing.
use std::env;

// Negate numbers.
use std::ops::Neg;

fn print_help() {
    let helpdoc = "Converts two's complement binary to decimal and vise-versa.\
                    \n\
                    Usage:\n\
                    \t./convert [OPTION] [VALUE]\n\
                    \n\
                    Options:\n\
                    \t-c\tconverts from two's complement\n\
                    \t-d\tconverts from decimal\n\
                    \n";
    print!("{}", helpdoc);
}

fn invert_bits(input_str: String) -> i32 {
    // Allocate new string.
    let mut inv = String::new();

    // Iterate through each character in the string and 'invert' each bit.
    for c in input_str.chars() {
        match c {
            '0' => inv.push('1'),
            _   => inv.push('0')
        }
    }

    // Return the base-10 integer.
    !i32::from_str_radix(&inv, 2).unwrap()
}

fn decimal_to_bin(input_str: String) {
    // Check if first character in string is a minus sign.
    let value = match input_str.chars().nth(0).unwrap() {
        '-' => Neg::neg(input_str[1..].parse::<i32>().unwrap()),
        _   => input_str.parse::<i32>().unwrap()
    };

    // If the value is positive then output a leading zero.
    if value >= 0 {
        println!("0{:b}", value);
    } else {
        println!("{:b}", value);
    }
}

fn bin_to_decimal(input_str: String) {
    // Output based on the value of the first bit.
    match input_str.chars().nth(0).unwrap() {
        '1' => println!("{}", invert_bits(input_str)),
        _   => println!("{}", i32::from_str_radix(&input_str, 2).unwrap())
    };
}

fn main() {
    // Get all arguments.
    let args: Vec<String> = env::args().collect();

    // Instantiate command options.
    let mut options = Options::new();
    options.optflag("c", "", "Converts to decimal from two's complement.");
    options.optflag("d", "", "Converts to two's complement from decimal.");

    // Create matches.
    let matches = match options.parse(&args[1..]) {
        Ok(m)  => { m }
        Err(f) => { panic!(f.to_string()) }
    };

    if matches.opt_present("c") {
        // Grab the argument's value and pass to `bin_to_decimal` function.
        bin_to_decimal(matches.free[0].clone())
    } else if matches.opt_present("d") {
        // Grab the argument's value and pass to `decimal_to_bin` function.
        decimal_to_bin(matches.free[0].clone());
    } else {
        // Print usage.
        print_help();
    }
}