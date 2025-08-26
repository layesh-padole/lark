"""
SAS Parser Core
Main SAS Parser class using Lark
"""

import os
from pathlib import Path
from lark import Lark
from lark.tree import Tree
from typing import Optional

from ast_nodes import Program
from sas_transformer import SASTransformer


class SASParser:
    """Main SAS Parser class"""
    
    def __init__(self, grammar_path: Optional[str] = None):
        """Initialize parser with grammar"""
        if grammar_path is None:
            grammar_path = Path(__file__).parent / "sas_grammar.lark"
        
        with open(grammar_path, 'r') as f:
            grammar = f.read()
        
        self.parser = Lark(grammar, parser='lalr')
        self.transformer = SASTransformer()
    
    def parse(self, sas_code: str) -> Program:
        """
        Parse SAS code and return semantic AST
        
        Args:
            sas_code: Raw SAS code string
            
        Returns:
            Program AST node containing parsed statements
        """
        tree = self.parser.parse(sas_code)
        return self.transformer.transform(tree)
    
    def parse_with_tree(self, sas_code: str) -> tuple[Tree, Program]:
        """
        Parse SAS code and return both parse tree and AST
        
        Args:
            sas_code: Raw SAS code string
            
        Returns:
            Tuple of (Lark parse tree, Program AST)
        """
        tree = self.parser.parse(sas_code)
        ast = self.transformer.transform(tree)
        
        return tree, ast