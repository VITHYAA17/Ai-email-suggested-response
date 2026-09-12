"""
Direct Test Runner for running all unit tests without third-party runner dependencies.
"""

import sys
import traceback

def run():
    print("==================================================")
    print("RUNNING UNIT TESTS FOR AI EMAIL SUGGESTED RESPONSE")
    print("==================================================")
    
    test_modules = [
        "tests.test_dataset",
        "tests.test_retriever",
        "tests.test_generator",
        "tests.test_evaluator"
    ]
    
    total_passed = 0
    total_failed = 0
    
    for mod_name in test_modules:
        print(f"\n[Module: {mod_name}]")
        try:
            mod = __import__(mod_name, fromlist=["*"])
        except Exception as e:
            print(f"  ❌ FAILED to import {mod_name}: {e}")
            total_failed += 1
            continue
            
        test_funcs = [attr for attr in dir(mod) if attr.startswith("test_") and callable(getattr(mod, attr))]
        
        for func_name in test_funcs:
            func = getattr(mod, func_name)
            try:
                func()
                print(f"  ✅ PASS: {func_name}")
                total_passed += 1
            except Exception as e:
                print(f"  ❌ FAIL: {func_name} -> {e}")
                traceback.print_exc()
                total_failed += 1
                
    print("\n==================================================")
    print(f"TEST RESULTS: {total_passed} Passed, {total_failed} Failed")
    print("==================================================")
    
    if total_failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    run()
