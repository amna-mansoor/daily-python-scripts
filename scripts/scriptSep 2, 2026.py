```python
import os
import argparse
import sys

# --- Constants for ASCII art visualization ---
# These strings are used to draw the tree structure in the console.
SPACE = '    '      # Used for indentation level
BRANCH = '├── '     # Connects to a child that has more siblings after it
LAST_BRANCH = '└── ' # Connects to a child that is the last sibling
VERTICAL = '│   '   # Extends the vertical line for parent's siblings
EMPTY = ''         # Used for the root level indentation

def _get_sorted_contents(path, ignore_patterns):
    """
    Helper function to scan a directory and return its sorted contents (files and subdirectories).
    Applies ignore patterns to filter out unwanted entries.

    Args:
        path (str): The path to the directory to scan.
        ignore_patterns (list): A list of strings (names or partial names) to ignore.

    Returns:
        list: A sorted list of tuples, where each tuple is (entry_name, is_directory).
              Returns an empty list if the path is not found or permissions are denied.
    """
    contents = []
    try:
        # Use os.scandir for better performance than os.listdir
        with os.scandir(path) as it:
            # Sort entries alphabetically for consistent output
            for entry in sorted(it, key=lambda e: e.name.lower()):
                # Check if the entry name matches any ignore pattern
                # This allows ignoring files/dirs with specific substrings in their names
                if any(p in entry.name for p in ignore_patterns):
                    continue # Skip this entry if it matches an ignore pattern

                if entry.is_dir():
                    contents.append((entry.name, True))
                elif entry.is_file():
                    contents.append((entry.name, False))
    except PermissionError:
        print(f"Error: Permission denied to access '{path}'. Skipping.", file=sys.stderr)
    except FileNotFoundError:
        print(f"Error: Path not found '{path}'. Skipping.", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred while scanning '{path}': {e}", file=sys.stderr)
    return contents

def _print_tree_recursive(current_path, indent, ignore_patterns, max_depth, current_depth):
    """
    Recursively prints the directory tree structure.

    Args:
        current_path (str): The current directory path being processed.
        indent (str): The current indentation string (e.g., "│   │   ").
        ignore_patterns (list): List of patterns to ignore.
        max_depth (int/float): Maximum depth to traverse. float('inf') for unlimited.
        current_depth (int): The current depth in the tree, starting from 0 for the root's children.
    """
    # Stop recursion if maximum depth is reached
    if current_depth > max_depth:
        return

    # Get contents of the current directory, applying ignore patterns
    contents = _get_sorted_contents(current_path, ignore_patterns)
    num_contents = len(contents)

    for i, (name, is_dir) in enumerate(contents):
        is_last = (i == num_contents - 1) # Check if this is the last item in the current directory

        # Determine the correct branch prefix based on whether it's the last sibling
        branch_prefix = LAST_BRANCH if is_last else BRANCH

        # Print the current file or directory with its appropriate indentation and prefix
        print(f"{indent}{branch_prefix}{name}")

        if is_dir:
            # Calculate the new indentation for children of this directory
            # If this directory is the last sibling, its children will be indented with SPACE.
            # Otherwise, they will continue the VERTICAL line of the parent.
            new_indent = indent + (SPACE if is_last else VERTICAL)

            # Recursively call this function for the subdirectory
            _print_tree_recursive(
                os.path.join(current_path, name), # Path to the subdirectory
                new_indent,                        # New indentation for children
                ignore_patterns,
                max_depth,
                current_depth + 1                  # Increment depth for the next level
            )

def print_directory_tree(root_path, ignore_patterns=None, max_depth=float('inf')):
    """
    Generates and prints an ASCII art representation of a directory tree.

    Args:
        root_path (str): The starting directory path for the tree visualization.
        ignore_patterns (list, optional): A list of file/directory names or partial names to ignore.
                                         Defaults to an empty list.
        max_depth (int/float, optional): The maximum depth to display. Defaults to float('inf') for
                                         unlimited depth. Use 0 to only show the root, 1 for root
                                         and its immediate children, etc.
    """
    # Ensure ignore_patterns is a list if not provided
    if ignore_patterns is None:
        ignore_patterns = []

    # Check if the root path exists
    if not os.path.exists(root_path):
        print(f"Error: The specified path '{root_path}' does not exist.", file=sys.stderr)
        return

    # Print the name of the root directory itself
    # os.path.abspath ensures a consistent path for the root display
    print(os.path.basename(os.path.abspath(root_path)))

    # Start the recursive tree printing process from the root's children
    # The initial indent is empty, and current_depth starts at 0 for the root's children.
    _print_tree_recursive(root_path, EMPTY, ignore_patterns, max_depth, 0)

if __name__ == "__main__":
    # Set up argument parsing for the command-line interface
    parser = argparse.ArgumentParser(
        description="Generates an ASCII art representation of a directory tree."
    )
    
    # Positional argument for the root path (defaults to current directory)
    parser.add_argument(
        "path",
        nargs="?",  # Makes the argument optional
        default=".", # Defaults to the current directory if not provided
        help="The root directory to visualize (defaults to current directory)."
    )
    
    # Optional argument to specify patterns to ignore
    parser.add_argument(
        "-i", "--ignore",
        nargs="*", # Allows zero or more arguments for ignore patterns
        # Default ignore patterns for common development artifacts
        default=[
            ".git", "__pycache__", ".DS_Store", ".pytest_cache", ".idea",
            "*.pyc", "venv", "env", "node_modules", "target", "build", ".vscode"
        ],
        help="List of file/directory names or partial names to ignore. "
             "Defaults to common development patterns. "
             "E.g., --ignore .git venv *.log"
    )
    
    # Optional argument to limit the depth of the tree
    parser.add_argument(
        "-d", "--depth",
        type=int,
        default=-1, # -1 signifies infinite depth (no limit)
        help="Maximum depth to display (0 for root only, 1 for root and its immediate children, etc.). "
             "Use -1 for unlimited depth (default)."
    )

    args = parser.parse_args()

    # Convert the depth argument: -1 means infinite depth
    max_depth_val = args.depth if args.depth >= 0 else float('inf')

    # Resolve the root path to an absolute path for clarity and consistency
    root_dir = os.path.abspath(args.path)

    # Call the main function to print the directory tree
    print_directory_tree(root_dir, args.ignore, max_depth_val)
```