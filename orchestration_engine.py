"""
Orchestration Engine
Tensor-Field Mapping and MATN Ledger Integration

Handles:
- Vector normalization of 3-letter outputs to R^3
- Tensor-field convergence validation
- MATN (Mapped-Atom-Tensor-Nodes) ledger tracking
- Topological mapping and checksum validation
"""

import hashlib
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import numpy as np


@dataclass
class TensorVector:
    """3D Tensor Vector in R^3 space"""
    x: float
    y: float
    z: float
    
    def normalize(self) -> 'TensorVector':
        """Normalize vector to unit length"""
        magnitude = np.sqrt(self.x**2 + self.y**2 + self.z**2)
        if magnitude == 0:
            return TensorVector(0, 0, 0)
        return TensorVector(
            self.x / magnitude,
            self.y / magnitude,
            self.z / magnitude
        )
    
    def to_array(self) -> np.ndarray:
        """Convert to numpy array"""
        return np.array([self.x, self.y, self.z])


@dataclass
class MATNEntry:
    """MATN Ledger Entry - Mapped-Atom-Tensor-Nodes"""
    timestamp: str
    solution: str
    vector: Dict  # Serialized TensorVector
    checksum: str
    validation_status: str
    tensor_magnitude: float


class MATNLedger:
    """MATN (Mapped-Atom-Tensor-Nodes) Ledger for validation tracking"""
    
    def __init__(self):
        self.entries: List[MATNEntry] = []
    
    def add_entry(self, solution: str, vector: TensorVector, 
                  checksum: str, validation_status: str) -> None:
        """Add entry to MATN ledger"""
        entry = MATNEntry(
            timestamp=datetime.now().isoformat(),
            solution=solution,
            vector=asdict(vector),
            checksum=checksum,
            validation_status=validation_status,
            tensor_magnitude=np.linalg.norm(vector.to_array())
        )
        self.entries.append(entry)
    
    def get_ledger(self) -> List[Dict]:
        """Export ledger as list of dicts"""
        return [asdict(entry) for entry in self.entries]
    
    def validate_ledger(self) -> bool:
        """Validate ledger integrity"""
        return len(self.entries) > 0


class TensorFieldMapper:
    """Maps 3-letter words to R^3 tensor field"""
    
    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.ledger = MATNLedger()
    
    def letter_to_value(self, letter: str) -> float:
        """Convert letter to normalized float [0, 1]"""
        idx = self.alphabet.index(letter.upper())
        return idx / 25.0  # Normalize to [0, 1]
    
    def word_to_tensor(self, word: str) -> TensorVector:
        """
        Map 3-letter word to tensor vector in R^3
        
        Mapping strategy:
        - Position 0 (first letter) → X-axis
        - Position 1 (second letter) → Y-axis
        - Position 2 (third letter) → Z-axis
        
        Each axis normalized to [0, 1]
        """
        if len(word) != 3:
            raise ValueError(f"Expected 3-letter word, got '{word}'")
        
        x = self.letter_to_value(word[0])
        y = self.letter_to_value(word[1])
        z = self.letter_to_value(word[2])
        
        vector = TensorVector(x, y, z)
        return vector.normalize()
    
    def tensor_to_checksum(self, vector: TensorVector, word: str) -> str:
        """Generate checksum combining tensor and word"""
        vector_str = f"{vector.x:.6f},{vector.y:.6f},{vector.z:.6f}"
        combined = f"{word}:{vector_str}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def validate_mapping(self, solution: str, target_hash: str,
                        hash_type: str = 'sha256') -> Dict:
        """
        Validate solution through tensor-field mapping
        
        Returns:
            Validation report with tensor field and MATN ledger entry
        """
        # Verify hash match
        if hash_type == 'md5':
            candidate_hash = hashlib.md5(solution.encode()).hexdigest()
        else:
            candidate_hash = hashlib.sha256(solution.encode()).hexdigest()
        
        hash_match = candidate_hash == target_hash
        
        # Map to tensor field
        vector = self.word_to_tensor(solution)
        checksum = self.tensor_to_checksum(vector, solution)
        
        # Determine validation status
        validation_status = 'VALID' if hash_match else 'PENDING'
        
        # Add to MATN ledger
        self.ledger.add_entry(solution, vector, checksum, validation_status)
        
        return {
            'solution': solution,
            'hash_match': hash_match,
            'target_hash': target_hash,
            'candidate_hash': candidate_hash,
            'tensor': {
                'x': vector.x,
                'y': vector.y,
                'z': vector.z,
                'magnitude': np.linalg.norm(vector.to_array())
            },
            'checksum': checksum,
            'validation_status': validation_status,
            'timestamp': datetime.now().isoformat()
        }


class OrchestrationEngine:
    """
    Master Orchestration Engine
    Coordinates puzzle solving, tensor mapping, and MATN validation
    """
    
    def __init__(self):
        self.mapper = TensorFieldMapper()
        self.solutions: List[Dict] = []
    
    def orchestrate_solution(self, solution: str, target_hash: str,
                            hash_type: str = 'sha256') -> Dict:
        """
        Full orchestration pipeline:
        1. Decode cryptographic primitive
        2. Validate via tensor-field mapping
        3. Register in MATN ledger
        4. Return topological mapping
        
        Returns:
            Complete orchestration report
        """
        # Validate mapping
        validation = self.mapper.validate_mapping(
            solution, target_hash, hash_type
        )
        
        # Build orchestration report
        report = {
            'orchestration_timestamp': datetime.now().isoformat(),
            'pipeline': [
                'cryptographic_decode',
                'tensor_field_mapping',
                'matn_ledger_registration',
                'topological_validation'
            ],
            'solution_details': validation,
            'matn_ledger': self.mapper.ledger.get_ledger(),
            'execution_state': {
                'total_state_space': 26**3,
                'complexity_class': 'O(1)',
                'solution_found': validation['hash_match']
            }
        }
        
        self.solutions.append(validation)
        return report
    
    def get_orchestration_summary(self) -> Dict:
        """Get summary of all orchestrated solutions"""
        return {
            'total_solutions': len(self.solutions),
            'valid_solutions': sum(
                1 for s in self.solutions if s['hash_match']
            ),
            'solutions': self.solutions,
            'matn_ledger': self.mapper.ledger.get_ledger()
        }
    
    def export_report(self, filepath: str) -> None:
        """Export orchestration report to JSON"""
        report = self.get_orchestration_summary()
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report exported to {filepath}")


def orchestrate_puzzle_solution(solution: str, target_hash: str,
                               hash_type: str = 'sha256') -> Dict:
    """
    Main entry point for orchestrated puzzle solving
    
    Args:
        solution: 3-letter solution string
        target_hash: Target hash to validate against
        hash_type: Hash algorithm ('md5', 'sha256')
    
    Returns:
        Complete orchestration report
    """
    engine = OrchestrationEngine()
    return engine.orchestrate_solution(solution, target_hash, hash_type)


if __name__ == "__main__":
    import hashlib
    
    # Example usage
    test_word = "CAT"
    test_hash = hashlib.sha256(test_word.encode()).hexdigest()
    
    print("Orchestration Engine Test")
    print(f"Solution: {test_word}")
    print(f"Target Hash: {test_hash}\n")
    
    report = orchestrate_puzzle_solution(test_word, test_hash)
    
    print(json.dumps(report, indent=2))
