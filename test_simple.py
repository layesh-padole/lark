#!/usr/bin/env python3
"""
Simple test with minimal SAS code to debug the parser
"""

from sas_parser import SASParser

# Very simple test case
simple_sas = """
data test;
    x = 1;
run;
"""

print("Testing with simple SAS code:")
print(simple_sas.strip())

try:
    parser = SASParser()
    tree, ast = parser.parse_with_tree(simple_sas)
    print("\nSuccess! Parse tree:")
    print(tree.pretty())
    print("\nAST:")
    print(ast)
except Exception as e:
    import traceback
    print(f"\nError: {e}")
    traceback.print_exc()