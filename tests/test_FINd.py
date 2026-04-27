"""
Unit Tests — FINd Optimised Hasher
====================================
Tests for the optimised FINd image hashing algorithm.
Verifies correctness, consistency, and known behaviour
of the FINDHasher implementation in src/fin/hasher.py.

Run with:
    pytest tests/test_FINd.py -v
"""

import unittest
import sys
import os

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

    # ─── 1. Valid square image ─────────────────────────────────────────────────────
    def test_hash_not_none(self):
        """
        Test 1: Verifies that the optimised FINd produces a valid
        hash for a standard square image.
        """
        hasher = FINDHasher()
        image_path = os.path.join(TEST_IMAGES_DIR, '0040_10318987.jpg')

        hash_result = hasher.fromFile(image_path)

        self.assertIsNotNone(hash_result,
            "Hash should not be None for a valid square image")

    # ─── 2. Invalid non-square image ───────────────────────────────────────────────
    def test_rectangle_image_raises_error(self):
        """
        Test 2: Verifies that the optimised FINd raises a ValueError
        for non-square images due to the rows indexing bug preserved
        for fair comparison with the original implementation.
        """
        hasher = FINDHasher()
        rect_image = Image.new('RGB', (400, 200), color=(128, 64, 32))

        with self.assertRaises(ValueError):
            hasher.fromImage(rect_image)

    # ─── 3. Identical hash for same images ─────────────────────────────────────────
    def test_hash_consistency(self):
        """
        Test 3: Verifies that hashing the same image twice
        produces identical results.
        """
        hasher = FINDHasher()
        image_path = os.path.join(TEST_IMAGES_DIR, '0040_10318987.jpg')

        hash1 = hasher.fromFile(image_path)
        hash2 = hasher.fromFile(image_path)

        self.assertEqual(hash1, hash2,
            "Same image should always produce the same hash")

    # ─── 4. Hash length  ───────────────────────────────────────────────────────────
    def test_hash_length(self):
        """
        Test 4: Verifies that the hash is always 256 bits.
        """
        hasher = FINDHasher()
        image_path = os.path.join(TEST_IMAGES_DIR, '0040_10318987.jpg')

        hash_result = hasher.fromFile(image_path)

        self.assertEqual(len(hash_result.hash.flatten()), 256,
            "Hash should always be 256 bits")


if __name__ == "__main__":
    unittest.main()