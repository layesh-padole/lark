"""
Lineage Extractor for SAS Parser
Extracts metadata from parsed DATA steps for data lineage analysis
"""

from typing import Dict, List, Set, Any
from ast_nodes import (
    Program, DataStep, SetStatement, MergeStatement, ByStatement, WhereClause,
    Assignment, IfStatement, Variable, DatasetRef, BinaryOperation, Condition
)


class LineageExtractor:
    """Extracts lineage metadata from SAS AST"""
    
    def extract_lineage(self, program: Program) -> Dict[str, Dict[str, Any]]:
        """
        Extract lineage metadata from a parsed SAS program
        
        Args:
            program: Parsed SAS Program AST
            
        Returns:
            Dictionary mapping dataset names to their metadata
        """
        lineage = {}
        
        for stmt in program.statements:
            if isinstance(stmt, DataStep):
                metadata = self._extract_data_step_metadata(stmt)
                if metadata and metadata.get('outputs'):
                    # Use the first output dataset as the key
                    dataset_name = metadata['outputs'][0]
                    lineage[dataset_name] = metadata
                    
        return lineage
    
    def _extract_data_step_metadata(self, data_step: DataStep) -> Dict[str, Any]:
        """Extract metadata from a single DATA step"""
        metadata = {
            "inputs": [],
            "outputs": [],
            "columns_created": [],
            "columns_used": set(),
            "filters": [],
            "keys": [],
            "operation": "data_step"
        }
        
        # Extract output dataset
        if data_step.output_dataset:
            metadata["outputs"].append(str(data_step.output_dataset))
        
        # Extract input datasets from SET statement
        if data_step.set_statement:
            metadata["inputs"].append(str(data_step.set_statement.dataset))
            # Add any variables from SET options to columns_used
            for option in data_step.set_statement.options:
                self._extract_variables_from_node(option.value, metadata["columns_used"])
        
        # Extract input datasets from MERGE statement
        if data_step.merge_statement:
            for dataset in data_step.merge_statement.datasets:
                metadata["inputs"].append(str(dataset))
            # Add any variables from MERGE options to columns_used
            for option in data_step.merge_statement.options:
                self._extract_variables_from_node(option.value, metadata["columns_used"])
        
        # Extract BY variables
        if data_step.by_statement:
            for var in data_step.by_statement.variables:
                key_var = str(var)
                metadata["keys"].append(key_var)
                metadata["columns_used"].add(key_var)
        
        # Extract WHERE clause
        if data_step.where_clause:
            filter_str = str(data_step.where_clause.condition)
            metadata["filters"].append(filter_str)
            self._extract_variables_from_node(data_step.where_clause.condition, metadata["columns_used"])
        
        # Process statements within the DATA step
        for stmt in data_step.statements:
            if isinstance(stmt, Assignment):
                # Column being created
                metadata["columns_created"].append(str(stmt.variable))
                # Variables used in the expression
                self._extract_variables_from_node(stmt.expression, metadata["columns_used"])
            elif isinstance(stmt, IfStatement):
                # Variables used in condition
                self._extract_variables_from_node(stmt.condition, metadata["columns_used"])
                # Variables used in then statement
                self._extract_variables_from_node(stmt.then_statement, metadata["columns_used"])
                # If the then statement is an assignment, track the created column
                if isinstance(stmt.then_statement, Assignment):
                    metadata["columns_created"].append(str(stmt.then_statement.variable))
        
        # Convert set to list for JSON serialization
        metadata["columns_used"] = sorted(list(metadata["columns_used"]))
        
        return metadata
    
    def _extract_variables_from_node(self, node: Any, variables: Set[str]) -> None:
        """Recursively extract variable names from an AST node"""
        if isinstance(node, Variable):
            variables.add(str(node))
        elif isinstance(node, BinaryOperation):
            self._extract_variables_from_node(node.left, variables)
            self._extract_variables_from_node(node.right, variables)
        elif isinstance(node, Condition):
            self._extract_variables_from_node(node.expression, variables)
        elif isinstance(node, Assignment):
            self._extract_variables_from_node(node.expression, variables)
        elif hasattr(node, '__dict__'):
            # For other AST nodes, check all attributes
            for attr_value in node.__dict__.values():
                if hasattr(attr_value, '__dict__') or isinstance(attr_value, (list, tuple)):
                    if isinstance(attr_value, (list, tuple)):
                        for item in attr_value:
                            self._extract_variables_from_node(item, variables)
                    else:
                        self._extract_variables_from_node(attr_value, variables)


def print_lineage_graph(lineage: Dict[str, Dict[str, Any]]) -> None:
    """
    Print a simple text representation of the data lineage graph
    
    Args:
        lineage: Lineage metadata dictionary
    """
    print("=" * 60)
    print("DATA LINEAGE GRAPH")
    print("=" * 60)
    
    if not lineage:
        print("No DATA steps found.")
        return
    
    for dataset_name, metadata in lineage.items():
        print(f"\n📊 Dataset: {dataset_name}")
        print(f"   Operation: {metadata['operation']}")
        
        if metadata['inputs']:
            inputs_str = ", ".join(metadata['inputs'])
            print(f"   📥 Inputs: {inputs_str}")
        
        if metadata['columns_created']:
            created_str = ", ".join(metadata['columns_created'])
            print(f"   ✨ Columns Created: {created_str}")
            
        if metadata['columns_used']:
            used_str = ", ".join(metadata['columns_used'])
            print(f"   🔧 Columns Used: {used_str}")
            
        if metadata['filters']:
            filters_str = "; ".join(metadata['filters'])
            print(f"   🔍 Filters: {filters_str}")
            
        if metadata['keys']:
            keys_str = ", ".join(metadata['keys'])
            print(f"   🔑 Keys: {keys_str}")
    
    print("\n" + "=" * 60)