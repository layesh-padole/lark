#!/usr/bin/env python3
"""
Test expression parsing specifically
"""

from sas_parser import SASParser

# Test with multiplication
expr_sas = """
data test;
    total = price * quantity;
run;
"""

print("Testing expression parsing:")
print(expr_sas.strip())

try:
    parser = SASParser()
    tree, ast = parser.parse_with_tree(expr_sas)
    print("\nSuccess! Parse tree:")
    print(tree.pretty())
    print("\nAST:")
    print(ast)
except Exception as e:
    import traceback
    print(f"\nError: {e}")
    traceback.print_exc()