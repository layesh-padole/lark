"""
AST Node Classes for SAS Parser
Provides clean semantic representation for parsed SAS code
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any
from dataclasses import dataclass


class ASTNode(ABC):
    """Base class for all AST nodes"""
    
    @abstractmethod
    def __str__(self) -> str:
        pass


@dataclass
class DatasetRef(ASTNode):
    """Represents a dataset reference (e.g., work.data1, data1)"""
    library: Optional[str]
    dataset: str
    
    def __str__(self) -> str:
        if self.library:
            return f"{self.library}.{self.dataset}"
        return self.dataset


@dataclass
class Variable(ASTNode):
    """Represents a variable reference"""
    name: str
    
    def __str__(self) -> str:
        return self.name


@dataclass
class Literal(ASTNode):
    """Represents literal values (numbers, strings)"""
    value: Any
    data_type: str  # 'number' or 'string'
    
    def __str__(self) -> str:
        if self.data_type == 'string':
            return f'"{self.value}"'
        return str(self.value)


@dataclass
class BinaryOperation(ASTNode):
    """Represents binary operations (+, -, *, /, =, <, etc.)"""
    left: ASTNode
    operator: str
    right: ASTNode
    
    def __str__(self) -> str:
        return f"({self.left} {self.operator} {self.right})"


@dataclass
class Assignment(ASTNode):
    """Represents variable assignments (x = y + 1;)"""
    variable: Variable
    expression: ASTNode
    
    def __str__(self) -> str:
        return f"{self.variable} = {self.expression};"


@dataclass
class Condition(ASTNode):
    """Represents conditional expressions"""
    expression: ASTNode
    
    def __str__(self) -> str:
        return str(self.expression)


@dataclass
class IfStatement(ASTNode):
    """Represents IF...THEN statements"""
    condition: Condition
    then_statement: ASTNode
    
    def __str__(self) -> str:
        return f"IF {self.condition} THEN {self.then_statement}"


@dataclass
class DatasetOption(ASTNode):
    """Represents dataset options (e.g., obs=100)"""
    name: str
    value: Any  # Changed from ASTNode to Any to handle lists
    
    def __str__(self) -> str:
        if self.name.lower() == 'keep' or self.name.lower() == 'drop':
            if isinstance(self.value, list):
                vars_str = " ".join(str(var) for var in self.value)
                return f"{self.name}={vars_str}"
        elif self.name.lower() == 'rename':
            if isinstance(self.value, list):
                rename_strs = [f"{old_var}={new_var}" for old_var, new_var in self.value]
                return f"{self.name}=({' '.join(rename_strs)})"
        
        return f"{self.name}={self.value}"


@dataclass
class SetStatement(ASTNode):
    """Represents SET statements in DATA steps"""
    dataset: DatasetRef
    options: List[DatasetOption]
    
    def __str__(self) -> str:
        if self.options:
            opts = ", ".join(str(opt) for opt in self.options)
            return f"SET {self.dataset} ({opts});"
        return f"SET {self.dataset};"


@dataclass
class MergeStatement(ASTNode):
    """Represents MERGE statements in DATA steps"""
    datasets: List[DatasetRef]
    options: List[DatasetOption]
    
    def __str__(self) -> str:
        datasets_str = " ".join(str(ds) for ds in self.datasets)
        if self.options:
            opts = ", ".join(str(opt) for opt in self.options)
            return f"MERGE {datasets_str} ({opts});"
        return f"MERGE {datasets_str};"


@dataclass
class ByStatement(ASTNode):
    """Represents BY statements in DATA steps"""
    variables: List[Variable]
    
    def __str__(self) -> str:
        vars_str = " ".join(str(var) for var in self.variables)
        return f"BY {vars_str};"


@dataclass
class WhereClause(ASTNode):
    """Represents WHERE clauses in DATA steps"""
    condition: Condition
    
    def __str__(self) -> str:
        return f"WHERE {self.condition};"


@dataclass
class DataStep(ASTNode):
    """Represents DATA steps"""
    output_dataset: Optional[DatasetRef]
    set_statement: Optional[SetStatement]
    merge_statement: Optional[MergeStatement]
    by_statement: Optional[ByStatement]
    where_clause: Optional[WhereClause]
    statements: List[ASTNode]
    
    def __str__(self) -> str:
        lines = []
        if self.output_dataset:
            lines.append(f"DATA {self.output_dataset};")
        else:
            lines.append("DATA;")
            
        if self.set_statement:
            lines.append(f"  {self.set_statement}")
        if self.merge_statement:
            lines.append(f"  {self.merge_statement}")
        if self.by_statement:
            lines.append(f"  {self.by_statement}")
        if self.where_clause:
            lines.append(f"  {self.where_clause}")
            
        for stmt in self.statements:
            lines.append(f"  {stmt}")
            
        lines.append("RUN;")
        return "\n".join(lines)


@dataclass
class ProcStep(ASTNode):
    """Represents PROC steps"""
    procedure: str
    dataset: Optional[DatasetRef]
    options: List[DatasetOption]
    statements: List[ASTNode]
    
    def __str__(self) -> str:
        lines = []
        proc_line = f"PROC {self.procedure.upper()}"
        if self.dataset:
            proc_line += f" DATA={self.dataset}"
        if self.options:
            opts = " ".join(str(opt) for opt in self.options)
            proc_line += f" {opts}"
        proc_line += ";"
        lines.append(proc_line)
        
        for stmt in self.statements:
            lines.append(f"  {stmt}")
            
        lines.append("RUN;")
        return "\n".join(lines)


@dataclass
class KeepStatement(ASTNode):
    """Represents KEEP statements"""
    variables: List[Variable]
    
    def __str__(self) -> str:
        vars_str = " ".join(str(var) for var in self.variables)
        return f"KEEP {vars_str};"


@dataclass
class DropStatement(ASTNode):
    """Represents DROP statements"""
    variables: List[Variable]
    
    def __str__(self) -> str:
        vars_str = " ".join(str(var) for var in self.variables)
        return f"DROP {vars_str};"


@dataclass
class RenameStatement(ASTNode):
    """Represents RENAME statements"""
    renames: List[tuple[Variable, Variable]]  # List of (old_var, new_var) tuples
    
    def __str__(self) -> str:
        rename_strs = [f"{old_var}={new_var}" for old_var, new_var in self.renames]
        return f"RENAME {' '.join(rename_strs)};"


@dataclass
class InputStatement(ASTNode):
    """Represents INPUT statements"""
    variables: List[Variable]
    input_specs: Optional[List[str]] = None  # Format specifications like $10. or 8.2
    
    def __str__(self) -> str:
        if self.input_specs:
            var_specs = []
            for i, var in enumerate(self.variables):
                spec = self.input_specs[i] if i < len(self.input_specs) else ""
                var_specs.append(f"{var} {spec}".strip())
            return f"INPUT {' '.join(var_specs)};"
        else:
            vars_str = " ".join(str(var) for var in self.variables)
            return f"INPUT {vars_str};"


@dataclass
class PutStatement(ASTNode):
    """Represents PUT statements"""
    variables: List[Variable]
    output_specs: Optional[List[str]] = None  # Format specifications
    
    def __str__(self) -> str:
        if self.output_specs:
            var_specs = []
            for i, var in enumerate(self.variables):
                spec = self.output_specs[i] if i < len(self.output_specs) else ""
                var_specs.append(f"{var} {spec}".strip())
            return f"PUT {' '.join(var_specs)};"
        else:
            vars_str = " ".join(str(var) for var in self.variables)
            return f"PUT {vars_str};"


@dataclass
class InfileStatement(ASTNode):
    """Represents INFILE statements"""
    filename: str
    options: List[DatasetOption]
    
    def __str__(self) -> str:
        if self.options:
            opts = " ".join(str(opt) for opt in self.options)
            return f"INFILE {self.filename} {opts};"
        return f"INFILE {self.filename};"


@dataclass
class FileStatement(ASTNode):
    """Represents FILE statements"""
    filename: str
    options: List[DatasetOption]
    
    def __str__(self) -> str:
        if self.options:
            opts = " ".join(str(opt) for opt in self.options)
            return f"FILE {self.filename} {opts};"
        return f"FILE {self.filename};"


@dataclass
class FormatStatement(ASTNode):
    """Represents FORMAT statements"""
    format_assignments: List[tuple[List[Variable], str]]  # List of (variables, format) tuples
    
    def __str__(self) -> str:
        assignments = []
        for variables, format_spec in self.format_assignments:
            vars_str = " ".join(str(var) for var in variables)
            assignments.append(f"{vars_str} {format_spec}")
        return f"FORMAT {' '.join(assignments)};"


@dataclass
class InformatStatement(ASTNode):
    """Represents INFORMAT statements"""
    informat_assignments: List[tuple[List[Variable], str]]  # List of (variables, informat) tuples
    
    def __str__(self) -> str:
        assignments = []
        for variables, informat_spec in self.informat_assignments:
            vars_str = " ".join(str(var) for var in variables)
            assignments.append(f"{vars_str} {informat_spec}")
        return f"INFORMAT {' '.join(assignments)};"


@dataclass
class LabelStatement(ASTNode):
    """Represents LABEL statements"""
    label_assignments: List[tuple[Variable, str]]  # List of (variable, label) tuples
    
    def __str__(self) -> str:
        assignments = []
        for variable, label in self.label_assignments:
            assignments.append(f"{variable} = {label}")
        return f"LABEL {' '.join(assignments)};"


@dataclass
class DoBlock(ASTNode):
    """Represents simple DO-END blocks"""
    statements: List[ASTNode]
    
    def __str__(self) -> str:
        lines = ["DO;"]
        for stmt in self.statements:
            lines.append(f"  {stmt}")
        lines.append("END;")
        return "\n".join(lines)


@dataclass
class DoWhileLoop(ASTNode):
    """Represents DO WHILE loops"""
    condition: Condition
    statements: List[ASTNode]
    
    def __str__(self) -> str:
        lines = [f"DO WHILE ({self.condition});"]
        for stmt in self.statements:
            lines.append(f"  {stmt}")
        lines.append("END;")
        return "\n".join(lines)


@dataclass
class DoUntilLoop(ASTNode):
    """Represents DO UNTIL loops"""
    condition: Condition
    statements: List[ASTNode]
    
    def __str__(self) -> str:
        lines = [f"DO UNTIL ({self.condition});"]
        for stmt in self.statements:
            lines.append(f"  {stmt}")
        lines.append("END;")
        return "\n".join(lines)


@dataclass
class IterativeDoLoop(ASTNode):
    """Represents iterative DO loops (DO i=1 TO n)"""
    variable: Variable
    start_value: ASTNode
    end_value: ASTNode
    by_value: Optional[ASTNode] = None
    statements: List[ASTNode] = None
    
    def __str__(self) -> str:
        do_clause = f"DO {self.variable} = {self.start_value} TO {self.end_value}"
        if self.by_value:
            do_clause += f" BY {self.by_value}"
        do_clause += ";"
        
        lines = [do_clause]
        if self.statements:
            for stmt in self.statements:
                lines.append(f"  {stmt}")
        lines.append("END;")
        return "\n".join(lines)


@dataclass
class OutputStatement(ASTNode):
    """Represents OUTPUT statements"""
    dataset: Optional[DatasetRef] = None
    
    def __str__(self) -> str:
        if self.dataset:
            return f"OUTPUT {self.dataset};"
        return "OUTPUT;"


@dataclass
class RetainStatement(ASTNode):
    """Represents RETAIN statements"""
    variables: List[Variable]
    initial_values: Optional[List[ASTNode]] = None
    
    def __str__(self) -> str:
        if self.initial_values:
            retain_pairs = []
            for i, var in enumerate(self.variables):
                if i < len(self.initial_values) and self.initial_values[i] is not None:
                    retain_pairs.append(f"{var} {self.initial_values[i]}")
                else:
                    retain_pairs.append(str(var))
            return f"RETAIN {' '.join(retain_pairs)};"
        else:
            vars_str = " ".join(str(var) for var in self.variables)
            return f"RETAIN {vars_str};"


@dataclass
class LengthStatement(ASTNode):
    """Represents LENGTH statements"""
    length_assignments: List[tuple[List[Variable], ASTNode]]  # List of (variables, length) tuples
    
    def __str__(self) -> str:
        assignments = []
        for variables, length in self.length_assignments:
            vars_str = " ".join(str(var) for var in variables)
            assignments.append(f"{vars_str} {length}")
        return f"LENGTH {' '.join(assignments)};"


@dataclass
class StopStatement(ASTNode):
    """Represents STOP statements"""
    
    def __str__(self) -> str:
        return "STOP;"


@dataclass
class DeleteStatement(ASTNode):
    """Represents DELETE statements"""
    
    def __str__(self) -> str:
        return "DELETE;"


@dataclass
class Program(ASTNode):
    """Represents the entire SAS program"""
    statements: List[ASTNode]
    
    def __str__(self) -> str:
        return "\n\n".join(str(stmt) for stmt in self.statements)