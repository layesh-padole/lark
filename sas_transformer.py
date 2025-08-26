"""
SAS AST Transformer
Transforms Lark parse tree into semantic AST
"""

from lark import Transformer, v_args
from typing import List, Optional, Any

from ast_nodes import (
    Program, DataStep, ProcStep, SetStatement, Assignment, IfStatement,
    Variable, DatasetRef, Literal, BinaryOperation, Condition, DatasetOption
)


class SASTransformer(Transformer):
    """Transforms Lark parse tree into semantic AST"""
    
    def program(self, statements):
        """Transform program root"""
        filtered_stmts = [s for s in statements if s is not None]
        return Program(statements=list(filtered_stmts))
    
    def statement(self, args):
        """Transform statement wrapper"""
        return args[0] if args else None
    
    def data_step(self, args):
        """Transform DATA step"""
        dataset = None
        set_stmt = None
        statements = []
        
        for arg in args:
            if isinstance(arg, DatasetRef):
                dataset = arg
            elif isinstance(arg, SetStatement):
                set_stmt = arg
            elif arg is not None:
                statements.append(arg)
                
        return DataStep(
            output_dataset=dataset,
            set_statement=set_stmt,
            statements=statements
        )
    
    def proc_step(self, args):
        """Transform PROC step"""
        proc_name = str(args[0])
        options = []
        statements = []
        dataset = None
        
        for arg in args[1:]:
            if isinstance(arg, DatasetOption):
                # Check if this is a data= option
                if arg.name.lower() == 'data':
                    dataset = arg.value
                else:
                    options.append(arg)
            elif isinstance(arg, list):  # proc_options
                for opt in arg:
                    if isinstance(opt, DatasetOption) and opt.name.lower() == 'data':
                        dataset = opt.value
                    else:
                        options.append(opt)
            elif arg is not None:
                statements.append(arg)
                
        return ProcStep(
            procedure=proc_name,
            dataset=dataset,
            options=options,
            statements=statements
        )
    
    def proc_options(self, options):
        """Transform PROC options"""
        return options
    
    def statement_body(self, args):
        """Transform statement body"""
        return args[0] if args else None
    
    def proc_body(self, args):
        """Transform PROC body"""
        return args[0] if args else None
    
    @v_args(inline=True)
    def set_statement(self, dataset, *options):
        """Transform SET statement"""
        filtered_opts = [opt for opt in options if isinstance(opt, DatasetOption)]
        return SetStatement(dataset=dataset, options=filtered_opts)
    
    @v_args(inline=True)
    def assignment(self, variable, expression):
        """Transform assignment statement"""
        return Assignment(variable=variable, expression=expression)
    
    @v_args(inline=True)
    def assignment_no_semicolon(self, variable, expression):
        """Transform assignment without semicolon"""
        return Assignment(variable=variable, expression=expression)
    
    @v_args(inline=True)
    def if_statement(self, condition, then_action):
        """Transform IF statement"""
        return IfStatement(condition=condition, then_statement=then_action)
    
    @v_args(inline=True)
    def then_action(self, action):
        """Transform THEN action"""
        return action
    
    def condition(self, args):
        """Transform condition"""
        if len(args) == 1:
            return Condition(expression=args[0])
        elif len(args) == 3:  # expression comparison_op expression
            comparison = BinaryOperation(left=args[0], operator=args[1], right=args[2])
            return Condition(expression=comparison)
        else:
            raise ValueError(f"Unexpected condition args: {args}")
    
    @v_args(inline=True)
    def variable(self, *parts):
        """Transform variable reference"""
        if len(parts) == 1:
            return Variable(name=str(parts[0]))
        else:
            # This is actually a dataset reference
            return DatasetRef(library=str(parts[0]), dataset=str(parts[1]))
    
    @v_args(inline=True)
    def dataset_ref(self, *parts):
        """Transform dataset reference"""
        if len(parts) == 1:
            return DatasetRef(library=None, dataset=str(parts[0]))
        else:
            return DatasetRef(library=str(parts[0]), dataset=str(parts[1]))
    
    @v_args(inline=True)
    def option(self, name, value):
        """Transform dataset option"""
        return DatasetOption(name=str(name), value=value)
    
    @v_args(inline=True)
    def option_value(self, value):
        """Transform option value"""
        return value
    
    def expression(self, args):
        """Transform expression"""
        if len(args) == 1:
            return args[0]
        elif len(args) == 3:  # left op right
            return BinaryOperation(left=args[0], operator=str(args[1]), right=args[2])
        else:
            raise ValueError(f"Unexpected expression args: {args}")
    
    def term(self, args):
        """Transform term (multiplication/division)"""
        if len(args) == 1:
            return args[0]
        elif len(args) == 3:  # left op right
            return BinaryOperation(left=args[0], operator=str(args[1]), right=args[2])
        else:
            raise ValueError(f"Unexpected term args: {args}")
    
    def factor(self, args):
        """Transform factor"""
        return args[0]
    
    def comparison_op(self, args):
        """Transform comparison operator"""
        return str(args[0])
    
    def IDENTIFIER(self, token):
        """Transform identifier token"""
        return str(token)
    
    def NUMBER(self, token):
        """Transform number token"""
        value = float(token) if '.' in str(token) else int(token)
        return Literal(value=value, data_type='number')
    
    def STRING(self, token):
        """Transform string token"""
        # Remove quotes
        value = str(token)[1:-1]  
        return Literal(value=value, data_type='string')
    
    def COMMENT(self, token):
        """Ignore comments for now"""
        return None
    
    def empty_statement(self, *args):
        """Ignore empty statements"""
        return None