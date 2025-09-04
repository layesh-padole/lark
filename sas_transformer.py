"""
SAS AST Transformer
Transforms Lark parse tree into semantic AST
"""

from lark import Transformer, v_args
from typing import List, Optional, Any

from ast_nodes import (
    Program, DataStep, ProcStep, SetStatement, MergeStatement, ByStatement, WhereClause,
    Assignment, IfStatement, Variable, DatasetRef, Literal, BinaryOperation, 
    Condition, DatasetOption, KeepStatement, DropStatement, RenameStatement,
    InputStatement, PutStatement, InfileStatement, FileStatement,
    FormatStatement, InformatStatement, LabelStatement,
    DoBlock, DoWhileLoop, DoUntilLoop, IterativeDoLoop,
    OutputStatement, RetainStatement, LengthStatement, StopStatement, DeleteStatement
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
        datasets = []
        set_stmt = None
        merge_stmt = None
        by_stmt = None
        where_clause = None
        statements = []
        
        for arg in args:
            if isinstance(arg, DatasetRef):
                datasets.append(arg)
            elif isinstance(arg, SetStatement):
                set_stmt = arg
            elif isinstance(arg, MergeStatement):
                merge_stmt = arg
            elif isinstance(arg, ByStatement):
                by_stmt = arg
            elif isinstance(arg, WhereClause):
                where_clause = arg
            elif isinstance(arg, (KeepStatement, DropStatement, RenameStatement, 
                                   InputStatement, PutStatement, InfileStatement, FileStatement,
                                   FormatStatement, InformatStatement, LabelStatement,
                                   DoBlock, DoWhileLoop, DoUntilLoop, IterativeDoLoop,
                                   OutputStatement, RetainStatement, LengthStatement, 
                                   StopStatement, DeleteStatement)):
                statements.append(arg)
            elif arg is not None:
                statements.append(arg)
        
        # For now, just use the first dataset as the primary output dataset
        dataset = datasets[0] if datasets else None
                
        return DataStep(
            output_dataset=dataset,
            set_statement=set_stmt,
            merge_statement=merge_stmt,
            by_statement=by_stmt,
            where_clause=where_clause,
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
    
    def data_step_body(self, args):
        """Transform DATA step body element"""
        return args[0] if args else None
    
    def set_statement(self, args):
        """Transform SET statement"""
        dataset = args[0]
        options = []
        
        for arg in args[1:]:
            if isinstance(arg, list):  # dataset_options
                options.extend(opt for opt in arg if isinstance(opt, DatasetOption))
            elif isinstance(arg, DatasetOption):
                options.append(arg)
                
        return SetStatement(dataset=dataset, options=options)
    
    def merge_statement(self, args):
        """Transform MERGE statement"""
        datasets = []
        options = []
        
        for arg in args:
            if isinstance(arg, DatasetRef):
                datasets.append(arg)
            elif isinstance(arg, list):  # dataset_options
                options.extend(opt for opt in arg if isinstance(opt, DatasetOption))
                
        return MergeStatement(datasets=datasets, options=options)
    
    def by_statement(self, variables):
        """Transform BY statement"""
        return ByStatement(variables=variables)
    
    @v_args(inline=True)
    def where_clause(self, condition):
        """Transform WHERE clause"""
        return WhereClause(condition=condition)
    
    def keep_statement(self, variables):
        """Transform KEEP statement"""
        return KeepStatement(variables=variables)
    
    def drop_statement(self, variables):
        """Transform DROP statement"""
        return DropStatement(variables=variables)
    
    def rename_statement(self, rename_pairs):
        """Transform RENAME statement"""
        return RenameStatement(renames=rename_pairs)
    
    @v_args(inline=True)
    def rename_pair(self, old_var, new_var):
        """Transform rename pair (old=new)"""
        return (old_var, new_var)
    
    def input_statement(self, input_specs):
        """Transform INPUT statement"""
        variables = []
        format_specs = []
        
        for spec in input_specs:
            if isinstance(spec, tuple):  # (variable, format_spec)
                variables.append(spec[0])
                format_specs.append(spec[1] if spec[1] else "")
            else:  # just variable
                variables.append(spec)
                format_specs.append("")
        
        return InputStatement(variables=variables, input_specs=format_specs if any(format_specs) else None)
    
    def input_spec(self, args):
        """Transform input specification"""
        variable = args[0]
        format_spec = args[1] if len(args) > 1 else None
        return (variable, format_spec)
    
    def put_statement(self, put_specs):
        """Transform PUT statement"""
        variables = []
        format_specs = []
        
        for spec in put_specs:
            if isinstance(spec, tuple):  # (variable, format_spec)
                variables.append(spec[0])
                format_specs.append(spec[1] if spec[1] else "")
            else:  # just variable
                variables.append(spec)
                format_specs.append("")
        
        return PutStatement(variables=variables, output_specs=format_specs if any(format_specs) else None)
    
    def put_spec(self, args):
        """Transform put specification"""
        variable = args[0]
        format_spec = args[1] if len(args) > 1 else None
        return (variable, format_spec)
    
    def infile_statement(self, args):
        """Transform INFILE statement"""
        file_ref = args[0]
        options = []
        
        for arg in args[1:]:
            if isinstance(arg, list):  # file_options
                options.extend(opt for opt in arg if isinstance(opt, DatasetOption))
            elif isinstance(arg, DatasetOption):
                options.append(arg)
        
        return InfileStatement(filename=str(file_ref), options=options)
    
    def file_statement(self, args):
        """Transform FILE statement"""
        file_ref = args[0]
        options = []
        
        for arg in args[1:]:
            if isinstance(arg, list):  # file_options
                options.extend(opt for opt in arg if isinstance(opt, DatasetOption))
            elif isinstance(arg, DatasetOption):
                options.append(arg)
        
        return FileStatement(filename=str(file_ref), options=options)
    
    def file_ref(self, args):
        """Transform file reference"""
        return args[0]
    
    def file_options(self, options):
        """Transform file options"""
        return options
    
    def format_spec(self, args):
        """Transform format specification"""
        return str(args[0])
    
    def FORMAT_LITERAL(self, token):
        """Transform format literal token"""
        return str(token)
    
    def format_statement(self, format_assignments):
        """Transform FORMAT statement"""
        return FormatStatement(format_assignments=format_assignments)
    
    def format_assignment(self, args):
        """Transform format assignment (variables + format_spec)"""
        variables = args[:-1]  # All but the last argument are variables
        format_spec = args[-1]  # Last argument is the format specification
        return (variables, str(format_spec))
    
    def informat_statement(self, informat_assignments):
        """Transform INFORMAT statement"""
        return InformatStatement(informat_assignments=informat_assignments)
    
    def informat_assignment(self, args):
        """Transform informat assignment (variables + informat_spec)"""
        variables = args[:-1]  # All but the last argument are variables
        informat_spec = args[-1]  # Last argument is the informat specification
        return (variables, str(informat_spec))
    
    def label_statement(self, label_assignments):
        """Transform LABEL statement"""
        return LabelStatement(label_assignments=label_assignments)
    
    @v_args(inline=True)
    def label_assignment(self, variable, label_string):
        """Transform label assignment (variable = "label")"""
        # Extract the string value from the Literal object
        if isinstance(label_string, Literal):
            label_value = label_string.value
        else:
            label_value = str(label_string)
        return (variable, f'"{label_value}"')
    
    def do_block(self, args):
        """Transform DO block wrapper"""
        return args[0] if args else None
    
    def do_simple(self, statements):
        """Transform simple DO block"""
        filtered_stmts = [s for s in statements if s is not None]
        return DoBlock(statements=filtered_stmts)
    
    def do_while_loop(self, args):
        """Transform DO WHILE loop"""
        condition = args[0]
        statements = [s for s in args[1:] if s is not None]
        return DoWhileLoop(condition=condition, statements=statements)
    
    def do_until_loop(self, args):
        """Transform DO UNTIL loop"""
        condition = args[0]
        statements = [s for s in args[1:] if s is not None]
        return DoUntilLoop(condition=condition, statements=statements)
    
    def do_iterative_loop(self, args):
        """Transform iterative DO loop"""
        variable = args[0]
        start_value = args[1]
        end_value = args[2]
        
        by_value = None
        statements_start_idx = 3
        
        # Check if there's a BY clause
        if len(args) > 3 and not isinstance(args[3], (Assignment, IfStatement, KeepStatement, 
                                                     DropStatement, RenameStatement, InputStatement,
                                                     PutStatement, InfileStatement, FileStatement,
                                                     FormatStatement, InformatStatement, LabelStatement,
                                                     DoBlock, DoWhileLoop, DoUntilLoop, IterativeDoLoop)):
            by_value = args[3]
            statements_start_idx = 4
        
        statements = [s for s in args[statements_start_idx:] if s is not None]
        
        return IterativeDoLoop(
            variable=variable,
            start_value=start_value,
            end_value=end_value,
            by_value=by_value,
            statements=statements
        )
    
    def output_statement(self, args):
        """Transform OUTPUT statement"""
        dataset = args[0] if args else None
        return OutputStatement(dataset=dataset)
    
    def retain_statement(self, retain_specs):
        """Transform RETAIN statement"""
        variables = []
        initial_values = []
        
        for spec in retain_specs:
            if isinstance(spec, tuple):  # (variable, initial_value)
                variables.append(spec[0])
                initial_values.append(spec[1])
            else:  # just variable
                variables.append(spec)
                initial_values.append(None)
        
        # Only include initial_values if at least one is not None
        if any(val is not None for val in initial_values):
            return RetainStatement(variables=variables, initial_values=initial_values)
        else:
            return RetainStatement(variables=variables)
    
    def retain_spec(self, args):
        """Transform retain specification"""
        variable = args[0]
        initial_value = args[1] if len(args) > 1 else None
        return (variable, initial_value)
    
    def initial_value(self, args):
        """Transform initial value"""
        return args[0]
    
    def length_statement(self, length_assignments):
        """Transform LENGTH statement"""
        return LengthStatement(length_assignments=length_assignments)
    
    def length_assignment(self, args):
        """Transform length assignment (variables + length_spec)"""
        variables = args[:-1]  # All but the last argument are variables
        length_spec = args[-1]  # Last argument is the length specification
        return (variables, length_spec)
    
    def length_spec(self, args):
        """Transform length specification"""
        # Return the token value - could be NUMBER (Literal) or FORMAT_LITERAL (string)
        return args[0]
    
    def stop_statement(self, args):
        """Transform STOP statement"""
        return StopStatement()
    
    def delete_statement(self, args):
        """Transform DELETE statement"""
        return DeleteStatement()
    
    @v_args(inline=True)
    def assignment(self, variable, expression):
        """Transform assignment statement"""
        return Assignment(variable=variable, expression=expression)
    
    @v_args(inline=True)
    def assignment_no_semicolon(self, variable, expression):
        """Transform assignment without semicolon"""
        return Assignment(variable=variable, expression=expression)
    
    def if_statement(self, args):
        """Transform IF statement"""
        condition = args[0]
        then_action = args[1]
        return IfStatement(condition=condition, then_statement=then_action)
    
    @v_args(inline=True)
    def then_action_with_semicolon(self, action):
        """Transform THEN action with semicolon (like DO blocks)"""
        return action
    
    @v_args(inline=True)
    def then_action_no_semicolon(self, action):
        """Transform THEN action without semicolon"""
        return action
    
    def output_no_semicolon(self, args):
        """Transform OUTPUT without semicolon for IF-THEN"""
        dataset = args[0] if args else None
        return OutputStatement(dataset=dataset)
    
    def stop_no_semicolon(self, args):
        """Transform STOP without semicolon for IF-THEN"""
        return StopStatement()
    
    def delete_no_semicolon(self, args):
        """Transform DELETE without semicolon for IF-THEN"""
        return DeleteStatement()
    
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
    
    def dataset_options(self, options):
        """Transform dataset options"""
        return options
    
    def dataset_option(self, args):
        """Transform dataset option"""
        return args[0] if args else None
    
    def keep_option(self, args):
        """Transform KEEP dataset option"""
        # args[0] should be the variable_list  
        variables = args[0] if args else []
        return DatasetOption(name='keep', value=variables)
    
    def drop_option(self, args):
        """Transform DROP dataset option"""
        # args[0] should be the variable_list
        variables = args[0] if args else []
        return DatasetOption(name='drop', value=variables)
    
    def rename_option(self, args):
        """Transform RENAME dataset option"""
        # args[0] should be the list of rename_pairs
        rename_pairs = args[0] if args else []
        return DatasetOption(name='rename', value=rename_pairs)
    
    def variable_list(self, variables):
        """Transform variable list"""
        return variables
    
    def expression(self, args):
        """Transform expression"""
        if len(args) == 1:
            return args[0]
        elif len(args) == 3:  # left_expression operator term
            return BinaryOperation(left=args[0], operator=str(args[1]), right=args[2])
        else:
            raise ValueError(f"Unexpected expression args: {args}")
    
    def term(self, args):
        """Transform term (multiplication/division)"""
        if len(args) == 1:
            return args[0]
        elif len(args) == 3:  # factor operator factor
            return BinaryOperation(left=args[0], operator=str(args[1]), right=args[2])
        else:
            raise ValueError(f"Unexpected term args: {args}")
    
    def ADD(self, token):
        """Transform ADD token"""
        return "+"
    
    def SUB(self, token):
        """Transform SUB token"""
        return "-"
    
    def MUL(self, token):
        """Transform MUL token"""
        return "*"
        
    def DIV(self, token):
        """Transform DIV token"""
        return "/"
    
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