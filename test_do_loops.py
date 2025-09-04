#!/usr/bin/env python3
"""
Test DO loop constructs
"""

from sas_parser import SASParser

# Test cases for DO loops
test_cases = [
    # Test 1: Simple DO block
    {
        "name": "Simple DO Block",
        "code": """
        data output;
            set input;
            do;
                x = x + 1;
                y = y * 2;
            end;
        run;
        """
    },
    
    # Test 2: DO WHILE loop
    {
        "name": "DO WHILE Loop",
        "code": """
        data output;
            set input;
            i = 1;
            do while (i <= 10);
                sum = sum + i;
                i = i + 1;
            end;
        run;
        """
    },
    
    # Test 3: DO UNTIL loop
    {
        "name": "DO UNTIL Loop",
        "code": """
        data output;
            set input;
            i = 1;
            do until (i > 10);
                sum = sum + i;
                i = i + 1;
            end;
        run;
        """
    },
    
    # Test 4: Iterative DO loop
    {
        "name": "Iterative DO Loop",
        "code": """
        data output;
            set input;
            do i = 1 to 10;
                sum = sum + i;
            end;
        run;
        """
    },
    
    # Test 5: Iterative DO loop with BY clause
    {
        "name": "Iterative DO Loop with BY",
        "code": """
        data output;
            set input;
            do i = 1 to 20 by 2;
                sum = sum + i;
            end;
        run;
        """
    },
    
    # Test 6: Nested DO loops
    {
        "name": "Nested DO Loops",
        "code": """
        data output;
            set input;
            do i = 1 to 5;
                do j = 1 to 3;
                    matrix = i * j;
                end;
            end;
        run;
        """
    },
    
    # Test 7: DO with IF (the failing test case from file_io)
    {
        "name": "DO with IF Statement",
        "code": """
        data output;
            set input;
            if age > 25 then do;
                qualified = 1;
                bonus = salary * 0.1;
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
    print("Testing DO loop functionality...")
    
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