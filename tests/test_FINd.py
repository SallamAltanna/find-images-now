"""
Unit Tests — FINd Optimised Hasher
====================================
Tests for the optimised FINd image hashing algorithm.
Verifies correctness, consistency, and known behaviour
of the FINDHasher implementation in src/fin/hasher.py.

Run with:
    pytest tests/test_FINd.py -v
"""
import numpy as np
import unittest
import sys
import os

def hex_to_hash_array(hex_str):
    """Converts a hex string back into a 16x16 boolean NumPy array."""
    # Convert hex to a large integer, then to a bitstring padded to 256 bits
    bit_str = bin(int(hex_str, 16))[2:].zfill(256)
    # Convert bitstring to a list of integers (0 or 1)
    bit_list = [int(b) for b in bit_str]
    # Reshape into the 16x16 grid your ImageHash class expects
    return np.array(bit_list).reshape((16, 16))


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

SRC_PATH = os.path.join(PROJECT_ROOT, 'src')
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from PIL import Image
from fin.hasher import FINDHasher

# path to test images — consistent with test_api.py
TEST_IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'test_images')


class TestFINdOptimisation(unittest.TestCase):

    def setUp(self):
        """Runs before every single test case."""
        self.hasher = FINDHasher()

    # ─── 1. Valid square image ─────────────────────────────────────────────────────
    def test_hash_not_none(self):
        """
        Test 1: Verifies that the optimised FINd produces a valid
        hash for a standard square image.
        """
        image_path = os.path.join(TEST_IMAGES_DIR, '0040_10318987.jpg')

        hash_result = self.hasher.fromFile(image_path)

        self.assertIsNotNone(hash_result,
            "Hash should not be None for a valid square image")

    # ─── 2. Invalid non-square image ───────────────────────────────────────────────
    def test_rectangle_image_raises_error(self):
        """
        Test 2: Verifies that the optimised FINd raises a ValueError
        for non-square images due to the rows indexing bug preserved
        for fair comparison with the original implementation.
        """
        rect_image = Image.new('RGB', (400, 200), color=(128, 64, 32))

        with self.assertRaises(ValueError):
            self.hasher.fromImage(rect_image)

    # ─── 3. Identical hash for same images ─────────────────────────────────────────
    def test_hash_consistency(self):
        """
        Test 3: Verifies that hashing the same image twice
        produces identical results.
        """
        image_path = os.path.join(TEST_IMAGES_DIR, '0040_10318987.jpg')

        hash1 = self.hasher.fromFile(image_path)
        hash2 = self.hasher.fromFile(image_path)

        self.assertEqual(hash1, hash2,
            "Same image should always produce the same hash")

    # ─── 4. Hash length  ───────────────────────────────────────────────────────────
    def test_hash_length(self):
        """
        Test 4: Verifies that the hash is always 256 bits.
        """
        image_path = os.path.join(TEST_IMAGES_DIR, '0040_10318987.jpg')

        hash_result = self.hasher.fromFile(image_path)

        self.assertEqual(len(hash_result.hash.flatten()), 256,
            "Hash should always be 256 bits")
        
    # ─── 5. Hardcoded Hash Regression Test ─────────────────────────────────────────
    def test_optimisation_drift_threshold(self):
            """
            Test 5: Verifies the optimised hash remains within the 33-bit threshold 
              of the original baseline using a hardcoded hash for the image "0000_12268686.jpg".
            """
            from fin.hasher import ImageHash
            image_path = os.path.join(TEST_IMAGES_DIR, '0000_12268686.jpg')
            
            golden_hex = "393b246d65a694dc5386279b8e7394f04c9da697877b18a31995ab9893235b65"
            
            # 1. Generate the optimised hash object
            opt_hash = self.hasher.fromFile(image_path)
            
            # Manually create the hardcoded Hash object using the helper
            golden_array = hex_to_hash_array(golden_hex)
            golden_hash = ImageHash(golden_array)
            
            distance = opt_hash - golden_hash
            
            self.assertLess(distance, 33, 
                f"Optimisation drift ({distance} bits) exceeds the 33-bit threshold")



if __name__ == "__main__":
    unittest.main()