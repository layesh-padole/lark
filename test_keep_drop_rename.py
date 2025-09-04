#!/usr/bin/env python3
"""
Test KEEP, DROP, and RENAME statements and dataset options
"""

from sas_parser import SASParser

# Test cases for KEEP/DROP/RENAME
test_cases = [
    # Test 1: Basic KEEP statement
    {
        "name": "KEEP Statement",
        "code": """
        data output;
            set input;
            keep customer_id name revenue;
        run;
        """
    },
    
    # Test 2: Basic DROP statement
    {
        "name": "DROP Statement", 
        "code": """
        data output;
            set input;
            drop temp_var1 temp_var2;
        run;
        """
    },
    
    # Test 3: Basic RENAME statement
    {
        "name": "RENAME Statement",
        "code": """
        data output;
            set input;
            rename old_name=new_name old_id=new_id;
        run;
        """
    },
    
    # Test 4: KEEP as dataset option
    {
        "name": "KEEP Dataset Option",
        "code": """
        data output;
            set input(keep=customer_id name);
        run;
        """
    },
    
    # Test 5: Multiple statements combined
    {
        "name": "Combined KEEP/DROP/RENAME",
        "code": """
        data customers_clean;
            set raw_customers;
            where status = 'Active';
            customer_value = revenue - cost;
            keep customer_id name region customer_value profit_margin tier join_year;
            drop temp1 temp2;
            rename old_col=new_col;
        run;
        """
    }
]

def run_test(test_case):
    """Run a single test case"""
    print(f"\n=== Testing: {test_case['name']} ===")
    print(f"Code:\n{test_case['code'].strip()}")
    
    try:
        parser = SASParser()
        tree, ast = parser.parse_with_tree(test_case['code'])
        print("\n✓ Parse successful!")
        print(f"\nAST:\n{ast}")
        return True
    except Exception as e:
        print(f"\n✗ Parse failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing KEEP/DROP/RENAME functionality...")
    
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        if run_test(test_case):
            passed += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print(f"❌ {total - passed} tests failed")