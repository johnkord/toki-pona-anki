#!/usr/bin/env python3
"""
Simple test to verify the cleanup scripts are syntactically correct and have basic functionality.
"""

import subprocess
import sys
import os

def test_python_script():
    """Test that the Python cleanup script is valid."""
    print("Testing Python cleanup script...")
    
    # Test syntax
    result = subprocess.run([sys.executable, "-m", "py_compile", "cleanup_releases.py"], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"✗ Python script syntax error: {result.stderr}")
        return False
    
    print("✓ Python script syntax is valid")
    
    # Test help/dry-run functionality by checking imports
    try:
        subprocess.run([sys.executable, "-c", "import cleanup_releases"], 
                      check=True, capture_output=True)
        print("✓ Python script imports successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Python script import error: {e}")
        return False
    
    return True

def test_shell_script():
    """Test that the shell cleanup script is valid."""
    print("\nTesting shell cleanup script...")
    
    # Test syntax
    result = subprocess.run(["bash", "-n", "cleanup_releases.sh"], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"✗ Shell script syntax error: {result.stderr}")
        return False
    
    print("✓ Shell script syntax is valid")
    return True

def test_workflow_syntax():
    """Test that the GitHub Actions workflow is valid YAML."""
    print("\nTesting GitHub Actions workflow...")
    
    try:
        import yaml
        with open(".github/workflows/release.yml", "r") as f:
            yaml.safe_load(f)
        print("✓ GitHub Actions workflow YAML is valid")
        return True
    except ImportError:
        print("⚠ PyYAML not available, skipping YAML validation")
        return True
    except Exception as e:
        print(f"✗ GitHub Actions workflow YAML error: {e}")
        return False

def main():
    """Run all tests."""
    print("Release Management Scripts Test")
    print("=" * 40)
    
    all_passed = True
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run tests
    all_passed &= test_python_script()
    all_passed &= test_shell_script()
    all_passed &= test_workflow_syntax()
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())