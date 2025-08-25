#!/usr/bin/env python3
"""
Test IF statement parsing specifically
"""

from lark import Lark
from pathlib import Path

# Test IF statement
if_sas = """
data test;
    if total > 1000 then high_value = 1;
run;
"""

print("Testing IF statement parsing:")
print(if_sas.strip())

try:
    grammar_path = Path(__file__).parent / "sas_grammar.lark"
    with open(grammar_path, 'r') as f:
        grammar = f.read()
    
    parser = Lark(grammar, parser='lalr')
    tree = parser.parse(if_sas)
    print("\nRaw parse tree:")
    print(tree.pretty())
except Exception as e:
    import traceback
    print(f"\nError: {e}")
    traceback.print_exc()