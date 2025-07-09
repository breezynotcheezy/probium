import unittest
import os
import sys
import json
import time

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
    total_tests_run = 0    # New: Counter for total tests executed
    successful_tests = 0   # New: Counter for successful tests

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

    @classmethod
    def tearDownClass(cls):
        # Report success rate after all tests are done
        print("\n--- Test Summary ---")
        if cls.total_tests_run > 0:
            success_percentage = (cls.successful_tests / cls.total_tests_run) * 100
            print(f"Total tests run: {cls.total_tests_run}")
            print(f"Successful tests: {cls.successful_tests}")
            print(f"Failed tests: {cls.total_tests_run - cls.successful_tests}")
            print(f"Success Rate: {success_percentage:.2f}%")
        else:
            print("No tests were run.")

    def _run_tests_for_category(self, category_name):
        tests_in_category = self.LOADED_TEST_CASES.get(category_name, [])
        if not tests_in_category:
            self.skipTest(f"No '{category_name}' tests found in {TEST_CASES_JSON_FILE}")

        for test_case in tests_in_category:
            # Increment total tests run for each test case encountered
            TestFileTypeDetection.total_tests_run += 1

            if not all(k in test_case for k in ["name", "test_file_path", "expected_mime_type"]):
                self.fail(f"Invalid test case format in '{category_name}': {test_case}. Missing required keys.")

            with self.subTest(msg=test_case["name"]):
                file_path_from_json = test_case["test_file_path"]
                full_filepath = os.path.join(current_script_dir, file_path_from_json)

                self.assertTrue(os.path.exists(full_filepath),
                                f"Test file not found: {full_filepath} for test '{test_case['name']}'")

                start_time = time.perf_counter()
                detected_result_object = _detect_file(full_filepath)
                end_time = time.perf_counter()
                execution_time = end_time - start_time

                expected_mime = test_case["expected_mime_type"]

                print(f'\n--- Running Test: {test_case["name"]} ---')
                print(f"Test File: {full_filepath}")
                print(f"Expected MIME type: {expected_mime}")
                print(f"Actual MIME extracted from Result: {detected_result_object.candidates[0].media_type}")
                print(f"Execution Time: {execution_time:.4f} seconds")

                try:
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
                    actual_mime_from_result = detected_result_object.candidates[0].media_type

                    self.assertEqual(actual_mime_from_result, expected_mime,
                                     f"Failed for {full_filepath} ('{test_case['name']}'). Expected '{expected_mime}', got '{actual_mime_from_result}' from Result object.")

                    # If all assertions pass, increment successful tests
                    TestFileTypeDetection.successful_tests += 1

                except AssertionError as e:
                    # If an assertion fails, it will be caught here, and the test will be marked as a failure
                    # The unittest framework will report the failure automatically
                    print(f"Test failed: {e}")
                    # No need to re-raise, unittest handles the failure via self.subTest context
                except Exception as e:
                    print(f"An unexpected error occurred during test execution: {e}")
                    # Mark as failed for success rate purposes if an unexpected error occurs
                    # This might already be handled by unittest, but good for explicit tracking
                    # Note: unittest.TestCase.fail() would explicitly mark it as failed
                    pass # Allow unittest to handle the failure normally

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
    
    def test_jpg_file_tests(self):
        self._run_tests_for_category("jpg file tests")
    
    def test_doc_file_tests(self):
        self._run_tests_for_category("doc file tests")

    def test_xml_file_tests(self):
        self._run_tests_for_category("xml file tests")

    def test_html_file_tests(self):
        self._run_tests_for_category("html file tests")

    def test_gz_file_tests(self):
        self._run_tests_for_category("gz file tests")

    def test_ppt_file_tests(self):
        self._run_tests_for_category("ppt file tests")

    def test_ps_file_tests(self):
        self._run_tests_for_category("ps file tests")

    def test_gif_file_tests(self):
        self._run_tests_for_category("gif file tests")

    def test_ods_file_tests(self):
        self._run_tests_for_category("ods file tests")

    def test_excel_file_tests(self):
        self._run_tests_for_category("excel file tests")

    
if __name__ == '__main__':
    unittest.main()