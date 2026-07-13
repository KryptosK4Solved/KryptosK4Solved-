import string

def caesar_shift(text, shift):
    """
    Shifts text by N positions in the alphabet using Caesar cipher.
    
    Args:
        text: Input text to shift
        shift: Number of positions to shift (0-25)
    
    Returns:
        Shifted text with non-alphabetic characters preserved
    """
    alphabet = string.ascii_uppercase
    shifted = ""
    for ch in text:
        if ch in alphabet:
            idx = (alphabet.index(ch) + shift) % 26
            shifted += alphabet[idx]
        else:
            shifted += ch
    return shifted


def syllable_score(text, syllables):
    """
    Scores decryption based on matching syllables/keywords.
    
    Args:
        text: Text to analyze
        syllables: List of syllables/keywords to search for
    
    Returns:
        Tuple of (score, list of found syllables)
    """
    score = 0
    found = []
    for s in syllables:
        if s in text:
            score += 1
            found.append(s)
    return score, found


def analyze_cipher(cipher, syllables, max_shift=25):
    """
    Brute-force Caesar cipher analysis.
    Tests all possible shifts and ranks by syllable matches.
    
    Args:
        cipher: Encrypted text
        syllables: List of known syllables to look for
        max_shift: Maximum shift to test (default 25)
    
    Returns:
        Sorted list of (shift, decrypted_text, score, found_syllables)
    """
    results = []
    for shift in range(max_shift + 1):
        shifted = caesar_shift(cipher, shift)
        score, found = syllable_score(shifted, syllables)
        if score > 0:
            results.append((shift, shifted, score, found))
    return sorted(results, key=lambda x: -x[2])


def brute_force_all(cipher, max_shift=25):
    """
    Returns all possible Caesar cipher decryptions without filtering.
    Useful for manual inspection.
    
    Args:
        cipher: Encrypted text
        max_shift: Maximum shift to test
    
    Returns:
        List of (shift, decrypted_text)
    """
    results = []
    for shift in range(max_shift + 1):
        shifted = caesar_shift(cipher, shift)
        results.append((shift, shifted))
    return results


# Example usage
if __name__ == "__main__":
    cipher = "QXPKFCKSHXGIEOQEHLDSBTGTWAYV"
    syllables = ["WAY", "MET", "NET", "LET", "CAT", "DOG"]  # expand as needed
    
    print("═" * 70)
    print("CAESAR CIPHER ANALYZER")
    print("═" * 70)
    print(f"\nCipher: {cipher}\n")
    
    results = analyze_cipher(cipher, syllables)
    
    if results:
        print("Results ranked by syllable matches:\n")
        for r in results:
            print(f"Shift {r[0]:2d} → {r[1]} | Score {r[2]} | Found {r[3]}")
    else:
        print("No syllable matches found. Showing all possibilities:\n")
        all_shifts = brute_force_all(cipher)
        for shift, text in all_shifts:
            print(f"Shift {shift:2d} → {text}")
    
    print("\n" + "═" * 70)
    print("#79 BTC")
    print("═" * 70)
