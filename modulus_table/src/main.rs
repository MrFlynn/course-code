// Modulus Table Generator
// Nick Pleatsikas <nick@pleatsikas.me>

// Use clap for argument parsing.
#[macro_use]
extern crate clap;
use clap::App;

// Output formatting.
extern crate colored;
use colored::*;

// Include process.
use std::process::exit;

// Include file related libraries.
use std::error::Error;
use std::io::prelude::*;
use std::fs::File;
use std::path::Path;

fn create_multiplication_table(size: usize) -> Vec<Vec<i32>> {
    // Create empty vector of specific size containing all zeros.
    let mut table = vec![vec![0; size]; size];

    for i in 0..size {
        for j in 0..size {
            // Generate modulus values.
            let value = ((i + 1) * (j + 1)) % (size + 1);
            table[i][j] = value as i32;       
        }
    }

    table
}

fn create_inverse_table(lookup: &Vec<Vec<i32>>) -> Vec<i32> {
    let mut table = Vec::new();

    for row in lookup.iter() {
        // Lookup horizontal index of value such that i * j = 1.
        let index = row.iter().position(|&j| j == 1).unwrap() + 1;
        table.push(index as i32);
    }

    table
}

fn vec_to_string(vect: Vec<i32>, sep: String) -> String {
    // Map over vector and turn all integers to strings and then join them.
    let transform: Vec<String> = vect.iter().map(|&i| i.to_string()).collect();
    let range_str: String = transform.join(&sep);

    range_str
}

fn print_multiplication_table(table: &Vec<Vec<i32>>) {
    // Generate top-most row of multiplication table.
    let header_range: Vec<i32> = (1..((table.len() as i32) + 1)).collect();
    let header_range_str: String = vec_to_string(header_range, " ".to_string());

    // Print the first row.
    println!("{}{}", " |".underline(), header_range_str.underline().bold());

    // Print all subsequent rows of the multiplication table.
    for (i, row) in table.iter().enumerate() {
        let row_str: String = vec_to_string(row.to_vec(), " ".to_string());
        println!("{}|{}", (i + 1).to_string().bold(), row_str);
    }
}

fn print_inverse_table(table: &Vec<i32>) {
    // Generate top-most row of inverses table.
    let header_range: Vec<i32> = (1..((table.len() as i32) + 1)).collect();
    let header_range_str: String = vec_to_string(header_range, " ".to_string());

    // Print header row and inverses table.
    println!("{}{}",  "    |".underline(), header_range_str.underline().bold());
    println!("{}|{}",  "x^-1".bold(), vec_to_string(table.to_vec(), 
                                                    " ".to_string()));
}

fn output_csv(contents: String, filename: String) {
    // Set and store path.
    let path = Path::new(&filename);
    let disp = path.display();

    let mut file = match File::create(&path) {
        // Check for file creation permission.
        Err(why) => panic!("Couldn't create {}: {}", disp, why.description()),
        Ok(file) => file,
    };

    match file.write_all(contents.as_bytes()) {
        // Check for write permissions.
        Err(why) => panic!("Couldn't write to {}: {}", disp, why.description()),
        Ok(_) => println!("Wrote to {}", disp),
    }
}

fn main() {
    // Load yaml file containing all CLI options and parse.
	let yaml = load_yaml!("cli.yml");
    let matches = App::from_yaml(yaml).get_matches();
    
    // Create variable that contains the base for the table. 
    let mod_base: usize;
    
    // Panic if base value was not provided
    if let Some(base) = matches.value_of("base") {
        mod_base = base.parse::<usize>().unwrap();
    } else {
        println!("No base provided. Run modulus_table --help.");
        exit(1);
    }

    // Create multiplicative and inverses table.
    let table = create_multiplication_table(mod_base - 1);
    let inv = create_inverse_table(&table);

    // If the CSV switch is present, silence ouput and dump contents to csv.
    if matches.is_present("csv") {
        // Create string to store contents of multiplication table.
        let mut mult_table_str: String = String::new();

        for row in table.iter() {
            // Get row into CSV format.
            let row_str: String = vec_to_string(row.to_vec(), ",".to_string());

            // Append new row to output string.
            mult_table_str.push_str(row_str.as_str());
            mult_table_str.push_str("\n");
        }

        // Output the multiplication table to csv.
        output_csv(mult_table_str, "table.csv".to_string());

        // Output the inverse table to csv.
        output_csv(vec_to_string(inv, ",".to_string()), "inv.csv".to_string());
    } else {
        // Print tables to terminal.
        print_multiplication_table(&table);
        println!("");
        print_inverse_table(&inv);
    }
}
