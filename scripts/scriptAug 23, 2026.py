```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Semantic Line Deduplicator:
A single-file Python utility to remove semantically duplicate lines from a text file.
It processes lines by applying a normalization function (e.g., stripping whitespace,
converting to lowercase) to determine uniqueness. The *original* first-seen unique
lines are then outputted.

Usage:
    python3 semantic_deduplicator.py <input_file> [output_file] [--count-only]

Arguments:
    <input_file>     : Path to the input text file.
    [output_file]    : Optional path to write the deduplicated output. If not provided,
                       output is printed to standard output.
    --count-only     : If present, only prints the count of unique lines found,
                       without writing or printing the lines themselves.

Example:
    # Deduplicate example.txt and print to console
    python3 semantic_deduplicator.py example.txt

    # Deduplicate example.txt and save to unique_example.txt
    python3 semantic_deduplicator.py example.txt unique_example.txt

    # Count unique lines in example.txt
    python3 semantic_deduplicator.py example.txt --count-only
"""

import sys
import os # Used for checking file existence and type

def _normalize_line(line: str) -> str:
    """
    Applies a standardization process to a line to make it comparable for uniqueness.
    By default, it strips leading/trailing whitespace and converts the line to
    lowercase. This function can be modified to implement different normalization
    strategies (e.g., removing all whitespace, ignoring specific characters, etc.).

    Args:
        line (str): The input line string.

    Returns:
        str: The normalized version of the line.
    """
    # Simple normalization: strip leading/trailing whitespace and convert to lowercase.
    # This treats " Hello World " and "hello world" as semantically identical.
    return line.strip().lower()

def deduplicate_file(input_filepath: str, output_filepath: str = None, count_only: bool = False) -> int:
    """
    Reads an input file, identifies unique lines based on a normalization function,
    and then either writes the original unique lines to an output file/stdout
    or just returns their count.

    Args:
        input_filepath (str): The path to the file to be processed.
        output_filepath (str, optional): The path to the file where unique lines
                                         will be written. If None, output goes to stdout.
                                         Defaults to None.
        count_only (bool, optional): If True, only the count of unique lines is
                                     returned/printed, no lines are outputted.
                                     Defaults to False.

    Returns:
        int: The total number of unique lines found, or -1 if an error occurred.
    """
    seen_normalized_lines = set()  # Stores normalized versions of lines already encountered.
    original_unique_lines = []     # Stores the *original* lines that are unique in order of appearance.

    try:
        # Open the input file for reading with UTF-8 encoding.
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            for line_num, line in enumerate(infile, 1):
                # Normalize the current line for comparison.
                normalized_line = _normalize_line(line)

                # Check if the normalized line has been seen before.
                if normalized_line not in seen_normalized_lines:
                    seen_normalized_lines.add(normalized_line)
                    # If it's unique, store the *original* line.
                    original_unique_lines.append(line)
        
        # If the 'count_only' flag is set, print the count and return.
        if count_only:
            print(f"Total unique lines found: {len(original_unique_lines)}")
            return len(original_unique_lines)

        # Handle output based on whether an output file was specified.
        if output_filepath:
            # Write unique lines to the specified output file.
            with open(output_filepath, 'w', encoding='utf-8') as outfile:
                for unique_line in original_unique_lines:
                    outfile.write(unique_line)
            print(f"Deduplicated {len(original_unique_lines)} unique lines to '{output_filepath}'.")
        else:
            # Print unique lines to standard output.
            for unique_line in original_unique_lines:
                sys.stdout.write(unique_line)
            # Add a newline for cleaner terminal output after all lines are printed.
            sys.stdout.write(f"\nPrinted {len(original_unique_lines)} unique lines to stdout.\n")

        return len(original_unique_lines)

    except FileNotFoundError:
        # Handle the case where the input file does not exist.
        sys.stderr.write(f"Error: Input file '{input_filepath}' not found.\n")
        return -1
    except Exception as e:
        # Catch any other unexpected errors during file processing.
        sys.stderr.write(f"An error occurred during file processing: {e}\n")
        return -1

def main():
    """
    Parses command-line arguments and orchestrates the file deduplication process.
    """
    args = sys.argv[1:] # Get command-line arguments, excluding the script name itself.

    # Basic argument validation.
    if not args or len(args) > 3:
        # Print the module's docstring (which includes usage instructions) if arguments are invalid.
        print(__doc__)
        sys.exit(1)

    input_file = args[0]
    output_file = None
    count_only = False

    # Parse optional arguments: output file and --count-only flag.
    if len(args) >= 2:
        if args[-1] == '--count-only':
            count_only = True
            # If --count-only is the only extra argument, no output file is specified.
            if len(args) == 3: # If there's an output file AND --count-only
                output_file = args[1]
        elif len(args) == 2: # If there are exactly two args and the second isn't --count-only, it's the output file.
            output_file = args[1]
        else: # More than 3 args or invalid combination
            print("Error: Invalid argument combination.\n")
            print(__doc__)
            sys.exit(1)

    # Validate input file existence and type.
    if not os.path.exists(input_file):
        sys.stderr.write(f"Error: Input file '{input_file}' does not exist.\n")
        sys.exit(1)
    if not os.path.isfile(input_file):
        sys.stderr.write(f"Error: Input path '{input_file}' is not a file.\n")
        sys.exit(1)

    # Execute the deduplication process.
    result = deduplicate_file(input_file, output_file, count_only)
    if result == -1:
        sys.exit(1) # Exit with an error code if the deduplication failed.

# This block ensures that main() is called only when the script is executed directly.
if __name__ == "__main__":
    main()
```