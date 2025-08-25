#!/usr/bin/env python3
"""
Demo script for SAS Parser
Shows both raw Lark parse tree and final semantic AST
"""

from sas_parser import SASParser
from lark.tree import pydot__tree_to_png
import sys


def main():
    """Run demo with sample SAS code"""
    
    # Sample SAS code with core constructs
    sample_sas = """
    /* Sample DATA step */
    data work.output;
        set work.input (obs=100);
        
        /* Variable assignments */
        total = price * quantity;
        discounted_price = price * 0.9;
        
        /* Conditional logic */
        if total > 1000 then high_value = 1;
        
    run;
    
    /* Simple PROC step */
    proc print data=work.output;
    run;
    """
    
    print("=" * 60)
    print("SAS PARSER DEMO")
    print("=" * 60)
    
    print("\nOriginal SAS Code:")
    print("-" * 40)
    print(sample_sas.strip())
    
    # Initialize parser
    parser = SASParser()
    
    try:
        # Parse and get both tree and AST
        tree, ast = parser.parse_with_tree(sample_sas)
        
        print("\n\nLark Parse Tree:")
        print("-" * 40)
        print(tree.pretty())
        
        print("\n\nSemantic AST:")
        print("-" * 40)
        print(ast)
        
        print("\n\nAST Structure Analysis:")
        print("-" * 40)
        analyze_ast(ast)

    except Exception as e:
        print(f"\nParsing Error: {e}")
        sys.exit(1)


def analyze_ast(program):
    """Analyze and describe the AST structure"""
    print(f"Program contains {len(program.statements)} top-level statements:")
    
    for i, stmt in enumerate(program.statements, 1):
        stmt_type = type(stmt).__name__
        print(f"\n{i}. {stmt_type}:")
        
        if hasattr(stmt, 'output_dataset') and stmt.output_dataset:
            print(f"   Output: {stmt.output_dataset}")
            
        if hasattr(stmt, 'set_statement') and stmt.set_statement:
            print(f"   Input: {stmt.set_statement.dataset}")
            if stmt.set_statement.options:
                opts = ", ".join(str(opt) for opt in stmt.set_statement.options)
                print(f"   Options: {opts}")
                
        if hasattr(stmt, 'procedure'):
            print(f"   Procedure: {stmt.procedure}")
            if stmt.dataset:
                print(f"   Dataset: {stmt.dataset}")
                
        if hasattr(stmt, 'statements') and stmt.statements:
            print(f"   Contains {len(stmt.statements)} sub-statements:")
            for j, sub_stmt in enumerate(stmt.statements, 1):
                sub_type = type(sub_stmt).__name__
                print(f"     {j}. {sub_type}")


if __name__ == "__main__":
    main()