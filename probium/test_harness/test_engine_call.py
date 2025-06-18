import sys
import os
import importlib # Required for dynamic module loading

# --- Path Configuration ---
# Get the absolute path of the current script's directory.
# This script is now at fastbackfilter-1.3.2/fastbackfilter/engines/test_harness
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up to the 'engines' directory (parent of test_harness)
engines_dir = os.path.dirname(current_script_dir)

# Navigate up one more level to the 'fastbackfilter' directory.
# This is the root of your package and needs to be in sys.path for relative imports to work.
package_root_dir = os.path.dirname(engines_dir)

# Add the 'fastbackfilter' directory to Python's system path.
# This tells Python that 'fastbackfilter' is a package it can import from.
if package_root_dir not in sys.path:
    sys.path.insert(0, package_root_dir) # Insert at the beginning to prioritize

def load_all_engines_for_harness():
    """
    Performs package structure diagnostics and attempts to load all specified engine modules.
    Returns a dictionary of successfully loaded engine modules.
    """
    # --- Diagnostic Check for __init__.py and core modules ---
    print("\n--- Performing Package Structure and Core Dependency Check (from test_engine_call) ---")
    fastbackfilter_init = os.path.join(package_root_dir, '__init__.py')
    engines_init = os.path.join(engines_dir, '__init__.py')

    if not os.path.exists(fastbackfilter_init):
        print(f"WARNING: Missing '{fastbackfilter_init}'. The 'fastbackfilter' directory might not be recognized as a Python package.")
        print("ACTION: Please create an empty file named '__init__.py' inside the 'fastbackfilter' directory.")
    else:
        print(f"'{fastbackfilter_init}' found.")

    if not os.path.exists(engines_init):
        print(f"WARNING: Missing '{engines_init}'. The 'fastbackfilter.engines' directory might not be recognized as a Python subpackage.")
        print("ACTION: Please create an empty file named '__init__.py' inside the 'fastbackfilter/engines' directory.")
    else:
        print(f"'{engines_init}' found.")

    # Attempt to import types and registry to catch syntax errors early within these core modules
    try:
        importlib.import_module('fastbackfilter.types')
        print(f"Successfully imported 'fastbackfilter.types'.")
    except Exception as e:
        print(f"ERROR: Failed to import 'fastbackfilter.types': {e}. Please check for syntax errors in 'fastbackfilter/types.py'.")

    try:
        importlib.import_module('fastbackfilter.registry')
        print(f"Successfully imported 'fastbackfilter.registry'.")
    except Exception as e:
        print(f"ERROR: Failed to import 'fastbackfilter.registry': {e}. Please check for syntax errors in 'fastbackfilter/registry.py'.")

    print("--- End of Package Structure and Core Dependency Check (from test_engine_call) ---\n")


    # --- Engine Loading ---
    # Define a list of engine module names to attempt to load.
    engine_submodule_names = [
        "base", "bat", "csv", "exe", "fallback", "gzip", "html", "image",
        "json", "legacy_office", "mp3", "mp4", "pdf", "png", "sh", "tar",
        "text", "wav", "xml", "zip_office"
    ]

    # A dictionary to store successfully loaded engine modules
    loaded_engines = {}

    print(f"Attempting to load engine modules from package 'fastbackfilter.engines'.")

    for submodule_name in engine_submodule_names:
        # Construct the full package path for the module
        full_module_path = f"fastbackfilter.engines.{submodule_name}"
        try:
            # Use importlib.import_module for a cleaner and more reliable dynamic import
            module = importlib.import_module(full_module_path)
            loaded_engines[submodule_name] = module # Store the module directly
            print(f"Successfully loaded engine module: {full_module_path}")
        except ImportError as e:
            print(f"ERROR: Could not load engine module '{full_module_path}': {e}.")
            print(f"  Check if '{submodule_name}.py' exists in '{engines_dir}', has no syntax errors,")
            print(f"  and verify all its internal imports (e.g., from ..types, from .base) are resolvable.")
        except Exception as e:
            print(f"ERROR: An unexpected error occurred while loading '{full_module_path}': {e}")
            print(f"  This might indicate a runtime error or a deeper issue within {submodule_name}.py.")

    return loaded_engines

# This block will only run if test_engine_call.py is executed directly.
if __name__ == "__main__":
    print("Running test_engine_call.py as a standalone script for engine loading diagnostics.")
    loaded_engines_standalone = load_all_engines_for_harness()
    print("\n--- Engine Loading Complete (Standalone Test) ---")
    if loaded_engines_standalone:
        print(f"{len(loaded_engines_standalone)} engine modules were successfully loaded.")
    else:
        print("No engine modules were successfully loaded.")
    print("\nStandalone script finished.")
