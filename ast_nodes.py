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
    value: ASTNode
    
    def __str__(self) -> str:
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
class Program(ASTNode):
    """Represents the entire SAS program"""
    statements: List[ASTNode]
    
    def __str__(self) -> str:
        return "\n\n".join(str(stmt) for stmt in self.statements)