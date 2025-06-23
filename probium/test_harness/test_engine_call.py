# test_engine_call.py
# Located at probium-x.x.x/probium/test_harness/test_engine_call.py

import sys
import os
import importlib.util # For dynamic loading from file path
import importlib.machinery # Potentially needed for source file loader

def load_all_engines_for_harness():
    """
    Dynamically discovers and loads all engine modules from the 'probium/engines' directory.
    This function focuses solely on the loading process, assuming the necessary package
    structure and internal imports (e.g., to 'probium.types' or 'probium.models')
    are correctly handled within each engine's own code.
    
    Returns:
        dict: A dictionary of successfully loaded engine modules, with module names as keys.
    """
    # --- Path Configuration ---
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # probium_package_dir is the parent of test_harness_dir (where this script resides)
    probium_package_dir = os.path.dirname(current_script_dir)
    
    # engines_dir is a sibling of test_harness_dir, both inside probium_package_dir
    engines_dir = os.path.join(probium_package_dir, 'engines')

    # Add the 'probium' package root to Python's system path.
    # This is CRITICAL for internal relative imports within engine files (e.g., from ..types, from ..models)
    # to resolve correctly when engines are loaded.
    if probium_package_dir not in sys.path:
        sys.path.insert(0, probium_package_dir)

    print(f"DEBUG: 'probium' package root added to sys.path: {probium_package_dir}")
    print(f"DEBUG: Engines directory to scan: {engines_dir}")

    # --- CRITICAL NEW DIAGNOSTIC: Attempt to import probium.models directly ---
    print("\n--- CRITICAL DIAGNOSTIC: Attempting to import 'probium.models' ---")
    models_file_path = os.path.join(probium_package_dir, 'models.py')
    print(f"DIAG: Expected 'probium/models.py' path: '{models_file_path}'")

    if not os.path.exists(models_file_path):
        print(f"ERROR: File '{models_file_path}' DOES NOT EXIST on disk.")
        print("ACTION: Ensure 'models.py' is correctly located inside your 'probium' package.")
        return {} # Cannot proceed without models.py

    print(f"DIAG: File '{models_file_path}' EXISTS on disk. Attempting to load its module spec and execute.")
    try:
        # First, try to find the module specification
        spec = importlib.util.find_spec('probium.models')
        if spec is None:
            print(f"ERROR: importlib.util.find_spec('probium.models') returned None.")
            print("  This means Python cannot find the 'models' module even with the 'probium' package root in sys.path.")
            print("  Possible reasons: incorrect `__init__.py` files, case sensitivity issues, or caching.")
            return {}

        # If spec is found, try to load and execute the module
        module = importlib.util.module_from_spec(spec)
        # Register the module in sys.modules so subsequent imports find it
        sys.modules[spec.name] = module
        # Execute the module's code
        spec.loader.exec_module(module)

        print(f"SUCCESS: Successfully loaded 'probium.models'. Module path: {module.__file__}")
        if hasattr(module, 'Result'):
            print(f"DIAG: 'Result' class found in 'probium.models'.")
        else:
            print(f"WARNING: 'Result' class NOT found in 'probium.models'. This may cause issues for 'base.py'.")

    except Exception as e:
        print(f"CRITICAL ERROR: Failed to load 'probium.models': {type(e).__name__}: {e}")
        print("  This means Python found 'models.py' but encountered an error while trying to execute its code.")
        print("  Common causes: Syntax errors *within* 'models.py', or missing dependencies *used by* 'models.py' (e.g., pydantic).")
        print("  Even if 'pydantic' is installed, ensure its version is compatible or check for other hidden issues in 'models.py'.")
        return {} # Return empty dict as engines won't work without models

    print("--- End of CRITICAL DIAGNOSTIC: probium.models ---\n")

    # --- Engine Loading ---
    loaded_engines = {}
    
    if not os.path.isdir(engines_dir):
        print(f"ERROR: Engines directory not found: {engines_dir}")
        print("Please ensure your directory structure is:")
        print("  probium-main/")
        print("  └── probium/")
        print("      ├── engines/  <-- This directory must exist and contain your engine files")
        print("      └── test_harness/ <-- This directory contains test_engine_call.py")
        return loaded_engines

    for item in os.listdir(engines_dir):
        if item.endswith('.py') and item != '__init__.py':
            module_name = item[:-3] # Remove .py extension
            engine_file_path = os.path.join(engines_dir, item)
            
            try:
                # Use importlib.util to load the module directly from its file path.
                # This explicitly loads each engine as 'probium.engines.module_name'.
                spec = importlib.util.spec_from_file_location(f"probium.engines.{module_name}", engine_file_path)
                if spec is None:
                    raise ImportError(f"Could not create module spec for {module_name} at {engine_file_path}")
                
                module = importlib.util.module_from_spec(spec)
                sys.modules[f"probium.engines.{module_name}"] = module # Register it in sys.modules
                spec.loader.exec_module(module) # Execute the module's code, triggering its internal imports

                loaded_engines[module_name] = module
                print(f"Successfully loaded engine: {module_name} from {engine_file_path}")
            except Exception as e:
                print(f"ERROR loading engine '{module_name}' from '{engine_file_path}': {e}")
                print(f"  This error indicates an issue within the engine's own code (e.g., syntax error, or failed internal import like 'from probium.types', 'from probium.models', or 'from .base').")
                print(f"  Please check the file: {engine_file_path}")
                
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
