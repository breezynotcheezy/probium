# test_engine_call.py
# Located at probium-x.x.x/probium/engines/test_harness/test_engine_call.py

import sys
import os
import importlib # Required for dynamic module loading

# --- Path Configuration ---
# Get the absolute path of the current script's directory.
# This script is now at probium-x.x.x/probium/engines/test_harness
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up to the 'engines' directory (parent of test_harness)
engines_dir = os.path.dirname(current_script_dir)

# Navigate up two more levels to the 'probium-x.x.x' project root.
# This is typically where main_harness.py would reside.
project_root_dir = os.path.dirname(os.path.dirname(engines_dir))

# The actual 'probium' package directory itself (e.g., probium-x.x.x/probium)
probium_package_dir = os.path.join(project_root_dir, 'probium')


# Add the 'probium' package root to Python's system path.
# This is crucial for Python to correctly resolve imports like probium.types or probium.engines.base
if probium_package_dir not in sys.path:
    sys.path.insert(0, probium_package_dir) # Insert at the beginning to prioritize

def load_all_engines_for_harness():
    """
    Performs package structure diagnostics and attempts to load all engine modules
    found dynamically within the probium/engines directory.
    Returns a dictionary of successfully loaded engine modules.
    """
    # --- Diagnostic Check for __init__.py and core modules ---
    print("\n--- Performing Package Structure and Core Dependency Check (from test_engine_call) ---")
    
    # Path to the probium package's __init__.py
    probium_init = os.path.join(probium_package_dir, '__init__.py')
    
    # Path to the probium/engines package's __init__.py
    engines_init = os.path.join(engines_dir, '__init__.py')

    # Path to the probium/types.py and probium/registry.py
    types_module_path = os.path.join(probium_package_dir, 'types.py')
    registry_module_path = os.path.join(probium_package_dir, 'registry.py')

    if not os.path.exists(probium_init):
        print(f"WARNING: Missing '{probium_init}'. The 'probium' directory might not be recognized as a Python package.")
        print("ACTION: Please create an empty file named '__init__.py' inside the 'probium' directory.")
    else:
        print(f"'{probium_init}' found.")

    if not os.path.exists(engines_init):
        print(f"WARNING: Missing '{engines_init}'. The 'probium.engines' directory might not be recognized as a Python subpackage.")
        print("ACTION: Please create an empty file named '__init__.py' inside the 'probium/engines' directory.")
    else:
        print(f"'{engines_init}' found.")

    # Attempt to import types and registry to catch syntax errors early within these core modules
    try:
        importlib.import_module('probium.types')
        print(f"Successfully imported 'probium.types'.")
    except Exception as e:
        print(f"ERROR: Failed to import 'probium.types': {e}. Please check for syntax errors in 'probium/types.py'.")

    try:
        importlib.import_module('probium.registry')
        print(f"Successfully imported 'probium.registry'.")
    except Exception as e:
        print(f"ERROR: Failed to import 'probium.registry': {e}. Please check for syntax errors in 'probium/registry.py'.")

    print("--- End of Package Structure and Core Dependency Check (from test_engine_call) ---\n")


    # --- Dynamic Engine Loading ---
    loaded_engines = {}
    
    print(f"Dynamically discovering and attempting to load engine modules from: {engines_dir}")

    # List all files in the engines directory
    for item in os.listdir(engines_dir):
        if item.endswith('.py') and item != '__init__.py':
            module_name = item[:-3] # Remove .py extension
            full_module_path = f"probium.engines.{module_name}"
            
            try:
                # Use importlib.import_module for a cleaner and more reliable dynamic import
                module = importlib.import_module(full_module_path)
                loaded_engines[module_name] = module # Store the module directly
                print(f"Successfully loaded engine module: {full_module_path}")
            except ImportError as e:
                print(f"ERROR: Could not load engine module '{full_module_path}': {e}.")
                print(f"  Check if '{module_name}.py' exists in '{engines_dir}', has no syntax errors,")
                print(f"  and verify all its internal imports (e.g., from ..types, from .base) are resolvable.")
            except Exception as e:
                print(f"ERROR: An unexpected error occurred while loading '{full_module_path}': {e}")
                print(f"  This might indicate a runtime error or a deeper issue within {module_name}.py.")

    return loaded_engines

# This block will only run if test_engine_call.py is executed directly.
if __name__ == "__main__":
    print("Running test_engine_call.py as a standalone script for engine loading diagnostics.")
    loaded_engines_standalone = load_all_engines_for_harness()
    print("\n--- Engine Loading Complete (Standalone Test) ---")
    if loaded_engines_standalone:
        print(f"{len(loaded_engines_standalone)} engine modules were successfully loaded:")
        for name in loaded_engines_standalone.keys():
            print(f"- {name}")
    else:
        print("No engine modules were successfully loaded.")
    print("\nStandalone script finished.")
