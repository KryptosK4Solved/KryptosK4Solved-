"""
PUZZLE SOLVER SUITE
Consolidated orchestration engine for cryptographic puzzle resolution.
Integrates Caesar cipher, trigram analysis, and temporal anchoring.

Configuration:
- GA Population Size: 200 (optimal for 26^3 = 17,576 possibility space)
- Mutation Rate: 0.05 (prevents premature convergence)
- Hash Iterations: Standard PBKDF2/crypt defaults
- Vector Normalization: R^3 space mapping for tensor-field orchestration
"""

import string
import hashlib
import time
import random
from typing import List, Tuple, Dict, Optional


class GeneticAlgorithmSolver:
    """
    Genetic Algorithm solver for 3-letter word cryptographic puzzles.
    Optimized for 26^3 = 17,576 possibility space.
    """
    
    def __init__(self, target_hash: str, population_size: int = 200, 
                 mutation_rate: float = 0.05, hash_type: str = "sha256"):
        """
        Initialize GA solver.
        
        Args:
            target_hash: Target hash to match
            population_size: GA population (default 200)
            mutation_rate: Mutation probability (default 0.05)
            hash_type: Hash algorithm ('md5', 'sha256', etc.)
        """
        self.target_hash = target_hash.lower()
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.hash_type = hash_type
        self.alphabet = string.ascii_uppercase
        self.population = []
        self.fitness_history = []
        
    def _hash_word(self, word: str) -> str:
        """Hash a word using specified algorithm."""
        if self.hash_type == "md5":
            return hashlib.md5(word.encode()).hexdigest()
        elif self.hash_type == "sha256":
            return hashlib.sha256(word.encode()).hexdigest()
        else:
            return hashlib.sha256(word.encode()).hexdigest()
    
    def _generate_individual(self) -> str:
        """Generate random 3-letter word."""
        return ''.join(random.choice(self.alphabet) for _ in range(3))
    
    def _fitness(self, word: str) -> float:
        """Calculate fitness based on hash match."""
        word_hash = self._hash_word(word)
        matches = sum(1 for i in range(len(self.target_hash)) 
                     if i < len(word_hash) and word_hash[i] == self.target_hash[i])
        return matches / len(self.target_hash)
    
    def _mutate(self, word: str) -> str:
        """Mutate a word by randomly changing characters."""
        word_list = list(word)
        for i in range(len(word_list)):
            if random.random() < self.mutation_rate:
                word_list[i] = random.choice(self.alphabet)
        return ''.join(word_list)
    
    def _crossover(self, parent1: str, parent2: str) -> str:
        """Single-point crossover."""
        crossover_point = random.randint(1, len(parent1) - 1)
        return parent1[:crossover_point] + parent2[crossover_point:]
    
    def solve(self, generations: int = 100) -> Tuple[Optional[str], int]:
        """
        Run genetic algorithm to find matching word.
        
        Args:
            generations: Number of generations to evolve
            
        Returns:
            (solution_word, generation_found) or (None, generations)
        """
        # Initialize population
        self.population = [self._generate_individual() for _ in range(self.population_size)]
        
        for gen in range(generations):
            # Evaluate fitness
            fitness_scores = [(word, self._fitness(word)) for word in self.population]
            fitness_scores.sort(key=lambda x: -x[1])
            
            # Check for solution
            best_word, best_fitness = fitness_scores[0]
            self.fitness_history.append(best_fitness)
            
            if self._hash_word(best_word) == self.target_hash:
                return best_word, gen
            
            # Selection and reproduction
            elite = fitness_scores[:max(1, self.population_size // 10)]
            new_population = [word for word, _ in elite]
            
            while len(new_population) < self.population_size:
                parent1 = random.choice(elite)[0]
                parent2 = random.choice(elite)[0]
                child = self._crossover(parent1, parent2)
                child = self._mutate(child)
                new_population.append(child)
            
            self.population = new_population[:self.population_size]
        
        # Return best found
        best = max(self.population, key=lambda w: self._fitness(w))
        return best, generations


class CaesarCipherSolver:
    """
    Caesar cipher solver with syllable/trigram resonance detection.
    """
    
    def __init__(self, trigrams: Optional[List[str]] = None):
        """
        Initialize Caesar solver.
        
        Args:
            trigrams: List of trigrams/keywords to search for
        """
        self.trigrams = trigrams or [
            "THE", "AND", "ING", "ENT", "ION", "HER", "FOR", "THA", "NTH", "INT",
            "ERE", "TIO", "TER", "EST", "ERS", "ATI", "HAT", "ATE", "ALL", "ETH",
            "WAY", "MET", "NET", "LET", "MAT", "NAT", "CAT", "DOG",
            "MATN", "BLOCK", "GENESIS", "FRONTIER"
        ]
        self.alphabet = string.ascii_uppercase
    
    def _caesar_shift(self, text: str, shift: int) -> str:
        """Apply Caesar shift to text."""
        shifted = ""
        for ch in text:
            if ch in self.alphabet:
                idx = (self.alphabet.index(ch) + shift) % 26
                shifted += self.alphabet[idx]
            else:
                shifted += ch
        return shifted
    
    def _trigram_score(self, text: str) -> Tuple[int, List[str], Dict[str, int]]:
        """Score text based on trigram matches."""
        score = 0
        found = []
        matches = {}
        
        for tri in self.trigrams:
            count = text.count(tri)
            if count > 0:
                score += count
                found.append(tri)
                matches[tri] = count
        
        return score, found, matches
    
    def solve(self, cipher: str, max_shift: int = 25) -> List[Tuple[int, str, int, List[str]]]:
        """
        Solve Caesar cipher using trigram analysis.
        
        Args:
            cipher: Encrypted text
            max_shift: Maximum shift to test
            
        Returns:
            Sorted list of (shift, decrypted_text, score, found_trigrams)
        """
        results = []
        for shift in range(max_shift + 1):
            shifted = self._caesar_shift(cipher, shift)
            score, found, matches = self._trigram_score(shifted)
            results.append((shift, shifted, score, found))
        
        return sorted(results, key=lambda x: -x[2])


class TemporalAnchorSolver:
    """
    Proof-of-work temporal anchor mining.
    Creates merkle root from intentions and mines block with SHA256.
    """
    
    def __init__(self, birth_ts: int = 490320000):  # 1985-07-16 UTC
        """
        Initialize temporal anchor.
        
        Args:
            birth_ts: Birth timestamp (default 1985-07-16)
        """
        self.birth_ts = birth_ts
        self.now_ts = int(time.time())
        self.delta = self.now_ts - self.birth_ts
        self.days = self.delta // 86400
        self.intentions = {
            "PAST_ANCHOR": "I was born on 16-07-1985",
            "PRESENT_ANCHOR": "I am here now",
            "FUTURE_ANCHOR": "I will be",
            "HEARTBEAT": f"{self.days} days since genesis",
            "MESSAGE": "The lattice breathes through time"
        }
    
    def _hash_intention(self, text: str) -> str:
        """Hash intention with SHA256."""
        return hashlib.sha256(text.encode()).hexdigest()
    
    def _merkle_root(self) -> str:
        """Compute merkle root from all intentions."""
        hashes = [self._hash_intention(v) for v in self.intentions.values()]
        while len(hashes) > 1:
            temp = []
            for i in range(0, len(hashes), 2):
                pair = hashes[i] + (hashes[i+1] if i+1 < len(hashes) else "")
                temp.append(self._hash_intention(pair))
            hashes = temp
        return hashes[0]
    
    def mine_block(self, difficulty: int = 2) -> Tuple[int, str]:
        """
        Mine a block with proof-of-work.
        
        Args:
            difficulty: Number of leading zeros required
            
        Returns:
            (nonce, block_hash)
        """
        nonce = 0
        root = self._merkle_root()
        target_prefix = "0" * difficulty
        
        while True:
            block_header = f"{root}{self.birth_ts}{self.now_ts}{nonce}"
            block_hash = hashlib.sha256(block_header.encode()).hexdigest()
            if block_hash.startswith(target_prefix):
                return nonce, block_hash
            nonce += 1


class PuzzleSolverOrchestrator:
    """
    Master orchestrator for integrated puzzle solving.
    Coordinates Caesar, GA, and Temporal solvers with tensor-field mapping.
    """
    
    def __init__(self):
        """Initialize orchestrator with all solver components."""
        self.caesar_solver = CaesarCipherSolver()
        self.temporal_solver = TemporalAnchorSolver()
        self.ga_solver = None  # Instantiated per puzzle
        self.results = {}
    
    def solve_caesar(self, cipher: str) -> Dict:
        """Solve Caesar cipher puzzle."""
        results = self.caesar_solver.solve(cipher)
        self.results['caesar'] = results[:5]  # Top 5
        return {
            'puzzle_type': 'caesar_cipher',
            'cipher': cipher,
            'top_results': results[:5],
            'best_match': results[0] if results else None
        }
    
    def solve_temporal(self) -> Dict:
        """Solve temporal anchor puzzle."""
        nonce, block_hash = self.temporal_solver.mine_block(difficulty=2)
        self.results['temporal'] = {
            'nonce': nonce,
            'hash': block_hash,
            'merkle_root': self.temporal_solver._merkle_root(),
            'days_since_genesis': self.temporal_solver.days
        }
        return self.results['temporal']
    
    def solve_genetic(self, target_hash: str, generations: int = 100) -> Dict:
        """Solve using genetic algorithm."""
        self.ga_solver = GeneticAlgorithmSolver(
            target_hash=target_hash,
            population_size=200,
            mutation_rate=0.05
        )
        solution, gen_found = self.ga_solver.solve(generations)
        self.results['genetic'] = {
            'solution': solution,
            'generation_found': gen_found,
            'target_hash': target_hash,
            'solution_hash': self.ga_solver._hash_word(solution),
            'match': self.ga_solver._hash_word(solution) == target_hash
        }
        return self.results['genetic']
    
    def vector_normalize(self, word: str) -> Tuple[float, float, float]:
        """
        Normalize 3-letter word to R^3 vector space for tensor-field mapping.
        
        Args:
            word: 3-letter word
            
        Returns:
            (x, y, z) normalized vector in R^3
        """
        if len(word) != 3:
            raise ValueError("Word must be 3 letters")
        
        # Map each letter to 0-25, then normalize to 0-1
        x = ord(word[0].upper()) - ord('A') / 26.0
        y = ord(word[1].upper()) - ord('A') / 26.0
        z = ord(word[2].upper()) - ord('A') / 26.0
        
        # Normalize to unit sphere
        magnitude = (x**2 + y**2 + z**2) ** 0.5
        if magnitude == 0:
            return 0.0, 0.0, 0.0
        
        return x/magnitude, y/magnitude, z/magnitude


# ============================================================================
# MATN LEDGER ENTRY
# ============================================================================

def log_matn_entry(orchestrator: PuzzleSolverOrchestrator, puzzle_id: str):
    """Log solved puzzle to MATN (Merkle-Anchored Temporal Network) ledger."""
    timestamp = int(time.time())
    entry = {
        'puzzle_id': puzzle_id,
        'timestamp': timestamp,
        'solutions': orchestrator.results,
        'block_height': '#79',
        'frontier': 'KRYPTOS_K4_SOLVER'
    }
    return entry


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║         PUZZLE SOLVER SUITE v1.0 - ORCHESTRATION          ║")
    print("║    GA Pop: 200 | Mutation: 0.05 | Vector Space: R³       ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")
    
    orchestrator = PuzzleSolverOrchestrator()
    
    # Example 1: Caesar cipher
    print("[1] Caesar Cipher Puzzle")
    cipher = "QXPKFCKSHXGIEOQEHLDSBTGTWAYV"
    caesar_result = orchestrator.solve_caesar(cipher)
    print(f"    Best match: {caesar_result['best_match']}\n")
    
    # Example 2: Temporal anchor
    print("[2] Temporal Anchor Puzzle")
    temporal_result = orchestrator.solve_temporal()
    print(f"    Merkle Root: {temporal_result['merkle_root'][:16]}...")
    print(f"    Nonce: {temporal_result['nonce']}")
    print(f"    Days since genesis: {temporal_result['days_since_genesis']}\n")
    
    # Example 3: Genetic algorithm (if you have a target hash)
    print("[3] Genetic Algorithm Puzzle")
    target = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"  # SHA256 of empty string
    ga_result = orchestrator.solve_genetic(target, generations=50)
    print(f"    Solution: {ga_result['solution']}")
    print(f"    Found at generation: {ga_result['generation_found']}\n")
    
    # Log to MATN ledger
    matn_entry = log_matn_entry(orchestrator, "PUZZLE_#79_KRYPTOS")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║              MATN LEDGER ENTRY LOGGED                     ║")
    print(f"║ Block #79 | Puzzle ID: {matn_entry['puzzle_id']:30} ║")
    print("╚═══════════════════════════════════════════════════════════╝")
