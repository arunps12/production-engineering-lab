"""
Exercise 3.D.3 — Debugging Imports
Guide: docs/python-guide/03-debugging.md

Tasks:
1. Fix circular import issues
2. Understand import order and sys.path
3. Debug "ModuleNotFoundError" scenarios
"""

import sys

# TODO: Print the Python path to understand where imports come from
# print("Python path:")
# for p in sys.path:
#     print(f"  {p}")

# TODO: Check if a module is importable
def check_import(module_name):
    """Check if a module can be imported."""
    try:
        __import__(module_name)
        print(f"  ✓ {module_name} — available")
    except ImportError as e:
        print(f"  ✗ {module_name} — {e}")


# TODO: Test these imports
modules_to_check = [
    "json",           # Standard library
    "csv",            # Standard library
    "requests",       # Third-party (may not be installed)
    "numpy",          # Third-party (may not be installed)
    "nonexistent",    # Does not exist
]

print("Checking module availability:")
for mod in modules_to_check:
    check_import(mod)
