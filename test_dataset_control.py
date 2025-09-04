#!/usr/bin/env python3
"""
Test OUTPUT, RETAIN, LENGTH, STOP, and DELETE statements
"""

from sas_parser import SASParser

# Test cases for dataset control statements
test_cases = [
    # Test 1: Basic OUTPUT statement
    {
        "name": "Basic OUTPUT Statement",
        "code": """
        data output;
            set input;
            if category = 'A' then output;
        run;
        """
    },
    
    # Test 2: OUTPUT to specific dataset
    {
        "name": "OUTPUT to Dataset",
        "code": """
        data output1 output2;
            set input;
            if category = 'A' then output output1;
            if category = 'B' then output output2;
        run;
        """
    },
    
    # Test 3: Basic RETAIN statement
    {
        "name": "Basic RETAIN Statement",
        "code": """
        data output;
            set input;
            retain total_sales;
            total_sales = total_sales + sales;
        run;
        """
    },
    
    # Test 4: RETAIN with initial values
    {
        "name": "RETAIN with Initial Values",
        "code": """
        data output;
            set input;
            retain counter 0 max_value 100;
            counter = counter + 1;
        run;
        """
    },
    
    # Test 5: LENGTH statement
    {
        "name": "LENGTH Statement",
        "code": """
        data output;
            length name 50 address 100;
            set input;
        run;
        """
    },
    
    # Test 6: Multiple LENGTH assignments
    {
        "name": "Multiple LENGTH Assignments",
        "code": """
        data output;
            length first_name last_name 30 phone 15;
            set input;
        run;
        """
    },
    
    # Test 7: STOP statement
    {
        "name": "STOP Statement",
        "code": """
        data output;
            set input;
            if _n_ >= 100 then stop;
            total = total + amount;
        run;
        """
    },
    
    # Test 8: DELETE statement
    {
        "name": "DELETE Statement",
        "code": """
        data output;
            set input;
            if status = 'INACTIVE' then delete;
            active_count = active_count + 1;
        run;
        """
    },
    
    # Test 9: Combined statements
    {
        "name": "Combined Dataset Control",
        "code": """
        data summary detail;
            length category 20;
            retain total_amount 0;
            set transactions;
            
            total_amount = total_amount + amount;
            
            if category = 'INVALID' then delete;
            
            if category = 'SUMMARY' then do;
                output summary;
                if total_amount > 10000 then stop;
            end;
            else output detail;
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
    print("Testing OUTPUT/RETAIN/LENGTH/STOP/DELETE functionality...")
    
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