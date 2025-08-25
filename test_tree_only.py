#!/usr/bin/env python3
"""
Test just the parse tree without transformation
"""

from lark import Lark
from pathlib import Path

# Test with multiplication
expr_sas = """
data test;
    total = price * quantity;
run;
"""

print("Testing raw parse tree:")
print(expr_sas.strip())

try:
    grammar_path = Path(__file__).parent / "sas_grammar.lark"
    with open(grammar_path, 'r') as f:
        grammar = f.read()
    
    parser = Lark(grammar, parser='lalr')
    tree = parser.parse(expr_sas)
    print("\nRaw parse tree:")
    print(tree.pretty())
except Exception as e:
    import traceback
    print(f"\nError: {e}")
    traceback.print_exc()