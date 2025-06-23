# main_harness.py
# Located at probium-x.x.x/main_harness.py

import sys
import os
import time

# --- Path Configuration for main_harness.py ---
# Get the absolute path of the current script's directory (e.g., probium-x.x.x)
project_root_dir = os.path.dirname(os.path.abspath(__file__))

# Add the 'probium' package root to sys.path
# This is crucial for importing probium.engines.*, probium.test_harness.*,
# and for engines to resolve their internal relative imports.
probium_package_dir = os.path.join(project_root_dir, 'probium')
if probium_package_dir not in sys.path:
    sys.path.insert(0, probium_package_dir)

# NO LONGER need to add test_harness_dir separately, as it's now part of probium_package_dir

# --- Diagnostic Check for test_harness __init__.py (New Location) ---
# This is crucial for Python to recognize 'probium.test_harness' as a subpackage.
print("\n--- Performing Test Harness Package Structure Check ---")
test_harness_dir = os.path.join(probium_package_dir, 'test_harness') # Path is now relative to probium_package_dir
test_harness_init_new_location = os.path.join(test_harness_dir, '__init__.py')

if not os.path.exists(test_harness_init_new_location):
    print(f"WARNING: Missing '{test_harness_init_new_location}'. The 'probium/test_harness' directory is not recognized as a Python subpackage.")
    print("ACTION: Please create an empty file named '__init__.py' inside the 'probium-x.x.x/probium/test_harness' directory.")
else:
    print(f"'{test_harness_init_new_location}' found.")
print("--- End of Test Harness Package Structure Check ---\n")


# Now, import the engine loading function from test_engine_call.py
# The import path now correctly reflects test_harness as a subpackage of 'probium'.
try:
    from probium.test_harness.test_engine_call import load_all_engines_for_harness
    print("Successfully imported load_all_engines_for_harness from probium.test_harness package.")
except ImportError as e:
    print(f"ERROR: Could not import load_all_engines_for_harness: {e}")
    print("Please ensure your directory structure is correct:")
    print(f"- {probium_package_dir}/test_harness/test_engine_call.py exists.")
    print(f"- All necessary __init__.py files are present (probium/__init__.py, probium/engines/__init__.py, probium/test_harness/__init__.py).")
    print(f"- Also ensure that test_engine_call.py itself has been updated to use 'probium' in its internal imports.")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: An unexpected error occurred during import: {e}")
    sys.exit(1)

# --- Load Engines ---
# Call the function from test_engine_call.py to load all engines
print("\n--- Initializing Engines via test_engine_call ---")
loaded_engines = load_all_engines_for_harness()

# Ensure EngineBase is loaded to check subclasses later
EngineBaseClass = None
if 'base' in loaded_engines:
    EngineBaseClass = getattr(loaded_engines['base'], 'EngineBase', None)
    if not EngineBaseClass:
        print("WARNING: 'base' module loaded but 'EngineBase' class not found within it. This might affect other engine tests.")
else:
    print("WARNING: 'base' engine module not loaded. Engines that subclass EngineBase cannot be properly identified/tested.")


def scan_file_with_engines(file_path: str, engines_to_use: dict, base_class: type):
    """
    Scans a single file's content using provided engines until a match is found.
    The 'fallback' engine is only used if no other engine provides a match.
    Returns the first successful result or None if no match.
    """
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
    except FileNotFoundError:
        print(f"  File not found: {file_path}")
        return None
    except Exception as e:
        print(f"  Error reading file {file_path}: {e}")
        return None

    file_size = len(file_content)
    print(f"  Scanning file: {os.path.basename(file_path)} (Size: {file_size} bytes)")

    # Separate fallback engine from others
    fallback_engine_module = engines_to_use.get('fallback')
    other_engines = {k: v for k, v in engines_to_use.items() if k != 'fallback' and k != 'base'}

    found_match = False
    result = None

    # First, try all engines except 'base' and 'fallback'
    for name, engine_module in other_engines.items():
        print(f"    Trying engine: {name} (primary)...")
        try:
            current_engine_class = None
            if base_class:
                for attr_name in dir(engine_module):
                    attr = getattr(engine_module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, base_class) and attr is not base_class:
                        current_engine_class = attr
                        break

            if current_engine_class:
                engine_instance = current_engine_class()
                if callable(engine_instance):
                    start_time = time.time()
                    scan_result = engine_instance(file_content) # Call the __call__ method
                    elapsed_time = (time.time() - start_time) * 1000 # Convert to milliseconds

                    print(f"      Result from {name}: {scan_result}")
                    if scan_result and hasattr(scan_result, 'candidates') and scan_result.candidates:
                        # Check if it's a specific match (not just a generic 'octet-stream' from a non-fallback engine)
                        if scan_result.candidates[0].media_type != 'application/octet-stream' or scan_result.candidates[0].confidence > 0.0:
                            print(f"    MATCH FOUND by {name} engine for {os.path.basename(file_path)}!")
                            print(f"    Detected type: {scan_result.candidates[0].media_type}")
                            print(f"    Elapsed: {elapsed_time:.2f} ms")
                            return scan_result # Return immediately on specific match
                        else:
                            print(f"      {name} returned generic octet-stream or low confidence. Continuing to next engine.")
                    else:
                        print(f"      No specific match from {name}.")
                else:
                    print(f"      Warning: {name} Engine instance ('{current_engine_class.__name__}') is not callable.")
            elif hasattr(engine_module, 'detect_content'): # Fallback for standalone functions
                start_time = time.time()
                scan_result = engine_module.detect_content(file_content)
                elapsed_time = (time.time() - start_time) * 1000 # Convert to milliseconds
                print(f"      Result from {name} (detect_content): {scan_result}")
                if scan_result and scan_result.get('type') and scan_result.get('type') != 'application/octet-stream': # Assuming standalone returns a dict with 'type'
                    print(f"    MATCH FOUND by {name} engine for {os.path.basename(file_path)} (standalone)!")
                    print(f"    Detected type: {scan_result.get('type')}")
                    print(f"    Elapsed: {elapsed_time:.2f} ms")
                    return scan_result
                else:
                    print(f"      No specific match from {name} (standalone).")
            else:
                print(f"      {name} module has no suitable EngineBase subclass or 'detect_content' function.")

        except Exception as e:
            print(f"    ERROR calling {name} engine: {e}")
            print(f"    Skipping {name} for this file.")
    
    # If no specific engine found a match, then try the fallback engine
    if fallback_engine_module:
        print(f"    No specific match found. Trying fallback engine...")
        name = 'fallback' # Explicitly set name for printing
        try:
            current_engine_class = None
            if base_class:
                for attr_name in dir(fallback_engine_module):
                    attr = getattr(fallback_engine_module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, base_class) and attr is not base_class:
                        current_engine_class = attr
                        break
            
            if current_engine_class:
                engine_instance = current_engine_class()
                if callable(engine_instance):
                    start_time = time.time()
                    result = engine_instance(file_content)
                    elapsed_time = (time.time() - start_time) * 1000

                    print(f"      Result from {name}: {result}")
                    if result and hasattr(result, 'candidates') and result.candidates:
                        print(f"    FALLBACK MATCH by {name} engine for {os.path.basename(file_path)}!")
                        print(f"    Detected type: {result.candidates[0].media_type}")
                        print(f"    Elapsed: {elapsed_time:.2f} ms")
                        return result
                    else:
                        print(f"      No match from {name}.")
                else:
                    print(f"      Warning: {name} Engine instance ('{current_engine_class.__name__}') is not callable.")
            elif hasattr(fallback_engine_module, 'detect_content'):
                start_time = time.time()
                result = fallback_engine_module.detect_content(file_content)
                elapsed_time = (time.time() - start_time) * 1000
                print(f"      Result from {name} (detect_content): {result}")
                if result and result.get('type'):
                    print(f"    FALLBACK MATCH by {name} engine for {os.path.basename(file_path)} (standalone)!")
                    print(f"    Detected type: {result.get('type')}")
                    print(f"    Elapsed: {elapsed_time:.2f} ms")
                    return result
                else:
                    print(f"      No match from {name} (standalone).")
            else:
                print(f"      {name} module has no suitable EngineBase subclass or 'detect_content' function.")

        except Exception as e:
            print(f"    ERROR calling {name} engine: {e}")
            print(f"    Skipping {name} for this file.")

    print(f"  No engine found a match for {os.path.basename(file_path)} (including fallback).")
    return None

def scan_all_files(directory_path: str, engines: dict, base_class: type):
    """Scans all files in a directory using the loaded engines."""
    print(f"\n--- Scanning all files in: {directory_path} ---")
    files_scanned = 0
    matches_found = 0
    
    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            files_scanned += 1
            print(f"\nScanning: {file_path}")
            result = scan_file_with_engines(file_path, engines, base_class)
            if result:
                matches_found += 1
            print("-" * 40) # Separator

    print(f"\nScan all complete: Scanned {files_scanned} files, found {matches_found} matches.")

def scan_one_file(directory_path: str, engines: dict, base_class: type):
    """Scans a single, user-specified file in a directory using the loaded engines."""
    print(f"\n--- Scanning one file in: {directory_path} ---")
    
    filename_to_scan = input("Enter the filename (e.g., 'document.pdf') to scan: ").strip()
    file_path = os.path.join(directory_path, filename_to_scan)

    if not os.path.exists(file_path):
        print(f"Error: File '{filename_to_scan}' not found in '{directory_path}'.")
        return

    print(f"\nScanning specific file: {file_path}")
    result = scan_file_with_engines(file_path, engines, base_class)
    if result:
        print(f"\nSuccessfully scanned and matched '{filename_to_scan}'.")
    else:
        print(f"\nNo match found for '{filename_to_scan}'.")
    print("-" * 40) # Separator


def main():
    if not loaded_engines:
        print("\nFATAL: No engines loaded. Cannot proceed with scanning.")
        sys.exit(1)

    print("\n--- Probium Test Harness ---")
    print("Available Engines:", ", ".join(loaded_engines.keys()))

    while True:
        target_directory = input("\nEnter the directory path to scan (e.g., /home/user/docs, or C:\\Users\\YourUser\\Documents\\TestFiles, or /mnt/c/Users/YourUser/Documents/TestFiles if in WSL). Type 'exit' to quit: ").strip()
        if target_directory.lower() == 'exit':
            break

        # DEBUG: Print the exact path string Python is checking
        print(f"DEBUG: Checking directory path: '{target_directory}'")

        if not os.path.isdir(target_directory):
            print(f"Error: Directory '{target_directory}' not found or is not a valid directory. Please try again.")
            continue

        while True:
            scan_option = input("Scan option: 'all' files or 'one' specific file? (or 'back' to choose directory again): ").strip().lower()

            if scan_option == 'all':
                scan_all_files(target_directory, loaded_engines, EngineBaseClass)
                break
            elif scan_option == 'one':
                scan_one_file(target_directory, loaded_engines, EngineBaseClass)
                break
            elif scan_option == 'back':
                break
            else:
                print("Invalid scan option. Please type 'all', 'one', or 'back'.")
        
        if scan_option != 'back':
            # Ask if user wants to scan another directory/file, or exit
            continue_harness = input("\nScan complete. Do you want to scan another directory/file? (yes/no): ").strip().lower()
            if continue_harness != 'yes':
                break

    print("\nExiting Probium Test Harness. Goodbye!")

if __name__ == "__main__":
    main()

