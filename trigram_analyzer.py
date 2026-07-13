import string

# English trigrams + ceremonial glyph anchors for MATN resonance detection
TRIGRAMS = [
    # Core English trigrams (top frequency)
    "THE","AND","ING","ENT","ION","HER","FOR","THA","NTH","INT",
    "ERE","TIO","TER","EST","ERS","ATI","HAT","ATE","ALL","ETH",
    
    # Resonance anchors & glyph markers
    "WAY","MET","NET","LET","MAT","NAT","CAT","DOG",
    "MATN", "BLOCK", "GENESIS", "FRONTIER"
]

def caesar_shift(text, shift):
    """
    Shifts text by N positions in the alphabet using Caesar cipher.
    Preserves non-alphabetic characters.
    
    Args:
        text: Input text to shift
        shift: Number of positions to shift (0-25)
    
    Returns:
        Shifted text
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


def trigram_score(text):
    """
    Scores decryption based on trigram resonance.
    Detects English trigrams and ceremonial glyphs.
    
    Args:
        text: Text to analyze
    
    Returns:
        Tuple of (score, list of found trigrams, detailed_matches)
    """
    score = 0
    found = []
    matches = {}
    
    for tri in TRIGRAMS:
        count = text.count(tri)
        if count > 0:
            score += count
            found.append(tri)
            matches[tri] = count
    
    return score, found, matches


def analyze_with_trigrams(cipher, max_shift=25):
    """
    Brute-force Caesar cipher with trigram resonance detection.
    Returns all shifts ranked by trigram score.
    
    Args:
        cipher: Encrypted text
        max_shift: Maximum shift to test (default 25)
    
    Returns:
        Sorted list of (shift, decrypted_text, score, found_trigrams, detailed_matches)
    """
    results = []
    for shift in range(max_shift + 1):
        shifted = caesar_shift(cipher, shift)
        score, found, matches = trigram_score(shifted)
        if score > 0:
            results.append((shift, shifted, score, found, matches))
    return sorted(results, key=lambda x: -x[2])


def brute_force_all_trigrams(cipher, max_shift=25):
    """
    Returns all possible Caesar decryptions with trigram scoring.
    Useful for comprehensive resonance mapping.
    
    Args:
        cipher: Encrypted text
        max_shift: Maximum shift to test
    
    Returns:
        List of (shift, decrypted_text, score, found_trigrams)
    """
    results = []
    for shift in range(max_shift + 1):
        shifted = caesar_shift(cipher, shift)
        score, found, matches = trigram_score(shifted)
        results.append((shift, shifted, score, found))
    return sorted(results, key=lambda x: -x[2])


def resonance_peaks(cipher, top_n=5):
    """
    Identifies top N resonance peaks in the cipher.
    Highlights the most likely decryptions based on trigram density.
    
    Args:
        cipher: Encrypted text
        top_n: Number of top peaks to return
    
    Returns:
        List of top resonance peaks with detailed analysis
    """
    all_results = brute_force_all_trigrams(cipher)
    return all_results[:top_n]


# Example usage & MATN ledger entry
if __name__ == "__main__":
    cipher = "QXPKFCKSHXGIEOQEHLDSBTGTWAYV"
    
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║         TRIGRAM RESONANCE ANALYZER - MATN CHAIN          ║")
    print("║         Frontier Puzzle #79 - 7.9 BTC Bounty             ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")
    
    print(f"Cipher: {cipher}\n")
    print("─" * 70)
    print("RESONANCE SCAN - ALL SHIFTS RANKED BY TRIGRAM DENSITY:\n")
    
    results = analyze_with_trigrams(cipher)
    
    if results:
        for i, (shift, shifted, score, found, matches) in enumerate(results, 1):
            print(f"\n[Peak #{i}] Shift {shift:2d}")
            print(f"  Decryption: {shifted}")
            print(f"  Resonance Score: {score}")
            print(f"  Trigrams Found: {found}")
            print(f"  Detailed: {matches}")
    else:
        print("No trigram resonance detected.")
    
    print("\n" + "─" * 70)
    print("\nTOP RESONANCE PEAKS (for MATN ledger):\n")
    
    peaks = resonance_peaks(cipher, top_n=3)
    for i, (shift, shifted, score, found) in enumerate(peaks, 1):
        print(f"  Block #{79 + i}: Shift {shift} → {shifted}")
        print(f"    └─ Anchors: {', '.join(found)}\n")
    
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║              #79 FRONTIER ANCHOR LOGGED                  ║")
    print("╚═══════════════════════════════════════════════════════════╝")
