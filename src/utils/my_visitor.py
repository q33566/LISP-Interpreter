from utils.my_ast import *
from dataclasses import dataclass

class EvalError(Exception):
    pass

@dataclass
class Function:
    param_names: list[str]
    fun_body: 'FunBody'
    env: 'Env'

class Env:
    def __init__(self, parent: 'Env' = None):
        self.variables = {}
        self.parent = parent
    
    def get(self, var_name):
        if var_name in self.variables:
            return self.variables[var_name]
        elif self.parent:
            return self.parent.get(var_name)
        else:
            raise EvalError(f"Undefined variable '{var_name}'")
        
    def set(self, var_name, var_value):
        self.variables[var_name] = var_value
        
    def extend(self, new_vars:dict = None):
        if new_vars is None:
            new_vars = {}
        child_env = Env(parent=self)
        child_env.variables.update(new_vars)
        return child_env
        
class Visitor:
    def __init__(self):
        self.global_env: Env = Env()
        self.current_env: Env = self.global_env
        
    def push_env(self, new_vars):
        self.current_env = self.current_env.extend(new_vars=new_vars)
        
    def pop_env(self):
        if self.current_env.parent:
            self.current_env = self.current_env.parent
        else:
            raise EvalError("Cannot pop the global environment")
    
    def visit_program_node(self, node: Program):
        stmts: list[AstNode] = node.stmts
        result = None
        for stmt in stmts:
            result = stmt.accept(self)
        return result
    
    def visit_number_node(self, node: Number):
        return node.value
    
    def visit_boolean_node(self, node: Boolean):
        return node.value
    
    def visit_print_node(self, node: Print):
        exp = node.exp.accept(self)
        print_type = node.print_type
        if(print_type == 'PRINT_NUM'):
            print(int(exp))
        elif(print_type == 'PRINT_BOOL'):
            symbol = '#t' if exp else '#f'
            print(symbol)
    
    def visit_numop_node(self, node: NumOp):
        operator = node.operator
        operands = [operand.accept(self) for operand in node.operands]
        for operand in operands:
            if isinstance(operand, bool):
                raise EvalError('Type error!')
        if operator == '+':
            return self._add(operands)
        elif operator == '-':
            return self._sub(operands)
        elif operator == '*':
            return self._mut(operands)
        elif operator == '/':
            return self._divide(operands)
        elif operator == '%':
            return self._mod(operands)
        elif operator == '>':
            return self._greater_than(operands)
        elif operator == '<':
            return self._less_than(operands)
        elif operator == '=':
            return self._equal(operands)
        else:
            raise EvalError(f"Unknown operator '{operator}'")
    
    def visit_logicalop_node(self, node: LogicalOp):
        operator = node.operator
        if operator == 'and':
            operands: list[AstNode] = node.operands
            return self._and(operands=operands)
        elif operator == 'or':
            operands: list[AstNode] =  node.operands
            return self._or(operands=operands)
        elif operator == 'not':
            if len(node.operands) != 1:
                raise EvalError("'not' operator requires exactly one operand")
            operand: AstNode =  node.operands[0]
            return self._not(operand=operand)
        else:
            raise EvalError(f"Unknown logical operator '{operator}'")
    
    def visit_ifexp_node(self, node: IfExp):
        condition: AstNode = node.condition
        true_branch: AstNode = node.true_branch
        false_branch: AstNode = node.false_branch
        if(condition.accept(self)):
            return true_branch.accept(self)
        return false_branch.accept(self)
    
    def visit_variable_node(self, node: Variable):
        var_name = node.var_name
        return self.current_env.get(var_name=var_name)
    
    def visit_defstmt_node(self, node: DefStmt):
        var_name = node.variable_node.var_name
        var_value = node.value_node.accept(self)
        self.current_env.set(var_name=var_name, var_value=var_value)
    
    def visit_funexp_node(self, node: FunExp):
        param_names: list[str] = node.fun_ids_node.fun_ids
        fun_body: FunBody = node.fun_body_node
        env = self.current_env
        return Function(param_names=param_names, fun_body=fun_body, env=env)
    
    def visit_funcall_node(self, node: FunCall):
        fun: Function =  node.fun_node.accept(self)
        if not isinstance(fun, Function):
            raise EvalError(f"'{fun}' is not a function") 
        
        args: list = [param.accept(self) for param in node.params]
        if len(args) != len(node.params):
            raise EvalError(f"Function expected {len(fun.param_names)} arguments, got {len(args)}")
        new_vars: dict = dict(zip(fun.param_names, args))
        previous_env = self.current_env
        self.current_env = fun.env.extend(new_vars=new_vars)
        
        try:
            result = fun.fun_body.accept(self)
        finally:
            self.current_env = previous_env
        return result
        
    def visit_funbody_node(self, node: FunBody):
        result = None
        for body_node in node.fun_body:
            result = body_node.accept(self)
        return result
        
    def _add(self, operands):
        return sum(operands)
    
    def _sub(self, operands):
        if len(operands) == 1:
            return -operands[0]
        return operands[0] - operands[1]
    
    def _mut(self, operands):
        result = 1
        for op in operands:
            result *= op
        return result
    
    def _divide(self, operands):
        if len(operands) != 2:
            raise EvalError("Division requires exactly two operands")
        if operands[1] == 0:
            raise EvalError("Division by zero")
        return int(operands[0] / operands[1])
    
    def _mod(self, operands):
        if len(operands) != 2:
            raise EvalError("Modulus requires exactly two operands")
        return operands[0] % operands[1]
    
    def _greater_than(self, operands):
        if len(operands) != 2:
            raise EvalError("Greater-than operator requires exactly two operands")
        return operands[0] > operands[1]
    
    def _less_than(self, operands):
        if len(operands) != 2:
            raise EvalError("Less-than operator requires exactly two operands")
        return operands[0] < operands[1]
    
    def _equal(self, operands):
        if len(operands) < 2:
            raise EvalError("Equality operator requires at least two operands")
        first = operands[0]
        return all(op == first for op in operands[1:])
    
    def _and(self, operands):
        for operand in operands:
            result = operand.accept(self)
            if not result:
                return False
        return True
    
    def _or(self, operands):
        for operand in operands:
            result = operand.accept(self)
            if result:
                return True
        return False
    
    def _not(self, operand):
        return not operand.accept(self)