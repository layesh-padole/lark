#!/usr/bin/env python3
"""
Test INPUT, PUT, INFILE, and FILE statements
"""

from sas_parser import SASParser

# Test cases for file I/O statements
test_cases = [
    # Test 1: Basic INPUT statement
    {
        "name": "Basic INPUT Statement",
        "code": """
        data output;
            input name age salary;
        run;
        """
    },
    
    # Test 2: INPUT with format specifications
    {
        "name": "INPUT with Format Specs",
        "code": """
        data output;
            input name $20 age 3 salary 8.2;
        run;
        """
    },
    
    # Test 3: Basic PUT statement
    {
        "name": "Basic PUT Statement",
        "code": """
        data output;
            set input;
            put name age salary;
        run;
        """
    },
    
    # Test 4: PUT with format specifications
    {
        "name": "PUT with Format Specs",
        "code": """
        data output;
            set input;
            put name $20 age 3 salary 8.2;
        run;
        """
    },
    
    # Test 5: INFILE statement
    {
        "name": "INFILE Statement",
        "code": """
        data output;
            infile "datafile.txt";
            input name age salary;
        run;
        """
    },
    
    # Test 6: INFILE with options
    {
        "name": "INFILE with Options",
        "code": """
        data output;
            infile myfile dlm=",";
            input name age salary;
        run;
        """
    },
    
    # Test 7: FILE statement
    {
        "name": "FILE Statement",
        "code": """
        data _null_;
            set input;
            file "output.txt";
            put name age salary;
        run;
        """
    },
    
    # Test 8: Combined file I/O
    {
        "name": "Combined File I/O",
        "code": """
        data output;
            infile "input.csv" dlm="," firstobs=2;
            input name $30 age 3 salary 8.2;
            
            if age > 25 then do;
                file "qualified.txt";
                put name $30 age 3 salary 8.2;
            end;
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
    print("Testing INPUT/PUT/INFILE/FILE functionality...")
    
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