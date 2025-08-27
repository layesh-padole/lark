#!/usr/bin/env python3
"""
Simple Data Lineage Demo
Demonstrates the enhanced SAS parser with lineage extraction
"""

from sas_parser import SASParser
from lineage_extractor import LineageExtractor, print_lineage_graph
import json


def main():
    """Demo of lineage extraction functionality"""
    
    # Sample SAS code with rich DATA step features
    sas_code = """
    data sales_summary;
        set raw.transactions;
        where region = 'APAC';
        
        profit = revenue - cost;
        margin_pct = profit / revenue * 100;
        
        if profit > 1000 then high_value = 1;
    run;
    
    data customer_analysis;
        merge customers accounts;
        by customer_id;
        where status = 'ACTIVE';
        
        total_value = account_balance + credit_limit;
    run;
    """
    
    print("Enhanced SAS Parser - Data Lineage Extraction")
    print("=" * 50)
    
    # Parse and extract lineage
    parser = SASParser()
    extractor = LineageExtractor()
    
    ast = parser.parse(sas_code)
    lineage = extractor.extract_lineage(ast)
    
    # Display results
    print("\nParsed SAS Code:")
    print("-" * 30)
    print(ast)
    
    print("\nExtracted Lineage Metadata:")
    print("-" * 30)
    print(json.dumps(lineage, indent=2))
    
    # Print visual lineage graph
    print_lineage_graph(lineage)


if __name__ == "__main__":
    main()