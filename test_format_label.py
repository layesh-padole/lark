#!/usr/bin/env python3
"""
Test FORMAT, INFORMAT, and LABEL statements
"""

from sas_parser import SASParser

# Test cases for FORMAT/INFORMAT/LABEL statements
test_cases = [
    # Test 1: Basic FORMAT statement
    {
        "name": "Basic FORMAT Statement",
        "code": """
        data output;
            set input;
            format salary dollar12.2;
        run;
        """
    },
    
    # Test 2: FORMAT with multiple variables
    {
        "name": "FORMAT Multiple Variables",
        "code": """
        data output;
            set input;
            format salary bonus dollar12.2;
        run;
        """
    },
    
    # Test 3: FORMAT with multiple assignments
    {
        "name": "FORMAT Multiple Assignments",
        "code": """
        data output;
            set input;
            format salary bonus dollar12.2 date_var mmddyy10.;
        run;
        """
    },
    
    # Test 4: Basic INFORMAT statement
    {
        "name": "Basic INFORMAT Statement",
        "code": """
        data output;
            informat date_var mmddyy10.;
            input name date_var salary;
        run;
        """
    },
    
    # Test 5: INFORMAT with multiple variables
    {
        "name": "INFORMAT Multiple Variables",
        "code": """
        data output;
            informat start_date end_date mmddyy10.;
            input name start_date end_date salary;
        run;
        """
    },
    
    # Test 6: Basic LABEL statement
    {
        "name": "Basic LABEL Statement",
        "code": """
        data output;
            set input;
            label name = "Employee Name";
        run;
        """
    },
    
    # Test 7: LABEL with multiple assignments
    {
        "name": "LABEL Multiple Assignments",
        "code": """
        data output;
            set input;
            label name = "Employee Name" salary = "Annual Salary";
        run;
        """
    },
    
    # Test 8: Combined FORMAT/INFORMAT/LABEL
    {
        "name": "Combined FORMAT/INFORMAT/LABEL",
        "code": """
        data employees;
            informat hire_date mmddyy10.;
            input emp_id name $ hire_date salary;
            
            format salary dollar12.2 hire_date mmddyy10.;
            label emp_id = "Employee ID" 
                  name = "Employee Name"
                  hire_date = "Date of Hire"
                  salary = "Annual Salary";
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
    print("Testing FORMAT/INFORMAT/LABEL functionality...")
    
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