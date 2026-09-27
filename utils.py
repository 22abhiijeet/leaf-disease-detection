"""
Base64 Image Test for Leaf Disease Detection
===========================================
"""

import json
import sys
import os
import base64
from pathlib import Path


def test_with_base64_data(base64_image_string: str):
    """
    Test disease detection with base64 image data
    """
    try:
        # Ensure 'Leaf Disease' folder is in system path safely
        leaf_disease_path = Path(__file__).parent / "Leaf Disease"
        if str(leaf_disease_path) not in sys.path:
            sys.path.insert(0, str(leaf_disease_path))

        from main import LeafDiseaseDetector

        detector = LeafDiseaseDetector()
        result = detector.analyze_leaf_image_base64(base64_image_string)
        return result
    except Exception as e:
        error_msg = f"Error in LeafDiseaseDetector: {str(e)}"
        print(error_msg)
        return {
            "disease_type": "invalid_image",
            "symptoms": [error_msg],
            "treatment": ["Please check server logs for more details."]
        }


def convert_image_to_base64_and_test(image_bytes: bytes):
    """
    Convert image bytes to base64 and test it
    """
    try:
        if not image_bytes:
            return {
                "disease_type": "invalid_image",
                "symptoms": ["No image bytes provided"],
                "treatment": ["Please upload a valid image."]
            }

        base64_string = base64.b64encode(image_bytes).decode('utf-8')
        return test_with_base64_data(base64_string)
    except Exception as e:
        error_msg = f"Error converting image: {str(e)}"
        print(error_msg)
        return {
            "disease_type": "invalid_image",
            "symptoms": [error_msg],
            "treatment": ["Please try again with a different image."]
        }