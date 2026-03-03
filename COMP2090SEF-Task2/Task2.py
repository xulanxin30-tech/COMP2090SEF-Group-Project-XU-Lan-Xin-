"""
Shell Sort – Advanced Study Implementation
------------------------------------------
This module demonstrates Shell sort with various gap sequences,
visualizes each pass, and compares performance.

Author: COMP2090SEF-Group 9 Student (self‑study)
Date: 2026
"""

import time
import random
from typing import List, Callable, Generator

# ===================== Binary Search Tree (from original code) =====================
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert_bst(root, value):
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = insert_bst(root.left, value)
    elif value > root.value:
        root.right = insert_bst(root.right, value)
    return root

def inorder_traversal(root, result):
    if root:
        inorder_traversal(root.left, result)
        result.append(root.value)
        inorder_traversal(root.right, result)

def build_bst_from_list(arr):
    root = None
    for value in arr:
        root = insert_bst(root, value)
    return root

def bst_sort(arr):
    """Return sorted list by building a BST and traversing in‑order."""
    root = build_bst_from_list(arr)
    sorted_arr = []
    inorder_traversal(root, sorted_arr)
    return sorted_arr

# ===================== Shell Sort with Customizable Gap Sequences =====================

def shell_original_gaps(n: int) -> Generator[int, None, None]:
    """Original Shell's gaps: n//2, n//4, ..., 1."""
    gap = n // 2
    while gap > 0:
        yield gap
        gap //= 2

def shell_hibbard_gaps(n: int) -> Generator[int, None, None]:
    """Hibbard's gaps: 2^k - 1 (..., 15, 7, 3, 1)."""
    k = 1
    while True:
        gap = (1 << k) - 1   # 2^k - 1
        if gap >= n:
            break
        k += 1
    k -= 1
    while k >= 1:
        yield (1 << k) - 1
        k -= 1

def shell_knuth_gaps(n: int) -> Generator[int, None, None]:
    """Knuth's gaps: (3^k - 1)//2 (..., 13, 4, 1)."""
    gaps = []
    k = 1
    while True:
        gap = (3**k - 1) // 2
        if gap > n:
            break
        gaps.append(gap)
        k += 1
    for gap in reversed(gaps):
        yield gap

def shell_sedgewick_gaps(n: int) -> Generator[int, None, None]:
    """
    Sedgewick's gaps (1986): 9*4^i - 9*2^i + 1 or 4^(i+2) - 3*2^(i+2) + 1.
    Simplified version that yields gaps up to n.
    """
    gaps = []
    i = 0
    while True:
        gap1 = 9 * (4**i) - 9 * (2**i) + 1
        gap2 = 4**(i+2) - 3 * 2**(i+2) + 1
        if gap1 < gap2:
            smaller = gap1
            larger = gap2
        else:
            smaller = gap2
            larger = gap1
        if smaller > n:
            break
        gaps.append(smaller)
        if larger <= n:
            gaps.append(larger)
        i += 1
    gaps.sort(reverse=True)
    for gap in gaps:
        yield gap

def shell_sort_with_gaps(arr: List[int], gap_generator: Callable[[int], Generator[int, None, None]],
                         verbose: bool = False) -> List[int]:
    """
    Generic Shell sort using a supplied gap generator.
    If verbose is True, prints detailed information after each pass.
    Returns the sorted list (in‑place sort, but returns for convenience).
    """
    n = len(arr)
    if n <= 1:
        return arr

    # Collect all gaps from the generator
    gaps = list(gap_generator(n))
    if verbose:
        print(f"\nUsing gaps: {gaps}")

    step = 1
    for gap in gaps:
        if verbose:
            print(f"\n--- Pass {step}, gap = {gap} ---")
            # Show sublists before pass
            sublists = [[] for _ in range(gap)]
            for i in range(n):
                sublists[i % gap].append(arr[i])
            print("  Sublists (by modulo gap):")
            for idx, subl in enumerate(sublists):
                print(f"    [{idx}]: {subl}")

        # Perform gapped insertion sort
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp

        if verbose:
            print("  Array after pass:", arr)
            # Show sublists after pass
            sublists_after = [[] for _ in range(gap)]
            for i in range(n):
                sublists_after[i % gap].append(arr[i])
            print("  Sublists after pass:")
            for idx, subl in enumerate(sublists_after):
                print(f"    [{idx}]: {subl}")

        step += 1

    return arr

# ===================== Testing and Comparison =====================

def test_shell_sort():
    """Test Shell sort with various gap sequences and compare with built‑in sort."""
    test_data = [64, 34, 25, 12, 22, 11, 90, 5, 38, 71, 47]
    print("=" * 70)
    print("SHELL SORT – ADVANCED STUDY")
    print("=" * 70)
    print(f"Original array: {test_data}\n")

    # 1. BST sort (in‑order traversal)
    print("--- Binary Search Tree Sort ---")
    bst_sorted = bst_sort(test_data)
    print(f"BST in‑order traversal gives: {bst_sorted}\n")

    # 2. Shell sort with different gap sequences
    gap_sequences = {
        "Original Shell (n/2^k)": shell_original_gaps,
        "Hibbard (2^k - 1)": shell_hibbard_gaps,
        "Knuth ((3^k-1)/2)": shell_knuth_gaps,
        "Sedgewick (1986)": shell_sedgewick_gaps,
    }

    results = {}
    for name, generator in gap_sequences.items():
        arr_copy = test_data.copy()
        print("-" * 50)
        print(f"Sequence: {name}")
        start = time.perf_counter()
        sorted_arr = shell_sort_with_gaps(arr_copy, generator, verbose=True)
        elapsed = time.perf_counter() - start
        results[name] = (sorted_arr, elapsed)
        print(f"Sorted: {sorted_arr}")
        print(f"Time: {elapsed:.6f} seconds")

    # 3. Verification against Python's built‑in sort
    builtin_sorted = sorted(test_data)
    print("\n" + "=" * 70)
    print("VERIFICATION")
    print("=" * 70)
    all_correct = True
    for name, (sorted_arr, _) in results.items():
        if sorted_arr == builtin_sorted:
            print(f"✓ {name}: correct")
        else:
            print(f"✗ {name}: INCORRECT")
            all_correct = False
    if all_correct:
        print("\n✅ All Shell sort implementations produced the correct sorted order.\n")
    else:
        print("\n❌ Some implementations failed.\n")

    # 4. Performance comparison (using a larger random array)
    print("=" * 70)
    print("PERFORMANCE COMPARISON (larger array)")
    print("=" * 70)
    large_size = 1000
    large_arr = random.sample(range(large_size * 10), large_size)  # unique random numbers
    print(f"Array size: {large_size}")

    for name, generator in gap_sequences.items():
        arr_copy = large_arr.copy()
        start = time.perf_counter()
        _ = shell_sort_with_gaps(arr_copy, generator, verbose=False)
        elapsed = time.perf_counter() - start
        print(f"{name:25} : {elapsed:.6f} seconds")

    # Also measure Python's built‑in sort for reference
    arr_copy = large_arr.copy()
    start = time.perf_counter()
    _ = sorted(arr_copy)
    elapsed_builtin = time.perf_counter() - start
    print(f"{'Python built-in sort':25} : {elapsed_builtin:.6f} seconds")

if __name__ == "__main__":
    test_shell_sort()