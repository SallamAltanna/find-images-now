"""
Unit Tests — /compare API Endpoint
====================================
Tests for the FINd RESTful API endpoint defined in api/main.py.

Run with:
    pytest tests/test_api.py -v
"""

import io
import os
import sys
import numpy as np
import unittest
from PIL import Image
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from api.main import app

client = TestClient(app)

TEST_IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'test_images')


class TestCompareEndpoint(unittest.TestCase):

    # ─── 1. Valid request ─────────────────────────────────────────────────────
    def test_valid_request(self):
        """Two valid real images return correct response format."""
        img1_path = os.path.join(TEST_IMAGES_DIR, '0040_10318987.jpg')
        img2_path = os.path.join(TEST_IMAGES_DIR, '0040_10321701.jpg')

        with open(img1_path, 'rb') as f1, open(img2_path, 'rb') as f2:
            response = client.post("/compare",
                files={
                    "image1": ("image1.jpg", f1, "image/jpeg"),
                    "image2": ("image2.jpg", f2, "image/jpeg")
                }
            )

        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("image1_hash", data)
        self.assertIn("image2_hash", data)
        self.assertIn("distance", data)
        self.assertIsInstance(data["distance"], int)
        self.assertTrue(0 <= data["distance"] <= 256)

    # ─── 2. Same image Test ─────────────────────────────────── ──────────────
    def test_same_image(self):
        """Same image uploaded twice should return distance of 0."""
        img_path = os.path.join(TEST_IMAGES_DIR, '0040_10318987.jpg')

        with open(img_path, 'rb') as f1, open(img_path, 'rb') as f2:
            response = client.post("/compare",
                files={
                    "image1": ("image1.jpg", f1, "image/jpeg"),
                    "image2": ("image2.jpg", f2, "image/jpeg")
                }
            )

        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["distance"], 0)

    # ─── 3. Regression Test ──────────────────────────────────────────────────
    def test_regression_assessment_images(self):
        """API should return expected distance for example images."""
        img1_path = os.path.join(TEST_IMAGES_DIR, '0000_12268686.jpg')
        img2_path = os.path.join(TEST_IMAGES_DIR, '0000_12270286.jpg')

        with open(img1_path, 'rb') as f1, open(img2_path, 'rb') as f2:
            response = client.post("/compare",
                files={
                    "image1": ("image1.jpg", f1, "image/jpeg"),
                    "image2": ("image2.jpg", f2, "image/jpeg")
                }
            )

        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["distance"], 44) # 44 is the expected true value 

    # ─── 4. Non-Square Images ────────────────────────────────────────────────
    def test_non_square_image(self):
        """Non-square image should return 400 with descriptive error message."""
        rect_img = Image.new('RGB', (400, 200), color=(128, 64, 32))
        square_img = Image.new('RGB', (200, 200), color=(128, 64, 32))

        buf1 = io.BytesIO()
        buf2 = io.BytesIO()
        rect_img.save(buf1, format='JPEG')
        square_img.save(buf2, format='JPEG')
        buf1.seek(0)
        buf2.seek(0)

        response = client.post("/compare",
            files={
                "image1": ("image1.jpg", buf1, "image/jpeg"),
                "image2": ("image2.jpg", buf2, "image/jpeg")
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Non-square images are not supported", response.json()["detail"])

    # ─── 5. Error Handling ───────────────────────────────────────────────────
    def test_missing_image(self):
        """Missing image2 should return 422 with descriptive error message."""
        img_path = os.path.join(TEST_IMAGES_DIR, '0040_10318987.jpg')

        with open(img_path, 'rb') as f1:
            response = client.post("/compare",
                files={
                    "image1": ("image1.jpg", f1, "image/jpeg")
                }
            )

        self.assertEqual(response.status_code, 422)
        self.assertIn("Both image1 and image2 are required.", response.json()["detail"])

    # ─── 6. Inavlid file  ──────────────────────────────────────────────
    def test_invalid_file_type(self):
        """Sending a .txt file instead of image should return 422 with error message."""
        txt_content = io.BytesIO(b"this is not an image")

        response = client.post("/compare",
            files={
                "image1": ("file.txt", txt_content, "text/plain"),
                "image2": ("file.txt", txt_content, "text/plain")
            }
        )

        self.assertEqual(response.status_code, 422)
        self.assertIn("Invalid image file.", response.json()["detail"])


if __name__ == '__main__':
    unittest.main()