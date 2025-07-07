import unittest
import os
import sys
import json

# Import both Result and Candidate classes from models
from probium.models import Result, Candidate

# --- PATH RESOLUTION STARTS HERE ---
current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_script_dir, '..', '..'))
sys.path.insert(0, project_root)

try:
    from probium.core import detect, _detect_file, scan_dir
except ImportError as e:
    print(f"Error: Could not import necessary modules. Details: {e}")
    print(f"Please ensure probium/core.py and probium/models.py (with Result and Candidate classes) are correctly placed and __init__.py files exist.")
    sys.exit(1)


TEST_CASES_JSON_FILE = os.path.join(current_script_dir, "test_cases.json")
BASE_TEST_DIR = os.path.join(current_script_dir, "test_cases_cft")
# --- PATH RESOLUTION ENDS HERE ---


class TestFileTypeDetection(unittest.TestCase):
    LOADED_TEST_CASES = {}

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(TEST_CASES_JSON_FILE):
            raise FileNotFoundError(f"Test cases JSON file not found: {TEST_CASES_JSON_FILE}. Expected at {TEST_CASES_JSON_FILE}")

        try:
            with open(TEST_CASES_JSON_FILE, 'r') as f:
                cls.LOADED_TEST_CASES = json.load(f)
            print(f"\nSuccessfully loaded test cases from {TEST_CASES_JSON_FILE}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON from {TEST_CASES_JSON_FILE}: {e}")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred while loading test cases: {e}")

        if not os.path.isdir(BASE_TEST_DIR):
            raise NotADirectoryError(
                f"Base test data directory not found: {BASE_TEST_DIR}. "
                "Please ensure your pre-gathered test files are rooted here."
            )
        print(f"Running tests from base directory: {BASE_TEST_DIR}")

    def _run_tests_for_category(self, category_name):
        tests_in_category = self.LOADED_TEST_CASES.get(category_name, [])
        if not tests_in_category:
            self.skipTest(f"No '{category_name}' tests found in {TEST_CASES_JSON_FILE}")

        for test_case in tests_in_category:
            if not all(k in test_case for k in ["name", "test_file_path", "expected_mime_type"]):
                self.fail(f"Invalid test case format in '{category_name}': {test_case}. Missing required keys.")

            with self.subTest(msg=test_case["name"]):
                file_path_from_json = test_case["test_file_path"]
                full_filepath = os.path.join(current_script_dir, file_path_from_json)

                self.assertTrue(os.path.exists(full_filepath),
                                f"Test file not found: {full_filepath} for test '{test_case['name']}'")

                detected_result_object = _detect_file(full_filepath) # This will be the Result object
                expected_mime = test_case["expected_mime_type"]

                print(f"--- Debugging '{test_case['name']}' ---")
                print(f"Detected value type: {type(detected_result_object)}")
                print(f"Detected value (Result object): {detected_result_object}")
                print(f"Expected MIME type: {expected_mime}")

                # 1. Assert that it's an instance of your Result class
                self.assertIsInstance(detected_result_object, Result,
                                      f"Expected _detect_file to return a Result object, but got {type(detected_result_object)} for {full_filepath}")

                # 2. Assert that the Result object has a non-empty list of candidates
                self.assertIsInstance(detected_result_object.candidates, list,
                                      f"Expected Result object to contain a list of candidates, but got {type(detected_result_object.candidates)} for {full_filepath}")
                self.assertTrue(len(detected_result_object.candidates) > 0,
                                f"Expected Result object to contain at least one candidate, but the list was empty for {full_filepath}")

                # 3. Assert that the first candidate is a Candidate object
                self.assertIsInstance(detected_result_object.candidates[0], Candidate,
                                      f"Expected first candidate to be a Candidate object, but got {type(detected_result_object.candidates[0])} for {full_filepath}")

                # 4. Finally, access the media_type from the first Candidate
                actual_mime_from_result = detected_result_object.candidates[0].media_type # <--- THIS IS THE DEFINITIVE FIX

                print(f"Actual MIME extracted from Result: {actual_mime_from_result}")

                self.assertEqual(actual_mime_from_result, expected_mime,
                                 f"Failed for {full_filepath} ('{test_case['name']}'). Expected '{expected_mime}', got '{actual_mime_from_result}' from Result object.")

    def test_false_file_tests(self):
        self._run_tests_for_category("false file tests")

    def test_csv_file_tests(self):
        self._run_tests_for_category("csv file tests")

    def test_docx_file_tests(self):
        self._run_tests_for_category("docx file tests")

    def test_pdf_file_tests(self):
        self._run_tests_for_category("pdf file tests")

    def test_corrupted_files_tests(self):
        self._run_tests_for_category("corrupted files tests")

    def test_edge_case_tests(self):
        self._run_tests_for_category("Edge case tests")


if __name__ == '__main__':
    unittest.main()
