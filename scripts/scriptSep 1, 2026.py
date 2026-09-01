```python
import sys
import math

def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculates the Levenshtein distance between two strings.
    The Levenshtein distance is a metric for measuring the difference between two sequences.
    It is the minimum number of single-character edits (insertions, deletions, or substitutions)
    required to change one word into the other.

    Args:
        s1 (str): The first string.
        s2 (str): The second string.

    Returns:
        int: The Levenshtein distance between s1 and s2.
    """
    # Handle edge cases: if strings are identical, no edits needed.
    if s1 == s2:
        return 0
    # If one string is empty, the distance is the length of the other.
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)

    # Initialize a matrix (dynamic programming table) to store the distances.
    # dp[i][j] will represent the Levenshtein distance between s1[:i] and s2[:j].
    rows = len(s1) + 1
    cols = len(s2) + 1
    dp = [[0 for _ in range(cols)] for _ in range(rows)]

    # Initialize the first row and column.
    # The distance from an empty string to a string of length 'i' is 'i' (i deletions/insertions).
    for i in range(rows):
        dp[i][0] = i
    for j in range(cols):
        dp[0][j] = j

    # Fill the matrix using the Levenshtein recurrence relation.
    for i in range(1, rows):
        for j in range(1, cols):
            # Cost of substitution: 0 if characters are the same, 1 otherwise.
            cost = 0 if s1[i-1] == s2[j-1] else 1

            # The current cell dp[i][j] is the minimum of three possibilities:
            # 1. Deletion: dp[i-1][j] + 1 (deleting s1[i-1] to match s2[:j])
            # 2. Insertion: dp[i][j-1] + 1 (inserting s2[j-1] to match s1[:i])
            # 3. Substitution: dp[i-1][j-1] + cost (substituting s1[i-1] with s2[j-1])
            dp[i][j] = min(dp[i-1][j] + 1,      # Deletion
                           dp[i][j-1] + 1,      # Insertion
                           dp[i-1][j-1] + cost) # Substitution

    # The bottom-right cell contains the final Levenshtein distance between s1 and s2.
    return dp[rows-1][cols-1]

def calculate_similarity_percentage(distance: int, max_len: int) -> float:
    """
    Calculates a simple similarity percentage based on Levenshtein distance.
    The percentage is derived from how 'different' the strings are relative
    to the maximum possible difference (which is the length of the longer string).

    Args:
        distance (int): The Levenshtein distance between two strings.
        max_len (int): The maximum length of the two strings being compared.

    Returns:
        float: A similarity percentage (0.0 to 100.0).
    """
    # If max_len is 0 (both strings were empty), they are 100% similar.
    if max_len == 0:
        return 100.0
    # Formula: (1 - (distance / max_possible_distance)) * 100
    # max_possible_distance is typically the length of the longer string.
    return (1 - (distance / max_len)) * 100.0

def find_best_match(target_string: str, candidates: list[str]) -> tuple[str, int, float]:
    """
    Finds the best matching string from a list of candidates for a given target string
    using Levenshtein distance.

    Args:
        target_string (str): The string to find a match for.
        candidates (list[str]): A list of strings to compare against.

    Returns:
        tuple[str, int, float]: A tuple containing:
            - The best matching candidate string.
            - Its Levenshtein distance to the target string.
            - Its similarity percentage to the target string.
        Returns ("", -1, 0.0) if the candidates list is empty.
    """
    if not candidates:
        return "", -1, 0.0

    best_match = ""
    min_distance = float('inf')  # Initialize with a very large distance
    best_similarity = 0.0

    # Iterate through each candidate to find the one with the smallest distance
    for candidate in candidates:
        distance = levenshtein_distance(target_string, candidate)
        
        # Calculate maximum length for similarity percentage calculation
        max_len = max(len(target_string), len(candidate))
        
        # Calculate similarity for the current candidate
        similarity = calculate_similarity_percentage(distance, max_len)

        # If the current candidate has a smaller distance, update the best match
        if distance < min_distance:
            min_distance = distance
            best_match = candidate
            best_similarity = similarity
        # Optional: If distances are equal, you might add logic to break ties
        # (e.g., prefer shorter string, or lexicographically smaller).
        # For this script, the first one found with the minimum distance is kept.

    return best_match, min_distance, best_similarity

if __name__ == "__main__":
    # --- Configuration: Default list of candidate strings ---
    # This list can be loaded from a file or another source in a real application.
    default_candidates = [
        "apple", "aple", "apply", "banana", "bandana", "orange",
        "grapefruit", "pineapple", "apricot", "strawberry", "blueberry",
        "raspberry", "blackcurrant", "avocado", "kiwi", "lemon", "lime",
        "mango", "peach", "pear", "plum", "cherry", "watermelon",
        "cantaloupe", "honeydew", "pomegranate", "fig", "date", "coconut"
    ]

    # --- Input Handling: Get target string from command line or user input ---
    target_input = ""
    if len(sys.argv) > 1:
        # If command-line arguments are provided, use the first one as the target string.
        target_input = sys.argv[1]
        print(f"Searching for best match for: '{target_input}' (from command line)")
    else:
        # Otherwise, prompt the user for input.
        print("--- Fuzzy String Matcher Utility ---")
        print("This script finds the closest match for a given string from a predefined list.")
        print("Usage: python fuzzy_match_utility.py \"your search term\"")
        print("Or enter it interactively below.")
        target_input = input("Enter target string: ").strip()

    # Exit if no target string is provided.
    if not target_input:
        print("No target string provided. Exiting.")
        sys.exit(1)

    # --- Find Best Match ---
    best_match_str, distance, similarity_percentage = find_best_match(
        target_input, default_candidates
    )

    # --- Output Results ---
    if distance == -1: # Indicates an empty candidates list was passed
        print("Error: No candidates provided to search within.")
    else:
        print("\n--- Match Results ---")
        print(f"Target String:        '{target_input}'")
        print(f"Best Matching Candidate: '{best_match_str}'")
        print(f"Levenshtein Distance: {distance}")
        print(f"Similarity Percentage: {similarity_percentage:.2f}%")

        # Provide a human-readable interpretation of the similarity.
        if similarity_percentage >= 90.0:
            print(f"\n'{target_input}' is an excellent match for '{best_match_str}'.")
        elif similarity_percentage >= 70.0:
            print(f"\n'{target_input}' is a good match for '{best_match_str}'.")
        elif similarity_percentage >= 40.0:
            print(f"\n'{target_input}' is a fair match for '{best_match_str}'.")
        else:
            print(f"\n'{target_input}' is a weak match for '{best_match_str}'.")
            print("Consider trying a different search term.")
```