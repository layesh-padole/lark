#!/usr/bin/env python3
"""
Demo script for SAS Parser
Shows parsing, AST generation, and data lineage extraction
"""

from sas_parser import SASParser
#from lineage_extractor import LineageExtractor, print_lineage_graph
import json
import sys


def main():
    """Run demo with sample SAS code"""
    backup_sas = """
    /* Basic DATA step with SET */
    data sales;
        set raw.transactions;
        where region = 'APAC';
        
        profit = revenue - cost;
        margin = profit / revenue * 100;
        
        if profit > 1000 then high_profit = 1;
    run;
    
    /* DATA step with MERGE */
    data customer_sales;
        merge customers accounts;
        by customer_id;
        where status = 'ACTIVE';
        
        total_value = account_balance + credit_limit;
    run;
    
    """
    # Enhanced sample SAS code with richer DATA step constructs
    sample_sas = """
    
    data length_example;
    length code $5;
    code = "ABC";
    run;



    """
    
    print("=" * 60)
    print("SAS PARSER DEMO")
    print("=" * 60)
    
    print("\nOriginal SAS Code:")
    print("-" * 40)
    print(sample_sas.strip())
    
    # Initialize parser and lineage extractor
    parser = SASParser()
    #extractor = LineageExtractor()
    
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
        
        # # Extract and display lineage metadata
        # print("\n\nData Lineage Extraction:")
        # print("-" * 40)
        # lineage = extractor.extract_lineage(ast)
        
        # # Print detailed metadata
        # print("\nDetailed Metadata (JSON):")
        # print(json.dumps(lineage, indent=2))
        
        # # Print lineage graph
        # print_lineage_graph(lineage)

    except Exception as e:
        print(f"\nParsing Error: {e}")
        import traceback
        traceback.print_exc()
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