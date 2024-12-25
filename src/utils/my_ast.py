from typing import TYPE_CHECKING, Union
from dataclasses import dataclass
if TYPE_CHECKING:
    from utils.my_visitor import Visitor

class AstNode:
    def accept(self, visitor: 'Visitor'):
        method_name = 'visit_' + self.__class__.__name__.lower() + '_node'
        visit = getattr(visitor, method_name)
        return visit(self)
    
@dataclass
class Program(AstNode):
    stmts: list[AstNode]

@dataclass        
class Number(AstNode):
    value: int
        
@dataclass        
class Boolean(AstNode):
    value: bool

@dataclass        
class Print(AstNode):
    exp: AstNode
    print_type: str

@dataclass
class NumOp(AstNode):
    operator: str
    operands: list[AstNode]

@dataclass
class LogicalOp(AstNode):
    operator: str
    operands: list[AstNode]

@dataclass        
class IfExp(AstNode):
    condition: AstNode
    true_branch: AstNode
    false_branch: AstNode

@dataclass        
class Variable(AstNode):
    var_name: str

@dataclass
class DefStmt(AstNode):
    variable_node: Variable
    value_node: AstNode

@dataclass
class FunExp(AstNode):
    fun_ids_node: 'FunIds'
    fun_body_node: 'FunBody'

@dataclass
class FunBody(AstNode):
    fun_body: list

@dataclass
class FunIds(AstNode):
    fun_ids: list

@dataclass
class FunCall(AstNode):
    fun_node: Union[Variable, FunExp]
    params: list[AstNode]