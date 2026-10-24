"""Example usage for GenPark SimHash Near-Duplicate Detector.
100% Python Standard Library.
"""

from client import SimHashNearDuplicateDetector

def main():
    detector = SimHashNearDuplicateDetector()
    
    doc1 = "The distributed transaction coordinator completed phase 1 prepare voting successfully."
    doc2 = "The distributed transaction coordinator completed phase 1 prepare voting without error."
    doc3 = "Quantum computing relies on superconducting qubits operating at near zero Kelvin."
    
    cmp12 = detector.is_near_duplicate(doc1, doc2)
    print("Doc1 vs Doc2 (near identical):", cmp12)
    
    cmp13 = detector.is_near_duplicate(doc1, doc3)
    print("Doc1 vs Doc3 (completely distinct):", cmp13)

if __name__ == "__main__":
    main()
