```python
import re
import argparse
import sys

# --- Utility Functions for Text Processing ---

def _tokenize_sentences(text: str) -> list[str]:
    """
    Splits the input text into a list of sentences.
    Uses a regular expression to find common sentence terminators
    (. ! ?) followed by a space or end of string.
    Handles multiple terminators (e.g., "Hello!!!").

    Note: This is a simplified tokenizer. For highly accurate sentence
    tokenization, especially with complex texts or abbreviations,
    libraries like NLTK are recommended. This utility aims for simplicity
    and no external dependencies.
    """
    # Pattern: finds a sequence of one or more sentence-ending punctuation marks
    # (period, exclamation, question mark) followed by a whitespace character
    # that is not a newline, or the end of the string.
    # The `(?<=[.!?])` is a positive lookbehind ensuring the split occurs
    # *after* the punctuation but doesn't include it in the split result.
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Filter out empty strings that might result from splitting and strip whitespace
    return [s.strip() for s in sentences if s.strip()]

def _tokenize_words(text: str) -> list[str]:
    """
    Splits the input text into a list of words.
    Converts words to lowercase and removes non-alphanumeric characters.
    A "word" is defined as a sequence of one or more alphabetic characters.
    """
    # Pattern: finds sequences of one or more letters (alphabetic characters).
    # This ignores numbers, punctuation, hyphens, etc., focusing purely on "words".
    words = re.findall(r'[a-z]+', text.lower())
    return words

# --- Main Analysis Function ---

def analyze_text_metrics(text_content: str) -> dict:
    """
    Analyzes the provided text content and calculates various linguistic metrics.

    Args:
        text_content: The string content of the text to be analyzed.

    Returns:
        A dictionary containing the calculated metrics:
        - 'total_words': Total number of words.
        - 'unique_words': Number of unique words.
        - 'total_sentences': Total number of sentences.
        - 'avg_words_per_sentence': Average number of words per sentence.
        - 'avg_chars_per_word': Average number of characters per word (excluding non-alphabetic).
        - 'lexical_diversity': Ratio of unique words to total words.
    """
    if not text_content:
        # Return default zero metrics for empty input
        return {
            'total_words': 0,
            'unique_words': 0,
            'total_sentences': 0,
            'avg_words_per_sentence': 0.0,
            'avg_chars_per_word': 0.0,
            'lexical_diversity': 0.0,
        }

    sentences = _tokenize_sentences(text_content)
    words = _tokenize_words(text_content)
    unique_words = set(words) # Use a set to easily count unique words

    total_words = len(words)
    total_sentences = len(sentences)
    num_unique_words = len(unique_words)

    # Calculate average words per sentence
    # Avoid division by zero if no sentences are found
    avg_words_per_sentence = total_words / total_sentences if total_sentences else 0.0

    # Calculate average characters per word
    # Sum of lengths of all words (as defined by _tokenize_words)
    total_chars = sum(len(word) for word in words)
    # Avoid division by zero if no words are found
    avg_chars_per_word = total_chars / total_words if total_words else 0.0

    # Calculate lexical diversity (ratio of unique words to total words)
    # Avoid division by zero if no words are found
    lexical_diversity = num_unique_words / total_words if total_words else 0.0

    return {
        'total_words': total_words,
        'unique_words': num_unique_words,
        'total_sentences': total_sentences,
        'avg_words_per_sentence': avg_words_per_sentence,
        'avg_chars_per_word': avg_chars_per_word,
        'lexical_diversity': lexical_diversity,
    }

# --- Command Line Interface (CLI) ---

def main():
    """
    Parses command-line arguments, reads text from a file or a direct string,
    analyzes it using the `analyze_text_metrics` function, and prints the results.
    """
    parser = argparse.ArgumentParser(
        description="Analyze linguistic metrics of a given text (e.g., word count, "
                    "sentence count, lexical diversity).",
        formatter_class=argparse.RawTextHelpFormatter # For better formatting of help message
    )
    parser.add_argument(
        '-f', '--file',
        type=str,
        help="Path to a text file to analyze. E.g., `python script.py -f document.txt`"
    )
    parser.add_argument(
        '-t', '--text',
        type=str,
        help="Direct text string to analyze. Enclose in quotes if it contains spaces.\n"
             "E.g., `python script.py -t \"Hello world! This is a test.\"`"
    )

    args = parser.parse_args()

    text_to_analyze = ""

    # Determine text source: file or direct string
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text_to_analyze = f.read()
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.", file=sys.stderr)
            sys.exit(1) # Exit with an error code
        except Exception as e:
            print(f"Error reading file '{args.file}': {e}", file=sys.stderr)
            sys.exit(1)
    elif args.text:
        text_to_analyze = args.text
    else:
        # If neither file nor text is provided, show error and help
        print("Error: Please provide either a file path (-f/--file) or a text string (-t/--text).", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)

    if not text_to_analyze.strip():
        # Handle empty input gracefully
        print("Warning: The provided text or file is empty. No metrics to calculate.", file=sys.stderr)
        sys.exit(0) # Exit successfully, but with a warning

    # Perform the analysis
    metrics = analyze_text_metrics(text_to_analyze)

    # Print the results in a formatted way
    print("\n--- Text Linguistic Metrics ---")
    print(f"Total Words:          {metrics['total_words']}")
    print(f"Unique Words:         {metrics['unique_words']}")
    print(f"Total Sentences:      {metrics['total_sentences']}")
    print(f"Avg. Words/Sentence:  {metrics['avg_words_per_sentence']:.2f}") # Format to 2 decimal places
    print(f"Avg. Chars/Word:      {metrics['avg_chars_per_word']:.2f}")    # Format to 2 decimal places
    print(f"Lexical Diversity:    {metrics['lexical_diversity']:.3f}")   # Format to 3 decimal places (ratio)

# --- Script Entry Point ---

if __name__ == "__main__":
    # This block ensures that `main()` is called only when the script is executed directly,
    # not when it's imported as a module into another script.
    main()
```