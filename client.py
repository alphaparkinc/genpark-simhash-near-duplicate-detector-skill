"""SimHash 64-bit Near-Duplicate Detection Engine.
100% Python Standard Library.
"""

import hashlib
from typing import Dict, List, Any

class SimHashNearDuplicateDetector:
    """Detects near-duplicate documents and LLM responses using 64-bit SimHash and Hamming distance."""

    def __init__(self, hash_bits: int = 64, ngram_size: int = 3):
        self.hash_bits = hash_bits
        self.ngram_size = ngram_size

    def _tokenize(self, text: str) -> List[str]:
        cleaned = "".join(c.lower() if c.isalnum() else " " for c in text).strip()
        if len(cleaned) < self.ngram_size:
            return [cleaned] if cleaned else []
        return [cleaned[i:i+self.ngram_size] for i in range(len(cleaned) - self.ngram_size + 1)]

    def compute_simhash(self, text: str) -> int:
        tokens = self._tokenize(text)
        if not tokens:
            return 0
        v = [0] * self.hash_bits
        for token in tokens:
            h = int.from_bytes(hashlib.md5(token.encode("utf-8")).digest()[:8], "big")
            for i in range(self.hash_bits):
                bit = (h >> i) & 1
                v[i] += 1 if bit else -1
        fingerprint = 0
        for i in range(self.hash_bits):
            if v[i] > 0:
                fingerprint |= (1 << i)
        return fingerprint

    def hamming_distance(self, hash1: int, hash2: int) -> int:
        return bin(hash1 ^ hash2).count("1")

    def is_near_duplicate(self, text1: str, text2: str, max_distance: int = 8, min_similarity: float = 0.85) -> Dict[str, Any]:
        h1 = self.compute_simhash(text1)
        h2 = self.compute_simhash(text2)
        dist = self.hamming_distance(h1, h2)
        similarity = round(1.0 - (dist / float(self.hash_bits)), 4)
        is_dup = (dist <= max_distance) or (similarity >= min_similarity)
        return {
            "is_duplicate": is_dup,
            "hamming_distance": dist,
            "similarity": similarity,
            "threshold_distance": max_distance,
            "threshold_similarity": min_similarity
        }
